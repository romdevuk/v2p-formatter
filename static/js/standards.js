/**
 * Standards Library - Standalone
 * Provides loadStandardsFromDraft and clearStandards functions immediately
 */

(function() {
    'use strict';
    
    let currentStandardsData = null;
    
    // Helper functions
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    function clearStandardsSearch() {
        const searchInput = document.getElementById('standardsSearchInput');
        if (searchInput) {
            searchInput.value = '';
        }
        
        const units = document.querySelectorAll('.standards-unit');
        units.forEach(unit => {
            unit.style.display = '';
            const acs = unit.querySelectorAll('.standards-ac');
            acs.forEach(ac => {
                ac.style.display = '';
            });
        });
    }
    
    function parseSections(text) {
        if (!text) return { hasSections: false, sections: [] };
        
        const sections = [];
        const lines = text.split('\n');
        let currentSection = null;
        let currentContent = [];
        let preSectionContent = [];
        
        const SECTION_COLORS = [
            '#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24',
            '#6c5ce7', '#a29bfe', '#fd79a8', '#00b894'
        ];
        
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
    
    function parseAcCoveredLine(line, targetUnitId, targetAcId) {
        const acList = line.replace(/^AC\s+covered\s*[:.]?\s*/i, '').trim();
        if (!acList) return false;
        
        const escapedUnitId = targetUnitId.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const escapedAcId = targetAcId.replace(/\./g, '\\.');
        
        // Check for explicit unit:AC format
        const explicitPattern = new RegExp(`${escapedUnitId}\\s*[:.]\\s*${escapedAcId}\\b`, 'i');
        if (explicitPattern.test(acList)) {
            return true;
        }
        
        // Check for shorthand AC after unit mention
        const unitMentionPattern = new RegExp(`${escapedUnitId}\\s*[:.]\\s*[\\d.]+(?:\\s*,\\s*[\\d.]+)*`, 'i');
        if (unitMentionPattern.test(acList)) {
            const shorthandPattern = new RegExp(`(?:^|,)\\s*${escapedAcId}\\b`, 'i');
            if (shorthandPattern.test(acList)) {
                return true;
            }
        }
        
        return false;
    }
    
    function renderUnit(unit, unitIndex) {
        const unitId = unit.unit_id || unit.unit_internal_id || 'Unknown';
        const unitName = unit.unit_name || 'Unnamed Unit';
        
        const textEditor = document.getElementById('observationTextEditor');
        const draftText = textEditor ? textEditor.value : '';
        const sectionData = parseSections(draftText);
        
        let html = `<div class="standards-unit" data-unit-index="${unitIndex % 8}" data-unit-id="${unitId}">`;
        html += `<div class="standards-unit-header" onclick="toggleStandardsUnit(this)">`;
        html += `<span class="standards-unit-icon">▶</span>`;
        html += `<span class="standards-unit-title">${unitId}: ${escapeHtml(unitName)}</span>`;
        html += `</div>`;
        html += `<div class="standards-unit-content">`;
        
        if (unit.learning_outcomes && unit.learning_outcomes.length > 0) {
            unit.learning_outcomes.forEach(lo => {
                if (lo.questions && lo.questions.length > 0) {
                    lo.questions.forEach(question => {
                        const acId = question.question_id || '';
                        const acText = question.question_name || '';
                        const acType = question.question_type || 'Other';
                        
                        const coveredSections = [];
                        if (sectionData.hasSections && acId && unitId) {
                            const escapedUnitId = unitId.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                            const escapedAcId = acId.replace(/\./g, '\\.');
                            
                            for (const section of sectionData.sections) {
                                const sectionContent = section.content;
                                let matches = false;
                                
                                // Pattern 1: Explicit unit:AC format
                                const explicitPattern = new RegExp(`${escapedUnitId}\\s*[:.]\\s*${escapedAcId}\\b`, 'i');
                                if (explicitPattern.test(sectionContent)) {
                                    matches = true;
                                }
                                
                                // Pattern 2: Unit mentioned, then ACs listed
                                if (!matches) {
                                    const unitMentionPattern = new RegExp(`${escapedUnitId}\\s*[:.]\\s*[\\d.]+(?:\\s*,\\s*[\\d.]+)*`, 'i');
                                    const unitMentionMatch = sectionContent.match(unitMentionPattern);
                                    if (unitMentionMatch) {
                                        const acListPattern = new RegExp(`${escapedUnitId}\\s*[:.]\\s*[\\d.]+(?:\\s*,\\s*[\\d.]+)*`, 'gi');
                                        const acLists = sectionContent.matchAll(acListPattern);
                                        for (const acList of acLists) {
                                            const listContent = acList[0];
                                            if (new RegExp(`${escapedUnitId}\\s*[:.]\\s*${escapedAcId}\\b`, 'i').test(listContent)) {
                                                matches = true;
                                                break;
                                            }
                                            if (new RegExp(`(?:^|,)\\s*${escapedAcId}\\b`, 'i').test(listContent)) {
                                                matches = true;
                                                break;
                                            }
                                        }
                                    }
                                }
                                
                                // Pattern 3: "Unit 641 AC 1.1" format
                                if (!matches) {
                                    const unitAcPattern = new RegExp(`(?:Unit\\s+)?${escapedUnitId}\\s+(?:AC\\s+)?${escapedAcId}\\b`, 'i');
                                    if (unitAcPattern.test(sectionContent)) {
                                        matches = true;
                                    }
                                }
                                
                                // Pattern 4: "AC 641:1.1" format
                                if (!matches) {
                                    const acUnitPattern = new RegExp(`AC\\s+${escapedUnitId}\\s*[:.]\\s*${escapedAcId}\\b`, 'i');
                                    if (acUnitPattern.test(sectionContent)) {
                                        matches = true;
                                    }
                                }
                                
                                // Pattern 5: "AC covered:" lines
                                if (!matches) {
                                    const acCoveredLinePattern = /AC\s+covered\s*[:.]?\s*([\s\S]*?)(?=\n\s*AC\s+covered\s*[:.]?\s*|$)/gi;
                                    const acCoveredLines = [];
                                    let match;
                                    acCoveredLinePattern.lastIndex = 0;
                                    
                                    while ((match = acCoveredLinePattern.exec(sectionContent)) !== null) {
                                        const fullLine = match[0].trim();
                                        if (fullLine) {
                                            acCoveredLines.push(fullLine);
                                        }
                                    }
                                    
                                    for (const acCoveredLine of acCoveredLines) {
                                        if (parseAcCoveredLine(acCoveredLine, unitId, acId)) {
                                            matches = true;
                                            break;
                                        }
                                    }
                                }
                                
                                if (matches) {
                                    coveredSections.push(section);
                                }
                            }
                        }
                        
                        html += `<div class="standards-ac" data-ac-type="${escapeHtml(acType)}">`;
                        html += `<div class="standards-ac-id">${escapeHtml(acId)}</div>`;
                        html += `<div class="standards-ac-text">${escapeHtml(acText)}</div>`;
                        
                        if (coveredSections.length > 0) {
                            const sectionBullets = coveredSections.map(section => {
                                const sectionColor = section.color || '#667eea';
                                const sectionLabel = section.title || section.id || `section-${section.index}`;
                                const sectionId = section.id || `section-${section.index}`;
                                return `<div style="margin-left: 12px; margin-top: 2px;"><span style="color: ${sectionColor}; cursor: pointer; text-decoration: underline; text-decoration-style: dotted;" onclick="if(typeof window.expandSectionInPreview === 'function') { window.expandSectionInPreview('${sectionId}'); } event.stopPropagation();">${escapeHtml(sectionLabel)}</span></div>`;
                            }).join('');
                            
                            html += `<div class="standards-ac-covered" style="margin-top: 6px; font-size: 12px; color: #999;">Covered:${sectionBullets}</div>`;
                        } else {
                            html += `<div class="standards-ac-covered" style="margin-top: 6px; font-size: 12px; color: #999;">Covered:</div>`;
                        }
                        
                        html += `</div>`;
                    });
                }
            });
        }
        
        html += `</div>`;
        html += `</div>`;
        
        return html;
    }
    
    function renderStandards(jsonData) {
        const standardsContent = document.getElementById('standardsContent');
        if (!standardsContent) {
            console.error('standardsContent element not found');
            return;
        }
        
        clearStandardsSearch();
        
        if (!jsonData || !jsonData.qualifications || jsonData.qualifications.length === 0) {
            standardsContent.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No standards data available.</p>';
            return;
        }
        
        let html = '';
        let unitIndex = 0;
        
        jsonData.qualifications.forEach(qualification => {
            if (qualification.units && qualification.units.length > 0) {
                qualification.units.forEach(unit => {
                    html += renderUnit(unit, unitIndex);
                    unitIndex++;
                });
            }
        });
        
        if (html === '') {
            standardsContent.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No units found in standards file.</p>';
            return;
        }
        
        standardsContent.innerHTML = html;
    }
    
    async function loadStandardsFromDraft(draft) {
        const standardsContent = document.getElementById('standardsContent');
        if (!standardsContent) {
            console.error('standardsContent element not found');
            return;
        }
        
        console.log('Loading standards from draft:', draft);
        
        if (!draft || !draft.json_file_id) {
            console.log('No json_file_id in draft:', draft);
            standardsContent.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No JSON Standards File assigned to this draft.</p>';
            currentStandardsData = null;
            return;
        }
        
        standardsContent.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Loading standards...</p>';
        
        try {
            const url = `/v2p-formatter/ac-matrix/json-files/${draft.json_file_id}`;
            console.log('Fetching JSON file from:', url);
            
            const response = await fetch(url);
            console.log('Response status:', response.status, response.statusText);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Response error:', errorText);
                throw new Error(`Failed to load JSON file: ${response.status} ${response.statusText}`);
            }
            
            const jsonData = await response.json();
            console.log('JSON data received:', jsonData);
            currentStandardsData = jsonData;
            renderStandards(jsonData);
        } catch (error) {
            console.error('Error loading standards:', error);
            standardsContent.innerHTML = `<p style="color: #ff6b6b; text-align: center; padding: 20px;">Error loading standards: ${error.message || 'Unknown error'}. Check console for details.</p>`;
            currentStandardsData = null;
        }
    }
    
    function clearStandards() {
        const standardsContent = document.getElementById('standardsContent');
        if (standardsContent) {
            standardsContent.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No draft loaded. Load a draft to view standards.</p>';
        }
        currentStandardsData = null;
        clearStandardsSearch();
    }
    
    function toggleStandardsUnit(header) {
        const unit = header.closest('.standards-unit');
        if (unit) {
            unit.classList.toggle('expanded');
            const icon = header.querySelector('.standards-unit-icon');
            if (icon) {
                icon.textContent = unit.classList.contains('expanded') ? '▼' : '▶';
            }
        }
    }
    
    // Standards search functions
    let previousUnitStates = {};
    let standardsSearchDebounceTimer = null;
    
    function handleStandardsSearch(searchTerm) {
        const clearBtn = document.getElementById('standardsSearchClear');
        if (clearBtn) {
            clearBtn.style.display = searchTerm && searchTerm.trim() ? 'block' : 'none';
        }
        
        clearTimeout(standardsSearchDebounceTimer);
        standardsSearchDebounceTimer = setTimeout(() => {
            performStandardsSearch(searchTerm);
        }, 300);
    }
    
    function performStandardsSearch(searchTerm) {
        if (!searchTerm || searchTerm.trim() === '') {
            clearStandardsSearch();
            return;
        }
        
        const trimmedTerm = searchTerm.trim();
        const isExactPhrase = trimmedTerm.startsWith('"') && trimmedTerm.endsWith('"') && trimmedTerm.length > 2;
        const searchTermLower = isExactPhrase 
            ? trimmedTerm.slice(1, -1).toLowerCase() 
            : trimmedTerm.toLowerCase();
        
        const units = document.querySelectorAll('.standards-unit');
        let hasMatches = false;
        let firstMatchElement = null;
        
        // Store unit states if first search
        if (Object.keys(previousUnitStates).length === 0) {
            units.forEach(unit => {
                const unitId = unit.getAttribute('data-unit-id');
                previousUnitStates[unitId] = unit.classList.contains('expanded');
            });
        }
        
        units.forEach(unit => {
            const acs = unit.querySelectorAll('.standards-ac');
            let unitHasMatch = false;
            
            acs.forEach(acElement => {
                const acTextElement = acElement.querySelector('.standards-ac-text');
                if (!acTextElement) return;
                
                const acText = acTextElement.textContent || acTextElement.innerText || '';
                removeHighlights(acTextElement);
                const cleanText = acTextElement.textContent || acTextElement.innerText || acText;
                const acTextLower = cleanText.toLowerCase();
                let matches = false;
                
                if (isExactPhrase) {
                    matches = acTextLower.includes(searchTermLower);
                } else {
                    const words = searchTermLower.split(/\s+/).filter(w => w.length > 0);
                    matches = words.every(word => acTextLower.includes(word));
                }
                
                if (matches) {
                    unitHasMatch = true;
                    acElement.style.display = 'block';
                    if (!firstMatchElement) {
                        firstMatchElement = acElement.closest('.standards-unit');
                    }
                    highlightText(acTextElement, cleanText, searchTermLower, isExactPhrase);
                } else {
                    acElement.style.display = 'none';
                }
            });
            
            if (unitHasMatch) {
                expandStandardsUnit(unit);
                hasMatches = true;
            } else {
                collapseStandardsUnit(unit);
            }
        });
        
        const standardsContent = document.getElementById('standardsContent');
        const noResultsMsg = standardsContent ? standardsContent.querySelector('.standards-no-results') : null;
        if (!hasMatches) {
            if (standardsContent && !noResultsMsg) {
                const msg = document.createElement('div');
                msg.className = 'standards-no-results';
                msg.style.cssText = 'color: #999; text-align: center; padding: 20px; font-style: italic;';
                msg.textContent = `No results found for "${trimmedTerm}"`;
                standardsContent.insertBefore(msg, standardsContent.firstChild);
            } else if (noResultsMsg) {
                noResultsMsg.textContent = `No results found for "${trimmedTerm}"`;
            }
        } else {
            if (noResultsMsg) {
                noResultsMsg.remove();
            }
            if (firstMatchElement) {
                setTimeout(() => {
                    firstMatchElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }, 100);
            }
        }
    }
    
    function highlightText(element, originalText, searchTerm, isExactPhrase) {
        if (!originalText || !searchTerm) return;
        
        const textLower = originalText.toLowerCase();
        
        if (isExactPhrase) {
            const index = textLower.indexOf(searchTerm);
            if (index !== -1) {
                const before = escapeHtml(originalText.substring(0, index));
                const match = escapeHtml(originalText.substring(index, index + searchTerm.length));
                const after = escapeHtml(originalText.substring(index + searchTerm.length));
                element.innerHTML = before + 
                    '<span class="standards-search-highlight" style="background: #f9ca24; color: #000; padding: 2px 4px; border-radius: 2px;">' + match + '</span>' + 
                    after;
            } else {
                element.innerHTML = escapeHtml(originalText);
            }
        } else {
            const words = searchTerm.split(/\s+/).filter(w => w.length > 0);
            let highlightedText = escapeHtml(originalText);
            
            words.forEach(word => {
                const escapedWord = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                const regex = new RegExp(`\\b(${escapedWord})\\b`, 'gi');
                highlightedText = highlightedText.replace(regex, (match, p1, offset) => {
                    const beforeMatch = highlightedText.substring(0, offset);
                    const lastTagStart = beforeMatch.lastIndexOf('<');
                    const lastTagEnd = beforeMatch.lastIndexOf('>');
                    if (lastTagStart > lastTagEnd) {
                        return match;
                    }
                    return '<span class="standards-search-highlight" style="background: #f9ca24; color: #000; padding: 2px 4px; border-radius: 2px;">' + p1 + '</span>';
                });
            });
            
            element.innerHTML = highlightedText;
        }
    }
    
    function removeHighlights(element) {
        const highlights = element.querySelectorAll('.standards-search-highlight');
        highlights.forEach(highlight => {
            const parent = highlight.parentNode;
            if (parent) {
                parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
                parent.normalize();
            }
        });
        if (element.innerHTML) {
            element.innerHTML = element.textContent;
        }
    }
    
    function expandStandardsUnit(unit) {
        if (unit && !unit.classList.contains('expanded')) {
            unit.classList.add('expanded');
            const icon = unit.querySelector('.standards-unit-icon');
            if (icon) {
                icon.textContent = '▼';
            }
        }
    }
    
    function collapseStandardsUnit(unit) {
        if (unit && unit.classList.contains('expanded')) {
            unit.classList.remove('expanded');
            const icon = unit.querySelector('.standards-unit-icon');
            if (icon) {
                icon.textContent = '▶';
            }
        }
    }
    
    // Export to window immediately
    window.loadStandardsFromDraft = loadStandardsFromDraft;
    window.clearStandards = clearStandards;
    window.toggleStandardsUnit = toggleStandardsUnit;
    window.handleStandardsSearch = handleStandardsSearch;
    window.performStandardsSearch = performStandardsSearch;
    window.clearStandardsSearch = clearStandardsSearch;
    
    console.log('✅ Standards library loaded');
})();

