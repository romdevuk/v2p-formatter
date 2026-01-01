"""
Observation Media Scanner Module
Handles subfolder listing and media file scanning from output directory
"""
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Supported media file extensions
MEDIA_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.mp4', '.mov', '.mp3', '.pdf'}


def list_qualifications(output_folder: Path) -> List[str]:
    """
    List all qualifications (top-level folders) in the output directory.
    
    Args:
        output_folder: Path to the output directory
        
    Returns:
        List of qualification names (sorted)
    """
    try:
        if not output_folder.exists():
            logger.warning(f"Output folder does not exist: {output_folder}")
            return []
        
        qualifications = []
        for item in output_folder.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                qualifications.append(item.name)
        
        return sorted(qualifications)
    except Exception as e:
        logger.error(f"Error listing qualifications: {e}")
        return []


def list_learners(output_folder: Path, qualification: str) -> List[str]:
    """
    List all learners (subfolders) within a qualification.
    
    Args:
        output_folder: Path to the output directory
        qualification: Name of the qualification folder
        
    Returns:
        List of learner names (sorted)
    """
    try:
        qualification_path = output_folder / qualification
        
        if not qualification_path.exists() or not qualification_path.is_dir():
            logger.warning(f"Qualification does not exist: {qualification_path}")
            return []
        
        learners = []
        for item in qualification_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                learners.append(item.name)
        
        return sorted(learners)
    except Exception as e:
        logger.error(f"Error listing learners for qualification {qualification}: {e}")
        return []


def list_output_subfolders(output_folder: Path) -> List[str]:
    """
    List all subfolders in the output directory.
    DEPRECATED: Use list_qualifications() instead.
    Kept for backward compatibility.
    
    Args:
        output_folder: Path to the output directory
        
    Returns:
        List of subfolder names (sorted)
    """
    return list_qualifications(output_folder)


def scan_media_subfolder(output_folder: Path, subfolder_name: str, qualification: str = None, learner: str = None) -> List[Dict]:
    """
    Scan a specific subfolder for media files recursively (including all nested subfolders).
    
    Args:
        output_folder: Path to the output directory
        subfolder_name: Name of the subfolder to scan (deprecated, use qualification/learner)
        qualification: Name of the qualification folder (new two-level system)
        learner: Name of the learner folder (new two-level system)
        
    Returns:
        List of media file dictionaries with metadata
    """
    try:
        # Support new two-level system (qualification/learner)
        if qualification and learner:
            subfolder_path = output_folder / qualification / learner
        else:
            # Fallback to old single-level system
            subfolder_path = output_folder / subfolder_name
        
        if not subfolder_path.exists() or not subfolder_path.is_dir():
            logger.warning(f"Subfolder does not exist: {subfolder_path}")
            return []
        
        media_files = []
        seen_files = set()  # Track processed files to avoid duplicates
        
        # Helper function to check if file extension matches (case-insensitive)
        def is_media_file(file_path: Path) -> bool:
            """Check if file has a supported media extension (case-insensitive)"""
            suffix = file_path.suffix.lower()
            return suffix in MEDIA_EXTENSIONS
        
        # Scan files directly in the folder itself (case-insensitive)
        for file_path in subfolder_path.iterdir():
            if file_path.is_file() and is_media_file(file_path):
                file_key = str(file_path)
                if file_key not in seen_files:
                    seen_files.add(file_key)
                    try:
                        media_info = get_media_info(file_path, subfolder_path)
                        if media_info:
                            media_files.append(media_info)
                    except Exception as e:
                        logger.error(f"Error processing file {file_path}: {e}")
                        continue
        
        # Recursively scan all files in subfolders (case-insensitive)
        for file_path in subfolder_path.rglob('*'):
            if file_path.is_file() and is_media_file(file_path):
                # Skip files already processed (files directly in folder)
                if file_path.parent == subfolder_path:
                    continue
                file_key = str(file_path)
                if file_key not in seen_files:
                    seen_files.add(file_key)
                    try:
                        media_info = get_media_info(file_path, subfolder_path)
                        if media_info:
                            media_files.append(media_info)
                    except Exception as e:
                        logger.error(f"Error processing file {file_path}: {e}")
                        continue
        
        # Sort by subfolder path, then by filename
        media_files.sort(key=lambda x: (x.get('subfolder', ''), x['name'].lower()))
        
        return media_files
    except Exception as e:
        logger.error(f"Error scanning subfolder {subfolder_name}: {e}")
        return []


def get_media_info(file_path: Path, base_subfolder_path: Path = None) -> Optional[Dict]:
    """
    Get metadata for a media file.
    
    Args:
        file_path: Path to the media file
        base_subfolder_path: Base subfolder path for calculating relative subfolder
        
    Returns:
        Dictionary with media file information or None if error
    """
    try:
        suffix = file_path.suffix.lower()
        if suffix in {'.jpg', '.jpeg', '.png'}:
            file_type = 'image'
        elif suffix == '.mp3':
            file_type = 'audio'
        elif suffix == '.pdf':
            file_type = 'document'
        else:
            file_type = 'video'
        
        # Get file size
        file_size = file_path.stat().st_size
        
        info = {
            'path': str(file_path),
            'name': file_path.name,
            'type': file_type,
            'size': file_size,
            'relative_path': str(file_path.relative_to(file_path.parent.parent)) if file_path.parent.parent != file_path.parent else file_path.name
        }
        
        # Include subfolder path if base_subfolder_path is provided
        if base_subfolder_path:
            relative_to_subfolder = file_path.relative_to(base_subfolder_path)
            if relative_to_subfolder.parent != Path('.'):
                # File is in a nested subfolder
                info['subfolder'] = str(relative_to_subfolder.parent)
            else:
                # File is directly in the selected subfolder
                info['subfolder'] = ''
        
        # For images, try to get dimensions (apply EXIF orientation first)
        if file_type == 'image':
            try:
                from PIL import Image, ImageOps
                with Image.open(file_path) as img:
                    # Apply EXIF orientation to get correct dimensions
                    img = ImageOps.exif_transpose(img)
                    info['width'] = img.width
                    info['height'] = img.height
            except Exception as e:
                logger.warning(f"Could not get image dimensions for {file_path}: {e}")
                info['width'] = None
                info['height'] = None
        
        # For videos and audio, duration will be added later if needed
        if file_type == 'video':
            info['width'] = None
            info['height'] = None
            info['duration'] = None  # Can be added later with video processing
        elif file_type == 'audio':
            info['width'] = None
            info['height'] = None
            info['duration'] = None  # Can be added later with audio processing
        
        return info
    except Exception as e:
        logger.error(f"Error getting media info for {file_path}: {e}")
        return None

