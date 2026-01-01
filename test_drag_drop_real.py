#!/usr/bin/env python3
"""
Test real drag and drop from media browser to preview - with console logging
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

def test_drag_drop_real():
    """Test real drag and drop with console monitoring"""
    print("=" * 60)
    print("🧪 Testing Real Drag and Drop: Media Browser → Preview")
    print("=" * 60)
    
    # Setup - NOT headless so we can see what's happening
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Commented out for debugging
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    
    try:
        # Navigate to page
        url = "http://localhost/v2p-formatter/observation-media?qualification=Inter&learner=lakhmaniuk"
        print(f"\n🌐 Navigating to: {url}")
        driver.get(url)
        time.sleep(3)
        take_screenshot(driver, "01_page_loaded")
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        # Load a draft first to get placeholders
        print("\n📋 Loading draft...")
        try:
            # Find and click the drafts button
            draft_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Drafts') or contains(text(), 'Load Draft')]")
            if not draft_buttons:
                # Try by ID
                draft_buttons = driver.find_elements(By.ID, "loadDraftBtn")
            
            if draft_buttons:
                print("✅ Found draft button, clicking...")
                # Use JavaScript click to avoid backdrop interception
                driver.execute_script("arguments[0].click();", draft_buttons[0])
                time.sleep(2)
                take_screenshot(driver, "01a_draft_dialog_opened")
                
                # Close backdrop if it exists and is blocking
                try:
                    backdrop = driver.find_element(By.CSS_SELECTOR, ".draft-selection-backdrop")
                    if backdrop.is_displayed():
                        print("✅ Found backdrop, closing it...")
                        driver.execute_script("arguments[0].style.display = 'none';", backdrop)
                        time.sleep(0.5)
                except:
                    pass
                
                # Find and click the Load button in the dialog
                load_buttons = wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Load') and not(contains(text(), 'Draft'))]"))
                )
                if load_buttons:
                    print(f"✅ Found {len(load_buttons)} load button(s), clicking first one...")
                    # Use JavaScript click
                    driver.execute_script("arguments[0].click();", load_buttons[0])
                    time.sleep(3)
                    print("✅ Draft loaded")
                    take_screenshot(driver, "01b_draft_loaded")
                else:
                    print("⚠️ No load buttons found in dialog")
            else:
                print("ℹ️ No draft button found - continuing without draft")
        except Exception as e:
            print(f"ℹ️ Could not load draft: {e}")
            import traceback
            traceback.print_exc()
        
        # Find media card
        print("\n🖼️ Finding media card...")
        try:
            media_cards = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".observation-media-card:not(.media-assigned)"))
            )
            print(f"✅ Found {len(media_cards)} unassigned media cards")
            
            if len(media_cards) == 0:
                print("❌ No unassigned media cards!")
                return False
            
            source_card = media_cards[0]
            media_path = source_card.get_attribute('data-media-path')
            media_name = source_card.get_attribute('data-media-name')
            print(f"✅ Selected: {media_name}")
            print(f"   Path: {media_path}")
            
        except TimeoutException:
            print("❌ No media cards found!")
            return False
        
        # Find preview area
        print("\n📄 Finding preview area...")
        try:
            preview_area = wait.until(
                EC.presence_of_element_located((By.ID, "observationPreview"))
            )
            print("✅ Found preview area")
        except TimeoutException:
            print("❌ Preview area not found!")
            return False
        
        # Clear console logs before drag
        driver.get_log('browser')
        
        # Perform drag and drop using JavaScript (more reliable than ActionChains)
        print("\n🔄 Performing drag and drop...")
        try:
            # Scroll both into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", source_card)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", preview_area)
            time.sleep(1)
            take_screenshot(driver, "02_before_drag")
            
            # Get media data from card
            media_data = {
                'path': source_card.get_attribute('data-media-path'),
                'name': source_card.get_attribute('data-media-name'),
                'type': source_card.get_attribute('data-media-type') or 'image'
            }
            print(f"📦 Media data: {media_data}")
            
            # Use JavaScript to simulate drag and drop properly
            drag_drop_script = """
            var sourceCard = arguments[0];
            var previewArea = arguments[1];
            var mediaData = arguments[2];
            
            // Create DataTransfer object
            var dataTransfer = new DataTransfer();
            var jsonData = JSON.stringify(mediaData);
            dataTransfer.setData('application/json', jsonData);
            dataTransfer.setData('text/plain', jsonData);
            dataTransfer.effectAllowed = 'copy';
            
            // Store in window for fallback
            window.lastDragData = mediaData;
            
            // Mark card as dragging
            sourceCard.classList.add('dragging');
            
            // Create and dispatch dragstart event
            var dragStartEvent = new DragEvent('dragstart', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            sourceCard.dispatchEvent(dragStartEvent);
            
            // Create and dispatch dragover event on preview
            var dragOverEvent = new DragEvent('dragover', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            dragOverEvent.preventDefault();
            previewArea.dispatchEvent(dragOverEvent);
            
            // Create and dispatch drop event
            var dropEvent = new DragEvent('drop', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            });
            dropEvent.preventDefault();
            dropEvent.stopPropagation();
            previewArea.dispatchEvent(dropEvent);
            
            // Clean up
            sourceCard.classList.remove('dragging');
            
            return {
                success: true,
                dragStartDispatched: true,
                dragOverDispatched: true,
                dropDispatched: true
            };
            """
            
            result = driver.execute_script(drag_drop_script, source_card, preview_area, media_data)
            print(f"✅ JavaScript drag and drop executed: {result}")
            time.sleep(3)
            take_screenshot(driver, "05_after_drop")
            
        except Exception as e:
            print(f"❌ Error during drag: {e}")
            import traceback
            traceback.print_exc()
            take_screenshot(driver, "error_drag")
            return False
        
        # Check console logs
        print("\n📋 Checking console logs...")
        try:
            logs = driver.get_log('browser')
            drop_logs = []
            drag_logs = []
            error_logs = []
            
            for log in logs:
                message = log.get('message', '')
                level = log.get('level', '')
                
                if 'DROP' in message or 'drop' in message.lower():
                    drop_logs.append(log)
                if 'DRAG' in message or 'drag' in message.lower():
                    drag_logs.append(log)
                if level == 'SEVERE' or 'error' in message.lower():
                    error_logs.append(log)
            
            print(f"\n📊 Found {len(drop_logs)} drop-related logs:")
            for log in drop_logs[-10:]:  # Last 10
                print(f"   [{log.get('level')}] {log.get('message')[:150]}")
            
            print(f"\n📊 Found {len(drag_logs)} drag-related logs:")
            for log in drag_logs[-10:]:  # Last 10
                print(f"   [{log.get('level')}] {log.get('message')[:150]}")
            
            # Also check all recent logs for debugging
            print(f"\n📊 All recent logs (last 20):")
            for log in logs[-20:]:
                msg = log.get('message', '')[:200]
                if msg:  # Only show non-empty messages
                    print(f"   [{log.get('level')}] {msg}")
            
            if error_logs:
                print(f"\n❌ Found {len(error_logs)} errors:")
                for log in error_logs[-10:]:  # Last 10
                    print(f"   [{log.get('level')}] {log.get('message')[:200]}")
            
            # Check for specific error
            no_data_errors = [log for log in logs if 'No data in dataTransfer' in log.get('message', '')]
            if no_data_errors:
                print(f"\n❌ Found {len(no_data_errors)} 'No data in dataTransfer' errors!")
                for log in no_data_errors:
                    print(f"   {log.get('message')}")
                return False
            
            # Check if placeholder dialog appeared
            print("\n🔍 Checking for placeholder dialog...")
            time.sleep(2)
            try:
                dialogs = driver.find_elements(By.CSS_SELECTOR, ".placeholder-dialog, .modal, [role='dialog'], .dialog")
                visible_dialogs = [d for d in dialogs if d.is_displayed()]
                if visible_dialogs:
                    print(f"✅ Found {len(visible_dialogs)} visible dialog(s)")
                    take_screenshot(driver, "06_dialog_appeared")
                    return True
                else:
                    print("⚠️ No visible dialogs found")
            except:
                pass
            
            # Check if media was assigned
            print("\n🔍 Checking if media was assigned...")
            try:
                assigned_cards = driver.find_elements(By.CSS_SELECTOR, ".observation-media-card.media-assigned")
                if len(assigned_cards) > 0:
                    print(f"✅ Found {len(assigned_cards)} assigned media cards")
                    return True
            except:
                pass
            
            # If we got here and no errors, check logs for success
            success_logs = [log for log in logs if 'Got data from' in log.get('message', '')]
            if success_logs:
                print(f"✅ Found {len(success_logs)} success logs indicating data was received")
                return True
            
            print("⚠️ No clear indication of success or failure")
            return False
            
        except Exception as e:
            print(f"❌ Error checking logs: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        take_screenshot(driver, "error_final")
        return False
        
    finally:
        print("\n⏳ Waiting 5 seconds before closing...")
        time.sleep(5)
        print("🔒 Closing browser...")
        driver.quit()

if __name__ == "__main__":
    success = test_drag_drop_real()
    print("\n" + "=" * 60)
    if success:
        print("✅ TEST PASSED")
    else:
        print("❌ TEST FAILED")
    print("=" * 60)
    sys.exit(0 if success else 1)

