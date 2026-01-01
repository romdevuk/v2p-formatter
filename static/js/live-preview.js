/**
 * Live Preview Library - Standalone
 * Provides updatePreview and related functions immediately
 */

(function() {
    'use strict';
    
    // Constants
    const PLACEHOLDER_PATTERN = /\{\{([A-Za-z0-9_]+)\}\}/g;
    const PLACEHOLDER_COLORS = [
        '#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', 
        '#6c5ce7', '#a29bfe', '#fd79a8', '#00b894'
    ];
    const SECTION_COLORS = [
        '#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24',
        '#6c5ce7', '#a29bfe', '#fd79a8', '#00b894'
    ];
    
    // Helper functions
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    function extractPlaceholders(text) {
        if (!text) return [];
        const matches = [];
        let match;
        const pattern = new RegExp(PLACEHOLDER_PATTERN);
        while ((match = pattern.exec(text)) !== null) {
            matches.push(match[1].toLowerCase());
        }
        return [...new Set(matches)].sort();
    }
    
    function assignPlaceholderColors(placeholders) {
        const colorMap = {};
        placeholders.forEach((placeholder, index) => {
            colorMap[placeholder] = PLACEHOLDER_COLORS[index % PLACEHOLDER_COLORS.length];
        });
        return colorMap;
    }
    
    function getCurrentAssignments() {
        return window.observationMediaAssignments || {};
    }
    
    function parseSections(text) {
        const sections = [];
        const lines = text.split('\n');
        let currentSection = null;
        let currentContent = [];
        let preSectionContent = [];
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const match = line.match(/^SECTION\s*[:-]?\s*(.+)$/i);
            
            if (match) {
                if (currentSection) {
                    currentSection.content = currentContent.join('\n');
                    sections.push(currentSection);
                }
                const title = match[1].trim();
                const sectionIndex = sections.length;
                currentSection = {
                    id: `section-${sectionIndex}`,
                    title: title,
                    color: SECTION_COLORS[sectionIndex % SECTION_COLORS.length],
                    content: '',
                    index: sectionIndex
                };
                currentContent = [];
            } else {
                if (currentSection) {
                    currentContent.push(line);
                } else {
                    preSectionContent.push(line);
                }
            }
        }
        
        if (currentSection) {
            currentSection.content = currentContent.join('\n');
            sections.push(currentSection);
        }
        
        return {
            hasSections: sections.length > 0,
            preSectionContent: preSectionContent.join('\n'),
            sections: sections
        };
    }
    
    function getSectionStates() {
        try {
            const stored = localStorage.getItem('observationSectionStates');
            return stored ? JSON.parse(stored) : {};
        } catch (e) {
            return {};
        }
    }
    
    function saveSectionStates(states) {
        try {
            localStorage.setItem('observationSectionStates', JSON.stringify(states));
        } catch (e) {
            // Ignore
        }
    }
    
    function validatePlaceholders(text, assignments) {
        const placeholders = extractPlaceholders(text);
        const assignedPlaceholders = new Set(Object.keys(assignments).map(k => k.toLowerCase()));
        const unassigned = placeholders.filter(p => !assignedPlaceholders.has(p));
        const assigned = placeholders.filter(p => assignedPlaceholders.has(p));
        
        return {
            all_placeholders: placeholders,
            assigned: assigned,
            unassigned: unassigned,
            is_valid: unassigned.length === 0,
            total_count: placeholders.length,
            assigned_count: assigned.length,
            unassigned_count: unassigned.length
        };
    }
    
    function generateMediaTable(mediaList, placeholder) {
        if (mediaList.length === 0) {
            return `<table class="placeholder-table" style="border: 1px solid #000; border-collapse: collapse; width: 100%; margin: 10px 0;" data-placeholder="${placeholder}">
                <tr>
                    <td style="border: 1px solid #000; padding: 10px; min-height: 50px;" ondrop="if(typeof window.handleTableDrop === 'function') { window.handleTableDrop(event, '${placeholder}'); } else if(typeof handleTableDrop === 'function') { handleTableDrop(event, '${placeholder}'); }" ondragover="if(typeof window.handleTableDragOver === 'function') { window.handleTableDragOver(event); } else if(typeof handleTableDragOver === 'function') { handleTableDragOver(event); }"></td>
                    <td style="border: 1px solid #000; padding: 10px; min-height: 50px;" ondrop="if(typeof window.handleTableDrop === 'function') { window.handleTableDrop(event, '${placeholder}'); } else if(typeof handleTableDrop === 'function') { handleTableDrop(event, '${placeholder}'); }" ondragover="if(typeof window.handleTableDragOver === 'function') { window.handleTableDragOver(event); } else if(typeof handleTableDragOver === 'function') { handleTableDragOver(event); }"></td>
                </tr>
            </table>`;
        }
        
        let tableHtml = `<table class="placeholder-table" style="border: 1px solid #000; border-collapse: collapse; width: 100%; margin: 10px 0;" data-placeholder="${placeholder}"><tbody>`;
        
        for (let i = 0; i < mediaList.length; i += 2) {
            tableHtml += '<tr>';
            for (let j = 0; j < 2; j++) {
                const media = mediaList[i + j];
                if (media) {
                    const thumbSize = '400x300';
                    tableHtml += `<td class="media-cell" style="border: 1px solid #000; padding: 10px; position: relative; cursor: grab;" 
                        draggable="true" 
                        ondragstart="if(typeof window.handleTableCellDragStart === 'function') { window.handleTableCellDragStart(event, ${i + j}, '${placeholder}'); }"
                        data-media-index="${i + j}" 
                        data-placeholder="${placeholder}"
                        title="Drag to reorder media">
                        <img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(media.path)}&size=${thumbSize}" 
                             alt="${escapeHtml(media.name)}" 
                             style="max-width: 100%; height: auto; display: block;">
                        <button class="remove-media-btn" onclick="if(typeof window.removeMediaFromPlaceholder === 'function') { window.removeMediaFromPlaceholder('${placeholder}', '${escapeHtml(media.path)}'); } else if(typeof removeMediaFromPlaceholder === 'function') { removeMediaFromPlaceholder('${placeholder}', '${escapeHtml(media.path)}'); }" 
                                style="position: absolute; top: 5px; right: 5px; background: #ff6b6b; color: white; border: none; border-radius: 50%; width: 24px; height: 24px; cursor: pointer; font-size: 14px; opacity: 0; transition: opacity 0.2s;">×</button>
                    </td>`;
                } else {
                    tableHtml += `<td class="media-cell" style="border: 1px solid #000; padding: 10px; min-height: 50px;" 
                        data-media-index="${i + j}" 
                        data-placeholder="${placeholder}"
                        ondrop="if(typeof window.handleTableDrop === 'function') { window.handleTableDrop(event, '${placeholder}'); }" 
                        ondragover="if(typeof window.handleTableDragOver === 'function') { window.handleTableDragOver(event); }"></td>`;
                }
            }
            tableHtml += '</tr>';
        }
        tableHtml += '</tbody></table>';
        return tableHtml;
    }
    
    function renderSectionContent(content, placeholders, colorMap, assignments, validation) {
        let html = '';
        let lastIndex = 0;
        const placeholderPositions = [];
        
        placeholders.forEach(placeholder => {
            const pattern = new RegExp(`\\{\\{${placeholder}\\}\\}`, 'gi');
            let match;
            while ((match = pattern.exec(content)) !== null) {
                placeholderPositions.push({
                    start: match.index,
                    end: match.index + match[0].length,
                    placeholder: placeholder
                });
            }
        });
        
        placeholderPositions.sort((a, b) => a.start - b.start);
        
        placeholderPositions.forEach(pos => {
            if (pos.start > lastIndex) {
                html += escapeHtml(content.substring(lastIndex, pos.start)).replace(/\n/g, '<br>');
            }
            
            const placeholder = pos.placeholder;
            const placeholderKey = placeholder.toLowerCase();
            const assignedMedia = assignments[placeholderKey] || [];
            
            if (assignedMedia.length > 0) {
                html += generateMediaTable(assignedMedia, placeholder);
            } else {
                html += `<div class="unassigned-placeholder-container" data-placeholder="${escapeHtml(placeholder)}">
                    <table class="placeholder-table unassigned" style="border: 2px dashed #ff6b6b; border-collapse: collapse; width: 100%; margin: 10px 0; background: rgba(255, 107, 107, 0.1);" ondrop="if(typeof window.handleTableDrop === 'function') { window.handleTableDrop(event, '${escapeHtml(placeholder)}'); } else if(typeof handleTableDrop === 'function') { handleTableDrop(event, '${escapeHtml(placeholder)}'); }" ondragover="if(typeof window.handleTableDragOver === 'function') { window.handleTableDragOver(event); } else if(typeof handleTableDragOver === 'function') { handleTableDragOver(event); }">
                        <tr>
                            <td style="border: 1px solid #ff6b6b; padding: 20px; min-height: 80px; text-align: center; color: #ff6b6b; font-size: 12px;">Drop media here</td>
                            <td style="border: 1px solid #ff6b6b; padding: 20px; min-height: 80px; text-align: center; color: #ff6b6b; font-size: 12px;">Drop media here</td>
                        </tr>
                    </table>
                    <div style="text-align: center; color: #ff6b6b; font-size: 11px; margin-top: 5px;">{{${escapeHtml(placeholder)}}} - Unassigned</div>
                </div>`;
            }
            
            lastIndex = pos.end;
        });
        
        if (lastIndex < content.length) {
            html += escapeHtml(content.substring(lastIndex)).replace(/\n/g, '<br>');
        }
        
        if (placeholderPositions.length === 0) {
            html = escapeHtml(content).replace(/\n/g, '<br>');
        }
        
        placeholders.forEach(placeholder => {
            const color = colorMap[placeholder];
            const placeholderPattern = new RegExp(`(\\{\\{${placeholder}\\}\\})`, 'gi');
            html = html.replace(placeholderPattern, `<span style="color: ${color}; font-weight: bold;">$1</span>`);
        });
        
        return html;
    }
    
    function renderSections(sectionData, placeholders, colorMap, assignments, validation) {
        const states = getSectionStates();
        let html = '';
        
        if (sectionData.preSectionContent.trim()) {
            html += escapeHtml(sectionData.preSectionContent).replace(/\n/g, '<br>');
        }
        
        sectionData.sections.forEach(section => {
            const isExpanded = states[section.id] === true;
            const sectionContent = renderSectionContent(section.content, placeholders, colorMap, assignments, validation);
            
            let mediaCount = 0;
            const sectionPlaceholders = extractPlaceholders(section.content);
            sectionPlaceholders.forEach(placeholder => {
                const placeholderKey = placeholder.toLowerCase();
                if (assignments[placeholderKey]) {
                    mediaCount += assignments[placeholderKey].length;
                }
            });
            
            const mediaCountBadge = mediaCount > 0 
                ? `<span class="section-media-count" style="background: ${section.color}30; border: 1px solid ${section.color}; color: ${section.color}; padding: 4px 8px; border-radius: 4px; font-size: 12px; margin-right: 10px;">${mediaCount} media</span>`
                : `<span class="section-media-count zero-media" style="background: rgba(153, 153, 153, 0.2); border: 1px solid #666; color: #999; padding: 4px 8px; border-radius: 4px; font-size: 12px; margin-right: 10px;">0 media</span>`;
            
            const contentStyle = isExpanded ? 'border: 1px solid ' + section.color + '30; display: block !important;' : 'border: 1px solid ' + section.color + '30; display: none;';
            
            html += `<div class="observation-section ${isExpanded ? '' : 'collapsed'}" data-section-id="${section.id}" style="border-left: 3px solid ${section.color};">
                <div class="observation-section-header" onclick="toggleSection('${section.id}')" style="background: ${section.color}20; border: 1px solid ${section.color}; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: ${section.color}; font-weight: bold; font-size: 16px;">${escapeHtml(section.title)}</span>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        ${mediaCountBadge}
                        <span class="observation-section-icon" style="color: ${section.color}; font-size: 16px;">${isExpanded ? '▼' : '▶'}</span>
                    </div>
                </div>
                <div class="observation-section-content" style="${contentStyle}">${sectionContent}</div>
            </div>`;
        });
        
        return html;
    }
    
    // Main updatePreview function
    function updatePreview() {
        const editor = document.getElementById('observationTextEditor');
        const preview = document.getElementById('observationPreview');
        if (!editor || !preview) return;
        
        const text = editor.value;
        const placeholders = extractPlaceholders(text);
        const colorMap = assignPlaceholderColors(placeholders);
        const assignments = getCurrentAssignments();
        const validation = validatePlaceholders(text, assignments);
        const sectionData = parseSections(text);
        
        let previewHtml = '';
        
        if (sectionData.hasSections) {
            previewHtml = renderSections(sectionData, placeholders, colorMap, assignments, validation);
        } else {
            // Simple rendering without sections
            let lastIndex = 0;
            const placeholderPositions = [];
            
            placeholders.forEach(placeholder => {
                const pattern = new RegExp(`\\{\\{${placeholder}\\}\\}`, 'gi');
                let match;
                while ((match = pattern.exec(text)) !== null) {
                    placeholderPositions.push({
                        start: match.index,
                        end: match.index + match[0].length,
                        placeholder: placeholder
                    });
                }
            });
            
            placeholderPositions.sort((a, b) => a.start - b.start);
            
            placeholderPositions.forEach(pos => {
                if (pos.start > lastIndex) {
                    previewHtml += escapeHtml(text.substring(lastIndex, pos.start)).replace(/\n/g, '<br>');
                }
                
                const placeholder = pos.placeholder;
                const assignedMedia = assignments[placeholder] || [];
                
                if (assignedMedia.length > 0) {
                    previewHtml += generateMediaTable(assignedMedia, placeholder);
                } else {
                    previewHtml += `<div class="unassigned-placeholder-container" data-placeholder="${escapeHtml(placeholder)}">
                        <table class="placeholder-table unassigned" style="border: 2px dashed #ff6b6b; border-collapse: collapse; width: 100%; margin: 10px 0; background: rgba(255, 107, 107, 0.1);" ondrop="if(typeof window.handleTableDrop === 'function') { window.handleTableDrop(event, '${escapeHtml(placeholder)}'); } else if(typeof handleTableDrop === 'function') { handleTableDrop(event, '${escapeHtml(placeholder)}'); }" ondragover="if(typeof window.handleTableDragOver === 'function') { window.handleTableDragOver(event); } else if(typeof handleTableDragOver === 'function') { handleTableDragOver(event); }">
                            <tr>
                                <td style="border: 1px solid #ff6b6b; padding: 20px; min-height: 80px; text-align: center; color: #ff6b6b; font-size: 12px;">Drop media here</td>
                                <td style="border: 1px solid #ff6b6b; padding: 20px; min-height: 80px; text-align: center; color: #ff6b6b; font-size: 12px;">Drop media here</td>
                            </tr>
                        </table>
                        <div style="text-align: center; color: #ff6b6b; font-size: 11px; margin-top: 5px;">{{${escapeHtml(placeholder)}}} - Unassigned</div>
                    </div>`;
                }
                
                lastIndex = pos.end;
            });
            
            if (lastIndex < text.length) {
                previewHtml += escapeHtml(text.substring(lastIndex)).replace(/\n/g, '<br>');
            }
            
            if (placeholderPositions.length === 0) {
                previewHtml = escapeHtml(text).replace(/\n/g, '<br>');
            }
            
            placeholders.forEach(placeholder => {
                const color = colorMap[placeholder];
                const placeholderPattern = new RegExp(`(\\{\\{${placeholder}\\}\\})`, 'gi');
                previewHtml = previewHtml.replace(placeholderPattern, `<span style="color: ${color}; font-weight: bold;">$1</span>`);
            });
        }
        
        preview.innerHTML = previewHtml;
        
        // Show/hide section controls
        const sectionControls = document.getElementById('sectionControls');
        if (sectionControls) {
            sectionControls.style.display = sectionData.hasSections ? 'flex' : 'none';
        }
    }
    
    // Toggle section function
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
    
    // Export to window immediately
    window.updatePreview = updatePreview;
    window.extractPlaceholders = extractPlaceholders;
    window.assignPlaceholderColors = assignPlaceholderColors;
    window.parseSections = parseSections;
    window.getSectionStates = getSectionStates;
    window.saveSectionStates = saveSectionStates;
    window.toggleSection = toggleSection;
    // Note: handleTableCellDragStart is exported from observation-media.js, not here
    
    console.log('✅ Live Preview library loaded');
})();

