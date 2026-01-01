"""
Test that extraction only gets text from the relevant section
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.ac_matrix_analyzer import extract_ac_references_with_context

# Test text with multiple sections
test_text = """SECTION: 1 - SITE ARRIVAL AND INDUCTION

He already wore full PPE: high-viz, hard hat, gloves, boots and glasses. Ivan showed me fire point and health & safety board. AC covered: 641:1.1, 1.2, 1.3, 2.1, 4.1; 642:1.1 Image suggestion: learner signing in and wearing PPE.

{{Site_arrival_and_induction_table}} 2. Inside the induction room Ivan displayed CSCS card, signed RAMS and daily sheet. I observed learner storing PPE and small tools correctly in tool bag. AC covered: 641:5.1; 642:1.1, 4.1 Image suggestion: induction paperwork and CSCS verification.

{{Site_arrival_and_induction_table}} SECTION 2 – HEALTH, SAFETY AND WELFARE 3. On way to work area Ivan spotted wires loose on floor. We discussed emergency actions and he explained he must raise alarm, go assembly point and call supervisor if safe. AC covered: 641:3.2, 4.1; 643:11 Image suggestion inspection of hon-up

SECTION 3 – COMMUNICATION AND WORK COORDINATION

Ivan spoke politely to supervisor and colleagues, confirming work sequence and access needs.

SECTION 5 – INSTALLATION OF DRYLINING SYSTEMS

Ivan installed metal stud partition: measuring, marking, fixing track, positioning studs, and securing them, following drawings and RAMS. AC covered: 129v4:1.1, 1.2, 3.1, 3.2, 4.1; 642:2.1 Image suggestion: learner fixing metal studs. Question asked about furring ceilings, lining systems, and encasements.

SECTION 6 - PLASTERBOARD FIXING

Ivan fixed plasterboard to metal studs: measured, cut, aligned, and screwed boards with correct spacing and formed opening. AC covered: 130v3:1.1, 1.2, 3.1, 3.2, 4.1 Image suggestion: correct screw pattern on plasterboard. Question asked about direct bonding.

SECTION 10 - WELFARE AND END-OF-SHIFT ACTIVITIES

Ivan cleaned the table and kept the area tidy. Reviewed evidence and discussed knowledge questions Ivan still needs to complete. AC covered: 641:3.2; 642:1.1; 643:7.2 Image suggestion: clean welfare table area."""

print("=" * 70)
print("Testing Section-Only Extraction for AC 1.1")
print("=" * 70)

found = extract_ac_references_with_context(test_text)
ac = found.get('1.1', {})

print(f"\nAC 1.1 found: {ac.get('ac_id')}")
print(f"Section: {ac.get('section_title', 'N/A')}")
print(f"Text length: {len(ac.get('observation_text_section', ''))} chars")
print(f"\nExtracted text:")
print("-" * 70)
text = ac.get('observation_text_section', '')
print(text)
print("-" * 70)

# Check for other sections
import re
other_sections = re.findall(r'SECTION\s*\d+\s*[–-]?\s*(.+)', text, re.IGNORECASE | re.MULTILINE)
if other_sections:
    print(f"\n⚠️  WARNING: Found other sections in text: {other_sections}")
else:
    print(f"\n✓ No other sections found in extracted text")

# Check section boundaries
section_start = text.find('SECTION')
if section_start >= 0:
    print(f"\n⚠️  WARNING: Text still contains 'SECTION' marker at position {section_start}")

print("\n" + "=" * 70)




