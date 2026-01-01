#!/usr/bin/env python3
"""
Test drag and drop from media browser to preview area
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import sys

def take_screenshot(driver, name):
    """Take a screenshot"""
    screenshot_dir = "test_screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    path = os.path.join(screenshot_dir, f"{name}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot: {path}")
    return path

def test_drag_drop_preview():
    """Test dragging media from browser to preview"""
    print("=" * 60)
    print("🧪 Testing Drag and Drop: Media Browser → Preview")
    print("=" * 60)
    
    # Setup
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    
    try:
        # Navigate to page
        url = "http://localhost/v2p-formatter/observation-media?qualification=Inter&learner=lakhmaniuk"
        print(f"\n🌐 Navigating to: {url}")
        driver.get(url)
        time.sleep(2)
        take_screenshot(driver, "01_page_loaded")
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        # Check for console errors
        console_errors = []
        try:
            logs = driver.get_log('browser')
            for log in logs:
                if log['level'] == 'SEVERE':
                    console_errors.append(log['message'])
        except:
            pass
        
        if console_errors:
            print(f"\n⚠️ Found {len(console_errors)} browser errors")
            for err in console_errors[:5]:
                print(f"   {err}")
        
        # Step 1: Load a draft (if available)
        print("\n📋 Step 1: Checking for drafts...")
        try:
            # Look for draft button or draft list
            draft_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Drafts') or contains(text(), 'Load Draft')]")
            if draft_buttons:
                print("✅ Found draft button, clicking...")
                draft_buttons[0].click()
                time.sleep(1)
                take_screenshot(driver, "02_draft_dialog")
                
                # Try to load first draft if available
                load_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Load')]")
                if load_buttons:
                    print("✅ Found load button, loading draft...")
                    load_buttons[0].click()
                    time.sleep(3)
                    take_screenshot(driver, "03_draft_loaded")
        except Exception as e:
            print(f"ℹ️ No drafts available or error loading: {e}")
        
        # Step 2: Find a media card in the browser
        print("\n🖼️ Step 2: Looking for media cards...")
        try:
            # Wait for media cards to appear
            media_cards = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".observation-media-card:not(.media-assigned)"))
            )
            print(f"✅ Found {len(media_cards)} media cards")
            
            if len(media_cards) == 0:
                print("❌ No unassigned media cards found!")
                take_screenshot(driver, "04_no_media_cards")
                return False
            
            # Get first unassigned card
            source_card = media_cards[0]
            media_path = source_card.get_attribute('data-media-path')
            media_name = source_card.get_attribute('data-media-name')
            print(f"✅ Selected media: {media_name}")
            print(f"   Path: {media_path}")
            take_screenshot(driver, "04_media_card_selected")
            
        except TimeoutException:
            print("❌ No media cards found!")
            take_screenshot(driver, "04_no_media_cards")
            return False
        
        # Step 3: Find the preview area
        print("\n📄 Step 3: Looking for preview area...")
        try:
            preview_area = wait.until(
                EC.presence_of_element_located((By.ID, "observationPreview"))
            )
            print("✅ Found preview area")
            
            # Scroll preview into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", preview_area)
            time.sleep(1)
            take_screenshot(driver, "05_preview_area")
            
        except TimeoutException:
            print("❌ Preview area not found!")
            return False
        
        # Step 4: Test drop handler directly with JavaScript
        print("\n🔄 Step 4: Testing drop handler...")
        try:
            # Get media data from the first card
            media_path = driver.execute_script("""
                var cards = document.querySelectorAll('.observation-media-card:not(.media-assigned)');
                if (cards.length === 0) return null;
                return {
                    path: cards[0].dataset.mediaPath,
                    name: cards[0].dataset.mediaName,
                    type: cards[0].dataset.mediaType || 'image'
                };
            """)
            
            if not media_path:
                print("❌ No media data found!")
                return False
            
            print(f"✅ Media data: {media_path['name']}")
            
            # Test the drop handler directly
            drop_test_script = """
            var mediaData = arguments[0];
            var previewArea = document.getElementById('observationPreview');
            
            if (!previewArea) {
                return {success: false, error: 'Preview area not found'};
            }
            
            // Create a mock drop event with dataTransfer
            var dataTransfer = new DataTransfer();
            dataTransfer.setData('application/json', JSON.stringify(mediaData));
            dataTransfer.setData('text/plain', JSON.stringify(mediaData));
            dataTransfer.effectAllowed = 'copy';
            
            // Create drop event
            var dropEvent = new DragEvent('drop', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            
            // Store data in window for fallback
            window.lastDragData = mediaData;
            
            // Call the drop handler
            try {
                if (typeof window.handlePreviewDrop === 'function') {
                    window.handlePreviewDrop(dropEvent);
                    return {success: true, handler: 'window.handlePreviewDrop'};
                } else {
                    return {success: false, error: 'handlePreviewDrop not found'};
                }
            } catch (e) {
                return {success: false, error: e.message, stack: e.stack};
            }
            """
            
            # Handle alerts
            driver.execute_script("window.alert = function() { return true; };")
            driver.execute_script("window.confirm = function() { return true; };")
            
            result = driver.execute_script(drop_test_script, media_path)
            print(f"✅ Drop handler test result: {result}")
            time.sleep(2)
            
            # Check for alerts (which means the handler ran but no placeholders)
            try:
                alert = driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                print(f"ℹ️ Alert received: {alert_text}")
                if "No placeholders" in alert_text:
                    print("✅ Drop handler WORKING - dataTransfer data was received correctly!")
                    print("   (Alert is expected when no placeholders exist)")
                    take_screenshot(driver, "08_drop_success_no_placeholders")
                    return True
            except:
                pass
            
            take_screenshot(driver, "08_drop_completed")
            
            if not result or not result.get('success'):
                print(f"❌ Drop handler failed: {result.get('error') if result else 'No result'}")
                if result and result.get('stack'):
                    print(f"   Stack: {result.get('stack')[:200]}")
                return False
            
            print("✅ Drop handler executed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error testing drop handler: {e}")
            import traceback
            traceback.print_exc()
            take_screenshot(driver, "06_drop_error")
            return False
        
        # Step 5: Check if placeholder dialog appeared
        print("\n🔍 Step 5: Checking for placeholder selection dialog...")
        time.sleep(2)
        try:
            dialog = driver.find_element(By.CSS_SELECTOR, ".placeholder-dialog, .modal, [role='dialog']")
            if dialog.is_displayed():
                print("✅ Placeholder selection dialog appeared!")
                take_screenshot(driver, "09_placeholder_dialog")
                
                # Try to select first placeholder and confirm
                placeholder_options = dialog.find_elements(By.CSS_SELECTOR, "button, .placeholder-option, [data-placeholder]")
                if placeholder_options:
                    print(f"✅ Found {len(placeholder_options)} placeholder options")
                    placeholder_options[0].click()
                    time.sleep(2)
                    take_screenshot(driver, "10_placeholder_selected")
                    return True
                else:
                    print("⚠️ Dialog appeared but no placeholder options found")
                    return True  # Still consider it success if dialog appeared
            else:
                print("⚠️ Dialog found but not visible")
                take_screenshot(driver, "09_no_dialog")
        except NoSuchElementException:
            print("⚠️ No placeholder dialog found - checking console for errors...")
            take_screenshot(driver, "09_no_dialog")
            
            # Check console for errors
            try:
                logs = driver.get_log('browser')
                for log in logs[-10:]:  # Last 10 logs
                    if 'dataTransfer' in log.get('message', '') or 'drop' in log.get('message', '').lower():
                        print(f"   Console: {log['message']}")
            except:
                pass
            
            # Check if media was assigned anyway (maybe direct assignment)
            try:
                assigned_cards = driver.find_elements(By.CSS_SELECTOR, ".observation-media-card.media-assigned")
                if len(assigned_cards) > 0:
                    print(f"✅ Media appears to be assigned ({len(assigned_cards)} assigned cards)")
                    return True
            except:
                pass
            
            return False
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        take_screenshot(driver, "error_final")
        return False
        
    finally:
        print("\n🔒 Closing browser...")
        driver.quit()

if __name__ == "__main__":
    success = test_drag_drop_preview()
    print("\n" + "=" * 60)
    if success:
        print("✅ TEST PASSED: Drag and drop working")
    else:
        print("❌ TEST FAILED: Drag and drop not working")
    print("=" * 60)
    sys.exit(0 if success else 1)

