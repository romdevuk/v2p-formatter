#!/usr/bin/env python3
"""
Test standalone reshuffle functionality
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sys

def take_screenshot(driver, name):
    screenshot_dir = "test_screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    path = os.path.join(screenshot_dir, f"{name}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot: {path}")
    return path

def test_reshuffle_standalone():
    print("=" * 60)
    print("🧪 Testing Standalone Reshuffle")
    print("=" * 60)
    
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    
    try:
        url = "http://localhost/v2p-formatter/observation-media?qualification=Inter&learner=lakhmaniuk"
        print(f"\n🌐 Navigating to: {url}")
        driver.get(url)
        time.sleep(3)
        
        wait = WebDriverWait(driver, 10)
        
        # Load draft
        print("\n📋 Loading draft...")
        try:
            draft_btn = driver.find_element(By.ID, "loadDraftBtn")
            driver.execute_script("arguments[0].click();", draft_btn)
            time.sleep(2)
            
            try:
                backdrop = driver.find_element(By.CSS_SELECTOR, ".draft-selection-backdrop")
                driver.execute_script("arguments[0].style.display = 'none';", backdrop)
            except:
                pass
            
            load_buttons = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Load') and not(contains(text(), 'Draft'))]"))
            )
            if load_buttons:
                driver.execute_script("arguments[0].click();", load_buttons[0])
                time.sleep(3)
                print("✅ Draft loaded")
        except Exception as e:
            print(f"⚠️ Could not load draft: {e}")
        
        # Open a section
        print("\n🔍 Opening section...")
        try:
            sections = driver.find_elements(By.CSS_SELECTOR, ".observation-section.collapsed")
            if sections:
                section_header = sections[0].find_element(By.CSS_SELECTOR, ".observation-section-header")
                driver.execute_script("arguments[0].click();", section_header)
                time.sleep(2)
                print("✅ Section opened")
        except Exception as e:
            print(f"⚠️ Could not open section: {e}")
        
        # Test reshuffle function directly
        print("\n🔄 Testing reshuffle function directly...")
        
        test_script = """
        // Get assignments
        var assignments = window.observationMediaAssignments || {};
        var placeholder = 'site_arrival_and_induction_table';
        var placeholderKey = placeholder.toLowerCase();
        
        if (!assignments[placeholderKey] || assignments[placeholderKey].length < 2) {
            return {success: false, error: 'Not enough media items'};
        }
        
        var before = assignments[placeholderKey].map((m, i) => ({index: i, name: m.name || m.path}));
        console.log('[TEST] Before:', before);
        
        // Call reorderMedia directly
        if (typeof window.reorderMedia === 'function') {
            var result = window.reorderMedia(placeholder, 0, 1);
            var after = assignments[placeholderKey].map((m, i) => ({index: i, name: m.name || m.path}));
            console.log('[TEST] After:', after);
            
            return {
                success: result,
                before: before,
                after: after,
                changed: before[0].name !== after[0].name || before[1].name !== after[1].name
            };
        } else {
            return {success: false, error: 'reorderMedia function not found'};
        }
        """
        
        result = driver.execute_script(test_script)
        print(f"✅ Test result: {result}")
        
        if result.get('success') and result.get('changed'):
            print("✅ Reshuffle function works!")
            take_screenshot(driver, "reshuffle_success")
            return True
        else:
            print("❌ Reshuffle function failed")
            print(f"   Error: {result.get('error')}")
            print(f"   Changed: {result.get('changed')}")
            take_screenshot(driver, "reshuffle_failed")
            return False
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    success = test_reshuffle_standalone()
    print("\n" + "=" * 60)
    if success:
        print("✅ TEST PASSED")
    else:
        print("❌ TEST FAILED")
    print("=" * 60)
    sys.exit(0 if success else 1)



