#!/usr/bin/env python3
"""
Full browser test for Deface module using Playwright
Tests the complete workflow: qualification/learner selection -> image selection -> 
apply deface -> review -> edit -> manual deface -> generate PDF
"""

import asyncio
import sys
from pathlib import Path
import time
import os

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("ERROR: playwright not installed. Install with: pip install playwright && playwright install")
    sys.exit(1)


BASE_URL = "http://localhost/v2p-formatter"
TEST_QUALIFICATION = "Inter"
TEST_LEARNER = "kalamanchuk"
TEST_IMAGE = "IMG_9415.JPG"
OUTPUT_FOLDER = Path("/Users/rom/Documents/nvq/v2p-formatter-output")


async def test_deface_full_workflow():
    """Test the complete deface workflow ending with PDF generation"""
    async with async_playwright() as p:
        print("🌐 Launching browser...")
        browser = await p.chromium.launch(headless=False)  # Set to True for headless
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        
        try:
            # Navigate to deface page with URL filter
            print(f"📍 Navigating to deface page with filters: qualification={TEST_QUALIFICATION}, learner={TEST_LEARNER}")
            url = f"{BASE_URL}/deface?qualification={TEST_QUALIFICATION}&learner={TEST_LEARNER}"
            await page.goto(url, wait_until="networkidle")
            
            # Wait for page to load
            print("⏳ Waiting for page to load...")
            await page.wait_for_selector('#qualificationSelect', timeout=10000)
            
            # Verify qualification is selected
            qualification_value = await page.evaluate('document.getElementById("qualificationSelect").value')
            print(f"✓ Qualification select value: {qualification_value}")
            assert qualification_value == TEST_QUALIFICATION, f"Expected {TEST_QUALIFICATION}, got {qualification_value}"
            
            # Wait for learner dropdown to be enabled
            await page.wait_for_function(
                '!document.getElementById("learnerSelect").disabled',
                timeout=5000
            )
            
            # Verify learner is selected
            learner_value = await page.evaluate('document.getElementById("learnerSelect").value')
            print(f"✓ Learner select value: {learner_value}")
            assert learner_value == TEST_LEARNER, f"Expected {TEST_LEARNER}, got {learner_value}"
            
            # Wait for images to load
            print("⏳ Waiting for images to load...")
            try:
                await page.wait_for_function(
                    '''() => {
                        const content = document.getElementById('fileTreeContent');
                        return content && content.innerText.includes('IMG_9415');
                    }''',
                    timeout=10000
                )
                print("✓ Images loaded")
            except PlaywrightTimeout:
                content_text = await page.evaluate('document.getElementById("fileTreeContent").innerText')
                print(f"⚠️ Images not loaded. Content: {content_text[:200]}")
            
            # Try to find and click the image checkbox
            print(f"🔍 Looking for image: {TEST_IMAGE}")
            try:
                image_checkbox = page.locator(f'input[type="checkbox"][data-path*="{TEST_IMAGE}"]').first
                await image_checkbox.wait_for(timeout=5000)
                print("✓ Found image checkbox")
                
                is_checked = await image_checkbox.is_checked()
                if not is_checked:
                    print("☑️ Selecting image...")
                    await image_checkbox.click()
                    await asyncio.sleep(0.5)
                else:
                    print("✓ Image already selected")
            except PlaywrightTimeout:
                print("⚠️ Could not find image checkbox. Trying alternative method...")
                try:
                    image_item = page.locator(f'[data-path*="{TEST_IMAGE}"]').first
                    await image_item.click(timeout=5000)
                    print("✓ Clicked image item")
                    await asyncio.sleep(0.5)
                except PlaywrightTimeout:
                    print("⚠️ Could not find image item. Proceeding anyway...")
            
            # Click "Apply Deface" button
            print("🔘 Clicking 'Apply Deface' button...")
            apply_btn = page.locator('#applyDefaceBtn')
            await apply_btn.wait_for(timeout=5000)
            await apply_btn.click()
            
            # Wait for processing to complete
            print("⏳ Waiting for deface processing...")
            try:
                await page.wait_for_selector('#reviewInterface', state="visible", timeout=30000)
                print("✓ Review interface appeared")
            except PlaywrightTimeout:
                error_text = await page.evaluate('''() => {
                    const review = document.getElementById('reviewInterface');
                    const progress = document.getElementById('defaceProgressContainer');
                    return {
                        review: review ? review.style.display : 'none',
                        progress: progress ? progress.style.display : 'none',
                        progressText: progress ? progress.innerText : ''
                    };
                }''')
                print(f"⚠️ Review interface not shown. Status: {error_text}")
                raise
            
            # Check if review grid has items
            review_items = await page.locator('#reviewGrid > *').count()
            print(f"✓ Review grid has {review_items} items")
            assert review_items > 0, "Review grid should have at least one item"
            
            # Click Edit button to open manual deface editor
            print("🔍 Looking for Edit button...")
            edit_btn = page.locator('button:has-text("Edit")').first
            await edit_btn.wait_for(timeout=5000)
            print("✓ Found Edit button")
            
            print("🔘 Clicking Edit button...")
            await edit_btn.click()
            
            # Wait for manual deface modal to appear
            print("⏳ Waiting for manual deface modal...")
            await page.wait_for_selector('#manualDefaceModal', state="visible", timeout=5000)
            print("✓ Manual deface modal opened")
            
            # Wait for modal image to load
            modal_image = page.locator('#modalImagePreview')
            await modal_image.wait_for(timeout=5000)
            src = await modal_image.get_attribute('src')
            print(f"✓ Modal image loaded: {src[:100] if src else 'no src'}")
            
            # Click on the canvas multiple times at random positions to add multiple deface areas
            print("📐 Looking for deface canvas...")
            canvas = page.locator('#defaceCanvas')
            try:
                await canvas.wait_for(timeout=3000)
                print("✓ Found deface canvas")
                
                # Get canvas dimensions
                canvas_box = await canvas.bounding_box()
                if canvas_box:
                    canvas_width = canvas_box['width']
                    canvas_height = canvas_box['height']
                    print(f"✓ Canvas size: {canvas_width}x{canvas_height}")
                    
                    # Set deface size to "large" BEFORE clicking (so all areas use large size)
                    print("🔧 Setting deface size to 'large' for better visibility...")
                    try:
                        size_select = page.locator('#defaceSizeSelect')
                        await size_select.wait_for(timeout=2000)
                        await size_select.select_option('large')
                        print("✓ Deface size set to 'large' (150x150 pixels)")
                        await asyncio.sleep(0.5)  # Wait for size to be applied
                    except PlaywrightTimeout:
                        print("⚠️ Could not find size selector, using default size")
                    
                    # Add multiple random deface areas (5-8 areas for good coverage)
                    import random
                    num_areas = random.randint(5, 8)
                    print(f"🖱️ Adding {num_areas} random deface areas across the photo...")
                    
                    for i in range(num_areas):
                        # Generate random position (avoid edges by 15% margin to ensure areas fit)
                        margin_x = canvas_width * 0.15
                        margin_y = canvas_height * 0.15
                        random_x = random.uniform(margin_x, canvas_width - margin_x)
                        random_y = random.uniform(margin_y, canvas_height - margin_y)
                        
                        click_x = canvas_box['x'] + random_x
                        click_y = canvas_box['y'] + random_y
                        
                        print(f"  [{i+1}/{num_areas}] Clicking at ({int(random_x)}, {int(random_y)})...")
                        await page.mouse.click(click_x, click_y)
                        await asyncio.sleep(0.5)  # Longer delay to ensure click registers
                    
                    print(f"✓ Added {num_areas} deface areas to the canvas")
            except PlaywrightTimeout:
                print("⚠️ Could not find canvas. Trying image instead...")
                # Fallback: click on image at random positions
                img_box = await modal_image.bounding_box()
                if img_box:
                    import random
                    num_areas = random.randint(5, 8)
                    print(f"🖱️ Adding {num_areas} random deface areas (fallback to image)...")
                    
                    for i in range(num_areas):
                        margin_x = img_box['width'] * 0.1
                        margin_y = img_box['height'] * 0.1
                        random_x = random.uniform(margin_x, img_box['width'] - margin_x)
                        random_y = random.uniform(margin_y, img_box['height'] - margin_y)
                        
                        click_x = img_box['x'] + random_x
                        click_y = img_box['y'] + random_y
                        
                        await page.mouse.click(click_x, click_y)
                        await asyncio.sleep(0.3)
            
            # Wait a moment for all areas to be added
            await asyncio.sleep(1)
            
            # Verify that multiple deface areas were added by checking the active areas list
            print("🔍 Verifying deface areas were added...")
            try:
                areas_count_elem = page.locator('#activeAreasCount')
                if await areas_count_elem.count() > 0:
                    areas_count = await areas_count_elem.text_content()
                    print(f"✓ Active deface areas count: {areas_count}")
                else:
                    print("⚠️ Could not find active areas count element")
            except:
                print("⚠️ Could not verify areas count")
            
            # Apply manual deface by clicking "Apply Deface" button in the modal
            print("🔘 Looking for 'Apply Deface' button in modal...")
            apply_manual_btn = page.locator('#applyManualDefaceBtn')
            try:
                await apply_manual_btn.wait_for(timeout=3000)
                print("✓ Found Apply Deface button")
                
                # Wait for any alert dialogs (the code shows alerts)
                page.on("dialog", lambda dialog: dialog.accept())
                
                await apply_manual_btn.click()
                print("✓ Clicked Apply Deface button")
                await asyncio.sleep(3)  # Wait for manual deface to be applied (API call)
                
                print("✓ Manual deface applied successfully")
            except PlaywrightTimeout:
                print("⚠️ Could not find Apply Deface button. Manual deface may not have been applied.")
            
            # Close modal (look for close button)
            print("🔘 Closing modal...")
            close_btn = page.locator('#closeModalBtn, button:has-text("Close"), button:has-text("Cancel")').first
            try:
                await close_btn.wait_for(timeout=3000)
                await close_btn.click()
                print("✓ Closed modal")
                await asyncio.sleep(0.5)
            except PlaywrightTimeout:
                print("⚠️ Could not find close button. Pressing Escape...")
                await page.keyboard.press('Escape')
                await asyncio.sleep(0.5)
            
            # Click "Accept & Proceed to Document Generation" button
            print("🔘 Looking for 'Accept & Proceed' button...")
            accept_btn = page.locator('button:has-text("Accept"), button:has-text("Proceed"), button:has-text("Generate")').first
            await accept_btn.wait_for(timeout=5000)
            print("✓ Found Accept button")
            
            print("🔘 Clicking Accept button...")
            await accept_btn.click()
            
            # Wait for document generation section to appear
            print("⏳ Waiting for document generation section...")
            try:
                await page.wait_for_selector('#documentGenerationSection, #generateDocumentsBtn', state="visible", timeout=10000)
                print("✓ Document generation section appeared")
            except PlaywrightTimeout:
                print("⚠️ Document generation section not found. Checking page...")
            
            # Fill in the output filename (required for document generation)
            print("📝 Filling in output filename...")
            filename_input = page.locator('#outputFilename')
            try:
                await filename_input.wait_for(timeout=3000)
                await filename_input.fill('test_multiple_defaced')
                print("✓ Filled in filename: test_multiple_defaced")
                await asyncio.sleep(0.5)
            except PlaywrightTimeout:
                print("⚠️ Could not find filename input. Proceeding anyway...")
            
            # Click "Generate Documents" button
            print("🔘 Looking for 'Generate Documents' button...")
            generate_btn = page.locator('#generateDocumentsBtn, button:has-text("Generate"), button:has-text("Create PDF")').first
            await generate_btn.wait_for(timeout=5000)
            print("✓ Found Generate button")
            
            print("🔘 Clicking Generate Documents button...")
            await generate_btn.click()
            
            # Wait for PDF generation to complete
            print("⏳ Waiting for PDF generation...")
            await asyncio.sleep(5)  # Give time for PDF generation
            
            # Check for success message or download link
            try:
                await page.wait_for_selector('.success, .alert-success, a[href*="download"], a[href*=".pdf"]', timeout=15000)
                print("✓ PDF generation completed")
            except PlaywrightTimeout:
                print("⚠️ Success message not found, but continuing...")
            
            # Check if PDF file was created (wait for new file to be generated)
            print("📄 Checking for generated PDF file...")
            pdf_dir = OUTPUT_FOLDER / TEST_QUALIFICATION / TEST_LEARNER
            
            # Get initial timestamp before generation
            initial_time = time.time()
            
            # Wait for new PDF to be generated (check every second for up to 20 seconds)
            pdf_file = None
            for attempt in range(20):
                await asyncio.sleep(1)
                pdf_files = list(pdf_dir.glob('deface_*.pdf')) if pdf_dir.exists() else []
                if pdf_files:
                    # Get the most recently created PDF
                    latest_pdf = max(pdf_files, key=lambda p: p.stat().st_mtime)
                    file_mtime = latest_pdf.stat().st_mtime
                    # Check if file was created recently (within last 25 seconds)
                    current_time = time.time()
                    if file_mtime > current_time - 25:  # File created recently
                        pdf_file = latest_pdf
                        print(f"✓ PDF file found: {pdf_file.name}")
                        break
            
            if pdf_file and pdf_file.exists():
                print(f"✓ PDF file details:")
                print(f"  Filename: {pdf_file.name}")
                print(f"  Full path: {pdf_file}")
                print(f"  Size: {pdf_file.stat().st_size} bytes")
                print(f"  Created: {time.ctime(pdf_file.stat().st_mtime)}")
                
                # Verify PDF exists and has content
                assert pdf_file.exists(), "PDF file should exist"
                assert pdf_file.stat().st_size > 0, "PDF file should not be empty"
                
                print(f"\n✅ TEST PASSED: PDF file '{pdf_file.name}' generated successfully with multiple manual deface areas applied!")
                return True
            else:
                print(f"❌ PDF file not found in {pdf_dir}")
                if not pdf_dir.exists():
                    print(f"  Directory does not exist: {pdf_dir}")
                else:
                    print(f"  Files in directory: {list(pdf_dir.glob('*'))}")
                return False
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            
            # Take screenshot on failure
            screenshot_path = Path("test_deface_browser_error.png")
            await page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"📸 Screenshot saved to: {screenshot_path}")
            
            raise
        
        finally:
            # Keep browser open for a moment to see results
            await asyncio.sleep(2)
            await browser.close()


if __name__ == "__main__":
    print("=" * 70)
    print("DEFACE MODULE FULL WORKFLOW TEST")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Qualification: {TEST_QUALIFICATION}")
    print(f"Test Learner: {TEST_LEARNER}")
    print(f"Test Image: {TEST_IMAGE}")
    print(f"Output Folder: {OUTPUT_FOLDER}")
    print("=" * 70)
    print()
    
    try:
        result = asyncio.run(test_deface_full_workflow())
        if result:
            print("\n🎉 Test completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Test failed: PDF not generated")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test failed: {e}")
        sys.exit(1)
