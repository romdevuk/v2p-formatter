from playwright.sync_api import sync_playwright
import time
import os

def capture_screenshots():
    print("Starting screenshot capture...")
    os.makedirs("reports/screenshots", exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        print("Navigating to app...")
        page.goto("http://127.0.0.1:5000/v2p-formatter/")
        
        # Setup media
        print("Setting up media...")
        page.fill("#observationTextEditor", "{{Test_Placeholder}}")
        page.evaluate("window.updatePreview()")
        
        page.evaluate("""
            window.observationMediaAssignments['Test_Placeholder'] = [];
            window.assignMediaToPlaceholder('Test_Placeholder', {
                path: 'tests/test_data/img1.jpg', 
                name: 'img1.jpg', 
                type: 'image'
            });
            window.assignMediaToPlaceholder('Test_Placeholder', {
                path: 'tests/test_data/img2.jpg', 
                name: 'img2.jpg', 
                type: 'image'
            });
            window.updatePreview();
        """)
        time.sleep(1)
        
        # Activate Reshuffle
        print("Activating Reshuffle...")
        page.click("#reshuffleBtn")
        time.sleep(1)
        
        # Screenshot 1
        page.screenshot(path="reports/screenshots/01_before_reshuffle.png")
        print("Captured 01_before_reshuffle.png")
        
        # Drag and Drop
        print("Dragging...")
        cells = page.locator(".media-cell")
        source = cells.nth(0)
        target = cells.nth(1)
        source.drag_to(target)
        time.sleep(1)
        
        # Screenshot 2
        page.screenshot(path="reports/screenshots/02_after_reshuffle.png")
        print("Captured 02_after_reshuffle.png")
        
        browser.close()
        print("Done.")

if __name__ == "__main__":
    capture_screenshots()
