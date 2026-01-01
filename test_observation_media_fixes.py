#!/usr/bin/env python3
"""
Test script to verify fixes for:
1. Media browser filtering by draft subfolder
2. Live preview section toggle
3. Standards search functionality
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

def take_screenshot(driver, name):
    """Take a screenshot"""
    screenshot_dir = "test_screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    driver.save_screenshot(f"{screenshot_dir}/{name}.png")
    print(f"📸 Screenshot: {name}.png")

def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("=" * 60)
        print("Testing Observation Media Fixes")
        print("=" * 60)
        
        # Navigate to page
        url = "http://localhost/v2p-formatter/observation-media?qualification=Inter&learner=lakhmaniuk"
        print(f"\n🌐 Navigating to: {url}")
        driver.get(url)
        time.sleep(3)
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
                return
            
            # Wait for draft to load
            time.sleep(5)
            take_screenshot(driver, "02_draft_loaded")
            
            # Check draft loaded
            current_draft = driver.find_element(By.ID, "currentDraftName")
            if current_draft.is_displayed() and "learner_lakhmaniuk_obs1" in current_draft.text:
                print("✅ Draft loaded successfully")
            else:
                print("❌ Draft not loaded")
                return
                
        except Exception as e:
            print(f"❌ Draft loading failed: {e}")
            take_screenshot(driver, "error_draft_load")
            return
        
        # Test 2: Media Browser - Check if filtered by draft subfolder
        print("\n📁 Test 2: Media Browser Filtering")
        print("-" * 60)
        time.sleep(3)
        try:
            # Check subfolder select value (may not exist if no subfolders)
            selected_subfolder = None
            try:
                subfolder_select = driver.find_element(By.ID, "observationSubfolderSelect")
                selected_subfolder = subfolder_select.get_attribute("value")
                print(f"📂 Selected subfolder: {selected_subfolder}")
            except:
                print("📂 No subfolder select found (may not have subfolders)")
            
            # Check media grid
            media_grid = driver.find_element(By.ID, "observationMediaGrid")
            media_text = media_grid.text
            
            # Check if media is filtered (should only show media from draft's learner path)
            if "Display function not available" not in media_text:
                # Count actual media cards (not images/videos inside cards)
                media_items = driver.find_elements(By.CSS_SELECTOR, 
                    "#observationMediaGrid .observation-media-card")
                print(f"📊 Found {len(media_items)} media cards")
                
                # Check media paths if available
                if len(media_items) > 0:
                    first_card = media_items[0]
                    media_path = first_card.get_attribute("data-media-path") or ""
                    if "Inter/lakhmaniuk" in media_path:
                        print(f"✅ Media paths correct - first media: {media_path[:80]}...")
                    else:
                        print(f"⚠️ Media paths may be incorrect - first media: {media_path[:80]}...")
                
                # Check if subfolder sections match
                subfolder_sections = driver.find_elements(By.CSS_SELECTOR, ".media-subfolder-section")
                if selected_subfolder:
                    print(f"✅ Media browser should be filtered to subfolder: {selected_subfolder}")
                    if len(subfolder_sections) > 0:
                        print("⚠️ Multiple subfolders shown - may not be filtered correctly")
                    else:
                        print("✅ Only showing media from selected subfolder")
                else:
                    print("⚠️ No subfolder selected - showing all media")
            else:
                print("❌ Media browser: Display function not available")
            
            take_screenshot(driver, "03_media_browser")
        except Exception as e:
            print(f"⚠️ Media browser check failed: {e}")
        
        # Test 3: Live Preview - Test section toggle
        print("\n👁️ Test 3: Live Preview Section Toggle")
        print("-" * 60)
        time.sleep(2)
        try:
            preview = driver.find_element(By.ID, "observationPreview")
            preview_html = preview.get_attribute("innerHTML")
            
            # Find section headers
            section_headers = driver.find_elements(By.CSS_SELECTOR, ".observation-section-header")
            print(f"📋 Found {len(section_headers)} sections")
            
            if len(section_headers) > 0:
                # Click first section header
                first_section = section_headers[0]
                section_id = first_section.find_element(By.XPATH, "./..").get_attribute("data-section-id")
                print(f"🖱️ Clicking section: {section_id}")
                
                # Check initial state
                section_content = driver.find_element(By.CSS_SELECTOR, f"[data-section-id='{section_id}'] .observation-section-content")
                initial_display = section_content.value_of_css_property("display")
                print(f"📊 Initial display: {initial_display}")
                
                # Click to toggle
                first_section.click()
                time.sleep(1)
                
                # Check new state
                section_content = driver.find_element(By.CSS_SELECTOR, f"[data-section-id='{section_id}'] .observation-section-content")
                new_display = section_content.value_of_css_property("display")
                print(f"📊 New display: {new_display}")
                
                if initial_display != new_display:
                    print("✅ Section toggle working!")
                else:
                    print("❌ Section toggle not working - display unchanged")
                
                take_screenshot(driver, "04_section_toggle")
            else:
                print("⚠️ No sections found in preview")
        except Exception as e:
            print(f"❌ Section toggle test failed: {e}")
            take_screenshot(driver, "error_section_toggle")
        
        # Test 4: Standards Search
        print("\n🔍 Test 4: Standards Search")
        print("-" * 60)
        time.sleep(2)
        try:
            search_input = driver.find_element(By.ID, "standardsSearchInput")
            if search_input:
                print("✅ Search input found")
                
                # Type a search term
                search_term = "health"
                print(f"🔍 Searching for: '{search_term}'")
                search_input.clear()
                search_input.send_keys(search_term)
                time.sleep(2)  # Wait for debounce
                
                take_screenshot(driver, "05_standards_search")
                
                # Check for results
                standards_content = driver.find_element(By.ID, "standardsContent")
                standards_html = standards_content.get_attribute("innerHTML")
                
                # Check for highlighted text
                highlights = driver.find_elements(By.CSS_SELECTOR, ".standards-search-highlight")
                print(f"✨ Found {len(highlights)} highlighted matches")
                
                # Check for no results message
                no_results = driver.find_elements(By.CSS_SELECTOR, ".standards-no-results")
                if no_results:
                    print(f"⚠️ No results message: {no_results[0].text}")
                else:
                    print("✅ Search executed (no 'no results' message)")
                
                # Check if ACs are hidden/shown
                acs = driver.find_elements(By.CSS_SELECTOR, ".standards-ac")
                visible_acs = [ac for ac in acs if ac.is_displayed()]
                print(f"📊 Total ACs: {len(acs)}, Visible: {len(visible_acs)}")
                
                if len(highlights) > 0 or len(visible_acs) < len(acs):
                    print("✅ Search filtering working!")
                else:
                    print("⚠️ Search may not be filtering results")
                
                # Clear search
                clear_btn = driver.find_element(By.ID, "standardsSearchClear")
                if clear_btn.is_displayed():
                    clear_btn.click()
                    time.sleep(1)
                    print("✅ Search cleared")
            else:
                print("❌ Search input not found")
        except Exception as e:
            print(f"❌ Standards search test failed: {e}")
            take_screenshot(driver, "error_standards_search")
        
        print("\n" + "=" * 60)
        print("✅ All tests completed")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        take_screenshot(driver, "error_final")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

