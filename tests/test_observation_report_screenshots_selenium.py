"""
Observation Report - Screenshot tests using Selenium (existing test framework)
Uses the same fixtures as other tests in this project
"""
import pytest
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="session")
def screenshot_dir():
    """Create screenshots directory"""
    screenshots = Path("test_screenshots/observation_report_workflows")
    screenshots.mkdir(parents=True, exist_ok=True)
    return screenshots


class TestObservationReportScreenshots:
    """Generate screenshots for Observation Report UI"""
    
    def test_01_initial_load(self, driver, base_url, screenshot_dir):
        """1. Initial page load"""
        driver.get(f"{base_url}/observation-report")
        time.sleep(3)  # Wait for page to load
        driver.save_screenshot(str(screenshot_dir / "01_initial_load.png"))
        print(f"✅ Screenshot: 01_initial_load.png")
    
    def test_02_qualification_dropdown(self, driver, base_url, screenshot_dir):
        """2. Qualification dropdown"""
        driver.get(f"{base_url}/observation-report")
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        
        qual_select = wait.until(EC.presence_of_element_located((By.ID, "qualificationSelect")))
        driver.save_screenshot(str(screenshot_dir / "02_qualification_dropdown.png"))
        print(f"✅ Screenshot: 02_qualification_dropdown.png")
    
    def test_03_select_qualification(self, driver, base_url, screenshot_dir):
        """3. After selecting qualification"""
        driver.get(f"{base_url}/observation-report")
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        
        qual_select = wait.until(EC.presence_of_element_located((By.ID, "qualificationSelect")))
        select = Select(qual_select)
        
        # Check if there are options
        if len(select.options) > 1:
            select.select_by_index(1)
            time.sleep(2)
            driver.save_screenshot(str(screenshot_dir / "03_qualification_selected.png"))
            print(f"✅ Screenshot: 03_qualification_selected.png")
    
    def test_04_select_learner(self, driver, base_url, screenshot_dir):
        """4. After selecting learner and media loads"""
        driver.get(f"{base_url}/observation-report")
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        
        # Select qualification
        qual_select = wait.until(EC.presence_of_element_located((By.ID, "qualificationSelect")))
        select_qual = Select(qual_select)
        if len(select_qual.options) > 1:
            select_qual.select_by_index(1)
            time.sleep(2)
            
            # Select learner
            learner_select = wait.until(EC.presence_of_element_located((By.ID, "learnerSelect")))
            select_learner = Select(learner_select)
            if len(select_learner.options) > 1:
                select_learner.select_by_index(1)
                time.sleep(3)  # Wait for media to load
                driver.save_screenshot(str(screenshot_dir / "04_learner_selected_media_loaded.png"))
                print(f"✅ Screenshot: 04_learner_selected_media_loaded.png")
    
    def test_05_media_browser(self, driver, base_url, screenshot_dir):
        """5. Media browser loaded"""
        driver.get(f"{base_url}/observation-report")
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        
        # Setup qualification and learner
        qual_select = wait.until(EC.presence_of_element_located((By.ID, "qualificationSelect")))
        select_qual = Select(qual_select)
        if len(select_qual.options) > 1:
            select_qual.select_by_index(1)
            time.sleep(1)
            
            learner_select = wait.until(EC.presence_of_element_located((By.ID, "learnerSelect")))
            select_learner = Select(learner_select)
            if len(select_learner.options) > 1:
                select_learner.select_by_index(1)
                time.sleep(3)
                
                # Take screenshot of media browser
                media_browser = driver.find_element(By.ID, "mediaBrowser")
                driver.save_screenshot(str(screenshot_dir / "05_media_browser.png"))
                print(f"✅ Screenshot: 05_media_browser.png")
    
    def test_06_text_with_placeholders(self, driver, base_url, screenshot_dir):
        """6. Text editor with placeholders"""
        driver.get(f"{base_url}/observation-report")
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        
        # Expand text editor section
        try:
            text_section = driver.find_element(By.CSS_SELECTOR, '[data-section="textEditor"]')
            section_header = text_section.find_element(By.CLASS_NAME, "section-header")
            section_header.click()
            time.sleep(0.5)
        except:
            pass  # Section might already be expanded
        
        # Enter text with placeholders
        text_editor = wait.until(EC.presence_of_element_located((By.ID, "textEditor")))
        text_editor.clear()
        text_editor.send_keys("SECTION 1: Site Arrival\n\n{{Site_Arrival_Induction}}\n\nThe site arrival process was conducted properly.\n\n{{Safety_Briefing}}\n\nSafety procedures were explained clearly.")
        time.sleep(1)
        
        driver.save_screenshot(str(screenshot_dir / "06_text_with_placeholders.png"))
        print(f"✅ Screenshot: 06_text_with_placeholders.png")
    
    def test_07_live_preview_placeholders(self, driver, base_url, screenshot_dir):
        """7. Live preview showing placeholders"""
        driver.get(f"{base_url}/observation-report")
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        
        # Setup text with placeholders
        text_editor = wait.until(EC.presence_of_element_located((By.ID, "textEditor")))
        text_editor.clear()
        text_editor.send_keys("{{Placeholder1}} content {{Placeholder2}}")
        time.sleep(1)
        
        driver.save_screenshot(str(screenshot_dir / "07_live_preview_placeholders.png"))
        print(f"✅ Screenshot: 07_live_preview_placeholders.png")
    
    def test_08_before_drag(self, driver, base_url, screenshot_dir):
        """8. Before drag operation"""
        driver.get(f"{base_url}/observation-report")
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        
        # Setup qualification/learner
        qual_select = wait.until(EC.presence_of_element_located((By.ID, "qualificationSelect")))
        select_qual = Select(qual_select)
        if len(select_qual.options) > 1:
            select_qual.select_by_index(1)
            time.sleep(1)
            
            learner_select = wait.until(EC.presence_of_element_located((By.ID, "learnerSelect")))
            select_learner = Select(learner_select)
            if len(select_learner.options) > 1:
                select_learner.select_by_index(1)
                time.sleep(2)
        
        # Setup text with placeholder
        text_editor = wait.until(EC.presence_of_element_located((By.ID, "textEditor")))
        text_editor.clear()
        text_editor.send_keys("{{TestPlaceholder}}")
        time.sleep(1)
        
        driver.save_screenshot(str(screenshot_dir / "08_before_drag.png"))
        print(f"✅ Screenshot: 08_before_drag.png")
    
    def test_09_after_drag(self, driver, base_url, screenshot_dir):
        """9. After drag and drop"""
        driver.get(f"{base_url}/observation-report")
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        
        # Setup qualification/learner
        qual_select = wait.until(EC.presence_of_element_located((By.ID, "qualificationSelect")))
        select_qual = Select(qual_select)
        if len(select_qual.options) > 1:
            select_qual.select_by_index(1)
            time.sleep(1)
            
            learner_select = wait.until(EC.presence_of_element_located((By.ID, "learnerSelect")))
            select_learner = Select(learner_select)
            if len(select_learner.options) > 1:
                select_learner.select_by_index(1)
                time.sleep(2)
        
        # Setup text with placeholder
        text_editor = wait.until(EC.presence_of_element_located((By.ID, "textEditor")))
        text_editor.clear()
        text_editor.send_keys("{{TestPlaceholder}}")
        time.sleep(1)
        
        # Try to find and perform drag and drop
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            
            media_cards = driver.find_elements(By.CSS_SELECTOR, ".media-card:not(.assigned)")
            drop_zones = driver.find_elements(By.CSS_SELECTOR, ".drop-zone")
            
            if media_cards and drop_zones:
                actions = ActionChains(driver)
                actions.drag_and_drop(media_cards[0], drop_zones[0]).perform()
                time.sleep(2)
        except Exception as e:
            print(f"Note: Drag and drop simulation failed: {e}")
        
        driver.save_screenshot(str(screenshot_dir / "09_after_drag.png"))
        print(f"✅ Screenshot: 09_after_drag.png")
    
    def test_10_draft_dialog(self, driver, base_url, screenshot_dir):
        """10. Draft load dialog"""
        driver.get(f"{base_url}/observation-report")
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        
        # Click load draft button
        try:
            load_btn = wait.until(EC.element_to_be_clickable((By.ID, "loadDraftBtn")))
            load_btn.click()
            time.sleep(1)
            
            driver.save_screenshot(str(screenshot_dir / "10_draft_dialog.png"))
            print(f"✅ Screenshot: 10_draft_dialog.png")
        except Exception as e:
            print(f"Note: Draft dialog not accessible: {e}")



