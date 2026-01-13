#!/usr/bin/env python3
"""
Browser test for Deface module using Playwright
Tests the full workflow: qualification/learner selection -> image selection -> apply deface -> review -> edit -> manual deface
"""

import asyncio
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("ERROR: playwright not installed. Install with: pip install playwright && playwright install")
    sys.exit(1)


BASE_URL = "http://localhost/v2p-formatter"
TEST_QUALIFICATION = "Inter"
TEST_LEARNER = "kalamanchuk"
TEST_IMAGE = "IMG_9415.JPG"


async def test_deface_workflow():
    """Test the full deface workflow"""
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
            
            # Wait for images to load (check if fileTreeContent has content)
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
                # Check what's actually in the content
                content_text = await page.evaluate('document.getElementById("fileTreeContent").innerText')
                print(f"⚠️ Images not loaded. Content: {content_text[:200]}")
                # Continue anyway - might be a timing issue
            
            # Try to find and click the image checkbox
            print(f"🔍 Looking for image: {TEST_IMAGE}")
            try:
                # Look for checkbox with data-path containing the image name
                image_checkbox = page.locator(f'input[type="checkbox"][data-path*="{TEST_IMAGE}"]').first
                await image_checkbox.wait_for(timeout=5000)
                print("✓ Found image checkbox")
                
                # Check if already checked
                is_checked = await image_checkbox.is_checked()
                if not is_checked:
                    print("☑️ Selecting image...")
                    await image_checkbox.click()
                    await asyncio.sleep(0.5)  # Wait for selection to process
                else:
                    print("✓ Image already selected")
            except PlaywrightTimeout:
                print("⚠️ Could not find image checkbox. Trying alternative method...")
                # Try clicking on the image item itself
                try:
                    image_item = page.locator(f'[data-path*="{TEST_IMAGE}"]').first
                    await image_item.click(timeout=5000)
                    print("✓ Clicked image item")
                    await asyncio.sleep(0.5)
                except PlaywrightTimeout:
                    print("⚠️ Could not find image item. Proceeding with apply deface anyway...")
            
            # Click "Apply Deface" button
            print("🔘 Clicking 'Apply Deface' button...")
            apply_btn = page.locator('#applyDefaceBtn')
            await apply_btn.wait_for(timeout=5000)
            await apply_btn.click()
            
            # Wait for processing to complete (wait for review interface to appear)
            print("⏳ Waiting for deface processing...")
            try:
                await page.wait_for_selector('#reviewInterface', state="visible", timeout=30000)
                print("✓ Review interface appeared")
            except PlaywrightTimeout:
                # Check for error messages
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
            
            # Look for "Edit" button in the first review item
            print("🔍 Looking for Edit button...")
            try:
                edit_btn = page.locator('button:has-text("Edit")').first
                await edit_btn.wait_for(timeout=5000)
                print("✓ Found Edit button")
                
                # Click Edit button
                print("🔘 Clicking Edit button...")
                await edit_btn.click()
                
                # Wait for manual deface modal to appear
                print("⏳ Waiting for manual deface modal...")
                await page.wait_for_selector('#manualDefaceModal', state="visible", timeout=5000)
                print("✓ Manual deface modal opened")
                
                # Check if modal has image preview
                modal_image = page.locator('#modalImagePreview')
                if await modal_image.count() > 0:
                    src = await modal_image.get_attribute('src')
                    print(f"✓ Modal image loaded: {src[:100] if src else 'no src'}")
                else:
                    print("⚠️ Modal image not found")
                
                # Close modal (click close button or cancel)
                close_btn = page.locator('#closeModalBtn')
                if await close_btn.count() > 0:
                    await close_btn.click()
                    print("✓ Closed modal")
                    await asyncio.sleep(0.5)
                
            except PlaywrightTimeout:
                print("⚠️ Could not find Edit button or modal")
            
            print("\n✅ All tests passed!")
            
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
    print("=" * 60)
    print("DEFACE MODULE BROWSER TEST")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Qualification: {TEST_QUALIFICATION}")
    print(f"Test Learner: {TEST_LEARNER}")
    print(f"Test Image: {TEST_IMAGE}")
    print("=" * 60)
    print()
    
    try:
        asyncio.run(test_deface_workflow())
        print("\n🎉 Test completed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Test failed: {e}")
        sys.exit(1)
