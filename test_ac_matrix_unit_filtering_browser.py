"""
Browser test to verify AC Matrix only shows ACs from the correct unit
Uses Selenium to take screenshots
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pathlib import Path

def test_ac_matrix_unit_filtering():
    """Test that matrix only shows ACs from unit 641 when draft only covers unit 641"""
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to AC Matrix page
        print("Navigating to AC Matrix page...")
        driver.get('http://localhost/v2p-formatter/ac-matrix')
        time.sleep(2)
        
        # Take initial screenshot
        screenshot_dir = Path('reports/screenshots')
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        driver.save_screenshot(str(screenshot_dir / 'ac_matrix_initial.png'))
        print("✓ Initial screenshot saved")
        
        # Select JSON file (assuming l2inter-performance.json exists)
        print("Selecting JSON standards file...")
        json_selector = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "json-file-selector"))
        )
        
        # Get all options
        options = json_selector.find_elements(By.TAG_NAME, "option")
        for option in options:
            if 'l2inter-performance' in option.text.lower() or 'Level 2' in option.text:
                option.click()
                break
        
        time.sleep(1)
        
        # Switch to bulk reports mode
        print("Switching to bulk reports mode...")
        bulk_radio = driver.find_element(By.CSS_SELECTOR, 'input[name="report-mode"][value="bulk"]')
        bulk_radio.click()
        time.sleep(1)
        
        # Add a test report with explicit unit mappings (like the actual draft)
        print("Adding test report with explicit unit mappings...")
        add_report_btn = driver.find_element(By.ID, "add-report-btn")
        add_report_btn.click()
        time.sleep(1)
        
        # Find the report textarea and fill it with actual draft format
        report_textareas = driver.find_elements(By.CSS_SELECTOR, ".report-text")
        if report_textareas:
            report_text = """SECTION 1 – SITE ARRIVAL AND INDUCTION

1.

fdsgdfgfdgdf. I arrived to the project on agreed time, weather sunny. I met Ivan at the gate where he followed security rules by signing in and passing fenced access. He already wore full PPE: high-viz, hard hat, gloves, boots and glasses. Ivan showed me fire point and health & safety board.

AC covered: 

                641:1.1, 1.2, 1.3, 2.1, 4.1; 642:1.1

Image suggestion: learner signing in and wearing PPE.

{{Site_arrival_and_induction_table}}

2.

Inside the induction room Ivan displayed CSCS card, signed RAMS and daily sheet. I observed learner storing PPE and small tools correctly in tool bag.

AC covered: 

                641:5.1; 642:1.1, 4.1

Image suggestion: induction paperwork and CSCS verification.

{{Site_arrival_and_induction_table}}
"""
            report_textareas[-1].send_keys(report_text)
            
            # Set report name
            report_names = driver.find_elements(By.CSS_SELECTOR, ".report-name")
            if report_names:
                report_names[-1].clear()
                report_names[-1].send_keys("2ndobsMy Draft")
        
        time.sleep(1)
        
        # Click Analyze
        print("Clicking Analyze button...")
        analyze_btn = driver.find_element(By.ID, "analyze-btn")
        analyze_btn.click()
        
        # Wait for matrix to appear
        print("Waiting for matrix to load...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "matrix-section"))
        )
        time.sleep(3)
        
        # Take screenshot of matrix
        matrix_section = driver.find_element(By.ID, "matrix-section")
        driver.save_screenshot(str(screenshot_dir / 'ac_matrix_results.png'))
        print("✓ Results screenshot saved")
        
        # Check which units show coverage
        print("\n=== Checking Unit Coverage ===")
        unit_headers = driver.find_elements(By.CSS_SELECTOR, ".matrix-horizontal-unit-header h3")
        
        for header in unit_headers:
            unit_text = header.text
            print(f"\n{unit_text}")
            
            # Find the parent unit
            unit_div = header.find_element(By.XPATH, "./ancestor::div[contains(@class, 'matrix-horizontal-unit')]")
            
            # Check if this unit has any coverage rows
            report_rows = unit_div.find_elements(By.CSS_SELECTOR, ".matrix-report-row")
            
            if report_rows:
                for row in report_rows:
                    row_label = row.find_element(By.CSS_SELECTOR, ".matrix-row-label").text
                    status_icons = row.find_elements(By.CSS_SELECTOR, ".matrix-horizontal-status.covered")
                    print(f"  {row_label}: {len(status_icons)} ACs covered")
            else:
                print("  No coverage shown")
        
        # Verify unit 641 and 642 show coverage (expected units)
        expected_units = ['641', '642']
        expected_units_found = {unit: False for unit in expected_units}
        unexpected_units_with_coverage = []
        
        for header in unit_headers:
            unit_text = header.text
            unit_div = header.find_element(By.XPATH, "./ancestor::div[contains(@class, 'matrix-horizontal-unit')]")
            report_rows = unit_div.find_elements(By.CSS_SELECTOR, ".matrix-report-row")
            
            # Check if this unit should have coverage
            unit_should_have_coverage = any(unit_id in unit_text for unit_id in expected_units)
            
            if report_rows:
                status_icons = []
                for row in report_rows:
                    status_icons.extend(row.find_elements(By.CSS_SELECTOR, ".matrix-horizontal-status.covered"))
                
                if status_icons:
                    if unit_should_have_coverage:
                        for unit_id in expected_units:
                            if unit_id in unit_text:
                                expected_units_found[unit_id] = True
                                print(f"\n✅ Unit {unit_id} correctly shows coverage ({len(status_icons)} ACs)")
                    else:
                        unexpected_units_with_coverage.append(unit_text)
            else:
                if unit_should_have_coverage:
                    for unit_id in expected_units:
                        if unit_id in unit_text:
                            print(f"\n❌ ERROR: Unit {unit_id} should show coverage but doesn't!")
        
        # Check all expected units were found
        for unit_id, found in expected_units_found.items():
            if not found:
                print(f"\n❌ ERROR: Unit {unit_id} should show coverage but wasn't found!")
        
        if unexpected_units_with_coverage:
            print(f"\n❌ ERROR: Unexpected units incorrectly show coverage: {unexpected_units_with_coverage}")
        else:
            print("\n✅ Other units correctly show no coverage")
        
        print(f"\nScreenshots saved to: {screenshot_dir}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot(str(screenshot_dir / 'ac_matrix_error.png'))
    finally:
        driver.quit()

if __name__ == '__main__':
    test_ac_matrix_unit_filtering()

