"""
Observation Media Scanner Module
Handles subfolder listing and media file scanning from output directory
"""
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Supported media file extensions
MEDIA_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.mp4', '.mov'}


def list_output_subfolders(output_folder: Path) -> List[str]:
    """
    List all subfolders in the output directory.
    
    Args:
        output_folder: Path to the output directory
        
    Returns:
        List of subfolder names (sorted)
    """
    try:
        if not output_folder.exists():
            logger.warning(f"Output folder does not exist: {output_folder}")
            return []
        
        subfolders = []
        for item in output_folder.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                subfolders.append(item.name)
        
        return sorted(subfolders)
    except Exception as e:
        logger.error(f"Error listing subfolders: {e}")
        return []


def scan_media_subfolder(output_folder: Path, subfolder_name: str) -> List[Dict]:
    """
    Scan a specific subfolder for media files recursively (including all nested subfolders).
    
    Args:
        output_folder: Path to the output directory
        subfolder_name: Name of the subfolder to scan
        
    Returns:
        List of media file dictionaries with metadata
    """
    try:
        subfolder_path = output_folder / subfolder_name
        
        if not subfolder_path.exists() or not subfolder_path.is_dir():
            logger.warning(f"Subfolder does not exist: {subfolder_path}")
            return []
        
        media_files = []
        
        # Recursively scan all files and subfolders
        for ext in MEDIA_EXTENSIONS:
            for file_path in subfolder_path.rglob(f'*{ext}'):
                if file_path.is_file():
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
        file_type = 'image' if file_path.suffix.lower() in {'.jpg', '.jpeg', '.png'} else 'video'
        
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
        
        # For images, try to get dimensions
        if file_type == 'image':
            try:
                from PIL import Image
                with Image.open(file_path) as img:
                    info['width'] = img.width
                    info['height'] = img.height
            except Exception as e:
                logger.warning(f"Could not get image dimensions for {file_path}: {e}")
                info['width'] = None
                info['height'] = None
        
        # For videos, duration will be added later if needed
        if file_type == 'video':
            info['width'] = None
            info['height'] = None
            info['duration'] = None  # Can be added later with video processing
        
        return info
    except Exception as e:
        logger.error(f"Error getting media info for {file_path}: {e}")
        return None

