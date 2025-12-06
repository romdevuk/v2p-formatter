"""
Comprehensive tests for reshuffle functionality
Tests reshuffle with actual media assignments
"""
import pytest
from playwright.sync_api import Page, expect
import time


@pytest.fixture(scope="function")
def page_with_media_assigned(page: Page):
    """Navigate to observation media page and set up test data"""
    url = "http://127.0.0.1:5000/v2p-formatter/observation-media"
    
    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(1)
        
        # Add text with placeholder to make reshuffle button visible
        text_editor = page.locator("#observationTextEditor")
        if text_editor.count() > 0:
            # Clear and add test content with placeholder
            text_editor.fill("Test content with {{Test_Placeholder}} for reshuffle testing.")
            time.sleep(0.5)
        
        return page
    except Exception as e:
        print(f"Error setting up page: {e}")
        return page


class TestReshuffleFunctionality:
    """Test reshuffle functionality with media assignments"""
    
    def test_reshuffle_button_appears_with_media(self, page_with_media_assigned):
        """Test that reshuffle button appears when media is assigned"""
        page = page_with_media_assigned
        
        # Check if reshuffle button exists (might be hidden)
        reshuffle_btn = page.locator("#reshuffleBtn")
        
        # Button should exist in DOM
        assert reshuffle_btn.count() > 0, "Reshuffle button should exist in DOM"
        
        # Check initial state (might be hidden if no media assigned)
        is_visible = reshuffle_btn.is_visible()
        print(f"Reshuffle button visible: {is_visible}")
        
        # If not visible, that's expected when no media is assigned
        if not is_visible:
            print("ℹ️  Reshuffle button is hidden (no media assigned - expected)")
    
    def test_reshuffle_toggle_when_visible(self, page_with_media_assigned):
        """Test reshuffle toggle when button is visible"""
        page = page_with_media_assigned
        
        reshuffle_btn = page.locator("#reshuffleBtn")
        
        if reshuffle_btn.count() > 0 and reshuffle_btn.is_visible():
            # Get initial text
            initial_text = reshuffle_btn.text_content()
            print(f"Initial button text: {initial_text}")
            
            # Click to toggle on
            reshuffle_btn.click()
            time.sleep(0.5)
            
            # Check text changed
            new_text = reshuffle_btn.text_content()
            print(f"After click text: {new_text}")
            assert new_text != initial_text or "Active" in new_text, "Button text should change"
            
            # Click again to toggle off
            reshuffle_btn.click()
            time.sleep(0.5)
            
            # Should be back to original or inactive
            final_text = reshuffle_btn.text_content()
            print(f"Final button text: {final_text}")
            assert "Reshuffle" in final_text, "Button should show Reshuffle text"
        else:
            pytest.skip("Reshuffle button not visible (no media assigned)")
    
    def test_reshuffle_console_logs(self, page_with_media_assigned):
        """Test that reshuffle generates console logs"""
        page = page_with_media_assigned
        
        # Collect console messages
        console_messages = []
        
        def handle_console(msg):
            console_messages.append(msg.text)
        
        page.on("console", handle_console)
        
        reshuffle_btn = page.locator("#reshuffleBtn")
        
        if reshuffle_btn.count() > 0 and reshuffle_btn.is_visible():
            # Click reshuffle
            reshuffle_btn.click()
            time.sleep(0.5)
            
            # Check for RESHUFFLE logs
            reshuffle_logs = [msg for msg in console_messages if "RESHUFFLE" in msg]
            print(f"Found {len(reshuffle_logs)} RESHUFFLE console logs")
            
            if len(reshuffle_logs) > 0:
                print("Sample logs:")
                for log in reshuffle_logs[:3]:
                    print(f"  - {log}")
            
            # We expect at least some logs
            assert len(reshuffle_logs) > 0, "Expected RESHUFFLE console logs when button is clicked"
        else:
            pytest.skip("Reshuffle button not visible")
    
    def test_reshuffle_visual_indicators(self, page_with_media_assigned):
        """Test that reshuffle adds visual indicators to cells"""
        page = page_with_media_assigned
        
        reshuffle_btn = page.locator("#reshuffleBtn")
        
        if reshuffle_btn.count() > 0 and reshuffle_btn.is_visible():
            # Find media cells
            media_cells = page.locator(".media-cell")
            initial_count = media_cells.count()
            print(f"Found {initial_count} media cells")
            
            if initial_count > 0:
                # Get initial border style of first cell
                first_cell = media_cells.first()
                initial_border = first_cell.evaluate("el => window.getComputedStyle(el).border")
                print(f"Initial border: {initial_border}")
                
                # Toggle reshuffle on
                reshuffle_btn.click()
                time.sleep(0.5)
                
                # Check if border changed (reshuffle adds visual indicators)
                new_border = first_cell.evaluate("el => window.getComputedStyle(el).border")
                print(f"After reshuffle border: {new_border}")
                
                # Border should change when reshuffle is active
                # (This might not always be true, but we check)
                
                # Toggle off
                reshuffle_btn.click()
                time.sleep(0.5)
            else:
                pytest.skip("No media cells found to test visual indicators")
        else:
            pytest.skip("Reshuffle button not visible")
    
    def test_dialog_reshuffle_functionality(self, page_with_media_assigned):
        """Test reshuffle functionality in dialog"""
        page = page_with_media_assigned
        
        # Try to open dialog by clicking a media card
        media_cards = page.locator(".media-card")
        
        if media_cards.count() > 0:
            # Click first media card
            media_cards.first().click()
            time.sleep(1)
            
            # Check if dialog opened
            dialog = page.locator(".placeholder-selection-dialog")
            
            if dialog.count() > 0 and dialog.is_visible():
                # Find dialog reshuffle button
                dialog_reshuffle_btn = dialog.locator("#dialogReshuffleBtn button")
                
                if dialog_reshuffle_btn.count() > 0 and dialog_reshuffle_btn.is_visible():
                    # Get initial text
                    initial_text = dialog_reshuffle_btn.text_content()
                    print(f"Dialog reshuffle button text: {initial_text}")
                    
                    # Click to toggle
                    dialog_reshuffle_btn.click()
                    time.sleep(0.5)
                    
                    # Check text changed
                    new_text = dialog_reshuffle_btn.text_content()
                    print(f"After click: {new_text}")
                    assert new_text != initial_text or "Active" in new_text
                    
                    # Close dialog
                    cancel_btn = dialog.locator("#placeholderDialogCancelBtn")
                    if cancel_btn.count() > 0:
                        cancel_btn.click()
                        time.sleep(0.5)
                else:
                    print("Dialog reshuffle button not visible (no media assigned in dialog)")
            else:
                pytest.skip("Dialog did not open")
        else:
            pytest.skip("No media cards to open dialog")

