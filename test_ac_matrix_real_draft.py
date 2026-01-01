"""
Test with actual draft from observation media to debug Unit 129v4 issue
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.draft_manager import list_drafts, load_draft
from app.ac_matrix_parser import parse_standards_json
from app.ac_matrix_analyzer import extract_ac_references_with_context, extract_unit_ac_mappings, generate_matrix_bulk
from config import AC_MATRIX_JSON_STANDARDS_DIR
import logging

# Enable debug logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_real_draft():
    """Test with actual draft 'My Draft (2025-12-07)'"""
    
    # Find the draft
    drafts = list_drafts()
    target_draft = None
    # Try exact match first, then partial match
    for draft in drafts:
        draft_name = draft.get('name', '')
        if 'My Draft (2025-12-07)' in draft_name or 'My Draft' == draft_name:
            target_draft = draft
            break
    
    if not target_draft:
        print("ERROR: Draft 'My Draft' not found")
        print(f"Available drafts: {[d.get('name') for d in drafts]}")
        # Use first draft if available
        if drafts:
            target_draft = drafts[0]
            print(f"Using first available draft: {target_draft.get('name')}")
        else:
            return
    
    print(f"Found draft: {target_draft.get('name')}")
    
    # Load draft
    draft_result = load_draft(target_draft['id'])
    if not draft_result['success']:
        print(f"ERROR: Could not load draft: {draft_result.get('error')}")
        return
    
    draft_text = draft_result['draft'].get('text_content', '')
    print(f"\nDraft text length: {len(draft_text)} characters")
    print(f"Draft text preview (first 500 chars):\n{draft_text[:500]}...")
    
    # Check for explicit unit mappings
    unit_mappings = extract_unit_ac_mappings(draft_text)
    print(f"\n=== Explicit Unit Mappings ===")
    if unit_mappings:
        for unit_id, acs in unit_mappings.items():
            print(f"  Unit {unit_id}: {', '.join(acs)}")
    else:
        print("  No explicit unit mappings found")
    
    # Extract ACs
    found_acs = extract_ac_references_with_context(draft_text)
    print(f"\n=== Extracted ACs ===")
    print(f"  Found {len(found_acs)} unique ACs: {', '.join(sorted(found_acs.keys()))}")
    
    # Load JSON standards
    json_file = AC_MATRIX_JSON_STANDARDS_DIR / 'l2inter-performance.json'
    if not json_file.exists():
        print(f"ERROR: JSON file not found: {json_file}")
        return
    
    parsed_data = parse_standards_json(json_file)
    
    # Find unit 129v4 and its ACs
    print(f"\n=== Unit 129v4 Standards ===")
    for unit in parsed_data.get('units', []):
        if unit.get('unit_id') == '129v4':
            all_acs = []
            for lo in unit.get('learning_outcomes', []):
                for ac in lo.get('acs', []):
                    ac_id = ac.get('ac_id', '')
                    if ac_id:
                        all_acs.append(ac_id)
            print(f"  Unit 129v4 ACs: {', '.join(sorted(all_acs))}")
            
            # Check which ACs from 129v4 are in the draft
            found_129v4_acs = [ac for ac in all_acs if ac in found_acs]
            print(f"  Unit 129v4 ACs found in draft: {', '.join(sorted(found_129v4_acs))}")
            print(f"  Unit 129v4 ACs NOT found: {', '.join(sorted([ac for ac in all_acs if ac not in found_acs]))}")
            break
    
    # Prepare data for bulk matrix
    all_found_acs_by_report = {}
    for ac_id, ac_info in found_acs.items():
        all_found_acs_by_report[ac_id] = [{
            **ac_info,
            'report_name': target_draft.get('name', 'My Draft (2025-12-07)'),
            'unit_id': None
        }]
    
    reports = [{'name': target_draft.get('name', 'My Draft (2025-12-07)'), 'text': draft_text}]
    
    # Generate matrix
    print(f"\n=== Generating Matrix ===")
    matrix_data = generate_matrix_bulk(parsed_data, all_found_acs_by_report, draft_text, reports)
    
    # Check results for unit 129v4
    print(f"\n=== Matrix Results for Unit 129v4 ===")
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
                    print(f"     This is the problem! Expected ACs: {', '.join(sorted(found_129v4_acs))}")
            break
    else:
        print("  ❌ Unit 129v4 not found in matrix results!")

if __name__ == '__main__':
    test_real_draft()

