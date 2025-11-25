"""
Complete workflow tests for v2p-formatter
Tests file selection, frame extraction, and PDF generation
"""
import pytest
import time
import os
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestCompleteWorkflow:
    """Test complete workflow scenarios"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url, flask_server):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 30)
        
    def test_scenario_1_single_frame_extraction(self):
        """Scenario 1: Select video, extract single frame, generate PDF"""
        print("\n=== Scenario 1: Single Frame Extraction ===")
        
        # Navigate to app
        self.driver.get(f"{self.base_url}/v2p-formatter/")
        print("✅ Page loaded")
        
        # Wait for Load Files button and click it
        load_btn = self.wait.until(EC.presence_of_element_located((By.ID, "loadFilesBtn")))
        print("✅ Load Files button found")
        load_btn.click()
        print("✅ Clicked Load MP4 Files")
        
        # Wait for file tree to load (scanning 756 files takes time)
        print("⏳ Waiting for file tree to load (scanning files...)")
        time.sleep(5)  # Give time for file scan
        
        # Wait for file tree container to be visible
        file_tree = self.wait.until(EC.presence_of_element_located((By.ID, "fileTree")))
        self.wait.until(lambda d: file_tree.is_displayed())
        print("✅ File tree container visible")
        
        # Wait for file items (they might be in collapsed folders)
        # First check if there are any folder headers to expand
        try:
            folder_headers = self.driver.find_elements(By.CLASS_NAME, "file-tree-folder-header")
            if folder_headers:
                print(f"✅ Found {len(folder_headers)} folders, expanding first one...")
                folder_headers[0].click()
                time.sleep(1)
        except:
            pass
        
        # Now wait for file items
        file_items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "file-tree-item")))
        print(f"✅ File tree loaded with {len(file_items)} files visible")
        
        # Find and click first MP4 file
        file_items = self.driver.find_elements(By.CLASS_NAME, "file-tree-item")
        assert len(file_items) > 0, "No files found in tree"
        first_file = file_items[0]
        file_name = first_file.find_element(By.CLASS_NAME, "file-name").text
        print(f"✅ Found file: {file_name}")
        
        first_file.click()
        print("✅ Clicked file")
        
        # Wait for video to load
        self.wait.until(EC.presence_of_element_located((By.ID, "videoPlayer")))
        time.sleep(2)
        print("✅ Video loaded")
        
        # Enter time point (single frame)
        time_input = self.wait.until(EC.element_to_be_clickable((By.ID, "timeInput")))
        time_input.clear()
        time_input.send_keys("5")
        print("✅ Entered time point: 5 seconds")
        
        # Click Extract Frames
        extract_btn = self.driver.find_element(By.ID, "extractFramesBtn")
        extract_btn.click()
        print("✅ Clicked Extract Frames")
        
        # Wait for extraction to complete
        self.wait.until(lambda d: "success" in d.find_element(By.ID, "results").text.lower() or 
                       "extracted" in d.find_element(By.ID, "results").text.lower(), 
                       timeout=60)
        print("✅ Frames extracted")
        
        # Verify images were created (check results message)
        results_text = self.driver.find_element(By.ID, "results").text
        assert "success" in results_text.lower() or "extracted" in results_text.lower(), \
            f"Extraction failed: {results_text}"
        
        # Click Generate PDF
        generate_pdf_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "generatePdfBtn")))
        generate_pdf_btn.click()
        print("✅ Clicked Generate PDF")
        
        # Wait for PDF generation
        self.wait.until(lambda d: "pdf" in d.find_element(By.ID, "results").text.lower() or
                       "download" in d.find_element(By.ID, "results").text.lower(),
                       timeout=60)
        print("✅ PDF generated")
        
        # Verify PDF was created
        results_text = self.driver.find_element(By.ID, "results").text
        assert "pdf" in results_text.lower() or "download" in results_text.lower(), \
            f"PDF generation failed: {results_text}"
        
        print("✅✅✅ Scenario 1 PASSED: Single frame extracted and PDF generated")
        
    def test_scenario_2_multiple_frames_extraction(self):
        """Scenario 2: Extract multiple frames at different time points"""
        print("\n=== Scenario 2: Multiple Frames Extraction ===")
        
        # Navigate to app
        self.driver.get(f"{self.base_url}/v2p-formatter/")
        time.sleep(2)
        
        # Load files
        load_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "loadFilesBtn")))
        load_btn.click()
        time.sleep(3)
        
        # Select first file
        file_items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "file-tree-item")))
        file_items[0].click()
        print("✅ File selected")
        
        # Wait for video to load
        self.wait.until(EC.presence_of_element_located((By.ID, "videoPlayer")))
        time.sleep(2)
        
        # Enter multiple time points
        time_input = self.wait.until(EC.element_to_be_clickable((By.ID, "timeInput")))
        time_input.clear()
        time_input.send_keys("5, 10, 15, 20")
        print("✅ Entered time points: 5, 10, 15, 20")
        
        # Extract frames
        extract_btn = self.driver.find_element(By.ID, "extractFramesBtn")
        extract_btn.click()
        print("✅ Clicked Extract Frames")
        
        # Wait for extraction
        self.wait.until(lambda d: "success" in d.find_element(By.ID, "results").text.lower() or 
                       "extracted" in d.find_element(By.ID, "results").text.lower(),
                       timeout=60)
        print("✅ Multiple frames extracted")
        
        # Generate PDF
        generate_pdf_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "generatePdfBtn")))
        generate_pdf_btn.click()
        print("✅ Clicked Generate PDF")
        
        # Wait for PDF
        self.wait.until(lambda d: "pdf" in d.find_element(By.ID, "results").text.lower() or
                       "download" in d.find_element(By.ID, "results").text.lower(),
                       timeout=60)
        print("✅ PDF generated with multiple frames")
        
        print("✅✅✅ Scenario 2 PASSED: Multiple frames extracted and PDF generated")
        
    def test_scenario_3_verify_files_created(self):
        """Scenario 3: Verify JPG files (1.jpg, 2.jpg, 3.jpg) and PDF are created"""
        print("\n=== Scenario 3: Verify Files Created ===")
        
        # Navigate to app
        self.driver.get(f"{self.base_url}/v2p-formatter/")
        time.sleep(2)
        
        # Load and select file
        load_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "loadFilesBtn")))
        load_btn.click()
        time.sleep(3)
        
        file_items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "file-tree-item")))
        file_items[0].click()
        
        # Get the file path from the file name
        file_name_element = file_items[0].find_element(By.CLASS_NAME, "file-name")
        video_filename = file_name_element.text
        print(f"✅ Selected video: {video_filename}")
        
        # Wait for video to load
        self.wait.until(EC.presence_of_element_located((By.ID, "videoPlayer")))
        time.sleep(2)
        
        # Extract 3 frames
        time_input = self.wait.until(EC.element_to_be_clickable((By.ID, "timeInput")))
        time_input.clear()
        time_input.send_keys("5, 10, 15")
        print("✅ Entered time points: 5, 10, 15")
        
        extract_btn = self.driver.find_element(By.ID, "extractFramesBtn")
        extract_btn.click()
        
        # Wait for extraction
        self.wait.until(lambda d: "success" in d.find_element(By.ID, "results").text.lower() or 
                       "extracted" in d.find_element(By.ID, "results").text.lower(),
                       timeout=60)
        print("✅ Frames extracted")
        
        # Get video path from results or extract from filename
        # We need to find the actual video path - it's in the visited directory
        visited_path = Path("/Users/rom/Documents/nvq/visited")
        video_file = None
        
        # Search for the video file
        for mp4_file in visited_path.rglob(video_filename):
            if mp4_file.is_file():
                video_file = mp4_file
                break
        
        assert video_file is not None, f"Could not find video file: {video_filename}"
        print(f"✅ Found video file: {video_file}")
        
        # Expected output directory
        output_dir = video_file.parent / f"{video_file.stem}_frames"
        pdf_path = video_file.parent / f"{video_file.stem}.pdf"
        
        print(f"✅ Expected output directory: {output_dir}")
        print(f"✅ Expected PDF path: {pdf_path}")
        
        # Generate PDF
        generate_pdf_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "generatePdfBtn")))
        generate_pdf_btn.click()
        
        # Wait for PDF generation
        self.wait.until(lambda d: "pdf" in d.find_element(By.ID, "results").text.lower() or
                       "download" in d.find_element(By.ID, "results").text.lower(),
                       timeout=60)
        print("✅ PDF generation completed")
        
        # Wait a bit for file system to sync
        time.sleep(2)
        
        # Verify JPG files exist
        jpg_files = []
        if output_dir.exists():
            jpg_files = sorted([f for f in output_dir.glob("*.jpg")])
            print(f"✅ Found {len(jpg_files)} JPG files in {output_dir}")
            for jpg in jpg_files:
                print(f"   - {jpg.name}")
        
        # Verify PDF exists
        pdf_exists = pdf_path.exists()
        print(f"✅ PDF exists: {pdf_exists} at {pdf_path}")
        
        # Assertions
        assert len(jpg_files) >= 3, f"Expected at least 3 JPG files, found {len(jpg_files)}"
        assert pdf_exists, f"PDF not found at {pdf_path}"
        
        # Verify specific files (1.jpg, 2.jpg, 3.jpg)
        expected_files = [output_dir / "1.jpg", output_dir / "2.jpg", output_dir / "3.jpg"]
        for expected_file in expected_files:
            assert expected_file.exists(), f"Expected file not found: {expected_file}"
            print(f"✅ Verified: {expected_file.name} exists")
        
        print("✅✅✅ Scenario 3 PASSED: All files verified")
        print(f"   - JPG files: {len(jpg_files)} files in {output_dir}")
        print(f"   - PDF file: {pdf_path}")
        
    def test_scenario_4_different_video_file(self):
        """Scenario 4: Test with a different video file"""
        print("\n=== Scenario 4: Different Video File ===")
        
        self.driver.get(f"{self.base_url}/")
        time.sleep(2)
        
        # Load files
        load_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "loadFilesBtn")))
        load_btn.click()
        time.sleep(3)
        
        # Select a different file (second file if available)
        file_items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "file-tree-item")))
        if len(file_items) > 1:
            file_items[1].click()
            print("✅ Selected second file")
        else:
            file_items[0].click()
            print("✅ Selected first file (only one available)")
        
        # Wait for video
        self.wait.until(EC.presence_of_element_located((By.ID, "videoPlayer")))
        time.sleep(2)
        
        # Extract frames
        time_input = self.wait.until(EC.element_to_be_clickable((By.ID, "timeInput")))
        time_input.clear()
        time_input.send_keys("2, 4, 6")
        
        extract_btn = self.driver.find_element(By.ID, "extractFramesBtn")
        extract_btn.click()
        
        self.wait.until(lambda d: "success" in d.find_element(By.ID, "results").text.lower() or 
                       "extracted" in d.find_element(By.ID, "results").text.lower(),
                       timeout=60)
        
        # Generate PDF
        generate_pdf_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "generatePdfBtn")))
        generate_pdf_btn.click()
        
        self.wait.until(lambda d: "pdf" in d.find_element(By.ID, "results").text.lower() or
                       "download" in d.find_element(By.ID, "results").text.lower(),
                       timeout=60)
        
        print("✅✅✅ Scenario 4 PASSED: Different video file processed successfully")
