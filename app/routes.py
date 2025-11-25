from flask import Blueprint, render_template, request, jsonify, send_file, send_from_directory
import os
from pathlib import Path
from werkzeug.utils import secure_filename
from app.utils import allowed_file, create_output_folder, get_pdf_output_path, parse_time_points
from app.video_processor import get_video_info, extract_frames_at_times
from app.pdf_generator import create_pdf
from app.image_editor import adjust_quality
from app.file_scanner import scan_mp4_files, organize_files_by_folder
from config import UPLOAD_FOLDER, DEFAULT_IMAGE_QUALITY, DEFAULT_RESOLUTION, RESOLUTION_PRESETS, INPUT_FOLDER, OUTPUT_FOLDER

bp = Blueprint('v2p_formatter', __name__)

@bp.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    from flask import current_app
    base_dir = Path(current_app.config.get('BASE_DIR', Path(__file__).parent.parent))
    return send_from_directory(str(base_dir / 'static'), filename)

@bp.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@bp.route('/list_files', methods=['GET'])
def list_files():
    """List all MP4 files in the input directory"""
    from config import INPUT_FOLDER
    
    try:
        files = scan_mp4_files(str(INPUT_FOLDER))
        tree = organize_files_by_folder(files)
        
        return jsonify({
            'success': True,
            'files': files,
            'tree': tree,
            'count': len(files),
            'input_folder': str(INPUT_FOLDER),
            'output_folder': str(OUTPUT_FOLDER)
        })
    except Exception as e:
        import logging
        logging.error(f"Error scanning files: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to scan files: {str(e)}'
        }), 500

@bp.route('/test')
def test_upload():
    """Simple test page for upload"""
    with open('test_upload_simple.html', 'r') as f:
        return f.read()

@bp.route('/select_file', methods=['POST'])
def select_file():
    """Handle file selection (file already exists on server)"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        data = request.json
        file_path = data.get('file_path')
        
        if not file_path:
            return jsonify({'error': 'No file path provided'}), 400
        
        logger.info(f"📁 File selected: {file_path}")
        
        # Validate file exists and is within input folder
        file_path = os.path.abspath(file_path)
        input_path = os.path.abspath(str(INPUT_FOLDER))
        
        if not file_path.startswith(input_path):
            logger.error(f"❌ File path outside input folder: {file_path}")
            return jsonify({'error': 'File path must be within input folder'}), 403
        
        if not os.path.exists(file_path):
            logger.error(f"❌ File not found: {file_path}")
            return jsonify({'error': 'File not found'}), 404
        
        # Validate it's an MP4 file
        if not file_path.lower().endswith('.mp4'):
            return jsonify({'error': 'Invalid file type. Only MP4 files are allowed.'}), 400
        
        # Get video info
        logger.info("🎬 Extracting video info...")
        video_info = get_video_info(file_path)
        
        if not video_info:
            logger.error("❌ Failed to read video file")
            return jsonify({'error': 'Failed to read video file'}), 400
        
        logger.info(f"✅ Video info extracted: {video_info['duration']}s, {video_info['width']}x{video_info['height']}")
        
        response_data = {
            'success': True,
            'filename': os.path.basename(file_path),
            'filepath': file_path,
            'duration': round(video_info['duration'], 2),
            'width': video_info['width'],
            'height': video_info['height'],
            'fps': round(video_info['fps'], 2)
        }
        
        logger.info("✅ File selection successful")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"❌ File selection error: {str(e)}", exc_info=True)
        return jsonify({'error': f'File selection failed: {str(e)}'}), 500

@bp.route('/preview_frame', methods=['POST'])
def preview_frame():
    """Preview frame at specific time point"""
    data = request.json
    video_path = data.get('video_path')
    time_point = float(data.get('time_point', 0))
    
    if not video_path or not os.path.exists(video_path):
        return jsonify({'error': 'Video file not found'}), 400
    
    # Extract frame to temporary location
    from app.video_processor import extract_frame
    import tempfile
    
    temp_dir = Path(tempfile.gettempdir())
    temp_frame = temp_dir / f"preview_{int(time_point)}.jpg"
    
    if extract_frame(video_path, time_point, temp_frame, quality=85):
        return send_file(str(temp_frame), mimetype='image/jpeg')
    else:
        return jsonify({'error': 'Failed to extract frame'}), 400

@bp.route('/extract_frames', methods=['POST'])
def extract_frames():
    """Extract frames at specified time points"""
    data = request.json
    video_path = data.get('video_path')
    time_input = data.get('time_points', '')
    quality = int(data.get('quality', DEFAULT_IMAGE_QUALITY))
    resolution = data.get('resolution', DEFAULT_RESOLUTION)
    
    if not video_path or not os.path.exists(video_path):
        return jsonify({'error': 'Video file not found'}), 400
    
    # Handle both array and string formats
    if isinstance(time_input, list):
        # Direct array of numbers
        time_points = [float(t) for t in time_input]
    elif isinstance(time_input, (int, float)):
        # Single number
        time_points = [float(time_input)]
    else:
        # String format - parse it
        time_points = parse_time_points(str(time_input))
        if not time_points:
            return jsonify({'error': 'Invalid time points format. Expected array of numbers or comma-separated string.'}), 400
    
    # Get video info to validate time points
    video_info = get_video_info(video_path)
    if not video_info:
        return jsonify({'error': 'Failed to read video file'}), 400
    
    # Validate time points are within duration (allow small floating point tolerance)
    max_time = video_info['duration']
    tolerance = 0.1  # Allow 0.1 second tolerance for floating point precision
    invalid_times = [t for t in time_points if t < -tolerance or t > (max_time + tolerance)]
    if invalid_times:
        # Clamp invalid times to valid range instead of erroring
        import logging
        logging.warning(f"Time points outside video duration, clamping: {invalid_times}")
        time_points = [max(0, min(t, max_time - 0.01)) for t in time_points]
        # Remove duplicates and sort
        time_points = sorted(list(set(time_points)))
    
    # Get resolution
    resolution_tuple = RESOLUTION_PRESETS.get(resolution)
    
    # Create output folder in output directory
    output_dir = create_output_folder(video_path)
    
    # Extract frames
    try:
        extracted_images = extract_frames_at_times(
            video_path, time_points, output_dir, quality, resolution_tuple
        )
        
        return jsonify({
            'success': True,
            'images': extracted_images,
            'count': len(extracted_images),
            'output_dir': str(output_dir)
        })
    except Exception as e:
        return jsonify({'error': f'Failed to extract frames: {str(e)}'}), 500

@bp.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    """Generate PDF from extracted images"""
    data = request.json
    video_path = data.get('video_path')
    image_paths = data.get('image_paths', [])
    layout = data.get('layout', 'grid')
    images_per_page = int(data.get('images_per_page', 4))
    
    if not video_path:
        return jsonify({'error': 'Video path not provided'}), 400
    
    if not image_paths:
        return jsonify({'error': 'No images provided'}), 400
    
    # Validate image paths exist
    missing_images = [img for img in image_paths if not os.path.exists(img)]
    if missing_images:
        return jsonify({'error': f'Images not found: {missing_images}'}), 400
    
    # Get PDF output path in output directory
    pdf_path = get_pdf_output_path(video_path)
    
    try:
        create_pdf(image_paths, pdf_path, layout, images_per_page)
        
        return jsonify({
            'success': True,
            'file_path': str(pdf_path),
            'pdf_path': str(pdf_path),  # Keep for backward compatibility
            'filename': pdf_path.name
        })
    except Exception as e:
        return jsonify({'error': f'Failed to generate PDF: {str(e)}'}), 500

@bp.route('/generate_docx', methods=['POST'])
def generate_docx():
    """Generate DOCX from extracted images"""
    data = request.json
    video_path = data.get('video_path')
    image_paths = data.get('image_paths', [])
    images_per_page = int(data.get('images_per_page', 1))
    
    if not video_path:
        return jsonify({'error': 'Video path not provided'}), 400
    
    if not image_paths:
        return jsonify({'error': 'No images provided'}), 400
    
    # Validate image paths exist
    missing_images = [img for img in image_paths if not os.path.exists(img)]
    if missing_images:
        return jsonify({'error': f'Images not found: {missing_images}'}), 400
    
    # Get DOCX output path in output directory
    from app.utils import get_docx_output_path
    docx_path = get_docx_output_path(video_path)
    
    try:
        from app.docx_generator import create_docx
        create_docx(image_paths, docx_path, images_per_page)
        
        return jsonify({
            'success': True,
            'file_path': str(docx_path),
            'filename': docx_path.name
        })
    except Exception as e:
        import logging
        logging.error(f"Error generating DOCX: {str(e)}", exc_info=True)
        return jsonify({'error': f'Failed to generate DOCX: {str(e)}'}), 500

@bp.route('/download')
def download_file():
    """Download generated file from output folder"""
    filepath = request.args.get('path')
    if not filepath:
        return jsonify({'error': 'No file path provided'}), 400
    
    # Security: validate path is within output directory
    filepath = os.path.abspath(filepath)
    output_path = os.path.abspath(str(OUTPUT_FOLDER))
    
    if not filepath.startswith(output_path):
        return jsonify({'error': 'Invalid file path - must be in output folder'}), 403
    
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@bp.route('/video_file')
def serve_video_file():
    """Serve video file for preview"""
    filepath = request.args.get('path')
    if not filepath:
        return jsonify({'error': 'No file path provided'}), 400
    
    # Security: validate path is within input directory
    filepath = os.path.abspath(filepath)
    input_path = os.path.abspath(str(INPUT_FOLDER))
    
    if not filepath.startswith(input_path):
        return jsonify({'error': 'Invalid file path'}), 403
    
    if os.path.exists(filepath) and os.path.isfile(filepath) and filepath.lower().endswith('.mp4'):
        return send_file(filepath, mimetype='video/mp4')
    return jsonify({'error': 'File not found'}), 404

