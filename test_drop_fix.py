#!/usr/bin/env python3
"""Test the drop fix"""
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
    
    # Get media card info
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
    
    print(f"Media to drop: {media_info}")
    
    # Simulate drop with proper data structure
    result = page.evaluate(f"""
        () => {{
            const media = {json.dumps(media_info)};
            const placeholder = 'unassigned_placeholder';
            
            // Get drop zone
            const dropZone = document.querySelector('.placeholder-table.unassigned');
            if (!dropZone) {{
                return {{ error: 'Drop zone not found' }};
            }}
            
            // Create proper dataTransfer
            const dataTransfer = {{
                data: {{}},
                setData: function(type, value) {{ this.data[type] = value; }},
                getData: function(type) {{ return this.data[type] || ''; }},
                effectAllowed: 'copy',
                dropEffect: 'copy'
            }};
            
            // Set data (same as handleMediaDragStart does)
            dataTransfer.setData('application/json', JSON.stringify(media));
            
            // Create drop event
            const dropEvent = new Event('drop', {{ bubbles: true, cancelable: true }});
            Object.defineProperty(dropEvent, 'dataTransfer', {{ 
                value: dataTransfer, 
                writable: false,
                configurable: true
            }});
            Object.defineProperty(dropEvent, 'target', {{ 
                value: dropZone, 
                writable: false 
            }});
            Object.defineProperty(dropEvent, 'currentTarget', {{ 
                value: dropZone, 
                writable: false 
            }});
            
            dropEvent.preventDefault = () => {{}};
            dropEvent.stopPropagation = () => {{}};
            
            // Get before state
            const before = (window.getCurrentAssignments()[placeholder] || []).length;
            
            // Call handler directly
            try {{
                window.handleTableDrop(dropEvent, placeholder);
            }} catch (err) {{
                return {{ error: err.message, stack: err.stack }};
            }}
            
            // Wait and check
            return new Promise(resolve => {{
                setTimeout(() => {{
                    const after = (window.getCurrentAssignments()[placeholder] || []).length;
                    const assigned = window.getCurrentAssignments()[placeholder] || [];
                    resolve({{
                        before,
                        after,
                        changed: before !== after,
                        assigned: assigned.map(m => m.name)
                    }});
                }}, 500);
            }});
        }}
    """)
    
    import asyncio
    if hasattr(result, '__await__'):
        result = asyncio.run(result)
    
    print(f"\nResult: {json.dumps(result, indent=2)}")
    
    if result.get('changed'):
        print("✅ Drop works!")
    else:
        print("❌ Drop failed")
        if result.get('error'):
            print(f"  Error: {result['error']}")
    
    page.screenshot(path="reports/screenshots/drop_fix_test.png", full_page=True)
    time.sleep(3)
    browser.close()


