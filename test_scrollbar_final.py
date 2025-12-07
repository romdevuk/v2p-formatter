#!/usr/bin/env python3
"""
Final test for scrollbar visibility with screenshots
"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def test_scrollbar():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        url = 'http://localhost/v2p-formatter/observation-media'
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until='networkidle')
        await asyncio.sleep(2)
        
        # Add test content with many sections
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
"""
            await editor.fill(test_content)
            await page.evaluate('updatePreview()')
            await asyncio.sleep(2)
        
        screenshot_dir = Path('reports/screenshots')
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Inject CSS to force scrollbar visibility
        await page.add_style_tag(content='''
            .preview-section-content::-webkit-scrollbar {
                width: 14px !important;
            }
            .preview-section-content::-webkit-scrollbar-track {
                background: #1e1e1e !important;
            }
            .preview-section-content::-webkit-scrollbar-thumb {
                background: #888 !important;
                border-radius: 7px;
            }
        ''')
        await asyncio.sleep(0.5)
        
        # Check scrollbar
        preview = await page.query_selector('.preview-section-content')
        if preview:
            scrollbar_info = await preview.evaluate('''
                el => {
                    return {
                        scrollbarWidth: el.offsetWidth - el.clientWidth,
                        scrollHeight: el.scrollHeight,
                        clientHeight: el.clientHeight,
                        overflowY: window.getComputedStyle(el).overflowY
                    };
                }
            ''')
            
            print(f"\nScrollbar Info:")
            print(f"  overflow-y: {scrollbar_info['overflowY']}")
            print(f"  scrollHeight: {scrollbar_info['scrollHeight']}px")
            print(f"  clientHeight: {scrollbar_info['clientHeight']}px")
            print(f"  scrollbarWidth: {scrollbar_info['scrollbarWidth']}px")
            
            # Scroll to show sections
            await preview.evaluate('el => el.scrollTop = 0')
            await asyncio.sleep(0.5)
            await page.screenshot(path=str(screenshot_dir / 'scrollbar_test_top.png'), full_page=True)
            print("✓ Screenshot at top saved")
            
            await preview.evaluate('el => el.scrollTop = el.scrollHeight / 2')
            await asyncio.sleep(0.5)
            await page.screenshot(path=str(screenshot_dir / 'scrollbar_test_middle.png'), full_page=True)
            print("✓ Screenshot at middle saved")
            
            await preview.evaluate('el => el.scrollTop = el.scrollHeight')
            await asyncio.sleep(0.5)
            await page.screenshot(path=str(screenshot_dir / 'scrollbar_test_bottom.png'), full_page=True)
            print("✓ Screenshot at bottom saved")
            
            # Close-up of preview area
            preview_box = await preview.bounding_box()
            if preview_box:
                await page.screenshot(
                    path=str(screenshot_dir / 'scrollbar_test_closeup.png'),
                    clip={
                        'x': max(0, preview_box['x'] - 20),
                        'y': max(0, preview_box['y'] - 20),
                        'width': min(preview_box['width'] + 40, 1920),
                        'height': min(preview_box['height'] + 40, 1080)
                    }
                )
                print("✓ Close-up screenshot saved")
        
        print("\n✓ All screenshots saved to reports/screenshots/")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_scrollbar())


