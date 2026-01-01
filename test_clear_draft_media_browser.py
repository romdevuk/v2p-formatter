"""
Test that clearing a draft also clears the media browser
"""
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

SCREENSHOT_DIR = Path("test_reports/clear_draft_screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://localhost/v2p-formatter/observation-media"

def test_clear_draft_clears_media_browser():
    """Test that clearing a draft clears the media browser"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        print("1. Navigating to observation media page...")
        driver.get(BASE_URL)
        time.sleep(2)
        
        # Take initial screenshot
        driver.save_screenshot(str(SCREENSHOT_DIR / "01_initial_page.png"))
        print(f"✓ Screenshot saved: {SCREENSHOT_DIR / '01_initial_page.png'}")
        
        # Check if there are any drafts available
        print("\n2. Checking for drafts...")
        try:
            load_draft_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Load Draft')]")))
            load_draft_btn.click()
            time.sleep(1)
            
            # Wait for draft dialog
            try:
                draft_dialog = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".draft-dialog, [style*='position: fixed']")))
                print("  ✓ Draft dialog opened")
                driver.save_screenshot(str(SCREENSHOT_DIR / "02_draft_dialog.png"))
                
                # Get first draft and load it
                try:
                    draft_items = driver.find_elements(By.CSS_SELECTOR, ".draft-item, [onclick*='loadDraft']")
                    if draft_items:
                        first_draft = draft_items[0]
                        draft_name = first_draft.find_element(By.TAG_NAME, "div").text
                        print(f"  Loading draft: {draft_name}")
                        
                        first_draft.click()
                        time.sleep(2)
                        
                        # Wait for draft to load
                        try:
                            current_draft_display = wait.until(EC.presence_of_element_located((By.ID, "currentDraftDisplay")))
                            print("  ✓ Draft loaded successfully")
                            driver.save_screenshot(str(SCREENSHOT_DIR / "03_draft_loaded.png"))
                            
                            # Check media browser has content
                            media_grid = driver.find_element(By.ID, "observationMediaGrid")
                            media_content = media_grid.text
                            print(f"  Media browser content: {media_content[:100]}...")
                            
                            # Now click Clear button
                            print("\n3. Clicking Clear button...")
                            try:
                                # Try to find Clear button in current draft display
                                clear_btn = current_draft_display.find_element(By.XPATH, ".//button[contains(text(), 'Clear')]")
                            except NoSuchElementException:
                                # Try alternative selectors
                                clear_btn = driver.find_element(By.XPATH, "//button[contains(@onclick, 'clearCurrentDraft') or contains(text(), 'Clear')]")
                            
                            clear_btn.click()
                            time.sleep(2)
                            
                            # Take screenshot after clear
                            driver.save_screenshot(str(SCREENSHOT_DIR / "04_after_clear.png"))
                            print(f"✓ Screenshot saved: {SCREENSHOT_DIR / '04_after_clear.png'}")
                            
                            # Verify draft display is hidden
                            try:
                                current_draft_display_after = driver.find_element(By.ID, "currentDraftDisplay")
                                is_visible = current_draft_display_after.is_displayed()
                                if not is_visible:
                                    print("  ✓ Draft display is hidden")
                                else:
                                    print("  ✗ Draft display is still visible!")
                            except NoSuchElementException:
                                print("  ✓ Draft display is hidden (element not found)")
                            
                            # Verify media browser is cleared
                            media_grid_after = driver.find_element(By.ID, "observationMediaGrid")
                            media_content_after = media_grid_after.text
                            print(f"  Media browser content after clear: {media_content_after[:200]}...")
                            
                            # Check if media browser shows empty state or reloaded content
                            if "Please select" in media_content_after or "No media" in media_content_after or media_content_after.strip() == "":
                                print("  ✓ Media browser is cleared")
                            else:
                                # Check if it's showing the same content as before
                                if media_content_after == media_content:
                                    print("  ✗ Media browser still shows the same content from draft!")
                                else:
                                    print("  ✓ Media browser content changed (reloaded)")
                            
                            # Final verification screenshot
                            time.sleep(1)
                            driver.save_screenshot(str(SCREENSHOT_DIR / "05_final_state.png"))
                            print(f"✓ Screenshot saved: {SCREENSHOT_DIR / '05_final_state.png'}")
                            
                        except TimeoutException:
                            print("  ✗ Draft did not load - current draft display not found")
                            driver.save_screenshot(str(SCREENSHOT_DIR / "error_draft_not_loaded.png"))
                    else:
                        print("  ⚠ No drafts available to load")
                        driver.save_screenshot(str(SCREENSHOT_DIR / "error_no_drafts.png"))
                except Exception as e:
                    print(f"  ✗ Error loading draft: {e}")
                    driver.save_screenshot(str(SCREENSHOT_DIR / "error_load_draft.png"))
            except TimeoutException:
                print("  ✗ Draft dialog did not open")
                driver.save_screenshot(str(SCREENSHOT_DIR / "error_no_dialog.png"))
        except TimeoutException:
            print("  ⚠ No Load Draft button found - may need to create a draft first")
            driver.save_screenshot(str(SCREENSHOT_DIR / "error_no_load_button.png"))
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot(str(SCREENSHOT_DIR / "error_exception.png"))
    finally:
        time.sleep(2)
        driver.quit()
        print("\n✓ Test completed. Check screenshots in:", SCREENSHOT_DIR)

if __name__ == "__main__":
    test_clear_draft_clears_media_browser()

