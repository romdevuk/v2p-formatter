#!/usr/bin/env python3
"""
Test folder height and overlap issues
"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('http://localhost/v2p-formatter/observation-media', wait_until='networkidle')
        await asyncio.sleep(2)
        
        # Load media by selecting a subfolder
        subfolder_select = await page.query_selector('#observationSubfolderSelect')
        if subfolder_select:
            # Get available options
            options = await subfolder_select.query_selector_all('option')
            if len(options) > 1:  # Skip first "Select Subfolder..." option
                value = await options[1].get_attribute('value')
                if value:
                    await subfolder_select.select_option(value)
                    await asyncio.sleep(1)
                    # Click load button
                    load_btn = await page.query_selector('button:has-text("Load")')
                    if load_btn:
                        await load_btn.click()
                        await asyncio.sleep(2)  # Wait for media to load
        
        screenshot_dir = Path('reports/screenshots')
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Take initial screenshot (all collapsed)
        await page.screenshot(path=str(screenshot_dir / 'folder_test_1_all_collapsed.png'), full_page=True)
        print("✓ Screenshot 1: All folders collapsed")
        
        # Check collapsed folder heights
        collapsed_sections = await page.query_selector_all('.media-subfolder-section.collapsed')
        print(f"\nFound {len(collapsed_sections)} collapsed folders")
        
        for i, section in enumerate(collapsed_sections[:3]):  # Check first 3
            box = await section.bounding_box()
            if box:
                header = await section.query_selector('.media-subfolder-header')
                content = await section.query_selector('.media-subfolder-content')
                header_box = await header.bounding_box() if header else None
                content_visible = await content.is_visible() if content else False
                
                print(f"  Folder {i+1}:")
                print(f"    Total height: {box['height']:.1f}px")
                if header_box:
                    print(f"    Header height: {header_box['height']:.1f}px")
                print(f"    Content visible: {content_visible}")
                
                # Check if height is acceptable (should be close to header height)
                if header_box and box['height'] <= header_box['height'] + 5:
                    print(f"    ✓ Height is acceptable (within 5px of header)")
                else:
                    print(f"    ✗ Height is too large!")
        
        # Expand first folder
        if collapsed_sections:
            first_section = collapsed_sections[0]
            header = await first_section.query_selector('.media-subfolder-header')
            if header:
                await header.click()
                await asyncio.sleep(0.5)
                
                await page.screenshot(path=str(screenshot_dir / 'folder_test_2_first_expanded.png'), full_page=True)
                print("\n✓ Screenshot 2: First folder expanded")
                
                # Check for overlap
                all_sections = await page.query_selector_all('.media-subfolder-section')
                print(f"\nChecking {len(all_sections)} folders for overlap:")
                
                prev_bottom = None
                overlap_found = False
                
                for i, section in enumerate(all_sections):
                    box = await section.bounding_box()
                    if box:
                        print(f"  Folder {i+1}: y={box['y']:.1f}, height={box['height']:.1f}, bottom={box['y'] + box['height']:.1f}")
                        
                        if prev_bottom is not None:
                            gap = box['y'] - prev_bottom
                            if gap < -5:  # Negative gap means overlap
                                print(f"    ✗ OVERLAP DETECTED! Gap: {gap:.1f}px")
                                overlap_found = True
                            elif gap < 2:
                                print(f"    ⚠ Very small gap: {gap:.1f}px")
                            else:
                                print(f"    ✓ Proper spacing: {gap:.1f}px")
                        
                        prev_bottom = box['y'] + box['height']
                
                if not overlap_found:
                    print("\n✓ No overlap detected - folders are properly spaced")
                else:
                    print("\n✗ OVERLAP ISSUE - folders are overlapping!")
        
        # Expand second folder to check multiple expanded
        if len(collapsed_sections) > 1:
            second_section = collapsed_sections[1]
            header = await second_section.query_selector('.media-subfolder-header')
            if header:
                await header.click()
                await asyncio.sleep(0.5)
                
                await page.screenshot(path=str(screenshot_dir / 'folder_test_3_two_expanded.png'), full_page=True)
                print("\n✓ Screenshot 3: Two folders expanded")
                
                # Check again for overlap
                all_sections = await page.query_selector_all('.media-subfolder-section')
                prev_bottom = None
                overlap_found = False
                
                print(f"\nRe-checking {len(all_sections)} folders for overlap:")
                for i, section in enumerate(all_sections):
                    box = await section.bounding_box()
                    if box:
                        if prev_bottom is not None:
                            gap = box['y'] - prev_bottom
                            if gap < -5:
                                print(f"  Folder {i+1}: ✗ OVERLAP! Gap: {gap:.1f}px")
                                overlap_found = True
                            elif gap >= 2:
                                print(f"  Folder {i+1}: ✓ Gap: {gap:.1f}px")
                        
                        prev_bottom = box['y'] + box['height']
                
                if not overlap_found:
                    print("\n✓ No overlap with multiple expanded folders")
        
        print(f"\n✓ All screenshots saved to {screenshot_dir}/")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test())

