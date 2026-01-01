"""
Simple screenshot tests for Observation Report - generates screenshots without complex dependencies
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, Page


def take_screenshots():
    """Take screenshots of Observation Report UI"""
    base_url = "http://localhost/v2p-formatter"
    screenshot_dir = Path("test_screenshots/observation_report_workflows")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Visible browser
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        
        try:
            print("📸 Taking screenshots of Observation Report...")
            
            # 1. Initial page load
            print("1. Loading page...")
            page.goto(f"{base_url}/observation-report")
            time.sleep(3)  # Wait for page to fully load
            page.screenshot(path=str(screenshot_dir / "01_initial_load.png"), full_page=True)
            print("   ✅ Screenshot: 01_initial_load.png")
            
            # 2. Qualification dropdown
            print("2. Checking qualification dropdown...")
            qualification_select = page.locator("#qualificationSelect")
            if qualification_select.is_visible():
                options = qualification_select.locator("option")
                option_count = options.count()
                print(f"   Found {option_count} qualifications")
                page.screenshot(path=str(screenshot_dir / "02_qualification_dropdown.png"), full_page=True)
                print("   ✅ Screenshot: 02_qualification_dropdown.png")
                
                # 3. Select qualification
                if option_count > 1:
                    print("3. Selecting qualification...")
                    qualification_select.select_option(index=1)
                    time.sleep(2)
                    page.screenshot(path=str(screenshot_dir / "03_qualification_selected.png"), full_page=True)
                    print("   ✅ Screenshot: 03_qualification_selected.png")
                    
                    # 4. Select learner
                    learner_select = page.locator("#learnerSelect")
                    if learner_select.is_visible() and not learner_select.is_disabled():
                        options = learner_select.locator("option")
                        if options.count() > 1:
                            print("4. Selecting learner...")
                            learner_select.select_option(index=1)
                            time.sleep(3)  # Wait for media to load
                            page.screenshot(path=str(screenshot_dir / "04_learner_selected.png"), full_page=True)
                            print("   ✅ Screenshot: 04_learner_selected.png")
                            
                            # 5. Media browser loaded
                            print("5. Media browser...")
                            media_browser = page.locator("#mediaBrowser")
                            if media_browser.is_visible():
                                page.screenshot(path=str(screenshot_dir / "05_media_browser_loaded.png"), full_page=True)
                                print("   ✅ Screenshot: 05_media_browser_loaded.png")
            
            # 6. Text editor with placeholders
            print("6. Text editor section...")
            text_editor_section = page.locator('[data-section="textEditor"]')
            if text_editor_section.is_visible():
                section_header = text_editor_section.locator(".section-header")
                section_header.click()
                time.sleep(0.5)
                
                text_editor = page.locator("#textEditor")
                test_text = "SECTION 1: Site Arrival\n\n{{Site_Arrival_Induction}}\n\nThe site arrival process was conducted properly.\n\n{{Safety_Briefing}}\n\nSafety procedures were explained."
                text_editor.fill(test_text)
                time.sleep(1)
                page.screenshot(path=str(screenshot_dir / "06_text_with_placeholders.png"), full_page=True)
                print("   ✅ Screenshot: 06_text_with_placeholders.png")
                
                # 7. Live preview with placeholders
                print("7. Live preview...")
                page.screenshot(path=str(screenshot_dir / "07_live_preview_placeholders.png"), full_page=True)
                print("   ✅ Screenshot: 07_live_preview_placeholders.png")
            
            # 8. Drag and drop
            print("8. Testing drag and drop...")
            media_cards = page.locator(".media-card:not(.assigned)")
            drop_zones = page.locator(".drop-zone")
            
            if media_cards.count() > 0 and drop_zones.count() > 0:
                # Before drag
                page.screenshot(path=str(screenshot_dir / "08_before_drag.png"), full_page=True)
                print("   ✅ Screenshot: 08_before_drag.png")
                
                # Perform drag
                media_cards.first.drag_to(drop_zones.first)
                time.sleep(2)
                
                # After drag
                page.screenshot(path=str(screenshot_dir / "09_after_drag.png"), full_page=True)
                print("   ✅ Screenshot: 09_after_drag.png")
            
            # 9. Load draft dialog
            print("9. Draft load dialog...")
            load_button = page.locator("#loadDraftBtn")
            if load_button.is_visible():
                load_button.click()
                time.sleep(1)
                page.screenshot(path=str(screenshot_dir / "10_draft_dialog.png"), full_page=True)
                print("   ✅ Screenshot: 10_draft_dialog.png")
                
                # Close dialog
                close_btn = page.locator("#draftLoadDialog .modal-close")
                if close_btn.is_visible():
                    close_btn.click()
                    time.sleep(0.5)
            
            print("\n✅ All screenshots taken!")
            print(f"📁 Location: {screenshot_dir.absolute()}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            # Take error screenshot
            page.screenshot(path=str(screenshot_dir / "error.png"), full_page=True)
        
        finally:
            browser.close()


if __name__ == "__main__":
    take_screenshots()



