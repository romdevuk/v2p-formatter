/**
 * Observation Media Module - Client-side JavaScript (API-free)
 * All processing done client-side, no API calls
 */

// Placeholder pattern: {{Placeholder_Name}} (case-insensitive, underscores only)
const PLACEHOLDER_PATTERN = /\{\{([A-Za-z0-9_]+)\}\}/g;

// Rainbow color palette
const PLACEHOLDER_COLORS = [
    '#ff6b6b',  // Red
    '#4ecdc4',  // Cyan
    '#45b7d1',  // Blue
    '#f9ca24',  // Yellow
    '#6c5ce7',  // Purple
    '#a29bfe',  // Lavender
    '#fd79a8',  // Pink
    '#00b894',  // Green
];

/**
 * Extract placeholders from text (client-side, API-free)
 */
function extractPlaceholders(text) {
    if (!text) return [];
    
    const matches = [];
    let match;
    const pattern = new RegExp(PLACEHOLDER_PATTERN);
    
    while ((match = pattern.exec(text)) !== null) {
        matches.push(match[1].toLowerCase());
    }
    
    // Return unique placeholders, sorted
    return [...new Set(matches)].sort();
}

/**
 * Assign colors to placeholders (client-side, API-free)
 */
function assignPlaceholderColors(placeholders) {
    const colorMap = {};
    placeholders.forEach((placeholder, index) => {
        colorMap[placeholder] = PLACEHOLDER_COLORS[index % PLACEHOLDER_COLORS.length];
    });
    return colorMap;
}

/**
 * Validate placeholder assignments (client-side, API-free)
 */
function validatePlaceholders(text, assignments) {
    const placeholders = extractPlaceholders(text);
    const assignedPlaceholders = new Set(Object.keys(assignments).map(k => k.toLowerCase()));
    
    const unassigned = placeholders.filter(p => !assignedPlaceholders.has(p));
    const assigned = placeholders.filter(p => assignedPlaceholders.has(p));
    
    return {
        all_placeholders: placeholders,
        assigned: assigned,
        unassigned: unassigned,
        is_valid: unassigned.length === 0,
        total_count: placeholders.length,
        assigned_count: assigned.length,
        unassigned_count: unassigned.length
    };
}

/**
 * Highlight placeholders in text editor with rainbow colors
 */
function highlightPlaceholdersInEditor() {
    const editor = document.getElementById('observationTextEditor');
    if (!editor) return;
    
    const text = editor.value;
    const placeholders = extractPlaceholders(text);
    const colorMap = assignPlaceholderColors(placeholders);
    
    // Update placeholder count
    document.getElementById('placeholderCount').textContent = placeholders.length;
    
    // Update word count
    const words = text.trim().split(/\s+/).filter(w => w.length > 0);
    document.getElementById('wordCount').textContent = words.length;
    
    // Update assigned/unassigned counts (will be updated when assignments change)
    updatePlaceholderStats();
    
    // Apply rainbow colors to placeholders in preview
    updatePreview();
}

/**
 * Update placeholder statistics
 */
function updatePlaceholderStats() {
    const editor = document.getElementById('observationTextEditor');
    if (!editor) return;
    
    const text = editor.value;
    const assignments = getCurrentAssignments(); // Get from state
    const validation = validatePlaceholders(text, assignments);
    
    document.getElementById('assignedCount').textContent = validation.assigned_count;
    document.getElementById('unassignedCount').textContent = validation.unassigned_count;
    
    // Highlight unassigned placeholders
    highlightUnassignedPlaceholders(validation.unassigned);
}

/**
 * Highlight unassigned placeholders in preview
 */
function highlightUnassignedPlaceholders(unassigned) {
    // Unassigned placeholders are already highlighted in the preview
    // with red color and empty tables
    // This function can be extended for additional visual feedback
}

/**
 * Get current media assignments (from state)
 */
function getCurrentAssignments() {
    // Get from global state
    return window.observationMediaAssignments || {};
}

/**
 * Assign media to a placeholder
 */
function assignMediaToPlaceholder(placeholder, media, targetIndex = null) {
    if (!window.observationMediaAssignments) {
        window.observationMediaAssignments = {};
    }
    
    const placeholderKey = placeholder.toLowerCase();
    if (!window.observationMediaAssignments[placeholderKey]) {
        window.observationMediaAssignments[placeholderKey] = [];
    }
    
    // Check if already assigned
    const existing = window.observationMediaAssignments[placeholderKey].find(m => m.path === media.path);
    if (existing) {
        return false; // Already assigned
    }
    
    // Add media to placeholder at specific index or append
    if (targetIndex !== null && targetIndex >= 0 && targetIndex <= window.observationMediaAssignments[placeholderKey].length) {
        // Insert at specific position
        window.observationMediaAssignments[placeholderKey].splice(targetIndex, 0, media);
    } else {
        // Append to end
        window.observationMediaAssignments[placeholderKey].push(media);
    }
    
    // Update UI
    updateMediaCardStates();
    updatePreview();
    updatePlaceholderStats();
    
    return true;
}

/**
 * Remove media from placeholder
 */
function removeMediaFromPlaceholder(placeholder, mediaPath) {
    const placeholderKey = placeholder.toLowerCase();
    if (window.observationMediaAssignments[placeholderKey]) {
        window.observationMediaAssignments[placeholderKey] = window.observationMediaAssignments[placeholderKey].filter(m => m.path !== mediaPath);
        
        // Clean up empty assignments
        if (window.observationMediaAssignments[placeholderKey].length === 0) {
            delete window.observationMediaAssignments[placeholderKey];
        }
        
        // Update UI
        updateMediaCardStates();
        updatePreview();
        updatePlaceholderStats();
    }
}

/**
 * Update media card states (enabled/disabled)
 */
function updateMediaCardStates() {
    const cards = document.querySelectorAll('.observation-media-card');
    cards.forEach(card => {
        const mediaPath = card.dataset.mediaPath;
        const isAssigned = isMediaAssigned(mediaPath);
        
        if (isAssigned) {
            card.classList.add('media-assigned');
            card.style.opacity = '0.5';
            card.style.cursor = 'not-allowed';
            card.draggable = false;
            
            // Update badge
            let badge = card.querySelector('.assigned-badge');
            if (!badge) {
                const thumbnail = card.querySelector('.observation-media-thumbnail');
                if (thumbnail) {
                    badge = document.createElement('span');
                    badge.className = 'assigned-badge';
                    badge.textContent = '✓ Assigned';
                    thumbnail.appendChild(badge);
                }
            }
        } else {
            card.classList.remove('media-assigned');
            card.style.opacity = '1';
            card.style.cursor = 'grab';
            card.draggable = true;
            
            // Remove badge
            const badge = card.querySelector('.assigned-badge');
            if (badge) {
                badge.remove();
            }
        }
    });
}

/**
 * Check if media is assigned
 */
function isMediaAssigned(mediaPath) {
    const assignments = getCurrentAssignments();
    for (const placeholder in assignments) {
        if (assignments[placeholder].some(m => m.path === mediaPath)) {
            return true;
        }
    }
    return false;
}

/**
 * Show placeholder selection dialog (supports single or bulk media)
 */
function showPlaceholderSelectionDialog(media, placeholders) {
    console.log('========================================');
    console.log('[DIALOG] ===== showPlaceholderSelectionDialog CALLED =====');
    console.log('[DIALOG] media:', media);
    console.log('[DIALOG] placeholders:', placeholders);
    console.log('[DIALOG] typeof media:', typeof media);
    console.log('[DIALOG] Array.isArray(media):', Array.isArray(media));
    alert('Dialog opening - check console for logs');
    
    // Handle both single media object and array of media
    const isBulk = Array.isArray(media);
    const mediaList = isBulk ? media : [media];
    console.log('[DIALOG] isBulk:', isBulk, 'mediaList length:', mediaList.length);
    
    const colorMap = assignPlaceholderColors(placeholders);
    const assignments = getCurrentAssignments();
    
    // Get text editor content to parse sections
    const textEditor = document.getElementById('observationTextEditor');
    const text = textEditor ? textEditor.value : '';
    const sectionData = parseSections(text);
    
    // Group placeholders by section
    const placeholdersBySection = {};
    const unassignedPlaceholders = [];
    
    if (sectionData.hasSections) {
        // Initialize sections
        sectionData.sections.forEach(section => {
            placeholdersBySection[section.id] = {
                section: section,
                placeholders: []
            };
        });
        
        // Assign each placeholder to its section
        placeholders.forEach(placeholder => {
            let found = false;
            // Find which section contains this placeholder
            for (let i = 0; i < sectionData.sections.length; i++) {
                const section = sectionData.sections[i];
                const placeholderPattern = new RegExp(`\\{\\{${placeholder}\\}\\}`, 'i');
                if (placeholderPattern.test(section.content)) {
                    placeholdersBySection[section.id].placeholders.push(placeholder);
                    found = true;
                    break;
                }
            }
            if (!found) {
                // Check if placeholder is in pre-section content
                const placeholderPattern = new RegExp(`\\{\\{${placeholder}\\}\\}`, 'i');
                if (placeholderPattern.test(sectionData.preSectionContent)) {
                    unassignedPlaceholders.push(placeholder);
                } else {
                    // Default to unassigned
                    unassignedPlaceholders.push(placeholder);
                }
            }
        });
    } else {
        // No sections - all placeholders are unassigned
        unassignedPlaceholders.push(...placeholders);
    }
    
    // Create dialog
    const dialog = document.createElement('div');
    dialog.className = 'placeholder-selection-dialog';
    dialog.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #2a2a2a;
        border: 2px solid #667eea;
        border-radius: 8px;
        padding: 20px;
        z-index: 10000;
        min-width: 500px;
        max-width: 900px;
        width: 80vw;
        max-height: 85vh;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        display: flex;
        flex-direction: column;
    `;
    
    // Store selected media globally for drag-and-drop
    window.bulkSelectedMedia = mediaList;
    console.log('[DIALOG] Stored bulkSelectedMedia:', window.bulkSelectedMedia);
    console.log('[DIALOG] handleBulkMediaDragStart available:', typeof handleBulkMediaDragStart);
    console.log('[DIALOG] window.handleBulkMediaDragStart available:', typeof window.handleBulkMediaDragStart);
    
    let dialogHTML = `
        <h3 style="color: #e0e0e0; margin-bottom: 15px;">Assign Media to Placeholder</h3>
        <div style="margin-bottom: 15px; padding: 10px; background: #1e1e1e; border-radius: 4px; border: 1px solid #555;">
            <div style="color: #999; font-size: 12px; margin-bottom: 8px;">Selected Media (${mediaList.length}):</div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px; max-height: 120px; overflow-y: auto;" id="bulkMediaThumbnails">
    `;
    
    // Show thumbnails of selected media - make them draggable with remove action
    mediaList.forEach((media, index) => {
        const thumbnailId = `bulk-thumb-${index}`;
        dialogHTML += `
            <div id="${thumbnailId}" 
                 class="bulk-media-thumbnail"
                 data-media-path="${media.path}"
                 data-media-name="${media.name}"
                 data-media-type="${media.type}"
                 data-media-index="${index}"
                 draggable="true"
                 style="position: relative; width: 80px; height: 60px; border: 2px solid #667eea; border-radius: 4px; overflow: hidden; background: #1a1a1a; cursor: grab; user-select: none;">
                <img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(media.path)}&size=80x60" 
                     alt="${media.name}" 
                     draggable="false"
                     style="width: 100%; height: 100%; object-fit: cover; pointer-events: none; user-select: none;">
                ${media.type === 'video' ? '<span style="position: absolute; top: 2px; right: 2px; background: rgba(0,0,0,0.7); color: white; font-size: 8px; padding: 2px 4px; border-radius: 2px; pointer-events: none;">⏯</span>' : ''}
                <button class="bulk-thumb-remove-btn" 
                        data-index="${index}"
                        style="position: absolute; top: 2px; left: 2px; background: #ff6b6b; color: white; border: none; border-radius: 50%; width: 20px; height: 20px; cursor: pointer; font-size: 12px; line-height: 1; display: flex; align-items: center; justify-content: center; padding: 0; z-index: 10;"
                        title="Remove from selection">×</button>
            </div>
        `;
    });
    
    dialogHTML += `
            </div>
            <div style="color: #999; font-size: 11px; margin-top: 8px;">💡 Tip: Drag thumbnails to drop zones below OR click on placeholder tables to assign</div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px; margin-bottom: 10px; padding: 10px; background: #1e1e1e; border-radius: 4px; border: 1px solid #555;">
            <div style="color: #e0e0e0; font-size: 14px; font-weight: bold;">Live Preview:</div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <div id="dialogSectionControls" style="display: ${sectionData.hasSections ? 'flex' : 'none'}; gap: 8px;">
                    <button onclick="expandAllDialogSections()" 
                            style="padding: 6px 12px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">
                        ▼ Expand All
                    </button>
                    <button onclick="collapseAllDialogSections()" 
                            style="padding: 6px 12px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">
                        ▶ Collapse All
                    </button>
                </div>
                <div id="dialogReshuffleBtn" style="display: none;">
                    <button onclick="toggleDialogReshuffleMode()" 
                            style="padding: 6px 12px; background: #43e97b; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">
                        🔄 Reshuffle
                    </button>
                </div>
            </div>
        </div>
        <div style="max-height: 450px; overflow-y: auto; flex: 1; padding: 15px; background: #1e1e1e; border-radius: 4px; border: 1px solid #555;"
             ondrop="handleDialogPreviewDrop(event)" 
             ondragover="handleDialogPreviewDragOver(event)">
            <div id="dialogPreview" style="color: #e0e0e0; font-size: 13px; line-height: 1.6;">
    `;
    
    // Generate preview HTML using the same logic as the main preview
    const validation = validatePlaceholders(text, assignments);
    let previewHtml = '';
    
    if (sectionData.hasSections) {
        // Render with sections
        previewHtml = renderSectionsForDialog(sectionData, placeholders, colorMap, assignments, validation, mediaList);
    } else {
        // Render without sections
        let previewHtmlTemp = '';
        let lastIndex = 0;
        
        // Find all placeholder positions in the text
        const placeholderPositions = [];
        placeholders.forEach(placeholder => {
            const pattern = new RegExp(`\\{\\{${placeholder}\\}\\}`, 'gi');
            let match;
            while ((match = pattern.exec(text)) !== null) {
                placeholderPositions.push({
                    start: match.index,
                    end: match.index + match[0].length,
                    placeholder: placeholder
                });
            }
        });
        
        // Sort by position
        placeholderPositions.sort((a, b) => a.start - b.start);
        
        // Build HTML by escaping text segments and inserting HTML tables
        placeholderPositions.forEach(pos => {
            // Add escaped text before this placeholder
            if (pos.start > lastIndex) {
                const textSegment = text.substring(lastIndex, pos.start);
                previewHtmlTemp += escapeHtml(textSegment).replace(/\n/g, '<br>');
            }
            
            // Add HTML table for this placeholder
            const placeholder = pos.placeholder;
            const assignedMedia = assignments[placeholder] || [];
            const isUnassigned = validation.unassigned.includes(placeholder);
            
            if (assignedMedia.length > 0) {
                // Generate table HTML with drag-and-drop support
                const tableHtml = generateMediaTable(assignedMedia, placeholder);
                previewHtmlTemp += tableHtml;
            } else {
                // Unassigned placeholder - show empty table with drop zone
                const emptyTable = `<div class="unassigned-placeholder-container" data-placeholder="${escapeHtml(placeholder)}">
                    <table class="placeholder-table unassigned" 
                           style="border: 2px dashed #667eea; border-collapse: collapse; width: 100%; margin: 10px 0; background: rgba(102, 126, 234, 0.1); cursor: pointer;"
                           ondrop="handleTableDrop(event, '${escapeHtml(placeholder)}')" 
                           ondragover="handleTableDragOver(event)"
                           onclick="selectPlaceholderForMedia('${placeholder}', ${JSON.stringify(mediaList).replace(/'/g, "\\'")})">
                        <tr>
                            <td style="border: 1px solid #667eea; padding: 20px; min-height: 60px; text-align: center; color: #667eea; font-size: 12px;">
                                Drop media here or click to assign
                            </td>
                            <td style="border: 1px solid #667eea; padding: 20px; min-height: 60px; text-align: center; color: #667eea; font-size: 12px;">
                                Drop media here or click to assign
                            </td>
                        </tr>
                    </table>
                    <div style="text-align: center; color: ${colorMap[placeholder]}; font-size: 11px; margin-top: 5px; font-weight: bold;">
                        {{${escapeHtml(placeholder)}}}
                    </div>
                </div>`;
                previewHtmlTemp += emptyTable;
            }
            
            lastIndex = pos.end;
        });
        
        // Add remaining text after last placeholder
        if (lastIndex < text.length) {
            const textSegment = text.substring(lastIndex);
            previewHtmlTemp += escapeHtml(textSegment).replace(/\n/g, '<br>');
        }
        
        // If no placeholders, just escape and display the text
        if (placeholderPositions.length === 0) {
            previewHtmlTemp = escapeHtml(text).replace(/\n/g, '<br>');
        }
        
        // Apply rainbow colors to any remaining placeholder text
        placeholders.forEach(placeholder => {
            const color = colorMap[placeholder];
            const placeholderPattern = new RegExp(`(\\{\\{${placeholder}\\}\\})`, 'gi');
            previewHtmlTemp = previewHtmlTemp.replace(placeholderPattern, `<span style="color: ${color}; font-weight: bold;">$1</span>`);
        });
        
        previewHtml = previewHtmlTemp;
    }
    
    dialogHTML += previewHtml;
    dialogHTML += `
            </div>
        </div>
    `;
    
    dialogHTML += `
        </div>
        <div style="margin-top: 15px; text-align: right; border-top: 1px solid #555; padding-top: 15px;">
            <button id="placeholderDialogCancelBtn" 
                    style="padding: 8px 16px; background: #555; color: white; border: none; border-radius: 4px; cursor: pointer;">
                Cancel
            </button>
        </div>
    `;
    
    dialog.innerHTML = dialogHTML;
    document.body.appendChild(dialog);
    
    // Store dialog reference
    window.currentPlaceholderDialog = dialog;
    window.currentPlaceholderDialogMedia = media;
    
    // Attach drag handlers immediately after DOM insertion
    console.log('[DIALOG] About to call attachBulkThumbnailHandlers');
    console.log('[DIALOG] attachBulkThumbnailHandlers type:', typeof attachBulkThumbnailHandlers);
    console.log('[DIALOG] window.attachBulkThumbnailHandlers type:', typeof window.attachBulkThumbnailHandlers);
    
    if (typeof attachBulkThumbnailHandlers === 'function') {
        try {
            attachBulkThumbnailHandlers(dialog, mediaList);
            console.log('[DIALOG] attachBulkThumbnailHandlers called successfully');
        } catch (err) {
            console.error('[DIALOG] Error calling attachBulkThumbnailHandlers:', err);
        }
    } else if (typeof window.attachBulkThumbnailHandlers === 'function') {
        try {
            window.attachBulkThumbnailHandlers(dialog, mediaList);
            console.log('[DIALOG] window.attachBulkThumbnailHandlers called successfully');
        } catch (err) {
            console.error('[DIALOG] Error calling window.attachBulkThumbnailHandlers:', err);
        }
    } else {
        console.error('[DIALOG] attachBulkThumbnailHandlers function not found!');
        alert('Error: attachBulkThumbnailHandlers function not found. Check console.');
    }
    
    // Update reshuffle button visibility based on assigned media
    const hasAssignedMedia = Object.keys(assignments).some(key => assignments[key] && assignments[key].length > 0);
    const dialogReshuffleBtn = dialog.querySelector('#dialogReshuffleBtn');
    if (dialogReshuffleBtn) {
        dialogReshuffleBtn.style.display = hasAssignedMedia ? 'block' : 'none';
    }
    
    // Add event listener to cancel button - use immediate function to ensure it works
    setTimeout(() => {
        const cancelBtn = dialog.querySelector('#placeholderDialogCancelBtn');
        if (cancelBtn) {
            // Remove any existing listeners by cloning
            const newCancelBtn = cancelBtn.cloneNode(true);
            cancelBtn.parentNode.replaceChild(newCancelBtn, cancelBtn);
            
            // Add fresh event listener
            newCancelBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                if (typeof closePlaceholderDialog === 'function') {
                    closePlaceholderDialog();
                } else if (typeof window.closePlaceholderDialog === 'function') {
                    window.closePlaceholderDialog();
                } else {
                    // Fallback: directly remove dialog
                    if (window.currentPlaceholderDialog) {
                        window.currentPlaceholderDialog.remove();
                        window.currentPlaceholderDialog = null;
                        window.currentPlaceholderDialogMedia = null;
                    }
                }
            });
        }
    }, 0);
    
    // Also allow closing by clicking outside the dialog
    dialog.addEventListener('click', function(e) {
        if (e.target === dialog) {
            if (typeof closePlaceholderDialog === 'function') {
                closePlaceholderDialog();
            } else if (typeof window.closePlaceholderDialog === 'function') {
                window.closePlaceholderDialog();
            } else {
                // Fallback: directly remove dialog
                if (window.currentPlaceholderDialog) {
                    window.currentPlaceholderDialog.remove();
                    window.currentPlaceholderDialog = null;
                    window.currentPlaceholderDialogMedia = null;
                }
            }
        }
    });
}

/**
 * Select placeholder for media (called from dialog)
 * Supports both single media and bulk assignment
 * Note: This is also defined in the template for inline onclick handlers
 */
function selectPlaceholderForMedia(placeholder, media) {
    // Handle both single media object and array of media
    const mediaList = Array.isArray(media) ? media : [media];
    let assignedCount = 0;
    let skippedCount = 0;
    
    mediaList.forEach(m => {
        if (assignMediaToPlaceholder(placeholder, m)) {
            assignedCount++;
        } else {
            skippedCount++;
        }
    });
    
    closePlaceholderDialog();
    
    if (skippedCount > 0 && assignedCount > 0) {
        alert(`${assignedCount} media item(s) assigned. ${skippedCount} item(s) were already assigned.`);
    } else if (skippedCount > 0) {
        alert('All selected media items are already assigned to this placeholder.');
    } else if (mediaList.length > 1) {
        alert(`${assignedCount} media items assigned successfully!`);
    }
}

/**
 * Close placeholder selection dialog
 * Note: This is also defined in the template for inline onclick handlers
 */
function closePlaceholderDialog() {
    if (window.currentPlaceholderDialog) {
        window.currentPlaceholderDialog.remove();
        window.currentPlaceholderDialog = null;
        window.currentPlaceholderDialogMedia = null;
    }
}

// Make functions globally available
if (typeof window !== 'undefined') {
    window.extractPlaceholders = extractPlaceholders;
    window.assignPlaceholderColors = assignPlaceholderColors;
    window.validatePlaceholders = validatePlaceholders;
    window.highlightPlaceholdersInEditor = highlightPlaceholdersInEditor;
    window.updatePlaceholderStats = updatePlaceholderStats;
    window.updatePreview = updatePreview;
    window.generateMediaTable = generateMediaTable;
    window.getCurrentAssignments = getCurrentAssignments;
    window.assignMediaToPlaceholder = assignMediaToPlaceholder;
    window.removeMediaFromPlaceholder = removeMediaFromPlaceholder;
    window.updateMediaCardStates = updateMediaCardStates;
    window.isMediaAssigned = isMediaAssigned;
    window.showPlaceholderSelectionDialog = showPlaceholderSelectionDialog;
    window.selectPlaceholderForMedia = selectPlaceholderForMedia;
    window.closePlaceholderDialog = closePlaceholderDialog;
    window.handleTableDrop = handleTableDrop;
    window.handleTableDragOver = handleTableDragOver;
    window.handleTableCellDragStart = handleTableCellDragStart;
    window.handleTableCellClick = handleTableCellClick;
    window.removeMediaFromTable = removeMediaFromTable;
    window.reorderMediaInPlaceholder = reorderMediaInPlaceholder;
    window.exportObservationDocx = exportObservationDocx;
    window.showSaveDraftDialog = showSaveDraftDialog;
    window.showLoadDraftDialog = showLoadDraftDialog;
    window.saveDraft = saveDraft;
    window.loadDraft = loadDraft;
    window.deleteDraft = deleteDraft;
    window.closeDraftDialog = closeDraftDialog;
    window.loadObservationMedia = loadObservationMedia;
}

/**
 * Show save draft dialog
 */
function showSaveDraftDialog() {
    const name = prompt('Enter draft name:', 'My Draft');
    if (!name) return;
    
    saveDraft(name);
}

/**
 * Save current draft
 */
function saveDraft(name) {
    const editor = document.getElementById('observationTextEditor');
    if (!editor) return;
    
    const text = editor.value;
    const assignments = getCurrentAssignments();
    const selectedSubfolder = document.getElementById('observationSubfolderSelect')?.value || null;
    
    // Show loading state
    const saveBtn = document.getElementById('saveDraftBtn');
    const originalText = saveBtn.textContent;
    saveBtn.disabled = true;
    saveBtn.textContent = '⏳ Saving...';
    
    // Save draft via API
    fetch('/v2p-formatter/media-converter/observation-media/drafts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: name,
            text_content: text,
            assignments: assignments,
            selected_subfolder: selectedSubfolder
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`Draft saved successfully!\n\nName: ${data.draft_name}`);
        } else {
            alert(`Error saving draft: ${data.error || 'Unknown error'}`);
        }
    })
    .catch(error => {
        console.error('Save draft error:', error);
        alert(`Error saving draft: ${error.message}`);
    })
    .finally(() => {
        saveBtn.disabled = false;
        saveBtn.textContent = originalText;
    });
}

/**
 * Show load draft dialog
 */
function showLoadDraftDialog() {
    // Load list of drafts
    fetch('/v2p-formatter/media-converter/observation-media/drafts')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.drafts.length > 0) {
                showDraftSelectionDialog(data.drafts);
            } else {
                alert('No drafts found.');
            }
        })
        .catch(error => {
            console.error('Load drafts error:', error);
            alert(`Error loading drafts: ${error.message}`);
        });
}

/**
 * Show draft selection dialog
 */
function showDraftSelectionDialog(drafts) {
    const dialog = document.createElement('div');
    dialog.className = 'draft-selection-dialog';
    dialog.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #2a2a2a;
        border: 2px solid #667eea;
        border-radius: 8px;
        padding: 20px;
        z-index: 10000;
        min-width: 500px;
        max-width: 700px;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    `;
    
    let dialogHTML = `
        <h3 style="color: #e0e0e0; margin-bottom: 15px;">Load Draft</h3>
        <div style="max-height: 400px; overflow-y: auto;">
    `;
    
    drafts.forEach(draft => {
        const date = new Date(draft.updated_at || draft.created_at);
        const dateStr = date.toLocaleString();
        
        dialogHTML += `
            <div class="draft-item" 
                 style="padding: 12px; margin-bottom: 8px; background: #1e1e1e; border: 1px solid #555; border-radius: 4px; cursor: pointer;"
                 onclick="loadDraft('${draft.id}'); closeDraftDialog();">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #e0e0e0; font-weight: bold; margin-bottom: 4px;">${draft.name}</div>
                        <div style="color: #999; font-size: 11px;">
                            Updated: ${dateStr}
                            ${draft.selected_subfolder ? ` • Subfolder: ${draft.selected_subfolder}` : ''}
                            ${draft.placeholder_count ? ` • ${draft.placeholder_count} placeholders` : ''}
                        </div>
                    </div>
                    <div style="display: flex; gap: 5px;">
                        <button onclick="event.stopPropagation(); loadDraft('${draft.id}'); closeDraftDialog();" 
                                style="padding: 6px 12px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">
                            Load
                        </button>
                        <button onclick="event.stopPropagation(); deleteDraft('${draft.id}'); closeDraftDialog(); showLoadDraftDialog();" 
                                style="padding: 6px 12px; background: #ff6b6b; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    dialogHTML += `
        </div>
        <div style="margin-top: 15px; text-align: right;">
            <button onclick="closeDraftDialog()" 
                    style="padding: 8px 16px; background: #555; color: white; border: none; border-radius: 4px; cursor: pointer;">
                Cancel
            </button>
        </div>
    `;
    
    dialog.innerHTML = dialogHTML;
    document.body.appendChild(dialog);
    
    // Store dialog reference
    window.currentDraftDialog = dialog;
}

/**
 * Close draft dialog
 */
function closeDraftDialog() {
    if (window.currentDraftDialog) {
        window.currentDraftDialog.remove();
        window.currentDraftDialog = null;
    }
}

/**
 * Load a draft
 */
function loadDraft(draftId) {
    fetch(`/v2p-formatter/media-converter/observation-media/drafts/${draftId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.draft) {
                const draft = data.draft;
                
                // Load text content
                const editor = document.getElementById('observationTextEditor');
                if (editor) {
                    editor.value = draft.text_content || '';
                }
                
                // Load assignments
                window.observationMediaAssignments = draft.assignments || {};
                
                // Load selected subfolder
                if (draft.selected_subfolder) {
                    const select = document.getElementById('observationSubfolderSelect');
                    if (select) {
                        select.value = draft.selected_subfolder;
                        loadObservationMedia();
                    }
                }
                
                // Update UI
                if (typeof highlightPlaceholdersInEditor === 'function') {
                    highlightPlaceholdersInEditor();
                }
                if (typeof updatePreview === 'function') {
                    updatePreview();
                }
                if (typeof updateMediaCardStates === 'function') {
                    updateMediaCardStates();
                }
                
                alert(`Draft loaded: ${draft.name}`);
            } else {
                alert(`Error loading draft: ${data.error || 'Unknown error'}`);
            }
        })
        .catch(error => {
            console.error('Load draft error:', error);
            alert(`Error loading draft: ${error.message}`);
        });
}

/**
 * Delete a draft
 */
function deleteDraft(draftId) {
    if (!confirm('Are you sure you want to delete this draft?')) {
        return;
    }
    
    fetch(`/v2p-formatter/media-converter/observation-media/drafts/${draftId}`, {
        method: 'DELETE'
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Dialog will be refreshed by caller
            } else {
                alert(`Error deleting draft: ${data.error || 'Unknown error'}`);
            }
        })
        .catch(error => {
            console.error('Delete draft error:', error);
            alert(`Error deleting draft: ${error.message}`);
        });
}

/**
 * Export observation document to DOCX
 */
function exportObservationDocx() {
    const editor = document.getElementById('observationTextEditor');
    if (!editor) return;
    
    const text = editor.value;
    const assignments = getCurrentAssignments();
    
    // Validate - check if all placeholders are assigned
    const validation = validatePlaceholders(text, assignments);
    if (!validation.is_valid) {
        const unassigned = validation.unassigned.map(p => `{{${p}}}`).join(', ');
        if (!confirm(`Some placeholders are not assigned: ${unassigned}\n\nDo you want to export anyway?`)) {
            return;
        }
    }
    
    // Get filename from user
    const filename = prompt('Enter filename (without extension):', 'observation_document');
    if (!filename) return;
    
    // Show loading state
    const exportBtn = document.getElementById('exportDocxBtn');
    const originalText = exportBtn.textContent;
    exportBtn.disabled = true;
    exportBtn.textContent = '⏳ Exporting...';
    
    // Export via API (this is the only API call needed - for file generation)
    fetch('/v2p-formatter/media-converter/observation-media/export-docx', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text: text,
            assignments: assignments,
            filename: filename
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Download file
            window.location.href = data.download_url;
            alert(`Document exported successfully!\n\nFile: ${data.file_name}`);
        } else {
            alert(`Error exporting document: ${data.error || 'Unknown error'}`);
        }
    })
    .catch(error => {
        console.error('Export error:', error);
        alert(`Error exporting document: ${error.message}`);
    })
    .finally(() => {
        exportBtn.disabled = false;
        exportBtn.textContent = originalText;
    });
}

/**
 * Section color palette
 */
const SECTION_COLORS = [
    '#667eea', // Blue
    '#f093fb', // Pink
    '#4facfe', // Light Blue
    '#43e97b', // Green
    '#fa709a', // Rose
    '#fee140', // Yellow
    '#30cfd0', // Cyan
    '#a8edea', // Aqua
    '#ff9a9e', // Coral
    '#fad0c4'  // Peach
];

/**
 * Parse sections from text
 */
function parseSections(text) {
    const sectionPattern = /^SECTION\s*[:-]?\s*(.+)$/gim;
    const sections = [];
    const lines = text.split('\n');
    let currentSection = null;
    let currentContent = [];
    let preSectionContent = [];
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const match = line.match(/^SECTION\s*[:-]?\s*(.+)$/i);
        
        if (match) {
            // Save previous section if exists
            if (currentSection) {
                currentSection.content = currentContent.join('\n');
                sections.push(currentSection);
            }
            
            // Start new section
            const title = match[1].trim();
            const sectionIndex = sections.length;
            currentSection = {
                id: `section-${sectionIndex}`,
                title: title,
                color: SECTION_COLORS[sectionIndex % SECTION_COLORS.length],
                content: '',
                index: sectionIndex
            };
            currentContent = [];
        } else {
            if (currentSection) {
                currentContent.push(line);
            } else {
                preSectionContent.push(line);
            }
        }
    }
    
    // Save last section
    if (currentSection) {
        currentSection.content = currentContent.join('\n');
        sections.push(currentSection);
    }
    
    return {
        hasSections: sections.length > 0,
        preSectionContent: preSectionContent.join('\n'),
        sections: sections
    };
}

/**
 * Get section state from localStorage
 */
function getSectionStates() {
    try {
        const stored = localStorage.getItem('observationSectionStates');
        return stored ? JSON.parse(stored) : {};
    } catch (e) {
        return {};
    }
}

/**
 * Save section state to localStorage
 */
function saveSectionStates(states) {
    try {
        localStorage.setItem('observationSectionStates', JSON.stringify(states));
    } catch (e) {
        // Ignore localStorage errors
    }
}

/**
 * Toggle section expand/collapse
 */
function toggleSection(sectionId) {
    const states = getSectionStates();
    const currentState = states[sectionId] || false;
    states[sectionId] = !currentState;
    saveSectionStates(states);
    
    const sectionEl = document.querySelector(`[data-section-id="${sectionId}"]`);
    if (sectionEl) {
        const contentEl = sectionEl.querySelector('.observation-section-content');
        const iconEl = sectionEl.querySelector('.observation-section-icon');
        
        if (states[sectionId]) {
            sectionEl.classList.remove('collapsed');
            if (contentEl) {
                contentEl.style.display = 'block';
            }
            if (iconEl) iconEl.textContent = '▼';
        } else {
            sectionEl.classList.add('collapsed');
            if (contentEl) {
                contentEl.style.display = 'none';
            }
            if (iconEl) iconEl.textContent = '▶';
        }
    }
}

/**
 * Expand all sections
 */
function expandAllSections() {
    const sections = document.querySelectorAll('.observation-section');
    const states = getSectionStates();
    
    sections.forEach(section => {
        const sectionId = section.dataset.sectionId;
        if (sectionId) {
            states[sectionId] = true;
            section.classList.remove('collapsed');
            const contentEl = section.querySelector('.observation-section-content');
            const iconEl = section.querySelector('.observation-section-icon');
            if (contentEl) {
                contentEl.style.display = 'block';
            }
            if (iconEl) iconEl.textContent = '▼';
        }
    });
    
    saveSectionStates(states);
}

/**
 * Collapse all sections
 */
function collapseAllSections() {
    const sections = document.querySelectorAll('.observation-section');
    const states = getSectionStates();
    
    sections.forEach(section => {
        const sectionId = section.dataset.sectionId;
        if (sectionId) {
            states[sectionId] = false;
            section.classList.add('collapsed');
            const contentEl = section.querySelector('.observation-section-content');
            const iconEl = section.querySelector('.observation-section-icon');
            if (contentEl) {
                contentEl.style.display = 'none';
            }
            if (iconEl) iconEl.textContent = '▶';
        }
    });
    
    saveSectionStates(states);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Render sections for dialog preview
 */
function renderSectionsForDialog(sectionData, placeholders, colorMap, assignments, validation, mediaList) {
    let html = '';
    
    // Pre-section content
    if (sectionData.preSectionContent.trim()) {
        html += escapeHtml(sectionData.preSectionContent).replace(/\n/g, '<br>');
    }
    
    // Render sections
    sectionData.sections.forEach(section => {
        const sectionContent = renderSectionContentForDialog(section.content, placeholders, colorMap, assignments, validation, mediaList);
        
        html += `
            <div class="dialog-section" style="margin-bottom: 15px; border-left: 3px solid ${section.color};">
                <div class="dialog-section-header" 
                     onclick="toggleDialogSection('${section.id}')"
                     style="padding: 8px 10px; background: ${section.color}20; border: 1px solid ${section.color}; border-radius: 4px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="color: ${section.color}; font-weight: bold; font-size: 13px;">${escapeHtml(section.title)}</span>
                    <span class="dialog-section-icon" style="color: ${section.color}; font-size: 12px;">▶</span>
                </div>
                <div class="dialog-section-content" data-section-id="${section.id}" style="padding-left: 10px; display: none;">
                    ${sectionContent}
                </div>
            </div>
        `;
    });
    
    return html;
}

/**
 * Render section content with placeholders for dialog
 */
function renderSectionContentForDialog(content, placeholders, colorMap, assignments, validation, mediaList) {
    let html = '';
    let lastIndex = 0;
    
    // Find all placeholder positions
    const placeholderPositions = [];
    placeholders.forEach(placeholder => {
        const pattern = new RegExp(`\\{\\{${placeholder}\\}\\}`, 'gi');
        let match;
        while ((match = pattern.exec(content)) !== null) {
            placeholderPositions.push({
                start: match.index,
                end: match.index + match[0].length,
                placeholder: placeholder
            });
        }
    });
    
    placeholderPositions.sort((a, b) => a.start - b.start);
    
    // Build HTML
    placeholderPositions.forEach(pos => {
        if (pos.start > lastIndex) {
            const textSegment = content.substring(lastIndex, pos.start);
            html += escapeHtml(textSegment).replace(/\n/g, '<br>');
        }
        
        const placeholder = pos.placeholder;
        const assignedMedia = assignments[placeholder] || [];
        const isUnassigned = validation.unassigned.includes(placeholder);
        
        if (assignedMedia.length > 0) {
            const tableHtml = generateMediaTable(assignedMedia, placeholder);
            html += tableHtml;
        } else {
            // Drop zone for unassigned placeholder
            const emptyTable = `<div class="unassigned-placeholder-container" data-placeholder="${escapeHtml(placeholder)}" style="margin: 10px 0;">
                <table class="placeholder-table unassigned" 
                       style="border: 2px dashed #667eea; border-collapse: collapse; width: 100%; background: rgba(102, 126, 234, 0.1); cursor: pointer;"
                       data-placeholder="${escapeHtml(placeholder)}"
                       ondrop="handleDialogPreviewDrop(event)" 
                       ondragover="handleDialogPreviewDragOver(event)"
                       onclick="selectPlaceholderForMedia('${placeholder}', ${JSON.stringify(mediaList).replace(/'/g, "\\'")})">
                    <tr>
                        <td style="border: 1px solid #667eea; padding: 15px; min-height: 50px; text-align: center; color: #667eea; font-size: 11px;"
                            data-placeholder="${escapeHtml(placeholder)}"
                            ondrop="handleDialogPreviewDrop(event)" 
                            ondragover="handleDialogPreviewDragOver(event)">
                            Drop media here or click
                        </td>
                        <td style="border: 1px solid #667eea; padding: 15px; min-height: 50px; text-align: center; color: #667eea; font-size: 11px;"
                            data-placeholder="${escapeHtml(placeholder)}"
                            ondrop="handleDialogPreviewDrop(event)" 
                            ondragover="handleDialogPreviewDragOver(event)">
                            Drop media here or click
                        </td>
                    </tr>
                </table>
                <div style="text-align: center; color: ${colorMap[placeholder]}; font-size: 10px; margin-top: 3px; font-weight: bold;">
                    {{${escapeHtml(placeholder)}}}
                </div>
            </div>`;
            html += emptyTable;
        }
        
        lastIndex = pos.end;
    });
    
    // Add remaining text
    if (lastIndex < content.length) {
        const textSegment = content.substring(lastIndex);
        html += escapeHtml(textSegment).replace(/\n/g, '<br>');
    }
    
    return html;
}

/**
 * Render section content with placeholders
 */
function renderSectionContent(content, placeholders, colorMap, assignments, validation) {
    
    let html = '';
    let lastIndex = 0;
    
    // Find all placeholder positions
    const placeholderPositions = [];
    placeholders.forEach(placeholder => {
        const pattern = new RegExp(`\\{\\{${placeholder}\\}\\}`, 'gi');
        let match;
        while ((match = pattern.exec(content)) !== null) {
            placeholderPositions.push({
                start: match.index,
                end: match.index + match[0].length,
                placeholder: placeholder
            });
        }
    });
    
    placeholderPositions.sort((a, b) => a.start - b.start);
    
    // Build HTML
    placeholderPositions.forEach(pos => {
        if (pos.start > lastIndex) {
            const textSegment = content.substring(lastIndex, pos.start);
            html += escapeHtml(textSegment).replace(/\n/g, '<br>');
        }
        
        const placeholder = pos.placeholder;
        const assignedMedia = assignments[placeholder] || [];
        
        if (assignedMedia.length > 0) {
            const tableHtml = generateMediaTable(assignedMedia, placeholder);
            html += tableHtml;
        } else {
            const emptyTable = `<div class="unassigned-placeholder-container" data-placeholder="${escapeHtml(placeholder)}">
                <table class="placeholder-table unassigned" 
                       style="border: 2px dashed #ff6b6b; border-collapse: collapse; width: 100%; margin: 10px 0; background: rgba(255, 107, 107, 0.1);"
                       ondrop="handleTableDrop(event, '${escapeHtml(placeholder)}')" 
                       ondragover="handleTableDragOver(event)">
                    <tr>
                        <td style="border: 1px solid #ff6b6b; padding: 20px; min-height: 80px; text-align: center; color: #ff6b6b; font-size: 12px;">
                            Drop media here
                        </td>
                        <td style="border: 1px solid #ff6b6b; padding: 20px; min-height: 80px; text-align: center; color: #ff6b6b; font-size: 12px;">
                            Drop media here
                        </td>
                    </tr>
                </table>
                <div style="text-align: center; color: #ff6b6b; font-size: 11px; margin-top: 5px;">
                    {{${escapeHtml(placeholder)}}} - Unassigned
                </div>
            </div>`;
            html += emptyTable;
        }
        
        lastIndex = pos.end;
    });
    
    if (lastIndex < content.length) {
        const textSegment = content.substring(lastIndex);
        html += escapeHtml(textSegment).replace(/\n/g, '<br>');
    }
    
    if (placeholderPositions.length === 0) {
        html = escapeHtml(content).replace(/\n/g, '<br>');
    }
    
    // Apply rainbow colors to placeholder text
    placeholders.forEach(placeholder => {
        const color = colorMap[placeholder];
        const placeholderPattern = new RegExp(`(\\{\\{${placeholder}\\}\\})`, 'gi');
        html = html.replace(placeholderPattern, `<span style="color: ${color}; font-weight: bold;">$1</span>`);
    });
    
    return html;
}

/**
 * Render sections in preview
 */
function renderSections(sectionData, placeholders, colorMap, assignments, validation) {
    const states = getSectionStates();
    let html = '';
    
    // Pre-section content
    if (sectionData.preSectionContent.trim()) {
        html += escapeHtml(sectionData.preSectionContent).replace(/\n/g, '<br>');
    }
    
    // Render sections
    sectionData.sections.forEach(section => {
        const isExpanded = states[section.id] === true;
        const sectionContent = renderSectionContent(section.content, placeholders, colorMap, assignments, validation);
        
        html += `
            <div class="observation-section ${isExpanded ? '' : 'collapsed'}" data-section-id="${section.id}" style="border-left: 3px solid ${section.color};">
                <div class="observation-section-header" onclick="toggleSection('${section.id}')" 
                     style="background: ${section.color}20; border: 1px solid ${section.color};">
                    <span style="color: ${section.color}; font-weight: bold; font-size: 16px;">${escapeHtml(section.title)}</span>
                    <span class="observation-section-icon" style="color: ${section.color}; font-size: 16px;">${isExpanded ? '▼' : '▶'}</span>
                </div>
                <div class="observation-section-content" style="border: 1px solid ${section.color}30;">
                    ${sectionContent}
                </div>
            </div>
        `;
    });
    
    return html;
}

/**
 * Update live preview
 */
function updatePreview() {
    const editor = document.getElementById('observationTextEditor');
    const preview = document.getElementById('observationPreview');
    if (!editor || !preview) return;
    
    const text = editor.value;
    const placeholders = extractPlaceholders(text);
    const colorMap = assignPlaceholderColors(placeholders);
    const assignments = getCurrentAssignments();
    const validation = validatePlaceholders(text, assignments);
    
    // Parse sections
    const sectionData = parseSections(text);
    
    let previewHtml = '';
    
    if (sectionData.hasSections) {
        // Render with sections
        previewHtml = renderSections(sectionData, placeholders, colorMap, assignments, validation);
    } else {
        // Render without sections (original behavior)
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        let previewHtmlTemp = '';
        let lastIndex = 0;
        
        // Find all placeholder positions in the text
        const placeholderPositions = [];
        placeholders.forEach(placeholder => {
            const pattern = new RegExp(`\\{\\{${placeholder}\\}\\}`, 'gi');
            let match;
            while ((match = pattern.exec(text)) !== null) {
                placeholderPositions.push({
                    start: match.index,
                    end: match.index + match[0].length,
                    placeholder: placeholder
                });
            }
        });
        
        // Sort by position
        placeholderPositions.sort((a, b) => a.start - b.start);
        
        // Build HTML by escaping text segments and inserting HTML tables
        placeholderPositions.forEach(pos => {
            // Add escaped text before this placeholder
            if (pos.start > lastIndex) {
                const textSegment = text.substring(lastIndex, pos.start);
                previewHtmlTemp += escapeHtml(textSegment).replace(/\n/g, '<br>');
            }
            
            // Add HTML table for this placeholder
            const placeholder = pos.placeholder;
            const assignedMedia = assignments[placeholder] || [];
            const isUnassigned = validation.unassigned.includes(placeholder);
            
            if (assignedMedia.length > 0) {
                // Generate table HTML with drag-and-drop support
                const tableHtml = generateMediaTable(assignedMedia, placeholder);
                previewHtmlTemp += tableHtml;
            } else {
                // Unassigned placeholder - show empty table with warning style
                const emptyTable = `<div class="unassigned-placeholder-container" data-placeholder="${escapeHtml(placeholder)}">
                    <table class="placeholder-table unassigned" 
                           style="border: 2px dashed #ff6b6b; border-collapse: collapse; width: 100%; margin: 10px 0; background: rgba(255, 107, 107, 0.1);"
                           ondrop="handleTableDrop(event, '${escapeHtml(placeholder)}')" 
                           ondragover="handleTableDragOver(event)">
                        <tr>
                            <td style="border: 1px solid #ff6b6b; padding: 20px; min-height: 80px; text-align: center; color: #ff6b6b; font-size: 12px;">
                                Drop media here
                            </td>
                            <td style="border: 1px solid #ff6b6b; padding: 20px; min-height: 80px; text-align: center; color: #ff6b6b; font-size: 12px;">
                                Drop media here
                            </td>
                        </tr>
                    </table>
                    <div style="text-align: center; color: #ff6b6b; font-size: 11px; margin-top: 5px;">
                        {{${escapeHtml(placeholder)}}} - Unassigned
                    </div>
                </div>`;
                previewHtmlTemp += emptyTable;
            }
            
            lastIndex = pos.end;
        });
        
        // Add remaining text after last placeholder
        if (lastIndex < text.length) {
            const textSegment = text.substring(lastIndex);
            previewHtmlTemp += escapeHtml(textSegment).replace(/\n/g, '<br>');
        }
        
        // If no placeholders, just escape and display the text
        if (placeholderPositions.length === 0) {
            previewHtmlTemp = escapeHtml(text).replace(/\n/g, '<br>');
        }
        
        // Apply rainbow colors to any remaining placeholder text (for text outside tables)
        placeholders.forEach(placeholder => {
            const color = colorMap[placeholder];
            const placeholderPattern = new RegExp(`(\\{\\{${placeholder}\\}\\})`, 'gi');
            previewHtmlTemp = previewHtmlTemp.replace(placeholderPattern, `<span style="color: ${color}; font-weight: bold;">$1</span>`);
        });
        
        previewHtml = previewHtmlTemp;
    }
    
    preview.innerHTML = previewHtml;
    
    // Add drag-and-drop handlers to table cells
    attachTableDragHandlers();
    
    // Show/hide section control buttons
    const sectionControls = document.getElementById('sectionControls');
    if (sectionControls) {
        sectionControls.style.display = sectionData.hasSections ? 'flex' : 'none';
    }
    
    // Show/hide reshuffle button (only when there are assigned media)
    const reshuffleBtn = document.getElementById('reshuffleBtn');
    if (reshuffleBtn) {
        const hasAssignedMedia = Object.keys(assignments).some(key => assignments[key] && assignments[key].length > 0);
        reshuffleBtn.style.display = hasAssignedMedia ? 'inline-block' : 'none';
    }
}

/**
 * Toggle reshuffle mode (enable/disable drag-and-drop reordering)
 */
let reshuffleMode = false;
function toggleReshuffleMode() {
    console.log('[RESHUFFLE] ========== toggleReshuffleMode CALLED ==========');
    console.log('[RESHUFFLE] Current reshuffleMode:', reshuffleMode);
    reshuffleMode = !reshuffleMode;
    console.log('[RESHUFFLE] New reshuffleMode:', reshuffleMode);
    const reshuffleBtn = document.getElementById('reshuffleBtn');
    console.log('[RESHUFFLE] reshuffleBtn element:', reshuffleBtn ? 'FOUND' : 'NOT FOUND');
    
    const mediaCells = document.querySelectorAll('.media-cell');
    console.log('[RESHUFFLE] Found', mediaCells.length, 'media cells');
    
    if (reshuffleMode) {
        console.log('[RESHUFFLE] ENABLING reshuffle mode');
        // Enable reshuffle mode
        if (reshuffleBtn) {
            reshuffleBtn.style.background = '#667eea';
            reshuffleBtn.textContent = '✓ Reshuffle Active';
            console.log('[RESHUFFLE] Button updated to active state');
        } else {
            console.error('[RESHUFFLE] reshuffleBtn not found!');
        }
        
        // Add visual indicator to draggable cells and ensure they're draggable
        let draggableCount = 0;
        mediaCells.forEach(cell => {
            // Check if cell has media content (img or div with content)
            const hasContent = cell.querySelector('img') || (cell.querySelector('div') && cell.querySelector('div').textContent.trim());
            
            if (hasContent) {
                // Ensure cell is draggable
                cell.draggable = true;
                cell.style.cursor = 'grab';
                cell.style.border = '2px dashed #667eea';
                cell.title = 'Drag to reorder media';
                draggableCount++;
                console.log('[RESHUFFLE] Made cell draggable:', cell.dataset.mediaIndex);
            }
        });
        console.log('[RESHUFFLE] Updated', draggableCount, 'draggable cells');
    } else {
        console.log('[RESHUFFLE] DISABLING reshuffle mode');
        // Disable reshuffle mode
        if (reshuffleBtn) {
            reshuffleBtn.style.background = '#555';
            reshuffleBtn.textContent = '🔄 Reshuffle';
            console.log('[RESHUFFLE] Button updated to inactive state');
        } else {
            console.error('[RESHUFFLE] reshuffleBtn not found!');
        }
        
        // Remove visual indicators (but keep draggable for cells with content)
        let removedCount = 0;
        mediaCells.forEach(cell => {
            const hasContent = cell.querySelector('img') || (cell.querySelector('div') && cell.querySelector('div').textContent.trim());
            
            if (cell.style.border === '2px dashed rgb(102, 126, 234)') {
                cell.style.border = '';
            }
            cell.style.cursor = '';
            cell.title = '';
            
            // Only keep draggable if it was originally set (has content and was draggable)
            // Otherwise, remove draggable attribute
            if (!hasContent) {
                cell.draggable = false;
            }
            removedCount++;
        });
        console.log('[RESHUFFLE] Removed visual indicators from', removedCount, 'cells');
    }
    console.log('[RESHUFFLE] ========== toggleReshuffleMode COMPLETE ==========');
}

/**
 * Generate media table HTML (2 columns) with drag-and-drop support
 */
function generateMediaTable(mediaList, placeholder) {
    if (mediaList.length === 0) {
        return `<table class="placeholder-table" 
                       style="border: 1px solid #000; border-collapse: collapse; width: 100%; margin: 10px 0;"
                       data-placeholder="${placeholder}">
            <tr>
                <td style="border: 1px solid #000; padding: 10px; min-height: 50px;"
                    ondrop="handleTableDrop(event, '${placeholder}')" 
                    ondragover="handleTableDragOver(event)"></td>
                <td style="border: 1px solid #000; padding: 10px; min-height: 50px;"
                    ondrop="handleTableDrop(event, '${placeholder}')" 
                    ondragover="handleTableDragOver(event)"></td>
            </tr>
        </table>`;
    }
    
    let tableHtml = `<table class="placeholder-table" 
                            style="border: 1px solid #000; border-collapse: collapse; width: 100%; margin: 10px 0;"
                            data-placeholder="${placeholder}">
        <tbody>`;
    
    // Generate rows (2 columns per row)
    for (let i = 0; i < mediaList.length; i += 2) {
        tableHtml += '<tr>';
        
        // Column 1
        const hasMedia1 = mediaList[i] !== undefined && mediaList[i] !== null;
        tableHtml += `<td class="media-cell" 
                          style="border: 1px solid #000; padding: 10px; width: 50%; position: relative;"
                          data-media-index="${i}"
                          data-placeholder="${placeholder}"
                          ondrop="handleTableDrop(event, '${placeholder}')" 
                          ondragover="handleTableDragOver(event)"
                          draggable="${hasMedia1 ? 'true' : 'false'}"
                          ondragstart="${hasMedia1 ? `handleTableCellDragStart(event, ${i}, '${placeholder}')` : ''}"
                          onclick="handleTableCellClick(event, ${i}, '${placeholder}')">`;
        if (mediaList[i]) {
            if (mediaList[i].type === 'image') {
                tableHtml += `<img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(mediaList[i].path)}&size=400x300" 
                                   style="max-width: 100%; height: auto;" 
                                   alt="${mediaList[i].name}">`;
            } else {
                tableHtml += `<div style="padding: 10px; text-align: center; color: #e0e0e0;">${mediaList[i].name}</div>`;
            }
            tableHtml += `<button class="remove-media-btn" 
                                   onclick="removeMediaFromTable(${i}, '${placeholder}'); event.stopPropagation();"
                                   style="position: absolute; top: 5px; right: 5px; background: #ff6b6b; color: white; border: none; border-radius: 50%; width: 24px; height: 24px; cursor: pointer; font-size: 14px; display: none;">×</button>`;
        }
        tableHtml += '</td>';
        
        // Column 2
        tableHtml += `<td class="media-cell" 
                          style="border: 1px solid #000; padding: 10px; width: 50%; position: relative;"
                          data-media-index="${i + 1}"
                          data-placeholder="${placeholder}"
                          ondrop="handleTableDrop(event, '${placeholder}')" 
                          ondragover="handleTableDragOver(event)"
                          draggable="${mediaList[i + 1] ? 'true' : 'false'}"
                          ondragstart="${mediaList[i + 1] ? `handleTableCellDragStart(event, ${i + 1}, '${placeholder}')` : ''}"
                          onclick="handleTableCellClick(event, ${i + 1}, '${placeholder}')">`;
        if (mediaList[i + 1]) {
            if (mediaList[i + 1].type === 'image') {
                tableHtml += `<img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(mediaList[i + 1].path)}&size=400x300" 
                                   style="max-width: 100%; height: auto;" 
                                   alt="${mediaList[i + 1].name}">`;
            } else {
                tableHtml += `<div style="padding: 10px; text-align: center; color: #e0e0e0;">${mediaList[i + 1].name}</div>`;
            }
            tableHtml += `<button class="remove-media-btn" 
                                   onclick="removeMediaFromTable(${i + 1}, '${placeholder}'); event.stopPropagation();"
                                   style="position: absolute; top: 5px; right: 5px; background: #ff6b6b; color: white; border: none; border-radius: 50%; width: 24px; height: 24px; cursor: pointer; font-size: 14px; display: none;">×</button>`;
        }
        tableHtml += '</td>';
        
        tableHtml += '</tr>';
    }
    
    // Add an empty row at the end for dropping new media (if there are items)
    if (mediaList.length > 0) {
        tableHtml += '<tr>';
        tableHtml += `<td class="media-cell" 
                          style="border: 1px solid #000; padding: 10px; min-height: 50px; width: 50%; position: relative;"
                          data-media-index="${mediaList.length}"
                          data-placeholder="${placeholder}"
                          ondrop="handleTableDrop(event, '${placeholder}')" 
                          ondragover="handleTableDragOver(event)">
                          <div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">Drop media here</div>
                      </td>`;
        tableHtml += `<td class="media-cell" 
                          style="border: 1px solid #000; padding: 10px; min-height: 50px; width: 50%; position: relative;"
                          data-media-index="${mediaList.length + 1}"
                          data-placeholder="${placeholder}"
                          ondrop="handleTableDrop(event, '${placeholder}')" 
                          ondragover="handleTableDragOver(event)">
                          <div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">Drop media here</div>
                      </td>`;
        tableHtml += '</tr>';
    }
    
    tableHtml += '</tbody></table>';
    return tableHtml;
}

/**
 * Attach drag handlers to table cells
 */
function attachTableDragHandlers() {
    const cells = document.querySelectorAll('.media-cell');
    cells.forEach(cell => {
        cell.addEventListener('mouseenter', function() {
            const removeBtn = this.querySelector('.remove-media-btn');
            if (removeBtn && this.querySelector('img, div')) {
                removeBtn.style.display = 'block';
            }
        });
        cell.addEventListener('mouseleave', function() {
            const removeBtn = this.querySelector('.remove-media-btn');
            if (removeBtn) {
                removeBtn.style.display = 'none';
            }
        });
    });
}

/**
 * Handle table cell drag start (for reordering)
 */
function handleTableCellDragStart(e, mediaIndex, placeholder) {
    const assignments = getCurrentAssignments();
    const media = assignments[placeholder] && assignments[placeholder][mediaIndex];
    if (media) {
        e.dataTransfer.setData('application/json', JSON.stringify({
            ...media,
            source: 'table',
            placeholder: placeholder,
            index: mediaIndex
        }));
        e.dataTransfer.effectAllowed = 'move';
    }
}

/**
 * Handle table cell click (for selection/editing)
 */
function handleTableCellClick(e, mediaIndex, placeholder) {
    // Could be used for editing or selecting media in table
    // For now, just prevent default behavior
}

/**
 * Handle table drop (for adding/reordering media)
 */
function handleTableDrop(e, placeholder) {
    e.preventDefault();
    e.stopPropagation();
    
    try {
        const data = JSON.parse(e.dataTransfer.getData('application/json'));
        if (!data) return;
        
        if (data.bulk && Array.isArray(data.media)) {
            // Bulk assignment - assign all selected media
            let assignedCount = 0;
            let skippedCount = 0;
            
            // Check if dropping on a specific cell
            const targetCell = e.target.closest('.media-cell') || e.target.closest('td');
            let targetIndex = null;
            
            if (targetCell && targetCell.dataset.mediaIndex !== undefined) {
                targetIndex = parseInt(targetCell.dataset.mediaIndex);
            }
            
            data.media.forEach(media => {
                if (assignMediaToPlaceholder(placeholder, media, targetIndex)) {
                    assignedCount++;
                    // Increment targetIndex for next item if inserting at specific position
                    if (targetIndex !== null) targetIndex++;
                } else {
                    skippedCount++;
                }
            });
            
            // Clear bulk selection after assignment
            if (window.bulkSelectedMedia) {
                const selectedCards = document.querySelectorAll('.media-selected');
                selectedCards.forEach(card => {
                    card.classList.remove('media-selected');
                    const checkbox = card.querySelector('.media-checkbox');
                    if (checkbox) checkbox.checked = false;
                });
                updateSelectedCount();
                window.bulkSelectedMedia = null;
            }
            
            // Close dialog if open
            if (window.currentPlaceholderDialog) {
                closePlaceholderDialog();
            }
            
            // Update preview
            updatePreview();
            
            if (skippedCount > 0 && assignedCount > 0) {
                alert(`${assignedCount} media item(s) assigned. ${skippedCount} item(s) were already assigned.`);
            } else if (skippedCount > 0) {
                alert('All selected media items are already assigned to this placeholder.');
            } else if (data.media.length > 1) {
                alert(`${assignedCount} media items assigned successfully!`);
            }
            
            return;
        }
        
        if (data.source === 'table') {
            // Reordering within same placeholder
            reorderMediaInPlaceholder(placeholder, data.index, e.target);
        } else {
            // Adding new media from grid
            // Check if dropping on a specific cell (with data-media-index)
            const targetCell = e.target.closest('.media-cell') || e.target.closest('td');
            let targetIndex = null;
            
            if (targetCell && targetCell.dataset.mediaIndex !== undefined) {
                targetIndex = parseInt(targetCell.dataset.mediaIndex);
            }
            
            assignMediaToPlaceholder(placeholder, data, targetIndex);
        }
    } catch (err) {
        console.error('Error handling table drop:', err);
    }
}

/**
 * Handle table drag over
 */
function handleTableDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.dataTransfer.dropEffect = 'copy';
    
    // Visual feedback for drop zone
    const target = e.currentTarget;
    if (target && target.style) {
        target.style.backgroundColor = 'rgba(102, 126, 234, 0.2)';
        
        // Reset background after a short delay
        setTimeout(() => {
            if (target && target.style) {
                target.style.backgroundColor = '';
            }
        }, 200);
    }
}

/**
 * Reorder media within placeholder table
 */
function reorderMediaInPlaceholder(placeholder, fromIndex, targetCell) {
    const assignments = getCurrentAssignments();
    const placeholderKey = placeholder.toLowerCase();
    if (!assignments[placeholderKey] || !assignments[placeholderKey][fromIndex]) {
        return;
    }
    
    // Get target index from cell
    const targetIndex = parseInt(targetCell.dataset.mediaIndex) || 0;
    
    // Reorder array
    const media = assignments[placeholderKey].splice(fromIndex, 1)[0];
    assignments[placeholderKey].splice(targetIndex, 0, media);
    
    // Update UI
    updatePreview();
    updatePlaceholderStats();
}

/**
 * Remove media from table
 */
function removeMediaFromTable(mediaIndex, placeholder) {
    const assignments = getCurrentAssignments();
    const placeholderKey = placeholder.toLowerCase();
    
    if (assignments[placeholderKey] && assignments[placeholderKey][mediaIndex]) {
        const media = assignments[placeholderKey][mediaIndex];
        removeMediaFromPlaceholder(placeholder, media.path);
    }
}

// Global state
let fontSizeMode = 'regular'; // 'regular' or 'big'

/**
 * Toggle font size between regular and big
 */
function toggleFontSize() {
    fontSizeMode = fontSizeMode === 'regular' ? 'big' : 'regular';
    const fontSize = fontSizeMode === 'big' ? '18px' : '14px';
    document.documentElement.style.setProperty('--obs-font-size', fontSize);
    document.body.classList.toggle('font-size-big', fontSizeMode === 'big');
    
    // Update button states
    const fontSizeRegular = document.getElementById('fontSizeRegular');
    const fontSizeBig = document.getElementById('fontSizeBig');
    if (fontSizeRegular) {
        fontSizeRegular.style.opacity = fontSizeMode === 'regular' ? '1' : '0.5';
    }
    if (fontSizeBig) {
        fontSizeBig.style.opacity = fontSizeMode === 'big' ? '1' : '0.5';
    }
}

/**
 * Load observation subfolders (API-free - already in template)
 */
function loadObservationSubfolders() {
    // API-free: Subfolders already populated in template via server-side rendering
    // No action needed - dropdown is already populated
}

/**
 * Load observation media for selected subfolder
 */
function loadObservationMedia() {
    // API-free: Use data already embedded in the page
    const subfolder = document.getElementById('observationSubfolderSelect').value;
    if (!subfolder) {
        document.getElementById('observationMediaGrid').innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Please select a subfolder</p>';
        document.getElementById('observationMediaCount').textContent = '0 files';
        return;
    }
    
    // Get media from embedded data (API-free)
    const mediaFiles = window.observationMediaData[subfolder] || [];
    displayObservationMedia(mediaFiles);
    document.getElementById('observationMediaCount').textContent = `${mediaFiles.length} files`;
}

/**
 * Load selected subfolder by reloading the page (API-free - re-scans server-side)
 */
function loadSelectedSubfolder() {
    const subfolderSelect = document.getElementById('observationSubfolderSelect');
    
    if (!subfolderSelect) {
        alert('Error: Subfolder selector not found. Please refresh the page.');
        return;
    }
    
    const subfolder = subfolderSelect.value;
    
    if (!subfolder) {
        alert('Please select a subfolder first');
        return;
    }
    
    // Reload the page with subfolder query parameter to auto-select it
    // This will trigger a server-side re-scan of all subfolders
    window.location.href = `/v2p-formatter/observation-media?subfolder=${encodeURIComponent(subfolder)}`;
}

/**
 * Display observation media in grid
 */
function displayObservationMedia(mediaFiles) {
    // Show bulk select label if there are media files
    const bulkSelectLabel = document.getElementById('bulkSelectLabel');
    if (bulkSelectLabel) {
        bulkSelectLabel.style.display = mediaFiles.length > 0 ? 'block' : 'none';
    }
    const grid = document.getElementById('observationMediaGrid');
    grid.innerHTML = '';
    
    if (mediaFiles.length === 0) {
        grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No media files found</p>';
        return;
    }
    
    // Group media by subfolder if available
    const groupedMedia = {};
    mediaFiles.forEach(media => {
        const subfolder = media.subfolder || '';
        if (!groupedMedia[subfolder]) {
            groupedMedia[subfolder] = [];
        }
        groupedMedia[subfolder].push(media);
    });
    
    // Display grouped by subfolder
    const subfolderKeys = Object.keys(groupedMedia).sort();
    
    subfolderKeys.forEach(subfolder => {
        // Add subfolder header if not empty
        if (subfolder) {
            const header = document.createElement('div');
            header.style.cssText = 'grid-column: 1 / -1; color: #667eea; font-weight: bold; margin-top: 20px; margin-bottom: 10px; padding: 8px; background: #1e1e1e; border-radius: 4px; border-left: 3px solid #667eea;';
            header.textContent = `📁 ${subfolder}`;
            grid.appendChild(header);
        }
        
        // Add media cards for this subfolder
        groupedMedia[subfolder].forEach((media, index) => {
            const card = document.createElement('div');
            card.className = 'observation-media-card';
            card.dataset.mediaIndex = index;
            card.dataset.mediaPath = media.path;
            card.dataset.mediaName = media.name;
            card.dataset.mediaType = media.type;
            
            // Check if media is already assigned (disabled state)
            const isAssigned = isMediaAssigned(media.path);
            if (isAssigned) {
                card.classList.add('media-assigned');
                card.style.opacity = '0.5';
                card.style.cursor = 'not-allowed';
            } else {
                card.draggable = true;
                card.style.cursor = 'grab';
            }
            
            card.innerHTML = `
                <div class="observation-media-thumbnail">
                    <img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(media.path)}&size=120x90" 
                         alt="${media.name}" 
                         onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'120\' height=\'90\'%3E%3Crect fill=\'%23333\' width=\'120\' height=\'90\'/%3E%3Ctext x=\'50%25\' y=\'50%25\' text-anchor=\'middle\' dy=\'.3em\' fill=\'%23999\' font-size=\'12\'%3E${media.type === 'video' ? 'VIDEO' : 'IMAGE'}%3C/text%3E%3C/svg%3E'">
                    ${media.type === 'video' ? '<span class="video-badge">⏯</span>' : ''}
                    ${isAssigned ? '<span class="assigned-badge">✓ Assigned</span>' : ''}
                </div>
                <div class="observation-media-info">
                    <div class="observation-media-name" title="${media.name}">${media.name}</div>
                    <div class="observation-media-size">${formatFileSize(media.size)}</div>
                </div>
            `;
            
            // Add drag and click handlers for unassigned media
            if (!isAssigned) {
                card.addEventListener('dragstart', handleMediaDragStart);
                card.addEventListener('click', () => handleMediaClick(media));
            }
            
            grid.appendChild(card);
        });
    });
}

/**
 * Handle media drag start
 */
function handleMediaDragStart(e) {
    const card = e.currentTarget;
    
    // Check if this card is part of bulk selection
    if (card.classList.contains('media-selected') && window.bulkSelectedMedia) {
        // Drag all selected media
        e.dataTransfer.setData('application/json', JSON.stringify({
            bulk: true,
            media: window.bulkSelectedMedia
        }));
    } else {
        // Drag single media
        const mediaData = {
            path: card.dataset.mediaPath,
            name: card.dataset.mediaName,
            type: card.dataset.mediaType
        };
        e.dataTransfer.setData('application/json', JSON.stringify(mediaData));
    }
    
    e.dataTransfer.effectAllowed = 'copy';
    card.style.opacity = '0.5';
}

/**
 * Handle media click
 */
function handleMediaClick(media, event) {
    // Check if bulk select mode is active
    const bulkSelectMode = document.getElementById('bulkSelectMode');
    if (bulkSelectMode && bulkSelectMode.checked) {
        // Toggle selection
        const card = event ? event.currentTarget : document.querySelector(`[data-media-path="${media.path}"]`);
        if (card) {
            if (card.classList.contains('media-selected')) {
                card.classList.remove('media-selected');
                const checkbox = card.querySelector('.media-checkbox');
                if (checkbox) checkbox.checked = false;
            } else {
                card.classList.add('media-selected');
                const checkbox = card.querySelector('.media-checkbox');
                if (checkbox) checkbox.checked = true;
            }
            updateSelectedCount();
        }
        return;
    }
    
    // Normal click - show placeholder selection dialog
    const textEditor = document.getElementById('observationTextEditor');
    const placeholders = extractPlaceholders(textEditor.value);
    if (placeholders.length === 0) {
        alert('No placeholders found in text. Add placeholders like {{Placeholder_Name}} first.');
        return;
    }
    
    // Create selection dialog
    showPlaceholderSelectionDialog(media, placeholders);
}

/**
 * Toggle bulk select mode
 */
function toggleBulkSelectMode() {
    const bulkSelectMode = document.getElementById('bulkSelectMode');
    const bulkAssignBtn = document.getElementById('bulkAssignBtn');
    const selectedCards = document.querySelectorAll('.media-selected');
    
    if (bulkSelectMode.checked) {
        // Enable bulk select mode
        bulkAssignBtn.style.display = 'inline-block';
        // Add checkboxes to all unassigned media cards
        const cards = document.querySelectorAll('.observation-media-card:not(.media-assigned)');
        cards.forEach(card => {
            if (!card.querySelector('.media-checkbox')) {
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.className = 'media-checkbox';
                checkbox.style.cssText = 'position: absolute; top: 5px; left: 5px; width: 20px; height: 20px; z-index: 10; cursor: pointer;';
                checkbox.addEventListener('click', function(e) {
                    e.stopPropagation();
                    if (this.checked) {
                        card.classList.add('media-selected');
                    } else {
                        card.classList.remove('media-selected');
                    }
                    updateSelectedCount();
                });
                card.style.position = 'relative';
                card.appendChild(checkbox);
            }
        });
    } else {
        // Disable bulk select mode
        bulkAssignBtn.style.display = 'none';
        // Remove all selections
        selectedCards.forEach(card => {
            card.classList.remove('media-selected');
            const checkbox = card.querySelector('.media-checkbox');
            if (checkbox) checkbox.checked = false;
        });
        updateSelectedCount();
    }
}

/**
 * Update selected media count
 */
function updateSelectedCount() {
    const selectedCount = document.querySelectorAll('.media-selected').length;
    const countSpan = document.getElementById('selectedCount');
    if (countSpan) {
        countSpan.textContent = selectedCount;
    }
    const bulkAssignBtn = document.getElementById('bulkAssignBtn');
    if (bulkAssignBtn) {
        bulkAssignBtn.style.display = selectedCount > 0 ? 'inline-block' : 'none';
    }
}

/**
 * Assign selected media to placeholder
 */
function assignSelectedMedia() {
    const selectedCards = document.querySelectorAll('.media-selected');
    if (selectedCards.length === 0) {
        alert('Please select at least one media item.');
        return;
    }
    
    // Collect selected media
    const selectedMedia = [];
    selectedCards.forEach(card => {
        selectedMedia.push({
            path: card.dataset.mediaPath,
            name: card.dataset.mediaName,
            type: card.dataset.mediaType
        });
    });
    
    // Store selected media globally for drag-and-drop
    window.bulkSelectedMedia = selectedMedia;
    
    // Ensure selected cards are draggable (they should already be, but ensure it)
    selectedCards.forEach(card => {
        card.draggable = true;
        card.style.cursor = 'grab';
    });
    
    // Show placeholder selection dialog with all selected media
    const textEditor = document.getElementById('observationTextEditor');
    const placeholders = extractPlaceholders(textEditor.value);
    if (placeholders.length === 0) {
        alert('No placeholders found in text. Add placeholders like {{Placeholder_Name}} first.');
        return;
    }
    
    showPlaceholderSelectionDialog(selectedMedia, placeholders);
    
    // Don't clear selections - keep them for drag-and-drop
    // User can clear manually or they'll be cleared when assigned
}

/**
 * Format file size
 */
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Make functions globally available
window.loadObservationSubfolders = loadObservationSubfolders;
window.loadObservationMedia = loadObservationMedia;
window.loadSelectedSubfolder = loadSelectedSubfolder;
window.displayObservationMedia = displayObservationMedia;
window.toggleFontSize = toggleFontSize;
window.handleMediaDragStart = handleMediaDragStart;
window.handleMediaClick = handleMediaClick;
window.formatFileSize = formatFileSize;
window.toggleBulkSelectMode = toggleBulkSelectMode;
window.assignSelectedMedia = assignSelectedMedia;
window.updateSelectedCount = updateSelectedCount;
window.handleBulkMediaDragStart = handleBulkMediaDragStart;
window.handleBulkMediaDragEnd = handleBulkMediaDragEnd;
window.attachBulkThumbnailHandlers = attachBulkThumbnailHandlers;

/**
 * Attach drag handlers to bulk thumbnails
 */
function attachBulkThumbnailHandlers(dialog, mediaList) {
    console.log('[ATTACH] Starting to attach handlers for', mediaList.length, 'thumbnails');
    
    // Attach remove button handlers
    const removeButtons = dialog.querySelectorAll('.bulk-thumb-remove-btn');
    removeButtons.forEach(btn => {
        const index = parseInt(btn.dataset.index);
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            e.preventDefault();
            removeMediaFromBulkSelection(index);
        });
    });
    
    // Attach drag handlers to thumbnails
    const thumbnails = dialog.querySelectorAll('.bulk-media-thumbnail');
    console.log('[ATTACH] Found', thumbnails.length, 'thumbnails');
    
    thumbnails.forEach((thumbnail, idx) => {
        const index = parseInt(thumbnail.dataset.mediaIndex);
        console.log('[ATTACH] Attaching handlers to thumbnail', index);
        
        // Ensure draggable
        thumbnail.draggable = true;
        
        // Remove any existing listeners
        const newThumb = thumbnail.cloneNode(true);
        thumbnail.parentNode.replaceChild(newThumb, thumbnail);
        
        // Attach drag start
        newThumb.addEventListener('dragstart', function(e) {
            console.log('[DRAG] dragstart event fired on thumbnail', index);
            e.stopPropagation();
            
            if (!window.bulkSelectedMedia || window.bulkSelectedMedia.length === 0) {
                console.error('[DRAG] No bulkSelectedMedia');
                e.preventDefault();
                return;
            }
            
            const dragData = {
                bulk: true,
                media: window.bulkSelectedMedia,
                singleIndex: index
            };
            
            try {
                const dataStr = JSON.stringify(dragData);
                e.dataTransfer.setData('application/json', dataStr);
                e.dataTransfer.setData('text/plain', dataStr);
                e.dataTransfer.effectAllowed = 'copy';
                newThumb.style.opacity = '0.5';
                console.log('[DRAG] Data set successfully:', dataStr.substring(0, 100));
            } catch (err) {
                console.error('[DRAG] Error setting data:', err);
                e.preventDefault();
            }
        });
        
        // Attach drag end
        newThumb.addEventListener('dragend', function(e) {
            console.log('[DRAG] dragend event fired');
            newThumb.style.opacity = '1';
        });
        
        // Prevent image from dragging
        const img = newThumb.querySelector('img');
        if (img) {
            img.draggable = false;
            img.addEventListener('dragstart', function(e) {
                e.preventDefault();
                e.stopPropagation();
            });
        }
        
        console.log('[ATTACH] Handlers attached to thumbnail', index);
    });
    
    console.log('[ATTACH] All handlers attached');
}

/**
 * Handle bulk media drag start from dialog thumbnails
 */
function handleBulkMediaDragStart(e, index) {
    console.log('[DRAG] ========== DRAG START ==========');
    console.log('[DRAG] handleBulkMediaDragStart called');
    console.log('[DRAG] index:', index);
    console.log('[DRAG] event:', e);
    console.log('[DRAG] currentTarget:', e.currentTarget);
    console.log('[DRAG] target:', e.target);
    console.log('[DRAG] window.bulkSelectedMedia:', window.bulkSelectedMedia);
    console.log('[DRAG] window.bulkSelectedMedia length:', window.bulkSelectedMedia ? window.bulkSelectedMedia.length : 'null');
    
    if (!window.bulkSelectedMedia || window.bulkSelectedMedia.length === 0) {
        console.error('[DRAG] ERROR: No bulk selected media available');
        console.error('[DRAG] window.bulkSelectedMedia:', window.bulkSelectedMedia);
        e.preventDefault();
        return false;
    }
    
    // Ensure index is valid
    if (index < 0 || index >= window.bulkSelectedMedia.length) {
        console.error('[DRAG] ERROR: Invalid media index:', index, 'Length:', window.bulkSelectedMedia.length);
        e.preventDefault();
        return false;
    }
    
    const media = window.bulkSelectedMedia[index];
    if (!media) {
        console.error('[DRAG] ERROR: Media not found at index:', index);
        e.preventDefault();
        return false;
    }
    
    console.log('[DRAG] Media found:', media);
    
    try {
        const dragData = {
            bulk: true,
            media: window.bulkSelectedMedia,
            singleIndex: index
        };
        
        const dataStr = JSON.stringify(dragData);
        console.log('[DRAG] Drag data string:', dataStr);
        console.log('[DRAG] dataTransfer types before:', e.dataTransfer.types);
        
        // Set data in multiple formats for compatibility
        e.dataTransfer.setData('application/json', dataStr);
        e.dataTransfer.setData('text/plain', dataStr);
        e.dataTransfer.effectAllowed = 'copy';
        
        console.log('[DRAG] dataTransfer types after:', e.dataTransfer.types);
        console.log('[DRAG] effectAllowed:', e.dataTransfer.effectAllowed);
        
        // Visual feedback
        if (e.currentTarget) {
            e.currentTarget.style.opacity = '0.5';
            console.log('[DRAG] Opacity set to 0.5');
        } else {
            console.warn('[DRAG] currentTarget is null!');
        }
        
        console.log('[DRAG] ✅ Drag started successfully');
        return true;
    } catch (err) {
        console.error('[DRAG] ❌ ERROR setting drag data:', err);
        console.error('[DRAG] Error stack:', err.stack);
        e.preventDefault();
        return false;
    }
}

/**
 * Handle bulk media drag end
 */
function handleBulkMediaDragEnd(e) {
    console.log('[DRAG] ========== DRAG END ==========');
    console.log('[DRAG] handleBulkMediaDragEnd called');
    console.log('[DRAG] currentTarget:', e.currentTarget);
    if (e.currentTarget && e.currentTarget.style) {
        e.currentTarget.style.opacity = '1';
        console.log('[DRAG] Opacity reset to 1');
    } else {
        console.warn('[DRAG] currentTarget is null or has no style');
    }
}

/**
 * Toggle dialog section expand/collapse
 */
function toggleDialogSection(sectionId) {
    const sectionContent = document.querySelector(`.dialog-section-content[data-section-id="${sectionId}"]`);
    const sectionHeader = document.querySelector(`.dialog-section-header[onclick*="${sectionId}"]`);
    const icon = sectionHeader ? sectionHeader.querySelector('.dialog-section-icon') : null;
    
    if (sectionContent) {
        if (sectionContent.style.display === 'none') {
            sectionContent.style.display = 'block';
            if (icon) icon.textContent = '▼';
        } else {
            sectionContent.style.display = 'none';
            if (icon) icon.textContent = '▶';
        }
    }
}

/**
 * Expand all dialog sections
 */
function expandAllDialogSections() {
    const dialog = window.currentPlaceholderDialog;
    if (!dialog) return;
    
    const sections = dialog.querySelectorAll('.dialog-section-content');
    sections.forEach(section => {
        section.style.display = 'block';
        const sectionId = section.dataset.sectionId;
        if (sectionId) {
            const header = dialog.querySelector(`.dialog-section-header[onclick*="${sectionId}"]`);
            const icon = header ? header.querySelector('.dialog-section-icon') : null;
            if (icon) icon.textContent = '▼';
        }
    });
}

/**
 * Collapse all dialog sections
 */
function collapseAllDialogSections() {
    const dialog = window.currentPlaceholderDialog;
    if (!dialog) return;
    
    const sections = dialog.querySelectorAll('.dialog-section-content');
    sections.forEach(section => {
        section.style.display = 'none';
        const sectionId = section.dataset.sectionId;
        if (sectionId) {
            const header = dialog.querySelector(`.dialog-section-header[onclick*="${sectionId}"]`);
            const icon = header ? header.querySelector('.dialog-section-icon') : null;
            if (icon) icon.textContent = '▶';
        }
    });
}

/**
 * Remove media from bulk selection in dialog
 */
function removeMediaFromBulkSelection(index) {
    if (!window.bulkSelectedMedia || !window.bulkSelectedMedia[index]) return;
    
    // Remove from array
    window.bulkSelectedMedia.splice(index, 1);
    
    // Update dialog if open
    const dialog = window.currentPlaceholderDialog;
    if (dialog) {
        // Remove thumbnail element
        const thumbnail = dialog.querySelector(`#bulk-thumb-${index}`);
        if (thumbnail) {
            thumbnail.remove();
        }
        
        // Update count
        const countText = dialog.querySelector('#bulkMediaThumbnails').previousElementSibling;
        if (countText) {
            countText.textContent = `Selected Media (${window.bulkSelectedMedia.length}):`;
        }
        
        // If no media left, close dialog
        if (window.bulkSelectedMedia.length === 0) {
            closePlaceholderDialog();
            // Also clear selections in main grid
            const selectedCards = document.querySelectorAll('.media-selected');
            selectedCards.forEach(card => {
                card.classList.remove('media-selected');
                const checkbox = card.querySelector('.media-checkbox');
                if (checkbox) checkbox.checked = false;
            });
            updateSelectedCount();
        } else {
            // Re-index remaining thumbnails
            const thumbnails = dialog.querySelectorAll('[id^="bulk-thumb-"]');
            thumbnails.forEach((thumb, newIndex) => {
                thumb.id = `bulk-thumb-${newIndex}`;
                thumb.dataset.mediaIndex = newIndex;
                const removeBtn = thumb.querySelector('button');
                if (removeBtn) {
                    removeBtn.setAttribute('onclick', `removeMediaFromBulkSelection(${newIndex}); event.stopPropagation();`);
                }
                const img = thumb.querySelector('img');
                if (img && img.ondragstart) {
                    thumb.setAttribute('ondragstart', `handleBulkMediaDragStart(event, ${newIndex})`);
                }
            });
        }
    }
}

/**
 * Remove media from bulk selection in dialog
 */
function removeMediaFromBulkSelection(index) {
    if (!window.bulkSelectedMedia || !window.bulkSelectedMedia[index]) return;
    
    // Remove from array
    window.bulkSelectedMedia.splice(index, 1);
    
    // Update dialog if open
    const dialog = window.currentPlaceholderDialog;
    if (dialog) {
        // Remove thumbnail element
        const thumbnail = dialog.querySelector(`#bulk-thumb-${index}`);
        if (thumbnail) {
            thumbnail.remove();
        }
        
        // Update count
        const countText = dialog.querySelector('#bulkMediaThumbnails').previousElementSibling;
        if (countText) {
            countText.textContent = `Selected Media (${window.bulkSelectedMedia.length}):`;
        }
        
        // If no media left, close dialog
        if (window.bulkSelectedMedia.length === 0) {
            closePlaceholderDialog();
            // Also clear selections in main grid
            const selectedCards = document.querySelectorAll('.media-selected');
            selectedCards.forEach(card => {
                card.classList.remove('media-selected');
                const checkbox = card.querySelector('.media-checkbox');
                if (checkbox) checkbox.checked = false;
            });
            updateSelectedCount();
        } else {
            // Re-index remaining thumbnails
            const thumbnails = dialog.querySelectorAll('[id^="bulk-thumb-"]');
            thumbnails.forEach((thumb, newIndex) => {
                thumb.id = `bulk-thumb-${newIndex}`;
                thumb.dataset.mediaIndex = newIndex;
                const removeBtn = thumb.querySelector('button');
                if (removeBtn) {
                    removeBtn.setAttribute('onclick', `removeMediaFromBulkSelection(${newIndex}); event.stopPropagation();`);
                }
                const img = thumb.querySelector('img');
                if (img && img.ondragstart) {
                    thumb.setAttribute('ondragstart', `handleBulkMediaDragStart(event, ${newIndex})`);
                }
            });
        }
    }
}

/**
 * Handle drag over in dialog preview
 */
function handleDialogPreviewDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.dataTransfer.dropEffect = 'copy';
    return false;
}

/**
 * Handle drop in dialog preview
 */
function handleDialogPreviewDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    
    // Find the closest placeholder drop zone
    const target = e.target;
    let placeholder = null;
    
    // Check if dropped on a table, cell, or placeholder container
    const table = target.closest('table.placeholder-table');
    const cell = target.closest('td');
    const container = target.closest('[data-placeholder]');
    
    if (table && table.dataset.placeholder) {
        placeholder = table.dataset.placeholder;
    } else if (cell && cell.dataset.placeholder) {
        placeholder = cell.dataset.placeholder;
    } else if (container && container.dataset.placeholder) {
        placeholder = container.dataset.placeholder;
    } else if (cell) {
        // Check parent table or container
        const parentTable = cell.closest('table');
        if (parentTable && parentTable.dataset.placeholder) {
            placeholder = parentTable.dataset.placeholder;
        } else {
            const parentContainer = cell.closest('[data-placeholder]');
            if (parentContainer) {
                placeholder = parentContainer.dataset.placeholder;
            }
        }
    }
    
    if (!placeholder) {
        console.log('No placeholder found for drop');
        return false;
    }
    
    // Get drag data - try both text/plain and application/json
    let dataStr = null;
    try {
        dataStr = e.dataTransfer.getData('application/json');
        if (!dataStr) {
            // Try text/plain as fallback
            dataStr = e.dataTransfer.getData('text/plain');
        }
        if (!dataStr) {
            // Try getting all types
            const types = e.dataTransfer.types;
            console.log('Available dataTransfer types:', types);
            for (let i = 0; i < types.length; i++) {
                const type = types[i];
                const data = e.dataTransfer.getData(type);
                if (data) {
                    console.log(`Found data in type ${type}:`, data);
                    dataStr = data;
                    break;
                }
            }
        }
    } catch (err) {
        console.error('Error getting drag data:', err);
    }
    
    if (!dataStr) {
        console.log('No drag data found. Available types:', e.dataTransfer.types);
        return false;
    }
    
    try {
        const data = JSON.parse(dataStr);
        if (!data) {
            console.log('Invalid drag data');
            return false;
        }
        
        console.log('Parsed drag data:', data);
        
        if (data.bulk && Array.isArray(data.media)) {
            // Bulk assignment
            let assignedCount = 0;
            let skippedCount = 0;
            
            // Check if dropping on a specific cell
            const targetCell = target.closest('.media-cell') || target.closest('td');
            let targetIndex = null;
            
            if (targetCell && targetCell.dataset.mediaIndex !== undefined) {
                targetIndex = parseInt(targetCell.dataset.mediaIndex);
            }
            
            data.media.forEach(media => {
                if (assignMediaToPlaceholder(placeholder, media, targetIndex)) {
                    assignedCount++;
                    if (targetIndex !== null) targetIndex++;
                } else {
                    skippedCount++;
                }
            });
            
            // Update main preview
            updatePreview();
            
            // Update dialog preview to show assigned media
            updateDialogPreview();
            
            // Expand the section containing the assigned placeholder
            expandDialogSectionForPlaceholder(placeholder);
            
            // Clear bulk selection after assignment
            if (window.bulkSelectedMedia) {
                const selectedCards = document.querySelectorAll('.media-selected');
                selectedCards.forEach(card => {
                    card.classList.remove('media-selected');
                    const checkbox = card.querySelector('.media-checkbox');
                    if (checkbox) checkbox.checked = false;
                });
                updateSelectedCount();
                window.bulkSelectedMedia = null;
            }
            
            // Show success message but keep dialog open
            if (skippedCount > 0 && assignedCount > 0) {
                console.log(`${assignedCount} media item(s) assigned. ${skippedCount} item(s) were already assigned.`);
            } else if (skippedCount > 0) {
                console.log('All selected media items are already assigned to this placeholder.');
            } else if (data.media.length > 1) {
                console.log(`${assignedCount} media items assigned successfully!`);
            }
            
            // Don't close dialog - keep it open
        } else {
            // Single media assignment
            const targetCell = target.closest('.media-cell') || target.closest('td');
            let targetIndex = null;
            
            if (targetCell && targetCell.dataset.mediaIndex !== undefined) {
                targetIndex = parseInt(targetCell.dataset.mediaIndex);
            }
            
            if (assignMediaToPlaceholder(placeholder, data, targetIndex)) {
                // Update main preview
                updatePreview();
                
                // Update dialog preview to show assigned media
                updateDialogPreview();
                
                // Expand the section containing the assigned placeholder
                expandDialogSectionForPlaceholder(placeholder);
                
                // Don't close dialog - keep it open
            } else {
                console.log('This media is already assigned to this placeholder.');
            }
        }
        
        return false;
    } catch (err) {
        console.error('Error handling dialog preview drop:', err);
        return false;
    }
}

/**
 * Update dialog preview with current assignments
 */
function updateDialogPreview() {
    const dialog = window.currentPlaceholderDialog;
    if (!dialog) return;
    
    const preview = dialog.querySelector('#dialogPreview');
    if (!preview) return;
    
    // Get current state
    const textEditor = document.getElementById('observationTextEditor');
    const text = textEditor ? textEditor.value : '';
    const placeholders = extractPlaceholders(text);
    const colorMap = assignPlaceholderColors(placeholders);
    const assignments = getCurrentAssignments();
    const validation = validatePlaceholders(text, assignments);
    const sectionData = parseSections(text);
    
    // Get media list from dialog
    const mediaList = window.bulkSelectedMedia || [];
    
    // Regenerate preview HTML
    let previewHtml = '';
    
    if (sectionData.hasSections) {
        previewHtml = renderSectionsForDialog(sectionData, placeholders, colorMap, assignments, validation, mediaList);
    } else {
        // Render without sections
        let previewHtmlTemp = '';
        let lastIndex = 0;
        
        const placeholderPositions = [];
        placeholders.forEach(placeholder => {
            const pattern = new RegExp(`\\{\\{${placeholder}\\}\\}`, 'gi');
            let match;
            while ((match = pattern.exec(text)) !== null) {
                placeholderPositions.push({
                    start: match.index,
                    end: match.index + match[0].length,
                    placeholder: placeholder
                });
            }
        });
        
        placeholderPositions.sort((a, b) => a.start - b.start);
        
        placeholderPositions.forEach(pos => {
            if (pos.start > lastIndex) {
                const textSegment = text.substring(lastIndex, pos.start);
                previewHtmlTemp += escapeHtml(textSegment).replace(/\n/g, '<br>');
            }
            
            const placeholder = pos.placeholder;
            const assignedMedia = assignments[placeholder] || [];
            
            if (assignedMedia.length > 0) {
                const tableHtml = generateMediaTable(assignedMedia, placeholder);
                previewHtmlTemp += tableHtml;
            } else {
                const emptyTable = `<div class="unassigned-placeholder-container" data-placeholder="${escapeHtml(placeholder)}" style="margin: 10px 0;">
                    <table class="placeholder-table unassigned" 
                           style="border: 2px dashed #667eea; border-collapse: collapse; width: 100%; background: rgba(102, 126, 234, 0.1); cursor: pointer;"
                           data-placeholder="${escapeHtml(placeholder)}"
                           ondrop="handleDialogPreviewDrop(event)" 
                           ondragover="handleDialogPreviewDragOver(event)"
                           onclick="selectPlaceholderForMedia('${placeholder}', ${JSON.stringify(mediaList).replace(/'/g, "\\'")})">
                        <tr>
                            <td style="border: 1px solid #667eea; padding: 15px; min-height: 50px; text-align: center; color: #667eea; font-size: 11px;"
                                data-placeholder="${escapeHtml(placeholder)}"
                                ondrop="handleDialogPreviewDrop(event)" 
                                ondragover="handleDialogPreviewDragOver(event)">
                                Drop media here or click
                            </td>
                            <td style="border: 1px solid #667eea; padding: 15px; min-height: 50px; text-align: center; color: #667eea; font-size: 11px;"
                                data-placeholder="${escapeHtml(placeholder)}"
                                ondrop="handleDialogPreviewDrop(event)" 
                                ondragover="handleDialogPreviewDragOver(event)">
                                Drop media here or click
                            </td>
                        </tr>
                    </table>
                    <div style="text-align: center; color: ${colorMap[placeholder]}; font-size: 10px; margin-top: 3px; font-weight: bold;">
                        {{${escapeHtml(placeholder)}}}
                    </div>
                </div>`;
                previewHtmlTemp += emptyTable;
            }
            
            lastIndex = pos.end;
        });
        
        if (lastIndex < text.length) {
            const textSegment = text.substring(lastIndex);
            previewHtmlTemp += escapeHtml(textSegment).replace(/\n/g, '<br>');
        }
        
        if (placeholderPositions.length === 0) {
            previewHtmlTemp = escapeHtml(text).replace(/\n/g, '<br>');
        }
        
        placeholders.forEach(placeholder => {
            const color = colorMap[placeholder];
            const placeholderPattern = new RegExp(`(\\{\\{${placeholder}\\}\\})`, 'gi');
            previewHtmlTemp = previewHtmlTemp.replace(placeholderPattern, `<span style="color: ${color}; font-weight: bold;">$1</span>`);
        });
        
        previewHtml = previewHtmlTemp;
    }
    
    preview.innerHTML = previewHtml;
    
    // Update reshuffle button visibility
    const hasAssignedMedia = Object.keys(assignments).some(key => assignments[key] && assignments[key].length > 0);
    const dialogReshuffleBtn = dialog.querySelector('#dialogReshuffleBtn');
    if (dialogReshuffleBtn) {
        dialogReshuffleBtn.style.display = hasAssignedMedia ? 'block' : 'none';
    }
}

/**
 * Expand dialog section containing a specific placeholder
 */
function expandDialogSectionForPlaceholder(placeholder) {
    const dialog = window.currentPlaceholderDialog;
    if (!dialog) return;
    
    // Find which section contains this placeholder
    const textEditor = document.getElementById('observationTextEditor');
    const text = textEditor ? textEditor.value : '';
    const sectionData = parseSections(text);
    
    if (!sectionData.hasSections) return;
    
    // Find the section containing this placeholder
    let targetSectionId = null;
    sectionData.sections.forEach(section => {
        const placeholderPattern = new RegExp(`\\{\\{${placeholder}\\}\\}`, 'i');
        if (placeholderPattern.test(section.content)) {
            targetSectionId = section.id;
        }
    });
    
    if (targetSectionId) {
        // Expand the section
        const sectionContent = dialog.querySelector(`.dialog-section-content[data-section-id="${targetSectionId}"]`);
        const sectionHeader = dialog.querySelector(`.dialog-section-header[onclick*="${targetSectionId}"]`);
        const icon = sectionHeader ? sectionHeader.querySelector('.dialog-section-icon') : null;
        
        if (sectionContent) {
            sectionContent.style.display = 'block';
            if (icon) icon.textContent = '▼';
        }
    }
}

/**
 * Toggle reshuffle mode in dialog
 */
let dialogReshuffleMode = false;
function toggleDialogReshuffleMode() {
    console.log('[RESHUFFLE] ========== toggleDialogReshuffleMode CALLED ==========');
    console.log('[RESHUFFLE] Current dialogReshuffleMode:', dialogReshuffleMode);
    dialogReshuffleMode = !dialogReshuffleMode;
    console.log('[RESHUFFLE] New dialogReshuffleMode:', dialogReshuffleMode);
    const dialog = window.currentPlaceholderDialog;
    console.log('[RESHUFFLE] dialog element:', dialog ? 'FOUND' : 'NOT FOUND');
    if (!dialog) {
        console.error('[RESHUFFLE] No dialog found! Cannot toggle reshuffle mode.');
        return;
    }
    
    const preview = dialog.querySelector('#dialogPreview');
    console.log('[RESHUFFLE] preview element:', preview ? 'FOUND' : 'NOT FOUND');
    
    const btn = dialog.querySelector('#dialogReshuffleBtn button');
    console.log('[RESHUFFLE] button element:', btn ? 'FOUND' : 'NOT FOUND');
    
    if (dialogReshuffleMode) {
        console.log('[RESHUFFLE] ENABLING dialog reshuffle mode');
        if (preview) {
            preview.classList.add('reshuffle-active');
            console.log('[RESHUFFLE] Added reshuffle-active class to preview');
        } else {
            console.error('[RESHUFFLE] Preview element not found!');
        }
        
        if (btn) {
            btn.style.background = '#ff6b6b';
            btn.textContent = '🔄 Reshuffle (Active)';
            console.log('[RESHUFFLE] Button updated to active state');
        } else {
            console.error('[RESHUFFLE] Button not found!');
        }
        
        // Add visual indicators to draggable cells
        const cells = preview ? preview.querySelectorAll('.media-cell') : [];
        console.log('[RESHUFFLE] Found', cells.length, 'media cells in dialog');
        let updatedCount = 0;
        cells.forEach(cell => {
            if (cell.querySelector('img, div')) {
                cell.style.border = '2px solid #43e97b';
                cell.style.cursor = 'grab';
                updatedCount++;
            }
        });
        console.log('[RESHUFFLE] Updated', updatedCount, 'cells with visual indicators');
    } else {
        console.log('[RESHUFFLE] DISABLING dialog reshuffle mode');
        if (preview) {
            preview.classList.remove('reshuffle-active');
            console.log('[RESHUFFLE] Removed reshuffle-active class from preview');
        }
        
        if (btn) {
            btn.style.background = '#43e97b';
            btn.textContent = '🔄 Reshuffle';
            console.log('[RESHUFFLE] Button updated to inactive state');
        } else {
            console.error('[RESHUFFLE] Button not found!');
        }
        
        // Remove visual indicators
        const cells = preview ? preview.querySelectorAll('.media-cell') : [];
        console.log('[RESHUFFLE] Removing visual indicators from', cells.length, 'cells');
        let removedCount = 0;
        cells.forEach(cell => {
            cell.style.border = '';
            cell.style.cursor = '';
            removedCount++;
        });
        console.log('[RESHUFFLE] Removed indicators from', removedCount, 'cells');
    }
    console.log('[RESHUFFLE] ========== toggleDialogReshuffleMode COMPLETE ==========');
}
window.extractPlaceholders = extractPlaceholders;
window.showPlaceholderSelectionDialog = showPlaceholderSelectionDialog;
window.selectPlaceholderForMedia = selectPlaceholderForMedia;
window.closePlaceholderDialog = closePlaceholderDialog;
window.assignMediaToPlaceholder = assignMediaToPlaceholder;
window.removeMediaFromPlaceholder = removeMediaFromPlaceholder;
window.updatePreview = updatePreview;
window.highlightPlaceholdersInEditor = highlightPlaceholdersInEditor;
window.exportObservationDocx = exportObservationDocx;
window.showSaveDraftDialog = showSaveDraftDialog;
window.showLoadDraftDialog = showLoadDraftDialog;
window.closeDraftDialog = closeDraftDialog;
window.toggleSection = toggleSection;
window.expandAllSections = expandAllSections;
window.collapseAllSections = collapseAllSections;
window.toggleReshuffleMode = toggleReshuffleMode;
window.toggleDialogSection = toggleDialogSection;
window.renderSectionsForDialog = renderSectionsForDialog;
window.renderSectionContentForDialog = renderSectionContentForDialog;
window.expandAllDialogSections = expandAllDialogSections;
window.collapseAllDialogSections = collapseAllDialogSections;
window.toggleDialogReshuffleMode = toggleDialogReshuffleMode;
window.updateDialogPreview = updateDialogPreview;
window.expandDialogSectionForPlaceholder = expandDialogSectionForPlaceholder;

