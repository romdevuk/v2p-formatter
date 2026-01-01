"""
AC Matrix Storage
Handles saving, loading, and deleting matrix analyses (file-based)
"""
import json
import logging
import uuid
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from config import AC_MATRIX_DATA_DIR

logger = logging.getLogger(__name__)

# Index file for metadata
INDEX_FILE = AC_MATRIX_DATA_DIR / 'index.json'


def _load_index() -> Dict:
    """Load index file or create empty index"""
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error loading index file, creating new one: {e}")
    
    return {"matrices": []}


def _save_index(index_data: Dict):
    """Save index file"""
    try:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        logger.error(f"Error saving index file: {e}")
        raise


def save_matrix(matrix_data: Dict, name: str, json_file_id: str, json_file_name: str, observation_report: str) -> Dict:
    """
    Save matrix to disk.
    
    Args:
        matrix_data: Matrix analysis data
        name: Matrix name (user-defined)
        json_file_id: ID of the JSON standards file used
        json_file_name: Name of the JSON standards file
        observation_report: Original observation report text
    
    Returns:
        {
            "success": bool,
            "matrix_id": str,
            "message": str
        }
    """
    try:
        # Generate unique matrix ID
        matrix_id = str(uuid.uuid4())
        
        # Create matrix file path
        matrix_file = AC_MATRIX_DATA_DIR / f"{matrix_id}.json"
        
        # Prepare full matrix data for storage
        full_matrix_data = {
            "matrix_id": matrix_id,
            "name": name,
            "json_file_id": json_file_id,
            "json_file_name": json_file_name,
            "observation_report": observation_report,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "analysis": matrix_data
        }
        
        # Save matrix file
        with open(matrix_file, 'w', encoding='utf-8') as f:
            json.dump(full_matrix_data, f, indent=2, ensure_ascii=False)
        
        # Update index
        index_data = _load_index()
        index_data["matrices"].append({
            "matrix_id": matrix_id,
            "name": name,
            "json_file_id": json_file_id,
            "json_file_name": json_file_name,
            "created_at": full_matrix_data["created_at"],
            "updated_at": full_matrix_data["updated_at"],
            "coverage_percentage": matrix_data.get("coverage_percentage", 0.0)
        })
        _save_index(index_data)
        
        logger.info(f"Matrix saved: {matrix_id} ({name})")
        
        return {
            "success": True,
            "matrix_id": matrix_id,
            "message": f"Matrix '{name}' saved successfully"
        }
        
    except Exception as e:
        logger.error(f"Error saving matrix: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


def load_matrix(matrix_id: str) -> Dict:
    """
    Load matrix from disk.
    
    Args:
        matrix_id: Matrix ID (UUID)
    
    Returns:
        {
            "success": bool,
            "matrix_data": dict,
            "error": str (if failed)
        }
    """
    try:
        # Validate matrix ID format (UUID)
        try:
            uuid.UUID(matrix_id)
        except ValueError:
            return {
                "success": False,
                "error": "Invalid matrix ID format"
            }
        
        matrix_file = AC_MATRIX_DATA_DIR / f"{matrix_id}.json"
        
        if not matrix_file.exists():
            return {
                "success": False,
                "error": "Matrix not found"
            }
        
        # Load matrix data
        with open(matrix_file, 'r', encoding='utf-8') as f:
            matrix_data = json.load(f)
        
        logger.info(f"Matrix loaded: {matrix_id}")
        
        return {
            "success": True,
            "matrix_data": matrix_data
        }
        
    except Exception as e:
        logger.error(f"Error loading matrix: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


def list_matrices() -> List[Dict]:
    """
    List all saved matrices.
    
    Returns:
        [
            {
                "matrix_id": str,
                "name": str,
                "json_file_name": str,
                "created_at": str,
                "updated_at": str,
                "coverage_percentage": float
            }
        ]
    """
    try:
        index_data = _load_index()
        matrices = index_data.get("matrices", [])
        
        # Sort by updated_at (most recent first)
        matrices.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        
        return matrices
        
    except Exception as e:
        logger.error(f"Error listing matrices: {e}", exc_info=True)
        return []


def delete_matrix(matrix_id: str) -> Dict:
    """
    Delete matrix from disk.
    
    Args:
        matrix_id: Matrix ID (UUID)
    
    Returns:
        {
            "success": bool,
            "message": str
        }
    """
    try:
        # Validate matrix ID format
        try:
            uuid.UUID(matrix_id)
        except ValueError:
            return {
                "success": False,
                "error": "Invalid matrix ID format"
            }
        
        matrix_file = AC_MATRIX_DATA_DIR / f"{matrix_id}.json"
        
        if not matrix_file.exists():
            return {
                "success": False,
                "error": "Matrix not found"
            }
        
        # Delete matrix file
        matrix_file.unlink()
        
        # Update index
        index_data = _load_index()
        index_data["matrices"] = [
            m for m in index_data.get("matrices", [])
            if m.get("matrix_id") != matrix_id
        ]
        _save_index(index_data)
        
        logger.info(f"Matrix deleted: {matrix_id}")
        
        return {
            "success": True,
            "message": "Matrix deleted successfully"
        }
        
    except Exception as e:
        logger.error(f"Error deleting matrix: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }




