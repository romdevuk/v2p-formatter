"""
Observation Report - Placeholder Parser Module

Purpose: Extract and validate placeholders from text content

⚠️ IMPORTANT: This is a NEW module - no legacy code from old modules.
The old observation-media module did not work properly and must be completely avoided.

Author: Backend Developer (Agent-1)
Created: Stage 1
"""

import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


# Placeholder pattern: {{Placeholder_Name}}
PLACEHOLDER_PATTERN = re.compile(r'\{\{([A-Za-z0-9_]+)\}\}')


# Rainbow color palette for placeholders
PLACEHOLDER_COLORS = [
    '#ff6b6b',  # Red
    '#4ecdc4',  # Cyan
    '#45b7d1',  # Blue
    '#f9ca24',  # Yellow
    '#6c5ce7',  # Purple
    '#a29bfe',  # Lavender
    '#fd79a8',  # Pink
    '#00b894',  # Green
]


def extract_placeholders(text: str) -> List[str]:
    """
    Extract all placeholder names from text
    
    Args:
        text: Text content with placeholders
        
    Returns:
        List of unique placeholder names (case-insensitive, normalized to lowercase)
    """
    if not text:
        return []
    
    # Find all placeholders
    matches = PLACEHOLDER_PATTERN.findall(text)
    
    # Normalize to lowercase and get unique values
    placeholders = []
    seen = set()
    
    for match in matches:
        normalized = match.lower()
        if normalized not in seen:
            seen.add(normalized)
            placeholders.append(normalized)
    
    return placeholders


def validate_placeholder(name: str) -> bool:
    """
    Validate placeholder name format
    
    Placeholders must:
    - Contain only alphanumeric characters and underscores
    - Not be empty
    
    Args:
        name: Placeholder name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not name:
        return False
    
    # Check if name contains only alphanumeric characters and underscores
    import re
    pattern = re.compile(r'^[A-Za-z0-9_]+$')
    return bool(pattern.match(name))


def assign_placeholder_colors(placeholders: List[str]) -> Dict[str, str]:
    """
    Assign rainbow colors to placeholders
    
    Args:
        placeholders: List of placeholder names
        
    Returns:
        Dictionary mapping placeholder names to colors
    """
    color_map = {}
    
    for idx, placeholder in enumerate(placeholders):
        # Cycle through colors if there are more placeholders than colors
        color_index = idx % len(PLACEHOLDER_COLORS)
        color_map[placeholder] = PLACEHOLDER_COLORS[color_index]
    
    return color_map

