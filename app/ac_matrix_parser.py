"""
AC Matrix Parser
Parses JSON standards files and extracts AC structure
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


def parse_standards_json(json_path: Path) -> Dict:
    """
    Parse JSON standards file and return structured data.
    Assumes one qualification per file.
    
    Args:
        json_path: Path to JSON standards file
    
    Returns:
        {
            "qualification_name": str,
            "units": [
                {
                    "unit_id": str,
                    "unit_name": str,
                    "learning_outcomes": [
                        {
                            "lo_number": str,
                            "lo_name": str,
                            "acs": [
                                {
                                    "ac_id": str,
                                    "ac_description": str,
                                    "question_type": str
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    
    Raises:
        FileNotFoundError: If JSON file doesn't exist
        json.JSONDecodeError: If JSON is invalid
        ValueError: If JSON structure is invalid
    """
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {json_path}: {e}")
        raise
    
    # Validate structure
    if 'qualifications' not in data:
        raise ValueError("JSON file must contain 'qualifications' field")
    
    if not data['qualifications']:
        raise ValueError("JSON file must contain at least one qualification")
    
    # Get first qualification (one qualification per file)
    qualification = data['qualifications'][0]
    
    if 'qualification_name' not in qualification:
        raise ValueError("Qualification must have 'qualification_name' field")
    
    if 'units' not in qualification:
        raise ValueError("Qualification must have 'units' field")
    
    # Parse units and learning outcomes
    parsed_units = []
    for unit in qualification.get('units', []):
        if 'unit_name' not in unit:
            logger.warning(f"Unit missing 'unit_name', skipping")
            continue
        
        unit_id = unit.get('unit_internal_id', '')
        unit_name = unit.get('unit_name', '')
        
        # Parse learning outcomes
        learning_outcomes = []
        for lo in unit.get('learning_outcomes', []):
            lo_number = lo.get('learning_outcome_number', '')
            lo_name = lo.get('learning_outcome_name', '')
            
            # Parse questions (ACs)
            acs = []
            for question in lo.get('questions', []):
                ac_id = question.get('question_id', '')
                ac_description = question.get('question_name', '')
                question_type = question.get('question_type', '')
                
                # Validate AC ID format (X.Y only)
                if ac_id and not _is_valid_ac_id(ac_id):
                    logger.warning(f"Invalid AC ID format '{ac_id}', skipping")
                    continue
                
                if ac_id:  # Only add if AC ID exists
                    acs.append({
                        'ac_id': ac_id,
                        'ac_description': ac_description,
                        'question_type': question_type
                    })
            
            if acs:  # Only add learning outcome if it has ACs
                learning_outcomes.append({
                    'lo_number': lo_number,
                    'lo_name': lo_name,
                    'acs': acs
                })
        
        if learning_outcomes:  # Only add unit if it has learning outcomes with ACs
            parsed_units.append({
                'unit_id': unit_id,
                'unit_name': unit_name,
                'learning_outcomes': learning_outcomes
            })
    
    result = {
        'qualification_name': qualification.get('qualification_name', ''),
        'units': parsed_units
    }
    
    logger.info(f"Parsed JSON file: {len(parsed_units)} units, {_count_total_acs(parsed_units)} ACs")
    
    return result


def extract_all_acs(parsed_data: Dict) -> List[Dict]:
    """
    Extract flat list of all ACs with unit context.
    
    Args:
        parsed_data: Parsed JSON standards data from parse_standards_json()
    
    Returns:
        [
            {
                "ac_id": "1.1",
                "ac_description": "...",
                "unit_id": "641",
                "unit_name": "...",
                "learning_outcome": "1"
            }
        ]
    """
    all_acs = []
    
    for unit in parsed_data.get('units', []):
        unit_id = unit.get('unit_id', '')
        unit_name = unit.get('unit_name', '')
        
        for lo in unit.get('learning_outcomes', []):
            lo_number = lo.get('lo_number', '')
            
            for ac in lo.get('acs', []):
                all_acs.append({
                    'ac_id': ac.get('ac_id', ''),
                    'ac_description': ac.get('ac_description', ''),
                    'unit_id': unit_id,
                    'unit_name': unit_name,
                    'learning_outcome': lo_number
                })
    
    return all_acs


def _is_valid_ac_id(ac_id: str) -> bool:
    """
    Validate AC ID format (X.Y only, no X.Y.Z).
    
    Args:
        ac_id: AC ID string to validate
    
    Returns:
        True if valid format, False otherwise
    """
    import re
    # Match pattern: one or more digits, dot, one or more digits
    # Must be exactly X.Y format (not X.Y.Z)
    pattern = r'^\d+\.\d+$'
    return bool(re.match(pattern, ac_id))


def _count_total_acs(units: List[Dict]) -> int:
    """Count total number of ACs across all units"""
    count = 0
    for unit in units:
        for lo in unit.get('learning_outcomes', []):
            count += len(lo.get('acs', []))
    return count




