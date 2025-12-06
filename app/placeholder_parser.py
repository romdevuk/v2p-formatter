"""
Placeholder Parser Module
Handles placeholder detection and parsing from text content
"""
import re
from typing import List, Dict, Set
import logging

logger = logging.getLogger(__name__)

# Placeholder pattern: {{Placeholder_Name}} (case-insensitive, underscores only)
PLACEHOLDER_PATTERN = re.compile(r'\{\{([A-Za-z0-9_]+)\}\}')


def extract_placeholders(text: str) -> List[str]:
    """
    Extract all placeholders from text content.
    
    Args:
        text: Text content to parse
        
    Returns:
        List of unique placeholder names (case-insensitive, normalized)
    """
    if not text:
        return []
    
    try:
        # Find all placeholders (case-insensitive)
        matches = PLACEHOLDER_PATTERN.findall(text)
        
        # Normalize to lowercase and get unique placeholders
        placeholders = list(set(name.lower() for name in matches))
        
        # Sort for consistency
        placeholders.sort()
        
        return placeholders
    except Exception as e:
        logger.error(f"Error extracting placeholders: {e}")
        return []


def validate_placeholders(text: str, assigned_media: Dict[str, List]) -> Dict[str, any]:
    """
    Validate placeholder assignments.
    
    Args:
        text: Text content
        assigned_media: Dictionary mapping placeholder names to media lists
        
    Returns:
        Dictionary with validation results
    """
    try:
        placeholders = extract_placeholders(text)
        assigned_placeholders = set(name.lower() for name in assigned_media.keys())
        
        unassigned = [p for p in placeholders if p not in assigned_placeholders]
        assigned = [p for p in placeholders if p in assigned_placeholders]
        
        return {
            'all_placeholders': placeholders,
            'assigned': assigned,
            'unassigned': unassigned,
            'is_valid': len(unassigned) == 0,
            'total_count': len(placeholders),
            'assigned_count': len(assigned),
            'unassigned_count': len(unassigned)
        }
    except Exception as e:
        logger.error(f"Error validating placeholders: {e}")
        return {
            'all_placeholders': [],
            'assigned': [],
            'unassigned': [],
            'is_valid': False,
            'total_count': 0,
            'assigned_count': 0,
            'unassigned_count': 0
        }


def get_placeholder_colors() -> List[str]:
    """
    Get rainbow color palette for placeholders.
    
    Returns:
        List of color hex codes
    """
    return [
        '#ff6b6b',  # Red
        '#4ecdc4',  # Cyan
        '#45b7d1',  # Blue
        '#f9ca24',  # Yellow
        '#6c5ce7',  # Purple
        '#a29bfe',  # Lavender
        '#fd79a8',  # Pink
        '#00b894',  # Green
    ]


def assign_placeholder_colors(placeholders: List[str]) -> Dict[str, str]:
    """
    Assign colors to placeholders using rainbow palette.
    
    Args:
        placeholders: List of placeholder names
        
    Returns:
        Dictionary mapping placeholder names to colors
    """
    colors = get_placeholder_colors()
    color_map = {}
    
    for i, placeholder in enumerate(placeholders):
        color_map[placeholder] = colors[i % len(colors)]
    
    return color_map

