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
    if (typeof window !== 'undefined' && typeof window.updatePreview === 'function') {
        try {
            window.updatePreview();
        } catch (e) {
            console.error('Error calling updatePreview:', e);
        }
    }
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
    if (typeof window !== 'undefined' && typeof window.updateMediaCardStates === 'function') {
        try {
            window.updateMediaCardStates();
        } catch (e) {
            console.error('Error calling updateMediaCardStates:', e);
        }
    }
    if (typeof window !== 'undefined' && typeof window.updatePreview === 'function') {
        try {
            window.updatePreview();
        } catch (e) {
            console.error('Error calling updatePreview:', e);
        }
    }
    if (typeof window !== 'undefined' && typeof window.updatePlaceholderStats === 'function') {
        try {
            window.updatePlaceholderStats();
        } catch (e) {
            console.error('Error calling updatePlaceholderStats:', e);
        }
    }

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
        if (typeof window !== 'undefined' && typeof window.updateMediaCardStates === 'function') {
            try {
                window.updateMediaCardStates();
            } catch (e) {
                console.error('Error calling updateMediaCardStates:', e);
            }
        }
        if (typeof window !== 'undefined' && typeof window.updatePreview === 'function') {
            try {
                window.updatePreview();
            } catch (e) {
                console.error('Error calling updatePreview:', e);
            }
        }
        if (typeof window !== 'undefined' && typeof window.updatePlaceholderStats === 'function') {
            try {
                window.updatePlaceholderStats();
            } catch (e) {
                console.error('Error calling updatePlaceholderStats:', e);
            }
        }
    }
}

/**
 * Update media card states (enabled/disabled)
 */
function updateMediaCardStates() {
    const cards = document.querySelectorAll('.observation-media-card');
    const assignments = getCurrentAssignments();
    const textEditor = document.getElementById('observationTextEditor');
    const text = textEditor ? textEditor.value : '';
    
    cards.forEach(card => {
        const mediaPath = card.dataset.mediaPath;
        const isAssigned = isMediaAssigned(mediaPath);

        if (isAssigned) {
            card.classList.add('media-assigned');
            card.style.opacity = '0.5';
            card.style.cursor = 'not-allowed';
            card.draggable = false;

            // Get section color for this media item
            let sectionColor = null;
            if (typeof window !== 'undefined' && typeof window.getSectionColorForMedia === 'function') {
                try {
                    sectionColor = window.getSectionColorForMedia(mediaPath, assignments, text);
                } catch (e) {
                    console.error('Error calling getSectionColorForMedia:', e);
                }
            } else if (typeof getSectionColorForMedia === 'function') {
                // Fallback to local function if available
                try {
                    sectionColor = getSectionColorForMedia(mediaPath, assignments, text);
                } catch (e) {
                    console.error('Error calling local getSectionColorForMedia:', e);
                }
            }
            
            // Update badge with section color
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
            
            // Apply section color to badge
            if (badge && sectionColor) {
                badge.style.background = `${sectionColor}E6`; // 90% opacity
                badge.style.borderColor = sectionColor;
                badge.style.color = 'white';
            } else if (badge) {
                // Fallback to default color if no section color found
                badge.style.background = 'rgba(78, 205, 196, 0.9)';
                badge.style.borderColor = '#4ecdc4';
                badge.style.color = 'white';
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
    console.log('[DIALOG] ===== showPlaceholderSelectionDialog CALLED =====');

    // Handle both single media object and array of media
    const isBulk = Array.isArray(media);
    const mediaList = isBulk ? media : [media];

    const colorMap = assignPlaceholderColors(placeholders);
    const assignments = getCurrentAssignments();

    // Get text editor content to parse sections
    const textEditor = document.getElementById('observationTextEditor');
    const text = textEditor ? textEditor.value : '';
    const sectionData = parseSections(text);
    
    // Track section expanded state to prevent collapse
    const sectionExpandedState = {};
    if (sectionData.hasSections) {
        sectionData.sections.forEach(section => {
            const sectionPlaceholders = extractPlaceholders(section.content);
            const hasAssignedMedia = sectionPlaceholders.some(placeholder => {
                const placeholderKey = placeholder.toLowerCase();
                return assignments[placeholderKey] && assignments[placeholderKey].length > 0;
            });
            sectionExpandedState[section.id] = hasAssignedMedia; // Start expanded if has assigned media
        });
    }

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

    // Create dialog with new layout: Media (left) | Preview (right)
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
        min-width: 900px;
        max-width: 95vw;
        width: 90vw;
        max-height: 85vh;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        display: flex;
        flex-direction: column;
    `;

    // Store selected media globally for drag-and-drop
    window.bulkSelectedMedia = mediaList;
    window.dialogSectionExpandedState = sectionExpandedState; // Store section state

    // Generate preview HTML
    const validation = validatePlaceholders(text, assignments);
    let previewHtml = '';
    if (sectionData.hasSections) {
        // Try to get renderSectionsForDialog from window or local scope
        const renderFn = typeof window.renderSectionsForDialog === 'function' 
            ? window.renderSectionsForDialog 
            : (typeof renderSectionsForDialog === 'function' ? renderSectionsForDialog : null);
        
        if (renderFn) {
            previewHtml = renderFn(sectionData, placeholders, colorMap, assignments, validation, mediaList);
        } else {
            console.error('[DIALOG] renderSectionsForDialog not available');
            previewHtml = '<p>Error: Preview rendering function not available</p>';
        }
    } else {
        // Render without sections (same logic as before)
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
                previewHtmlTemp += generateMediaTable(assignedMedia, placeholder);
            } else {
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
        if (lastIndex < text.length) {
            previewHtmlTemp += escapeHtml(text.substring(lastIndex)).replace(/\n/g, '<br>');
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

    // Build dialog HTML with two-column layout
    let dialogHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="color: #e0e0e0; margin: 0;">Assign Media to Placeholder</h3>
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
        <div style="display: flex; gap: 20px; flex: 1; min-height: 0;">
            <!-- LEFT: Media List -->
            <div style="flex: 0 0 300px; display: flex; flex-direction: column; border: 1px solid #555; border-radius: 4px; background: #1e1e1e; overflow: hidden;">
                <div style="padding: 10px; border-bottom: 1px solid #555; background: #2a2a2a;">
                    <div style="color: #e0e0e0; font-size: 14px; font-weight: bold;">Media (${mediaList.length})</div>
                    <div style="color: #999; font-size: 11px; margin-top: 4px;">💡 Drag to preview on right</div>
                </div>
                <div style="flex: 1; overflow-y: auto; padding: 10px; display: flex; flex-wrap: wrap; gap: 8px; align-content: flex-start;" id="dialogMediaList">
    `;

    // Add media thumbnails to left panel
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
                 style="position: relative; width: 130px; height: 100px; border: 2px solid #667eea; border-radius: 4px; overflow: hidden; background: #1a1a1a; cursor: grab; user-select: none;">
                <img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(media.path)}&size=130x100" 
                     alt="${media.name}" 
                     draggable="false"
                     style="width: 100%; height: 100%; object-fit: cover; pointer-events: none; user-select: none;">
                ${media.type === 'video' ? '<span style="position: absolute; top: 2px; right: 2px; background: rgba(0,0,0,0.7); color: white; font-size: 8px; padding: 2px 4px; border-radius: 2px; pointer-events: none;">⏯</span>' : ''}
                ${media.type === 'document' ? '<span style="position: absolute; top: 2px; right: 2px; background: rgba(200,0,0,0.8); color: white; font-size: 8px; padding: 2px 4px; border-radius: 2px; pointer-events: none;">📄</span>' : ''}
                <div style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.7); color: white; font-size: 10px; padding: 2px 4px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; pointer-events: none;">${escapeHtml(media.name)}</div>
            </div>
        `;
    });

    dialogHTML += `
                </div>
            </div>
            <!-- RIGHT: Live Preview -->
            <div style="flex: 1; display: flex; flex-direction: column; border: 1px solid #555; border-radius: 4px; background: #1e1e1e; overflow: hidden; min-width: 0;">
                <div style="padding: 10px; border-bottom: 1px solid #555; background: #2a2a2a;">
                    <div style="color: #e0e0e0; font-size: 14px; font-weight: bold;">Live Preview</div>
                </div>
                <div style="flex: 1; overflow-y: auto; padding: 15px;"
                     ondrop="handleDialogPreviewDrop(event)" 
                     ondragover="handleDialogPreviewDragOver(event)">
                    <div id="dialogPreview" style="color: #e0e0e0; font-size: 13px; line-height: 1.6;">
                        ${previewHtml}
                    </div>
                </div>
            </div>
        </div>
    `;

    dialogHTML += `
        <div style="margin-top: 15px; text-align: right; border-top: 1px solid #555; padding-top: 15px;">
            <button id="placeholderDialogCancelBtn" 
                    onclick="if(window.currentPlaceholderDialog){window.currentPlaceholderDialog.remove();window.currentPlaceholderDialog=null;window.currentPlaceholderDialogMedia=null;}if(typeof window.closePlaceholderDialog==='function'){window.closePlaceholderDialog();}return false;"
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
    
    // Force delete buttons to be visible in dialog immediately after creation
    setTimeout(() => {
        const preview = dialog.querySelector('#dialogPreview');
        if (preview) {
            const deleteButtons = preview.querySelectorAll('.dialog-delete-btn, .remove-media-btn');
            deleteButtons.forEach(btn => {
                btn.style.setProperty('display', 'flex', 'important');
                btn.style.setProperty('visibility', 'visible', 'important');
                btn.style.setProperty('opacity', '1', 'important');
                btn.style.setProperty('position', 'absolute', 'important');
                btn.style.setProperty('top', '5px', 'important');
                btn.style.setProperty('right', '5px', 'important');
                btn.style.setProperty('z-index', '100', 'important');
            });
        }
    }, 100);

    // Add event listener to cancel button - use immediate function to ensure it works
    setTimeout(() => {
        const cancelBtn = dialog.querySelector('#placeholderDialogCancelBtn');
        if (cancelBtn) {
            // Remove any existing listeners by cloning
            const newCancelBtn = cancelBtn.cloneNode(true);
            cancelBtn.parentNode.replaceChild(newCancelBtn, cancelBtn);

            // Add fresh event listener - directly close the dialog
            newCancelBtn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                // Directly close the dialog
                    if (window.currentPlaceholderDialog) {
                        window.currentPlaceholderDialog.remove();
                        window.currentPlaceholderDialog = null;
                        window.currentPlaceholderDialogMedia = null;
                    }
                // Also try calling the function if available
                if (typeof window.closePlaceholderDialog === 'function') {
                    window.closePlaceholderDialog();
                }
            });
        }
    }, 0);

    // Also allow closing by clicking outside the dialog
    dialog.addEventListener('click', function (e) {
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
// Note: Most functions are assigned to window later in the file after they are defined
// This early block only assigns functions that are already defined above
if (typeof window !== 'undefined') {
    // Functions defined earlier in the file can be assigned here
    // Functions defined later are assigned after their definitions
}

/**
 * Initialize current draft tracking
 */
if (!window.currentDraft) {
    window.currentDraft = {
        id: null,
        name: null
    };
}

/**
 * Show current draft in UI
 */
function updateCurrentDraftDisplay() {
    const display = document.getElementById('currentDraftDisplay');
    const nameSpan = document.getElementById('currentDraftName');
    const saveBtn = document.getElementById('saveDraftBtn');
    
    if (window.currentDraft.id && window.currentDraft.name) {
        // Show draft display
        if (display) display.style.display = 'block';
        if (nameSpan) nameSpan.textContent = window.currentDraft.name;
        if (saveBtn) {
            saveBtn.textContent = '💾 Update Draft';
            saveBtn.onclick = handleSaveOrUpdateDraft;
        }
    } else {
        // Hide draft display
        if (display) display.style.display = 'none';
        if (nameSpan) nameSpan.textContent = '';
        if (saveBtn) {
            saveBtn.textContent = '💾 Save Draft';
            saveBtn.onclick = handleSaveOrUpdateDraft;
        }
    }
}

/**
 * Clear current draft
 */
function clearCurrentDraft() {
    // Clear draft info
    window.currentDraft.id = null;
    window.currentDraft.name = null;
    
    // Clear localStorage
    try {
        localStorage.removeItem('observationMediaCurrentDraftId');
    } catch (e) {
        console.warn('Failed to clear draft ID from localStorage:', e);
    }
    
    // Clear editor content
    const editor = document.getElementById('observationTextEditor');
    if (editor) {
        editor.value = '';
    }
    
    // Clear assignments
    window.observationMediaAssignments = {};
    
    // Clear selected subfolder
    const subfolderSelect = document.getElementById('observationSubfolderSelect');
    if (subfolderSelect) {
        subfolderSelect.value = '';
    }
    
    // Directly clear the media browser grid - this is the key fix
    const grid = document.getElementById('observationMediaGrid');
    if (grid) {
        // Clear all content immediately
        grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;" id="mediaBrowserMessage">Please select both qualification and learner</p>';
    }
    const countEl = document.getElementById('observationMediaCount');
    if (countEl) {
        countEl.textContent = '0 files';
    }
    
    // Clear any media-related state
    if (window.observationMediaData) {
        window.observationMediaData = {};
    }
    
    // Don't reload media automatically - let the user manually reload if they want
    // The grid is already cleared above, so it will show the empty state
    // If qualification/learner are selected, the user can manually reload media if needed
    
    // Clear standards
    if (typeof window !== 'undefined' && typeof window.clearStandards === 'function') {
        try {
            window.clearStandards();
        } catch (e) {
            console.error('Error calling clearStandards:', e);
        }
    }
    
    // Update UI to reflect cleared state
    if (typeof window !== 'undefined' && typeof window.highlightPlaceholdersInEditor === 'function') {
        try {
            window.highlightPlaceholdersInEditor();
        } catch (e) {
            console.error('Error calling highlightPlaceholdersInEditor:', e);
        }
    }
    if (typeof window !== 'undefined' && typeof window.updatePreview === 'function') {
        try {
            window.updatePreview();
        } catch (e) {
            console.error('Error calling updatePreview:', e);
        }
    }
    if (typeof window !== 'undefined' && typeof window.updateMediaCardStates === 'function') {
        try {
            window.updateMediaCardStates();
        } catch (e) {
            console.error('Error calling updateMediaCardStates:', e);
        }
    }
    
    // Update current draft display (will hide the draft display)
    updateCurrentDraftDisplay();
}

/**
 * Handle save or update draft
 */
function handleSaveOrUpdateDraft() {
    // Show enhanced dialog exists, use it; otherwise fall back to simple prompt
    if (typeof showEnhancedDraftDialog === 'function') {
        showEnhancedDraftDialog();
    } else {
        // Fallback to old behavior
    if (window.currentDraft.id) {
        updateDraft(window.currentDraft.id);
    } else {
        showSaveDraftDialog();
        }
    }
}

/**
 * Show enhanced save/update draft dialog with JSON file and unit selection
 */
async function showEnhancedDraftDialog() {
    const isUpdate = !!window.currentDraft.id;
    const currentDraftName = window.currentDraft.name || '';
    
    // Get learner ID from dropdown
    const learnerSelect = document.getElementById('learnerSelect');
    const learnerId = learnerSelect ? learnerSelect.value : null;
    
    if (!learnerId && !isUpdate) {
        alert('Please select a learner first before saving a draft first before saving a draft.');
        return;
    }
    
    // Create dialog
    const dialog = document.createElement('div');
    dialog.className = 'draft-dialog';
    dialog.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); z-index: 10000; display: flex; align-items: center; justify-content: center;';
    dialog.onclick = function(e) {
        if (e.target === dialog) {
            dialog.remove();
        }
    };
    
    // Get current draft data if updating
    let currentJsonFileId = '';
    let currentSelectedUnitIds = [];
    if (isUpdate && window.currentDraft.id) {
        try {
            const response = await fetch(`/v2p-formatter/media-converter/observation-media/drafts/${window.currentDraft.id}`);
            const data = await response.json();
            if (data.success && data.draft) {
                currentJsonFileId = data.draft.json_file_id || '';
                currentSelectedUnitIds = data.draft.selected_unit_ids || [];
            }
        } catch (e) {
            console.warn('Could not load current draft data:', e);
        }
    }
    
    // Build dialog HTML
    const prefix = learnerId ? `learner_${learnerId}_` : '';
    const defaultName = isUpdate ? currentDraftName.replace(prefix, '') : 'My Draft';
    
    dialog.innerHTML = `
        <div style="background: #2a2a2a; border: 2px solid #667eea; border-radius: 8px; padding: 25px; width: 90%; max-width: 600px; max-height: 90vh; overflow-y: auto;" onclick="event.stopPropagation();">
            <h3 style="color: #e0e0e0; margin: 0 0 20px 0;">${isUpdate ? 'Update Draft' : 'Save Draft'}</h3>
            
            <div style="margin-bottom: 15px;">
                <label style="color: #e0e0e0; display: block; margin-bottom: 5px; font-weight: 500;">Draft Name:</label>
                <input type="text" id="draftDialogName" value="${defaultName}" 
                       style="width: 100%; padding: 8px 12px; background: #1e1e1e; color: #e0e0e0; border: 1px solid #555; border-radius: 4px; font-size: 14px; box-sizing: border-box;">
                ${learnerId ? `<div style="color: #999; font-size: 12px; margin-top: 4px;">Will be saved as: ${prefix}[name]</div>` : ''}
            </div>
            
            <div style="margin-bottom: 15px;">
                <label style="color: #e0e0e0; display: block; margin-bottom: 5px; font-weight: 500;">JSON Standards File (Optional):</label>
                <select id="draftDialogJsonFile" 
                        style="width: 100%; padding: 8px 12px; background: #1e1e1e; color: #e0e0e0; border: 1px solid #555; border-radius: 4px; font-size: 14px; box-sizing: border-box;">
                    <option value="">None (no JSON file assigned)</option>
                </select>
            </div>
            
            <div id="draftDialogUnitsContainer" style="margin-bottom: 15px; display: none;">
                <label style="color: #e0e0e0; display: block; margin-bottom: 5px; font-weight: 500;">Select Units (Optional):</label>
                <div id="draftDialogUnitsList" style="max-height: 200px; overflow-y: auto; border: 1px solid #555; border-radius: 4px; padding: 10px; background: #1a1a1a;">
                    <p style="color: #999; text-align: center; padding: 10px;">Select a JSON file to load units</p>
                </div>
                <div style="margin-top: 10px; display: flex; gap: 10px;">
                    <button onclick="selectAllDraftDialogUnits()" style="padding: 6px 12px; background: #555; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">Select All</button>
                    <button onclick="deselectAllDraftDialogUnits()" style="padding: 6px 12px; background: #555; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">Deselect All</button>
                </div>
            </div>
            
            <div style="margin-top: 20px; text-align: right; border-top: 1px solid #555; padding-top: 15px;">
                <button onclick="closeEnhancedDraftDialog()" 
                        style="padding: 8px 16px; background: #555; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 10px;">
                    Cancel
                </button>
                <button onclick="saveDraftFromDialog()" 
                        style="padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    ${isUpdate ? 'Update Draft' : 'Save Draft'}
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(dialog);
    window.currentDraftDialog = dialog;
    
    // Load JSON files
    await loadJSONFilesForDraftDialog();
    
    // Set current JSON file if updating
    if (currentJsonFileId) {
        const jsonSelect = document.getElementById('draftDialogJsonFile');
        if (jsonSelect) {
            jsonSelect.value = currentJsonFileId;
            jsonSelect.dispatchEvent(new Event('change'));
        }
    }
    
    // Setup JSON file change handler
    const jsonSelect = document.getElementById('draftDialogJsonFile');
    if (jsonSelect) {
        jsonSelect.addEventListener('change', async function() {
            const jsonFileId = this.value;
            if (jsonFileId) {
                await loadUnitsForDraftDialog(jsonFileId, currentSelectedUnitIds);
            } else {
                document.getElementById('draftDialogUnitsContainer').style.display = 'none';
            }
        });
    }
}

/**
 * Load JSON files for draft dialog
 */
async function loadJSONFilesForDraftDialog() {
    try {
        const response = await fetch('/v2p-formatter/ac-matrix/json-files');
        const data = await response.json();
        
        if (data.success) {
            const selector = document.getElementById('draftDialogJsonFile');
            if (selector) {
                data.files.forEach(file => {
                    const option = document.createElement('option');
                    option.value = file.id;
                    option.textContent = file.qualification_name || file.name;
                    selector.appendChild(option);
                });
            }
        }
    } catch (error) {
        console.error('Error loading JSON files:', error);
    }
}

/**
 * Load units for draft dialog
 */
async function loadUnitsForDraftDialog(jsonFileId, preselectedUnitIds = []) {
    const container = document.getElementById('draftDialogUnitsContainer');
    const unitsList = document.getElementById('draftDialogUnitsList');
    
    if (!container || !unitsList) return;
    
    container.style.display = 'block';
    unitsList.innerHTML = '<p style="color: #999; text-align: center; padding: 10px;">Loading units...</p>';
    
    try {
        const response = await fetch(`/v2p-formatter/ac-matrix/json-files/${jsonFileId}/units`);
        const data = await response.json();
        
        if (data.success && data.units && data.units.length > 0) {
            unitsList.innerHTML = '';
            
            data.units.forEach(unit => {
                const label = document.createElement('label');
                label.style.cssText = 'display: block; padding: 8px; cursor: pointer; color: #e0e0e0; border-radius: 4px; margin-bottom: 4px;';
                
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.value = unit.unit_id;
                checkbox.className = 'draft-dialog-unit-checkbox';
                checkbox.checked = preselectedUnitIds.length === 0 || preselectedUnitIds.includes(unit.unit_id);
                checkbox.style.cssText = 'margin-right: 8px; cursor: pointer;';
                
                const unitLabel = document.createElement('span');
                unitLabel.textContent = `Unit ${unit.unit_id}: ${unit.unit_name || 'Unnamed Unit'}`;
                
                label.appendChild(checkbox);
                label.appendChild(unitLabel);
                unitsList.appendChild(label);
            });
        } else {
            unitsList.innerHTML = '<p style="color: #999; text-align: center; padding: 10px;">No units found</p>';
        }
    } catch (error) {
        console.error('Error loading units:', error);
        unitsList.innerHTML = '<p style="color: #ff6b6b; text-align: center; padding: 10px;">Error loading units</p>';
    }
}

/**
 * Select all units in draft dialog
 */
function selectAllDraftDialogUnits() {
    const checkboxes = document.querySelectorAll('.draft-dialog-unit-checkbox');
    checkboxes.forEach(cb => cb.checked = true);
}

/**
 * Deselect all units in draft dialog
 */
function deselectAllDraftDialogUnits() {
    const checkboxes = document.querySelectorAll('.draft-dialog-unit-checkbox');
    checkboxes.forEach(cb => cb.checked = false);
}

/**
 * Close enhanced draft dialog
 */
function closeEnhancedDraftDialog() {
    if (window.currentDraftDialog) {
        window.currentDraftDialog.remove();
        window.currentDraftDialog = null;
    }
}

/**
 * Save draft from dialog
 */
function saveDraftFromDialog() {
    const nameInput = document.getElementById('draftDialogName');
    const jsonSelect = document.getElementById('draftDialogJsonFile');
    const unitCheckboxes = document.querySelectorAll('.draft-dialog-unit-checkbox:checked');
    
    if (!nameInput || !nameInput.value.trim()) {
        alert('Please enter a draft name');
        return;
    }
    
    const learnerSelect = document.getElementById('learnerSelect');
    const learnerId = learnerSelect ? learnerSelect.value : null;
    const prefix = learnerId ? `learner_${learnerId}_` : '';
    const draftName = nameInput.value.trim().startsWith(prefix) ? nameInput.value.trim() : `${prefix}${nameInput.value.trim()}`;
    
    const jsonFileId = jsonSelect ? jsonSelect.value : '';
    const selectedUnitIds = Array.from(unitCheckboxes).map(cb => cb.value);
    
    closeEnhancedDraftDialog();
    
    if (window.currentDraft.id) {
        updateDraft(window.currentDraft.id, draftName, jsonFileId, selectedUnitIds);
    } else {
        saveDraft(draftName, jsonFileId, selectedUnitIds);
    }
}

/**
 * Show save draft dialog (legacy - kept for compatibility)
 */
function showSaveDraftDialog() {
    // Get learner ID from dropdown
    const learnerSelect = document.getElementById('learnerSelect');
    const learnerId = learnerSelect ? learnerSelect.value : null;
    
    if (!learnerId) {
        alert('Please select a learner first before saving a draft.');
        return;
    }
    
    const name = prompt(`Enter draft name (will be prefixed with "learner_${learnerId}_"):`, 'My Draft');
    if (!name) return;

    // Add "learner_{learnerId}_" prefix to the name
    const prefix = `learner_${learnerId}_`;
    const prefixedName = name.startsWith(prefix) ? name : `${prefix}${name}`;
    
    saveDraft(prefixedName);
}
// Make function available globally immediately
if (typeof window !== 'undefined') {
    window.showSaveDraftDialog = showSaveDraftDialog;
}

/**
 * Save current draft (creates new)
 */
function saveDraft(name, jsonFileId = '', selectedUnitIds = []) {
    const editor = document.getElementById('observationTextEditor');
    if (!editor) return;

    const text = editor.value;
    const assignments = getCurrentAssignments();
    const selectedSubfolder = document.getElementById('observationSubfolderSelect')?.value || null;
    
    // Get qualification and learner from dropdowns
    const qualificationSelect = document.getElementById('qualificationSelect');
    const learnerSelect = document.getElementById('learnerSelect');
    const qualification = qualificationSelect ? qualificationSelect.value : null;
    const learner = learnerSelect ? learnerSelect.value : null;
    
    // Get header fields
    const headerData = {
        learner: document.getElementById('headerLearner')?.value || '',
        assessor: document.getElementById('headerAssessor')?.value || '',
        visit_date: document.getElementById('headerVisitDate')?.value || '',
        location: document.getElementById('headerLocation')?.value || '',
        address: document.getElementById('headerAddress')?.value || ''
    };
    
    // Get assessor feedback
    const assessorFeedback = document.getElementById('assessorFeedback')?.value || '';

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
            selected_subfolder: selectedSubfolder,
            qualification: qualification,
            learner: learner,
            json_file_id: jsonFileId || null,
            selected_unit_ids: selectedUnitIds,
            header_data: headerData,
            assessor_feedback: assessorFeedback
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Store current draft info
                window.currentDraft.id = data.draft_id;
                window.currentDraft.name = data.draft_name;
                
                // Save draft ID to localStorage for persistence across page refreshes
                try {
                    localStorage.setItem('observationMediaCurrentDraftId', data.draft_id);
                } catch (e) {
                    console.warn('Failed to save draft ID to localStorage:', e);
                }
                
                updateCurrentDraftDisplay();
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
            updateCurrentDraftDisplay();
        });
}
// Make function available globally immediately
if (typeof window !== 'undefined') {
    window.saveDraft = saveDraft;
}

/**
 * Update existing draft
 */
function updateDraft(draftId, draftName = null, jsonFileId = '', selectedUnitIds = []) {
    const editor = document.getElementById('observationTextEditor');
    if (!editor) return;

    const text = editor.value;
    const assignments = getCurrentAssignments();
    const selectedSubfolder = document.getElementById('observationSubfolderSelect')?.value || null;
    
    // Get qualification and learner from dropdowns
    const qualificationSelect = document.getElementById('qualificationSelect');
    const learnerSelect = document.getElementById('learnerSelect');
    const qualification = qualificationSelect ? qualificationSelect.value : null;
    const learner = learnerSelect ? learnerSelect.value : null;
    
    // Get header fields
    const headerData = {
        learner: document.getElementById('headerLearner')?.value || '',
        assessor: document.getElementById('headerAssessor')?.value || '',
        visit_date: document.getElementById('headerVisitDate')?.value || '',
        location: document.getElementById('headerLocation')?.value || '',
        address: document.getElementById('headerAddress')?.value || ''
    };
    
    // Get assessor feedback
    const assessorFeedback = document.getElementById('assessorFeedback')?.value || '';

    // Show loading state
    const saveBtn = document.getElementById('saveDraftBtn');
    const originalText = saveBtn.textContent;
    saveBtn.disabled = true;
    saveBtn.textContent = '⏳ Updating...';

    // Build update payload
    const payload = {
        text_content: text,
        assignments: assignments,
        selected_subfolder: selectedSubfolder,
        qualification: qualification,
        learner: learner,
        json_file_id: jsonFileId || null,
        selected_unit_ids: selectedUnitIds,
        header_data: headerData,
        assessor_feedback: assessorFeedback
    };
    
    // Include name if provided (for renaming)
    if (draftName) {
        payload.name = draftName;
    }

    // Update draft via API
    fetch(`/v2p-formatter/media-converter/observation-media/drafts/${draftId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Draft updated successfully!\n\nName: ${window.currentDraft.name}`);
            } else {
                alert(`Error updating draft: ${data.error || 'Unknown error'}`);
            }
        })
        .catch(error => {
            console.error('Update draft error:', error);
            alert(`Error updating draft: ${error.message}`);
        })
        .finally(() => {
            saveBtn.disabled = false;
            saveBtn.textContent = originalText;
            updateCurrentDraftDisplay();
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
// Make function available globally immediately
if (typeof window !== 'undefined') {
    window.showLoadDraftDialog = showLoadDraftDialog;
}

/**
 * Show draft selection dialog
 */
function showDraftSelectionDialog(drafts) {
    // Create backdrop overlay
    const backdrop = document.createElement('div');
    backdrop.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: 9999;
    `;
    backdrop.onclick = function() {
        closeDraftDialog();
    };
    document.body.appendChild(backdrop);

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
        padding: 25px;
        z-index: 10000;
        min-width: 550px;
        max-width: 700px;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    `;
    dialog.onclick = function(e) {
        e.stopPropagation();
    };

    let dialogHTML = `
        <h3 style="color: #e0e0e0; margin-bottom: 20px; font-size: 18px; border-bottom: 1px solid #555; padding-bottom: 10px;">Select a draft to load</h3>
        <div style="max-height: 400px; overflow-y: auto;">
    `;

    drafts.forEach(draft => {
        const date = new Date(draft.updated_at || draft.created_at);
        const dateStr = date.toLocaleString();

        dialogHTML += `
            <div class="draft-item" 
                 style="padding: 12px; margin-bottom: 8px; background: #1e1e1e; border: 1px solid #555; border-radius: 4px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 1;">
                        <div style="color: #e0e0e0; font-weight: bold; margin-bottom: 4px;">${draft.name}</div>
                        <div style="color: #999; font-size: 11px;">
                            Updated: ${dateStr}
                            ${draft.selected_subfolder ? ` • Subfolder: ${draft.selected_subfolder}` : ''}
                            ${draft.placeholder_count ? ` • ${draft.placeholder_count} placeholders` : ''}
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px; margin-left: 15px;">
                        <button onclick="event.stopPropagation(); loadDraft('${draft.id}'); closeDraftDialog();" 
                                style="padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 500; transition: background 0.2s;"
                                onmouseover="this.style.background='#5568d3'"
                                onmouseout="this.style.background='#667eea'">
                            Load
                        </button>
                        <button onclick="event.stopPropagation(); deleteDraft('${draft.id}'); closeDraftDialog(); showLoadDraftDialog();" 
                                style="padding: 8px 16px; background: #ff6b6b; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 500; transition: background 0.2s;"
                                onmouseover="this.style.background='#ee5a5a'"
                                onmouseout="this.style.background='#ff6b6b'">
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

    // Store dialog and backdrop references
    window.currentDraftDialog = dialog;
    backdrop.className = 'draft-selection-backdrop';
}

/**
 * Close draft dialog
 */
function closeDraftDialog() {
    if (window.currentDraftDialog) {
        window.currentDraftDialog.remove();
        window.currentDraftDialog = null;
    }
    // Remove backdrop if it exists
    const backdrop = document.querySelector('.draft-selection-backdrop');
    if (backdrop) {
        backdrop.remove();
    }
}
// Make function available globally immediately
if (typeof window !== 'undefined') {
    window.closeDraftDialog = closeDraftDialog;
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

                // Store current draft info
                window.currentDraft.id = draftId;
                window.currentDraft.name = draft.name;
                
                // Save draft ID to localStorage for persistence across page refreshes
                try {
                    localStorage.setItem('observationMediaCurrentDraftId', draftId);
                } catch (e) {
                    console.warn('Failed to save draft ID to localStorage:', e);
                }

                // Load text content
                const editor = document.getElementById('observationTextEditor');
                if (editor) {
                    editor.value = draft.text_content || '';
                }

                // Load header fields
                if (draft.header_data) {
                    const headerData = draft.header_data;
                    if (document.getElementById('headerLearner')) {
                        document.getElementById('headerLearner').value = headerData.learner || '';
                    }
                    if (document.getElementById('headerAssessor')) {
                        document.getElementById('headerAssessor').value = headerData.assessor || '';
                    }
                    if (document.getElementById('headerVisitDate')) {
                        document.getElementById('headerVisitDate').value = headerData.visit_date || '';
                    }
                    if (document.getElementById('headerLocation')) {
                        document.getElementById('headerLocation').value = headerData.location || '';
                    }
                    if (document.getElementById('headerAddress')) {
                        document.getElementById('headerAddress').value = headerData.address || '';
                    }
                }
                
                // Load assessor feedback
                if (draft.assessor_feedback !== undefined) {
                    const feedbackField = document.getElementById('assessorFeedback');
                    if (feedbackField) {
                        feedbackField.value = draft.assessor_feedback || '';
                    }
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

                // Restore qualification and learner if saved in draft
                if (draft.qualification) {
                    const qualificationSelect = document.getElementById('qualificationSelect');
                    if (qualificationSelect) {
                        qualificationSelect.value = draft.qualification;
                        // Trigger change event to load learners
                        qualificationSelect.dispatchEvent(new Event('change'));
                    }
                }
                
                if (draft.learner) {
                    const learnerSelect = document.getElementById('learnerSelect');
                    if (learnerSelect) {
                        // Wait a bit for learners to load if qualification was just set
                        setTimeout(() => {
                            learnerSelect.value = draft.learner;
                            // Trigger change event to reload media
                            learnerSelect.dispatchEvent(new Event('change'));
                        }, 300);
                    }
                }

                // Update UI
                if (typeof highlightPlaceholdersInEditor === 'function') {
                    highlightPlaceholdersInEditor();
                }
                if (typeof window !== 'undefined' && typeof window.updatePreview === 'function') {
                    try {
                        window.updatePreview();
                    } catch (e) {
                        console.error('Error calling updatePreview:', e);
                    }
                }
                if (typeof updateMediaCardStates === 'function') {
                    updateMediaCardStates();
                }

                // Update current draft display
                updateCurrentDraftDisplay();

                // Load standards if JSON file is assigned
                if (draft.json_file_id) {
                    if (typeof window !== 'undefined' && typeof window.loadStandardsFromDraft === 'function') {
                        try {
                            window.loadStandardsFromDraft(draft).catch(error => {
                                console.error('Error loading standards:', error);
                            });
                        } catch (e) {
                            console.error('Error calling loadStandardsFromDraft:', e);
                        }
                    }
                } else {
                    if (typeof window !== 'undefined' && typeof window.clearStandards === 'function') {
                        try {
                            window.clearStandards();
                        } catch (e) {
                            console.error('Error calling clearStandards:', e);
                        }
                    }
                }

                // No alert - draft is loaded silently (name shown in UI)
            } else {
                // If draft failed to load (e.g., was deleted), clear localStorage
                if (draftId === localStorage.getItem('observationMediaCurrentDraftId')) {
                    try {
                        localStorage.removeItem('observationMediaCurrentDraftId');
                    } catch (e) {
                        console.warn('Failed to clear draft ID from localStorage:', e);
                    }
                }
                alert(`Error loading draft: ${data.error || 'Unknown error'}`);
            }
        })
        .catch(error => {
            console.error('Load draft error:', error);
            // If draft failed to load, clear localStorage
            try {
                const savedDraftId = localStorage.getItem('observationMediaCurrentDraftId');
                if (savedDraftId === draftId) {
                    localStorage.removeItem('observationMediaCurrentDraftId');
                }
            } catch (e) {
                console.warn('Failed to clear draft ID from localStorage:', e);
            }
            alert(`Error loading draft: ${error.message}`);
        });
}
// Make function available globally immediately
if (typeof window !== 'undefined') {
    window.loadDraft = loadDraft;
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
                // If the deleted draft was the current one, clear it
                if (window.currentDraft && window.currentDraft.id === draftId) {
                    clearCurrentDraft();
                }
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
// Make function available globally immediately
if (typeof window !== 'undefined') {
    window.deleteDraft = deleteDraft;
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

    // Determine filename: use draft name if available, otherwise prompt user
    let filename;
    if (window.currentDraft && window.currentDraft.id && window.currentDraft.name) {
        // Use draft name as filename
        filename = window.currentDraft.name;
        // Ensure it doesn't already have .docx extension
        if (filename.toLowerCase().endsWith('.docx')) {
            filename = filename.slice(0, -5); // Remove .docx extension
        }
    } else {
        // No draft loaded, prompt user
        filename = prompt('Enter filename (without extension):', 'observation_document');
        if (!filename) return;
    }

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
                // Ensure filename shows .docx extension
                let displayName = data.file_name;
                if (!displayName.toLowerCase().endsWith('.docx')) {
                    displayName += '.docx';
                }
                
                // Download file
                window.location.href = data.download_url;
                alert(`Document exported successfully!\n\nFile: ${displayName}`);
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

// Undo/Redo stacks for preview
let previewUndoStack = [];
let previewRedoStack = [];
const MAX_UNDO_STATES = 50;

// Store original text content when preview is opened (to preserve placeholders)
let previewOriginalText = '';
let previewPlaceholderMap = new Map(); // Maps table IDs to placeholder names

/**
 * Save current preview state for undo
 */
function savePreviewState() {
    const contentDiv = document.getElementById('draftPreviewContent');
    if (!contentDiv) return;
    
    const currentState = contentDiv.innerHTML;
    
    // Don't save if same as last state
    if (previewUndoStack.length > 0 && previewUndoStack[previewUndoStack.length - 1] === currentState) {
        return;
    }
    
    // Add to undo stack
    previewUndoStack.push(currentState);
    
    // Limit stack size
    if (previewUndoStack.length > MAX_UNDO_STATES) {
        previewUndoStack.shift();
    }
    
    // Clear redo stack (new edit clears redo)
    previewRedoStack = [];
    
    // Update button states
    updateUndoRedoButtons();
}

/**
 * Update undo/redo button states
 */
function updateUndoRedoButtons() {
    const undoBtn = document.getElementById('previewUndoBtn');
    const redoBtn = document.getElementById('previewRedoBtn');
    
    if (undoBtn) {
        undoBtn.disabled = previewUndoStack.length === 0;
        undoBtn.style.opacity = previewUndoStack.length === 0 ? '0.5' : '1';
    }
    
    if (redoBtn) {
        redoBtn.disabled = previewRedoStack.length === 0;
        redoBtn.style.opacity = previewRedoStack.length === 0 ? '0.5' : '1';
    }
}

/**
 * Undo last change in preview
 */
function previewUndo() {
    const contentDiv = document.getElementById('draftPreviewContent');
    if (!contentDiv || previewUndoStack.length === 0) return;
    
    // Save current state to redo stack
    previewRedoStack.push(contentDiv.innerHTML);
    
    // Restore previous state
    const previousState = previewUndoStack.pop();
    contentDiv.innerHTML = previousState;
    
    // Re-apply display settings
    updatePreviewDisplay();
    
    // Rebuild section navigation (in case sections changed)
    buildPreviewSectionNavigation();
    
    // Update button states
    updateUndoRedoButtons();
}

/**
 * Redo last undone change in preview
 */
function previewRedo() {
    const contentDiv = document.getElementById('draftPreviewContent');
    if (!contentDiv || previewRedoStack.length === 0) return;
    
    // Save current state to undo stack
    previewUndoStack.push(contentDiv.innerHTML);
    
    // Restore next state from redo stack
    const nextState = previewRedoStack.pop();
    contentDiv.innerHTML = nextState;
    
    // Re-apply display settings
    updatePreviewDisplay();
    
    // Rebuild section navigation (in case sections changed)
    buildPreviewSectionNavigation();
    
    // Update button states
    updateUndoRedoButtons();
}

/**
 * Select all hide elements checkboxes
 */
function selectAllHideElements() {
    const checkboxes = [
        document.getElementById('hideSectionTitles'),
        document.getElementById('hideAcCovered'),
        document.getElementById('hideImageSuggestion'),
        document.getElementById('hideParagraphNumbers'),
        document.getElementById('hideEmptyMediaFields'),
        document.getElementById('trimEmptyParagraphs')
    ];
    
    checkboxes.forEach(checkbox => {
        if (checkbox) {
            checkbox.checked = true;
        }
    });
    
    // Update preview display
    updatePreviewDisplay();
}

/**
 * Deselect all hide elements checkboxes
 */
function deselectAllHideElements() {
    const checkboxes = [
        document.getElementById('hideSectionTitles'),
        document.getElementById('hideAcCovered'),
        document.getElementById('hideImageSuggestion'),
        document.getElementById('hideParagraphNumbers'),
        document.getElementById('hideEmptyMediaFields'),
        document.getElementById('trimEmptyParagraphs'),
        document.getElementById('showHeader'),
        document.getElementById('showAssessorFeedback')
    ];
    
    checkboxes.forEach(checkbox => {
        if (checkbox) {
            checkbox.checked = false;
        }
    });
    
    // Update preview display
    updatePreviewDisplay();
}

/**
 * Extract text content from editable preview
 * Removes HTML structure (tables, buttons, etc.) and returns clean text
 * Replaces tables with their original placeholders
 * @param {boolean} preserveHiddenElements - If true, hidden elements are preserved in the extracted text (for Update Draft). If false, hidden elements are removed (for Export).
 */
function extractTextFromPreview(preserveHiddenElements = false) {
    const contentDiv = document.getElementById('draftPreviewContent');
    if (!contentDiv) return '';
    
    // Clone the content to avoid modifying the original
    const clone = contentDiv.cloneNode(true);
    
    // Remove all buttons (delete buttons, etc.)
    const buttons = clone.querySelectorAll('button');
    buttons.forEach(button => button.remove());
    
    // Check if empty media fields should be hidden (for export only)
    const hideEmptyMediaFields = !preserveHiddenElements && (document.getElementById('hideEmptyMediaFields')?.checked || false);
    
    // Remove empty tables if hideEmptyMediaFields is enabled (for export)
    if (hideEmptyMediaFields) {
        const emptyTables = clone.querySelectorAll('.preview-empty-table');
        emptyTables.forEach(table => {
            table.remove();
        });
    }
    
    // Only remove hidden elements if preserveHiddenElements is false (for export)
    // If true (for Update Draft), we want to preserve all elements in the original text
    if (!preserveHiddenElements) {
        // Remove hidden elements (like paragraph numbers when hidden)
        const hiddenElements = clone.querySelectorAll('.preview-paragraph-number[style*="display: none"], .preview-section-title[style*="display: none"], .preview-ac-covered-label[style*="display: none"], .preview-image-suggestion[style*="display: none"]');
        hiddenElements.forEach(el => {
            // For hidden labels, just remove the span, keep the parent
            if (el.classList.contains('preview-ac-covered-label')) {
                el.remove();
            } else {
                el.remove();
            }
        });
    } else {
        // For Update Draft: restore all hidden elements to their original state
        // This ensures the original text structure is preserved
        const hiddenSectionTitles = clone.querySelectorAll('.preview-section-title[style*="display: none"]');
        hiddenSectionTitles.forEach(el => {
            el.style.display = 'block';
        });
        
        const hiddenAcLabels = clone.querySelectorAll('.preview-ac-covered-label[style*="display: none"]');
        hiddenAcLabels.forEach(el => {
            el.style.display = 'inline';
        });
        
        const hiddenImageSuggestions = clone.querySelectorAll('.preview-image-suggestion[style*="display: none"]');
        hiddenImageSuggestions.forEach(el => {
            el.style.display = 'block';
        });
        
        const hiddenParagraphNumbers = clone.querySelectorAll('.preview-paragraph-number[style*="display: none"]');
        hiddenParagraphNumbers.forEach(el => {
            el.style.display = 'inline';
        });
    }
    
    // Replace all placeholder tables with their original placeholder text
    // This must happen AFTER removing buttons but BEFORE extracting text
    const placeholderTables = clone.querySelectorAll('.preview-placeholder-table, table[data-placeholder], .preview-empty-table');
    placeholderTables.forEach(table => {
        // Get placeholder name from data attribute
        let placeholderName = table.getAttribute('data-placeholder-name');
        if (!placeholderName) {
            const placeholderKey = table.getAttribute('data-placeholder');
            if (placeholderKey) {
                // Convert key to placeholder format (e.g., "image1" -> "{{Image1}}")
                placeholderName = `{{${placeholderKey.charAt(0).toUpperCase() + placeholderKey.slice(1)}}}`;
            } else {
                placeholderName = '{{Placeholder}}';
            }
        }
        
        // Replace table with placeholder text on its own line
        const placeholderText = document.createTextNode(placeholderName);
        if (table.parentNode) {
            // Insert placeholder before table
            table.parentNode.insertBefore(placeholderText, table);
            // Remove the table
            table.remove();
        }
    });
    
    // Extract text by processing each child node in order
    let text = '';
    const children = Array.from(clone.childNodes);
    
    for (let i = 0; i < children.length; i++) {
        const child = children[i];
        
        if (child.nodeType === Node.TEXT_NODE) {
            // Direct text node (could be from placeholder replacement)
            const txt = child.textContent.trim();
            if (txt && txt !== 'Empty' && txt !== 'Delete' && !txt.match(/^🗑️/)) {
                // If text doesn't end with newline, add one after placeholder
                if (txt.startsWith('{{') && txt.endsWith('}}')) {
                    // Placeholder - ensure it's on its own line
                    if (text && !text.endsWith('\n')) {
                        text += '\n';
                    }
                    text += txt + '\n';
                } else {
                    text += child.textContent;
                }
            }
        } else if (child.nodeType === Node.ELEMENT_NODE) {
            const tagName = child.tagName.toLowerCase();
            
            if (tagName === 'p') {
                // Check if this is an AC covered paragraph
                const isAcCovered = child.classList.contains('preview-ac-covered');
                
                // Extract text from paragraph
                let paraText = extractTextFromElement(child);
                
                // For AC covered paragraphs, ensure label and values stay on one line
                // Remove any internal newlines or excessive whitespace
                if (isAcCovered) {
                    // Replace any newlines within the AC covered text with a single space
                    paraText = paraText.replace(/\n+/g, ' ');
                    // Normalize multiple spaces to single space
                    paraText = paraText.replace(/\s+/g, ' ');
                }
                
                // Check if paragraph contains a placeholder (from table replacement)
                // If so, ensure placeholder is on its own line
                const placeholderPattern = /\{\{([A-Za-z0-9_]+)\}\}/g;
                if (placeholderPattern.test(paraText)) {
                    // Replace placeholder with newline + placeholder + newline
                    paraText = paraText.replace(placeholderPattern, '\n$&\n');
                }
                
                const trimmed = paraText.trim();
                
                if (trimmed) {
                    // For AC covered paragraphs, if previous paragraph ended with newline,
                    // we want AC covered on the next line (no blank line), so don't add extra newline before
                    if (isAcCovered) {
                        // AC covered should be directly after previous paragraph (if there was one)
                        // If text already ends with newline, that's perfect - just add AC text
                        // If text doesn't end with newline, add one
                        if (text && !text.endsWith('\n')) {
                            text += '\n';
                        }
                        // Don't add extra newline before AC covered - it will be on the line after previous paragraph
                    } else {
                        // Regular paragraph - ensure newline before (unless it's the first element)
                        if (text && !text.endsWith('\n')) {
                            text += '\n';
                        }
                    }
                    
                    text += trimmed;
                    // Always add newline after paragraph
                    text += '\n';
                } else {
                    // Empty paragraph - add blank line
                    if (text && !text.endsWith('\n')) {
                        text += '\n';
                    }
                    text += '\n';
                }
            } else if (tagName === 'br') {
                text += '\n';
            } else if (tagName === 'table') {
                // Tables should already be replaced, but handle just in case
                const placeholderName = child.getAttribute('data-placeholder-name') || '{{Placeholder}}';
                if (text && !text.endsWith('\n')) {
                    text += '\n';
                }
                text += placeholderName + '\n';
            }
        }
    }
    
    // Clean up: remove any remaining "Empty" or "Delete" text
    text = text.replace(/\bEmpty\b/g, '').replace(/\bDelete\b/g, '').replace(/🗑️/g, '');
    
    // Fix AC covered lines that are broken across multiple lines
    // Pattern: "AC covered: " followed by newline(s) and then AC values on next line
    // Replace with: "AC covered: " followed by AC values on same line
    text = text.replace(/(AC\s+covered\s*[:-]\s*)\n+(\s*[\d§\s,.;:]+)/gi, '$1$2');
    
    // Remove blank lines before AC covered lines
    // Pattern 1: AC covered with label (when label is visible)
    text = text.replace(/\n\n(AC\s+covered\s*[:-]\s*)/gi, '\n$1');
    // Pattern 2: AC values only (when label is hidden) - matches lines starting with number followed by colon
    // Typical AC value pattern: "641:3.2, 4.1; 642:1.1" or "§41:3.2, 4.1; 643:1.1"
    // Matches: newline, newline, optional whitespace/symbols, number, colon
    text = text.replace(/\n\n(\s*[§]?\s*\d+\s*:\s*[\d\s,.;]+)/g, '\n$1');
    
    // Normalize whitespace: replace 3+ consecutive newlines with 2 newlines (preserve blank lines)
    text = text.replace(/\n{3,}/g, '\n\n');
    
    // Trim leading/trailing whitespace but preserve internal structure
    text = text.trim();
    
    return text;
}

/**
 * Helper function to extract text from an element, handling nested elements
 */
function extractTextFromElement(element) {
    let text = '';
    
    // Process child nodes in order
    for (let i = 0; i < element.childNodes.length; i++) {
        const node = element.childNodes[i];
        
        if (node.nodeType === Node.TEXT_NODE) {
            const txt = node.textContent;
            // Don't filter out text here - preserve all text content
            // Filtering will happen at a higher level
            if (txt && txt !== 'Empty' && txt !== 'Delete' && !txt.match(/^🗑️/)) {
                text += txt;
            }
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            const tagName = node.tagName.toLowerCase();
            
            if (tagName === 'br') {
                text += '\n';
            } else if (tagName === 'span') {
                // Check if span is hidden
                const isHidden = node.style.display === 'none' || 
                                node.style.display === '' && 
                                window.getComputedStyle(node).display === 'none';
                
                if (!isHidden) {
                    // Recursively extract text from span
                    const spanText = extractTextFromElement(node);
                    // For AC covered spans (label and values), ensure no line breaks
                    // These are inline elements and should stay on one line
                    if (node.classList.contains('preview-ac-covered-label') || 
                        node.classList.contains('preview-ac-covered-values')) {
                        // Replace any newlines with space to keep on one line
                        text += spanText.replace(/\n+/g, ' ');
                    } else {
                        text += spanText;
                    }
                }
            } else if (tagName === 'table') {
                // Tables should already be replaced, but if we encounter one, skip it
                continue;
            } else {
                // For other elements, recursively extract text
                text += extractTextFromElement(node);
            }
        }
    }
    
    return text;
}

/**
 * Update draft from preview content
 */
function updateDraftFromPreview() {
    if (!window.currentDraft || !window.currentDraft.id) {
        alert('No draft loaded. Please load a draft first.');
        return;
    }
    
    const contentDiv = document.getElementById('draftPreviewContent');
    if (!contentDiv) return;
    
    // Extract text from preview with preserveHiddenElements=true
    // This ensures hidden elements are preserved in the original text when updating the draft
    const text = extractTextFromPreview(true);
    
    // Get assignments (unchanged)
    const assignments = getCurrentAssignments();
    const selectedSubfolder = document.getElementById('observationSubfolderSelect')?.value || null;
    
    // Get header fields
    const headerData = {
        learner: document.getElementById('headerLearner')?.value || '',
        assessor: document.getElementById('headerAssessor')?.value || '',
        visit_date: document.getElementById('headerVisitDate')?.value || '',
        location: document.getElementById('headerLocation')?.value || '',
        address: document.getElementById('headerAddress')?.value || ''
    };
    
    // Get assessor feedback
    const assessorFeedback = document.getElementById('assessorFeedback')?.value || '';
    
    // Show loading state
    const updateBtn = document.getElementById('updateDraftFromPreviewBtn');
    const originalText = updateBtn.textContent;
    updateBtn.disabled = true;
    updateBtn.textContent = '⏳ Updating...';
    
    // Update draft via API
    fetch(`/v2p-formatter/media-converter/observation-media/drafts/${window.currentDraft.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text_content: text,
            assignments: assignments,
            selected_subfolder: selectedSubfolder,
            header_data: headerData,
            assessor_feedback: assessorFeedback
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update editor with new content
                const editor = document.getElementById('observationTextEditor');
                if (editor) {
                    editor.value = text;
                }
                
                alert(`Draft updated successfully!\n\nName: ${window.currentDraft.name}`);
                closeDraftPreview();
            } else {
                alert(`Error updating draft: ${data.error || 'Unknown error'}`);
            }
        })
        .catch(error => {
            console.error('Error updating draft:', error);
            alert(`Error updating draft: ${error.message}`);
        })
        .finally(() => {
            updateBtn.disabled = false;
            updateBtn.textContent = originalText;
        });
}

/**
 * Toggle preview settings menu
 */
// togglePreviewSettings removed - settings are now always visible in the 3rd column

/**
 * Show draft preview modal
 */
function showDraftPreview() {
    try {
        const editor = document.getElementById('observationTextEditor');
        if (!editor) {
            console.error('Editor not found');
            alert('Text editor not found. Please refresh the page.');
            return;
        }

        const text = editor.value || '';
        const assignments = getCurrentAssignments();
        
        // Store original text for placeholder restoration
        previewOriginalText = text;
        previewPlaceholderMap.clear();
        
        // Generate preview HTML that mimics DOCX format
        const previewContent = generateDocxPreview(text, assignments);
        
        // Show modal
        const modal = document.getElementById('draftPreviewModal');
        const contentDiv = document.getElementById('draftPreviewContent');
        
        if (!modal) {
            console.error('Modal element not found');
            alert('Preview modal not found. Please refresh the page.');
            return;
        }
        
        if (!contentDiv) {
            console.error('Content div not found');
            alert('Preview content area not found. Please refresh the page.');
            return;
        }
        
        contentDiv.innerHTML = previewContent;
        // Make content editable
        contentDiv.contentEditable = 'true';
        contentDiv.setAttribute('contenteditable', 'true');
        
        // Apply initial display settings (header hidden by default)
        updatePreviewDisplay();
        
        // Build section navigation
        buildPreviewSectionNavigation();
        
        // Initialize undo/redo stacks with initial state
        previewUndoStack = [previewContent]; // Initial state
        previewRedoStack = [];
        updateUndoRedoButtons();
        
        // Set up change tracking with immediate save on first change
        let isFirstChange = true;
        let changeTimeout;
        
        const saveState = () => {
            savePreviewState();
            isFirstChange = false;
        };
        
        // Remove existing listeners to avoid duplicates
        const newInputHandler = () => {
            if (isFirstChange) {
                // Save immediately on first change
                saveState();
            } else {
                clearTimeout(changeTimeout);
                changeTimeout = setTimeout(() => {
                    saveState();
                }, 300); // Debounce: save state 300ms after last change
            }
        };
        
        // Remove old listener if exists
        if (contentDiv._previewInputHandler) {
            contentDiv.removeEventListener('input', contentDiv._previewInputHandler);
        }
        contentDiv._previewInputHandler = newInputHandler;
        contentDiv.addEventListener('input', newInputHandler);
        
        // Track deletions (like table removal) - save immediately
        if (contentDiv._previewObserver) {
            contentDiv._previewObserver.disconnect();
        }
        
        const observer = new MutationObserver((mutations) => {
            // Only track significant changes (not just text edits)
            const hasSignificantChange = mutations.some(m => 
                m.type === 'childList' && (m.addedNodes.length > 0 || m.removedNodes.length > 0)
            );
            
            if (hasSignificantChange) {
                // Save immediately for structural changes
                saveState();
            } else if (!isFirstChange) {
                clearTimeout(changeTimeout);
                changeTimeout = setTimeout(() => {
                    saveState();
                }, 300);
            }
        });
        contentDiv._previewObserver = observer;
        observer.observe(contentDiv, {
            childList: true,
            subtree: true,
            characterData: true
        });
        
        // Apply initial font settings
        updatePreviewDisplay();
        modal.style.display = 'flex';
    } catch (error) {
        console.error('Error showing preview:', error);
        alert('Error showing preview: ' + error.message + '\n\nPlease check the browser console for details.');
    }
}

/**
 * Close draft preview modal
 * Optionally sync edited content back to editor
 */
function closeDraftPreview() {
    const modal = document.getElementById('draftPreviewModal');
    const contentDiv = document.getElementById('draftPreviewContent');
    const editor = document.getElementById('observationTextEditor');
    
    // If content was edited, ask if user wants to sync back
    if (contentDiv && contentDiv.contentEditable === 'true' && editor) {
        // Check if content was modified (simple check - could be improved)
        const currentContent = contentDiv.innerText || contentDiv.textContent;
        const originalContent = editor.value;
        
        // For now, just close - user can manually copy if needed
        // In future, could add a "Sync changes back" button
    }
    
    if (modal) {
        modal.style.display = 'none';
    }
}

/**
 * Update preview display based on control settings
 */
function updatePreviewDisplay() {
    const contentDiv = document.getElementById('draftPreviewContent');
    if (!contentDiv) return;
    
    // Get control values
    const hideSectionTitles = document.getElementById('hideSectionTitles')?.checked || false;
    const hideAcCovered = document.getElementById('hideAcCovered')?.checked || false;
    const hideImageSuggestion = document.getElementById('hideImageSuggestion')?.checked || false;
    const hideParagraphNumbers = document.getElementById('hideParagraphNumbers')?.checked || false;
    const hideEmptyMediaFields = document.getElementById('hideEmptyMediaFields')?.checked || false;
    const trimEmptyParagraphs = document.getElementById('trimEmptyParagraphs')?.checked || false;
    const showHeader = document.getElementById('showHeader')?.checked || false;
    const showAssessorFeedback = document.getElementById('showAssessorFeedback')?.checked || false;
    const fontSize = document.getElementById('previewFontSize')?.value || '16pt';
    const fontType = document.getElementById('previewFontType')?.value || "'Times New Roman', serif";
    
    // Apply font settings
    contentDiv.style.fontSize = fontSize;
    contentDiv.style.fontFamily = fontType;
    
    // Show/hide header table
    const headerTable = contentDiv.querySelector('#previewHeaderTable');
    if (headerTable) {
        headerTable.style.display = showHeader ? 'block' : 'none';
    }
    
    // Show/hide assessor feedback table
    const assessorFeedbackTable = contentDiv.querySelector('#previewAssessorFeedback');
    if (assessorFeedbackTable) {
        assessorFeedbackTable.style.display = showAssessorFeedback ? 'block' : 'none';
        // Update feedback content from textarea
        const feedbackContent = document.getElementById('previewAssessorFeedbackContent');
        if (feedbackContent) {
            const feedback = document.getElementById('assessorFeedback')?.value || '';
            feedbackContent.textContent = feedback;
        }
    }
    
    // Show/hide section titles
    const sectionTitles = contentDiv.querySelectorAll('.preview-section-title');
    sectionTitles.forEach(el => {
        el.style.display = hideSectionTitles ? 'none' : 'block';
    });
    
    // Show/hide AC covered label only (keep values visible)
    // IMPORTANT: Only hide the label span, NOT the paragraph or values
    const acCoveredLabels = contentDiv.querySelectorAll('.preview-ac-covered-label');
    acCoveredLabels.forEach(el => {
        el.style.display = hideAcCovered ? 'none' : 'inline';
    });
    
    // Ensure the paragraph and values are always visible
    const acCoveredParagraphs = contentDiv.querySelectorAll('.preview-ac-covered');
    acCoveredParagraphs.forEach(el => {
        el.style.display = 'block'; // Always show the paragraph
    });
    
    const acCoveredValues = contentDiv.querySelectorAll('.preview-ac-covered-values');
    acCoveredValues.forEach(el => {
        el.style.display = 'inline'; // Always show the values
    });
    
    // Show/hide Image suggestion
    const imageSuggestions = contentDiv.querySelectorAll('.preview-image-suggestion');
    imageSuggestions.forEach(el => {
        el.style.display = hideImageSuggestion ? 'none' : 'block';
    });
    
    // Show/hide paragraph numbers (e.g., "1.", "2.", etc.)
    const paragraphNumbers = contentDiv.querySelectorAll('.preview-paragraph-number');
    console.log(`Found ${paragraphNumbers.length} paragraph number elements, hideParagraphNumbers=${hideParagraphNumbers}`);
    paragraphNumbers.forEach((el, index) => {
        const text = el.textContent.trim();
        el.style.display = hideParagraphNumbers ? 'none' : 'inline';
        console.log(`Paragraph ${index + 1}: text='${text}', display=${el.style.display}`);
    });
    
    // Show/hide empty media fields (empty tables)
    const emptyTables = contentDiv.querySelectorAll('.preview-empty-table');
    emptyTables.forEach(table => {
        table.style.display = hideEmptyMediaFields ? 'none' : 'table';
    });
    
    // Trim empty paragraphs: if there are 2+ consecutive empty paragraphs, reduce to 1
    // This must run AFTER all hide operations to catch paragraphs that become empty
    // Use setTimeout to ensure DOM has updated after all hide operations
    if (trimEmptyParagraphs) {
        // Force a reflow to ensure all style changes are applied
        void contentDiv.offsetHeight;
        
        // Helper function to check if an element is visible
        const isElementVisible = (el) => {
            if (!el) return false;
            // Check computed style (most reliable)
            const style = window.getComputedStyle(el);
            if (style.display === 'none' || style.visibility === 'hidden' || parseFloat(style.opacity) === 0) {
                return false;
            }
            // Check inline style as fallback
            if (el.style.display === 'none' || el.style.visibility === 'hidden') {
                return false;
            }
            return true;
        };
        
        // Helper function to check if a paragraph is empty (considering hidden elements)
        const isParagraphEmpty = (p) => {
            // First, check if paragraph itself is hidden - if so, don't process it
            if (!isElementVisible(p)) {
                return false; // Don't consider hidden paragraphs for trimming
            }
            
            // Use innerText which automatically excludes hidden elements
            // This is the most reliable way to check visible content
            const visibleText = (p.innerText || '').trim();
            const visibleTextClean = visibleText.replace(/[\u00A0\u2000-\u200B\u2028\u2029\s]/g, '');
            
            // If there's any visible text, paragraph is not empty
            if (visibleTextClean.length > 0) {
                return false;
            }
            
            // Check for visible images
            const visibleImages = Array.from(p.querySelectorAll('img')).filter(img => isElementVisible(img));
            if (visibleImages.length > 0) {
                return false;
            }
            
            // Check for visible tables
            const visibleTables = Array.from(p.querySelectorAll('table')).filter(table => isElementVisible(table));
            if (visibleTables.length > 0) {
                return false;
            }
            
            // Check for any other visible block elements with content
            const allElements = p.querySelectorAll('*');
            for (const el of allElements) {
                if (!isElementVisible(el)) continue;
                
                // Skip paragraph numbers (they're inline markers)
                if (el.classList.contains('preview-paragraph-number')) continue;
                
                // Check if element has any visible content
                const elText = (el.innerText || el.textContent || '').trim();
                const elTextClean = elText.replace(/[\u00A0\u2000-\u200B\u2028\u2029\s]/g, '');
                if (elTextClean.length > 0) {
                    return false; // Has visible content
                }
            }
            
            // Paragraph is empty (no visible content)
            return true;
        };
        
        // Function to perform trimming (iterative until no more changes)
        const performTrimming = () => {
            let iterations = 0;
            const maxIterations = 10; // Prevent infinite loops
            
            const trimOnce = () => {
                iterations++;
                if (iterations > maxIterations) {
                    console.warn('Trim empty paragraphs: max iterations reached');
                    return;
                }
                
                // Get all paragraphs in document order (fresh query each time)
                const allParagraphs = Array.from(contentDiv.querySelectorAll('p'));
                
                if (allParagraphs.length === 0) return;
                
                // Collect paragraphs to remove
                const paragraphsToRemove = [];
                
                // Find consecutive empty paragraphs
                for (let i = 0; i < allParagraphs.length; i++) {
                    if (isParagraphEmpty(allParagraphs[i])) {
                        // Found an empty paragraph, check how many consecutive empty ones follow
                        let emptyCount = 1;
                        let j = i + 1;
                        while (j < allParagraphs.length && isParagraphEmpty(allParagraphs[j])) {
                            emptyCount++;
                            j++;
                        }
                        
                        // If we have 2 or more consecutive empty paragraphs, mark all but the first for removal
                        if (emptyCount >= 2) {
                            // Mark all but the first empty paragraph for removal
                            for (let k = i + 1; k < j; k++) {
                                paragraphsToRemove.push(allParagraphs[k]);
                            }
                            // Skip the remaining empty paragraphs we've already processed
                            i = j - 1; // -1 because the loop will increment
                        }
                    }
                }
                
                // Remove the marked paragraphs (in reverse order to maintain DOM stability)
                if (paragraphsToRemove.length > 0) {
                    paragraphsToRemove.reverse().forEach(p => {
                        if (p.parentNode) {
                            p.remove();
                        }
                    });
                    
                    // Force a reflow
                    void contentDiv.offsetHeight;
                    
                    // Run trimming again to catch any new sequences
                    setTimeout(trimOnce, 0);
                }
            };
            
            // Start trimming
            trimOnce();
        };
        
        // Run trimming with a small delay to ensure all hide operations have taken effect
        setTimeout(() => {
            performTrimming();
        }, 50);
    }
}

/**
 * Delete empty table from preview (no confirmation)
 */
function deleteEmptyTable(tableId) {
    const table = document.getElementById(tableId);
    if (table) {
        // Save state for undo before deleting
        savePreviewState();
        table.remove();
    }
}

/**
 * Build section navigation list from preview content
 */
function buildPreviewSectionNavigation() {
    const contentDiv = document.getElementById('draftPreviewContent');
    const sectionsList = document.getElementById('previewSectionsList');
    
    if (!contentDiv || !sectionsList) return;
    
    // Find all section titles
    const sectionTitles = contentDiv.querySelectorAll('.preview-section-title');
    
    // Clear existing navigation
    sectionsList.innerHTML = '';
    
    if (sectionTitles.length === 0) {
        sectionsList.innerHTML = '<div style="color: #999; font-size: 12px; padding: 10px; text-align: center;">No sections found</div>';
        return;
    }
    
    // Build navigation items
    sectionTitles.forEach((titleEl, index) => {
        const sectionId = titleEl.id || `preview-section-${index + 1}`;
        const sectionText = titleEl.textContent.trim();
        
        // Extract section number and name
        const sectionMatch = sectionText.match(/SECTION\s*[:-]?\s*(\d+)\s*[:-]?\s*(.+)/i);
        const sectionNum = sectionMatch ? sectionMatch[1] : (index + 1).toString();
        const sectionName = sectionMatch ? sectionMatch[2].trim() : sectionText.replace(/^SECTION\s*[:-]?\s*/i, '').trim();
        
        // Get color for this section
        const sectionColor = SECTION_COLORS[index % SECTION_COLORS.length];
        
        // Create navigation item
        const navItem = document.createElement('div');
        navItem.className = 'preview-section-nav-item';
        navItem.style.cssText = `
            padding: 10px 12px;
            margin-bottom: 6px;
            background: #2a2a2a;
            border-left: 4px solid ${sectionColor};
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
            color: #e0e0e0;
            font-size: 13px;
        `;
        navItem.innerHTML = `
            <div style="font-weight: 600; color: ${sectionColor}; margin-bottom: 2px;">Section ${sectionNum}</div>
            <div style="font-size: 11px; color: #bbb; line-height: 1.3;">${escapeHtml(sectionName)}</div>
        `;
        
        // Add hover effect
        navItem.onmouseenter = function() {
            this.style.background = '#333';
            this.style.transform = 'translateX(2px)';
        };
        navItem.onmouseleave = function() {
            this.style.background = '#2a2a2a';
            this.style.transform = 'translateX(0)';
        };
        
        // Add click handler to scroll to section
        navItem.onclick = function() {
            scrollToPreviewSection(sectionId);
        };
        
        sectionsList.appendChild(navItem);
    });
}

/**
 * Scroll to a specific section in the preview
 */
function scrollToPreviewSection(sectionId) {
    const contentDiv = document.getElementById('draftPreviewContent');
    const sectionEl = document.getElementById(sectionId);
    
    if (!contentDiv || !sectionEl) return;
    
    // Calculate scroll position (account for any fixed headers)
    const containerRect = contentDiv.getBoundingClientRect();
    const elementRect = sectionEl.getBoundingClientRect();
    const scrollTop = contentDiv.scrollTop;
    const targetScrollTop = scrollTop + elementRect.top - containerRect.top - 20; // 20px offset from top
    
    // Smooth scroll
    contentDiv.scrollTo({
        top: targetScrollTop,
        behavior: 'smooth'
    });
    
    // Highlight the section briefly
    const originalBg = sectionEl.style.backgroundColor;
    sectionEl.style.backgroundColor = 'rgba(102, 126, 234, 0.2)';
    setTimeout(() => {
        sectionEl.style.backgroundColor = originalBg || '';
    }, 1000);
}

/**
 * Start resizing preview columns
 */
let isResizingPreview = false;
let resizeStartX = 0;
let resizeStartWidth = 0;

let isResizingPreview2 = false;
let resizeStartX2 = 0;
let resizeStartWidth2 = 0;

function startResizePreview(e) {
    e.preventDefault();
    isResizingPreview = true;
    resizeStartX = e.clientX;
    const navColumn = document.getElementById('previewSectionsNav');
    resizeStartWidth = navColumn.offsetWidth;
    
    document.addEventListener('mousemove', handleResizePreview);
    document.addEventListener('mouseup', stopResizePreview);
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
}

function handleResizePreview(e) {
    if (!isResizingPreview) return;
    
    const navColumn = document.getElementById('previewSectionsNav');
    const diff = e.clientX - resizeStartX;
    const newWidth = resizeStartWidth + diff;
    
    // Constrain width between min and max
    const minWidth = 200;
    const maxWidth = 400;
    const constrainedWidth = Math.max(minWidth, Math.min(maxWidth, newWidth));
    
    navColumn.style.width = constrainedWidth + 'px';
}

function stopResizePreview() {
    isResizingPreview = false;
    document.removeEventListener('mousemove', handleResizePreview);
    document.removeEventListener('mouseup', stopResizePreview);
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
}

function startResizePreview2(e) {
    e.preventDefault();
    isResizingPreview2 = true;
    resizeStartX2 = e.clientX;
    const settingsColumn = document.getElementById('previewSettingsColumn');
    resizeStartWidth2 = settingsColumn.offsetWidth;
    
    document.addEventListener('mousemove', handleResizePreview2);
    document.addEventListener('mouseup', stopResizePreview2);
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
}

function handleResizePreview2(e) {
    if (!isResizingPreview2) return;
    
    const settingsColumn = document.getElementById('previewSettingsColumn');
    const diff = resizeStartX2 - e.clientX; // Reverse direction (dragging left increases width)
    const newWidth = resizeStartWidth2 + diff;
    
    // Constrain width between min and max
    const minWidth = 250;
    const maxWidth = 400;
    const constrainedWidth = Math.max(minWidth, Math.min(maxWidth, newWidth));
    
    settingsColumn.style.width = constrainedWidth + 'px';
}

function stopResizePreview2() {
    isResizingPreview2 = false;
    document.removeEventListener('mousemove', handleResizePreview2);
    document.removeEventListener('mouseup', stopResizePreview2);
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
}

/**
 * Export DOCX from preview (uses preview content with hidden elements excluded)
 */
function exportObservationDocxFromPreview() {
    const contentDiv = document.getElementById('draftPreviewContent');
    if (!contentDiv) {
        alert('Preview not found. Please open the preview first.');
        return;
    }
    
    // Extract text from preview with preserveHiddenElements=false
    // This excludes hidden elements from the export
    const text = extractTextFromPreview(false);
    
    if (!text || !text.trim()) {
        alert('No content to export. Please ensure the preview has content.');
        return;
    }
    
    const assignments = getCurrentAssignments();
    
    // Get header fields
    const headerData = {
        learner: document.getElementById('headerLearner')?.value || '',
        assessor: document.getElementById('headerAssessor')?.value || '',
        visit_date: document.getElementById('headerVisitDate')?.value || '',
        location: document.getElementById('headerLocation')?.value || '',
        address: document.getElementById('headerAddress')?.value || ''
    };
    
    // Get assessor feedback
    const assessorFeedback = document.getElementById('assessorFeedback')?.value || '';
    
    // Get font settings from preview controls
    const fontSize = document.getElementById('previewFontSize')?.value || '16pt';
    const fontType = document.getElementById('previewFontType')?.value || "'Times New Roman', serif";
    
    // Extract font name from fontType (remove quotes and fallback fonts)
    // e.g., "'Times New Roman', serif" -> "Times New Roman"
    let fontName = fontType;
    if (fontType.includes("'")) {
        const match = fontType.match(/'([^']+)'/);
        if (match) {
            fontName = match[1];
        }
    } else if (fontType.includes(',')) {
        fontName = fontType.split(',')[0].trim();
    }
    
    // Extract font size number from "16pt" -> 16
    const fontSizeMatch = fontSize.match(/(\d+)/);
    const fontSizeNum = fontSizeMatch ? parseInt(fontSizeMatch[1]) : 16;
    
    // Validate - check if all placeholders are assigned
    const validation = validatePlaceholders(text, assignments);
    if (!validation.is_valid) {
        const unassigned = validation.unassigned.map(p => `{{${p}}}`).join(', ');
        if (!confirm(`Some placeholders are not assigned: ${unassigned}\n\nDo you want to export anyway?`)) {
            return;
        }
    }
    
    // Determine filename: use draft name if available, otherwise prompt user
    let filename;
    if (window.currentDraft && window.currentDraft.id && window.currentDraft.name) {
        // Use draft name as filename
        filename = window.currentDraft.name;
        // Ensure it doesn't already have .docx extension
        if (filename.toLowerCase().endsWith('.docx')) {
            filename = filename.slice(0, -5); // Remove .docx extension
        }
    } else {
        // No draft loaded, prompt user
        filename = prompt('Enter filename (without extension):', 'observation_document');
        if (!filename) return;
    }
    
    // Show loading state
    const exportBtn = document.getElementById('exportDocxFromPreviewBtn');
    const originalText = exportBtn ? exportBtn.textContent : 'Export DOCX';
    if (exportBtn) {
        exportBtn.disabled = true;
        exportBtn.textContent = '⏳ Exporting...';
    }
    
    // Export via API
    fetch('/v2p-formatter/media-converter/observation-media/export-docx', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text: text,
            assignments: assignments,
            filename: filename,
            font_size: fontSizeNum,
            font_name: fontName,
            header_data: headerData,
            assessor_feedback: assessorFeedback
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Ensure filename shows .docx extension
                let displayName = data.file_name;
                if (!displayName.toLowerCase().endsWith('.docx')) {
                    displayName += '.docx';
                }
                
                // Download file
                window.location.href = data.download_url;
                alert(`Document exported successfully!\n\nFile: ${displayName}`);
            } else {
                alert(`Error exporting document: ${data.error || 'Unknown error'}`);
            }
        })
        .catch(error => {
            console.error('Export error:', error);
            alert(`Error exporting document: ${error.message}`);
        })
        .finally(() => {
            if (exportBtn) {
                exportBtn.disabled = false;
                exportBtn.textContent = originalText;
            }
        });
}

/**
 * Format date from YYYY-MM-DD to readable format (DD Month YYYY)
 */
function formatDateForDisplay(dateString) {
    if (!dateString) return '';
    
    try {
        const date = new Date(dateString + 'T00:00:00'); // Add time to avoid timezone issues
        const months = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December'];
        const day = date.getDate();
        const month = months[date.getMonth()];
        const year = date.getFullYear();
        return `${day} ${month} ${year}`;
    } catch (e) {
        return dateString; // Return original if parsing fails
    }
}

/**
 * Generate header table HTML
 */
function generateHeaderTableHTML() {
    const learner = document.getElementById('headerLearner')?.value || '';
    const assessor = document.getElementById('headerAssessor')?.value || '';
    const visitDate = document.getElementById('headerVisitDate')?.value || '';
    const location = document.getElementById('headerLocation')?.value || '';
    const address = document.getElementById('headerAddress')?.value || '';
    
    const formattedDate = formatDateForDisplay(visitDate);
    
    return `
        <div id="previewHeaderTable" class="preview-header-container" style="margin-bottom: 20px;">
            <table class="preview-header-table">
                <tr>
                    <td>Learner</td>
                    <td>${escapeHtml(learner)}</td>
                </tr>
                <tr>
                    <td>Assessor</td>
                    <td>${escapeHtml(assessor)}</td>
                </tr>
                <tr>
                    <td>Visit Date</td>
                    <td>${escapeHtml(formattedDate)}</td>
                </tr>
                <tr>
                    <td>Location</td>
                    <td>${escapeHtml(location)}</td>
                </tr>
                <tr>
                    <td>Address</td>
                    <td>${escapeHtml(address)}</td>
                </tr>
            </table>
        </div>
    `;
}

/**
 * Generate assessor feedback table HTML
 */
function generateAssessorFeedbackHTML() {
    const feedback = document.getElementById('assessorFeedback')?.value || '';
    
    return `
        <div id="previewAssessorFeedback" class="preview-assessor-feedback-container" style="display: none; margin-top: 20px;">
            <table class="preview-assessor-feedback-table">
                <tr>
                    <td>Assessor Feedback</td>
                </tr>
                <tr>
                    <td id="previewAssessorFeedbackContent">${escapeHtml(feedback)}</td>
                </tr>
            </table>
        </div>
    `;
}

/**
 * Generate DOCX-style preview HTML
 */
function generateDocxPreview(text, assignments) {
    let html = '';
    
    // Add header table at the beginning (will be shown/hidden based on checkbox)
    html += generateHeaderTableHTML();
    
    if (!text) {
        html += '<p style="color: #999; font-style: italic;">No content to preview</p>';
    } else {
        const lines = text.split('\n');
    
    // Parse placeholders
    const placeholderPattern = /\{\{([A-Za-z0-9_]+)\}\}/g;
    
    // Patterns for elements to hide
    const sectionTitlePattern = /^SECTION\s*[:-]?\s*(.+)$/i;
    // AC covered pattern: must have colon or dash after "covered", followed by AC values
    const acCoveredPattern = /AC\s+covered\s*[:-]\s*(.+)/i;
    const imageSuggestionPattern = /Image\s+suggestion\s*[:-]?\s*(.+)/i;
    
    for (let line of lines) {
        if (!line.trim()) {
            html += '<p>&nbsp;</p>';
            continue;
        }
        
        // Check if line is a section title
        const sectionMatch = line.match(sectionTitlePattern);
        if (sectionMatch) {
            // Extract section number and title
            const sectionTitle = sectionMatch[1].trim();
            // Create a unique ID for the section (use section number if available, otherwise use title)
            const sectionNumMatch = line.match(/SECTION\s*[:-]?\s*(\d+)/i);
            const sectionNum = sectionNumMatch ? sectionNumMatch[1] : (html.match(/preview-section-/g) || []).length + 1;
            const sectionId = `preview-section-${sectionNum}`;
            // Get color for this section
            const sectionIndex = (html.match(/preview-section-/g) || []).length;
            const sectionColor = SECTION_COLORS[sectionIndex % SECTION_COLORS.length];
            html += `<p id="${sectionId}" class="preview-section-title" style="font-weight: bold; font-size: 14pt; margin: 15px 0 10px 0; color: ${sectionColor}; border-left: 4px solid ${sectionColor}; padding-left: 10px;">${escapeHtml(line)}</p>`;
            continue;
        }
        
        // Check if line contains AC covered
        const acMatch = line.match(acCoveredPattern);
        if (acMatch) {
            // Split line: hide only "AC covered:" label, keep AC values
            // Match pattern: /AC\s+covered\s*[:-]?\s*(.+)/i
            // acMatch[0] = full match (e.g., "AC covered: AC1, AC2")
            // acMatch[1] = captured group (the AC values part - what comes after the label)
            const matchIndex = acMatch.index;
            const fullMatch = acMatch[0];
            // Extract just the label part: "AC covered" + optional colon/dash + optional whitespace
            const labelMatch = fullMatch.match(/^(AC\s+covered\s*[:-]?\s*)/i);
            const labelText = labelMatch ? labelMatch[1] : 'AC covered: ';
            // Get the AC values (everything after the label)
            const acValues = acMatch[1] || line.substring(matchIndex + labelText.length).trim();
            
            html += `<p class="preview-ac-covered" style="color: #999; font-style: italic; margin: 0;">
                <span class="preview-ac-covered-label">${escapeHtml(labelText)}</span>
                <span class="preview-ac-covered-values">${escapeHtml(acValues)}</span>
            </p>`;
            continue;
        }
        
        // Check if line contains Image suggestion
        const imgSuggestionMatch = line.match(imageSuggestionPattern);
        if (imgSuggestionMatch) {
            html += `<p class="preview-image-suggestion" style="color: #666; font-style: italic; margin: 5px 0;">${escapeHtml(line)}</p>`;
            continue;
        }
        
        // Check if line contains placeholders
        const matches = [...line.matchAll(placeholderPattern)];
        
        if (matches.length > 0) {
            // Process line with placeholders
            let lastIndex = 0;
            let lineHtml = '';
            
            for (const match of matches) {
                // Add text before placeholder
                if (match.index > lastIndex) {
                    const textSegment = line.substring(lastIndex, match.index);
                    lineHtml += escapeHtml(textSegment).replace(/\n/g, '<br>');
                }
                
                // Add table for placeholder (outside paragraph, as a sibling)
                const placeholderKey = match[1].toLowerCase();
                const placeholderName = match[0]; // e.g., "{{Image1}}"
                const assignedMedia = assignments[placeholderKey] || [];
                
                // Store placeholder name for later restoration
                const tableHtml = generateDocxTablePreview(assignedMedia, placeholderKey);
                lineHtml += tableHtml;
                
                lastIndex = match.index + match[0].length;
            }
            
            // Add remaining text
            if (lastIndex < line.length) {
                const textSegment = line.substring(lastIndex);
                lineHtml += escapeHtml(textSegment).replace(/\n/g, '<br>');
            }
            
            // Wrap in paragraph if there's text, otherwise just output the tables
            if (lineHtml.trim()) {
                html += '<p style="color: #e0e0e0;">' + lineHtml + '</p>';
            } else {
                html += lineHtml;
            }
        } else {
            // Regular text line (dark theme)
            // Check for paragraph numbers (e.g., "1.", "2.", "10.", etc.)
            // Pattern 1: Number on same line as text: "1. Text here"
            // Pattern 2: Number on its own line: "1." (followed by empty lines and then text)
            const paragraphNumberPattern = /^(\d+\.)\s*(.*)$/;
            const paraMatch = line.match(paragraphNumberPattern);
            
            if (paraMatch) {
                const paraNumber = paraMatch[1]; // e.g., "1."
                const paraText = paraMatch[2]; // e.g., "Text here" or empty
                
                if (paraText.trim()) {
                    // Number and text on same line: "1. Text here"
                    html += `<p style="color: #e0e0e0;">
                        <span class="preview-paragraph-number">${escapeHtml(paraNumber + ' ')}</span>
                        ${escapeHtml(paraText).replace(/\n/g, '<br>')}
                    </p>`;
                } else {
                    // Number on its own line: "1."
                    html += `<p style="color: #e0e0e0;">
                        <span class="preview-paragraph-number">${escapeHtml(paraNumber)}</span>
                    </p>`;
                }
            } else {
                // Regular line without paragraph number
                html += '<p style="color: #e0e0e0;">' + escapeHtml(line).replace(/\n/g, '<br>') + '</p>';
            }
        }
    }
    
    // Add assessor feedback table at the end (will be shown/hidden based on checkbox)
    html += generateAssessorFeedbackHTML();
    
    return html;
}

/**
 * Generate DOCX-style table preview (2 columns)
 */
function generateDocxTablePreview(mediaList, placeholderKey) {
    // Construct placeholder name from key (e.g., "image1" -> "{{Image1}}")
    const placeholderName = `{{${placeholderKey.charAt(0).toUpperCase() + placeholderKey.slice(1)}}}`;
    
    if (!mediaList || mediaList.length === 0) {
        // Empty table with delete icon (dark theme)
        const tableId = `empty-table-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        // Store mapping
        previewPlaceholderMap.set(tableId, placeholderName);
        return `
            <table class="preview-empty-table preview-placeholder-table" data-placeholder="${escapeHtml(placeholderKey)}" data-placeholder-name="${escapeHtml(placeholderName)}" id="${tableId}" style="width: 100%; border-collapse: collapse; border: 1px solid #555; margin: 10px 0; position: relative;">
                <tr>
                    <td style="width: 50%; border: 1px solid #555; padding: 10px; vertical-align: middle; text-align: center; min-height: 100px; background: #2a2a2a; position: relative;">
                        <span style="color: #999; font-style: italic;">Empty</span>
                    </td>
                    <td style="width: 50%; border: 1px solid #555; padding: 10px; vertical-align: middle; text-align: center; min-height: 100px; background: #2a2a2a; position: relative;">
                        <span style="color: #999; font-style: italic;">Empty</span>
                    </td>
                </tr>
                <tr>
                    <td colspan="2" style="text-align: right; padding: 5px 10px; background: #2a2a2a; border-top: 1px solid #555;">
                        <button onclick="deleteEmptyTable('${tableId}')" style="background: #ff6b6b; color: white; border: none; border-radius: 4px; padding: 4px 8px; cursor: pointer; font-size: 11px; display: inline-flex; align-items: center; gap: 4px;" title="Delete empty table">
                            🗑️ Delete
                        </button>
                    </td>
                </tr>
            </table>
        `;
    }
    
    // Calculate number of rows needed
    const numRows = Math.ceil(mediaList.length / 2);
    const tableId = `media-table-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    // Store mapping
    previewPlaceholderMap.set(tableId, placeholderName);
    let tableHtml = `
        <table class="preview-placeholder-table" data-placeholder="${escapeHtml(placeholderKey)}" data-placeholder-name="${escapeHtml(placeholderName)}" id="${tableId}" style="width: 100%; border-collapse: collapse; border: 1px solid #555; margin: 10px 0;">
    `;
    
    for (let row = 0; row < numRows; row++) {
        tableHtml += '<tr>';
        
        for (let col = 0; col < 2; col++) {
            const index = row * 2 + col;
            const media = mediaList[index];
            
            tableHtml += '<td style="width: 50%; border: 1px solid #555; padding: 10px; vertical-align: middle; text-align: center; min-height: 150px; background: #2a2a2a;">';
            
            if (media) {
                if (media.type === 'image') {
                    // Show image thumbnail
                    const imagePath = media.path;
                    const imageName = media.name || 'Image';
                    
                    // Try to get thumbnail URL
                    const sizeStr = '240x180';
                    const thumbnailUrl = `/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(imagePath)}&size=${sizeStr}`;
                    
                    tableHtml += `
                        <div style="margin: 0 auto;">
                            <img src="${thumbnailUrl}" 
                                 alt="${escapeHtml(imageName)}" 
                                 style="max-width: 100%; max-height: 250px; object-fit: contain; border: 1px solid #555; display: block;"
                                 onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                            <div style="display: none; color: #999; font-size: 11px; margin-top: 10px;">
                                ${escapeHtml(imageName)}
                            </div>
                        </div>
                    `;
                } else if (media.type === 'video' || media.type === 'audio' || media.type === 'document') {
                    // Video, Audio, or PDF - show filename
                    const mediaLabel = media.type === 'audio' ? 'Audio' : media.type === 'document' ? 'PDF' : 'Video';
                    tableHtml += `<div style="color: #999; font-size: 11px;">${escapeHtml(media.name || mediaLabel)}</div>`;
                }
            } else {
                // Empty cell
                tableHtml += '<span style="color: #666;">&nbsp;</span>';
            }
            
            tableHtml += '</td>';
        }
        
        tableHtml += '</tr>';
    }
    
    tableHtml += '</table>';
    return tableHtml;
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
        
        // Check if section has assigned media - if so, expand it (especially during reshuffle)
        const sectionPlaceholders = extractPlaceholders(section.content);
        const hasAssignedMedia = sectionPlaceholders.some(placeholder => {
            const placeholderKey = placeholder.toLowerCase();
            return assignments[placeholderKey] && assignments[placeholderKey].length > 0;
        });
        
        // Use stored expanded state if available, otherwise use hasAssignedMedia
        const storedState = window.dialogSectionExpandedState && window.dialogSectionExpandedState[section.id];
        const isExpanded = storedState !== undefined ? storedState : (hasAssignedMedia || dialogReshuffleMode);
        const displayStyle = isExpanded ? 'display: block !important;' : 'display: none;';
        const icon = isExpanded ? '▼' : '▶';
        // During reshuffle mode, disable toggle for sections with assigned media
        const toggleHandler = (dialogReshuffleMode && hasAssignedMedia) ? 'return false;' : `toggleDialogSection('${section.id}')`;
        
        // Update stored state
        if (!window.dialogSectionExpandedState) {
            window.dialogSectionExpandedState = {};
        }
        if (isExpanded) {
            window.dialogSectionExpandedState[section.id] = true;
        }

        // Count media items in this section
        const mediaCount = countMediaInSection(section, assignments);
        const mediaCountBadge = mediaCount > 0 
            ? `<span class="section-media-count" style="background: ${section.color}30; border: 1px solid ${section.color}; color: ${section.color}; padding: 3px 6px; border-radius: 4px; font-size: 11px; font-weight: normal; white-space: nowrap; margin-right: 8px;">${mediaCount} media</span>`
            : `<span class="section-media-count zero-media" style="background: rgba(153, 153, 153, 0.2); border: 1px solid #666; color: #999; padding: 3px 6px; border-radius: 4px; font-size: 11px; font-weight: normal; white-space: nowrap; margin-right: 8px;">0 media</span>`;

        html += `
            <div class="dialog-section" style="margin-bottom: 15px; border-left: 3px solid ${section.color};">
                <div class="dialog-section-header" 
                     onclick="${toggleHandler}"
                     style="padding: 8px 10px; background: ${section.color}20; border: 1px solid ${section.color}; border-radius: 4px; cursor: ${(dialogReshuffleMode && hasAssignedMedia) ? 'default' : 'pointer'}; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="color: ${section.color}; font-weight: bold; font-size: 13px;">${escapeHtml(section.title)}</span>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        ${mediaCountBadge}
                        <span class="dialog-section-icon" style="color: ${section.color}; font-size: 12px;">${icon}</span>
                    </div>
                </div>
                <div class="dialog-section-content" data-section-id="${section.id}" style="padding-left: 10px; ${displayStyle}">
                    ${sectionContent}
                </div>
            </div>
        `;
    });

    return html;
}

// Export to window immediately so it's available for showPlaceholderSelectionDialog
if (typeof window !== 'undefined') {
    window.renderSectionsForDialog = renderSectionsForDialog;
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
        const placeholderKey = placeholder.toLowerCase();
        const assignedMedia = assignments[placeholderKey] || [];
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

// Export to window immediately
if (typeof window !== 'undefined') {
    window.renderSectionContentForDialog = renderSectionContentForDialog;
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
        const placeholderKey = placeholder.toLowerCase();
        const assignedMedia = assignments[placeholderKey] || [];

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
 * Count total media items assigned to all placeholders in a section
 */
function countMediaInSection(section, assignments) {
    // Extract placeholders from section content
    const sectionPlaceholders = extractPlaceholders(section.content);
    
    // Count media items assigned to all placeholders in this section
    let totalCount = 0;
    sectionPlaceholders.forEach(placeholder => {
        const placeholderKey = placeholder.toLowerCase();
        if (assignments[placeholderKey]) {
            totalCount += assignments[placeholderKey].length;
        }
    });
    
    return totalCount;
}

/**
 * Find which placeholder a media item is assigned to
 */
function findPlaceholderForMedia(mediaPath, assignments) {
    for (const placeholder in assignments) {
        if (assignments[placeholder].some(m => m.path === mediaPath)) {
            return placeholder;
        }
    }
    return null;
}

/**
 * Get section color for a placeholder
 */
function getSectionColorForPlaceholder(placeholder, text) {
    if (!text || !placeholder) return null;
    
    const sectionData = parseSections(text);
    if (!sectionData.hasSections) return null;
    
    // Find which section contains this placeholder
    for (const section of sectionData.sections) {
        const sectionPlaceholders = extractPlaceholders(section.content);
        if (sectionPlaceholders.some(p => p.toLowerCase() === placeholder.toLowerCase())) {
            return section.color;
        }
    }
    
    return null;
}

/**
 * Get section color for a media item (based on which placeholder it's assigned to)
 */
function getSectionColorForMedia(mediaPath, assignments, text) {
    const placeholder = findPlaceholderForMedia(mediaPath, assignments);
    if (!placeholder) return null;
    
    return getSectionColorForPlaceholder(placeholder, text);
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
        // If reshuffle mode is active, expand sections with assigned media
        let isExpanded = states[section.id] === true;
        if (reshuffleMode) {
            const sectionPlaceholders = extractPlaceholders(section.content);
            const hasAssignedMedia = sectionPlaceholders.some(placeholder => {
                const placeholderKey = placeholder.toLowerCase();
                return assignments[placeholderKey] && assignments[placeholderKey].length > 0;
            });
            if (hasAssignedMedia) {
                isExpanded = true;
                states[section.id] = true; // Save the state
            }
        }
        const sectionContent = renderSectionContent(section.content, placeholders, colorMap, assignments, validation);

        // Count media items in this section
        const mediaCount = countMediaInSection(section, assignments);
        const mediaCountBadge = mediaCount > 0 
            ? `<span class="section-media-count" style="background: ${section.color}30; border: 1px solid ${section.color}; color: ${section.color}; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: normal; white-space: nowrap; margin-right: 10px;">${mediaCount} media</span>`
            : `<span class="section-media-count zero-media" style="background: rgba(153, 153, 153, 0.2); border: 1px solid #666; color: #999; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: normal; white-space: nowrap; margin-right: 10px;">0 media</span>`;

        // Force display style for expanded sections, especially during reshuffle
        const contentStyle = isExpanded ? 
            `border: 1px solid ${section.color}30; display: block !important;` : 
            `border: 1px solid ${section.color}30; display: none;`;
        
        html += `
            <div class="observation-section ${isExpanded ? '' : 'collapsed'}" data-section-id="${section.id}" style="border-left: 3px solid ${section.color};">
                <div class="observation-section-header" onclick="toggleSection('${section.id}')" 
                     style="background: ${section.color}20; border: 1px solid ${section.color}; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: ${section.color}; font-weight: bold; font-size: 16px;">${escapeHtml(section.title)}</span>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        ${mediaCountBadge}
                        <span class="observation-section-icon" style="color: ${section.color}; font-size: 16px;">${isExpanded ? '▼' : '▶'}</span>
                    </div>
                </div>
                <div class="observation-section-content" style="${contentStyle}">
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

    // If reshuffle mode is active, ensure sections with assigned media remain expanded
    if (reshuffleMode && sectionData.hasSections) {
        const states = getSectionStates();
        sectionData.sections.forEach(section => {
            const sectionPlaceholders = extractPlaceholders(section.content);
            const hasAssignedMedia = sectionPlaceholders.some(placeholder => {
                const placeholderKey = placeholder.toLowerCase();
                return assignments[placeholderKey] && assignments[placeholderKey].length > 0;
            });
            if (hasAssignedMedia) {
                states[section.id] = true;
            }
        });
        saveSectionStates(states);
    }

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

    // Reshuffle is now always enabled by default - no button needed
}

/**
 * Toggle reshuffle mode (enable/disable drag-and-drop reordering)
 */
let reshuffleMode = true; // Always enabled by default
window.reshuffleMode = true; // Make it accessible globally
function toggleReshuffleMode() {
    console.log('[RESHUFFLE] ========== toggleReshuffleMode CALLED ==========');
    console.log('[RESHUFFLE] Current reshuffleMode:', reshuffleMode);
    reshuffleMode = !reshuffleMode;
    window.reshuffleMode = reshuffleMode; // Update global reference
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

        // Expand all sections that have assigned media to make reshuffling easier
        const assignments = getCurrentAssignments();
        const textEditor = document.getElementById('observationTextEditor');
        const text = textEditor ? textEditor.value : '';
        const sectionData = parseSections(text);
        
        if (sectionData.hasSections) {
            const states = getSectionStates();
            let expandedCount = 0;
            
            sectionData.sections.forEach(section => {
                // Check if this section has any assigned media
                const sectionPlaceholders = extractPlaceholders(section.content);
                const hasAssignedMedia = sectionPlaceholders.some(placeholder => {
                    const placeholderKey = placeholder.toLowerCase();
                    return assignments[placeholderKey] && assignments[placeholderKey].length > 0;
                });
                
                if (hasAssignedMedia) {
                    states[section.id] = true;
                    expandedCount++;
                    
                    // Also expand in DOM if section exists
                    const sectionEl = document.querySelector(`[data-section-id="${section.id}"]`);
                    if (sectionEl) {
                        sectionEl.classList.remove('collapsed');
                        const contentEl = sectionEl.querySelector('.observation-section-content');
                        const iconEl = sectionEl.querySelector('.observation-section-icon');
                        if (contentEl) {
                            contentEl.style.display = 'block';
                        }
                        if (iconEl) iconEl.textContent = '▼';
                    }
                }
            });
            
            saveSectionStates(states);
            console.log('[RESHUFFLE] Expanded', expandedCount, 'sections with assigned media');
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
        
        // Refresh preview to ensure all cells have proper drag handlers
        if (typeof window !== 'undefined' && typeof window.updatePreview === 'function') {
            window.updatePreview();
        } else if (typeof updatePreview === 'function') {
            updatePreview();
        }
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
function generateMediaTable(mediaList, placeholder, thumbnailSize = null) {
    // If in dialog context, use smaller thumbnails (50% of default)
    const isDialog = window.currentPlaceholderDialog !== undefined && window.currentPlaceholderDialog !== null;
    const thumbSize = thumbnailSize || (isDialog ? '200x150' : '400x300');
    
    if (mediaList.length === 0) {
        return `<table class="placeholder-table" 
                       style="border: 1px solid #000; border-collapse: collapse; width: 100%; margin: 10px 0;"
                       data-placeholder="${placeholder}">
            <tr>
                <td class="media-cell" style="border: 1px solid #000; padding: 10px; min-height: 50px;"
                          data-media-index="0"
                          data-placeholder="${placeholder}"
                          ondrop="if(typeof window.handleTableDrop === 'function') { window.handleTableDrop(event, '${placeholder}'); }" 
                          ondragover="if(typeof window.handleTableDragOver === 'function') { window.handleTableDragOver(event); }"></td>
                <td class="media-cell" style="border: 1px solid #000; padding: 10px; min-height: 50px;"
                          data-media-index="1"
                          data-placeholder="${placeholder}"
                          ondrop="if(typeof window.handleTableDrop === 'function') { window.handleTableDrop(event, '${placeholder}'); }" 
                          ondragover="if(typeof window.handleTableDragOver === 'function') { window.handleTableDragOver(event); }"></td>
            </tr>
        </table>`;
    }

    let tableHtml = `<table class="placeholder-table" 
                            style="border: 1px solid #000; border-collapse: collapse; width: 100%; margin: 10px 0;"
                            data-placeholder="${placeholder}">
        <tbody>`;

    // Define delete button style and icon based on dialog context
    // Always show delete button in dialog, hide in main preview
    const deleteBtnStyle = isDialog 
        ? `position: absolute !important; top: 5px !important; right: 5px !important; background: #ff6b6b !important; color: white !important; border: none !important; border-radius: 4px !important; width: 28px !important; height: 28px !important; cursor: pointer !important; font-size: 16px !important; display: flex !important; align-items: center !important; justify-content: center !important; z-index: 100 !important; box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important; opacity: 1 !important; visibility: visible !important;`
        : `position: absolute; top: 5px; right: 5px; background: #ff6b6b; color: white; border: none; border-radius: 50%; width: 24px; height: 24px; cursor: pointer; font-size: 14px; display: none;`;
    const deleteIcon = isDialog ? '🗑️' : '×';

    // Generate rows (2 columns per row)
    for (let i = 0; i < mediaList.length; i += 2) {
        tableHtml += '<tr>';

        // Column 1
        const hasMedia1 = mediaList[i] !== undefined && mediaList[i] !== null;
        tableHtml += `<td class="media-cell" 
                          style="border: 1px solid #000; padding: 10px; width: 50%; position: relative;${hasMedia1 ? ' cursor: grab;' : ''}"
                          data-media-index="${i}"
                          data-placeholder="${placeholder}"
                          ondrop="if(typeof window.handleTableDrop === 'function') { window.handleTableDrop(event, '${placeholder}'); }" 
                          ondragover="if(typeof window.handleTableDragOver === 'function') { window.handleTableDragOver(event); }"
                          draggable="${hasMedia1 ? 'true' : 'false'}"
                          ondragstart="${hasMedia1 ? `if(typeof window.handleTableCellDragStart === 'function') { window.handleTableCellDragStart(event, ${i}, '${placeholder}'); }` : ''}"
                          onclick="handleTableCellClick(event, ${i}, '${placeholder}')"
                          ${hasMedia1 ? `title="Drag to reorder media"` : ''}>`;
        if (mediaList[i]) {
            if (mediaList[i].type === 'image') {
                tableHtml += `<img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(mediaList[i].path)}&size=${thumbSize}" 
                                   style="max-width: 100%; height: auto;" 
                                   alt="${mediaList[i].name}">`;
            } else {
                tableHtml += `<div style="padding: 10px; text-align: center; color: #e0e0e0;">${mediaList[i].name}</div>`;
            }
            tableHtml += `<button class="remove-media-btn dialog-delete-btn" 
                                   onclick="removeMediaFromTable(${i}, '${placeholder}'); event.stopPropagation();"
                                   style="${deleteBtnStyle}"
                                   title="Remove media">${deleteIcon}</button>`;
        }
        tableHtml += '</td>';

        // Column 2
        tableHtml += `<td class="media-cell" 
                          style="border: 1px solid #000; padding: 10px; width: 50%; position: relative;${mediaList[i + 1] ? ' cursor: grab;' : ''}"
                          data-media-index="${i + 1}"
                          data-placeholder="${placeholder}"
                          ondrop="if(typeof window.handleTableDrop === 'function') { window.handleTableDrop(event, '${placeholder}'); }" 
                          ondragover="if(typeof window.handleTableDragOver === 'function') { window.handleTableDragOver(event); }"
                          draggable="${mediaList[i + 1] ? 'true' : 'false'}"
                          ondragstart="${mediaList[i + 1] ? `if(typeof window.handleTableCellDragStart === 'function') { window.handleTableCellDragStart(event, ${i + 1}, '${placeholder}'); }` : ''}"
                          onclick="handleTableCellClick(event, ${i + 1}, '${placeholder}')"
                          ${mediaList[i + 1] ? `title="Drag to reorder media"` : ''}>`;
        if (mediaList[i + 1]) {
            if (mediaList[i + 1].type === 'image') {
                tableHtml += `<img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(mediaList[i + 1].path)}&size=${thumbSize}" 
                                   style="max-width: 100%; height: auto;" 
                                   alt="${mediaList[i + 1].name}">`;
            } else {
                tableHtml += `<div style="padding: 10px; text-align: center; color: #e0e0e0;">${mediaList[i + 1].name}</div>`;
            }
            tableHtml += `<button class="remove-media-btn dialog-delete-btn" 
                                   onclick="removeMediaFromTable(${i + 1}, '${placeholder}'); event.stopPropagation();"
                                   style="${deleteBtnStyle}"
                                   title="Remove media">${deleteIcon}</button>`;
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
                          ondrop="if(typeof window.handleTableDrop === 'function') { window.handleTableDrop(event, '${placeholder}'); }" 
                          ondragover="if(typeof window.handleTableDragOver === 'function') { window.handleTableDragOver(event); }">
                          <div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">Drop media here</div>
                      </td>`;
        tableHtml += `<td class="media-cell" 
                          style="border: 1px solid #000; padding: 10px; min-height: 50px; width: 50%; position: relative;"
                          data-media-index="${mediaList.length + 1}"
                          data-placeholder="${placeholder}"
                          ondrop="if(typeof window.handleTableDrop === 'function') { window.handleTableDrop(event, '${placeholder}'); }" 
                          ondragover="if(typeof window.handleTableDragOver === 'function') { window.handleTableDragOver(event); }">
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
    const isDialog = window.currentPlaceholderDialog !== undefined && window.currentPlaceholderDialog !== null;
    const cells = document.querySelectorAll('.media-cell');
    cells.forEach(cell => {
        cell.addEventListener('mouseenter', function () {
            const removeBtn = this.querySelector('.remove-media-btn');
            if (removeBtn && this.querySelector('img, div')) {
                // In dialog, button is always visible, so don't change it
                if (!isDialog) {
                    removeBtn.style.display = 'block';
                }
            }
        });
        cell.addEventListener('mouseleave', function () {
            const removeBtn = this.querySelector('.remove-media-btn');
            if (removeBtn) {
                // In dialog, keep button visible; only hide in main preview
                if (!isDialog) {
                    removeBtn.style.display = 'none';
                }
            }
        });
    });
}

/**
 * Handle table cell drag start (for reordering)
 */
function handleTableCellDragStart(e, mediaIndex, placeholder) {
    console.log('[RESHUFFLE] Drag start', { mediaIndex, placeholder });
    const assignments = getCurrentAssignments();
    const placeholderKey = placeholder.toLowerCase();
    const media = assignments[placeholderKey] && assignments[placeholderKey][mediaIndex];
    if (media) {
        const dragData = {
            ...media,
            source: 'table',
            placeholder: placeholder,
            index: mediaIndex
        };
        console.log('[RESHUFFLE] Setting drag data', dragData);
        e.dataTransfer.setData('application/json', JSON.stringify(dragData));
        e.dataTransfer.setData('text/plain', mediaIndex.toString()); // Fallback for Playwright
        e.dataTransfer.effectAllowed = 'move';
        
        // Mark cell as dragging for fallback detection
        const dragElement = e.currentTarget;
        if (dragElement) {
            dragElement.classList.add('dragging');
            setTimeout(() => {
                // Check if element still exists in DOM before removing class
                if (dragElement && dragElement.parentNode) {
                    dragElement.classList.remove('dragging');
                }
            }, 1000);
        }
    } else {
        console.error('[RESHUFFLE] No media found at index', mediaIndex, 'for placeholder', placeholder);
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
    console.log('[DROP] handleTableDrop ENTRY', { placeholder, hasEvent: !!e, hasDataTransfer: !!e?.dataTransfer });
    
    e.preventDefault();
    e.stopPropagation();
    
    // Get data to check if this is a reshuffle
    let dataStr = '';
    try {
        dataStr = e.dataTransfer ? e.dataTransfer.getData('application/json') : '';
    } catch (err) {
        console.warn('[DROP] Error getting dataTransfer data:', err);
    }
    
    // Check if this is a reshuffle operation
    if (dataStr) {
        try {
            const data = JSON.parse(dataStr);
            // If it's a reshuffle (source === 'table'), let reshuffle.js handle it
            if (data.source === 'table' && data.placeholder && data.index !== undefined) {
                console.log('[DROP] Detected reshuffle operation, delegating to reshuffle.js');
                // Call reshuffle function directly if available
                if (typeof window._reshuffleHandleTableDrop === 'function') {
                    const result = window._reshuffleHandleTableDrop(e, placeholder);
                    if (result === true) {
                        console.log('[DROP] Reshuffle handled successfully');
                        return; // Reshuffle handled
                    }
                } else if (typeof window.reorderMedia === 'function') {
                    // Fallback: use reorderMedia directly
                    const targetCell = (e.target && e.target.closest) ? e.target.closest('.media-cell') || e.target.closest('td') : null;
                    if (targetCell) {
                        const targetIndex = parseInt(targetCell.dataset?.mediaIndex);
                        if (!isNaN(targetIndex)) {
                            console.log('[DROP] Calling reshuffle reorderMedia directly');
                            const success = window.reorderMedia(placeholder, data.index, targetIndex);
                            if (success) {
                                return; // Reshuffle handled
                            }
                        }
                    }
                }
            }
        } catch (err) {
            console.warn('[DROP] Error parsing drop data:', err);
            // Continue with normal handling
        }
    }
    
    // Not a reshuffle - handle as normal drop (media browser drop, etc.)
    console.log('[DROP] Handling as normal drop (not reshuffle)');
    
    const targetInfo = e.target ? { tagName: e.target.tagName, className: e.target.className } : { tagName: 'null', className: 'null' };
    console.log('[DROP] handleTableDrop called', { placeholder, target: targetInfo });

    try {
        // Try to get data from dataTransfer
        let dataStr = '';
        try {
            dataStr = e.dataTransfer ? e.dataTransfer.getData('application/json') : '';
        } catch (err) {
            console.warn('[DROP] Error getting dataTransfer data:', err);
        }
        
        console.log('[DROP] DataTransfer data:', dataStr ? 'found' : 'empty', dataStr ? dataStr.substring(0, 100) : '');
        
        // If no data in dataTransfer, try fallback methods
        if (!dataStr || dataStr === '') {
            // Try text/plain as fallback
            try {
                dataStr = e.dataTransfer ? e.dataTransfer.getData('text/plain') : '';
                if (dataStr) {
                    console.log('[DROP] Got data from text/plain fallback');
                }
            } catch (err) {
                console.warn('[DROP] Error getting text/plain:', err);
            }
            
            // Try to get from window.lastDragData (set by media browser)
            if ((!dataStr || dataStr === '') && window.lastDragData) {
                console.log('[DROP] Using window.lastDragData fallback');
                dataStr = JSON.stringify(window.lastDragData);
                window.lastDragData = null; // Clear after use
            }
            
            if (!dataStr || dataStr === '') {
                console.warn('[DROP] No dataTransfer data - cannot process drop');
                return;
            }
        }
        
        let data;
        try {
            data = JSON.parse(dataStr);
        } catch (err) {
            console.warn('[DROP] Failed to parse dataTransfer data:', err);
            return;
        }
        
        if (!data) {
            console.warn('[DROP] Parsed data is null/undefined');
            return;
        }
        
        console.log('[DROP] Parsed data:', { hasPath: !!data.path, hasName: !!data.name, source: data.source });
        
        // If placeholder not provided as parameter, try to get from target element
        if (!placeholder) {
            const targetElement = (e.target && e.target.closest) ? 
                                 (e.target.closest('[data-placeholder]') || 
                                  e.target.closest('.unassigned-placeholder-container') ||
                                  e.target.closest('.placeholder-table')) : null;
            if (targetElement) {
                placeholder = targetElement.dataset.placeholder || 
                            (targetElement.closest && targetElement.closest('[data-placeholder]')?.dataset.placeholder);
                console.log('[DROP] Got placeholder from target element:', placeholder);
            }
        }
        
        // If still no placeholder, try to extract from the ondrop attribute
        if (!placeholder && e.currentTarget) {
            const ondropAttr = e.currentTarget.getAttribute('ondrop');
            if (ondropAttr) {
                const match = ondropAttr.match(/handleTableDrop\([^,]+,\s*['"]([^'"]+)['"]/);
                if (match) {
                    placeholder = match[1];
                    console.log('[DROP] Got placeholder from ondrop attribute:', placeholder);
                }
            }
        }
        
        if (!placeholder) {
            console.error('[DROP] No placeholder specified and could not determine from target');
            alert('Error: Could not determine placeholder for drop. Please try clicking the placeholder to assign media.');
            return;
        }

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
            if (typeof window !== 'undefined' && typeof window.updatePreview === 'function') {
                try {
                    window.updatePreview();
                } catch (e) {
                    console.error('Error calling updatePreview:', e);
                }
            }

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
            console.log('[DROP] Reordering within table', { placeholder, fromIndex: data.index, draggedPlaceholder: data.placeholder });
            
            // Verify placeholder matches (case-insensitive)
            const draggedPlaceholderKey = (data.placeholder || '').toLowerCase();
            const targetPlaceholderKey = placeholder.toLowerCase();
            
            if (draggedPlaceholderKey !== targetPlaceholderKey) {
                console.warn('[DROP] Placeholder mismatch - cannot reorder across placeholders', { 
                    dragged: draggedPlaceholderKey, 
                    target: targetPlaceholderKey 
                });
                return;
            }
            
            const targetCell = e.target.closest('.media-cell') || e.target.closest('td');
            if (targetCell) {
                console.log('[DROP] Target cell found', { 
                    targetIndex: targetCell.dataset.mediaIndex,
                    placeholder: targetCell.dataset.placeholder 
                });
                
                // Use standalone reshuffle function if available
                const targetIndex = parseInt(targetCell.dataset.mediaIndex);
                if (!isNaN(targetIndex) && typeof window.reorderMedia === 'function') {
                    console.log('[DROP] Using standalone reorderMedia function');
                    const success = window.reorderMedia(placeholder, data.index, targetIndex);
                    if (success) {
                        console.log('[DROP] Reshuffle successful');
                    } else {
                        console.warn('[DROP] Reshuffle failed');
                    }
                } else if (typeof reorderMediaInPlaceholder === 'function') {
                    // Fallback to old function
                    reorderMediaInPlaceholder(placeholder, data.index, targetCell);
                } else {
                    console.error('[DROP] No reshuffle function available');
                }
            } else {
                console.error('[DROP] Target cell not found for drop', { 
                    target: e.target.tagName, 
                    targetClass: e.target.className 
                });
            }
        } else if (data.path && data.name) {
            // Adding new media from grid (has path and name, but no source field)
            console.log('[DROP] Adding media from grid to placeholder', { placeholder, mediaName: data.name });
            
            // Check if dropping on a specific cell (with data-media-index)
            const targetCell = e.target.closest('.media-cell') || e.target.closest('td');
            let targetIndex = null;

            if (targetCell && targetCell.dataset.mediaIndex !== undefined) {
                targetIndex = parseInt(targetCell.dataset.mediaIndex);
                console.log('[DROP] Dropping on specific cell, targetIndex:', targetIndex);
            } else {
                console.log('[DROP] Dropping on empty placeholder table, will append');
            }

            const result = assignMediaToPlaceholder(placeholder, data, targetIndex);
            console.log('[DROP] Assignment result:', result);
            
            // Update preview to show the new assignment
            if (typeof window !== 'undefined' && typeof window.updatePreview === 'function') {
                window.updatePreview();
            } else if (typeof updatePreview === 'function') {
                updatePreview();
            }
            if (typeof window !== 'undefined' && typeof window.updatePlaceholderStats === 'function') {
                window.updatePlaceholderStats();
            } else if (typeof updatePlaceholderStats === 'function') {
                updatePlaceholderStats();
            }
        } else {
            // Fallback: If dataTransfer doesn't have proper data structure
            console.log('[DROP] Fallback: Invalid data structure, trying to infer from elements');
            const targetCell = e.target.closest('.media-cell') || e.target.closest('td');
            const sourceCell = document.querySelector('.media-cell.dragging') || 
                             (e.dataTransfer && e.dataTransfer.getData('text/plain') ? 
                              document.querySelector(`[data-media-index="${e.dataTransfer.getData('text/plain')}"]`) : null);
            
            if (targetCell && sourceCell && targetCell !== sourceCell) {
                const sourceIndex = parseInt(sourceCell.dataset.mediaIndex);
                const targetPlaceholder = targetCell.dataset.placeholder || placeholder;
                if (!isNaN(sourceIndex) && targetPlaceholder === placeholder) {
                    console.log('[DROP] Fallback: Using source and target cells', { sourceIndex, targetCell: targetCell.dataset.mediaIndex });
                    reorderMediaInPlaceholder(placeholder, sourceIndex, targetCell);
                }
            } else {
                console.error('[DROP] Fallback failed - could not determine source or target');
            }
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
    
    // Set drop effect based on what's being dragged
    if (e.dataTransfer) {
        // If dragging from table (reshuffle), use 'move', otherwise 'copy'
        const effectAllowed = e.dataTransfer.effectAllowed;
        if (effectAllowed === 'move' || effectAllowed === 'all') {
            e.dataTransfer.dropEffect = 'move';
        } else {
            e.dataTransfer.dropEffect = 'copy';
        }
    }

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
    
    // Log for debugging reshuffle
    const placeholder = target?.dataset?.placeholder || target?.closest?.('[data-placeholder]')?.dataset?.placeholder;
    if (placeholder && e.dataTransfer?.effectAllowed === 'move') {
        console.log('[RESHUFFLE] Drag over cell', { placeholder, dropEffect: e.dataTransfer?.dropEffect });
    }
}

/**
 * Reorder media within placeholder table
 */
function reorderMediaInPlaceholder(placeholder, fromIndex, targetCell) {
    console.log('[RESHUFFLE] reorderMediaInPlaceholder called', { placeholder, fromIndex, targetCell });
    
    // Ensure assignments object exists
    if (!window.observationMediaAssignments) {
        window.observationMediaAssignments = {};
    }
    
    const assignments = window.observationMediaAssignments; // Use directly to ensure we're modifying the actual object
    const placeholderKey = placeholder.toLowerCase();
    
    if (!assignments[placeholderKey] || !assignments[placeholderKey][fromIndex]) {
        console.error('[RESHUFFLE] Invalid source index or no assignments', { 
            placeholderKey, 
            fromIndex, 
            assignmentsExists: !!assignments[placeholderKey],
            assignmentsLength: assignments[placeholderKey] ? assignments[placeholderKey].length : 0,
            assignments: assignments[placeholderKey] 
        });
        return;
    }

    // Get target index from cell
    let targetIndex = parseInt(targetCell.dataset.mediaIndex);
    console.log('[RESHUFFLE] Target index from dataset:', targetIndex, 'targetCell:', targetCell);
    
    if (isNaN(targetIndex)) {
        // Try to find the index by looking at the cell's position in the table
        // Try both original placeholder and lowercased version
        const allCells1 = Array.from(document.querySelectorAll(`.media-cell[data-placeholder="${placeholder}"]`));
        const allCells2 = Array.from(document.querySelectorAll(`.media-cell[data-placeholder="${placeholderKey}"]`));
        const allCells = allCells1.length > 0 ? allCells1 : allCells2;
        console.log('[RESHUFFLE] Found', allCells.length, 'cells for placeholder', placeholder, 'or', placeholderKey);
        targetIndex = allCells.indexOf(targetCell);
        console.log('[RESHUFFLE] Target index from cell position:', targetIndex);
        if (targetIndex === -1) {
            console.error('[RESHUFFLE] Could not determine target index. Cell not found in selector results.');
            console.error('[RESHUFFLE] Target cell dataset:', targetCell.dataset);
            return;
        }
    }
    
    console.log('[RESHUFFLE] Reordering from index', fromIndex, 'to index', targetIndex);
    
    // If dragging to the same position, do nothing
    if (fromIndex === targetIndex) {
        console.log('[RESHUFFLE] Same position, no reorder needed');
        return;
    }

    // Reorder array - need to handle the case where removing shifts indices
    const media = assignments[placeholderKey][fromIndex];
    console.log('[RESHUFFLE] Media to move:', media.name || media.path);
    console.log('[RESHUFFLE] Array before removal:', assignments[placeholderKey].map((m, i) => `${i}:${m.name || m.path}`));
    
    // Remove from source
    const removed = assignments[placeholderKey].splice(fromIndex, 1);
    console.log('[RESHUFFLE] Removed:', removed[0].name || removed[0].path, 'from index', fromIndex);
    console.log('[RESHUFFLE] Array after removal:', assignments[placeholderKey].map((m, i) => `${i}:${m.name || m.path}`));
    
    // Adjust target index based on where we're inserting
    // When dragging to a cell, we want to insert at that cell's position (replacing it)
    // After removing an item, indices shift, so we need to adjust
    let adjustedTargetIndex = targetIndex;
    
    if (fromIndex < targetIndex) {
        // Source is before target: after removal, the target position shifts left by 1
        // We want to insert at the target position, which is now at targetIndex - 1
        // Example: [A(0), B(1)] - move A to position 1 (B's position)
        //   Remove A: [B(0)]
        //   Insert at 1: [B(0), A(1)] - A is now at position 1, B at 0 ✓
        // But wait - if we want A to be at position 1 (where B was), we insert at 1
        // However, if we want A to be BEFORE B, we'd insert at 0
        // The current behavior inserts AT the target position, which means AFTER the item that was there
        // So we keep targetIndex as-is
        adjustedTargetIndex = targetIndex;
        console.log('[RESHUFFLE] Source before target: inserting at target position', adjustedTargetIndex);
    } else if (fromIndex > targetIndex) {
        // Source is after target: no adjustment needed, insert at target position
        // Example: [A(0), B(1), C(2)] - move C to position 0 (A's position)
        //   Remove C: [A(0), B(1)]
        //   Insert at 0: [C(0), A(1), B(2)] - C is now at position 0 ✓
        adjustedTargetIndex = targetIndex;
        console.log('[RESHUFFLE] Source after target: inserting at target position', adjustedTargetIndex);
    } else {
        // Same position - should have been caught earlier, but handle it
        console.log('[RESHUFFLE] Same position, no reorder needed');
        return;
    }
    
    // Insert at target
    console.log('[RESHUFFLE] Inserting at index', adjustedTargetIndex);
    assignments[placeholderKey].splice(adjustedTargetIndex, 0, media);
    console.log('[RESHUFFLE] Array after insertion:', assignments[placeholderKey].map((m, i) => `${i}:${m.name || m.path}`));
    console.log('[RESHUFFLE] Reorder complete. Final order:', assignments[placeholderKey].map(m => m.name || m.path));

    // Before updating preview, ensure sections with assigned media are expanded
    const currentReshuffleMode = (typeof window !== 'undefined' && window.reshuffleMode !== undefined) ? window.reshuffleMode : reshuffleMode;
    if (currentReshuffleMode) {
        const textEditor = document.getElementById('observationTextEditor');
        const text = textEditor ? textEditor.value : '';
        const sectionData = parseSections(text);
        
        if (sectionData.hasSections) {
            const states = getSectionStates();
            sectionData.sections.forEach(section => {
                const sectionPlaceholders = extractPlaceholders(section.content);
                const hasAssignedMedia = sectionPlaceholders.some(ph => {
                    const phKey = ph.toLowerCase();
                    return assignments[phKey] && assignments[phKey].length > 0;
                });
                if (hasAssignedMedia) {
                    states[section.id] = true;
                }
            });
            saveSectionStates(states);
        }
    }

    // Update UI
    if (typeof window !== 'undefined' && typeof window.updatePreview === 'function') {
        window.updatePreview();
    } else if (typeof updatePreview === 'function') {
        updatePreview();
    }
    if (typeof window !== 'undefined' && typeof window.updatePlaceholderStats === 'function') {
        window.updatePlaceholderStats();
    } else if (typeof updatePlaceholderStats === 'function') {
        updatePlaceholderStats();
    }
    
    // Also update dialog preview if dialog is open
    if (window.currentPlaceholderDialog) {
        updateDialogPreview();
        
        // After dialog preview update, ensure sections with assigned media are expanded
        if (dialogReshuffleMode) {
            setTimeout(() => {
                const dialog = window.currentPlaceholderDialog;
                if (!dialog) return;
                
                const preview = dialog.querySelector('#dialogPreview');
                if (!preview) return;
                
                const assignments = getCurrentAssignments();
                const textEditor = document.getElementById('observationTextEditor');
                const text = textEditor ? textEditor.value : '';
                const sectionData = parseSections(text);
                
                if (sectionData.hasSections) {
                    sectionData.sections.forEach(section => {
                        const sectionPlaceholders = extractPlaceholders(section.content);
                        const hasAssignedMedia = sectionPlaceholders.some(ph => {
                            const phKey = ph.toLowerCase();
                            return assignments[phKey] && assignments[phKey].length > 0;
                        });
                        
                        if (hasAssignedMedia) {
                            const sectionContent = preview.querySelector(`.dialog-section-content[data-section-id="${section.id}"]`);
                            const sectionHeader = preview.querySelector(`.dialog-section-header[onclick*="${section.id}"]`);
                            const icon = sectionHeader ? sectionHeader.querySelector('.dialog-section-icon') : null;
                            
                            if (sectionContent) {
                                sectionContent.style.display = 'block';
                                sectionContent.style.setProperty('display', 'block', 'important');
                                console.log('[RESHUFFLE] Forced dialog section expansion in reorderMediaInPlaceholder:', section.id);
                            }
                            if (icon) {
                                icon.textContent = '▼';
                            }
                        }
                    });
                }
            }, 150);
        }
    }
    
    // After preview update, ensure sections are still expanded in DOM
    if (reshuffleMode) {
        setTimeout(() => {
            const textEditor = document.getElementById('observationTextEditor');
            const text = textEditor ? textEditor.value : '';
            const sectionData = parseSections(text);
            
            if (sectionData.hasSections) {
                const assignments = getCurrentAssignments();
                sectionData.sections.forEach(section => {
                    const sectionPlaceholders = extractPlaceholders(section.content);
                    const hasAssignedMedia = sectionPlaceholders.some(ph => {
                        const phKey = ph.toLowerCase();
                        return assignments[phKey] && assignments[phKey].length > 0;
                    });
                    if (hasAssignedMedia) {
                        const sectionEl = document.querySelector(`[data-section-id="${section.id}"]`);
                        if (sectionEl) {
                            // Remove collapsed class (this is critical - CSS uses it to hide content)
                            sectionEl.classList.remove('collapsed');
                            
                            // Force display with !important to override CSS
                            const contentEl = sectionEl.querySelector('.observation-section-content');
                            const iconEl = sectionEl.querySelector('.observation-section-icon');
                            
                            if (contentEl) {
                                // Use setAttribute to ensure !important takes effect
                                contentEl.setAttribute('style', 
                                    contentEl.getAttribute('style') + '; display: block !important; max-height: none !important; opacity: 1 !important; padding: 15px !important;');
                            }
                            if (iconEl) {
                                iconEl.textContent = '▼';
                            }
                            
                            console.log('[RESHUFFLE] Forced section expansion:', section.id, 'collapsed class removed:', !sectionEl.classList.contains('collapsed'));
                        }
                    }
                });
            }
        }, 100); // Increased timeout to ensure DOM is ready
    }
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
        
        // Update dialog preview if dialog is open
        if (window.currentPlaceholderDialog) {
            updateDialogPreview();
        }
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
 * Updated to support new two-level dropdown system
 */
function loadObservationMedia() {
    // Check if new two-level system is being used
    const qualificationSelect = document.getElementById('qualificationSelect');
    const learnerSelect = document.getElementById('learnerSelect');
    
    if (qualificationSelect && learnerSelect) {
        // New two-level system - check if template's version exists and call it
        // The template's version should be defined in the HTML and override this
        // But if it hasn't loaded yet, we'll handle it here as fallback
        const qualification = qualificationSelect.value;
        const learner = learnerSelect.value;
        
        if (!qualification || !learner) {
            const grid = document.getElementById('observationMediaGrid');
            if (grid) {
                grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;" id="mediaBrowserMessage">Please select both qualification and learner</p>';
            }
            const countEl = document.getElementById('observationMediaCount');
            if (countEl) {
                countEl.textContent = '0 files';
            }
            return;
        }
        
        // Try to call the template's version if it exists (it should override this)
        // If we're here, it means the template version hasn't loaded yet or was overridden
        // So we need to implement the fetch here as fallback
        const grid = document.getElementById('observationMediaGrid');
        if (grid) {
            grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;" id="mediaBrowserMessage">Loading media files...</p>';
        }
        
        const fetchUrl = `/v2p-formatter/media-converter/observation-media/media?qualification=${encodeURIComponent(qualification)}&learner=${encodeURIComponent(learner)}`;
        console.log('Fetching media from:', fetchUrl);
        fetch(fetchUrl)
            .then(response => {
                console.log('Fetch response received, status:', response.status, response.statusText);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Media data received:', data);
                console.log('Success:', data.success, 'Media count:', data.media ? data.media.length : 0);
                
                if (data.success) {
                    const mediaFiles = data.media || [];
                    console.log('Media files count:', mediaFiles.length);
                    
                    if (mediaFiles.length === 0) {
                        console.warn('No media files returned');
                        const grid = document.getElementById('observationMediaGrid');
                        if (grid) {
                            grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;" id="mediaBrowserMessage">No media files found</p>';
                        }
                        const countEl = document.getElementById('observationMediaCount');
                        if (countEl) {
                            countEl.textContent = '0 files';
                        }
                        return;
                    }
                    
                    // Display media
                    console.log('Calling displayObservationMedia with', mediaFiles.length, 'files');
                    if (typeof displayObservationMedia === 'function') {
                        displayObservationMedia(mediaFiles);
                        console.log('displayObservationMedia called successfully');
                    } else if (typeof window.displayObservationMedia === 'function') {
                        window.displayObservationMedia(mediaFiles);
                        console.log('window.displayObservationMedia called successfully');
                    } else {
                        console.warn('displayObservationMedia function not found - will retry');
                        const grid = document.getElementById('observationMediaGrid');
                        if (grid) {
                            grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Display function not available</p>';
                        }
                        return;
                    }
                    
                    const countEl = document.getElementById('observationMediaCount');
                    if (countEl) {
                        countEl.textContent = `${mediaFiles.length} files`;
                        console.log('File count updated to:', countEl.textContent);
                    }
                } else {
                    console.error('Media load failed:', data.error);
                    const grid = document.getElementById('observationMediaGrid');
                    if (grid) {
                        grid.innerHTML = `<p style="color: #999; text-align: center; padding: 20px;" id="mediaBrowserMessage">Error: ${data.error || 'Failed to load media'}</p>`;
                    }
                    const countEl = document.getElementById('observationMediaCount');
                    if (countEl) {
                        countEl.textContent = '0 files';
                    }
                }
            })
            .catch(error => {
                console.error('Error loading media:', error);
                console.error('Error stack:', error.stack);
                const grid = document.getElementById('observationMediaGrid');
                if (grid) {
                    grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;" id="mediaBrowserMessage">Error loading media files: ' + error.message + '</p>';
                }
                const countEl = document.getElementById('observationMediaCount');
                if (countEl) {
                    countEl.textContent = '0 files';
                }
            });
        return;
    }
    
    // Fallback to old single-level system for backward compatibility
    const subfolderSelect = document.getElementById('observationSubfolderSelect');
    if (!subfolderSelect) {
        // Neither system available
        const grid = document.getElementById('observationMediaGrid');
        if (grid) {
            grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Media browser not initialized</p>';
        }
        return;
    }
    
    const subfolder = subfolderSelect.value;
    if (!subfolder) {
        const grid = document.getElementById('observationMediaGrid');
        if (grid) {
            grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Please select a subfolder</p>';
        }
        const countEl = document.getElementById('observationMediaCount');
        if (countEl) {
            countEl.textContent = '0 files';
        }
        return;
    }

    // Get media from embedded data (API-free)
    const mediaFiles = window.observationMediaData && window.observationMediaData[subfolder] ? window.observationMediaData[subfolder] : [];
    
    if (typeof displayObservationMedia === 'function') {
        displayObservationMedia(mediaFiles);
    } else if (typeof window.displayObservationMedia === 'function') {
        window.displayObservationMedia(mediaFiles);
    } else {
        const grid = document.getElementById('observationMediaGrid');
        if (grid) {
            grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Display function not available</p>';
        }
        return;
    }
    
    const countEl = document.getElementById('observationMediaCount');
    if (countEl) {
        countEl.textContent = `${mediaFiles.length} files`;
    }
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
    
    // Check if we have subfolders (non-empty subfolder names)
    const hasSubfolders = subfolderKeys.some(key => key && key.trim() !== '');
    
    // Check if we have files directly in the folder (empty subfolder)
    const hasRootFiles = groupedMedia[''] && groupedMedia[''].length > 0;

    // First, display files directly in the folder if they exist (main category files first)
    if (hasRootFiles) {
        const assignments = getCurrentAssignments();
        const textEditor = document.getElementById('observationTextEditor');
        const text = textEditor ? textEditor.value : '';
        
        // Create container for root files with grid layout
        const rootContainer = document.createElement('div');
        rootContainer.className = 'media-root-files-container';
        rootContainer.style.display = 'grid';
        rootContainer.style.gap = '15px';
        rootContainer.style.padding = '10px 0';
        
        // Apply grid layout settings to root files container
        updateSubfolderContentGrid(rootContainer);
        
        const rootMedia = groupedMedia[''];
        rootMedia.forEach((media, index) => {
            const card = document.createElement('div');
            card.className = 'observation-media-card';
            card.dataset.mediaIndex = index;
            card.dataset.mediaPath = media.path;
            card.dataset.mediaName = media.name;
            card.dataset.mediaType = media.type;

            // Check if media is already assigned (disabled state)
            const isAssigned = isMediaAssigned(media.path);
            
            // Get section color for assigned media
            let sectionColor = null;
            let badgeStyle = '';
            if (isAssigned) {
                sectionColor = getSectionColorForMedia(media.path, assignments, text);
                if (sectionColor) {
                    badgeStyle = `style="background: ${sectionColor}E6; border-color: ${sectionColor}; color: white;"`;
                } else {
                    badgeStyle = 'style="background: rgba(78, 205, 196, 0.9); border-color: #4ecdc4; color: white;"';
                }
            }
            
            if (isAssigned) {
                card.classList.add('media-assigned');
                card.style.opacity = '0.5';
                card.style.cursor = 'not-allowed';
            } else {
                card.draggable = true;
                card.style.cursor = 'grab';
            }

            // Get thumbnail size from settings - increased for crystal clear quality
            let thumbSize = '640x480'; // Default - increased from 240x180 for better quality
            let thumbWidth = 640;
            let thumbHeight = 480;
            
            if (typeof getThumbnailSizeString === 'function') {
                thumbSize = getThumbnailSizeString();
                // Parse size string to get width and height for fallback SVG
                const sizeMatch = thumbSize.match(/(\d+)x(\d+)/);
                if (sizeMatch) {
                    thumbWidth = parseInt(sizeMatch[1]);
                    thumbHeight = parseInt(sizeMatch[2]);
                }
            }
            
            card.innerHTML = `
                <div class="observation-media-thumbnail">
                    <img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(media.path)}&size=${thumbSize}" 
                         alt="${media.name}" 
                         onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'${thumbWidth}\' height=\'${thumbHeight}\'%3E%3Crect fill=\'%23333\' width=\'${thumbWidth}\' height=\'${thumbHeight}\'/%3E%3Ctext x=\'50%25\' y=\'50%25\' text-anchor=\'middle\' dy=\'.3em\' fill=\'%23999\' font-size=\'12\'%3E${media.type === 'video' ? 'VIDEO' : media.type === 'audio' ? 'AUDIO' : media.type === 'document' ? 'PDF' : 'IMAGE'}%3C/text%3E%3C/svg%3E'">
                    ${media.type === 'video' ? '<span class="video-badge">⏯</span>' : ''}
                    ${media.type === 'audio' ? '<span class="audio-badge">🎵</span>' : ''}
                    ${media.type === 'document' ? '<span class="pdf-badge">📄</span>' : ''}
                    ${media.type === 'audio' ? `<div class="audio-player-overlay" onclick="event.stopPropagation(); playAudioFile('${encodeURIComponent(media.path)}', '${escapeHtml(media.name)}');"><span class="audio-play-button">▶</span></div>` : ''}
                    ${isAssigned ? `<span class="assigned-badge" ${badgeStyle}>✓ Assigned</span>` : ''}
                </div>
                <div class="observation-media-info">
                    <div class="observation-media-name" 
                         title="${media.name}"
                         data-media-path="${media.path}"
                         data-media-name="${media.name}"
                         onclick="handleMediaNameClick(event, this)"
                         style="cursor: pointer; user-select: none;">
                        ${media.name}
                    </div>
                    <div class="observation-media-size">${formatFileSize(media.size)}</div>
                </div>
            `;

            // Add drag and click handlers for unassigned media
            if (!isAssigned) {
                card.addEventListener('dragstart', handleMediaDragStart);
                card.addEventListener('click', () => handleMediaClick(media));
            }

            rootContainer.appendChild(card);
        });
        
        // Append root files container to grid FIRST
        grid.appendChild(rootContainer);
    }

    // Then, display files in subfolders if they exist (subfolders after main category files)
    if (hasSubfolders) {
        // Create collapsible sections for each subfolder
        subfolderKeys.forEach(subfolder => {
            if (!subfolder || subfolder.trim() === '') return;
            
            const mediaCount = groupedMedia[subfolder].length;
            
            // Create section container
            const section = document.createElement('div');
            section.className = 'media-subfolder-section collapsed';
            section.dataset.subfolder = subfolder;
            
            // Create header
            const header = document.createElement('div');
            header.className = 'media-subfolder-header';
            header.onclick = function() { toggleSubfolderSection(subfolder); };
            header.innerHTML = `
                <span class="section-icon">▶</span>
                <span class="folder-icon">📁</span>
                <span class="subfolder-name">${escapeHtml(subfolder)}</span>
                <span class="file-count">(${mediaCount} file${mediaCount !== 1 ? 's' : ''})</span>
            `;
            section.appendChild(header);
            
            // Create content container
            const content = document.createElement('div');
            content.className = 'media-subfolder-content';
            content.style.display = 'none';
            content.style.visibility = 'hidden';
            content.style.height = '0';
            content.style.minHeight = '0';
            content.style.maxHeight = '0';
            
            // Initialize grid layout for content
            updateSubfolderContentGrid(content);
            
            // Add media cards for this subfolder
            const assignments = getCurrentAssignments();
            const textEditor = document.getElementById('observationTextEditor');
            const text = textEditor ? textEditor.value : '';
            
            groupedMedia[subfolder].forEach((media, index) => {
            const card = document.createElement('div');
            card.className = 'observation-media-card';
            card.dataset.mediaIndex = index;
            card.dataset.mediaPath = media.path;
            card.dataset.mediaName = media.name;
            card.dataset.mediaType = media.type;

            // Check if media is already assigned (disabled state)
            const isAssigned = isMediaAssigned(media.path);
            
            // Get section color for assigned media
            let sectionColor = null;
            let badgeStyle = '';
            if (isAssigned) {
                sectionColor = getSectionColorForMedia(media.path, assignments, text);
                if (sectionColor) {
                    badgeStyle = `style="background: ${sectionColor}E6; border-color: ${sectionColor}; color: white;"`;
                } else {
                    badgeStyle = 'style="background: rgba(78, 205, 196, 0.9); border-color: #4ecdc4; color: white;"';
                }
            }
            
            if (isAssigned) {
                card.classList.add('media-assigned');
                card.style.opacity = '0.5';
                card.style.cursor = 'not-allowed';
            } else {
                card.draggable = true;
                card.style.cursor = 'grab';
            }

            // Get thumbnail size from settings - increased for crystal clear quality
            let thumbSize = '640x480'; // Default - increased from 240x180 for better quality
            let thumbWidth = 640;
            let thumbHeight = 480;
            
            if (typeof getThumbnailSizeString === 'function') {
                thumbSize = getThumbnailSizeString();
                // Parse size string to get width and height for fallback SVG
                const sizeMatch = thumbSize.match(/(\d+)x(\d+)/);
                if (sizeMatch) {
                    thumbWidth = parseInt(sizeMatch[1]);
                    thumbHeight = parseInt(sizeMatch[2]);
                }
            }
            
            card.innerHTML = `
                <div class="observation-media-thumbnail">
                    <img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(media.path)}&size=${thumbSize}" 
                         alt="${media.name}" 
                         onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'${thumbWidth}\' height=\'${thumbHeight}\'%3E%3Crect fill=\'%23333\' width=\'${thumbWidth}\' height=\'${thumbHeight}\'/%3E%3Ctext x=\'50%25\' y=\'50%25\' text-anchor=\'middle\' dy=\'.3em\' fill=\'%23999\' font-size=\'12\'%3E${media.type === 'video' ? 'VIDEO' : media.type === 'audio' ? 'AUDIO' : media.type === 'document' ? 'PDF' : 'IMAGE'}%3C/text%3E%3C/svg%3E'">
                    ${media.type === 'video' ? '<span class="video-badge">⏯</span>' : ''}
                    ${media.type === 'audio' ? '<span class="audio-badge">🎵</span>' : ''}
                    ${media.type === 'document' ? '<span class="pdf-badge">📄</span>' : ''}
                    ${media.type === 'audio' ? `<div class="audio-player-overlay" onclick="event.stopPropagation(); playAudioFile('${encodeURIComponent(media.path)}', '${escapeHtml(media.name)}');"><span class="audio-play-button">▶</span></div>` : ''}
                    ${isAssigned ? `<span class="assigned-badge" ${badgeStyle}>✓ Assigned</span>` : ''}
                </div>
                <div class="observation-media-info">
                    <div class="observation-media-name" 
                         title="${media.name}"
                         data-media-path="${media.path}"
                         data-media-name="${media.name}"
                         onclick="handleMediaNameClick(event, this)"
                         style="cursor: pointer; user-select: none;">
                        ${media.name}
                    </div>
                    <div class="observation-media-size">${formatFileSize(media.size)}</div>
                </div>
            `;

            // Add drag and click handlers for unassigned media
            if (!isAssigned) {
                card.addEventListener('dragstart', handleMediaDragStart);
                card.addEventListener('click', () => handleMediaClick(media));
            }

            content.appendChild(card);
            });
            
            // Append content to section, then section to grid
            section.appendChild(content);
            grid.appendChild(section);
        });
    }
    
    // Fallback: if no subfolders and no root files were displayed, show all files (shouldn't happen normally)
    if (!hasRootFiles && !hasSubfolders) {
        // No subfolders - display media files directly (flat display with grid layout)
        const assignments = getCurrentAssignments();
        const textEditor = document.getElementById('observationTextEditor');
        const text = textEditor ? textEditor.value : '';
        
        // Create container for root files with grid layout
        const rootContainer = document.createElement('div');
        rootContainer.className = 'media-root-files-container';
        rootContainer.style.display = 'grid';
        rootContainer.style.gap = '15px';
        rootContainer.style.padding = '10px 0';
        
        // Apply grid layout settings to root files container
        updateSubfolderContentGrid(rootContainer);
        
        const flatMedia = groupedMedia[''] || mediaFiles;
        flatMedia.forEach((media, index) => {
            const card = document.createElement('div');
            card.className = 'observation-media-card';
            card.dataset.mediaIndex = index;
            card.dataset.mediaPath = media.path;
            card.dataset.mediaName = media.name;
            card.dataset.mediaType = media.type;

            // Check if media is already assigned (disabled state)
            const isAssigned = isMediaAssigned(media.path);
            
            // Get section color for assigned media
            let sectionColor = null;
            let badgeStyle = '';
            if (isAssigned) {
                sectionColor = getSectionColorForMedia(media.path, assignments, text);
                if (sectionColor) {
                    badgeStyle = `style="background: ${sectionColor}E6; border-color: ${sectionColor}; color: white;"`;
                } else {
                    badgeStyle = 'style="background: rgba(78, 205, 196, 0.9); border-color: #4ecdc4; color: white;"';
                }
            }
            
            if (isAssigned) {
                card.classList.add('media-assigned');
                card.style.opacity = '0.5';
                card.style.cursor = 'not-allowed';
            } else {
                card.draggable = true;
                card.style.cursor = 'grab';
            }

            // Get thumbnail size from settings - increased for crystal clear quality
            let thumbSize = '640x480'; // Default - increased from 240x180 for better quality
            let thumbWidth = 640;
            let thumbHeight = 480;
            
            if (typeof getThumbnailSizeString === 'function') {
                thumbSize = getThumbnailSizeString();
                // Parse size string to get width and height for fallback SVG
                const sizeMatch = thumbSize.match(/(\d+)x(\d+)/);
                if (sizeMatch) {
                    thumbWidth = parseInt(sizeMatch[1]);
                    thumbHeight = parseInt(sizeMatch[2]);
                }
            }
            
            card.innerHTML = `
                <div class="observation-media-thumbnail">
                    <img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(media.path)}&size=${thumbSize}" 
                         alt="${media.name}" 
                         onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'${thumbWidth}\' height=\'${thumbHeight}\'%3E%3Crect fill=\'%23333\' width=\'${thumbWidth}\' height=\'${thumbHeight}\'/%3E%3Ctext x=\'50%25\' y=\'50%25\' text-anchor=\'middle\' dy=\'.3em\' fill=\'%23999\' font-size=\'12\'%3E${media.type === 'video' ? 'VIDEO' : media.type === 'audio' ? 'AUDIO' : media.type === 'document' ? 'PDF' : 'IMAGE'}%3C/text%3E%3C/svg%3E'">
                    ${media.type === 'video' ? '<span class="video-badge">⏯</span>' : ''}
                    ${media.type === 'audio' ? '<span class="audio-badge">🎵</span>' : ''}
                    ${media.type === 'document' ? '<span class="pdf-badge">📄</span>' : ''}
                    ${media.type === 'audio' ? `<div class="audio-player-overlay" onclick="event.stopPropagation(); playAudioFile('${encodeURIComponent(media.path)}', '${escapeHtml(media.name)}');"><span class="audio-play-button">▶</span></div>` : ''}
                    ${isAssigned ? `<span class="assigned-badge" ${badgeStyle}>✓ Assigned</span>` : ''}
                </div>
                <div class="observation-media-info">
                    <div class="observation-media-name" 
                         title="${media.name}"
                         data-media-path="${media.path}"
                         data-media-name="${media.name}"
                         onclick="handleMediaNameClick(event, this)"
                         style="cursor: pointer; user-select: none;">
                        ${media.name}
                    </div>
                    <div class="observation-media-size">${formatFileSize(media.size)}</div>
                </div>
            `;

            // Add drag and click handlers for unassigned media
            if (!isAssigned) {
                card.addEventListener('dragstart', handleMediaDragStart);
                card.addEventListener('click', () => handleMediaClick(media));
            }

            rootContainer.appendChild(card);
        });
        
        // Append root files container to grid
        grid.appendChild(rootContainer);
    }
}

/**
 * Handle media drag start
 */
function handleMediaDragStart(e) {
    const card = e.currentTarget;

    // Check if this card is part of bulk selection
    if (card.classList.contains('media-selected') && window.bulkSelectedMedia) {
        // Drag all selected media
        const bulkData = {
            bulk: true,
            media: window.bulkSelectedMedia
        };
        const bulkDataStr = JSON.stringify(bulkData);
        e.dataTransfer.setData('application/json', bulkDataStr);
        e.dataTransfer.setData('text/plain', bulkDataStr); // Fallback
        // Store in window for fallback
        window.lastDragData = bulkData;
        console.log('[DRAG] Started drag with bulk data:', bulkData);
    } else {
        // Drag single media
        const mediaData = {
            path: card.dataset.mediaPath,
            name: card.dataset.mediaName,
            type: card.dataset.mediaType
        };
        const mediaDataStr = JSON.stringify(mediaData);
        e.dataTransfer.setData('application/json', mediaDataStr);
        e.dataTransfer.setData('text/plain', mediaDataStr); // Fallback
        e.dataTransfer.setData('text/html', mediaData.path); // Another fallback
        // Store in window for fallback
        window.lastDragData = mediaData;
        console.log('[DRAG] Started drag with media data:', mediaData);
    }

    e.dataTransfer.effectAllowed = 'copy';
    card.style.opacity = '0.5';
    card.classList.add('dragging'); // Mark as dragging for fallback detection
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
 * Toggle subfolder section expand/collapse
 */
function toggleSubfolderSection(subfolderName) {
    // Find section by data attribute (subfolder name)
    const sections = document.querySelectorAll('.media-subfolder-section');
    let section = null;
    
    sections.forEach(sec => {
        if (sec.dataset.subfolder === subfolderName) {
            section = sec;
        }
    });
    
    if (!section) return;
    
    const isCollapsed = section.classList.contains('collapsed');
    const content = section.querySelector('.media-subfolder-content');
    const icon = section.querySelector('.section-icon');
    
    if (isCollapsed) {
        // Expand
        section.classList.remove('collapsed');
        if (content) {
            content.style.display = 'grid';
            content.style.visibility = 'visible';
            content.style.height = 'auto';
            content.style.minHeight = 'auto';
            content.style.maxHeight = 'none';
            // Apply grid layout settings
            updateSubfolderContentGrid(content);
        }
        if (icon) icon.textContent = '▼';
    } else {
        // Collapse
        section.classList.add('collapsed');
        if (content) {
            content.style.display = 'none';
            content.style.visibility = 'hidden';
            content.style.height = '0';
            content.style.minHeight = '0';
            content.style.maxHeight = '0';
        }
        if (icon) icon.textContent = '▶';
    }
}

/**
 * Update grid layout for subfolder content based on current settings
 */
function updateSubfolderContentGrid(contentElement) {
    if (!contentElement) return;
    
    const leftPanel = document.querySelector('.observation-media-left-panel');
    const isExpanded = leftPanel && leftPanel.classList.contains('expanded');
    
    // Get settings
    let thumbnailsPerRow = 3; // Default
    if (typeof window.loadMediaBrowserSettings === 'function') {
        const settings = window.loadMediaBrowserSettings();
        thumbnailsPerRow = settings.thumbnailsPerRow || 3;
    } else {
        // Try to get from localStorage directly
        try {
            thumbnailsPerRow = parseInt(localStorage.getItem('mediaBrowser.thumbnailsPerRow')) || 3;
        } catch (e) {
            // Use default
        }
    }
    
    if (isExpanded) {
        // Expanded browser: auto-calculate columns
        contentElement.style.gridTemplateColumns = 'repeat(auto-fill, minmax(240px, 1fr))';
    } else {
        // Collapsed browser: use user-selected columns
        contentElement.style.gridTemplateColumns = `repeat(${thumbnailsPerRow}, 1fr)`;
    }
}

/**
 * Update all subfolder content grids (when settings change)
 */
function updateAllSubfolderGrids() {
    const contents = document.querySelectorAll('.media-subfolder-content');
    contents.forEach(content => {
        if (content.style.display !== 'none') {
            updateSubfolderContentGrid(content);
        }
    });
    
    // Also update root files container
    const rootContainers = document.querySelectorAll('.media-root-files-container');
    rootContainers.forEach(container => {
        updateSubfolderContentGrid(container);
    });
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
                checkbox.addEventListener('click', function (e) {
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
window.toggleSubfolderSection = toggleSubfolderSection;
window.getSectionColorForMedia = getSectionColorForMedia;
window.findPlaceholderForMedia = findPlaceholderForMedia;
window.getSectionColorForPlaceholder = getSectionColorForPlaceholder;
window.updateAllSubfolderGrids = updateAllSubfolderGrids;
window.handleTableDrop = handleTableDrop;
window.handleTableDragOver = handleTableDragOver;
window.handleTableCellDragStart = handleTableCellDragStart;
window.removeMediaFromPlaceholder = removeMediaFromPlaceholder;
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
        btn.addEventListener('click', function (e) {
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
        newThumb.addEventListener('dragstart', function (e) {
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
        newThumb.addEventListener('dragend', function (e) {
            console.log('[DRAG] dragend event fired');
            newThumb.style.opacity = '1';
        });

        // Prevent image from dragging
        const img = newThumb.querySelector('img');
        if (img) {
            img.draggable = false;
            img.addEventListener('dragstart', function (e) {
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
    // Prevent collapsing sections with assigned media during reshuffle mode
    if (window.dialogReshuffleMode) {
        const sectionContent = document.querySelector(`.dialog-section-content[data-section-id="${sectionId}"]`);
        if (sectionContent) {
            const textEditor = document.getElementById('observationTextEditor');
            const text = textEditor ? textEditor.value : '';
            const sectionData = parseSections(text);
            const section = sectionData.sections.find(s => s.id === sectionId);
            if (section) {
                const sectionPlaceholders = extractPlaceholders(section.content);
                const assignments = getCurrentAssignments();
                const hasAssignedMedia = sectionPlaceholders.some(placeholder => {
                    const placeholderKey = placeholder.toLowerCase();
                    return assignments[placeholderKey] && assignments[placeholderKey].length > 0;
                });
                if (hasAssignedMedia) {
                    console.log('[DIALOG TOGGLE] Prevented collapse during reshuffle:', sectionId);
                    return; // Prevent toggle during reshuffle if section has assigned media
                }
            }
        }
    }
    
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
    
    // Set drop effect based on what's being dragged
    if (e.dataTransfer) {
        const effectAllowed = e.dataTransfer.effectAllowed;
        if (effectAllowed === 'move' || effectAllowed === 'all') {
            e.dataTransfer.dropEffect = 'move';
        } else {
            e.dataTransfer.dropEffect = 'copy';
        }
    }
    
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

    let data;
    try {
        data = JSON.parse(dataStr);
        if (!data) {
            console.log('Invalid drag data');
            return false;
        }

        console.log('[DIALOG DROP] Parsed drag data:', { hasPath: !!data.path, hasName: !!data.name, source: data.source, index: data.index });

        // Check if this is a reshuffle (reordering within table)
        if (data.source === 'table') {
            console.log('[DIALOG DROP] Reshuffle detected - reordering within table', { placeholder, fromIndex: data.index });
            
            // Verify placeholder matches (case-insensitive)
            const draggedPlaceholderKey = (data.placeholder || '').toLowerCase();
            const targetPlaceholderKey = placeholder.toLowerCase();
            
            if (draggedPlaceholderKey !== targetPlaceholderKey) {
                console.warn('[DIALOG DROP] Placeholder mismatch - cannot reorder across placeholders', { 
                    dragged: draggedPlaceholderKey, 
                    target: targetPlaceholderKey 
                });
                return false;
            }
            
            const targetCell = target.closest('.media-cell') || target.closest('td');
            if (targetCell) {
                console.log('[DIALOG DROP] Target cell found', { 
                    targetIndex: targetCell.dataset.mediaIndex,
                    placeholder: targetCell.dataset.placeholder 
                });
                reorderMediaInPlaceholder(placeholder, data.index, targetCell);
                
                // Update dialog preview to reflect the reorder
                updateDialogPreview();
                
                // Force expand sections with assigned media after update
                setTimeout(() => {
                    const dialog = window.currentPlaceholderDialog;
                    if (dialog && dialogReshuffleMode) {
                        const preview = dialog.querySelector('#dialogPreview');
                        if (preview) {
                            const assignments = getCurrentAssignments();
                            const textEditor = document.getElementById('observationTextEditor');
                            const text = textEditor ? textEditor.value : '';
                            const sectionData = parseSections(text);
                            
                            if (sectionData.hasSections) {
                                sectionData.sections.forEach(section => {
                                    const sectionPlaceholders = extractPlaceholders(section.content);
                                    const hasAssignedMedia = sectionPlaceholders.some(ph => {
                                        const phKey = ph.toLowerCase();
                                        return assignments[phKey] && assignments[phKey].length > 0;
                                    });
                                    
                                    if (hasAssignedMedia) {
                                        const sectionContent = preview.querySelector(`.dialog-section-content[data-section-id="${section.id}"]`);
                                        const sectionHeader = preview.querySelector(`.dialog-section-header[onclick*="${section.id}"]`);
                                        const icon = sectionHeader ? sectionHeader.querySelector('.dialog-section-icon') : null;
                                        
                                        if (sectionContent) {
                                            sectionContent.style.display = 'block';
                                            sectionContent.style.setProperty('display', 'block', 'important');
                                            console.log('[DIALOG RESHUFFLE] Forced section expansion:', section.id);
                                        }
                                        if (icon) {
                                            icon.textContent = '▼';
                                        }
                                    }
                                });
                            }
                        }
                    }
                }, 150);
                
                // Update main preview
                updatePreview();
                updatePlaceholderStats();
            } else {
                console.error('[DIALOG DROP] Target cell not found for drop');
            }
            return false;
        }

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
        console.log('[DIALOG UPDATE] Rendering sections, dialogReshuffleMode:', dialogReshuffleMode);
        previewHtml = renderSectionsForDialog(sectionData, placeholders, colorMap, assignments, validation, mediaList);
        console.log('[DIALOG UPDATE] Generated HTML length:', previewHtml.length);
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

    // Force delete buttons to be visible in dialog
    if (window.currentPlaceholderDialog) {
        const deleteButtons = preview.querySelectorAll('.dialog-delete-btn, .remove-media-btn');
        deleteButtons.forEach(btn => {
            btn.style.display = 'flex';
            btn.style.visibility = 'visible';
            btn.style.opacity = '1';
            btn.style.position = 'absolute';
            btn.style.top = '5px';
            btn.style.right = '5px';
            btn.style.zIndex = '100';
        });
    }

    // Update reshuffle button visibility
    const hasAssignedMedia = Object.keys(assignments).some(key => assignments[key] && assignments[key].length > 0);
    const dialogReshuffleBtn = dialog.querySelector('#dialogReshuffleBtn');
    if (dialogReshuffleBtn) {
        dialogReshuffleBtn.style.display = hasAssignedMedia ? 'block' : 'none';
    }
    
    // Preserve section expanded state - CRITICAL for preventing collapse during reshuffle
    if (sectionData.hasSections) {
        // Update stored state: sections with assigned media should always be expanded
        if (!window.dialogSectionExpandedState) {
            window.dialogSectionExpandedState = {};
        }
        sectionData.sections.forEach(section => {
            const sectionPlaceholders = extractPlaceholders(section.content);
            const sectionHasAssignedMedia = sectionPlaceholders.some(placeholder => {
                const placeholderKey = placeholder.toLowerCase();
                return assignments[placeholderKey] && assignments[placeholderKey].length > 0;
            });
            // If section has assigned media OR is in reshuffle mode, keep it expanded
            if (sectionHasAssignedMedia || (dialogReshuffleMode && window.dialogSectionExpandedState[section.id])) {
                window.dialogSectionExpandedState[section.id] = true;
            }
        });
        
        // Immediately apply stored state after HTML is set
        requestAnimationFrame(() => {
            sectionData.sections.forEach(section => {
                const shouldBeExpanded = window.dialogSectionExpandedState[section.id] || false;
                if (shouldBeExpanded || dialogReshuffleMode) {
                    const sectionContent = preview.querySelector(`.dialog-section-content[data-section-id="${section.id}"]`);
                    const sectionHeader = preview.querySelector(`.dialog-section-header[onclick*="${section.id}"]`);
                    const icon = sectionHeader ? sectionHeader.querySelector('.dialog-section-icon') : null;
                    
                    if (sectionContent) {
                        sectionContent.style.display = 'block';
                        sectionContent.style.setProperty('display', 'block', 'important');
                        if (icon) icon.textContent = '▼';
                    }
                }
            });
        });
    }
    
    // Force delete buttons to be visible in dialog (also in setTimeout to ensure they stay visible)
    setTimeout(() => {
        if (window.currentPlaceholderDialog) {
            const deleteButtons = preview.querySelectorAll('.dialog-delete-btn, .remove-media-btn');
            deleteButtons.forEach(btn => {
                btn.style.setProperty('display', 'flex', 'important');
                btn.style.setProperty('visibility', 'visible', 'important');
                btn.style.setProperty('opacity', '1', 'important');
                btn.style.setProperty('position', 'absolute', 'important');
                btn.style.setProperty('top', '5px', 'important');
                btn.style.setProperty('right', '5px', 'important');
                btn.style.setProperty('z-index', '100', 'important');
            });
        }
    }, 100);

    // If reshuffle mode is active, re-apply it to the new cells
    if (dialogReshuffleMode) {
        // Use setTimeout to ensure DOM is ready for cell manipulation
        setTimeout(() => {
            const cells = preview.querySelectorAll('.media-cell');
            cells.forEach(cell => {
                const hasContent = cell.querySelector('img') || (cell.querySelector('div') && cell.querySelector('div').textContent.trim());
                if (hasContent) {
                    cell.draggable = true;
                    cell.style.border = '2px solid #43e97b';
                    cell.style.cursor = 'grab';
                    
                    // Add drag start handler if not already present
                    if (!cell.hasAttribute('data-drag-handler-added')) {
                        cell.addEventListener('dragstart', function(e) {
                            const mediaIndex = parseInt(this.dataset.mediaIndex);
                            const placeholder = this.dataset.placeholder;
                            handleTableCellDragStart(e, mediaIndex, placeholder);
                        });
                        cell.setAttribute('data-drag-handler-added', 'true');
                    }
                    
                    // Ensure delete button is visible
                    const deleteBtn = cell.querySelector('.remove-media-btn, .dialog-delete-btn');
                    if (deleteBtn) {
                        deleteBtn.style.setProperty('display', 'flex', 'important');
                        deleteBtn.style.setProperty('visibility', 'visible', 'important');
                        deleteBtn.style.setProperty('opacity', '1', 'important');
                    }
                }
            });
            
            // Double-check sections are still expanded (in case something collapsed them)
            const assignmentsAfter = getCurrentAssignments();
            const textEditorAfter = document.getElementById('observationTextEditor');
            const textAfter = textEditorAfter ? textEditorAfter.value : '';
            const sectionDataAfter = parseSections(textAfter);
            
            if (sectionDataAfter.hasSections) {
                sectionDataAfter.sections.forEach(section => {
                    const sectionPlaceholders = extractPlaceholders(section.content);
                    const hasAssignedMedia = sectionPlaceholders.some(placeholder => {
                        const placeholderKey = placeholder.toLowerCase();
                        return assignmentsAfter[placeholderKey] && assignmentsAfter[placeholderKey].length > 0;
                    });
                    
                    if (hasAssignedMedia) {
                        const sectionContent = preview.querySelector(`.dialog-section-content[data-section-id="${section.id}"]`);
                        const sectionHeader = preview.querySelector(`.dialog-section-header[onclick*="${section.id}"]`);
                        const icon = sectionHeader ? sectionHeader.querySelector('.dialog-section-icon') : null;
                        
                        if (sectionContent && sectionContent.style.display !== 'block') {
                            sectionContent.style.display = 'block';
                            sectionContent.style.setProperty('display', 'block', 'important');
                        }
                        if (icon && icon.textContent !== '▼') {
                            icon.textContent = '▼';
                        }
                    }
                });
            }
        }, 50);
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

        // Regenerate preview with sections expanded (this ensures HTML is correct)
        updateDialogPreview();
        
        // Then immediately force-expand sections with assigned media (double-check)
        setTimeout(() => {
            const assignments = getCurrentAssignments();
            const textEditor = document.getElementById('observationTextEditor');
            const text = textEditor ? textEditor.value : '';
            const sectionData = parseSections(text);
            
            if (sectionData.hasSections && preview) {
                sectionData.sections.forEach(section => {
                    const sectionPlaceholders = extractPlaceholders(section.content);
                    const hasAssignedMedia = sectionPlaceholders.some(placeholder => {
                        const placeholderKey = placeholder.toLowerCase();
                        return assignments[placeholderKey] && assignments[placeholderKey].length > 0;
                    });
                    
                    if (hasAssignedMedia) {
                        const sectionContent = preview.querySelector(`.dialog-section-content[data-section-id="${section.id}"]`);
                        const sectionHeader = preview.querySelector(`.dialog-section-header[onclick*="${section.id}"]`);
                        const icon = sectionHeader ? sectionHeader.querySelector('.dialog-section-icon') : null;
                        
                        if (sectionContent) {
                            sectionContent.style.display = 'block';
                            sectionContent.style.setProperty('display', 'block', 'important');
                            console.log('[RESHUFFLE] Force-expanded dialog section:', section.id);
                        }
                        if (icon) {
                            icon.textContent = '▼';
                        }
                    }
                });
            }
        }, 100);

        // Add visual indicators and make cells draggable
        const cells = preview ? preview.querySelectorAll('.media-cell') : [];
        console.log('[RESHUFFLE] Found', cells.length, 'media cells in dialog');
        let updatedCount = 0;
        cells.forEach(cell => {
            const hasContent = cell.querySelector('img') || (cell.querySelector('div') && cell.querySelector('div').textContent.trim());
            if (hasContent) {
                // Make cell draggable
                cell.draggable = true;
                cell.style.border = '2px solid #43e97b';
                cell.style.cursor = 'grab';
                
                // Add drag start handler if not already present
                if (!cell.hasAttribute('data-drag-handler-added')) {
                    cell.addEventListener('dragstart', function(e) {
                        const mediaIndex = parseInt(this.dataset.mediaIndex);
                        const placeholder = this.dataset.placeholder;
                        handleTableCellDragStart(e, mediaIndex, placeholder);
                    });
                    cell.setAttribute('data-drag-handler-added', 'true');
                }
                updatedCount++;
            }
        });
        console.log('[RESHUFFLE] Updated', updatedCount, 'cells with visual indicators and drag handlers');
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

        // Remove visual indicators and disable dragging
        const cells = preview ? preview.querySelectorAll('.media-cell') : [];
        console.log('[RESHUFFLE] Removing visual indicators from', cells.length, 'cells');
        let removedCount = 0;
        cells.forEach(cell => {
            cell.draggable = false;
            cell.style.border = '';
            cell.style.cursor = '';
            removedCount++;
        });
        console.log('[RESHUFFLE] Removed indicators and disabled dragging from', removedCount, 'cells');
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
window.showDraftPreview = showDraftPreview;
window.closeDraftPreview = closeDraftPreview;
window.updatePreviewDisplay = updatePreviewDisplay;
window.deleteEmptyTable = deleteEmptyTable;
window.exportObservationDocxFromPreview = exportObservationDocxFromPreview;
window.previewUndo = previewUndo;
window.previewRedo = previewRedo;
// togglePreviewSettings removed - settings are now always visible in the 3rd column
window.startResizePreview = startResizePreview;
window.startResizePreview2 = startResizePreview2;
window.updateDraftFromPreview = updateDraftFromPreview;
// ============================================
// Column Resizing Functions
// ============================================

let isResizing = false;
let currentResizer = null;
let startX = 0;
let startLeftWidth = 0;
let startMiddleWidth = 0;
let startRightWidth = 0;

function startColumnResize(e, resizerNum) {
    e.preventDefault();
    isResizing = true;
    currentResizer = resizerNum;
    
    const container = document.querySelector('.observation-media-container');
    const leftPanel = document.querySelector('.observation-media-left-panel');
    const middlePanel = document.querySelector('.observation-media-middle-panel');
    const rightPanel = document.querySelector('.observation-media-right-panel');
    
    startX = e.clientX;
    startLeftWidth = leftPanel.offsetWidth;
    startMiddleWidth = middlePanel.offsetWidth;
    startRightWidth = rightPanel.offsetWidth;
    
    document.addEventListener('mousemove', handleColumnResize);
    document.addEventListener('mouseup', stopColumnResize);
    
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
}

function handleColumnResize(e) {
    if (!isResizing) return;
    
    const container = document.querySelector('.observation-media-container');
    const leftPanel = document.querySelector('.observation-media-left-panel');
    const middlePanel = document.querySelector('.observation-media-middle-panel');
    const rightPanel = document.querySelector('.observation-media-right-panel');
    const containerWidth = container.offsetWidth;
    
    const diff = e.clientX - startX;
    
    if (currentResizer === 1) {
        // Resizing between left and middle
        const newLeftWidth = startLeftWidth + diff;
        const newMiddleWidth = startMiddleWidth - diff;
        
        const minWidth = 200;
        if (newLeftWidth >= minWidth && newMiddleWidth >= minWidth && 
            newLeftWidth <= containerWidth * 0.6 && newMiddleWidth <= containerWidth * 0.6) {
            leftPanel.style.width = newLeftWidth + 'px';
            leftPanel.style.flex = '0 0 ' + newLeftWidth + 'px';
            middlePanel.style.flex = '1';
        }
    } else if (currentResizer === 2) {
        // Resizing between middle and right
        const newMiddleWidth = startMiddleWidth + diff;
        const newRightWidth = startRightWidth - diff;
        
        const minWidth = 250;
        if (newMiddleWidth >= minWidth && newRightWidth >= minWidth &&
            newMiddleWidth <= containerWidth * 0.6 && newRightWidth <= containerWidth * 0.6) {
            middlePanel.style.width = newMiddleWidth + 'px';
            middlePanel.style.flex = '0 0 ' + newMiddleWidth + 'px';
            rightPanel.style.flex = '1';
        }
    }
}

function stopColumnResize() {
    if (!isResizing) return;
    
    isResizing = false;
    currentResizer = null;
    
    document.removeEventListener('mousemove', handleColumnResize);
    document.removeEventListener('mouseup', stopColumnResize);
    
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
    
    // Save column widths to localStorage
    saveColumnWidths();
}

function saveColumnWidths() {
    const leftPanel = document.querySelector('.observation-media-left-panel');
    const middlePanel = document.querySelector('.observation-media-middle-panel');
    const rightPanel = document.querySelector('.observation-media-right-panel');
    
    if (leftPanel && middlePanel && rightPanel) {
        const widths = {
            left: leftPanel.offsetWidth,
            middle: middlePanel.offsetWidth,
            right: rightPanel.offsetWidth
        };
        localStorage.setItem('observationMediaColumnWidths', JSON.stringify(widths));
    }
}

function loadColumnWidths() {
    const saved = localStorage.getItem('observationMediaColumnWidths');
    if (saved) {
        try {
            const widths = JSON.parse(saved);
            const leftPanel = document.querySelector('.observation-media-left-panel');
            const middlePanel = document.querySelector('.observation-media-middle-panel');
            const rightPanel = document.querySelector('.observation-media-right-panel');
            
            if (leftPanel && middlePanel && rightPanel && widths.left && widths.middle && widths.right) {
                leftPanel.style.flex = '0 0 ' + widths.left + 'px';
                middlePanel.style.flex = '0 0 ' + widths.middle + 'px';
                rightPanel.style.flex = '0 0 ' + widths.right + 'px';
            }
        } catch (e) {
            console.error('Error loading column widths:', e);
        }
    }
}

// ============================================
// Standards Loading and Display Functions
// ============================================

let currentStandardsData = null;

async function loadStandardsFromDraft(draft) {
    const standardsContent = document.getElementById('standardsContent');
    
    console.log('Loading standards from draft:', draft);
    
    if (!draft || !draft.json_file_id) {
        console.log('No json_file_id in draft:', draft);
        standardsContent.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No JSON Standards File assigned to this draft.</p>';
        currentStandardsData = null;
        return;
    }
    
    standardsContent.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Loading standards...</p>';
    
    try {
        const url = `/v2p-formatter/ac-matrix/json-files/${draft.json_file_id}`;
        console.log('Fetching JSON file from:', url);
        
        const response = await fetch(url);
        console.log('Response status:', response.status, response.statusText);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Response error:', errorText);
            throw new Error(`Failed to load JSON file: ${response.status} ${response.statusText}`);
        }
        
        const jsonData = await response.json();
        console.log('JSON data received:', jsonData);
        currentStandardsData = jsonData;
        renderStandards(jsonData);
    } catch (error) {
        console.error('Error loading standards:', error);
        console.error('Error details:', {
            message: error.message,
            stack: error.stack,
            draft: draft
        });
        standardsContent.innerHTML = `<p style="color: #ff6b6b; text-align: center; padding: 20px;">Error loading standards: ${error.message || 'Unknown error'}. Check console for details.</p>`;
        currentStandardsData = null;
    }
}

function renderStandards(jsonData) {
    const standardsContent = document.getElementById('standardsContent');
    
    // Clear any active search when rendering new standards
    clearStandardsSearch();
    
    if (!jsonData || !jsonData.qualifications || jsonData.qualifications.length === 0) {
        standardsContent.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No standards data available.</p>';
        return;
    }
    
    let html = '';
    let unitIndex = 0;
    
    // Extract all units from all qualifications
    jsonData.qualifications.forEach(qualification => {
        if (qualification.units && qualification.units.length > 0) {
            qualification.units.forEach(unit => {
                html += renderUnit(unit, unitIndex);
                unitIndex++;
            });
        }
    });
    
    if (html === '') {
        standardsContent.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No units found in standards file.</p>';
        return;
    }
    
    standardsContent.innerHTML = html;
}

function renderUnit(unit, unitIndex) {
    const unitId = unit.unit_id || unit.unit_internal_id || 'Unknown';
    const unitName = unit.unit_name || 'Unnamed Unit';
    
    // Get draft text to check for AC coverage
    const textEditor = document.getElementById('observationTextEditor');
    const draftText = textEditor ? textEditor.value : '';
    const sectionData = parseSections(draftText);
    
    let html = `<div class="standards-unit" data-unit-index="${unitIndex % 8}" data-unit-id="${unitId}">`;
    html += `<div class="standards-unit-header" onclick="toggleStandardsUnit(this)">`;
    html += `<span class="standards-unit-icon">▶</span>`;
    html += `<span class="standards-unit-title">${unitId}: ${escapeHtml(unitName)}</span>`;
    html += `</div>`;
    html += `<div class="standards-unit-content">`;
    
    // Extract all ACs directly from all learning outcomes (no LO display)
    if (unit.learning_outcomes && unit.learning_outcomes.length > 0) {
        unit.learning_outcomes.forEach(lo => {
            if (lo.questions && lo.questions.length > 0) {
                lo.questions.forEach(question => {
                    const acId = question.question_id || '';
                    const acText = question.question_name || '';
                    const acType = question.question_type || 'Other';
                    
                    // Check if AC is covered in any section (unit-specific matching)
                    const coveredSections = [];
                    if (sectionData.hasSections && acId && unitId) {
                        // Escape unit ID and AC ID for regex
                        const escapedUnitId = unitId.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                        const escapedAcId = acId.replace(/\./g, '\\.');
                        
                        for (const section of sectionData.sections) {
                            const sectionContent = section.content;
                            let matches = false;
                            
                            // Pattern 1: Explicit unit:AC format (641:1.1, 641:1.2, etc.)
                            const explicitPattern = new RegExp(`${escapedUnitId}\\s*[:.]\\s*${escapedAcId}\\b`, 'i');
                            if (explicitPattern.test(sectionContent)) {
                                matches = true;
                            }
                            
                            // Pattern 2: Unit mentioned, then ACs listed (641:1.1, 1.2, 1.3 where 1.2 and 1.3 are from 641)
                            // Look for pattern like "641:1.1" or "Unit 641" followed by AC list containing our AC
                            if (!matches) {
                                // Find where unit 641 is mentioned, then check if AC appears nearby
                                const unitMentionPattern = new RegExp(`${escapedUnitId}\\s*[:.]\\s*[\\d.]+(?:\\s*,\\s*[\\d.]+)*`, 'i');
                                const unitMentionMatch = sectionContent.match(unitMentionPattern);
                                if (unitMentionMatch) {
                                    // Check if our AC ID appears in the same context (within the same AC list)
                                    const acListPattern = new RegExp(`${escapedUnitId}\\s*[:.]\\s*[\\d.]+(?:\\s*,\\s*[\\d.]+)*`, 'gi');
                                    const acLists = sectionContent.matchAll(acListPattern);
                                    for (const acList of acLists) {
                                        // Check if our AC ID is in this list (could be explicit like 641:1.2 or shorthand like 1.2)
                                        const listContent = acList[0];
                                        // Check for explicit match first
                                        if (new RegExp(`${escapedUnitId}\\s*[:.]\\s*${escapedAcId}\\b`, 'i').test(listContent)) {
                                            matches = true;
                                            break;
                                        }
                                        // Check for shorthand match (1.2 after 641:1.1)
                                        if (new RegExp(`(?:^|,)\\s*${escapedAcId}\\b`, 'i').test(listContent)) {
                                            matches = true;
                                            break;
                                        }
                                    }
                                }
                            }
                            
                            // Pattern 3: "Unit 641 AC 1.1" or "641 AC 1.1" format
                            if (!matches) {
                                const unitAcPattern = new RegExp(`(?:Unit\\s+)?${escapedUnitId}\\s+(?:AC\\s+)?${escapedAcId}\\b`, 'i');
                                if (unitAcPattern.test(sectionContent)) {
                                    matches = true;
                                }
                            }
                            
                            // Pattern 4: "AC 641:1.1" format
                            if (!matches) {
                                const acUnitPattern = new RegExp(`AC\\s+${escapedUnitId}\\s*[:.]\\s*${escapedAcId}\\b`, 'i');
                                if (acUnitPattern.test(sectionContent)) {
                                    matches = true;
                                }
                            }
                            
                            // Pattern 5: "AC covered: 641:1.1, 1.2, 1.3" format - check if AC is in the list
                            // FIXED: Properly parse each "AC covered:" line separately to avoid false positives
                            if (!matches) {
                                // Find all "AC covered:" lines in the section
                                // Pattern matches from "AC covered:" to the next "AC covered:" or end of section
                                // Uses multiline mode to handle cases where AC covered spans multiple lines
                                const acCoveredLinePattern = /AC\s+covered\s*[:.]?\s*([\s\S]*?)(?=\n\s*AC\s+covered\s*[:.]?\s*|$)/gi;
                                const acCoveredLines = [];
                                let match;
                                
                                // Reset regex lastIndex to ensure we start from the beginning
                                acCoveredLinePattern.lastIndex = 0;
                                
                                while ((match = acCoveredLinePattern.exec(sectionContent)) !== null) {
                                    // Include the "AC covered:" prefix in the matched line
                                    const fullLine = match[0].trim();
                                    if (fullLine) {
                                        acCoveredLines.push(fullLine);
                                    }
                                }
                                
                                // Check each "AC covered:" line separately
                                for (const acCoveredLine of acCoveredLines) {
                                    if (parseAcCoveredLine(acCoveredLine, unitId, acId)) {
                                        matches = true;
                                        break;
                                    }
                                }
                            }
                            
                            if (matches) {
                                coveredSections.push(section);
                            }
                        }
                    }
                    
                    html += `<div class="standards-ac" data-ac-type="${escapeHtml(acType)}">`;
                    html += `<div class="standards-ac-id">${escapeHtml(acId)}</div>`;
                    html += `<div class="standards-ac-text">${escapeHtml(acText)}</div>`;
                    
                    // Always show "Covered:..." line for every AC
                    if (coveredSections.length > 0) {
                        // Show all sections that contain this AC as bullet points
                        const sectionBullets = coveredSections.map(section => {
                            const sectionColor = section.color || SECTION_COLORS[section.index % SECTION_COLORS.length];
                            // Use section title if available, otherwise use section ID
                            const sectionLabel = section.title || section.id || `section-${section.index}`;
                            const sectionId = section.id || `section-${section.index}`;
                            // Make section name clickable to expand section in Live Preview (dotted underline)
                            return `<div style="margin-left: 12px; margin-top: 2px;"><span style="color: ${sectionColor}; cursor: pointer; text-decoration: underline; text-decoration-style: dotted;" onclick="expandSectionInPreview('${sectionId}'); event.stopPropagation();">${escapeHtml(sectionLabel)}</span></div>`;
                        }).join('');
                        
                        html += `<div class="standards-ac-covered" style="margin-top: 6px; font-size: 12px; color: #999;">Covered:${sectionBullets}</div>`;
                    } else {
                        // Show "Covered:" with no sections if not covered
                        html += `<div class="standards-ac-covered" style="margin-top: 6px; font-size: 12px; color: #999;">Covered:</div>`;
                    }
                    
                    html += `</div>`;
                });
            }
        });
    }
    
    html += `</div>`;
    html += `</div>`;
    
    return html;
}

function toggleStandardsUnit(header) {
    const unit = header.closest('.standards-unit');
    if (unit) {
        unit.classList.toggle('expanded');
        const icon = header.querySelector('.standards-unit-icon');
        if (icon) {
            icon.textContent = unit.classList.contains('expanded') ? '▼' : '▶';
        }
    }
}

function expandAllStandardsUnits() {
    const units = document.querySelectorAll('.standards-unit');
    units.forEach(unit => {
        unit.classList.add('expanded');
        const icon = unit.querySelector('.standards-unit-icon');
        if (icon) {
            icon.textContent = '▼';
        }
    });
}

function collapseAllStandardsUnits() {
    const units = document.querySelectorAll('.standards-unit');
    units.forEach(unit => {
        unit.classList.remove('expanded');
        const icon = unit.querySelector('.standards-unit-icon');
        if (icon) {
            icon.textContent = '▶';
        }
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Escape special regex characters
 */
function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Parse an "AC covered:" line to check if a specific AC is listed
 * @param {string} line - The "AC covered:" line (including the "AC covered:" prefix)
 * @param {string} targetUnitId - The unit ID to check (e.g., "129v4")
 * @param {string} targetAcId - The AC ID to check (e.g., "5.1")
 * @returns {boolean} - True if the AC is found in this line
 */
function parseAcCoveredLine(line, targetUnitId, targetAcId) {
    // Remove "AC covered:" prefix
    const acList = line.replace(/^AC\s+covered\s*[:.]?\s*/i, '').trim();
    
    if (!acList) {
        return false;
    }
    
    // Escape for regex
    const escapedUnitId = escapeRegex(targetUnitId);
    const escapedAcId = escapeRegex(targetAcId);
    
    // Split by semicolons to get unit blocks
    const blocks = acList.split(';').map(b => b.trim()).filter(b => b.length > 0);
    
    for (const block of blocks) {
        // Check if this block contains our unit
        const unitMatch = block.match(new RegExp(`(${escapedUnitId})\\s*[:.]\\s*`, 'i'));
        
        if (unitMatch) {
            // This block is for our unit
            const acsInBlock = block.substring(unitMatch.index + unitMatch[0].length);
            
            // Check for explicit match: unitId:acId
            const explicitPattern = new RegExp(`${escapedUnitId}\\s*[:.]\\s*${escapedAcId}\\b`, 'i');
            if (explicitPattern.test(block)) {
                return true;
            }
            
            // Check for shorthand match: acId after unitId: (must be in the AC list part)
            // Look for the AC ID as a standalone value (not part of another AC like 5.10)
            // Pattern: start of string, comma, semicolon, or space, followed by our AC ID, followed by word boundary
            const shorthandPattern = new RegExp(`(?:^|[,;]|\\s)${escapedAcId}\\b`, 'i');
            if (shorthandPattern.test(acsInBlock)) {
                return true;
            }
        }
    }
    
    return false;
}

/**
 * Expand a section in Live Preview when clicked from Standards column
 */
function expandSectionInPreview(sectionId) {
    // Toggle the section to expand it (if collapsed) or ensure it's expanded
    if (typeof toggleSection === 'function') {
        // Get current section states
        const states = getSectionStates();
        const currentState = states[sectionId] || false;
        
        // If section is collapsed, expand it
        if (!currentState) {
            toggleSection(sectionId);
        } else {
            // If already expanded, scroll to it
            const sectionElement = document.querySelector(`[data-section-id="${sectionId}"]`);
            if (sectionElement) {
                sectionElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }
        
        // Scroll Live Preview into view if needed
        const previewElement = document.getElementById('observationPreview');
        if (previewElement) {
            previewElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }
}

// Clear standards when draft is cleared
function clearStandards() {
    const standardsContent = document.getElementById('standardsContent');
    if (standardsContent) {
        standardsContent.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No draft loaded. Load a draft to view standards.</p>';
    }
    currentStandardsData = null;
    // Clear search when standards are cleared
    clearStandardsSearch();
}

// ============================================
// Standards Search Functions
// ============================================

let standardsSearchDebounceTimer = null;
let previousUnitStates = {}; // Store unit states before search

function handleStandardsSearch(searchTerm) {
    const clearBtn = document.getElementById('standardsSearchClear');
    if (clearBtn) {
        clearBtn.style.display = searchTerm.trim() ? 'block' : 'none';
    }
    
    // Debounce search (300ms)
    clearTimeout(standardsSearchDebounceTimer);
    standardsSearchDebounceTimer = setTimeout(() => {
        performStandardsSearch(searchTerm);
    }, 300);
}

function performStandardsSearch(searchTerm) {
    if (!searchTerm || searchTerm.trim() === '') {
        clearStandardsSearch();
        return;
    }
    
    const trimmedTerm = searchTerm.trim();
    const isExactPhrase = trimmedTerm.startsWith('"') && trimmedTerm.endsWith('"') && trimmedTerm.length > 2;
    const searchTermLower = isExactPhrase 
        ? trimmedTerm.slice(1, -1).toLowerCase() 
        : trimmedTerm.toLowerCase();
    
    const units = document.querySelectorAll('.standards-unit');
    let hasMatches = false;
    let firstMatchElement = null;
    
    // Store unit states if first search
    if (Object.keys(previousUnitStates).length === 0) {
        units.forEach(unit => {
            const unitId = unit.getAttribute('data-unit-id');
            previousUnitStates[unitId] = unit.classList.contains('expanded');
        });
    }
    
    units.forEach(unit => {
        const acs = unit.querySelectorAll('.standards-ac');
        let unitHasMatch = false;
        
        acs.forEach(acElement => {
            const acTextElement = acElement.querySelector('.standards-ac-text');
            if (!acTextElement) return;
            
            // Get original text before removing highlights (in case it's already highlighted)
            const acText = acTextElement.textContent || acTextElement.innerText || '';
            
            // Remove previous highlights
            removeHighlights(acTextElement);
            
            // Get clean text after removing highlights
            const cleanText = acTextElement.textContent || acTextElement.innerText || acText;
            const acTextLower = cleanText.toLowerCase();
            let matches = false;
            
            if (isExactPhrase) {
                // Exact phrase match (case-insensitive)
                matches = acTextLower.includes(searchTermLower);
            } else {
                // Multiple words: all must be present (AND logic, case-insensitive)
                const words = searchTermLower.split(/\s+/).filter(w => w.length > 0);
                matches = words.every(word => acTextLower.includes(word));
            }
            
            if (matches) {
                unitHasMatch = true;
                // Show this AC
                acElement.style.display = 'block';
                if (!firstMatchElement) {
                    firstMatchElement = acElement.closest('.standards-unit');
                }
                // Use original text for highlighting to preserve formatting
                highlightText(acTextElement, cleanText, searchTermLower, isExactPhrase);
            } else {
                // Hide ACs that don't match
                acElement.style.display = 'none';
            }
        });
        
        // Expand/collapse unit based on matches
        if (unitHasMatch) {
            expandStandardsUnit(unit);
            hasMatches = true;
        } else {
            collapseStandardsUnit(unit);
        }
    });
    
    // Show no results message if no matches
    const standardsContent = document.getElementById('standardsContent');
    const noResultsMsg = standardsContent.querySelector('.standards-no-results');
    if (!hasMatches) {
        if (!noResultsMsg) {
            const msg = document.createElement('div');
            msg.className = 'standards-no-results';
            msg.textContent = `No results found for "${trimmedTerm}"`;
            standardsContent.insertBefore(msg, standardsContent.firstChild);
        } else {
            noResultsMsg.textContent = `No results found for "${trimmedTerm}"`;
        }
    } else {
        if (noResultsMsg) {
            noResultsMsg.remove();
        }
        // Scroll to first match
        if (firstMatchElement) {
            setTimeout(() => {
                firstMatchElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 100);
        }
    }
}

function highlightText(element, originalText, searchTerm, isExactPhrase) {
    if (!originalText || !searchTerm) {
        return;
    }
    
    const textLower = originalText.toLowerCase();
    
    if (isExactPhrase) {
        // Highlight exact phrase (case-insensitive match, but preserve original case)
        const index = textLower.indexOf(searchTerm);
        if (index !== -1) {
            const before = escapeHtml(originalText.substring(0, index));
            const match = escapeHtml(originalText.substring(index, index + searchTerm.length));
            const after = escapeHtml(originalText.substring(index + searchTerm.length));
            element.innerHTML = before + 
                '<span class="standards-search-highlight">' + match + '</span>' + 
                after;
        } else {
            element.innerHTML = escapeHtml(originalText);
        }
    } else {
        // Highlight all words (case-insensitive, preserve original case)
        const words = searchTerm.split(/\s+/).filter(w => w.length > 0);
        let highlightedText = escapeHtml(originalText);
        
        // Find and highlight each word (case-insensitive)
        // Process words to avoid highlighting within HTML tags
        words.forEach(word => {
            // Escape special regex characters
            const escapedWord = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            // Match word boundaries, but avoid matching inside HTML tags
            // Simple approach: match word boundaries
            const regex = new RegExp(`\\b(${escapedWord})\\b`, 'gi');
            // Replace only if not inside an HTML tag
            highlightedText = highlightedText.replace(regex, (match, p1, offset) => {
                // Check if we're inside an HTML tag by looking backwards
                const beforeMatch = highlightedText.substring(0, offset);
                const lastTagStart = beforeMatch.lastIndexOf('<');
                const lastTagEnd = beforeMatch.lastIndexOf('>');
                // If last < is after last >, we're inside a tag
                if (lastTagStart > lastTagEnd) {
                    return match; // Don't highlight inside tags
                }
                return '<span class="standards-search-highlight">' + p1 + '</span>';
            });
        });
        
        element.innerHTML = highlightedText;
    }
}

function removeHighlights(element) {
    // Remove highlight spans and restore plain text
    const highlights = element.querySelectorAll('.standards-search-highlight');
    highlights.forEach(highlight => {
        const parent = highlight.parentNode;
        if (parent) {
            parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
            parent.normalize();
        }
    });
    // Also handle nested highlights
    if (element.innerHTML) {
        element.innerHTML = element.textContent;
    }
}

function expandStandardsUnit(unit) {
    if (unit && !unit.classList.contains('expanded')) {
        unit.classList.add('expanded');
        const icon = unit.querySelector('.standards-unit-icon');
        if (icon) {
            icon.textContent = '▼';
        }
    }
}

function collapseStandardsUnit(unit) {
    if (unit && unit.classList.contains('expanded')) {
        unit.classList.remove('expanded');
        const icon = unit.querySelector('.standards-unit-icon');
        if (icon) {
            icon.textContent = '▶';
        }
    }
}

function clearStandardsSearch() {
    const searchInput = document.getElementById('standardsSearchInput');
    const clearBtn = document.getElementById('standardsSearchClear');
    
    if (searchInput) {
        searchInput.value = '';
    }
    if (clearBtn) {
        clearBtn.style.display = 'none';
    }
    
    // Show all ACs (remove display:none)
    const allAcs = document.querySelectorAll('.standards-ac');
    allAcs.forEach(ac => {
        ac.style.display = '';
    });
    
    // Remove all highlights
    const highlightedElements = document.querySelectorAll('.standards-search-highlight');
    highlightedElements.forEach(highlight => {
        const parent = highlight.parentNode;
        if (parent) {
            parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
            parent.normalize();
        }
    });
    
    // Remove no results message
    const noResultsMsg = document.querySelector('.standards-no-results');
    if (noResultsMsg) {
        noResultsMsg.remove();
    }
    
    // Restore unit states
    const units = document.querySelectorAll('.standards-unit');
    units.forEach(unit => {
        const unitId = unit.getAttribute('data-unit-id');
        const wasExpanded = previousUnitStates[unitId] || false;
        if (wasExpanded) {
            expandStandardsUnit(unit);
        } else {
            collapseStandardsUnit(unit);
        }
    });
    
    // Clear stored states
    previousUnitStates = {};
}

window.handleStandardsSearch = handleStandardsSearch;
window.loadStandardsFromDraft = loadStandardsFromDraft;
window.clearStandardsSearch = clearStandardsSearch;

window.showSaveDraftDialog = showSaveDraftDialog;
window.showEnhancedDraftDialog = showEnhancedDraftDialog;
window.closeEnhancedDraftDialog = closeEnhancedDraftDialog;
window.saveDraftFromDialog = saveDraftFromDialog;
window.selectAllDraftDialogUnits = selectAllDraftDialogUnits;
window.deselectAllDraftDialogUnits = deselectAllDraftDialogUnits;
window.showSaveDraftDialog = showSaveDraftDialog;
window.showLoadDraftDialog = showLoadDraftDialog;
window.showDraftSelectionDialog = showDraftSelectionDialog;
window.saveDraft = saveDraft;
window.loadDraft = loadDraft;
window.deleteDraft = deleteDraft;
window.closeDraftDialog = closeDraftDialog;
window.toggleSection = toggleSection;
window.expandAllSections = expandAllSections;
window.startColumnResize = startColumnResize;
window.expandAllStandardsUnits = expandAllStandardsUnits;
window.collapseAllStandardsUnits = collapseAllStandardsUnits;
window.toggleStandardsUnit = toggleStandardsUnit;
window.expandSectionInPreview = expandSectionInPreview;
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

/**
 * Handle media name click to enable inline editing
 */
function handleMediaNameClick(event, element) {
    // Stop event propagation to prevent card click
    event.stopPropagation();
    
    const mediaPath = element.dataset.mediaPath;
    const currentName = element.dataset.mediaName;
    
    // Extract name without extension
    const nameParts = currentName.split('.');
    const extension = nameParts.length > 1 ? '.' + nameParts.pop() : '';
    const nameWithoutExt = nameParts.join('.');
    
    // Create input element
    const input = document.createElement('input');
    input.type = 'text';
    input.value = nameWithoutExt;
    input.style.cssText = `
        background: #1e1e1e;
        color: #e0e0e0;
        border: 2px solid #667eea;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 14px;
        width: 100%;
        font-family: inherit;
    `;
    
    // Replace element content with input
    element.innerHTML = '';
    element.appendChild(input);
    input.focus();
    input.select();
    
    // Handle save on Enter or blur
    const saveName = async () => {
        const newName = input.value.trim();
        
        // Validate name
        if (!newName) {
            // Restore original name
            element.textContent = currentName;
            element.dataset.mediaName = currentName;
            return;
        }
        
        // Check if name changed
        if (newName === nameWithoutExt) {
            // No change, restore original
            element.textContent = currentName;
            element.dataset.mediaName = currentName;
            return;
        }
        
        // Sanitize name (remove invalid characters)
        const sanitizedName = newName.replace(/[<>:"|?*\x00-\x1f]/g, '');
        if (sanitizedName !== newName) {
            alert('Invalid characters removed from file name.');
        }
        
        if (!sanitizedName) {
            element.textContent = currentName;
            element.dataset.mediaName = currentName;
            return;
        }
        
        // Show loading state
        element.textContent = 'Renaming...';
        element.style.color = '#999';
        
        try {
            // Call rename API
            const response = await fetch('/v2p-formatter/media-converter/observation-media/rename-file', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    file_path: mediaPath,
                    new_name: sanitizedName
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Update element with new name
                element.textContent = data.new_name;
                element.dataset.mediaName = data.new_name;
                element.title = data.new_name;
                element.style.color = '#e0e0e0';
                
                // Update card dataset
                const card = element.closest('.observation-media-card');
                if (card) {
                    card.dataset.mediaName = data.new_name;
                    card.dataset.mediaPath = data.new_path;
                }
                
                // Update media data if it exists in window
                if (window.observationMediaData) {
                    // Find and update the media in the data structure
                    for (const subfolder in window.observationMediaData) {
                        const mediaList = window.observationMediaData[subfolder];
                        const mediaIndex = mediaList.findIndex(m => m.path === mediaPath);
                        if (mediaIndex !== -1) {
                            mediaList[mediaIndex].name = data.new_name;
                            mediaList[mediaIndex].path = data.new_path;
                            break;
                        }
                    }
                }
                
                // Show success message briefly
                const originalColor = element.style.color;
                element.style.color = '#4ecdc4';
                setTimeout(() => {
                    element.style.color = originalColor;
                }, 1000);
            } else {
                // Show error and restore original name
                alert(`Error renaming file: ${data.error || 'Unknown error'}`);
                element.textContent = currentName;
                element.dataset.mediaName = currentName;
                element.style.color = '#e0e0e0';
            }
        } catch (error) {
            console.error('Error renaming file:', error);
            alert(`Error renaming file: ${error.message}`);
            element.textContent = currentName;
            element.dataset.mediaName = currentName;
            element.style.color = '#e0e0e0';
        }
    };
    
    // Save on Enter key
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            input.blur();
        } else if (e.key === 'Escape') {
            e.preventDefault();
            element.textContent = currentName;
            element.dataset.mediaName = currentName;
        }
    });
    
    // Save on blur
    input.addEventListener('blur', saveName);
}

// Make function globally available
window.handleMediaNameClick = handleMediaNameClick;

/**
 * Handle media name click to enable inline editing
 */
function handleMediaNameClick(event, element) {
    // Stop event propagation to prevent card click
    event.stopPropagation();
    
    const mediaPath = element.dataset.mediaPath;
    const currentName = element.dataset.mediaName;
    
    // Extract name without extension
    const nameParts = currentName.split('.');
    const extension = nameParts.length > 1 ? '.' + nameParts.pop() : '';
    const nameWithoutExt = nameParts.join('.');
    
    // Create input element
    const input = document.createElement('input');
    input.type = 'text';
    input.value = nameWithoutExt;
    input.style.cssText = `
        background: #1e1e1e;
        color: #e0e0e0;
        border: 2px solid #667eea;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 14px;
        width: 100%;
        font-family: inherit;
    `;
    
    // Replace element content with input
    element.innerHTML = '';
    element.appendChild(input);
    input.focus();
    input.select();
    
    // Handle save on Enter or blur
    const saveName = async () => {
        const newName = input.value.trim();
        
        // Validate name
        if (!newName) {
            // Restore original name
            element.textContent = currentName;
            element.dataset.mediaName = currentName;
            return;
        }
        
        // Check if name changed
        if (newName === nameWithoutExt) {
            // No change, restore original
            element.textContent = currentName;
            element.dataset.mediaName = currentName;
            return;
        }
        
        // Sanitize name (remove invalid characters)
        const sanitizedName = newName.replace(/[<>:"|?*\x00-\x1f]/g, '');
        if (sanitizedName !== newName) {
            alert('Invalid characters removed from file name.');
        }
        
        if (!sanitizedName) {
            element.textContent = currentName;
            element.dataset.mediaName = currentName;
            return;
        }
        
        // Show loading state
        element.textContent = 'Renaming...';
        element.style.color = '#999';
        
        try {
            // Call rename API
            const response = await fetch('/v2p-formatter/media-converter/observation-media/rename-file', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    file_path: mediaPath,
                    new_name: sanitizedName
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Update element with new name
                element.textContent = data.new_name;
                element.dataset.mediaName = data.new_name;
                element.title = data.new_name;
                element.style.color = '#e0e0e0';
                
                // Update card dataset
                const card = element.closest('.observation-media-card');
                if (card) {
                    card.dataset.mediaName = data.new_name;
                    card.dataset.mediaPath = data.new_path;
                }
                
                // Update media data if it exists in window
                if (window.observationMediaData) {
                    // Find and update the media in the data structure
                    for (const subfolder in window.observationMediaData) {
                        const mediaList = window.observationMediaData[subfolder];
                        const mediaIndex = mediaList.findIndex(m => m.path === mediaPath);
                        if (mediaIndex !== -1) {
                            mediaList[mediaIndex].name = data.new_name;
                            mediaList[mediaIndex].path = data.new_path;
                            break;
                        }
                    }
                }
                
                // Show success message briefly
                const originalColor = element.style.color;
                element.style.color = '#4ecdc4';
                setTimeout(() => {
                    element.style.color = originalColor;
                }, 1000);
            } else {
                // Show error and restore original name
                alert(`Error renaming file: ${data.error || 'Unknown error'}`);
                element.textContent = currentName;
                element.dataset.mediaName = currentName;
                element.style.color = '#e0e0e0';
            }
        } catch (error) {
            console.error('Error renaming file:', error);
            alert(`Error renaming file: ${error.message}`);
            element.textContent = currentName;
            element.dataset.mediaName = currentName;
            element.style.color = '#e0e0e0';
        }
    };
    
    // Save on Enter key
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            input.blur();
        } else if (e.key === 'Escape') {
            e.preventDefault();
            element.textContent = currentName;
            element.dataset.mediaName = currentName;
        }
    });
    
    // Save on blur
    input.addEventListener('blur', saveName);
}

// Make function globally available
window.handleMediaNameClick = handleMediaNameClick;


/**
 * Play audio file in a modal dialog
 */
function playAudioFile(audioPath, audioName) {
    // Create modal overlay
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        animation: fadeIn 0.2s ease-in;
    `;
    
    // Create modal content
    const content = document.createElement('div');
    content.style.cssText = `
        background: #1e1e1e;
        border: 2px solid #667eea;
        border-radius: 8px;
        padding: 30px;
        max-width: 500px;
        width: 90%;
        text-align: center;
    `;
    
    // Audio player
    const audio = document.createElement('audio');
    audio.controls = true;
    audio.style.cssText = 'width: 100%; margin: 20px 0;';
    audio.src = `/v2p-formatter/media-converter/audio-file?path=${audioPath}`;
    
    // Title
    const title = document.createElement('div');
    title.style.cssText = 'color: #e0e0e0; font-size: 18px; font-weight: bold; margin-bottom: 10px;';
    title.textContent = audioName;
    
    // Close button
    const closeBtn = document.createElement('button');
    closeBtn.textContent = 'Close';
    closeBtn.style.cssText = `
        margin-top: 20px;
        padding: 10px 20px;
        background: #667eea;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
    `;
    closeBtn.onclick = () => {
        audio.pause();
        document.body.removeChild(modal);
    };
    
    // Close on overlay click
    modal.onclick = (e) => {
        if (e.target === modal) {
            audio.pause();
            document.body.removeChild(modal);
        }
    };
    
    content.appendChild(title);
    content.appendChild(audio);
    content.appendChild(closeBtn);
    modal.appendChild(content);
    document.body.appendChild(modal);
    
    // Auto-play
    audio.play().catch(e => {
        console.log('Auto-play prevented:', e);
    });
}

// Make function globally available
window.playAudioFile = playAudioFile;

} // Close if (typeof window !== 'undefined') block


