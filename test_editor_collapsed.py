#!/usr/bin/env python3
"""Test that text editor is collapsed by default"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('http://localhost/v2p-formatter/observation-media', wait_until='networkidle')
        await asyncio.sleep(1)
        
        editor_section = await page.query_selector('.editor-section')
        if editor_section:
            classes = await editor_section.get_attribute('class') or ''
            has_collapsed = 'collapsed' in classes
            editor_content = await page.query_selector('.editor-section-content-wrapper')
            is_visible = await editor_content.is_visible() if editor_content else False
            
            screenshot_dir = Path('reports/screenshots')
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=str(screenshot_dir / 'editor_collapsed_default.png'), full_page=True)
            
            print(f"Editor section has 'collapsed' class: {has_collapsed}")
            print(f"Editor content wrapper visible: {is_visible}")
            
            if has_collapsed and not is_visible:
                print("✓ Editor is collapsed by default")
            else:
                print("✗ Editor is NOT collapsed by default")
        else:
            print("Editor section not found!")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test())


