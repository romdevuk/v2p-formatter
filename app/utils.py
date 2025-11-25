import os
from pathlib import Path
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_video_directory(video_path):
    """Get the directory containing the video file"""
    return Path(video_path).parent

def get_video_output_folder(video_path):
    """
    Get the output subfolder for a video file, preserving input folder structure
    
    Example:
        Input: /Users/rom/Documents/nvq/v2p-formatter-input/folder1/subfolder/video.mp4
        Output: /Users/rom/Documents/nvq/v2p-formatter-output/folder1/subfolder/video/
    """
    from config import INPUT_FOLDER, OUTPUT_FOLDER
    video_file = Path(video_path)
    
    # Get relative path from INPUT_FOLDER
    try:
        relative_path = video_file.relative_to(INPUT_FOLDER)
    except ValueError:
        # If video is not in INPUT_FOLDER, just use filename
        folder_name = video_file.stem
        output_dir = OUTPUT_FOLDER / folder_name
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    # Get parent folder structure (if any)
    parent_folders = relative_path.parent
    
    # Create output path: OUTPUT_FOLDER / parent_folders / video_name
    folder_name = video_file.stem  # Filename without extension
    if parent_folders and str(parent_folders) != '.':
        # Preserve subfolder structure
        output_dir = OUTPUT_FOLDER / parent_folders / folder_name
    else:
        # No subfolders, just use video name
        output_dir = OUTPUT_FOLDER / folder_name
    
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def create_output_folder(video_path, output_base=None):
    """Create output folder for frames in the video's subfolder"""
    output_dir = get_video_output_folder(video_path)
    frames_dir = output_dir / 'frames'
    frames_dir.mkdir(parents=True, exist_ok=True)
    return frames_dir

def get_pdf_output_path(video_path, output_base=None):
    """Get PDF output path in the video's subfolder"""
    output_dir = get_video_output_folder(video_path)
    video_file = Path(video_path)
    pdf_path = output_dir / f"{video_file.stem}.pdf"
    return pdf_path

def get_docx_output_path(video_path):
    """Get DOCX output path in the video's subfolder"""
    output_dir = get_video_output_folder(video_path)
    video_file = Path(video_path)
    docx_path = output_dir / f"{video_file.stem}.docx"
    return docx_path

def parse_time_points(time_input):
    """
    Parse time input string into list of time points in seconds.
    Supports:
    - Single: '30'
    - Multiple: '10, 25, 45, 60'
    - Range: '10-20' (continuous)
    """
    time_points = []
    
    # Remove whitespace
    time_input = time_input.strip()
    
    # Handle range (e.g., '10-20')
    if '-' in time_input and ',' not in time_input:
        try:
            start, end = map(float, time_input.split('-'))
            # Generate continuous range
            time_points = list(range(int(start), int(end) + 1))
            return time_points
        except ValueError:
            return None
    
    # Handle comma-separated values
    parts = [p.strip() for p in time_input.split(',')]
    for part in parts:
        try:
            time_points.append(float(part))
        except ValueError:
            return None
    
    return sorted(time_points) if time_points else None

