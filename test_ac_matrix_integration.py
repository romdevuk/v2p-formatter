"""
Integration Test for AC Matrix Module
Tests complete workflow end-to-end
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.ac_matrix_parser import parse_standards_json, extract_all_acs
from app.ac_matrix_analyzer import extract_ac_references_with_context, generate_matrix
from app.ac_matrix_storage import save_matrix, list_matrices, load_matrix, delete_matrix
from config import AC_MATRIX_JSON_STANDARDS_DIR

def test_complete_workflow():
    """Test complete AC Matrix workflow"""
    print("=" * 70)
    print("AC Matrix - Complete Integration Test")
    print("=" * 70)
    
    # Step 1: Parse JSON file
    print("\n[Step 1] Parsing JSON Standards File...")
    json_file = AC_MATRIX_JSON_STANDARDS_DIR / 'l2inter-performance.json'
    if not json_file.exists():
        print(f"   ✗ JSON file not found: {json_file}")
        return False
    
    try:
        parsed_data = parse_standards_json(json_file)
        print(f"   ✓ Qualification: {parsed_data['qualification_name']}")
        print(f"   ✓ Units: {len(parsed_data['units'])}")
        
        all_acs = extract_all_acs(parsed_data)
        print(f"   ✓ Total ACs: {len(all_acs)}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 2: Create observation report with sections
    print("\n[Step 2] Creating Observation Report...")
    observation_text = """SECTION: Site Induction

During the site induction, AC 1.1 was covered when the site manager explained the workplace procedures. 
The operative demonstrated understanding of AC 1.2 by using safety equipment correctly.
AC 1.3 was not mentioned in this observation.

SECTION: Hazard Reporting

Hazards were reported in accordance with AC 2.1 when a potential risk was identified during the work.
AC 3.1, 3.2, and 3.3 were not covered in this observation.

SECTION: Equipment Use

AC 7.1 was demonstrated when the operative used tools correctly."""
    
    print(f"   ✓ Observation text created ({len(observation_text)} characters)")
    
    # Step 3: Extract AC references
    print("\n[Step 3] Extracting AC References...")
    try:
        found_acs = extract_ac_references_with_context(observation_text)
        print(f"   ✓ Found ACs: {sorted(found_acs.keys())}")
        
        for ac_id in sorted(found_acs.keys()):
            ac_info = found_acs[ac_id]
            section = ac_info.get('section_title', 'N/A')
            print(f"     - AC {ac_id}: Section '{section}' (index: {ac_info.get('section_index', -1)})")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 4: Generate matrix
    print("\n[Step 4] Generating Matrix...")
    try:
        matrix_data = generate_matrix(parsed_data, found_acs, observation_text)
        print(f"   ✓ Total ACs: {matrix_data['total_ac_count']}")
        print(f"   ✓ Covered: {matrix_data['covered_ac_count']}")
        print(f"   ✓ Missing: {matrix_data['missing_ac_count']}")
        print(f"   ✓ Coverage: {matrix_data['coverage_percentage']}%")
        print(f"   ✓ Units: {len(matrix_data['units'])}")
        
        # Verify section titles in covered ACs
        covered_with_sections = 0
        for unit in matrix_data['units']:
            for ac in unit['acs']:
                if ac['status'] == 'covered' and ac.get('section_title'):
                    covered_with_sections += 1
        
        print(f"   ✓ Covered ACs with section titles: {covered_with_sections}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 5: Save matrix
    print("\n[Step 5] Saving Matrix...")
    try:
        save_result = save_matrix(
            matrix_data,
            'Integration Test Matrix',
            'l2inter-performance',
            'l2inter-performance.json',
            observation_text
        )
        
        if save_result['success']:
            matrix_id = save_result['matrix_id']
            print(f"   ✓ Matrix saved with ID: {matrix_id}")
        else:
            print(f"   ✗ Save failed: {save_result.get('error')}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 6: List matrices
    print("\n[Step 6] Listing Saved Matrices...")
    try:
        matrices = list_matrices()
        print(f"   ✓ Found {len(matrices)} saved matrix(es)")
        if matrices:
            print(f"     - Latest: {matrices[0]['name']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 7: Load matrix
    print("\n[Step 7] Loading Saved Matrix...")
    try:
        load_result = load_matrix(matrix_id)
        if load_result['success']:
            loaded_data = load_result['matrix_data']
            print(f"   ✓ Matrix loaded: {loaded_data['name']}")
            print(f"   ✓ Coverage: {loaded_data['analysis']['coverage_percentage']}%")
            print(f"   ✓ Observation report length: {len(loaded_data['observation_report'])} chars")
        else:
            print(f"   ✗ Load failed: {load_result.get('error')}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 8: Delete matrix
    print("\n[Step 8] Deleting Test Matrix...")
    try:
        delete_result = delete_matrix(matrix_id)
        if delete_result['success']:
            print(f"   ✓ Matrix deleted successfully")
        else:
            print(f"   ✗ Delete failed: {delete_result.get('error')}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 9: Verify deletion
    print("\n[Step 9] Verifying Deletion...")
    try:
        matrices_after = list_matrices()
        test_matrix_exists = any(m['matrix_id'] == matrix_id for m in matrices_after)
        if not test_matrix_exists:
            print(f"   ✓ Matrix successfully removed from list")
        else:
            print(f"   ✗ Matrix still in list")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✓ ALL INTEGRATION TESTS PASSED!")
    print("=" * 70)
    print("\nReady for screenshot testing:")
    print("1. Start server: python run.py")
    print("2. Navigate to: http://localhost/v2p-formatter/ac-matrix")
    print("3. Test complete workflow and capture screenshots")
    print("=" * 70)
    
    return True

if __name__ == '__main__':
    success = test_complete_workflow()
    sys.exit(0 if success else 1)




