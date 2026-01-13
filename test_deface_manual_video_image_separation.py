"""
Test that video manual deface is separate from image manual deface
"""
import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

BASE_URL = "http://localhost/v2p-formatter"
TEST_QUALIFICATION = "Inter"
TEST_LEARNER = "kalamanchuk"
TEST_IMAGE = "IMG_9415.JPG"

async def test_video_image_manual_deface_separation():
    """Test that video manual deface UI is separate from image manual deface UI"""
    async with async_playwright() as p:
        print("🌐 Launching browser...")
        browser = await p.chromium.launch(headless=False)  # Set to True for headless
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        
        try:
            # Navigate to deface page with URL filter
            print(f"\n📍 Navigating to deface page with filters: qualification={TEST_QUALIFICATION}, learner={TEST_LEARNER}")
            url = f"{BASE_URL}/deface?qualification={TEST_QUALIFICATION}&learner={TEST_LEARNER}"
            await page.goto(url, wait_until="networkidle")
            
            # Wait for page to load
            print("⏳ Waiting for page to load...")
            await page.wait_for_selector('#qualificationSelect', timeout=10000)
            
            # Verify qualification is selected
            qualification_value = await page.evaluate('document.getElementById("qualificationSelect").value')
            print(f"✓ Qualification select value: {qualification_value}")
            
            # Wait for learner dropdown to be enabled
            await page.wait_for_function(
                '!document.getElementById("learnerSelect").disabled',
                timeout=5000
            )
            
            # Verify learner is selected
            learner_value = await page.evaluate('document.getElementById("learnerSelect").value')
            print(f"✓ Learner select value: {learner_value}")
            
            # Wait for files to load
            print("⏳ Waiting for files to load...")
            try:
                # Wait for both image and video sections to be visible
                await page.wait_for_selector('#imageFilesList', state="visible", timeout=5000)
                await page.wait_for_selector('#videoFilesList', state="visible", timeout=5000)
                print("✓ Files loaded")
            except Exception as e:
                print(f"⚠️ Files not fully loaded: {e}")
                await page.wait_for_timeout(3000)
            
            # Try to find and click an image (like the existing test does)
            print(f"\n🔍 Looking for image: {TEST_IMAGE}")
            image_selected = False
            try:
                # Look for checkbox with data-path containing the image name
                image_checkbox = page.locator(f'input[type="checkbox"][data-path*="{TEST_IMAGE}"]').first
                try:
                    await image_checkbox.wait_for(timeout=5000)
                    print("  ✓ Found image checkbox")
                    is_checked = await image_checkbox.is_checked()
                    if not is_checked:
                        print("  ☑️ Selecting image...")
                        await image_checkbox.click()
                        await page.wait_for_timeout(500)
                    else:
                        print("  ✓ Image already selected")
                    image_selected = True
                except:
                    print("  ⚠️ Could not find image checkbox. Trying alternative method...")
                    # Try clicking on the image item itself
                    try:
                        image_item = page.locator(f'[data-path*="{TEST_IMAGE}"]').first
                        await image_item.click(timeout=5000)
                        print("  ✓ Clicked image item")
                        await page.wait_for_timeout(500)
                        image_selected = True
                    except:
                        image_selected = False
            except Exception as e:
                print(f"  ⚠️  Could not find image: {e}")
                
            # Try to find a video to select (separate from images)
            print("\n🔍 Looking for video...")
            video_selected = False
            try:
                video_item = page.locator('[data-path*=".mp4"], [data-path*=".MP4"]').first
                await video_item.wait_for(timeout=5000)
                print("  ✓ Found video item, clicking...")
                await video_item.click()
                await page.wait_for_timeout(500)
                video_selected = True
            except:
                print("  ⚠️  Could not find video item")
            
            if not image_selected and not video_selected:
                print("  ⚠️  No media files selected")
            
            # Apply deface
            print("\n✨ Applying deface...")
            apply_deface_btn = page.locator('#applyDefaceBtn')
            await apply_deface_btn.wait_for(state="visible", timeout=5000)
            await apply_deface_btn.click()
            
            # Wait for processing to complete (wait for review interface to appear)
            print("  ⏳ Waiting for deface processing...")
            try:
                await page.wait_for_selector('#reviewInterface', state="visible", timeout=30000)
                print("  ✓ Review interface appeared")
            except:
                print("  ⚠️  Review interface timeout, checking page state...")
            
            # Check for review grid
            print("\n🔍 Checking for review grid...")
            review_grid = page.locator('#reviewGrid')
            await review_grid.wait_for(state="visible", timeout=30000)
            await page.wait_for_timeout(2000)
            
            # Find Edit buttons
            edit_buttons = page.locator('button:has-text("Edit")')
            edit_count = await edit_buttons.count()
            print(f"  Found {edit_count} Edit buttons")
            
            if edit_count == 0:
                print("\n❌ TEST FAILED: No Edit buttons found in review grid")
                return False
            
            # Check what types of items are in the review grid by examining the rendered HTML
            # We'll test the first and last Edit buttons to check for different types
            print("\n🧪 Testing manual deface UI separation...")
            
            # Test all Edit buttons to verify UI separation
            tests_passed = 0
            tests_run = 0
            
            for i in range(min(edit_count, 5)):  # Test up to 5 items
                edit_btn = edit_buttons.nth(i)
                print(f"\n  Testing item {i+1}/{min(edit_count, 5)}...")
                
                await edit_btn.click()
                await page.wait_for_timeout(1000)
                
                # Check for manual deface modal
                modal = page.locator('#manualDefaceModal')
                await modal.wait_for(state="visible", timeout=5000)
                
                # Check video frame selection visibility
                video_frame_selection = page.locator('#videoFrameSelection')
                video_frame_visible = await video_frame_selection.is_visible()
                
                # Check image preview container visibility
                image_preview_container = page.locator('#imagePreviewContainer')
                image_preview_visible = await image_preview_container.is_visible()
                
                # Check for video player
                video_player = page.locator('#manualDefaceVideoPlayer')
                video_player_exists = await video_player.count() > 0
                
                # Determine item type based on UI state
                if video_frame_visible and video_player_exists:
                    # This is a video
                    print(f"    Item {i+1} is VIDEO")
                    print(f"      Video frame selection: {video_frame_visible} ✓")
                    print(f"      Image preview (should be hidden): {image_preview_visible} {'✓' if not image_preview_visible else '✗'}")
                    print(f"      Video player exists: {video_player_exists} ✓")
                    
                    if not image_preview_visible and video_frame_visible:
                        print(f"    ✅ Item {i+1}: Video UI correct")
                        tests_passed += 1
                    else:
                        print(f"    ❌ Item {i+1}: Video UI incorrect")
                    tests_run += 1
                else:
                    # This is an image
                    print(f"    Item {i+1} is IMAGE")
                    print(f"      Video frame selection (should be hidden): {video_frame_visible} {'✓' if not video_frame_visible else '✗'}")
                    print(f"      Image preview container: {image_preview_visible} ✓")
                    
                    if not video_frame_visible and image_preview_visible:
                        print(f"    ✅ Item {i+1}: Image UI correct")
                        tests_passed += 1
                    else:
                        print(f"    ❌ Item {i+1}: Image UI incorrect")
                    tests_run += 1
                
                # Close modal
                close_btn = page.locator('#closeModalBtn')
                await close_btn.click()
                await page.wait_for_timeout(500)
            
            print(f"\n📊 Test Results: {tests_passed}/{tests_run} items passed UI separation test")
            
            if tests_run == 0:
                print("\n❌ TEST FAILED: No items tested")
                return False
            
            if tests_passed < tests_run:
                print("\n❌ TEST FAILED: Some items failed UI separation test")
                return False
            
            print("\n✅ ALL TESTS PASSED: Video and image manual deface UIs are properly separated!")
            return True
            
        except PlaywrightTimeoutError as e:
            print(f"\n❌ TEST FAILED: Timeout error - {e}")
            await page.screenshot(path="test_deface_separation_timeout.png")
            return False
        except Exception as e:
            print(f"\n❌ TEST FAILED: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            await page.screenshot(path="test_deface_separation_error.png")
            return False
        finally:
            await browser.close()

if __name__ == "__main__":
    result = asyncio.run(test_video_image_manual_deface_separation())
    sys.exit(0 if result else 1)
