"""
Observation Report - Media Scanner Module

Purpose: Scan media files from qualification/learner folders

⚠️ IMPORTANT: This is a NEW module - no legacy code from old modules.
The old observation-media module did not work properly and must be completely avoided.

Author: Backend Developer (Agent-1)
Created: Stage 1
"""

from pathlib import Path
from typing import List, Dict, Optional
import logging
import os

logger = logging.getLogger(__name__)

# Import for metadata extraction
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.warning("PIL not available - image metadata extraction will be limited")

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    logger.warning("cv2 not available - video metadata extraction will be limited")


# Supported media file extensions
SUPPORTED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
SUPPORTED_VIDEO_EXTENSIONS = {'.mp4', '.mov'}
SUPPORTED_PDF_EXTENSIONS = {'.pdf'}
SUPPORTED_AUDIO_EXTENSIONS = {'.mp3'}

ALL_SUPPORTED_EXTENSIONS = (
    SUPPORTED_IMAGE_EXTENSIONS | 
    SUPPORTED_VIDEO_EXTENSIONS | 
    SUPPORTED_PDF_EXTENSIONS | 
    SUPPORTED_AUDIO_EXTENSIONS
)


def scan_media_files(qualification: str, learner: str, output_folder: Path) -> List[Dict]:
    """
    Scan media files recursively from /output/{qualification}/{learner}/
    
    Args:
        qualification: Qualification folder name
        learner: Learner folder name
        output_folder: Base output folder path
        
    Returns:
        List of media file dictionaries with metadata
    """
    scan_path = output_folder / qualification / learner
    
    if not scan_path.exists():
        logger.warning(f"Scan path does not exist: {scan_path}")
        return []
    
    media_files = []
    
    # Scan recursively for all supported media types
    for ext in ALL_SUPPORTED_EXTENSIONS:
        pattern = f"*{ext}" if not ext.startswith('.') else f"*{ext}"
        for file_path in scan_path.rglob(pattern):
            try:
                if file_path.is_file():
                    # Get relative path from qualification/learner
                    relative_path = file_path.relative_to(scan_path)
                    
                    # Determine subfolder if nested
                    subfolder = str(relative_path.parent) if relative_path.parent != Path('.') else None
                    
                    # Get metadata
                    metadata = get_media_metadata(file_path)
                    
                    # Determine file type
                    file_type = _get_file_type(file_path)
                    
                    # Generate thumbnail path
                    thumbnail_path = generate_thumbnail_path(file_path)
                    
                    # Calculate relative path from OUTPUT_FOLDER for serving
                    relative_path_from_output = file_path.relative_to(output_folder)
                    
                    media_file = {
                        'path': str(file_path),  # Keep absolute for internal use
                        'relative_path': str(relative_path_from_output),  # For serving (relative to OUTPUT_FOLDER)
                        'name': file_path.name,
                        'type': file_type,
                        'size': metadata.get('size', 0),
                        'qualification': qualification,
                        'learner': learner,
                        'subfolder': subfolder,
                    }
                    
                    # Add type-specific metadata
                    if file_type in ['image', 'video']:
                        media_file['width'] = metadata.get('width')
                        media_file['height'] = metadata.get('height')
                    
                    if file_type in ['video', 'audio']:
                        media_file['duration'] = metadata.get('duration')
                    
                    if thumbnail_path:
                        media_file['thumbnail_path'] = thumbnail_path
                        # Also add relative path for thumbnail (same as image for images)
                        if file_type == 'image':
                            # Images are their own thumbnails, use same relative path
                            media_file['thumbnail_relative_path'] = str(relative_path_from_output)
                        else:
                            # For other types, if thumbnail exists, calculate relative path
                            thumbnail_path_obj = Path(thumbnail_path)
                            if thumbnail_path_obj.exists():
                                media_file['thumbnail_relative_path'] = str(thumbnail_path_obj.relative_to(output_folder))
                    
                    media_files.append(media_file)
                    
            except (OSError, PermissionError) as e:
                logger.warning(f"Error accessing file {file_path}: {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error processing file {file_path}: {e}")
                continue
    
    # Sort by subfolder, then by name
    media_files.sort(key=lambda x: (x['subfolder'] or '', x['name']))
    
    return media_files


def _get_file_type(file_path: Path) -> str:
    """Determine file type from extension"""
    ext = file_path.suffix.lower()
    if ext in SUPPORTED_IMAGE_EXTENSIONS:
        return 'image'
    elif ext in SUPPORTED_VIDEO_EXTENSIONS:
        return 'video'
    elif ext in SUPPORTED_PDF_EXTENSIONS:
        return 'pdf'
    elif ext in SUPPORTED_AUDIO_EXTENSIONS:
        return 'audio'
    return 'unknown'


def get_media_metadata(file_path: Path) -> Dict:
    """
    Extract metadata from a media file
    
    Args:
        file_path: Path to media file
        
    Returns:
        Dictionary with file metadata (size, dimensions, duration, etc.)
    """
    metadata = {}
    
    # Get file size
    try:
        stat = file_path.stat()
        metadata['size'] = stat.st_size
    except OSError:
        metadata['size'] = 0
    
    ext = file_path.suffix.lower()
    
    # Extract dimensions for images
    if ext in SUPPORTED_IMAGE_EXTENSIONS and PIL_AVAILABLE:
        try:
            with Image.open(file_path) as img:
                metadata['width'] = img.width
                metadata['height'] = img.height
        except Exception as e:
            logger.warning(f"Could not extract image dimensions from {file_path}: {e}")
            metadata['width'] = None
            metadata['height'] = None
    
    # Extract dimensions and duration for videos
    elif ext in SUPPORTED_VIDEO_EXTENSIONS and CV2_AVAILABLE:
        try:
            cap = cv2.VideoCapture(str(file_path))
            if cap.isOpened():
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                duration = frame_count / fps if fps > 0 else 0
                metadata['width'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                metadata['height'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                metadata['duration'] = round(duration, 2)
                cap.release()
            else:
                metadata['width'] = None
                metadata['height'] = None
                metadata['duration'] = None
        except Exception as e:
            logger.warning(f"Could not extract video metadata from {file_path}: {e}")
            metadata['width'] = None
            metadata['height'] = None
            metadata['duration'] = None
    
    # Extract duration for audio (MP3)
    elif ext in SUPPORTED_AUDIO_EXTENSIONS:
        # Try to get duration using mutagen if available
        try:
            from mutagen.mp3 import MP3  # type: ignore
            audio = MP3(file_path)
            metadata['duration'] = round(audio.info.length, 2)
        except ImportError:
            logger.debug("mutagen not available - audio duration extraction skipped")
            metadata['duration'] = None
        except Exception as e:
            logger.warning(f"Could not extract audio duration from {file_path}: {e}")
            metadata['duration'] = None
    
    return metadata


def generate_thumbnail_path(file_path: Path) -> Optional[str]:
    """
    Generate thumbnail path for images/videos
    
    For images: Return the image path itself (images are their own thumbnails)
    For videos: Return path to potential thumbnail (same path, could generate later)
    For PDF/MP3: Return None (no thumbnail)
    
    Args:
        file_path: Path to media file
        
    Returns:
        Thumbnail path or None for PDF/MP3
    """
    ext = file_path.suffix.lower()
    
    # Images are their own thumbnails
    if ext in SUPPORTED_IMAGE_EXTENSIONS:
        return str(file_path)
    
    # Videos could have thumbnails (for now return None, could generate later)
    if ext in SUPPORTED_VIDEO_EXTENSIONS:
        # For now, return None - thumbnails can be generated on demand
        # Could implement: return str(file_path.parent / f"{file_path.stem}_thumb.jpg")
        return None
    
    # PDF and MP3 don't have thumbnails
    return None

