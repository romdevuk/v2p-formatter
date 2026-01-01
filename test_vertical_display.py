"""
Test what data is actually sent to frontend for vertical display
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.ac_matrix_parser import parse_standards_json, extract_all_acs
from app.ac_matrix_analyzer import extract_ac_references_with_context, generate_matrix
from config import AC_MATRIX_JSON_STANDARDS_DIR

# Test with longer observation text that has multiple sections
test_text = """SECTION: Site Induction

He already wore full PPE: high-viz, hard hat, gloves, boots and glasses. Ivan showed me fire point and health & safety board. AC covered: 641:1.1, 1.2, 1.3, 2.1, 4.1; 642:1.1 Image suggestion: learner signing in and wearing PPE.

{{Site_arrival_and_induction_table}} 2. Inside the induction room Ivan displayed CSCS card, signed RAMS and daily sheet. I observed learner storing PPE and small tools correctly in tool bag. AC covered: 641:5.1; 642:1.1, 4.1 Image suggestion: induction paperwork and CSCS verification.

{{Site_arrival_and_induction_table}} SECTION 2 – HEALTH, SAFETY AND WELFARE 3. On way to work area Ivan spotted wires loose on floor. We discussed emergency actions and he explained he must raise alarm, go assembly point and call supervisor if safe. AC covered: 641:3.2, 4.1; 643:11 Image suggestion inspection of hon-up"""

print("=" * 70)
print("Testing Vertical Display Data")
print("=" * 70)

# Parse JSON
json_file = AC_MATRIX_JSON_STANDARDS_DIR / 'l2inter-performance.json'
if not json_file.exists():
    print(f"JSON file not found: {json_file}")
    sys.exit(1)

parsed_data = parse_standards_json(json_file)

# Extract ACs
found_acs = extract_ac_references_with_context(test_text)

# Generate matrix
matrix_data = generate_matrix(parsed_data, found_acs, test_text)

# Check what's in the matrix data for vertical display
print("\nMatrix Data for Vertical Display:")
print("-" * 70)

for unit in matrix_data['units']:
    print(f"\nUnit: {unit['unit_name']}")
    for ac in unit['acs'][:5]:  # First 5 ACs
        if ac['status'] == 'covered':
            text_section = ac.get('observation_text_section', '')
            print(f"\n  AC {ac['ac_id']}:")
            print(f"    Section: {ac.get('section_title', 'N/A')}")
            print(f"    Text length: {len(text_section)} chars")
            print(f"    Text preview (first 200 chars):")
            print(f"      {text_section[:200]}...")
            
            # Check if it contains other sections
            if 'SECTION' in text_section.upper():
                import re
                sections = re.findall(r'SECTION\s*[:-]?\s*(.+)', text_section, re.IGNORECASE | re.MULTILINE)
                if len(sections) > 1:
                    print(f"    ⚠️  WARNING: Contains {len(sections)} section markers: {sections}")
                elif len(sections) == 1:
                    print(f"    ⚠️  WARNING: Contains section marker: {sections[0]}")
            else:
                print(f"    ✓ No section markers")
            
            # Check if text is longer than expected (more than 500 chars might be too much)
            if len(text_section) > 500:
                print(f"    ⚠️  WARNING: Text is very long ({len(text_section)} chars)")

print("\n" + "=" * 70)




