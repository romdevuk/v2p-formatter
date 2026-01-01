"""
Test script to verify trim empty paragraphs functionality
Tests that when section titles are hidden, empty paragraphs are trimmed to 1
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import os

# Setup
SCREENSHOT_DIR = Path("reports/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=chrome_options)

def take_screenshot(driver, name):
    """Take a screenshot and save it"""
    filepath = SCREENSHOT_DIR / f"{name}.png"
    driver.save_screenshot(str(filepath))
    print(f"📸 Screenshot saved: {filepath}")
    return filepath

def test_trim_empty_paragraphs():
    """Test trim empty paragraphs functionality"""
    driver = setup_driver()
    
    try:
        print("🌐 Opening observation media page...")
        driver.get("http://localhost/v2p-formatter/observation-media")
        time.sleep(2)
        
        # Take initial screenshot
        take_screenshot(driver, "01_initial_page")
        
        # Check if there's a draft to load
        print("📂 Checking for drafts...")
        load_draft_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "loadDraftBtn"))
        )
        load_draft_btn.click()
        time.sleep(1)
        
        # Try to load first draft if available
        try:
            draft_items = driver.find_elements(By.CSS_SELECTOR, ".draft-item")
            if draft_items:
                print(f"📄 Found {len(draft_items)} draft(s), loading first one...")
                draft_items[0].click()
                time.sleep(2)
                take_screenshot(driver, "02_draft_loaded")
            else:
                print("⚠️ No drafts found, creating test content...")
                # Enter some test content
                text_editor = driver.find_element(By.ID, "observationTextEditor")
                test_text = """SECTION 1 - TEST SECTION

Ivan was on site wearing full PPE and preparing his work area within a narrow internal corridor undergoing refurbishment. He mentioned that he had completed the site induction earlier that morning and reviewed the RAMS, paying attention to manual handling, cutting tools and working at height. Materials were positioned to keep the walkway clear for other operatives. (129v4: 1.1, 1.2; 130v3: 1.1, 1.2; 643: 1.1, 1.2)

SECTION 2 - ANOTHER SECTION

Plasterboards were sorted and stored safely upright along the corridor wall to avoid bending. Using drawings for reference, Ivan measured and marked the boards with a tape measure. When asked about reducing waste, he explained that he plans his cutting sequence, checks dimensions twice and confirms service locations with other trades before cutting. (129v4: 3.1, 3.2; 130v3: 3.1, 3.2; 643: 3.1, 3.2, 4.1)"""
                text_editor.clear()
                text_editor.send_keys(test_text)
                time.sleep(1)
                take_screenshot(driver, "02_test_content_entered")
        except Exception as e:
            print(f"⚠️ Could not load draft: {e}")
        
        # Open preview
        print("👁️ Opening document preview...")
        preview_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "previewDraftBtn"))
        )
        preview_btn.click()
        time.sleep(2)
        
        take_screenshot(driver, "03_preview_opened")
        
        # Enable "Trim empty paragraphs" and hide section titles
        print("⚙️ Configuring settings...")
        
        # Find and check "Trim empty paragraphs"
        trim_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "trimEmptyParagraphs"))
        )
        if not trim_checkbox.is_selected():
            trim_checkbox.click()
            time.sleep(0.5)
        
        # Find and check "Section Titles" to hide them
        section_titles_checkbox = driver.find_element(By.ID, "hideSectionTitles")
        if not section_titles_checkbox.is_selected():
            section_titles_checkbox.click()
            time.sleep(0.5)
        
        # Wait for updates to apply
        time.sleep(1)
        take_screenshot(driver, "04_settings_applied")
        
        # Check the preview content
        preview_content = driver.find_element(By.ID, "draftPreviewContent")
        
        # Count empty paragraphs
        paragraphs = preview_content.find_elements(By.TAG_NAME, "p")
        print(f"📊 Found {len(paragraphs)} paragraphs in preview")
        
        # Check for consecutive empty paragraphs
        empty_count = 0
        max_consecutive_empty = 0
        current_consecutive = 0
        
        for p in paragraphs:
            # Check if paragraph is empty (no visible text)
            text = p.text.strip()
            inner_text = p.get_attribute("innerText") or ""
            inner_text_clean = inner_text.strip()
            
            # Check if paragraph is visible
            is_visible = p.is_displayed()
            
            if is_visible and (not text and not inner_text_clean):
                empty_count += 1
                current_consecutive += 1
                max_consecutive_empty = max(max_consecutive_empty, current_consecutive)
            else:
                current_consecutive = 0
        
        print(f"📊 Empty paragraphs: {empty_count}")
        print(f"📊 Max consecutive empty: {max_consecutive_empty}")
        
        # Take final screenshot
        take_screenshot(driver, "05_final_state")
        
        # Verify: should have at most 1 consecutive empty paragraph
        if max_consecutive_empty > 1:
            print(f"❌ FAIL: Found {max_consecutive_empty} consecutive empty paragraphs (should be ≤ 1)")
            return False
        else:
            print("✅ PASS: No more than 1 consecutive empty paragraph found")
            return True
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        take_screenshot(driver, "error_state")
        return False
    finally:
        print("🔚 Closing browser...")
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    print("🧪 Starting trim empty paragraphs test...")
    success = test_trim_empty_paragraphs()
    if success:
        print("✅ Test passed!")
    else:
        print("❌ Test failed!")
        exit(1)




