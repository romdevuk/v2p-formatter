"""
Selenium tests for image configuration options
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class TestImageConfiguration:
    """Test image quality and resolution configuration"""
    
    def test_quality_slider_exists(self, driver, base_url, wait):
        """Test that quality slider exists and has correct range"""
        driver.get(base_url)
        
        quality_slider = wait.until(
            EC.presence_of_element_located((By.ID, "qualitySlider"))
        )
        assert quality_slider is not None
        assert quality_slider.get_attribute("min") == "1"
        assert quality_slider.get_attribute("max") == "100"
    
    def test_quality_value_display(self, driver, base_url, wait):
        """Test that quality value is displayed"""
        driver.get(base_url)
        
        quality_value = driver.find_element(By.ID, "qualityValue")
        assert quality_value is not None
        assert quality_value.text.isdigit()
    
    def test_quality_slider_updates_value(self, driver, base_url, wait):
        """Test that moving slider updates displayed value"""
        driver.get(base_url)
        
        quality_slider = wait.until(
            EC.presence_of_element_located((By.ID, "qualitySlider"))
        )
        quality_value = driver.find_element(By.ID, "qualityValue")
        
        # Get initial value
        initial_value = quality_value.text
        
        # Move slider
        quality_slider.clear()
        quality_slider.send_keys("50")
        
        # Check value updated (may need to wait for JS to update)
        wait.until(lambda d: quality_value.text != initial_value)
    
    def test_resolution_select_exists(self, driver, base_url, wait):
        """Test that resolution dropdown exists"""
        driver.get(base_url)
        
        resolution_select = wait.until(
            EC.presence_of_element_located((By.ID, "resolutionSelect"))
        )
        assert resolution_select is not None
        
        # Check options
        select = Select(resolution_select)
        options = [opt.text for opt in select.options]
        assert "Original" in options
        assert "1920x1080" in options
    
    def test_resolution_select_changeable(self, driver, base_url, wait):
        """Test that resolution can be changed"""
        driver.get(base_url)
        
        resolution_select = wait.until(
            EC.presence_of_element_located((By.ID, "resolutionSelect"))
        )
        select = Select(resolution_select)
        
        # Change selection
        select.select_by_value("1280x720")
        assert select.first_selected_option.get_attribute("value") == "1280x720"

