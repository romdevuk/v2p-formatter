"""
Browser-based test for DOCX export with screenshots
Tests the actual export functionality through the web interface
"""
import os
import time
from pathlib import Path

# Try to import playwright
try:
    from playwright.sync_api import sync_playwright, expect
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not available, skipping browser tests")

BASE_URL = os.environ.get('TEST_URL', 'http://localhost:5000/v2p-formatter')
OUTPUT_FOLDER = Path('/Users/rom/Documents/nvq/v2p-formatter-output')

def test_docx_export_with_screenshots():
    """Test DOCX export through browser and take screenshots"""
    
    if not PLAYWRIGHT_AVAILABLE:
        print("Skipping browser test - Playwright not available")
        return
    
    # Create screenshots directory
    screenshots_dir = Path('reports/screenshots')
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Visible browser for debugging
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            accept_downloads=True
        )
        page = context.new_page()
        
        try:
            print("Navigating to observation-media page...")
            page.goto(f"{BASE_URL}/observation-media")
            page.wait_for_load_state('networkidle')
            
            # Wait for page elements
            page.wait_for_selector('#observationTextEditor', timeout=10000)
            time.sleep(1)
            page.screenshot(path=str(screenshots_dir / '01_page_loaded.png'), full_page=True)
            print("✓ Screenshot 1: Page loaded")
            
            # Enter test content
            text_editor = page.locator('#observationTextEditor')
            test_content = """Test document for media table formatting.

This is text before the first placeholder.

{{Image1}}

Text between placeholders.

{{Image2}}

Final text section."""
            
            text_editor.fill(test_content)
            time.sleep(0.5)
            page.screenshot(path=str(screenshots_dir / '02_text_entered.png'), full_page=True)
            print("✓ Screenshot 2: Text entered")
            
            # Select subfolder if available
            subfolder_select = page.locator('#observationSubfolderSelect')
            if subfolder_select.count() > 0:
                options = subfolder_select.locator('option').all()
                if len(options) > 1:
                    subfolder_select.select_option(index=1)
                    time.sleep(2)  # Wait for media to load
                    page.screenshot(path=str(screenshots_dir / '03_subfolder_selected.png'), full_page=True)
                    print("✓ Screenshot 3: Subfolder selected")
            
            # Show preview
            preview_btn = page.locator('#previewDraftBtn')
            if preview_btn.is_visible():
                preview_btn.click()
                time.sleep(1.5)
                page.screenshot(path=str(screenshots_dir / '04_preview_modal.png'), full_page=True)
                print("✓ Screenshot 4: Preview modal")
                
                # Close preview
                close_btn = page.locator('button:has-text("Close")')
                if close_btn.is_visible():
                    close_btn.click()
                    time.sleep(0.5)
            
            # Export DOCX
            export_btn = page.locator('#exportDocxBtn')
            print("\nExporting DOCX...")
            
            with page.expect_download() as download_info:
                export_btn.click()
                time.sleep(3)  # Wait for download
            
            download = download_info.value
            
            # Save file
            download_path = OUTPUT_FOLDER / download.suggested_filename
            if not download_path.suffix == '.docx':
                download_path = download_path.with_suffix('.docx')
            
            download.save_as(download_path)
            time.sleep(1)
            
            page.screenshot(path=str(screenshots_dir / '05_export_complete.png'), full_page=True)
            print("✓ Screenshot 5: Export complete")
            
            # Verify file
            if download_path.exists():
                file_size = download_path.stat().st_size
                print(f"\n✓ File saved: {download_path.name}")
                print(f"  Size: {file_size} bytes")
                print(f"  Extension: {download_path.suffix}")
                
                # Analyze DOCX structure
                analyze_docx(download_path)
            else:
                print(f"\n✗ File not saved: {download_path}")
            
            print(f"\n✓ All screenshots saved in: {screenshots_dir}")
            
        except Exception as e:
            print(f"\n✗ Error during test: {e}")
            import traceback
            traceback.print_exc()
            page.screenshot(path=str(screenshots_dir / 'error_screenshot.png'), full_page=True)
        
        finally:
            time.sleep(2)  # Keep browser open briefly to see result
            browser.close()


def analyze_docx(docx_path: Path):
    """Analyze DOCX file structure"""
    from zipfile import ZipFile
    import xml.etree.ElementTree as ET
    
    try:
        with ZipFile(docx_path, 'r') as zip_file:
            doc_xml = zip_file.read('word/document.xml')
            root = ET.fromstring(doc_xml)
            
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            tables = root.findall('.//w:tbl', ns)
            print(f"\nDOCX Analysis:")
            print(f"  Tables: {len(tables)}")
            
            for i, table in enumerate(tables):
                tbl_pr = table.find('w:tblPr', ns)
                if tbl_pr is not None:
                    tbl_width = tbl_pr.find('w:tblW', ns)
                    if tbl_width is not None:
                        width_val = tbl_width.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w')
                        width_type = tbl_width.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type')
                        
                        # Convert to readable format
                        if width_type == 'dxa':  # twips
                            width_twips = int(width_val)
                            width_inches = width_twips / 1440.0
                            print(f"  Table {i+1} width: {width_inches:.2f} inches ({width_val} twips)")
                        else:
                            print(f"  Table {i+1} width: {width_val} ({width_type})")
                
                rows = table.findall('.//w:tr', ns)
                if rows:
                    first_row = rows[0]
                    cells = first_row.findall('.//w:tc', ns)
                    print(f"  Table {i+1} columns: {len(cells)}")
                    
                    # Check column widths
                    for j, cell in enumerate(cells):
                        tc_pr = cell.find('w:tcPr', ns)
                        if tc_pr is not None:
                            tc_width = tc_pr.find('w:tcW', ns)
                            if tc_width is not None:
                                c_width = tc_width.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w')
                                c_type = tc_width.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type')
                                if c_type == 'dxa':
                                    c_inches = int(c_width) / 1440.0
                                    print(f"    Column {j+1}: {c_inches:.2f} inches")
            
            paragraphs = root.findall('.//w:p', ns)
            images = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip',
                                 {'': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
            print(f"  Paragraphs: {len(paragraphs)}")
            print(f"  Images: {len(images)}")
            
    except Exception as e:
        print(f"  Error analyzing DOCX: {e}")


if __name__ == '__main__':
    test_docx_export_with_screenshots()


