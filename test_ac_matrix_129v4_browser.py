"""
Browser test to verify Unit 129v4 shows coverage with actual draft
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from pathlib import Path

def test_129v4_coverage():
    """Test that Unit 129v4 shows coverage when using actual draft"""
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    screenshot_dir = Path('reports/screenshots')
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Navigate to AC Matrix page
        print("Navigating to AC Matrix page...")
        driver.get('http://localhost/v2p-formatter/ac-matrix')
        time.sleep(2)
        
        # Select JSON file
        print("Selecting JSON standards file...")
        json_selector = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "json-file-selector"))
        )
        
        select = Select(json_selector)
        options = select.options
        for option in options:
            if 'l2inter-performance' in option.text.lower() or 'Level 2' in option.text:
                select.select_by_visible_text(option.text)
                break
        
        time.sleep(1)
        
        # Switch to bulk reports mode
        print("Switching to bulk reports mode...")
        bulk_radio = driver.find_element(By.CSS_SELECTOR, 'input[name="report-mode"][value="bulk"]')
        bulk_radio.click()
        time.sleep(1)
        
        # Load draft from dropdown
        print("Loading draft from dropdown...")
        draft_selector = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "bulk-drafts-selector"))
        )
        
        select = Select(draft_selector)
        # Find "My Draft" option
        for option in select.options:
            if 'My Draft' in option.text and '2ndobs' not in option.text:
                select.select_by_visible_text(option.text)
                break
        
        time.sleep(1)
        
        # Click "Add Selected Drafts" button
        add_drafts_btn = driver.find_element(By.ID, "add-selected-drafts-btn")
        add_drafts_btn.click()
        time.sleep(2)
        
        driver.save_screenshot(str(screenshot_dir / 'test_129v4_draft_loaded.png'))
        print("✓ Screenshot: Draft loaded")
        
        # Analyze
        print("Clicking Analyze button...")
        analyze_btn = driver.find_element(By.ID, "analyze-btn")
        analyze_btn.click()
        
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "matrix-section"))
        )
        time.sleep(3)
        
        driver.save_screenshot(str(screenshot_dir / 'test_129v4_results.png'))
        print("✓ Screenshot: Results displayed")
        
        # Check Unit 129v4 coverage
        print("\n=== Checking Unit 129v4 Coverage ===")
        unit_headers = driver.find_elements(By.CSS_SELECTOR, ".matrix-horizontal-unit-header h3")
        
        unit_129v4_found = False
        for header in unit_headers:
            unit_text = header.text
            if '129v4' in unit_text:
                unit_129v4_found = True
                print(f"Found: {unit_text}")
                
                unit_div = header.find_element(By.XPATH, "./ancestor::div[contains(@class, 'matrix-horizontal-unit')]")
                report_rows = unit_div.find_elements(By.CSS_SELECTOR, ".matrix-report-row")
                
                if report_rows:
                    for row in report_rows:
                        status_icons = row.find_elements(By.CSS_SELECTOR, ".matrix-horizontal-status.covered")
                        if status_icons:
                            print(f"  ✅ Unit 129v4 shows {len(status_icons)} covered ACs")
                        else:
                            print(f"  ❌ Unit 129v4 shows NO covered ACs")
                else:
                    print(f"  ❌ Unit 129v4 has no report rows")
                break
        
        if not unit_129v4_found:
            print("  ❌ ERROR: Unit 129v4 not found in matrix!")
        
        print(f"\nScreenshots saved to: {screenshot_dir}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot(str(screenshot_dir / 'test_129v4_error.png'))
    finally:
        driver.quit()

if __name__ == '__main__':
    test_129v4_coverage()




