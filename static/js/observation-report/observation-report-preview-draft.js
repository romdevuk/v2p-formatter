/**
 * Observation Report - Preview Draft Library
 * 
 * Standalone component for preview dialog functionality
 * 
 * ⚠️ IMPORTANT: This is a NEW module - no legacy code from old modules.
 * The old observation-media module did not work properly and must be completely avoided.
 * 
 * Author: Frontend Developer (Agent-2)
 * Created: Stage 2
 */

class ObservationReportPreviewDraft {
    constructor(options = {}) {
        this.options = {
            apiBase: options.apiBase || '/v2p-formatter/observation-report',
            ...options
        };
        this.isOpen = false;
        this.dialog = null;
        this.livePreview = null;
        this.columnResizer = null;
        this.eventHandlers = {};
        this.settings = {
            fontSize: 16,
            fontName: 'Times New Roman',
            showHeader: true,
            showFeedback: true,
            showSections: true,
            showACCoverage: false,
            showImageSuggestions: false,
            showParagraphNumbers: false,
            showEmptyMedia: false,
            trimParagraphs: false
        };
        
        this.createDialog();
    }
    
    /**
     * Create dialog structure
     */
    createDialog() {
        // Create dialog overlay
        this.dialog = document.createElement('div');
        this.dialog.className = 'preview-dialog-overlay';
        this.dialog.style.cssText = `
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 10000;
        `;
        
        // Create dialog content
        this.dialog.innerHTML = `
            <div class="preview-dialog" style="
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                background: #1e1e1e;
                color: #e0e0e0;
            ">
                <div class="preview-dialog-header" style="
                    padding: 15px 20px;
                    border-bottom: 1px solid #555;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-shrink: 0;
                ">
                    <h2 style="margin: 0;">📄 Document Preview</h2>
                    <button class="close-btn" style="
                        background: #2a2a2a;
                        color: #e0e0e0;
                        border: 1px solid #555;
                        padding: 8px 16px;
                        cursor: pointer;
                        border-radius: 4px;
                    ">✕ Close</button>
                </div>
                <div class="preview-dialog-content" style="
                    flex: 1;
                    display: flex;
                    overflow: hidden;
                ">
                    <div id="preview-left-column" style="
                        width: 200px;
                        min-width: 150px;
                        border-right: 1px solid #555;
                        overflow-y: auto;
                        padding: 15px;
                    ">
                        <div class="sections-list"></div>
                    </div>
                    <div id="preview-center-column" style="
                        flex: 1;
                        min-width: 300px;
                        overflow-y: auto;
                        padding: 20px;
                        border-right: 1px solid #555;
                    ">
                        <div id="preview-content"></div>
                    </div>
                    <div id="preview-right-column" style="
                        width: 250px;
                        min-width: 200px;
                        overflow-y: auto;
                        padding: 15px;
                    ">
                        <div class="preview-actions"></div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(this.dialog);
        
        // Set up event listeners
        const closeBtn = this.dialog.querySelector('.close-btn');
        closeBtn.addEventListener('click', () => this.close());
        
        this.dialog.addEventListener('click', (e) => {
            if (e.target === this.dialog) {
                this.close();
            }
        });
        
        // Initialize column resizer
        this.columnResizer = new ObservationReportColumnResizer('preview-dialog-content', {
            storageKey: 'observation-report-preview-columns'
        });
        
        // Set up resizers
        this.columnResizer.addResizer('preview-left-column', 'preview-center-column');
        this.columnResizer.addResizer('preview-center-column', 'preview-right-column');
    }
    
    /**
     * Open preview dialog
     */
    open(content, assignments, sections, headerData, assessorFeedback) {
        if (this.isOpen) return;
        
        this.isOpen = true;
        this.dialog.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        // Initialize Live Preview if not already
        if (!this.livePreview) {
            this.livePreview = new ObservationReportLivePreview('preview-content', {
                placeholderColors: [
                    '#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24',
                    '#6c5ce7', '#a29bfe', '#fd79a8', '#00b894'
                ]
            });
            
            // Connect section navigation
            this.livePreview.on('sectionToggle', (data) => {
                this.updateSectionsList();
            });
        }
        
        // Update content
        this.updateContent(content, assignments);
        
        // Update sections
        this.sections = sections || [];
        this.updateSectionsList();
        
        // Store header and feedback
        this.headerData = headerData || {};
        this.assessorFeedback = assessorFeedback || '';
        
        // Render actions panel
        this.renderActionsPanel();
        
        // Load saved column widths
        this.columnResizer.loadWidths('observation-report-preview-columns');
        
        this.emit('open');
    }
    
    /**
     * Close preview dialog
     */
    close() {
        if (!this.isOpen) return;
        
        this.isOpen = false;
        this.dialog.style.display = 'none';
        document.body.style.overflow = '';
        
        // Save column widths
        this.columnResizer.saveWidths('observation-report-preview-columns');
        
        this.emit('close');
    }
    
    /**
     * Update preview content
     */
    updateContent(content, assignments) {
        if (this.livePreview) {
            this.livePreview.updateContent(content, assignments, this.sections);
        }
    }
    
    /**
     * Update settings
     */
    updateSettings(settings) {
        this.settings = { ...this.settings, ...settings };
        
        // Apply settings to live preview if open
        if (this.livePreview && this.isOpen) {
            // Settings like font size/name would be applied during DOCX export
            // For now, just store them
        }
        
        this.renderActionsPanel();
    }
    
    /**
     * Update sections list
     */
    updateSectionsList() {
        const sectionsList = this.dialog.querySelector('.sections-list');
        if (!sectionsList) return;
        
        if (!this.sections || this.sections.length === 0) {
            sectionsList.innerHTML = '<p style="color: #999;">No sections</p>';
            return;
        }
        
        let html = '<div class="sections-list-header">Sections</div>';
        this.sections.forEach(section => {
            const icon = section.isExpanded ? '▼' : '▶';
            html += `
                <div class="section-item" data-section-id="${section.id}" style="
                    padding: 8px;
                    cursor: pointer;
                    border-radius: 4px;
                    margin: 4px 0;
                ">
                    <span>${icon}</span> ${this.escapeHtml(section.title)}
                </div>
            `;
        });
        
        sectionsList.innerHTML = html;
        
        // Set up click handlers
        const sectionItems = sectionsList.querySelectorAll('.section-item');
        sectionItems.forEach(item => {
            item.addEventListener('click', () => {
                const sectionId = item.dataset.sectionId;
                if (this.livePreview) {
                    this.livePreview.scrollToSection(sectionId);
                }
            });
        });
    }
    
    /**
     * Render actions panel
     */
    renderActionsPanel() {
        const actionsPanel = this.dialog.querySelector('.preview-actions');
        if (!actionsPanel) return;
        
        let html = '<h3>⚙️ Actions</h3>';
        
        // Font settings
        html += '<div class="action-group" style="margin: 15px 0;">';
        html += '<label>Font Settings:</label><br>';
        html += `<label>Size: <input type="number" class="font-size-input" value="${this.settings.fontSize}" min="8" max="24"></label><br>`;
        html += `<label>Type: <select class="font-name-input">
            <option value="Times New Roman" ${this.settings.fontName === 'Times New Roman' ? 'selected' : ''}>Times New Roman</option>
            <option value="Arial" ${this.settings.fontName === 'Arial' ? 'selected' : ''}>Arial</option>
            <option value="Calibri" ${this.settings.fontName === 'Calibri' ? 'selected' : ''}>Calibri</option>
        </select></label>`;
        html += '</div>';
        
        // Hide elements toggles
        html += '<div class="action-group" style="margin: 15px 0;">';
        html += '<label>Hide Elements:</label><br>';
        const toggles = [
            { key: 'showSections', label: 'Section' },
            { key: 'showACCoverage', label: 'AC covered' },
            { key: 'showImageSuggestions', label: 'Image sug' },
            { key: 'showParagraphNumbers', label: 'Para nums' },
            { key: 'showEmptyMedia', label: 'Empty med' },
            { key: 'trimParagraphs', label: 'Trim para' },
            { key: 'showHeader', label: 'Show head' },
            { key: 'showFeedback', label: 'Show feed' }
        ];
        toggles.forEach(toggle => {
            const checked = this.settings[toggle.key] ? 'checked' : '';
            html += `<label><input type="checkbox" class="toggle-input" data-key="${toggle.key}" ${checked}> ${toggle.label}</label><br>`;
        });
        html += '</div>';
        
        // Action buttons
        html += '<div class="action-buttons" style="margin: 15px 0;">';
        html += '<button class="update-draft-btn" style="width: 100%; padding: 10px; margin: 5px 0; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">Update Draft</button>';
        html += '<button class="export-docx-btn" style="width: 100%; padding: 10px; margin: 5px 0; background: #4ecdc4; color: white; border: none; border-radius: 4px; cursor: pointer;">Export DOCX</button>';
        html += '</div>';
        
        actionsPanel.innerHTML = html;
        
        // Set up event listeners
        const fontSizeInput = actionsPanel.querySelector('.font-size-input');
        const fontNameInput = actionsPanel.querySelector('.font-name-input');
        const toggleInputs = actionsPanel.querySelectorAll('.toggle-input');
        const updateDraftBtn = actionsPanel.querySelector('.update-draft-btn');
        const exportDocxBtn = actionsPanel.querySelector('.export-docx-btn');
        
        fontSizeInput?.addEventListener('change', (e) => {
            this.settings.fontSize = parseInt(e.target.value);
        });
        
        fontNameInput?.addEventListener('change', (e) => {
            this.settings.fontName = e.target.value;
        });
        
        toggleInputs.forEach(input => {
            input.addEventListener('change', (e) => {
                this.settings[input.dataset.key] = e.target.checked;
            });
        });
        
        updateDraftBtn?.addEventListener('click', () => {
            this.emit('updateDraft', this.settings);
        });
        
        exportDocxBtn?.addEventListener('click', () => {
            this.emit('exportDOCX', this.settings);
        });
    }
    
    /**
     * Export DOCX
     */
    async exportDOCX(options = {}) {
        const settings = { ...this.settings, ...options };
        
        if (!this.livePreview) {
            console.error('Preview Draft: Live Preview not initialized');
            return;
        }
        
        // Get content from live preview
        const content = this.livePreview.textContent || '';
        const assignments = this.livePreview.assignments || {};
        
        try {
            const response = await fetch(`${this.options.apiBase}/export-docx`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text_content: content,
                    assignments: assignments,
                    header_data: this.headerData,
                    assessor_feedback: this.assessorFeedback,
                    font_size: settings.fontSize,
                    font_name: settings.fontName,
                    filename: options.filename
                })
            });
            
            const data = await response.json();
            if (data.success) {
                // Trigger download
                window.location.href = data.download_url;
                this.emit('docxExported', data);
            } else {
                console.error('Preview Draft: Error exporting DOCX', data.error);
                alert('Error exporting DOCX: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Preview Draft: Error exporting DOCX', error);
            alert('Error exporting DOCX');
        }
    }
    
    /**
     * Escape HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
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
                console.error(`Preview Draft: Error in event handler for ${event}`, error);
            }
        });
    }
}

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ObservationReportPreviewDraft;
}

