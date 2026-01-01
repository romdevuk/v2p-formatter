"""
Test for Standards "Covered" Logic Fix
Tests that ACs are only shown as covered in sections where they're actually listed
"""
import pytest
import json
from pathlib import Path


class TestStandardsCoveredLogic:
    """Test the fixed Covered logic for standards"""
    
    @pytest.fixture
    def base_url(self):
        """Base URL for the application"""
        return "http://localhost/v2p-formatter/observation-media"
    
    def test_covered_logic_no_false_positives(self, page, base_url):
        """
        Test that 129v4:5.1 is NOT incorrectly shown as covered in sections 5 and 9
        when it's not actually listed in those sections' AC covered lines
        """
        print("\n=== Testing Covered Logic Fix ===")
        
        # Navigate to observation media page
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        
        # Wait for page to be ready
        page.wait_for_selector("#standardsContent", timeout=10000)
        
        # Expand editor section if collapsed
        page.evaluate("""
            const editorSection = document.querySelector('.editor-section');
            if (editorSection && editorSection.classList.contains('collapsed')) {
                editorSection.classList.remove('collapsed');
            }
        """)
        
        # Wait for editor to be available (may be hidden but should exist)
        page.wait_for_selector("#observationTextEditor", state="attached", timeout=10000)
        
        # Create draft text with specific AC covered lines
        # Section 5: AC covered: 129v4:5.2, 5.3 (NOT 5.1)
        # Section 9: AC covered: 129v4:9.1, 9.2 (NOT 5.1)
        draft_text = """SECTION: 5 – INSTALLATION OF DRYLINING SYSTEMS
Some text here.
AC covered: 129v4:5.2, 5.3
More text.

SECTION: 9 – COMPLETION OF WORK AND HANDOVER
Some text here.
AC covered: 129v4:9.1, 9.2
More text."""
        
        # Set draft text in editor
        page.fill("#observationTextEditor", draft_text)
        
        # Trigger input event to parse sections
        page.evaluate("""
            const editor = document.getElementById('observationTextEditor');
            if (editor) {
                editor.dispatchEvent(new Event('input', { bubbles: true }));
            }
        """)
        
        # Wait for parsing
        page.wait_for_timeout(500)
        
        # Mock standards data with 129v4:5.1 (correct structure)
        standards_data = {
            "qualifications": [
                {
                    "units": [
                        {
                            "unit_id": "129v4",
                            "unit_name": "Test Unit",
                            "learning_outcomes": [
                                {
                                    "questions": [
                                        {
                                            "question_id": "5.1",
                                            "question_name": "Test AC 5.1",
                                            "question_type": "Knowledge"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Render standards
        page.evaluate(f"""
            if (typeof renderStandards === 'function') {{
                renderStandards({json.dumps(standards_data)});
            }}
        """)
        
        # Wait for rendering
        page.wait_for_timeout(1000)
        
        # Check that 129v4:5.1 is NOT shown as covered in section 5 or 9
        standards_html = page.evaluate("() => document.getElementById('standardsContent').innerHTML")
        
        print(f"\nStandards HTML length: {len(standards_html)}")
        
        # Check if 129v4:5.1 appears in the standards
        assert "5.1" in standards_html, "AC 5.1 should be displayed in standards"
        
        # Extract the covered sections for 5.1
        covered_sections = page.evaluate("""() => {
            const acElement = Array.from(document.querySelectorAll('.standards-ac')).find(el => {
                return el.querySelector('.standards-ac-id')?.textContent === '5.1';
            });
            
            if (acElement) {
                const coveredDiv = acElement.querySelector('.standards-ac-covered');
                if (coveredDiv) {
                    return coveredDiv.textContent;
                }
            }
            return '';
        }""")
        
        print(f"\nCovered sections for 5.1: {covered_sections}")
        
        # Verify that section 5 (INSTALLATION OF DRYLINING SYSTEMS) is NOT in the covered list
        assert "INSTALLATION OF DRYLINING SYSTEMS" not in covered_sections, \
            "129v4:5.1 should NOT be shown as covered in section 5"
        
        # Verify that section 9 (COMPLETION OF WORK AND HANDOVER) is NOT in the covered list
        assert "COMPLETION OF WORK AND HANDOVER" not in covered_sections, \
            "129v4:5.1 should NOT be shown as covered in section 9"
        
        print("\n✅ Test passed: No false positives detected")
    
    def test_covered_logic_correct_matches(self, page, base_url):
        """
        Test that ACs ARE correctly shown as covered when they ARE in the AC covered lists
        """
        print("\n=== Testing Correct Matches ===")
        
        # Navigate to observation media page
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        
        # Wait for page to be ready
        page.wait_for_selector("#standardsContent", timeout=10000)
        
        # Expand editor section if collapsed
        page.evaluate("""
            const editorSection = document.querySelector('.editor-section');
            if (editorSection && editorSection.classList.contains('collapsed')) {
                editorSection.classList.remove('collapsed');
            }
        """)
        
        # Wait for editor to be available
        page.wait_for_selector("#observationTextEditor", state="attached", timeout=10000)
        
        # Create draft text where 129v4:5.1 IS actually covered
        draft_text = """SECTION: 5 – INSTALLATION OF DRYLINING SYSTEMS
Some text here.
AC covered: 129v4:5.1, 5.2, 5.3
More text."""
        
        # Set draft text in editor
        page.fill("#observationTextEditor", draft_text)
        
        # Trigger input event to parse sections
        page.evaluate("""
            const editor = document.getElementById('observationTextEditor');
            if (editor) {
                editor.dispatchEvent(new Event('input', { bubbles: true }));
            }
        """)
        
        # Wait for parsing
        page.wait_for_timeout(500)
        
        # Mock standards data (correct structure)
        standards_data = {
            "qualifications": [
                {
                    "units": [
                        {
                            "unit_id": "129v4",
                            "unit_name": "Test Unit",
                            "learning_outcomes": [
                                {
                                    "questions": [
                                        {
                                            "question_id": "5.1",
                                            "question_name": "Test AC 5.1",
                                            "question_type": "Knowledge"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Render standards
        page.evaluate(f"""
            if (typeof renderStandards === 'function') {{
                renderStandards({json.dumps(standards_data)});
            }}
        """)
        
        # Wait for rendering
        page.wait_for_timeout(1000)
        
        # Check that 129v4:5.1 IS shown as covered in section 5
        covered_sections = page.evaluate("""() => {
            const acElement = Array.from(document.querySelectorAll('.standards-ac')).find(el => {
                return el.querySelector('.standards-ac-id')?.textContent === '5.1';
            });
            
            if (acElement) {
                const coveredDiv = acElement.querySelector('.standards-ac-covered');
                if (coveredDiv) {
                    return coveredDiv.textContent;
                }
            }
            return '';
        }""")
        
        print(f"\nCovered sections for 5.1: {covered_sections}")
        
        # Verify that section 5 IS in the covered list
        assert "INSTALLATION OF DRYLINING SYSTEMS" in covered_sections, \
            "129v4:5.1 SHOULD be shown as covered in section 5"
        
        print("\n✅ Test passed: Correct matches detected")
    
    def test_covered_logic_shorthand_format(self, page, base_url):
        """
        Test that shorthand format (5.1 after 129v4:) is correctly recognized
        """
        print("\n=== Testing Shorthand Format ===")
        
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("#standardsContent", timeout=10000)
        
        # Expand editor section if collapsed
        page.evaluate("""
            const editorSection = document.querySelector('.editor-section');
            if (editorSection && editorSection.classList.contains('collapsed')) {
                editorSection.classList.remove('collapsed');
            }
        """)
        
        # Wait for editor to be available
        page.wait_for_selector("#observationTextEditor", state="attached", timeout=10000)
        
        # Test draft with shorthand format: 129v4:5.1, 5.2 (where 5.2 is shorthand)
        draft_text = """SECTION: Test Section
AC covered: 129v4:5.1, 5.2"""
        
        # Set draft text in editor
        page.fill("#observationTextEditor", draft_text)
        
        # Trigger input event to parse sections
        page.evaluate("""
            const editor = document.getElementById('observationTextEditor');
            if (editor) {
                editor.dispatchEvent(new Event('input', { bubbles: true }));
            }
        """)
        
        # Wait for parsing
        page.wait_for_timeout(500)
        
        # Mock standards data (correct structure)
        standards_data = {
            "qualifications": [
                {
                    "units": [
                        {
                            "unit_id": "129v4",
                            "unit_name": "Test Unit",
                            "learning_outcomes": [
                                {
                                    "questions": [
                                        {
                                            "question_id": "5.1",
                                            "question_name": "Test AC 5.1",
                                            "question_type": "Knowledge"
                                        },
                                        {
                                            "question_id": "5.2",
                                            "question_name": "Test AC 5.2",
                                            "question_type": "Knowledge"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Render standards
        page.evaluate(f"""
            if (typeof renderStandards === 'function') {{
                renderStandards({json.dumps(standards_data)});
            }}
        """)
        
        page.wait_for_timeout(1000)
        
        # Check both 5.1 and 5.2 are covered
        for ac_id in ["5.1", "5.2"]:
            covered_sections = page.evaluate(f"""() => {{
                const acElement = Array.from(document.querySelectorAll('.standards-ac')).find(el => {{
                    return el.querySelector('.standards-ac-id')?.textContent === '{ac_id}';
                }});
                
                if (acElement) {{
                    const coveredDiv = acElement.querySelector('.standards-ac-covered');
                    if (coveredDiv) {{
                        return coveredDiv.textContent;
                    }}
                }}
                return '';
            }}""")
            
            print(f"\nCovered sections for {ac_id}: {covered_sections}")
            assert "Test Section" in covered_sections, \
                f"129v4:{ac_id} SHOULD be shown as covered (shorthand format)"
        
        print("\n✅ Test passed: Shorthand format correctly recognized")

