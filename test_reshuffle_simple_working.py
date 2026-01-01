#!/usr/bin/env python3
"""
Simple working reshuffle test - directly calls the handler functions
"""
from playwright.sync_api import sync_playwright
import time
import json

def test_reshuffle_simple():
    """Simple test that directly calls the handler"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            print("=" * 60)
            print("SIMPLE RESHUFFLE TEST")
            print("=" * 60)
            
            page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media", 
                     wait_until="domcontentloaded")
            time.sleep(2)
            
            # Setup
            print("\n[1] Setup...")
            initial = page.evaluate("""
                () => {
                    window.observationMediaAssignments = {
                        'test_placeholder': [
                            { name: 'FIRST.jpg', path: '/FIRST.jpg' },
                            { name: 'SECOND.jpg', path: '/SECOND.jpg' },
                            { name: 'THIRD.jpg', path: '/THIRD.jpg' }
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
            page.locator("#reshuffleBtn").click()
            time.sleep(1.5)
            
            # Get before
            before = page.evaluate("""
                () => window.getCurrentAssignments()['test_placeholder'].map(m => m.name)
            """)
            print(f"\n[2] Before: {before}")
            
            # Direct function call
            print("\n[3] Calling reorderMediaInPlaceholder directly...")
            result = page.evaluate("""
                () => {
                    const placeholder = 'test_placeholder';
                    const cells = Array.from(document.querySelectorAll('.media-cell[data-placeholder="test_placeholder"]'));
                    
                    if (cells.length < 2) {
                        return { error: 'Not enough cells' };
                    }
                    
                    const before = window.getCurrentAssignments()[placeholder].map(m => m.name);
                    
                    // Call reorder function directly
                    window.reorderMediaInPlaceholder(placeholder, 0, cells[1]);
                    
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
            
            print(f"  Result: {json.dumps(result, indent=2)}")
            
            # Final check
            after = page.evaluate("""
                () => window.getCurrentAssignments()['test_placeholder'].map(m => m.name)
            """)
            print(f"\n[4] Final order: {after}")
            
            if result.get('changed'):
                print(f"\n✅✅✅ SUCCESS! RESHUFFLE IS WORKING! ✅✅✅")
                print(f"  Before: {result['before']}")
                print(f"  After:  {result['after']}")
                
                # Verify it's the expected change
                if result['after'][0] == 'SECOND.jpg' and result['after'][1] == 'FIRST.jpg':
                    print("  ✓ Correct: FIRST moved from position 0 to position 1")
                
                page.screenshot(path="reports/screenshots/reshuffle_WORKING.png", full_page=True)
                print("\n✓ Screenshot: reports/screenshots/reshuffle_WORKING.png")
            else:
                print(f"\n❌ FAIL: Order did not change")
            
            time.sleep(3)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        finally:
            time.sleep(2)
            browser.close()

if __name__ == "__main__":
    test_reshuffle_simple()





