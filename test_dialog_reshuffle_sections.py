#!/usr/bin/env python3
"""Test reshuffle in dialog window with sections"""
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
    
    # Enable bulk select mode
    print("🖱️  Enabling bulk select mode...")
    page.evaluate("""
        () => {
            const checkbox = document.getElementById('bulkSelectMode');
            if (checkbox) {
                checkbox.checked = true;
                checkbox.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }
    """)
    time.sleep(1)
    
    # Select media cards
    print("🖱️  Selecting media cards...")
    for i in range(4):
        page.evaluate(f"""
            () => {{
                const cards = Array.from(document.querySelectorAll('.observation-media-card:not(.media-assigned)'));
                if (cards.length > {i}) {{
                    const card = cards[{i}];
                    if (!card.classList.contains('media-selected')) {{
                        card.click();
                    }}
                }}
            }}
        """)
        time.sleep(0.3)
    
    time.sleep(1)
    
    # Click "Assign Selected" to open dialog
    print("📎 Opening dialog...")
    page.evaluate("""
        () => {
            const btn = document.getElementById('bulkAssignBtn');
            if (btn) btn.click();
        }
    """)
    time.sleep(3)
    
    # Check if dialog is open
    dialog_status = page.evaluate("""
        () => {
            const dialog = window.currentPlaceholderDialog || document.querySelector('.placeholder-selection-dialog');
            return {
                found: !!dialog,
                hasPreview: dialog && !!dialog.querySelector('#dialogPreview')
            };
        }
    """)
    
    print(f"Dialog status: {dialog_status}")
    
    if not dialog_status.get('found'):
        print("❌ Dialog not found")
        browser.close()
        exit(1)
    
    # Assign media in dialog
    placeholder = "Site_Arrival_and_Induction_table"
    print(f"📎 Assigning media in dialog to: {placeholder}")
    
    assign_result = page.evaluate(f"""
        () => {{
            const dialog = window.currentPlaceholderDialog || document.querySelector('.placeholder-selection-dialog');
            if (!dialog) return {{ error: 'Dialog not found' }};
            
            const mediaList = window.bulkSelectedMedia || [];
            const placeholder = '{placeholder}';
            const placeholderKey = '{placeholder.lower()}';
            
            // Get assignments before
            const assignments = window.getCurrentAssignments();
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
    
    if hasattr(assign_result, '__await__'):
        import asyncio
        assign_result = asyncio.run(assign_result)
    
    print(f"Assignment result: {assign_result}")
    time.sleep(1)
    page.screenshot(path="reports/screenshots/dialog_section_01_after_assignment.png", full_page=True)
    print("📸 Screenshot 1: After assignment in dialog")
    
    # Check section state in dialog
    section_state = page.evaluate("""
        () => {
            const dialog = window.currentPlaceholderDialog || document.querySelector('.placeholder-selection-dialog');
            if (!dialog) return { error: 'Dialog not found' };
            
            const preview = dialog.querySelector('#dialogPreview');
            if (!preview) return { error: 'Preview not found' };
            
            // Dialog uses .dialog-section, not .observation-section
            const sections = Array.from(preview.querySelectorAll('.dialog-section'));
            const sectionContents = Array.from(preview.querySelectorAll('.dialog-section-content'));
            
            return {
                sections: sections.map(section => ({
                    id: section.querySelector('.dialog-section-content')?.dataset.sectionId,
                    className: section.className
                })),
                sectionContents: sectionContents.map(content => ({
                    id: content.dataset.sectionId,
                    display: content.style.display,
                    isVisible: content.offsetParent !== null
                }))
            };
        }
    """)
    print(f"📋 Section states in dialog after assignment: {section_state}")
    
    # Enable reshuffle mode in dialog
    print("🔄 Enabling reshuffle mode in dialog...")
    reshuffle_enabled = page.evaluate("""
        () => {
            const dialog = window.currentPlaceholderDialog || document.querySelector('.placeholder-selection-dialog');
            if (!dialog) return { error: 'Dialog not found' };
            
            const btn = dialog.querySelector('#dialogReshuffleBtn button');
            if (!btn) return { error: 'Button not found' };
            
            btn.click();
            
            return new Promise(resolve => {
                setTimeout(() => {
                    const preview = dialog.querySelector('#dialogPreview');
                    const sections = preview ? Array.from(preview.querySelectorAll('.observation-section')) : [];
                    const sectionStates = sections.map(section => ({
                        id: section.dataset.sectionId,
                        isCollapsed: section.classList.contains('collapsed'),
                        hasContent: section.querySelector('.observation-section-content')?.style.display !== 'none'
                    }));
                    
                    resolve({
                        clicked: true,
                        btnText: btn.textContent,
                        sectionStates: sectionStates
                    });
                }, 500);
            });
        }
    """)
    
    if hasattr(reshuffle_enabled, '__await__'):
        import asyncio
        reshuffle_enabled = asyncio.run(reshuffle_enabled)
    
    print(f"Reshuffle enabled: {reshuffle_enabled}")
    print(f"📋 Section states after enabling reshuffle: {reshuffle_enabled.get('sectionStates', [])}")
    time.sleep(1)
    page.screenshot(path="reports/screenshots/dialog_section_02_reshuffle_enabled.png", full_page=True)
    print("📸 Screenshot 2: Reshuffle mode enabled in dialog")
    
    # Perform reshuffle in dialog
    print("🔄 Performing reshuffle in dialog...")
    
    # Check section state before reshuffle
    section_before = page.evaluate("""
        () => {
            const dialog = window.currentPlaceholderDialog || document.querySelector('.placeholder-selection-dialog');
            if (!dialog) return { error: 'Dialog not found' };
            const preview = dialog.querySelector('#dialogPreview');
            if (!preview) return { error: 'Preview not found' };
            
            // Dialog uses .dialog-section-content, not .observation-section
            const sectionContents = Array.from(preview.querySelectorAll('.dialog-section-content'));
            return sectionContents.map(content => ({
                id: content.dataset.sectionId,
                display: content.style.display,
                isVisible: content.offsetParent !== null,
                computedDisplay: window.getComputedStyle(content).display
            }));
        }
    """)
    print(f"📋 Section states BEFORE reshuffle: {section_before}")
    
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
            
            // Get cells
            const allCellsInPreview = Array.from(preview.querySelectorAll('.media-cell'));
            let cells = [];
            
            cells = allCellsInPreview.filter(c => c.dataset.placeholder === placeholder);
            if (cells.length === 0) {{
                cells = allCellsInPreview.filter(c => c.dataset.placeholder && 
                    c.dataset.placeholder.toLowerCase() === placeholderKey);
            }}
            
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
            
            // Wait and check
            return new Promise(resolve => {{
                setTimeout(() => {{
                    // Check section states after reshuffle
                    const sections = Array.from(preview.querySelectorAll('.observation-section'));
                    const sectionStates = sections.map(section => ({{
                        id: section.dataset.sectionId,
                        isCollapsed: section.classList.contains('collapsed'),
                        hasContent: section.querySelector('.observation-section-content')?.style.display !== 'none'
                    }}));
                    
                    const assignmentsAfter = window.getCurrentAssignments();
                    const after = (assignmentsAfter[placeholderKey] || []).map(m => m.name);
                    
                    resolve({{
                        before,
                        after,
                        changed: JSON.stringify(before) !== JSON.stringify(after),
                        sectionStates: sectionStates
                    }});
                }}, 1000);
            }});
        }}
    """)
    
    if hasattr(reshuffle_result, '__await__'):
        import asyncio
        reshuffle_result = asyncio.run(reshuffle_result)
    
    print(f"📋 Order before: {reshuffle_result.get('before', [])}")
    print(f"📋 Order after: {reshuffle_result.get('after', [])}")
    print(f"📋 Section states AFTER reshuffle: {reshuffle_result.get('sectionStates', [])}")
    
    if reshuffle_result.get('changed'):
        print("✅ Reshuffle successful!")
    else:
        print("❌ Reshuffle failed")
    
    time.sleep(1)
    page.screenshot(path="reports/screenshots/dialog_section_03_after_reshuffle.png", full_page=True)
    print("📸 Screenshot 3: After reshuffle in dialog")
    
    # Final check
    section_final = page.evaluate("""
        () => {
            const dialog = window.currentPlaceholderDialog || document.querySelector('.placeholder-selection-dialog');
            if (!dialog) return { error: 'Dialog not found' };
            const preview = dialog.querySelector('#dialogPreview');
            if (!preview) return { error: 'Preview not found' };
            
            const sections = Array.from(preview.querySelectorAll('.observation-section'));
            return sections.map(section => ({
                id: section.dataset.sectionId,
                isCollapsed: section.classList.contains('collapsed'),
                hasContent: section.querySelector('.observation-section-content')?.style.display !== 'none',
                className: section.className
            }));
        }
    """)
    print(f"📋 Section states FINAL check: {section_final}")
    
    time.sleep(1)
    page.screenshot(path="reports/screenshots/dialog_section_04_final_state.png", full_page=True)
    print("📸 Screenshot 4: Final state in dialog")
    
    print("\n✅ Test complete!")
    print(f"📁 Screenshots saved in reports/screenshots/")
    
    time.sleep(2)
    browser.close()

