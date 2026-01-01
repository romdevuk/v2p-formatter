"""
Observation Report - Media Browser Visual Tests
Tests media browser functionality with detailed screenshots
"""
import pytest
import time
from pathlib import Path
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def screenshot_dir():
    """Create screenshots directory"""
    screenshots = Path("test_screenshots/observation_report_media_browser")
    screenshots.mkdir(parents=True, exist_ok=True)
    return screenshots


class TestMediaBrowserVisual:
    """Visual tests for Media Browser"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, screenshot_dir):
        """Navigate to observation report page"""
        self.page = page
        self.base_url = "http://localhost/v2p-formatter"
        self.screenshot_dir = screenshot_dir
        self.page.goto(f"{self.base_url}/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
    
    def test_01_media_browser_initial_state(self, page: Page):
        """Test 1: Media browser initial empty state"""
        print("\n=== Test: Media Browser Initial State ===")
        
        media_browser = page.locator("#mediaBrowser")
        expect(media_browser).to_be_visible(timeout=10000)
        
        # Screenshot of empty media browser
        page.screenshot(path=str(self.screenshot_dir / "01_media_browser_empty.png"), full_page=True)
        print("✅ Screenshot: 01_media_browser_empty.png")
        
        # Verify elements
        header = page.locator(".media-browser-header")
        count_display = page.locator(".media-count")
        
        if header.is_visible():
            print("✅ Media browser header visible")
        if count_display.is_visible():
            count_text = count_display.inner_text()
            print(f"✅ Media count display: '{count_text}'")
        
        print("✅ Test: Media Browser Initial State - COMPLETE")
    
    def test_02_media_browser_after_qualification_selection(self, page: Page):
        """Test 2: Media browser after selecting qualification"""
        print("\n=== Test: Media Browser After Qualification Selection ===")
        
        # Select qualification
        qual_select = page.locator("#qualificationSelect")
        expect(qual_select).to_be_visible(timeout=10000)
        
        options = qual_select.locator("option")
        option_count = options.count()
        print(f"✅ Found {option_count} qualification options")
        
        if option_count > 1:
            qual_select.select_option(index=1)
            time.sleep(2)
            
            page.screenshot(path=str(self.screenshot_dir / "02_media_browser_qualification_selected.png"), full_page=True)
            print("✅ Screenshot: 02_media_browser_qualification_selected.png")
            
            # Check if learner dropdown is enabled
            learner_select = page.locator("#learnerSelect")
            if learner_select.is_visible():
                is_disabled = learner_select.is_disabled()
                print(f"✅ Learner dropdown enabled: {not is_disabled}")
        
        print("✅ Test: Media Browser After Qualification Selection - COMPLETE")
    
    def test_03_media_browser_with_files(self, page: Page):
        """Test 3: Media browser with files loaded"""
        print("\n=== Test: Media Browser With Files ===")
        
        # Select qualification and learner
        qual_select = page.locator("#qualificationSelect")
        if qual_select.locator("option").count() > 1:
            qual_select.select_option(index=1)
            time.sleep(1)
            
            learner_select = page.locator("#learnerSelect")
            if learner_select.locator("option").count() > 1:
                learner_select.select_option(index=1)
                time.sleep(3)  # Wait for media to load
                
                # Screenshot of media browser with files
                page.screenshot(path=str(self.screenshot_dir / "03_media_browser_with_files.png"), full_page=True)
                print("✅ Screenshot: 03_media_browser_with_files.png")
                
                # Check media count
                count_display = page.locator(".media-count")
                if count_display.is_visible():
                    count_text = count_display.inner_text()
                    print(f"✅ Media count: {count_text}")
                
                # Check for media cards
                media_cards = page.locator(".media-card")
                card_count = media_cards.count()
                print(f"✅ Found {card_count} media cards")
                
                if card_count > 0:
                    # Screenshot focused on media browser
                    media_browser = page.locator("#mediaBrowser")
                    media_browser.screenshot(path=str(self.screenshot_dir / "03b_media_browser_closeup.png"))
                    print("✅ Screenshot: 03b_media_browser_closeup.png")
        
        print("✅ Test: Media Browser With Files - COMPLETE")
    
    def test_04_media_browser_subfolders(self, page: Page):
        """Test 4: Media browser subfolder display"""
        print("\n=== Test: Media Browser Subfolders ===")
        
        # Setup qualification and learner
        qual_select = page.locator("#qualificationSelect")
        if qual_select.locator("option").count() > 1:
            qual_select.select_option(index=1)
            time.sleep(1)
            
            learner_select = page.locator("#learnerSelect")
            if learner_select.locator("option").count() > 1:
                learner_select.select_option(index=1)
                time.sleep(3)
                
                # Check for folder headers
                folder_headers = page.locator(".media-folder-header")
                header_count = folder_headers.count()
                print(f"✅ Found {header_count} folder headers")
                
                if header_count > 0:
                    # List folders
                    for i in range(min(header_count, 5)):
                        header = folder_headers.nth(i)
                        if header.is_visible():
                            text = header.inner_text()
                            print(f"   Folder {i+1}: {text}")
                    
                    # Screenshot showing folders
                    page.screenshot(path=str(self.screenshot_dir / "04_media_browser_subfolders.png"), full_page=True)
                    print("✅ Screenshot: 04_media_browser_subfolders.png")
                    
                    # Closeup of folder structure
                    media_browser = page.locator("#mediaBrowser")
                    media_browser.screenshot(path=str(self.screenshot_dir / "04b_media_browser_folders_closeup.png"))
                    print("✅ Screenshot: 04b_media_browser_folders_closeup.png")
                else:
                    print("   ℹ️ No subfolders detected (flat structure)")
                    page.screenshot(path=str(self.screenshot_dir / "04_media_browser_no_subfolders.png"), full_page=True)
        
        print("✅ Test: Media Browser Subfolders - COMPLETE")
    
    def test_05_media_browser_media_cards(self, page: Page):
        """Test 5: Media browser card details"""
        print("\n=== Test: Media Browser Media Cards ===")
        
        # Setup
        qual_select = page.locator("#qualificationSelect")
        if qual_select.locator("option").count() > 1:
            qual_select.select_option(index=1)
            time.sleep(1)
            
            learner_select = page.locator("#learnerSelect")
            if learner_select.locator("option").count() > 1:
                learner_select.select_option(index=1)
                time.sleep(3)
                
                # Get media cards
                media_cards = page.locator(".media-card")
                card_count = media_cards.count()
                print(f"✅ Found {card_count} media cards")
                
                if card_count > 0:
                    # Inspect first few cards
                    for i in range(min(card_count, 5)):
                        card = media_cards.nth(i)
                        if card.is_visible():
                            # Check card elements
                            filename = card.locator(".media-filename")
                            type_indicator = card.locator(".media-type")
                            thumbnail = card.locator("img")
                            
                            if filename.is_visible():
                                name = filename.inner_text()
                                print(f"   Card {i+1}: {name}")
                            
                            if type_indicator.is_visible():
                                type_text = type_indicator.inner_text()
                                print(f"      Type: {type_text}")
                            
                            # Check if assigned
                            if "assigned" in card.get_attribute("class") or "":
                                print(f"      Status: Assigned")
                    
                    # Screenshot of cards
                    page.screenshot(path=str(self.screenshot_dir / "05_media_browser_cards.png"), full_page=True)
                    print("✅ Screenshot: 05_media_browser_cards.png")
                    
                    # Screenshot of first card closeup
                    if card_count > 0:
                        first_card = media_cards.first
                        first_card.screenshot(path=str(self.screenshot_dir / "05b_media_card_detail.png"))
                        print("✅ Screenshot: 05b_media_card_detail.png")
        
        print("✅ Test: Media Browser Media Cards - COMPLETE")
    
    def test_06_media_browser_assigned_state(self, page: Page):
        """Test 6: Media browser showing assigned state"""
        print("\n=== Test: Media Browser Assigned State ===")
        
        # Setup qualification and learner
        qual_select = page.locator("#qualificationSelect")
        if qual_select.locator("option").count() > 1:
            qual_select.select_option(index=1)
            time.sleep(1)
            
            learner_select = page.locator("#learnerSelect")
            if learner_select.locator("option").count() > 1:
                learner_select.select_option(index=1)
                time.sleep(2)
        
        # Add placeholder and assign media
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("{{TestPlaceholder}}")
            time.sleep(1)
        
        # Assign a few media items
        media_cards = page.locator(".media-card:not(.assigned)")
        drop_zones = page.locator(".drop-zone")
        
        assigned_count = 0
        if media_cards.count() > 0 and drop_zones.count() > 0:
            # Assign up to 3 items
            for i in range(min(3, media_cards.count())):
                card = media_cards.nth(i)
                if card.is_visible():
                    card.drag_to(drop_zones.first)
                    time.sleep(1)
                    assigned_count += 1
        
        print(f"✅ Assigned {assigned_count} media items")
        time.sleep(1)
        
        # Check assigned cards
        assigned_cards = page.locator(".media-card.assigned")
        assigned_count_actual = assigned_cards.count()
        print(f"✅ Found {assigned_count_actual} assigned cards")
        
        # Screenshot showing assigned state
        page.screenshot(path=str(self.screenshot_dir / "06_media_browser_assigned_state.png"), full_page=True)
        print("✅ Screenshot: 06_media_browser_assigned_state.png")
        
        # Closeup of assigned cards
        media_browser = page.locator("#mediaBrowser")
        media_browser.screenshot(path=str(self.screenshot_dir / "06b_media_browser_assigned_closeup.png"))
        print("✅ Screenshot: 06b_media_browser_assigned_closeup.png")
        
        print("✅ Test: Media Browser Assigned State - COMPLETE")
    
    def test_07_media_browser_grid_layout(self, page: Page):
        """Test 7: Media browser grid layout"""
        print("\n=== Test: Media Browser Grid Layout ===")
        
        # Setup
        qual_select = page.locator("#qualificationSelect")
        if qual_select.locator("option").count() > 1:
            qual_select.select_option(index=1)
            time.sleep(1)
            
            learner_select = page.locator("#learnerSelect")
            if learner_select.locator("option").count() > 1:
                learner_select.select_option(index=1)
                time.sleep(3)
                
                # Check grid layout
                media_grid = page.locator(".media-grid")
                if media_grid.is_visible():
                    # Get computed styles
                    display = media_grid.evaluate("el => window.getComputedStyle(el).display")
                    grid_template = media_grid.evaluate("el => window.getComputedStyle(el).gridTemplateColumns")
                    
                    print(f"✅ Grid display: {display}")
                    print(f"✅ Grid template: {grid_template}")
                    
                    # Screenshot of grid
                    media_grid.screenshot(path=str(self.screenshot_dir / "07_media_grid_layout.png"))
                    print("✅ Screenshot: 07_media_grid_layout.png")
                
                # Full page screenshot
                page.screenshot(path=str(self.screenshot_dir / "07b_media_browser_full_layout.png"), full_page=True)
                print("✅ Screenshot: 07b_media_browser_full_layout.png")
        
        print("✅ Test: Media Browser Grid Layout - COMPLETE")
    
    def test_08_media_browser_scrolling(self, page: Page):
        """Test 8: Media browser scrolling behavior"""
        print("\n=== Test: Media Browser Scrolling ===")
        
        # Setup
        qual_select = page.locator("#qualificationSelect")
        if qual_select.locator("option").count() > 1:
            qual_select.select_option(index=1)
            time.sleep(1)
            
            learner_select = page.locator("#learnerSelect")
            if learner_select.locator("option").count() > 1:
                learner_select.select_option(index=1)
                time.sleep(3)
                
                media_browser = page.locator("#mediaBrowser")
                
                # Screenshot at top
                media_browser.screenshot(path=str(self.screenshot_dir / "08a_media_browser_top.png"))
                print("✅ Screenshot: 08a_media_browser_top.png")
                
                # Scroll down
                media_browser.evaluate("el => el.scrollTop = el.scrollHeight / 2")
                time.sleep(0.5)
                
                # Screenshot at middle
                media_browser.screenshot(path=str(self.screenshot_dir / "08b_media_browser_middle.png"))
                print("✅ Screenshot: 08b_media_browser_middle.png")
                
                # Scroll to bottom
                media_browser.evaluate("el => el.scrollTop = el.scrollHeight")
                time.sleep(0.5)
                
                # Screenshot at bottom
                media_browser.screenshot(path=str(self.screenshot_dir / "08c_media_browser_bottom.png"))
                print("✅ Screenshot: 08c_media_browser_bottom.png")
        
        print("✅ Test: Media Browser Scrolling - COMPLETE")



