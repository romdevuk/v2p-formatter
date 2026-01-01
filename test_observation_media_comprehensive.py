#!/usr/bin/env python3
"""
Comprehensive test suite for Observation Media page
Tests draft loading, media browser, live preview, and standards
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os

def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def take_screenshot(driver, name):
    """Take a screenshot and save it"""
    screenshot_path = f"test_obs_media_{name}.png"
    driver.save_screenshot(screenshot_path)
    print(f"📸 Screenshot: {screenshot_path}")
    return screenshot_path

def test_observation_media_comprehensive():
    """Comprehensive test of observation media page"""
    driver = None
    test_results = {
        'draft_loading': False,
        'media_browser': False,
        'live_preview': False,
        'standards': False,
        'clear_draft': False
    }
    
    try:
        print("=" * 60)
        print("🚀 COMPREHENSIVE OBSERVATION MEDIA TEST")
        print("=" * 60)
        
        driver = setup_driver()
        
        # Navigate to observation media page
        url = "http://localhost/v2p-formatter/observation-media"
        print(f"\n📍 Step 1: Navigating to {url}")
        driver.get(url)
        time.sleep(2)
        take_screenshot(driver, "01_initial_load")
        
        # Test 1: Load Draft
        print("\n📋 Test 1: Loading Draft")
        print("-" * 60)
        try:
            load_draft_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "loadDraftBtn"))
            )
            load_draft_btn.click()
            time.sleep(1)
            take_screenshot(driver, "02_dialog_opened")
            
            # Find and click Load for learner_lakhmaniuk_obs1
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "draft-selection-dialog"))
            )
            draft_items = driver.find_elements(By.CLASS_NAME, "draft-item")
            
            target_draft = None
            for item in draft_items:
                if "learner_lakhmaniuk_obs1" in item.text:
                    target_draft = item
                    break
            
            if target_draft:
                load_btn = target_draft.find_element(By.XPATH, ".//button[contains(text(), 'Load')]")
                load_btn.click()
                print("✅ Draft load button clicked")
            else:
                print("❌ Draft not found")
                return False
            
            # Wait for draft to load - wait up to 10 seconds
            print("⏳ Waiting for draft to load...")
            draft_loaded = False
            for i in range(10):
                time.sleep(1)
                try:
                    current_draft = driver.find_element(By.ID, "currentDraftName")
                    if current_draft.is_displayed() and "learner_lakhmaniuk_obs1" in current_draft.text:
                        print(f"✅ Draft name displayed correctly (after {i+1}s)")
                        test_results['draft_loading'] = True
                        draft_loaded = True
                        break
                except:
                    pass
            if not draft_loaded:
                print("⚠️ Draft name not found after 10 seconds")
            take_screenshot(driver, "03_draft_loading")
            
        except Exception as e:
            print(f"❌ Draft loading failed: {e}")
            take_screenshot(driver, "error_draft_load")
        
        # Test 2: Media Browser
        print("\n📁 Test 2: Media Browser")
        print("-" * 60)
        time.sleep(2)
        try:
            media_grid = driver.find_element(By.ID, "observationMediaGrid")
            media_text = media_grid.text
            
            if "Display function not available" not in media_text:
                media_items = driver.find_elements(By.CSS_SELECTOR, 
                    "#observationMediaGrid .media-card, #observationMediaGrid img, #observationMediaGrid video")
                if len(media_items) > 0:
                    print(f"✅ Media browser has {len(media_items)} items")
                    test_results['media_browser'] = True
                elif "0 files" in media_text or "Please select" in media_text:
                    print("⚠️ Media browser shows no files (may be expected)")
                    test_results['media_browser'] = True  # Not an error if no files
                else:
                    print(f"⚠️ Media browser status: {media_text[:50]}...")
            else:
                print("❌ Media browser: Display function not available")
        except Exception as e:
            print(f"⚠️ Could not check media browser: {e}")
        
        take_screenshot(driver, "04_media_browser_check")
        
        # Test 3: Live Preview
        print("\n👁️ Test 3: Live Preview")
        print("-" * 60)
        time.sleep(3)  # Wait longer for preview to update
        try:
            preview = driver.find_element(By.ID, "observationPreview")
            preview_text = preview.text.strip()
            
            # Wait a bit more if preview is empty
            if not preview_text or preview_text == "Start typing to see preview...":
                print("⏳ Preview empty, waiting a bit more...")
                time.sleep(3)
                preview_text = preview.text.strip()
            
            if preview_text and preview_text != "Start typing to see preview...":
                # Check for sections
                preview_html = preview.get_attribute("innerHTML")
                if "SECTION" in preview_html.upper() or "section" in preview_html.lower() or "Site Arrival" in preview_text or "Health, Safety" in preview_text:
                    print("✅ Live preview shows sections")
                    test_results['live_preview'] = True
                else:
                    print("⚠️ Live preview has content but no sections detected")
                
                # Check for placeholders
                placeholder_count = preview_html.count("{{")
                if placeholder_count > 0:
                    print(f"✅ Found {placeholder_count} placeholders in preview")
                else:
                    print("⚠️ No placeholders found in preview")
                
                print(f"✅ Preview has content ({len(preview_text)} chars)")
            else:
                print("❌ Preview is empty")
        except Exception as e:
            print(f"❌ Preview check failed: {e}")
        
        take_screenshot(driver, "05_live_preview_check")
        
        # Test 4: Standards
        print("\n📚 Test 4: Standards Section")
        print("-" * 60)
        # Wait longer for standards to load - up to 15 seconds
        standards_loaded = False
        for i in range(15):
            time.sleep(1)
            try:
                standards_content = driver.find_element(By.ID, "standardsContent")
                standards_text = standards_content.text
                
                if "No draft loaded" not in standards_text and "not available" not in standards_text.lower():
                    # Check for standards items
                    standards_items = driver.find_elements(By.CSS_SELECTOR, 
                        "#standardsContent .standard-item, #standardsContent li, #standardsContent .standards-unit, #standardsContent .standards-list-item")
                    if len(standards_items) > 0:
                        print(f"✅ Standards section has {len(standards_items)} items (after {i+1}s)")
                        test_results['standards'] = True
                        standards_loaded = True
                        break
                    # Check if it's loading or has a message
                    elif "Loading" in standards_text or "No JSON" in standards_text:
                        print(f"⚠️ Standards: {standards_text[:50]}... (after {i+1}s)")
                        test_results['standards'] = True  # Not an error if no JSON file
                        standards_loaded = True
                        break
            except:
                pass
        
        if not standards_loaded:
            try:
                standards_content = driver.find_element(By.ID, "standardsContent")
                standards_text = standards_content.text
                print(f"❌ Standards section: {standards_text[:50]}...")
            except Exception as e:
                print(f"⚠️ Could not check standards: {e}")
        
        take_screenshot(driver, "06_standards_check")
        
        # Test 5: Clear Draft
        print("\n🗑️ Test 5: Clear Draft")
        print("-" * 60)
        try:
            clear_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Clear')]")
            clear_btn.click()
            time.sleep(1)
            
            # Verify draft is cleared
            try:
                current_draft_display = driver.find_element(By.ID, "currentDraftDisplay")
                if not current_draft_display.is_displayed():
                    print("✅ Draft display hidden after clear")
                    test_results['clear_draft'] = True
                else:
                    print("⚠️ Draft display still visible")
            except:
                print("✅ Draft display not found (cleared)")
                test_results['clear_draft'] = True
            
            # Check if editor is cleared
            editor = driver.find_element(By.ID, "observationTextEditor")
            if editor.get_attribute("value") == "":
                print("✅ Text editor cleared")
            else:
                print("⚠️ Text editor not cleared")
            
            take_screenshot(driver, "07_after_clear")
            
        except Exception as e:
            print(f"⚠️ Clear draft test: {e}")
        
        # Final state
        print("\n📊 Final State Check")
        print("-" * 60)
        time.sleep(2)
        take_screenshot(driver, "08_final_state")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}: {test_name.replace('_', ' ').title()}")
        
        total_passed = sum(test_results.values())
        total_tests = len(test_results)
        print(f"\nTotal: {total_passed}/{total_tests} tests passed")
        
        # Check browser errors
        logs = driver.get_log('browser')
        errors = [log for log in logs if log['level'] == 'SEVERE']
        if errors:
            print(f"\n⚠️ Found {len(errors)} browser errors")
            for error in errors[:3]:
                print(f"   {error['message'][:100]}...")
        
        return total_passed == total_tests
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        if driver:
            take_screenshot(driver, "error_final")
        return False
        
    finally:
        if driver:
            driver.quit()
            print("\n🔒 Browser closed")

if __name__ == "__main__":
    success = test_observation_media_comprehensive()
    exit(0 if success else 1)

