"""
Selenium tests for PDF configuration options
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class TestPDFConfiguration:
    """Test PDF layout and configuration options"""
    
    def test_layout_select_exists(self, driver, base_url, wait):
        """Test that layout dropdown exists"""
        driver.get(base_url)
        
        layout_select = wait.until(
            EC.presence_of_element_located((By.ID, "layoutSelect"))
        )
        assert layout_select is not None
        
        # Check options
        select = Select(layout_select)
        options = [opt.text for opt in select.options]
        assert "Grid" in options
        assert "Custom" in options
    
    def test_images_per_page_select_exists(self, driver, base_url, wait):
        """Test that images per page dropdown exists"""
        driver.get(base_url)
        
        images_per_page = wait.until(
            EC.presence_of_element_located((By.ID, "imagesPerPage"))
        )
        assert images_per_page is not None
        
        # Check options
        select = Select(images_per_page)
        options = [opt.get_attribute("value") for opt in select.options]
        assert "1" in options
        assert "4" in options
        assert "9" in options
    
    def test_layout_configuration_changeable(self, driver, base_url, wait):
        """Test that layout configuration can be changed"""
        driver.get(base_url)
        
        layout_select = wait.until(
            EC.presence_of_element_located((By.ID, "layoutSelect"))
        )
        images_per_page = driver.find_element(By.ID, "imagesPerPage")
        
        # Change layout
        select_layout = Select(layout_select)
        select_layout.select_by_value("custom")
        assert select_layout.first_selected_option.get_attribute("value") == "custom"
        
        # Change images per page
        select_images = Select(images_per_page)
        select_images.select_by_value("6")
        assert select_images.first_selected_option.get_attribute("value") == "6"

