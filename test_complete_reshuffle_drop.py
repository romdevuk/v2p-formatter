#!/usr/bin/env python3
"""
Complete test: Reshuffle + Drop zones with real subfolder data
"""
from playwright.sync_api import sync_playwright
import time
import json

def test_complete():
    """Complete test with real data"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            print("=" * 60)
            print("COMPLETE TEST - Reshuffle + Drop Zones")
            print("=" * 60)
            
            # Navigate with subfolder
            page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media?subfolder=lakhmaniuk", 
                     wait_until="domcontentloaded")
            time.sleep(3)
            
            # Add text with TWO placeholders - one assigned, one unassigned
            print("\n[1] Setting up test scenario...")
            text_editor = page.locator("#observationTextEditor")
            if text_editor.count() > 0:
                text_editor.fill("Observation with {{Assigned_Placeholder}} and {{Unassigned_Placeholder}}.")
                time.sleep(1)
            
            # Assign media to first placeholder
            assignment_result = page.evaluate("""
                () => {
                    if (!window.observationMediaData || !window.observationMediaData['lakhmaniuk']) {
                        return { error: 'No media data' };
                    }
                    
                    const mediaList = window.observationMediaData['lakhmaniuk'] || [];
                    if (mediaList.length < 3) {
                        return { error: 'Not enough media' };
                    }
                    
                    // Assign 3 media to first placeholder
                    if (!window.observationMediaAssignments) {
                        window.observationMediaAssignments = {};
                    }
                    
                    window.observationMediaAssignments['assigned_placeholder'] = mediaList.slice(0, 3);
                    
                    if (window.updatePreview) {
                        window.updatePreview();
                    }
                    
                    return {
                        success: true,
                        assigned: window.observationMediaAssignments['assigned_placeholder'].map(m => m.name)
                    };
                }
            """)
            print(f"  Assigned to first placeholder: {assignment_result.get('assigned', [])}")
            time.sleep(2)
            
            # Check reshuffle button
            print("\n[2] Checking reshuffle button...")
            reshuffle_btn = page.locator("#reshuffleBtn")
            btn_visible = reshuffle_btn.is_visible() if reshuffle_btn.count() > 0 else False
            print(f"  Reshuffle button visible: {btn_visible}")
            
            if btn_visible:
                # Enable reshuffle
                reshuffle_btn.click()
                time.sleep(1)
                print("  ✓ Reshuffle enabled")
                
                # Test reordering
                order_before = page.evaluate("""
                    () => {
                        const assignments = window.getCurrentAssignments();
                        return assignments['assigned_placeholder'] ? assignments['assigned_placeholder'].map(m => m.name) : [];
                    }
                """)
                print(f"  Order before: {order_before}")
                
                # Reorder
                reorder_result = page.evaluate("""
                    () => {
                        const placeholder = 'assigned_placeholder';
                        const cells = Array.from(document.querySelectorAll('.media-cell[data-placeholder="assigned_placeholder"]'));
                        if (cells.length < 2) return { error: 'Not enough cells' };
                        
                        const before = window.getCurrentAssignments()[placeholder].map(m => m.name);
                        window.reorderMediaInPlaceholder(placeholder, 0, cells[1]);
                        
                        return new Promise(resolve => {
                            setTimeout(() => {
                                const after = window.getCurrentAssignments()[placeholder].map(m => m.name);
                                resolve({ before, after, changed: before.join(',') !== after.join(',') });
                            }, 500);
                        });
                    }
                """)
                
                import asyncio
                if hasattr(reorder_result, '__await__'):
                    reorder_result = asyncio.run(reorder_result)
                
                if reorder_result.get('changed'):
                    print(f"  ✅ Reshuffle works! {reorder_result['before']} -> {reorder_result['after']}")
                else:
                    print(f"  ❌ Reshuffle failed")
            
            # Check drop zones for unassigned placeholder
            print("\n[3] Checking drop zones for unassigned placeholder...")
            drop_zones = page.evaluate("""
                () => {
                    const zones = Array.from(document.querySelectorAll('.placeholder-table.unassigned[data-placeholder="unassigned_placeholder"]'));
                    return zones.length;
                }
            """)
            print(f"  Unassigned drop zones found: {drop_zones}")
            
            # Get unassigned media
            unassigned_media = page.evaluate("""
                () => {
                    const cards = Array.from(document.querySelectorAll('.observation-media-card:not(.media-assigned)'));
                    return cards.slice(0, 1).map(c => ({
                        path: c.dataset.mediaPath,
                        name: c.dataset.mediaName,
                        type: c.dataset.mediaType
                    }));
                }
            """)
            print(f"  Unassigned media available: {len(unassigned_media)}")
            
            # Test dropping media into unassigned placeholder
            drop_result = None
            if drop_zones > 0 and len(unassigned_media) > 0:
                print("\n[4] Testing drop into unassigned placeholder...")
                drop_result = page.evaluate(f"""
                    () => {{
                        const media = {json.dumps(unassigned_media[0])};
                        const placeholder = 'unassigned_placeholder';
                        
                        const before = (window.getCurrentAssignments()[placeholder] || []).length;
                        const result = window.assignMediaToPlaceholder(placeholder, media);
                        
                        if (window.updatePreview) {{
                            window.updatePreview();
                        }}
                        
                        const after = (window.getCurrentAssignments()[placeholder] || []).length;
                        
                        return {{
                            success: result,
                            beforeCount: before,
                            afterCount: after,
                            assigned: window.getCurrentAssignments()[placeholder]?.map(m => m.name) || []
                        }};
                    }}
                """)
                print(f"  Drop result: {json.dumps(drop_result, indent=2)}")
                
                if drop_result.get('success') and drop_result.get('afterCount', 0) > 0:
                    print("  ✅ Drop into unassigned placeholder works!")
                else:
                    print("  ❌ Drop failed")
            else:
                print(f"\n[4] Cannot test drop - drop_zones={drop_zones}, unassigned_media={len(unassigned_media)}")
                # Check why drop zones aren't found
                debug_info = page.evaluate("""
                    () => {
                        const text = document.getElementById('observationTextEditor').value;
                        const placeholders = window.extractPlaceholders ? window.extractPlaceholders(text) : [];
                        const assignments = window.getCurrentAssignments();
                        
                        return {
                            placeholders,
                            assignments: Object.keys(assignments),
                            unassigned: placeholders.filter(p => !assignments[p.toLowerCase()] || assignments[p.toLowerCase()].length === 0)
                        };
                    }
                """)
                print(f"  Debug: {json.dumps(debug_info, indent=2)}")
            
            # Screenshots
            page.screenshot(path="reports/screenshots/complete_test_1_initial.png", full_page=True)
            print("\n✓ Screenshot 1: Initial state")
            
            if btn_visible:
                page.screenshot(path="reports/screenshots/complete_test_2_reshuffle.png", full_page=True)
                print("✓ Screenshot 2: Reshuffle enabled")
            
            if drop_result and drop_result.get('success'):
                page.screenshot(path="reports/screenshots/complete_test_3_dropped.png", full_page=True)
                print("✓ Screenshot 3: After drop")
            
            print("\n" + "=" * 60)
            print("TEST COMPLETE")
            print("=" * 60)
            
            time.sleep(3)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        finally:
            time.sleep(2)
            browser.close()

if __name__ == "__main__":
    test_complete()

