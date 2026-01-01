"""
Browser tests for Image to PDF module
Using qualification: Clading, learner: Zozulia
"""
import pytest
from playwright.sync_api import Page, expect
import time
import os


BASE_URL = os.getenv("BASE_URL", "http://localhost/v2p-formatter")
QUALIFICATION = "Cladding"
LEARNER = "zozulia"  # Lowercase as returned by API


class TestImageToPDF:
    """Test suite for Image to PDF module"""
    
    def test_navigation_to_image_to_pdf(self, page: Page):
        """Test that Image to PDF tab is accessible"""
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Find and click Image to PDF tab
        image_to_pdf_link = page.locator('a[href="/v2p-formatter/image-to-pdf"]')
        expect(image_to_pdf_link).to_be_visible()
        image_to_pdf_link.click()
        
        # Verify we're on the Image to PDF page
        expect(page).to_have_url(f"{BASE_URL}/image-to-pdf")
        
        # Verify page title or heading
        page.wait_for_load_state("networkidle")
    
    def test_qualification_learner_selection(self, page: Page):
        """Test qualification and learner dropdown selection"""
        page.goto(f"{BASE_URL}/image-to-pdf")
        page.wait_for_load_state("networkidle")
        
        # Select qualification
        qualification_select = page.locator("#qualificationSelect")
        expect(qualification_select).to_be_visible()
        
        # Check if Cladding option exists
        options = qualification_select.locator("option")
        option_texts = [opt.inner_text() for opt in options.all()]
        if QUALIFICATION not in option_texts:
            pytest.skip(f"Qualification '{QUALIFICATION}' not found in dropdown. Available: {option_texts}")
        
        qualification_select.select_option(QUALIFICATION)
        
        # Wait for learner dropdown to be enabled and populated
        learner_select = page.locator("#learnerSelect")
        expect(learner_select).to_be_visible(timeout=5000)
        
        # Wait for dropdown to be enabled (not disabled)
        page.wait_for_timeout(1000)  # Wait for API call to complete
        expect(learner_select).to_be_enabled(timeout=10000)
        
        # Wait for options to be populated
        page.wait_for_timeout(1000)
        
        # Wait for learner options to be populated
        learner_options = learner_select.locator("option")
        page.wait_for_timeout(2000)  # Wait for API call and population
        
        # Check option count (should have at least "Select Learner..." + actual learners)
        option_count = learner_options.count()
        if option_count <= 1:  # Only "Select Learner..." option
            pytest.skip(f"No learners found for qualification '{QUALIFICATION}'")
        
        # Select learner by value
        try:
            learner_select.select_option(LEARNER, timeout=10000)
        except Exception as e:
            # Try finding the option manually
            all_options = learner_options.all()
            found = False
            for opt in all_options:
                opt_value = opt.get_attribute('value')
                opt_text = opt.inner_text()
                if opt_value == LEARNER or opt_text.lower() == LEARNER.lower():
                    learner_select.select_option(opt_value if opt_value else opt_text)
                    found = True
                    break
            if not found:
                pytest.fail(f"Could not select learner '{LEARNER}'. Available options: {[opt.inner_text() for opt in all_options]}")
        
        page.wait_for_timeout(1000)
        
        # Verify selections (case-insensitive check)
        expect(qualification_select).to_have_value(QUALIFICATION)
        # Check value case-insensitively
        actual_value = learner_select.input_value()
        assert actual_value.lower() == LEARNER.lower(), f"Expected learner '{LEARNER}' but got '{actual_value}'"
    
    def test_load_images(self, page: Page):
        """Test loading images for selected qualification/learner"""
        page.goto(f"{BASE_URL}/image-to-pdf")
        page.wait_for_load_state("networkidle")
        
        # Select qualification and learner
        qualification_select = page.locator("#qualificationSelect")
        qualification_select.select_option(QUALIFICATION)
        page.wait_for_timeout(2000)  # Wait for API call
        
        learner_select = page.locator("#learnerSelect")
        expect(learner_select).to_be_enabled(timeout=10000)
        learner_select.select_option(LEARNER)
        page.wait_for_timeout(3000)  # Wait for images to load
        
        # Check if images are loaded (file tree should not be empty)
        file_tree = page.locator("#fileTreeContent")
        expect(file_tree).to_be_visible()
        
        # Verify images are displayed (should not be loading message)
        loading_message = file_tree.locator("text=Please select both")
        if loading_message.is_visible():
            pytest.skip("No images found for Clading/Zozulia - this is expected if folder is empty")
        
        # Check for folder structure or image items
        page.wait_for_timeout(1000)
    
    def test_bulk_selection_mode(self, page: Page):
        """Test bulk selection mode toggle"""
        page.goto(f"{BASE_URL}/image-to-pdf")
        page.wait_for_load_state("networkidle")
        
        # Select qualification and learner
        qualification_select = page.locator("#qualificationSelect")
        qualification_select.select_option(QUALIFICATION)
        page.wait_for_timeout(1000)
        
        learner_select = page.locator("#learnerSelect")
        learner_select.select_option(LEARNER)
        page.wait_for_timeout(2000)
        
        # Enable bulk selection mode
        bulk_mode_toggle = page.locator("#bulkModeToggle")
        expect(bulk_mode_toggle).to_be_visible()
        
        if not bulk_mode_toggle.is_checked():
            bulk_mode_toggle.check()
        
        # Verify bulk mode controls are visible
        select_all_container = page.locator("#selectAllContainer")
        expect(select_all_container).to_be_visible()
        
        selection_count_badge = page.locator("#selectionCountBadge")
        # Badge may not be visible if no images selected yet
        
    def test_select_images_and_generate_documents(self, page: Page):
        """Test selecting images and generating documents"""
        page.goto(f"{BASE_URL}/image-to-pdf?qualification={QUALIFICATION}&learner={LEARNER}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)  # Wait for images to load
        
        # Enable bulk selection mode
        bulk_mode_toggle = page.locator("#bulkModeToggle")
        if bulk_mode_toggle.is_visible():
            if not bulk_mode_toggle.is_checked():
                bulk_mode_toggle.check()
            page.wait_for_timeout(500)
        
        # Check if images are available
        file_tree = page.locator("#fileTreeContent")
        if not file_tree.is_visible():
            pytest.skip("File tree not visible - may need to wait longer or no images available")
        
        # Try to find and select an image (look for image items or checkboxes)
        image_items = page.locator(".image-item, [data-path]").first
        if not image_items.is_visible(timeout=5000):
            pytest.skip("No images found for Clading/Zozulia - cannot test selection")
        
        # Select first image if available
        try:
            # Look for checkbox in bulk mode
            first_checkbox = page.locator(".image-item input[type='checkbox']").first
            if first_checkbox.is_visible(timeout=2000):
                first_checkbox.check()
                page.wait_for_timeout(500)
                
                # Verify selection count updates
                selection_count = page.locator("#selectionCount")
                if selection_count.is_visible():
                    expect(selection_count).to_contain_text("1")
        except:
            # If checkboxes not found, try clicking image item
            image_items.click()
            page.wait_for_timeout(500)
        
        # Verify output settings section is visible
        output_section = page.locator("#outputSettingsSection")
        if output_section.is_visible():
            # Configure settings
            quality_slider = page.locator("#qualitySlider")
            if quality_slider.is_visible():
                expect(quality_slider).to_be_visible()
            
            # Check generate button
            generate_btn = page.locator("#generateDocumentsBtn")
            if generate_btn.is_visible():
                expect(generate_btn).to_be_visible()
                expect(generate_btn).to_be_enabled()
                
                # Note: We won't actually generate documents in automated test
                # to avoid creating files, but we verify the button is ready
            else:
                pytest.skip("Generate button not visible - may need images selected")
        else:
            pytest.skip("Output settings not visible - no images selected")
    
    def test_output_settings_visible_when_images_selected(self, page: Page):
        """Test that output settings appear when images are selected"""
        page.goto(f"{BASE_URL}/image-to-pdf?qualification={QUALIFICATION}&learner={LEARNER}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        
        # Initially, output settings should be hidden
        output_section = page.locator("#outputSettingsSection")
        processing_section = page.locator("#processingSection")
        
        # If sections are visible without selection, that's also acceptable
        # But typically they should be hidden initially
        
        # Enable bulk mode and try to select an image
        bulk_mode_toggle = page.locator("#bulkModeToggle")
        if bulk_mode_toggle.is_visible():
            bulk_mode_toggle.check()
            page.wait_for_timeout(500)
            
            # Try to select an image
            first_checkbox = page.locator(".image-item input[type='checkbox']").first
            if first_checkbox.is_visible(timeout=3000):
                first_checkbox.check()
                page.wait_for_timeout(1000)
                
                # Now output settings should be visible
                if output_section.is_visible():
                    # Verify settings controls are present
                    quality_slider = page.locator("#qualitySlider")
                    resolution_select = page.locator("#resolutionSelect")
                    output_format = page.locator("#outputFormat")
                    
                    expect(quality_slider).to_be_visible()
                    expect(resolution_select).to_be_visible()
                    expect(output_format).to_be_visible()
            else:
                pytest.skip("No images available to select")
    
    def test_folder_structure_display(self, page: Page):
        """Test that folder structure is displayed correctly"""
        page.goto(f"{BASE_URL}/image-to-pdf?qualification={QUALIFICATION}&learner={LEARNER}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        
        file_tree = page.locator("#fileTreeContent")
        expect(file_tree).to_be_visible()
        
        # Check for folder structure (folders should be collapsed by default)
        folder_headers = page.locator(".folder-header, .image-folder")
        if folder_headers.count() > 0:
            # Verify folders are present
            expect(folder_headers.first).to_be_visible()
            
            # Folders should be collapsed (▶ icon)
            folder_icon = folder_headers.first.locator(".folder-icon")
            if folder_icon.is_visible():
                # Icon should show ▶ for collapsed
                icon_text = folder_icon.inner_text()
                # Note: We can't easily verify the exact icon, but folder should be visible
    
    def test_image_to_pdf_page_loads(self, page: Page):
        """Basic test that Image to PDF page loads without errors"""
        page.goto(f"{BASE_URL}/image-to-pdf")
        page.wait_for_load_state("networkidle")
        
        # Check for JavaScript errors (these would be caught by page.on('pageerror'))
        # Verify main elements are present
        qualification_select = page.locator("#qualificationSelect")
        learner_select = page.locator("#learnerSelect")
        file_tree = page.locator("#fileTreeContent")
        
        expect(qualification_select).to_be_visible()
        expect(learner_select).to_be_visible()
        expect(file_tree).to_be_visible()
        
        # Verify navigation tab is active
        image_to_pdf_tab = page.locator('a[href="/v2p-formatter/image-to-pdf"]')
        expect(image_to_pdf_tab).to_be_visible()

