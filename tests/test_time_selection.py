"""
Selenium tests for time point selection functionality
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class TestTimeSelection:
    """Test time point selection interface"""
    
    def test_time_input_exists(self, driver, base_url, wait):
        """Test that time input field exists"""
        driver.get(base_url)
        
        time_input = wait.until(
            EC.presence_of_element_located((By.ID, "timeInput"))
        )
        assert time_input is not None
        assert time_input.get_attribute("placeholder") is not None
    
    def test_time_input_examples_displayed(self, driver, base_url, wait):
        """Test that time input examples are shown"""
        driver.get(base_url)
        
        # Check for examples section
        examples = driver.find_elements(By.CSS_SELECTOR, ".input-examples")
        assert len(examples) > 0
        
        # Check for example codes
        example_codes = driver.find_elements(By.CSS_SELECTOR, ".input-examples code")
        assert len(example_codes) > 0
    
    def test_preview_frames_button_exists(self, driver, base_url, wait):
        """Test that preview frames button exists"""
        driver.get(base_url)
        
        preview_btn = wait.until(
            EC.presence_of_element_located((By.ID, "previewFramesBtn"))
        )
        assert preview_btn is not None
        assert "Preview Frames" in preview_btn.text
    
    def test_time_input_accepts_values(self, driver, base_url, wait):
        """Test that time input accepts and stores values"""
        driver.get(base_url)
        
        time_input = wait.until(
            EC.presence_of_element_located((By.ID, "timeInput"))
        )
        
        # Enter test values
        test_value = "10, 25, 45, 60"
        time_input.clear()
        time_input.send_keys(test_value)
        
        # Verify value is stored
        assert time_input.get_attribute("value") == test_value
    
    def test_frame_preview_area_exists(self, driver, base_url, wait):
        """Test that frame preview area exists"""
        driver.get(base_url)
        
        preview_area = driver.find_element(By.ID, "framePreview")
        assert preview_area is not None

