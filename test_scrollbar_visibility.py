#!/usr/bin/env python3
"""
Test script to verify scrollbar is visible and properly styled
"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def test_scrollbar():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        # Navigate to observation media page
        url = 'http://localhost/v2p-formatter/observation-media'
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until='networkidle')
        await asyncio.sleep(2)
        
        # Add test content
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

9 - ADDITIONAL SECTION
More content here {{Image23}} {{Image24}}

10 - ANOTHER SECTION
Even more content {{Image25}} {{Image26}}
"""
            await editor.fill(test_content)
            await page.evaluate('updatePreview()')
            await asyncio.sleep(2)
        
        screenshot_dir = Path('reports/screenshots')
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Check preview section content
        preview = await page.query_selector('.preview-section-content')
        if preview:
            # Get scrollbar information
            scrollbar_info = await preview.evaluate('''
                el => {
                    const style = window.getComputedStyle(el);
                    const scrollbarWidth = el.offsetWidth - el.clientWidth;
                    const scrollHeight = el.scrollHeight;
                    const clientHeight = el.clientHeight;
                    const needsScroll = scrollHeight > clientHeight;
                    
                    // Check for webkit scrollbar styles
                    const testEl = document.createElement('div');
                    testEl.className = 'preview-section-content';
                    testEl.style.cssText = 'overflow-y: scroll; width: 200px; height: 100px;';
                    document.body.appendChild(testEl);
                    const testStyle = window.getComputedStyle(testEl, '::-webkit-scrollbar');
                    const scrollbarStyle = window.getComputedStyle(testEl);
                    document.body.removeChild(testEl);
                    
                    return {
                        overflowY: style.overflowY,
                        scrollbarWidth: scrollbarWidth,
                        scrollHeight: scrollHeight,
                        clientHeight: clientHeight,
                        needsScroll: needsScroll,
                        offsetWidth: el.offsetWidth,
                        clientWidth: el.clientWidth
                    };
                }
            ''')
            
            print(f"\nScrollbar Information:")
            print(f"  overflow-y: {scrollbar_info['overflowY']}")
            print(f"  scrollHeight: {scrollbar_info['scrollHeight']}px")
            print(f"  clientHeight: {scrollbar_info['clientHeight']}px")
            print(f"  offsetWidth: {scrollbar_info['offsetWidth']}px")
            print(f"  clientWidth: {scrollbar_info['clientWidth']}px")
            print(f"  scrollbarWidth: {scrollbar_info['scrollbarWidth']}px")
            print(f"  Needs scroll: {scrollbar_info['needsScroll']}")
            
            if scrollbar_info['needsScroll']:
                if scrollbar_info['scrollbarWidth'] >= 10:
                    print("  ✓ Scrollbar is visible and properly sized")
                else:
                    print(f"  ⚠️  Scrollbar width is only {scrollbar_info['scrollbarWidth']}px - should be at least 10px")
        
        # Take screenshot of preview area
        preview_box = await preview.bounding_box()
        if preview_box:
            await page.screenshot(
                path=str(screenshot_dir / 'preview_scrollbar_visible.png'),
                clip={
                    'x': preview_box['x'] - 50,
                    'y': preview_box['y'] - 50,
                    'width': preview_box['width'] + 100,
                    'height': preview_box['height'] + 100
                }
            )
            print("\n✓ Screenshot of preview area with scrollbar saved")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_scrollbar())


