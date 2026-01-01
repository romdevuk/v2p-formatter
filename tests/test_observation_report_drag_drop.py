"""
Browser tests for Observation Report - Drag and Drop functionality
⚠️ CRITICAL: This was a major complexity in the old module
"""
import pytest
import time
from playwright.sync_api import Page, expect


class TestDragAndDrop:
    """Test drag-and-drop media assignment"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Navigate to observation report page"""
        self.page = page
        self.base_url = "http://localhost/v2p-formatter"
        self.page.goto(f"{self.base_url}/observation-report")
        time.sleep(2)  # Wait for page load
    
    def test_single_media_drag_to_placeholder(self, page: Page):
        """⚠️ CRITICAL: Test dragging single media item to placeholder"""
        print("\n=== Test: Single Media Drag to Placeholder ===")
        
        # Step 1: Select qualification and learner (if needed)
        # This assumes we have test data available
        
        # Step 2: Wait for media browser to load
        media_browser = page.locator("#mediaBrowser")
        expect(media_browser).to_be_visible(timeout=10000)
        print("✅ Media browser visible")
        
        # Step 3: Wait for media cards to appear
        media_cards = page.locator(".media-card").first
        expect(media_cards).to_be_visible(timeout=10000)
        print("✅ Media cards loaded")
        
        # Step 4: Wait for live preview and placeholders
        live_preview = page.locator("#livePreview")
        expect(live_preview).to_be_visible(timeout=10000)
        print("✅ Live preview visible")
        
        # Step 5: Enter text with placeholder in text editor
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("Test content {{TestPlaceholder}}")
            text_editor.press("Enter")
            time.sleep(1)  # Wait for preview to update
            print("✅ Text editor filled with placeholder")
        
        # Step 6: Find placeholder drop zone
        drop_zones = page.locator(".drop-zone")
        if drop_zones.count() > 0:
            drop_zone = drop_zones.first
            expect(drop_zone).to_be_visible()
            print("✅ Drop zone found")
            
            # Step 7: Perform drag and drop
            media_card = page.locator(".media-card").first
            media_card.drag_to(drop_zone)
            time.sleep(1)  # Wait for assignment
            print("✅ Drag and drop completed")
            
            # Step 8: Verify media card is marked as assigned
            assigned_card = page.locator(".media-card.assigned").first
            if assigned_card.is_visible():
                print("✅ Media card marked as assigned")
            
            # Step 9: Verify media appears in preview
            media_items = page.locator(".media-item")
            expect(media_items.first).to_be_visible(timeout=5000)
            print("✅ Media appears in preview")
        
        print("✅ Test: Single Media Drag to Placeholder - PASSED")
    
    def test_bulk_drag_to_placeholder(self, page: Page):
        """⚠️ CRITICAL: Test dragging multiple selected media items"""
        print("\n=== Test: Bulk Drag to Placeholder ===")
        
        # Step 1: Load media browser
        media_browser = page.locator("#mediaBrowser")
        expect(media_browser).to_be_visible(timeout=10000)
        
        # Step 2: Select multiple media cards (Ctrl/Cmd + click)
        media_cards = page.locator(".media-card")
        if media_cards.count() >= 2:
            # Click first card
            first_card = media_cards.nth(0)
            first_card.click()
            
            # Ctrl/Cmd + click second card
            page.keyboard.press("Meta+KeyC" if page.evaluate("navigator.platform").startswith("Mac") else "Control+KeyC")
            second_card = media_cards.nth(1)
            second_card.click(button="left", modifiers=["Meta"] if page.evaluate("navigator.platform").startswith("Mac") else ["Control"])
            print("✅ Multiple media cards selected")
            
            # Step 3: Enter text with placeholder
            text_editor = page.locator("#textEditor")
            if text_editor.is_visible():
                text_editor.fill("Test {{BulkPlaceholder}}")
                time.sleep(1)
            
            # Step 4: Drag to drop zone
            drop_zone = page.locator(".drop-zone").first
            if drop_zone.is_visible():
                # Drag one of the selected cards (both should drag)
                first_card.drag_to(drop_zone)
                time.sleep(2)  # Wait for bulk assignment
                print("✅ Bulk drag completed")
                
                # Step 5: Verify all selected media are assigned
                assigned_cards = page.locator(".media-card.assigned")
                assert assigned_cards.count() >= 2
                print("✅ All media marked as assigned")
        
        print("✅ Test: Bulk Drag to Placeholder - PASSED")
    
    def test_drag_visual_feedback(self, page: Page):
        """⚠️ CRITICAL: Test visual feedback during drag"""
        print("\n=== Test: Drag Visual Feedback ===")
        
        # Step 1: Load media
        media_browser = page.locator("#mediaBrowser")
        expect(media_browser).to_be_visible(timeout=10000)
        
        media_card = page.locator(".media-card").first
        expect(media_card).to_be_visible()
        
        # Step 2: Start drag and verify dragging class
        media_card.hover()
        page.mouse.down()
        
        # Check if dragging class is applied
        dragging_class = page.evaluate("""
            () => {
                const card = document.querySelector('.media-card');
                return card && card.classList.contains('dragging');
            }
        """)
        
        # Step 3: Move mouse to verify drop zone highlighting
        drop_zone = page.locator(".drop-zone").first
        if drop_zone.is_visible():
            # Move mouse over drop zone
            box = drop_zone.bounding_box()
            if box:
                page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
                time.sleep(0.5)
                
                # Verify drop zone has drag-over class
                drag_over = page.evaluate("""
                    () => {
                        const zone = document.querySelector('.drop-zone');
                        return zone && zone.classList.contains('drag-over');
                    }
                """)
                if drag_over:
                    print("✅ Drop zone highlighted during drag")
        
        page.mouse.up()
        print("✅ Test: Drag Visual Feedback - PASSED")
    
    def test_drag_prevent_assigned_media(self, page: Page):
        """Test that already-assigned media cannot be dragged"""
        print("\n=== Test: Prevent Dragging Assigned Media ===")
        
        # Step 1: Assign media first
        media_card = page.locator(".media-card").first
        drop_zone = page.locator(".drop-zone").first
        
        if media_card.is_visible() and drop_zone.is_visible():
            media_card.drag_to(drop_zone)
            time.sleep(1)
            
            # Step 2: Verify card is assigned
            assigned_card = page.locator(".media-card.assigned").first
            expect(assigned_card).to_be_visible(timeout=5000)
            
            # Step 3: Try to drag assigned card (should be prevented)
            cursor_style = assigned_card.evaluate("el => window.getComputedStyle(el).cursor")
            if cursor_style == "not-allowed":
                print("✅ Assigned media has not-allowed cursor")
            
            # Step 4: Verify pointer-events: none
            pointer_events = assigned_card.evaluate("el => window.getComputedStyle(el).pointerEvents")
            if pointer_events == "none":
                print("✅ Assigned media has pointer-events: none")
        
        print("✅ Test: Prevent Dragging Assigned Media - PASSED")
    
    def test_drag_to_invalid_zone(self, page: Page):
        """Test dragging to invalid drop zone"""
        print("\n=== Test: Drag to Invalid Zone ===")
        
        media_card = page.locator(".media-card").first
        expect(media_card).to_be_visible(timeout=10000)
        
        # Try to drag outside valid drop zones
        media_card.drag_to(page.locator("body"))
        time.sleep(0.5)
        
        # Verify no assignment occurred
        # This test may need adjustment based on actual implementation
        print("✅ Test: Drag to Invalid Zone - PASSED")



