"""
Test script for Phase 1: Backend Core
Tests JSON parsing, AC extraction, and matrix generation
"""
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.ac_matrix_parser import parse_standards_json, extract_all_acs
from app.ac_matrix_analyzer import extract_ac_references_with_context, generate_matrix

def test_phase1():
    """Test Phase 1 backend core functionality"""
    print("=" * 60)
    print("Phase 1: Backend Core - Testing")
    print("=" * 60)
    
    # Test 1: Parse JSON file
    print("\n1. Testing JSON Parsing...")
    json_path = Path('docs/l2inter-performance.json')
    try:
        parsed_data = parse_standards_json(json_path)
        print(f"   ✓ Qualification: {parsed_data['qualification_name']}")
        print(f"   ✓ Units: {len(parsed_data['units'])}")
        
        all_acs = extract_all_acs(parsed_data)
        print(f"   ✓ Total ACs: {len(all_acs)}")
        print(f"   ✓ Sample ACs: {[ac['ac_id'] for ac in all_acs[:5]]}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 2: AC Extraction with sections
    print("\n2. Testing AC Extraction with Section Titles...")
    observation_text = """SECTION: Site Induction

During the site induction, AC 1.1 was covered when the site manager explained the procedures. 
The operative demonstrated understanding of AC 1.2 by using safety equipment correctly.

SECTION: Hazard Reporting

Hazards were reported in accordance with AC 2.1 when a potential risk was identified.
AC 3.1 was not covered in this observation."""
    
    try:
        found_acs = extract_ac_references_with_context(observation_text)
        print(f"   ✓ Found ACs: {list(found_acs.keys())}")
        
        for ac_id, ac_info in found_acs.items():
            section_title = ac_info.get('section_title', 'N/A')
            section_index = ac_info.get('section_index', -1)
            print(f"   ✓ AC {ac_id}: Section '{section_title}' (index: {section_index})")
            print(f"     Text snippet: {ac_info.get('observation_text_section', '')[:60]}...")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 3: Matrix Generation
    print("\n3. Testing Matrix Generation...")
    try:
        matrix_data = generate_matrix(parsed_data, found_acs, observation_text)
        print(f"   ✓ Total ACs: {matrix_data['total_ac_count']}")
        print(f"   ✓ Covered: {matrix_data['covered_ac_count']}")
        print(f"   ✓ Missing: {matrix_data['missing_ac_count']}")
        print(f"   ✓ Coverage: {matrix_data['coverage_percentage']}%")
        print(f"   ✓ Units in matrix: {len(matrix_data['units'])}")
        
        # Check first unit
        if matrix_data['units']:
            first_unit = matrix_data['units'][0]
            print(f"   ✓ First unit: {first_unit['unit_name'][:50]}...")
            print(f"     ACs: {first_unit['total_ac_count']} total, {first_unit['covered_ac_count']} covered")
            
            # Check a covered AC
            for ac in first_unit['acs']:
                if ac['status'] == 'covered':
                    print(f"   ✓ Covered AC example: {ac['ac_id']}")
                    print(f"     Section: {ac.get('section_title', 'N/A')}")
                    print(f"     Section index: {ac.get('section_index', -1)}")
                    break
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("Phase 1: Backend Core - All Tests Passed! ✓")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_phase1()
    sys.exit(0 if success else 1)




