"""
Test script to verify AC Matrix correctly handles explicit unit mappings
Tests with the actual draft text format: "641:1.1, 1.2, 1.3, 2.1, 4.1; 642:1.1"
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.ac_matrix_parser import parse_standards_json
from app.ac_matrix_analyzer import extract_ac_references_with_context, extract_unit_ac_mappings, generate_matrix_bulk
from config import AC_MATRIX_JSON_STANDARDS_DIR

def test_explicit_unit_mappings():
    """Test that matrix correctly uses explicit unit mappings from draft text"""
    
    # Load JSON standards
    json_file = AC_MATRIX_JSON_STANDARDS_DIR / 'l2inter-performance.json'
    if not json_file.exists():
        print(f"ERROR: JSON file not found: {json_file}")
        return
    
    parsed_data = parse_standards_json(json_file)
    
    # Test with actual draft text format
    test_draft = """SECTION 1 – SITE ARRIVAL AND INDUCTION

1.

fdsgdfgfdgdf. I arrived to the project on agreed time, weather sunny. I met Ivan at the gate where he followed security rules by signing in and passing fenced access. He already wore full PPE: high-viz, hard hat, gloves, boots and glasses. Ivan showed me fire point and health & safety board.

AC covered: 

                641:1.1, 1.2, 1.3, 2.1, 4.1; 642:1.1

Image suggestion: learner signing in and wearing PPE.

{{Site_arrival_and_induction_table}}

2.

Inside the induction room Ivan displayed CSCS card, signed RAMS and daily sheet. I observed learner storing PPE and small tools correctly in tool bag.

AC covered: 

                641:5.1; 642:1.1, 4.1

Image suggestion: induction paperwork and CSCS verification.

{{Site_arrival_and_induction_table}}
"""
    
    print("=== Testing with Explicit Unit Mappings ===")
    print(f"\nDraft Text:\n{test_draft[:200]}...")
    
    # Extract unit mappings
    unit_mappings = extract_unit_ac_mappings(test_draft)
    print(f"\nExtracted Unit Mappings: {unit_mappings}")
    
    # Extract ACs
    found_acs = extract_ac_references_with_context(test_draft)
    print(f"Extracted ACs: {list(found_acs.keys())}")
    
    # Prepare data for bulk matrix
    all_found_acs_by_report = {}
    for ac_id, ac_info in found_acs.items():
        all_found_acs_by_report[ac_id] = [{
            **ac_info,
            'report_name': '2ndobsMy Draft',
            'unit_id': None  # Will be determined by unit mappings
        }]
    
    reports = [{'name': '2ndobsMy Draft', 'text': test_draft}]
    
    # Generate matrix
    matrix_data = generate_matrix_bulk(parsed_data, all_found_acs_by_report, test_draft, reports)
    
    # Check results
    print("\n=== Matrix Results ===")
    expected_units = {'641', '642'}  # Should only show these units
    
    for unit in matrix_data.get('units', []):
        unit_id = unit.get('unit_id', '')
        unit_name = unit.get('unit_name', '')
        all_acs = unit.get('all_acs', [])
        report_coverage = unit.get('report_coverage', {})
        
        print(f"\nUnit {unit_id}: {unit_name}")
        
        for report_name, coverage in report_coverage.items():
            covered_acs = list(coverage.keys())
            if covered_acs:
                print(f"  {report_name} covers: {', '.join(sorted(covered_acs))}")
                
                # Verify unit is in expected list
                if unit_id in expected_units:
                    print(f"  ✅ Correctly shows coverage for unit {unit_id}")
                else:
                    print(f"  ❌ ERROR: Unit {unit_id} should NOT show coverage!")
                    print(f"    Expected units: {expected_units}")
            else:
                if unit_id in expected_units:
                    print(f"  ❌ ERROR: Unit {unit_id} should show coverage but doesn't!")
                else:
                    print(f"  ✅ Correctly shows no coverage (unit {unit_id} not in draft)")

if __name__ == '__main__':
    test_explicit_unit_mappings()




