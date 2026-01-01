"""
Browser test to debug media browser loading issue
Takes screenshots at various stages to identify the problem
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import json

def test_media_browser_loading():
    """Test media browser loading with screenshots"""
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("=" * 80)
        print("MEDIA BROWSER DEBUG TEST")
        print("=" * 80)
        
        # Navigate to observation media page with qualification and learner
        url = "http://localhost/v2p-formatter/observation-media?qualification=Fire&learner=lesnoi"
        print(f"\n1. Navigating to: {url}")
        driver.get(url)
        time.sleep(2)
        
        # Screenshot 1: Initial page load
        driver.save_screenshot('test_media_browser_01_initial_load.png')
        print("   ✓ Screenshot saved: test_media_browser_01_initial_load.png")
        
        # Check console logs
        print("\n2. Checking browser console logs...")
        logs = driver.get_log('browser')
        if logs:
            print(f"   Found {len(logs)} console log entries:")
            for log in logs[:10]:  # Show first 10 logs
                print(f"   [{log['level']}] {log['message']}")
        else:
            print("   No console logs found")
        
        # Check network requests
        print("\n3. Checking network requests...")
        try:
            # Get performance logs
            perf_logs = driver.get_log('performance')
            network_requests = []
            for log in perf_logs:
                message = json.loads(log['message'])
                if message['message']['method'] == 'Network.responseReceived':
                    url = message['message']['params']['response']['url']
                    status = message['message']['params']['response']['status']
                    network_requests.append((url, status))
            
            print(f"   Found {len(network_requests)} network requests:")
            for url, status in network_requests[:10]:  # Show first 10
                if 'observation-media' in url or 'media' in url.lower():
                    print(f"   [{status}] {url}")
        except Exception as e:
            print(f"   Could not get network logs: {e}")
        
        # Wait for qualification select to be present
        print("\n4. Waiting for qualification select...")
        try:
            qualification_select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'qualificationSelect'))
            )
            qualification_value = qualification_select.get_attribute('value')
            print(f"   ✓ Qualification select found, value: {qualification_value}")
        except TimeoutException:
            print("   ✗ Qualification select not found!")
            driver.save_screenshot('test_media_browser_02_no_qualification_select.png')
            return
        
        # Wait for learner select to be present
        print("\n5. Waiting for learner select...")
        try:
            learner_select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'learnerSelect'))
            )
            learner_value = learner_select.get_attribute('value')
            print(f"   ✓ Learner select found, value: {learner_value}")
        except TimeoutException:
            print("   ✗ Learner select not found!")
            driver.save_screenshot('test_media_browser_03_no_learner_select.png')
            return
        
        # Check if media grid exists
        print("\n6. Checking media grid...")
        try:
            media_grid = driver.find_element(By.ID, 'observationMediaGrid')
            grid_text = media_grid.text
            print(f"   ✓ Media grid found")
            print(f"   Grid content: {grid_text[:100]}...")
            
            # Screenshot 2: After page load
            driver.save_screenshot('test_media_browser_04_after_page_load.png')
            print("   ✓ Screenshot saved: test_media_browser_04_after_page_load.png")
        except Exception as e:
            print(f"   ✗ Media grid not found: {e}")
            driver.save_screenshot('test_media_browser_05_no_media_grid.png')
            return
        
        # Wait for loading to complete (check for "Loading" text to disappear)
        print("\n7. Waiting for media to load (max 30 seconds)...")
        start_time = time.time()
        max_wait = 30
        
        while time.time() - start_time < max_wait:
            try:
                # Check if loading message is gone
                media_grid = driver.find_element(By.ID, 'observationMediaGrid')
                grid_text = media_grid.text
                
                if 'Loading' not in grid_text:
                    print(f"   ✓ Loading completed! Grid text: {grid_text[:100]}...")
                    break
                
                # Check for error messages
                if 'Error' in grid_text or 'error' in grid_text.lower():
                    print(f"   ✗ Error detected: {grid_text[:200]}")
                    break
                
                time.sleep(1)
            except Exception as e:
                print(f"   Error checking grid: {e}")
                break
        
        elapsed = time.time() - start_time
        print(f"   Waited {elapsed:.1f} seconds")
        
        # Screenshot 3: After waiting
        driver.save_screenshot('test_media_browser_06_after_wait.png')
        print("   ✓ Screenshot saved: test_media_browser_06_after_wait.png")
        
        # Check final state
        print("\n8. Checking final state...")
        try:
            media_grid = driver.find_element(By.ID, 'observationMediaGrid')
            grid_text = media_grid.text
            print(f"   Grid text: {grid_text[:200]}...")
            
            # Check for media cards
            media_cards = driver.find_elements(By.CLASS_NAME, 'observation-media-card')
            print(f"   Media cards found: {len(media_cards)}")
            
            # Check file count
            try:
                count_el = driver.find_element(By.ID, 'observationMediaCount')
                count_text = count_el.text
                print(f"   File count display: {count_text}")
            except:
                print("   File count element not found")
            
            # Screenshot 4: Final state
            driver.save_screenshot('test_media_browser_07_final_state.png')
            print("   ✓ Screenshot saved: test_media_browser_07_final_state.png")
            
        except Exception as e:
            print(f"   Error checking final state: {e}")
        
        # Check console logs again
        print("\n9. Final console logs check...")
        logs = driver.get_log('browser')
        error_logs = [log for log in logs if log['level'] == 'SEVERE']
        if error_logs:
            print(f"   Found {len(error_logs)} error logs:")
            for log in error_logs[-5:]:  # Show last 5 errors
                print(f"   ERROR: {log['message']}")
        
        # Execute JavaScript to check for errors
        print("\n10. Executing JavaScript checks...")
        try:
            # Check if loadObservationMedia function exists
            has_load_func = driver.execute_script("return typeof loadObservationMedia === 'function';")
            print(f"   loadObservationMedia function exists: {has_load_func}")
            
            # Check if displayObservationMedia function exists
            has_display_func = driver.execute_script("return typeof displayObservationMedia === 'function';")
            print(f"   displayObservationMedia function exists: {has_display_func}")
            
            # Check window.observationMediaData
            has_data = driver.execute_script("return typeof window.observationMediaData !== 'undefined';")
            print(f"   window.observationMediaData exists: {has_data}")
            
            # Try to get the fetch URL that should be called
            qualification = driver.execute_script("return document.getElementById('qualificationSelect')?.value || '';")
            learner = driver.execute_script("return document.getElementById('learnerSelect')?.value || '';")
            print(f"   Qualification from JS: {qualification}")
            print(f"   Learner from JS: {learner}")
            
            # Check what learners are available
            learner_options = driver.execute_script("""
                const select = document.getElementById('learnerSelect');
                if (!select) return [];
                return Array.from(select.options).map(opt => opt.value);
            """)
            print(f"   Available learners in dropdown: {learner_options}")
            
            if qualification and learner:
                expected_url = f"/v2p-formatter/media-converter/observation-media/media?qualification={qualification}&learner={learner}"
                print(f"   Expected fetch URL: {expected_url}")
                
                # Try to call the API directly
                print(f"\n11. Testing API endpoint directly...")
                import requests
                try:
                    api_url = f"http://localhost{expected_url}"
                    print(f"   Calling: {api_url}")
                    response = requests.get(api_url, timeout=5)
                    print(f"   Status: {response.status_code}")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"   Success: {data.get('success')}")
                        print(f"   Media count: {data.get('count', 0)}")
                        print(f"   Error: {data.get('error', 'None')}")
                    else:
                        print(f"   Response: {response.text[:200]}")
                except Exception as e:
                    print(f"   Error calling API: {e}")
            
        except Exception as e:
            print(f"   Error executing JavaScript: {e}")
        
        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)
        print("\nScreenshots saved:")
        print("  - test_media_browser_01_initial_load.png")
        print("  - test_media_browser_04_after_page_load.png")
        print("  - test_media_browser_06_after_wait.png")
        print("  - test_media_browser_07_final_state.png")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED WITH EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot('test_media_browser_ERROR.png')
    finally:
        driver.quit()

if __name__ == '__main__':
    test_media_browser_loading()

