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
    Get the output folder for a video file - saves in the same directory as the video
    
    Example:
        Input: /Users/rom/Documents/nvq/v2p-formatter-output/Inter/lakhmaniuk/visit2/tasks/mp4/video.mp4
        Output: /Users/rom/Documents/nvq/v2p-formatter-output/Inter/lakhmaniuk/visit2/tasks/mp4/video_frames/
    """
    video_file = Path(video_path)
    
    # Get the directory containing the video file
    video_dir = video_file.parent
    
    # Create folder name based on video filename (without extension)
    folder_name = f"{video_file.stem}_frames"
    output_dir = video_dir / folder_name
    
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def create_output_folder(video_path, output_base=None):
    """Create output folder for frames in the same directory as the video"""
    output_dir = get_video_output_folder(video_path)
    return output_dir

def get_pdf_output_path(video_path, output_base=None):
    """Get PDF output path in the same directory as the video"""
    video_file = Path(video_path)
    video_dir = video_file.parent
    pdf_path = video_dir / f"{video_file.stem}.pdf"
    return pdf_path

def get_docx_output_path(video_path):
    """Get DOCX output path in the same directory as the video"""
    video_file = Path(video_path)
    video_dir = video_file.parent
    docx_path = video_dir / f"{video_file.stem}.docx"
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


def get_media_output_path(input_path: Path, output_base: Path, new_extension: str) -> Path:
    """
    Generate output path for media conversion, preserving subfolder structure.
    Handles duplicate files by adding suffix (_1, _2, etc.)
    
    Args:
        input_path: Path to input file
        output_base: Base output folder
        new_extension: New file extension (e.g., '.mp4', '.jpg')
    
    Returns:
        Path to output file (with suffix if duplicate exists)
    
    Example:
        Input: /input/folder1/video.mov
        Output: /output/folder1/video.mp4
        If exists: /output/folder1/video_1.mp4
    """
    from config import INPUT_FOLDER
    
    input_file = Path(input_path)
    
    # Get relative path from INPUT_FOLDER
    try:
        relative_path = input_file.relative_to(INPUT_FOLDER)
    except ValueError:
        # If file is not in INPUT_FOLDER, just use filename
        output_path = output_base / f"{input_file.stem}{new_extension}"
    else:
        # Preserve subfolder structure
        parent_folders = relative_path.parent
        if parent_folders and str(parent_folders) != '.':
            output_dir = output_base / parent_folders
        else:
            output_dir = output_base
        
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{input_file.stem}{new_extension}"
    
    # Handle duplicates
    if output_path.exists():
        counter = 1
        while True:
            if parent_folders and str(parent_folders) != '.':
                new_path = output_base / parent_folders / f"{input_file.stem}_{counter}{new_extension}"
            else:
                new_path = output_base / f"{input_file.stem}_{counter}{new_extension}"
            
            if not new_path.exists():
                return new_path
            counter += 1
    
    return output_path


def validate_input_path(file_path: str, input_folder: Path) -> tuple[bool, str]:
    """
    Validate that file path is within input folder (prevent path traversal)
    
    Returns:
        (is_valid, error_message)
    """
    try:
        file_path_obj = Path(file_path).resolve()
        input_folder_obj = input_folder.resolve()
        
        # Check if path is within input folder
        try:
            file_path_obj.relative_to(input_folder_obj)
            return True, ""
        except ValueError:
            return False, "File path is outside input folder"
    
    except Exception as e:
        return False, f"Invalid path: {str(e)}"


def validate_output_path(file_path: str, output_folder: Path) -> tuple[bool, str]:
    """
    Validate that file path is within output folder (prevent path traversal)
    
    Returns:
        (is_valid, error_message)
    """
    try:
        file_path_obj = Path(file_path).resolve()
        output_folder_obj = output_folder.resolve()
        
        # Check if path is within output folder
        try:
            file_path_obj.relative_to(output_folder_obj)
            return True, ""
        except ValueError:
            return False, "File path is outside output folder"
    
    except Exception as e:
        return False, f"Invalid path: {str(e)}"

