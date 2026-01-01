/**
 * Observation Report - Column Resizer Library
 * 
 * Standalone utility for creating resizable column layouts
 * 
 * ⚠️ IMPORTANT: This is a NEW module - no legacy code from old modules.
 * The old observation-media module did not work properly and must be completely avoided.
 * 
 * Author: Frontend Developer (Agent-2)
 * Created: Stage 2
 */

class ObservationReportColumnResizer {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.options = {
            minWidth: options.minWidth || 100,
            storageKey: options.storageKey || null,
            ...options
        };
        this.resizers = [];
        this.container = null;
        
        this.init();
    }
    
    /**
     * Initialize container
     */
    init() {
        this.container = document.getElementById(this.containerId);
        if (!this.container) {
            console.error(`Column Resizer: Container #${this.containerId} not found`);
            return;
        }
        
        // Load saved widths if storage key provided
        if (this.options.storageKey) {
            this.loadWidths(this.options.storageKey);
        }
    }
    
    /**
     * Add a resizer between two columns
     */
    addResizer(leftColumnId, rightColumnId, options = {}) {
        const leftColumn = document.getElementById(leftColumnId);
        const rightColumn = document.getElementById(rightColumnId);
        
        if (!leftColumn || !rightColumn) {
            console.error(`Column Resizer: Columns not found (${leftColumnId}, ${rightColumnId})`);
            return;
        }
        
        // Create resizer element
        const resizer = document.createElement('div');
        resizer.className = 'column-resizer';
        resizer.style.cssText = `
            width: 4px;
            background: #555;
            cursor: col-resize;
            user-select: none;
            position: relative;
            flex-shrink: 0;
        `;
        
        // Insert resizer between columns
        if (rightColumn.parentNode) {
            rightColumn.parentNode.insertBefore(resizer, rightColumn);
        }
        
        // Set up drag handlers
        let isDragging = false;
        let startX = 0;
        let startLeftWidth = 0;
        let startRightWidth = 0;
        
        const minWidth = options.minWidth || this.options.minWidth;
        
        resizer.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX;
            startLeftWidth = leftColumn.offsetWidth;
            startRightWidth = rightColumn.offsetWidth;
            
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
            
            e.preventDefault();
        });
        
        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            const deltaX = e.clientX - startX;
            const newLeftWidth = startLeftWidth + deltaX;
            const newRightWidth = startRightWidth - deltaX;
            
            // Check minimum width constraints
            if (newLeftWidth >= minWidth && newRightWidth >= minWidth) {
                leftColumn.style.width = `${newLeftWidth}px`;
                rightColumn.style.width = `${newRightWidth}px`;
                
                // Save widths if storage key provided
                if (this.options.storageKey) {
                    this.saveWidths(this.options.storageKey);
                }
                
                // Emit resize event
                this.emit('resize', {
                    leftColumn: leftColumnId,
                    rightColumn: rightColumnId,
                    leftWidth: newLeftWidth,
                    rightWidth: newRightWidth
                });
            }
        });
        
        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                document.body.style.cursor = '';
                document.body.style.userSelect = '';
            }
        });
        
        // Store resizer info
        this.resizers.push({
            resizer,
            leftColumn: leftColumnId,
            rightColumn: rightColumnId,
            options
        });
    }
    
    /**
     * Save column widths to localStorage
     */
    saveWidths(storageKey) {
        if (!storageKey) return;
        
        const widths = {};
        
        this.resizers.forEach(resizerInfo => {
            const leftCol = document.getElementById(resizerInfo.leftColumn);
            const rightCol = document.getElementById(resizerInfo.rightColumn);
            
            if (leftCol && rightCol) {
                widths[resizerInfo.leftColumn] = leftCol.offsetWidth;
                widths[resizerInfo.rightColumn] = rightCol.offsetWidth;
            }
        });
        
        try {
            localStorage.setItem(storageKey, JSON.stringify(widths));
        } catch (error) {
            console.warn('Column Resizer: Error saving widths to localStorage', error);
        }
    }
    
    /**
     * Load column widths from localStorage
     */
    loadWidths(storageKey) {
        if (!storageKey) return;
        
        try {
            const saved = localStorage.getItem(storageKey);
            if (!saved) return;
            
            const widths = JSON.parse(saved);
            
            Object.keys(widths).forEach(columnId => {
                const column = document.getElementById(columnId);
                if (column && widths[columnId] >= this.options.minWidth) {
                    column.style.width = `${widths[columnId]}px`;
                }
            });
        } catch (error) {
            console.warn('Column Resizer: Error loading widths from localStorage', error);
        }
    }
    
    /**
     * Reset column widths to defaults
     */
    resetWidths() {
        this.resizers.forEach(resizerInfo => {
            const leftCol = document.getElementById(resizerInfo.leftColumn);
            const rightCol = document.getElementById(resizerInfo.rightColumn);
            
            if (leftCol) {
                leftCol.style.width = '';
            }
            if (rightCol) {
                rightCol.style.width = '';
            }
        });
        
        // Clear saved widths
        if (this.options.storageKey) {
            try {
                localStorage.removeItem(this.options.storageKey);
            } catch (error) {
                console.warn('Column Resizer: Error clearing localStorage', error);
            }
        }
    }
    
    /**
     * Event handlers
     */
    eventHandlers = {};
    
    /**
     * Event subscription
     */
    on(event, callback) {
        if (!this.eventHandlers[event]) {
            this.eventHandlers[event] = [];
        }
        this.eventHandlers[event].push(callback);
    }
    
    /**
     * Event unsubscription
     */
    off(event, callback) {
        if (!this.eventHandlers[event]) return;
        this.eventHandlers[event] = this.eventHandlers[event].filter(cb => cb !== callback);
    }
    
    /**
     * Emit event
     */
    emit(event, data) {
        if (!this.eventHandlers[event]) return;
        this.eventHandlers[event].forEach(callback => {
            try {
                callback(data);
            } catch (error) {
                console.error(`Column Resizer: Error in event handler for ${event}`, error);
            }
        });
    }
}

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ObservationReportColumnResizer;
}



