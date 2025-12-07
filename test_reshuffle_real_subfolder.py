#!/usr/bin/env python3
"""
Test reshuffle with real subfolder data - lakhmaniuk
"""
from playwright.sync_api import sync_playwright
import time
import json

def test_reshuffle_real_subfolder():
    """Test with real subfolder data"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            print("=" * 60)
            print("RESHUFFLE TEST - Real Subfolder (lakhmaniuk)")
            print("=" * 60)
            
            # Navigate with subfolder parameter
            print("\n[1] Navigating to observation media with subfolder...")
            page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media?subfolder=lakhmaniuk", 
                     wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
            
            # Check if subfolder is loaded
            subfolder_select = page.locator("#observationSubfolderSelect")
            selected_value = subfolder_select.input_value() if subfolder_select.count() > 0 else None
            print(f"  Subfolder select value: {selected_value}")
            
            # Check if media is loaded
            print("\n[2] Checking media availability...")
            media_info = page.evaluate("""
                () => {
                    return {
                        hasMediaData: !!window.observationMediaData,
                        mediaDataKeys: window.observationMediaData ? Object.keys(window.observationMediaData) : [],
                        mediaCount: window.observationMediaData ? Object.values(window.observationMediaData).flat().length : 0
                    };
                }
            """)
            print(f"  Media data available: {media_info.get('hasMediaData')}")
            print(f"  Subfolders in data: {media_info.get('mediaDataKeys')}")
            print(f"  Total media items: {media_info.get('mediaCount')}")
            
            # Add text with placeholder
            print("\n[3] Adding text with placeholder...")
            text_editor = page.locator("#observationTextEditor")
            if text_editor.count() > 0:
                test_text = "Observation with {{Test_Placeholder}} for reshuffle testing."
                text_editor.fill(test_text)
                time.sleep(1)
                print("  ✓ Text added")
            
            # Check if reshuffle button exists
            print("\n[4] Checking reshuffle button...")
            reshuffle_btn = page.locator("#reshuffleBtn")
            btn_count = reshuffle_btn.count()
            btn_visible = reshuffle_btn.is_visible() if btn_count > 0 else False
            print(f"  Button exists: {btn_count > 0}")
            print(f"  Button visible: {btn_visible}")
            
            if btn_count > 0:
                btn_text = reshuffle_btn.text_content()
                print(f"  Button text: {btn_text}")
                btn_style = page.evaluate("""
                    () => {
                        const btn = document.getElementById('reshuffleBtn');
                        return btn ? window.getComputedStyle(btn).display : 'not found';
                    }
                """)
                print(f"  Button display style: {btn_style}")
            
            # Assign some real media to placeholder
            print("\n[5] Assigning real media to placeholder...")
            assignment_result = page.evaluate("""
                () => {
                    if (!window.observationMediaData || !window.observationMediaData['lakhmaniuk']) {
                        return { error: 'No media data for lakhmaniuk' };
                    }
                    
                    const mediaList = window.observationMediaData['lakhmaniuk'] || [];
                    if (mediaList.length === 0) {
                        return { error: 'No media items in lakhmaniuk subfolder' };
                    }
                    
                    // Get first 3 media items
                    const mediaToAssign = mediaList.slice(0, 3);
                    
                    // Initialize assignments
                    if (!window.observationMediaAssignments) {
                        window.observationMediaAssignments = {};
                    }
                    
                    window.observationMediaAssignments['test_placeholder'] = mediaToAssign;
                    
                    // Update preview
                    if (window.updatePreview) {
                        window.updatePreview();
                    }
                    
                    return {
                        success: true,
                        assigned: mediaToAssign.map(m => m.name),
                        count: mediaToAssign.length
                    };
                }
            """)
            print(f"  Assignment result: {json.dumps(assignment_result, indent=2)}")
            time.sleep(2)
            
            # Check reshuffle button again after assignment
            print("\n[6] Checking reshuffle button after assignment...")
            reshuffle_btn_after = page.locator("#reshuffleBtn")
            btn_visible_after = reshuffle_btn_after.is_visible() if reshuffle_btn_after.count() > 0 else False
            print(f"  Button visible after assignment: {btn_visible_after}")
            
            if btn_visible_after:
                btn_text_after = reshuffle_btn_after.text_content()
                print(f"  Button text: {btn_text_after}")
                
                # Try to enable reshuffle
                print("\n[7] Enabling reshuffle...")
                reshuffle_btn_after.click()
                time.sleep(1.5)
                
                btn_text_enabled = reshuffle_btn_after.text_content()
                print(f"  Button text after click: {btn_text_enabled}")
                
                # Check media cells
                cells_info = page.evaluate("""
                    () => {
                        const cells = Array.from(document.querySelectorAll('.media-cell'));
                        return {
                            total: cells.length,
                            draggable: cells.filter(c => c.draggable).length,
                            withContent: cells.filter(c => c.querySelector('img, div')).length
                        };
                    }
                """)
                print(f"  Media cells: {cells_info}")
                
                # Test reordering
                print("\n[8] Testing reorder...")
                order_before = page.evaluate("""
                    () => {
                        const assignments = window.getCurrentAssignments();
                        return assignments['test_placeholder'] ? assignments['test_placeholder'].map(m => m.name) : [];
                    }
                """)
                print(f"  Order before: {order_before}")
                
                if len(order_before) >= 2:
                    reorder_result = page.evaluate("""
                        () => {
                            const placeholder = 'test_placeholder';
                            const cells = Array.from(document.querySelectorAll('.media-cell[data-placeholder="test_placeholder"]'));
                            
                            if (cells.length < 2) {
                                return { error: 'Not enough cells' };
                            }
                            
                            const before = window.getCurrentAssignments()[placeholder].map(m => m.name);
                            window.reorderMediaInPlaceholder(placeholder, 0, cells[1]);
                            
                            return new Promise(resolve => {
                                setTimeout(() => {
                                    const after = window.getCurrentAssignments()[placeholder].map(m => m.name);
                                    resolve({
                                        before,
                                        after,
                                        changed: before.join(',') !== after.join(',')
                                    });
                                }, 500);
                            });
                        }
                    """)
                    
                    import asyncio
                    if hasattr(reorder_result, '__await__'):
                        reorder_result = asyncio.run(reorder_result)
                    
                    print(f"  Reorder result: {json.dumps(reorder_result, indent=2)}")
            else:
                print("  ✗ Reshuffle button not visible - cannot test reshuffle")
            
            # Test drop zones
            print("\n[9] Testing drop zones...")
            drop_zones = page.evaluate("""
                () => {
                    const zones = Array.from(document.querySelectorAll('.unassigned-placeholder-container, .placeholder-table.unassigned'));
                    return zones.map(z => ({
                        placeholder: z.dataset.placeholder || z.closest('[data-placeholder]')?.dataset.placeholder,
                        hasOndrop: !!z.ondrop || z.hasAttribute('ondrop'),
                        hasOndragover: !!z.ondragover || z.hasAttribute('ondragover')
                    }));
                }
            """)
            print(f"  Drop zones found: {len(drop_zones)}")
            for i, zone in enumerate(drop_zones[:3]):
                print(f"    Zone {i}: placeholder={zone.get('placeholder')}, ondrop={zone.get('hasOndrop')}, ondragover={zone.get('hasOndragover')}")
            
            # Take screenshots
            page.screenshot(path="reports/screenshots/reshuffle_real_subfolder_1_initial.png", full_page=True)
            print("\n✓ Screenshot 1: Initial state")
            
            if assignment_result.get('success'):
                page.screenshot(path="reports/screenshots/reshuffle_real_subfolder_2_after_assignment.png", full_page=True)
                print("✓ Screenshot 2: After assignment")
            
            if btn_visible_after:
                page.screenshot(path="reports/screenshots/reshuffle_real_subfolder_3_reshuffle_enabled.png", full_page=True)
                print("✓ Screenshot 3: Reshuffle enabled")
            
            time.sleep(3)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            page.screenshot(path="reports/screenshots/reshuffle_real_subfolder_ERROR.png", full_page=True)
        finally:
            time.sleep(2)
            browser.close()

if __name__ == "__main__":
    test_reshuffle_real_subfolder()


