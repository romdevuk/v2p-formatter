#!/usr/bin/env python3
"""
Manual test of reshuffle functionality - directly calls JavaScript functions
to verify reordering works
"""
from playwright.sync_api import sync_playwright
import time
import json

def test_reshuffle_manual():
    """Test reshuffle by directly calling JavaScript functions"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            # Navigate to observation media
            print("Navigating to observation media page...")
            page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media", 
                     wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            
            # Add text with placeholder
            print("Adding text with placeholder...")
            text_editor = page.locator("#observationTextEditor")
            if text_editor.count() > 0:
                text_editor.fill("Test with {{Test_Placeholder}}")
                time.sleep(1)
            
            # Assign 3 media items
            print("Assigning 3 media items...")
            result = page.evaluate("""
                () => {
                    if (!window.observationMediaAssignments) {
                        window.observationMediaAssignments = {};
                    }
                    
                    window.observationMediaAssignments['test_placeholder'] = [
                        { path: '/test1.jpg', name: 'test1.jpg', type: 'image' },
                        { path: '/test2.jpg', name: 'test2.jpg', type: 'image' },
                        { path: '/test3.jpg', name: 'test3.jpg', type: 'image' }
                    ];
                    
                    if (window.updatePreview) {
                        window.updatePreview();
                    }
                    
                    return window.observationMediaAssignments['test_placeholder'].map(m => m.name);
                }
            """)
            print(f"Initial order: {result}")
            
            time.sleep(1)
            
            # Enable reshuffle
            print("Enabling reshuffle...")
            reshuffle_btn = page.locator("#reshuffleBtn")
            if reshuffle_btn.count() > 0 and reshuffle_btn.is_visible():
                reshuffle_btn.click()
                time.sleep(1)
            
            # Get current order
            order_before = page.evaluate("""
                () => {
                    const assignments = window.getCurrentAssignments();
                    return assignments['test_placeholder'] ? assignments['test_placeholder'].map(m => m.name) : [];
                }
            """)
            print(f"Order before reorder: {order_before}")
            
            # Manually call reorderMediaInPlaceholder to test the function
            print("Manually calling reorderMediaInPlaceholder...")
            
            # Collect console messages
            console_messages = []
            def handle_console(msg):
                console_messages.append(msg.text)
            page.on("console", handle_console)
            
            reorder_result = page.evaluate("""
                () => {
                    const assignments = window.getCurrentAssignments();
                    const placeholder = 'test_placeholder';
                    
                    console.log('[TEST] Before reorder:', assignments[placeholder].map(m => m.name));
                    
                    // Get a target cell - try multiple selectors
                    let cells = document.querySelectorAll('.media-cell[data-placeholder="test_placeholder"]');
                    if (cells.length === 0) {
                        cells = document.querySelectorAll('.media-cell[data-placeholder="Test_Placeholder"]');
                    }
                    if (cells.length === 0) {
                        cells = document.querySelectorAll('.media-cell');
                    }
                    
                    console.log('[TEST] Found', cells.length, 'cells');
                    
                    if (cells.length < 2) {
                        return { error: 'Not enough cells', count: cells.length, cells: Array.from(cells).map(c => ({
                            index: c.dataset.mediaIndex,
                            placeholder: c.dataset.placeholder,
                            hasContent: !!c.querySelector('img, div')
                        })) };
                    }
                    
                    const sourceIndex = 0;
                    const targetCell = cells[1]; // Second cell
                    
                    console.log('[TEST] Source index:', sourceIndex);
                    console.log('[TEST] Target cell:', {
                        index: targetCell.dataset.mediaIndex,
                        placeholder: targetCell.dataset.placeholder
                    });
                    
                    console.log('[TEST] Calling reorderMediaInPlaceholder...');
                    window.reorderMediaInPlaceholder(placeholder, sourceIndex, targetCell);
                    
                    // Wait a bit for async operations
                    return new Promise(resolve => {
                        setTimeout(() => {
                            const newAssignments = window.getCurrentAssignments();
                            console.log('[TEST] After reorder:', newAssignments[placeholder].map(m => m.name));
                            resolve({
                                success: true,
                                before: assignments[placeholder].map(m => m.name),
                                after: newAssignments[placeholder].map(m => m.name)
                            });
                        }, 100);
                    });
                }
            """)
            
            # Wait for promise to resolve
            import asyncio
            if hasattr(reorder_result, '__await__'):
                reorder_result = asyncio.run(reorder_result)
            
            # Print console messages
            print("\nConsole messages:")
            for msg in console_messages:
                if 'RESHUFFLE' in msg or 'TEST' in msg:
                    print(f"  {msg}")
            
            print(f"Reorder result: {json.dumps(reorder_result, indent=2)}")
            
            # Get final order
            order_after = page.evaluate("""
                () => {
                    const assignments = window.getCurrentAssignments();
                    return assignments['test_placeholder'] ? assignments['test_placeholder'].map(m => m.name) : [];
                }
            """)
            print(f"Order after reorder: {order_after}")
            
            # Check if order changed
            if order_before != order_after:
                print("✅ SUCCESS: Order changed!")
                print(f"  Before: {order_before}")
                print(f"  After: {order_after}")
            else:
                print("❌ FAIL: Order did not change")
                print(f"  Order: {order_before}")
            
            # Take screenshot
            page.screenshot(path="reports/screenshots/reshuffle_manual_test.png", full_page=True)
            print("Screenshot saved: reports/screenshots/reshuffle_manual_test.png")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            time.sleep(3)
            browser.close()

if __name__ == "__main__":
    test_reshuffle_manual()

