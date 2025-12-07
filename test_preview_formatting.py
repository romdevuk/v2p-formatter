#!/usr/bin/env python3
"""
Test script to verify that updating draft from preview preserves proper formatting with line breaks.
"""

import asyncio
from playwright.async_api import async_playwright
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_preview_formatting():
    """Test that draft update preserves line breaks"""
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            # Navigate to observation media page
            print("Navigating to observation media page...")
            await page.goto('http://localhost:5000/v2p-formatter/media-converter/observation-media')
            await page.wait_for_load_state('networkidle')
            
            # Wait for page to be ready
            await page.wait_for_selector('#observationTextEditor', timeout=10000)
            print("Page loaded successfully")
            
            # Expand editor if collapsed
            editor_section = page.locator('.editor-section')
            if await editor_section.count() > 0:
                collapsed = await editor_section.evaluate('el => el.classList.contains("collapsed")')
                if collapsed:
                    print("Expanding editor section...")
                    toggle_btn = page.locator('.editor-section-header').first
                    await toggle_btn.click()
                    await page.wait_for_timeout(500)
            
            # Fill editor with properly formatted text
            test_text = """SECTION 1 – SITE ARRIVAL AND INDUCTION
1.I arrived to the project on time, weather sunny and warm. I met Ivan near the main gate and he followed the site security rules by signing in and entering through fenced access. I observed Ivan already wearing his full PPE: high-viz, hard hat, gloves, safety boots and glasses. He spoke to me polite and explained where is fire point and showed the health and safety notice board.
AC covered: 641:1.1, 1.2, 1.3, 2.1, 4.1; 642:1.1
Image suggestion: photo of Ivan signing in at the gate showing PPE.
{{Section_name_table}}
2.We went inside the office for induction. Ivan provided his CSCS card and completed all the sign-in paperwork, RAMS and site briefing. I observed learner storing his PPE and tools properly inside his tool bag after instruction from induction manager.
AC covered: 641:5.1; 642:1.1, 4.1
Image suggestion: image of induction paperwork and CSCS card check.
{{Section_name_table}}
SECTION 2 – HEALTH, SAFETY AND WELFARE
3.While walking to the work zone, Ivan observed some wires loose on the floor. He immediately reported hazard to the site manager. He also explained to me that slips and trips cause serious injury and he always try to remove or report hazard.
AC covered: 641:2.1, 3.1, 3.3, 3.4, 3.5
Image suggestion: photo of hazard reporting (staged example).
{{Section_name_table}}"""
            
            print("Filling editor with test text...")
            editor = page.locator('#observationTextEditor')
            await editor.fill(test_text)
            await page.wait_for_timeout(500)
            
            # Create a draft first
            print("Creating a draft...")
            draft_name_input = page.locator('#draftNameInput')
            if await draft_name_input.count() > 0:
                await draft_name_input.fill('Test Formatting Draft')
                await page.wait_for_timeout(300)
            
            save_draft_btn = page.locator('button:has-text("Save Draft")')
            if await save_draft_btn.count() > 0:
                await save_draft_btn.click()
                await page.wait_for_timeout(1000)
            
            # Open preview
            print("Opening preview...")
            preview_btn = page.locator('button:has-text("Preview Draft")')
            await preview_btn.click()
            await page.wait_for_timeout(1000)
            
            # Wait for preview modal to appear
            await page.wait_for_selector('#draftPreviewModal', timeout=5000)
            await page.wait_for_selector('#draftPreviewContent', timeout=5000)
            print("Preview modal opened")
            
            # Take screenshot of preview
            await page.screenshot(path='reports/screenshots/preview_before_update.png', full_page=True)
            print("Screenshot saved: preview_before_update.png")
            
            # Click "Update Draft" button
            print("Clicking Update Draft button...")
            update_btn = page.locator('#updateDraftFromPreviewBtn')
            await update_btn.click()
            
            # Wait for alert/confirmation
            def handle_dialog(dialog):
                print(f"Dialog message: {dialog.message}")
                dialog.accept()
            
            page.on('dialog', handle_dialog)
            await page.wait_for_timeout(2000)
            
            # Close preview modal (it should close automatically, but just in case)
            close_btn = page.locator('#closeDraftPreviewBtn')
            if await close_btn.count() > 0:
                await close_btn.click()
                await page.wait_for_timeout(500)
            
            # Get the text from the editor
            print("Reading updated text from editor...")
            updated_text = await editor.input_value()
            
            # Verify formatting - check for line breaks
            print("\n=== FORMATTING VERIFICATION ===")
            lines = updated_text.split('\n')
            print(f"Total lines: {len(lines)}")
            print(f"First 10 lines:")
            for i, line in enumerate(lines[:10], 1):
                print(f"  {i}: {repr(line[:80])}")  # Show first 80 chars
            
            # Check for specific patterns that should be on separate lines
            issues = []
            
            # Check if section titles are on their own line
            if 'SECTION 1' in updated_text:
                idx = updated_text.find('SECTION 1')
                if idx > 0 and updated_text[idx-1] != '\n':
                    issues.append("SECTION 1 not on new line")
            
            # Check if paragraph numbers are followed by newlines (after their text)
            if '1.I arrived' in updated_text:
                # Should have newline after the paragraph
                if '1.I arrived' in updated_text and 'AC covered:' in updated_text:
                    idx1 = updated_text.find('1.I arrived')
                    idx2 = updated_text.find('AC covered:', idx1)
                    if idx2 > idx1:
                        between = updated_text[idx1:idx2]
                        if '\n' not in between:
                            issues.append("No newline between paragraph 1 and AC covered")
            
            # Check if placeholders are on their own lines
            if '{{Section_name_table}}' in updated_text:
                placeholder_positions = []
                start = 0
                while True:
                    pos = updated_text.find('{{Section_name_table}}', start)
                    if pos == -1:
                        break
                    placeholder_positions.append(pos)
                    start = pos + 1
                
                for pos in placeholder_positions:
                    # Check if there's a newline before (unless it's at the start)
                    if pos > 0 and updated_text[pos-1] != '\n':
                        issues.append(f"Placeholder at position {pos} not on new line (before)")
                    # Check if there's a newline after
                    after_pos = pos + len('{{Section_name_table}}')
                    if after_pos < len(updated_text) and updated_text[after_pos] != '\n':
                        issues.append(f"Placeholder at position {pos} not on new line (after)")
            
            # Save the updated text to a file for inspection
            with open('reports/test_updated_text.txt', 'w') as f:
                f.write(updated_text)
            print(f"\nUpdated text saved to: reports/test_updated_text.txt")
            
            # Take screenshot of editor with updated text
            await page.screenshot(path='reports/screenshots/editor_after_update.png', full_page=True)
            print("Screenshot saved: editor_after_update.png")
            
            # Report results
            print("\n=== TEST RESULTS ===")
            if issues:
                print(f"❌ ISSUES FOUND ({len(issues)}):")
                for issue in issues:
                    print(f"  - {issue}")
                return False
            else:
                print("✅ All formatting checks passed!")
                print(f"✅ Text has {len(lines)} lines (expected multiple lines)")
                return True
                
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            await page.screenshot(path='reports/screenshots/error_formatting_test.png', full_page=True)
            return False
        finally:
            await browser.close()

if __name__ == '__main__':
    # Create reports directory if it doesn't exist
    os.makedirs('reports/screenshots', exist_ok=True)
    
    result = asyncio.run(test_preview_formatting())
    sys.exit(0 if result else 1)

