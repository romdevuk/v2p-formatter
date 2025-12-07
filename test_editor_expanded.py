#!/usr/bin/env python3
"""Test that text editor shows full textarea when expanded"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('http://localhost/v2p-formatter/observation-media', wait_until='networkidle')
        await asyncio.sleep(1)
        
        screenshot_dir = Path('reports/screenshots')
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Check collapsed state
        editor_section = await page.query_selector('.editor-section')
        editor_textarea = await page.query_selector('#observationTextEditor')
        
        if editor_section:
            classes = await editor_section.get_attribute('class') or ''
            is_collapsed = 'collapsed' in classes
            
            if is_collapsed:
                print(f"✓ Editor is collapsed initially")
                
                # Click to expand
                header = await page.query_selector('.editor-section-header')
                if header:
                    await header.click()
                    await asyncio.sleep(0.5)
                    
                    classes_after = await editor_section.get_attribute('class') or ''
                    is_collapsed_after = 'collapsed' in classes_after
                    
                    if editor_textarea:
                        box = await editor_textarea.bounding_box()
                        is_visible = await editor_textarea.is_visible()
                        
                        print(f"After click - collapsed: {is_collapsed_after}")
                        print(f"Textarea visible: {is_visible}")
                        if box:
                            print(f"Textarea height: {box['height']:.1f}px")
                            print(f"Textarea width: {box['width']:.1f}px")
                            
                            if box['height'] >= 200:
                                print("✓ Textarea has proper height when expanded")
                            else:
                                print(f"✗ Textarea height is too small: {box['height']:.1f}px")
                        
                        await page.screenshot(path=str(screenshot_dir / 'editor_expanded.png'), full_page=True)
                        print("\n✓ Screenshot saved")
        else:
            print("Editor section not found!")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test())


