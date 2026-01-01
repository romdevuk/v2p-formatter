"""
Test media browser to verify JPEG files are shown for lesnoi/fire learner
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import requests

def test_media_browser_jpeg_files():
    """Test that media browser shows JPEG files for lesnoi/fire learner"""
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("=" * 80)
        print("TEST: Media Browser JPEG Files for lesnoi/fire")
        print("=" * 80)
        
        qualification = "fire"
        learner = "lesnoi"
        
        # First, test the API directly
        print(f"\n1. Testing API endpoint directly...")
        api_url = f"http://localhost/v2p-formatter/media-converter/observation-media/media?qualification={qualification}&learner={learner}"
        print(f"   URL: {api_url}")
        
        try:
            response = requests.get(api_url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Success: {data.get('success')}")
                print(f"   Media count: {data.get('count', 0)}")
                
                if data.get('success'):
                    media_files = data.get('media', [])
                    print(f"\n   Media files found: {len(media_files)}")
                    
                    # Check file types
                    mp4_files = [f for f in media_files if f.get('name', '').lower().endswith('.mp4')]
                    jpeg_files = [f for f in media_files if f.get('name', '').lower().endswith(('.jpg', '.jpeg'))]
                    png_files = [f for f in media_files if f.get('name', '').lower().endswith('.png')]
                    
                    print(f"   MP4 files: {len(mp4_files)}")
                    print(f"   JPEG files: {len(jpeg_files)}")
                    print(f"   PNG files: {len(png_files)}")
                    
                    if jpeg_files:
                        print(f"\n   ✓ JPEG files found:")
                        for jpeg_file in jpeg_files[:5]:  # Show first 5
                            print(f"      - {jpeg_file.get('name')} ({jpeg_file.get('type', 'unknown')})")
                    else:
                        print(f"\n   ✗ No JPEG files found!")
                    
                    if mp4_files:
                        print(f"\n   MP4 files found:")
                        for mp4_file in mp4_files[:5]:  # Show first 5
                            print(f"      - {mp4_file.get('name')} ({mp4_file.get('type', 'unknown')})")
                    
                    # Show all file names for debugging
                    print(f"\n   All file names:")
                    for media_file in media_files[:10]:  # Show first 10
                        print(f"      - {media_file.get('name')} (type: {media_file.get('type', 'unknown')})")
                else:
                    print(f"   Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"   Response: {response.text[:200]}")
        except Exception as e:
            print(f"   ✗ Error calling API: {e}")
            import traceback
            traceback.print_exc()
        
        # Now test in browser
        print(f"\n2. Testing in browser...")
        url = f"http://localhost/v2p-formatter/observation-media?qualification={qualification}&learner={learner}"
        print(f"   URL: {url}")
        driver.get(url)
        time.sleep(3)
        
        # Set qualification dropdown if not already set
        print(f"\n2a. Setting qualification dropdown...")
        try:
            qualification_select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'qualificationSelect'))
            )
            current_qual = qualification_select.get_attribute('value')
            print(f"   Current qualification value: '{current_qual}'")
            
            # Get all available options
            from selenium.webdriver.support.ui import Select
            select = Select(qualification_select)
            options = [opt.text for opt in select.options]
            print(f"   Available qualifications: {options[:10]}")  # Show first 10
            
            # Try to find matching qualification (case-insensitive)
            matching_qual = None
            for opt in select.options:
                opt_value = opt.get_attribute('value')
                if opt.text.lower() == qualification.lower() or (opt_value and opt_value.lower() == qualification.lower()):
                    matching_qual = opt.text
                    break
            
            if matching_qual:
                print(f"   Found matching qualification: {matching_qual}")
                select.select_by_visible_text(matching_qual)
                time.sleep(2)
            elif current_qual != qualification:
                print(f"   Warning: Could not find exact match for '{qualification}', trying case variations...")
                # Try capitalized version
                try:
                    select.select_by_visible_text(qualification.capitalize())
                    time.sleep(2)
                except:
                    print(f"   Could not set qualification dropdown")
            
            # Wait for learner dropdown to populate
            learner_select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'learnerSelect'))
            )
            time.sleep(1)
            
            # Set learner dropdown
            current_learner = learner_select.get_attribute('value')
            print(f"   Current learner value: '{current_learner}'")
            if current_learner != learner:
                print(f"   Setting learner to: {learner}")
                select_learner = Select(learner_select)
                # Get learner options
                learner_options = [opt.text for opt in select_learner.options]
                print(f"   Available learners: {learner_options[:10]}")
                
                # Try to find matching learner (case-insensitive)
                matching_learner = None
                for opt in select_learner.options:
                    opt_value = opt.get_attribute('value')
                    if opt.text.lower() == learner.lower() or (opt_value and opt_value.lower() == learner.lower()):
                        matching_learner = opt.text
                        break
                
                if matching_learner:
                    select_learner.select_by_visible_text(matching_learner)
                    time.sleep(2)
                else:
                    print(f"   Warning: Could not find exact match for learner '{learner}'")
        except Exception as e:
            print(f"   Error setting dropdowns: {e}")
            import traceback
            traceback.print_exc()
        
        # Wait for media grid
        print(f"\n3. Waiting for media grid...")
        try:
            media_grid = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, 'observationMediaGrid'))
            )
            print(f"   ✓ Media grid found")
        except TimeoutException:
            print(f"   ✗ Media grid not found!")
            driver.save_screenshot('test_media_browser_jpeg_no_grid.png')
            return False
        
        # Wait for loading to complete
        print(f"\n4. Waiting for media to load...")
        max_wait = 45
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            grid_text = media_grid.text
            # Check if loading is done (no "Loading" text and has content)
            if 'Loading' not in grid_text and grid_text.strip() and 'Please select' not in grid_text:
                # Check if we have media cards
                media_cards = driver.find_elements(By.CLASS_NAME, 'observation-media-card')
                if len(media_cards) > 0:
                    print(f"   ✓ Media loaded! Found {len(media_cards)} cards")
                    break
            time.sleep(2)
        
        # Check for media cards
        print(f"\n5. Checking for media cards...")
        media_cards = driver.find_elements(By.CLASS_NAME, 'observation-media-card')
        print(f"   Media cards found: {len(media_cards)}")
        
        # Check for JPEG files in the grid
        jpeg_cards = []
        mp4_cards = []
        
        for card in media_cards:
            try:
                # Try to find the file name in the card
                card_text = card.text.lower()
                if '.jpg' in card_text or '.jpeg' in card_text:
                    jpeg_cards.append(card)
                elif '.mp4' in card_text:
                    mp4_cards.append(card)
            except:
                continue
        
        print(f"   JPEG cards found: {len(jpeg_cards)}")
        print(f"   MP4 cards found: {len(mp4_cards)}")
        
        # Take screenshot
        driver.save_screenshot('test_media_browser_jpeg_result.png')
        print(f"\n   ✓ Screenshot saved: test_media_browser_jpeg_result.png")
        
        # Check JavaScript data and console errors
        print(f"\n6. Checking JavaScript data and errors...")
        try:
            # Check console logs for errors
            logs = driver.get_log('browser')
            error_logs = [log for log in logs if log['level'] == 'SEVERE']
            if error_logs:
                print(f"   Found {len(error_logs)} JavaScript errors:")
                for log in error_logs[-5:]:
                    print(f"      ERROR: {log['message']}")
            
            # Check if functions exist
            has_load = driver.execute_script("return typeof loadObservationMedia === 'function';")
            has_display = driver.execute_script("return typeof displayObservationMedia === 'function';")
            print(f"   loadObservationMedia exists: {has_load}")
            print(f"   displayObservationMedia exists: {has_display}")
            
            # Check dropdown values
            qualification_val = driver.execute_script("return document.getElementById('qualificationSelect')?.value || '';")
            learner_val = driver.execute_script("return document.getElementById('learnerSelect')?.value || '';")
            print(f"   Qualification value: {qualification_val}")
            print(f"   Learner value: {learner_val}")
            
            # Try to manually call loadObservationMedia
            if has_load:
                print(f"   Attempting to manually call loadObservationMedia...")
                driver.execute_script("if (typeof loadObservationMedia === 'function') loadObservationMedia();")
                time.sleep(5)
                
                # Check again for media cards
                media_cards_after = driver.find_elements(By.CLASS_NAME, 'observation-media-card')
                print(f"   Media cards after manual call: {len(media_cards_after)}")
                
                if len(media_cards_after) > 0:
                    jpeg_cards_after = [c for c in media_cards_after if '.jpg' in c.text.lower() or '.jpeg' in c.text.lower()]
                    print(f"   JPEG cards after manual call: {len(jpeg_cards_after)}")
            
            media_data = driver.execute_script("""
                return window.observationMediaData || null;
            """)
            
            if media_data:
                print(f"   Media data found: {len(media_data.get('media', []))} files")
            else:
                print(f"   No media data in window")
        except Exception as e:
            print(f"   Error checking JS data: {e}")
            import traceback
            traceback.print_exc()
        
        # Final check
        print(f"\n7. Final verification...")
        if len(jpeg_cards) > 0 or len(jpeg_files) > 0:
            print(f"   ✓ SUCCESS: JPEG files are being displayed!")
            return True
        else:
            print(f"   ✗ FAILED: No JPEG files found in media browser")
            return False
        
    except Exception as e:
        print(f"\n✗ TEST FAILED WITH EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot('test_media_browser_jpeg_ERROR.png')
        return False
    finally:
        driver.quit()

if __name__ == '__main__':
    success = test_media_browser_jpeg_files()
    exit(0 if success else 1)

