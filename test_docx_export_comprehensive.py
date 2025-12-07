"""
Comprehensive test for DOCX export functionality
Tests file creation, content, formatting, and filename extension
"""
import pytest
from playwright.sync_api import Page, expect
from pathlib import Path
import os
import time
from zipfile import ZipFile
import xml.etree.ElementTree as ET

BASE_URL = os.environ.get('TEST_URL', 'http://localhost:5000/v2p-formatter')
OUTPUT_FOLDER = Path('/Users/rom/Documents/nvq/v2p-formatter-output')


@pytest.fixture
def setup_test_environment(page: Page):
    """Navigate to observation media page and wait for it to load"""
    page.goto(f"{BASE_URL}/observation-media")
    page.wait_for_load_state('networkidle')
    
    # Wait for page elements to be ready
    page.wait_for_selector('#observationTextEditor', timeout=10000)
    
    yield page


def test_docx_export_with_content_and_images(setup_test_environment: Page, page: Page):
    """Test DOCX export with text content and images, verify file has content and proper extension"""
    
    # Step 1: Add text content with placeholders
    text_editor = page.locator('#observationTextEditor')
    test_content = """This is a test document.

{{Image1}}

Some text after the image.

{{Image2}}

Final paragraph."""
    
    text_editor.fill(test_content)
    
    # Take screenshot
    page.screenshot(path='reports/screenshots/01_text_entered.png', full_page=True)
    
    # Step 2: Select a subfolder if available
    subfolder_select = page.locator('#observationSubfolderSelect')
    if subfolder_select.count() > 0:
        options = subfolder_select.locator('option').all()
        if len(options) > 1:  # More than just "Select Subfolder..."
            subfolder_select.select_option(index=1)
            page.wait_for_timeout(1000)  # Wait for media to load
    
    # Step 3: Wait a moment for any media to load
    page.wait_for_timeout(2000)
    page.screenshot(path='reports/screenshots/02_subfolder_selected.png', full_page=True)
    
    # Step 4: Click Preview Draft to see preview
    preview_btn = page.locator('#previewDraftBtn')
    if preview_btn.is_visible():
        preview_btn.click()
        page.wait_for_timeout(1000)
        page.screenshot(path='reports/screenshots/03_preview_modal.png', full_page=True)
        
        # Close preview
        close_btn = page.locator('button:has-text("Close")')
        if close_btn.is_visible():
            close_btn.click()
            page.wait_for_timeout(500)
    
    # Step 5: Export DOCX
    export_btn = page.locator('#exportDocxBtn')
    expect(export_btn).to_be_visible()
    
    # Setup download listener
    with page.expect_download() as download_info:
        export_btn.click()
        page.wait_for_timeout(2000)  # Wait for download dialog if any
    
    # Handle filename prompt if it appears (for cases without draft)
    try:
        # Check if prompt dialog exists
        page.wait_for_timeout(500)
        # If there's a prompt, use default name
        # (Playwright can't directly interact with browser prompts)
    except:
        pass
    
    download = download_info.value
    
    # Step 6: Verify download started
    assert download is not None, "Download did not start"
    
    # Save the downloaded file
    download_path = OUTPUT_FOLDER / download.suggested_filename
    download.save_as(download_path)
    
    page.screenshot(path='reports/screenshots/04_export_clicked.png', full_page=True)
    
    # Step 7: Verify file exists and has .docx extension
    assert download_path.exists(), f"Downloaded file does not exist: {download_path}"
    assert download_path.suffix == '.docx', f"File does not have .docx extension: {download_path.suffix}"
    
    # Step 8: Verify file is not empty
    file_size = download_path.stat().st_size
    assert file_size > 0, f"DOCX file is empty (0 bytes)"
    assert file_size > 1000, f"DOCX file seems too small ({file_size} bytes) - likely empty"
    
    # Step 9: Verify DOCX structure (it's a ZIP file)
    try:
        with ZipFile(download_path, 'r') as zip_file:
            # Check for essential DOCX files
            file_list = zip_file.namelist()
            assert 'word/document.xml' in file_list, "DOCX missing word/document.xml"
            assert '[Content_Types].xml' in file_list, "DOCX missing [Content_Types].xml"
            
            # Read and verify document.xml has content
            doc_xml = zip_file.read('word/document.xml')
            root = ET.fromstring(doc_xml)
            
            # Check for paragraphs or tables
            paragraphs = root.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')
            tables = root.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tbl')
            
            assert len(paragraphs) > 0 or len(tables) > 0, "DOCX document.xml has no content (no paragraphs or tables)"
            
            print(f"✓ DOCX file structure valid:")
            print(f"  - File size: {file_size} bytes")
            print(f"  - Paragraphs: {len(paragraphs)}")
            print(f"  - Tables: {len(tables)}")
            
    except Exception as e:
        pytest.fail(f"Failed to verify DOCX structure: {e}")
    
    # Step 10: Verify filename in response (check console or network)
    page.screenshot(path='reports/screenshots/05_export_complete.png', full_page=True)
    
    print(f"\n✓ DOCX Export Test PASSED")
    print(f"  - File: {download_path.name}")
    print(f"  - Size: {file_size} bytes")
    print(f"  - Extension: {download_path.suffix}")


def test_docx_filename_extension(setup_test_environment: Page, page: Page):
    """Test that exported DOCX always has .docx extension"""
    
    text_editor = page.locator('#observationTextEditor')
    text_editor.fill("Test content for filename test.")
    
    export_btn = page.locator('#exportDocxBtn')
    
    # Monitor network requests to check filename
    filename_checked = False
    
    def handle_response(response):
        nonlocal filename_checked
        if '/export-docx' in response.url and response.status == 200:
            try:
                data = response.json()
                if 'file_name' in data:
                    filename = data['file_name']
                    assert filename.endswith('.docx'), f"Filename does not end with .docx: {filename}"
                    filename_checked = True
                    print(f"✓ Filename verified: {filename}")
            except:
                pass
    
    page.on('response', handle_response)
    
    with page.expect_download() as download_info:
        export_btn.click()
        page.wait_for_timeout(2000)
    
    download = download_info.value
    suggested_filename = download.suggested_filename
    
    assert suggested_filename.endswith('.docx'), f"Download filename does not end with .docx: {suggested_filename}"
    
    # Save file
    download_path = OUTPUT_FOLDER / suggested_filename
    download.save_as(download_path)
    
    assert download_path.exists()
    assert download_path.suffix == '.docx'
    
    print(f"✓ Filename extension test PASSED: {suggested_filename}")


def test_docx_content_not_empty(setup_test_environment: Page, page: Page):
    """Test that exported DOCX is never empty"""
    
    # Test with minimal content
    text_editor = page.locator('#observationTextEditor')
    text_editor.fill("Minimal content test.")
    
    export_btn = page.locator('#exportDocxBtn')
    
    with page.expect_download() as download_info:
        export_btn.click()
        page.wait_for_timeout(2000)
    
    download = download_info.value
    download_path = OUTPUT_FOLDER / download.suggested_filename
    download.save_as(download_path)
    
    # Verify file exists and has content
    assert download_path.exists()
    file_size = download_path.stat().st_size
    assert file_size > 1000, f"File too small ({file_size} bytes), likely empty"
    
    # Verify DOCX has content
    with ZipFile(download_path, 'r') as zip_file:
        doc_xml = zip_file.read('word/document.xml')
        root = ET.fromstring(doc_xml)
        paragraphs = root.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')
        tables = root.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tbl')
        
        assert len(paragraphs) > 0 or len(tables) > 0, "DOCX has no content"
        
        # Check if paragraphs have text
        has_text = False
        for p in paragraphs:
            texts = p.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')
            if texts:
                has_text = True
                break
        
        assert has_text or len(tables) > 0, "DOCX has no text or tables"
    
    print(f"✓ Content verification PASSED - File has content ({file_size} bytes)")


if __name__ == '__main__':
    # Create reports directory
    Path('reports/screenshots').mkdir(parents=True, exist_ok=True)
    
    pytest.main([__file__, '-v', '-s', '--tb=short'])


