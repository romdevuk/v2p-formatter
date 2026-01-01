"""
Scan for image files in a directory tree
"""
import os
from pathlib import Path
from typing import List, Dict

# Supported image formats (as per spec approval)
SUPPORTED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def scan_image_files(root_path: str) -> List[Dict]:
    """
    Scan for image files in directory tree
    
    Args:
        root_path: Directory to scan (e.g., OUTPUT_FOLDER/qualification/learner)
        
    Returns:
        List of dicts with file info: {
            'path': full path,
            'relative_path': path relative to root,
            'name': filename,
            'size': file size in bytes,
            'folder': containing folder name
        }
    """
    root = Path(root_path)
    if not root.exists():
        return []
    
    image_files = []
    
    # Recursively scan for all supported image formats (case-insensitive)
    # Check both lowercase and uppercase extensions
    extensions_to_check = set()
    for ext in SUPPORTED_IMAGE_EXTENSIONS:
        extensions_to_check.add(ext.lower())
        extensions_to_check.add(ext.upper())
        # Also add capitalized version
        if len(ext) > 1:
            extensions_to_check.add(ext[0].upper() + ext[1:].lower())
    
    for ext in extensions_to_check:
        for image_file in root.rglob(f'*{ext}'):
            try:
                if image_file.is_file():
                    stat = image_file.stat()
                    relative_path = image_file.relative_to(root)
                    
                    image_files.append({
                        'path': str(image_file),
                        'relative_path': str(relative_path),
                        'name': image_file.name,
                        'size': stat.st_size,
                        'size_mb': round(stat.st_size / (1024 * 1024), 2),
                        'folder': str(relative_path.parent) if relative_path.parent != Path('.') else 'root',
                        'modified_time': stat.st_mtime,  # Modification time (Unix timestamp)
                        'modified_date': stat.st_mtime  # For sorting
                    })
            except (OSError, PermissionError) as e:
                # Skip files we can't access
                continue
    
    # Sort by folder, then by name
    image_files.sort(key=lambda x: (x['folder'], x['name']))
    
    return image_files


def organize_images_by_folder(files: List[Dict]) -> Dict:
    """
    Organize images into a folder tree structure
    
    Returns:
        Dict with folder structure
    """
    tree = {}
    
    for file_info in files:
        folder_path = file_info['folder']
        
        if folder_path == 'root':
            if 'root' not in tree:
                tree['root'] = []
            tree['root'].append(file_info)
        else:
            # Split folder path into parts
            parts = folder_path.split(os.sep)
            current = tree
            
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            if 'files' not in current:
                current['files'] = []
            current['files'].append(file_info)
    
    return tree

