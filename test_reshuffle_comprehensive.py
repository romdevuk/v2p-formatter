#!/usr/bin/env python3
"""
Comprehensive reshuffle test - verifies drag and drop actually works
"""
from playwright.sync_api import sync_playwright
import time
import json

def test_reshuffle_comprehensive():
    """Test reshuffle with detailed verification at each step"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            print("=" * 60)
            print("COMPREHENSIVE RESHUFFLE TEST")
            print("=" * 60)
            
            # Navigate
            print("\n[1] Navigating to observation media...")
            page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media", 
                     wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            
            # Add text
            print("\n[2] Adding text with placeholder...")
            text_editor = page.locator("#observationTextEditor")
            if text_editor.count() > 0:
                text_editor.fill("Test observation with {{Test_Placeholder}} for reshuffle.")
                time.sleep(1)
            
            # Assign 3 distinct media items
            print("\n[3] Assigning 3 media items...")
            initial_order = page.evaluate("""
                () => {
                    if (!window.observationMediaAssignments) {
                        window.observationMediaAssignments = {};
                    }
                    
                    window.observationMediaAssignments['test_placeholder'] = [
                        { path: '/media1.jpg', name: 'media1.jpg', type: 'image' },
                        { path: '/media2.jpg', name: 'media2.jpg', type: 'image' },
                        { path: '/media3.jpg', name: 'media3.jpg', type: 'image' }
                    ];
                    
                    if (window.updatePreview) {
                        window.updatePreview();
                    }
                    
                    return window.observationMediaAssignments['test_placeholder'].map(m => m.name);
                }
            """)
            print(f"  Initial order: {initial_order}")
            time.sleep(2)
            
            # Enable reshuffle
            print("\n[4] Enabling reshuffle mode...")
            reshuffle_btn = page.locator("#reshuffleBtn")
            if reshuffle_btn.count() > 0 and reshuffle_btn.is_visible():
                reshuffle_btn.click()
                time.sleep(1.5)
                print("  ✓ Reshuffle enabled")
            else:
                print("  ✗ Reshuffle button not found/visible")
                return
            
            # Get cells and verify they're draggable
            print("\n[5] Checking media cells...")
            cells_info = page.evaluate("""
                () => {
                    const cells = Array.from(document.querySelectorAll('.media-cell'));
                    return cells.map((cell, i) => ({
                        index: i,
                        dataIndex: cell.dataset.mediaIndex,
                        placeholder: cell.dataset.placeholder,
                        draggable: cell.draggable,
                        hasContent: !!(cell.querySelector('img, div'))
                    }));
                }
            """)
            print(f"  Found {len(cells_info)} cells")
            for cell in cells_info[:3]:
                print(f"    Cell {cell['index']}: data-index={cell['dataIndex']}, draggable={cell['draggable']}")
            
            if len(cells_info) < 2:
                print("  ✗ Not enough cells for drag and drop")
                return
            
            # Get order before drag
            order_before = page.evaluate("""
                () => {
                    const assignments = window.getCurrentAssignments();
                    return assignments['test_placeholder'] ? assignments['test_placeholder'].map(m => m.name) : [];
                }
            """)
            print(f"\n[6] Order BEFORE drag: {order_before}")
            
            # Perform drag and drop using JavaScript events
            print("\n[7] Performing drag and drop via JavaScript events...")
            result = page.evaluate("""
                () => {
                    const cells = Array.from(document.querySelectorAll('.media-cell[data-placeholder="test_placeholder"]'));
                    if (cells.length < 2) {
                        return { error: 'Not enough cells', count: cells.length };
                    }
                    
                    const sourceCell = cells[0];
                    const targetCell = cells[1];
                    
                    console.log('[TEST] Source cell:', sourceCell.dataset.mediaIndex);
                    console.log('[TEST] Target cell:', targetCell.dataset.mediaIndex);
                    
                    // Create drag events manually
                    const dragStartEvent = new DragEvent('dragstart', {
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: new DataTransfer()
                    });
                    
                    // Set data on dragstart
                    const sourceIndex = parseInt(sourceCell.dataset.mediaIndex) || 0;
                    const placeholder = 'test_placeholder';
                    const assignments = window.getCurrentAssignments();
                    const media = assignments['test_placeholder'][sourceIndex];
                    
                    if (media) {
                        dragStartEvent.dataTransfer.setData('application/json', JSON.stringify({
                            ...media,
                            source: 'table',
                            placeholder: placeholder,
                            index: sourceIndex
                        }));
                        dragStartEvent.dataTransfer.effectAllowed = 'move';
                    }
                    
                    // Trigger dragstart
                    sourceCell.dispatchEvent(dragStartEvent);
                    console.log('[TEST] Dragstart triggered');
                    
                    // Create dragover event
                    const dragOverEvent = new DragEvent('dragover', {
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dragStartEvent.dataTransfer
                    });
                    dragOverEvent.preventDefault = () => {}; // Prevent default
                    targetCell.dispatchEvent(dragOverEvent);
                    console.log('[TEST] Dragover triggered');
                    
                    // Create drop event
                    const dropEvent = new DragEvent('drop', {
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dragStartEvent.dataTransfer
                    });
                    dropEvent.preventDefault = () => {}; // Prevent default
                    targetCell.dispatchEvent(dropEvent);
                    console.log('[TEST] Drop triggered');
                    
                    // Wait a bit for async operations
                    return new Promise(resolve => {
                        setTimeout(() => {
                            const newAssignments = window.getCurrentAssignments();
                            resolve({
                                success: true,
                                before: assignments['test_placeholder'].map(m => m.name),
                                after: newAssignments['test_placeholder'].map(m => m.name)
                            });
                        }, 500);
                    });
                }
            """)
            
            # Wait for promise
            import asyncio
            if hasattr(result, '__await__'):
                result = asyncio.run(result)
            
            print(f"  Result: {json.dumps(result, indent=2)}")
            
            # Get order after drag
            time.sleep(1)
            order_after = page.evaluate("""
                () => {
                    const assignments = window.getCurrentAssignments();
                    return assignments['test_placeholder'] ? assignments['test_placeholder'].map(m => m.name) : [];
                }
            """)
            print(f"\n[8] Order AFTER drag: {order_after}")
            
            # Verify change
            if order_before != order_after:
                print("\n✅ SUCCESS: Order changed!")
                print(f"  Before: {order_before}")
                print(f"  After: {order_after}")
            else:
                print("\n❌ FAIL: Order did not change")
                print(f"  Order: {order_before}")
                
                # Try alternative: direct function call
                print("\n[9] Trying direct function call...")
                direct_result = page.evaluate("""
                    () => {
                        const assignments = window.getCurrentAssignments();
                        const placeholder = 'test_placeholder';
                        const cells = Array.from(document.querySelectorAll('.media-cell[data-placeholder="test_placeholder"]'));
                        
                        if (cells.length < 2) {
                            return { error: 'Not enough cells' };
                        }
                        
                        const before = assignments[placeholder].map(m => m.name);
                        window.reorderMediaInPlaceholder(placeholder, 0, cells[1]);
                        
                        // Wait for updatePreview
                        return new Promise(resolve => {
                            setTimeout(() => {
                                const after = window.getCurrentAssignments()[placeholder].map(m => m.name);
                                resolve({ before, after, changed: before.join(',') !== after.join(',') });
                            }, 500);
                        });
                    }
                """)
                
                if hasattr(direct_result, '__await__'):
                    direct_result = asyncio.run(direct_result)
                
                print(f"  Direct call result: {json.dumps(direct_result, indent=2)}")
                
                if direct_result.get('changed'):
                    print("  ✅ Direct function call works!")
                else:
                    print("  ❌ Direct function call also failed")
            
            # Take screenshot
            page.screenshot(path="reports/screenshots/reshuffle_comprehensive_test.png", full_page=True)
            print("\n✓ Screenshot saved: reports/screenshots/reshuffle_comprehensive_test.png")
            
            time.sleep(3)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        finally:
            time.sleep(2)
            browser.close()

if __name__ == "__main__":
    test_reshuffle_comprehensive()


