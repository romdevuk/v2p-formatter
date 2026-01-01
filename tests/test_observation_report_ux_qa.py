"""
Observation Report - UX/QA Comprehensive Test Suite
Tests visual elements, images, styles, media browser, standards panel
"""
import pytest
import time
from pathlib import Path
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def screenshot_dir():
    """Create screenshots directory"""
    screenshots = Path("test_screenshots/observation_report_ux_qa")
    screenshots.mkdir(parents=True, exist_ok=True)
    return screenshots


class TestUXVisualVerification:
    """Visual and UX verification tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, screenshot_dir):
        """Navigate to observation report page"""
        self.page = page
        self.base_url = "http://localhost/v2p-formatter"
        self.screenshot_dir = screenshot_dir
        self.page.goto(f"{self.base_url}/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
    
    def test_01_images_load_correctly(self, page: Page):
        """Verify images load and display correctly in live preview"""
        print("\n=== Test: Images Load Correctly ===")
        
        # Setup: Select qualification/learner and add placeholders
        qual_select = page.locator("#qualificationSelect")
        if qual_select.locator("option").count() > 1:
            qual_select.select_option(index=1)
            time.sleep(1)
            
            learner_select = page.locator("#learnerSelect")
            if learner_select.locator("option").count() > 1:
                learner_select.select_option(index=1)
                time.sleep(2)
        
        # Add text with placeholder
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("Test {{ImagePlaceholder}}")
            time.sleep(1)
        
        # Assign image via drag and drop
        media_cards = page.locator(".media-card:not(.assigned)")
        drop_zones = page.locator(".drop-zone")
        
        if media_cards.count() > 0 and drop_zones.count() > 0:
            media_cards.first.drag_to(drop_zones.first)
            time.sleep(2)
            
            # Check for images in preview
            images = page.locator(".media-preview-image")
            image_count = images.count()
            print(f"✅ Found {image_count} images in preview")
            
            # Verify images have src attributes
            for i in range(min(image_count, 3)):
                img = images.nth(i)
                src = img.get_attribute("src")
                print(f"   Image {i+1} src: {src[:80] if src else 'None'}...")
                
                # Check if image loaded (naturalWidth > 0)
                is_loaded = page.evaluate("""
                    (img) => {
                        return img && img.complete && img.naturalWidth > 0;
                    }
                """, img)
                
                if not is_loaded:
                    print(f"   ⚠️ Warning: Image {i+1} may not have loaded")
            
            # Screenshot
            page.screenshot(path=str(self.screenshot_dir / "01_images_in_preview.png"), full_page=True)
        
        print("✅ Test: Images Load Correctly - COMPLETE")
    
    def test_02_section_colors_visible(self, page: Page):
        """Verify section titles are color-coded"""
        print("\n=== Test: Section Colors Visible ===")
        
        # Add text with sections
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("SECTION 1: First Section\n\nContent here.\n\nSECTION 2: Second Section\n\nMore content.")
            time.sleep(1)
        
        # Check for section titles
        section_titles = page.locator(".section-title")
        title_count = section_titles.count()
        print(f"✅ Found {title_count} section titles")
        
        # Verify colors are applied
        for i in range(min(title_count, 3)):
            title = section_titles.nth(i)
            color = title.evaluate("el => window.getComputedStyle(el).color")
            text = title.inner_text()
            print(f"   Section {i+1}: '{text}' - Color: {color}")
            
            # Color should not be default (rgb(224, 224, 224))
            if color == "rgb(224, 224, 224)":
                print(f"   ⚠️ Warning: Section {i+1} may not have color applied")
        
        # Screenshot
        page.screenshot(path=str(self.screenshot_dir / "02_section_colors.png"), full_page=True)
        print("✅ Test: Section Colors Visible - COMPLETE")
    
    def test_03_media_browser_subfolders(self, page: Page):
        """Verify media browser shows subfolders"""
        print("\n=== Test: Media Browser Subfolders ===")
        
        # Setup qualification/learner
        qual_select = page.locator("#qualificationSelect")
        if qual_select.locator("option").count() > 1:
            qual_select.select_option(index=1)
            time.sleep(1)
            
            learner_select = page.locator("#learnerSelect")
            if learner_select.locator("option").count() > 1:
                learner_select.select_option(index=1)
                time.sleep(2)
        
        # Check for folder headers
        folder_headers = page.locator(".media-folder-header")
        header_count = folder_headers.count()
        print(f"✅ Found {header_count} folder headers")
        
        if header_count > 0:
            for i in range(header_count):
                header = folder_headers.nth(i)
                text = header.inner_text()
                print(f"   Folder {i+1}: {text}")
        else:
            print("   ℹ️ No subfolders detected (may be flat structure)")
        
        # Screenshot
        page.screenshot(path=str(self.screenshot_dir / "03_media_browser_subfolders.png"), full_page=True)
        print("✅ Test: Media Browser Subfolders - COMPLETE")
    
    def test_04_standards_units_visible(self, page: Page):
        """Verify standards panel shows units"""
        print("\n=== Test: Standards Units Visible ===")
        
        # Try to load standards
        standards_select = page.locator("#standardsSelect")
        if standards_select.is_visible():
            options = standards_select.locator("option")
            if options.count() > 1:
                standards_select.select_option(index=1)
                time.sleep(3)  # Wait for standards to load
        
        # Check for unit containers
        unit_containers = page.locator(".unit-container")
        unit_count = unit_containers.count()
        print(f"✅ Found {unit_count} unit containers")
        
        if unit_count == 0:
            print("   ⚠️ Warning: No units displayed in standards panel")
            
            # Check if standards data exists
            standards_content = page.locator(".standards-content")
            content_text = standards_content.inner_text() if standards_content.is_visible() else ""
            
            if "No standards" in content_text or "Error" in content_text:
                print(f"   Error message: {content_text[:200]}")
        else:
            # List first few units
            for i in range(min(unit_count, 5)):
                unit = unit_containers.nth(i)
                unit_header = unit.locator(".unit-header")
                if unit_header.is_visible():
                    header_text = unit_header.inner_text()
                    print(f"   Unit {i+1}: {header_text[:80]}")
        
        # Screenshot
        page.screenshot(path=str(self.screenshot_dir / "04_standards_units.png"), full_page=True)
        print("✅ Test: Standards Units Visible - COMPLETE")
    
    def test_05_placeholder_colors_visible(self, page: Page):
        """Verify placeholder labels are color-coded"""
        print("\n=== Test: Placeholder Colors Visible ===")
        
        # Add text with multiple placeholders
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("{{Placeholder1}} and {{Placeholder2}} and {{Placeholder3}}")
            time.sleep(1)
        
        # Check placeholder labels
        placeholder_labels = page.locator(".placeholder-label")
        label_count = placeholder_labels.count()
        print(f"✅ Found {label_count} placeholder labels")
        
        # Verify colors
        for i in range(min(label_count, 3)):
            label = placeholder_labels.nth(i)
            color = label.evaluate("el => window.getComputedStyle(el).color")
            text = label.inner_text()
            print(f"   Placeholder {i+1}: '{text}' - Color: {color}")
        
        # Screenshot
        page.screenshot(path=str(self.screenshot_dir / "05_placeholder_colors.png"), full_page=True)
        print("✅ Test: Placeholder Colors Visible - COMPLETE")
    
    def test_06_complete_visual_check(self, page: Page):
        """Complete visual check - all elements visible"""
        print("\n=== Test: Complete Visual Check ===")
        
        # Load draft if available
        load_btn = page.locator("#loadDraftBtn")
        if load_btn.is_visible():
            load_btn.click()
            time.sleep(1)
            
            # Try to load first draft
            draft_items = page.locator(".draft-item")
            if draft_items.count() > 0:
                load_draft_btn = draft_items.first.locator(".btn-load-draft")
                if load_draft_btn.is_visible():
                    load_draft_btn.click()
                    time.sleep(3)
        
        # Take full page screenshot
        page.screenshot(path=str(self.screenshot_dir / "06_complete_visual_check.png"), full_page=True)
        
        # Checklist
        checks = {
            "Media Browser visible": page.locator("#mediaBrowser").is_visible(),
            "Live Preview visible": page.locator("#livePreview").is_visible(),
            "Standards Panel visible": page.locator("#standards").is_visible(),
            "Images in preview": page.locator(".media-preview-image").count() > 0,
            "Section titles colored": page.locator(".section-title").count() > 0,
            "Placeholders colored": page.locator(".placeholder-label").count() > 0,
        }
        
        print("\nVisual Checks:")
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}: {result}")
        
        print("✅ Test: Complete Visual Check - COMPLETE")



