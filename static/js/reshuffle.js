/**
 * Reshuffle Library - Standalone
 * Handles reordering media within placeholder tables
 */

(function() {
    'use strict';
    
    /**
     * Reorder media within a placeholder
     * @param {string} placeholder - The placeholder name
     * @param {number} fromIndex - Source index
     * @param {number} toIndex - Target index
     */
    function reorderMedia(placeholder, fromIndex, toIndex) {
        console.log('[RESHUFFLE] reorderMedia called', { placeholder, fromIndex, toIndex });
        
        // Get assignments
        if (!window.observationMediaAssignments) {
            console.error('[RESHUFFLE] No assignments found');
            return false;
        }
        
        const placeholderKey = placeholder.toLowerCase();
        const assignments = window.observationMediaAssignments;
        
        if (!assignments[placeholderKey] || !assignments[placeholderKey][fromIndex]) {
            console.error('[RESHUFFLE] Invalid source', { placeholderKey, fromIndex, length: assignments[placeholderKey]?.length });
            return false;
        }
        
        // Same position - no change
        if (fromIndex === toIndex) {
            console.log('[RESHUFFLE] Same position, no change');
            return false;
        }
        
        // Get the media item
        const media = assignments[placeholderKey][fromIndex];
        console.log('[RESHUFFLE] Moving:', media.name || media.path, 'from', fromIndex, 'to', toIndex);
        
        // Remove from source
        assignments[placeholderKey].splice(fromIndex, 1);
        
        // Adjust target index if needed
        let adjustedToIndex = toIndex;
        if (fromIndex < toIndex) {
            // Moving forward: target index stays the same after removal
            adjustedToIndex = toIndex;
        } else {
            // Moving backward: target index stays the same
            adjustedToIndex = toIndex;
        }
        
        // Insert at target
        assignments[placeholderKey].splice(adjustedToIndex, 0, media);
        
        console.log('[RESHUFFLE] Reorder complete. New order:', 
            assignments[placeholderKey].map((m, i) => `${i}:${m.name || m.path}`));
        
        // Update preview
        if (typeof window.updatePreview === 'function') {
            window.updatePreview();
        }
        
        return true;
    }
    
    /**
     * Handle table cell drag start
     */
    function handleTableCellDragStart(e, mediaIndex, placeholder) {
        console.log('[RESHUFFLE] Drag start', { mediaIndex, placeholder });
        
        if (!window.observationMediaAssignments) {
            console.error('[RESHUFFLE] No assignments available');
            return;
        }
        
        const placeholderKey = placeholder.toLowerCase();
        const assignments = window.observationMediaAssignments;
        const media = assignments[placeholderKey] && assignments[placeholderKey][mediaIndex];
        
        if (!media) {
            console.error('[RESHUFFLE] Media not found', { placeholderKey, mediaIndex });
            return;
        }
        
        const dragData = {
            ...media,
            source: 'table',
            placeholder: placeholder,
            index: mediaIndex
        };
        
        e.dataTransfer.setData('application/json', JSON.stringify(dragData));
        e.dataTransfer.setData('text/plain', JSON.stringify(dragData));
        e.dataTransfer.effectAllowed = 'move';
        
        // Mark as dragging
        if (e.currentTarget) {
            e.currentTarget.classList.add('dragging');
        }
    }
    
    /**
     * Handle table drop
     */
    function handleTableDrop(e, placeholder) {
        console.log('[RESHUFFLE] handleTableDrop called', { 
            placeholder,
            targetTag: e.target?.tagName,
            targetClass: e.target?.className,
            currentTargetTag: e.currentTarget?.tagName,
            currentTargetClass: e.currentTarget?.className
        });
        
        // Get data from dataTransfer first to check if this is a reshuffle
        let dataStr = '';
        try {
            dataStr = e.dataTransfer ? e.dataTransfer.getData('application/json') : '';
        } catch (err) {
            console.warn('[RESHUFFLE] Error getting data:', err);
            // Not a reshuffle - let observation-media.js handle it
            return false;
        }
        
        // If no data, this might be a media browser drop - let observation-media.js handle it
        if (!dataStr) {
            console.log('[RESHUFFLE] No data in dataTransfer - not a reshuffle, delegating to observation-media.js');
            return false;
        }
        
        let data;
        try {
            data = JSON.parse(dataStr);
        } catch (err) {
            console.warn('[RESHUFFLE] Failed to parse data:', err);
            // Not a reshuffle - let observation-media.js handle it
            return false;
        }
        
        console.log('[RESHUFFLE] Drop data:', { source: data.source, placeholder: data.placeholder, index: data.index });
        
        // Only handle reshuffle operations (source === 'table')
        // Everything else should be handled by observation-media.js
        if (data.source === 'table' && data.placeholder && data.index !== undefined) {
            // This is a reshuffle - handle it
            e.preventDefault();
            e.stopPropagation();
            const draggedPlaceholder = data.placeholder.toLowerCase();
            const targetPlaceholder = placeholder.toLowerCase();
            
            if (draggedPlaceholder !== targetPlaceholder) {
                console.warn('[RESHUFFLE] Placeholder mismatch', { dragged: draggedPlaceholder, target: targetPlaceholder });
                return;
            }
            
            // Get target cell index - try multiple methods
            let targetCell = null;
            
            // Method 1: Try closest from target
            if (e.target && e.target.closest) {
                targetCell = e.target.closest('.media-cell');
                if (!targetCell) {
                    targetCell = e.target.closest('td');
                }
                // If target is table, find the cell under the drop point
                if (!targetCell && e.target.tagName === 'TABLE') {
                    // Try to find cell from coordinates if available
                    if (e.clientX && e.clientY) {
                        const elementAtPoint = document.elementFromPoint(e.clientX, e.clientY);
                        if (elementAtPoint) {
                            targetCell = elementAtPoint.closest('.media-cell') || elementAtPoint.closest('td');
                        }
                    }
                }
            }
            
            // Method 2: Check if target itself is a cell
            if (!targetCell && e.target) {
                if (e.target.classList && e.target.classList.contains('media-cell')) {
                    targetCell = e.target;
                } else if (e.target.tagName === 'TD') {
                    targetCell = e.target;
                }
            }
            
            // Method 3: Try currentTarget (the element with ondrop handler)
            if (!targetCell && e.currentTarget) {
                if (e.currentTarget.classList && e.currentTarget.classList.contains('media-cell')) {
                    targetCell = e.currentTarget;
                } else if (e.currentTarget.tagName === 'TD') {
                    targetCell = e.currentTarget;
                } else if (e.currentTarget.closest) {
                    targetCell = e.currentTarget.closest('.media-cell') || e.currentTarget.closest('td');
                }
            }
            
            console.log('[RESHUFFLE] Target cell found:', {
                found: !!targetCell,
                tag: targetCell?.tagName,
                class: targetCell?.className,
                hasDataIndex: targetCell?.dataset?.mediaIndex !== undefined
            });
            
            if (!targetCell) {
                console.warn('[RESHUFFLE] No target cell found', {
                    targetTag: e.target?.tagName,
                    targetClass: e.target?.className,
                    currentTargetTag: e.currentTarget?.tagName,
                    currentTargetClass: e.currentTarget?.className
                });
                return;
            }
            
            // Get index from data attribute
            let targetIndex = null;
            
            // Try dataset first
            if (targetCell.dataset && targetCell.dataset.mediaIndex !== undefined) {
                targetIndex = parseInt(targetCell.dataset.mediaIndex);
            }
            
            // Fallback: try getAttribute
            if ((isNaN(targetIndex) || targetIndex === null) && targetCell.getAttribute) {
                const attrValue = targetCell.getAttribute('data-media-index');
                if (attrValue) {
                    targetIndex = parseInt(attrValue);
                }
            }
            
            // Last resort: find by position in table
            if ((isNaN(targetIndex) || targetIndex === null) && targetCell.closest) {
                const table = targetCell.closest('table');
                if (table) {
                    // Get all cells in the table row
                    const row = targetCell.closest('tr');
                    if (row) {
                        const cellsInRow = Array.from(row.querySelectorAll('td'));
                        const cellPosition = cellsInRow.indexOf(targetCell);
                        
                        // Get all rows
                        const allRows = Array.from(table.querySelectorAll('tr'));
                        const rowIndex = allRows.indexOf(row);
                        
                        // Calculate index: (rowIndex * 2) + cellPosition (assuming 2 columns per row)
                        const calculatedIndex = (rowIndex * 2) + cellPosition;
                        
                        console.log('[RESHUFFLE] Calculated index from position', {
                            rowIndex,
                            cellPosition,
                            calculatedIndex,
                            totalRows: allRows.length
                        });
                        
                        // Verify this makes sense by checking if there's media at this index
                        const assignments = window.observationMediaAssignments || {};
                        const placeholderKey = placeholder.toLowerCase();
                        const mediaList = assignments[placeholderKey] || [];
                        
                        if (calculatedIndex >= 0 && calculatedIndex <= mediaList.length) {
                            targetIndex = calculatedIndex;
                            console.log('[RESHUFFLE] Using calculated index:', targetIndex);
                        } else {
                            // Try finding by counting all cells with data-media-index before this one
                            const allCells = Array.from(table.querySelectorAll('.media-cell'));
                            let count = 0;
                            for (let i = 0; i < allCells.length; i++) {
                                if (allCells[i] === targetCell) {
                                    targetIndex = count;
                                    break;
                                }
                                const cellIndex = allCells[i].dataset?.mediaIndex;
                                if (cellIndex !== undefined) {
                                    count = Math.max(count, parseInt(cellIndex) + 1);
                                } else {
                                    count++;
                                }
                            }
                        }
                    }
                }
            }
            
            if (isNaN(targetIndex) || targetIndex === null || targetIndex < 0) {
                console.warn('[RESHUFFLE] Invalid target index', {
                    targetIndex,
                    cellDataset: targetCell.dataset,
                    cellTag: targetCell.tagName,
                    cellClass: targetCell.className,
                    cellAttributes: targetCell.getAttribute ? {
                        'data-media-index': targetCell.getAttribute('data-media-index'),
                        'data-placeholder': targetCell.getAttribute('data-placeholder')
                    } : 'no getAttribute'
                });
                return;
            }
            
            const fromIndex = parseInt(data.index);
            const toIndex = targetIndex;
            
            console.log('[RESHUFFLE] Reordering from', fromIndex, 'to', toIndex);
            
            // Perform reorder
            const success = reorderMedia(placeholder, fromIndex, toIndex);
            
            if (success) {
                console.log('[RESHUFFLE] Reorder successful');
            } else {
                console.warn('[RESHUFFLE] Reorder failed');
            }
            
            return true; // Reshuffle handled
        }
        
        // Not a reshuffle - return false to let observation-media.js handle it
        console.log('[RESHUFFLE] Not a reshuffle operation, delegating to observation-media.js');
        return false;
    }
    
    /**
     * Handle table drag over
     */
    function handleTableDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        
        if (e.dataTransfer) {
            e.dataTransfer.dropEffect = 'move';
        }
    }
    
    // Export to window
    window.reorderMedia = reorderMedia;
    window.handleTableCellDragStart = handleTableCellDragStart;
    window.handleTableDragOver = handleTableDragOver;
    
    // Store reshuffle handleTableDrop separately - DO NOT export to window.handleTableDrop
    // observation-media.js will export its handleTableDrop to window.handleTableDrop
    // and call this one when it detects a reshuffle operation
    window._reshuffleHandleTableDrop = handleTableDrop;
    
    console.log('✅ Reshuffle library loaded');
})();

