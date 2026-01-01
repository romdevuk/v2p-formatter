# Stage 2: Frontend Core Libraries

**Status**: ⏳ Pending  
**Owner**: Frontend Developer (Agent-2)  
**Estimated Duration**: 3-4 days  
**Dependencies**: Stage 1 Complete (APIs available)

---

## 📋 Objectives

Implement all standalone JavaScript libraries for the Observation Report module:
- Media Browser Library
- Live Preview Library
- Standards Library
- Preview Draft Library
- Column Resizer Library
- Main Orchestrator

**⚠️ IMPORTANT**: All libraries must be standalone, reusable, and follow ES6 module pattern.

---

## 🚨 CRITICAL COMPLEX FEATURES

### ⚠️ Drag-and-Drop Media Assignment (HIGH COMPLEXITY)

**This was a major complexity in the old module. Pay EXTRA attention to:**

1. **Drag Source**: Media cards in Media Browser
   - Must handle single media drag
   - Must handle multiple selected media drag (bulk)
   - Must track drag state visually
   - Must prevent dragging already-assigned media

2. **Drop Target**: Placeholder tables in Live Preview
   - Must detect valid drop zones (placeholder table cells)
   - Must highlight drop zones on drag over
   - Must handle multiple placeholder scenario (show selection dialog)
   - Must handle single placeholder scenario (direct assignment)
   - Must prevent invalid drops (wrong target)

3. **State Management**:
   - Track which media is being dragged
   - Track which placeholder is target
   - Update assignments state atomically
   - Update UI immediately after drop
   - Sync Media Browser and Live Preview states

4. **Event Handling**:
   - `dragstart` on media card
   - `dragover` on placeholder cells (prevent default)
   - `drop` on placeholder cells
   - `dragend` cleanup
   - Handle touch events for mobile (if needed)

**Implementation Requirements**:
- Use native HTML5 Drag-and-Drop API
- Implement visual feedback (drag preview, drop zone highlighting)
- Handle edge cases (cancelled drag, invalid drop targets)
- Test thoroughly with multiple media items
- Test with multiple placeholders
- Test bulk drag-and-drop

### ⚠️ Media Reshuffle/Reordering (HIGH COMPLEXITY)

**This was a major complexity in the old module. Pay EXTRA attention to:**

1. **Reorder Context**: Within a single placeholder's media list
   - Media appear in 2-column table layout
   - Order is left-to-right, top-to-bottom
   - Position 0 = Row 0, Col 0
   - Position 1 = Row 0, Col 1
   - Position 2 = Row 1, Col 0
   - etc.

2. **Reorder Methods**:
   - **Drag-and-Drop**: Drag media item to new position within table
   - **Arrow Buttons**: Up/Down buttons to move items

3. **Table Layout Logic**:
   - Calculate row/col from position index
   - Recalculate positions when order changes
   - Maintain 2-column layout after reorder
   - Update visual layout immediately

4. **State Synchronization**:
   - Update media order in assignments state
   - Update Live Preview display
   - Persist order in draft save
   - Restore order on draft load

5. **Visual Feedback**:
   - Highlight source item during drag
   - Show insertion point indicator
   - Animate item movement
   - Update table immediately

**Implementation Requirements**:
- Implement drag-and-drop within table cells
- Implement arrow button navigation
- Handle edge cases (first item, last item, single item)
- Maintain correct 2-column layout
- Test with various media counts (1, 2, 3, 4, 5+ items)
- Test reorder persistence
- Test reorder with different media types

---

## 📝 Special Implementation Notes

### Drag-and-Drop Implementation Strategy

**Recommended Approach**:
1. **Separate drag handlers** for Media Browser and Live Preview
2. **Shared state manager** for assignments
3. **Event-based communication** between libraries
4. **Visual feedback layer** for drag states
5. **Comprehensive error handling** for invalid operations

**Key Code Structure**:
```javascript
// Media Browser - Drag Source
class ObservationReportMediaBrowser {
  handleDragStart(media, event) {
    // Set drag data
    // Add visual feedback
    // Emit dragStart event
  }
}

// Live Preview - Drop Target
class ObservationReportLivePreview {
  handleDragOver(placeholderId, cellIndex, event) {
    // Prevent default
    // Highlight drop zone
    // Show visual indicator
  }
  
  handleDrop(placeholderId, cellIndex, event) {
    // Get dragged media data
    // Validate drop target
    // Assign media to placeholder
    // Update UI
    // Emit assignment event
  }
}

// Main Orchestrator - State Management
class ObservationReport {
  handleMediaAssignment(media, placeholder) {
    // Update assignments state
    // Notify Media Browser (disable media)
    // Notify Live Preview (update table)
    // Persist to draft (if loaded)
  }
}
```

### Reshuffle Implementation Strategy

**Recommended Approach**:
1. **Position-based indexing** (0, 1, 2, 3... for table positions)
2. **Row/Column calculation** from position
3. **Array reordering** in assignments state
4. **Immediate visual update** in Live Preview
5. **Persistence** in draft save

**Key Code Structure**:
```javascript
// Live Preview - Reshuffle Handler
class ObservationReportLivePreview {
  reorderMedia(placeholderId, oldIndex, newIndex) {
    // Get current media array
    // Reorder array
    // Update assignments state
    // Re-render table
    // Emit reorder event
  }
  
  calculatePosition(row, col) {
    // Convert row/col to position index
    return row * 2 + col;
  }
  
  calculateRowCol(position) {
    // Convert position to row/col
    return {
      row: Math.floor(position / 2),
      col: position % 2
    };
  }
}
```

---

---

## 📁 Files to Create

### 1. Media Browser Library
**File**: `static/js/observation-report/observation-report-media-browser.js`  
**Purpose**: Standalone component for browsing and selecting media files

**API**:
```javascript
class ObservationReportMediaBrowser {
  constructor(containerId, options = {})
  loadMedia(qualification, learner)
  updateAssignmentState(assignments)
  setMediaList(mediaList)
  refresh()
  on(event, callback)
  off(event, callback)
}
```

**Features**:
- Media grid display with thumbnails
- Assignment state visualization
- Filename inline editing
- Drag-and-drop support
- Multi-select support
- File type indicators

**Events Emitted**:
- `mediaSelect`
- `mediaDeselect`
- `mediaDragStart`
- `filenameUpdate`

### 2. Live Preview Library
**File**: `static/js/observation-report/observation-report-live-preview.js`  
**Purpose**: Real-time document preview rendering

**API**:
```javascript
class ObservationReportLivePreview {
  constructor(containerId, options = {})
  updateContent(text, assignments, sections)
  renderPlaceholderTable(placeholder, mediaList)
  updateSectionStates(sections)
  expandSection(sectionId)
  collapseSection(sectionId)
  scrollToSection(sectionId)
  on(event, callback)
  off(event, callback)
}
```

**Features**:
- Real-time preview rendering
- Placeholder detection and highlighting
- 2-column table generation
- Section rendering with collapsible behavior
- Media embedding (images/videos/PDFs/MP3s)
- Rainbow color coding
- Dark theme support

**Events Emitted**:
- `placeholderClick`
- `sectionToggle`
- `mediaRemove`

### 3. Standards Library
**File**: `static/js/observation-report/observation-report-standards.js`  
**Purpose**: Standards/AC management component

**API**:
```javascript
class ObservationReportStandards {
  constructor(containerId, options = {})
  loadStandards(jsonFileId)
  searchStandards(keyword)
  clearSearch()
  expandUnit(unitId)
  collapseUnit(unitId)
  expandAllUnits()
  collapseAllUnits()
  updateCoverage(textContent)
  on(event, callback)
  off(event, callback)
}
```

**Features**:
- Unit/AC display
- AC coverage detection
- Search functionality with highlighting
- Section navigation links
- Expand/collapse functionality

**Events Emitted**:
- `sectionClick`
- `unitToggle`

### 4. Preview Draft Library
**File**: `static/js/observation-report/observation-report-preview-draft.js`  
**Purpose**: Preview dialog functionality

**API**:
```javascript
class ObservationReportPreviewDraft {
  constructor(options = {})
  open(content, assignments, sections, headerData, assessorFeedback)
  close()
  updateContent(content, assignments)
  updateSettings(settings)
  exportDOCX(options)
  updateDraft(options)
  on(event, callback)
  off(event, callback)
}
```

**Features**:
- 3-column resizable layout
- Section navigation
- Preview content rendering
- Actions panel (font settings, visibility toggles)
- DOCX export trigger
- Draft update trigger

**Dependencies**: Uses LivePreview and ColumnResizer libraries

### 5. Column Resizer Library
**File**: `static/js/observation-report/observation-report-column-resizer.js`  
**Purpose**: Resizable column layouts utility

**API**:
```javascript
class ObservationReportColumnResizer {
  constructor(containerId, options = {})
  addResizer(leftColumnId, rightColumnId, options)
  saveWidths(storageKey)
  loadWidths(storageKey)
  resetWidths()
  on(event, callback)
  off(event, callback)
}
```

**Features**:
- Drag-to-resize functionality
- Minimum width constraints
- localStorage persistence
- Multiple column support
- Smooth resize animation

### 6. Main Orchestrator
**File**: `static/js/observation-report.js`  
**Purpose**: Coordinates all libraries and manages module-level state

**Responsibilities**:
- Initialize all libraries
- Connect libraries via events/callbacks
- Manage module-level state
- Handle user interactions
- Coordinate API calls

---

## ✅ Implementation Checklist

### Media Browser Library
- [ ] Create class structure
- [ ] Implement media grid display
- [ ] Implement thumbnail generation
- [ ] Implement assignment state management
- [ ] Implement filename editing
- [ ] **⚠️ CRITICAL: Implement drag-and-drop (HIGH COMPLEXITY)**
  - [ ] Single media drag
  - [ ] Multiple media drag (bulk)
  - [ ] Drag state visual feedback
  - [ ] Prevent dragging assigned media
  - [ ] Drag data transfer setup
  - [ ] Drag end cleanup
- [ ] Implement multi-select
- [ ] Add event system
- [ ] Unit test library

### Live Preview Library
- [ ] Create class structure
- [ ] Implement placeholder extraction
- [ ] Implement placeholder highlighting
- [ ] Implement 2-column table generation
- [ ] **⚠️ CRITICAL: Implement drop zone handling (HIGH COMPLEXITY)**
  - [ ] Detect valid drop zones (placeholder table cells)
  - [ ] Highlight drop zones on drag over
  - [ ] Handle drop events
  - [ ] Handle multiple placeholder scenario (show dialog)
  - [ ] Handle single placeholder scenario (direct assignment)
  - [ ] Validate drop targets
  - [ ] Update assignments on drop
- [ ] **⚠️ CRITICAL: Implement media reshuffle/reordering (HIGH COMPLEXITY)**
  - [ ] Drag-and-drop reordering within table
  - [ ] Arrow button reordering (up/down)
  - [ ] Position-to-row/col calculation
  - [ ] Row/col-to-position calculation
  - [ ] Maintain 2-column layout after reorder
  - [ ] Visual feedback during reorder
  - [ ] State synchronization
- [ ] Implement section detection
- [ ] Implement section rendering
- [ ] Implement media embedding
- [ ] Implement rainbow colors
- [ ] Add event system
- [ ] Unit test library

### Standards Library
- [ ] Create class structure
- [ ] Implement unit/AC display
- [ ] Implement AC coverage detection
- [ ] Implement search functionality
- [ ] Implement section navigation
- [ ] Implement expand/collapse
- [ ] Add event system
- [ ] Unit test library

### Preview Draft Library
- [ ] Create class structure
- [ ] Implement 3-column layout
- [ ] Integrate LivePreview
- [ ] Integrate ColumnResizer
- [ ] Implement actions panel
- [ ] Implement settings management
- [ ] Add event system
- [ ] Unit test library

### Column Resizer Library
- [ ] Create class structure
- [ ] Implement drag-to-resize
- [ ] Implement width constraints
- [ ] Implement localStorage persistence
- [ ] Add event system
- [ ] Unit test library

### Main Orchestrator
- [ ] Create main class
- [ ] Initialize all libraries
- [ ] Connect event handlers
- [ ] Implement state management
- [ ] Implement API integration
- [ ] Test full integration

---

## 🧪 Testing Requirements

Each library should be testable independently:
- Create simple HTML test files for each library
- Test API contracts
- Test event emission
- Test edge cases

Test files:
- `tests/browser/test_media_browser_library.html`
- `tests/browser/test_live_preview_library.html`
- `tests/browser/test_standards_library.html`
- `tests/browser/test_preview_draft_library.html`
- `tests/browser/test_column_resizer_library.html`

---

## 📚 Reference Documentation

- **Specification**: `docs/observation-media-complete-specification.md`
  - Section: Standalone Libraries Architecture (lines 1731-2059)
  - Section: Technology Stack (lines 1046-1276)

---

## 🎯 Completion Criteria

Stage 2 is complete when:
- [ ] All 6 library files created
- [ ] All libraries follow ES6 module pattern
- [ ] All libraries have clear APIs
- [ ] All libraries are standalone (no dependencies except documented ones)
- [ ] Event systems working
- [ ] Libraries tested independently
- [ ] Main orchestrator coordinates all libraries
- [ ] Code reviewed and documented

---

## 📝 Notes

- Use ES6 modules (`export`/`import`)
- No external dependencies (jQuery, React, etc.)
- Follow specification API contracts exactly
- Libraries should work independently
- Event-driven architecture for library communication

---

## ✅ Stage 2 Gate

**Ready to proceed to Stage 3** when:
- All checklist items complete
- All libraries independently testable
- Progress tracker updated
- Orchestrator approval received

