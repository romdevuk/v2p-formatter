/**
 * Observation Report - Main Orchestrator
 * 
 * Coordinates all libraries and manages module-level state
 * 
 * ⚠️ IMPORTANT: This is a NEW module - no legacy code from old modules.
 * The old observation-media module did not work properly and must be completely avoided.
 * 
 * Author: Frontend Developer (Agent-2)
 * Created: Stage 2
 */

class ObservationReport {
    constructor(options = {}) {
        this.options = {
            apiBase: options.apiBase || '/v2p-formatter/observation-report',
            ...options
        };
        
        // Module-level state
        this.state = {
            assignments: {},
            textContent: '',
            sections: [],
            headerData: {},
            assessorFeedback: '',
            qualification: null,
            learner: null,
            draftName: null,
            standardsFileId: null
        };
        
        // Library instances
        this.mediaBrowser = null;
        this.livePreview = null;
        this.standards = null;
        this.previewDraft = null;
        this.columnResizer = null;
        
        // Current draft data
        this.currentDraft = null;
        
        this.init();
        
        // Auto-load draft from localStorage if available (after libraries are initialized)
        setTimeout(() => {
            this.loadDraftFromStorage();
        }, 1000); // Wait for libraries to be ready
    }
    
    /**
     * Load draft from localStorage on page load
     */
    async loadDraftFromStorage() {
        try {
            const savedDraftName = localStorage.getItem('observation-report-current-draft');
            if (savedDraftName && savedDraftName !== 'null' && savedDraftName !== '' && savedDraftName !== 'undefined') {
                console.log('Auto-loading saved draft from localStorage:', savedDraftName);
                await this.loadDraft(savedDraftName);
            }
        } catch (error) {
            console.warn('Error loading draft from storage:', error);
        }
    }
    
    /**
     * Initialize orchestrator
     */
    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initializeLibraries());
        } else {
            this.initializeLibraries();
        }
    }
    
    /**
     * Initialize all libraries
     */
    initializeLibraries() {
        // Initialize Media Browser
        const mediaBrowserContainer = document.getElementById('mediaBrowser');
        if (mediaBrowserContainer) {
            this.mediaBrowser = new ObservationReportMediaBrowser('mediaBrowser', {
                apiBase: this.options.apiBase
            });
        }
        
        // Initialize Live Preview
        const livePreviewContainer = document.getElementById('livePreview');
        if (livePreviewContainer) {
            this.livePreview = new ObservationReportLivePreview('livePreview', {
                placeholderColors: [
                    '#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24',
                    '#6c5ce7', '#a29bfe', '#fd79a8', '#00b894'
                ]
            });
        }
        
        // Initialize Standards
        const standardsContainer = document.getElementById('standards');
        if (standardsContainer) {
            this.standards = new ObservationReportStandards('standards', {
                apiBase: '/v2p-formatter/ac-matrix'
            });
        }
        
        // Initialize Preview Draft
        this.previewDraft = new ObservationReportPreviewDraft({
            apiBase: this.options.apiBase
        });
        
        // Initialize Column Resizer for main layout
        const mainLayout = document.getElementById('mainLayout');
        if (mainLayout) {
            this.columnResizer = new ObservationReportColumnResizer('mainLayout', {
                storageKey: 'observation-report-columns'
            });
            // Add resizers if columns exist
            const leftCol = document.getElementById('mediaBrowserColumn');
            const centerCol = document.getElementById('livePreviewColumn');
            const rightCol = document.getElementById('standardsColumn');
            
            if (leftCol && centerCol) {
                this.columnResizer.addResizer('mediaBrowserColumn', 'livePreviewColumn');
            }
            if (centerCol && rightCol) {
                this.columnResizer.addResizer('livePreviewColumn', 'standardsColumn');
            }
        }
        
        // Connect libraries via events
        this.setupEventHandlers();
    }
    
    /**
     * Connect libraries via events
     */
    setupEventHandlers() {
        // Media Browser events
        if (this.mediaBrowser) {
            this.mediaBrowser.on('mediaDragStart', (data) => {
                // Media drag started - Live Preview will handle drop
            });
            
            this.mediaBrowser.on('filenameUpdate', (data) => {
                // Filename updated - may need to update assignments if file was renamed
                this.updateAssignmentPaths(data.oldPath, data.newPath);
            });
        }
        
        // Live Preview events
        if (this.livePreview) {
            this.livePreview.on('mediaAssignment', (data) => {
                // Media assigned - update state and Media Browser
                this.state.assignments = data.assignments;
                if (this.mediaBrowser) {
                    this.mediaBrowser.updateAssignmentState(data.assignments);
                }
                
                // Auto-save draft if loaded
                if (this.currentDraft) {
                    this.autoSaveDraft();
                }
            });
            
            this.livePreview.on('mediaRemove', (data) => {
                // Media removed - update state
                this.state.assignments = this.livePreview.assignments;
                if (this.mediaBrowser) {
                    this.mediaBrowser.updateAssignmentState(this.state.assignments);
                }
                
                if (this.currentDraft) {
                    this.autoSaveDraft();
                }
            });
            
            this.livePreview.on('mediaReorder', (data) => {
                // Media reordered - update state
                this.state.assignments = this.livePreview.assignments;
                
                if (this.currentDraft) {
                    this.autoSaveDraft();
                }
            });
        }
        
        // Standards events
        if (this.standards) {
            // Provide section color getter to standards
            this.standards.getSectionColor = (sectionTitle) => {
                if (this.livePreview) {
                    return this.livePreview.getSectionColor(sectionTitle);
                }
                return null;
            };
            
            this.standards.on('sectionClick', (data) => {
                // Section clicked - scroll to section in Live Preview
                if (this.livePreview) {
                    const sectionId = `section-${data.sectionTitle.toLowerCase().replace(/\s+/g, '-')}`;
                    this.livePreview.scrollToSection(sectionId);
                }
            });
        }
        
        // Preview Draft events
        if (this.previewDraft) {
            this.previewDraft.on('updateDraft', () => {
                // Update draft requested
                this.saveDraft();
            });
            
            this.previewDraft.on('exportDOCX', (settings) => {
                // Export DOCX requested
                this.previewDraft.exportDOCX(settings);
            });
        }
    }
    
    /**
     * Load media for qualification/learner
     */
    loadMedia(qualification, learner) {
        this.state.qualification = qualification;
        this.state.learner = learner;
        
        if (this.mediaBrowser) {
            this.mediaBrowser.loadMedia(qualification, learner);
        }
    }
    
    /**
     * Update text content
     */
    updateTextContent(text) {
        this.state.textContent = text;
        
        if (this.livePreview) {
            this.livePreview.updateContent(text, this.state.assignments, this.state.sections);
        }
        
        // Update standards coverage
        if (this.standards) {
            this.standards.updateCoverage(text);
        }
        
        // Extract sections
        this.extractSections(text);
    }
    
    /**
     * Extract sections from text
     */
    extractSections(text) {
        const sections = [];
        const sectionPattern = /SECTION\s+([^\n:]+)[:\-]?\s*\n/gi;
        let match;
        let index = 0;
        
        while ((match = sectionPattern.exec(text)) !== null) {
            const title = match[1].trim();
            const sectionId = `section-${title.toLowerCase().replace(/\s+/g, '-')}`;
            
            sections.push({
                id: sectionId,
                title: title,
                isExpanded: true,
                index: index++
            });
        }
        
        this.state.sections = sections;
        
        if (this.livePreview) {
            this.livePreview.updateSectionStates(sections);
        }
    }
    
    /**
     * Update header data
     */
    updateHeaderData(headerData) {
        this.state.headerData = { ...this.state.headerData, ...headerData };
    }
    
    /**
     * Update assessor feedback
     */
    updateAssessorFeedback(feedback) {
        this.state.assessorFeedback = feedback;
    }
    
    /**
     * Load standards
     */
    async loadStandards(jsonFileId) {
        this.state.standardsFileId = jsonFileId;
        
        if (this.standards) {
            await this.standards.loadStandards(jsonFileId);
        }
    }
    
    /**
     * Load draft
     */
    async loadDraft(draftName) {
        try {
            const response = await fetch(`${this.options.apiBase}/drafts/${encodeURIComponent(draftName)}`);
            const data = await response.json();
            
            if (data.success && data.draft) {
                this.currentDraft = data.draft;
                this.state.draftName = data.draft.draft_name;
                this.state.textContent = data.draft.text_content || '';
                this.state.assignments = data.draft.assignments || {};
                this.state.headerData = data.draft.header_data || {};
                this.state.assessorFeedback = data.draft.assessor_feedback || '';
                this.state.qualification = data.draft.qualification || null;
                this.state.learner = data.draft.learner || null;
                
                // Save draft name to localStorage for persistence across page refresh
                if (draftName) {
                    localStorage.setItem('observation-report-current-draft', draftName);
                } else {
                    localStorage.removeItem('observation-report-current-draft');
                }
                
                // Update libraries
                this.updateTextContent(this.state.textContent);
                
                if (this.mediaBrowser && this.state.qualification && this.state.learner) {
                    this.mediaBrowser.loadMedia(this.state.qualification, this.state.learner);
                    this.mediaBrowser.updateAssignmentState(this.state.assignments);
                }
                
                // Load standards if available - check multiple possible field names
                if (this.standards) {
                    // Priority 1: Direct standards data
                    if (data.draft.standards_data) {
                        if (data.draft.standards_data.qualifications && Array.isArray(data.draft.standards_data.qualifications)) {
                            // Direct standards data with qualifications array
                            console.log('Loading standards from draft: direct data');
                            this.standards.setStandardsData(data.draft.standards_data);
                        } else if (typeof data.draft.standards_data === 'object' && Object.keys(data.draft.standards_data).length > 0) {
                            // Try to use it anyway
                            console.log('Loading standards from draft: object data');
                            this.standards.setStandardsData(data.draft.standards_data);
                        }
                    }
                    
                    // Priority 2: Load from file ID (only if we don't have data yet)
                    if (!this.standards.standardsData || !this.standards.standardsData.qualifications || 
                        (Array.isArray(this.standards.standardsData.qualifications) && this.standards.standardsData.qualifications.length === 0)) {
                        let fileIdToLoad = null;
                        
                        if (data.draft.json_file_id && data.draft.json_file_id !== 'null' && data.draft.json_file_id !== '') {
                            fileIdToLoad = data.draft.json_file_id;
                            console.log('Loading standards from draft: json_file_id =', fileIdToLoad);
                        } else if (data.draft.standards_file_id && data.draft.standards_file_id !== 'null' && data.draft.standards_file_id !== '') {
                            fileIdToLoad = data.draft.standards_file_id;
                            console.log('Loading standards from draft: standards_file_id =', fileIdToLoad);
                        } else if (this.state.standardsFileId && this.state.standardsFileId !== 'null' && this.state.standardsFileId !== '') {
                            fileIdToLoad = this.state.standardsFileId;
                            console.log('Loading standards from draft: state.standardsFileId =', fileIdToLoad);
                        }
                        
                        if (fileIdToLoad) {
                            await this.loadStandards(fileIdToLoad);
                        } else {
                            console.warn('No valid standards file ID found in draft');
                        }
                    }
                }
                
                return true;
            }
            return false;
        } catch (error) {
            console.error('Observation Report: Error loading draft', error);
            // Clear invalid draft from storage
            localStorage.removeItem('observation-report-current-draft');
            return false;
        }
    }
    
    /**
     * Save draft
     */
    async saveDraft(draftName = null) {
        const name = draftName || this.state.draftName || 'Untitled';
        
        // Update current draft name in state and save to localStorage
        this.state.draftName = name;
        if (name) {
            localStorage.setItem('observation-report-current-draft', name);
            console.log('Saved draft name to localStorage:', name);
        }
        
        const draftData = {
            draft_name: name,
            text_content: this.state.textContent,
            assignments: this.state.assignments,
            qualification: this.state.qualification,
            learner: this.state.learner,
            header_data: this.state.headerData,
            assessor_feedback: this.state.assessorFeedback,
            units: 'all', // Default to all units
            standards_data: this.standards?.standardsData || null,
            json_file_id: this.state.standardsFileId || null
        };
        
        try {
            const method = this.currentDraft ? 'PUT' : 'POST';
            const url = this.currentDraft 
                ? `${this.options.apiBase}/drafts/${encodeURIComponent(name)}`
                : `${this.options.apiBase}/drafts`;
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(draftData)
            });
            
            const data = await response.json();
            if (data.success) {
                this.state.draftName = name;
                this.currentDraft = draftData;
                
                // Save draft name to localStorage for persistence
                if (name) {
                    localStorage.setItem('observation-report-current-draft', name);
                    console.log('Saved draft name to localStorage:', name);
                }
                
                return true;
            }
            return false;
        } catch (error) {
            console.error('Observation Report: Error saving draft', error);
            return false;
        }
    }
    
    /**
     * Auto-save draft (debounced)
     */
    autoSaveDraft() {
        if (this.autoSaveTimeout) {
            clearTimeout(this.autoSaveTimeout);
        }
        
        this.autoSaveTimeout = setTimeout(() => {
            if (this.currentDraft) {
                this.saveDraft();
            }
        }, 2000); // Auto-save after 2 seconds of inactivity
    }
    
    /**
     * Open preview dialog
     */
    openPreview() {
        if (this.previewDraft) {
            this.previewDraft.open(
                this.state.textContent,
                this.state.assignments,
                this.state.sections,
                this.state.headerData,
                this.state.assessorFeedback
            );
        }
    }
    
    /**
     * Update assignment paths (when file renamed)
     */
    updateAssignmentPaths(oldPath, newPath) {
        // Update all assignments that reference oldPath
        Object.keys(this.state.assignments).forEach(placeholder => {
            const mediaList = this.state.assignments[placeholder];
            if (Array.isArray(mediaList)) {
                mediaList.forEach(media => {
                    if (media.path === oldPath) {
                        media.path = newPath;
                    }
                });
            }
        });
        
        // Update live preview
        if (this.livePreview) {
            this.livePreview.assignments = this.state.assignments;
            this.livePreview.render();
        }
    }
}

// Initialize on page load
if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.observationReport = new ObservationReport();
        });
    } else {
        window.observationReport = new ObservationReport();
    }
}


