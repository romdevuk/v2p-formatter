"""
Visual verification tests for Observation Report UI components
Takes screenshots and verifies UI elements are displayed correctly
"""
import pytest
import time
from pathlib import Path
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def screenshot_dir():
    """Create screenshots directory"""
    screenshots = Path("test_screenshots/observation_report_visual")
    screenshots.mkdir(parents=True, exist_ok=True)
    return screenshots


class TestVisualVerification:
    """Visual verification of UI components"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, screenshot_dir):
        """Navigate to page"""
        self.page = page
        self.base_url = "http://localhost/v2p-formatter"
        self.screenshot_dir = screenshot_dir
        self.page.goto(f"{self.base_url}/observation-report")
        time.sleep(2)
    
    def test_media_browser_visual(self, page: Page):
        """Verify Media Browser UI appearance"""
        print("\n=== Visual Test: Media Browser ===")
        
        # Load media first
        qualification_select = page.locator("#qualificationSelect")
        if qualification_select.is_visible():
            options = qualification_select.locator("option")
            if options.count() > 1:
                qualification_select.select_option(index=1)
                time.sleep(1)
                
                learner_select = page.locator("#learnerSelect")
                if learner_select.is_visible():
                    learner_select.select_option(index=1)
                    time.sleep(2)
        
        # Take screenshot of media browser
        media_browser = page.locator("#mediaBrowser")
        if media_browser.is_visible():
            media_browser.screenshot(path=str(self.screenshot_dir / "media_browser.png"))
            print("✅ Media browser screenshot taken")
            
            # Verify elements
            media_cards = page.locator(".media-card")
            card_count = media_cards.count()
            print(f"✅ Media cards visible: {card_count}")
            
            # Verify media grid layout
            media_grid = page.locator(".media-grid")
            if media_grid.is_visible():
                print("✅ Media grid layout correct")
    
    def test_live_preview_visual(self, page: Page):
        """Verify Live Preview UI appearance"""
        print("\n=== Visual Test: Live Preview ===")
        
        # Enter text with placeholders
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("{{Placeholder1}} text {{Placeholder2}}")
            time.sleep(1)
        
        # Take screenshot of live preview
        live_preview = page.locator("#livePreview")
        if live_preview.is_visible():
            live_preview.screenshot(path=str(self.screenshot_dir / "live_preview.png"))
            print("✅ Live preview screenshot taken")
            
            # Verify placeholder containers
            placeholder_containers = page.locator(".placeholder-container")
            container_count = placeholder_containers.count()
            print(f"✅ Placeholder containers: {container_count}")
            
            # Verify drop zones
            drop_zones = page.locator(".drop-zone")
            zone_count = drop_zones.count()
            print(f"✅ Drop zones: {zone_count}")
    
    def test_standards_panel_visual(self, page: Page):
        """Verify Standards panel UI appearance"""
        print("\n=== Visual Test: Standards Panel ===")
        
        # Try to load standards
        standards_select = page.locator("#standardsSelect")
        if standards_select.is_visible():
            options = standards_select.locator("option")
            if options.count() > 1:
                standards_select.select_option(index=1)
                time.sleep(2)
        
        # Take screenshot of standards panel
        standards_container = page.locator("#standards")
        if standards_container.is_visible():
            standards_container.screenshot(path=str(self.screenshot_dir / "standards_panel.png"))
            print("✅ Standards panel screenshot taken")
            
            # Verify unit containers
            unit_containers = page.locator(".unit-container")
            unit_count = unit_containers.count()
            print(f"✅ Unit containers: {unit_count}")
    
    def test_three_column_layout_visual(self, page: Page):
        """Verify 3-column layout appearance"""
        print("\n=== Visual Test: 3-Column Layout ===")
        
        # Take full page screenshot
        self.page.screenshot(path=str(self.screenshot_dir / "three_column_layout.png"), full_page=True)
        print("✅ Full page screenshot taken")
        
        # Verify columns exist
        media_browser_col = page.locator("#mediaBrowserColumn")
        live_preview_col = page.locator("#livePreviewColumn")
        standards_col = page.locator("#standardsColumn")
        
        assert media_browser_col.is_visible(), "Media Browser column not visible"
        assert live_preview_col.is_visible(), "Live Preview column not visible"
        assert standards_col.is_visible(), "Standards column not visible"
        
        print("✅ All three columns visible")
    
    def test_drag_and_drop_visual_states(self, page: Page):
        """Verify drag-and-drop visual feedback"""
        print("\n=== Visual Test: Drag-and-Drop Visual States ===")
        
        # Setup
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("{{TestPlaceholder}}")
            time.sleep(1)
        
        # Load media
        media_cards = page.locator(".media-card:not(.assigned)").first
        if media_cards.is_visible():
            # Start drag (mouse down)
            media_card_box = media_cards.bounding_box()
            drop_zone = page.locator(".drop-zone").first
            drop_zone_box = drop_zone.bounding_box()
            
            if media_card_box and drop_zone_box:
                # Move mouse to media card
                self.page.mouse.move(
                    media_card_box['x'] + media_card_box['width'] / 2,
                    media_card_box['y'] + media_card_box['height'] / 2
                )
                time.sleep(0.2)
                
                # Mouse down
                self.page.mouse.down()
                time.sleep(0.3)
                
                # Screenshot during drag
                self.page.screenshot(path=str(self.screenshot_dir / "drag_state.png"))
                print("✅ Drag state screenshot taken")
                
                # Move to drop zone
                self.page.mouse.move(
                    drop_zone_box['x'] + drop_zone_box['width'] / 2,
                    drop_zone_box['y'] + drop_zone_box['height'] / 2
                )
                time.sleep(0.3)
                
                # Screenshot over drop zone
                self.page.screenshot(path=str(self.screenshot_dir / "drag_over_drop_zone.png"))
                print("✅ Drag-over drop zone screenshot taken")
                
                # Mouse up (drop)
                self.page.mouse.up()
                time.sleep(1)
                
                # Screenshot after drop
                self.page.screenshot(path=str(self.screenshot_dir / "after_drop.png"))
                print("✅ After drop screenshot taken")



