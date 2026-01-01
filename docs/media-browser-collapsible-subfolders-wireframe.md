# Media Browser - Collapsible Subfolder Sections - Text Wireframe

## Overview
This wireframe specifies the implementation of collapsible subfolder sections in the media browser. When media files are organized into subfolders, each subfolder will be displayed as a collapsible section that can be expanded or collapsed. All subfolder sections will be collapsed by default.

## Version
**1.0.0** - Initial Specification

---

## 1. Functional Requirements

### 1.1 Collapsible Subfolder Sections
- **Requirement**: Each subfolder containing media files should be displayed as a collapsible section
- **Default State**: All subfolder sections collapsed by default
- **Behavior**: Clicking the section header toggles expand/collapse
- **Visual Indicator**: Clear icon/arrow showing expanded (▼) or collapsed (▶) state
- **File Count**: Display number of files in each subfolder in the header

### 1.2 Section Structure
- **Header**: Clickable header with subfolder name, file count, and expand/collapse icon
- **Content**: Media thumbnails grid contained within the section
- **Styling**: Visual distinction between sections (borders, background, spacing)
- **Grid Layout**: Media thumbnails within each section follow the configured grid layout

### 1.3 Empty Subfolders
- **Requirement**: Empty subfolders should not be displayed
- **Behavior**: Only subfolders with media files are shown

---

## 2. Text Wireframe: Current Layout vs. Proposed Layout

### 2.1 Current Layout (Flat Display)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MEDIA BROWSER                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ 📊 24 files                              [⚙️ Settings] [⬛ Expand] │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ Media Thumbnails (3 columns)                                      │  │
│ │                                                                     │  │
│ │ ┌──────────────────────────────────────────────────────────────┐  │  │
│ │ │ 📁 Subfolder1                              (12 files)        │  │  │
│ │ └──────────────────────────────────────────────────────────────┘  │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │IMG │ │IMG │ │VID │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │VID │ │IMG │ │IMG │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ │                                                                     │  │
│ │ ┌──────────────────────────────────────────────────────────────┐  │  │
│ │ │ 📁 Subfolder2                              (8 files)         │  │  │
│ │ └──────────────────────────────────────────────────────────────┘  │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │IMG │ │IMG │ │VID │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ │                                                                     │  │
│ │ ┌──────────────────────────────────────────────────────────────┐  │  │
│ │ │ 📁 Subfolder3                              (4 files)         │  │  │
│ │ └──────────────────────────────────────────────────────────────┘  │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │VID │ │IMG │ │IMG │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Proposed Layout (Collapsible Sections - All Collapsed by Default)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MEDIA BROWSER                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ 📊 24 files                              [⚙️ Settings] [⬛ Expand] │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ Media Thumbnails (3 columns)                                      │  │
│ │                                                                     │  │
│ │ ┌──────────────────────────────────────────────────────────────┐  │  │
│ │ │ ▶ 📁 Subfolder1                              (12 files)      │  │  │
│ │ └──────────────────────────────────────────────────────────────┘  │  │
│ │                                                                     │  │
│ │ ┌──────────────────────────────────────────────────────────────┐  │  │
│ │ │ ▶ 📁 Subfolder2                              (8 files)       │  │  │
│ │ └──────────────────────────────────────────────────────────────┘  │  │
│ │                                                                     │  │
│ │ ┌──────────────────────────────────────────────────────────────┐  │  │
│ │ │ ▶ 📁 Subfolder3                              (4 files)       │  │  │
│ │ └──────────────────────────────────────────────────────────────┘  │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Proposed Layout (One Section Expanded)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MEDIA BROWSER                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ 📊 24 files                              [⚙️ Settings] [⬛ Expand] │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ Media Thumbnails (3 columns)                                      │  │
│ │                                                                     │  │
│ │ ┌──────────────────────────────────────────────────────────────┐  │  │
│ │ │ ▼ 📁 Subfolder1                              (12 files)      │  │  │
│ │ └──────────────────────────────────────────────────────────────┘  │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │IMG │ │IMG │ │VID │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │VID │ │IMG │ │IMG │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │IMG │ │IMG │ │VID │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ │                                                                     │  │
│ │ ┌──────────────────────────────────────────────────────────────┐  │  │
│ │ │ ▶ 📁 Subfolder2                              (8 files)       │  │  │
│ │ └──────────────────────────────────────────────────────────────┘  │  │
│ │                                                                     │  │
│ │ ┌──────────────────────────────────────────────────────────────┐  │  │
│ │ │ ▶ 📁 Subfolder3                              (4 files)       │  │  │
│ │ └──────────────────────────────────────────────────────────────┘  │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Behavior Specifications

### 3.1 Section Header Design

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Subfolder Section Header (Collapsed State)                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ ▶ 📁 Subfolder Name                                  (12 files)   │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  Components:                                                             │
│  - ▶ Icon (collapsed) / ▼ Icon (expanded)                               │
│  - 📁 Folder icon                                                        │
│  - Subfolder name (bold, colored)                                        │
│  - File count badge "(12 files)"                                         │
│  - Clickable area (entire header)                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Subfolder Section Header (Expanded State)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ ▼ 📁 Subfolder Name                                  (12 files)   │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  Components:                                                             │
│  - ▼ Icon (expanded) / ▶ Icon (collapsed)                               │
│  - 📁 Folder icon                                                        │
│  - Subfolder name (bold, colored)                                        │
│  - File count badge "(12 files)"                                         │
│  - Clickable area (entire header)                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Section Content (Media Grid)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Expanded Section Content                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ ▼ 📁 Subfolder1                                  (12 files)       │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ Media Thumbnails (within section)                                 │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │IMG │ │IMG │ │VID │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │VID │ │IMG │ │IMG │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │IMG │ │IMG │ │VID │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │VID │ │IMG │ │IMG │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Visual Design Specifications

### 4.1 Section Header Styling

#### Collapsed State
```
┌──────────────────────────────────────────┐
│ Background: #1e1e1e                      │
│ Border: 1px solid #555                   │
│ Border-left: 3px solid #667eea          │
│ Border-radius: 4px                       │
│ Padding: 12px 15px                       │
│ Cursor: pointer                          │
│ Hover: Background #2a2a2a                │
│                                          │
│ ▶ Icon: #667eea, 14px                    │
│ 📁 Icon: #667eea, 16px                   │
│ Text: #e0e0e0, bold, 14px               │
│ File count: #999, normal, 12px           │
└──────────────────────────────────────────┘
```

#### Expanded State
```
┌──────────────────────────────────────────┐
│ Background: #1e1e1e                      │
│ Border: 1px solid #555                   │
│ Border-left: 3px solid #667eea          │
│ Border-radius: 4px 4px 0 0              │
│ Padding: 12px 15px                       │
│ Cursor: pointer                          │
│ Hover: Background #2a2a2a                │
│                                          │
│ ▼ Icon: #667eea, 14px                    │
│ 📁 Icon: #667eea, 16px                   │
│ Text: #e0e0e0, bold, 14px               │
│ File count: #999, normal, 12px           │
└──────────────────────────────────────────┘
```

### 4.2 Section Content Styling

```
┌──────────────────────────────────────────┐
│ Background: transparent (inherits grid)  │
│ Border: 1px solid #555                   │
│ Border-top: none                         │
│ Border-radius: 0 0 4px 4px              │
│ Padding: 15px                            │
│ Margin-bottom: 15px                      │
│                                          │
│ Grid layout matches parent settings      │
│ (2-6 columns when collapsed)             │
│ (auto-calculated when expanded)          │
└──────────────────────────────────────────┘
```

### 4.3 Section Spacing

```
┌──────────────────────────────────────────┐
│ Section 1                                │
│ ┌──────────────────────────────────────┐ │
│ │ Header + Content                     │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ Margin-bottom: 15px                      │
│                                          │
│ Section 2                                │
│ ┌──────────────────────────────────────┐ │
│ │ Header + Content                     │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ Margin-bottom: 15px                      │
│                                          │
│ Section 3                                │
│ ┌──────────────────────────────────────┐ │
│ │ Header + Content                     │ │
│ └──────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

---

## 5. Technical Implementation Details

### 5.1 HTML Structure

```html
<div id="observationMediaGrid" class="observation-media-grid">
    <!-- Subfolder Section 1 -->
    <div class="media-subfolder-section collapsed" data-subfolder="Subfolder1">
        <div class="media-subfolder-header" onclick="toggleSubfolderSection('Subfolder1')">
            <span class="section-icon">▶</span>
            <span class="folder-icon">📁</span>
            <span class="subfolder-name">Subfolder1</span>
            <span class="file-count">(12 files)</span>
        </div>
        <div class="media-subfolder-content" style="display: none;">
            <!-- Media cards grid -->
            <div class="observation-media-card">...</div>
            <div class="observation-media-card">...</div>
            <!-- ... more cards ... -->
        </div>
    </div>
    
    <!-- Subfolder Section 2 -->
    <div class="media-subfolder-section collapsed" data-subfolder="Subfolder2">
        <!-- ... -->
    </div>
</div>
```

### 5.2 CSS Classes

```css
.media-subfolder-section {
    margin-bottom: 15px;
    border: 1px solid #555;
    border-radius: 4px;
    background: transparent;
}

.media-subfolder-header {
    background: #1e1e1e;
    border-bottom: 1px solid #555;
    padding: 12px 15px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    user-select: none;
    border-left: 3px solid #667eea;
    border-radius: 4px 4px 0 0;
    transition: background 0.2s;
}

.media-subfolder-header:hover {
    background: #2a2a2a;
}

.media-subfolder-section.collapsed .media-subfolder-header {
    border-radius: 4px;
    border-bottom: none;
}

.media-subfolder-content {
    padding: 15px;
    display: grid;
    /* Grid columns set dynamically based on settings */
}

.media-subfolder-section.collapsed .media-subfolder-content {
    display: none;
}

.section-icon {
    color: #667eea;
    font-size: 14px;
    transition: transform 0.2s;
}

.folder-icon {
    color: #667eea;
    font-size: 16px;
}

.subfolder-name {
    color: #e0e0e0;
    font-weight: bold;
    font-size: 14px;
    flex: 1;
}

.file-count {
    color: #999;
    font-size: 12px;
    font-weight: normal;
}
```

### 5.3 JavaScript Functions

```javascript
// Toggle subfolder section expand/collapse
function toggleSubfolderSection(subfolderName) {
    const section = document.querySelector(`[data-subfolder="${subfolderName}"]`);
    if (!section) return;
    
    const isCollapsed = section.classList.contains('collapsed');
    const content = section.querySelector('.media-subfolder-content');
    const icon = section.querySelector('.section-icon');
    
    if (isCollapsed) {
        // Expand
        section.classList.remove('collapsed');
        if (content) content.style.display = 'grid';
        if (icon) icon.textContent = '▼';
        
        // Save expanded state to localStorage
        saveSubfolderState(subfolderName, true);
    } else {
        // Collapse
        section.classList.add('collapsed');
        if (content) content.style.display = 'none';
        if (icon) icon.textContent = '▶';
        
        // Save collapsed state to localStorage
        saveSubfolderState(subfolderName, false);
    }
}

// Save subfolder expanded/collapsed state
function saveSubfolderState(subfolderName, isExpanded) {
    const states = JSON.parse(localStorage.getItem('mediaBrowser.subfolderStates') || '{}');
    states[subfolderName] = isExpanded;
    localStorage.setItem('mediaBrowser.subfolderStates', JSON.stringify(states));
}

// Load subfolder expanded/collapsed states
function loadSubfolderStates() {
    return JSON.parse(localStorage.getItem('mediaBrowser.subfolderStates') || '{}');
}

// Apply saved states on page load (optional - default is all collapsed)
function applySubfolderStates() {
    const states = loadSubfolderStates();
    Object.keys(states).forEach(subfolderName => {
        if (states[subfolderName]) {
            // Expand this subfolder
            const section = document.querySelector(`[data-subfolder="${subfolderName}"]`);
            if (section) {
                section.classList.remove('collapsed');
                const content = section.querySelector('.media-subfolder-content');
                const icon = section.querySelector('.section-icon');
                if (content) content.style.display = 'grid';
                if (icon) icon.textContent = '▼';
            }
        }
    });
}
```

---

## 6. Behavior Specifications

### 6.1 Default Behavior

#### On Page Load
1. All subfolder sections are **collapsed by default**
2. Section headers display ▶ icon (collapsed state)
3. Section content is hidden
4. File count is visible in header

#### User Interaction
1. Clicking section header toggles expand/collapse
2. Icon changes: ▶ (collapsed) ↔ ▼ (expanded)
3. Content animates (optional smooth transition)
4. State can be saved to localStorage (optional feature)

### 6.2 Edge Cases

#### Single Subfolder
- If only one subfolder exists, it's still collapsed by default
- User can expand it manually if needed

#### Many Subfolders
- All subfolders remain collapsed by default
- User can expand multiple subfolders simultaneously
- Scroll behavior works normally within expanded sections

#### Empty Subfolders
- Empty subfolders are not displayed
- Only subfolders with at least one media file are shown

#### No Subfolders
- If media files are not grouped by subfolder, display normally (no sections)
- Flat grid layout as before

---

## 7. User Experience Considerations

### 7.1 Benefits
- **Organized View**: Clear visual organization by subfolder
- **Space Efficient**: Collapsed by default saves screen space
- **Easy Navigation**: Quick access to specific subfolders
- **Scalability**: Works well with many subfolders

### 7.2 Visual Hierarchy
```
Media Browser
  └─ Subfolder Section 1 (collapsed) ▶
  └─ Subfolder Section 2 (collapsed) ▶
  └─ Subfolder Section 3 (collapsed) ▶

After expanding Section 1:
  └─ Subfolder Section 1 (expanded) ▼
      └─ Media Grid (thumbnails)
  └─ Subfolder Section 2 (collapsed) ▶
  └─ Subfolder Section 3 (collapsed) ▶
```

### 7.3 Interaction Flow

```
1. Page loads → All sections collapsed
   └─ User sees: ▶ Subfolder1 (12 files)
   └─ User sees: ▶ Subfolder2 (8 files)
   └─ User sees: ▶ Subfolder3 (4 files)

2. User clicks Subfolder1 header
   └─ Section expands
   └─ Icon changes: ▶ → ▼
   └─ Thumbnails appear below header

3. User clicks Subfolder1 header again
   └─ Section collapses
   └─ Icon changes: ▼ → ▶
   └─ Thumbnails hide
```

---

## 8. Grid Layout Within Sections

### 8.1 Grid Behavior

#### Collapsed Sections
- No grid visible (content hidden)
- Header takes full width

#### Expanded Sections
- Grid follows configured settings:
  - **Collapsed browser (50% width)**: Uses user-selected columns (2-6)
  - **Expanded browser (100% width)**: Auto-calculated columns
- Grid spans full width of section content area
- Media cards maintain consistent sizing

### 8.2 Grid CSS

```css
.media-subfolder-content {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* Dynamic based on settings */
    gap: 15px;
    padding: 15px;
}

/* When browser is collapsed */
.media-subfolder-content {
    grid-template-columns: repeat(N, 1fr); /* N from settings */
}

/* When browser is expanded */
.observation-media-left-panel.expanded .media-subfolder-content {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
}
```

---

## 9. Animation and Transitions

### 9.1 Expand/Collapse Animation (Optional)

```
Collapsed → Expanded:
┌──────────────┐
│ Header       │
└──────────────┘
        ↓ (smooth transition, 200ms)
┌──────────────┐
│ Header       │
├──────────────┤
│ Content      │
│ (fade in)    │
└──────────────┘

Expanded → Collapsed:
┌──────────────┐
│ Header       │
├──────────────┤
│ Content      │
│ (fade out)   │
└──────────────┘
        ↓ (smooth transition, 200ms)
┌──────────────┐
│ Header       │
└──────────────┘
```

### 9.2 Icon Rotation (Optional)

```
▶ (collapsed) → ▼ (expanded)
- Rotate 90 degrees clockwise
- Transition: 200ms ease-in-out
```

---

## 10. Implementation Checklist

### 10.1 Required Changes

- [ ] Update `displayObservationMedia()` function to create collapsible sections
- [ ] Add CSS classes for subfolder sections (header, content, collapsed/expanded states)
- [ ] Implement `toggleSubfolderSection()` JavaScript function
- [ ] Update grid layout to work within sections
- [ ] Ensure default state is collapsed for all sections
- [ ] Handle case when no subfolders exist (flat display)
- [ ] Test with single subfolder
- [ ] Test with multiple subfolders
- [ ] Test with many subfolders (scrolling)

### 10.2 Optional Enhancements

- [ ] Save/restore expanded states to localStorage
- [ ] Smooth expand/collapse animations
- [ ] Icon rotation animation
- [ ] "Expand All" / "Collapse All" buttons
- [ ] Keyboard shortcuts (Enter/Space to toggle)

---

## 11. Questions for Approval

1. **Default State**: All sections collapsed by default?
   - Recommendation: Yes, as specified

2. **State Persistence**: Should expanded/collapsed states be saved?
   - Recommendation: Optional enhancement, not required initially

3. **Animation**: Smooth transitions when expanding/collapsing?
   - Recommendation: Simple display toggle initially, add animations later if needed

4. **Expand All / Collapse All**: Add buttons to expand/collapse all sections?
   - Recommendation: Optional enhancement for later

5. **No Subfolders**: When media files aren't in subfolders, display normally?
   - Recommendation: Yes, fallback to current flat display

---

## 12. Approval Checklist

- [ ] Collapsible subfolder sections approved
- [ ] Default collapsed state approved
- [ ] Section header design approved
- [ ] Section content styling approved
- [ ] Grid layout within sections approved
- [ ] Visual hierarchy approved
- [ ] Implementation approach approved

---

**Document Status**: Draft - Awaiting Approval  
**Last Updated**: [Current Date]  
**Author**: AI Assistant  
**Reviewer**: [Pending]





