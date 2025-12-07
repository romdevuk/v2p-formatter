"""
Test script to verify AC covered label hiding in preview
"""
from playwright.sync_api import sync_playwright
import time
import os

def test_ac_covered_hiding():
    """Test that only 'AC covered:' label is hidden, not the AC values"""
    
    # Create screenshots directory
    os.makedirs('reports/screenshots', exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Navigate to observation media page
            print("Navigating to observation media page...")
            page.goto('http://localhost/v2p-formatter/observation-media', wait_until='networkidle')
            time.sleep(2)
            
            # Expand editor if collapsed
            print("Expanding editor if needed...")
            editor_section = page.query_selector('.editor-section')
            if editor_section:
                is_collapsed = 'collapsed' in editor_section.get_attribute('class') or ''
                if is_collapsed:
                    editor_header = page.query_selector('.editor-section-header')
                    if editor_header:
                        editor_header.click()
                        time.sleep(0.5)
            
            # Add test content to editor
            print("Adding test content with AC covered...")
            editor = page.query_selector('#observationTextEditor')
            if editor:
                # Wait for editor to be visible
                page.wait_for_selector('#observationTextEditor', state='visible', timeout=5000)
                test_content = """SECTION: Test Section

AC covered: 641:1.1, 1.2, 1.3, 2.1, 4.1; 642:1.1;

This is some test content with AC covered information.
"""
                # Use evaluate to set value directly
                page.evaluate(f'document.getElementById("observationTextEditor").value = {repr(test_content)}')
                # Trigger input event
                page.evaluate('document.getElementById("observationTextEditor").dispatchEvent(new Event("input", { bubbles: true }))')
                time.sleep(1)
            
            # Click Preview Draft button
            print("Opening preview draft...")
            preview_btn = page.query_selector('#previewDraftBtn')
            if preview_btn:
                preview_btn.click()
                time.sleep(2)
            
            # Take screenshot 1: Before hiding AC covered
            print("Taking screenshot 1: AC covered visible...")
            page.screenshot(path='reports/screenshots/preview_ac_visible.png', full_page=True)
            
            # Check if AC covered text is visible
            content = page.query_selector('#draftPreviewContent')
            if content:
                inner_html = content.inner_html()
                print(f"\nContent HTML (first 500 chars):\n{inner_html[:500]}")
                
                # Check for AC covered elements
                ac_covered_elements = page.query_selector_all('.preview-ac-covered')
                print(f"\nFound {len(ac_covered_elements)} AC covered elements")
                
                for i, elem in enumerate(ac_covered_elements):
                    print(f"  Element {i+1}: {elem.inner_text()[:100]}")
                    
                    # Check for label and values spans
                    label = elem.query_selector('.preview-ac-covered-label')
                    values = elem.query_selector('.preview-ac-covered-values')
                    
                    if label:
                        print(f"    Label span found: '{label.inner_text()}'")
                        label_display = page.evaluate('el => window.getComputedStyle(el).display', label)
                        print(f"    Label display: {label_display}")
                    
                    if values:
                        print(f"    Values span found: '{values.inner_text()}'")
                        values_display = page.evaluate('el => window.getComputedStyle(el).display', values)
                        print(f"    Values display: {values_display}")
            
            # Open Settings menu
            print("\nOpening Settings menu...")
            settings_btn = page.query_selector('#previewSettingsBtn')
            if settings_btn:
                settings_btn.click()
                time.sleep(0.5)
            
            # Check the "AC covered" checkbox
            print("Checking AC covered checkbox...")
            ac_checkbox = page.query_selector('#hideAcCovered')
            if ac_checkbox:
                ac_checkbox.check()
                time.sleep(0.5)
            
            # Take screenshot 2: After hiding AC covered
            print("Taking screenshot 2: AC covered label hidden...")
            page.screenshot(path='reports/screenshots/preview_ac_hidden.png', full_page=True)
            
            # Verify that only label is hidden, values are visible
            print("\nVerifying AC covered hiding...")
            content = page.query_selector('#draftPreviewContent')
            if content:
                ac_covered_elements = page.query_selector_all('.preview-ac-covered')
                print(f"Found {len(ac_covered_elements)} AC covered elements after hiding")
                
                for i, elem in enumerate(ac_covered_elements):
                    print(f"\nElement {i+1}:")
                    full_text = elem.inner_text()
                    print(f"  Full text: '{full_text}'")
                    
                    # Check label and values
                    label = elem.query_selector('.preview-ac-covered-label')
                    values = elem.query_selector('.preview-ac-covered-values')
                    
                    if label:
                        label_text = label.inner_text()
                        label_display = page.evaluate('el => window.getComputedStyle(el).display', label)
                        print(f"  Label: '{label_text}' - display: {label_display}")
                        if label_display != 'none':
                            print(f"  ❌ ERROR: Label should be hidden (display: none) but is: {label_display}")
                    
                    if values:
                        values_text = values.inner_text()
                        values_display = page.evaluate('el => window.getComputedStyle(el).display', values)
                        print(f"  Values: '{values_text}' - display: {values_display}")
                        if values_display == 'none':
                            print(f"  ❌ ERROR: Values should be visible but are hidden!")
                        elif values_text.strip():
                            print(f"  ✓ Values are visible: '{values_text}'")
                        else:
                            print(f"  ⚠ WARNING: Values span is empty")
            
            # Check if the AC values are still visible in the content
            content_text = content.inner_text() if content else ""
            if "641:1.1" in content_text or "642:1.1" in content_text:
                print("\n✓ AC values are still visible in content")
            else:
                print("\n❌ ERROR: AC values are missing from content!")
            
            print("\n✓ Test completed. Check screenshots in reports/screenshots/")
            
        except Exception as e:
            print(f"\n❌ Error during test: {e}")
            import traceback
            traceback.print_exc()
            page.screenshot(path='reports/screenshots/preview_ac_error.png', full_page=True)
        
        finally:
            time.sleep(2)
            browser.close()

if __name__ == '__main__':
    test_ac_covered_hiding()

