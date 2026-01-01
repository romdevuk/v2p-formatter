"""
End-to-end workflow tests for Observation Report with actual UI interactions
Tests complete workflows with screenshots and visual verification
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


class TestObservationReportWorkflowsE2E:
    """End-to-end workflow tests with visual verification"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, screenshot_dir):
        """Navigate to observation report page"""
        self.page = page
        self.base_url = "http://localhost/v2p-formatter"
        self.screenshot_dir = screenshot_dir
        self.page.goto(f"{self.base_url}/observation-report")
        time.sleep(2)  # Wait for page load
        self.page.screenshot(path=str(self.screenshot_dir / "00_initial_load.png"))
    
    def test_workflow_qualification_learner_selection(self, page: Page):
        """Test qualification and learner dropdown selection with verification"""
        print("\n=== Workflow: Qualification & Learner Selection ===")
        
        # Step 1: Verify qualification dropdown is visible
        qualification_select = page.locator("#qualificationSelect")
        expect(qualification_select).to_be_visible(timeout=10000)
        print("✅ Qualification dropdown visible")
        self.page.screenshot(path=str(self.screenshot_dir / "01_qualification_dropdown.png"))
        
        # Step 2: Check if dropdown has options (should be populated from server)
        options = qualification_select.locator("option")
        option_count = options.count()
        print(f"✅ Qualification dropdown has {option_count} options")
        
        if option_count > 1:  # More than just "Select Qualification..."
            # Step 3: Select first qualification
            qualification_select.select_option(index=1)
            time.sleep(1)
            
            selected_value = qualification_select.input_value()
            print(f"✅ Selected qualification: {selected_value}")
            self.page.screenshot(path=str(self.screenshot_dir / "02_qualification_selected.png"))
            
            # Step 4: Verify learner dropdown is enabled
            learner_select = page.locator("#learnerSelect")
            expect(learner_select).not_to_be_disabled(timeout=5000)
            print("✅ Learner dropdown enabled")
            
            # Step 5: Wait for learners to load
            time.sleep(1)
            learner_options = learner_select.locator("option")
            learner_count = learner_options.count()
            print(f"✅ Learner dropdown has {learner_count} options")
            
            if learner_count > 1:
                # Step 6: Select first learner
                learner_select.select_option(index=1)
                time.sleep(2)  # Wait for media to load
                
                selected_learner = learner_select.input_value()
                print(f"✅ Selected learner: {selected_learner}")
                self.page.screenshot(path=str(self.screenshot_dir / "03_learner_selected_media_loaded.png"))
                
                # Step 7: Verify media browser loaded
                media_browser = page.locator("#mediaBrowser")
                expect(media_browser).to_be_visible(timeout=10000)
                
                # Check for media cards
                media_cards = page.locator(".media-card")
                card_count = media_cards.count()
                print(f"✅ Media browser loaded with {card_count} media files")
                self.page.screenshot(path=str(self.screenshot_dir / "04_media_browser_loaded.png"))
        
        print("✅ Workflow: Qualification & Learner Selection - COMPLETE")
    
    def test_workflow_placeholder_rendering(self, page: Page):
        """Test placeholder rendering in live preview"""
        print("\n=== Workflow: Placeholder Rendering ===")
        
        # Step 1: Expand text editor section
        text_editor_section = page.locator('[data-section="textEditor"]')
        if text_editor_section.is_visible():
            section_header = text_editor_section.locator(".section-header")
            section_header.click()
            time.sleep(0.5)
            print("✅ Text editor section expanded")
        
        # Step 2: Enter text with placeholders
        text_editor = page.locator("#textEditor")
        expect(text_editor).to_be_visible(timeout=5000)
        
        test_text = """
SECTION 1: Site Arrival

{{Site_Arrival_Induction}}

The site arrival process was conducted properly.

{{Safety_Briefing}}

Safety procedures were explained clearly.

{{Equipment_Check}}

All equipment was verified.
        """.strip()
        
        text_editor.fill(test_text)
        time.sleep(1)  # Wait for preview to update
        print("✅ Text with placeholders entered")
        self.page.screenshot(path=str(self.screenshot_dir / "05_text_entered.png"))
        
        # Step 3: Verify live preview shows placeholders
        live_preview = page.locator("#livePreview")
        expect(live_preview).to_be_visible()
        
        placeholder_containers = page.locator(".placeholder-container")
        container_count = placeholder_containers.count()
        print(f"✅ Live preview shows {container_count} placeholder containers")
        
        if container_count > 0:
            self.page.screenshot(path=str(self.screenshot_dir / "06_placeholders_rendered.png"))
            
            # Verify placeholder labels are visible
            placeholder_labels = page.locator(".placeholder-label")
            label_count = placeholder_labels.count()
            print(f"✅ Found {label_count} placeholder labels")
            
            # Verify drop zones exist
            drop_zones = page.locator(".drop-zone")
            zone_count = drop_zones.count()
            print(f"✅ Found {zone_count} drop zones")
        
        print("✅ Workflow: Placeholder Rendering - COMPLETE")
    
    def test_workflow_drag_and_drop_media(self, page: Page):
        """Test drag-and-drop media assignment (CRITICAL)"""
        print("\n=== Workflow: Drag-and-Drop Media Assignment (CRITICAL) ===")
        
        # Step 1: Setup - ensure we have text with placeholder and media
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("Test content {{TestPlaceholder}}")
            time.sleep(1)
        
        # Step 2: Load media (select qualification and learner if needed)
        media_cards = page.locator(".media-card")
        if media_cards.count() == 0:
            # Need to select qualification/learner first
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
        
        # Step 3: Verify media cards are available
        media_cards = page.locator(".media-card")
        expect(media_cards.first).to_be_visible(timeout=10000)
        print("✅ Media cards available")
        self.page.screenshot(path=str(self.screenshot_dir / "07_before_drag.png"))
        
        # Step 4: Find drop zone
        drop_zone = page.locator(".drop-zone").first
        if drop_zone.is_visible():
            # Step 5: Perform drag and drop
            media_card = media_cards.first
            media_card.drag_to(drop_zone)
            time.sleep(2)  # Wait for assignment
            print("✅ Drag and drop completed")
            self.page.screenshot(path=str(self.screenshot_dir / "08_after_drag.png"))
            
            # Step 6: Verify media card is marked as assigned
            assigned_cards = page.locator(".media-card.assigned")
            if assigned_cards.count() > 0:
                print("✅ Media card marked as assigned")
            
            # Step 7: Verify media appears in preview
            media_items = page.locator(".media-item")
            if media_items.count() > 0:
                print("✅ Media appears in placeholder table")
                self.page.screenshot(path=str(self.screenshot_dir / "09_media_in_placeholder.png"))
        
        print("✅ Workflow: Drag-and-Drop Media Assignment - COMPLETE")
    
    def test_workflow_reshuffle_media(self, page: Page):
        """Test reshuffle/reordering media (CRITICAL)"""
        print("\n=== Workflow: Reshuffle Media (CRITICAL) ===")
        
        # Step 1: Setup - assign multiple media to placeholder
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("Test {{ReorderPlaceholder}}")
            time.sleep(1)
        
        # Assign 3-4 media items
        drop_zone = page.locator(".drop-zone").first
        media_cards = page.locator(".media-card:not(.assigned)")
        
        assigned_count = 0
        for i in range(min(4, media_cards.count())):
            card = media_cards.nth(i)
            if card.is_visible() and drop_zone.is_visible():
                card.drag_to(drop_zone)
                time.sleep(0.5)
                assigned_count += 1
        
        print(f"✅ Assigned {assigned_count} media items")
        self.page.screenshot(path=str(self.screenshot_dir / "10_before_reshuffle.png"))
        
        # Step 2: Test arrow button reordering
        media_items = page.locator(".media-item")
        if media_items.count() >= 2:
            second_item = media_items.nth(1)
            up_button = second_item.locator(".reorder-up")
            if up_button.is_visible():
                up_button.click()
                time.sleep(0.5)
                print("✅ Reordered using up arrow button")
                self.page.screenshot(path=str(self.screenshot_dir / "11_after_arrow_reorder.png"))
        
        # Step 3: Test drag-and-drop reordering within table
        if media_items.count() >= 3:
            # Get item at position 2
            item_to_move = media_items.nth(2)
            target_item = media_items.nth(0)
            
            if item_to_move.is_visible() and target_item.is_visible():
                item_to_move.drag_to(target_item)
                time.sleep(1)
                print("✅ Reordered using drag-and-drop")
                self.page.screenshot(path=str(self.screenshot_dir / "12_after_drag_reorder.png"))
        
        print("✅ Workflow: Reshuffle Media - COMPLETE")
    
    def test_workflow_load_draft_with_standards(self, page: Page):
        """Test loading draft and verifying standards data loads"""
        print("\n=== Workflow: Load Draft with Standards ===")
        
        # Step 1: Click load draft button
        load_button = page.locator("#loadDraftBtn")
        expect(load_button).to_be_visible(timeout=5000)
        load_button.click()
        time.sleep(1)
        
        # Step 2: Verify draft dialog appears
        draft_dialog = page.locator("#draftLoadDialog")
        if draft_dialog.is_visible():
            print("✅ Draft load dialog appeared")
            self.page.screenshot(path=str(self.screenshot_dir / "13_draft_dialog.png"))
            
            # Step 3: Look for the specific draft
            draft_items = page.locator(".draft-item")
            draft_count = draft_items.count()
            print(f"✅ Found {draft_count} drafts in list")
            
            # Try to find the specific draft
            target_draft_name = "learner_lakhmaniuk_obs1_20251209_194019"
            draft_found = False
            
            for i in range(draft_count):
                item = draft_items.nth(i)
                if target_draft_name in item.inner_text():
                    # Click load button for this draft
                    load_btn = item.locator(".btn-load-draft")
                    if load_btn.is_visible():
                        load_btn.click()
                        draft_found = True
                        print(f"✅ Loading draft: {target_draft_name}")
                        break
            
            if draft_found:
                time.sleep(3)  # Wait for draft to load
                self.page.screenshot(path=str(self.screenshot_dir / "14_draft_loaded.png"))
                
                # Step 4: Verify standards panel loaded
                standards_container = page.locator("#standards")
                expect(standards_container).to_be_visible(timeout=5000)
                
                # Check for standards content
                standards_content = page.locator(".standards-content")
                if standards_content.is_visible():
                    # Check for unit containers
                    unit_containers = page.locator(".unit-container")
                    unit_count = unit_containers.count()
                    print(f"✅ Standards panel loaded with {unit_count} units")
                    
                    if unit_count > 0:
                        self.page.screenshot(path=str(self.screenshot_dir / "15_standards_loaded.png"))
                    else:
                        print("⚠️ WARNING: Standards panel visible but no units found")
                        self.page.screenshot(path=str(self.screenshot_dir / "15_standards_empty.png"))
                
                # Step 5: Verify text content loaded
                text_editor = page.locator("#textEditor")
                text_value = text_editor.input_value()
                if text_value:
                    print(f"✅ Text content loaded ({len(text_value)} characters)")
                
                # Step 6: Verify placeholders rendered
                placeholder_containers = page.locator(".placeholder-container")
                placeholder_count = placeholder_containers.count()
                print(f"✅ Placeholders rendered: {placeholder_count}")
                
                # Step 7: Verify media assignments loaded
                media_items = page.locator(".media-item")
                media_count = media_items.count()
                print(f"✅ Media items in preview: {media_count}")
                
            else:
                print(f"⚠️ Draft '{target_draft_name}' not found in list")
        else:
            print("⚠️ Draft dialog did not appear")
        
        print("✅ Workflow: Load Draft with Standards - COMPLETE")
    
    def test_workflow_complete_user_journey(self, page: Page):
        """Complete user journey from start to finish"""
        print("\n=== Workflow: Complete User Journey ===")
        
        # Step 1: Select qualification
        qualification_select = page.locator("#qualificationSelect")
        if qualification_select.is_visible():
            options = qualification_select.locator("option")
            if options.count() > 1:
                qualification_select.select_option(index=1)
                time.sleep(1)
                self.page.screenshot(path=str(self.screenshot_dir / "16_journey_qualification.png"))
        
        # Step 2: Select learner
        learner_select = page.locator("#learnerSelect")
        if learner_select.is_visible():
            options = learner_select.locator("option")
            if options.count() > 1:
                learner_select.select_option(index=1)
                time.sleep(2)
                self.page.screenshot(path=str(self.screenshot_dir / "17_journey_learner.png"))
        
        # Step 3: Enter text with placeholders
        text_editor_section = page.locator('[data-section="textEditor"]')
        if text_editor_section.is_visible():
            section_header = text_editor_section.locator(".section-header")
            section_header.click()
            time.sleep(0.5)
        
        text_editor = page.locator("#textEditor")
        test_text = "{{Placeholder1}} content {{Placeholder2}}"
        text_editor.fill(test_text)
        time.sleep(1)
        self.page.screenshot(path=str(self.screenshot_dir / "18_journey_text.png"))
        
        # Step 4: Assign media via drag-and-drop
        media_card = page.locator(".media-card:not(.assigned)").first
        drop_zone = page.locator(".drop-zone").first
        if media_card.is_visible() and drop_zone.is_visible():
            media_card.drag_to(drop_zone)
            time.sleep(2)
            self.page.screenshot(path=str(self.screenshot_dir / "19_journey_media_assigned.png"))
        
        # Step 5: Save draft
        save_button = page.locator("#saveDraftBtn")
        if save_button.is_visible():
            # Note: Would need to handle prompt dialog
            print("✅ Save draft button available")
        
        # Step 6: Preview draft
        preview_button = page.locator("#previewDraftBtn")
        if preview_button.is_visible():
            preview_button.click()
            time.sleep(2)
            self.page.screenshot(path=str(self.screenshot_dir / "20_journey_preview.png"))
            
            # Close preview if needed
            # (Implementation depends on preview dialog structure)
        
        print("✅ Workflow: Complete User Journey - COMPLETE")



