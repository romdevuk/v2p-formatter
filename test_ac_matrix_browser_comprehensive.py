"""
Comprehensive browser test for AC Matrix with screenshots
Tests both explicit unit mappings and drafts without explicit mappings
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pathlib import Path

def test_ac_matrix_comprehensive():
    """Test AC Matrix with different draft scenarios"""
    
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
        driver.save_screenshot(str(screenshot_dir / 'test1_initial.png'))
        print("✓ Screenshot 1: Initial page")
        
        # Select JSON file
        print("Selecting JSON standards file...")
        json_selector = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "json-file-selector"))
        )
        
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
        driver.save_screenshot(str(screenshot_dir / 'test2_bulk_mode.png'))
        print("✓ Screenshot 2: Bulk mode enabled")
        
        # Test 1: Draft with explicit unit mappings
        print("\n=== Test 1: Draft with Explicit Unit Mappings ===")
        add_report_btn = driver.find_element(By.ID, "add-report-btn")
        add_report_btn.click()
        time.sleep(1)
        
        report_textareas = driver.find_elements(By.CSS_SELECTOR, ".report-text")
        if report_textareas:
            report_text = """SECTION 1 – SITE ARRIVAL AND INDUCTION

1.

I arrived to the project on agreed time. I met Ivan at the gate where he followed security rules by signing in and passing fenced access. He already wore full PPE: high-viz, hard hat, gloves, boots and glasses.

AC covered: 

                641:1.1, 1.2, 1.3, 2.1, 4.1; 642:1.1

2.

Inside the induction room Ivan displayed CSCS card, signed RAMS and daily sheet.

AC covered: 

                641:5.1; 642:1.1, 4.1
"""
            report_textareas[-1].send_keys(report_text)
            
            report_names = driver.find_elements(By.CSS_SELECTOR, ".report-name")
            if report_names:
                report_names[-1].clear()
                report_names[-1].send_keys("2ndobsMy Draft")
        
        time.sleep(1)
        driver.save_screenshot(str(screenshot_dir / 'test3_draft_with_mappings.png'))
        print("✓ Screenshot 3: Draft with explicit unit mappings added")
        
        # Analyze
        print("Clicking Analyze button...")
        analyze_btn = driver.find_element(By.ID, "analyze-btn")
        analyze_btn.click()
        
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "matrix-section"))
        )
        time.sleep(3)
        driver.save_screenshot(str(screenshot_dir / 'test4_results_explicit_mappings.png'))
        print("✓ Screenshot 4: Results with explicit unit mappings")
        
        # Check results
        print("\n=== Checking Results (Explicit Mappings) ===")
        unit_headers = driver.find_elements(By.CSS_SELECTOR, ".matrix-horizontal-unit-header h3")
        
        expected_units_explicit = {'641', '642'}
        found_units_explicit = set()
        
        for header in unit_headers:
            unit_text = header.text
            unit_div = header.find_element(By.XPATH, "./ancestor::div[contains(@class, 'matrix-horizontal-unit')]")
            report_rows = unit_div.find_elements(By.CSS_SELECTOR, ".matrix-report-row")
            
            if report_rows:
                status_icons = []
                for row in report_rows:
                    status_icons.extend(row.find_elements(By.CSS_SELECTOR, ".matrix-horizontal-status.covered"))
                if status_icons:
                    # Extract unit ID from text
                    for unit_id in expected_units_explicit:
                        if unit_id in unit_text:
                            found_units_explicit.add(unit_id)
                            print(f"  ✅ Unit {unit_id} shows coverage ({len(status_icons)} ACs)")
                            break
        
        # Check unexpected units
        for header in unit_headers:
            unit_text = header.text
            if not any(uid in unit_text for uid in expected_units_explicit):
                unit_div = header.find_element(By.XPATH, "./ancestor::div[contains(@class, 'matrix-horizontal-unit')]")
                report_rows = unit_div.find_elements(By.CSS_SELECTOR, ".matrix-report-row")
                if report_rows:
                    status_icons = []
                    for row in report_rows:
                        status_icons.extend(row.find_elements(By.CSS_SELECTOR, ".matrix-horizontal-status.covered"))
                    if status_icons:
                        print(f"  ❌ ERROR: {unit_text} incorrectly shows coverage!")
        
        # Test 2: Draft without explicit mappings (should show all units)
        print("\n=== Test 2: Draft without Explicit Unit Mappings ===")
        
        # Clear and add new report
        remove_btns = driver.find_elements(By.CSS_SELECTOR, ".remove-report-btn")
        if remove_btns:
            remove_btns[0].click()
            time.sleep(1)
        
        add_report_btn.click()
        time.sleep(1)
        
        report_textareas = driver.find_elements(By.CSS_SELECTOR, ".report-text")
        if report_textareas:
            report_text = """SECTION 1 – SITE ARRIVAL AND INDUCTION

1.

I arrived to the project on agreed time. I met Ivan at the gate where he followed security rules by signing in and passing fenced access. He already wore full PPE: high-viz, hard hat, gloves, boots and glasses.

AC 1.1 was covered when the site manager explained the procedures.
AC 1.2 was demonstrated during the site induction.
AC 1.3 was observed when the worker followed safety protocols.
AC 2.1 was covered when proper equipment was used.
AC 3.1 was demonstrated during the task.
AC 3.2 was covered.
AC 3.3 was observed.
AC 3.4 was demonstrated.
AC 3.5 was covered.
AC 4.1 was observed.
AC 5.1 was demonstrated.

Inside the induction room Ivan displayed CSCS card, signed RAMS and daily sheet.

AC 2.2 was covered.
AC 4.2 was demonstrated.
"""
            report_textareas[-1].send_keys(report_text)
            
            report_names = driver.find_elements(By.CSS_SELECTOR, ".report-name")
            if report_names:
                report_names[-1].clear()
                report_names[-1].send_keys("My Draft")
        
        time.sleep(1)
        driver.save_screenshot(str(screenshot_dir / 'test5_draft_no_mappings.png'))
        print("✓ Screenshot 5: Draft without explicit mappings added")
        
        # Analyze
        print("Clicking Analyze button...")
        analyze_btn.click()
        
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "matrix-section"))
        )
        time.sleep(3)
        driver.save_screenshot(str(screenshot_dir / 'test6_results_no_mappings.png'))
        print("✓ Screenshot 6: Results without explicit mappings")
        
        # Check results - should show coverage in all units that have the mentioned ACs
        print("\n=== Checking Results (No Explicit Mappings) ===")
        unit_headers = driver.find_elements(By.CSS_SELECTOR, ".matrix-horizontal-unit-header h3")
        
        units_with_coverage = []
        units_without_coverage = []
        
        for header in unit_headers:
            unit_text = header.text
            unit_div = header.find_element(By.XPATH, "./ancestor::div[contains(@class, 'matrix-horizontal-unit')]")
            report_rows = unit_div.find_elements(By.CSS_SELECTOR, ".matrix-report-row")
            
            if report_rows:
                status_icons = []
                for row in report_rows:
                    status_icons.extend(row.find_elements(By.CSS_SELECTOR, ".matrix-horizontal-status.covered"))
                if status_icons:
                    units_with_coverage.append(unit_text)
                    print(f"  ✅ {unit_text}: {len(status_icons)} ACs covered")
                else:
                    units_without_coverage.append(unit_text)
            else:
                units_without_coverage.append(unit_text)
        
        print(f"\n=== Summary ===")
        print(f"Units with coverage: {len(units_with_coverage)}")
        print(f"Units without coverage: {len(units_without_coverage)}")
        
        if len(units_with_coverage) >= 2:
            print("✅ Matrix correctly shows coverage in multiple units")
        else:
            print("❌ ERROR: Matrix should show coverage in multiple units!")
        
        print(f"\nScreenshots saved to: {screenshot_dir}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot(str(screenshot_dir / 'test_error.png'))
    finally:
        driver.quit()

if __name__ == '__main__':
    test_ac_matrix_comprehensive()




