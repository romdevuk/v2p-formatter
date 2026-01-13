"""
Session management for deface operations
Stores defaced file paths, original paths, settings, and manual deface areas
"""
import uuid
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import shutil

logger = logging.getLogger(__name__)

# In-memory session storage (for production, consider Redis or database)
_sessions: Dict[str, Dict] = {}

# Session timeout: 1 hour
SESSION_TIMEOUT = timedelta(hours=1)


def create_session(temp_dir: Path) -> str:
    """
    Create a new deface session
    
    Args:
        temp_dir: Temporary directory for this session
        
    Returns:
        Session ID (string)
    """
    session_id = str(uuid.uuid4())
    
    _sessions[session_id] = {
        'session_id': session_id,
        'temp_dir': str(temp_dir),
        'created_at': datetime.now(),
        'processed': [],  # List of processed media items
        'settings': {},  # Deface settings used
        'manual_defaces': {},  # Dict mapping media_id to list of manual deface areas
        'progress': {  # Progress tracking
            'total': 0,
            'completed': 0,
            'current_item': None,
            'status': 'idle'  # 'idle', 'processing', 'complete', 'error'
        }
    }
    
    logger.info(f"Created deface session: {session_id}")
    return session_id


def get_session(session_id: str) -> Optional[Dict]:
    """
    Get session data
    
    Args:
        session_id: Session ID
        
    Returns:
        Session dict or None if not found/expired
    """
    if session_id not in _sessions:
        return None
    
    session = _sessions[session_id]
    
    # Check if session expired
    created_at = session.get('created_at')
    if isinstance(created_at, str):
        try:
            created_at = datetime.fromisoformat(created_at)
        except:
            created_at = datetime.now()
    
    if datetime.now() - created_at > SESSION_TIMEOUT:
        logger.warning(f"Session expired: {session_id}")
        cleanup_session(session_id)
        return None
    
    # Convert datetime to ISO string for JSON serialization
    session_copy = session.copy()
    if isinstance(session_copy.get('created_at'), datetime):
        session_copy['created_at'] = session_copy['created_at'].isoformat()
    
    return session_copy


def update_session_processed(session_id: str, processed_items: List[Dict]) -> bool:
    """
    Update session with processed media items
    
    Args:
        session_id: Session ID
        processed_items: List of processed media items (each with original_path, defaced_path, type, etc.)
        
    Returns:
        True if updated successfully, False if session not found
    """
    if session_id not in _sessions:
        return False
    
    # Update the original session, not a copy
    _sessions[session_id]['processed'] = processed_items
    return True


def update_session_settings(session_id: str, settings: Dict) -> bool:
    """
    Update session with deface settings
    
    Args:
        session_id: Session ID
        settings: Deface settings dict
        
    Returns:
        True if updated successfully, False if session not found
    """
    if session_id not in _sessions:
        return False
    
    # Update the original session, not a copy
    _sessions[session_id]['settings'] = settings
    return True


def add_manual_defaces(session_id: str, media_id: str, deface_areas: List[Dict]) -> bool:
    """
    Add manual deface areas to a media item in session
    
    Args:
        session_id: Session ID
        media_id: Media item ID (index or unique identifier)
        deface_areas: List of deface area definitions (each with x, y, width, height, shape, method)
        
    Returns:
        True if updated successfully, False if session not found
    """
    if session_id not in _sessions:
        return False
    
    # Update the original session, not a copy
    session = _sessions[session_id]
    if 'manual_defaces' not in session:
        session['manual_defaces'] = {}
    
    session['manual_defaces'][media_id] = deface_areas
    return True


def get_manual_defaces(session_id: str, media_id: str) -> List[Dict]:
    """
    Get manual deface areas for a media item
    
    Args:
        session_id: Session ID
        media_id: Media item ID
        
    Returns:
        List of deface area definitions or empty list
    """
    session = get_session(session_id)
    if not session:
        return []
    
    return session.get('manual_defaces', {}).get(media_id, [])


def cleanup_session(session_id: str) -> bool:
    """
    Clean up session and delete temporary directory
    
    Args:
        session_id: Session ID
        
    Returns:
        True if cleaned up, False if session not found
    """
    if session_id not in _sessions:
        return False
    
    session = _sessions[session_id]
    temp_dir = Path(session.get('temp_dir', ''))
    
    # Delete temporary directory
    if temp_dir.exists():
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.info(f"Cleaned up temp directory for session {session_id}: {temp_dir}")
        except Exception as e:
            logger.error(f"Error cleaning up temp directory {temp_dir}: {e}")
    
    # Remove session from memory
    del _sessions[session_id]
    logger.info(f"Cleaned up session: {session_id}")
    
    return True


def cleanup_expired_sessions():
    """
    Clean up all expired sessions (call periodically)
    """
    expired_sessions = []
    
    for session_id, session in list(_sessions.items()):
        created_at = session.get('created_at')
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at)
            except:
                created_at = datetime.now()
        
        if datetime.now() - created_at > SESSION_TIMEOUT:
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        cleanup_session(session_id)
    
    if expired_sessions:
        logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")


def update_session_progress(session_id: str, total: int = None, completed: int = None, current_item: str = None, status: str = None) -> bool:
    """
    Update progress tracking in session
    
    Args:
        session_id: Session ID
        total: Total number of items to process
        completed: Number of items completed
        current_item: Name of currently processing item
        status: Status ('idle', 'processing', 'complete', 'error')
        
    Returns:
        True if updated successfully, False if session not found
    """
    if session_id not in _sessions:
        return False
    
    session = _sessions[session_id]
    if 'progress' not in session:
        session['progress'] = {'total': 0, 'completed': 0, 'current_item': None, 'status': 'idle'}
    
    if total is not None:
        session['progress']['total'] = total
    if completed is not None:
        session['progress']['completed'] = completed
    if current_item is not None:
        session['progress']['current_item'] = current_item
    if status is not None:
        session['progress']['status'] = status
    
    return True


def get_session_progress(session_id: str) -> Optional[Dict]:
    """
    Get progress tracking from session
    
    Args:
        session_id: Session ID
        
    Returns:
        Progress dict or None if session not found
    """
    if session_id not in _sessions:
        return None
    
    return _sessions[session_id].get('progress', {'total': 0, 'completed': 0, 'current_item': None, 'status': 'idle'})


def get_session_temp_dir(session_id: str) -> Optional[Path]:
    """
    Get temporary directory path for a session
    
    Args:
        session_id: Session ID
        
    Returns:
        Path to temp directory or None
    """
    session = get_session(session_id)
    if not session:
        return None
    
    temp_dir_str = session.get('temp_dir', '')
    if temp_dir_str:
        return Path(temp_dir_str)
    
    return None
