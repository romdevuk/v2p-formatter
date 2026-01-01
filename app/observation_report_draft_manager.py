"""
Observation Report - Draft Manager Module

Purpose: Save, load, list, and delete drafts

⚠️ IMPORTANT: This is a NEW module - no legacy code from old modules.
The old observation-media module did not work properly and must be completely avoided.

Author: Backend Developer (Agent-1)
Created: Stage 1
"""

from pathlib import Path
from typing import Dict, List, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def get_drafts_folder(output_folder: Path) -> Path:
    """Get the drafts folder path"""
    drafts_folder = output_folder / '.drafts'
    drafts_folder.mkdir(exist_ok=True)
    return drafts_folder


def save_draft(draft_data: Dict, output_folder: Path) -> bool:
    """
    Save draft to /output/.drafts/{draft_name}.json
    
    Args:
        draft_data: Draft data dictionary (must contain 'draft_name' key)
        output_folder: Base output folder path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Validate draft_name exists
        draft_name = draft_data.get('draft_name')
        if not draft_name:
            logger.error("Draft name is required")
            return False
        
        # Sanitize draft name for filename
        import re
        safe_name = re.sub(r'[^\w\-_\.]', '_', draft_name)
        if not safe_name:
            safe_name = 'draft'
        
        # Get drafts folder
        drafts_folder = get_drafts_folder(output_folder)
        
        # Check if draft already exists to preserve created_at
        existing_draft_path = drafts_folder / f"{safe_name}.json"
        existing_created_at = None
        
        if existing_draft_path.exists():
            try:
                with open(existing_draft_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    existing_created_at = existing_data.get('created_at')
            except Exception as e:
                logger.warning(f"Could not read existing draft to preserve created_at: {e}")
        
        # Add/update timestamps
        now = datetime.utcnow().isoformat() + 'Z'
        if existing_created_at:
            draft_data['created_at'] = existing_created_at
        else:
            draft_data['created_at'] = now
        draft_data['updated_at'] = now
        
        # Save to JSON file
        draft_file = drafts_folder / f"{safe_name}.json"
        with open(draft_file, 'w', encoding='utf-8') as f:
            json.dump(draft_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Draft saved: {draft_name} -> {draft_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving draft: {e}", exc_info=True)
        return False


def load_draft(draft_name: str, output_folder: Path) -> Optional[Dict]:
    """
    Load draft from JSON file
    
    Args:
        draft_name: Name of draft to load
        output_folder: Base output folder path
        
    Returns:
        Draft data dictionary or None if not found
    """
    try:
        # Sanitize draft name
        import re
        safe_name = re.sub(r'[^\w\-_\.]', '_', draft_name)
        
        # Get drafts folder
        drafts_folder = get_drafts_folder(output_folder)
        draft_file = drafts_folder / f"{safe_name}.json"
        
        if not draft_file.exists():
            logger.warning(f"Draft not found: {draft_name}")
            return None
        
        # Load JSON file
        with open(draft_file, 'r', encoding='utf-8') as f:
            draft_data = json.load(f)
        
        # Basic validation - check for required fields
        if 'draft_name' not in draft_data:
            logger.warning(f"Invalid draft structure: missing draft_name in {draft_name}")
            draft_data['draft_name'] = draft_name  # Add it if missing
        
        logger.info(f"Draft loaded: {draft_name}")
        return draft_data
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing draft JSON {draft_name}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading draft {draft_name}: {e}", exc_info=True)
        return None


def list_drafts(output_folder: Path) -> List[Dict]:
    """
    List all saved drafts with metadata
    
    Args:
        output_folder: Base output folder path
        
    Returns:
        List of draft metadata dictionaries with:
        - draft_name
        - created_at
        - updated_at
        - qualification
        - learner
        - placeholder_count (from assignments)
        - media_count (total media items in assignments)
    """
    try:
        drafts_folder = get_drafts_folder(output_folder)
        
        if not drafts_folder.exists():
            return []
        
        drafts_list = []
        
        # Scan for all JSON files
        for draft_file in drafts_folder.glob('*.json'):
            try:
                with open(draft_file, 'r', encoding='utf-8') as f:
                    draft_data = json.load(f)
                
                # Extract metadata
                metadata = {
                    'draft_name': draft_data.get('draft_name', draft_file.stem),
                    'created_at': draft_data.get('created_at', ''),
                    'updated_at': draft_data.get('updated_at', ''),
                    'qualification': draft_data.get('qualification', ''),
                    'learner': draft_data.get('learner', ''),
                }
                
                # Count placeholders and media
                assignments = draft_data.get('assignments', {})
                metadata['placeholder_count'] = len(assignments)
                
                # Count total media items
                media_count = 0
                for placeholder_media in assignments.values():
                    if isinstance(placeholder_media, list):
                        media_count += len(placeholder_media)
                metadata['media_count'] = media_count
                
                drafts_list.append(metadata)
                
            except Exception as e:
                logger.warning(f"Error reading draft metadata from {draft_file}: {e}")
                continue
        
        # Sort by updated_at (most recent first)
        drafts_list.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        
        return drafts_list
        
    except Exception as e:
        logger.error(f"Error listing drafts: {e}", exc_info=True)
        return []


def delete_draft(draft_name: str, output_folder: Path) -> bool:
    """
    Delete a draft file
    
    Args:
        draft_name: Name of draft to delete
        output_folder: Base output folder path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Sanitize draft name
        import re
        safe_name = re.sub(r'[^\w\-_\.]', '_', draft_name)
        
        # Get drafts folder
        drafts_folder = get_drafts_folder(output_folder)
        draft_file = drafts_folder / f"{safe_name}.json"
        
        if not draft_file.exists():
            logger.warning(f"Draft not found for deletion: {draft_name}")
            return False
        
        # Delete the file
        draft_file.unlink()
        logger.info(f"Draft deleted: {draft_name}")
        return True
        
    except Exception as e:
        logger.error(f"Error deleting draft {draft_name}: {e}", exc_info=True)
        return False

