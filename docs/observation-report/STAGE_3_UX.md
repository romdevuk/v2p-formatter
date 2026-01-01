# Stage 3: UI/UX Implementation

**Status**: ⏳ Pending  
**Owner**: UX Designer (Agent-3)  
**Estimated Duration**: 2-3 days  
**Dependencies**: Stage 2 Complete (Libraries available)

---

## 📋 Objectives

Implement complete UI/UX for the Observation Report module:
- HTML template structure
- Dark theme styling
- 3-column resizable layout
- Navigation integration
- Responsive design
- All dialogs and modals

**⚠️ IMPORTANT**: Follow wireframes exactly, implement dark theme throughout.

---

## 🚨 CRITICAL UI/UX FEATURES

### ⚠️ Drag-and-Drop Visual Feedback (HIGH COMPLEXITY)

**This was a major complexity in the old module. Pay EXTRA attention to:**

1. **Drag State Styling**:
   - Media card opacity reduction during drag
   - Cursor change (grabbing/grabbed)
   - Drag preview image/ghost
   - Source card visual feedback

2. **Drop Zone Styling**:
   - Highlight valid drop zones (border, background)
   - Show insertion indicator
   - Invalidate hover states for invalid zones
   - Visual feedback for multiple drop zones

3. **CSS Classes Needed**:
   ```css
   .media-card.dragging { opacity: 0.5; cursor: grabbing; }
   .media-card.drag-source { opacity: 0.3; }
   .placeholder-cell.drop-zone-active { border: 2px dashed #667eea; background: rgba(102, 126, 234, 0.1); }
   .placeholder-cell.drop-zone-invalid { border: 2px dashed #ff6b6b; }
   .placeholder-cell.drop-zone-insert { /* insertion line indicator */ }
   ```

4. **Transitions**:
   - Smooth opacity transitions
   - Smooth border/background transitions
   - Animate drop zone highlighting
   - Animate insertion indicators

### ⚠️ Reshuffle Visual Feedback (HIGH COMPLEXITY)

**This was a major complexity in the old module. Pay EXTRA attention to:**

1. **Reorder Styling**:
   - Dragged item styling (higher z-index, opacity)
   - Target position indicator
   - Insertion line/arrow
   - Smooth item movement animation

2. **Table Cell States**:
   - Hover state for reorderable items
   - Active drag state
   - Target position highlight
   - Disabled state for non-reorderable

3. **Arrow Button Styling**:
   - Up/Down arrow buttons on each media item
   - Hover states
   - Disabled states (first/last item)
   - Click feedback

4. **CSS Classes Needed**:
   ```css
   .media-item.reordering { z-index: 1000; opacity: 0.8; transform: scale(1.05); }
   .media-item.reorder-target { border: 2px solid #667eea; }
   .media-item.insert-before { /* insertion indicator before */ }
   .media-item.insert-after { /* insertion indicator after */ }
   .reorder-button { /* arrow button styling */ }
   .reorder-button:disabled { opacity: 0.3; cursor: not-allowed; }
   ```

5. **Animations**:
   - Smooth position transitions
   - Fade in/out for insertions
   - Scale animation for drag start
   - Smooth table reflow

---

## 📝 Special Styling Notes

### Drag-and-Drop CSS Implementation

**Key CSS Requirements**:
```css
/* Media Browser - Drag States */
.observation-report-media-card {
  cursor: grab;
  transition: opacity 0.2s, transform 0.2s;
}

.observation-report-media-card:active {
  cursor: grabbing;
}

.observation-report-media-card.dragging {
  opacity: 0.5;
  transform: scale(0.95);
}

.observation-report-media-card.assigned {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* Live Preview - Drop Zones */
.observation-report-placeholder-cell {
  transition: border 0.2s, background 0.2s;
  min-height: 100px;
}

.observation-report-placeholder-cell.drag-over {
  border: 2px dashed #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.observation-report-placeholder-cell.drop-invalid {
  border: 2px dashed #ff6b6b;
  background: rgba(255, 107, 107, 0.1);
}

.observation-report-placeholder-cell.drop-target {
  border: 2px solid #667eea;
  background: rgba(102, 126, 234, 0.2);
}
```

### Reshuffle CSS Implementation

**Key CSS Requirements**:
```css
/* Media Item Reordering */
.observation-report-media-item {
  position: relative;
  transition: transform 0.3s, opacity 0.3s;
  cursor: move;
}

.observation-report-media-item.reordering {
  z-index: 1000;
  opacity: 0.8;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.observation-report-media-item.reorder-target {
  border: 2px solid #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.observation-report-media-item.insert-before::before {
  content: '';
  position: absolute;
  top: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: #667eea;
}

.observation-report-media-item.insert-after::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: #667eea;
}

/* Reorder Buttons */
.observation-report-reorder-button {
  padding: 4px 8px;
  background: #2a2a2a;
  border: 1px solid #555;
  color: #e0e0e0;
  cursor: pointer;
  transition: background 0.2s;
}

.observation-report-reorder-button:hover:not(:disabled) {
  background: #333;
  border-color: #667eea;
}

.observation-report-reorder-button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
```

---

---

## 📁 Files to Create

### 1. Main Template
**File**: `templates/observation_report.html`  
**Purpose**: Main page structure for Observation Report module

**Requirements**:
- Extends base template
- 95% viewport width (centered)
- Top controls section
- 3-column resizable layout (Media Browser | Live Preview | Standards)
- Collapsible sections at bottom (Header, Text Editor, Assessor Feedback)
- Actions buttons

**Structure**:
```html
{% extends "base.html" %}
<div class="observation-report-container">
  <!-- Top Navigation (with Observation Report tab active) -->
  <!-- Top Controls -->
  <!-- 3-Column Layout -->
  <!-- Collapsible Sections -->
  <!-- Actions -->
</div>
```

### 2. Main CSS
**File**: `static/css/observation-report.css`  
**Purpose**: Main module styles

**Requirements**:
- Page width: 95% of viewport, centered
- Dark theme colors
- Text input styling
- Textarea styling
- Select/dropdown styling
- Button styling
- Icon styling
- Scrollbar styling
- Focus states
- Disabled states

### 3. Library Component CSS
**Files**:
- `static/css/observation-report/observation-report-media-browser.css`
- `static/css/observation-report/observation-report-live-preview.css`
- `static/css/observation-report/observation-report-standards.css`
- `static/css/observation-report/observation-report-preview-draft.css`
- `static/css/observation-report/observation-report-column-resizer.css`

**Purpose**: Component-specific styling for each library

---

## 🎨 Dark Theme Specifications

### Color Palette
```css
/* Base Colors */
--bg-primary: #1e1e1e;
--bg-secondary: #2a2a2a;
--text-primary: #e0e0e0;
--text-secondary: #999;
--border: #555;
--accent: #667eea;

/* Input Fields */
input, textarea, select {
  background: #1e1e1e;
  color: #e0e0e0;
  border: 1px solid #555;
}
input:focus, textarea:focus, select:focus {
  border-color: #667eea;
  background: #2a2a2a;
}

/* Buttons */
button {
  background: #2a2a2a;
  color: #e0e0e0;
  border: 1px solid #555;
}
button.primary {
  background: #667eea;
  color: #fff;
}

/* Scrollbars */
::-webkit-scrollbar {
  width: 10px;
  background: #1e1e1e;
}
::-webkit-scrollbar-thumb {
  background: #555;
}
```

---

## ✅ Implementation Checklist

### Navigation Integration
- [ ] Add "Observation Report" tab to top navigation
- [ ] Set tab as active when on `/observation-report`
- [ ] Match navigation styling with other modules

### Main Template
- [ ] Create base structure
- [ ] Implement 95% width container (centered)
- [ ] Add top controls section
- [ ] Add 3-column layout containers
- [ ] Add collapsible sections
- [ ] Add actions buttons
- [ ] Include all library script tags

### Main CSS
- [ ] Implement page width and centering
- [ ] Implement dark theme base colors
- [ ] Style text inputs
- [ ] Style textareas
- [ ] Style selects/dropdowns
- [ ] Style buttons (primary/secondary)
- [ ] Style icons
- [ ] Style scrollbars
- [ ] Implement focus states
- [ ] Implement disabled states
- [ ] Implement hover states

### Media Browser CSS
- [ ] Style media grid layout
- [ ] Style media cards
- [ ] Style thumbnails
- [ ] Style assignment badges
- [ ] Style filename editing
- [ ] **⚠️ CRITICAL: Style drag-and-drop states (HIGH COMPLEXITY)**
  - [ ] Dragging state (opacity, cursor)
  - [ ] Drag source visual feedback
  - [ ] Drag preview styling
  - [ ] Assigned media disabled state
  - [ ] Transitions and animations

### Live Preview CSS
- [ ] Style preview container
- [ ] Style placeholder highlighting
- [ ] Style 2-column tables
- [ ] **⚠️ CRITICAL: Style drop zones (HIGH COMPLEXITY)**
  - [ ] Valid drop zone highlighting
  - [ ] Invalid drop zone styling
  - [ ] Drag-over state
  - [ ] Insertion indicators
  - [ ] Smooth transitions
- [ ] **⚠️ CRITICAL: Style reshuffle/reorder (HIGH COMPLEXITY)**
  - [ ] Reordering item styling
  - [ ] Target position indicators
  - [ ] Insertion line/arrow styling
  - [ ] Arrow button styling
  - [ ] Disabled button states
  - [ ] Smooth animations
- [ ] Style section containers
- [ ] Style section headers
- [ ] Style expand/collapse icons
- [ ] Style media in tables

### Standards CSS
- [ ] Style standards panel
- [ ] Style unit headers
- [ ] Style AC items
- [ ] Style coverage links
- [ ] Style search box
- [ ] Style expand/collapse controls

### Preview Draft CSS
- [ ] Style preview dialog (full-screen)
- [ ] Style 3-column layout in dialog
- [ ] Style sections list
- [ ] Style actions panel
- [ ] Style font settings
- [ ] Style visibility checkboxes
- [ ] Style close button

### Column Resizer CSS
- [ ] Style resizer bars
- [ ] Style drag cursor
- [ ] Style resize feedback

### Dialogs and Modals
- [ ] Style assignment dialog
- [ ] Style save draft dialog
- [ ] Style load draft dialog
- [ ] Style confirmation dialogs
- [ ] Style overlay/backdrop

### Responsive Design
- [ ] Test on different screen sizes
- [ ] Ensure 95% width maintained
- [ ] Ensure columns resize properly
- [ ] Test mobile layout (if needed)

---

## 📐 Layout Specifications

### Page Width
```css
.observation-report-container {
  width: 95%;
  max-width: 95%;
  margin: 0 auto;
  padding: 20px;
}
```

### 3-Column Layout
```css
.main-layout {
  display: flex;
  gap: 0;
}
.column {
  flex: 1;
  min-width: 200px; /* or 250px for right column */
}
.resizer {
  width: 4px;
  background: #555;
  cursor: col-resize;
}
```

### Collapsible Sections
```css
.collapsible-section {
  border: 1px solid #555;
  border-radius: 4px;
  margin-bottom: 10px;
}
.section-header {
  padding: 12px;
  background: #2a2a2a;
  cursor: pointer;
}
.section-content {
  padding: 12px;
  display: none; /* shown when expanded */
}
```

---

## 📚 Reference Documentation

- **Specification**: `docs/observation-media-complete-specification.md`
  - Section: Text Wireframes (lines 769-1010)
  - Section: UI Features (lines 621-767)
  - Section: CSS Requirements (lines 1530-1698)

---

## 🎯 Completion Criteria

Stage 3 is complete when:
- [ ] HTML template matches wireframes
- [ ] Dark theme applied throughout
- [ ] 95% width layout implemented
- [ ] 3-column resizable layout working
- [ ] Navigation tab integrated and active
- [ ] All dialogs styled
- [ ] Responsive design verified
- [ ] All library components styled
- [ ] Visual inspection matches specification

---

## 📝 Notes

- Reference existing modules for navigation pattern
- Use CSS variables for theme colors (easier to maintain)
- Ensure contrast ratios meet accessibility standards
- Test all interactive elements (hover, focus, active states)

---

## ✅ Stage 3 Gate

**Ready to proceed to Stage 4** when:
- All checklist items complete
- Visual verification matches wireframes
- Dark theme consistent throughout
- Progress tracker updated
- Orchestrator approval received

