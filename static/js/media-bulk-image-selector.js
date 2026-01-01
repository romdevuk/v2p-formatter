/**
 * Media Bulk Image Selector Modal Component
 * Full-screen modal for bulk image selection with zoom controls
 */

(function() {
    'use strict';

    // Modal state
    const modalState = {
        isOpen: false,
        zoomLevel: 1,  // 1-10, default 1 (8 columns)
        columns: 8,
        availableImages: [],
        isLoading: false
    };

    // Initialize modal
    function init() {
        createModalStructure();
        attachEventListeners();
    }

    // Create modal HTML structure
    function createModalStructure() {
        const modalHTML = `
            <div id="mediaBulkSelectorModal" class="modal-overlay">
                <div class="modal-container">
                    <!-- Header Bar -->
                    <div class="modal-header">
                        <div class="header-left">
                            <button class="close-btn" id="modalCloseBtn" aria-label="Close modal">←</button>
                            <h2 class="modal-title">Media Selector</h2>
                        </div>
                        <div class="header-right">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <label style="color: #e0e0e0; font-size: 14px; white-space: nowrap;">Sort by:</label>
                                <select id="modalSortBy" style="padding: 6px 12px; background: #1e1e1e; color: #e0e0e0; border: 1px solid #555; border-radius: 4px; font-size: 14px; cursor: pointer;">
                                    <option value="name" selected>Name</option>
                                    <option value="date">Date/Time</option>
                                </select>
                            </div>
                            <div class="selection-counter" id="modalSelectionCounter">
                                <span id="modalSelectionCount">0</span> selected
                            </div>
                            <button class="reset-order-btn" id="modalResetOrderBtn">Reset Order</button>
                            <button class="reset-selection-btn" id="modalResetSelectionBtn">Reset Selection</button>
                        </div>
                    </div>
                    
                    <!-- Content Area (Scrollable) -->
                    <div class="modal-content" id="modalContent">
                        <div class="loading-placeholder">
                            <p>Loading images...</p>
                        </div>
                    </div>
                    
                    <!-- Footer Bar (Zoom Controls) -->
                    <div class="modal-footer">
                        <div class="zoom-controls">
                            <button class="zoom-btn" id="zoomOutBtn" aria-label="Zoom out">−</button>
                            <input type="range" 
                                   class="zoom-slider" 
                                   id="zoomSlider" 
                                   min="1" 
                                   max="10" 
                                   value="1"
                                   aria-label="Zoom level">
                            <button class="zoom-btn" id="zoomInBtn" aria-label="Zoom in">+</button>
                            <div class="zoom-level-indicator" id="zoomLevelIndicator">
                                Level 1 (8 per row)
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Load CSS if not already loaded
        if (!document.getElementById('mediaBulkSelectorCSS')) {
            const link = document.createElement('link');
            link.id = 'mediaBulkSelectorCSS';
            link.rel = 'stylesheet';
            link.href = '/v2p-formatter/static/css/media-bulk-image-selector.css';
            document.head.appendChild(link);
        }
    }

    // Attach event listeners
    function attachEventListeners() {
        const modal = document.getElementById('mediaBulkSelectorModal');
        const closeBtn = document.getElementById('modalCloseBtn');
        const zoomSlider = document.getElementById('zoomSlider');
        const zoomInBtn = document.getElementById('zoomInBtn');
        const zoomOutBtn = document.getElementById('zoomOutBtn');
        const resetOrderBtn = document.getElementById('modalResetOrderBtn');

        // Close modal
        if (closeBtn) {
            closeBtn.addEventListener('click', closeModal);
        }

        // Escape key to close
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && modalState.isOpen) {
                closeModal();
            }
        });

        // Zoom controls
        if (zoomSlider) {
            zoomSlider.addEventListener('input', function() {
                updateZoom(parseInt(this.value));
            });
        }

        if (zoomInBtn) {
            zoomInBtn.addEventListener('click', function() {
                if (modalState.zoomLevel < 10) {
                    updateZoom(modalState.zoomLevel + 1);
                    zoomSlider.value = modalState.zoomLevel;
                }
            });
        }

        if (zoomOutBtn) {
            zoomOutBtn.addEventListener('click', function() {
                if (modalState.zoomLevel > 1) {
                    updateZoom(modalState.zoomLevel - 1);
                    zoomSlider.value = modalState.zoomLevel;
                }
            });
        }

        // Reset order
        if (resetOrderBtn) {
            resetOrderBtn.addEventListener('click', function() {
                resetOrder();
            });
        }

        // Reset selection
        const resetSelectionBtn = document.getElementById('modalResetSelectionBtn');
        if (resetSelectionBtn) {
            resetSelectionBtn.addEventListener('click', function() {
                resetSelection();
            });
        }

        // Sort by selector in modal
        const modalSortBy = document.getElementById('modalSortBy');
        if (modalSortBy) {
            // Sync with main view sort order
            modalSortBy.value = (window.appData && window.appData.sortBy) || 'name';
            modalSortBy.addEventListener('change', function() {
                // Update main view sort order
                if (window.appData) {
                    window.appData.sortBy = this.value;
                }
                // Re-render modal with new sort order
                if (modalState.availableImages.length > 0) {
                    renderImageGrid(modalState.availableImages, {});
                }
            });
        }
    }

    // Open modal
    function openModal() {
        const modal = document.getElementById('mediaBulkSelectorModal');
        if (!modal) {
            console.error('Modal not found');
            return;
        }

        modalState.isOpen = true;
        modal.classList.add('open');
        document.body.style.overflow = 'hidden'; // Prevent body scroll

        // Load existing selections from window.appData
        if (window.appData && window.appData.selectedImages) {
            // Selections are already loaded, just render
        }

        // Load images
        loadImages();

        // Update selection counter
        updateSelectionCounter();
        
        // Set default zoom to Level 1 (8 columns) if not already set
        const slider = document.getElementById('zoomSlider');
        if (slider && !localStorage.getItem('mediaSelectorZoomLevel')) {
            updateZoom(1);
            slider.value = 1;
        } else if (slider) {
            // Load saved preference
            const savedZoom = localStorage.getItem('mediaSelectorZoomLevel');
            if (savedZoom) {
                const zoomLevel = parseInt(savedZoom);
                if (zoomLevel >= 1 && zoomLevel <= 10) {
                    updateZoom(zoomLevel);
                    slider.value = zoomLevel;
                } else {
                    updateZoom(1);
                    slider.value = 1;
                }
            } else {
                updateZoom(1);
                slider.value = 1;
            }
        }
    }

    // Close modal
    function closeModal() {
        const modal = document.getElementById('mediaBulkSelectorModal');
        if (!modal) {
            return;
        }

        modalState.isOpen = false;
        modal.classList.remove('open');
        document.body.style.overflow = ''; // Restore body scroll
    }

    // Load images from API
    function loadImages() {
        const qualification = document.getElementById('qualificationSelect')?.value;
        const learner = document.getElementById('learnerSelect')?.value;

        if (!qualification || !learner) {
            showEmptyState('Please select both qualification and learner first');
            return;
        }

        modalState.isLoading = true;
        const content = document.getElementById('modalContent');
        content.innerHTML = '<div class="loading-placeholder"><p>Loading images...</p></div>';

        fetch(`/v2p-formatter/list_images?qualification=${encodeURIComponent(qualification)}&learner=${encodeURIComponent(learner)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                modalState.isLoading = false;
                if (data.success && data.files && data.files.length > 0) {
                    modalState.availableImages = data.files;
                    renderImageGrid(data.files, data.tree);
                } else {
                    const message = data.error || 'No images found';
                    showEmptyState(message);
                }
            })
            .catch(error => {
                modalState.isLoading = false;
                console.error('Error loading images:', error);
                showEmptyState(`Error loading images: ${error.message || 'Unknown error'}`);
            });
    }

    // Sort images based on selected sort order
    function sortImages(images) {
        // Get sort order from main view or default to 'name'
        const sortBy = (window.appData && window.appData.sortBy) || 'name';
        const sorted = [...images];
        
        if (sortBy === 'date') {
            // Sort by modification time (newest first, then oldest)
            sorted.sort((a, b) => {
                const timeA = a.modified_time || a.modified_date || 0;
                const timeB = b.modified_time || b.modified_date || 0;
                return timeB - timeA; // Newest first
            });
        } else if (sortBy === 'name') {
            // Sort by name (alphabetical)
            sorted.sort((a, b) => a.name.localeCompare(b.name));
        }
        
        return sorted;
    }

    // Render image grid with folder structure
    function renderImageGrid(images, tree) {
        const content = document.getElementById('modalContent');
        if (!images || images.length === 0) {
            showEmptyState('No images found');
            return;
        }

        // Sort images first
        const sortedImages = sortImages(images);

        let html = '';

        // Organize images by folder
        const folders = {};
        sortedImages.forEach(img => {
            const folder = img.folder || 'root';
            if (!folders[folder]) {
                folders[folder] = [];
            }
            folders[folder].push(img);
        });

        // Render subfolders first (sorted)
        const subfolders = Object.keys(folders).filter(f => f !== 'root').sort();
        subfolders.forEach(folder => {
            html += renderFolder(folder, folders[folder], true);
        });

        // Render root images last
        if (folders['root'] && folders['root'].length > 0) {
            if (subfolders.length > 0) {
                html += '<div class="folder-header"><h3 class="folder-name">📁 Root Folder<span class="folder-count">(' + folders['root'].length + ' images)</span></h3></div>';
            }
            html += renderImageGridItems(folders['root'], 'root');
        }

        content.innerHTML = html;
        attachImageEventListeners();
        
        // Attach folder toggle listeners
        attachFolderToggleListeners();
    }

    // Render folder with images (collapsible)
    function renderFolder(folderName, images, isSubfolder) {
        const folderId = 'modal-folder-' + folderName.replace(/[^a-zA-Z0-9]/g, '-');
        
        // Check if any images in this folder are selected - if so, expand the folder
        const hasSelectedImages = images.some(img => isImageSelected(img.path));
        const isCollapsed = !hasSelectedImages; // Expand if folder contains selected images
        
        let html = '';
        
        if (isSubfolder) {
            html += `<div class="folder-container" data-folder-id="${folderId}">`;
            html += `<div class="folder-header clickable" data-folder-toggle="${folderId}">`;
            html += `<span class="folder-icon">${isCollapsed ? '▶' : '▼'}</span>`;
            html += `<h3 class="folder-name">📁 ${escapeHtml(folderName)}<span class="folder-count">(${images.length} images)</span></h3>`;
            html += `</div>`;
            html += `<div class="folder-content" id="${folderId}" style="display: ${isCollapsed ? 'none' : 'block'}; margin-top: 10px;">`;
        }
        
        html += renderImageGridItems(images, folderName);
        
        if (isSubfolder) {
            html += `</div></div>`; // Close folder-content and folder-container
        }
        
        return html;
    }

    // Render image grid items
    function renderImageGridItems(images, folderName) {
        const itemWidth = calculateItemWidth();
        let html = '<div class="image-grid" style="gap: 16px;">';
        
        // Sort images by name
        images.sort((a, b) => a.name.localeCompare(b.name));
        
        images.forEach((img, index) => {
            const isSelected = isImageSelected(img.path);
            const sequenceNumber = getSequenceNumber(img.path);
            const cacheBuster = new Date().getTime();
            const thumbnailUrl = `/v2p-formatter/thumbnail?path=${encodeURIComponent(img.path)}&size=240x180&t=${cacheBuster}`;
            
            html += `
                <div class="image-item ${isSelected ? 'selected' : ''}" 
                     data-path="${escapeHtml(img.path)}" 
                     data-name="${escapeHtml(img.name)}"
                     data-folder="${escapeHtml(folderName)}"
                     style="width: ${itemWidth};">
                    <div class="thumbnail-container">
                        <input type="checkbox" 
                               class="checkbox" 
                               ${isSelected ? 'checked' : ''}
                               data-path="${escapeHtml(img.path)}">
                        ${isSelected && sequenceNumber ? `<div class="sequence-badge">${sequenceNumber}</div>` : ''}
                        <img src="${thumbnailUrl}" 
                             alt="${escapeHtml(img.name)}"
                             onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
                             onload="this.nextElementSibling.style.display='none';">
                        <div style="display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; flex-direction: column; align-items: center; justify-content: center; color: #999; font-size: 11px; background: #1a1a1a;">
                            <span style="font-size: 2em;">🖼️</span>
                        </div>
                    </div>
                    <div class="image-name">${escapeHtml(img.name)}</div>
                    <div class="image-size">(${(img.size_mb || 0).toFixed(2)} MB)</div>
                </div>
            `;
        });
        
        html += '</div>';
        return html;
    }

    // Calculate item width based on columns
    function calculateItemWidth() {
        const gap = 16;
        const percentage = 100 / modalState.columns;
        return `calc(${percentage}% - ${gap}px)`;
    }

    // Check if image is selected
    function isImageSelected(imagePath) {
        if (!window.appData || !window.appData.selectedImages) {
            return false;
        }
        return window.appData.selectedImages.some(img => img.path === imagePath);
    }

    // Get sequence number for selected image
    function getSequenceNumber(imagePath) {
        if (!window.appData || !window.appData.selectedImages) {
            return null;
        }
        const selected = window.appData.selectedImages.find(img => img.path === imagePath);
        return selected ? selected.sequence : null;
    }

    // Attach event listeners to image items
    function attachImageEventListeners() {
        const imageItems = document.querySelectorAll('#modalContent .image-item');
        imageItems.forEach(item => {
            // Click on image item toggles selection
            item.addEventListener('click', function(e) {
                // Don't toggle if clicking checkbox (handled separately)
                if (e.target.type === 'checkbox') {
                    return;
                }
                const path = this.dataset.path;
                toggleImageSelection(path);
            });

            // Checkbox click
            const checkbox = item.querySelector('.checkbox');
            if (checkbox) {
                checkbox.addEventListener('click', function(e) {
                    e.stopPropagation(); // Prevent item click
                    const path = this.dataset.path;
                    toggleImageSelection(path);
                });
            }
        });
    }

    // Toggle image selection with auto-save
    function toggleImageSelection(imagePath) {
        // Ensure window.appData exists
        if (!window.appData) {
            window.appData = {};
        }
        if (!window.appData.selectedImages) {
            window.appData.selectedImages = [];
        }
        if (!window.appData.imageOrder) {
            window.appData.imageOrder = [];
        }

        // Find image info
        const image = modalState.availableImages.find(img => img.path === imagePath);
        if (!image) {
            console.error('Image not found:', imagePath);
            return;
        }

        // Check if already selected
        const existingIndex = window.appData.selectedImages.findIndex(img => img.path === imagePath);
        const isSelected = existingIndex !== -1;

        if (isSelected) {
            // Deselect: Remove from selectedImages
            window.appData.selectedImages.splice(existingIndex, 1);
            window.appData.imageOrder = window.appData.imageOrder.filter(path => path !== imagePath);
        } else {
            // Select: Add to selectedImages with sequence number
            const sequenceNumber = window.appData.selectedImages.length + 1;
            window.appData.selectedImages.push({
                path: imagePath,
                name: image.name,
                folder: image.folder || 'root',
                sequence: sequenceNumber
            });
            window.appData.imageOrder.push(imagePath);
        }

        // Update sequence numbers for all selected images
        updateSequenceNumbers();

        // Auto-save: Sync to main view immediately
        syncSelectionToMainView();

        // Update UI
        updateImageItemUI(imagePath);
        updateSelectionCounter();
    }

    // Update sequence numbers for all selected images
    function updateSequenceNumbers() {
        window.appData.selectedImages.forEach((img, index) => {
            img.sequence = index + 1;
        });
    }

    // Sync selection to main view (auto-save)
    function syncSelectionToMainView() {
        // Update main view selection count badge if it exists
        const mainSelectionCount = document.getElementById('selectionCount');
        if (mainSelectionCount) {
            mainSelectionCount.textContent = window.appData.selectedImages.length;
        }

        const mainSelectionBadge = document.getElementById('selectionCountBadge');
        if (mainSelectionBadge) {
            if (window.appData.selectedImages.length > 0) {
                mainSelectionBadge.style.display = 'block';
            } else {
                mainSelectionBadge.style.display = 'none';
            }
        }

        // Trigger custom event for main view to update (if needed)
        const event = new CustomEvent('imageSelectionChanged', {
            detail: {
                selectedImages: window.appData.selectedImages,
                imageOrder: window.appData.imageOrder
            }
        });
        document.dispatchEvent(event);
    }

    // Update individual image item UI
    function updateImageItemUI(imagePath) {
        const item = document.querySelector(`#modalContent .image-item[data-path="${escapeHtml(imagePath)}"]`);
        if (!item) return;

        const isSelected = isImageSelected(imagePath);
        const sequenceNumber = getSequenceNumber(imagePath);
        const checkbox = item.querySelector('.checkbox');
        const sequenceBadge = item.querySelector('.sequence-badge');

        // Update item class
        if (isSelected) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }

        // Update checkbox
        if (checkbox) {
            checkbox.checked = isSelected;
        }

        // Update or create sequence badge
        if (isSelected && sequenceNumber) {
            if (sequenceBadge) {
                sequenceBadge.textContent = sequenceNumber;
                sequenceBadge.style.display = 'flex';
            } else {
                // Create sequence badge
                const badge = document.createElement('div');
                badge.className = 'sequence-badge';
                badge.textContent = sequenceNumber;
                const thumbnailContainer = item.querySelector('.thumbnail-container');
                if (thumbnailContainer) {
                    thumbnailContainer.appendChild(badge);
                }
            }
        } else {
            // Remove sequence badge
            if (sequenceBadge) {
                sequenceBadge.style.display = 'none';
            }
        }
    }

    // Reset order to default (alphabetical by folder/name)
    function resetOrder() {
        if (!window.appData || !window.appData.selectedImages || window.appData.selectedImages.length === 0) {
            return;
        }

        // Sort selected images by folder, then by name
        window.appData.selectedImages.sort((a, b) => {
            if (a.folder !== b.folder) {
                return a.folder.localeCompare(b.folder);
            }
            return a.name.localeCompare(b.name);
        });

        // Update sequence numbers
        updateSequenceNumbers();

        // Update imageOrder array
        window.appData.imageOrder = window.appData.selectedImages.map(img => img.path);

        // Auto-save
        syncSelectionToMainView();

        // Re-render grid to reflect new order
        if (modalState.availableImages.length > 0) {
            // Re-render with updated selections
            const content = document.getElementById('modalContent');
            const currentHTML = content.innerHTML;
            // Update all sequence badges
            window.appData.selectedImages.forEach(img => {
                updateImageItemUI(img.path);
            });
        }

        updateSelectionCounter();
    }

    // Reset selection - clear all selected images
    function resetSelection() {
        // Clear all selected images
        if (window.appData) {
            window.appData.selectedImages = [];
            window.appData.imageOrder = [];
        }

        // Auto-save
        syncSelectionToMainView();

        // Re-render grid to remove selection indicators
        if (modalState.availableImages.length > 0) {
            const content = document.getElementById('modalContent');
            const imageItems = content.querySelectorAll('.image-item');
            imageItems.forEach(item => {
                const path = item.dataset.path;
                updateImageItemUI(path);
            });
        }

        updateSelectionCounter();
    }

    // Attach folder toggle listeners using event delegation for reliability
    function attachFolderToggleListeners() {
        const modalContent = document.getElementById('modalContent');
        if (!modalContent) {
            console.error('❌ Modal content not found');
            return;
        }
        
        // Remove existing listener if any (to prevent duplicates)
        if (modalContent._folderToggleHandler) {
            modalContent.removeEventListener('click', modalContent._folderToggleHandler, true);
        }
        
        // Create new event handler
        modalContent._folderToggleHandler = function(e) {
            // Check if click is on a folder header
            const header = e.target.closest('.folder-header.clickable[data-folder-toggle]');
            if (!header) return;
            
            e.preventDefault();
            e.stopPropagation();
            
            const folderId = header.dataset.folderToggle;
            if (folderId) {
                console.log('🖱️ Folder header clicked:', folderId);
                toggleModalFolder(folderId);
            }
        };
        
        // Attach event listener using event delegation (capture phase)
        modalContent.addEventListener('click', modalContent._folderToggleHandler, true);
        
        const folderHeaders = document.querySelectorAll('#modalContent .folder-header.clickable[data-folder-toggle]');
        console.log(`✅ Using event delegation for ${folderHeaders.length} folder headers`);
    }

    // Toggle folder expand/collapse
    function toggleModalFolder(folderId) {
        console.log('🔄 toggleModalFolder called with:', folderId);
        const content = document.getElementById(folderId);
        if (!content) {
            console.error('❌ Folder content element not found:', folderId);
            return;
        }
        
        const container = content.closest('.folder-container');
        if (!container) {
            console.error('❌ Folder container not found for:', folderId);
            return;
        }
        
        const header = container.querySelector('.folder-header.clickable');
        if (!header) {
            console.error('❌ Folder header not found');
            return;
        }
        
        const icon = header.querySelector('.folder-icon');
        if (!icon) {
            console.error('❌ Folder icon not found');
            return;
        }
        
        const isVisible = content.style.display !== 'none';
        const newDisplay = isVisible ? 'none' : 'block';
        const newIcon = isVisible ? '▶' : '▼';
        
        console.log('📂 Toggling folder:', { folderId, isVisible, newDisplay, newIcon });
        
        content.style.display = newDisplay;
        icon.textContent = newIcon;
        
        console.log('✅ Folder toggled successfully');
    }

    // Make toggleModalFolder globally accessible
    window.toggleModalFolder = toggleModalFolder;

    // Utility: Escape HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Show empty state
    function showEmptyState(message) {
        const content = document.getElementById('modalContent');
        content.innerHTML = `<div class="empty-state"><p>${message}</p></div>`;
    }

    // Update zoom level
    function updateZoom(level) {
        if (level < 1 || level > 10) return;

        modalState.zoomLevel = level;
        modalState.columns = calculateColumnsFromZoom(level);

        // Update UI
        const slider = document.getElementById('zoomSlider');
        const indicator = document.getElementById('zoomLevelIndicator');
        const zoomInBtn = document.getElementById('zoomInBtn');
        const zoomOutBtn = document.getElementById('zoomOutBtn');

        if (slider) slider.value = level;
        if (indicator) indicator.textContent = `Level ${level} (${modalState.columns} per row)`;
        if (zoomInBtn) zoomInBtn.disabled = level >= 10;
        if (zoomOutBtn) zoomOutBtn.disabled = level <= 1;

        // Save zoom preference to localStorage
        localStorage.setItem('mediaSelectorZoomLevel', level.toString());

        // Re-render grid with new column count
        if (modalState.availableImages.length > 0) {
            // Get current tree structure (we need to reconstruct it)
            const folders = {};
            modalState.availableImages.forEach(img => {
                const folder = img.folder || 'root';
                if (!folders[folder]) {
                    folders[folder] = [];
                }
                folders[folder].push(img);
            });

            // Re-render with new column count
            const content = document.getElementById('modalContent');
            let html = '';

            // Render subfolders first
            const subfolders = Object.keys(folders).filter(f => f !== 'root').sort();
            subfolders.forEach(folder => {
                html += renderFolder(folder, folders[folder], true);
            });

            // Render root images
            if (folders['root'] && folders['root'].length > 0) {
                if (subfolders.length > 0) {
                    html += '<div class="folder-header"><h3 class="folder-name">📁 Root Folder<span class="folder-count">(' + folders['root'].length + ' images)</span></h3></div>';
                }
                html += renderImageGridItems(folders['root'], 'root');
            }

            content.innerHTML = html;
            attachImageEventListeners();
        }
    }

    // Calculate columns from zoom level
    function calculateColumnsFromZoom(zoomLevel) {
        const columnMap = {
            1: 8, 2: 7, 3: 6, 4: 5, 5: 4,
            6: 4, 7: 3, 8: 3, 9: 2, 10: 2
        };
        return columnMap[zoomLevel] || 4;
    }

    // Update selection counter
    function updateSelectionCounter() {
        const counter = document.getElementById('modalSelectionCounter');
        const countSpan = document.getElementById('modalSelectionCount');
        
        // Get current selection count from window.appData (if available)
        const selectedCount = (window.appData && window.appData.selectedImages) 
            ? window.appData.selectedImages.length 
            : 0;

        if (countSpan) {
            countSpan.textContent = selectedCount;
        }

        if (counter) {
            counter.style.display = selectedCount > 0 ? 'block' : 'none';
        }
    }

    // Public API
    window.MediaBulkImageSelector = {
        open: openModal,
        close: closeModal,
        isOpen: function() { return modalState.isOpen; },
        updateSelectionCounter: updateSelectionCounter,
        toggleSelection: toggleImageSelection,
        resetOrder: resetOrder
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();

