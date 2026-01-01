#!/usr/bin/env python3
"""
Test reshuffle functionality - dragging media within preview tables to reorder
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def test_reshuffle():
    """Test reshuffle - reordering media within tables"""
    print("=" * 60)
    print("🧪 Testing Reshuffle: Reordering Media in Preview Tables")
    print("=" * 60)
    
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    
    try:
        url = "http://localhost/v2p-formatter/observation-media?qualification=Inter&learner=lakhmaniuk"
        print(f"\n🌐 Navigating to: {url}")
        driver.get(url)
        time.sleep(3)
        take_screenshot(driver, "01_page_loaded")
        
        wait = WebDriverWait(driver, 10)
        
        # Load a draft
        print("\n📋 Loading draft...")
        try:
            draft_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Drafts')]")
            if not draft_buttons:
                draft_buttons = driver.find_elements(By.ID, "loadDraftBtn")
            
            if draft_buttons:
                driver.execute_script("arguments[0].click();", draft_buttons[0])
                time.sleep(2)
                
                # Close backdrop
                try:
                    backdrop = driver.find_element(By.CSS_SELECTOR, ".draft-selection-backdrop")
                    if backdrop.is_displayed():
                        driver.execute_script("arguments[0].style.display = 'none';", backdrop)
                        time.sleep(0.5)
                except:
                    pass
                
                load_buttons = wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Load') and not(contains(text(), 'Draft'))]"))
                )
                if load_buttons:
                    driver.execute_script("arguments[0].click();", load_buttons[0])
                    time.sleep(3)
                    print("✅ Draft loaded")
                    take_screenshot(driver, "02_draft_loaded")
        except Exception as e:
            print(f"ℹ️ Could not load draft: {e}")
        
        # First, open a section that has media
        print("\n🔍 Opening a section with media...")
        time.sleep(2)
        
        try:
            # Find collapsed sections
            sections = driver.find_elements(By.CSS_SELECTOR, ".observation-section.collapsed, [data-section-id].collapsed")
            print(f"✅ Found {len(sections)} collapsed sections")
            
            if sections:
                # Try to open the first collapsed section
                section = sections[0]
                section_id = section.get_attribute('data-section-id')
                print(f"✅ Opening section: {section_id}")
                
                # Click the section header to expand it
                section_header = section.find_element(By.CSS_SELECTOR, ".observation-section-header, .section-header")
                driver.execute_script("arguments[0].click();", section_header)
                time.sleep(2)
                take_screenshot(driver, "03_section_opened")
                
                # Check if section is now expanded
                if 'collapsed' not in section.get_attribute('class'):
                    print("✅ Section expanded")
                else:
                    print("⚠️ Section may still be collapsed")
            
            # Now find media cells in preview tables
            print("\n🔍 Finding media cells in preview...")
            time.sleep(1)
            
            # Find all media cells (td elements with media)
            media_cells = driver.find_elements(By.CSS_SELECTOR, ".media-cell[data-media-index]")
            print(f"✅ Found {len(media_cells)} media cells")
            
            if len(media_cells) < 2:
                print("❌ Need at least 2 media cells to test reshuffle!")
                take_screenshot(driver, "03_not_enough_cells")
                return False
            
            # Get first two cells from the same placeholder
            first_cell = media_cells[0]
            first_index = first_cell.get_attribute('data-media-index')
            first_placeholder = first_cell.get_attribute('data-placeholder')
            
            print(f"✅ First cell: index={first_index}, placeholder={first_placeholder}")
            
            # Find second cell in same placeholder
            second_cell = None
            for cell in media_cells[1:]:
                if cell.get_attribute('data-placeholder') == first_placeholder:
                    second_cell = cell
                    second_index = cell.get_attribute('data-media-index')
                    print(f"✅ Second cell: index={second_index}, placeholder={first_placeholder}")
                    break
            
            if not second_cell:
                print("❌ Could not find second cell in same placeholder!")
                take_screenshot(driver, "03_no_second_cell")
                return False
            
            # Scroll cells into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_cell)
            time.sleep(0.5)
            take_screenshot(driver, "04_before_reshuffle")
            
            # Get media names before reshuffle
            first_img = first_cell.find_element(By.TAG_NAME, "img")
            second_img = second_cell.find_element(By.TAG_NAME, "img")
            first_name_before = first_img.get_attribute("alt") or first_img.get_attribute("src")
            second_name_before = second_img.get_attribute("alt") or second_img.get_attribute("src")
            print(f"📦 Before: Cell 0={first_name_before[:50]}, Cell 1={second_name_before[:50]}")
            
            # Perform reshuffle using JavaScript - call handleTableCellDragStart first
            print("\n🔄 Performing reshuffle (drag first cell to second cell position)...")
            
            reshuffle_script = """
            var sourceCell = arguments[0];
            var targetCell = arguments[1];
            var sourceIndex = parseInt(arguments[2]);
            var placeholder = arguments[3];
            
            if (!sourceCell || !targetCell) {
                return {success: false, error: 'Cells not found'};
            }
            
            console.log('[TEST] Starting reshuffle:', {
                sourceIndex: sourceIndex, 
                targetIndex: parseInt(targetCell.dataset.mediaIndex), 
                placeholder: placeholder
            });
            
            // Get media data from assignments
            var assignments = window.observationMediaAssignments || {};
            var placeholderKey = placeholder.toLowerCase();
            var mediaList = assignments[placeholderKey] || [];
            
            if (!mediaList[sourceIndex]) {
                return {success: false, error: 'Source media not found'};
            }
            
            var mediaData = {
                ...mediaList[sourceIndex],
                source: 'table',
                placeholder: placeholder,
                index: sourceIndex
            };
            
            // Create DataTransfer
            var dataTransfer = new DataTransfer();
            dataTransfer.setData('application/json', JSON.stringify(mediaData));
            dataTransfer.setData('text/plain', JSON.stringify(mediaData));
            dataTransfer.effectAllowed = 'move';
            
            // Create drop event
            var dropEvent = {
                preventDefault: function() {},
                stopPropagation: function() {},
                dataTransfer: dataTransfer,
                target: targetCell,
                currentTarget: targetCell
            };
            
            // Add closest method to dropEvent.target for handleTableDrop
            if (!dropEvent.target.closest) {
                dropEvent.target.closest = function(selector) {
                    var element = this;
                    while (element) {
                        if (element.matches && element.matches(selector)) {
                            return element;
                        }
                        element = element.parentElement;
                    }
                    return null;
                };
            }
            
            // Call handleTableDrop directly
            if (typeof window.handleTableDrop === 'function') {
                console.log('[TEST] Calling window.handleTableDrop');
                try {
                    window.handleTableDrop(dropEvent, placeholder);
                    return {
                        success: true,
                        sourceIndex: sourceIndex,
                        targetIndex: parseInt(targetCell.dataset.mediaIndex),
                        placeholder: placeholder
                    };
                } catch (e) {
                    return {success: false, error: e.message};
                }
            } else {
                return {success: false, error: 'handleTableDrop not found'};
            }
            """
            
            result = driver.execute_script(
                reshuffle_script, 
                first_cell, 
                second_cell, 
                first_index, 
                first_placeholder
            )
            print(f"✅ Reshuffle script executed: {result}")
            time.sleep(3)
            take_screenshot(driver, "05_after_reshuffle")
            
            # Check if order changed
            print("\n🔍 Checking if order changed...")
            time.sleep(1)
            
            # Re-find cells (they might have been re-rendered)
            media_cells_after = driver.find_elements(By.CSS_SELECTOR, f".media-cell[data-placeholder='{first_placeholder}']")
            if len(media_cells_after) >= 2:
                first_cell_after = media_cells_after[0]
                second_cell_after = media_cells_after[1]
                
                first_img_after = first_cell_after.find_element(By.TAG_NAME, "img")
                second_img_after = second_cell_after.find_element(By.TAG_NAME, "img")
                first_name_after = first_img_after.get_attribute("alt") or first_img_after.get_attribute("src")
                second_name_after = second_img_after.get_attribute("alt") or second_img_after.get_attribute("src")
                
                print(f"📦 After: Cell 0={first_name_after[:50]}, Cell 1={second_name_after[:50]}")
                
                # Check if order swapped
                if first_name_before != first_name_after or second_name_before != second_name_after:
                    print("✅ Order changed - reshuffle worked!")
                    return True
                else:
                    print("⚠️ Order did not change - reshuffle may not have worked")
                    return False
            else:
                print("⚠️ Could not find cells after reshuffle")
                return False
            
        except Exception as e:
            print(f"❌ Error during reshuffle test: {e}")
            import traceback
            traceback.print_exc()
            take_screenshot(driver, "error_reshuffle")
            return False
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        print("\n⏳ Waiting 3 seconds...")
        time.sleep(3)
        print("🔒 Closing browser...")
        driver.quit()

if __name__ == "__main__":
    success = test_reshuffle()
    print("\n" + "=" * 60)
    if success:
        print("✅ TEST PASSED: Reshuffle working")
    else:
        print("❌ TEST FAILED: Reshuffle not working")
    print("=" * 60)
    sys.exit(0 if success else 1)

