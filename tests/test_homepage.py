"""
Selenium tests for the homepage and basic UI elements
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class TestHomepage:
    """Test homepage loading and basic elements"""
    
    def test_homepage_loads(self, driver, base_url, wait):
        """Test that homepage loads successfully"""
        driver.get(base_url)
        
        # Check page title
        assert "Video to Image Formatter" in driver.title
        
        # Check main heading
        heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        assert "Video to Image Formatter" in heading.text
    
    def test_upload_section_displayed(self, driver, base_url, wait):
        """Test that upload section is visible"""
        driver.get(base_url)
        
        # Check upload section exists
        upload_section = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".upload-section"))
        )
        assert upload_section.is_displayed()
        
        # Check upload button exists
        upload_button = driver.find_element(By.CSS_SELECTOR, ".btn-primary")
        assert upload_button.is_displayed()
        assert "Choose File" in upload_button.text
    
    def test_all_sections_present(self, driver, base_url, wait):
        """Test that all main sections are present on the page"""
        driver.get(base_url)
        
        sections = [
            "upload-section",
            "preview-section",
            "time-section",
            "config-section",
            "pdf-section",
            "processing-section"
        ]
        
        for section_id in sections:
            section = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"#{section_id}, .{section_id}"))
            )
            assert section is not None

