#!/usr/bin/env python3
"""Test reshuffle with sections to diagnose collapse issue"""
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
    
    # Assign first 4 media items to the placeholder
    placeholder = "Site_Arrival_and_Induction_table"
    print(f"📎 Assigning media to placeholder: {placeholder}")
    
    for i, media in enumerate(media_list[:4]):
        result = page.evaluate(f"""
            () => {{
                const media = {json.dumps(media)};
                const placeholder = '{placeholder}';
                
                const result = window.assignMediaToPlaceholder(placeholder, media);
                window.updatePreview();
                window.updatePlaceholderStats();
                
                return {{
                    success: result,
                    assigned: (window.getCurrentAssignments()[placeholder.toLowerCase()] || []).length,
                    mediaName: media.name
                }};
            }}
        """)
        
        print(f"  ✓ Assigned {result['mediaName']} (total: {result['assigned']})")
        time.sleep(0.5)
    
    # Take screenshot after assignment
    page.screenshot(path="reports/screenshots/reshuffle_section_01_after_assignment.png", full_page=True)
    print("📸 Screenshot 1: After assignment")
    
    # Check section state
    section_state = page.evaluate("""
        () => {
            const sections = Array.from(document.querySelectorAll('.observation-section'));
            return sections.map(section => ({
                id: section.dataset.sectionId,
                isCollapsed: section.classList.contains('collapsed'),
                hasContent: section.querySelector('.observation-section-content')?.style.display !== 'none'
            }));
        }
    """)
    print(f"📋 Section states after assignment: {section_state}")
    time.sleep(1)
    
    # Enable reshuffle mode
    print("🔄 Enabling reshuffle mode...")
    reshuffle_enabled = page.evaluate("""
        () => {
            const btn = document.getElementById('reshuffleBtn');
            if (!btn) return { error: 'Button not found' };
            
            btn.click();
            
            return new Promise(resolve => {
                setTimeout(() => {
                    const sections = Array.from(document.querySelectorAll('.observation-section'));
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
    page.screenshot(path="reports/screenshots/reshuffle_section_02_reshuffle_enabled.png", full_page=True)
    print("📸 Screenshot 2: Reshuffle mode enabled")
    
    # Get initial order
    initial_order = page.evaluate(f"""
        () => {{
            const assignments = window.getCurrentAssignments();
            const placeholderKey = '{placeholder.lower()}';
            return (assignments[placeholderKey] || []).map(m => m.name);
        }}
    """)
    
    print(f"📋 Initial order: {initial_order}")
    
    # Perform reshuffle: move item from index 0 to index 2
    print("🔄 Performing reshuffle: moving item from index 0 to index 2...")
    
    # Check section state before reshuffle
    section_before = page.evaluate("""
        () => {
            const sections = Array.from(document.querySelectorAll('.observation-section'));
            return sections.map(section => ({
                id: section.dataset.sectionId,
                isCollapsed: section.classList.contains('collapsed'),
                hasContent: section.querySelector('.observation-section-content')?.style.display !== 'none'
            }));
        }
    """)
    print(f"📋 Section states BEFORE reshuffle: {section_before}")
    
    reshuffle_result = page.evaluate(f"""
        () => {{
            const placeholder = '{placeholder}';
            const placeholderKey = '{placeholder.lower()}';
            const fromIndex = 0;
            const targetIndex = 2;
            
            // Get all cells
            const allCellsInPreview = Array.from(document.querySelectorAll('.media-cell'));
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
                    const sections = Array.from(document.querySelectorAll('.observation-section'));
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
    page.screenshot(path="reports/screenshots/reshuffle_section_03_after_reshuffle.png", full_page=True)
    print("📸 Screenshot 3: After reshuffle")
    
    # Check section states one more time
    section_final = page.evaluate("""
        () => {
            const sections = Array.from(document.querySelectorAll('.observation-section'));
            return sections.map(section => ({
                id: section.dataset.sectionId,
                isCollapsed: section.classList.contains('collapsed'),
                hasContent: section.querySelector('.observation-section-content')?.style.display !== 'none',
                innerHTML: section.innerHTML.substring(0, 100)
            }));
        }
    """)
    print(f"📋 Section states FINAL check: {section_final}")
    
    # Check localStorage for section states
    storage_states = page.evaluate("""
        () => {
            try {
                const stored = localStorage.getItem('observationSectionStates');
                return stored ? JSON.parse(stored) : {};
            } catch (e) {
                return { error: str(e) };
            }
        }
    """)
    print(f"📋 localStorage section states: {storage_states}")
    
    time.sleep(1)
    page.screenshot(path="reports/screenshots/reshuffle_section_04_final_state.png", full_page=True)
    print("📸 Screenshot 4: Final state")
    
    print("\n✅ Test complete!")
    print(f"📁 Screenshots saved in reports/screenshots/")
    
    time.sleep(2)
    browser.close()


