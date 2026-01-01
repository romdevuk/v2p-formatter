/**
 * Media Browser Library - Standalone
 * Provides displayObservationMedia and loadObservationMedia functions immediately
 */

(function() {
    'use strict';
    
    // Helper functions
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }
    
    function getCurrentAssignments() {
        return window.observationMediaAssignments || {};
    }
    
    function isMediaAssigned(mediaPath) {
        const assignments = getCurrentAssignments();
        for (const placeholder in assignments) {
            if (assignments[placeholder].some(m => m.path === mediaPath)) {
                return true;
            }
        }
        return false;
    }
    
    function getSectionColorForMedia(mediaPath, assignments, text) {
        // Find which placeholder this media is assigned to
        for (const placeholder in assignments) {
            if (assignments[placeholder].some(m => m.path === mediaPath)) {
                // Try to get section color from text
                if (text && typeof window.parseSections === 'function') {
                    try {
                        const sectionData = window.parseSections(text);
                        if (sectionData.hasSections) {
                            for (const section of sectionData.sections) {
                                const sectionPlaceholders = window.extractPlaceholders ? window.extractPlaceholders(section.content) : [];
                                if (sectionPlaceholders.includes(placeholder)) {
                                    return section.color;
                                }
                            }
                        }
                    } catch (e) {
                        console.error('Error getting section color:', e);
                    }
                }
            }
        }
        return null;
    }
    
    function displayObservationMedia(mediaFiles) {
        // IMPORTANT: Filter by draft's qualification/learner path FIRST
        // This ensures we only show media from the draft's learner path
        let filteredMediaFiles = mediaFiles;
        
        if (window.currentDraft && window.currentDraft.id && window.currentDraft.qualification && window.currentDraft.learner) {
            const draftQualification = window.currentDraft.qualification;
            const draftLearner = window.currentDraft.learner;
            const expectedPath = `${draftQualification}/${draftLearner}`;
            
            filteredMediaFiles = mediaFiles.filter(media => {
                const mediaPath = media.path || '';
                // Check if media path contains the draft's qualification/learner path
                return mediaPath.includes(`/${expectedPath}/`) || mediaPath.includes(`\\${expectedPath}\\`);
            });
            
            console.log('Media Browser: displayObservationMedia - Filtered from', mediaFiles.length, 'to', filteredMediaFiles.length, 'files for draft path:', expectedPath);
        }
        
        // Then filter by draft subfolder if draft is loaded
        if (window.currentDraft && window.currentDraft.id && window.currentDraft.selected_subfolder) {
            const draftSubfolder = window.currentDraft.selected_subfolder;
            const beforeSubfolderFilter = filteredMediaFiles.length;
            filteredMediaFiles = filteredMediaFiles.filter(media => {
                const mediaSubfolder = media.subfolder || '';
                return mediaSubfolder === draftSubfolder;
            });
            console.log('Media Browser: displayObservationMedia - Filtered from', beforeSubfolderFilter, 'to', filteredMediaFiles.length, 'files for draft subfolder:', draftSubfolder);
        }
        
        const bulkSelectLabel = document.getElementById('bulkSelectLabel');
        if (bulkSelectLabel) {
            bulkSelectLabel.style.display = filteredMediaFiles.length > 0 ? 'block' : 'none';
        }
        
        const grid = document.getElementById('observationMediaGrid');
        if (!grid) {
            console.error('observationMediaGrid element not found');
            return;
        }
        
        grid.innerHTML = '';
        
        if (filteredMediaFiles.length === 0) {
            grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No media files found</p>';
            return;
        }
        
        // Group by subfolder
        const groupedMedia = {};
        filteredMediaFiles.forEach(media => {
            const subfolder = media.subfolder || '';
            if (!groupedMedia[subfolder]) {
                groupedMedia[subfolder] = [];
            }
            groupedMedia[subfolder].push(media);
        });
        
        const subfolderKeys = Object.keys(groupedMedia).sort();
        const hasSubfolders = subfolderKeys.some(key => key && key.trim() !== '');
        const hasRootFiles = groupedMedia[''] && groupedMedia[''].length > 0;
        
        const assignments = getCurrentAssignments();
        const textEditor = document.getElementById('observationTextEditor');
        const text = textEditor ? textEditor.value : '';
        
        // Display root files first (only if draft doesn't restrict to a subfolder)
        if (hasRootFiles && (!window.currentDraft || !window.currentDraft.id || !window.currentDraft.selected_subfolder)) {
            const rootContainer = document.createElement('div');
            rootContainer.className = 'media-root-files-container';
            rootContainer.style.cssText = 'display: grid; gap: 15px; padding: 10px 0; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));';
            
            groupedMedia[''].forEach((media, index) => {
                const card = createMediaCard(media, index, assignments, text);
                rootContainer.appendChild(card);
            });
            
            grid.appendChild(rootContainer);
        }
        
        // Display subfolders (filtered by draft if applicable)
        if (hasSubfolders) {
            subfolderKeys.forEach(subfolder => {
                if (!subfolder || subfolder.trim() === '') return;
                
                // If draft has subfolder, only show that subfolder
                if (window.currentDraft && window.currentDraft.id && window.currentDraft.selected_subfolder) {
                    if (subfolder !== window.currentDraft.selected_subfolder) {
                        return; // Skip this subfolder
                    }
                }
                
                const mediaCount = groupedMedia[subfolder].length;
                const section = document.createElement('div');
                section.className = 'media-subfolder-section collapsed';
                section.dataset.subfolder = subfolder;
                
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
                
                const content = document.createElement('div');
                content.className = 'media-subfolder-content';
                content.style.cssText = 'display: none; visibility: hidden; height: 0; min-height: 0; max-height: 0; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; padding: 10px 0;';
                
                // Add media cards to content BEFORE appending to section
                // This ensures cards are in the DOM when the section is expanded
                groupedMedia[subfolder].forEach((media, index) => {
                    const card = createMediaCard(media, index, assignments, text);
                    content.appendChild(card);
                });
                
                console.log('Media Browser: Created subfolder section for', subfolder, 'with', groupedMedia[subfolder].length, 'files, content has', content.children.length, 'children');
                
                section.appendChild(content);
                grid.appendChild(section);
            });
        }
        
        // Update count - IMPORTANT: Count actual displayed files after DOM is updated
        // Use setTimeout to ensure DOM is fully updated before counting
        setTimeout(() => {
            const countEl = document.getElementById('observationMediaCount');
            if (countEl) {
                // Count actual displayed files by counting media cards in the grid
                const displayedCards = grid.querySelectorAll('.observation-media-card');
                const actualCount = displayedCards.length;
                countEl.textContent = `${actualCount} file${actualCount !== 1 ? 's' : ''}`;
                console.log('Media Browser: Count updated - filteredMediaFiles:', filteredMediaFiles.length, '| displayedCards:', actualCount);
                
                // Warn if there's a mismatch (but allow for async loading)
                if (filteredMediaFiles.length !== actualCount && actualCount > 0 && Math.abs(filteredMediaFiles.length - actualCount) > 10) {
                    console.warn('Media Browser: Large count mismatch - filteredMediaFiles:', filteredMediaFiles.length, 'vs displayedCards:', actualCount);
                }
            }
        }, 200);
        
        // Update media card states
        if (typeof window.updateMediaCardStates === 'function') {
            try {
                window.updateMediaCardStates();
            } catch (e) {
                console.error('Error calling updateMediaCardStates:', e);
            }
        }
    }
    
    function createMediaCard(media, index, assignments, text) {
        const card = document.createElement('div');
        card.className = 'observation-media-card';
        card.dataset.mediaIndex = index;
        card.dataset.mediaPath = media.path;
        card.dataset.mediaName = media.name;
        card.dataset.mediaType = media.type;
        
        const isAssigned = isMediaAssigned(media.path);
        const sectionColor = isAssigned ? getSectionColorForMedia(media.path, assignments, text) : null;
        
        if (isAssigned) {
            card.classList.add('media-assigned');
            card.style.opacity = '0.5';
            card.style.cursor = 'not-allowed';
        } else {
            card.draggable = true;
            card.style.cursor = 'grab';
        }
        
        const thumbSize = '640x480';
        const thumbWidth = 640;
        const thumbHeight = 480;
        
        const badgeStyle = isAssigned 
            ? (sectionColor 
                ? `style="background: ${sectionColor}E6; border-color: ${sectionColor}; color: white;"`
                : 'style="background: rgba(78, 205, 196, 0.9); border-color: #4ecdc4; color: white;"')
            : '';
        
        card.innerHTML = `
            <div class="observation-media-thumbnail">
                <img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(media.path)}&size=${thumbSize}" 
                     alt="${escapeHtml(media.name)}" 
                     onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'${thumbWidth}\' height=\'${thumbHeight}\'%3E%3Crect fill=\'%23333\' width=\'${thumbWidth}\' height=\'${thumbHeight}\'/%3E%3Ctext x=\'50%25\' y=\'50%25\' text-anchor=\'middle\' dy=\'.3em\' fill=\'%23999\' font-size=\'12\'%3E${media.type === 'video' ? 'VIDEO' : media.type === 'audio' ? 'AUDIO' : media.type === 'document' ? 'PDF' : 'IMAGE'}%3C/text%3E%3C/svg%3E'">
                ${media.type === 'video' ? '<span class="video-badge">⏯</span>' : ''}
                ${media.type === 'audio' ? '<span class="audio-badge">🎵</span>' : ''}
                ${media.type === 'document' ? '<span class="pdf-badge">📄</span>' : ''}
                ${media.type === 'audio' ? `<div class="audio-player-overlay" onclick="event.stopPropagation(); if(typeof window.playAudioFile === 'function') { window.playAudioFile('${encodeURIComponent(media.path)}', '${escapeHtml(media.name)}'); }"><span class="audio-play-button">▶</span></div>` : ''}
                ${isAssigned ? `<span class="assigned-badge" ${badgeStyle}>✓ Assigned</span>` : ''}
            </div>
            <div class="observation-media-info">
                <div class="observation-media-name" 
                     title="${escapeHtml(media.name)}"
                     data-media-path="${escapeHtml(media.path)}"
                     data-media-name="${escapeHtml(media.name)}"
                     onclick="if(typeof window.handleMediaNameClick === 'function') { window.handleMediaNameClick(event, this); }"
                     style="cursor: pointer; user-select: none;">
                    ${escapeHtml(media.name)}
                </div>
                <div class="observation-media-size">${formatFileSize(media.size)}</div>
            </div>
        `;
        
        if (!isAssigned) {
            card.addEventListener('dragstart', function(e) {
                // The event's currentTarget is automatically set to the card
                // Just call handleMediaDragStart - it will use e.currentTarget
                if (typeof window.handleMediaDragStart === 'function') {
                    window.handleMediaDragStart(e);
                }
            });
            // Also add dragend to clean up
            card.addEventListener('dragend', function(e) {
                card.classList.remove('dragging');
                card.style.opacity = '';
            });
            card.addEventListener('click', function() {
                if (typeof window.handleMediaClick === 'function') {
                    window.handleMediaClick(media);
                }
            });
        }
        
        return card;
    }
    
    function toggleSubfolderSection(subfolder) {
        const section = document.querySelector(`[data-subfolder="${subfolder}"]`);
        if (section) {
            const wasCollapsed = section.classList.contains('collapsed');
            section.classList.toggle('collapsed');
            const content = section.querySelector('.media-subfolder-content');
            const icon = section.querySelector('.section-icon');
            
            if (section.classList.contains('collapsed')) {
                // Collapse
                if (content) {
                    content.style.display = 'none';
                    content.style.visibility = 'hidden';
                    content.style.height = '0';
                    content.style.minHeight = '0';
                    content.style.maxHeight = '0';
                }
                if (icon) icon.textContent = '▶';
            } else {
                // Expand
                if (content) {
                    // Verify cards exist before expanding
                    const cards = content.querySelectorAll('.observation-media-card');
                    console.log('Media Browser: Expanding subfolder', subfolder, '- Found', cards.length, 'cards, content has', content.children.length, 'children');
                    
                    if (cards.length === 0 && content.children.length > 0) {
                        console.warn('Media Browser: Subfolder', subfolder, 'has children but no .observation-media-card elements! Children:', Array.from(content.children).map(c => c.className || c.tagName));
                    }
                    
                    // Ensure grid layout is set with all necessary properties
                    content.style.display = 'grid';
                    content.style.visibility = 'visible';
                    content.style.height = 'auto';
                    content.style.minHeight = 'auto';
                    content.style.maxHeight = 'none';
                    content.style.gridTemplateColumns = 'repeat(auto-fill, minmax(200px, 1fr))';
                    content.style.gap = '15px';
                    content.style.padding = '10px 0';
                    
                    // Force a reflow to ensure rendering
                    void content.offsetHeight;
                }
                if (icon) icon.textContent = '▼';
            }
        }
    }
    
    function loadObservationMedia() {
        const qualificationSelect = document.getElementById('qualificationSelect');
        const learnerSelect = document.getElementById('learnerSelect');
        const subfolderSelect = document.getElementById('observationSubfolderSelect');
        
        if (!qualificationSelect || !learnerSelect) {
            console.error('Qualification or learner select not found');
            return;
        }
        
        // IMPORTANT: If draft is loaded, use draft's qualification/learner to ensure correct path
        // This ensures media browser shows only media from the draft's learner path
        let qualification, learner;
        if (window.currentDraft && window.currentDraft.id && window.currentDraft.qualification && window.currentDraft.learner) {
            qualification = window.currentDraft.qualification;
            learner = window.currentDraft.learner;
            console.log('Media Browser: Using draft qualification/learner:', qualification, '/', learner, '(path: OUTPUT_FOLDER/', qualification, '/', learner, ')');
            // Also update dropdowns to match draft
            if (qualificationSelect.value !== qualification) {
                qualificationSelect.value = qualification;
            }
            if (learnerSelect.value !== learner) {
                learnerSelect.value = learner;
            }
        } else {
            // No draft or draft doesn't have qualification/learner - use dropdown values
            qualification = qualificationSelect.value;
            learner = learnerSelect.value;
            console.log('Media Browser: Using dropdown qualification/learner:', qualification, '/', learner);
        }
        
        let subfolder = subfolderSelect ? subfolderSelect.value : '';
        
        // If draft is loaded, use draft's selected subfolder to filter media
        // This ensures we only show media relevant to the loaded draft
        if (window.currentDraft && window.currentDraft.id && window.currentDraft.selected_subfolder) {
            subfolder = window.currentDraft.selected_subfolder;
            console.log('Media Browser: Draft loaded - filtering to subfolder:', subfolder);
            // Also update the select if it exists
            if (subfolderSelect) {
                subfolderSelect.value = subfolder;
            }
        }
        
        if (!qualification || !learner) {
            const grid = document.getElementById('observationMediaGrid');
            if (grid) {
                grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Please select both qualification and learner</p>';
            }
            const countEl = document.getElementById('observationMediaCount');
            if (countEl) {
                countEl.textContent = '0 files';
            }
            return;
        }
        
        // Try to get media from window.observationMediaData first
        let mediaFiles = [];
        if (window.observationMediaData) {
            if (subfolder && window.observationMediaData[subfolder]) {
                // Only show media from the selected subfolder
                mediaFiles = window.observationMediaData[subfolder];
                console.log('Media Browser: Filtered to subfolder:', subfolder, '- Found', mediaFiles.length, 'files');
            } else if (!subfolder) {
                // If no subfolder selected and draft has subfolder, don't show any media
                if (window.currentDraft && window.currentDraft.id && window.currentDraft.selected_subfolder) {
                    console.log('Media Browser: Draft has subfolder but none selected - showing empty');
                    mediaFiles = [];
                } else {
                    // Get all media from all subfolders only if no draft subfolder restriction
                    Object.keys(window.observationMediaData).forEach(key => {
                        if (window.observationMediaData[key] && Array.isArray(window.observationMediaData[key])) {
                            mediaFiles = mediaFiles.concat(window.observationMediaData[key]);
                        }
                    });
                }
            }
        }
        
        // If no data available, fetch from API
        if (mediaFiles.length === 0) {
            const grid = document.getElementById('observationMediaGrid');
            if (grid) {
                grid.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Loading media files...</p>';
            }
            
            // Ensure we use draft's qualification/learner if available
            const fetchQualification = (window.currentDraft && window.currentDraft.id && window.currentDraft.qualification) 
                ? window.currentDraft.qualification 
                : qualification;
            const fetchLearner = (window.currentDraft && window.currentDraft.id && window.currentDraft.learner) 
                ? window.currentDraft.learner 
                : learner;
            
            const fetchUrl = `/v2p-formatter/media-converter/observation-media/media?qualification=${encodeURIComponent(fetchQualification)}&learner=${encodeURIComponent(fetchLearner)}`;
            console.log('Media Browser: Fetching media from:', fetchUrl, '(draft path:', fetchQualification, '/', fetchLearner, ')');
            
            fetch(fetchUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success && data.media) {
                        // IMPORTANT: When loading for a draft, clear old data first to avoid incorrect counts
                        // Only keep data if it's for the same qualification/learner as the draft
                        if (window.currentDraft && window.currentDraft.id && window.currentDraft.qualification && window.currentDraft.learner) {
                            const draftQualification = window.currentDraft.qualification;
                            const draftLearner = window.currentDraft.learner;
                            const expectedPath = `${draftQualification}/${draftLearner}`;
                            
                            // Clear old data that doesn't match the draft's path
                            if (window.observationMediaData) {
                                const oldKeys = Object.keys(window.observationMediaData);
                                let clearedCount = 0;
                                oldKeys.forEach(key => {
                                    const oldMedia = window.observationMediaData[key];
                                    if (oldMedia && oldMedia.length > 0) {
                                        const samplePath = oldMedia[0].path || '';
                                        const isSamePath = samplePath.includes(`/${expectedPath}/`) || samplePath.includes(`\\${expectedPath}\\`);
                                        if (!isSamePath) {
                                            clearedCount += oldMedia.length;
                                            delete window.observationMediaData[key];
                                        }
                                    }
                                });
                                if (clearedCount > 0) {
                                    console.log('Media Browser: Cleared', clearedCount, 'old files from different path');
                                }
                            }
                        }
                        
                        if (!window.observationMediaData) {
                            window.observationMediaData = {};
                        }
                        // Group by subfolder
                        data.media.forEach(media => {
                            const sf = media.subfolder || '';
                            if (!window.observationMediaData[sf]) {
                                window.observationMediaData[sf] = [];
                            }
                            window.observationMediaData[sf].push(media);
                        });
                        
                        console.log('Media Browser: Stored', data.media.length, 'files grouped by subfolder for path:', fetchQualification, '/', fetchLearner);
                        
                        // IMPORTANT: Filter by draft subfolder if draft is loaded
                        // Re-check draft subfolder (it might have been set during fetch)
                        const draftSubfolderAfterFetch = (window.currentDraft && window.currentDraft.id && window.currentDraft.selected_subfolder) 
                            ? window.currentDraft.selected_subfolder 
                            : null;
                        
                        // Use draft subfolder if available, otherwise use manual selection
                        const finalSubfolder = draftSubfolderAfterFetch || subfolder;
                        
                        console.log('Media Browser: After fetch - Draft subfolder:', draftSubfolderAfterFetch, '| Manual subfolder:', subfolder, '| Final:', finalSubfolder);
                        
                        if (finalSubfolder && window.observationMediaData[finalSubfolder]) {
                            // Show only media from final subfolder
                            mediaFiles = window.observationMediaData[finalSubfolder];
                            console.log('Media Browser: After fetch - Filtered to subfolder:', finalSubfolder, '- Found', mediaFiles.length, 'files', draftSubfolderAfterFetch ? '(draft filter)' : '(manual selection)');
                        } else if (finalSubfolder) {
                            // Subfolder specified but not found - show empty
                            mediaFiles = [];
                            console.log('Media Browser: After fetch - Subfolder', finalSubfolder, 'not found - showing empty');
                        } else {
                            // No subfolder filter - show all media ONLY if no draft restriction
                            if (draftSubfolderAfterFetch) {
                                // Draft has subfolder but it's not in data - show empty
                                mediaFiles = [];
                                console.log('Media Browser: After fetch - Draft subfolder', draftSubfolderAfterFetch, 'not in fetched data - showing empty');
                            } else {
                                // No draft, no subfolder - show all
                                Object.keys(window.observationMediaData).forEach(key => {
                                    if (window.observationMediaData[key] && Array.isArray(window.observationMediaData[key])) {
                                        mediaFiles = mediaFiles.concat(window.observationMediaData[key]);
                                    }
                                });
                                console.log('Media Browser: After fetch - No subfolder filter - showing all', mediaFiles.length, 'files');
                            }
                        }
                        
                        displayObservationMedia(mediaFiles);
                    } else {
                        const grid = document.getElementById('observationMediaGrid');
                        if (grid) {
                            grid.innerHTML = `<p style="color: #999; text-align: center; padding: 20px;">${data.error || 'No media files found'}</p>`;
                        }
                        const countEl = document.getElementById('observationMediaCount');
                        if (countEl) {
                            countEl.textContent = '0 files';
                        }
                    }
                })
                .catch(error => {
                    console.error('Media Browser: Error loading media:', error);
                    const grid = document.getElementById('observationMediaGrid');
                    if (grid) {
                        grid.innerHTML = `<p style="color: #ff6b6b; text-align: center; padding: 20px;">Error loading media: ${error.message}</p>`;
                    }
                    const countEl = document.getElementById('observationMediaCount');
                    if (countEl) {
                        countEl.textContent = '0 files';
                    }
                });
        } else {
            displayObservationMedia(mediaFiles);
        }
    }
    
    // Export to window immediately
    window.displayObservationMedia = displayObservationMedia;
    window.loadObservationMedia = loadObservationMedia;
    window.toggleSubfolderSection = toggleSubfolderSection;
    
    console.log('✅ Media Browser library loaded');
})();

