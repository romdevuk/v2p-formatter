"""
Test media loading with Inter qualification
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def test_inter_media_loading():
    """Test loading media with Inter qualification"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("🌐 Navigating to observation-media page...")
        driver.get('http://localhost/v2p-formatter/observation-media')
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'qualificationSelect'))
        )
        print("✅ Page loaded successfully")
        
        # Take initial screenshot
        driver.save_screenshot('test_inter_initial.png')
        print("📸 Screenshot saved: test_inter_initial.png")
        
        # Select Inter qualification
        qualification_select = Select(driver.find_element(By.ID, 'qualificationSelect'))
        qualification_select.select_by_visible_text('Inter')
        print("✅ Selected qualification: Inter")
        
        # Wait for learner dropdown to be enabled
        time.sleep(1)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, 'learnerSelect'))
        )
        print("✅ Learner dropdown enabled")
        
        # Take screenshot after qualification selection
        driver.save_screenshot('test_inter_qualification_selected.png')
        print("📸 Screenshot saved: test_inter_qualification_selected.png")
        
        # Get learner options
        learner_select = Select(driver.find_element(By.ID, 'learnerSelect'))
        learner_options = [opt.text for opt in learner_select.options]
        print(f"📋 Learners found: {learner_options}")
        
        if len(learner_options) > 1:  # More than just "Select Learner..."
            # Select first learner
            first_learner = learner_options[1]
            learner_select.select_by_visible_text(first_learner)
            print(f"✅ Selected learner: {first_learner}")
            
            # Manually trigger change event via JavaScript
            driver.execute_script("""
                const learnerSelect = document.getElementById('learnerSelect');
                if (learnerSelect) {
                    const event = new Event('change', { bubbles: true });
                    learnerSelect.dispatchEvent(event);
                    console.log('Manually triggered change event');
                }
            """)
            print("✅ Manually triggered change event")
            
            # Wait for media to load
            print("⏳ Waiting for media to load...")
            time.sleep(3)
            
            # Take screenshot after learner selection
            driver.save_screenshot('test_inter_learner_selected.png')
            print("📸 Screenshot saved: test_inter_learner_selected.png")
            
            # Check browser console for errors
            logs = driver.get_log('browser')
            errors = [log for log in logs if log['level'] == 'SEVERE']
            warnings = [log for log in logs if log['level'] == 'WARNING']
            
            if errors:
                print(f"\n❌ Browser errors found: {len(errors)}")
                for error in errors[:5]:
                    print(f"   - {error['message']}")
            else:
                print("✅ No browser errors")
            
            if warnings:
                print(f"\n⚠️  Browser warnings found: {len(warnings)}")
                for warning in warnings[:5]:
                    print(f"   - {warning['message']}")
            
            # Check media grid content
            try:
                media_grid = driver.find_element(By.ID, 'observationMediaGrid')
                grid_content = media_grid.text
                print(f"\n📊 Media grid content:")
                print(f"   {grid_content[:200]}...")
                
                # Check if it shows loading or error
                if "Loading" in grid_content:
                    print("⏳ Still loading...")
                elif "error" in grid_content.lower() or "not found" in grid_content.lower():
                    print("❌ Error in media grid")
                elif "Please select" in grid_content:
                    print("⚠️  Still showing selection message")
                else:
                    print("✅ Media grid has content")
            except NoSuchElementException:
                print("❌ Media grid not found")
            
            # Check file count
            try:
                file_count = driver.find_element(By.ID, 'observationMediaCount')
                print(f"\n📁 File count: {file_count.text}")
            except NoSuchElementException:
                print("⚠️  File count element not found")
            
            # Check console logs for debugging
            console_logs = driver.get_log('browser')
            all_logs = [log for log in console_logs if log['level'] != 'SEVERE' or 'favicon' not in log['message'].lower()]
            print(f"\n📝 Recent console logs (last 15):")
            for log in all_logs[-15:]:
                print(f"   [{log['level']}] {log['message'][:150]}")
            
            # Check if displayObservationMedia function exists
            has_display_func = driver.execute_script("return typeof displayObservationMedia === 'function'")
            print(f"\n🔍 displayObservationMedia function exists: {has_display_func}")
            
            # Check current values
            current_qual = driver.execute_script("return document.getElementById('qualificationSelect')?.value")
            current_learner = driver.execute_script("return document.getElementById('learnerSelect')?.value")
            print(f"🔍 Current qualification: {current_qual}")
            print(f"🔍 Current learner: {current_learner}")
            
            # Try calling loadObservationMedia directly and check response
            try:
                result = driver.execute_script("""
                    const qualification = document.getElementById('qualificationSelect')?.value;
                    const learner = document.getElementById('learnerSelect')?.value;
                    console.log('Calling loadObservationMedia with:', qualification, learner);
                    
                    // Set up a promise to track fetch completion
                    window.fetchCompleted = false;
                    window.fetchError = null;
                    window.fetchData = null;
                    
                    // Override fetch temporarily to track it
                    const originalFetch = window.fetch;
                    window.fetch = function(...args) {
                        console.log('Fetch called with:', args[0]);
                        return originalFetch.apply(this, args)
                            .then(response => {
                                console.log('Fetch response:', response.status);
                                return response.json().then(data => {
                                    window.fetchCompleted = true;
                                    window.fetchData = data;
                                    console.log('Fetch data:', data);
                                    return new Response(JSON.stringify(data), {
                                        status: response.status,
                                        statusText: response.statusText,
                                        headers: response.headers
                                    });
                                });
                            })
                            .catch(error => {
                                window.fetchError = error.message;
                                console.error('Fetch error:', error);
                                throw error;
                            });
                    };
                    
                    if (typeof loadObservationMedia === 'function') {
                        loadObservationMedia();
                        return {called: true, qualification: qualification, learner: learner};
                    }
                    return {called: false, error: 'function not found'};
                """)
                print(f"🔍 Direct call result: {result}")
                if result.get('error'):
                    print(f"❌ Error calling loadObservationMedia: {result.get('error')}")
                    if result.get('stack'):
                        print(f"   Stack: {result.get('stack')[:200]}")
                
                time.sleep(2)  # Wait a bit
                
                # Check test result
                test_result = driver.execute_script("return window.testResult || null;")
                if test_result:
                    print(f"🔍 Before/After comparison: {test_result}")
                
                time.sleep(3)  # Wait for fetch to complete
                
                # Check if fetch was called by checking network activity
                # Also check if the message changed
                status_check = driver.execute_script("""
                    const grid = document.getElementById('observationMediaGrid');
                    const message = document.getElementById('mediaBrowserMessage');
                    return {
                        gridText: grid ? grid.textContent.substring(0, 100) : 'no grid',
                        messageText: message ? message.textContent : 'no message',
                        gridHTML: grid ? grid.innerHTML.substring(0, 200) : 'no grid'
                    };
                """)
                print(f"🔍 Final grid status: {status_check}")
                
                # Check media grid again
                media_grid = driver.find_element(By.ID, 'observationMediaGrid')
                grid_content = media_grid.text
                grid_html = media_grid.get_attribute('innerHTML')
                print(f"\n📊 Media grid content after direct call:")
                print(f"   Text: {grid_content[:300]}...")
                print(f"   HTML length: {len(grid_html)}")
                
                # Check message element
                try:
                    msg_element = driver.find_element(By.ID, 'mediaBrowserMessage')
                    msg_text = msg_element.text
                    print(f"   Message element text: {msg_text}")
                except:
                    print(f"   Message element not found")
                
                # Check if fetch completed by looking at network activity
                # Try to get the actual media count
                try:
                    count_el = driver.find_element(By.ID, 'observationMediaCount')
                    count_text = count_el.text
                    print(f"   File count element: {count_text}")
                except:
                    print(f"   File count element not found")
                    
                # Check if there are any media cards
                try:
                    media_cards = driver.find_elements(By.CLASS_NAME, 'observation-media-card')
                    print(f"   Media cards found: {len(media_cards)}")
                except:
                    print(f"   Could not find media cards")
                
                # Check for fetch errors in console
                console_logs_after = driver.get_log('browser')
                fetch_logs = [log for log in console_logs_after if 'fetch' in log['message'].lower() or 'media' in log['message'].lower() or 'error' in log['message'].lower()]
                if fetch_logs:
                    print(f"\n📝 Fetch/Media related logs:")
                    for log in fetch_logs[-10:]:
                        print(f"   [{log['level']}] {log['message'][:200]}")
                        
            except Exception as e:
                print(f"❌ Error calling loadObservationMedia: {e}")
                import traceback
                traceback.print_exc()
            
        else:
            print("⚠️  No learners found in Inter qualification")
        
        print("\n✅ Test completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot('test_inter_error.png')
        print("📸 Error screenshot saved: test_inter_error.png")
        raise
    finally:
        driver.quit()

if __name__ == '__main__':
    test_inter_media_loading()

