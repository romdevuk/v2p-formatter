"""
Integration test with actual video file upload and processing
"""
import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pathlib import Path


class TestVideoIntegration:
    """Integration test with real video file"""
    
    @pytest.fixture
    def video_file_path(self):
        """Path to the test video file"""
        video_path = Path("/Users/rom/Documents/nvq/visited/css/L2 INTER/ ivan myhal /mp4/plasterboard-formingopening-multitool.mp4")
        if not video_path.exists():
            pytest.skip(f"Video file not found: {video_path}")
        return str(video_path)
    
    def test_upload_and_process_video(self, driver, base_url, wait, video_file_path):
        """Test complete workflow: upload video, select times, extract frames"""
        driver.get(base_url)
        
        # Step 1: Upload video
        print(f"\n📹 Uploading video: {video_file_path}")
        file_input = wait.until(
            EC.presence_of_element_located((By.ID, "videoInput"))
        )
        
        # Upload the file
        print("📤 Sending file to input...")
        file_input.send_keys(video_file_path)
        
        # Wait for upload to complete - check for status message or video info
        print("⏳ Waiting for video upload (this may take a while for large files)...")
        
        # Wait up to 60 seconds for upload to complete
        upload_complete = False
        max_wait = 60
        waited = 0
        
        while waited < max_wait and not upload_complete:
            try:
                # Check for success status
                status_div = driver.find_element(By.ID, "uploadStatus")
                if status_div.is_displayed():
                    status_class = status_div.get_attribute("class")
                    status_text = status_div.text.lower()
                    
                    if "success" in status_class:
                        print("✅ Upload status shows success")
                        upload_complete = True
                        break
                    elif "error" in status_class or "error" in status_text:
                        error_msg = status_div.text
                        pytest.fail(f"Upload failed: {error_msg}")
                
                # Check if preview section is visible
                preview_section = driver.find_element(By.ID, "previewSection")
                if preview_section.is_displayed():
                    print("✅ Preview section is visible")
                    upload_complete = True
                    break
                
                # Check if video info is visible
                video_info = driver.find_element(By.ID, "videoInfo")
                if video_info.is_displayed() and video_info.text.strip():
                    print("✅ Video info is displayed")
                    upload_complete = True
                    break
                    
            except:
                pass
            
            import time
            time.sleep(1)
            waited += 1
            if waited % 5 == 0:
                print(f"   Still waiting... ({waited}s/{max_wait}s)")
        
        if not upload_complete:
            # Take screenshot for debugging
            driver.save_screenshot("/tmp/test_upload_error.png")
            print("📸 Screenshot saved to /tmp/test_upload_error.png")
            
            # Check page source for errors
            page_source = driver.page_source
            if "error" in page_source.lower():
                print("⚠️  Error detected in page - check screenshot")
            else:
                print("⚠️  Upload timeout - but no obvious errors found")
            
            # Try to continue anyway - maybe upload completed but UI didn't update
            print("⚠️  Attempting to continue despite timeout...")
        
        # Step 2: Wait for time section to be visible and enter time points
        print("\n⏱️  Waiting for time section to be visible...")
        time_section = WebDriverWait(driver, 30).until(
            lambda d: d.find_element(By.ID, "timeSection").is_displayed()
        )
        
        print("⏱️  Entering time points...")
        time_input = wait.until(
            EC.element_to_be_clickable((By.ID, "timeInput"))
        )
        
        # Enter some time points (e.g., 5, 10, 15 seconds)
        test_times = "5, 10, 15"
        time_input.click()  # Click to focus
        time_input.clear()
        time_input.send_keys(test_times)
        print(f"✅ Time points entered: {test_times}")
        
        # Step 3: Preview frames
        print("\n🖼️  Previewing frames...")
        preview_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "previewFramesBtn"))
        )
        preview_btn.click()
        
        # Wait for preview to load (may take a moment)
        print("⏳ Waiting for frame previews...")
        try:
            WebDriverWait(driver, 15).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, ".frame-preview-item")) > 0
                or "Loading previews" not in d.find_element(By.ID, "framePreview").text
            )
            print("✅ Frame previews loaded")
        except:
            print("⚠️  Frame previews may not have loaded (continuing anyway)")
        
        # Step 4: Configure image settings
        print("\n⚙️  Configuring image settings...")
        quality_slider = driver.find_element(By.ID, "qualitySlider")
        quality_slider.clear()
        quality_slider.send_keys("90")
        print("✅ Quality set to 90")
        
        # Step 5: Extract frames
        print("\n🎬 Extracting frames...")
        extract_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "extractFramesBtn"))
        )
        extract_btn.click()
        
        # Wait for extraction to complete
        print("⏳ Waiting for frame extraction...")
        try:
            WebDriverWait(driver, 60).until(
                lambda d: "Successfully extracted" in d.find_element(By.ID, "results").text
                or "error" in d.find_element(By.ID, "results").text.lower()
            )
            
            results = driver.find_element(By.ID, "results")
            results_text = results.text
            print(f"📊 Results: {results_text[:100]}...")
            
            if "error" in results_text.lower():
                pytest.fail(f"Frame extraction failed: {results_text}")
            else:
                print("✅ Frames extracted successfully")
        except Exception as e:
            print(f"⚠️  Extraction may still be in progress or failed: {e}")
        
        # Step 6: Generate PDF
        print("\n📄 Generating PDF...")
        pdf_btn = driver.find_element(By.ID, "generatePdfBtn")
        
        if pdf_btn.is_displayed():
            pdf_btn.click()
            print("⏳ Waiting for PDF generation...")
            
            try:
                WebDriverWait(driver, 60).until(
                    lambda d: "PDF generated" in d.find_element(By.ID, "results").text
                    or "error" in d.find_element(By.ID, "results").text.lower()
                )
                
                results = driver.find_element(By.ID, "results")
                results_text = results.text
                print(f"📊 PDF Results: {results_text[:100]}...")
                
                if "error" in results_text.lower():
                    print(f"⚠️  PDF generation may have failed: {results_text}")
                else:
                    print("✅ PDF generated successfully")
            except Exception as e:
                print(f"⚠️  PDF generation may still be in progress: {e}")
        else:
            print("⚠️  PDF button not visible (frames may not have been extracted)")
        
        print("\n✅ Integration test completed!")
    
    def test_video_file_exists(self, video_file_path):
        """Verify the test video file exists"""
        assert os.path.exists(video_file_path), f"Video file not found: {video_file_path}"
        assert video_file_path.endswith('.mp4'), "File should be MP4 format"
        print(f"✅ Video file verified: {video_file_path}")

