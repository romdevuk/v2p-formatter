"""
Test script to verify AC Matrix shows coverage when draft covers all units
Tests the case where a draft doesn't have explicit unit mappings but covers ACs from all units
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

def test_all_units_coverage():
    """Test that matrix shows coverage when draft covers ACs from all units without explicit mappings"""
    
    # Load JSON standards
    json_file = AC_MATRIX_JSON_STANDARDS_DIR / 'l2inter-performance.json'
    if not json_file.exists():
        print(f"ERROR: JSON file not found: {json_file}")
        return
    
    parsed_data = parse_standards_json(json_file)
    
    # Test with draft that covers ACs from multiple units but NO explicit unit mappings
    # This should use the heuristic to determine which units qualify
    test_draft = """SECTION 1 – SITE ARRIVAL AND INDUCTION

1.

I arrived to the project on agreed time. I met Ivan at the gate where he followed security rules by signing in and passing fenced access. He already wore full PPE: high-viz, hard hat, gloves, boots and glasses.

AC 1.1 was covered when the site manager explained the procedures.
AC 1.2 was demonstrated during the site induction.
AC 1.3 was observed when the worker followed safety protocols.
AC 2.1 was covered when proper equipment was used.
AC 3.1 was demonstrated during the task.
AC 3.2 was covered.
AC 3.3 was observed.
AC 3.4 was demonstrated.
AC 3.5 was covered.
AC 4.1 was observed.
AC 5.1 was demonstrated.

Inside the induction room Ivan displayed CSCS card, signed RAMS and daily sheet. I observed learner storing PPE and small tools correctly in tool bag.

AC 1.1 was covered again (different unit).
AC 2.1 was covered.
AC 2.2 was demonstrated.
AC 3.1 was observed.
AC 4.1 was covered.
AC 4.2 was demonstrated.
"""
    
    print("=== Testing with Draft that Covers Multiple Units (No Explicit Mappings) ===")
    print(f"\nDraft Text (first 300 chars):\n{test_draft[:300]}...")
    
    # Extract unit mappings (should be empty)
    unit_mappings = extract_unit_ac_mappings(test_draft)
    print(f"\nExtracted Unit Mappings: {unit_mappings}")
    print(f"Expected: Empty (no explicit mappings)")
    
    # Extract ACs
    found_acs = extract_ac_references_with_context(test_draft)
    print(f"\nExtracted ACs: {sorted(found_acs.keys())}")
    
    # Prepare data for bulk matrix
    all_found_acs_by_report = {}
    for ac_id, ac_info in found_acs.items():
        all_found_acs_by_report[ac_id] = [{
            **ac_info,
            'report_name': 'My Draft',
            'unit_id': None
        }]
    
    reports = [{'name': 'My Draft', 'text': test_draft}]
    
    # Generate matrix
    print("\n=== Generating Matrix ===")
    matrix_data = generate_matrix_bulk(parsed_data, all_found_acs_by_report, test_draft, reports)
    
    # Check results
    print("\n=== Matrix Results ===")
    units_with_coverage = []
    units_without_coverage = []
    
    for unit in matrix_data.get('units', []):
        unit_id = unit.get('unit_id', '')
        unit_name = unit.get('unit_name', '')
        report_coverage = unit.get('report_coverage', {})
        
        print(f"\nUnit {unit_id}: {unit_name}")
        
        for report_name, coverage in report_coverage.items():
            covered_acs = list(coverage.keys())
            if covered_acs:
                units_with_coverage.append(unit_id)
                print(f"  {report_name} covers: {', '.join(sorted(covered_acs))} ({len(covered_acs)} ACs)")
            else:
                units_without_coverage.append(unit_id)
                print(f"  {report_name}: No coverage")
    
    print(f"\n=== Summary ===")
    print(f"Units with coverage: {units_with_coverage}")
    print(f"Units without coverage: {units_without_coverage}")
    
    # The draft should show coverage in at least some units (using heuristic)
    if units_with_coverage:
        print(f"\n✅ Matrix shows coverage in {len(units_with_coverage)} unit(s)")
    else:
        print(f"\n❌ ERROR: Matrix shows NO coverage in any unit!")
        print("This suggests the heuristic is too strict or not working correctly.")

if __name__ == '__main__':
    test_all_units_coverage()




