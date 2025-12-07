"""
Test to verify paragraph numbers are detected and can be hidden in preview.
"""
from playwright.sync_api import sync_playwright
import time

def test_paragraph_numbers():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to observation media page
        page.goto("http://localhost/v2p-formatter/observation-media")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # Get the text editor
        editor = page.locator("#observationTextEditor")
        if not editor.is_visible():
            # Try to expand it
            expand_btn = page.locator(".editor-section-header")
            if expand_btn.is_visible():
                expand_btn.click()
                time.sleep(1)
        
        # Fill with test text that has paragraph numbers on their own lines
        test_text = """SECTION 1 – SITE ARRIVAL AND INDUCTION

1.



I arrived to the project on time, weather sunny and warm. I met Ivan near the main gate and he followed the site security rules by signing in and entering through fenced access. I observed Ivan already wearing his full PPE: high-viz, hard hat, gloves, safety boots and glasses. He spoke to me polite and explained where is fire point and showed the health and safety notice board.

AC covered: 641:1.1, 1.2, 1.3, 2.1, 4.1; 642:1.1

Image suggestion: photo of Ivan signing in at the gate showing PPE.

{{section_name_table}}



2.



We went inside the office for induction. Ivan provided his CSCS card and completed all the sign-in paperwork, RAMS and site briefing. I observed learner storing his PPE and tools properly inside his tool bag after instruction from induction manager.

AC covered: 641:5.1; 642:1.1, 4.1

Image suggestion: image of induction paperwork and CSCS card check.

{{section_name_table}}"""
        
        editor.fill(test_text)
        time.sleep(1)
        
        # Click Preview Draft button
        preview_btn = page.locator("#previewDraftBtn")
        if preview_btn.is_visible():
            preview_btn.click()
            time.sleep(2)
            
            # Check if modal is visible
            modal = page.locator("#draftPreviewModal")
            if modal.is_visible():
                print("✓ Modal is visible")
                
                # Check if paragraph numbers are present
                para_numbers = page.locator(".preview-paragraph-number")
                count = para_numbers.count()
                print(f"✓ Found {count} paragraph number elements")
                
                if count > 0:
                    # Check first paragraph number
                    first_para = para_numbers.first
                    text = first_para.inner_text()
                    print(f"✓ First paragraph number text: '{text}'")
                    
                    # Check if it's visible
                    is_visible = first_para.is_visible()
                    print(f"✓ First paragraph number visible: {is_visible}")
                    
                    # Open settings menu first
                    settings_btn = page.locator("#previewSettingsBtn")
                    if settings_btn.is_visible():
                        settings_btn.click()
                        time.sleep(0.5)
                        print("✓ Settings menu opened")
                    
                    # Find the hide paragraph numbers checkbox
                    hide_checkbox = page.locator("#hideParagraphNumbers")
                    if hide_checkbox.is_visible():
                        print("✓ Hide paragraph numbers checkbox found")
                        
                        # Click to hide
                        hide_checkbox.click()
                        time.sleep(0.5)
                        
                        # Check if paragraph numbers are now hidden
                        # We need to check the computed style
                        first_para_hidden = first_para.evaluate("el => window.getComputedStyle(el).display === 'none'")
                        print(f"✓ After hiding, first paragraph number display='none': {first_para_hidden}")
                        
                        # Take screenshot
                        page.screenshot(path="test_preview_paragraph_numbers_hidden.png", full_page=True)
                        print("✓ Screenshot saved: test_preview_paragraph_numbers_hidden.png")
                        
                        # Click again to show
                        hide_checkbox.click()
                        time.sleep(0.5)
                        
                        first_para_visible = first_para.evaluate("el => window.getComputedStyle(el).display !== 'none'")
                        print(f"✓ After showing, first paragraph number visible: {first_para_visible}")
                        
                        page.screenshot(path="test_preview_paragraph_numbers_visible.png", full_page=True)
                        print("✓ Screenshot saved: test_preview_paragraph_numbers_visible.png")
                    else:
                        print("✗ Hide paragraph numbers checkbox not found")
                else:
                    print("✗ No paragraph number elements found")
                    # Take screenshot to see what's in the preview
                    page.screenshot(path="test_preview_paragraph_numbers_no_elements.png", full_page=True)
                    print("✓ Screenshot saved: test_preview_paragraph_numbers_no_elements.png")
            else:
                print("✗ Modal not visible")
        else:
            print("✗ Preview Draft button not found")
        
        browser.close()

if __name__ == "__main__":
    test_paragraph_numbers()

