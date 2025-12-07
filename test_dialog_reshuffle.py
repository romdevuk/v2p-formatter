#!/usr/bin/env python3
"""Test reshuffle functionality in the Assign Media to Placeholder dialog"""
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
    
    # Get available media
    media_list = page.evaluate("""
        () => {
            const cards = Array.from(document.querySelectorAll('.observation-media-card:not(.media-assigned)'));
            return cards.slice(0, 4).map(card => ({
                path: card.dataset.mediaPath,
                name: card.dataset.mediaName,
                type: card.dataset.mediaType
            }));
        }
    """)
    
    print(f"📸 Found {len(media_list)} media items")
    
    if len(media_list) < 4:
        print("❌ Need at least 4 media items for test")
        browser.close()
        exit(1)
    
    # Enable bulk select mode first
    print("🖱️  Enabling bulk select mode...")
    bulk_mode = page.evaluate("""
        () => {
            const checkbox = document.getElementById('bulkSelectMode');
            if (!checkbox) {
                return { enabled: false, error: 'Bulk select checkbox not found' };
            }
            checkbox.checked = true;
            checkbox.dispatchEvent(new Event('change', { bubbles: true }));
            return { enabled: true };
        }
    """)
    print(f"Bulk select mode: {bulk_mode}")
    time.sleep(1)
    
    # Now select media cards by clicking them (in bulk mode, clicking toggles selection)
    print("🖱️  Selecting media cards...")
    selected_count = 0
    for i in range(4):
        result = page.evaluate(f"""
            () => {{
                const cards = Array.from(document.querySelectorAll('.observation-media-card:not(.media-assigned)'));
                if (cards.length > {i}) {{
                    const card = cards[{i}];
                    if (!card.classList.contains('media-selected')) {{
                        // Click the card to select it (bulk mode is active)
                        card.click();
                        return {{ success: true, name: card.dataset.mediaName }};
                    }}
                }}
                return {{ success: false }};
            }}
        """)
        if result.get('success'):
            selected_count += 1
            print(f"  ✓ Selected {result.get('name')}")
        time.sleep(0.3)
    
    print(f"Selected {selected_count} media items")
    time.sleep(1)
    
    # Check if "Assign Selected" button is visible
    btn_visible = page.evaluate("""
        () => {
            const btn = document.getElementById('bulkAssignBtn');
            return {
                found: !!btn,
                visible: btn && (btn.style.display !== 'none' && btn.offsetParent !== null),
                text: btn ? btn.textContent : null
            };
        }
    """)
    
    print(f"Assign Selected button: {btn_visible}")
    
    if not btn_visible.get('visible'):
        print("❌ Assign Selected button not visible - cannot open dialog")
        browser.close()
        exit(1)
    
    # Click "Assign Selected" button to open dialog
    placeholder = "Site_Arrival_and_Induction_table"
    print(f"📎 Clicking 'Assign Selected' to open dialog...")
    
    dialog_opened = page.evaluate("""
        () => {
            const btn = document.getElementById('bulkAssignBtn');
            if (!btn) {
                return { opened: false, error: 'Button not found' };
            }
            
            // Click the button
            btn.click();
            
            return { opened: true, clicked: true };
        }
    """)
    
    print(f"Dialog opened: {dialog_opened}")
    time.sleep(3)
    
    # Check if dialog is visible
    dialog_visible = page.evaluate("""
        () => {
            const dialog = window.currentPlaceholderDialog || document.querySelector('.placeholder-dialog');
            return {
                found: !!dialog,
                visible: dialog && (dialog.style.display !== 'none' && dialog.offsetParent !== null),
                hasPreview: dialog && !!dialog.querySelector('#dialogPreview')
            };
        }
    """)
    
    print(f"Dialog status: {dialog_visible}")
    
    if not dialog_visible.get('found'):
        print("❌ Dialog not found - cannot test")
        page.screenshot(path="reports/screenshots/dialog_reshuffle_00_no_dialog.png", full_page=True)
        browser.close()
        exit(1)
    
    # Assign media in dialog
    print("📎 Assigning media in dialog...")
    assign_result = page.evaluate(f"""
        () => {{
            const dialog = window.currentPlaceholderDialog || document.querySelector('.placeholder-dialog');
            if (!dialog) return {{ error: 'Dialog not found' }};
            
            const placeholder = '{placeholder}';
            const mediaList = window.bulkSelectedMedia || [];
            
            if (mediaList.length === 0) {{
                return {{ error: 'No media selected' }};
            }}
            
            // Get assignments before
            const assignments = window.getCurrentAssignments();
            const placeholderKey = '{placeholder.lower()}';
            const before = (assignments[placeholderKey] || []).length;
            
            // Assign all media
            let assignedCount = 0;
            mediaList.forEach(media => {{
                if (window.assignMediaToPlaceholder(placeholder, media)) {{
                    assignedCount++;
                }}
            }});
            
            // Update previews
            window.updateDialogPreview();
            window.updatePreview();
            
            // Wait a bit
            return new Promise(resolve => {{
                setTimeout(() => {{
                    const assignmentsAfter = window.getCurrentAssignments();
                    const after = (assignmentsAfter[placeholderKey] || []).length;
                    resolve({{
                        before,
                        after,
                        assignedCount,
                        changed: before !== after
                    }});
                }}, 500);
            }});
        }}
    """)
    
    # Handle promise
    if hasattr(assign_result, '__await__'):
        import asyncio
        assign_result = asyncio.run(assign_result)
    
    print(f"Assignment result: {assign_result}")
    time.sleep(1)
    page.screenshot(path="reports/screenshots/dialog_reshuffle_01_after_assignment.png", full_page=True)
    
    # Check reshuffle button
    print("🔄 Checking reshuffle button...")
    reshuffle_btn = page.evaluate("""
        () => {
            const dialog = window.currentPlaceholderDialog || document.querySelector('.placeholder-dialog');
            if (!dialog) return { found: false, error: 'Dialog not found' };
            
            const btn = dialog.querySelector('#dialogReshuffleBtn button');
            return {
                found: !!btn,
                visible: btn && (btn.style.display !== 'none' && btn.offsetParent !== null),
                text: btn ? btn.textContent : null
            };
        }
    """)
    
    print(f"Reshuffle button: {reshuffle_btn}")
    
    if not reshuffle_btn.get('found') or not reshuffle_btn.get('visible'):
        print("❌ Reshuffle button not found or not visible")
        browser.close()
        exit(1)
    
    # Enable reshuffle mode
    print("🔄 Enabling reshuffle mode...")
    reshuffle_enabled = page.evaluate("""
        () => {
            const dialog = window.currentPlaceholderDialog || document.querySelector('.placeholder-dialog');
            if (!dialog) return { error: 'Dialog not found' };
            
            const btn = dialog.querySelector('#dialogReshuffleBtn button');
            if (!btn) return { error: 'Button not found' };
            
            // Click button
            btn.click();
            
            // Check if mode is enabled
            return new Promise(resolve => {
                setTimeout(() => {
                    const preview = dialog.querySelector('#dialogPreview');
                    const cells = preview ? preview.querySelectorAll('.media-cell') : [];
                    const draggableCells = Array.from(cells).filter(cell => cell.draggable === true);
                    
                    resolve({
                        clicked: true,
                        cellsFound: cells.length,
                        draggableCells: draggableCells.length,
                        btnText: btn.textContent,
                        previewHasClass: preview && preview.classList.contains('reshuffle-active')
                    });
                }, 500);
            });
        }
    """)
    
    # Handle promise
    if hasattr(reshuffle_enabled, '__await__'):
        import asyncio
        reshuffle_enabled = asyncio.run(reshuffle_enabled)
    
    print(f"Reshuffle enabled: {reshuffle_enabled}")
    time.sleep(1)
    page.screenshot(path="reports/screenshots/dialog_reshuffle_02_reshuffle_enabled.png", full_page=True)
    
    # Get initial order
    initial_order = page.evaluate(f"""
        () => {{
            const assignments = window.getCurrentAssignments();
            const placeholderKey = '{placeholder.lower()}';
            return (assignments[placeholderKey] || []).map(m => m.name);
        }}
    """)
    
    print(f"📋 Initial order: {initial_order}")
    
    # Test reshuffle: move from index 0 to index 2
    print("🔄 Testing reshuffle: moving item from index 0 to index 2...")
    
    reshuffle_result = page.evaluate(f"""
        () => {{
            const dialog = window.currentPlaceholderDialog || document.querySelector('.placeholder-selection-dialog');
            if (!dialog) return {{ error: 'Dialog not found' }};
            
            const preview = dialog.querySelector('#dialogPreview');
            if (!preview) return {{ error: 'Preview not found' }};
            
            const placeholder = '{placeholder}';
            const placeholderKey = '{placeholder.lower()}';
            const fromIndex = 0;
            const targetIndex = 2;
            
            // Get all cells in preview
            const allCellsInPreview = Array.from(preview.querySelectorAll('.media-cell'));
            console.log('[TEST] Total cells in preview:', allCellsInPreview.length);
            
            // Get cells for this placeholder - try multiple ways
            let cells = [];
            
            // Method 1: Exact match
            cells = allCellsInPreview.filter(c => c.dataset.placeholder === placeholder);
            console.log('[TEST] Cells with exact placeholder match:', cells.length);
            
            // Method 2: Case-insensitive match
            if (cells.length === 0) {{
                cells = allCellsInPreview.filter(c => c.dataset.placeholder && 
                    c.dataset.placeholder.toLowerCase() === placeholderKey);
                console.log('[TEST] Cells with case-insensitive match:', cells.length);
            }}
            
            // Method 3: Contains match
            if (cells.length === 0) {{
                cells = allCellsInPreview.filter(c => c.dataset.placeholder && 
                    (c.dataset.placeholder.includes(placeholder) || 
                     c.dataset.placeholder.toLowerCase().includes(placeholderKey)));
                console.log('[TEST] Cells with contains match:', cells.length);
            }}
            
            // Method 4: Check parent table
            if (cells.length === 0) {{
                const tables = Array.from(preview.querySelectorAll('table.placeholder-table'));
                tables.forEach(table => {{
                    if (table.dataset.placeholder === placeholder || 
                        table.dataset.placeholder?.toLowerCase() === placeholderKey) {{
                        const tableCells = Array.from(table.querySelectorAll('.media-cell'));
                        cells = cells.concat(tableCells);
                    }}
                }});
                console.log('[TEST] Cells from parent table:', cells.length);
            }}
            
            console.log('[TEST] Final cells found:', cells.length);
            cells.forEach((c, i) => {{
                console.log('[TEST] Cell', i, ':', c.dataset.mediaIndex, 'placeholder:', c.dataset.placeholder);
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
                    cellPlaceholders: cells.map(c => c.dataset.placeholder),
                    targetIndex: targetIndex,
                    allCellsCount: allCellsInPreview.length
                }};
            }}
            
            // Get assignments before
            const assignments = window.getCurrentAssignments();
            console.log('[TEST] All assignments keys:', Object.keys(assignments));
            console.log('[TEST] Looking for key:', placeholderKey);
            const before = (assignments[placeholderKey] || []).map(m => m.name);
            console.log('[TEST] Before order:', before);
            
            // Perform reorder
            window.reorderMediaInPlaceholder(placeholder, fromIndex, targetCell);
            
            // Update previews
            window.updateDialogPreview();
            window.updatePreview();
            
            // Wait and check
            return new Promise(resolve => {{
                setTimeout(() => {{
                    const assignmentsAfter = window.getCurrentAssignments();
                    const after = (assignmentsAfter[placeholderKey] || []).map(m => m.name);
                    console.log('[TEST] After order:', after);
                    resolve({{
                        before,
                        after,
                        changed: JSON.stringify(before) !== JSON.stringify(after),
                        targetCellFound: !!targetCell,
                        assignmentsKeys: Object.keys(assignmentsAfter)
                    }});
                }}, 500);
            }});
        }}
    """)
    
    # Handle promise
    if hasattr(reshuffle_result, '__await__'):
        import asyncio
        reshuffle_result = asyncio.run(reshuffle_result)
    
    print(f"📋 Order before: {reshuffle_result.get('before', [])}")
    print(f"📋 Order after: {reshuffle_result.get('after', [])}")
    
    if reshuffle_result.get('changed'):
        print("✅ Reshuffle successful!")
    else:
        print("❌ Reshuffle failed")
        if reshuffle_result.get('error'):
            print(f"   Error: {reshuffle_result['error']}")
    
    time.sleep(1)
    page.screenshot(path="reports/screenshots/dialog_reshuffle_03_after_reshuffle.png", full_page=True)
    
    # Test drag and drop simulation
    print("🔄 Testing drag and drop simulation in dialog...")
    
    drag_result = page.evaluate(f"""
        () => {{
            const dialog = window.currentPlaceholderDialog || document.querySelector('.placeholder-selection-dialog');
            if (!dialog) return {{ error: 'Dialog not found' }};
            
            const preview = dialog.querySelector('#dialogPreview');
            if (!preview) return {{ error: 'Preview not found' }};
            
            const placeholder = '{placeholder}';
            const placeholderKey = '{placeholder.lower()}';
            
            // Get all cells in preview
            const allCellsInPreview = Array.from(preview.querySelectorAll('.media-cell'));
            
            // Get cells for this placeholder - try multiple ways
            let cells = [];
            
            // Method 1: Exact match
            cells = allCellsInPreview.filter(c => c.dataset.placeholder === placeholder);
            
            // Method 2: Case-insensitive match
            if (cells.length === 0) {{
                cells = allCellsInPreview.filter(c => c.dataset.placeholder && 
                    c.dataset.placeholder.toLowerCase() === placeholderKey);
            }}
            
            // Method 3: Contains match
            if (cells.length === 0) {{
                cells = allCellsInPreview.filter(c => c.dataset.placeholder && 
                    (c.dataset.placeholder.includes(placeholder) || 
                     c.dataset.placeholder.toLowerCase().includes(placeholderKey)));
            }}
            
            // Method 4: Check parent table
            if (cells.length === 0) {{
                const tables = Array.from(preview.querySelectorAll('table.placeholder-table'));
                tables.forEach(table => {{
                    if (table.dataset.placeholder === placeholder || 
                        table.dataset.placeholder?.toLowerCase() === placeholderKey) {{
                        const tableCells = Array.from(table.querySelectorAll('.media-cell'));
                        cells = cells.concat(tableCells);
                    }}
                }});
            }}
            
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
                    cellsFound: cells.length,
                    cellIndices: cells.map(c => c.dataset.mediaIndex)
                }};
            }}
            
            // Get assignments before
            const assignments = window.getCurrentAssignments();
            const before = (assignments[placeholderKey] || []).map(m => m.name);
            
            if (before.length === 0) {{
                return {{ error: 'No assignments found', assignmentsKeys: Object.keys(assignments) }};
            }}
            
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
                dropEffect: 'move',
                types: ['application/json', 'text/plain']
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
                window.handleDialogPreviewDrop(dropEvent);
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
    
    # Handle promise
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
    
    time.sleep(1)
    page.screenshot(path="reports/screenshots/dialog_reshuffle_04_final.png", full_page=True)
    
    print("\n✅ Test complete!")
    print(f"📁 Screenshots saved in reports/screenshots/")
    
    time.sleep(2)
    browser.close()

