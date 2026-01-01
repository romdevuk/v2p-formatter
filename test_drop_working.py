#!/usr/bin/env python3
"""
Test actual drop functionality into unassigned placeholder
"""
from playwright.sync_api import sync_playwright
import time
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    try:
        print("=" * 60)
        print("DROP FUNCTIONALITY TEST")
        print("=" * 60)
        
        page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media?subfolder=lakhmaniuk", 
                 wait_until="domcontentloaded")
        time.sleep(3)
        
        # Add text with unassigned placeholder
        print("\n[1] Setting up...")
        page.locator("#observationTextEditor").fill("Test with {{Unassigned_Placeholder}}.")
        time.sleep(1)
        
        # Get media card and drop zone
        print("\n[2] Finding elements...")
        elements = page.evaluate("""
            () => {
                const card = document.querySelector('.observation-media-card:not(.media-assigned)');
                const dropZone = document.querySelector('.placeholder-table.unassigned');
                
                return {
                    hasCard: !!card,
                    cardPath: card ? card.dataset.mediaPath : null,
                    cardName: card ? card.dataset.mediaName : null,
                    hasDropZone: !!dropZone,
                    dropZoneOndrop: dropZone ? dropZone.getAttribute('ondrop') : null,
                    containerPlaceholder: dropZone ? dropZone.closest('[data-placeholder]')?.dataset.placeholder : null
                };
            }
        """)
        print(f"  Elements: {json.dumps(elements, indent=2)}")
        
        if elements.get('hasCard') and elements.get('hasDropZone'):
            # Simulate drag and drop
            print("\n[3] Simulating drag and drop...")
            result = page.evaluate(f"""
                () => {{
                    const media = {{
                        path: '{elements['cardPath']}',
                        name: '{elements['cardName']}',
                        type: 'image'
                    }};
                    const placeholder = 'unassigned_placeholder';
                    
                    // Get before state
                    const before = (window.getCurrentAssignments()[placeholder] || []).length;
                    console.log('[TEST] Before:', before);
                    
                    // Create DataTransfer mock
                    const dataTransfer = {{
                        data: {{}},
                        setData: function(type, value) {{ this.data[type] = value; }},
                        getData: function(type) {{ return this.data[type] || ''; }},
                        effectAllowed: 'copy',
                        dropEffect: 'copy'
                    }};
                    
                    // Set drag data
                    dataTransfer.setData('application/json', JSON.stringify(media));
                    
                    // Get drop zone
                    const dropZone = document.querySelector('.placeholder-table.unassigned');
                    if (!dropZone) {{
                        return {{ error: 'Drop zone not found' }};
                    }}
                    
                    // Create and dispatch events
                    const dragStart = new Event('dragstart', {{ bubbles: true }});
                    Object.defineProperty(dragStart, 'dataTransfer', {{ value: dataTransfer, writable: false }});
                    
                    const dragOver = new Event('dragover', {{ bubbles: true, cancelable: true }});
                    Object.defineProperty(dragOver, 'dataTransfer', {{ value: dataTransfer, writable: false }});
                    dragOver.preventDefault = () => {{}};
                    
                    const drop = new Event('drop', {{ bubbles: true, cancelable: true }});
                    Object.defineProperty(drop, 'dataTransfer', {{ value: dataTransfer, writable: false }});
                    drop.preventDefault = () => {{}};
                    
                    // Try calling handleTableDrop directly
                    console.log('[TEST] Calling handleTableDrop directly...');
                    try {{
                        window.handleTableDrop(drop, placeholder);
                    }} catch (err) {{
                        console.error('[TEST] Error calling handleTableDrop:', err);
                        return {{ error: err.message }};
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
            
            print(f"  Result: {json.dumps(result, indent=2)}")
            
            if result.get('changed'):
                print("  ✅ Drop works!")
            else:
                print("  ❌ Drop didn't work")
        else:
            print("  ✗ Missing elements for test")
        
        page.screenshot(path="reports/screenshots/drop_working_test.png", full_page=True)
        print("\n✓ Screenshot saved")
        
        time.sleep(3)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        time.sleep(2)
        browser.close()





