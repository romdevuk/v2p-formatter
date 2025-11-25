"""
Scan for MP4 files in a directory tree
"""
import os
from pathlib import Path
from typing import List, Dict


def scan_mp4_files(root_path: str) -> List[Dict]:
    """
    Scan for MP4 files in input directory tree
    
    Args:
        root_path: Input directory to scan (e.g., /Users/rom/Documents/nvq/v2p-formatter-input)
        
    Returns:
        List of dicts with file info: {
            'path': full path,
            'relative_path': path relative to input folder,
            'name': filename,
            'size': file size in bytes,
            'folder': containing folder name
        }
    """
    root = Path(root_path)
    if not root.exists():
        return []
    
    mp4_files = []
    
    for mp4_file in root.rglob('*.mp4'):
        try:
            if mp4_file.is_file():
                stat = mp4_file.stat()
                relative_path = mp4_file.relative_to(root)
                
                mp4_files.append({
                    'path': str(mp4_file),
                    'relative_path': str(relative_path),
                    'name': mp4_file.name,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'folder': str(relative_path.parent) if relative_path.parent != Path('.') else 'root'
                })
        except (OSError, PermissionError) as e:
            # Skip files we can't access
            continue
    
    # Sort by folder, then by name
    mp4_files.sort(key=lambda x: (x['folder'], x['name']))
    
    return mp4_files


def organize_files_by_folder(files: List[Dict]) -> Dict:
    """
    Organize files into a folder tree structure
    
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

