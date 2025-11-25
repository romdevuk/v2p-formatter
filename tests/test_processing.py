"""
Selenium tests for frame extraction and PDF generation
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestProcessing:
    """Test frame extraction and PDF generation buttons"""
    
    def test_extract_frames_button_exists(self, driver, base_url, wait):
        """Test that extract frames button exists"""
        driver.get(base_url)
        
        extract_btn = wait.until(
            EC.presence_of_element_located((By.ID, "extractFramesBtn"))
        )
        assert extract_btn is not None
        assert "Extract Frames" in extract_btn.text
    
    def test_generate_pdf_button_exists(self, driver, base_url, wait):
        """Test that generate PDF button exists (initially hidden)"""
        driver.get(base_url)
        
        pdf_btn = driver.find_element(By.ID, "generatePdfBtn")
        assert pdf_btn is not None
        # Initially should be hidden
        assert not pdf_btn.is_displayed() or pdf_btn.get_attribute("style") == "display: none;"
    
    def test_progress_container_exists(self, driver, base_url, wait):
        """Test that progress container exists"""
        driver.get(base_url)
        
        progress_container = driver.find_element(By.ID, "progressContainer")
        assert progress_container is not None
        # Initially should be hidden
        assert not progress_container.is_displayed()
    
    def test_results_area_exists(self, driver, base_url, wait):
        """Test that results area exists"""
        driver.get(base_url)
        
        results = driver.find_element(By.ID, "results")
        assert results is not None

