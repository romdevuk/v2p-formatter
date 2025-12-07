#!/usr/bin/env python3
"""
Test script to verify Live Preview scrolling with actual content
"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def test_preview_scrolling():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        # Navigate to observation media page
        url = 'http://localhost/v2p-formatter/observation-media'
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until='networkidle')
        await asyncio.sleep(2)
        
        # Take initial screenshot
        screenshot_dir = Path('reports/screenshots')
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(screenshot_dir / 'preview_scroll_test_1_initial.png'), full_page=True)
        print("✓ Initial screenshot taken")
        
        # Add test content with many sections to force scrolling
        editor = await page.query_selector('#observationTextEditor')
        if editor:
            test_content = """1 - SITE ARRIVAL AND INDUCTION
Content for section 1 {{Image1}} {{Image2}} {{Image3}}

2 - HEALTH, SAFETY AND WELFARE
Content for section 2 {{Image4}} {{Image5}}

3 - COMMUNICATION AND WORK COORDINATION
Content for section 3 {{Image6}}

4 - RESOURCE HANDLING, MOVEMENT AND STORAGE
Content for section 4 {{Image7}} {{Image8}} {{Image9}}

5 - INSTALLATION OF DRYLINING SYSTEMS
Content for section 5 {{Image10}} {{Image11}}

6 - PLASTERBOARD FIXING
Content for section 6 {{Image12}} {{Image13}} {{Image14}} {{Image15}}

7 - WORKING AT HEIGHT
Content for section 7 {{Image16}} {{Image17}} {{Image18}} {{Image19}} {{Image20}}

8 - HOUSEKEEPING AND WASTE DISPOSAL
Content for section 8 {{Image21}} {{Image22}}

9 - ADDITIONAL SECTION 1
Content for additional section 1 {{Image23}} {{Image24}} {{Image25}}

10 - ADDITIONAL SECTION 2
Content for additional section 2 {{Image26}} {{Image27}} {{Image28}}

11 - ADDITIONAL SECTION 3
Content for additional section 3 {{Image29}} {{Image30}} {{Image31}}

12 - ADDITIONAL SECTION 4
Content for additional section 4 {{Image32}} {{Image33}} {{Image34}}
"""
            await editor.fill(test_content)
            await editor.press('Enter')  # Trigger update
            await asyncio.sleep(1)
            
            # Trigger preview update
            await page.evaluate('updatePreview()')
            await asyncio.sleep(2)
            
            await page.screenshot(path=str(screenshot_dir / 'preview_scroll_test_2_with_content.png'), full_page=True)
            print("✓ Screenshot with content taken")
        
        # Check preview section
        preview_section_content = await page.query_selector('.preview-section-content')
        if preview_section_content:
            # Get computed styles and dimensions
            overflow_y = await preview_section_content.evaluate('el => window.getComputedStyle(el).overflowY')
            height = await preview_section_content.evaluate('el => window.getComputedStyle(el).height')
            scroll_height = await preview_section_content.evaluate('el => el.scrollHeight')
            client_height = await preview_section_content.evaluate('el => el.clientHeight')
            scroll_top = await preview_section_content.evaluate('el => el.scrollTop')
            
            print(f"\nPreview Section Content:")
            print(f"  overflow-y: {overflow_y}")
            print(f"  height: {height}")
            print(f"  scrollHeight: {scroll_height}px")
            print(f"  clientHeight: {client_height}px")
            print(f"  scrollTop: {scroll_top}px")
            print(f"  Needs scroll: {scroll_height > client_height}")
            
            if scroll_height > client_height:
                print(f"  ✓ Content exceeds viewport ({scroll_height - client_height}px overflow)")
                
                # Scroll to bottom
                await preview_section_content.evaluate('el => el.scrollTop = el.scrollHeight')
                await asyncio.sleep(0.5)
                scroll_top_bottom = await preview_section_content.evaluate('el => el.scrollTop')
                print(f"  Scrolled to bottom, scrollTop: {scroll_top_bottom}px")
                
                await page.screenshot(path=str(screenshot_dir / 'preview_scroll_test_3_scrolled_bottom.png'), full_page=True)
                print("✓ Screenshot at bottom taken")
                
                # Check if scrollbar is visible
                scrollbar_width = await preview_section_content.evaluate('el => el.offsetWidth - el.clientWidth')
                print(f"  Scrollbar width: {scrollbar_width}px")
                
                if scrollbar_width > 0:
                    print("  ✓ Scrollbar is visible")
                else:
                    print("  ❌ Scrollbar is NOT visible (width = 0)")
            else:
                print("  ⚠️  Content fits in viewport, no scrolling needed")
        
        # Check observation sections
        sections = await page.query_selector_all('.observation-section')
        print(f"\nFound {len(sections)} observation sections")
        
        if sections:
            for i, section in enumerate(sections[:5]):  # Check first 5 sections
                is_visible = await section.is_visible()
                bounding_box = await section.bounding_box()
                if bounding_box:
                    print(f"  Section {i+1}: visible={is_visible}, y={bounding_box['y']:.1f}, height={bounding_box['height']:.1f}")
        
        # Final screenshot
        await page.screenshot(path=str(screenshot_dir / 'preview_scroll_test_4_final.png'), full_page=True)
        print("\n✓ All screenshots saved to reports/screenshots/")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_preview_scrolling())


