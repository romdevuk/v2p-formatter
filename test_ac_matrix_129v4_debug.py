"""
Debug test for Unit 129v4 coverage issue
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.ac_matrix_parser import parse_standards_json
from app.ac_matrix_analyzer import extract_ac_references_with_context, extract_unit_ac_mappings, generate_matrix_bulk
from config import AC_MATRIX_JSON_STANDARDS_DIR
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_129v4_coverage():
    """Test why Unit 129v4 is not showing coverage"""
    
    # Load JSON standards
    json_file = AC_MATRIX_JSON_STANDARDS_DIR / 'l2inter-performance.json'
    if not json_file.exists():
        print(f"ERROR: JSON file not found: {json_file}")
        return
    
    parsed_data = parse_standards_json(json_file)
    
    # Find unit 129v4 and its ACs
    print("=== Unit 129v4 ACs ===")
    for unit in parsed_data.get('units', []):
        if unit.get('unit_id') == '129v4':
            print(f"Unit {unit.get('unit_id')}: {unit.get('unit_name')}")
            all_acs = []
            for lo in unit.get('learning_outcomes', []):
                for ac in lo.get('acs', []):
                    ac_id = ac.get('ac_id', '')
                    if ac_id:
                        all_acs.append(ac_id)
            print(f"  ACs: {', '.join(sorted(all_acs))}")
            break
    
    # Test with a draft that should cover unit 129v4
    # Unit 129v4 has: 1.1, 1.2, 3.1, 3.2, 4.1, 5.1, 5.2, 5.3, 6.1, 7.1, 7.2, 7.3, 7.4
    test_draft = """SECTION 1 – SITE ARRIVAL AND INDUCTION

1.

I arrived to the project on agreed time. I met Ivan at the gate where he followed security rules by signing in and passing fenced access. He already wore full PPE: high-viz, hard hat, gloves, boots and glasses.

AC 1.1 was covered when the site manager explained the procedures.
AC 1.2 was demonstrated during the site induction.
AC 3.1 was observed when the worker followed safety protocols.
AC 3.2 was covered when proper equipment was used.
AC 4.1 was demonstrated during the task.
AC 5.1 was covered.
AC 5.2 was demonstrated.
AC 5.3 was observed.
AC 6.1 was covered.
AC 7.1 was demonstrated.
AC 7.2 was covered.
AC 7.3 was observed.
AC 7.4 was demonstrated.
"""
    
    print("\n=== Testing Draft Coverage ===")
    
    # Extract unit mappings
    unit_mappings = extract_unit_ac_mappings(test_draft)
    print(f"Extracted Unit Mappings: {unit_mappings}")
    
    # Extract ACs
    found_acs = extract_ac_references_with_context(test_draft)
    print(f"Extracted ACs: {sorted(found_acs.keys())}")
    
    # Check which ACs from 129v4 are in the draft
    unit_129v4_acs = ['1.1', '1.2', '3.1', '3.2', '4.1', '5.1', '5.2', '5.3', '6.1', '7.1', '7.2', '7.3', '7.4']
    found_129v4_acs = [ac for ac in unit_129v4_acs if ac in found_acs]
    print(f"\nUnit 129v4 ACs found in draft: {found_129v4_acs}")
    print(f"Unit 129v4 ACs NOT found: {[ac for ac in unit_129v4_acs if ac not in found_acs]}")
    
    # Prepare data for bulk matrix
    all_found_acs_by_report = {}
    for ac_id, ac_info in found_acs.items():
        all_found_acs_by_report[ac_id] = [{
            **ac_info,
            'report_name': 'My Draft (2025-12-07)',
            'unit_id': None
        }]
    
    reports = [{'name': 'My Draft (2025-12-07)', 'text': test_draft}]
    
    # Generate matrix
    print("\n=== Generating Matrix ===")
    matrix_data = generate_matrix_bulk(parsed_data, all_found_acs_by_report, test_draft, reports)
    
    # Check results for unit 129v4
    print("\n=== Matrix Results for Unit 129v4 ===")
    for unit in matrix_data.get('units', []):
        if unit.get('unit_id') == '129v4':
            unit_id = unit.get('unit_id', '')
            unit_name = unit.get('unit_name', '')
            report_coverage = unit.get('report_coverage', {})
            
            print(f"Unit {unit_id}: {unit_name}")
            
            for report_name, coverage in report_coverage.items():
                covered_acs = list(coverage.keys())
                if covered_acs:
                    print(f"  ✅ {report_name} covers: {', '.join(sorted(covered_acs))} ({len(covered_acs)} ACs)")
                else:
                    print(f"  ❌ {report_name}: No coverage")
                    print(f"     Expected ACs: {', '.join(sorted(found_129v4_acs))}")
            break

if __name__ == '__main__':
    test_129v4_coverage()




