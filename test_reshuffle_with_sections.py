#!/usr/bin/env python3
"""Test reshuffle functionality with real sections and placeholders"""
from playwright.sync_api import sync_playwright
import time
import json

# The observation text with sections
OBSERVATION_TEXT = """SECTION 1 – SITE ARRIVAL AND INDUCTION

1.



I arrived to the project on agreed time, weather sunny. I met Ivan at the gate where he followed security rules by signing in and passing fenced access. He already wore full PPE: high-viz, hard hat, gloves, boots and glasses. Ivan showed me fire point and health & safety board.

AC covered: 641:1.1, 1.2, 1.3, 2.1, 4.1; 642:1.1

Image suggestion: learner signing in and wearing PPE.

{{Site_Arrival_and_Induction_table}}



2.



Inside the induction room Ivan displayed CSCS card, signed RAMS and daily sheet. I observed learner storing PPE and small tools correctly in tool bag.

AC covered: 641:5.1; 642:1.1, 4.1

Image suggestion: induction paperwork and CSCS verification.

{{Site_Arrival_and_Induction_table}}"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Navigate to observation media page with real data
    page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media?subfolder=lakhmaniuk", 
             wait_until="domcontentloaded")
    time.sleep(3)
    
    print("📝 Setting up observation text...")
    
    # Set the observation text
    page.locator("#observationTextEditor").fill(OBSERVATION_TEXT)
    time.sleep(2)
    
    # Wait for placeholders to be detected
    print("⏳ Waiting for placeholders to be detected...")
    time.sleep(2)
    
    # Get available media
    media_list = page.evaluate("""
        () => {
            const cards = Array.from(document.querySelectorAll('.observation-media-card:not(.media-assigned)'));
            return cards.slice(0, 6).map(card => ({
                path: card.dataset.mediaPath,
                name: card.dataset.mediaName,
                type: card.dataset.mediaType
            }));
        }
    """)
    
    print(f"📸 Found {len(media_list)} media items to assign")
    
    if len(media_list) < 4:
        print("❌ Need at least 4 media items for reshuffle test")
        browser.close()
        exit(1)
    
    # Assign first 4 media items to the placeholder
    placeholder = "Site_Arrival_and_Induction_table"
    print(f"📎 Assigning media to placeholder: {placeholder}")
    
    for i, media in enumerate(media_list[:4]):
        result = page.evaluate(f"""
            () => {{
                const media = {json.dumps(media)};
                const placeholder = '{placeholder}';
                
                // Get current assignments
                const assignments = window.getCurrentAssignments();
                const placeholderKey = placeholder.toLowerCase();
                
                // Assign media
                const result = window.assignMediaToPlaceholder(placeholder, media);
                
                // Update preview
                window.updatePreview();
                window.updatePlaceholderStats();
                
                return {{
                    success: result,
                    assigned: (window.getCurrentAssignments()[placeholderKey] || []).length,
                    mediaName: media.name
                }};
            }}
        """)
        
        print(f"  ✓ Assigned {result['mediaName']} (total: {result['assigned']})")
        time.sleep(0.5)
    
    # Take screenshot after assignment
    page.screenshot(path="reports/screenshots/reshuffle_01_after_assignment.png", full_page=True)
    print("📸 Screenshot: After assignment")
    time.sleep(1)
    
    # Enable reshuffle mode
    print("🔄 Enabling reshuffle mode...")
    reshuffle_visible = page.evaluate("""
        () => {
            const btn = document.getElementById('reshuffleBtn');
            if (!btn) return { visible: false, error: 'Button not found' };
            
            if (btn.style.display === 'none' || btn.offsetParent === null) {
                return { visible: false, error: 'Button is hidden', display: btn.style.display };
            }
            
            btn.click();
            return { visible: true, clicked: true, text: btn.textContent };
        }
    """)
    
    if not reshuffle_visible.get('visible'):
        print(f"❌ Reshuffle button issue: {reshuffle_visible.get('error', 'Unknown')}")
        browser.close()
        exit(1)
    
    time.sleep(1)
    page.screenshot(path="reports/screenshots/reshuffle_02_reshuffle_enabled.png", full_page=True)
    print("📸 Screenshot: Reshuffle mode enabled")
    
    # Get initial order
    initial_order = page.evaluate(f"""
        () => {{
            const assignments = window.getCurrentAssignments();
            const placeholderKey = '{placeholder.lower()}';
            return (assignments[placeholderKey] || []).map(m => m.name);
        }}
    """)
    
    print(f"📋 Initial order: {initial_order}")
    
    # Wait for UI to update after assignment
    time.sleep(1)
    
    # Perform reshuffle: move item from index 0 to index 2
    print("🔄 Performing reshuffle: moving item from index 0 to index 2...")
    
    reshuffle_result = page.evaluate(f"""
        () => {{
            const placeholder = '{placeholder}';
            const placeholderKey = '{placeholder.lower()}';
            const fromIndex = 0;
            const targetIndex = 2;
            
            // Get all cells - try both exact and case-insensitive matching
            const cells1 = Array.from(document.querySelectorAll('.media-cell[data-placeholder="{placeholder}"]'));
            const cells2 = Array.from(document.querySelectorAll('.media-cell[data-placeholder="{placeholder.lower()}"]'));
            const cells = cells1.length > 0 ? cells1 : cells2;
            
            console.log('Found cells:', cells.length, 'for placeholder:', placeholder);
            cells.forEach((cell, i) => {{
                console.log('Cell', i, ':', cell.dataset.mediaIndex, 'placeholder:', cell.dataset.placeholder);
            }});
            
            const targetCell = cells.find(cell => {{
                const idx = parseInt(cell.dataset.mediaIndex);
                return idx === targetIndex;
            }});
            
            if (!targetCell) {{
                return {{ 
                    error: 'Target cell not found', 
                    cellsFound: cells.length,
                    cellIndices: cells.map(c => c.dataset.mediaIndex),
                    targetIndex: targetIndex
                }};
            }}
            
            // Get assignments before
            const assignments = window.getCurrentAssignments();
            const before = (assignments[placeholderKey] || []).map(m => m.name);
            console.log('Before reorder:', before);
            
            // Perform reorder
            window.reorderMediaInPlaceholder(placeholder, fromIndex, targetCell);
            
            // Wait a bit for UI to update
            return new Promise(resolve => {{
                setTimeout(() => {{
                    const assignmentsAfter = window.getCurrentAssignments();
                    const after = (assignmentsAfter[placeholderKey] || []).map(m => m.name);
                    console.log('After reorder:', after);
                    resolve({{
                        before,
                        after,
                        changed: JSON.stringify(before) !== JSON.stringify(after),
                        targetCellFound: !!targetCell,
                        cellsFound: cells.length
                    }});
                }}, 500);
            }});
        }}
    """)
    
    # Handle promise result
    if hasattr(reshuffle_result, '__await__'):
        import asyncio
        reshuffle_result = asyncio.run(reshuffle_result)
    
    print(f"📋 Order before: {reshuffle_result.get('before', [])}")
    print(f"📋 Order after: {reshuffle_result.get('after', [])}")
    
    if reshuffle_result.get('changed'):
        print("✅ Reshuffle successful!")
    else:
        print("❌ Reshuffle failed - order unchanged")
        if reshuffle_result.get('error'):
            print(f"   Error: {reshuffle_result['error']}")
    
    time.sleep(1)
    page.screenshot(path="reports/screenshots/reshuffle_03_after_reshuffle.png", full_page=True)
    print("📸 Screenshot: After reshuffle")
    
    # Perform another reshuffle: move item from index 2 to index 0 (reverse)
    print("🔄 Performing reverse reshuffle: moving item from index 2 to index 0...")
    
    reshuffle_result2 = page.evaluate(f"""
        () => {{
            const placeholder = '{placeholder}';
            const placeholderKey = '{placeholder.lower()}';
            const fromIndex = 2;
            const targetIndex = 0;
            
            // Get all cells - try both exact and case-insensitive matching
            const cells1 = Array.from(document.querySelectorAll('.media-cell[data-placeholder="{placeholder}"]'));
            const cells2 = Array.from(document.querySelectorAll('.media-cell[data-placeholder="{placeholder.lower()}"]'));
            const cells = cells1.length > 0 ? cells1 : cells2;
            
            const targetCell = cells.find(cell => {{
                const idx = parseInt(cell.dataset.mediaIndex);
                return idx === targetIndex;
            }});
            
            if (!targetCell) {{
                return {{ error: 'Target cell not found', cellsFound: cells.length }};
            }}
            
            // Get assignments before
            const assignments = window.getCurrentAssignments();
            const before = (assignments[placeholderKey] || []).map(m => m.name);
            
            // Perform reorder
            window.reorderMediaInPlaceholder(placeholder, fromIndex, targetCell);
            
            // Wait a bit for UI to update
            return new Promise(resolve => {{
                setTimeout(() => {{
                    const assignmentsAfter = window.getCurrentAssignments();
                    const after = (assignmentsAfter[placeholderKey] || []).map(m => m.name);
                    resolve({{
                        before,
                        after,
                        changed: JSON.stringify(before) !== JSON.stringify(after)
                    }});
                }}, 500);
            }});
        }}
    """)
    
    # Handle promise result
    if hasattr(reshuffle_result2, '__await__'):
        import asyncio
        reshuffle_result2 = asyncio.run(reshuffle_result2)
    
    print(f"📋 Order before: {reshuffle_result2.get('before', [])}")
    print(f"📋 Order after: {reshuffle_result2.get('after', [])}")
    
    if reshuffle_result2.get('changed'):
        print("✅ Reverse reshuffle successful!")
    else:
        print("❌ Reverse reshuffle failed")
    
    time.sleep(1)
    page.screenshot(path="reports/screenshots/reshuffle_04_after_reverse.png", full_page=True)
    print("📸 Screenshot: After reverse reshuffle")
    
    # Test drag and drop simulation
    print("🔄 Testing drag and drop simulation...")
    
    # Get console messages to see if drop events are firing
    console_messages = []
    
    def handle_console(msg):
        console_messages.append(msg.text)
    
    page.on("console", handle_console)
    
    # Try to simulate a drag and drop
    drag_result = page.evaluate(f"""
        () => {{
            const placeholder = '{placeholder}';
            const placeholderKey = '{placeholder.lower()}';
            
            // Get source and target cells - try both exact and case-insensitive matching
            const cells1 = Array.from(document.querySelectorAll('.media-cell[data-placeholder="{placeholder}"]'));
            const cells2 = Array.from(document.querySelectorAll('.media-cell[data-placeholder="{placeholder.lower()}"]'));
            const cells = cells1.length > 0 ? cells1 : cells2;
            
            const sourceCell = cells.find(cell => {{
                const idx = parseInt(cell.dataset.mediaIndex);
                return idx === 0;
            }});
            const targetCell = cells.find(cell => {{
                const idx = parseInt(cell.dataset.mediaIndex);
                return idx === 3;
            }});
            
            if (!sourceCell || !targetCell) {{
                return {{ 
                    error: 'Cells not found', 
                    sourceFound: !!sourceCell, 
                    targetFound: !!targetCell,
                    cellsFound: cells.length
                }};
            }}
            
            // Get assignments before
            const assignments = window.getCurrentAssignments();
            const before = (assignments[placeholderKey] || []).map(m => m.name);
            
            // Create drag data
            const dragData = {{
                ...assignments[placeholderKey][0],
                source: 'table',
                placeholder: placeholder,
                index: 0
            }};
            
            // Create drop event
            const dropEvent = new Event('drop', {{ bubbles: true, cancelable: true }});
            const dataTransfer = {{
                data: {{}},
                setData: function(type, value) {{ this.data[type] = value; }},
                getData: function(type) {{ return this.data[type] || ''; }},
                effectAllowed: 'move',
                dropEffect: 'move'
            }};
            dataTransfer.setData('application/json', JSON.stringify(dragData));
            dataTransfer.setData('text/plain', '0');
            
            Object.defineProperty(dropEvent, 'dataTransfer', {{ 
                value: dataTransfer, 
                writable: false 
            }});
            Object.defineProperty(dropEvent, 'target', {{ 
                value: targetCell, 
                writable: false 
            }});
            Object.defineProperty(dropEvent, 'currentTarget', {{ 
                value: targetCell, 
                writable: false 
            }});
            
            dropEvent.preventDefault = () => {{}};
            dropEvent.stopPropagation = () => {{}};
            
            // Call handler
            try {{
                window.handleTableDrop(dropEvent, placeholder);
            }} catch (err) {{
                return {{ error: err.message, stack: err.stack }};
            }}
            
            // Wait and check
            return new Promise(resolve => {{
                setTimeout(() => {{
                    const assignmentsAfter = window.getCurrentAssignments();
                    const after = (assignmentsAfter[placeholderKey] || []).map(m => m.name);
                    resolve({{
                        before,
                        after,
                        changed: JSON.stringify(before) !== JSON.stringify(after)
                    }});
                }}, 500);
            }});
        }}
    """)
    
    # Handle promise result
    if hasattr(drag_result, '__await__'):
        import asyncio
        drag_result = asyncio.run(drag_result)
    
    print(f"📋 Order before drag: {drag_result.get('before', [])}")
    print(f"📋 Order after drag: {drag_result.get('after', [])}")
    
    if drag_result.get('changed'):
        print("✅ Drag and drop simulation successful!")
    else:
        print("❌ Drag and drop simulation failed")
        if drag_result.get('error'):
            print(f"   Error: {drag_result['error']}")
    
    # Check console for drop logs
    drop_logs = [msg for msg in console_messages if '[DROP]' in msg or '[RESHUFFLE]' in msg]
    if drop_logs:
        print("\n📋 Console logs:")
        for log in drop_logs[-10:]:  # Last 10 logs
            print(f"   {log}")
    
    time.sleep(1)
    page.screenshot(path="reports/screenshots/reshuffle_05_final_state.png", full_page=True)
    print("📸 Screenshot: Final state")
    
    print("\n✅ Test complete!")
    print(f"📁 Screenshots saved in reports/screenshots/")
    
    time.sleep(2)
    browser.close()

