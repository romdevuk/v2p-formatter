"""
Test AC extraction to verify each AC only gets text from its section
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.ac_matrix_analyzer import extract_ac_references_with_context, find_section_boundaries

# Test text with multiple sections and multiple ACs
test_text = """SECTION: 1 - SITE ARRIVAL AND INDUCTION

He already wore full PPE: high-viz, hard hat, gloves, boots and glasses. Ivan showed me fire point and health & safety board. AC covered: 641:1.1, 1.2, 1.3, 2.1, 4.1; 642:1.1 Image suggestion: learner signing in and wearing PPE.

{{Site_arrival_and_induction_table}} 2. Inside the induction room Ivan displayed CSCS card, signed RAMS and daily sheet. I observed learner storing PPE and small tools correctly in tool bag. AC covered: 641:5.1; 642:1.1, 4.1 Image suggestion: induction paperwork and CSCS verification.

{{Site_arrival_and_induction_table}} SECTION 2 – HEALTH, SAFETY AND WELFARE 3. On way to work area Ivan spotted wires loose on floor. We discussed emergency actions and he explained he must raise alarm, go assembly point and call supervisor if safe. AC covered: 641:3.2, 4.1; 643:11 Image suggestion inspection of hon-up

SECTION 3 – COMMUNICATION AND WORK COORDINATION

Ivan spoke politely to supervisor and colleagues, confirming work sequence and access needs.

SECTION 5 – INSTALLATION OF DRYLINING SYSTEMS

Ivan installed metal stud partition: measuring, marking, fixing track, positioning studs, and securing them, following drawings and RAMS. AC covered: 129v4:1.1, 1.2, 3.1, 3.2, 4.1; 642:2.1 Image suggestion: learner fixing metal studs."""

print("=" * 70)
print("Testing AC Section Extraction")
print("=" * 70)

# Extract ACs
found_acs = extract_ac_references_with_context(test_text)

# Check each AC
for ac_id in sorted(found_acs.keys()):
    ac = found_acs[ac_id]
    text = ac.get('observation_text_section', '')
    section = ac.get('section_title', 'N/A')
    
    print(f"\nAC {ac_id}:")
    print(f"  Section: {section}")
    print(f"  Text length: {len(text)} chars")
    
    # Check for other sections
    import re
    other_sections = re.findall(r'SECTION\s*\d+\s*[–-]?\s*([^\n]+)', text, re.IGNORECASE)
    if other_sections:
        print(f"  ⚠️  WARNING: Contains other section markers: {other_sections}")
    
    # Check if text contains section 2, 3, 5 (should only have section 1 for ACs 1.1, 1.2, etc.)
    if section == "1 - SITE ARRIVAL AND INDUCTION":
        if "SECTION 2" in text or "SECTION 3" in text or "SECTION 5" in text:
            print(f"  ⚠️  WARNING: Section 1 AC contains text from other sections!")
    
    # Show first 150 chars
    print(f"  Text preview: {text[:150]}...")

print("\n" + "=" * 70)




