#!/usr/bin/env python3
"""
Working reshuffle test - properly simulates drag and drop events
"""
from playwright.sync_api import sync_playwright
import time

def test_reshuffle_working():
    """Test that properly simulates drag and drop"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            print("=" * 60)
            print("RESHUFFLE TEST - Proper Event Simulation")
            print("=" * 60)
            
            # Navigate
            page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media", 
                     wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            
            # Setup
            print("\n[1] Setting up test data...")
            initial = page.evaluate("""
                () => {
                    window.observationMediaAssignments = {
                        'test_placeholder': [
                            { path: '/1.jpg', name: '1.jpg', type: 'image' },
                            { path: '/2.jpg', name: '2.jpg', type: 'image' },
                            { path: '/3.jpg', name: '3.jpg', type: 'image' }
                        ]
                    };
                    document.getElementById('observationTextEditor').value = 'Test {{Test_Placeholder}}';
                    if (window.updatePreview) window.updatePreview();
                    return window.observationMediaAssignments['test_placeholder'].map(m => m.name);
                }
            """)
            print(f"  Initial: {initial}")
            time.sleep(2)
            
            # Enable reshuffle
            print("\n[2] Enabling reshuffle...")
            page.locator("#reshuffleBtn").click()
            time.sleep(1.5)
            
            # Get order before
            before = page.evaluate("""
                () => window.getCurrentAssignments()['test_placeholder'].map(m => m.name)
            """)
            print(f"  Before: {before}")
            
            # Simulate proper drag and drop
            print("\n[3] Simulating drag and drop...")
            result = page.evaluate("""
                () => {
                    const placeholder = 'test_placeholder';
                    const cells = Array.from(document.querySelectorAll('.media-cell[data-placeholder="test_placeholder"]'));
                    
                    if (cells.length < 2) {
                        return { error: 'Not enough cells' };
                    }
                    
                    const sourceCell = cells[0];
                    const targetCell = cells[1];
                    const sourceIndex = 0;
                    
                    const before = window.getCurrentAssignments()[placeholder].map(m => m.name);
                    
                    // Create proper DataTransfer
                    const dataTransfer = {
                        data: {},
                        setData: function(type, value) { this.data[type] = value; },
                        getData: function(type) { return this.data[type] || ''; },
                        effectAllowed: 'move',
                        dropEffect: 'move'
                    };
                    
                    // Set drag data
                    const media = window.getCurrentAssignments()[placeholder][sourceIndex];
                    dataTransfer.setData('application/json', JSON.stringify({
                        ...media,
                        source: 'table',
                        placeholder: placeholder,
                        index: sourceIndex
                    }));
                    
                    // Create and dispatch dragstart
                    const dragStart = new DragEvent('dragstart', {
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dataTransfer
                    });
                    Object.defineProperty(dragStart, 'dataTransfer', { value: dataTransfer, writable: false });
                    sourceCell.dispatchEvent(dragStart);
                    
                    // Create and dispatch dragover
                    const dragOver = new DragEvent('dragover', {
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dataTransfer
                    });
                    Object.defineProperty(dragOver, 'dataTransfer', { value: dataTransfer, writable: false });
                    dragOver.preventDefault = () => {};
                    targetCell.dispatchEvent(dragOver);
                    
                    // Create and dispatch drop
                    const drop = new DragEvent('drop', {
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dataTransfer
                    });
                    Object.defineProperty(drop, 'dataTransfer', { value: dataTransfer, writable: false });
                    drop.preventDefault = () => {};
                    targetCell.dispatchEvent(drop);
                    
                    return new Promise(resolve => {
                        setTimeout(() => {
                            const after = window.getCurrentAssignments()[placeholder].map(m => m.name);
                            resolve({
                                before,
                                after,
                                changed: before.join(',') !== after.join(','),
                                success: true
                            });
                        }, 500);
                    });
                }
            """)
            
            import asyncio
            if hasattr(result, '__await__'):
                result = asyncio.run(result)
            
            print(f"  Result: {result}")
            
            # Verify
            after = page.evaluate("""
                () => window.getCurrentAssignments()['test_placeholder'].map(m => m.name)
            """)
            print(f"\n[4] Final order: {after}")
            
            if result.get('changed'):
                print(f"\n✅ SUCCESS! Reshuffle is working!")
                print(f"  Before: {result['before']}")
                print(f"  After:  {result['after']}")
                
                # Take success screenshot
                page.screenshot(path="reports/screenshots/reshuffle_working_success.png", full_page=True)
                print("\n✓ Success screenshot saved")
            else:
                print(f"\n❌ FAIL: Order did not change")
                print(f"  Order: {before}")
            
            time.sleep(3)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        finally:
            time.sleep(2)
            browser.close()

if __name__ == "__main__":
    test_reshuffle_working()





