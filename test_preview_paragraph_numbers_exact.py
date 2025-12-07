"""
Test with exact user text format to verify paragraph numbers are detected and hidden.
"""
from playwright.sync_api import sync_playwright
import time

def test_paragraph_numbers_exact():
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
        
        # Use exact text from user's example
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
            time.sleep(3)  # Give more time for preview generation
            
            # Check if modal is visible
            modal = page.locator("#draftPreviewModal")
            if modal.is_visible():
                print("✓ Modal is visible")
                
                # Wait for content to load
                content = page.locator("#draftPreviewContent")
                if content.is_visible():
                    time.sleep(1)
                    
                    # Check if paragraph numbers are present
                    para_numbers = page.locator(".preview-paragraph-number")
                    count = para_numbers.count()
                    print(f"✓ Found {count} paragraph number elements")
                    
                    # Get all paragraph number texts
                    for i in range(min(count, 5)):
                        para = para_numbers.nth(i)
                        text = para.inner_text()
                        is_visible = para.is_visible()
                        display_style = para.evaluate("el => window.getComputedStyle(el).display")
                        print(f"  Paragraph {i+1}: text='{text}', visible={is_visible}, display={display_style}")
                    
                    if count > 0:
                        # Open settings menu
                        settings_btn = page.locator("#previewSettingsBtn")
                        if settings_btn.is_visible():
                            settings_btn.click()
                            time.sleep(0.5)
                            print("✓ Settings menu opened")
                        
                        # Find the hide paragraph numbers checkbox
                        hide_checkbox = page.locator("#hideParagraphNumbers")
                        if hide_checkbox.is_visible():
                            print("✓ Hide paragraph numbers checkbox found")
                            
                            # Check initial state
                            is_checked = hide_checkbox.is_checked()
                            print(f"✓ Initial checkbox state: {is_checked}")
                            
                            # Click to hide
                            hide_checkbox.click()
                            time.sleep(0.5)
                            
                            # Check all paragraph numbers are hidden
                            all_hidden = True
                            for i in range(count):
                                para = para_numbers.nth(i)
                                is_hidden = para.evaluate("el => window.getComputedStyle(el).display === 'none'")
                                if not is_hidden:
                                    all_hidden = False
                                    text = para.inner_text()
                                    print(f"  ✗ Paragraph {i+1} ('{text}') is NOT hidden")
                            
                            if all_hidden:
                                print(f"✓ All {count} paragraph numbers are hidden")
                            else:
                                print(f"✗ Some paragraph numbers are not hidden")
                            
                            # Take screenshot
                            page.screenshot(path="test_preview_paragraph_numbers_exact_hidden.png", full_page=True)
                            print("✓ Screenshot saved: test_preview_paragraph_numbers_exact_hidden.png")
                        else:
                            print("✗ Hide paragraph numbers checkbox not found")
                            # Take screenshot to see settings menu
                            page.screenshot(path="test_preview_settings_menu.png", full_page=True)
                    else:
                        print("✗ No paragraph number elements found")
                        # Take screenshot to see what's in the preview
                        page.screenshot(path="test_preview_paragraph_numbers_exact_no_elements.png", full_page=True)
                        print("✓ Screenshot saved: test_preview_paragraph_numbers_exact_no_elements.png")
                        
                        # Also check the HTML content
                        html_content = content.inner_html()
                        print(f"\nFirst 500 chars of preview HTML:")
                        print(html_content[:500])
            else:
                print("✗ Modal not visible")
        else:
            print("✗ Preview Draft button not found")
        
        browser.close()

if __name__ == "__main__":
    test_paragraph_numbers_exact()


