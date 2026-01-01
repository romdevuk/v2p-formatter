/**
 * Observation Report - Standards Library
 * 
 * Standalone component for managing standards/AC display and coverage
 * 
 * ⚠️ IMPORTANT: This is a NEW module - no legacy code from old modules.
 * The old observation-media module did not work properly and must be completely avoided.
 * 
 * Author: Frontend Developer (Agent-2)
 * Created: Stage 2
 */

class ObservationReportStandards {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.options = {
            apiBase: options.apiBase || '/v2p-formatter/ac-matrix',
            ...options
        };
        this.standardsData = null;
        this.textContent = '';
        this.searchKeyword = '';
        this.unitStates = {}; // Track expand/collapse state
        this.originalUnitStates = {}; // Store original states for search restore
        this.coverageMap = {}; // Map of AC IDs to sections that cover them
        this.eventHandlers = {};
        this.container = null;
        
        this.init();
    }
    
    /**
     * Initialize container
     */
    init() {
        this.container = document.getElementById(this.containerId);
        if (!this.container) {
            console.error(`Standards: Container #${this.containerId} not found`);
            return;
        }
        
        // Set up container structure
        this.container.innerHTML = `
            <div class="standards-header">
                <h3>Standards</h3>
                <div class="standards-controls">
                    <button class="expand-all-btn">▼ Expand All</button>
                    <button class="collapse-all-btn">▶ Collapse All</button>
                </div>
                <div class="search-container">
                    <input type="text" class="search-input" placeholder="🔍 Search ACs...">
                    <button class="clear-search-btn" style="display: none;">✕</button>
                </div>
                <div class="unit-filter">
                    <select class="unit-select">
                        <option value="all">All Units</option>
                    </select>
                </div>
            </div>
            <div class="standards-content"></div>
        `;
        
        // Store references
        this.contentContainer = this.container.querySelector('.standards-content');
        this.searchInput = this.container.querySelector('.search-input');
        this.clearSearchBtn = this.container.querySelector('.clear-search-btn');
        this.unitSelect = this.container.querySelector('.unit-select');
        
        // Set up event listeners
        this.setupEventListeners();
    }
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Expand/Collapse All
        const expandAllBtn = this.container.querySelector('.expand-all-btn');
        const collapseAllBtn = this.container.querySelector('.collapse-all-btn');
        
        expandAllBtn?.addEventListener('click', () => this.expandAllUnits());
        collapseAllBtn?.addEventListener('click', () => this.collapseAllUnits());
        
        // Search
        this.searchInput?.addEventListener('input', (e) => {
            this.searchStandards(e.target.value);
        });
        
        this.clearSearchBtn?.addEventListener('click', () => {
            this.clearSearch();
        });
        
        // Unit filter
        this.unitSelect?.addEventListener('change', (e) => {
            this.filterByUnit(e.target.value);
        });
    }
    
    /**
     * Load standards from JSON file
     */
    async loadStandards(jsonFileId) {
        if (!jsonFileId) {
            console.warn('Standards: jsonFileId required, received:', jsonFileId);
            return;
        }
        
        // Validate jsonFileId is not undefined, null, or empty string
        if (jsonFileId === 'undefined' || jsonFileId === 'null' || jsonFileId === '' || jsonFileId === null || jsonFileId === undefined) {
            console.warn('Standards: Invalid jsonFileId:', jsonFileId);
            return;
        }
        
        try {
            const url = `${this.options.apiBase}/json-files/${encodeURIComponent(jsonFileId)}`;
            console.log('Standards: Fetching from:', url);
            const response = await fetch(url);
            
            if (!response.ok) {
                console.error('Standards: HTTP error', response.status, response.statusText);
                return;
            }
            
            const data = await response.json();
            
            if (data.success && data.file) {
                this.standardsData = data.file;
                this.initializeUnitStates();
                this.populateUnitFilter();
                this.render();
                this.emit('standardsLoaded', this.standardsData);
                console.log('Standards: Successfully loaded', this.standardsData.qualifications?.length || 0, 'qualifications');
            } else {
                console.error('Standards: Error loading standards', data.error || 'Unknown error', data);
            }
        } catch (error) {
            console.error('Standards: Fetch error', error);
        }
    }
    
    /**
     * Set standards data directly
     */
    setStandardsData(data) {
        this.standardsData = data;
        this.initializeUnitStates();
        this.populateUnitFilter();
        this.render();
    }
    
    /**
     * Initialize unit expand/collapse states
     */
    initializeUnitStates() {
        if (!this.standardsData) return;
        
        this.unitStates = {};
        this.originalUnitStates = {};
        
        // Initialize all units as collapsed by default
        if (this.standardsData.qualifications) {
            this.standardsData.qualifications.forEach(qual => {
                if (qual.units) {
                    qual.units.forEach(unit => {
                        this.unitStates[unit.unit_id] = false;
                        this.originalUnitStates[unit.unit_id] = false;
                    });
                }
            });
        }
    }
    
    /**
     * Populate unit filter dropdown
     */
    populateUnitFilter() {
        if (!this.unitSelect || !this.standardsData) return;
        
        // Clear existing options except "All Units"
        this.unitSelect.innerHTML = '<option value="all">All Units</option>';
        
        if (this.standardsData.qualifications) {
            this.standardsData.qualifications.forEach(qual => {
                if (qual.units) {
                    qual.units.forEach(unit => {
                        const option = document.createElement('option');
                        option.value = unit.unit_id;
                        option.textContent = `${unit.unit_id}: ${unit.unit_title || ''}`;
                        this.unitSelect.appendChild(option);
                    });
                }
            });
        }
    }
    
    /**
     * Update coverage detection based on text content
     */
    updateCoverage(textContent) {
        this.textContent = textContent || '';
        this.detectCoverage();
        this.render();
    }
    
    /**
     * Detect which sections cover which ACs
     */
    detectCoverage() {
        this.coverageMap = {};
        
        if (!this.textContent || !this.standardsData) return;
        
        // Extract section titles from text
        const sectionPattern = /SECTION\s+([^\n:]+)[:\-]?\s*\n([\s\S]*?)(?=SECTION|$)/gi;
        const sections = [];
        let match;
        
        while ((match = sectionPattern.exec(this.textContent)) !== null) {
            sections.push({
                title: match[1].trim(),
                content: match[2]
            });
        }
        
        // Search for AC references in each section
        if (this.standardsData.qualifications) {
            this.standardsData.qualifications.forEach(qual => {
                if (qual.units) {
                    qual.units.forEach(unit => {
                        if (unit.assessment_criteria) {
                            unit.assessment_criteria.forEach(ac => {
                                const acId = ac.ac_id || '';
                                const acText = ac.ac_text || '';
                                
                                // Check if AC text appears in any section
                                sections.forEach(section => {
                                    const searchText = `${acId} ${acText}`.toLowerCase();
                                    if (section.content.toLowerCase().includes(searchText)) {
                                        if (!this.coverageMap[acId]) {
                                            this.coverageMap[acId] = [];
                                        }
                                        if (!this.coverageMap[acId].includes(section.title)) {
                                            this.coverageMap[acId].push(section.title);
                                        }
                                    }
                                });
                            });
                        }
                    });
                }
            });
        }
    }
    
    /**
     * Render standards display
     */
    render() {
        if (!this.contentContainer || !this.standardsData) {
            return;
        }
        
        let html = '';
        
        if (this.standardsData.qualifications) {
            this.standardsData.qualifications.forEach(qual => {
                if (qual.units) {
                    qual.units.forEach(unit => {
                        html += this.renderUnit(unit);
                    });
                }
            });
        }
        
        this.contentContainer.innerHTML = html;
        
        // Set up unit toggle listeners
        this.setupUnitToggles();
        
        // Set up section navigation listeners
        this.setupSectionNavigation();
    }
    
    /**
     * Render a unit
     */
    renderUnit(unit) {
        const isExpanded = this.unitStates[unit.unit_id] !== false;
        const toggleIcon = isExpanded ? '▼' : '▶';
        
        let html = `<div class="unit-container" data-unit-id="${unit.unit_id}">`;
        html += `<div class="unit-header" data-unit-id="${unit.unit_id}">`;
        html += `<span class="unit-toggle">${toggleIcon}</span>`;
        html += `<strong class="unit-title">${unit.unit_id}: ${this.escapeHtml(unit.unit_title || '')}</strong>`;
        html += `</div>`;
        
        if (isExpanded) {
            html += `<div class="unit-content" data-unit-id="${unit.unit_id}">`;
            
            if (unit.assessment_criteria) {
                unit.assessment_criteria.forEach(ac => {
                    html += this.renderAC(ac, unit.unit_id);
                });
            }
            
            html += `</div>`;
        }
        
        html += `</div>`;
        return html;
    }
    
    /**
     * Render an AC (Assessment Criterion)
     */
    renderAC(ac, unitId) {
        const acId = ac.ac_id || '';
        const acText = ac.ac_text || '';
        const coveredSections = this.coverageMap[acId] || [];
        
        // Check if AC matches search keyword
        const matchesSearch = !this.searchKeyword || 
            acText.toLowerCase().includes(this.searchKeyword.toLowerCase());
        
        if (!matchesSearch && this.searchKeyword) {
            return ''; // Skip ACs that don't match search
        }
        
        // Highlight search keyword in AC text
        let highlightedText = this.escapeHtml(acText);
        if (this.searchKeyword) {
            const regex = new RegExp(`(${this.escapeRegex(this.searchKeyword)})`, 'gi');
            highlightedText = highlightedText.replace(regex, '<mark>$1</mark>');
        }
        
        let html = `<div class="ac-item" data-ac-id="${acId}">`;
        html += `<div class="ac-id">${this.escapeHtml(acId)}</div>`;
        html += `<div class="ac-text">${highlightedText}</div>`;
        
        if (coveredSections.length > 0) {
            html += `<div class="ac-coverage">Covered: `;
            coveredSections.forEach((sectionTitle, idx) => {
                // Get section color from live preview if available
                const sectionColor = (typeof this.getSectionColor === 'function') ? this.getSectionColor(sectionTitle) : null;
                const colorStyle = sectionColor ? `style="color: ${sectionColor}; text-decoration: underline; text-decoration-style: dotted; text-decoration-color: ${sectionColor};"` : '';
                html += `<a href="#" class="section-link" data-section="${this.escapeHtml(sectionTitle)}" ${colorStyle}>${this.escapeHtml(sectionTitle)}</a>`;
                if (idx < coveredSections.length - 1) {
                    html += ', ';
                }
            });
            html += `</div>`;
        } else {
            html += `<div class="ac-coverage">Covered: <em>Not yet covered</em></div>`;
        }
        
        html += `</div>`;
        return html;
    }
    
    /**
     * Setup unit toggle listeners
     */
    setupUnitToggles() {
        const unitHeaders = this.contentContainer.querySelectorAll('.unit-header');
        unitHeaders.forEach(header => {
            header.addEventListener('click', (e) => {
                const unitId = header.dataset.unitId;
                this.toggleUnit(unitId);
            });
        });
    }
    
    /**
     * Setup section navigation listeners
     */
    setupSectionNavigation() {
        const sectionLinks = this.contentContainer.querySelectorAll('.section-link');
        sectionLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const sectionTitle = link.dataset.section;
                this.emit('sectionClick', { sectionTitle });
            });
        });
    }
    
    /**
     * Toggle unit expand/collapse
     */
    toggleUnit(unitId) {
        this.unitStates[unitId] = !this.unitStates[unitId];
        this.render();
        this.emit('unitToggle', { unitId, isExpanded: this.unitStates[unitId] });
    }
    
    /**
     * Expand unit
     */
    expandUnit(unitId) {
        this.unitStates[unitId] = true;
        this.render();
    }
    
    /**
     * Collapse unit
     */
    collapseUnit(unitId) {
        this.unitStates[unitId] = false;
        this.render();
    }
    
    /**
     * Expand all units
     */
    expandAllUnits() {
        Object.keys(this.unitStates).forEach(unitId => {
            this.unitStates[unitId] = true;
        });
        this.render();
    }
    
    /**
     * Collapse all units
     */
    collapseAllUnits() {
        Object.keys(this.unitStates).forEach(unitId => {
            this.unitStates[unitId] = false;
        });
        this.render();
    }
    
    /**
     * Search standards by keyword
     */
    searchStandards(keyword) {
        this.searchKeyword = keyword.trim();
        
        if (this.searchKeyword) {
            // Expand units with matching ACs, collapse others
            if (this.standardsData && this.standardsData.qualifications) {
                this.standardsData.qualifications.forEach(qual => {
                    if (qual.units) {
                        qual.units.forEach(unit => {
                            let hasMatch = false;
                            if (unit.assessment_criteria) {
                                unit.assessment_criteria.forEach(ac => {
                                    const acText = (ac.ac_text || '').toLowerCase();
                                    if (acText.includes(this.searchKeyword.toLowerCase())) {
                                        hasMatch = true;
                                    }
                                });
                            }
                            this.unitStates[unit.unit_id] = hasMatch;
                        });
                    }
                });
            }
            this.clearSearchBtn.style.display = 'block';
        } else {
            // Restore original states
            this.unitStates = { ...this.originalUnitStates };
            this.clearSearchBtn.style.display = 'none';
        }
        
        this.render();
    }
    
    /**
     * Clear search
     */
    clearSearch() {
        this.searchInput.value = '';
        this.searchKeyword = '';
        this.unitStates = { ...this.originalUnitStates };
        this.clearSearchBtn.style.display = 'none';
        this.render();
    }
    
    /**
     * Filter by unit
     */
    filterByUnit(unitId) {
        // Implementation can be enhanced to show only selected unit
        // For now, just re-render all
        this.render();
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
     * Escape regex special characters
     */
    escapeRegex(text) {
        return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
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
                console.error(`Standards: Error in event handler for ${event}`, error);
            }
        });
    }
}

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ObservationReportStandards;
}

