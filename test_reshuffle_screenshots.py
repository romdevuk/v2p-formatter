#!/usr/bin/env python3
"""
Comprehensive reshuffle functionality test with screenshots
Tests all stages of the reshuffle process and captures screenshots
"""
from playwright.sync_api import sync_playwright
import time
import os
from pathlib import Path

def test_reshuffle_with_screenshots():
    """Test reshuffle functionality and capture screenshots at each stage"""
    
    # Create screenshots directory
    screenshots_dir = Path("reports/screenshots/reshuffle")
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("RESHUFFLE FUNCTIONALITY TEST WITH SCREENSHOTS")
    print("=" * 60)
    
    with sync_playwright() as p:
        # Launch browser in headed mode so we can see what's happening
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        try:
            # Stage 1: Navigate to observation media page
            print("\n[Stage 1] Navigating to observation media page...")
            url = "http://127.0.0.1:5000/v2p-formatter/observation-media"
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)  # Wait for page to fully load
            
            screenshot_path = screenshots_dir / "01_initial_page_load.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"✓ Screenshot saved: {screenshot_path}")
            
            # Stage 2: Add text with placeholder
            print("\n[Stage 2] Adding text with placeholder...")
            text_editor = page.locator("#observationTextEditor")
            if text_editor.count() > 0:
                test_text = "This is a test observation with {{Test_Placeholder}} for reshuffle testing."
                text_editor.fill(test_text)
                time.sleep(1)
                
                screenshot_path = screenshots_dir / "02_text_with_placeholder.png"
                page.screenshot(path=str(screenshot_path), full_page=True)
                print(f"✓ Screenshot saved: {screenshot_path}")
            else:
                print("⚠️  Text editor not found!")
            
            # Stage 3: Assign media to placeholder (simulate having media)
            print("\n[Stage 3] Assigning media to placeholder...")
            page.evaluate("""
                // Initialize assignments if not exists
                if (!window.observationMediaAssignments) {
                    window.observationMediaAssignments = {};
                }
                
                // Clear existing assignments for test
                window.observationMediaAssignments['test_placeholder'] = [];
                
                // Assign first image
                window.assignMediaToPlaceholder('test_placeholder', {
                    path: '/Users/rom/Documents/nvq/v2p-formatter-output/test1.jpg',
                    name: 'test1.jpg',
                    type: 'image'
                });
                
                // Assign second image
                window.assignMediaToPlaceholder('test_placeholder', {
                    path: '/Users/rom/Documents/nvq/v2p-formatter-output/test2.jpg',
                    name: 'test2.jpg',
                    type: 'image'
                });
                
                // Assign third image
                window.assignMediaToPlaceholder('test_placeholder', {
                    path: '/Users/rom/Documents/nvq/v2p-formatter-output/test3.jpg',
                    name: 'test3.jpg',
                    type: 'image'
                });
                
                // Update preview to show assignments
                if (window.updatePreview) {
                    window.updatePreview();
                }
            """)
            time.sleep(2)  # Wait for preview to update
            
            screenshot_path = screenshots_dir / "03_media_assigned.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"✓ Screenshot saved: {screenshot_path}")
            
            # Stage 4: Check if reshuffle button is visible
            print("\n[Stage 4] Checking reshuffle button visibility...")
            reshuffle_btn = page.locator("#reshuffleBtn")
            btn_count = reshuffle_btn.count()
            is_visible = reshuffle_btn.is_visible() if btn_count > 0 else False
            
            print(f"  Reshuffle button found: {btn_count > 0}")
            print(f"  Reshuffle button visible: {is_visible}")
            
            if btn_count > 0:
                btn_text = reshuffle_btn.text_content()
                print(f"  Button text: {btn_text}")
            
            screenshot_path = screenshots_dir / "04_before_reshuffle_enabled.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"✓ Screenshot saved: {screenshot_path}")
            
            # Stage 5: Enable reshuffle mode
            if btn_count > 0 and is_visible:
                print("\n[Stage 5] Enabling reshuffle mode...")
                reshuffle_btn.click()
                time.sleep(1.5)  # Wait for mode to activate
                
                # Check button state after click
                new_btn_text = reshuffle_btn.text_content()
                print(f"  Button text after click: {new_btn_text}")
                
                screenshot_path = screenshots_dir / "05_reshuffle_enabled.png"
                page.screenshot(path=str(screenshot_path), full_page=True)
                print(f"✓ Screenshot saved: {screenshot_path}")
                
                # Stage 6: Check media cells for visual indicators
                print("\n[Stage 6] Checking media cells for visual indicators...")
                media_cells = page.locator(".media-cell")
                cell_count = media_cells.count()
                print(f"  Found {cell_count} media cells")
                
                if cell_count > 0:
                    # Check first cell for visual indicators
                    first_cell = media_cells.first
                    border_style = first_cell.evaluate("""
                        el => {
                            const style = window.getComputedStyle(el);
                            return {
                                border: style.border,
                                cursor: style.cursor,
                                draggable: el.draggable
                            };
                        }
                    """)
                    print(f"  First cell border: {border_style['border'][:50]}...")
                    print(f"  First cell cursor: {border_style['cursor']}")
                    print(f"  First cell draggable: {border_style['draggable']}")
                
                screenshot_path = screenshots_dir / "06_reshuffle_visual_indicators.png"
                page.screenshot(path=str(screenshot_path), full_page=True)
                print(f"✓ Screenshot saved: {screenshot_path}")
                
                # Stage 7: Perform drag and drop reordering
                if cell_count >= 2:
                    print("\n[Stage 7] Performing drag and drop reordering...")
                    print("  Dragging first cell to second cell position...")
                    
                    source_cell = media_cells.nth(0)
                    target_cell = media_cells.nth(1)
                    
                    # Get initial order
                    initial_order = page.evaluate("""
                        () => {
                            const cells = Array.from(document.querySelectorAll('.media-cell'));
                            return cells.map(cell => {
                                const img = cell.querySelector('img');
                                return img ? img.alt || img.src : 'no-image';
                            });
                        }
                    """)
                    print(f"  Initial order: {initial_order[:3]}")
                    
                    # Perform drag and drop
                    source_cell.drag_to(target_cell)
                    time.sleep(2)  # Wait for reorder to complete
                    
                    screenshot_path = screenshots_dir / "07_during_drag_drop.png"
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    print(f"✓ Screenshot saved: {screenshot_path}")
                    
                    # Stage 8: After drag and drop
                    print("\n[Stage 8] Checking order after drag and drop...")
                    time.sleep(1)
                    
                    final_order = page.evaluate("""
                        () => {
                            const cells = Array.from(document.querySelectorAll('.media-cell'));
                            return cells.map(cell => {
                                const img = cell.querySelector('img');
                                return img ? img.alt || img.src : 'no-image';
                            });
                        }
                    """)
                    print(f"  Final order: {final_order[:3]}")
                    
                    screenshot_path = screenshots_dir / "08_after_drag_drop.png"
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    print(f"✓ Screenshot saved: {screenshot_path}")
                    
                    # Stage 9: Disable reshuffle mode
                    print("\n[Stage 9] Disabling reshuffle mode...")
                    reshuffle_btn.click()
                    time.sleep(1.5)
                    
                    final_btn_text = reshuffle_btn.text_content()
                    print(f"  Button text after disable: {final_btn_text}")
                    
                    screenshot_path = screenshots_dir / "09_reshuffle_disabled.png"
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    print(f"✓ Screenshot saved: {screenshot_path}")
                    
                    # Stage 10: Final state
                    print("\n[Stage 10] Final state...")
                    time.sleep(1)
                    
                    screenshot_path = screenshots_dir / "10_final_state.png"
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    print(f"✓ Screenshot saved: {screenshot_path}")
                else:
                    print("⚠️  Not enough cells for drag and drop test (need at least 2)")
            else:
                print("⚠️  Reshuffle button not visible - cannot test reshuffle functionality")
                print("   This might be because no media is assigned to placeholders")
            
            # Test dialog reshuffle if possible
            print("\n[Stage 11] Testing dialog reshuffle (if available)...")
            media_cards = page.locator(".media-card")
            if media_cards.count() > 0:
                print(f"  Found {media_cards.count()} media cards")
                media_cards.first.click()
                time.sleep(1.5)
                
                dialog = page.locator(".placeholder-selection-dialog")
                if dialog.count() > 0 and dialog.is_visible():
                    print("  Dialog opened successfully")
                    
                    screenshot_path = screenshots_dir / "11_dialog_opened.png"
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    print(f"✓ Screenshot saved: {screenshot_path}")
                    
                    dialog_reshuffle_btn = dialog.locator("#dialogReshuffleBtn button")
                    if dialog_reshuffle_btn.count() > 0 and dialog_reshuffle_btn.is_visible():
                        print("  Dialog reshuffle button found and visible")
                        dialog_reshuffle_btn.click()
                        time.sleep(1)
                        
                        screenshot_path = screenshots_dir / "12_dialog_reshuffle_enabled.png"
                        page.screenshot(path=str(screenshot_path), full_page=True)
                        print(f"✓ Screenshot saved: {screenshot_path}")
                        
                        # Close dialog
                        cancel_btn = dialog.locator("#placeholderDialogCancelBtn")
                        if cancel_btn.count() > 0:
                            cancel_btn.click()
                            time.sleep(0.5)
                    else:
                        print("  Dialog reshuffle button not visible")
                else:
                    print("  Dialog did not open")
            else:
                print("  No media cards found to test dialog")
            
            print("\n" + "=" * 60)
            print("TEST COMPLETE!")
            print(f"All screenshots saved to: {screenshots_dir}")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            
            # Take error screenshot
            error_screenshot = screenshots_dir / "ERROR_screenshot.png"
            page.screenshot(path=str(error_screenshot), full_page=True)
            print(f"Error screenshot saved: {error_screenshot}")
        
        finally:
            # Keep browser open for a moment to see final state
            print("\nKeeping browser open for 3 seconds to view final state...")
            time.sleep(3)
            browser.close()

if __name__ == "__main__":
    test_reshuffle_with_screenshots()





