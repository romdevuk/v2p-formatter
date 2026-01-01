"""
Test section extraction to verify only section text is extracted
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.ac_matrix_analyzer import extract_ac_references_with_context, find_section_boundaries

# Test observation text with multiple sections
test_text = """SECTION: Site Induction

During the site induction, AC 1.1 was covered when the site manager explained the workplace procedures. 
The operative demonstrated understanding of AC 1.2 by using safety equipment correctly.
AC 1.3 was not mentioned in this observation.

SECTION: Hazard Reporting

Hazards were reported in accordance with AC 2.1 when a potential risk was identified during the work.
AC 3.1, 3.2, and 3.3 were not covered in this observation.

SECTION: Equipment Use

AC 7.1 was demonstrated when the operative used tools correctly."""

print("=" * 70)
print("Testing Section Extraction")
print("=" * 70)

# Test section boundaries
print("\n1. Testing Section Boundaries:")
print("-" * 70)
for i, char in enumerate(test_text):
    if char == 'A' and test_text[i:i+3] == 'AC ':
        bounds = find_section_boundaries(test_text, i)
        section_start = bounds['start']
        section_end = bounds['end']
        section_text = test_text[section_start:section_end]
        print(f"\nPosition {i} (AC found here):")
        print(f"  Section boundaries: {section_start} to {section_end}")
        print(f"  Section text length: {len(section_text)} chars")
        print(f"  Section text preview: {section_text[:100]}...")
        break

# Test AC extraction
print("\n2. Testing AC Extraction:")
print("-" * 70)
found_acs = extract_ac_references_with_context(test_text, context_window=150)

for ac_id, ac_info in sorted(found_acs.items()):
    print(f"\nAC {ac_id}:")
    print(f"  Section: {ac_info.get('section_title', 'N/A')}")
    print(f"  Text section length: {len(ac_info.get('observation_text_section', ''))} chars")
    text_section = ac_info.get('observation_text_section', '')
    print(f"  Text preview (first 200 chars):")
    print(f"    {text_section[:200]}...")
    
    # Check if text contains other sections
    if 'SECTION:' in text_section.upper():
        sections_in_text = []
        import re
        for match in re.finditer(r'SECTION\s*[:-]?\s*(.+)', text_section, re.IGNORECASE | re.MULTILINE):
            sections_in_text.append(match.group(1).strip())
        if len(sections_in_text) > 1:
            print(f"  ⚠️  WARNING: Contains multiple sections: {sections_in_text}")
        elif len(sections_in_text) == 1:
            print(f"  ✓ Contains only one section: {sections_in_text[0]}")
    else:
        print(f"  ✓ No section markers found (good)")

print("\n" + "=" * 70)




