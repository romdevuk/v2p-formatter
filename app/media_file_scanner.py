"""
Scan for media files (MOV, JPG, JPEG, PNG) in a directory tree
"""
import os
from pathlib import Path
from typing import List, Dict


def scan_media_files(root_path: str) -> Dict:
    """
    Scan for media files (MOV, JPG, JPEG, PNG) in input directory tree
    
    Args:
        root_path: Input directory to scan
        
    Returns:
        Dict with 'videos' and 'images' lists, each containing file info:
        {
            'path': full path,
            'relative_path': path relative to input folder,
            'name': filename,
            'size': file size in bytes,
            'size_mb': file size in MB,
            'type': 'mov' or 'jpg' or 'png',
            'folder': containing folder name
        }
    """
    root = Path(root_path)
    if not root.exists():
        return {'videos': [], 'images': []}
    
    videos = []
    images = []
    
    # Scan for MOV files (case insensitive)
    for mov_file in root.rglob('*.mov'):
        try:
            if mov_file.is_file():
                stat = mov_file.stat()
                relative_path = mov_file.relative_to(root)
                
                videos.append({
                    'path': str(mov_file),
                    'relative_path': str(relative_path),
                    'name': mov_file.name,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'type': 'mov',
                    'folder': str(relative_path.parent) if relative_path.parent != Path('.') else 'root',
                    'mtime': stat.st_mtime  # Modification time for cache busting
                })
        except (OSError, PermissionError):
            continue
    
    # Scan for MOV files (uppercase)
    for mov_file in root.rglob('*.MOV'):
        try:
            if mov_file.is_file():
                stat = mov_file.stat()
                relative_path = mov_file.relative_to(root)
                
                videos.append({
                    'path': str(mov_file),
                    'relative_path': str(relative_path),
                    'name': mov_file.name,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'type': 'mov',
                    'folder': str(relative_path.parent) if relative_path.parent != Path('.') else 'root',
                    'mtime': stat.st_mtime  # Modification time for cache busting
                })
        except (OSError, PermissionError):
            continue
    
    # Scan for JPG files (lowercase)
    for jpg_file in root.rglob('*.jpg'):
        try:
            if jpg_file.is_file():
                stat = jpg_file.stat()
                relative_path = jpg_file.relative_to(root)
                
                images.append({
                    'path': str(jpg_file),
                    'relative_path': str(relative_path),
                    'name': jpg_file.name,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'type': 'jpg',
                    'folder': str(relative_path.parent) if relative_path.parent != Path('.') else 'root',
                    'mtime': stat.st_mtime  # Modification time for cache busting
                })
        except (OSError, PermissionError):
            continue
    
    # Scan for JPG files (uppercase)
    for jpg_file in root.rglob('*.JPG'):
        try:
            if jpg_file.is_file():
                stat = jpg_file.stat()
                relative_path = jpg_file.relative_to(root)
                
                images.append({
                    'path': str(jpg_file),
                    'relative_path': str(relative_path),
                    'name': jpg_file.name,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'type': 'jpg',
                    'folder': str(relative_path.parent) if relative_path.parent != Path('.') else 'root',
                    'mtime': stat.st_mtime  # Modification time for cache busting
                })
        except (OSError, PermissionError):
            continue
    
    # Scan for JPEG files (lowercase)
    for jpeg_file in root.rglob('*.jpeg'):
        try:
            if jpeg_file.is_file():
                stat = jpeg_file.stat()
                relative_path = jpeg_file.relative_to(root)
                
                images.append({
                    'path': str(jpeg_file),
                    'relative_path': str(relative_path),
                    'name': jpeg_file.name,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'type': 'jpeg',
                    'folder': str(relative_path.parent) if relative_path.parent != Path('.') else 'root',
                    'mtime': stat.st_mtime  # Modification time for cache busting
                })
        except (OSError, PermissionError):
            continue
    
    # Scan for JPEG files (uppercase)
    for jpeg_file in root.rglob('*.JPEG'):
        try:
            if jpeg_file.is_file():
                stat = jpeg_file.stat()
                relative_path = jpeg_file.relative_to(root)
                
                images.append({
                    'path': str(jpeg_file),
                    'relative_path': str(relative_path),
                    'name': jpeg_file.name,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'type': 'jpeg',
                    'folder': str(relative_path.parent) if relative_path.parent != Path('.') else 'root',
                    'mtime': stat.st_mtime  # Modification time for cache busting
                })
        except (OSError, PermissionError):
            continue
    
    # Scan for PNG files (lowercase)
    for png_file in root.rglob('*.png'):
        try:
            if png_file.is_file():
                stat = png_file.stat()
                relative_path = png_file.relative_to(root)
                
                images.append({
                    'path': str(png_file),
                    'relative_path': str(relative_path),
                    'name': png_file.name,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'type': 'png',
                    'folder': str(relative_path.parent) if relative_path.parent != Path('.') else 'root',
                    'mtime': stat.st_mtime  # Modification time for cache busting
                })
        except (OSError, PermissionError):
            continue
    
    # Scan for PNG files (uppercase)
    for png_file in root.rglob('*.PNG'):
        try:
            if png_file.is_file():
                stat = png_file.stat()
                relative_path = png_file.relative_to(root)
                
                images.append({
                    'path': str(png_file),
                    'relative_path': str(relative_path),
                    'name': png_file.name,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'type': 'png',
                    'folder': str(relative_path.parent) if relative_path.parent != Path('.') else 'root',
                    'mtime': stat.st_mtime  # Modification time for cache busting
                })
        except (OSError, PermissionError):
            continue
    
    # Sort by folder, then by name
    videos.sort(key=lambda x: (x['folder'], x['name']))
    images.sort(key=lambda x: (x['folder'], x['name']))
    
    return {
        'videos': videos,
        'images': images
    }


def get_file_info(file_path: Path) -> Dict:
    """
    Get file metadata (size, duration for videos, resolution for images)
    
    Args:
        file_path: Path to file
        
    Returns:
        Dict with file information
    """
    try:
        stat = file_path.stat()
        info = {
            'size': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'exists': True
        }
        
        # For videos, get duration and resolution using ffprobe
        if file_path.suffix.lower() == '.mov':
            try:
                import subprocess
                import json
                
                # Use ffprobe to get video info
                cmd = [
                    'ffprobe', '-v', 'quiet', '-print_format', 'json',
                    '-show_format', '-show_streams', str(file_path)
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    # Get video stream
                    video_stream = next((s for s in data.get('streams', []) if s.get('codec_type') == 'video'), None)
                    if video_stream:
                        width = int(video_stream.get('width', 0))
                        height = int(video_stream.get('height', 0))
                        
                        # Check for rotation metadata
                        # Rotation can be in tags (e.g., 'rotate': '90') or in side_data_list
                        rotation = 0
                        
                        # Check tags for rotation
                        tags = video_stream.get('tags', {})
                        if 'rotate' in tags:
                            try:
                                rotation = int(tags['rotate'])
                            except (ValueError, TypeError):
                                rotation = 0
                        
                        # Check side_data_list for rotation (display matrix)
                        side_data_list = video_stream.get('side_data_list', [])
                        for side_data in side_data_list:
                            if side_data.get('side_data_type') == 'Display Matrix':
                                rotation_str = side_data.get('rotation', '0')
                                try:
                                    # Rotation is usually in format like "90" or "-90"
                                    rotation = int(float(rotation_str))
                                except (ValueError, TypeError):
                                    rotation = 0
                                break
                        
                        # If rotated 90 or 270 degrees, swap width and height
                        if rotation in (90, -270, 270, -90):
                            width, height = height, width
                        
                        info['width'] = width
                        info['height'] = height
                        info['duration'] = float(data.get('format', {}).get('duration', 0))
                    else:
                        info['width'] = 0
                        info['height'] = 0
                        info['duration'] = 0
                else:
                    info['width'] = 0
                    info['height'] = 0
                    info['duration'] = 0
            except Exception:
                info['width'] = 0
                info['height'] = 0
                info['duration'] = 0
        
        # For images, get resolution using Pillow
        elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            try:
                from PIL import Image
                with Image.open(file_path) as img:
                    info['width'] = img.width
                    info['height'] = img.height
            except Exception:
                info['width'] = 0
                info['height'] = 0
        
        return info
    except Exception as e:
        return {
            'exists': False,
            'error': str(e)
        }

