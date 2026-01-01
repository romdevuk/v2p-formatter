"""
Test script to verify AC Matrix only shows ACs from the correct unit
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.ac_matrix_parser import parse_standards_json
from app.ac_matrix_analyzer import extract_ac_references_with_context, generate_matrix_bulk
from config import AC_MATRIX_JSON_STANDARDS_DIR

def test_unit_filtering():
    """Test that matrix only shows ACs from the unit where they're covered"""
    
    # Load JSON standards
    json_file = AC_MATRIX_JSON_STANDARDS_DIR / 'l2inter-performance.json'
    if not json_file.exists():
        print(f"ERROR: JSON file not found: {json_file}")
        return
    
    parsed_data = parse_standards_json(json_file)
    
    # Print all units and their ACs
    print("\n=== All Units and ACs in Standards ===")
    for unit in parsed_data.get('units', []):
        unit_id = unit.get('unit_id', '')
        unit_name = unit.get('unit_name', '')
        print(f"\nUnit {unit_id}: {unit_name}")
        
        all_acs = []
        for lo in unit.get('learning_outcomes', []):
            for ac in lo.get('acs', []):
                ac_id = ac.get('ac_id', '')
                if ac_id:
                    all_acs.append(ac_id)
        print(f"  ACs: {', '.join(sorted(all_acs))}")
    
    # Test with a draft that only covers unit 641
    print("\n=== Testing with Draft that Only Covers Unit 641 ===")
    
    # Create test draft text with only ACs from unit 641
    # First, find which ACs belong to unit 641
    unit_641_acs = []
    for unit in parsed_data.get('units', []):
        if unit.get('unit_id') == '641':
            for lo in unit.get('learning_outcomes', []):
                for ac in lo.get('acs', []):
                    ac_id = ac.get('ac_id', '')
                    if ac_id:
                        unit_641_acs.append(ac_id)
            break
    
    print(f"Unit 641 ACs: {', '.join(sorted(unit_641_acs))}")
    
    # Create draft text with only unit 641 ACs
    test_draft = f"""
SECTION: Test Section

This observation covers the following assessment criteria: {', '.join(unit_641_acs[:5])}.

AC {unit_641_acs[0]} was covered when...
AC {unit_641_acs[1]} was demonstrated...
"""
    
    print(f"\nTest Draft Text:\n{test_draft}")
    
    # Extract ACs from draft
    found_acs = extract_ac_references_with_context(test_draft)
    print(f"\nExtracted ACs from draft: {list(found_acs.keys())}")
    
    # Prepare data for bulk matrix
    all_found_acs_by_report = {}
    for ac_id, ac_info in found_acs.items():
        all_found_acs_by_report[ac_id] = [{
            **ac_info,
            'report_name': 'Test Draft'
        }]
    
    reports = [{'name': 'Test Draft', 'text': test_draft}]
    
    # Generate matrix
    matrix_data = generate_matrix_bulk(parsed_data, all_found_acs_by_report, test_draft, reports)
    
    # Check results
    print("\n=== Matrix Results ===")
    for unit in matrix_data.get('units', []):
        unit_id = unit.get('unit_id', '')
        unit_name = unit.get('unit_name', '')
        all_acs = unit.get('all_acs', [])
        report_coverage = unit.get('report_coverage', {})
        
        print(f"\nUnit {unit_id}: {unit_name}")
        print(f"  Standards ACs: {', '.join(all_acs)}")
        
        for report_name, coverage in report_coverage.items():
            covered_acs = list(coverage.keys())
            print(f"  {report_name} covers: {', '.join(sorted(covered_acs))}")
            
            # Check if unit 641 shows ACs from other units
            if unit_id == '641':
                # All covered ACs should be in unit 641's AC list
                invalid_acs = [ac for ac in covered_acs if ac not in all_acs]
                if invalid_acs:
                    print(f"  ❌ ERROR: Unit 641 shows ACs not in its standards: {invalid_acs}")
                else:
                    print(f"  ✅ All covered ACs are valid for unit 641")
            else:
                # Other units should not show any coverage if draft only has unit 641 ACs
                if covered_acs:
                    print(f"  ❌ ERROR: Unit {unit_id} shows coverage but draft only has unit 641 ACs!")
                    print(f"    Covered ACs: {covered_acs}")
                else:
                    print(f"  ✅ No coverage shown (correct - draft doesn't cover this unit)")

if __name__ == '__main__':
    test_unit_filtering()




