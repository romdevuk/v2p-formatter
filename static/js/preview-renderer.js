/**
 * Shared Preview Renderer Library
 * Provides consistent preview rendering across AC Matrix and Observation Media modules
 */

// Section color palette
const SECTION_COLORS = [
    '#667eea', // Blue
    '#f093fb', // Pink
    '#4facfe', // Light Blue
    '#43e97b', // Green
    '#fa709a', // Rose
    '#fee140', // Yellow
    '#30cfd0', // Cyan
    '#a8edea', // Aqua
    '#ff9a9e', // Coral
    '#fad0c4'  // Peach
];

// Placeholder pattern
const PLACEHOLDER_PATTERN = /\{\{([A-Za-z0-9_]+)\}\}/g;

/**
 * Extract placeholders from text
 */
function extractPlaceholders(text) {
    if (!text) return [];

    const matches = [];
    let match;
    const pattern = new RegExp(PLACEHOLDER_PATTERN);

    while ((match = pattern.exec(text)) !== null) {
        matches.push(match[1].toLowerCase());
    }

    // Return unique placeholders, sorted
    return [...new Set(matches)].sort();
}

/**
 * Parse sections from text
 */
function parseSections(text) {
    const sectionPattern = /^SECTION\s*[:-]?\s*(.+)$/gim;
    const sections = [];
    const lines = text.split('\n');
    let currentSection = null;
    let currentContent = [];
    let preSectionContent = [];

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const match = line.match(/^SECTION\s*[:-]?\s*(.+)$/i);

        if (match) {
            // Save previous section if exists
            if (currentSection) {
                currentSection.content = currentContent.join('\n');
                sections.push(currentSection);
            }

            // Start new section
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

    // Save last section
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

/**
 * Count media items in a section
 */
function countMediaInSection(section, assignments) {
    if (!section || !assignments) return 0;
    
    const placeholders = extractPlaceholders(section.content);
    let totalCount = 0;
    
    placeholders.forEach(placeholder => {
        const placeholderKey = placeholder.toLowerCase();
        const mediaList = assignments[placeholderKey];
        if (mediaList && Array.isArray(mediaList)) {
            totalCount += mediaList.length;
        }
    });
    
    return totalCount;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Generate read-only media table HTML (for preview display)
 */
function generateReadOnlyMediaTable(mediaList, placeholder) {
    if (!mediaList || mediaList.length === 0) {
        return `<div class="unassigned-placeholder-container" data-placeholder="${escapeHtml(placeholder)}">
            <table class="placeholder-table unassigned" 
                   style="border: 2px dashed #667eea; border-collapse: collapse; width: 100%; margin: 10px 0; background: rgba(102, 126, 234, 0.1);">
                <tr>
                    <td style="border: 1px solid #667eea; padding: 20px; min-height: 60px; text-align: center; color: #667eea; font-size: 12px;">
                        {{${escapeHtml(placeholder)}}} - Unassigned
                    </td>
                </tr>
            </table>
        </div>`;
    }

    const thumbSize = '400x300';
    let tableHtml = `<table class="placeholder-table" 
                            style="border: 1px solid #000; border-collapse: collapse; width: 100%; margin: 10px 0;"
                            data-placeholder="${placeholder}">
        <tbody>`;

    // Generate rows (2 columns per row)
    for (let i = 0; i < mediaList.length; i += 2) {
        tableHtml += '<tr>';

        // Column 1
        const hasMedia1 = mediaList[i] !== undefined && mediaList[i] !== null;
        tableHtml += `<td class="media-cell" 
                          style="border: 1px solid #000; padding: 10px; width: 50%; position: relative;">`;
        if (mediaList[i]) {
            if (mediaList[i].type === 'image') {
                tableHtml += `<img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(mediaList[i].path)}&size=${thumbSize}" 
                                   style="max-width: 100%; height: auto;" 
                                   alt="${mediaList[i].name}">`;
            } else {
                tableHtml += `<div style="padding: 10px; text-align: center; color: #e0e0e0;">${mediaList[i].name}</div>`;
            }
        }
        tableHtml += '</td>';

        // Column 2
        tableHtml += `<td class="media-cell" 
                          style="border: 1px solid #000; padding: 10px; width: 50%; position: relative;">`;
        if (mediaList[i + 1]) {
            if (mediaList[i + 1].type === 'image') {
                tableHtml += `<img src="/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(mediaList[i + 1].path)}&size=${thumbSize}" 
                                   style="max-width: 100%; height: auto;" 
                                   alt="${mediaList[i + 1].name}">`;
            } else {
                tableHtml += `<div style="padding: 10px; text-align: center; color: #e0e0e0;">${mediaList[i + 1].name}</div>`;
            }
        }
        tableHtml += '</td>';

        tableHtml += '</tr>';
    }

    tableHtml += '</tbody></table>';
    return tableHtml;
}

/**
 * Render content with media tables
 */
function renderContentWithMedia(text, assignments = {}) {
    if (!text) return '';
    const placeholders = extractPlaceholders(text);
    const assignmentsLower = {};
    Object.keys(assignments || {}).forEach(k => {
        assignmentsLower[k.toLowerCase()] = assignments[k] || [];
    });

    let html = '';
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
            const segment = text.substring(lastIndex, pos.start);
            // Highlight AC patterns
            const acPattern = /\b\d{3,}(?::\d+(?:\.\d+)*|\.\d+(?:\.\d+)*)?/g;
            const escaped = escapeHtml(segment);
            html += escaped
                .replace(acPattern, match => `<span class="preview-ac-highlight">${match}</span>`)
                .replace(/\n/g, '<br>');
        }

        const placeholder = pos.placeholder;
        const assignedMedia = assignmentsLower[placeholder] || [];
        if (assignedMedia.length > 0) {
            html += generateReadOnlyMediaTable(assignedMedia, placeholder);
        } else {
            html += `<div class="unassigned-placeholder-container" data-placeholder="${escapeHtml(placeholder)}">
                <table class="placeholder-table unassigned" 
                       style="border: 2px dashed #667eea; border-collapse: collapse; width: 100%; margin: 10px 0; background: rgba(102, 126, 234, 0.1);">
                    <tr>
                        <td style="border: 1px solid #667eea; padding: 20px; min-height: 60px; text-align: center; color: #667eea; font-size: 12px;">
                            {{${escapeHtml(placeholder)}}} - Unassigned
                        </td>
                    </tr>
                </table>
            </div>`;
        }

        lastIndex = pos.end;
    });

    if (lastIndex < text.length) {
        const segment = text.substring(lastIndex);
        const acPattern = /\b\d{3,}(?::\d+(?:\.\d+)*|\.\d+(?:\.\d+)*)?/g;
        const escaped = escapeHtml(segment);
        html += escaped
            .replace(acPattern, match => `<span class="preview-ac-highlight">${match}</span>`)
            .replace(/\n/g, '<br>');
    }

    if (placeholderPositions.length === 0) {
        const acPattern = /\b\d{3,}(?::\d+(?:\.\d+)*|\.\d+(?:\.\d+)*)?/g;
        const escaped = escapeHtml(text);
        html = escaped
            .replace(acPattern, match => `<span class="preview-ac-highlight">${match}</span>`)
            .replace(/\n/g, '<br>');
    }

    return html;
}

/**
 * Render sections with media
 */
function renderSections(sectionData, assignments = {}, getSectionStates = null, saveSectionStates = null, toggleSection = null) {
    const states = getSectionStates ? getSectionStates() : {};
    let html = '';

    // Pre-section content
    if (sectionData.preSectionContent.trim()) {
        html += renderContentWithMedia(sectionData.preSectionContent, assignments);
    }

    // Render sections
    sectionData.sections.forEach(section => {
        const isExpanded = states[section.id] === true;
        const sectionContent = renderContentWithMedia(section.content, assignments);

        // Count actual media items in this section
        const mediaCount = countMediaInSection(section, assignments);
        const mediaCountBadge = mediaCount > 0 
            ? `<span class="section-media-count" style="background: ${section.color}30; border: 1px solid ${section.color}; color: ${section.color}; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: normal; white-space: nowrap; margin-right: 10px;">${mediaCount} media</span>`
            : `<span class="section-media-count zero-media" style="background: rgba(153, 153, 153, 0.2); border: 1px solid #666; color: #999; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: normal; white-space: nowrap; margin-right: 10px;">0 media</span>`;

        const contentStyle = isExpanded ? 
            `border: 1px solid ${section.color}30; display: block !important;` : 
            `border: 1px solid ${section.color}30; display: none;`;
        
        const toggleHandler = toggleSection ? `onclick="toggleSection('${section.id}')"` : '';
        
        html += `
            <div class="observation-section ${isExpanded ? '' : 'collapsed'}" data-section-id="${section.id}" style="border-left: 3px solid ${section.color}; margin-bottom: 10px; border-radius: 6px; overflow: hidden;">
                <div class="observation-section-header" ${toggleHandler}
                     style="background: linear-gradient(135deg, ${section.color}30 0%, ${section.color}10 100%); border: 1px solid ${section.color}; display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; cursor: pointer;">
                    <span style="color: #e0e0e0; font-weight: bold; font-size: 16px;">${section.index + 1} - ${escapeHtml(section.title)}</span>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        ${mediaCountBadge}
                        <span class="observation-section-icon" style="color: ${section.color}; font-size: 16px; font-weight: bold;">${isExpanded ? '▼' : '▶'}</span>
                    </div>
                </div>
                <div class="observation-section-content" style="${contentStyle} padding: 15px; background: #1a1a1a;">
                    <div class="preview-text" style="color: #e0e0e0; line-height: 1.6;">${sectionContent}</div>
                </div>
            </div>
        `;
    });

    return html;
}

// Export functions for use in other modules
if (typeof window !== 'undefined') {
    window.PreviewRenderer = {
        SECTION_COLORS,
        extractPlaceholders,
        parseSections,
        countMediaInSection,
        escapeHtml,
        generateReadOnlyMediaTable,
        renderContentWithMedia,
        renderSections
    };
}




