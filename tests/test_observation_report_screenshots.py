"""
Observation Report - Screenshot tests using Playwright
Uses existing conftest.py fixtures
"""
import pytest
import time
from pathlib import Path
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def screenshot_dir():
    """Create screenshots directory"""
    screenshots = Path("test_screenshots/observation_report_workflows")
    screenshots.mkdir(parents=True, exist_ok=True)
    return screenshots


class TestObservationReportScreenshots:
    """Generate screenshots for Observation Report UI"""
    
    def test_01_initial_load(self, page: Page, screenshot_dir):
        """1. Initial page load"""
        page.goto("http://localhost/v2p-formatter/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        page.screenshot(path=str(screenshot_dir / "01_initial_load.png"), full_page=True)
        print(f"✅ Screenshot: 01_initial_load.png")
    
    def test_02_qualification_dropdown(self, page: Page, screenshot_dir):
        """2. Qualification dropdown"""
        page.goto("http://localhost/v2p-formatter/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        qual_select = page.locator("#qualificationSelect")
        expect(qual_select).to_be_visible(timeout=10000)
        page.screenshot(path=str(screenshot_dir / "02_qualification_dropdown.png"), full_page=True)
        print(f"✅ Screenshot: 02_qualification_dropdown.png")
    
    def test_03_select_qualification(self, page: Page, screenshot_dir):
        """3. After selecting qualification"""
        page.goto("http://localhost/v2p-formatter/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        qual_select = page.locator("#qualificationSelect")
        options = qual_select.locator("option")
        
        if options.count() > 1:
            qual_select.select_option(index=1)
            time.sleep(2)
            page.screenshot(path=str(screenshot_dir / "03_qualification_selected.png"), full_page=True)
            print(f"✅ Screenshot: 03_qualification_selected.png")
    
    def test_04_select_learner(self, page: Page, screenshot_dir):
        """4. After selecting learner and media loads"""
        page.goto("http://localhost/v2p-formatter/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # Select qualification
        qual_select = page.locator("#qualificationSelect")
        if qual_select.locator("option").count() > 1:
            qual_select.select_option(index=1)
            time.sleep(2)
            
            # Select learner
            learner_select = page.locator("#learnerSelect")
            if learner_select.locator("option").count() > 1:
                learner_select.select_option(index=1)
                time.sleep(3)  # Wait for media to load
                page.screenshot(path=str(screenshot_dir / "04_learner_selected_media_loaded.png"), full_page=True)
                print(f"✅ Screenshot: 04_learner_selected_media_loaded.png")
    
    def test_05_media_browser(self, page: Page, screenshot_dir):
        """5. Media browser loaded"""
        page.goto("http://localhost/v2p-formatter/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # Setup qualification and learner
        qual_select = page.locator("#qualificationSelect")
        if qual_select.locator("option").count() > 1:
            qual_select.select_option(index=1)
            time.sleep(1)
            
            learner_select = page.locator("#learnerSelect")
            if learner_select.locator("option").count() > 1:
                learner_select.select_option(index=1)
                time.sleep(3)
                
                # Take screenshot of media browser
                media_browser = page.locator("#mediaBrowser")
                if media_browser.is_visible():
                    page.screenshot(path=str(screenshot_dir / "05_media_browser.png"), full_page=True)
                    print(f"✅ Screenshot: 05_media_browser.png")
    
    def test_06_text_with_placeholders(self, page: Page, screenshot_dir):
        """6. Text editor with placeholders"""
        page.goto("http://localhost/v2p-formatter/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # Expand text editor section if needed
        text_section = page.locator('[data-section="textEditor"]')
        if text_section.is_visible():
            section_header = text_section.locator(".section-header")
            if section_header.is_visible():
                section_header.click()
                time.sleep(0.5)
        
        # Enter text with placeholders
        text_editor = page.locator("#textEditor")
        text_editor.fill("SECTION 1: Site Arrival\n\n{{Site_Arrival_Induction}}\n\nThe site arrival process was conducted properly.\n\n{{Safety_Briefing}}\n\nSafety procedures were explained clearly.")
        time.sleep(1)
        
        page.screenshot(path=str(screenshot_dir / "06_text_with_placeholders.png"), full_page=True)
        print(f"✅ Screenshot: 06_text_with_placeholders.png")
    
    def test_07_live_preview_placeholders(self, page: Page, screenshot_dir):
        """7. Live preview showing placeholders"""
        page.goto("http://localhost/v2p-formatter/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # Expand text editor section if needed
        text_section = page.locator('[data-section="textEditor"]')
        if text_section.is_visible():
            section_header = text_section.locator(".section-header")
            if section_header.is_visible():
                section_header.click()
                time.sleep(0.5)
        
        # Setup text with placeholders
        text_editor = page.locator("#textEditor")
        expect(text_editor).to_be_visible(timeout=10000)
        text_editor.fill("{{Placeholder1}} content {{Placeholder2}}")
        time.sleep(1)
        
        page.screenshot(path=str(screenshot_dir / "07_live_preview_placeholders.png"), full_page=True)
        print(f"✅ Screenshot: 07_live_preview_placeholders.png")
    
    def test_08_before_drag(self, page: Page, screenshot_dir):
        """8. Before drag operation"""
        page.goto("http://localhost/v2p-formatter/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # Setup qualification/learner
        qual_select = page.locator("#qualificationSelect")
        if qual_select.locator("option").count() > 1:
            qual_select.select_option(index=1)
            time.sleep(1)
            
            learner_select = page.locator("#learnerSelect")
            if learner_select.locator("option").count() > 1:
                learner_select.select_option(index=1)
                time.sleep(2)
        
        # Expand text editor section if needed
        text_section = page.locator('[data-section="textEditor"]')
        if text_section.is_visible():
            section_header = text_section.locator(".section-header")
            if section_header.is_visible():
                section_header.click()
                time.sleep(0.5)
        
        # Setup text with placeholder
        text_editor = page.locator("#textEditor")
        expect(text_editor).to_be_visible(timeout=10000)
        text_editor.fill("{{TestPlaceholder}}")
        time.sleep(1)
        
        page.screenshot(path=str(screenshot_dir / "08_before_drag.png"), full_page=True)
        print(f"✅ Screenshot: 08_before_drag.png")
    
    def test_09_after_drag(self, page: Page, screenshot_dir):
        """9. After drag and drop"""
        page.goto("http://localhost/v2p-formatter/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # Setup qualification/learner
        qual_select = page.locator("#qualificationSelect")
        if qual_select.locator("option").count() > 1:
            qual_select.select_option(index=1)
            time.sleep(1)
            
            learner_select = page.locator("#learnerSelect")
            if learner_select.locator("option").count() > 1:
                learner_select.select_option(index=1)
                time.sleep(2)
        
        # Expand text editor section if needed
        text_section = page.locator('[data-section="textEditor"]')
        if text_section.is_visible():
            section_header = text_section.locator(".section-header")
            if section_header.is_visible():
                section_header.click()
                time.sleep(0.5)
        
        # Setup text with placeholder
        text_editor = page.locator("#textEditor")
        expect(text_editor).to_be_visible(timeout=10000)
        text_editor.fill("{{TestPlaceholder}}")
        time.sleep(1)
        
        # Try to perform drag and drop
        media_cards = page.locator(".media-card:not(.assigned)")
        drop_zones = page.locator(".drop-zone")
        
        if media_cards.count() > 0 and drop_zones.count() > 0:
            media_cards.first.drag_to(drop_zones.first)
            time.sleep(2)
        
        page.screenshot(path=str(screenshot_dir / "09_after_drag.png"), full_page=True)
        print(f"✅ Screenshot: 09_after_drag.png")
    
    def test_10_draft_dialog(self, page: Page, screenshot_dir):
        """10. Draft load dialog"""
        page.goto("http://localhost/v2p-formatter/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # Click load draft button
        load_btn = page.locator("#loadDraftBtn")
        if load_btn.is_visible():
            load_btn.click()
            time.sleep(1)
            
            page.screenshot(path=str(screenshot_dir / "10_draft_dialog.png"), full_page=True)
            print(f"✅ Screenshot: 10_draft_dialog.png")
    
    def test_11_load_draft_standards(self, page: Page, screenshot_dir):
        """11. Load draft and verify standards"""
        page.goto("http://localhost/v2p-formatter/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # Click load draft button
        load_btn = page.locator("#loadDraftBtn")
        if load_btn.is_visible():
            load_btn.click()
            time.sleep(1)
            
            # Find and click on the specific draft
            draft_items = page.locator(".draft-item")
            target_draft = "learner_lakhmaniuk_obs1_20251209_194019"
            
            for i in range(draft_items.count()):
                item = draft_items.nth(i)
                if target_draft in item.inner_text():
                    load_draft_btn = item.locator(".btn-load-draft")
                    if load_draft_btn.is_visible():
                        load_draft_btn.click()
                        time.sleep(3)  # Wait for draft to load
                        
                        # Screenshot after loading
                        page.screenshot(path=str(screenshot_dir / "11_draft_loaded.png"), full_page=True)
                        print(f"✅ Screenshot: 11_draft_loaded.png")
                        
                        # Screenshot of standards panel
                        standards_container = page.locator("#standards")
                        if standards_container.is_visible():
                            page.screenshot(path=str(screenshot_dir / "12_standards_panel.png"), full_page=True)
                            print(f"✅ Screenshot: 12_standards_panel.png")
                        break

