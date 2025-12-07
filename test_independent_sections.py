#!/usr/bin/env python3
"""Test that preview and editor sections are independent"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('http://localhost/v2p-formatter/observation-media', wait_until='networkidle')
        await asyncio.sleep(1)
        
        # Add test content
        editor = await page.query_selector('#observationTextEditor')
        if editor:
            test_content = """1 - SITE ARRIVAL AND INDUCTION
Content for section 1 {{Image1}} {{Image2}} {{Image3}}

2 - HEALTH, SAFETY AND WELFARE
Content for section 2 {{Image4}} {{Image5}}

3 - COMMUNICATION AND WORK COORDINATION
Content for section 3 {{Image6}}
"""
            await editor.fill(test_content)
            await page.evaluate('updatePreview()')
            await asyncio.sleep(1)
        
        # Check preview section
        preview_section = await page.query_selector('.preview-section')
        preview_content = await page.query_selector('.preview-section-content')
        editor_section = await page.query_selector('.editor-section')
        editor_element = await page.query_selector('#observationTextEditor')
        
        screenshot_dir = Path('reports/screenshots')
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(screenshot_dir / 'independent_sections.png'), full_page=True)
        
        if preview_section:
            preview_box = await preview_section.bounding_box()
            print(f"Preview Section:")
            if preview_box:
                print(f"  Height: {preview_box['height']:.1f}px")
        
        if editor_section:
            editor_box = await editor_section.bounding_box()
            print(f"\nEditor Section:")
            if editor_box:
                print(f"  Height: {editor_box['height']:.1f}px")
        
        if preview_content:
            preview_info = await preview_content.evaluate('''
                el => ({
                    scrollHeight: el.scrollHeight,
                    clientHeight: el.clientHeight,
                    canScroll: el.scrollHeight > el.clientHeight
                })
            ''')
            print(f"\nPreview Content:")
            print(f"  scrollHeight: {preview_info['scrollHeight']}px")
            print(f"  clientHeight: {preview_info['clientHeight']}px")
            print(f"  Can scroll: {preview_info['canScroll']}")
        
        if editor_element:
            editor_info = await editor_element.evaluate('''
                el => ({
                    scrollHeight: el.scrollHeight,
                    clientHeight: el.clientHeight,
                    canScroll: el.scrollHeight > el.clientHeight
                })
            ''')
            print(f"\nEditor Element:")
            print(f"  scrollHeight: {editor_info['scrollHeight']}px")
            print(f"  clientHeight: {editor_info['clientHeight']}px")
            print(f"  Can scroll: {editor_info['canScroll']}")
        
        print("\n✓ Screenshot saved to reports/screenshots/independent_sections.png")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test())


