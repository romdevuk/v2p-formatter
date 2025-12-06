"""
Draft Manager for Observation Media
Handles saving and loading drafts (text content, assignments, subfolder selection)
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Draft storage location
DRAFTS_FOLDER = Path('/Users/rom/Documents/nvq/v2p-formatter-output/.drafts')
DRAFTS_FOLDER.mkdir(parents=True, exist_ok=True)


def save_draft(name: str, text_content: str, assignments: Dict, selected_subfolder: Optional[str] = None) -> Dict:
    """
    Save a draft to disk.
    
    Args:
        name: Draft name (user-defined)
        text_content: Text content with placeholders
        assignments: Dictionary mapping placeholder names to media lists
        selected_subfolder: Currently selected subfolder (optional)
        
    Returns:
        Dictionary with success status and draft info
    """
    try:
        # Sanitize draft name for filename
        import re
        safe_name = re.sub(r'[^\w\-_\.]', '_', name)
        if not safe_name:
            safe_name = 'draft'
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{safe_name}_{timestamp}.json"
        file_path = DRAFTS_FOLDER / filename
        
        # Create draft data
        draft_data = {
            'name': name,
            'text_content': text_content,
            'assignments': assignments,
            'selected_subfolder': selected_subfolder,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Save to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(draft_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Draft saved: {file_path}")
        
        return {
            'success': True,
            'draft_id': filename,
            'draft_name': name,
            'file_path': str(file_path)
        }
        
    except Exception as e:
        logger.error(f"Error saving draft: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def load_draft(draft_id: str) -> Dict:
    """
    Load a draft from disk.
    
    Args:
        draft_id: Draft filename (with .json extension)
        
    Returns:
        Dictionary with success status and draft data
    """
    try:
        # Security: validate filename
        import re
        if not re.match(r'^[\w\-_\.]+\.json$', draft_id):
            return {
                'success': False,
                'error': 'Invalid draft ID'
            }
        
        file_path = DRAFTS_FOLDER / draft_id
        
        if not file_path.exists():
            return {
                'success': False,
                'error': 'Draft not found'
            }
        
        # Load draft data
        with open(file_path, 'r', encoding='utf-8') as f:
            draft_data = json.load(f)
        
        logger.info(f"Draft loaded: {file_path}")
        
        return {
            'success': True,
            'draft': draft_data
        }
        
    except Exception as e:
        logger.error(f"Error loading draft: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def list_drafts() -> List[Dict]:
    """
    List all available drafts.
    
    Returns:
        List of draft dictionaries with metadata
    """
    try:
        drafts = []
        
        for file_path in DRAFTS_FOLDER.glob('*.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    draft_data = json.load(f)
                
                drafts.append({
                    'id': file_path.name,
                    'name': draft_data.get('name', file_path.stem),
                    'created_at': draft_data.get('created_at', ''),
                    'updated_at': draft_data.get('updated_at', ''),
                    'selected_subfolder': draft_data.get('selected_subfolder'),
                    'placeholder_count': len(draft_data.get('assignments', {}))
                })
            except Exception as e:
                logger.warning(f"Error reading draft {file_path}: {e}")
                continue
        
        # Sort by updated_at (most recent first)
        drafts.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        
        return drafts
        
    except Exception as e:
        logger.error(f"Error listing drafts: {e}", exc_info=True)
        return []


def delete_draft(draft_id: str) -> Dict:
    """
    Delete a draft.
    
    Args:
        draft_id: Draft filename (with .json extension)
        
    Returns:
        Dictionary with success status
    """
    try:
        # Security: validate filename
        import re
        if not re.match(r'^[\w\-_\.]+\.json$', draft_id):
            return {
                'success': False,
                'error': 'Invalid draft ID'
            }
        
        file_path = DRAFTS_FOLDER / draft_id
        
        if not file_path.exists():
            return {
                'success': False,
                'error': 'Draft not found'
            }
        
        # Delete file
        file_path.unlink()
        
        logger.info(f"Draft deleted: {file_path}")
        
        return {
            'success': True
        }
        
    except Exception as e:
        logger.error(f"Error deleting draft: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def update_draft(draft_id: str, text_content: str, assignments: Dict, selected_subfolder: Optional[str] = None) -> Dict:
    """
    Update an existing draft.
    
    Args:
        draft_id: Draft filename (with .json extension)
        text_content: Updated text content
        assignments: Updated assignments
        selected_subfolder: Updated selected subfolder
        
    Returns:
        Dictionary with success status
    """
    try:
        # Load existing draft
        result = load_draft(draft_id)
        if not result['success']:
            return result
        
        draft_data = result['draft']
        
        # Update fields
        draft_data['text_content'] = text_content
        draft_data['assignments'] = assignments
        draft_data['selected_subfolder'] = selected_subfolder
        draft_data['updated_at'] = datetime.now().isoformat()
        
        # Save updated draft
        file_path = DRAFTS_FOLDER / draft_id
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(draft_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Draft updated: {file_path}")
        
        return {
            'success': True
        }
        
    except Exception as e:
        logger.error(f"Error updating draft: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }

