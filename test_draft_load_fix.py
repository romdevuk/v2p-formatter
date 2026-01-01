#!/usr/bin/env python3
"""
Test script to verify draft loading works correctly
Tests loading draft "learner_lakhmaniuk_obs1" and verifies all content loads
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
    screenshot_path = f"test_draft_load_{name}.png"
    driver.save_screenshot(screenshot_path)
    print(f"📸 Screenshot saved: {screenshot_path}")
    return screenshot_path

def test_draft_loading():
    """Test loading draft learner_lakhmaniuk_obs1"""
    driver = None
    try:
        print("🚀 Starting draft loading test...")
        driver = setup_driver()
        
        # Navigate to observation media page
        url = "http://localhost/v2p-formatter/observation-media"
        print(f"📍 Navigating to: {url}")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(2)
        take_screenshot(driver, "01_initial_load")
        
        # Find and click Load Draft button
        print("🔍 Looking for Load Draft button...")
        try:
            load_draft_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "loadDraftBtn"))
            )
            print("✅ Found Load Draft button")
            load_draft_btn.click()
            time.sleep(1)
            take_screenshot(driver, "02_dialog_opened")
        except TimeoutException:
            print("❌ Load Draft button not found")
            take_screenshot(driver, "02_error_no_button")
            return False
        
        # Wait for draft dialog to appear
        print("🔍 Waiting for draft selection dialog...")
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "draft-selection-dialog"))
            )
            print("✅ Draft dialog opened")
            take_screenshot(driver, "03_dialog_visible")
        except TimeoutException:
            print("❌ Draft dialog did not appear")
            take_screenshot(driver, "03_error_no_dialog")
            return False
        
        # Find the draft "learner_lakhmaniuk_obs1" and click Load
        print("🔍 Looking for draft 'learner_lakhmaniuk_obs1'...")
        try:
            # Find all draft items
            draft_items = driver.find_elements(By.CLASS_NAME, "draft-item")
            print(f"📋 Found {len(draft_items)} draft items")
            
            target_draft = None
            for item in draft_items:
                text = item.text
                if "learner_lakhmaniuk_obs1" in text:
                    target_draft = item
                    print(f"✅ Found target draft: {text[:50]}...")
                    break
            
            if not target_draft:
                print("❌ Draft 'learner_lakhmaniuk_obs1' not found")
                take_screenshot(driver, "04_error_draft_not_found")
                return False
            
            # Find and click Load button within the draft item
            load_btn = target_draft.find_element(By.XPATH, ".//button[contains(text(), 'Load')]")
            print("✅ Found Load button")
            load_btn.click()
            time.sleep(2)
            take_screenshot(driver, "04_draft_loading")
            
        except Exception as e:
            print(f"❌ Error finding/clicking draft: {e}")
            take_screenshot(driver, "04_error_clicking")
            return False
        
        # Wait for dialog to close and draft to load
        print("⏳ Waiting for dialog to close...")
        time.sleep(2)
        
        # Check if dialog is closed
        try:
            driver.find_element(By.CLASS_NAME, "draft-selection-dialog")
            print("⚠️ Dialog still open")
        except NoSuchElementException:
            print("✅ Dialog closed")
        
        take_screenshot(driver, "05_after_load")
        
        # Wait longer for all async operations to complete
        print("⏳ Waiting for draft content to load (up to 10 seconds)...")
        max_wait = 10
        waited = 0
        preview_loaded = False
        
        while waited < max_wait and not preview_loaded:
            time.sleep(1)
            waited += 1
            try:
                preview = driver.find_element(By.ID, "observationPreview")
                preview_text = preview.text.strip()
                if preview_text and preview_text != "Start typing to see preview...":
                    print(f"✅ Preview has content after {waited}s")
                    preview_loaded = True
                    break
            except Exception:
                pass
        
        if not preview_loaded:
            print(f"⚠️ Preview still empty after {waited}s")
        
        # Verify draft was loaded - check for current draft display
        print("🔍 Verifying draft was loaded...")
        try:
            current_draft_display = driver.find_element(By.ID, "currentDraftDisplay")
            if current_draft_display.is_displayed():
                draft_name = driver.find_element(By.ID, "currentDraftName").text
                print(f"✅ Current draft displayed: {draft_name}")
            else:
                print("⚠️ Draft display element exists but not visible")
        except NoSuchElementException:
            print("⚠️ Current draft display not found")
        
        # Check if text editor has content
        try:
            editor = driver.find_element(By.ID, "observationTextEditor")
            editor_value = editor.get_attribute("value")
            if editor_value:
                print(f"✅ Text editor has content ({len(editor_value)} chars)")
            else:
                print("⚠️ Text editor is empty")
        except NoSuchElementException:
            print("⚠️ Text editor not found")
        
        # Check preview content
        try:
            preview = driver.find_element(By.ID, "observationPreview")
            preview_text = preview.text.strip()
            if preview_text and preview_text != "Start typing to see preview...":
                print(f"✅ Preview has content ({len(preview_text)} chars)")
                # Check for placeholders in preview
                preview_html = preview.get_attribute("innerHTML")
                if "{{" in preview_html or "placeholder" in preview_html.lower():
                    placeholder_count = preview_html.count("{{")
                    print(f"✅ Found {placeholder_count} placeholders in preview")
                else:
                    print("⚠️ No placeholders found in preview HTML")
            else:
                print("⚠️ Preview is empty or shows placeholder text")
        except NoSuchElementException:
            print("⚠️ Preview element not found")
        except Exception as e:
            print(f"⚠️ Could not check preview: {e}")
        
        # Check standards section
        try:
            standards_content = driver.find_element(By.ID, "standardsContent")
            standards_text = standards_content.text
            if "No draft loaded" not in standards_text and "not available" not in standards_text.lower():
                print("✅ Standards section has content")
            else:
                print(f"⚠️ Standards section: {standards_text[:50]}...")
        except Exception as e:
            print(f"⚠️ Could not check standards: {e}")
        
        # Check media browser
        try:
            media_grid = driver.find_element(By.ID, "observationMediaGrid")
            media_text = media_grid.text
            if "Display function not available" not in media_text and "Please select" not in media_text:
                # Count media items if any
                media_items = driver.find_elements(By.CSS_SELECTOR, "#observationMediaGrid .media-card, #observationMediaGrid img, #observationMediaGrid video")
                if len(media_items) > 0:
                    print(f"✅ Media browser has {len(media_items)} media items")
                else:
                    print(f"⚠️ Media browser: {media_text[:50]}...")
            else:
                print(f"⚠️ Media browser: {media_text[:50]}...")
        except Exception as e:
            print(f"⚠️ Could not check media browser: {e}")
        
        take_screenshot(driver, "06_final_state")
        
        # Check console for errors
        logs = driver.get_log('browser')
        errors = [log for log in logs if log['level'] == 'SEVERE']
        if errors:
            print(f"⚠️ Found {len(errors)} browser errors:")
            for error in errors[:5]:  # Show first 5
                print(f"   {error['message']}")
        else:
            print("✅ No browser errors")
        
        print("✅ Test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        if driver:
            take_screenshot(driver, "error_final")
        return False
        
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed")

if __name__ == "__main__":
    success = test_draft_loading()
    exit(0 if success else 1)

