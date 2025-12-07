#!/usr/bin/env python3
"""
Test script to verify Live Preview scrolling works correctly
"""
import asyncio
from playwright.async_api import async_playwright
import os
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
        await page.screenshot(path=str(screenshot_dir / 'preview_initial.png'), full_page=True)
        print("✓ Initial screenshot taken")
        
        # Check if preview section exists
        preview = await page.query_selector('#observationPreview')
        if not preview:
            print("❌ Preview element not found!")
            await browser.close()
            return
        
        # Check preview section content
        preview_section_content = await page.query_selector('.preview-section-content')
        if preview_section_content:
            print("✓ Preview section content found")
            
            # Get computed styles
            overflow_y = await preview_section_content.evaluate('el => window.getComputedStyle(el).overflowY')
            overflow_x = await preview_section_content.evaluate('el => window.getComputedStyle(el).overflowX')
            height = await preview_section_content.evaluate('el => window.getComputedStyle(el).height')
            max_height = await preview_section_content.evaluate('el => window.getComputedStyle(el).maxHeight')
            scroll_height = await preview_section_content.evaluate('el => el.scrollHeight')
            client_height = await preview_section_content.evaluate('el => el.clientHeight')
            
            print(f"  overflow-y: {overflow_y}")
            print(f"  overflow-x: {overflow_x}")
            print(f"  height: {height}")
            print(f"  max-height: {max_height}")
            print(f"  scrollHeight: {scroll_height}")
            print(f"  clientHeight: {client_height}")
            
            needs_scroll = scroll_height > client_height
            print(f"  Needs scroll: {needs_scroll}")
            
            if overflow_y != 'auto' and overflow_y != 'scroll':
                print(f"❌ overflow-y should be 'auto' or 'scroll', got '{overflow_y}'")
            
            if needs_scroll and overflow_y == 'auto':
                print("✓ Scrolling should be available")
            elif needs_scroll:
                print(f"⚠️  Content exceeds viewport but overflow-y is '{overflow_y}'")
        
        # Check observation sections
        sections = await page.query_selector_all('.observation-section')
        print(f"\nFound {len(sections)} observation sections")
        
        # Try to scroll the preview
        if preview_section_content:
            # Scroll to bottom
            await preview_section_content.evaluate('el => el.scrollTop = el.scrollHeight')
            await asyncio.sleep(0.5)
            await page.screenshot(path=str(screenshot_dir / 'preview_scrolled_bottom.png'), full_page=True)
            print("✓ Scrolled to bottom, screenshot taken")
            
            # Scroll back to top
            await preview_section_content.evaluate('el => el.scrollTop = 0')
            await asyncio.sleep(0.5)
            await page.screenshot(path=str(screenshot_dir / 'preview_scrolled_top.png'), full_page=True)
            print("✓ Scrolled to top, screenshot taken")
            
            # Check if scrollbar is visible
            scrollbar_width = await preview_section_content.evaluate('''
                el => {
                    return el.offsetWidth - el.clientWidth;
                }
            ''')
            print(f"Scrollbar width: {scrollbar_width}px (should be > 0 if visible)")
        
        # Check if any sections are cut off
        sections_info = []
        for i, section in enumerate(sections):
            bounding_box = await section.bounding_box()
            if bounding_box:
                sections_info.append({
                    'index': i,
                    'top': bounding_box['y'],
                    'bottom': bounding_box['y'] + bounding_box['height'],
                    'height': bounding_box['height']
                })
        
        if sections_info:
            print(f"\nSection positions:")
            for info in sections_info:
                print(f"  Section {info['index']}: top={info['top']:.1f}, bottom={info['bottom']:.1f}, height={info['height']:.1f}")
        
        # Final screenshot
        await page.screenshot(path=str(screenshot_dir / 'preview_final.png'), full_page=True)
        print("\n✓ All screenshots saved to reports/screenshots/")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_preview_scrolling())


