#!/usr/bin/env python3
"""
Final reshuffle test - uses Playwright's native drag_to and verifies it works
"""
from playwright.sync_api import sync_playwright
import time

def test_reshuffle_final():
    """Test reshuffle with Playwright's drag_to method"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            print("=" * 60)
            print("FINAL RESHUFFLE TEST - Playwright drag_to")
            print("=" * 60)
            
            # Navigate
            page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media", 
                     wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            
            # Add text
            text_editor = page.locator("#observationTextEditor")
            if text_editor.count() > 0:
                text_editor.fill("Test with {{Test_Placeholder}}")
                time.sleep(1)
            
            # Assign 3 media items with distinct names
            print("\n[1] Setting up media...")
            initial_order = page.evaluate("""
                () => {
                    window.observationMediaAssignments = {
                        'test_placeholder': [
                            { path: '/A.jpg', name: 'A.jpg', type: 'image' },
                            { path: '/B.jpg', name: 'B.jpg', type: 'image' },
                            { path: '/C.jpg', name: 'C.jpg', type: 'image' }
                        ]
                    };
                    if (window.updatePreview) window.updatePreview();
                    return window.observationMediaAssignments['test_placeholder'].map(m => m.name);
                }
            """)
            print(f"  Initial order: {initial_order}")
            time.sleep(2)
            
            # Enable reshuffle
            print("\n[2] Enabling reshuffle...")
            reshuffle_btn = page.locator("#reshuffleBtn")
            if reshuffle_btn.is_visible():
                reshuffle_btn.click()
                time.sleep(1.5)
            
            # Get order before
            order_before = page.evaluate("""
                () => window.getCurrentAssignments()['test_placeholder'].map(m => m.name)
            """)
            print(f"  Order before drag: {order_before}")
            
            # Find cells
            cells = page.locator(".media-cell[data-placeholder='test_placeholder']")
            cell_count = cells.count()
            print(f"\n[3] Found {cell_count} cells")
            
            if cell_count >= 2:
                # Get cell info
                cell_info = page.evaluate("""
                    () => {
                        const cells = Array.from(document.querySelectorAll('.media-cell[data-placeholder="test_placeholder"]'));
                        return cells.slice(0, 3).map(c => ({
                            index: c.dataset.mediaIndex,
                            placeholder: c.dataset.placeholder,
                            draggable: c.draggable
                        }));
                    }
                """)
                print(f"  Cell 0: index={cell_info[0]['index']}, draggable={cell_info[0]['draggable']}")
                print(f"  Cell 1: index={cell_info[1]['index']}, draggable={cell_info[1]['draggable']}")
                
                # Perform drag and drop
                print("\n[4] Performing drag and drop (cell 0 -> cell 1)...")
                source = cells.nth(0)
                target = cells.nth(1)
                
                # Use Playwright's drag_to
                source.drag_to(target)
                time.sleep(2)  # Wait for drop to process
                
                # Get order after
                order_after = page.evaluate("""
                    () => window.getCurrentAssignments()['test_placeholder'].map(m => m.name)
                """)
                print(f"  Order after drag: {order_after}")
                
                # Verify
                if order_before != order_after:
                    print(f"\n✅ SUCCESS! Order changed:")
                    print(f"  Before: {order_before}")
                    print(f"  After:  {order_after}")
                    
                    # Expected: A should move to position 1, so B should be first
                    if order_after[0] == 'B.jpg' and order_after[1] == 'A.jpg':
                        print("  ✓ Correct reordering: A moved from 0 to 1")
                    else:
                        print(f"  ⚠️  Unexpected order, but change occurred")
                else:
                    print(f"\n❌ FAIL: Order did not change")
                    print(f"  Order: {order_before}")
                    
                    # Try manual event dispatch as fallback
                    print("\n[5] Trying manual event dispatch...")
                    manual_result = page.evaluate("""
                        () => {
                            const cells = Array.from(document.querySelectorAll('.media-cell[data-placeholder="test_placeholder"]'));
                            if (cells.length < 2) return { error: 'Not enough cells' };
                            
                            const source = cells[0];
                            const target = cells[1];
                            const placeholder = 'test_placeholder';
                            const sourceIndex = 0;
                            
                            // Get current order
                            const before = window.getCurrentAssignments()[placeholder].map(m => m.name);
                            
                            // Create and dispatch events
                            const dt = new DataTransfer();
                            const media = window.getCurrentAssignments()[placeholder][sourceIndex];
                            dt.setData('application/json', JSON.stringify({
                                ...media,
                                source: 'table',
                                placeholder: placeholder,
                                index: sourceIndex
                            }));
                            
                            const dragStart = new DragEvent('dragstart', { bubbles: true, dataTransfer: dt });
                            source.dispatchEvent(dragStart);
                            
                            const dragOver = new DragEvent('dragover', { bubbles: true, dataTransfer: dt });
                            dragOver.preventDefault = () => {};
                            target.dispatchEvent(dragOver);
                            
                            const drop = new DragEvent('drop', { bubbles: true, dataTransfer: dt });
                            drop.preventDefault = () => {};
                            target.dispatchEvent(drop);
                            
                            return new Promise(resolve => {
                                setTimeout(() => {
                                    const after = window.getCurrentAssignments()[placeholder].map(m => m.name);
                                    resolve({ before, after, changed: before.join(',') !== after.join(',') });
                                }, 500);
                            });
                        }
                    """)
                    
                    import asyncio
                    if hasattr(manual_result, '__await__'):
                        manual_result = asyncio.run(manual_result)
                    
                    print(f"  Manual result: {manual_result}")
                    if manual_result.get('changed'):
                        print("  ✅ Manual event dispatch worked!")
            
            # Screenshot
            page.screenshot(path="reports/screenshots/reshuffle_final_test.png", full_page=True)
            print("\n✓ Screenshot: reports/screenshots/reshuffle_final_test.png")
            
            time.sleep(3)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        finally:
            time.sleep(2)
            browser.close()

if __name__ == "__main__":
    test_reshuffle_final()


