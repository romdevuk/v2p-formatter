#!/usr/bin/env python3
"""
Reshuffle functionality test with REAL media files
Uses actual media from the output folder for more realistic testing
"""
from playwright.sync_api import sync_playwright
import time
import os
from pathlib import Path

def test_reshuffle_with_real_media():
    """Test reshuffle with actual media files from output folder"""
    
    screenshots_dir = Path("reports/screenshots/reshuffle_real")
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("RESHUFFLE TEST WITH REAL MEDIA FILES")
    print("=" * 60)
    
    # Find real media files
    output_folder = Path("/Users/rom/Documents/nvq/v2p-formatter-output")
    real_media_files = []
    
    if output_folder.exists():
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.mp4']:
            real_media_files.extend(list(output_folder.rglob(ext)))
    
    # Use first 3 media files found
    test_media = real_media_files[:3]
    
    if len(test_media) < 2:
        print("⚠️  Not enough real media files found. Need at least 2 files.")
        print(f"   Found: {len(test_media)} files")
        return
    
    print(f"\nUsing {len(test_media)} real media files:")
    for i, media in enumerate(test_media, 1):
        print(f"  {i}. {media.name} ({media.parent.name})")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            # Navigate to observation media
            print("\n[1] Navigating to observation media page...")
            page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media", 
                     wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            
            # Select subfolder if available
            subfolder_select = page.locator("#observationSubfolderSelect")
            if subfolder_select.count() > 0:
                options = subfolder_select.locator("option")
                option_count = options.count()
                if option_count > 1:  # More than just "Select Subfolder..."
                    # Select first real subfolder
                    first_option = options.nth(1)
                    subfolder_value = first_option.get_attribute("value")
                    if subfolder_value:
                        print(f"  Selecting subfolder: {subfolder_value}")
                        subfolder_select.select_option(subfolder_value)
                        time.sleep(1)
                        
                        # Click load button
                        load_btn = page.locator("#observationLoadBtn")
                        if load_btn.count() > 0:
                            load_btn.click()
                            time.sleep(2)
            
            screenshot_path = screenshots_dir / "01_page_with_subfolder.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"✓ Screenshot: {screenshot_path}")
            
            # Add text with placeholder
            print("\n[2] Adding text with placeholder...")
            text_editor = page.locator("#observationTextEditor")
            if text_editor.count() > 0:
                test_text = "Observation with {{Test_Placeholder}} for reshuffle testing."
                text_editor.fill(test_text)
                time.sleep(1)
            
            screenshot_path = screenshots_dir / "02_text_added.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"✓ Screenshot: {screenshot_path}")
            
            # Assign real media files
            print("\n[3] Assigning real media files...")
            media_paths = [str(m) for m in test_media]
            page.evaluate(f"""
                if (!window.observationMediaAssignments) {{
                    window.observationMediaAssignments = {{}};
                }}
                
                window.observationMediaAssignments['test_placeholder'] = [];
                
                const mediaFiles = {media_paths};
                mediaFiles.forEach((path, index) => {{
                    const fileName = path.split('/').pop();
                    window.assignMediaToPlaceholder('test_placeholder', {{
                        path: path,
                        name: fileName,
                        type: fileName.toLowerCase().endsWith('.mp4') ? 'video' : 'image'
                    }});
                }});
                
                if (window.updatePreview) {{
                    window.updatePreview();
                }}
            """)
            time.sleep(2)
            
            screenshot_path = screenshots_dir / "03_real_media_assigned.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"✓ Screenshot: {screenshot_path}")
            
            # Enable reshuffle
            print("\n[4] Enabling reshuffle mode...")
            reshuffle_btn = page.locator("#reshuffleBtn")
            if reshuffle_btn.count() > 0 and reshuffle_btn.is_visible():
                reshuffle_btn.click()
                time.sleep(1.5)
                
                screenshot_path = screenshots_dir / "04_reshuffle_enabled.png"
                page.screenshot(path=str(screenshot_path), full_page=True)
                print(f"✓ Screenshot: {screenshot_path}")
                
                # Perform drag and drop
                print("\n[5] Performing drag and drop...")
                media_cells = page.locator(".media-cell")
                cell_count = media_cells.count()
                print(f"  Found {cell_count} media cells")
                
                if cell_count >= 2:
                    # Get initial order
                    initial_order = page.evaluate("""
                        () => {
                            const cells = Array.from(document.querySelectorAll('.media-cell'));
                            return cells.map(cell => {
                                const img = cell.querySelector('img');
                                return img ? (img.alt || img.src.split('/').pop()) : 'no-image';
                            });
                        }
                    """)
                    print(f"  Initial order: {[o[:20] for o in initial_order[:3]]}")
                    
                    # Drag first to second
                    source = media_cells.nth(0)
                    target = media_cells.nth(1)
                    source.drag_to(target)
                    time.sleep(2)
                    
                    screenshot_path = screenshots_dir / "05_after_drag_drop.png"
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    print(f"✓ Screenshot: {screenshot_path}")
                    
                    # Check final order
                    final_order = page.evaluate("""
                        () => {
                            const cells = Array.from(document.querySelectorAll('.media-cell'));
                            return cells.map(cell => {
                                const img = cell.querySelector('img');
                                return img ? (img.alt || img.src.split('/').pop()) : 'no-image';
                            });
                        }
                    """)
                    print(f"  Final order: {[o[:20] for o in final_order[:3]]}")
                    
                    # Disable reshuffle
                    print("\n[6] Disabling reshuffle...")
                    reshuffle_btn.click()
                    time.sleep(1)
                    
                    screenshot_path = screenshots_dir / "06_reshuffle_disabled.png"
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    print(f"✓ Screenshot: {screenshot_path}")
                else:
                    print("  ⚠️  Not enough cells for drag and drop")
            else:
                print("  ⚠️  Reshuffle button not visible")
            
            print("\n" + "=" * 60)
            print("TEST COMPLETE!")
            print(f"Screenshots: {screenshots_dir}")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            
            error_screenshot = screenshots_dir / "ERROR.png"
            page.screenshot(path=str(error_screenshot), full_page=True)
        
        finally:
            time.sleep(2)
            browser.close()

if __name__ == "__main__":
    test_reshuffle_with_real_media()


