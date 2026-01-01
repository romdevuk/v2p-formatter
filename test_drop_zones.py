#!/usr/bin/env python3
"""
Test drop zones for unassigned placeholders
"""
from playwright.sync_api import sync_playwright
import time
import json

def test_drop_zones():
    """Test dropping media into unassigned placeholder drop zones"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            print("=" * 60)
            print("DROP ZONE TEST")
            print("=" * 60)
            
            page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media?subfolder=lakhmaniuk", 
                     wait_until="domcontentloaded")
            time.sleep(3)
            
            # Add text with placeholder (but don't assign media yet)
            print("\n[1] Adding text with unassigned placeholder...")
            text_editor = page.locator("#observationTextEditor")
            if text_editor.count() > 0:
                text_editor.fill("Observation with {{Unassigned_Placeholder}} for drop testing.")
                time.sleep(1)
            
            # Check for drop zones
            print("\n[2] Checking for drop zones...")
            drop_zones = page.evaluate("""
                () => {
                    const zones = Array.from(document.querySelectorAll('.unassigned-placeholder-container, .placeholder-table.unassigned, [data-placeholder]'));
                    return zones.map(z => ({
                        tag: z.tagName,
                        className: z.className,
                        placeholder: z.dataset.placeholder,
                        hasOndrop: z.hasAttribute('ondrop') || z.ondrop !== null,
                        hasOndragover: z.hasAttribute('ondragover') || z.ondragover !== null,
                        innerHTML: z.innerHTML.substring(0, 100)
                    }));
                }
            """)
            print(f"  Found {len(drop_zones)} potential drop zones")
            for i, zone in enumerate(drop_zones[:5]):
                print(f"    Zone {i}: {zone.get('tag')} - placeholder={zone.get('placeholder')}, ondrop={zone.get('hasOndrop')}")
            
            # Check if unassigned placeholder table exists
            unassigned_tables = page.evaluate("""
                () => {
                    const tables = Array.from(document.querySelectorAll('.placeholder-table.unassigned'));
                    return tables.map(t => ({
                        placeholder: t.dataset.placeholder || t.closest('[data-placeholder]')?.dataset.placeholder,
                        hasOndrop: t.hasAttribute('ondrop'),
                        ondropValue: t.getAttribute('ondrop')
                    }));
                }
            """)
            print(f"\n[3] Unassigned placeholder tables: {len(unassigned_tables)}")
            for i, table in enumerate(unassigned_tables):
                print(f"    Table {i}: placeholder={table.get('placeholder')}, ondrop={table.get('hasOndrop')}, value={table.get('ondropValue', '')[:50]}")
            
            # Get media cards
            print("\n[4] Checking media cards...")
            media_cards = page.evaluate("""
                () => {
                    const cards = Array.from(document.querySelectorAll('.observation-media-card'));
                    return cards.filter(c => !c.classList.contains('media-assigned')).slice(0, 3).map(c => ({
                        path: c.dataset.mediaPath,
                        name: c.dataset.mediaName,
                        draggable: c.draggable
                    }));
                }
            """)
            print(f"  Found {len(media_cards)} unassigned media cards")
            for card in media_cards:
                print(f"    {card['name']} - draggable: {card['draggable']}")
            
            # Try to simulate drag and drop
            if len(media_cards) > 0 and len(unassigned_tables) > 0:
                print("\n[5] Simulating drag and drop...")
                result = page.evaluate(f"""
                    () => {{
                        const media = {json.dumps(media_cards[0])};
                        const placeholder = 'unassigned_placeholder';
                        
                        // Get current assignments
                        const before = window.getCurrentAssignments()[placeholder] || [];
                        console.log('[TEST] Before assignment:', before.length);
                        
                        // Try to assign media
                        const result = window.assignMediaToPlaceholder(placeholder, media);
                        console.log('[TEST] Assignment result:', result);
                        
                        // Get assignments after
                        const after = window.getCurrentAssignments()[placeholder] || [];
                        console.log('[TEST] After assignment:', after.length);
                        
                        // Update preview
                        if (window.updatePreview) {{
                            window.updatePreview();
                        }}
                        
                        return {{
                            success: result,
                            beforeCount: before.length,
                            afterCount: after.length,
                            assigned: after.map(m => m.name)
                        }};
                    }}
                """)
                print(f"  Result: {json.dumps(result, indent=2)}")
                
                # Check if drop zone still exists (should be gone if media assigned)
                time.sleep(1)
                remaining_zones = page.evaluate("""
                    () => {
                        return document.querySelectorAll('.placeholder-table.unassigned').length;
                    }
                """)
                print(f"\n[6] Remaining unassigned drop zones: {remaining_zones}")
                
                if result.get('success') and result.get('afterCount', 0) > 0:
                    print("  ✅ Media assigned successfully!")
                else:
                    print("  ❌ Failed to assign media")
            
            # Screenshot
            page.screenshot(path="reports/screenshots/drop_zones_test.png", full_page=True)
            print("\n✓ Screenshot saved")
            
            time.sleep(3)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        finally:
            time.sleep(2)
            browser.close()

if __name__ == "__main__":
    test_drop_zones()





