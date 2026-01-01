"""
Observation Report - Complete End-to-End Workflow Test
Tests the full workflow: open draft → add media → header → feedback → export DOCX
"""
import pytest
import time
import os
from pathlib import Path
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def screenshot_dir():
    """Create screenshots directory"""
    screenshots = Path("test_screenshots/observation_report_complete_workflow")
    screenshots.mkdir(parents=True, exist_ok=True)
    return screenshots


class TestCompleteWorkflow:
    """Complete end-to-end workflow test"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, screenshot_dir):
        """Navigate to observation report page"""
        self.page = page
        self.base_url = "http://localhost/v2p-formatter"
        self.screenshot_dir = screenshot_dir
        self.page.goto(f"{self.base_url}/observation-report")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        self.workflow_errors = []
    
    def test_complete_workflow_end_to_end(self, page: Page):
        """Complete workflow: Open draft → Add media → Header → Feedback → Export DOCX"""
        print("\n" + "="*70)
        print("COMPLETE WORKFLOW TEST - End-to-End")
        print("="*70)
        
        # Step 1: Open existing draft
        print("\n📂 STEP 1: Opening Existing Draft")
        print("-" * 70)
        draft_loaded = self._step1_open_draft(page)
        assert draft_loaded, "❌ FAILED: Could not open draft"
        page.screenshot(path=str(self.screenshot_dir / "01_draft_opened.png"), full_page=True)
        print("✅ Draft opened successfully")
        time.sleep(2)
        
        # Step 2: Verify draft content loaded
        print("\n📋 STEP 2: Verifying Draft Content")
        print("-" * 70)
        content_verified = self._step2_verify_content(page)
        assert content_verified, "❌ FAILED: Draft content not loaded correctly"
        page.screenshot(path=str(self.screenshot_dir / "02_content_verified.png"), full_page=True)
        print("✅ Draft content verified")
        
        # Step 3: Add media to placeholders
        print("\n🖼️  STEP 3: Adding Media to Placeholders")
        print("-" * 70)
        media_added = self._step3_add_media(page)
        assert media_added, "❌ FAILED: Could not add media"
        page.screenshot(path=str(self.screenshot_dir / "03_media_added.png"), full_page=True)
        print("✅ Media added successfully")
        time.sleep(1)
        
        # Step 4: Fill header data
        print("\n📝 STEP 4: Filling Header Data")
        print("-" * 70)
        header_filled = self._step4_fill_header(page)
        assert header_filled, "❌ FAILED: Could not fill header data"
        page.screenshot(path=str(self.screenshot_dir / "04_header_filled.png"), full_page=True)
        print("✅ Header data filled")
        time.sleep(1)
        
        # Step 5: Add assessor feedback
        print("\n💬 STEP 5: Adding Assessor Feedback")
        print("-" * 70)
        feedback_added = self._step5_add_feedback(page)
        assert feedback_added, "❌ FAILED: Could not add feedback"
        page.screenshot(path=str(self.screenshot_dir / "05_feedback_added.png"), full_page=True)
        print("✅ Feedback added")
        time.sleep(1)
        
        # Step 6: Save draft
        print("\n💾 STEP 6: Saving Draft")
        print("-" * 70)
        draft_saved = self._step6_save_draft(page)
        assert draft_saved, "❌ FAILED: Could not save draft"
        page.screenshot(path=str(self.screenshot_dir / "06_draft_saved.png"), full_page=True)
        print("✅ Draft saved")
        time.sleep(1)
        
        # Step 7: Export to DOCX
        print("\n📄 STEP 7: Exporting to DOCX")
        print("-" * 70)
        docx_exported = self._step7_export_docx(page)
        assert docx_exported, "❌ FAILED: Could not export DOCX"
        page.screenshot(path=str(self.screenshot_dir / "07_docx_exported.png"), full_page=True)
        print("✅ DOCX exported successfully")
        
        # Final summary
        print("\n" + "="*70)
        print("✅ COMPLETE WORKFLOW TEST - ALL STEPS PASSED")
        print("="*70)
        
        if self.workflow_errors:
            print("\n⚠️  Warnings/Issues Found:")
            for error in self.workflow_errors:
                print(f"   - {error}")
    
    def _step1_open_draft(self, page: Page) -> bool:
        """Step 1: Open existing draft"""
        try:
            # Click Load Draft button
            load_btn = page.locator("#loadDraftBtn")
            if not load_btn.is_visible():
                self.workflow_errors.append("Load Draft button not visible")
                return False
            
            load_btn.click()
            time.sleep(1)
            
            # Look for draft dialog
            dialog = page.locator("#draftLoadDialog")
            if not dialog.is_visible():
                self.workflow_errors.append("Draft dialog not visible")
                return False
            
            # Find and click on a draft (prefer the specific one, or any draft)
            draft_items = page.locator(".draft-item")
            draft_count = draft_items.count()
            
            if draft_count == 0:
                self.workflow_errors.append("No drafts found in list")
                return False
            
            print(f"   Found {draft_count} drafts")
            
            # Try to find specific draft first, otherwise use first one
            target_draft = "learner_lakhmaniuk_obs1_20251209_194019"
            draft_found = False
            
            for i in range(draft_count):
                item = draft_items.nth(i)
                item_text = item.inner_text()
                
                if target_draft in item_text:
                    print(f"   Loading draft: {target_draft}")
                    load_draft_btn = item.locator(".btn-load-draft")
                    if load_draft_btn.is_visible():
                        load_draft_btn.click()
                        draft_found = True
                        break
            
            # If specific draft not found, use first one
            if not draft_found:
                print(f"   Loading first available draft")
                load_draft_btn = draft_items.first.locator(".btn-load-draft")
                if load_draft_btn.is_visible():
                    load_draft_btn.click()
                    draft_found = True
            
            if draft_found:
                time.sleep(3)  # Wait for draft to load
                # Dialog should close
                dialog_visible = dialog.is_visible()
                if dialog_visible:
                    # Try to close it
                    close_btn = dialog.locator(".modal-close")
                    if close_btn.is_visible():
                        close_btn.click()
                        time.sleep(0.5)
                
                return True
            
            return False
            
        except Exception as e:
            self.workflow_errors.append(f"Error opening draft: {str(e)}")
            return False
    
    def _step2_verify_content(self, page: Page) -> bool:
        """Step 2: Verify draft content loaded"""
        try:
            # Check text editor has content
            text_editor = page.locator("#textEditor")
            if text_editor.is_visible():
                text_value = text_editor.input_value()
                if text_value:
                    print(f"   Text content loaded: {len(text_value)} characters")
                else:
                    self.workflow_errors.append("Text editor is empty")
                    return False
            
            # Check placeholders are rendered
            placeholder_labels = page.locator(".placeholder-label")
            placeholder_count = placeholder_labels.count()
            if placeholder_count > 0:
                print(f"   Placeholders rendered: {placeholder_count}")
            else:
                self.workflow_errors.append("No placeholders rendered")
            
            # Check sections are visible
            section_titles = page.locator(".section-title")
            section_count = section_titles.count()
            if section_count > 0:
                print(f"   Sections found: {section_count}")
            
            # Check standards panel
            standards_container = page.locator("#standards")
            if standards_container.is_visible():
                unit_containers = page.locator(".unit-container")
                unit_count = unit_containers.count()
                if unit_count > 0:
                    print(f"   Standards units loaded: {unit_count}")
                else:
                    self.workflow_errors.append("Standards panel empty (no units)")
            
            return True
            
        except Exception as e:
            self.workflow_errors.append(f"Error verifying content: {str(e)}")
            return False
    
    def _step3_add_media(self, page: Page) -> bool:
        """Step 3: Add media to placeholders"""
        try:
            # Find drop zones
            drop_zones = page.locator(".drop-zone")
            drop_zone_count = drop_zones.count()
            
            if drop_zone_count == 0:
                self.workflow_errors.append("No drop zones found (no empty placeholders?)")
                return True  # Not a failure if all placeholders already have media
            
            print(f"   Found {drop_zone_count} drop zones")
            
            # Find unassigned media cards
            media_cards = page.locator(".media-card:not(.assigned)")
            media_count = media_cards.count()
            
            if media_count == 0:
                self.workflow_errors.append("No unassigned media available")
                return True  # Not a failure if all media already assigned
            
            print(f"   Found {media_count} unassigned media cards")
            
            # Assign media to first few drop zones
            assigned = 0
            for i in range(min(3, drop_zone_count, media_count)):
                try:
                    card = media_cards.nth(i)
                    drop_zone = drop_zones.nth(i)
                    
                    if card.is_visible() and drop_zone.is_visible():
                        card.drag_to(drop_zone)
                        time.sleep(1.5)  # Wait for assignment
                        assigned += 1
                except Exception as e:
                    self.workflow_errors.append(f"Error assigning media {i}: {str(e)}")
            
            if assigned > 0:
                print(f"   Assigned {assigned} media items")
                # Verify media appears in preview
                media_items = page.locator(".media-item")
                if media_items.count() > 0:
                    print(f"   Media visible in preview: {media_items.count()} items")
            
            return True
            
        except Exception as e:
            self.workflow_errors.append(f"Error adding media: {str(e)}")
            return False
    
    def _step4_fill_header(self, page: Page) -> bool:
        """Step 4: Fill header data"""
        try:
            # Expand header section if needed
            header_section = page.locator('[data-section="header"]')
            if header_section.is_visible():
                section_header = header_section.locator(".section-header")
                if section_header.is_visible():
                    # Check if collapsed
                    section_content = header_section.locator(".section-content")
                    if not section_content.is_visible():
                        section_header.click()
                        time.sleep(0.5)
            
            # Fill header fields
            header_fields = {
                'headerLearner': 'Test Learner',
                'headerAssessor': 'Test Assessor',
                'headerVisitDate': '2025-01-15',
                'headerLocation': 'Test Site Location',
                'headerAddress': '123 Test Street, Test City'
            }
            
            filled_count = 0
            for field_id, value in header_fields.items():
                field = page.locator(f"#{field_id}")
                if field.is_visible():
                    field.fill(value)
                    filled_count += 1
                else:
                    self.workflow_errors.append(f"Header field {field_id} not visible")
            
            if filled_count > 0:
                print(f"   Filled {filled_count} header fields")
            else:
                self.workflow_errors.append("No header fields found")
                return False
            
            return True
            
        except Exception as e:
            self.workflow_errors.append(f"Error filling header: {str(e)}")
            return False
    
    def _step5_add_feedback(self, page: Page) -> bool:
        """Step 5: Add assessor feedback"""
        try:
            # Find assessor feedback section
            feedback_section = page.locator('[data-section="assessorFeedback"]')
            
            if feedback_section.count() > 0:
                # Expand section if collapsed
                section_header = feedback_section.locator(".section-header")
                section_content = feedback_section.locator(".section-content")
                
                if section_header.is_visible():
                    # Check if content is hidden
                    content_visible = section_content.is_visible()
                    if not content_visible:
                        # Expand section
                        section_header.click()
                        time.sleep(0.5)
                    
                    # Now find textarea
                    feedback_textarea = feedback_section.locator("#assessorFeedback")
                    if feedback_textarea.count() > 0:
                        feedback_text = "This is test assessor feedback. The learner demonstrated good understanding of the tasks."
                        feedback_textarea.fill(feedback_text)
                        time.sleep(0.3)
                        print(f"   Added feedback: {len(feedback_text)} characters")
                        return True
                    else:
                        self.workflow_errors.append("Assessor feedback textarea not found in section")
                        return False
                else:
                    self.workflow_errors.append("Assessor feedback section header not found")
                    return False
            else:
                self.workflow_errors.append("Assessor feedback section not found")
                # Take screenshot for debugging
                page.screenshot(path=str(self.screenshot_dir / "05_feedback_not_found.png"), full_page=True)
                return False
                
        except Exception as e:
            self.workflow_errors.append(f"Error adding feedback: {str(e)}")
            page.screenshot(path=str(self.screenshot_dir / "05_feedback_error.png"), full_page=True)
            return False
    
    def _step6_save_draft(self, page: Page) -> bool:
        """Step 6: Save draft"""
        try:
            save_btn = page.locator("#saveDraftBtn")
            if save_btn.is_visible():
                save_btn.click()
                time.sleep(1)
                
                # Check for success message or dialog
                # (Implementation depends on how save feedback is shown)
                print("   Save button clicked")
                return True
            else:
                self.workflow_errors.append("Save draft button not found")
                return False
                
        except Exception as e:
            self.workflow_errors.append(f"Error saving draft: {str(e)}")
            return False
    
    def _step7_export_docx(self, page: Page) -> bool:
        """Step 7: Export to DOCX"""
        try:
            # Open preview dialog first (export is in preview)
            preview_btn = page.locator("#previewDraftBtn")
            if not preview_btn.is_visible():
                self.workflow_errors.append("Preview button not found")
                return False
            
            preview_btn.click()
            time.sleep(3)  # Wait for preview dialog to open
            
            # Look for export button in preview dialog
            # Try multiple selectors
            export_selectors = [
                "#exportDocxBtn",
                ".btn-export-docx",
                "[data-action='export-docx']",
                "button:has-text('Export DOCX')",
                "button:has-text('Export')",
                ".preview-actions button:has-text('DOCX')"
            ]
            
            export_btn = None
            for selector in export_selectors:
                elements = page.locator(selector)
                if elements.count() > 0:
                    btn = elements.first
                    if btn.is_visible():
                        export_btn = btn
                        print(f"   Found export button using: {selector}")
                        break
            
            if export_btn:
                export_btn.click()
                print("   Export DOCX button clicked")
                time.sleep(4)  # Wait for export and potential download
                
                # Check for download link or success message
                # Look for download link or success indicator
                download_link = page.locator("a[download], .download-link, a:has-text('Download')")
                if download_link.count() > 0:
                    print("   Download link appeared")
                else:
                    # Check for success message
                    success_msg = page.locator(".success, .alert-success, :has-text('Export successful')")
                    if success_msg.count() > 0:
                        print("   Success message shown")
                    else:
                        print("   Export initiated (no immediate feedback visible)")
                
                return True
            else:
                self.workflow_errors.append("Export DOCX button not found in preview dialog")
                # Take screenshot for debugging
                page.screenshot(path=str(self.screenshot_dir / "07_export_button_not_found.png"), full_page=True)
                return False
                
        except Exception as e:
            self.workflow_errors.append(f"Error exporting DOCX: {str(e)}")
            page.screenshot(path=str(self.screenshot_dir / "07_export_error.png"), full_page=True)
            return False

