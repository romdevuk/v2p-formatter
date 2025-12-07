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
from app.observation_media_scanner import list_output_subfolders, scan_media_subfolder
from app.placeholder_parser import extract_placeholders, validate_placeholders, assign_placeholder_colors

bp = Blueprint('v2p_formatter', __name__)

@bp.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    from flask import current_app
    base_dir = Path(current_app.config.get('BASE_DIR', Path(__file__).parent.parent))
    return send_from_directory(str(base_dir / 'static'), filename)

@bp.route('/static/cache/<path:filename>')
def serve_cache(filename):
    """Serve cached files (thumbnails)"""
    from flask import current_app
    base_dir = Path(current_app.config.get('BASE_DIR', Path(__file__).parent.parent))
    return send_from_directory(str(base_dir / 'static' / 'cache'), filename)

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
    
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return send_file(filepath, mimetype='video/mp4')
    return jsonify({'error': 'File not found'}), 404

@bp.route('/thumbnail', methods=['GET'])
def get_video_thumbnail():
    """Generate and serve thumbnail for MP4 video files (main page)"""
    from app.utils import validate_input_path
    from app.thumbnail_generator import get_thumbnail, get_thumbnail_cache_path
    from pathlib import Path
    from flask import Response
    
    file_path = request.args.get('path')
    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400
    
    file_path_obj = Path(file_path)
    
    # Validate path is within INPUT_FOLDER
    is_valid, error_msg = validate_input_path(str(file_path_obj), INPUT_FOLDER)
    if not is_valid:
        return jsonify({'error': error_msg}), 403
    
    # Check if file exists
    if not file_path_obj.exists() or not file_path_obj.is_file():
        return jsonify({'error': 'File not found'}), 404
    
    # Check if it's an MP4 file
    ext = file_path_obj.suffix.lower()
    if ext != '.mp4':
        return jsonify({'error': 'Only MP4 files are supported'}), 400
    
    # Get size parameter (optional)
    size_str = request.args.get('size', '120x90')
    try:
        width, height = map(int, size_str.split('x'))
        size = (width, height)
    except:
        size = (120, 90)
    
    # Check if cache is stale
    cache_path = get_thumbnail_cache_path(file_path_obj, size)
    if cache_path.exists():
        try:
            file_mtime = file_path_obj.stat().st_mtime
            cache_mtime = cache_path.stat().st_mtime
            if file_mtime > cache_mtime:
                cache_path.unlink()
        except Exception:
            pass
    
    try:
        # Generate thumbnail (will use cache if valid, or create new)
        thumbnail_data = get_thumbnail(file_path_obj, 'mp4', size)
        
        return Response(
            thumbnail_data,
            mimetype='image/jpeg',
            headers={
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        )
    except Exception as e:
        import logging
        logging.error(f"Error generating thumbnail: {e}", exc_info=True)
        return jsonify({'error': f'Failed to generate thumbnail: {str(e)}'}), 500
    
    if os.path.exists(filepath) and os.path.isfile(filepath) and filepath.lower().endswith('.mp4'):
        return send_file(filepath, mimetype='video/mp4')
    return jsonify({'error': 'File not found'}), 404


# ============================================================================
# Media Converter Routes
# ============================================================================

@bp.route('/media-converter')
def media_converter():
    """Media converter main page"""
    return render_template('media_converter.html')


@bp.route('/observation-media')
def observation_media():
    """Observation Media standalone page"""
    # Get subfolders for Observation Media (API-free approach - pass data in template)
    subfolders = list_output_subfolders(OUTPUT_FOLDER)
    
    # Get selected subfolder from query parameter (for auto-selection after reload)
    selected_subfolder = request.args.get('subfolder', '')
    
    # Get media for each subfolder (API-free - all data in template)
    # This re-scans ALL subfolders on every page load
    subfolder_media = {}
    for subfolder in subfolders:
        subfolder_media[subfolder] = scan_media_subfolder(OUTPUT_FOLDER, subfolder)
    
    return render_template('observation_media.html', 
                         observation_subfolders=subfolders,
                         observation_subfolder_media=subfolder_media,
                         selected_subfolder=selected_subfolder)


@bp.route('/media-converter/list', methods=['GET'])
def list_media_files():
    """List all MOV, JPG, JPEG, and PNG files in input folder"""
    from config import MEDIA_CONVERTER_INPUT_FOLDER
    from app.media_file_scanner import scan_media_files, get_file_info
    from pathlib import Path
    
    try:
        result = scan_media_files(str(MEDIA_CONVERTER_INPUT_FOLDER))
        
        # Add file info (width, height, duration) to each file
        for video in result['videos']:
            file_info = get_file_info(Path(video['path']))
            video.update({
                'width': file_info.get('width', 0),
                'height': file_info.get('height', 0),
                'duration': file_info.get('duration', 0)
            })
        
        for image in result['images']:
            file_info = get_file_info(Path(image['path']))
            image.update({
                'width': file_info.get('width', 0),
                'height': file_info.get('height', 0)
            })
        
        return jsonify({
            'success': True,
            'videos': result['videos'],
            'images': result['images'],
            'video_count': len(result['videos']),
            'image_count': len(result['images']),
            'input_folder': str(MEDIA_CONVERTER_INPUT_FOLDER),
            'output_folder': str(OUTPUT_FOLDER)
        })
    except Exception as e:
        import logging
        logging.error(f"Error scanning media files: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to scan files: {str(e)}'
        }), 500


@bp.route('/media-converter/convert', methods=['POST'])
def convert_media():
    """Start conversion job (asynchronous)"""
    from config import MEDIA_CONVERTER_INPUT_FOLDER, MEDIA_CONVERTER_OUTPUT_FOLDER
    from app.conversion_job import job_manager
    from app.utils import validate_input_path, get_media_output_path
    from pathlib import Path
    
    try:
        data = request.get_json()
        files = data.get('files', [])  # List of {type, path, ...}
        settings = data.get('settings', {})  # {video: {...}, image: {...}}
        
        if not files:
            return jsonify({
                'success': False,
                'error': 'No files selected for conversion'
            }), 400
        
        # Validate all file paths
        validated_files = []
        for file_info in files:
            file_path = file_info.get('path')
            if not file_path:
                continue
            
            is_valid, error_msg = validate_input_path(file_path, MEDIA_CONVERTER_INPUT_FOLDER)
            if not is_valid:
                return jsonify({
                    'success': False,
                    'error': f'Invalid file path: {error_msg}'
                }), 400
            
            validated_files.append(file_info)
        
        if not validated_files:
            return jsonify({
                'success': False,
                'error': 'No valid files to convert'
            }), 400
        
        # Create conversion job
        job_id = job_manager.create_job(validated_files, settings)
        job = job_manager.get_job(job_id)
        
        # Start conversion in background
        def converter_func(file_info, settings):
            """Converter function for job"""
            file_path = Path(file_info['path'])
            file_type = file_info.get('type', '')
            
            if file_type == 'mov':
                # Video conversion
                from app.video_converter import convert_mov_to_mp4
                video_settings = settings.get('video', {})
                quality_preset = video_settings.get('quality', 'medium')
                custom_settings = video_settings.get('custom')
                
                output_path = get_media_output_path(
                    file_path,
                    MEDIA_CONVERTER_OUTPUT_FOLDER,
                    '.mp4'
                )
                
                return convert_mov_to_mp4(file_path, output_path, quality_preset, custom_settings)
            
            elif file_type in ('jpg', 'jpeg', 'png'):
                # Image conversion
                from app.image_converter import convert_image_to_jpeg
                from config import IMAGE_RESOLUTION_PRESETS, IMAGE_QUALITY_PRESETS
                
                image_settings = settings.get('image', {})
                resolution_preset = image_settings.get('resolution', 'original')
                quality_preset = image_settings.get('quality', 'medium')
                maintain_aspect = image_settings.get('maintain_aspect', True)
                allow_stretch = image_settings.get('allow_stretch', False)
                
                # Get resolution
                resolution = None
                if resolution_preset != 'original':
                    resolution = IMAGE_RESOLUTION_PRESETS.get(resolution_preset)
                elif image_settings.get('custom_resolution'):
                    width = image_settings.get('custom_width', 1920)
                    height = image_settings.get('custom_height', 1080)
                    resolution = (width, height)
                
                # Get quality
                quality = IMAGE_QUALITY_PRESETS.get(quality_preset, 80)
                if image_settings.get('custom_quality'):
                    quality = image_settings.get('custom_quality_value', 80)
                
                # Determine output extension (keep original for JPG, use .jpeg for PNG)
                if file_type == 'png':
                    output_ext = '.jpeg'
                else:
                    output_ext = file_path.suffix  # Keep original extension
                
                output_path = get_media_output_path(
                    file_path,
                    MEDIA_CONVERTER_OUTPUT_FOLDER,
                    output_ext
                )
                
                return convert_image_to_jpeg(
                    file_path,
                    output_path,
                    resolution,
                    quality,
                    maintain_aspect,
                    allow_stretch
                )
            
            else:
                return {
                    'success': False,
                    'error': f'Unsupported file type: {file_type}'
                }
        
        job.start(converter_func)
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': f'Conversion job started with {len(validated_files)} file(s)'
        })
    
    except Exception as e:
        import logging
        logging.error(f"Error starting conversion: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to start conversion: {str(e)}'
        }), 500


@bp.route('/media-converter/status/<job_id>', methods=['GET'])
def conversion_status(job_id):
    """Get conversion job status"""
    from app.conversion_job import job_manager
    
    job = job_manager.get_job(job_id)
    if not job:
        return jsonify({
            'success': False,
            'error': 'Job not found'
        }), 404
    
    status = job.get_status()
    return jsonify({
        'success': True,
        **status
    })


@bp.route('/media-converter/cancel/<job_id>', methods=['POST'])
def cancel_conversion(job_id):
    """Cancel running conversion job"""
    from app.conversion_job import job_manager
    
    success = job_manager.cancel_job(job_id)
    if success:
        return jsonify({
            'success': True,
            'message': 'Conversion cancelled'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Job not found or cannot be cancelled'
        }), 404


@bp.route('/media-converter/preview/<path:file_path>', methods=['GET'])
def preview_converted_file(file_path):
    """Serve converted file for preview"""
    from config import MEDIA_CONVERTER_OUTPUT_FOLDER
    from app.utils import validate_output_path
    from pathlib import Path
    
    file_path_obj = Path(file_path)
    
    # Validate path
    is_valid, error_msg = validate_output_path(str(file_path_obj), MEDIA_CONVERTER_OUTPUT_FOLDER)
    if not is_valid:
        return jsonify({'error': error_msg}), 403
    
    # Check if file exists
    if not file_path_obj.exists() or not file_path_obj.is_file():
        return jsonify({'error': 'File not found'}), 404
    
    # Determine MIME type
    ext = file_path_obj.suffix.lower()
    mime_types = {
        '.mp4': 'video/mp4',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png'
    }
    mimetype = mime_types.get(ext, 'application/octet-stream')
    
    return send_file(str(file_path_obj), mimetype=mimetype)

@bp.route('/media-converter/video-preview', methods=['GET'])
def preview_video_file():
    """Serve original video file for preview (from input folder)"""
    from config import MEDIA_CONVERTER_INPUT_FOLDER
    from app.utils import validate_input_path
    from pathlib import Path
    
    file_path = request.args.get('path')
    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400
    
    file_path_obj = Path(file_path)
    
    # Validate path is within input folder
    is_valid, error_msg = validate_input_path(str(file_path_obj), MEDIA_CONVERTER_INPUT_FOLDER)
    if not is_valid:
        return jsonify({'error': error_msg}), 403
    
    # Check if file exists
    if not file_path_obj.exists() or not file_path_obj.is_file():
        return jsonify({'error': 'File not found'}), 404
    
    # Check if it's a video file
    ext = file_path_obj.suffix.lower()
    if ext not in ('.mov', '.mp4'):
        return jsonify({'error': 'Only video files are supported'}), 400
    
    # Determine MIME type
    mime_types = {
        '.mov': 'video/quicktime',
        '.mp4': 'video/mp4'
    }
    mimetype = mime_types.get(ext, 'video/mp4')
    
    return send_file(str(file_path_obj), mimetype=mimetype)


@bp.route('/media-converter/download/<path:file_path>', methods=['GET'])
def download_converted_file(file_path):
    """Download converted file"""
    from config import MEDIA_CONVERTER_OUTPUT_FOLDER
    from app.utils import validate_output_path
    from pathlib import Path
    
    file_path_obj = Path(file_path)
    
    # Validate path
    is_valid, error_msg = validate_output_path(str(file_path_obj), MEDIA_CONVERTER_OUTPUT_FOLDER)
    if not is_valid:
        return jsonify({'error': error_msg}), 403
    
    # Check if file exists
    if not file_path_obj.exists() or not file_path_obj.is_file():
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(str(file_path_obj), as_attachment=True)


@bp.route('/media-converter/rotate-images', methods=['POST'])
def rotate_images():
    """Rotate selected images in place"""
    from config import MEDIA_CONVERTER_INPUT_FOLDER
    from app.utils import validate_input_path
    from app.image_rotator import rotate_image
    from pathlib import Path
    
    try:
        data = request.get_json()
        files = data.get('files', [])  # List of {path, type}
        angle = data.get('angle', 90)  # Rotation angle in degrees
        
        if not files:
            return jsonify({
                'success': False,
                'error': 'No files selected for rotation'
            }), 400
        
        # Validate angle
        if angle not in (-90, 90, 180, -180, 270, -270):
            return jsonify({
                'success': False,
                'error': 'Invalid rotation angle. Must be 90, -90, 180, or 270 degrees'
            }), 400
        
        # Validate all file paths
        validated_files = []
        for file_info in files:
            file_path = file_info.get('path')
            if not file_path:
                continue
            
            is_valid, error_msg = validate_input_path(file_path, MEDIA_CONVERTER_INPUT_FOLDER)
            if not is_valid:
                return jsonify({
                    'success': False,
                    'error': f'Invalid file path: {error_msg}'
                }), 400
            
            # Check if it's an image file
            file_type = file_info.get('type', '')
            if file_type not in ('jpg', 'jpeg', 'png'):
                continue
            
            validated_files.append(Path(file_path))
        
        if not validated_files:
            return jsonify({
                'success': False,
                'error': 'No valid image files to rotate'
            }), 400
        
        # Rotate each image
        results = []
        errors = []
        
        for file_path in validated_files:
            result = rotate_image(file_path, angle)
            if result.get('success'):
                results.append(result)
            else:
                errors.append({
                    'path': str(file_path),
                    'error': result.get('error', 'Unknown error')
                })
        
        # If any failed, return error (stop on failure as per requirements)
        if errors:
            return jsonify({
                'success': False,
                'error': f'Failed to rotate {len(errors)} file(s)',
                'errors': errors,
                'rotated_count': len(results)
            }), 500
        
        return jsonify({
            'success': True,
            'rotated_count': len(results),
            'message': f'Successfully rotated {len(results)} image(s)'
        })
    
    except Exception as e:
        import logging
        logging.error(f"Error rotating images: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to rotate images: {str(e)}'
        }), 500


@bp.route('/media-converter/trim-video', methods=['POST'])
def trim_video():
    """Trim video to specified time range"""
    from config import MEDIA_CONVERTER_INPUT_FOLDER, MEDIA_CONVERTER_OUTPUT_FOLDER
    from app.utils import validate_input_path, get_media_output_path
    from app.video_converter import trim_video as trim_video_func
    from pathlib import Path
    
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        start_time = float(data.get('start_time', 0))
        end_time = float(data.get('end_time', 0))
        quality_preset = data.get('quality', 'medium')
        custom_settings = data.get('custom_settings')
        
        if not file_path:
            return jsonify({
                'success': False,
                'error': 'No file path provided'
            }), 400
        
        # Validate path
        is_valid, error_msg = validate_input_path(file_path, MEDIA_CONVERTER_INPUT_FOLDER)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': f'Invalid file path: {error_msg}'
            }), 400
        
        file_path_obj = Path(file_path)
        
        # Check if it's a video file
        ext = file_path_obj.suffix.lower()
        if ext not in ('.mov', '.mp4'):
            return jsonify({
                'success': False,
                'error': 'Only video files (MOV/MP4) are supported'
            }), 400
        
        # Get output path
        output_path = get_media_output_path(
            file_path_obj,
            MEDIA_CONVERTER_OUTPUT_FOLDER,
            '.mp4'
        )
        
        # Trim video
        result = trim_video_func(
            file_path_obj,
            output_path,
            start_time,
            end_time,
            quality_preset,
            custom_settings
        )
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'output_path': result['output_path'],
                'output_size_mb': result['output_size_mb'],
                'trimmed_duration': result.get('trimmed_duration', 0),
                'message': f'Video trimmed successfully ({start_time}s - {end_time}s)'
            })
        else:
            # Return detailed error information
            error_response = {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'error_type': result.get('error_type', 'Unknown')
            }
            
            # Include FFmpeg error details if available
            if result.get('ffmpeg_stderr'):
                error_response['ffmpeg_stderr'] = result['ffmpeg_stderr']
            if result.get('ffmpeg_stdout'):
                error_response['ffmpeg_stdout'] = result['ffmpeg_stdout']
            if result.get('processing_time'):
                error_response['processing_time'] = result['processing_time']
            
            logger.error(f"Trim video failed: {error_response}")
            return jsonify(error_response), 500
    
    except Exception as e:
        import logging
        logging.error(f"Error trimming video: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to trim video: {str(e)}'
        }), 500


@bp.route('/media-converter/crop-video', methods=['POST'])
def crop_video():
    """Crop video to specified region"""
    from config import MEDIA_CONVERTER_INPUT_FOLDER, MEDIA_CONVERTER_OUTPUT_FOLDER
    from app.utils import validate_input_path, get_media_output_path
    from app.video_converter import crop_video as crop_video_func
    from pathlib import Path
    
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        x = int(data.get('x', 0))
        y = int(data.get('y', 0))
        width = int(data.get('width', 0))
        height = int(data.get('height', 0))
        quality_preset = data.get('quality', 'medium')
        custom_settings = data.get('custom_settings')
        
        if not file_path:
            return jsonify({
                'success': False,
                'error': 'No file path provided'
            }), 400
        
        # Validate path
        is_valid, error_msg = validate_input_path(file_path, MEDIA_CONVERTER_INPUT_FOLDER)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': f'Invalid file path: {error_msg}'
            }), 400
        
        file_path_obj = Path(file_path)
        
        # Check if it's a video file
        ext = file_path_obj.suffix.lower()
        if ext not in ('.mov', '.mp4'):
            return jsonify({
                'success': False,
                'error': 'Only video files (MOV/MP4) are supported'
            }), 400
        
        # Get output path
        output_path = get_media_output_path(
            file_path_obj,
            MEDIA_CONVERTER_OUTPUT_FOLDER,
            '.mp4'
        )
        
        # Crop video
        result = crop_video_func(
            file_path_obj,
            output_path,
            x,
            y,
            width,
            height,
            quality_preset,
            custom_settings
        )
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'output_path': result['output_path'],
                'output_size_mb': result['output_size_mb'],
                'crop_width': result.get('crop_width', width),
                'crop_height': result.get('crop_height', height),
                'message': f'Video cropped successfully ({width}x{height} @ {x},{y})'
            })
        else:
            # Return detailed error information
            error_response = {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'error_type': result.get('error_type', 'Unknown')
            }
            
            # Include FFmpeg error details if available
            if result.get('ffmpeg_stderr'):
                error_response['ffmpeg_stderr'] = result['ffmpeg_stderr']
            if result.get('ffmpeg_stdout'):
                error_response['ffmpeg_stdout'] = result['ffmpeg_stdout']
            if result.get('processing_time'):
                error_response['processing_time'] = result['processing_time']
            
            logger.error(f"Crop video failed: {error_response}")
            return jsonify(error_response), 500
    
    except Exception as e:
        import logging
        logging.error(f"Error cropping video: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to crop video: {str(e)}'
        }), 500


@bp.route('/media-converter/thumbnail', methods=['GET'])
def get_thumbnail():
    """Generate and serve thumbnail for a media file"""
    from config import MEDIA_CONVERTER_INPUT_FOLDER, OUTPUT_FOLDER
    from app.utils import validate_input_path
    from app.thumbnail_generator import get_thumbnail, get_thumbnail_cache_path
    from pathlib import Path
    from flask import Response
    
    file_path = request.args.get('path')
    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400
    
    file_path_obj = Path(file_path).resolve()
    
    # Validate path - check both MEDIA_CONVERTER_INPUT_FOLDER and OUTPUT_FOLDER
    # (Observation Media files are in OUTPUT_FOLDER)
    input_folder_obj = MEDIA_CONVERTER_INPUT_FOLDER.resolve()
    output_folder_obj = OUTPUT_FOLDER.resolve()
    
    # Check if path is within either folder
    is_valid = False
    try:
        file_path_obj.relative_to(input_folder_obj)
        is_valid = True
    except ValueError:
        try:
            file_path_obj.relative_to(output_folder_obj)
            is_valid = True
        except ValueError:
            pass
    
    if not is_valid:
        return jsonify({'error': 'File path must be within input or output folder'}), 403
    
    # Check if file exists
    if not file_path_obj.exists() or not file_path_obj.is_file():
        return jsonify({'error': 'File not found'}), 404
    
    # Determine file type
    ext = file_path_obj.suffix.lower()
    if ext == '.mov':
        file_type = 'mov'
    elif ext == '.mp4':
        file_type = 'mp4'
    elif ext in ('.jpg', '.jpeg'):
        file_type = 'jpg'
    elif ext == '.png':
        file_type = 'png'
    else:
        return jsonify({'error': 'Unsupported file type'}), 400
    
    # Get size parameter (optional)
    size_str = request.args.get('size', '120x90')
    try:
        width, height = map(int, size_str.split('x'))
        size = (width, height)
    except:
        size = (120, 90)
    
    # Check if cache is stale (file was modified after cache was created)
    cache_path = get_thumbnail_cache_path(file_path_obj, size)
    if cache_path.exists():
        try:
            file_mtime = file_path_obj.stat().st_mtime
            cache_mtime = cache_path.stat().st_mtime
            # If file was modified after cache was created, delete cache
            if file_mtime > cache_mtime:
                cache_path.unlink()
        except Exception:
            pass  # If we can't check, just regenerate
    
    try:
        # Generate thumbnail (will use cache if valid, or create new)
        thumbnail_data = get_thumbnail(file_path_obj, file_type, size)
        
        return Response(
            thumbnail_data,
            mimetype='image/jpeg',
            headers={
                'Cache-Control': 'no-cache, no-store, must-revalidate',  # Don't cache in browser
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        )
    except Exception as e:
        import logging
        logging.error(f"Error generating thumbnail: {e}", exc_info=True)
        return jsonify({'error': f'Failed to generate thumbnail: {str(e)}'}), 500




# ============================================================================
# Observation Media DOCX Export
# ============================================================================

@bp.route('/media-converter/observation-media/export-docx', methods=['POST'])
def export_observation_docx():
    """Export observation media document to DOCX"""
    try:
        data = request.get_json()
        text_content = data.get('text', '')
        assignments = data.get('assignments', {})
        filename = data.get('filename', 'observation_document.docx')
        font_size = data.get('font_size', 16)  # Default 16pt
        font_name = data.get('font_name', 'Times New Roman')  # Default Times New Roman
        
        # Sanitize filename first (before adding extension)
        import re
        filename = re.sub(r'[^\w\-_\.]', '_', filename)
        
        # Ensure filename has .docx extension
        if not filename.lower().endswith('.docx'):
            # Remove any existing extension before adding .docx
            filename = filename.rsplit('.', 1)[0] + '.docx'
        
        # Final sanitization to ensure no invalid characters remain
        filename = re.sub(r'[^\w\-_\.]', '_', filename)
        
        # Set output path
        output_path = OUTPUT_FOLDER / filename
        
        # Generate DOCX
        from app.observation_docx_generator import create_observation_docx
        result = create_observation_docx(text_content, assignments, output_path, font_size=font_size, font_name=font_name)
        
        if result['success']:
            return jsonify({
                'success': True,
                'file_path': result['file_path'],
                'file_name': result['file_name'],
                'download_url': f'/v2p-formatter/media-converter/observation-media/download-docx/{result["file_name"]}'
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error')
            }), 500
            
    except Exception as e:
        logger.error(f"Error exporting DOCX: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to export DOCX: {str(e)}'
        }), 500


@bp.route('/media-converter/observation-media/download-docx/<filename>', methods=['GET'])
def download_observation_docx(filename):
    """Download generated DOCX file"""
    try:
        # Security: validate filename
        import re
        if not re.match(r'^[\w\-_\.]+\.docx$', filename):
            return jsonify({'error': 'Invalid filename'}), 400
        
        file_path = OUTPUT_FOLDER / filename
        
        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            str(file_path),
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        logger.error(f"Error downloading DOCX: {e}", exc_info=True)
        return jsonify({
            'error': f'Failed to download file: {str(e)}'
        }), 500


# ============================================================================
# Observation Media Draft Management
# ============================================================================

@bp.route('/media-converter/observation-media/drafts', methods=['GET'])
def list_observation_drafts():
    """List all available drafts"""
    try:
        from app.draft_manager import list_drafts
        drafts = list_drafts()
        return jsonify({
            'success': True,
            'drafts': drafts
        })
    except Exception as e:
        logger.error(f"Error listing drafts: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to list drafts: {str(e)}'
        }), 500


@bp.route('/media-converter/observation-media/drafts', methods=['POST'])
def save_observation_draft():
    """Save a new draft"""
    try:
        from app.draft_manager import save_draft
        data = request.get_json()
        name = data.get('name', 'Untitled Draft')
        text_content = data.get('text_content', '')
        assignments = data.get('assignments', {})
        selected_subfolder = data.get('selected_subfolder')
        
        result = save_draft(name, text_content, assignments, selected_subfolder)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error saving draft: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to save draft: {str(e)}'
        }), 500


@bp.route('/media-converter/observation-media/drafts/<draft_id>', methods=['GET'])
def load_observation_draft(draft_id):
    """Load a draft"""
    try:
        from app.draft_manager import load_draft
        result = load_draft(draft_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 404
            
    except Exception as e:
        logger.error(f"Error loading draft: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to load draft: {str(e)}'
        }), 500


@bp.route('/media-converter/observation-media/drafts/<draft_id>', methods=['PUT'])
def update_observation_draft(draft_id):
    """Update an existing draft"""
    try:
        from app.draft_manager import update_draft
        data = request.get_json()
        text_content = data.get('text_content', '')
        assignments = data.get('assignments', {})
        selected_subfolder = data.get('selected_subfolder')
        
        result = update_draft(draft_id, text_content, assignments, selected_subfolder)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error updating draft: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to update draft: {str(e)}'
        }), 500


@bp.route('/media-converter/observation-media/drafts/<draft_id>', methods=['DELETE'])
def delete_observation_draft(draft_id):
    """Delete a draft"""
    try:
        from app.draft_manager import delete_draft
        result = delete_draft(draft_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 404
            
    except Exception as e:
        logger.error(f"Error deleting draft: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to delete draft: {str(e)}'
        }), 500


@bp.route('/media-converter/observation-media/rename-file', methods=['POST'])
def rename_observation_media_file():
    """Rename a media file (only the name part, not the extension)"""
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        new_name = data.get('new_name')
        
        if not file_path or not new_name:
            return jsonify({
                'success': False,
                'error': 'File path and new name are required'
            }), 400
        
        # Validate new name (no path separators, no extension)
        import re
        if not re.match(r'^[^/\\<>:"|?*\x00-\x1f]+$', new_name):
            return jsonify({
                'success': False,
                'error': 'Invalid file name. Name cannot contain path separators or special characters.'
            }), 400
        
        # Get file path
        file_path_obj = Path(file_path)
        
        if not file_path_obj.exists():
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        # Get original extension
        original_extension = file_path_obj.suffix
        
        # Create new path with new name but same extension
        new_path = file_path_obj.parent / f"{new_name}{original_extension}"
        
        # Check if new file already exists
        if new_path.exists() and new_path != file_path_obj:
            return jsonify({
                'success': False,
                'error': 'A file with this name already exists'
            }), 400
        
        # Rename the file
        file_path_obj.rename(new_path)
        
        # Return success with new path and name
        return jsonify({
            'success': True,
            'new_path': str(new_path),
            'new_name': new_path.name,
            'message': 'File renamed successfully'
        })
        
    except PermissionError:
        return jsonify({
            'success': False,
            'error': 'Permission denied. Cannot rename file.'
        }), 403
    except Exception as e:
        logger.error(f"Error renaming file: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to rename file: {str(e)}'
        }), 500
