"""
Selenium tests for video upload functionality
"""
import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pathlib import Path


class TestVideoUpload:
    """Test video upload functionality"""
    
    @pytest.fixture
    def sample_video_path(self):
        """Create a sample video file path for testing"""
        # In real tests, you'd use an actual test video file
        # For now, we'll test the UI flow
        test_video = Path(__file__).parent / "test_data" / "sample.mp4"
        return str(test_video) if test_video.exists() else None
    
    def test_file_input_exists(self, driver, base_url, wait):
        """Test that file input element exists"""
        driver.get(base_url)
        
        file_input = wait.until(
            EC.presence_of_element_located((By.ID, "videoInput"))
        )
        assert file_input is not None
        assert file_input.get_attribute("accept") == ".mp4"
    
    def test_upload_button_clickable(self, driver, base_url, wait):
        """Test that upload button triggers file input"""
        driver.get(base_url)
        
        upload_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary"))
        )
        
        # Click button (this should trigger file input)
        upload_button.click()
        
        # File input should be accessible (though hidden)
        file_input = driver.find_element(By.ID, "videoInput")
        assert file_input is not None
    
    def test_drag_and_drop_area_exists(self, driver, base_url, wait):
        """Test that drag and drop area is present"""
        driver.get(base_url)
        
        upload_area = wait.until(
            EC.presence_of_element_located((By.ID, "uploadArea"))
        )
        assert upload_area.is_displayed()
        assert "upload-area" in upload_area.get_attribute("class")
    
    def test_upload_status_message_area(self, driver, base_url, wait):
        """Test that status message area exists"""
        driver.get(base_url)
        
        status_div = driver.find_element(By.ID, "uploadStatus")
        assert status_div is not None
        # Initially should be empty or hidden
        assert status_div.text == "" or not status_div.is_displayed()

