#!/usr/bin/env python3
"""Debug drop zones"""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media?subfolder=lakhmaniuk", 
             wait_until="domcontentloaded")
    time.sleep(3)
    
    # Add text
    page.locator("#observationTextEditor").fill("Test with {{Unassigned_Placeholder}}.")
    time.sleep(1)
    
    # Check what's in the preview
    debug_info = page.evaluate("""
        () => {
            const preview = document.getElementById('observationPreview');
            if (!preview) return { error: 'No preview element' };
            
            // Find all tables
            const tables = Array.from(preview.querySelectorAll('table'));
            const unassignedTables = Array.from(preview.querySelectorAll('.placeholder-table.unassigned'));
            const containers = Array.from(preview.querySelectorAll('.unassigned-placeholder-container'));
            
            return {
                totalTables: tables.length,
                unassignedTables: unassignedTables.length,
                containers: containers.length,
                tableDetails: unassignedTables.map(t => ({
                    className: t.className,
                    dataPlaceholder: t.dataset.placeholder,
                    ondrop: t.getAttribute('ondrop'),
                    parentPlaceholder: t.closest('[data-placeholder]')?.dataset.placeholder
                })),
                containerDetails: containers.map(c => ({
                    dataPlaceholder: c.dataset.placeholder,
                    innerHTML: c.innerHTML.substring(0, 200)
                })),
                previewHTML: preview.innerHTML.substring(0, 500)
            };
        }
    """)
    
    import json
    print(json.dumps(debug_info, indent=2))
    
    page.screenshot(path="reports/screenshots/drop_zones_debug.png", full_page=True)
    
    time.sleep(3)
    browser.close()





