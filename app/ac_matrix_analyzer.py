"""
AC Matrix Analyzer
Extracts AC references from observation report and generates matrix
"""
import re
import logging
from typing import Dict, Set

logger = logging.getLogger(__name__)

# AC extraction patterns (case-insensitive, exact match only)
AC_PATTERNS = [
    r'\bAC\s*(\d+\.\d+)',                    # "AC 1.1", "AC1.1"
    r'\bAssessment\s+Criteria\s*(\d+\.\d+)', # "Assessment Criteria 1.1"
    r'\bACs\s*[:\-]?\s*((?:\d+\.\d+(?:\s*,\s*)?)+)', # "ACs: 1.1, 1.2, 2.3"
    r'\b(\d+\.\d+)\b',                       # Standalone "1.1", "2.3"
]

# Pattern to identify bracketed unit:AC mapping hints that should be ignored for AC extraction
# Matches patterns like: (129v4: 1.1, 1.2; 130v3: 1.1, 1.2; 643: 1.1, 1.2)
# Handles both parentheses () and square brackets []
# Pattern: matches brackets containing "unit_id: AC" pattern (unit_id is alphanumeric, AC is X.Y format)
BRACKETED_UNIT_MAPPING_PATTERN = re.compile(
    r'[\(\[][^)\]]*[A-Za-z0-9]+\s*:\s*\d+\.\d+[^)\]]*[\)\]]',
    re.IGNORECASE
)


def strip_bracketed_unit_mappings(text: str) -> str:
    """
    Remove bracketed unit:AC mapping hints from observation text so they don't
    count as AC coverage (e.g., "(129v4: 1.1, 1.2; 130v3: 1.1, 1.2; 643: 1.1)").
    These are guidance hints, not observed coverage text.
    
    Handles both parentheses () and square brackets [].
    """
    if not text:
        return text
    
    # Strategy: Find all brackets that contain "unit: AC" pattern and remove them
    # We need to match balanced brackets, so we'll iterate and find matching pairs
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        
        # Check if this is an opening bracket
        if char in '([':
            # Find the matching closing bracket
            open_char = char
            close_char = ')' if char == '(' else ']'
            depth = 1
            j = i + 1
            bracket_content = ''
            
            while j < len(text) and depth > 0:
                if text[j] == open_char:
                    depth += 1
                elif text[j] == close_char:
                    depth -= 1
                if depth > 0:
                    bracket_content += text[j]
                j += 1
            
            # Check if this bracket contains a unit:AC mapping pattern
            # Pattern: alphanumeric unit_id followed by colon and AC format (X.Y)
            if re.search(r'[A-Za-z0-9]+\s*:\s*\d+\.\d+', bracket_content, re.IGNORECASE):
                # This is a unit:AC mapping bracket - skip it
                i = j
                continue
            else:
                # Not a unit:AC mapping - keep the bracket
                result.append(char)
                i += 1
        else:
            result.append(char)
            i += 1
    
    cleaned_text = ''.join(result)
    
    # Clean up any double spaces or extra whitespace left behind
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text = re.sub(r'\s+\.', '.', cleaned_text)  # Fix spaces before periods
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text


def find_section_title(text: str, position: int) -> Dict:
    """
    Find the section title that contains the given position.
    Section titles match pattern: "SECTION:" or "SECTION -" followed by title.
    Returns both title and section index for color coding.
    
    Args:
        text: Full observation report text
        position: Character position to find section for
    
    Returns:
        {
            'title': str,  # Section title (without "SECTION:" prefix) or empty string
            'index': int   # Section index (0-based) for color coding, or -1 if not found
        }
    """
    section_pattern = re.compile(r'^SECTION\s*[:-]?\s*(.+)$', re.MULTILINE | re.IGNORECASE)
    
    # Find all section titles and their positions
    sections = []
    for match in section_pattern.finditer(text):
        sections.append({
            'title': match.group(1).strip(),
            'position': match.start()
        })
    
    # Find the section that contains the position
    current_section = None
    section_index = -1
    for idx, section in enumerate(sections):
        if section['position'] <= position:
            current_section = section
            section_index = idx
        else:
            break
    
    return {
        'title': current_section['title'] if current_section else '',
        'index': section_index
    }


def extract_unit_ac_mappings(text: str) -> Dict:
    """
    Extract unit-AC mappings from text patterns like "641:1.1, 1.2, 1.3" or "AC covered: 641:1.1, 1.2".
    
    Args:
        text: Observation report text
    
    Returns:
        {
            "641": ["1.1", "1.2", "1.3"],
            "642": ["1.1", "4.1"]
        }
    """
    unit_ac_map = {}
    
    # Pattern: unit_id:ac_id,ac_id,ac_id (with optional spaces)
    # Examples: "641:1.1, 1.2", "AC covered: 641:1.1, 1.2, 1.3; 642:1.1", "129v4:1.1"
    pattern = r'([A-Za-z0-9]+)\s*:\s*((?:\d+\.\d+(?:\s*,\s*)?)+)'
    
    for match in re.finditer(pattern, text):
        unit_id = match.group(1)
        acs_str = match.group(2)
        
        # Parse AC IDs from the comma-separated list
        ac_ids = [ac.strip() for ac in acs_str.split(',') if _is_valid_ac_id(ac.strip())]
        
        if unit_id and ac_ids:
            if unit_id not in unit_ac_map:
                unit_ac_map[unit_id] = []
            unit_ac_map[unit_id].extend(ac_ids)
    
    # Remove duplicates while preserving order
    for unit_id in unit_ac_map:
        seen = set()
        unique_ac_ids = []
        for ac_id in unit_ac_map[unit_id]:
            if ac_id not in seen:
                seen.add(ac_id)
                unique_ac_ids.append(ac_id)
        unit_ac_map[unit_id] = unique_ac_ids
    
    if unit_ac_map:
        logger.info(f"Extracted unit-AC mappings: {unit_ac_map}")
    
    return unit_ac_map


def extract_ac_references_with_context(text: str, context_window: int = 150) -> Dict:
    """
    Extract AC IDs from observation report text with surrounding context and section title.
    Returns the text section from the observation report where each AC is covered.
    
    Args:
        text: Observation report text
        context_window: Number of characters before/after match to include (default 150)
    
    Returns:
        {
            "1.1": {
                "ac_id": "1.1",
                "matched_text": "AC 1.1",
                "section_title": "Site Induction",
                "section_index": 0,
                "observation_text_section": "During the site induction, AC 1.1 was covered...",
                "context_start": 45,
                "context_end": 320,
                "match_position": 50,
                "full_section": True
            }
        }
    """
    # CRITICAL: Strip bracketed unit:AC mappings BEFORE extracting ACs
    # This prevents ACs inside brackets like "(129v4: 1.1, 1.2)" from being counted as coverage
    text = strip_bracketed_unit_mappings(text)
    
    found_acs = {}
    
    for pattern in AC_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            ac_id = match.group(1) if match.groups() else match.group(0)
            
            # Handle comma-separated lists
            if ',' in ac_id:
                ac_ids = [ac.strip() for ac in ac_id.split(',')]
                for ac in ac_ids:
                    if _is_valid_ac_id(ac):
                        add_ac_with_context(found_acs, ac, match, text, context_window)
            else:
                if _is_valid_ac_id(ac_id):
                    add_ac_with_context(found_acs, ac_id, match, text, context_window)
    
    logger.info(f"Extracted {len(found_acs)} AC references from observation text")
    
    return found_acs


def find_section_boundaries(text: str, position: int) -> Dict:
    """
    Find the start and end boundaries of the section that contains the given position.
    Section markers must be at the start of a line (after newline or start of text).
    Only matches real section headers, not embedded text.
    
    Args:
        text: Full observation report text
        position: Character position to find section boundaries for
    
    Returns:
        {
            'start': int,  # Section start position
            'end': int     # Section end position (or end of text if last section)
        }
    """
    # Match SECTION at start of line (must be after newline or start of text)
    # Pattern: (start of text OR newline), optional whitespace, "SECTION", optional number, optional dash/colon, title, then newline
    # This ensures we only match real section headers, not embedded text
    section_pattern = re.compile(r'(?:^|\n)\s*SECTION\s*\d*\s*[–-]?\s*(.+?)(?=\n|$)', re.MULTILINE | re.IGNORECASE)
    
    # Find all section titles and their positions
    sections = []
    for match in section_pattern.finditer(text):
        # Get the actual start position
        actual_start = match.start()
        # If match starts with newline, the section actually starts after it
        if actual_start < len(text) and text[actual_start] == '\n':
            actual_start += 1
        # Skip leading whitespace to get to "SECTION"
        while actual_start < len(text) and text[actual_start] in ' \t':
            actual_start += 1
        
        # Only add if this looks like a real section header (starts with "SECTION")
        if actual_start < len(text) and text[actual_start:actual_start+7].upper() == 'SECTION':
            sections.append({
                'title': match.group(1).strip(),
                'position': actual_start
            })
    
    # If no sections found, return full text
    if not sections:
        return {
            'start': 0,
            'end': len(text)
        }
    
    # Find the section that contains the position
    section_start = 0
    section_end = len(text)
    
    for idx, section in enumerate(sections):
        if section['position'] <= position:
            section_start = section['position']
            # Section ends at the start of the next section, or end of text
            if idx + 1 < len(sections):
                section_end = sections[idx + 1]['position']
            else:
                section_end = len(text)
        else:
            break
    
    return {
        'start': section_start,
        'end': section_end
    }


def add_ac_with_context(found_acs: Dict, ac_id: str, match: re.Match, text: str, context_window: int):
    """
    Add AC with observation text section and section title to found_acs dict.
    Extracts the text section from the observation report where the AC is covered.
    Limits extraction to the section boundaries where the AC was found.
    """
    match_start = match.start()
    match_end = match.end()
    
    # Find section title for this AC (returns title and index for color coding)
    section_info = find_section_title(text, match_start)
    section_title = section_info['title']
    section_index = section_info['index']
    
    # Find section boundaries to limit extraction to this section only
    section_bounds = find_section_boundaries(text, match_start)
    section_start = section_bounds['start']
    section_end = section_bounds['end']
    
    # Extract ONLY the paragraph/sentence where this specific AC was mentioned
    # But limit it to the section boundaries
    
    # Find paragraph boundaries around the AC match
    # Look for patterns that indicate paragraph/sentence starts:
    # - Double newlines
    # - Numbered items (like "2.", "3.")
    # - Template markers (like "{{...}}")
    # - Section markers (embedded)
    para_start = section_start
    para_end = section_end
    
    # Find paragraph start - look backwards for paragraph boundaries
    for i in range(match_start, section_start - 1, -1):
        if i <= section_start:
            para_start = section_start
            break
        # Check for double newline (paragraph break)
        if i > 0 and text[i-1:i+1] == '\n\n':
            para_start = i + 1
            while para_start < match_start and para_start < len(text) and text[para_start] in ' \t':
                para_start += 1
            break
        # Check for numbered item pattern (like "2. " or "3. ")
        if i > 1:
            check_text = text[i-2:i+3]
            if re.match(r'^\d+\.\s', check_text):
                para_start = i - 2
                while para_start < match_start and para_start < len(text) and text[para_start] in ' \t':
                    para_start += 1
                break
        # Check for template marker (like "{{...}}")
        if i > 1 and text[i-1:i+1] == '}}':
            # Find the start of this template marker
            template_start = text.rfind('{{', section_start, i+1)
            if template_start >= 0:
                para_start = template_start
                break
    
    # Find paragraph end - look forwards for paragraph boundaries
    for i in range(match_end, section_end):
        if i >= section_end:
            para_end = section_end
            break
        # Check for double newline (paragraph break)
        if i < len(text) - 1 and text[i:i+2] == '\n\n':
            para_end = i
            break
        # Check for next numbered item (like "2. " or "3. ")
        if i < len(text) - 2:
            check_pattern = re.match(r'^\d+\.\s', text[i:i+5])
            if check_pattern and i > match_end + 10:  # Only if it's a new item, not part of current sentence
                para_end = i
                break
    
    # Extract the paragraph
    observation_text_section = text[para_start:para_end].strip()
    
    # Check if the extracted text contains an embedded section marker
    # If it does, handle it based on where the AC is mentioned
    embedded_section_match = re.search(r'SECTION\s+\d+\s*[–:\-]\s*[^\n]+', observation_text_section, re.IGNORECASE)
    if embedded_section_match:
        # Find where the AC is mentioned in the text (look for AC ID pattern)
        ac_pattern = re.compile(r'\b' + re.escape(ac_id) + r'\b', re.IGNORECASE)
        ac_match = ac_pattern.search(observation_text_section)
        
        embedded_section_pos = embedded_section_match.start()
        embedded_section_end = embedded_section_match.end()
        
        if ac_match:
            ac_position_in_text = ac_match.start()
            
            if ac_position_in_text < embedded_section_pos:
                # AC is before the embedded section marker, keep only up to the marker
                observation_text_section = observation_text_section[:embedded_section_pos].strip()
            else:
                # AC is after the embedded section marker
                # Remove the embedded section marker but keep the text after it (where AC is)
                observation_text_section = observation_text_section[embedded_section_end:].strip()
                # Remove any leading numbers or markers that might be left
                # Pattern: number followed by period and space at start of line
                observation_text_section = re.sub(r'^\d+\.\s+', '', observation_text_section)
                # Also remove if it's at start after whitespace
                observation_text_section = re.sub(r'^\s*\d+\.\s+', '', observation_text_section)
                # Clean up any leading/trailing whitespace
                observation_text_section = observation_text_section.strip()
        else:
            # AC not found in text (shouldn't happen, but handle it)
            # Remove embedded section marker and keep what's before it
            observation_text_section = observation_text_section[:embedded_section_pos].strip()
    
    # If paragraph is very short, expand to get more context (but still within section)
    if len(observation_text_section) < 100:
        # Expand to include more context, but stop at paragraph breaks or section boundaries
        expanded_start = max(section_start, para_start - 100)
        expanded_end = min(section_end, para_end + 100)
        
        # Don't cross paragraph boundaries
        for i in range(expanded_start, para_start):
            if i > 0 and text[i-1:i+1] == '\n\n':
                expanded_start = i + 1
                break
        
        for i in range(para_end, expanded_end):
            if i < len(text) - 1 and text[i:i+2] == '\n\n':
                expanded_end = i
                break
        
        observation_text_section = text[expanded_start:expanded_end].strip()
        para_start = expanded_start
        para_end = expanded_end
    
    # Remove section header from the extracted text if it's at the start
    section_header_pattern = re.compile(r'^SECTION\s*\d*\s*[–-]?\s*.+?\n+', re.IGNORECASE | re.MULTILINE)
    observation_text_section = section_header_pattern.sub('', observation_text_section, count=1).strip()
    
    # Remove any remaining embedded section markers that might appear in the middle of text
    # These are not real section breaks, just text that mentions "SECTION X"
    # Remove the entire marker including title
    observation_text_section = re.sub(r'\s+SECTION\s+\d+\s*[–:\-]\s*[^\n]+', '', observation_text_section, flags=re.IGNORECASE)
    # Also remove if it appears at the start of a line within the text
    observation_text_section = re.sub(r'\n\s*SECTION\s+\d+\s*[–:\-]\s*[^\n]+', '', observation_text_section, flags=re.IGNORECASE)
    # Remove if it appears at the start of the text
    observation_text_section = re.sub(r'^SECTION\s+\d+\s*[–:\-]\s*[^\n]+\s*', '', observation_text_section, flags=re.IGNORECASE | re.MULTILINE)
    
    # Clean up multiple newlines (more than 2 consecutive)
    observation_text_section = re.sub(r'\n{3,}', '\n\n', observation_text_section)
    
    # Format the text: preserve paragraph breaks and clean up whitespace
    paragraphs = [p.strip() for p in observation_text_section.split('\n\n') if p.strip()]
    observation_text_section = '\n\n'.join(paragraphs)
    
    # Store the full section boundaries for reference
    context_start = section_start
    context_end = section_end
    
    # If AC already found, keep only the first occurrence (don't merge multiple sections)
    # This ensures we only show text from one section
    if ac_id not in found_acs:
        found_acs[ac_id] = {
            "ac_id": ac_id,
            "matched_text": match.group(0),
            "section_title": section_title,
            "section_index": section_index,  # For color coding (matches observation-media)
            "observation_text_section": observation_text_section,
            "context_start": context_start,
            "context_end": context_end,
            "match_position": match_start,
            "full_section": (context_end - context_start) < (context_window * 3)  # Rough check if truncated
        }
    else:
        # If AC found multiple times, only keep the first occurrence
        # This prevents showing text from multiple sections
        pass


def generate_matrix(parsed_data: Dict, found_acs: Dict, observation_text: str) -> Dict:
    """
    Generate matrix comparing found ACs against all ACs.
    
    Args:
        parsed_data: Parsed JSON standards data
        found_acs: Dict of AC IDs with context (from extract_ac_references_with_context)
        observation_text: Full observation report text
    
    Returns:
        Matrix data structure with observation context included
    """
    from app.ac_matrix_parser import extract_all_acs
    
    # Get all ACs from standards
    all_acs = extract_all_acs(parsed_data)
    
    # Create set of found AC IDs for quick lookup
    found_ac_ids = set(found_acs.keys())
    
    # Build matrix by unit
    matrix_units = []
    total_ac_count = 0
    covered_ac_count = 0
    
    for unit in parsed_data.get('units', []):
        unit_id = unit.get('unit_id', '')
        unit_name = unit.get('unit_name', '')
        
        unit_acs = []
        unit_total = 0
        unit_covered = 0
        
        for lo in unit.get('learning_outcomes', []):
            lo_number = lo.get('lo_number', '')
            
            for ac in lo.get('acs', []):
                ac_id = ac.get('ac_id', '')
                if not ac_id:
                    continue
                
                unit_total += 1
                total_ac_count += 1
                
                # Check if AC was found in observation
                is_covered = ac_id in found_ac_ids
                if is_covered:
                    unit_covered += 1
                    covered_ac_count += 1
                
                # Get observation context if covered
                ac_data = {
                    "ac_id": ac_id,
                    "ac_description": ac.get('ac_description', ''),
                    "learning_outcome": lo_number,
                    "status": "covered" if is_covered else "missing"
                }
                
                if is_covered and ac_id in found_acs:
                    ac_info = found_acs[ac_id]
                    ac_data.update({
                        "matched_text": ac_info.get("matched_text", ""),
                        "section_title": ac_info.get("section_title", ""),
                        "section_index": ac_info.get("section_index", -1),
                        "observation_text_section": ac_info.get("observation_text_section", ""),
                        "observation_context_start": ac_info.get("context_start", 0),
                        "observation_context_end": ac_info.get("context_end", 0),
                        "full_section": ac_info.get("full_section", True)
                    })
                
                unit_acs.append(ac_data)
        
        if unit_acs:  # Only add unit if it has ACs
            matrix_units.append({
                "unit_id": unit_id,
                "unit_name": unit_name,
                "total_ac_count": unit_total,
                "covered_ac_count": unit_covered,
                "missing_ac_count": unit_total - unit_covered,
                "acs": unit_acs
            })
    
    # Calculate overall statistics
    missing_ac_count = total_ac_count - covered_ac_count
    coverage_percentage = (covered_ac_count / total_ac_count * 100) if total_ac_count > 0 else 0.0
    
    matrix_data = {
        "total_ac_count": total_ac_count,
        "covered_ac_count": covered_ac_count,
        "missing_ac_count": missing_ac_count,
        "coverage_percentage": round(coverage_percentage, 1),
        "units": matrix_units
    }
    
    logger.info(f"Matrix generated: {covered_ac_count}/{total_ac_count} ACs covered ({coverage_percentage:.1f}%)")
    
    return matrix_data


def calculate_coverage_stats(matrix_data: Dict) -> Dict:
    """
    Calculate coverage statistics.
    
    Args:
        matrix_data: Matrix data structure
    
    Returns:
        {
            "total_ac_count": int,
            "covered_ac_count": int,
            "missing_ac_count": int,
            "coverage_percentage": float
        }
    """
    return {
        "total_ac_count": matrix_data.get("total_ac_count", 0),
        "covered_ac_count": matrix_data.get("covered_ac_count", 0),
        "missing_ac_count": matrix_data.get("missing_ac_count", 0),
        "coverage_percentage": matrix_data.get("coverage_percentage", 0.0)
    }


def _is_valid_ac_id(ac_id: str) -> bool:
    """
    Validate AC ID format (X.Y only, no X.Y.Z).
    Exact match only, case-insensitive matching handled at pattern level.
    
    Args:
        ac_id: AC ID string to validate
    
    Returns:
        True if valid format, False otherwise
    """
    # Match pattern: one or more digits, dot, one or more digits
    # Must be exactly X.Y format (not X.Y.Z)
    pattern = r'^\d+\.\d+$'
    return bool(re.match(pattern, ac_id))


def generate_matrix_bulk(parsed_data: Dict, found_acs_by_report: Dict, observation_text: str, reports: list) -> Dict:
    """
    Generate matrix comparing found ACs against all ACs, with support for multiple reports.
    Creates separate rows for each report that covers an AC.
    
    Args:
        parsed_data: Parsed JSON standards data
        found_acs_by_report: Dict of AC IDs -> list of {report_name, ac_info} entries
                           Each entry represents one report covering that AC
        observation_text: Combined observation report text
        reports: List of report dicts with 'name' and 'text' keys
    
    Returns:
        Matrix data structure with separate rows for each report
    """
    from app.ac_matrix_parser import extract_all_acs
    
    # Get all ACs from standards
    all_acs = extract_all_acs(parsed_data)
    
    # Create set of found AC IDs for quick lookup
    found_ac_ids = set(found_acs_by_report.keys())
    
    # Build matrix by unit
    matrix_units = []
    total_ac_count = 0
    covered_ac_count = 0
    
    for unit in parsed_data.get('units', []):
        unit_id = unit.get('unit_id', '')
        unit_name = unit.get('unit_name', '')
        
        # First, collect all ACs in order (for standards row)
        all_unit_acs = []  # All ACs in order for standards row
        unit_total = 0
        
        # Map AC ID to its full info for quick lookup
        ac_info_map = {}
        
        for lo in unit.get('learning_outcomes', []):
            lo_number = lo.get('lo_number', '')
            
            for ac in lo.get('acs', []):
                ac_id = ac.get('ac_id', '')
                if not ac_id:
                    continue
                
                unit_total += 1
                total_ac_count += 1
                
                # Store AC info for standards row
                ac_info_map[ac_id] = {
                    "ac_id": ac_id,
                    "ac_description": ac.get('ac_description', ''),
                    "learning_outcome": lo_number
                }
                all_unit_acs.append(ac_id)
                
        # Build report coverage map: {report_name: {ac_id: ac_data}}
        # CRITICAL FIX: Use explicit unit-AC mappings from draft text (e.g., "641:1.1, 1.2")
        # If no explicit mapping, fall back to heuristic based on unique ACs
        report_coverage = {}
        for report in reports:
            report_name = report.get('name', 'Unknown Report')
            report_coverage[report_name] = {}
        
        # Get unit-AC mappings from report text (if available)
        # Structure: {report_name: {unit_id: [ac_ids]}}
        report_unit_mappings = {}
        for report in reports:
            report_name = report.get('name', 'Unknown Report')
            report_text = report.get('text', '')
            if report_text:
                unit_mappings = extract_unit_ac_mappings(report_text)
                if unit_mappings:
                    report_unit_mappings[report_name] = unit_mappings
                    logger.info(f"Found explicit unit mappings for {report_name}: {unit_mappings}")
                else:
                    logger.info(f"No explicit unit mappings found for {report_name}, will use heuristic")
        
        # Build map of which units each AC belongs to (for fallback heuristic)
        all_units_acs_map = {}  # {ac_id: [unit_ids]}
        for u in parsed_data.get('units', []):
            u_id = u.get('unit_id', '')
            for lo in u.get('learning_outcomes', []):
                for ac in lo.get('acs', []):
                    ac_id = ac.get('ac_id', '')
                    if ac_id:
                        if ac_id not in all_units_acs_map:
                            all_units_acs_map[ac_id] = []
                        if u_id not in all_units_acs_map[ac_id]:
                            all_units_acs_map[ac_id].append(u_id)
        
        # Determine which units qualify for each report
        # Priority 1: Explicit unit mappings from text (e.g., "641:1.1, 1.2")
        # Priority 2: Show coverage in ALL units that have the mentioned ACs (no filtering)
        unit_qualifies_for_reports = {}  # {report_name: {unit_id: bool}}
        
        for report in reports:
            report_name = report.get('name', 'Unknown Report')
            unit_qualifies_for_reports[report_name] = {}
            
            # Check if we have explicit unit mappings for this report
            if report_name in report_unit_mappings and report_unit_mappings[report_name]:
                # Use explicit mappings - only show coverage in explicitly mentioned units
                # Map short unit IDs (e.g., "4") to full unit IDs (e.g., "129v4")
                explicit_unit_keys = set(report_unit_mappings[report_name].keys())
                logger.info(f"Using explicit unit mappings for {report_name}: {explicit_unit_keys}")
                
                # Build a map of which full unit IDs match the explicit mappings
                matched_full_unit_ids = set()
                for u in parsed_data.get('units', []):
                    u_id = u.get('unit_id', '')
                    # Try exact match first
                    if u_id in explicit_unit_keys:
                        matched_full_unit_ids.add(u_id)
                    else:
                        # Try to match short unit IDs (e.g., "4" -> "129v4")
                        for mapping_key in explicit_unit_keys:
                            # Check if full unit_id ends with mapping_key or contains it
                            if u_id.endswith(mapping_key) or mapping_key in u_id:
                                matched_full_unit_ids.add(u_id)
                                logger.debug(f"Matched short unit ID '{mapping_key}' to full unit ID '{u_id}'")
                                break
                
                logger.info(f"Mapped explicit unit keys to full unit IDs: {matched_full_unit_ids}")
                for u in parsed_data.get('units', []):
                    u_id = u.get('unit_id', '')
                    unit_qualifies_for_reports[report_name][u_id] = u_id in matched_full_unit_ids
            else:
                # Fall back: show coverage in ALL units that have at least one of the found ACs
                # This ensures that if a draft mentions ACs from multiple units, all those units show coverage
                logger.info(f"Using per-unit check for {report_name} (no explicit mappings)")
                
                # We'll check per unit in the loop below
                # For now, mark all units as potentially qualifying (will be checked per unit)
                for u in parsed_data.get('units', []):
                    u_id = u.get('unit_id', '')
                    unit_qualifies_for_reports[report_name][u_id] = True  # Will be checked per unit
        
        # Fill in coverage data for each report
        # CRITICAL: If we have explicit unit mappings but no ACs found in observation text,
        # we should still create coverage entries from the unit mappings
        logger.info(f"Processing unit {unit_id}: {len(found_ac_ids)} ACs found in text, {len(report_unit_mappings)} reports with mappings")
        
        # First, process ACs found in observation text (after bracket stripping)
        for ac_id in found_ac_ids:
            # Only process if this AC ID exists in the current unit's standards
            if ac_id in ac_info_map:
                ac_entries = found_acs_by_report[ac_id]
                for ac_entry in ac_entries:
                    report_name = ac_entry.get('report_name', 'Unknown Report')
                    
                    # Determine if this AC should be shown for this unit
                    unit_qualifies = False
                    
                    # Priority 1: Check explicit unit mappings (e.g., "641:1.1, 1.2")
                    if report_name in report_unit_mappings and report_unit_mappings[report_name]:
                        unit_mapping = report_unit_mappings[report_name]
                        
                        # Try exact match first
                        matched_unit_key = None
                        if unit_id in unit_mapping:
                            matched_unit_key = unit_id
                        else:
                            # Try to match short unit IDs (e.g., "4" -> "129v4")
                            # Check if unit_id ends with the mapping key, or contains it
                            for mapping_key in unit_mapping.keys():
                                # Check if full unit_id ends with mapping_key (e.g., "129v4" ends with "4")
                                if unit_id.endswith(mapping_key) or mapping_key in unit_id:
                                    matched_unit_key = mapping_key
                                    logger.debug(f"Matched short unit ID '{mapping_key}' to full unit ID '{unit_id}'")
                                    break
                        
                        if matched_unit_key and matched_unit_key in unit_mapping:
                            # This unit is explicitly mentioned - only show ACs that are in the mapping
                            if ac_id in unit_mapping[matched_unit_key]:
                                unit_qualifies = True
                                logger.debug(f"AC {ac_id} qualifies for unit {unit_id} in {report_name} (explicit mapping via '{matched_unit_key}')")
                            else:
                                logger.debug(f"AC {ac_id} does NOT qualify for unit {unit_id} in {report_name} (not in explicit mapping)")
                        else:
                            logger.debug(f"Unit {unit_id} not in explicit mappings for {report_name}, skipping")
                    else:
                        # Priority 2: If no explicit mappings, show AC if it exists in this unit's standards
                        # This ensures all units that have the mentioned ACs will show coverage
                        unit_qualifies = True  # AC exists in this unit's standards (checked by ac_id in ac_info_map)
                        logger.debug(f"AC {ac_id} qualifies for unit {unit_id} in {report_name} (exists in unit standards)")
                    
                    if unit_qualifies and report_name in report_coverage:
                        report_coverage[report_name][ac_id] = {
                            "ac_id": ac_id,
                            "ac_description": ac_info_map[ac_id]["ac_description"],
                            "learning_outcome": ac_info_map[ac_id]["learning_outcome"],
                            "status": "covered",
                            "report_name": report_name,
                            "matched_text": ac_entry.get("matched_text", ""),
                            "section_title": ac_entry.get("section_title", ""),
                            "section_index": ac_entry.get("section_index", -1),
                            "observation_text_section": ac_entry.get("observation_text_section", ""),
                            "observation_context_start": ac_entry.get("context_start", 0),
                            "observation_context_end": ac_entry.get("context_end", 0),
                            "full_section": ac_entry.get("full_section", True)
                        }
                        logger.debug(f"Added AC {ac_id} to coverage for unit {unit_id} in {report_name}")
        
        # Second, if we have explicit unit mappings but no ACs found in text,
        # create coverage entries from the unit mappings
        for report_name, unit_mapping in report_unit_mappings.items():
            if report_name not in report_coverage:
                continue
            
            # Try to match this unit to the mapping
            matched_unit_key = None
            # First try exact match
            if unit_id in unit_mapping:
                matched_unit_key = unit_id
                logger.debug(f"Exact match: unit '{unit_id}' found in mapping")
            else:
                # Try to match unit IDs (e.g., "129v4" matches "129v4" or "129")
                # Priority: exact match > ends with > contains
                for mapping_key in unit_mapping.keys():
                    # Try exact match (already checked above, but keep for clarity)
                    if unit_id == mapping_key:
                        matched_unit_key = mapping_key
                        logger.debug(f"Exact match: unit '{unit_id}' == mapping key '{mapping_key}'")
                        break
                    # Try if unit_id ends with mapping_key (e.g., "129v4" ends with "v4")
                    elif unit_id.endswith(mapping_key):
                        matched_unit_key = mapping_key
                        logger.debug(f"Ends-with match: unit '{unit_id}' ends with mapping key '{mapping_key}'")
                        break
                    # Try if mapping_key is a prefix of unit_id (e.g., "129" is prefix of "129v4")
                    elif unit_id.startswith(mapping_key) and (len(mapping_key) < len(unit_id)):
                        # Additional check: make sure it's not just a partial number match
                        # e.g., "129" should match "129v4" but "12" shouldn't match "129v4"
                        next_char = unit_id[len(mapping_key)] if len(unit_id) > len(mapping_key) else ''
                        if next_char in ['v', 'V', '-', '_', ':', ' '] or not next_char.isdigit():
                            matched_unit_key = mapping_key
                            logger.debug(f"Prefix match: unit '{unit_id}' starts with mapping key '{mapping_key}'")
                            break
            
            if matched_unit_key and matched_unit_key in unit_mapping:
                # This unit is in the mapping - create coverage for all ACs in the mapping
                for ac_id in unit_mapping[matched_unit_key]:
                    # Only add if AC exists in this unit's standards and not already added
                    if ac_id in ac_info_map and ac_id not in report_coverage[report_name]:
                        report_coverage[report_name][ac_id] = {
                            "ac_id": ac_id,
                            "ac_description": ac_info_map[ac_id]["ac_description"],
                            "learning_outcome": ac_info_map[ac_id]["learning_outcome"],
                            "status": "covered",
                            "report_name": report_name,
                            "matched_text": "",  # No text match since it came from brackets
                            "section_title": "",  # No section since it came from brackets
                            "section_index": -1,
                            "observation_text_section": "",  # No observation text since it came from brackets
                            "observation_context_start": 0,
                            "observation_context_end": 0,
                            "full_section": True
                        }
                        logger.debug(f"Added AC {ac_id} to coverage for unit {unit_id} in {report_name} from unit mapping (matched via '{matched_unit_key}')")
        
        # Log coverage summary for this unit
        for report_name, coverage in report_coverage.items():
            if coverage:
                logger.info(f"Unit {unit_id} - {report_name}: {len(coverage)} ACs covered: {list(coverage.keys())}")
            else:
                logger.info(f"Unit {unit_id} - {report_name}: No ACs covered")
        
        # Determine which ACs are actually covered in this unit (after mapping)
        unit_covered_ac_ids = set()
        for coverage in report_coverage.values():
            unit_covered_ac_ids.update(coverage.keys())
        
        if all_unit_acs:  # Only add unit if it has ACs
            matrix_units.append({
                "unit_id": unit_id,
                "unit_name": unit_name,
                "total_ac_count": unit_total,
                "covered_ac_count": len(unit_covered_ac_ids),  # Unique ACs covered after mapping
                "missing_ac_count": unit_total - len(unit_covered_ac_ids),
                "all_acs": all_unit_acs,  # All ACs in order for standards row
                "ac_info_map": ac_info_map,  # AC details for standards row
                "report_coverage": report_coverage  # Coverage by report
            })
            covered_ac_count += len(unit_covered_ac_ids)
    
    # Calculate overall statistics
    missing_ac_count = total_ac_count - covered_ac_count
    coverage_percentage = (covered_ac_count / total_ac_count * 100) if total_ac_count > 0 else 0.0
    
    matrix_data = {
        "total_ac_count": total_ac_count,
        "covered_ac_count": covered_ac_count,
        "missing_ac_count": missing_ac_count,
        "coverage_percentage": round(coverage_percentage, 1),
        "units": matrix_units,
        "report_count": len(reports),
        "report_names": [r.get('name', 'Unknown') for r in reports]
    }
    
    logger.info(f"Bulk matrix generated: {covered_ac_count}/{total_ac_count} ACs covered ({coverage_percentage:.1f}%) from {len(reports)} reports")
    
    return matrix_data

