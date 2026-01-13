from flask import Blueprint, render_template, request, jsonify, send_file, send_from_directory
import os
import logging
import json
import time
from pathlib import Path
from werkzeug.utils import secure_filename
from app.utils import allowed_file, create_output_folder, get_pdf_output_path, parse_time_points
from app.video_processor import get_video_info, extract_frames_at_times
from app.pdf_generator import create_pdf
from app.image_editor import adjust_quality
from app.file_scanner import scan_mp4_files, organize_files_by_folder
from app.image_scanner import scan_image_files, organize_images_by_folder
from app.image_pdf_generator import create_image_pdf
from app.image_docx_generator import create_image_docx
from app.deface_processor import deface_images, deface_video, apply_manual_deface, apply_manual_deface_to_video
from app.deface_session import (
    create_session, get_session, update_session_processed, 
    update_session_settings, add_manual_defaces, get_manual_defaces,
    cleanup_session, get_session_temp_dir, update_session_progress,
    get_session_progress
)
from config import UPLOAD_FOLDER, DEFAULT_IMAGE_QUALITY, DEFAULT_RESOLUTION, RESOLUTION_PRESETS, INPUT_FOLDER, OUTPUT_FOLDER
from app.observation_media_scanner import list_output_subfolders, scan_media_subfolder, list_qualifications, list_learners
from app.placeholder_parser import extract_placeholders, validate_placeholders, assign_placeholder_colors
from app.observation_report_scanner import scan_media_files
from app.observation_report_placeholder_parser import extract_placeholders as obs_extract_placeholders, validate_placeholder, assign_placeholder_colors as obs_assign_placeholder_colors
from app.observation_report_draft_manager import save_draft, load_draft, list_drafts, delete_draft
from app.observation_report_docx_generator import generate_docx as obs_generate_docx

bp = Blueprint('v2p_formatter', __name__)
logger = logging.getLogger(__name__)

# Static files are now served directly by nginx, not Flask
# Removed /static/<path:filename> route to prevent MIME type errors

@bp.route('/static/cache/<path:filename>')
def serve_cache(filename):
    """Serve cached files (thumbnails)"""
    from flask import current_app
    base_dir = Path(current_app.config.get('BASE_DIR', Path(__file__).parent.parent))
    return send_from_directory(str(base_dir / 'static' / 'cache'), filename)

@bp.route('/')
def index():
    """Main page"""
    from config import OUTPUT_FOLDER
    
    # Get qualifications (top-level folders) from OUTPUT_FOLDER
    qualifications = list_qualifications(OUTPUT_FOLDER)
    
    # Get selected qualification and learner from query parameters
    selected_qualification = request.args.get('qualification', '')
    selected_learner = request.args.get('learner', '')
    
    # Get learners for selected qualification (if any)
    learners = []
    if selected_qualification:
        learners = list_learners(OUTPUT_FOLDER, selected_qualification)
    
    return render_template('index.html',
                         qualifications=qualifications,
                         learners=learners,
                         selected_qualification=selected_qualification,
                         selected_learner=selected_learner)

@bp.route('/qualifications', methods=['GET'])
def get_qualifications():
    """List all top-level folders in the output directory (qualifications)"""
    from config import OUTPUT_FOLDER
    try:
        qualifications = list_qualifications(OUTPUT_FOLDER)
        return jsonify({'success': True, 'qualifications': qualifications})
    except Exception as e:
        logger.error(f"Error listing qualifications: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/learners', methods=['GET'])
def get_input_learners():
    """List subfolders (learners) within a selected qualification for output folder"""
    from config import OUTPUT_FOLDER
    qualification = request.args.get('qualification')
    if not qualification:
        return jsonify({'success': False, 'error': 'Qualification not provided'}), 400
    try:
        learners = list_learners(OUTPUT_FOLDER, qualification)
        return jsonify({'success': True, 'learners': learners})
    except Exception as e:
        logger.error(f"Error listing learners for qualification {qualification}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/list_files', methods=['GET'])
def list_files():
    """List all MP4 files in the output directory, optionally filtered by qualification/learner"""
    from config import OUTPUT_FOLDER
    from pathlib import Path
    
    # Get filter parameters
    qualification = request.args.get('qualification', '')
    learner = request.args.get('learner', '')
    
    try:
        # Only scan when both qualification and learner are selected
        if qualification and learner:
            # Scan only within qualification/learner folder and all its subfolders
            scan_path = OUTPUT_FOLDER / qualification / learner
            if not scan_path.exists():
                return jsonify({
                    'success': True,
                    'files': [],
                    'tree': {},
                    'count': 0,
                    'input_folder': str(INPUT_FOLDER),
                    'output_folder': str(OUTPUT_FOLDER)
                })
            # Scan files recursively from the specific qualification/learner path
            # scan_mp4_files uses rglob which recursively scans all subfolders
            all_files = scan_mp4_files(str(scan_path))
            
            # Update relative paths to be relative to OUTPUT_FOLDER (not scan_path)
            base_path = OUTPUT_FOLDER
            filtered_files = []
            for file_info in all_files:
                file_path = Path(file_info['path'])
                try:
                    # Calculate relative path from OUTPUT_FOLDER
                    relative_to_base = file_path.relative_to(base_path)
                    rel_str = str(relative_to_base)
                    file_info['relative_path'] = rel_str
                    # Update folder to be relative to OUTPUT_FOLDER as well
                    # The folder should be the path relative to OUTPUT_FOLDER, excluding filename
                    folder_path = relative_to_base.parent
                    file_info['folder'] = str(folder_path) if folder_path != Path('.') else 'root'
                    filtered_files.append(file_info)
                except ValueError:
                    # Path not relative to base, skip
                    continue
        else:
            # No learner selected - return empty (only show files when learner is selected)
            return jsonify({
                'success': True,
                'files': [],
                'tree': {},
                'count': 0,
                'input_folder': str(INPUT_FOLDER),
                'output_folder': str(OUTPUT_FOLDER)
            })
        
        tree = organize_files_by_folder(filtered_files)
        
        return jsonify({
            'success': True,
            'files': filtered_files,
            'tree': tree,
            'count': len(filtered_files),
            'input_folder': str(INPUT_FOLDER),
            'output_folder': str(OUTPUT_FOLDER),
            'qualification': qualification,
            'learner': learner
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
        
        # Validate file exists and is within output folder
        file_path = os.path.abspath(file_path)
        output_path = os.path.abspath(str(OUTPUT_FOLDER))
        
        if not file_path.startswith(output_path):
            logger.error(f"❌ File path outside output folder: {file_path}")
            return jsonify({'error': 'File path must be within output folder'}), 403
        
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
        
        # Calculate relative path for download/Preview links
        pdf_relative_path = pdf_path.relative_to(OUTPUT_FOLDER)
        
        return jsonify({
            'success': True,
            'file_path': str(pdf_path),
            'pdf_path': str(pdf_path),  # Keep for backward compatibility
            'pdf_relative_path': str(pdf_relative_path),  # For Preview link
            'filename': pdf_path.name,
            'output_folder_path': str(pdf_path.parent)  # Output folder path
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

@bp.route('/batch_video_info', methods=['POST'])
def batch_video_info():
    """Get video information for multiple videos at once"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        data = request.json
        video_paths = data.get('video_paths', [])
        
        if not video_paths:
            return jsonify({'error': 'No video paths provided'}), 400
        
        if not isinstance(video_paths, list):
            return jsonify({'error': 'video_paths must be an array'}), 400
        
        # Limit batch size to prevent abuse
        if len(video_paths) > 20:
            return jsonify({'error': 'Maximum 20 videos allowed per batch'}), 400
        
        results = []
        errors = []
        
        for idx, video_path in enumerate(video_paths):
            try:
                # Validate file path
                video_path = os.path.abspath(str(video_path))
                output_path = os.path.abspath(str(OUTPUT_FOLDER))
                
                if not video_path.startswith(output_path):
                    errors.append({
                        'index': idx,
                        'video_path': video_path,
                        'error': 'File path must be within output folder'
                    })
                    continue
                
                if not os.path.exists(video_path):
                    errors.append({
                        'index': idx,
                        'video_path': video_path,
                        'error': 'File not found'
                    })
                    continue
                
                if not video_path.lower().endswith('.mp4'):
                    errors.append({
                        'index': idx,
                        'video_path': video_path,
                        'error': 'Invalid file type. Only MP4 files are allowed.'
                    })
                    continue
                
                # Get video info
                video_info = get_video_info(video_path)
                
                if not video_info:
                    errors.append({
                        'index': idx,
                        'video_path': video_path,
                        'error': 'Failed to read video file'
                    })
                    continue
                
                results.append({
                    'video_path': video_path,
                    'filename': os.path.basename(video_path),
                    'duration': round(video_info['duration'], 2),
                    'width': video_info['width'],
                    'height': video_info['height'],
                    'fps': round(video_info['fps'], 2),
                    'frame_count': video_info.get('frame_count', 0)
                })
                
            except Exception as e:
                logger.error(f"Error processing video {idx}: {str(e)}", exc_info=True)
                errors.append({
                    'index': idx,
                    'video_path': str(video_path) if video_path else 'unknown',
                    'error': f'Error processing video: {str(e)}'
                })
        
        return jsonify({
            'success': True,
            'videos': results,
            'errors': errors,
            'total_requested': len(video_paths),
            'successful': len(results),
            'failed': len(errors)
        })
        
    except Exception as e:
        logger.error(f"Batch video info error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Failed to get video info: {str(e)}'}), 500

@bp.route('/validate_batch_time_points', methods=['POST'])
def validate_batch_time_points():
    """Validate time points against multiple videos' durations"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        data = request.json
        video_paths = data.get('video_paths', [])
        time_points = data.get('time_points', [])
        
        if not video_paths:
            return jsonify({'error': 'No video paths provided'}), 400
        
        if not isinstance(video_paths, list):
            return jsonify({'error': 'video_paths must be an array'}), 400
        
        if not time_points:
            return jsonify({'error': 'No time points provided'}), 400
        
        if not isinstance(time_points, list):
            return jsonify({'error': 'time_points must be an array'}), 400
        
        # Limit batch size
        if len(video_paths) > 20:
            return jsonify({'error': 'Maximum 20 videos allowed per batch'}), 400
        
        # Validate time_points are numbers
        try:
            time_points = [float(t) for t in time_points]
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid time_points format. Must be array of numbers.'}), 400
        
        validation_results = []
        overall_valid = True
        tolerance = 0.1  # Allow small tolerance for floating point precision
        
        for idx, video_path in enumerate(video_paths):
            try:
                # Validate file path
                video_path = os.path.abspath(str(video_path))
                output_path = os.path.abspath(str(OUTPUT_FOLDER))
                
                if not video_path.startswith(output_path):
                    validation_results.append({
                        'video_path': video_path,
                        'valid': False,
                        'error': 'File path must be within output folder',
                        'warnings': []
                    })
                    overall_valid = False
                    continue
                
                if not os.path.exists(video_path):
                    validation_results.append({
                        'video_path': video_path,
                        'valid': False,
                        'error': 'File not found',
                        'warnings': []
                    })
                    overall_valid = False
                    continue
                
                # Get video info
                video_info = get_video_info(video_path)
                
                if not video_info:
                    validation_results.append({
                        'video_path': video_path,
                        'valid': False,
                        'error': 'Failed to read video file',
                        'warnings': []
                    })
                    overall_valid = False
                    continue
                
                duration = video_info['duration']
                max_time = duration
                
                # Check each time point
                invalid_times = []
                warnings = []
                
                for time_point in time_points:
                    if time_point < -tolerance or time_point > (max_time + tolerance):
                        invalid_times.append(time_point)
                
                if invalid_times:
                    warnings.append({
                        'type': 'time_points_exceed_duration',
                        'message': f'Time points exceed video duration ({duration:.2f}s)',
                        'invalid_times': invalid_times,
                        'video_duration': duration
                    })
                    # Still valid, but with warnings (will be clamped during extraction)
                    validation_results.append({
                        'video_path': video_path,
                        'filename': os.path.basename(video_path),
                        'valid': True,
                        'duration': duration,
                        'warnings': warnings,
                        'invalid_time_points': invalid_times
                    })
                else:
                    validation_results.append({
                        'video_path': video_path,
                        'filename': os.path.basename(video_path),
                        'valid': True,
                        'duration': duration,
                        'warnings': []
                    })
                
            except Exception as e:
                logger.error(f"Error validating video {idx}: {str(e)}", exc_info=True)
                validation_results.append({
                    'video_path': str(video_path) if video_path else 'unknown',
                    'valid': False,
                    'error': f'Error validating video: {str(e)}',
                    'warnings': []
                })
                overall_valid = False
        
        return jsonify({
            'success': True,
            'valid': overall_valid,
            'results': validation_results,
            'total_videos': len(video_paths),
            'has_warnings': any(r.get('warnings') for r in validation_results)
        })
        
    except Exception as e:
        logger.error(f"Batch time points validation error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Failed to validate time points: {str(e)}'}), 500

@bp.route('/open_folder', methods=['POST'])
def open_folder():
    """Open folder in macOS Finder"""
    import subprocess
    import platform
    
    try:
        data = request.json
        folder_path = data.get('path')
        
        if not folder_path:
            return jsonify({
                'success': False,
                'error': 'No folder path provided'
            }), 400
        
        folder_path_obj = Path(folder_path)
        
        # Validate path exists
        if not folder_path_obj.exists() or not folder_path_obj.is_dir():
            return jsonify({
                'success': False,
                'error': 'Folder does not exist'
            }), 400
        
        # On macOS, use 'open' command to open Finder
        if platform.system() == 'Darwin':
            try:
                subprocess.Popen(['open', str(folder_path_obj)])
                return jsonify({
                    'success': True,
                    'message': 'Folder opened in Finder'
                })
            except Exception as e:
                logger.error(f"Error opening folder in Finder: {e}", exc_info=True)
                return jsonify({
                    'success': False,
                    'error': f'Failed to open folder: {str(e)}'
                }), 500
        else:
            # For other platforms, return success but don't open (could implement Windows/Linux later)
            return jsonify({
                'success': True,
                'message': 'Folder path returned (open not supported on this platform)'
            })
            
    except Exception as e:
        logger.error(f"Error in open_folder: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to open folder: {str(e)}'
        }), 500

@bp.route('/open_file', methods=['POST'])
def open_file():
    """Open file in macOS Preview (PDF) or default app"""
    import subprocess
    import platform
    
    try:
        data = request.json
        file_path = data.get('path')
        
        if not file_path:
            return jsonify({
                'success': False,
                'error': 'No file path provided'
            }), 400
        
        # Handle both relative and absolute paths
        if os.path.isabs(file_path):
            file_path_abs = Path(file_path)
        else:
            # Relative path - join with OUTPUT_FOLDER
            file_path_abs = OUTPUT_FOLDER / file_path
        
        file_path_abs = file_path_abs.resolve()
        
        # Validate path exists
        if not file_path_abs.exists() or not file_path_abs.is_file():
            return jsonify({
                'success': False,
                'error': 'File does not exist'
            }), 400
        
        # Security: validate path is within OUTPUT_FOLDER
        try:
            file_path_abs.relative_to(OUTPUT_FOLDER.resolve())
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid file path - must be in output folder'
            }), 403
        
        # On macOS, use 'open -a Preview' for PDFs, 'open' for others
        if platform.system() == 'Darwin':
            try:
                if file_path_abs.suffix.lower() == '.pdf':
                    # Open PDF in Preview
                    subprocess.Popen(['open', '-a', 'Preview', str(file_path_abs)])
                else:
                    # Open other files with default app
                    subprocess.Popen(['open', str(file_path_abs)])
                return jsonify({
                    'success': True,
                    'message': 'File opened in Preview' if file_path_abs.suffix.lower() == '.pdf' else 'File opened'
                })
            except Exception as e:
                logger.error(f"Error opening file: {e}", exc_info=True)
                return jsonify({
                    'success': False,
                    'error': f'Failed to open file: {str(e)}'
                }), 500
        else:
            # For other platforms, return success but don't open (could implement Windows/Linux later)
            return jsonify({
                'success': True,
                'message': 'File path returned (open not supported on this platform)'
            })
            
    except Exception as e:
        logger.error(f"Error in open_file: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to open file: {str(e)}'
        }), 500

@bp.route('/download')
def download_file():
    """Download generated file from output folder"""
    filepath = request.args.get('path')
    if not filepath:
        return jsonify({'error': 'No file path provided'}), 400
    
    # Handle both relative and absolute paths
    if os.path.isabs(filepath):
        # Absolute path provided
        filepath_abs = os.path.abspath(filepath)
    else:
        # Relative path - join with OUTPUT_FOLDER
        filepath_abs = os.path.abspath(os.path.join(str(OUTPUT_FOLDER), filepath))
    
    output_path = os.path.abspath(str(OUTPUT_FOLDER))
    
    # Security: validate path is within output directory
    if not filepath_abs.startswith(output_path):
        return jsonify({'error': 'Invalid file path - must be in output folder'}), 403
    
    if os.path.exists(filepath_abs) and os.path.isfile(filepath_abs):
        return send_file(filepath_abs, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@bp.route('/video_file')
def serve_video_file():
    """Serve video file for preview"""
    filepath = request.args.get('path')
    if not filepath:
        return jsonify({'error': 'No file path provided'}), 400
    
    # Security: validate path is within output directory
    filepath = os.path.abspath(filepath)
    output_path = os.path.abspath(str(OUTPUT_FOLDER))
    
    if not filepath.startswith(output_path):
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
    
    file_path_obj = Path(file_path).resolve()  # Resolve to handle absolute paths
    
    # Validate path is within OUTPUT_FOLDER
    is_valid, error_msg = validate_input_path(str(file_path_obj), OUTPUT_FOLDER)
    if not is_valid:
        return jsonify({'error': error_msg}), 403
    
    # Check if file exists
    if not file_path_obj.exists() or not file_path_obj.is_file():
        return jsonify({'error': 'File not found'}), 404
    
    # Check file type
    ext = file_path_obj.suffix.lower()
    file_type = None
    
    if ext == '.mp4':
        file_type = 'mp4'
    elif ext in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}:
        # Pass the extension without the dot (e.g., 'jpg', 'png')
        file_type = ext.lstrip('.')
    else:
        return jsonify({'error': f'File type {ext} not supported for thumbnails'}), 400
    
    # Get size parameter (optional) - increased default for better quality
    size_str = request.args.get('size', '640x480')
    try:
        width, height = map(int, size_str.split('x'))
        size = (width, height)
    except:
        size = (640, 480)
    
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
        thumbnail_data = get_thumbnail(file_path_obj, file_type, size)
        
        # Get file modification time for ETag
        try:
            file_mtime = file_path_obj.stat().st_mtime
            etag = f'"{hash(str(file_mtime) + str(size))}"'
        except:
            etag = None
        
        # Check if client has cached version
        if etag and request.headers.get('If-None-Match') == etag:
            from flask import Response
            return Response(status=304)  # Not Modified
        
        # Set cache headers for long-term browser caching (1 year)
        # Cache will be invalidated when file modification time changes (via URL parameter)
        headers = {
            'Cache-Control': 'public, max-age=31536000',  # 1 year
            'ETag': etag
        }
        
        return Response(
            thumbnail_data,
            mimetype='image/jpeg',
            headers=headers
        )
    except Exception as e:
        import logging
        import traceback
        error_details = traceback.format_exc()
        logging.error(f"Error generating thumbnail for {file_path}: {e}\n{error_details}", exc_info=True)
        return jsonify({'error': f'Failed to generate thumbnail: {str(e)}', 'details': str(e)}), 500


# ============================================================================
# Media Converter Routes
# ============================================================================

@bp.route('/media-converter')
def media_converter():
    """Media converter main page"""
    from config import MEDIA_CONVERTER_INPUT_FOLDER
    
    # Get qualifications (top-level folders)
    qualifications = list_qualifications(MEDIA_CONVERTER_INPUT_FOLDER)
    
    # Get selected qualification and learner from query parameters
    selected_qualification = request.args.get('qualification', '')
    selected_learner = request.args.get('learner', '')
    
    # Get learners for selected qualification (if any)
    learners = []
    if selected_qualification:
        learners = list_learners(MEDIA_CONVERTER_INPUT_FOLDER, selected_qualification)
    
    return render_template('media_converter.html',
                         qualifications=qualifications,
                         learners=learners,
                         selected_qualification=selected_qualification,
                         selected_learner=selected_learner)


@bp.route('/media-converter/qualifications', methods=['GET'])
def get_media_converter_qualifications():
    """List all top-level folders in the input directory (qualifications)"""
    from config import MEDIA_CONVERTER_INPUT_FOLDER
    try:
        qualifications = list_qualifications(MEDIA_CONVERTER_INPUT_FOLDER)
        return jsonify({'success': True, 'qualifications': qualifications})
    except Exception as e:
        logger.error(f"Error listing qualifications: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/media-converter/learners', methods=['GET'])
def get_media_converter_learners():
    """List subfolders (learners) within a selected qualification"""
    from config import MEDIA_CONVERTER_INPUT_FOLDER
    qualification = request.args.get('qualification')
    if not qualification:
        return jsonify({'success': False, 'error': 'Qualification not provided'}), 400
    try:
        learners = list_learners(MEDIA_CONVERTER_INPUT_FOLDER, qualification)
        return jsonify({'success': True, 'learners': learners})
    except Exception as e:
        logger.error(f"Error listing learners for qualification {qualification}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/media-converter/list', methods=['GET'])
def list_media_files():
    """List all MOV, JPG, JPEG, and PNG files in input folder, optionally filtered by qualification/learner"""
    from config import MEDIA_CONVERTER_INPUT_FOLDER
    from app.media_file_scanner import scan_media_files, get_file_info
    from pathlib import Path
    
    # Get filter parameters
    qualification = request.args.get('qualification', '')
    learner = request.args.get('learner', '')
    
    try:
        # Determine scan path based on filters
        if qualification and learner:
            # Scan only within qualification/learner folder
            scan_path = MEDIA_CONVERTER_INPUT_FOLDER / qualification / learner
            if not scan_path.exists():
                return jsonify({
                    'success': True,
                    'videos': [],
                    'images': [],
                    'video_count': 0,
                    'image_count': 0,
                    'input_folder': str(MEDIA_CONVERTER_INPUT_FOLDER),
                    'output_folder': str(OUTPUT_FOLDER)
                })
        elif qualification:
            # If only qualification selected, return empty (per requirements)
            return jsonify({
                'success': True,
                'videos': [],
                'images': [],
                'video_count': 0,
                'image_count': 0,
                'input_folder': str(MEDIA_CONVERTER_INPUT_FOLDER),
                'output_folder': str(OUTPUT_FOLDER)
            })
        else:
            # No filters - return empty (per requirements: show no files until both selected)
            return jsonify({
                'success': True,
                'videos': [],
                'images': [],
                'video_count': 0,
                'image_count': 0,
                'input_folder': str(MEDIA_CONVERTER_INPUT_FOLDER),
                'output_folder': str(OUTPUT_FOLDER)
            })
        
        result = scan_media_files(str(scan_path))
        
        # Filter files to ensure they're within the qualification/learner path
        # and update relative_path to be relative to INPUT_FOLDER for output path calculation
        base_path = MEDIA_CONVERTER_INPUT_FOLDER
        filtered_videos = []
        filtered_images = []
        
        for video in result['videos']:
            video_path = Path(video['path'])
            try:
                relative_to_base = video_path.relative_to(base_path)
                # Ensure it starts with qualification/learner
                if str(relative_to_base).startswith(f"{qualification}/{learner}/") or str(relative_to_base) == f"{qualification}/{learner}":
                    video['relative_path'] = str(relative_to_base)
                    filtered_videos.append(video)
            except ValueError:
                # Path not relative to base, skip
                continue
        
        for image in result['images']:
            image_path = Path(image['path'])
            try:
                relative_to_base = image_path.relative_to(base_path)
                # Ensure it starts with qualification/learner
                if str(relative_to_base).startswith(f"{qualification}/{learner}/") or str(relative_to_base) == f"{qualification}/{learner}":
                    image['relative_path'] = str(relative_to_base)
                    filtered_images.append(image)
            except ValueError:
                # Path not relative to base, skip
                continue
        
        # Add file info (width, height, duration) to each file
        for video in filtered_videos:
            file_info = get_file_info(Path(video['path']))
            video.update({
                'width': file_info.get('width', 0),
                'height': file_info.get('height', 0),
                'duration': file_info.get('duration', 0)
            })
        
        for image in filtered_images:
            file_info = get_file_info(Path(image['path']))
            image.update({
                'width': file_info.get('width', 0),
                'height': file_info.get('height', 0)
            })
        
        return jsonify({
            'success': True,
            'videos': filtered_videos,
            'images': filtered_images,
            'video_count': len(filtered_videos),
            'image_count': len(filtered_images),
            'input_folder': str(MEDIA_CONVERTER_INPUT_FOLDER),
            'output_folder': str(OUTPUT_FOLDER),
            'qualification': qualification,
            'learner': learner
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
    elif ext == '.mp3':
        file_type = 'mp3'  # Audio files - will return placeholder
    elif ext in ('.jpg', '.jpeg'):
        file_type = 'jpg'
    elif ext == '.png':
        file_type = 'png'
    elif ext == '.pdf':
        file_type = 'pdf'
    else:
        return jsonify({'error': 'Unsupported file type'}), 400
    
    # Get size parameter (optional) - increased default for better quality
    size_str = request.args.get('size', '640x480')
    try:
        width, height = map(int, size_str.split('x'))
        size = (width, height)
    except:
        size = (640, 480)
    
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
        
        # Get file modification time for ETag
        try:
            file_mtime = file_path_obj.stat().st_mtime
            etag = f'"{hash(str(file_mtime) + str(size))}"'
        except:
            etag = None
        
        # Check if client has cached version
        if etag and request.headers.get('If-None-Match') == etag:
            from flask import Response
            return Response(status=304)  # Not Modified
        
        # Set cache headers for long-term browser caching (1 year)
        # Cache will be invalidated when file modification time changes (via URL parameter)
        headers = {
            'Cache-Control': 'public, max-age=31536000',  # 1 year
            'ETag': etag
        }
        
        return Response(
            thumbnail_data,
            mimetype='image/jpeg',
            headers=headers
        )
    except Exception as e:
        import logging
        logging.error(f"Error generating thumbnail: {e}", exc_info=True)
        return jsonify({'error': f'Failed to generate thumbnail: {str(e)}'}), 500



# ============================================================================
# Observation Media DOCX Export
# ============================================================================

@bp.route('/media-converter/audio-file', methods=['GET'])
def serve_audio_file():
    """Serve audio file for preview"""
    filepath = request.args.get('path')
    if not filepath:
        return jsonify({'error': 'No file path provided'}), 400
    
    # Security: validate path is within output directory
    filepath = os.path.abspath(filepath)
    output_path = os.path.abspath(str(OUTPUT_FOLDER))
    
    if not filepath.startswith(output_path):
        return jsonify({'error': 'Invalid file path - must be in output folder'}), 403
    
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return send_file(filepath, mimetype='audio/mpeg')
    return jsonify({'error': 'File not found'}), 404

# ============================================================================
# Image to PDF Module Routes
# ============================================================================

@bp.route('/image-to-pdf', methods=['GET'])
def image_to_pdf_index():
    """Image to PDF main page"""
    from config import OUTPUT_FOLDER
    
    # Get qualifications (top-level folders) from OUTPUT_FOLDER
    qualifications = list_qualifications(OUTPUT_FOLDER)
    
    # Get selected qualification and learner from query parameters
    selected_qualification = request.args.get('qualification', '')
    selected_learner = request.args.get('learner', '')
    
    # Get learners for selected qualification (if any)
    learners = []
    if selected_qualification:
        learners = list_learners(OUTPUT_FOLDER, selected_qualification)
    
    return render_template('image_to_pdf.html',
                         qualifications=qualifications,
                         selected_qualification=selected_qualification,
                         learners=learners,
                         selected_learner=selected_learner)


@bp.route('/list_images', methods=['GET'])
def list_images():
    """List all image and video files in the output directory, optionally filtered by qualification/learner"""
    from config import OUTPUT_FOLDER
    from pathlib import Path
    
    # Get filter parameters
    qualification = request.args.get('qualification', '')
    learner = request.args.get('learner', '')
    
    try:
        # Only scan when both qualification and learner are selected
        if qualification and learner:
            # Scan only within qualification/learner folder and all its subfolders
            scan_path = OUTPUT_FOLDER / qualification / learner
            if not scan_path.exists():
                return jsonify({
                    'success': True,
                    'files': [],
                    'tree': {},
                    'count': 0,
                    'output_folder': str(OUTPUT_FOLDER)
                })
            
            # Scan images recursively from the specific qualification/learner path
            all_image_files = scan_image_files(str(scan_path))
            
            # Scan videos (MP4 files) recursively
            all_video_files = scan_mp4_files(str(scan_path))
            
            # Combine images and videos
            # Add 'type' field to distinguish between images and videos
            for file_info in all_image_files:
                file_info['type'] = 'image'
            
            for file_info in all_video_files:
                file_info['type'] = 'video'
            
            all_files = all_image_files + all_video_files
            
            # Update relative paths to be relative to OUTPUT_FOLDER (for downloads)
            # But folder paths should be relative to the learner folder (scan_path)
            base_path = OUTPUT_FOLDER
            filtered_files = []
            for file_info in all_files:
                file_path = Path(file_info['path'])
                try:
                    # Calculate relative path from OUTPUT_FOLDER (for download links)
                    relative_to_base = file_path.relative_to(base_path)
                    rel_str = str(relative_to_base)
                    file_info['relative_path'] = rel_str
                    
                    # Calculate folder relative to scan_path (learner folder) for UI display
                    relative_to_learner = file_path.relative_to(scan_path)
                    folder_path = relative_to_learner.parent
                    # If image is directly in learner folder, it's 'root', otherwise use folder name
                    file_info['folder'] = str(folder_path) if folder_path != Path('.') else 'root'
                    
                    filtered_files.append(file_info)
                except ValueError:
                    # Path not relative to base, skip
                    continue
            
            # Sort files: subfolders first, then root, then alphabetical within each
            filtered_files.sort(key=lambda x: (
                1 if x['folder'] == 'root' else 0,  # Root last
                x['folder'],  # Then by folder name
                x['name']  # Then by filename
            ))
            
            # Organize files by folder for tree structure
            tree = organize_images_by_folder(filtered_files)
            
            return jsonify({
                'success': True,
                'files': filtered_files,
                'tree': tree,
                'count': len(filtered_files),
                'output_folder': str(OUTPUT_FOLDER)
            })
        else:
            # No learner selected - return empty (only show files when learner is selected)
            return jsonify({
                'success': True,
                'files': [],
                'tree': {},
                'count': 0,
                'output_folder': str(OUTPUT_FOLDER)
            })
    except Exception as e:
        logger.error(f"Error listing images: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to list images: {str(e)}'
        }), 500


@bp.route('/generate_image_documents', methods=['POST'])
def generate_image_documents():
    """Generate PDF and/or DOCX documents from selected images"""
    from config import OUTPUT_FOLDER, RESOLUTION_PRESETS
    from pathlib import Path
    import tempfile
    
    try:
        data = request.json
        image_paths = data.get('image_paths', [])
        image_order = data.get('image_order', image_paths)  # Use custom order if provided
        quality = int(data.get('quality', 95))
        max_size = data.get('max_size', '640x480')
        output_format = data.get('output_format', 'both')  # 'pdf', 'docx', or 'both'
        layout = data.get('layout', 'grid')
        images_per_page = int(data.get('images_per_page', 2))
        
        if not image_paths:
            return jsonify({
                'success': False,
                'error': 'No images provided'
            }), 400
        
        # Validate paths
        validated_paths = []
        for path in image_order if image_order else image_paths:
            img_path = Path(path)
            
            # Validate path is within OUTPUT_FOLDER
            try:
                img_path.resolve().relative_to(OUTPUT_FOLDER.resolve())
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': f'Invalid image path: {path}'
                }), 400
            
            if img_path.exists():
                validated_paths.append(str(img_path.resolve()))
        
        if not validated_paths:
            return jsonify({
                'success': False,
                'error': 'No valid images found'
            }), 400
        
        # Extract filenames (without extension)
        image_names = []
        for path in validated_paths:
            filename = Path(path).stem  # Get filename without extension
            image_names.append(filename)
        
        # Get resolution settings
        max_width = None
        max_height = None
        if max_size and max_size != 'original' and max_size in RESOLUTION_PRESETS:
            if RESOLUTION_PRESETS[max_size]:
                max_width, max_height = RESOLUTION_PRESETS[max_size]
        elif max_size and max_size != 'original':
            # Try to parse custom size (e.g., "800x600")
            try:
                parts = max_size.split('x')
                if len(parts) == 2:
                    max_width = int(parts[0])
                    max_height = int(parts[1])
            except:
                pass
        
        # Determine output location (use learner folder if provided, otherwise use first image's directory)
        qualification = data.get('qualification', '')
        learner = data.get('learner', '')
        
        if qualification and learner:
            # Output to learner folder: OUTPUT_FOLDER/qualification/learner
            output_dir = OUTPUT_FOLDER / qualification / learner
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            # Fallback: use first image's directory
            output_dir = Path(validated_paths[0]).parent
        
        # Get filename from request (mandatory)
        filename = data.get('filename', '').strip()
        if not filename:
            return jsonify({
                'success': False,
                'error': 'Filename is required'
            }), 400
        
        # Sanitize filename: remove invalid characters
        import re
        filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename)
        # Remove leading/trailing dots and spaces
        filename = re.sub(r'^[.\s]+|[.\s]+$', '', filename)
        
        if not filename:
            return jsonify({
                'success': False,
                'error': 'Filename contains only invalid characters'
            }), 400
        
        output_base_name = filename
        
        results = {}
        
        # Generate PDF if requested
        if output_format in ('pdf', 'both'):
            pdf_path = output_dir / f'{output_base_name}.pdf'
            try:
                create_image_pdf(
                    images=validated_paths,
                    image_names=image_names,
                    output_path=str(pdf_path),
                    layout=layout,
                    images_per_page=images_per_page,
                    quality=quality,
                    max_width=max_width,
                    max_height=max_height
                )
                results['pdf_path'] = str(pdf_path)
                results['pdf_url'] = f'/v2p-formatter/download?path={pdf_path.relative_to(OUTPUT_FOLDER)}'
            except Exception as e:
                logger.error(f"Error generating PDF: {e}", exc_info=True)
                results['pdf_error'] = str(e)
        
        # Generate DOCX if requested
        if output_format in ('docx', 'both'):
            docx_path = output_dir / f'{output_base_name}.docx'
            try:
                create_image_docx(
                    images=validated_paths,
                    image_names=image_names,
                    output_path=str(docx_path),
                    images_per_page=images_per_page,
                    quality=quality,
                    max_width=max_width,
                    max_height=max_height
                )
                results['docx_path'] = str(docx_path)
                results['docx_relative_path'] = str(docx_path.relative_to(OUTPUT_FOLDER))
                results['docx_url'] = f'/v2p-formatter/download?path={docx_path.relative_to(OUTPUT_FOLDER)}'
            except Exception as e:
                logger.error(f"Error generating DOCX: {e}", exc_info=True)
                results['docx_error'] = str(e)
        
        # Determine primary file path
        if 'pdf_path' in results:
            results['file_path'] = results['pdf_path']
        elif 'docx_path' in results:
            results['file_path'] = results['docx_path']
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate any documents'
            }), 500
        
        # Add output folder path to response
        results['output_folder_path'] = str(output_dir)
        
        return jsonify({
            'success': True,
            **results
        })
        
    except Exception as e:
        logger.error(f"Error generating image documents: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Failed to generate documents: {str(e)}'
        }), 500

# ============================================================================
# Deface Module Routes
# ============================================================================

@bp.route('/deface', methods=['GET'])
def deface_index():
    """Deface main page"""
    from config import OUTPUT_FOLDER
    
    # Get qualifications (top-level folders) from OUTPUT_FOLDER
    qualifications = list_qualifications(OUTPUT_FOLDER)
    
    # Get selected qualification and learner from query parameters
    selected_qualification = request.args.get('qualification', '')
    selected_learner = request.args.get('learner', '')
    
    # Get learners for selected qualification (if any)
    learners = []
    if selected_qualification:
        learners = list_learners(OUTPUT_FOLDER, selected_qualification)
    
    return render_template('deface.html',
                         qualifications=qualifications,
                         selected_qualification=selected_qualification,
                         learners=learners,
                         selected_learner=selected_learner)


@bp.route('/apply_deface', methods=['POST'])
def apply_deface():
    """Apply deface to images/videos and return preview URLs with session ID"""
    from config import OUTPUT_FOLDER
    from pathlib import Path
    import tempfile
    
    try:
        data = request.json
        image_paths = data.get('image_paths', [])
        quality = int(data.get('quality', 95))
        max_size = data.get('max_size', '640x480')
        
        # Deface settings
        replacewith = data.get('replacewith', 'blur')
        boxes = data.get('boxes', False)
        thresh = float(data.get('thresh', 0.2))
        scale_str = data.get('scale', '')
        mosaicsize = int(data.get('mosaicsize', 20))
        draw_scores = data.get('draw_scores', False)
        approve_video_processing = data.get('approve_video_processing', False)
        
        if not image_paths:
            return jsonify({
                'success': False,
                'error': 'No images or videos provided'
            }), 400
        
        # Validate paths and separate images from videos
        validated_images = []
        validated_videos = []
        
        for path in image_paths:
            file_path = Path(path)
            
            # Validate path is within OUTPUT_FOLDER
            try:
                file_path.resolve().relative_to(OUTPUT_FOLDER.resolve())
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': f'Invalid file path: {path}'
                }), 400
            
            if file_path.exists():
                ext = file_path.suffix.lower()
                if ext == '.mp4':
                    validated_videos.append(file_path.resolve())
                elif ext in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}:
                    validated_images.append(file_path.resolve())
        
        if not validated_images and not validated_videos:
            return jsonify({
                'success': False,
                'error': 'No valid images or videos found'
            }), 400
        
        # Check approval for video processing
        if validated_videos and not approve_video_processing:
            return jsonify({
                'success': False,
                'error': 'Video processing requires approval. Please check "Approve Video Processing" setting.'
            }), 400
        
        # Parse scale if provided
        scale = None
        if scale_str and scale_str != 'original':
            try:
                parts = scale_str.split('x')
                if len(parts) == 2:
                    scale = (int(parts[0]), int(parts[1]))
            except:
                pass
        
        # Create session and temporary directory
        temp_dir = Path(tempfile.mkdtemp(prefix='deface_'))
        session_id = create_session(temp_dir)
        # #region agent log
        log_path = Path('/Users/rom/Documents/nvq/apps/v2p-formatter/.cursor/debug.log')
        with open(log_path, 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"F","location":"routes.py:2131","message":"Session created in apply_deface","data":{"session_id":session_id,"temp_dir":str(temp_dir)},"timestamp":int(time.time()*1000)}) + '\n')
        # #endregion
        
        # Store settings in session
        update_session_settings(session_id, {
            'replacewith': replacewith,
            'boxes': boxes,
            'thresh': thresh,
            'scale': scale_str,
            'mosaicsize': mosaicsize,
            'draw_scores': draw_scores,
            'approve_video_processing': approve_video_processing,
            'quality': quality,
            'max_size': max_size
        })
        
        processed_items = []
        sequence = 0
        
        # Calculate total items for progress tracking
        total_items = len(validated_images) + len(validated_videos)
        update_session_progress(session_id, total=total_items, completed=0, status='processing')
        
        try:
            # Process images with deface
            if validated_images:
                deface_result = deface_images(
                    validated_images,
                    temp_dir,
                    replacewith=replacewith,
                    boxes=boxes,
                    thresh=thresh,
                    scale=scale,
                    mosaicsize=mosaicsize,
                    draw_scores=draw_scores,
                    output_prefix='deface_'
                )
                
                # Log errors if any
                if deface_result.get('errors'):
                    logger.warning(f"Deface processing errors: {deface_result.get('errors')}")
                
                # Process each defaced image
                for defaced_path_str in deface_result.get('processed', []):
                    defaced_file = Path(defaced_path_str)
                    
                    # Verify file exists
                    if not defaced_file.exists():
                        logger.error(f"Defaced file does not exist: {defaced_file}")
                        continue
                    
                    # Find corresponding original image
                    original_path = None
                    for orig_path in validated_images:
                        if defaced_file.name == f'deface_{orig_path.name}':
                            original_path = orig_path
                            break
                    
                    if not original_path:
                        logger.warning(f"Could not find original for defaced file: {defaced_file.name}")
                        continue
                    
                    # Calculate relative path for URL
                    try:
                        rel_path = defaced_file.relative_to(temp_dir)
                    except ValueError:
                        logger.error(f"Defaced file {defaced_file} is not in temp_dir {temp_dir}")
                        continue
                    
                    # Convert to string with forward slashes
                    rel_path_str = str(rel_path).replace('\\', '/')
                    defaced_url = f'/v2p-formatter/deface_temp/{session_id}/{rel_path_str}'
                    
                    sequence += 1
                    processed_items.append({
                        'original_path': str(original_path),
                        'original_name': original_path.name,
                        'defaced_path': str(defaced_file),
                        'defaced_url': defaced_url,
                        'type': 'image',
                        'sequence': sequence,
                        'manual_defaces': []
                    })
            
            # Process videos: process directly with deface tool (outputs MP4)
            if validated_videos:
                completed_images = len([item for item in processed_items if item.get('type') == 'image'])
                completed = completed_images
                for video_path in validated_videos:
                    # Update progress
                    update_session_progress(session_id, completed=completed, current_item=video_path.name)
                    video_result = deface_video(
                        video_path,
                        temp_dir,
                        replacewith=replacewith,
                        boxes=boxes,
                        thresh=thresh,
                        scale=scale,
                        mosaicsize=mosaicsize,
                        draw_scores=draw_scores,
                        output_prefix='deface_'
                    )
                    
                    # Process video result (single MP4 file)
                    if video_result.get('processed'):
                        defaced_path = video_result.get('processed', [])[0]
                        defaced_file = Path(defaced_path)
                        
                        # Verify file exists
                        if not defaced_file.exists():
                            logger.error(f"Defaced video file does not exist: {defaced_file}")
                            continue
                        
                        # Calculate relative path for URL
                        try:
                            rel_path = defaced_file.relative_to(temp_dir)
                        except ValueError:
                            logger.error(f"Defaced file {defaced_file} is not in temp_dir {temp_dir}")
                            continue
                        
                        # Convert to string with forward slashes
                        rel_path_str = str(rel_path).replace('\\', '/')
                        defaced_url = f'/v2p-formatter/deface_temp/{session_id}/{rel_path_str}'
                        
                        sequence += 1
                        processed_items.append({
                            'original_path': str(video_path),
                            'original_name': video_path.name,
                            'defaced_path': str(defaced_file),
                            'defaced_url': defaced_url,
                            'type': 'video',
                            'sequence': sequence,
                            'manual_defaces': []
                        })
                    
                    # Log errors if any
                    if video_result.get('errors'):
                        logger.warning(f"Video deface processing errors: {video_result.get('errors')}")
                    
                    completed += 1
            
            # Update progress to complete
            update_session_progress(session_id, completed=total_items, status='complete')
            
            # Update session with processed items
            update_session_processed(session_id, processed_items)
            
            return jsonify({
                'success': True,
                'processed': processed_items,
                'temp_dir': str(temp_dir),
                'session_id': session_id
            })
        
        except Exception as e:
            logger.error(f"Error in apply_deface: {e}", exc_info=True)
            cleanup_session(session_id)
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    except Exception as e:
        logger.error(f"Error in apply_deface: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/apply_manual_deface', methods=['POST'])
def apply_manual_deface_route():
    """Apply manual deface areas to a specific image/frame"""
    try:
        # #region agent log
        log_path = Path('/Users/rom/Documents/nvq/apps/v2p-formatter/.cursor/debug.log')
        with open(log_path, 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"routes.py:2291","message":"apply_manual_deface_route called","data":{"has_request_json":bool(request.json)},"timestamp":int(time.time()*1000)}) + '\n')
        # #endregion
        data = request.json
        session_id = data.get('session_id')
        media_id = data.get('media_id')  # Index or identifier for media item
        deface_areas = data.get('deface_areas', [])
        mosaicsize = int(data.get('mosaicsize', 20))
        time_point = data.get('time_point')  # For videos only
        
        # #region agent log
        with open(log_path, 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"routes.py:2300","message":"Request params extracted","data":{"session_id":session_id,"media_id":media_id,"media_id_type":type(media_id).__name__,"deface_areas_count":len(deface_areas)},"timestamp":int(time.time()*1000)}) + '\n')
        # #endregion
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID required'
            }), 400
        
        if not media_id:
            return jsonify({
                'success': False,
                'error': 'Media ID required'
            }), 400
        
        if not deface_areas:
            return jsonify({
                'success': False,
                'error': 'No deface areas provided'
            }), 400
        
        # Get session
        # #region agent log
        log_path = Path('/Users/rom/Documents/nvq/apps/v2p-formatter/.cursor/debug.log')
        with open(log_path, 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"E","location":"routes.py:2332","message":"Looking up session","data":{"session_id":session_id,"session_id_type":type(session_id).__name__},"timestamp":int(time.time()*1000)}) + '\n')
        # #endregion
        session = get_session(session_id)
        # #region agent log
        with open(log_path, 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"E","location":"routes.py:2335","message":"Session lookup result","data":{"session_found":session is not None,"session_keys":list(session.keys()) if session else []},"timestamp":int(time.time()*1000)}) + '\n')
        # #endregion
        if not session:
            # #region agent log
            with open(log_path, 'a') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run2","hypothesisId":"E","location":"routes.py:2342","message":"Session expired or not found - returning 404","data":{"session_id":session_id},"timestamp":int(time.time()*1000)}) + '\n')
            # #endregion
            return jsonify({
                'success': False,
                'error': 'Session expired or not found'
            }), 404
        
        # Get processed items
        processed_items = session.get('processed', [])
        
        # #region agent log
        log_path = Path('/Users/rom/Documents/nvq/apps/v2p-formatter/.cursor/debug.log')
        sequences = [item.get('sequence') for item in processed_items]
        with open(log_path, 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"routes.py:2337","message":"Processing items lookup","data":{"media_id":media_id,"processed_items_count":len(processed_items),"sequences":sequences,"media_id_type":type(media_id).__name__},"timestamp":int(time.time()*1000)}) + '\n')
        # #endregion
        
        # Find media item by sequence first (as frontend sends sequence), then by index
        media_item = None
        
        # Try sequence lookup first (frontend sends sequence || index, but prioritizes sequence)
        for item in processed_items:
            item_seq = item.get('sequence')
            # #region agent log
            with open(log_path, 'a') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"routes.py:2347","message":"Comparing sequences","data":{"item_sequence":item_seq,"media_id":media_id,"match":str(item_seq) == str(media_id)},"timestamp":int(time.time()*1000)}) + '\n')
            # #endregion
            if item_seq is not None and str(item_seq) == str(media_id):
                media_item = item
                # #region agent log
                with open(log_path, 'a') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"routes.py:2352","message":"Sequence match found","data":{},"timestamp":int(time.time()*1000)}) + '\n')
                # #endregion
                break
        
        # If sequence lookup failed, try index lookup as fallback
        if not media_item:
            try:
                media_idx = int(media_id)
                # #region agent log
                with open(log_path, 'a') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"routes.py:2360","message":"Trying index lookup as fallback","data":{"media_idx":media_idx,"len_processed":len(processed_items),"index_valid":0 <= media_idx < len(processed_items)},"timestamp":int(time.time()*1000)}) + '\n')
                # #endregion
                if 0 <= media_idx < len(processed_items):
                    media_item = processed_items[media_idx]
                    # #region agent log
                    with open(log_path, 'a') as f:
                        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"routes.py:2364","message":"Index lookup success","data":{"found_sequence":media_item.get('sequence')},"timestamp":int(time.time()*1000)}) + '\n')
                    # #endregion
            except (ValueError, TypeError):
                # media_id is not a valid integer, ignore
                pass
        
        if not media_item:
            # #region agent log
            with open(log_path, 'a') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"routes.py:2366","message":"Media item not found - returning 404","data":{"media_id":media_id,"processed_count":len(processed_items),"sequences":sequences},"timestamp":int(time.time()*1000)}) + '\n')
            # #endregion
            return jsonify({
                'success': False,
                'error': f'Media item not found: {media_id}'
            }), 404
        
        # Get defaced path (for images and videos, use defaced_path)
        temp_dir = get_session_temp_dir(session_id)
        if not temp_dir:
            return jsonify({
                'success': False,
                'error': 'Session temp directory not found'
            }), 404
        
        if media_item.get('type') == 'image':
            # For images: apply manual deface directly
            defaced_path = Path(media_item.get('defaced_path', ''))
            
            if not defaced_path.exists():
                return jsonify({
                    'success': False,
                    'error': f'Defaced file not found: {defaced_path}'
                }), 404
            
            # Create output path with _manual suffix
            output_path = defaced_path.parent / f"{defaced_path.stem}_manual{defaced_path.suffix}"
            
            # Apply manual deface
            logger.info(f"Applying manual deface with {len(deface_areas)} areas to {defaced_path}")
            logger.debug(f"Deface areas: {deface_areas}")
            
            result = apply_manual_deface(
                defaced_path,
                output_path,
                deface_areas,
                mosaicsize=mosaicsize
            )
            
            if not result.get('success'):
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Failed to apply manual deface')
                }), 500
            
            # Update media item defaced_path to point to manual defaced version
            media_item['defaced_path'] = str(output_path)
            rel_path = output_path.relative_to(temp_dir)
            media_item['defaced_url'] = f'/v2p-formatter/deface_temp/{session_id}/{rel_path}'
        
        else:
            # For videos: extract frame at time_point and apply manual deface
            if not time_point or time_point < 0:
                return jsonify({
                    'success': False,
                    'error': 'Time point is required for video manual deface'
                }), 400
            
            defaced_video_path = Path(media_item.get('defaced_path', ''))
            if not defaced_video_path.exists():
                # Try to construct full path from temp_dir
                defaced_video_path = temp_dir / media_item.get('defaced_path', '')
            
            if not defaced_video_path.exists():
                return jsonify({
                    'success': False,
                    'error': f'Defaced video not found: {defaced_video_path}'
                }), 404
            
            # Create directory for manual defaced frames
            manual_frames_dir = temp_dir / f"manual_frames_{media_id}"
            manual_frames_dir.mkdir(parents=True, exist_ok=True)
            
            # Apply manual deface to video frame
            result = apply_manual_deface_to_video(
                defaced_video_path,
                float(time_point),
                manual_frames_dir,
                deface_areas,
                mosaicsize=mosaicsize
            )
            
            if not result.get('success'):
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Failed to apply manual deface to video frame')
                }), 500
            
            # Store manually defaced frame information
            output_path = Path(result['output_path'])
            rel_path = output_path.relative_to(temp_dir)
            
            # Initialize manual_frames list if not exists
            if 'manual_frames' not in media_item:
                media_item['manual_frames'] = []
            
            # Add or update manual frame entry for this time point
            frame_entry = {
                'time_point': result['time_point'],
                'frame_path': str(output_path),
                'frame_url': f'/v2p-formatter/deface_temp/{session_id}/{rel_path}'
            }
            
            # Check if frame for this time point already exists and replace it
            existing_frame = None
            for idx, frame in enumerate(media_item['manual_frames']):
                if abs(frame.get('time_point', -1) - float(time_point)) < 0.01:
                    existing_frame = idx
                    break
            
            if existing_frame is not None:
                media_item['manual_frames'][existing_frame] = frame_entry
            else:
                media_item['manual_frames'].append(frame_entry)
            
            # Store the output path for response
            output_path = Path(result['output_path'])
            rel_path = output_path.relative_to(temp_dir)
            frame_url = f'/v2p-formatter/deface_temp/{session_id}/{rel_path}'
        
        # Store manual defaces in session
        add_manual_defaces(session_id, str(media_id), deface_areas)
        update_session_processed(session_id, processed_items)
        
        # Return updated defaced URL
        if media_item.get('type') == 'image':
            defaced_url = media_item.get('defaced_url')
            return_time_point = None
        else:
            # For videos, return the manually defaced frame URL
            defaced_url = frame_entry.get('frame_url') if 'frame_entry' in locals() else frame_url
            return_time_point = float(time_point) if time_point else None
        
        return jsonify({
            'success': True,
            'defaced_path': str(output_path),
            'defaced_url': defaced_url,
            'deface_areas_applied': len(deface_areas),
            'time_point': return_time_point
        })
    
    except Exception as e:
        logger.error(f"Error in apply_manual_deface: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/deface_temp/<session_id>/<path:filename>')
def serve_deface_temp(session_id: str, filename: str):
    """Serve temporary defaced images from session"""
    try:
        temp_dir = get_session_temp_dir(session_id)
        if not temp_dir:
            return jsonify({'error': 'Session not found or expired'}), 404
        
        file_path = temp_dir / filename
        
        # Security check: ensure file is within temp_dir
        try:
            file_path.resolve().relative_to(temp_dir.resolve())
        except ValueError:
            return jsonify({'error': 'Invalid file path'}), 403
        
        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404
        
        return send_from_directory(str(temp_dir), filename)
    
    except Exception as e:
        logger.error(f"Error serving deface temp file: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/generate_deface_documents', methods=['POST'])
def generate_deface_documents():
    """Generate PDF and/or DOCX documents from accepted defaced files in session"""
    from config import OUTPUT_FOLDER, RESOLUTION_PRESETS
    from pathlib import Path
    import shutil
    
    try:
        data = request.json
        session_id = data.get('session_id')
        image_order = data.get('image_order', [])  # Use custom order if provided
        output_format = data.get('output_format', 'pdf')  # 'pdf', 'docx', 'both', 'mp4', 'mp4+pdf'
        layout = data.get('layout', 'grid')
        images_per_page = int(data.get('images_per_page', 2))
        quality = int(data.get('quality', 95))
        max_size = data.get('max_size', '640x480')
        # Determine if MP4 export is requested from output_format
        export_mp4_videos = output_format in ('mp4', 'mp4+pdf')
        logger.info(f"Output format: {output_format}, Export MP4 videos: {export_mp4_videos}")
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID required'
            }), 400
        
        # Get session
        session = get_session(session_id)
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session expired or not found'
            }), 404
        
        # Get processed items from session
        processed_items = session.get('processed', [])
        if not processed_items:
            return jsonify({
                'success': False,
                'error': 'No processed files found in session'
            }), 400
        
        # Get session settings for quality/max_size if not provided
        session_settings = session.get('settings', {})
        if not quality:
            quality = session_settings.get('quality', 95)
        if not max_size:
            max_size = session_settings.get('max_size', '640x480')
        
        # Get temp directory for session
        temp_dir = get_session_temp_dir(session_id)
        if not temp_dir:
            return jsonify({
                'success': False,
                'error': 'Session temp directory not found'
            }), 404
        
        # Build list of defaced images from session processed items (skip for MP4-only format)
        defaced_images = []
        image_names = []
        
        # Skip image/frame extraction for MP4-only format
        if output_format != 'mp4':
            processed_items_map = {item.get('sequence', idx): item for idx, item in enumerate(processed_items)}
            
            # Apply custom order if provided, otherwise use sequence order
            if image_order:
                # image_order contains sequence numbers or indices
                ordered_items = []
                for order_key in image_order:
                    # Try to find by sequence number
                    item = None
                    for seq, proc_item in processed_items_map.items():
                        if str(seq) == str(order_key) or str(proc_item.get('sequence')) == str(order_key):
                            item = proc_item
                            break
                    if item:
                        ordered_items.append(item)
            else:
                # Use sequence order (1, 2, 3...)
                ordered_items = sorted(processed_items, key=lambda x: x.get('sequence', 0))
            
            # Build defaced_images list and image_names from ordered items
            for item in ordered_items:
                if item.get('type') == 'image':
                    defaced_path = Path(item.get('defaced_path', ''))
                    if defaced_path.exists():
                        defaced_images.append(defaced_path)
                        # Extract filename without 'deface_' prefix
                        filename = defaced_path.stem
                        if filename.startswith('deface_'):
                            filename = filename[7:]
                        image_names.append(filename)
                elif item.get('type') == 'video':
                    # For videos, use manually defaced frames if available, otherwise extract frames
                    defaced_video_path = Path(item.get('defaced_path', ''))
                    if not defaced_video_path.exists():
                        defaced_video_path = temp_dir / item.get('defaced_path', '')
                    
                    if defaced_video_path.exists() and defaced_video_path.suffix.lower() == '.mp4':
                        # Check for manually defaced frames
                        manual_frames = item.get('manual_frames', [])
                        manual_frame_map = {frame.get('time_point'): frame for frame in manual_frames}
                        
                        # Extract frames from defaced MP4 video
                        from app.video_processor import get_video_info, extract_frames_at_times
                        import tempfile as tf
                        
                        video_info = get_video_info(defaced_video_path)
                        if video_info:
                            duration = video_info['duration']
                            # Extract frames every 1 second
                            time_points = [float(i) for i in range(0, int(duration) + 1)]
                            
                            # Create temporary directory for extracted frames (only for non-manual frames)
                            temp_frames_dir = Path(tf.mkdtemp(prefix='deface_frames_'))
                            try:
                                # For each time point, use manual frame if available, otherwise extract
                                video_stem = defaced_video_path.stem
                                if video_stem.startswith('deface_'):
                                    video_stem = video_stem[7:]
                                
                                for idx, time_point in enumerate(time_points, start=1):
                                    # Check if manual frame exists for this time point
                                    manual_frame = None
                                    for manual_time, manual_frame_data in manual_frame_map.items():
                                        if abs(manual_time - time_point) < 0.5:  # Within 0.5 seconds
                                            manual_frame = manual_frame_data
                                            break
                                    
                                    if manual_frame and manual_frame.get('frame_path'):
                                        # Use manually defaced frame
                                        manual_frame_path = Path(manual_frame['frame_path'])
                                        if not manual_frame_path.exists():
                                            manual_frame_path = temp_dir / manual_frame['frame_path']
                                        
                                        if manual_frame_path.exists():
                                            defaced_images.append(manual_frame_path)
                                            time_str = f"{int(time_point)}_{int((time_point % 1) * 100):02d}"
                                            filename = f"{video_stem}_frame_{time_str}_manual"
                                            image_names.append(filename)
                                            continue
                                    
                                    # Extract regular frame for this time point
                                    frame_output_path = temp_frames_dir / f"{idx}.jpg"
                                    from app.video_processor import extract_frame
                                    if extract_frame(defaced_video_path, time_point, frame_output_path, quality=95, resolution=None):
                                        if frame_output_path.exists():
                                            defaced_images.append(frame_output_path)
                                            time_str = f"{int(time_point)}_{int((time_point % 1) * 100):02d}"
                                            filename = f"{video_stem}_frame_{time_str}"
                                            image_names.append(filename)
                            except Exception as e:
                                logger.error(f"Error processing frames from video {defaced_video_path}: {e}", exc_info=True)
                            finally:
                                # Note: temp_frames_dir cleanup happens after document generation
                                pass
        
        # Only require defaced_images for PDF/DOCX generation, not for MP4-only export
        if output_format not in ('mp4',) and not defaced_images:
            return jsonify({
                'success': False,
                'error': 'No defaced files found in session'
            }), 400
        
        # Determine output location (use learner folder if provided, otherwise use first original file's directory)
        qualification = data.get('qualification', '')
        learner = data.get('learner', '')
        
        if qualification and learner:
            # Output to learner folder: OUTPUT_FOLDER/qualification/learner
            output_dir = OUTPUT_FOLDER / qualification / learner
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            # Fallback: use first original file's directory from session
            first_original = processed_items[0].get('original_path', '') if processed_items else ''
            if first_original:
                first_file = Path(first_original)
                if first_file.exists():
                    output_dir = first_file.parent
                else:
                    output_dir = OUTPUT_FOLDER
            else:
                output_dir = OUTPUT_FOLDER
        
        # Get resolution settings
        max_width = None
        max_height = None
        if max_size and max_size != 'original' and max_size in RESOLUTION_PRESETS:
            if RESOLUTION_PRESETS[max_size]:
                max_width, max_height = RESOLUTION_PRESETS[max_size]
        elif max_size and max_size != 'original':
            # Try to parse custom size (e.g., "800x600")
            try:
                parts = max_size.split('x')
                if len(parts) == 2:
                    max_width = int(parts[0])
                    max_height = int(parts[1])
            except:
                pass
            
        # Get filename from request (mandatory)
        filename = data.get('filename', '').strip()
        if not filename:
            return jsonify({
                'success': False,
                'error': 'Filename is required'
            }), 400
        
        # Sanitize filename: remove invalid characters
        import re
        filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename)
        # Remove leading/trailing dots and spaces
        filename = re.sub(r'^[.\s]+|[.\s]+$', '', filename)
        
        if not filename:
            return jsonify({
                'success': False,
                'error': 'Filename contains only invalid characters'
            }), 400
        
        # Add 'deface_' prefix to output filename
        output_base_name = f'deface_{filename}'
        
        results = {}
        
        # Generate PDF if requested
        if output_format in ('pdf', 'both', 'mp4+pdf'):
            # Skip PDF generation if no images (e.g., MP4+PDF with only videos)
            if defaced_images:
                pdf_path = output_dir / f'{output_base_name}.pdf'
                try:
                    create_image_pdf(
                        images=[str(p) for p in defaced_images],
                        image_names=image_names,
                        output_path=str(pdf_path),
                        layout=layout,
                        images_per_page=images_per_page,
                        quality=quality,
                        max_width=max_width,
                        max_height=max_height
                    )
                    results['pdf_path'] = str(pdf_path)
                    results['pdf_url'] = f'/v2p-formatter/download?path={pdf_path.relative_to(OUTPUT_FOLDER)}'
                except Exception as e:
                    logger.error(f"Error generating PDF: {e}", exc_info=True)
                    results['pdf_error'] = str(e)
            else:
                logger.warning("Skipping PDF generation: no images available (MP4+PDF with only videos)")
                results['pdf_error'] = 'No images available for PDF generation'
        
        # Generate DOCX if requested
        if output_format in ('docx', 'both'):
            docx_path = output_dir / f'{output_base_name}.docx'
            try:
                create_image_docx(
                    images=[str(p) for p in defaced_images],
                    image_names=image_names,
                    output_path=str(docx_path),
                    images_per_page=images_per_page,
                    quality=quality,
                    max_width=max_width,
                    max_height=max_height
                )
                results['docx_path'] = str(docx_path)
                results['docx_relative_path'] = str(docx_path.relative_to(OUTPUT_FOLDER))
                results['docx_url'] = f'/v2p-formatter/download?path={docx_path.relative_to(OUTPUT_FOLDER)}'
            except Exception as e:
                logger.error(f"Error generating DOCX: {e}", exc_info=True)
                results['docx_error'] = str(e)
        
        # Export MP4 videos if requested
        exported_videos = []  # Initialize empty list for all cases
        if export_mp4_videos:
            try:
                # Filter video items from processed items
                video_items = [item for item in processed_items if item.get('type') == 'video']
                logger.info(f"Found {len(video_items)} video items to export")
                
                for item in video_items:
                    defaced_video_path_str = item.get('defaced_path', '')
                    defaced_video_path = Path(defaced_video_path_str)
                    
                    logger.info(f"Processing video item: {item.get('original_name')}, defaced_path: {defaced_video_path_str}")
                    
                    # Path is already absolute (stored as absolute in apply_deface)
                    # Just verify it exists
                    if not defaced_video_path.exists():
                        logger.warning(f"Defaced video file does not exist (absolute path): {defaced_video_path}")
                        # If it's an absolute path that doesn't exist, there's nothing we can do
                        logger.error(f"Cannot export video - file not found: {defaced_video_path}")
                        continue
                    
                    if defaced_video_path.suffix.lower() == '.mp4':
                        # Get original filename (without deface_ prefix if present)
                        original_name = item.get('original_name', defaced_video_path.name)
                        if original_name.startswith('deface_'):
                            output_name = original_name
                        else:
                            output_name = f'deface_{original_name}'
                        
                        # Copy video to output directory
                        output_video_path = output_dir / output_name
                        logger.info(f"Copying video from {defaced_video_path} to {output_video_path}")
                        shutil.copy2(defaced_video_path, output_video_path)
                        exported_videos.append({
                            'path': str(output_video_path),
                            'relative_path': str(output_video_path.relative_to(OUTPUT_FOLDER)),
                            'url': f'/v2p-formatter/download?path={output_video_path.relative_to(OUTPUT_FOLDER)}',
                            'name': output_name
                        })
                        logger.info(f"Exported defaced video: {output_video_path}")
                    else:
                        logger.warning(f"Defaced video file is not MP4: {defaced_video_path}")
                
                if exported_videos:
                    results['exported_videos'] = exported_videos
                    results['exported_videos_count'] = len(exported_videos)
                    logger.info(f"Successfully exported {len(exported_videos)} MP4 videos")
                else:
                    logger.warning("No videos were exported (video_items found but export failed)")
            except Exception as e:
                logger.error(f"Error exporting MP4 videos: {e}", exc_info=True)
                results['exported_videos_error'] = str(e)
            
        # Determine primary file path
        # If MP4 only, don't require PDF/DOCX
        if output_format == 'mp4':
            # MP4 only - just need exported videos
            if not exported_videos:
                return jsonify({
                    'success': False,
                    'error': 'No videos to export'
                }), 400
        else:
            # PDF/DOCX formats require at least one document
            # For mp4+pdf, allow success if MP4 export succeeded even if PDF failed
            if 'pdf_path' in results:
                results['file_path'] = results['pdf_path']
            elif 'docx_path' in results:
                results['file_path'] = results['docx_path']
            elif output_format == 'mp4+pdf' and exported_videos:
                # MP4+PDF: MP4 export succeeded, PDF failed - still success
                # Set file_path to first exported video (or leave empty, videos are in exported_videos)
                if exported_videos:
                    results['file_path'] = exported_videos[0].get('path', '')
            elif output_format not in ('mp4', 'mp4+pdf'):
                return jsonify({
                    'success': False,
                    'error': 'Failed to generate any documents'
                }), 500
        
        # Cleanup session after successful document generation
        cleanup_session(session_id)
        
        # Add output folder path to response
        results['output_folder_path'] = str(output_dir)
        
        return jsonify({
            'success': True,
            **results
        })
    
    except Exception as e:
        logger.error(f"Error in generate_deface_documents: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
