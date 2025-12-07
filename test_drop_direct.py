#!/usr/bin/env python3
"""Test drop by directly calling assignment"""
from playwright.sync_api import sync_playwright
import time
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media?subfolder=lakhmaniuk", 
             wait_until="domcontentloaded")
    time.sleep(3)
    
    # Setup
    page.locator("#observationTextEditor").fill("Test with {{Unassigned_Placeholder}}.")
    time.sleep(1)
    
    # Get media
    media_info = page.evaluate("""
        () => {
            const card = document.querySelector('.observation-media-card:not(.media-assigned)');
            return card ? {
                path: card.dataset.mediaPath,
                name: card.dataset.mediaName,
                type: card.dataset.mediaType
            } : null;
        }
    """)
    
    print(f"Media: {media_info}")
    
    if media_info:
        # Test direct assignment
        result = page.evaluate(f"""
            () => {{
                const media = {json.dumps(media_info)};
                const placeholder = 'unassigned_placeholder';
                
                console.log('[TEST] Assigning media:', media);
                console.log('[TEST] To placeholder:', placeholder);
                
                const before = (window.getCurrentAssignments()[placeholder] || []).length;
                console.log('[TEST] Before count:', before);
                
                const result = window.assignMediaToPlaceholder(placeholder, media);
                console.log('[TEST] Assignment result:', result);
                
                if (window.updatePreview) {{
                    window.updatePreview();
                }}
                
                const after = (window.getCurrentAssignments()[placeholder] || []).length;
                console.log('[TEST] After count:', after);
                
                const assigned = window.getCurrentAssignments()[placeholder] || [];
                console.log('[TEST] Assigned media:', assigned.map(m => m.name));
                
                return {{
                    success: result,
                    before,
                    after,
                    assigned: assigned.map(m => m.name)
                }};
            }}
        """)
        
        print(f"\nResult: {json.dumps(result, indent=2)}")
        
        # Check if drop zone disappeared
        time.sleep(1)
        remaining_zones = page.evaluate("""
            () => document.querySelectorAll('.placeholder-table.unassigned').length
        """)
        print(f"\nRemaining drop zones: {remaining_zones}")
        
        if result.get('success') and result.get('after', 0) > 0:
            print("✅ Direct assignment works!")
            if remaining_zones == 0:
                print("✅ Drop zone disappeared (media assigned)")
        else:
            print("❌ Direct assignment failed")
    
    page.screenshot(path="reports/screenshots/drop_direct_test.png", full_page=True)
    time.sleep(3)
    browser.close()


