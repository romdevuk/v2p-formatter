#!/usr/bin/env python3
"""Test that text field is visible"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('http://localhost/v2p-formatter/observation-media', wait_until='networkidle')
        await asyncio.sleep(1)
        
        editor = await page.query_selector('#observationTextEditor')
        if editor:
            is_visible = await editor.is_visible()
            box = await editor.bounding_box()
            screenshot_dir = Path('reports/screenshots')
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=str(screenshot_dir / 'text_field_check.png'), full_page=True)
            
            print(f"Text editor:")
            print(f"  Visible: {is_visible}")
            if box:
                print(f"  Position: x={box['x']:.1f}, y={box['y']:.1f}")
                print(f"  Size: width={box['width']:.1f}, height={box['height']:.1f}")
            else:
                print("  No bounding box!")
        else:
            print("Text editor NOT found!")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test())


