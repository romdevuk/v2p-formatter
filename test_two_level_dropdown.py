"""
Test two-level dropdown system for observation-media page
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

def test_two_level_dropdown():
    """Test the two-level dropdown system"""
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
        
        # Take screenshot of initial state
        driver.save_screenshot('test_two_level_initial.png')
        print("📸 Screenshot saved: test_two_level_initial.png")
        
        # Check if qualification dropdown exists
        qualification_select = driver.find_element(By.ID, 'qualificationSelect')
        assert qualification_select is not None, "Qualification dropdown not found"
        print("✅ Qualification dropdown found")
        
        # Check if learner dropdown exists and is disabled
        learner_select = driver.find_element(By.ID, 'learnerSelect')
        assert learner_select is not None, "Learner dropdown not found"
        assert not learner_select.is_enabled(), "Learner dropdown should be disabled initially"
        print("✅ Learner dropdown found and disabled")
        
        # Get qualification options
        qualification_options = [opt.text for opt in qualification_select.find_elements(By.TAG_NAME, 'option')]
        print(f"📋 Qualifications found: {qualification_options}")
        
        if len(qualification_options) > 1:  # More than just "Select Qualification..."
            # Select first qualification
            qualification_select.click()
            time.sleep(0.5)
            qualification_select.find_elements(By.TAG_NAME, 'option')[1].click()
            selected_qualification = qualification_options[1]
            print(f"✅ Selected qualification: {selected_qualification}")
            
            # Wait for learner dropdown to be enabled
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'learnerSelect'))
            )
            print("✅ Learner dropdown enabled")
            
            # Take screenshot after qualification selection
            driver.save_screenshot('test_two_level_qualification_selected.png')
            print("📸 Screenshot saved: test_two_level_qualification_selected.png")
            
            # Get learner options
            learner_select = driver.find_element(By.ID, 'learnerSelect')
            learner_options = [opt.text for opt in learner_select.find_elements(By.TAG_NAME, 'option')]
            print(f"📋 Learners found: {learner_options}")
            
            if len(learner_options) > 1:  # More than just "Select Learner..."
                # Select first learner
                learner_select.click()
                time.sleep(0.5)
                learner_select.find_elements(By.TAG_NAME, 'option')[1].click()
                selected_learner = learner_options[1]
                print(f"✅ Selected learner: {selected_learner}")
                
                # Wait for media to load (check for media grid or loading message)
                time.sleep(2)  # Give time for media to load
                
                # Take screenshot after learner selection
                driver.save_screenshot('test_two_level_learner_selected.png')
                print("📸 Screenshot saved: test_two_level_learner_selected.png")
                
                # Check if media browser shows content
                try:
                    media_grid = driver.find_element(By.ID, 'observationMediaGrid')
                    grid_content = media_grid.text
                    print(f"📊 Media grid content: {grid_content[:100]}...")
                    
                    # Check for error messages
                    if "error" in grid_content.lower() or "not found" in grid_content.lower():
                        print("⚠️  Warning: Possible error in media grid")
                    else:
                        print("✅ Media grid loaded successfully")
                except NoSuchElementException:
                    print("⚠️  Media grid not found")
                
                # Check file count
                try:
                    file_count = driver.find_element(By.ID, 'observationMediaCount')
                    print(f"📁 File count: {file_count.text}")
                except NoSuchElementException:
                    print("⚠️  File count element not found")
                
                # Check browser console for errors
                logs = driver.get_log('browser')
                errors = [log for log in logs if log['level'] == 'SEVERE']
                if errors:
                    print(f"❌ Browser errors found: {len(errors)}")
                    for error in errors[:5]:  # Show first 5 errors
                        print(f"   - {error['message']}")
                else:
                    print("✅ No browser errors")
            else:
                print("⚠️  No learners found in dropdown")
        else:
            print("⚠️  No qualifications found in dropdown")
        
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        driver.save_screenshot('test_two_level_error.png')
        print("📸 Error screenshot saved: test_two_level_error.png")
        raise
    finally:
        driver.quit()

if __name__ == '__main__':
    test_two_level_dropdown()




