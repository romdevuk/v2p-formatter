/**
 * Observation Report - Media Browser Library
 * 
 * Standalone component for browsing and selecting media files
 * 
 * ⚠️ IMPORTANT: This is a NEW module - no legacy code from old modules.
 * The old observation-media module did not work properly and must be completely avoided.
 * 
 * Author: Frontend Developer (Agent-2)
 * Created: Stage 2
 */

class ObservationReportMediaBrowser {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.options = {
            apiBase: options.apiBase || '/v2p-formatter/observation-report',
            ...options
        };
        this.mediaList = [];
        this.assignments = {};
        this.selectedMedia = new Set();
        this.eventHandlers = {};
        this.container = null;
        this.isDragging = false;
        
        this.init();
    }
    
    /**
     * Initialize container and event listeners
     */
    init() {
        this.container = document.getElementById(this.containerId);
        if (!this.container) {
            console.error(`Media Browser: Container #${this.containerId} not found`);
            return;
        }
        
        // Set up container structure
        this.container.innerHTML = `
            <div class="media-browser-header">
                <h3>Media Browser</h3>
                <div class="media-count"></div>
            </div>
            <div class="media-grid"></div>
        `;
        
        // Store references
        this.gridContainer = this.container.querySelector('.media-grid');
        this.headerContainer = this.container.querySelector('.media-browser-header');
        this.countContainer = this.container.querySelector('.media-count');
    }
    
    /**
     * Load media files for qualification/learner
     */
    async loadMedia(qualification, learner) {
        if (!qualification || !learner) {
            console.warn('Media Browser: Qualification and learner required');
            return;
        }
        
        try {
            const url = `${this.options.apiBase}/media?qualification=${encodeURIComponent(qualification)}&learner=${encodeURIComponent(learner)}`;
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.success) {
                this.mediaList = data.media || [];
                this.render();
                this.emit('mediaLoaded', this.mediaList);
            } else {
                console.error('Media Browser: Error loading media', data.error);
                this.mediaList = [];
                this.render();
            }
        } catch (error) {
            console.error('Media Browser: Fetch error', error);
            this.mediaList = [];
            this.render();
        }
    }
    
    /**
     * Update assignment state for media items
     */
    updateAssignmentState(assignments) {
        this.assignments = assignments || {};
        this.refresh();
    }
    
    /**
     * Check if media is assigned to any placeholder
     */
    isMediaAssigned(mediaPath) {
        for (const placeholderName in this.assignments) {
            const mediaList = this.assignments[placeholderName];
            if (Array.isArray(mediaList)) {
                if (mediaList.some(item => item.path === mediaPath)) {
                    return true;
                }
            }
        }
        return false;
    }
    
    /**
     * Set media list programmatically
     */
    setMediaList(mediaList) {
        this.mediaList = mediaList || [];
        this.render();
    }
    
    /**
     * Refresh media display
     */
    refresh() {
        this.render();
    }
    
    /**
     * Render media grid (with collapsible subfolder grouping)
     */
    render() {
        if (!this.gridContainer) return;
        
        // Update count
        const assignedCount = this.mediaList.filter(m => this.isMediaAssigned(m.path)).length;
        this.countContainer.textContent = `${this.mediaList.length} files (${assignedCount} assigned)`;
        
        // Clear grid
        this.gridContainer.innerHTML = '';
        
        // Group media by subfolder
        const grouped = this.groupBySubfolder(this.mediaList);
        
        // Render grouped media with collapsible folders
        if (Object.keys(grouped).length > 1 || (Object.keys(grouped).length === 1 && Object.keys(grouped)[0] !== '')) {
            // Multiple folders or single non-root folder - show collapsible folder structure
            Object.keys(grouped).sort().forEach(subfolder => {
                const folderName = subfolder || 'Root';
                const mediaItems = grouped[subfolder];
                
                // Create folder container
                const folderContainer = document.createElement('div');
                folderContainer.className = 'media-folder-container';
                folderContainer.dataset.folderName = folderName;
                
                // Create folder header (clickable to toggle)
                const folderHeader = document.createElement('div');
                folderHeader.className = 'media-folder-header';
                const toggleIcon = document.createElement('span');
                toggleIcon.className = 'folder-toggle';
                toggleIcon.textContent = '▶'; // Collapsed by default
                
                const folderNameSpan = document.createElement('strong');
                folderNameSpan.innerHTML = `📁 ${folderName}`;
                
                const countSpan = document.createElement('span');
                countSpan.className = 'folder-count';
                countSpan.textContent = `(${mediaItems.length})`;
                
                folderHeader.appendChild(toggleIcon);
                folderHeader.appendChild(folderNameSpan);
                folderHeader.appendChild(countSpan);
                folderHeader.style.cursor = 'pointer';
                
                // Create folder content (collapsed by default)
                const folderContent = document.createElement('div');
                folderContent.className = 'media-folder-content'; // CSS sets display: none by default
                // Ensure collapsed state
                folderContent.style.display = 'none';
                folderContent.style.gridTemplateColumns = 'repeat(auto-fill, minmax(150px, 1fr))';
                folderContent.style.gap = '12px';
                folderContent.style.padding = '12px 15px';
                folderContent.style.background = 'var(--obs-bg-primary, #1e1e1e)';
                folderContent.style.borderLeft = '3px solid var(--obs-accent, #667eea)';
                folderContent.style.borderRight = '1px solid var(--obs-border, #555)';
                folderContent.style.borderBottom = '1px solid var(--obs-border, #555)';
                folderContent.style.borderRadius = '0 0 4px 4px';
                
                // Add media cards to folder content
                mediaItems.forEach(media => {
                    const card = this.createMediaCard(media);
                    folderContent.appendChild(card);
                });
                
                // Toggle on header click
                folderHeader.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Check current state - prioritize inline style over class
                    const currentDisplay = folderContent.style.display || getComputedStyle(folderContent).display;
                    const isExpanded = currentDisplay === 'grid' || currentDisplay === 'flex' || folderContent.classList.contains('expanded');
                    
                    console.log('Folder toggle clicked:', folderName, 'Current state:', isExpanded ? 'expanded' : 'collapsed');
                    
                    if (isExpanded) {
                        // Collapse
                        folderContent.style.display = 'none';
                        folderContent.classList.remove('expanded');
                        toggleIcon.textContent = '▶';
                        console.log('Folder collapsed:', folderName);
                    } else {
                        // Expand
                        folderContent.style.display = 'grid';
                        folderContent.classList.add('expanded');
                        toggleIcon.textContent = '▼';
                        console.log('Folder expanded:', folderName);
                    }
                });
                
                folderContainer.appendChild(folderHeader);
                folderContainer.appendChild(folderContent);
                this.gridContainer.appendChild(folderContainer);
            });
        } else {
            // Single root folder or no folders - flat list (no folder structure needed)
            this.mediaList.forEach(media => {
                const card = this.createMediaCard(media);
                this.gridContainer.appendChild(card);
            });
        }
    }
    
    /**
     * Group media files by subfolder
     */
    groupBySubfolder(mediaList) {
        const grouped = {};
        mediaList.forEach(media => {
            const folder = media.subfolder || '';
            if (!grouped[folder]) {
                grouped[folder] = [];
            }
            grouped[folder].push(media);
        });
        return grouped;
    }
    
    /**
     * Create media card element
     */
    createMediaCard(media) {
        const isAssigned = this.isMediaAssigned(media.path);
        const isSelected = this.selectedMedia.has(media.path);
        
        const card = document.createElement('div');
        card.className = 'media-card';
        card.dataset.mediaPath = media.path;
        card.draggable = !isAssigned; // Only allow dragging unassigned media
        
        if (isAssigned) {
            card.classList.add('assigned');
        }
        if (isSelected) {
            card.classList.add('selected');
        }
        
        // Media thumbnail/preview
        const thumbnail = this.createThumbnail(media);
        
        // Media info
        const info = document.createElement('div');
        info.className = 'media-info';
        
        // Filename (editable)
        const filename = document.createElement('div');
        filename.className = 'media-filename';
        filename.contentEditable = true;
        filename.textContent = media.name;
        filename.addEventListener('blur', (e) => {
            const newName = e.target.textContent.trim();
            if (newName && newName !== media.name) {
                this.handleFilenameUpdate(media, newName);
            } else {
                e.target.textContent = media.name;
            }
        });
        
        // File type indicator
        const typeIndicator = document.createElement('div');
        typeIndicator.className = 'media-type';
        typeIndicator.textContent = this.getTypeIcon(media.type);
        
        info.appendChild(filename);
        info.appendChild(typeIndicator);
        
        // Selection checkbox
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = isSelected;
        checkbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                this.selectedMedia.add(media.path);
                card.classList.add('selected');
                this.emit('mediaSelect', media);
            } else {
                this.selectedMedia.delete(media.path);
                card.classList.remove('selected');
                this.emit('mediaDeselect', media);
            }
        });
        
        card.appendChild(checkbox);
        card.appendChild(thumbnail);
        card.appendChild(info);
        
        // ⚠️ CRITICAL: Drag-and-drop setup
        this.setupDragAndDrop(card, media);
        
        return card;
    }
    
    /**
     * Create thumbnail/preview element
     */
    createThumbnail(media) {
        const thumbnail = document.createElement('div');
        thumbnail.className = 'media-thumbnail';
        
        if (media.type === 'image' && media.thumbnail_path) {
            const img = document.createElement('img');
            // Use relative_path for thumbnail if available
            const thumbPath = media.thumbnail_relative_path || media.thumbnail_path;
            const pathSegments = thumbPath.split('/').filter(seg => seg).map(seg => encodeURIComponent(seg));
            const encodedThumbPath = pathSegments.join('/');
            img.src = `/v2p-formatter/observation-report/media/${encodedThumbPath}`;
            img.alt = media.name;
            img.onerror = () => {
                thumbnail.textContent = '🖼️';
            };
            thumbnail.appendChild(img);
        } else {
            thumbnail.textContent = this.getTypeIcon(media.type);
        }
        
        return thumbnail;
    }
    
    /**
     * Get icon for media type
     */
    getTypeIcon(type) {
        const icons = {
            'image': '🖼️',
            'video': '🎬',
            'pdf': '📄',
            'audio': '🎵'
        };
        return icons[type] || '📎';
    }
    
    /**
     * ⚠️ CRITICAL: Setup drag-and-drop for media card
     * This was a major complexity in the old module - pay EXTRA attention
     */
    setupDragAndDrop(card, media) {
        if (!card.draggable) return; // Skip if already assigned
        
        card.addEventListener('dragstart', (e) => {
            this.handleDragStart(media, e);
        });
        
        card.addEventListener('dragend', (e) => {
            this.handleDragEnd(e);
        });
    }
    
    /**
     * ⚠️ CRITICAL: Handle drag start for media items
     * This was a major complexity in the old module - pay EXTRA attention
     */
    handleDragStart(media, event) {
        this.isDragging = true;
        
        // Determine what to drag (single or multiple selected)
        let mediaToDrag = [media];
        if (this.selectedMedia.has(media.path) && this.selectedMedia.size > 1) {
            // Bulk drag: drag all selected items
            mediaToDrag = this.mediaList.filter(m => this.selectedMedia.has(m.path));
        }
        
        // Set drag data
        const dragData = {
            media: mediaToDrag,
            type: mediaToDrag.length > 1 ? 'bulk' : 'single'
        };
        
        event.dataTransfer.setData('application/json', JSON.stringify(dragData));
        event.dataTransfer.effectAllowed = 'copy';
        
        // Add visual feedback
        event.target.classList.add('dragging');
        
        // Create custom drag image (optional)
        const dragImage = event.target.cloneNode(true);
        dragImage.style.opacity = '0.5';
        document.body.appendChild(dragImage);
        event.dataTransfer.setDragImage(dragImage, 0, 0);
        setTimeout(() => document.body.removeChild(dragImage), 0);
        
        // Emit event
        this.emit('mediaDragStart', {
            media: mediaToDrag,
            type: dragData.type
        });
    }
    
    /**
     * Handle drag end
     */
    handleDragEnd(event) {
        this.isDragging = false;
        event.target.classList.remove('dragging');
        this.emit('mediaDragEnd');
    }
    
    /**
     * Handle filename update
     */
    async handleFilenameUpdate(media, newName) {
        try {
            const response = await fetch(`${this.options.apiBase}/rename-file`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    old_path: media.path,
                    new_name: newName
                })
            });
            
            const data = await response.json();
            if (data.success) {
                // Update local media object
                media.path = data.new_path;
                media.name = data.new_name;
                this.emit('filenameUpdate', {
                    oldPath: media.path,
                    newPath: data.new_path,
                    newName: data.new_name
                });
                this.refresh();
            } else {
                console.error('Media Browser: Error renaming file', data.error);
                alert('Error renaming file: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Media Browser: Error renaming file', error);
            alert('Error renaming file');
        }
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
                console.error(`Media Browser: Error in event handler for ${event}`, error);
            }
        });
    }
}

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ObservationReportMediaBrowser;
}

