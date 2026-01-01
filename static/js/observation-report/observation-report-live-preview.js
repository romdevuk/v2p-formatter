/**
 * Observation Report - Live Preview Library
 * 
 * Standalone component for real-time document preview rendering
 * 
 * ⚠️ IMPORTANT: This is a NEW module - no legacy code from old modules.
 * The old observation-media module did not work properly and must be completely avoided.
 * 
 * Author: Frontend Developer (Agent-2)
 * Created: Stage 2
 */

class ObservationReportLivePreview {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.options = {
            placeholderColors: options.placeholderColors || [
                '#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24',
                '#6c5ce7', '#a29bfe', '#fd79a8', '#00b894'
            ],
            ...options
        };
        this.textContent = '';
        this.assignments = {};
        this.sections = [];
        this.eventHandlers = {};
        this.placeholderPattern = /\{\{([A-Za-z0-9_]+)\}\}/g;
        this.placeholderColors = {};
        this.sectionColors = {};  // Store section colors
        this.container = null;
        this.currentDragTarget = null;
        
        this.init();
    }
    
    /**
     * Initialize container
     */
    init() {
        this.container = document.getElementById(this.containerId);
        if (!this.container) {
            console.error(`Live Preview: Container #${this.containerId} not found`);
            return;
        }
        
        // Set up container
        this.container.className = 'live-preview-container';
    }
    
    /**
     * Update preview content
     */
    updateContent(text, assignments, sections) {
        this.textContent = text || '';
        this.assignments = assignments || {};
        this.sections = sections || [];
        
        // Extract placeholders and assign colors
        this.assignPlaceholderColors();
        
        // Extract sections and assign colors
        this.assignSectionColors();
        
        // Render preview
        this.render();
    }
    
    /**
     * Extract placeholders from text
     */
    extractPlaceholders(text) {
        const placeholders = [];
        const seen = new Set();
        let match;
        
        // Reset regex
        this.placeholderPattern.lastIndex = 0;
        
        while ((match = this.placeholderPattern.exec(text)) !== null) {
            const name = match[1].toLowerCase();
            if (!seen.has(name)) {
                seen.add(name);
                placeholders.push(name);
            }
        }
        
        return placeholders;
    }
    
    /**
     * Assign colors to placeholders
     */
    assignPlaceholderColors() {
        const placeholders = this.extractPlaceholders(this.textContent);
        placeholders.forEach((placeholder, index) => {
            const colorIndex = index % this.options.placeholderColors.length;
            this.placeholderColors[placeholder] = this.options.placeholderColors[colorIndex];
        });
    }
    
    /**
     * Extract sections from text
     */
    extractSections(text) {
        const sections = [];
        const sectionPattern = /^SECTION\s+([^\n:]+)[:\-]?\s*\n/gi;
        const seen = new Set();
        let match;
        
        // Reset regex
        sectionPattern.lastIndex = 0;
        
        while ((match = sectionPattern.exec(text)) !== null) {
            const title = match[1].trim().toLowerCase();
            if (!seen.has(title)) {
                seen.add(title);
                sections.push(title);
            }
        }
        
        return sections;
    }
    
    /**
     * Assign colors to sections
     */
    assignSectionColors() {
        const sections = this.extractSections(this.textContent);
        sections.forEach((sectionTitle, index) => {
            // Use same color palette but offset to differentiate from placeholders
            const colorIndex = index % this.options.placeholderColors.length;
            this.sectionColors[sectionTitle] = this.options.placeholderColors[colorIndex];
        });
    }
    
    /**
     * Get color for section
     */
    getSectionColor(sectionTitle) {
        const normalized = sectionTitle.toLowerCase().trim();
        return this.sectionColors[normalized] || '#999';
    }
    
    /**
     * Get color for placeholder
     */
    getPlaceholderColor(placeholderName) {
        return this.placeholderColors[placeholderName.toLowerCase()] || '#999';
    }
    
    /**
     * Render preview
     */
    render() {
        if (!this.container) return;
        
        // Split content into parts (text and placeholders)
        const parts = this.splitContent(this.textContent);
        
        // Build HTML
        let html = '<div class="preview-content">';
        
        parts.forEach(part => {
            if (part.type === 'placeholder') {
                html += this.renderPlaceholder(part.name, part.fullMatch);
            } else if (part.type === 'section') {
                html += this.renderSection(part.title, part.content);
            } else {
                // Preserve newlines in text content
                const text = part.text;
                const escapedText = this.escapeHtml(text);
                html += `<span class="preview-text">${escapedText.replace(/\n/g, '<br>')}</span>`;
            }
        });
        
        html += '</div>';
        
        this.container.innerHTML = html;
        
        // Set up drop zones and event listeners
        this.setupDropZones();
    }
    
    /**
     * Split content into parts (text, placeholders, sections)
     */
    splitContent(text) {
        const parts = [];
        let lastIndex = 0;
        let match;
        
        // Reset regex
        this.placeholderPattern.lastIndex = 0;
        
        // Check for section markers (SECTION ... - or SECTION ... :)
        const sectionPattern = /^SECTION\s+([^\n:]+)[:\-]?\s*\n/gi;
        const sectionMatches = [];
        let sectionMatch;
        
        // Find all section markers
        while ((sectionMatch = sectionPattern.exec(text)) !== null) {
            sectionMatches.push({
                index: sectionMatch.index,
                title: sectionMatch[1].trim(),
                fullMatch: sectionMatch[0]
            });
        }
        
        // Find all placeholder matches
        const placeholderMatches = [];
        this.placeholderPattern.lastIndex = 0;
        while ((match = this.placeholderPattern.exec(text)) !== null) {
            placeholderMatches.push({
                index: match.index,
                name: match[1].toLowerCase(),
                fullMatch: match[0]
            });
        }
        
        // Combine and sort all matches
        const allMatches = [
            ...sectionMatches.map(m => ({ ...m, type: 'section' })),
            ...placeholderMatches.map(m => ({ ...m, type: 'placeholder' }))
        ].sort((a, b) => a.index - b.index);
        
        // Build parts array
        allMatches.forEach((match, idx) => {
            // Add text before match
            if (match.index > lastIndex) {
                parts.push({
                    type: 'text',
                    text: text.substring(lastIndex, match.index)
                });
            }
            
            // Add match
            if (match.type === 'section') {
                // Find content until next section or end
                const nextMatch = allMatches.find((m, i) => i > idx && m.type === 'section');
                const contentEnd = nextMatch ? nextMatch.index : text.length;
                const content = text.substring(match.index + match.fullMatch.length, contentEnd);
                parts.push({
                    type: 'section',
                    title: match.title,
                    content: content,
                    fullMatch: match.fullMatch
                });
                lastIndex = contentEnd;
            } else {
                parts.push({
                    type: 'placeholder',
                    name: match.name,
                    fullMatch: match.fullMatch
                });
                lastIndex = match.index + match.fullMatch.length;
            }
        });
        
        // Add remaining text
        if (lastIndex < text.length) {
            parts.push({
                type: 'text',
                text: text.substring(lastIndex)
            });
        }
        
        return parts;
    }
    
    /**
     * Render placeholder with table
     */
    renderPlaceholder(placeholderName, fullMatch) {
        const color = this.getPlaceholderColor(placeholderName);
        const mediaList = this.assignments[placeholderName] || [];
        
        let html = `<div class="placeholder-container" data-placeholder="${placeholderName}">`;
        html += `<span class="placeholder-label" style="color: ${color};">${fullMatch}</span>`;
        
        if (mediaList.length === 0) {
            // Empty placeholder - show drop zone
            html += this.renderEmptyPlaceholderTable(placeholderName);
        } else {
            // Render table with media
            html += this.renderPlaceholderTable(placeholderName, mediaList);
        }
        
        html += '</div>';
        return html;
    }
    
    /**
     * Render empty placeholder table (drop zone)
     */
    renderEmptyPlaceholderTable(placeholderName) {
        const color = this.getPlaceholderColor(placeholderName);
        return `
            <table class="placeholder-table empty" data-placeholder="${placeholderName}">
                <tr>
                    <td class="drop-zone" data-placeholder="${placeholderName}" data-position="0" 
                        style="border: 2px dashed ${color};">
                        Drop media here
                    </td>
                    <td class="drop-zone" data-placeholder="${placeholderName}" data-position="1"
                        style="border: 2px dashed ${color};">
                        Drop media here
                    </td>
                </tr>
            </table>
        `;
    }
    
    /**
     * Render placeholder table with media items
     */
    renderPlaceholderTable(placeholderName, mediaList) {
        // Sort by order
        const sortedMedia = [...mediaList].sort((a, b) => (a.order || 0) - (b.order || 0));
        
        // Always ensure at least one empty drop zone is available
        // Calculate rows needed: current items + 1 extra row for drop zone
        const numRows = Math.max(1, Math.ceil(sortedMedia.length / 2) + 1);
        
        let html = `<table class="placeholder-table" data-placeholder="${placeholderName}">`;
        
        for (let row = 0; row < numRows; row++) {
            html += '<tr>';
            for (let col = 0; col < 2; col++) {
                const position = this.calculatePosition(row, col);
                const media = sortedMedia[position];
                
                html += '<td class="media-cell" ';
                html += `data-placeholder="${placeholderName}" `;
                html += `data-position="${position}" `;
                html += `data-row="${row}" data-col="${col}">`;
                
                if (media) {
                    html += this.renderMediaItem(placeholderName, media, position);
                } else {
                    // Empty cell - show drop zone
                    const color = this.getPlaceholderColor(placeholderName);
                    html += `<div class="drop-zone" data-placeholder="${placeholderName}" data-position="${position}" 
                        style="border: 2px dashed ${color}; min-height: 80px; display: flex; align-items: center; justify-content: center; cursor: pointer;">
                        Drop media here
                    </div>`;
                }
                
                html += '</td>';
            }
            html += '</tr>';
        }
        
        html += '</table>';
        return html;
    }
    
    /**
     * Render media item in table cell
     */
    renderMediaItem(placeholderName, media, position) {
        let html = '<div class="media-item" draggable="true" ';
        html += `data-placeholder="${placeholderName}" `;
        html += `data-position="${position}" `;
        html += `data-media-path="${this.escapeHtml(media.path)}">`;
        
        // Remove button
        html += `<button class="remove-media" data-placeholder="${placeholderName}" data-position="${position}">×</button>`;
        
        // Reorder buttons
        const mediaList = this.assignments[placeholderName] || [];
        if (mediaList.length > 1) {
            if (position > 0) {
                html += `<button class="reorder-up" data-placeholder="${placeholderName}" data-position="${position}">↑</button>`;
            }
            if (position < mediaList.length - 1) {
                html += `<button class="reorder-down" data-placeholder="${placeholderName}" data-position="${position}">↓</button>`;
            }
        }
        
        // Media content
        if (media.type === 'image') {
            // Prefer relative_path (from OUTPUT_FOLDER) for serving
            // Fall back to path if relative_path not available
            let imagePath = media.relative_path || '';
            
            // If no relative_path, check if path is absolute and extract relative part
            if (!imagePath && media.path) {
                const fullPath = media.path;
                // Check if it's an absolute path within OUTPUT_FOLDER
                // Try multiple possible OUTPUT_FOLDER markers
                const possibleMarkers = [
                    '/v2p-formatter-output/',
                    'v2p-formatter-output/',
                    '/output/',
                    'output/'
                ];
                
                let foundMarker = null;
                for (const marker of possibleMarkers) {
                    const markerIndex = fullPath.indexOf(marker);
                    if (markerIndex !== -1) {
                        foundMarker = marker;
                        // Extract relative path after OUTPUT_FOLDER
                        imagePath = fullPath.substring(markerIndex + marker.length);
                        break;
                    }
                }
                
                // If still no path found, try to extract qualification/learner pattern
                // Pattern: .../{qualification}/{learner}/...
                if (!imagePath && media.qualification && media.learner) {
                    const qualIndex = fullPath.indexOf(`/${media.qualification}/${media.learner}/`);
                    if (qualIndex !== -1) {
                        // Extract from qualification onwards
                        imagePath = fullPath.substring(qualIndex + 1); // +1 to skip leading /
                    }
                }
                
                // Last resort: use full path (backend endpoint handles absolute paths)
                if (!imagePath) {
                    imagePath = fullPath;
                }
            }
            
            if (!imagePath) {
                // No path available
                html += `<div class="media-error">⚠️ Image path not available: ${this.escapeHtml(media.name)}</div>`;
            } else {
                // Ensure path is properly encoded (encode each segment separately for path handling)
                const pathSegments = imagePath.split('/').filter(seg => seg).map(seg => encodeURIComponent(seg));
                const encodedPath = pathSegments.join('/');
                
                html += `<img src="/v2p-formatter/observation-report/media/${encodedPath}" alt="${this.escapeHtml(media.name)}" class="media-preview-image" onerror="this.style.display='none'; this.nextElementSibling.style.display='block'; console.error('Image load error:', this.src);" />`;
                html += `<div class="media-error" style="display:none;">⚠️ Image not found: ${this.escapeHtml(media.name)}</div>`;
            }
        } else {
            html += `<div class="media-filename">${this.escapeHtml(media.name)}</div>`;
            html += `<div class="media-type">${this.getTypeIcon(media.type)}</div>`;
        }
        
        html += '</div>';
        return html;
    }
    
    /**
     * Get icon for media type
     */
    getTypeIcon(type) {
        const icons = { 'image': '🖼️', 'video': '🎬', 'pdf': '📄', 'audio': '🎵' };
        return icons[type] || '📎';
    }
    
    /**
     * Render section
     */
    renderSection(title, content) {
        const sectionId = `section-${title.toLowerCase().replace(/\s+/g, '-')}`;
        const section = this.sections.find(s => s.id === sectionId);
        // Default to collapsed (false) per spec: "All sections collapsed by default"
        const isExpanded = section ? section.isExpanded === true : false;
        const color = this.getSectionColor(title);
        
        let html = `<div class="preview-section" data-section-id="${sectionId}">`;
        html += `<div class="section-header" data-section-id="${sectionId}" style="cursor: pointer;">`;
        html += `<span class="section-toggle">${isExpanded ? '▼' : '▶'}</span>`;
        html += `<h3 class="section-title" style="color: ${color};">SECTION ${title}</h3>`;
        html += '</div>';
        
        if (isExpanded) {
            html += `<div class="section-content" data-section-id="${sectionId}" style="display: block;">`;
            // Process content recursively for nested placeholders
            html += this.processSectionContent(content);
            html += '</div>';
        } else {
            html += `<div class="section-content" data-section-id="${sectionId}" style="display: none;"></div>`;
        }
        
        html += '</div>';
        return html;
    }
    
    /**
     * Process section content (handle placeholders within sections)
     */
    processSectionContent(content) {
        // Split by placeholders
        const parts = [];
        let lastIndex = 0;
        let match;
        
        this.placeholderPattern.lastIndex = 0;
        while ((match = this.placeholderPattern.exec(content)) !== null) {
            if (match.index > lastIndex) {
                parts.push({
                    type: 'text',
                    text: content.substring(lastIndex, match.index)
                });
            }
            parts.push({
                type: 'placeholder',
                name: match[1].toLowerCase(),
                fullMatch: match[0]
            });
            lastIndex = match.index + match[0].length;
        }
        
        if (lastIndex < content.length) {
            parts.push({
                type: 'text',
                text: content.substring(lastIndex)
            });
        }
        
        // Render parts
        return parts.map(part => {
            if (part.type === 'placeholder') {
                return this.renderPlaceholder(part.name, part.fullMatch);
            }
            return this.escapeHtml(part.text);
        }).join('');
    }
    
    /**
     * Setup drop zones and event listeners
     */
    setupDropZones() {
        if (!this.container) return;
        
        // Setup drop zones for empty placeholders and empty cells
        const dropZones = this.container.querySelectorAll('.drop-zone');
        dropZones.forEach(zone => {
            zone.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.handleDragOver(e.target, e);
            });
            
            zone.addEventListener('drop', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.handleDrop(e.target, e);
            });
            
            zone.addEventListener('dragleave', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.handleDragLeave(e.target, e);
            });
        });
        
        // Setup media item drag for reordering
        const mediaItems = this.container.querySelectorAll('.media-item');
        mediaItems.forEach(item => {
            item.addEventListener('dragstart', (e) => {
                this.handleReorderDragStart(item, e);
            });
            
            item.addEventListener('dragend', (e) => {
                this.handleReorderDragEnd(item, e);
            });
        });
        
        // Setup remove buttons
        const removeButtons = this.container.querySelectorAll('.remove-media');
        removeButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const placeholder = btn.dataset.placeholder;
                const position = parseInt(btn.dataset.position);
                this.removeMedia(placeholder, position);
            });
        });
        
        // Setup reorder buttons
        const reorderButtons = this.container.querySelectorAll('.reorder-up, .reorder-down');
        reorderButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const placeholder = btn.dataset.placeholder;
                const position = parseInt(btn.dataset.position);
                const direction = btn.classList.contains('reorder-up') ? 'up' : 'down';
                this.reorderMediaWithButton(placeholder, position, direction);
            });
        });
        
        // Setup section toggles
        const sectionHeaders = this.container.querySelectorAll('.section-header');
        sectionHeaders.forEach(header => {
            header.addEventListener('click', (e) => {
                const sectionId = header.dataset.sectionId;
                this.toggleSection(sectionId);
            });
        });
    }
    
    /**
     * ⚠️ CRITICAL: Handle drag over for drop zones
     */
    handleDragOver(target, event) {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'copy';
        
        // Highlight drop zone
        target.classList.add('drag-over');
        this.currentDragTarget = target;
    }
    
    /**
     * Handle drag leave
     */
    handleDragLeave(target, event) {
        target.classList.remove('drag-over');
        if (this.currentDragTarget === target) {
            this.currentDragTarget = null;
        }
    }
    
    /**
     * ⚠️ CRITICAL: Handle drop events for media assignment
     */
    handleDrop(target, event) {
        event.preventDefault();
        
        // Remove highlight
        target.classList.remove('drag-over');
        this.currentDragTarget = null;
        
        // Get drag data
        let dragData;
        try {
            const dataStr = event.dataTransfer.getData('application/json');
            if (!dataStr) {
                console.warn('Live Preview: No drag data found');
                return;
            }
            dragData = JSON.parse(dataStr);
        } catch (error) {
            console.error('Live Preview: Error parsing drag data', error);
            return;
        }
        
        const mediaItems = dragData.media || [];
        if (mediaItems.length === 0) {
            console.warn('Live Preview: No media in drag data');
            return;
        }
        
        // Get drop target info
        const placeholderName = target.dataset.placeholder;
        const position = parseInt(target.dataset.position) || 0;
        
        if (!placeholderName) {
            console.warn('Live Preview: Invalid drop target - no placeholder');
            return;
        }
        
        // Check if multiple placeholders exist
        const placeholders = this.extractPlaceholders(this.textContent);
        if (placeholders.length > 1 && mediaItems.length > 1) {
            // Show dialog for placeholder selection
            this.showPlaceholderSelectionDialog(mediaItems, (selectedPlaceholder) => {
                this.assignMediaToPlaceholder(selectedPlaceholder, mediaItems);
            });
        } else {
            // Direct assignment
            this.assignMediaToPlaceholder(placeholderName, mediaItems, position);
        }
    }
    
    /**
     * Assign media to placeholder
     */
    assignMediaToPlaceholder(placeholderName, mediaItems, startPosition = null) {
        if (!this.assignments[placeholderName]) {
            this.assignments[placeholderName] = [];
        }
        
        const existingMedia = this.assignments[placeholderName];
        let nextPosition = startPosition !== null ? startPosition : existingMedia.length;
        
        mediaItems.forEach((media, idx) => {
            // Find next available position
            while (existingMedia.some(m => m.order === nextPosition)) {
                nextPosition++;
            }
            
            existingMedia.push({
                path: media.path,
                type: media.type,
                name: media.name,
                order: nextPosition
            });
            nextPosition++;
        });
        
        // Sort by order
        existingMedia.sort((a, b) => (a.order || 0) - (b.order || 0));
        
        // Re-render and emit event
        this.render();
        this.emit('mediaAssignment', {
            placeholder: placeholderName,
            media: mediaItems,
            assignments: this.assignments
        });
    }
    
    /**
     * Show placeholder selection dialog (for multiple placeholders)
     */
    showPlaceholderSelectionDialog(mediaItems, callback) {
        const placeholders = this.extractPlaceholders(this.textContent);
        
        // Simple prompt for now (can be enhanced with modal dialog)
        const options = placeholders.map(p => `${p} (${this.getPlaceholderColor(p)})`).join('\n');
        const selection = prompt(`Select placeholder for ${mediaItems.length} media item(s):\n\n${placeholders.join('\n')}`);
        
        if (selection && placeholders.includes(selection.toLowerCase())) {
            callback(selection.toLowerCase());
        }
    }
    
    /**
     * Remove media from placeholder
     */
    removeMedia(placeholderName, position) {
        if (!this.assignments[placeholderName]) return;
        
        this.assignments[placeholderName] = this.assignments[placeholderName].filter(
            (item, idx) => item.order !== position
        );
        
        // Renumber remaining items
        this.assignments[placeholderName].forEach((item, idx) => {
            item.order = idx;
        });
        
        this.render();
        this.emit('mediaRemove', {
            placeholder: placeholderName,
            position: position
        });
    }
    
    /**
     * Handle reorder drag start (within table)
     */
    handleReorderDragStart(item, event) {
        event.dataTransfer.effectAllowed = 'move';
        item.classList.add('dragging');
    }
    
    /**
     * Handle reorder drag end
     */
    handleReorderDragEnd(item, event) {
        item.classList.remove('dragging');
    }
    
    /**
     * Reorder media with button (up/down)
     */
    reorderMediaWithButton(placeholderName, position, direction) {
        const mediaList = this.assignments[placeholderName];
        if (!mediaList || mediaList.length < 2) return;
        
        const currentIndex = mediaList.findIndex(m => m.order === position);
        if (currentIndex === -1) return;
        
        const newIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;
        if (newIndex < 0 || newIndex >= mediaList.length) return;
        
        // Swap orders
        const tempOrder = mediaList[currentIndex].order;
        mediaList[currentIndex].order = mediaList[newIndex].order;
        mediaList[newIndex].order = tempOrder;
        
        // Sort and re-render
        mediaList.sort((a, b) => (a.order || 0) - (b.order || 0));
        this.render();
        
        this.emit('mediaReorder', {
            placeholder: placeholderName,
            oldPosition: position,
            newPosition: mediaList[newIndex].order
        });
    }
    
    /**
     * ⚠️ CRITICAL: Reorder media within placeholder (for drag-and-drop)
     */
    reorderMedia(placeholderName, oldPosition, newPosition) {
        const mediaList = this.assignments[placeholderName];
        if (!mediaList) return;
        
        const oldIndex = mediaList.findIndex(m => m.order === oldPosition);
        if (oldIndex === -1) return;
        
        // Remove from old position
        const [movedItem] = mediaList.splice(oldIndex, 1);
        
        // Insert at new position
        const newIndex = mediaList.findIndex(m => m.order === newPosition);
        if (newIndex === -1) {
            movedItem.order = newPosition;
            mediaList.push(movedItem);
        } else {
            mediaList.splice(newIndex, 0, movedItem);
        }
        
        // Renumber all items
        mediaList.forEach((item, idx) => {
            item.order = idx;
        });
        
        // Sort and re-render
        mediaList.sort((a, b) => (a.order || 0) - (b.order || 0));
        this.render();
        
        this.emit('mediaReorder', {
            placeholder: placeholderName,
            oldPosition: oldPosition,
            newPosition: newPosition
        });
    }
    
    /**
     * Calculate position index from row/col (for 2-column table)
     */
    calculatePosition(row, col) {
        return row * 2 + col;
    }
    
    /**
     * Calculate row/col from position index (for 2-column table)
     */
    calculateRowCol(position) {
        return {
            row: Math.floor(position / 2),
            col: position % 2
        };
    }
    
    /**
     * Toggle section expand/collapse
     */
    toggleSection(sectionId) {
        // Find or create section
        let section = this.sections.find(s => s.id === sectionId);
        if (!section) {
            // Create new section entry (default to collapsed)
            section = { id: sectionId, isExpanded: false };
            this.sections.push(section);
        }
        
        // Toggle state
        section.isExpanded = !section.isExpanded;
        
        // Update UI directly without full re-render
        const sectionElement = this.container.querySelector(`.preview-section[data-section-id="${sectionId}"]`);
        if (sectionElement) {
            const content = sectionElement.querySelector('.section-content');
            const toggle = sectionElement.querySelector('.section-toggle');
            
            if (content && toggle) {
                if (section.isExpanded) {
                    content.style.display = 'block';
                    toggle.textContent = '▼';
                    
                    // Process content if it's empty (first expansion)
                    if (!content.innerHTML.trim()) {
                        // Find section in text and process content
                        const sectionTitleElement = sectionElement.querySelector('.section-title');
                        const sectionTitle = sectionTitleElement?.textContent?.replace('SECTION ', '').trim();
                        if (sectionTitle && this.textContent) {
                            const sectionPattern = new RegExp(`SECTION\\s+${sectionTitle.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[:\-]?\\s*\\n([\\s\\S]*?)(?=SECTION|$)`, 'i');
                            const match = this.textContent.match(sectionPattern);
                            if (match && match[1]) {
                                content.innerHTML = this.processSectionContent(match[1]);
                                this.setupDropZones(); // Re-setup drop zones after content added
                            }
                        }
                    }
                } else {
                    content.style.display = 'none';
                    toggle.textContent = '▶';
                }
            }
        } else {
            // Fallback: re-render if element not found
            this.render();
        }
        
        this.emit('sectionToggle', { sectionId, isExpanded: section.isExpanded });
    }
    
    /**
     * Update section states
     */
    updateSectionStates(sections) {
        this.sections = sections || [];
        this.render();
    }
    
    /**
     * Expand specific section
     */
    expandSection(sectionId) {
        const section = this.sections.find(s => s.id === sectionId);
        if (section) {
            section.isExpanded = true;
            this.render();
            this.scrollToSection(sectionId);
        }
    }
    
    /**
     * Collapse specific section
     */
    collapseSection(sectionId) {
        const section = this.sections.find(s => s.id === sectionId);
        if (section) {
            section.isExpanded = false;
            this.render();
        }
    }
    
    /**
     * Scroll to section
     */
    scrollToSection(sectionId) {
        if (!this.container) return;
        const sectionElement = this.container.querySelector(`[data-section-id="${sectionId}"]`);
        if (sectionElement) {
            sectionElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
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
                console.error(`Live Preview: Error in event handler for ${event}`, error);
            }
        });
    }
}

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ObservationReportLivePreview;
}
