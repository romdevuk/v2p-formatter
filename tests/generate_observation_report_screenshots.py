#!/usr/bin/env python3
"""
Generate screenshots for Observation Report module
Simple script that can be run directly to capture UI screenshots
"""
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not available. Install with: pip install playwright && playwright install chromium")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


def take_screenshots_playwright():
    """Take screenshots using Playwright"""
    base_url = "http://localhost/v2p-formatter"
    screenshot_dir = Path("test_screenshots/observation_report_workflows")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        try:
            print("📸 Taking Observation Report screenshots with Playwright...")
            
            # 1. Initial load
            print("1. Loading page...")
            page.goto(f"{base_url}/observation-report", wait_until="networkidle")
            time.sleep(2)
            page.screenshot(path=str(screenshot_dir / "01_initial_load.png"), full_page=True)
            print(f"   ✅ Saved: {screenshot_dir / '01_initial_load.png'}")
            
            # 2. Qualification dropdown
            print("2. Qualification dropdown...")
            qual_select = page.locator("#qualificationSelect")
            if qual_select.is_visible():
                page.screenshot(path=str(screenshot_dir / "02_qualification_dropdown.png"), full_page=True)
                print(f"   ✅ Saved: {screenshot_dir / '02_qualification_dropdown.png'}")
                
                options = qual_select.locator("option")
                if options.count() > 1:
                    # 3. Select qualification
                    print("3. Selecting qualification...")
                    qual_select.select_option(index=1)
                    time.sleep(2)
                    page.screenshot(path=str(screenshot_dir / "03_qualification_selected.png"), full_page=True)
                    print(f"   ✅ Saved: {screenshot_dir / '03_qualification_selected.png'}")
                    
                    # 4. Select learner
                    learner_select = page.locator("#learnerSelect")
                    if learner_select.is_visible() and not learner_select.is_disabled():
                        options = learner_select.locator("option")
                        if options.count() > 1:
                            print("4. Selecting learner...")
                            learner_select.select_option(index=1)
                            time.sleep(3)
                            page.screenshot(path=str(screenshot_dir / "04_learner_selected_media_loaded.png"), full_page=True)
                            print(f"   ✅ Saved: {screenshot_dir / '04_learner_selected_media_loaded.png'}")
                            
                            # 5. Media browser
                            print("5. Media browser...")
                            page.screenshot(path=str(screenshot_dir / "05_media_browser.png"), full_page=True)
                            print(f"   ✅ Saved: {screenshot_dir / '05_media_browser.png'}")
            
            # 6. Text with placeholders
            print("6. Text editor with placeholders...")
            text_section = page.locator('[data-section="textEditor"]')
            if text_section.is_visible():
                header = text_section.locator(".section-header")
                if header.is_visible():
                    header.click()
                    time.sleep(0.5)
                    
                    text_editor = page.locator("#textEditor")
                    text_editor.fill("SECTION 1: Site Arrival\n\n{{Site_Arrival_Induction}}\n\nProcess description.\n\n{{Safety_Briefing}}\n\nSafety notes.")
                    time.sleep(1)
                    page.screenshot(path=str(screenshot_dir / "06_text_with_placeholders.png"), full_page=True)
                    print(f"   ✅ Saved: {screenshot_dir / '06_text_with_placeholders.png'}")
                    
                    # 7. Live preview
                    print("7. Live preview with placeholders...")
                    page.screenshot(path=str(screenshot_dir / "07_live_preview_placeholders.png"), full_page=True)
                    print(f"   ✅ Saved: {screenshot_dir / '07_live_preview_placeholders.png'}")
            
            # 8. Drag and drop
            print("8. Drag and drop test...")
            media_cards = page.locator(".media-card:not(.assigned)")
            drop_zones = page.locator(".drop-zone")
            
            if media_cards.count() > 0 and drop_zones.count() > 0:
                page.screenshot(path=str(screenshot_dir / "08_before_drag.png"), full_page=True)
                print(f"   ✅ Saved: {screenshot_dir / '08_before_drag.png'}")
                
                media_cards.first.drag_to(drop_zones.first)
                time.sleep(2)
                
                page.screenshot(path=str(screenshot_dir / "09_after_drag.png"), full_page=True)
                print(f"   ✅ Saved: {screenshot_dir / '09_after_drag.png'}")
            
            # 9. Draft dialog
            print("9. Draft load dialog...")
            load_btn = page.locator("#loadDraftBtn")
            if load_btn.is_visible():
                load_btn.click()
                time.sleep(1)
                page.screenshot(path=str(screenshot_dir / "10_draft_dialog.png"), full_page=True)
                print(f"   ✅ Saved: {screenshot_dir / '10_draft_dialog.png'}")
            
            print(f"\n✅ All screenshots saved to: {screenshot_dir.absolute()}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            page.screenshot(path=str(screenshot_dir / "error.png"), full_page=True)
        
        finally:
            print("\nClosing browser...")
            browser.close()


def take_screenshots_selenium():
    """Take screenshots using Selenium (fallback)"""
    base_url = "http://localhost/v2p-formatter"
    screenshot_dir = Path("test_screenshots/observation_report_workflows")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        print("📸 Taking Observation Report screenshots with Selenium...")
        
        # 1. Initial load
        print("1. Loading page...")
        driver.get(f"{base_url}/observation-report")
        time.sleep(3)
        driver.save_screenshot(str(screenshot_dir / "01_initial_load.png"))
        print(f"   ✅ Saved: {screenshot_dir / '01_initial_load.png'}")
        
        # 2. Qualification dropdown
        print("2. Qualification dropdown...")
        qual_select = wait.until(EC.presence_of_element_located((By.ID, "qualificationSelect")))
        driver.save_screenshot(str(screenshot_dir / "02_qualification_dropdown.png"))
        print(f"   ✅ Saved: {screenshot_dir / '02_qualification_dropdown.png'}")
        
        # Continue with other screenshots...
        # (Similar pattern as Playwright version)
        
        print(f"\n✅ Screenshots saved to: {screenshot_dir.absolute()}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\nClosing browser...")
        driver.quit()


def main():
    """Main function"""
    print("=" * 60)
    print("Observation Report - Screenshot Generator")
    print("=" * 60)
    print()
    
    # Check if Flask server is running
    import urllib.request
    try:
        urllib.request.urlopen("http://localhost/v2p-formatter/observation-report", timeout=2)
        print("✅ Flask server is running")
    except Exception:
        print("❌ ERROR: Flask server is not running!")
        print("   Please start the server with: python run.py")
        return
    
    print()
    
    # Try Playwright first, then Selenium
    if PLAYWRIGHT_AVAILABLE:
        take_screenshots_playwright()
    elif SELENIUM_AVAILABLE:
        print("⚠️  Using Selenium (Playwright preferred)")
        take_screenshots_selenium()
    else:
        print("❌ ERROR: No browser automation available!")
        print()
        print("Install one of the following:")
        print("  1. Playwright (recommended):")
        print("     pip install playwright")
        print("     playwright install chromium")
        print()
        print("  2. Selenium:")
        print("     pip install selenium")
        print("     (also need ChromeDriver)")
        print()
        print("Then run this script again.")


if __name__ == "__main__":
    main()

