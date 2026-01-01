/**
 * AC Matrix Module - JavaScript
 * Handles AC Matrix functionality
 * Uses shared PreviewRenderer library for consistent preview rendering
 */

// Use shared preview renderer library
const PreviewRenderer = window.PreviewRenderer || {};
// Reference SECTION_COLORS from PreviewRenderer (don't redeclare)
// Use PreviewRenderer.SECTION_COLORS directly where needed

// Helper to get functions from shared library (use directly, don't create aliases)
function getPreviewRendererFunction(name, fallback) {
    return PreviewRenderer[name] || fallback;
}

// Helper functions that use PreviewRenderer
function parseSections(text) {
    return getPreviewRendererFunction('parseSections', function() { 
        return { hasSections: false, sections: [], preSectionContent: '' }; 
    })(text);
}

function renderContentWithMedia(text, assignments) {
    const fn = getPreviewRendererFunction('renderContentWithMedia', function(text) {
        const div = document.createElement('div');
        div.textContent = text || '';
        return div.innerHTML;
    });
    return fn(text, assignments);
}

function countMediaInSection(section, assignments) {
    const fn = getPreviewRendererFunction('countMediaInSection', function() { return 0; });
    return fn(section, assignments);
}

function escapeHtml(text) {
    const fn = getPreviewRendererFunction('escapeHtml', function(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    });
    return fn(text);
}

// Global state
let currentMatrixData = null;
let currentJsonFileId = null;
let currentObservationReport = '';
let lastPreviewTitle = '';
let currentAssignments = {};
let currentUnits = []; // All units from current JSON file
let selectedUnitIds = []; // Selected unit IDs for filtering
let promptStore = []; // {id, name, body}
let selectedPromptId = '';
let editingPromptId = '';
let promptFormMode = 'add'; // 'add' | 'edit'

// Helpers
function getDraftById(draftId) {
    if (!draftsData || !draftId) return null;
    const draft = draftsData.find(d => String(d.id) === String(draftId)) || null;
    // Also check data attributes from option element if draft not found in array
    if (!draft) {
        const draftSelector = document.getElementById('draft-selector');
        if (draftSelector) {
            const option = draftSelector.querySelector(`option[value="${draftId}"]`);
            if (option) {
                return {
                    id: draftId,
                    name: option.textContent,
                    text_content: option.dataset.textContent || '',
                    assignments: option.dataset.assignments ? JSON.parse(option.dataset.assignments) : {},
                    selected_subfolder: option.dataset.subfolder || '',
                    json_file_id: option.dataset.jsonFileId || '',
                    selected_unit_ids: option.dataset.selectedUnitIds ? JSON.parse(option.dataset.selectedUnitIds) : []
                };
            }
        }
    }
    return draft;
}

// Format text for simple preview (AC highlighting, no media) - used for bulk report previews
function formatSectionContent(text) {
    if (!text) return '';
    // Lightly highlight AC-like tokens (e.g., 641:1.1)
    const acPattern = /\b\d{3,}(?::\d+(?:\.\d+)*|\.\d+(?:\.\d+)*)?/g;
    const escaped = escapeHtml(text);
    return escaped
        .replace(acPattern, match => `<span class="preview-ac-highlight">${match}</span>`)
        .replace(/\n/g, '<br>');
}

// Get section state from localStorage
function getSectionStates() {
    try {
        const stored = localStorage.getItem('acMatrixSectionStates');
        return stored ? JSON.parse(stored) : {};
    } catch (e) {
        return {};
    }
}

// Save section state to localStorage
function saveSectionStates(states) {
    try {
        localStorage.setItem('acMatrixSectionStates', JSON.stringify(states));
    } catch (e) {
        // Ignore localStorage errors
    }
}

// Toggle section expand/collapse
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

// Expand all sections
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

// Collapse all sections
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

// Render sections wrapper - uses shared library with AC Matrix-specific state management
function renderSections(sectionData, assignments = {}, useInlineHandlers = true) {
    if (!PreviewRenderer.renderSections) {
        return '';
    }
    // For bulk reports, don't use inline handlers - use event delegation instead
    const toggleFunc = useInlineHandlers ? toggleSection : null;
    return PreviewRenderer.renderSections(
        sectionData, 
        assignments, 
        getSectionStates, 
        saveSectionStates, 
        toggleFunc
    );
}

function renderLivePreview(title, text, assignments = {}, reports = null) {
    const preview = document.getElementById('live-preview-content');
    const sectionControls = document.getElementById('sectionControls');
    
    if (!preview) return;
    
    if (reports && Array.isArray(reports) && reports.length > 0) {
        let combinedHtml = '';
        reports.forEach((report, idx) => {
            const sectionData = parseSections(report.text || '');
            const reportTitle = report.name || `Report ${idx + 1}`;
            if (sectionData.hasSections) {
                combinedHtml += `<div class="preview-block"><h4>${escapeHtml(reportTitle)}</h4>${renderSections(sectionData, report.assignments || {})}</div>`;
            } else {
                combinedHtml += `<div class="preview-block"><h4>${escapeHtml(reportTitle)}</h4><div class="preview-text">${renderContentWithMedia(report.text || '', report.assignments || {})}</div></div>`;
            }
        });
        preview.innerHTML = combinedHtml || '<p style="color: #999; text-align: center;">Select drafts to preview</p>';
        if (sectionControls) sectionControls.style.display = 'flex';
        currentObservationReport = reports.map(r => r.text || '').join('\n\n');
        lastPreviewTitle = 'Bulk Reports';
        return;
    }

    if (!text || !text.trim()) {
        preview.innerHTML = '<p style="color: #999; text-align: center;">Select a draft to see the live preview</p>';
        if (sectionControls) sectionControls.style.display = 'none';
        currentObservationReport = '';
        lastPreviewTitle = '';
        return;
    }
    
    // Parse sections
    const sectionData = parseSections(text);
    
    let previewHtml = '';
    
    if (sectionData.hasSections) {
        // Render with sections
        previewHtml = renderSections(sectionData, assignments);
        if (sectionControls) sectionControls.style.display = 'flex';
    } else {
        // Render without sections (simple text)
        const safeTitle = title ? escapeHtml(title) : 'Live Preview';
        previewHtml = `
            <div class="preview-block">
                <h4>${safeTitle}</h4>
                <div class="preview-text">${renderContentWithMedia(text, assignments)}</div>
            </div>
        `;
        if (sectionControls) sectionControls.style.display = 'none';
    }
    
    preview.innerHTML = previewHtml;
    currentObservationReport = text;
    lastPreviewTitle = title || 'Live Preview';
}

// Make functions globally available
window.toggleSection = toggleSection;
window.expandAllSections = expandAllSections;
window.collapseAllSections = collapseAllSections;

// Initialize module when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initACMatrix();
    
    // Also check for pre-selected JSON file after a short delay (to ensure dropdown is populated)
    setTimeout(() => {
        const selector = document.getElementById('json-file-selector');
        if (selector && selector.value) {
            console.log('JSON file pre-selected, loading units...');
            loadUnitsForJsonFile();
        }
    }, 500);
});

function initACMatrix() {
    console.log('Initializing AC Matrix module...');
    
    setupEventListeners();
    setupDraftLoader();
    setupBulkReports();
    setupExpandCollapseAll();
    setupSaveLoadDelete();
    setupUnitSelector();
    setupPrompts();
    
    // Load JSON files and then check if one is already selected
    loadJSONFiles().then(() => {
        // After JSON files are loaded, check if one is already selected and load units
        const selector = document.getElementById('json-file-selector');
        if (selector && selector.value) {
            console.log('JSON file already selected on page load:', selector.value);
            loadUnitsForJsonFile();
        }
    });
}

// Load available JSON files
async function loadJSONFiles() {
    try {
        const response = await fetch('/v2p-formatter/ac-matrix/json-files');
        const data = await response.json();
        
        if (data.success) {
            const selector = document.getElementById('json-file-selector');
            selector.innerHTML = '<option value="">Select a standards file...</option>';
            
            data.files.forEach(file => {
                const option = document.createElement('option');
                option.value = file.id;
                option.textContent = file.qualification_name || file.name;
                option.dataset.fileName = file.name;
                selector.appendChild(option);
            });
            
            // Show/hide delete button based on selection
            updateDeleteButtonVisibility();
            
            console.log(`Loaded ${data.files.length} JSON files`);
        } else {
            console.error('Error loading JSON files:', data.error);
        }
    } catch (error) {
        console.error('Error loading JSON files:', error);
    }
}

// Update delete button visibility
function updateDeleteButtonVisibility() {
    const selector = document.getElementById('json-file-selector');
    const deleteBtn = document.getElementById('delete-json-btn');
    
    if (deleteBtn && selector) {
        if (selector.value) {
            deleteBtn.style.display = 'inline-block';
        } else {
            deleteBtn.style.display = 'none';
        }
    }
}

// Delete JSON file
async function deleteJSONFile() {
    const selector = document.getElementById('json-file-selector');
    const fileId = selector.value;
    
    if (!fileId) {
        alert('Please select a file to delete');
        return;
    }
    
    const selectedOption = selector.options[selector.selectedIndex];
    const fileName = selectedOption ? (selectedOption.textContent || selectedOption.dataset.fileName) : 'this file';
    
    // Confirm deletion
    if (!confirm(`Are you sure you want to delete "${fileName}"?\n\nThis action cannot be undone.`)) {
        return;
    }
    
    try {
        const response = await fetch(`/v2p-formatter/ac-matrix/json-files/${fileId}`, {
            method: 'DELETE'
        });
        
        let data;
        try {
            data = await response.json();
        } catch (parseError) {
            console.error('Error parsing response:', parseError);
            alert(`Error deleting file: Invalid server response (Status: ${response.status})`);
            return;
        }
        
        if (response.ok && data.success) {
            alert(`File deleted successfully: ${fileName}`);
            // Clear selection
            selector.value = '';
            updateDeleteButtonVisibility();
            // Reload file list
            loadJSONFiles();
        } else {
            const errorMsg = data.error || data.message || `Server error (Status: ${response.status})`;
            alert(`Error deleting file: ${errorMsg}`);
            console.error('Delete error:', data);
        }
    } catch (error) {
        console.error('Error deleting file:', error);
        alert(`Error deleting file: ${error.message || 'Network error or server unavailable'}`);
    }
}

// Setup event listeners
function setupEventListeners() {
    // Upload JSON button
    const uploadBtn = document.getElementById('upload-json-btn');
    if (uploadBtn) {
        uploadBtn.addEventListener('click', showUploadJSONDialog);
    }
    
    // Delete JSON button
    const deleteBtn = document.getElementById('delete-json-btn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', deleteJSONFile);
    }
    
    // JSON file selector change - update delete button visibility and load units
    const selector = document.getElementById('json-file-selector');
    if (selector) {
        selector.addEventListener('change', () => {
            updateDeleteButtonVisibility();
            loadUnitsForJsonFile();
        });
    }
    
    // Analyze button
    const analyzeBtn = document.getElementById('analyze-btn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', analyzeReport);
    }
}

// Setup draft loader (drafts already loaded in page, no API needed)
function setupDraftLoader() {
    const draftSelector = document.getElementById('draft-selector');
    
    if (draftSelector) {
        draftSelector.addEventListener('change', () => {
            const selectedOption = draftSelector.options[draftSelector.selectedIndex];
            if (!selectedOption || !selectedOption.value) {
                currentAssignments = {};
                renderLivePreview('', '', currentAssignments);
                return;
            }
            
            const draft = getDraftById(selectedOption.value);
            if (draft) {
                currentAssignments = draft.assignments || {};
                renderLivePreview(draft.name, draft.text_content, currentAssignments);
                console.log('Draft loaded automatically:', selectedOption.textContent);
                
                // Auto-select JSON file if draft has one assigned
                if (draft.json_file_id) {
                    const jsonSelector = document.getElementById('json-file-selector');
                    if (jsonSelector) {
                        // Wait for JSON files to be loaded if not already
                        const selectJsonFile = () => {
                            if (jsonSelector.querySelector(`option[value="${draft.json_file_id}"]`)) {
                                jsonSelector.value = draft.json_file_id;
                                currentJsonFileId = draft.json_file_id;
                                updateDeleteButtonVisibility();
                                
                                // Restore selected units if draft has them
                                const savedUnitIds = draft.selected_unit_ids || [];
                                if (savedUnitIds.length > 0) {
                                    selectedUnitIds = savedUnitIds;
                                    loadUnitsForJsonFile(true); // Preserve selected units
                                    console.log('Selected units restored:', savedUnitIds);
                                } else {
                                    loadUnitsForJsonFile();
                                }
                                
                                console.log('JSON file auto-selected:', draft.json_file_id);
                            } else {
                                // JSON files not loaded yet, wait a bit and try again
                                setTimeout(selectJsonFile, 100);
                            }
                        };
                        
                        // Check if JSON files are already loaded
                        if (jsonSelector.options.length > 1) {
                            selectJsonFile();
                        } else {
                            // Wait for JSON files to load first
                            loadJSONFiles().then(() => {
                                setTimeout(selectJsonFile, 100);
                            });
                        }
                    }
                }
            } else {
                currentAssignments = {};
                renderLivePreview('', '', currentAssignments);
            }
        });
    }
}

// Setup bulk reports mode
function setupBulkReports() {
    const reportModeRadios = document.querySelectorAll('input[name="report-mode"]');
    const singleMode = document.getElementById('single-report-mode');
    const bulkMode = document.getElementById('bulk-reports-mode');
    const addSelectedDraftsBtn = document.getElementById('add-selected-drafts-btn');
    const bulkReportsList = document.getElementById('bulk-reports-list');
    
    // Toggle between single and bulk mode
    reportModeRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            if (radio.value === 'single') {
                singleMode.style.display = 'block';
                bulkMode.style.display = 'none';
                // Refresh preview from current selection
                const draftSelector = document.getElementById('draft-selector');
                const selectedId = draftSelector ? draftSelector.value : '';
                const draft = getDraftById(selectedId);
                renderLivePreview(draft ? draft.name : '', draft ? draft.text_content : '');
            } else {
                singleMode.style.display = 'none';
                bulkMode.style.display = 'block';
                updateBulkPreview();
            }
        });
    });
    
    // Add selected drafts button
    if (addSelectedDraftsBtn) {
        addSelectedDraftsBtn.addEventListener('click', addSelectedDrafts);
    }
}

// Add selected drafts to bulk reports
function addSelectedDrafts() {
    const checkboxes = document.querySelectorAll('.draft-checkbox:checked');
    
    if (checkboxes.length === 0) {
        alert('Please select at least one draft to add');
        return;
    }
    
    checkboxes.forEach(checkbox => {
        const draftName = checkbox.dataset.name || 'Draft';
        const draftText = checkbox.getAttribute('data-text-content') || '';
        const assignmentsRaw = checkbox.getAttribute('data-assignments') || '{}';
        let assignments = {};
        try {
            assignments = JSON.parse(assignmentsRaw);
        } catch (e) {
            assignments = {};
        }
        
        // Decode HTML entities
        const textareaElement = document.createElement('textarea');
        textareaElement.innerHTML = draftText;
        const decodedText = textareaElement.value;
        
        // Add report with draft content
        addBulkReportWithContent(draftName, decodedText, checkbox.value, assignments);
        
        // Uncheck the checkbox
        checkbox.checked = false;
    });
    
    updateBulkPreview();
}

// Add a bulk report with pre-filled content
function addBulkReportWithContent(name, text, draftId = '', assignments = {}) {
    const bulkReportsList = document.getElementById('bulk-reports-list');
    if (!bulkReportsList) return;
    
    // Prevent duplicate entries for the same draft
    if (draftId && bulkReportsList.querySelector(`[data-draft-id="${draftId}"]`)) {
        return;
    }
    
    const reportIndex = bulkReportsList.children.length;
    const reportItem = document.createElement('div');
    reportItem.className = 'bulk-report-item';
    reportItem.dataset.reportIndex = reportIndex;
    reportItem.dataset.reportText = text || '';
    reportItem.dataset.assignments = JSON.stringify(assignments || {});
    if (draftId) {
        reportItem.dataset.draftId = draftId;
    }
    
    // Render preview with sections and media (same as Live Preview)
    const sectionData = parseSections(text || '');
    let previewHtml = '';
    
    if (sectionData.hasSections) {
        // Make section IDs unique per bulk report by prefixing with report index
        const uniqueSectionData = {
            ...sectionData,
            sections: sectionData.sections.map(section => ({
                ...section,
                id: `bulk-${reportIndex}-${section.id}`
            }))
        };
        // Don't use inline handlers for bulk reports - use event delegation instead
        previewHtml = renderSections(uniqueSectionData, assignments || {}, false);
    } else {
        previewHtml = renderContentWithMedia(text || '', assignments || {});
    }
    
    reportItem.innerHTML = `
        <div class="bulk-report-item-header">
            <input type="text" class="report-name" placeholder="Report ${reportIndex + 1} (optional)" value="${escapeHtml(name)}">
            <button class="btn btn-danger remove-report-btn" style="padding: 6px 12px; background: #d32f2f; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">Remove</button>
        </div>
        <div class="report-preview" style="max-height: 400px; overflow-y: auto; padding: 10px; background: #1a1a1a; border-radius: 4px; margin-top: 10px;">${previewHtml || '<span style="color:#777;">No text available</span>'}</div>
    `;
    
    bulkReportsList.appendChild(reportItem);
    
    // Setup remove button
    const removeBtn = reportItem.querySelector('.remove-report-btn');
    removeBtn.addEventListener('click', () => {
        reportItem.remove();
        // Renumber remaining reports
        renumberBulkReports();
        updateBulkPreview();
    });
    
    // Setup click handlers for sections within this bulk report using event delegation
    // This handles clicks on section headers to toggle expand/collapse
    const reportPreview = reportItem.querySelector('.report-preview');
    reportPreview.addEventListener('click', function(e) {
        const header = e.target.closest('.observation-section-header');
        if (header && !e.target.closest('button') && !e.target.closest('input')) {
            e.preventDefault();
            e.stopPropagation();
            const sectionEl = header.closest('.observation-section');
            if (sectionEl) {
                const sectionId = sectionEl.getAttribute('data-section-id');
                if (sectionId) {
                    // Toggle the section directly
                    const contentEl = sectionEl.querySelector('.observation-section-content');
                    const iconEl = sectionEl.querySelector('.observation-section-icon');
                    const isCollapsed = sectionEl.classList.contains('collapsed');
                    
                    if (isCollapsed) {
                        sectionEl.classList.remove('collapsed');
                        if (contentEl) contentEl.style.display = 'block';
                        if (iconEl) iconEl.textContent = '▼';
                    } else {
                        sectionEl.classList.add('collapsed');
                        if (contentEl) contentEl.style.display = 'none';
                        if (iconEl) iconEl.textContent = '▶';
                    }
                }
            }
        }
    });
}

// Add a new bulk report item
function addBulkReport() {
    const bulkReportsList = document.getElementById('bulk-reports-list');
    if (!bulkReportsList) return;
    
    const reportIndex = bulkReportsList.children.length;
    const reportItem = document.createElement('div');
    reportItem.className = 'bulk-report-item';
    reportItem.dataset.reportIndex = reportIndex;
    reportItem.dataset.reportText = '';
    
    reportItem.innerHTML = `
        <div class="bulk-report-item-header">
            <input type="text" class="report-name" placeholder="Report ${reportIndex + 1} (optional)" value="Report ${reportIndex + 1}">
            <button class="btn btn-danger remove-report-btn" style="padding: 6px 12px; background: #d32f2f; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">Remove</button>
        </div>
        <div class="report-preview"><span style="color:#777;">No draft attached</span></div>
    `;
    
    bulkReportsList.appendChild(reportItem);
    
    // Setup remove button
    const removeBtn = reportItem.querySelector('.remove-report-btn');
    removeBtn.addEventListener('click', () => {
        reportItem.remove();
        // Renumber remaining reports
        renumberBulkReports();
        updateBulkPreview();
    });
}

// Renumber bulk reports after removal
function renumberBulkReports() {
    const bulkReportsList = document.getElementById('bulk-reports-list');
    if (!bulkReportsList) return;
    
    Array.from(bulkReportsList.children).forEach((item, index) => {
        item.dataset.reportIndex = index;
        const nameInput = item.querySelector('.report-name');
        if (nameInput && !nameInput.value.trim()) {
            nameInput.placeholder = `Report ${index + 1} (optional)`;
        }
    });
}

// Get all bulk reports
function getBulkReports() {
    const bulkReportsList = document.getElementById('bulk-reports-list');
    if (!bulkReportsList) return [];
    
    const reports = [];
    Array.from(bulkReportsList.children).forEach((item, index) => {
        const nameInput = item.querySelector('.report-name');
        const reportText = item.dataset.reportText || '';
        let assignments = {};
        try {
            assignments = item.dataset.assignments ? JSON.parse(item.dataset.assignments) : {};
        } catch (e) {
            assignments = {};
        }
        
        if (reportText.trim()) {
            reports.push({
                name: nameInput ? (nameInput.value.trim() || `Report ${index + 1}`) : `Report ${index + 1}`,
                text: reportText.trim(),
                assignments: assignments
            });
        }
    });
    
    return reports;
}

// Update preview based on bulk selection
function updateBulkPreview() {
    const reports = getBulkReports();
    if (reports.length === 0) {
        renderLivePreview('', '', {});
        return;
    }
    
    renderLivePreview('Bulk Reports', '', {}, reports);
}

// Setup Expand/Collapse All
function setupExpandCollapseAll() {
    const expandAllBtn = document.getElementById('expand-all-btn');
    const collapseAllBtn = document.getElementById('collapse-all-btn');
    
    if (expandAllBtn) {
        expandAllBtn.addEventListener('click', () => {
            document.querySelectorAll('.ac-details-panel').forEach(panel => {
                panel.style.display = 'block';
            });
        });
    }
    
    if (collapseAllBtn) {
        collapseAllBtn.addEventListener('click', () => {
            document.querySelectorAll('.ac-details-panel').forEach(panel => {
                panel.style.display = 'none';
            });
        });
    }
}

// Setup Save/Load/Delete
function setupSaveLoadDelete() {
    // Save button
    const saveBtn = document.getElementById('save-matrix-btn');
    if (saveBtn) {
        saveBtn.addEventListener('click', showSaveMatrixDialog);
    }
    
    // Load button
    const loadBtn = document.getElementById('load-matrix-btn');
    if (loadBtn) {
        loadBtn.addEventListener('click', toggleLoadMatrixMenu);
    }
    
    // Delete button
    const deleteBtn = document.getElementById('delete-matrix-btn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', showDeleteMatrixDialog);
    }
    
    // Copy missing ACs button
    const copyMissingAcsBtn = document.getElementById('copy-missing-acs-btn');
    if (copyMissingAcsBtn) {
        copyMissingAcsBtn.addEventListener('click', async () => {
            const missingAcsField = document.getElementById('missing-acs-field');
            if (missingAcsField && missingAcsField.value.trim()) {
                try {
                    await navigator.clipboard.writeText(missingAcsField.value);
                    const originalText = copyMissingAcsBtn.textContent;
                    copyMissingAcsBtn.textContent = 'Copied!';
                    copyMissingAcsBtn.style.background = '#4a8a4a';
                    setTimeout(() => {
                        copyMissingAcsBtn.textContent = originalText;
                        copyMissingAcsBtn.style.background = '';
                    }, 2000);
                } catch (err) {
                    // Fallback for older browsers
                    missingAcsField.select();
                    document.execCommand('copy');
                    alert('Copied to clipboard!');
                }
            } else {
                alert('No missing ACs to copy');
            }
        });
    }
    
    // Save dialog buttons
    const saveConfirmBtn = document.getElementById('save-dialog-confirm-btn');
    const saveCancelBtn = document.getElementById('save-dialog-cancel-btn');
    
    if (saveConfirmBtn) {
        saveConfirmBtn.addEventListener('click', saveMatrix);
    }
    
    if (saveCancelBtn) {
        saveCancelBtn.addEventListener('click', () => {
            document.getElementById('save-matrix-dialog').style.display = 'none';
        });
    }
}

// Show upload JSON dialog (placeholder - to be implemented)
function showUploadJSONDialog() {
    // Create file input
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/v2p-formatter/ac-matrix/json-files', {
                method: 'POST',
                body: formData
            });
            
            let data;
            try {
                data = await response.json();
            } catch (parseError) {
                console.error('Error parsing response:', parseError);
                alert(`Error uploading file: Invalid server response (Status: ${response.status})`);
                return;
            }
            
            if (response.ok && data.success) {
                alert(`File uploaded successfully: ${data.qualification_name || data.file_name}`);
                loadJSONFiles(); // Reload list
            } else {
                const errorMsg = data.error || data.message || `Server error (Status: ${response.status})`;
                alert(`Error uploading file: ${errorMsg}`);
                console.error('Upload error:', data);
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            alert(`Error uploading file: ${error.message || 'Network error or server unavailable'}`);
        }
    });
    
    input.click();
}

// Setup unit selector
function setupUnitSelector() {
    const filterToggle = document.getElementById('filter-units-toggle');
    const selectAllBtn = document.getElementById('select-all-units-btn');
    const deselectAllBtn = document.getElementById('deselect-all-units-btn');
    
    if (filterToggle) {
        filterToggle.addEventListener('change', handleFilterToggle);
    }
    
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', selectAllUnits);
    }
    
    if (deselectAllBtn) {
        deselectAllBtn.addEventListener('click', deselectAllUnits);
    }
}

// Load units for selected JSON file
async function loadUnitsForJsonFile(preserveSelectedUnits = false) {
    const jsonFileId = document.getElementById('json-file-selector').value;
    const unitContainer = document.getElementById('unit-selector-container');
    const unitList = document.getElementById('unit-selection-list');
    const unitCheckboxesContainer = document.getElementById('unit-checkboxes-container');
    const filterToggle = document.getElementById('filter-units-toggle');
    const controls = document.getElementById('unit-selector-controls');
    
    if (!jsonFileId) {
        unitContainer.style.display = 'none';
        currentUnits = [];
        if (!preserveSelectedUnits) {
            selectedUnitIds = [];
        }
        if (filterToggle) filterToggle.checked = false;
        if (controls) controls.style.display = 'none';
        return;
    }
    
    // Reset filter toggle when JSON file changes (unless preserving selection)
    if (filterToggle && !preserveSelectedUnits) {
        filterToggle.checked = false;
    }
    if (controls && !preserveSelectedUnits) {
        controls.style.display = 'none';
    }
    
    try {
        console.log(`Loading units for JSON file: ${jsonFileId}`);
        
        // Load units directly from the units endpoint
        const response = await fetch(`/v2p-formatter/ac-matrix/json-files/${jsonFileId}/units`);
        console.log('Units response status:', response.status);
        
        if (!response.ok) {
            console.error('Error loading units:', response.status, response.statusText);
            if (unitContainer) unitContainer.style.display = 'none';
            currentUnits = [];
            return;
        }
        
        const unitsData = await response.json();
        console.log('Units data received:', unitsData);
        
        if (unitsData.success && unitsData.units && unitsData.units.length > 0) {
            currentUnits = unitsData.units;
            console.log(`Loaded ${currentUnits.length} units:`, currentUnits);
            
            // Initialize selectedUnitIds - preserve existing if requested, otherwise all units
            if (!preserveSelectedUnits || selectedUnitIds.length === 0) {
                selectedUnitIds = currentUnits.map(u => u.unit_id);
            } else {
                // Filter to only include units that exist in current JSON file
                const availableUnitIds = currentUnits.map(u => u.unit_id);
                selectedUnitIds = selectedUnitIds.filter(id => availableUnitIds.includes(id));
                // If no valid units selected, select all
                if (selectedUnitIds.length === 0) {
                    selectedUnitIds = availableUnitIds;
                }
            }
            
            // Render checkboxes first
            renderUnitCheckboxes();
            
            // Show container and unit list
            if (unitContainer) {
                unitContainer.style.display = 'block';
                console.log('Unit selector container displayed');
            }
            
            // Show unit list even if filter is off (but checkboxes disabled)
            if (unitList) {
                unitList.style.display = 'block';
                console.log('Unit selection list displayed');
            }
        } else {
            const errorMsg = unitsData.error || 'No units found';
            console.error('Error loading units:', errorMsg);
            if (unitContainer) {
                // Show container even if error, so user knows something happened
                unitContainer.style.display = 'block';
                const container = document.getElementById('unit-checkboxes-container');
                if (container) {
                    container.innerHTML = `<p style="color: #999; padding: 10px;">${errorMsg}</p>`;
                }
            }
            currentUnits = [];
        }
    } catch (error) {
        console.error('Error loading units:', error);
        if (unitContainer) unitContainer.style.display = 'none';
        currentUnits = [];
    }
}

// -----------------------
// Prompt management
// -----------------------

// Load prompts from localStorage
function loadPromptsFromStorage() {
    try {
        const stored = localStorage.getItem('acMatrixPrompts');
        if (stored) {
            const parsed = JSON.parse(stored);
            if (Array.isArray(parsed) && parsed.length > 0) {
                return parsed;
            }
        }
    } catch (e) {
        console.error('Error loading prompts from storage:', e);
    }
    // Return default example prompt if nothing stored
    return [
        { id: 'example', name: 'Summary Prompt', body: 'Summarize the draft: {{draft_text}}' },
    ];
}

// Save prompts to localStorage
function savePromptsToStorage() {
    try {
        localStorage.setItem('acMatrixPrompts', JSON.stringify(promptStore));
    } catch (e) {
        console.error('Error saving prompts to storage:', e);
    }
}

function setupPrompts() {
    const addBtn = document.getElementById('add-prompt-btn');
    const editBtn = document.getElementById('edit-prompt-btn');
    const deleteBtn = document.getElementById('delete-prompt-btn');
    const selector = document.getElementById('prompt-selector');
    const cancelBtn = document.getElementById('prompt-cancel-btn');
    const saveBtn = document.getElementById('prompt-save-btn');

    // Load prompts from localStorage
    promptStore = loadPromptsFromStorage();
    selectedPromptId = '';
    renderPromptSelector();

    if (selector) {
        selector.addEventListener('change', onPromptSelect);
    }
    if (addBtn) {
        addBtn.addEventListener('click', () => showPromptForm('add'));
    }
    if (editBtn) {
        editBtn.addEventListener('click', () => showPromptForm('edit'));
    }
    if (deleteBtn) {
        deleteBtn.addEventListener('click', deletePrompt);
    }
    if (cancelBtn) {
        cancelBtn.addEventListener('click', hidePromptForm);
    }
    if (saveBtn) {
        saveBtn.addEventListener('click', savePrompt);
    }
}

function renderPromptSelector() {
    const selector = document.getElementById('prompt-selector');
    const deleteBtn = document.getElementById('delete-prompt-btn');
    const editBtn = document.getElementById('edit-prompt-btn');
    const bodyView = document.getElementById('prompt-body-view');
    if (!selector) return;

    selector.innerHTML = '<option value="">Select a prompt...</option>';
    promptStore.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.id;
        opt.textContent = p.name;
        selector.appendChild(opt);
    });

    const hasSelection = !!selectedPromptId;
    if (deleteBtn) {
        deleteBtn.disabled = !hasSelection;
    }
    if (editBtn) {
        editBtn.disabled = !hasSelection;
    }
    if (bodyView) {
        if (selectedPromptId) {
            const found = promptStore.find(p => p.id === selectedPromptId);
            bodyView.value = found ? resolvePromptBody(found.body) : '';
        } else {
            bodyView.value = '';
        }
    }
}

function onPromptSelect() {
    const selector = document.getElementById('prompt-selector');
    const deleteBtn = document.getElementById('delete-prompt-btn');
    const editBtn = document.getElementById('edit-prompt-btn');
    const bodyView = document.getElementById('prompt-body-view');
    if (!selector) return;

    selectedPromptId = selector.value;
    const hasSelection = !!selectedPromptId;
    if (deleteBtn) {
        deleteBtn.disabled = !hasSelection;
    }
    if (editBtn) {
        editBtn.disabled = !hasSelection;
    }
    if (bodyView) {
        const found = promptStore.find(p => p.id === selectedPromptId);
        bodyView.value = found ? resolvePromptBody(found.body) : '';
    }
}

function showPromptForm(mode = 'add') {
    const form = document.getElementById('prompt-form');
    const nameInput = document.getElementById('prompt-name-input');
    const bodyInput = document.getElementById('prompt-body-input');
    promptFormMode = mode;

    if (form) form.style.display = 'block';

    if (mode === 'edit') {
        // Must have a selected prompt
        const selected = promptStore.find(p => p.id === selectedPromptId);
        if (!selected) {
            alert('Select a prompt to edit.');
            hidePromptForm();
            return;
        }
        editingPromptId = selected.id;
        if (nameInput) nameInput.value = selected.name;
        if (bodyInput) bodyInput.value = selected.body;
    } else {
        editingPromptId = '';
        if (nameInput) nameInput.value = '';
        if (bodyInput) bodyInput.value = '';
    }
}

function hidePromptForm() {
    const form = document.getElementById('prompt-form');
    const nameInput = document.getElementById('prompt-name-input');
    const bodyInput = document.getElementById('prompt-body-input');
    if (form) form.style.display = 'none';
    if (nameInput) nameInput.value = '';
    if (bodyInput) bodyInput.value = '';
    promptFormMode = 'add';
    editingPromptId = '';
}

function savePrompt() {
    const nameInput = document.getElementById('prompt-name-input');
    const bodyInput = document.getElementById('prompt-body-input');
    if (!nameInput || !bodyInput) return;

    const name = (nameInput.value || '').trim();
    const body = (bodyInput.value || '').trim();
    if (!name || !body) {
        alert('Please enter a prompt name and text.');
        return;
    }

    if (promptFormMode === 'edit' && editingPromptId) {
        // Update existing prompt
        const existing = promptStore.find(p => p.id === editingPromptId);
        if (!existing) {
            alert('Selected prompt no longer exists.');
            hidePromptForm();
            return;
        }
        // Prevent duplicate names (other than this one)
        if (promptStore.some(p => p.id !== editingPromptId && p.name.toLowerCase() === name.toLowerCase())) {
            alert('A prompt with that name already exists.');
            return;
        }
        existing.name = name;
        existing.body = body;
        selectedPromptId = editingPromptId;
    } else {
        // Ensure unique id
        const idBase = name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'prompt';
        let id = idBase;
        let counter = 1;
        while (promptStore.some(p => p.id === id)) {
            id = `${idBase}-${counter++}`;
        }
        // Prevent duplicate names
        if (promptStore.some(p => p.name.toLowerCase() === name.toLowerCase())) {
            alert('A prompt with that name already exists.');
            return;
        }
        promptStore.push({ id, name, body });
        selectedPromptId = id;
    }

    hidePromptForm();
    savePromptsToStorage(); // Save to localStorage
    renderPromptSelector();
    const selector = document.getElementById('prompt-selector');
    if (selector) selector.value = selectedPromptId;
    onPromptSelect();
}

function deletePrompt() {
    if (!selectedPromptId) {
        alert('Select a prompt to delete.');
        return;
    }
    const prompt = promptStore.find(p => p.id === selectedPromptId);
    const confirmDelete = confirm(`Delete prompt '${prompt ? prompt.name : selectedPromptId}'?`);
    if (!confirmDelete) return;

    promptStore = promptStore.filter(p => p.id !== selectedPromptId);
    selectedPromptId = '';
    editingPromptId = '';
    savePromptsToStorage(); // Save to localStorage
    renderPromptSelector();
    onPromptSelect();
    const selector = document.getElementById('prompt-selector');
    if (selector) selector.value = '';
}

// Resolve placeholders in prompt text
function resolvePromptBody(body) {
    if (!body) return '';
    let resolved = body;
    // Replace draft text placeholder
    resolved = resolved.replace(/{{\s*draft_text\s*}}/gi, currentObservationReport || '');
    // Replace ac_missing placeholder with current missing ACs text
    const missingField = document.getElementById('missing-acs-field');
    const missingText = missingField ? (missingField.value || '') : '';
    resolved = resolved.replace(/{{\s*ac_missing\s*}}/gi, missingText);
    return resolved;
}

// Render unit checkboxes
function renderUnitCheckboxes() {
    const container = document.getElementById('unit-checkboxes-container');
    const filterToggle = document.getElementById('filter-units-toggle');
    const isFilterEnabled = filterToggle ? filterToggle.checked : false;
    
    if (!container) return;
    
    container.innerHTML = '';
    
    if (currentUnits.length === 0) {
        container.innerHTML = '<p style="color: #999; padding: 10px;">No units found in this standards file</p>';
        return;
    }
    
    // Initialize selectedUnitIds to all units if empty
    if (selectedUnitIds.length === 0 && currentUnits.length > 0) {
        selectedUnitIds = currentUnits.map(u => u.unit_id);
    }
    
    currentUnits.forEach(unit => {
        const label = document.createElement('label');
        label.className = 'unit-checkbox-item';
        label.style.cssText = 'display: block; padding: 8px; cursor: pointer; color: #e0e0e0; border-radius: 4px; margin-bottom: 4px; transition: background 0.2s;';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = unit.unit_id;
        checkbox.dataset.unitId = unit.unit_id;
        // When filter is off, all checked (but disabled). When filter is on, use selectedUnitIds
        checkbox.checked = !isFilterEnabled || selectedUnitIds.includes(unit.unit_id);
        checkbox.disabled = !isFilterEnabled;
        checkbox.style.cssText = 'margin-right: 8px; cursor: pointer;';
        checkbox.addEventListener('change', updateUnitSelection);
        
        const unitLabel = document.createElement('span');
        unitLabel.textContent = `Unit ${unit.unit_id}: ${unit.unit_name || 'Unnamed Unit'}`;
        
        label.appendChild(checkbox);
        label.appendChild(unitLabel);
        
        // Add hover effect
        label.addEventListener('mouseenter', () => {
            if (!checkbox.disabled) {
                label.style.background = '#2a2a2a';
            }
        });
        label.addEventListener('mouseleave', () => {
            label.style.background = 'transparent';
        });
        
        container.appendChild(label);
    });
    
    updateSelectionCounter();
}

// Handle filter toggle
function handleFilterToggle() {
    const filterToggle = document.getElementById('filter-units-toggle');
    const controls = document.getElementById('unit-selector-controls');
    const unitList = document.getElementById('unit-selection-list');
    const isEnabled = filterToggle.checked;
    
    if (controls) {
        controls.style.display = isEnabled ? 'block' : 'none';
    }
    
    if (unitList) {
        unitList.style.display = 'block'; // Always show when units are loaded
    }
    
    // Update checkbox states
    const checkboxes = document.querySelectorAll('#unit-checkboxes-container input[type="checkbox"]');
    checkboxes.forEach(cb => {
        cb.disabled = !isEnabled;
        if (!isEnabled) {
            // When filter is off, all are checked (but disabled)
            cb.checked = true;
        } else {
            // When filter is on, use selectedUnitIds
            // If no units selected yet, select all
            if (selectedUnitIds.length === 0 && currentUnits.length > 0) {
                selectedUnitIds = currentUnits.map(u => u.unit_id);
            }
            cb.checked = selectedUnitIds.includes(cb.value);
        }
    });
    
    updateSelectionCounter();
}

// Update unit selection
function updateUnitSelection() {
    const checkboxes = document.querySelectorAll('#unit-checkboxes-container input[type="checkbox"]:not(:disabled)');
    selectedUnitIds = Array.from(checkboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);
    
    updateSelectionCounter();
}

// Select all units
function selectAllUnits() {
    const checkboxes = document.querySelectorAll('#unit-checkboxes-container input[type="checkbox"]:not(:disabled)');
    checkboxes.forEach(cb => {
        cb.checked = true;
    });
    updateUnitSelection();
}

// Deselect all units
function deselectAllUnits() {
    const checkboxes = document.querySelectorAll('#unit-checkboxes-container input[type="checkbox"]:not(:disabled)');
    checkboxes.forEach(cb => {
        cb.checked = false;
    });
    updateUnitSelection();
}

// Update selection counter
function updateSelectionCounter() {
    const counter = document.getElementById('unit-selection-counter');
    const filterToggle = document.getElementById('filter-units-toggle');
    
    if (!counter) return;
    
    if (!filterToggle || !filterToggle.checked) {
        counter.textContent = 'Selected: All units';
        return;
    }
    
    const total = currentUnits.length;
    const selected = selectedUnitIds.length;
    counter.textContent = `Selected: ${selected} of ${total} units`;
}

// Analyze observation report(s)
async function analyzeReport() {
    const jsonFileId = document.getElementById('json-file-selector').value;
    const reportMode = document.querySelector('input[name="report-mode"]:checked')?.value || 'single';
    
    if (!jsonFileId) {
        alert('Please select a JSON standards file');
        return;
    }
    
    // Check if filter is enabled and units are selected
    const filterToggle = document.getElementById('filter-units-toggle');
    if (filterToggle && filterToggle.checked) {
        if (selectedUnitIds.length === 0) {
            alert('Please select at least one unit to analyze');
            return;
        }
    }
    
    let reports = [];
    
    if (reportMode === 'single') {
        const draftSelector = document.getElementById('draft-selector');
        const selectedDraft = draftSelector ? getDraftById(draftSelector.value) : null;
        if (!selectedDraft) {
            alert('Please select a draft to analyze');
            return;
        }
        reports = [{ name: selectedDraft.name || 'Selected Draft', text: selectedDraft.text_content || '' }];
        currentObservationReport = selectedDraft.text_content || '';
        currentAssignments = selectedDraft.assignments || {};
        renderLivePreview(selectedDraft.name, selectedDraft.text_content, currentAssignments);
    } else {
        // Bulk mode
        reports = getBulkReports();
        if (reports.length === 0) {
            alert('Please add at least one observation report');
            return;
        }
        // Store combined text for saving
        currentObservationReport = reports.map(r => `=== ${r.name} ===\n\n${r.text}`).join('\n\n');
        renderLivePreview('Bulk Reports', '', {}, reports);
    }
    
    // Store current state
    currentJsonFileId = jsonFileId;
    
    // Show loading state
    const analyzeBtn = document.getElementById('analyze-btn');
    const originalText = analyzeBtn.textContent;
    analyzeBtn.textContent = 'Analyzing...';
    analyzeBtn.disabled = true;
    
    try {
        const response = await fetch('/v2p-formatter/ac-matrix/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                json_file_id: jsonFileId,
                observation_reports: reports,  // Send array of reports
                selected_unit_ids: (filterToggle && filterToggle.checked) ? selectedUnitIds : null  // Send selected units if filter enabled
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentMatrixData = data.matrix_data;
            renderMatrix(data.matrix_data);
            document.getElementById('matrix-section').style.display = 'block';
            
            // Scroll to matrix
            document.getElementById('matrix-section').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error analyzing report:', error);
        alert('Error analyzing report');
    } finally {
        analyzeBtn.textContent = originalText;
        analyzeBtn.disabled = false;
    }
}

// Generate matrix HTML
function renderMatrix(matrixData) {
    renderHorizontalMatrix(matrixData);
    
    // Store for reference
    window.currentMatrixData = matrixData;
}

// Render horizontal style matrix
function renderHorizontalMatrix(matrixData) {
    const contentDiv = document.getElementById('matrix-content');
    const summaryDiv = document.getElementById('matrix-summary');
    
    // Render summary
    const stats = matrixData;
    let summaryHtml = `
        <h3>Coverage Summary</h3>
        <p>Total ACs: <strong>${stats.total_ac_count}</strong></p>
        <p>Covered: <strong style="color: #4a8a4a;">${stats.covered_ac_count}</strong> | Missing: <strong style="color: #8a4a4a;">${stats.missing_ac_count}</strong></p>
        <p>Coverage: <strong>${stats.coverage_percentage}%</strong></p>
    `;
    
    // Show report count if bulk mode
    if (stats.report_count && stats.report_count > 1) {
        summaryHtml += `<p style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #444;">Reports Analyzed: <strong>${stats.report_count}</strong></p>`;
        if (stats.report_names && stats.report_names.length > 0) {
            summaryHtml += `<p style="font-size: 0.9em; color: #999;">${stats.report_names.join(', ')}</p>`;
        }
    }
    
    summaryDiv.innerHTML = summaryHtml;
    
    // Generate and display missing ACs
    generateMissingACsText(matrixData);
    
    // Render matrix
    let html = '<div class="matrix-horizontal">';
    
    matrixData.units.forEach(unit => {
        html += `<div class="matrix-horizontal-unit">`;
        html += `<div class="matrix-horizontal-unit-header">`;
        html += `<h3>Unit ${escapeHtml(unit.unit_id)}: ${escapeHtml(unit.unit_name)}</h3>`;
        html += `</div>`;
        
        // Get all ACs in order and report coverage
        const allAcs = unit.all_acs || [];
        const acInfoMap = unit.ac_info_map || {};
        const reportCoverage = unit.report_coverage || {};
        const reportNames = Object.keys(reportCoverage).sort();
        
        if (allAcs.length === 0) {
            html += `<p style="color: #999;">No ACs found in this unit</p>`;
            html += `</div>`;
            return;
        }
        
        // Row 1: Standards ACs (reference row)
        html += `<div class="matrix-row matrix-standards-row">`;
        html += `<div class="matrix-row-label" style="color: #e0e0e0; font-weight: 600; min-width: 150px; display: inline-block; vertical-align: top; padding-right: 15px;">Standards ACs:</div>`;
        html += `<div class="matrix-acs-container" style="display: inline-block; flex: 1;">`;
        allAcs.forEach(acId => {
            const acInfo = acInfoMap[acId] || {};
            const acDescription = acInfo.ac_description || '';
            const tooltipText = acDescription ? escapeHtml(acDescription) : 'No description available';
            html += `<div class="ac-with-status" style="display: inline-block; vertical-align: top; margin: 0 8px 8px 0; text-align: center;">`;
            html += `<div class="matrix-horizontal-ac standards-ac" data-ac-id="${acId}" data-unit-id="${unit.unit_id}" style="cursor: pointer; text-align: center; display: block; margin-bottom: 4px; color: #e0e0e0; font-weight: 600; position: relative;">`;
            html += `${escapeHtml(acId)}`;
            if (tooltipText && tooltipText !== 'No description available') {
                html += `<div class="standards-ac-tooltip">${tooltipText}</div>`;
            }
            html += `</div>`;
            html += `<div class="matrix-horizontal-status-placeholder" style="text-align: center; display: block; height: 1.2em;"></div>`;
            html += `</div>`;
        });
        html += `</div>`;
        html += `</div>`;
        
        // Row 2+: One row per report
        reportNames.forEach(reportName => {
            const coverage = reportCoverage[reportName] || {};
            
            html += `<div class="matrix-row matrix-report-row">`;
            html += `<div class="matrix-row-label" style="color: #667eea; font-weight: 600; min-width: 150px; display: inline-block; vertical-align: top; padding-right: 15px;">${escapeHtml(reportName)}:</div>`;
            html += `<div class="matrix-acs-container" style="display: inline-block; flex: 1;">`;
            
            // Render status for each AC in the same order as standards row
            allAcs.forEach(acId => {
                const acData = coverage[acId];
                const isCovered = !!acData;
                const symbol = isCovered ? '✓' : '✗';
                const statusClass = isCovered ? 'covered' : 'missing';
                const acUniqueId = isCovered ? `${acId}-${reportName}` : `${acId}-missing-${reportName}`;
                
                html += `<div class="ac-with-status" style="display: inline-block; vertical-align: top; margin: 0 8px 8px 0; text-align: center;">`;
                html += `<div class="matrix-horizontal-ac-placeholder" style="text-align: center; display: block; margin-bottom: 4px; height: 1em; visibility: hidden;">${escapeHtml(acId)}</div>`;
                html += `<div class="matrix-horizontal-status ${statusClass}" data-ac-id="${acId}" data-unit-id="${unit.unit_id}" data-ac-unique-id="${acUniqueId}" data-report-name="${reportName || ''}" style="cursor: pointer; text-align: center; display: block; font-size: 1.2em; font-weight: bold;">${symbol}</div>`;
                html += `</div>`;
            });
            
            html += `</div>`;
            html += `</div>`;
        });
        
        // Create details panels for all covered ACs
        reportNames.forEach(reportName => {
            const coverage = reportCoverage[reportName] || {};
            Object.keys(coverage).forEach(acId => {
                const acData = coverage[acId];
                const acUniqueId = `${acId}-${reportName}`;
                
                html += `<div class="ac-details-panel" id="details-${unit.unit_id}-${acUniqueId}" style="display: none;">`;
                html += `<h4>AC ${escapeHtml(acId)} - ✓ COVERED</h4>`;
                
                if (acData.section_title) {
                    const sectionIndex = acData.section_index >= 0 ? acData.section_index : 0;
                    const sectionColor = PreviewRenderer.SECTION_COLORS[sectionIndex % PreviewRenderer.SECTION_COLORS.length];
                    
                    html += `<div class="report-source-list">`;
                    html += `<span style="color: #999; font-size: 0.85em; margin-right: 8px;">From Report:</span>`;
                    html += `<span class="report-source-item">${escapeHtml(reportName)}</span>`;
                    html += `</div>`;
                    
                    html += `<div class="section-title" style="color: ${sectionColor}; border-left-color: ${sectionColor};">Section: ${escapeHtml(acData.section_title)}</div>`;
                    html += `<div class="observation-text-section-label">Observation Text:</div>`;
                    html += `<div class="observation-text-section">${escapeHtml(acData.observation_text_section || '')}</div>`;
                } else {
                    html += `<p style="color: #999;">(No section information available)</p>`;
                }
                
                html += `</div>`;
            });
        });
        
        // Create details panels for missing ACs (clicking on standards row AC)
        allAcs.forEach(acId => {
            // Check if AC is covered in any report
            let isCoveredAnywhere = false;
            reportNames.forEach(reportName => {
                if (reportCoverage[reportName] && reportCoverage[reportName][acId]) {
                    isCoveredAnywhere = true;
                }
            });
            
            if (!isCoveredAnywhere) {
                const acUniqueId = `${acId}-standards`;
                html += `<div class="ac-details-panel" id="details-${unit.unit_id}-${acUniqueId}" style="display: none;">`;
                html += `<h4>AC ${escapeHtml(acId)} - ✗ MISSING</h4>`;
                html += `<p style="color: #999;">(Not covered in any report)</p>`;
                html += `</div>`;
            }
        });
        
        html += `</div>`;
    });
    
    html += '</div>';
    contentDiv.innerHTML = html;
    
    // Show missing ACs section
    document.getElementById('missing-acs-section').style.display = 'block';
    document.getElementById('prompts-section').style.display = 'block';
    
    // Add click handlers and tooltip positioning for standards row ACs
    document.querySelectorAll('.standards-ac').forEach(acEl => {
        // Click handler
        acEl.addEventListener('click', function() {
            const acId = this.dataset.acId;
            const unitId = this.dataset.unitId;
            
            // Try to find first covered occurrence, otherwise show missing
            const reportName = this.dataset.reportName;
            let detailsPanel = null;
            
            if (reportName) {
                // Try specific report
                detailsPanel = document.getElementById(`details-${unitId}-${acId}-${reportName}`);
            }
            
            if (!detailsPanel) {
                // Try standards panel (for missing)
                detailsPanel = document.getElementById(`details-${unitId}-${acId}-standards`);
            }
            
            if (detailsPanel) {
                const isVisible = detailsPanel.style.display !== 'none';
                // Hide all other detail panels in this unit first
                document.querySelectorAll(`[id^="details-${unitId}-"]`).forEach(panel => {
                    panel.style.display = 'none';
                });
                // Toggle the clicked panel
                detailsPanel.style.display = isVisible ? 'none' : 'block';
            }
        });
        
        // Tooltip positioning on hover - ensure it's always fully visible
        const tooltip = acEl.querySelector('.standards-ac-tooltip');
        if (tooltip) {
            acEl.addEventListener('mouseenter', function() {
                const rect = acEl.getBoundingClientRect();
                const viewportHeight = window.innerHeight;
                const viewportWidth = window.innerWidth;
                const margin = 10;
                
                // Get tooltip dimensions (use computed styles for accurate size)
                const tooltipStyle = window.getComputedStyle(tooltip);
                const tooltipWidth = parseFloat(tooltipStyle.maxWidth) || 700;
                const tooltipHeight = tooltip.offsetHeight || 100;
                
                // Reset positioning
                tooltip.style.left = '';
                tooltip.style.right = '';
                tooltip.style.top = '';
                tooltip.style.bottom = '';
                tooltip.style.transform = '';
                tooltip.style.marginTop = '';
                tooltip.style.marginBottom = '';
                
                // Calculate horizontal position - center on AC element, but keep within viewport
                let leftPos = rect.left + (rect.width / 2) - (tooltipWidth / 2);
                
                // Adjust if tooltip would be cut off on the left
                if (leftPos < margin) {
                    leftPos = margin;
                }
                // Adjust if tooltip would be cut off on the right
                else if (leftPos + tooltipWidth > viewportWidth - margin) {
                    leftPos = viewportWidth - tooltipWidth - margin;
                }
                
                // Calculate vertical position - prefer above, but use below if needed
                const spaceAbove = rect.top;
                const spaceBelow = viewportHeight - rect.bottom;
                const useBelow = spaceAbove < tooltipHeight + margin && spaceBelow > spaceAbove;
                
                if (useBelow) {
                    // Position below AC element
                    const topPos = rect.bottom + margin;
                    tooltip.style.top = topPos + 'px';
                    tooltip.style.bottom = 'auto';
                    tooltip.setAttribute('data-below', 'true');
                } else {
                    // Position above AC element (default)
                    const bottomPos = viewportHeight - rect.top + margin;
                    tooltip.style.bottom = bottomPos + 'px';
                    tooltip.style.top = 'auto';
                    tooltip.removeAttribute('data-below');
                }
                
                // Set horizontal position (using fixed positioning relative to viewport)
                tooltip.style.left = leftPos + 'px';
            });
        }
    });
    
    // Add click handlers for status icons (report rows)
    document.querySelectorAll('.matrix-horizontal-status').forEach(statusEl => {
        statusEl.addEventListener('click', function() {
            const acUniqueId = this.dataset.acUniqueId;
            const unitId = this.dataset.unitId;
            
            if (acUniqueId && unitId) {
                const detailsPanel = document.getElementById(`details-${unitId}-${acUniqueId}`);
                if (detailsPanel) {
                    const isVisible = detailsPanel.style.display !== 'none';
                    // Hide all other detail panels in this unit first
                    document.querySelectorAll(`[id^="details-${unitId}-"]`).forEach(panel => {
                        panel.style.display = 'none';
                    });
                    // Toggle the clicked panel
                    detailsPanel.style.display = isVisible ? 'none' : 'block';
                } else {
                    console.warn(`Details panel not found for AC ${acUniqueId} in unit ${unitId}`);
                }
            }
        });
    });
}

// Generate missing ACs text in format: "draft name: unit:ac;unit:ac"
function generateMissingACsText(matrixData) {
    const missingAcsField = document.getElementById('missing-acs-field');
    if (!missingAcsField) return;
    
    const missingACsByReport = {};
    
    // Go through each unit and find missing ACs per report
    matrixData.units.forEach(unit => {
        const unitId = unit.unit_id;
        const allAcs = unit.all_acs || [];
        const reportCoverage = unit.report_coverage || {};
        const reportNames = Object.keys(reportCoverage).sort();
        
        // If no reports, all ACs are missing
        if (reportNames.length === 0) {
            const defaultReportName = 'Selected Draft';
            if (!missingACsByReport[defaultReportName]) {
                missingACsByReport[defaultReportName] = [];
            }
            allAcs.forEach(acId => {
                missingACsByReport[defaultReportName].push(`${unitId}:${acId}`);
            });
        } else {
            // For each report, find missing ACs
            reportNames.forEach(reportName => {
                if (!missingACsByReport[reportName]) {
                    missingACsByReport[reportName] = [];
                }
                const coverage = reportCoverage[reportName] || {};
                
                allAcs.forEach(acId => {
                    if (!coverage[acId]) {
                        // AC is missing in this report
                        missingACsByReport[reportName].push(`${unitId}:${acId}`);
                    }
                });
            });
        }
    });
    
    // Format the text: "draft name: unit:ac;unit:ac"
    let formattedText = '';
    Object.keys(missingACsByReport).sort().forEach(reportName => {
        const missingACs = missingACsByReport[reportName];
        if (missingACs.length > 0) {
            formattedText += `${reportName}: ${missingACs.join(';')}\n`;
        }
    });
    
    // Update the textarea
    missingAcsField.value = formattedText.trim();
}

// Save matrix
function showSaveMatrixDialog() {
    if (!currentMatrixData) {
        alert('No matrix to save. Please analyze a report first.');
        return;
    }
    
    const dialog = document.getElementById('save-matrix-dialog');
    const nameInput = document.getElementById('matrix-name-input');
    
    // Suggest name based on current date/time
    const now = new Date();
    const suggestedName = `Matrix ${now.toLocaleDateString()} ${now.toLocaleTimeString()}`;
    nameInput.value = suggestedName;
    
    dialog.style.display = 'flex';
    nameInput.focus();
}

async function saveMatrix() {
    const nameInput = document.getElementById('matrix-name-input');
    const name = nameInput.value.trim();
    
    if (!name) {
        alert('Please enter a matrix name');
        return;
    }
    
    if (!currentMatrixData || !currentJsonFileId) {
        alert('No matrix data to save');
        return;
    }
    
    try {
        const response = await fetch('/v2p-formatter/ac-matrix/matrices', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                json_file_id: currentJsonFileId,
                observation_report: currentObservationReport,
                matrix_data: currentMatrixData
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`Matrix '${name}' saved successfully!`);
            document.getElementById('save-matrix-dialog').style.display = 'none';
            loadMatrixList(); // Refresh list
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error saving matrix:', error);
        alert('Error saving matrix');
    }
}

// Load matrix list
async function loadMatrixList() {
    try {
        const response = await fetch('/v2p-formatter/ac-matrix/matrices');
        const data = await response.json();
        
        if (data.success) {
            const menu = document.getElementById('load-matrix-menu');
            menu.innerHTML = '';
            
            if (data.matrices.length === 0) {
                menu.innerHTML = '<div class="dropdown-menu-item">No saved matrices</div>';
            } else {
                data.matrices.forEach(matrix => {
                    const item = document.createElement('div');
                    item.className = 'dropdown-menu-item';
                    item.innerHTML = `
                        <div class="dropdown-menu-item-name">${escapeHtml(matrix.name)}</div>
                        <div class="dropdown-menu-item-meta">${matrix.json_file_name} • ${new Date(matrix.created_at).toLocaleDateString()}</div>
                    `;
                    item.addEventListener('click', () => loadMatrix(matrix.matrix_id));
                    menu.appendChild(item);
                });
            }
        }
    } catch (error) {
        console.error('Error loading matrix list:', error);
    }
}

function toggleLoadMatrixMenu() {
    const menu = document.getElementById('load-matrix-menu');
    if (menu.style.display === 'none' || !menu.style.display) {
        loadMatrixList();
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
}

// Load matrix
async function loadMatrix(matrixId) {
    try {
        const response = await fetch(`/v2p-formatter/ac-matrix/matrices/${matrixId}`);
        const data = await response.json();
        
        if (data.success) {
            const matrixData = data.matrix_data;
            
            // Restore state
            currentJsonFileId = matrixData.json_file_id;
            currentObservationReport = matrixData.observation_report;
            currentMatrixData = matrixData.analysis;
            
            // Restore UI
            const jsonSelector = document.getElementById('json-file-selector');
            // Try to set the JSON file selector
            // If file doesn't exist in selector, that's okay - user can select it
            if (jsonSelector.querySelector(`option[value="${currentJsonFileId}"]`)) {
                jsonSelector.value = currentJsonFileId;
            }
            
            // Restore preview
            renderLivePreview(matrixData.name || 'Loaded Matrix', currentObservationReport);
            
            // Render matrix
            renderMatrix(currentMatrixData);
            document.getElementById('matrix-section').style.display = 'block';
            
            // Close menu
            document.getElementById('load-matrix-menu').style.display = 'none';
            
            // Scroll to matrix
            document.getElementById('matrix-section').scrollIntoView({ behavior: 'smooth' });
            
            console.log(`Matrix '${matrixData.name}' loaded successfully`);
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error loading matrix:', error);
        alert('Error loading matrix');
    }
}

// Delete matrix
async function showDeleteMatrixDialog() {
    // Load list of matrices
    try {
        const response = await fetch('/v2p-formatter/ac-matrix/matrices');
        const data = await response.json();
        
        if (!data.success || data.matrices.length === 0) {
            alert('No saved matrices to delete');
            return;
        }
        
        // Show list for selection
        const matrixList = data.matrices.map(m => 
            `${m.name} (${m.json_file_name}, ${new Date(m.created_at).toLocaleDateString()})`
        ).join('\n');
        
        const index = prompt(`Select matrix to delete (enter number 1-${data.matrices.length}):\n\n${data.matrices.map((m, i) => `${i + 1}. ${m.name}`).join('\n')}`);
        
        if (index === null) return;
        
        const selectedIndex = parseInt(index) - 1;
        if (isNaN(selectedIndex) || selectedIndex < 0 || selectedIndex >= data.matrices.length) {
            alert('Invalid selection');
            return;
        }
        
        const selectedMatrix = data.matrices[selectedIndex];
        
        if (confirm(`Are you sure you want to delete "${selectedMatrix.name}"?`)) {
            await deleteMatrix(selectedMatrix.matrix_id);
        }
    } catch (error) {
        console.error('Error loading matrices for deletion:', error);
        alert('Error loading matrices');
    }
}

async function deleteMatrix(matrixId) {
    try {
        const response = await fetch(`/v2p-formatter/ac-matrix/matrices/${matrixId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Matrix deleted successfully!');
            
            // If deleted matrix was currently loaded, clear it
            if (currentMatrixData) {
                // Check if we need to clear (would need to track current matrix ID)
                loadMatrixList(); // Refresh list
            }
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error deleting matrix:', error);
        alert('Error deleting matrix');
    }
}

// escapeHtml is provided by PreviewRenderer library

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const loadBtn = document.getElementById('load-matrix-btn');
    const menu = document.getElementById('load-matrix-menu');
    
    if (loadBtn && menu && !loadBtn.contains(event.target) && !menu.contains(event.target)) {
        menu.style.display = 'none';
    }
});

