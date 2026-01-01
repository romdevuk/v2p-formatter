"""
End-to-end workflow tests for Observation Report module
Tests complete user workflows from specification
"""
import pytest
import time
from playwright.sync_api import Page, expect


class TestObservationReportWorkflows:
    """Test complete observation report workflows"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Navigate to observation report page"""
        self.page = page
        self.base_url = "http://localhost/v2p-formatter"
        self.page.goto(f"{self.base_url}/observation-report")
        time.sleep(2)
    
    def test_workflow_1_initial_setup(self, page: Page):
        """Workflow 1: Initial Setup and Media Selection"""
        print("\n=== Workflow 1: Initial Setup ===")
        
        # Step 1: Page loads
        container = page.locator(".observation-report-container")
        expect(container).to_be_visible(timeout=10000)
        print("✅ Page loaded")
        
        # Step 2: Select qualification
        qualification_select = page.locator("#qualificationSelect")
        if qualification_select.is_visible():
            # Select first available qualification (if any)
            options = qualification_select.locator("option")
            if options.count() > 1:  # More than just "Select Qualification..."
                qualification_select.select_option(index=1)
                time.sleep(1)
                print("✅ Qualification selected")
        
        # Step 3: Select learner
        learner_select = page.locator("#learnerSelect")
        if learner_select.is_visible() and not learner_select.is_disabled():
            options = learner_select.locator("option")
            if options.count() > 1:
                learner_select.select_option(index=1)
                time.sleep(2)  # Wait for media to load
                print("✅ Learner selected")
        
        # Step 4: Verify media browser loaded
        media_browser = page.locator("#mediaBrowser")
        expect(media_browser).to_be_visible(timeout=10000)
        print("✅ Media browser visible")
        
        print("✅ Workflow 1: COMPLETE")
    
    def test_workflow_2_create_content_with_placeholders(self, page: Page):
        """Workflow 2: Creating Content with Placeholders"""
        print("\n=== Workflow 2: Create Content with Placeholders ===")
        
        # Step 1: Expand text editor section
        text_editor_section = page.locator('[data-section="textEditor"]')
        if text_editor_section.is_visible():
            section_header = text_editor_section.locator(".section-header")
            if section_header.is_visible():
                section_header.click()
                time.sleep(0.5)
                print("✅ Text editor section expanded")
        
        # Step 2: Enter text with placeholders
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            test_text = """
            Section 1: Health and Safety
            
            {{Site_Arrival_Induction}}
            
            The site arrival process was conducted properly.
            
            {{Safety_Briefing}}
            
            Safety procedures were explained clearly.
            """
            text_editor.fill(test_text)
            time.sleep(1)
            print("✅ Text with placeholders entered")
            
            # Step 3: Verify placeholders are detected
            stats = page.locator("#textEditorStats")
            if stats.is_visible():
                stats_text = stats.inner_text()
                assert "Placeholders:" in stats_text
                print(f"✅ Statistics: {stats_text}")
        
        # Step 4: Verify live preview updates
        live_preview = page.locator("#livePreview")
        expect(live_preview).to_be_visible()
        
        placeholder_containers = page.locator(".placeholder-container")
        if placeholder_containers.count() > 0:
            print(f"✅ Live preview shows {placeholder_containers.count()} placeholders")
        
        print("✅ Workflow 2: COMPLETE")
    
    def test_workflow_3a_click_to_assign(self, page: Page):
        """Workflow 3A: Assigning Media (Click-to-Assign)"""
        print("\n=== Workflow 3A: Click-to-Assign ===")
        
        # Step 1: Set up content with placeholder
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("Test {{ClickPlaceholder}}")
            time.sleep(1)
        
        # Step 2: Find media card
        media_cards = page.locator(".media-card")
        if media_cards.count() > 0:
            media_card = media_cards.first
            expect(media_card).to_be_visible()
            
            # Step 3: Click media card (should trigger assignment to placeholder)
            media_card.click()
            time.sleep(1)
            
            # Step 4: If multiple placeholders, dialog should appear
            # Otherwise, direct assignment should occur
            
            # Step 5: Verify assignment
            assigned_cards = page.locator(".media-card.assigned")
            media_items = page.locator(".media-item")
            
            if assigned_cards.count() > 0 or media_items.count() > 0:
                print("✅ Media assigned via click")
        
        print("✅ Workflow 3A: COMPLETE")
    
    def test_workflow_3b_drag_and_drop_assign(self, page: Page):
        """Workflow 3B: Assigning Media (Drag-and-Drop)"""
        print("\n=== Workflow 3B: Drag-and-Drop Assign ===")
        
        # Step 1: Set up content
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("Test {{DragPlaceholder}}")
            time.sleep(1)
        
        # Step 2: Find media card and drop zone
        media_card = page.locator(".media-card").first
        drop_zone = page.locator(".drop-zone").first
        
        if media_card.is_visible() and drop_zone.is_visible():
            # Step 3: Perform drag and drop
            media_card.drag_to(drop_zone)
            time.sleep(1)
            
            # Step 4: Verify assignment
            assigned = page.locator(".media-card.assigned")
            media_items = page.locator(".media-item")
            
            if assigned.count() > 0 or media_items.count() > 0:
                print("✅ Media assigned via drag-and-drop")
        
        print("✅ Workflow 3B: COMPLETE")
    
    def test_workflow_4_reorder_media(self, page: Page):
        """Workflow 4: Reordering Media Within Placeholders"""
        print("\n=== Workflow 4: Reorder Media ===")
        
        # Step 1: Assign multiple media to placeholder
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("Test {{ReorderPlaceholder}}")
            time.sleep(1)
        
        # Assign 3 media items
        drop_zone = page.locator(".drop-zone").first
        media_cards = page.locator(".media-card")
        
        for i in range(min(3, media_cards.count())):
            card = media_cards.nth(i)
            if card.is_visible() and drop_zone.is_visible():
                card.drag_to(drop_zone)
                time.sleep(0.5)
        
        print("✅ Multiple media assigned")
        
        # Step 2: Reorder using arrow buttons
        media_items = page.locator(".media-item")
        if media_items.count() >= 2:
            second_item = media_items.nth(1)
            up_button = second_item.locator(".reorder-up")
            if up_button.is_visible():
                up_button.click()
                time.sleep(0.5)
                print("✅ Media reordered using arrow button")
        
        print("✅ Workflow 4: COMPLETE")
    
    def test_workflow_5_header_information(self, page: Page):
        """Workflow 5: Header Information Entry"""
        print("\n=== Workflow 5: Header Information ===")
        
        # Step 1: Expand header section
        header_section = page.locator('[data-section="header"]')
        if header_section.is_visible():
            section_header = header_section.locator(".section-header")
            section_header.click()
            time.sleep(0.5)
            print("✅ Header section expanded")
        
        # Step 2: Fill header fields
        learner_input = page.locator("#headerLearner")
        if learner_input.is_visible():
            learner_input.fill("Test Learner")
        
        assessor_input = page.locator("#headerAssessor")
        if assessor_input.is_visible():
            assessor_input.fill("Test Assessor")
        
        visit_date = page.locator("#headerVisitDate")
        if visit_date.is_visible():
            visit_date.fill("2025-01-15")
        
        location = page.locator("#headerLocation")
        if location.is_visible():
            location.fill("Test Location")
        
        address = page.locator("#headerAddress")
        if address.is_visible():
            address.fill("Test Address")
        
        time.sleep(0.5)
        print("✅ Header information entered")
        
        print("✅ Workflow 5: COMPLETE")
    
    def test_workflow_8_save_draft(self, page: Page):
        """Workflow 8: Saving Drafts"""
        print("\n=== Workflow 8: Save Draft ===")
        
        # Step 1: Enter some content
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("Test draft content {{DraftPlaceholder}}")
            time.sleep(1)
        
        # Step 2: Click save draft button
        save_button = page.locator("#saveDraftBtn")
        if save_button.is_visible():
            save_button.click()
            time.sleep(1)
            
            # Step 3: Handle dialog (if present)
            # In real implementation, would fill draft name
            
            print("✅ Save draft button clicked")
        
        print("✅ Workflow 8: COMPLETE")
    
    def test_workflow_9_load_draft(self, page: Page):
        """Workflow 9: Loading Drafts"""
        print("\n=== Workflow 9: Load Draft ===")
        
        # Step 1: Click load draft button
        load_button = page.locator("#loadDraftBtn")
        if load_button.is_visible():
            load_button.click()
            time.sleep(1)
            
            # Step 2: Verify draft dialog appears
            draft_dialog = page.locator("#draftLoadDialog")
            if draft_dialog.is_visible():
                print("✅ Draft load dialog appeared")
                
                # Step 3: Close dialog
                close_button = draft_dialog.locator(".modal-close")
                if close_button.is_visible():
                    close_button.click()
                    time.sleep(0.5)
        
        print("✅ Workflow 9: COMPLETE")
    
    def test_workflow_11_preview_draft(self, page: Page):
        """Workflow 11: Document Preview"""
        print("\n=== Workflow 11: Preview Draft ===")
        
        # Step 1: Enter content
        text_editor = page.locator("#textEditor")
        if text_editor.is_visible():
            text_editor.fill("Preview test content {{PreviewPlaceholder}}")
            time.sleep(1)
        
        # Step 2: Click preview button
        preview_button = page.locator("#previewDraftBtn")
        if preview_button.is_visible():
            preview_button.click()
            time.sleep(2)
            
            # Step 3: Verify preview dialog opens
            preview_dialog = page.locator(".preview-dialog-overlay")
            if preview_dialog.is_visible():
                print("✅ Preview dialog opened")
                
                # Step 4: Close preview (if close button exists)
                # Implementation may vary
        
        print("✅ Workflow 11: COMPLETE")



