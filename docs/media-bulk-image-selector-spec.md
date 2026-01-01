# Media Bulk Image Selector Interface - Specification

## Overview
Create a full-screen modal component for bulk image selection that provides an immersive, Apple Photos-style interface with zoom controls, date/folder grouping, and intuitive selection workflows.

---

## Component Purpose
- **Standalone Component**: Reusable "Media Bulk Image Selector" interface
- **Full-Screen Experience**: Opens in a modal overlay covering the entire viewport
- **Enhanced Navigation**: Large grid view with zoom controls for optimal browsing
- **Better Selection**: Visual feedback for selected images with sequence numbers

---

## User Interface Requirements

### 1. Entry Point
**Trigger:**
- **Icon Button**: Add a "Full Screen Selector" icon (📺 or ⛶ or 🔍) next to "Thumbnails per row" dropdown
- **Location**: In the bulk selection controls bar
- **Behavior**: Clicking opens the full-screen modal

**Visual:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ Mode: [☑] Bulk Selection Mode  [☐] Select All  [5] selected      │
│ Thumbnails per row: [3 ▼]  [📺 Open Full Screen Selector]         │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 2. Full-Screen Modal Component

#### 2.1 Modal Container
**Layout:**
- **Full viewport coverage**: 100vw x 100vh
- **Dark overlay background**: rgba(0, 0, 0, 0.95) or #0a0a0a
- **Z-index**: Highest priority (9999)
- **Animation**: Fade in/out, smooth transition

**Structure:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ ╔═══════════════════════════════════════════════════════════════╗ │
│ ║ [← Back]  Media Selector              [5 selected]  [Reset] ║ │ ← Header Bar (Auto-save enabled)
│ ╟───────────────────────────────────────────────────────────────╢ │
│ ║ ┌─────────────────────────────────────────────────────────┐   ║ │
│ ║ │                                                          │   ║ │
│ ║ │  📁 Root Folder                                         │   ║ │ ← Folder/Date Header
│ ║ │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐     │   ║ │
│ ║ │  │[☑]│ │[☑]│ │[☐]│ │[☐]│ │[☑]│ │[☐]│ │[☐]│     │   ║ │ ← Image Grid
│ ║ │  │[1] │ │[2] │ │    │ │    │ │[3] │ │    │ │    │     │   ║ │
│ ║ │  │IMG │ │IMG │ │IMG │ │IMG │ │IMG │ │IMG │ │IMG │     │   ║ │
│ ║ │  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘     │   ║ │
│ ║ │                                                          │   ║ │
│ ║ │  📁 Subfolder 1                                         │   ║ │ ← Folder Header
│ ║ │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐     │   ║ │
│ ║ │  │[☑]│ │[☐]│ │[☐]│ │[☐]│ │[☐]│ │[☐]│ │[☐]│     │   ║ │
│ ║ │  │[4] │ │    │ │    │ │    │ │    │ │    │ │    │     │   ║ │
│ ║ │  │IMG │ │IMG │ │IMG │ │IMG │ │IMG │ │IMG │ │IMG │     │   ║ │
│ ║ │  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘     │   ║ │
│ ║ │                                                          │   ║ │
│ ║ │  (Scrollable content continues...)                       │   ║ │
│ ║ └─────────────────────────────────────────────────────────┘   ║ │
│ ╟───────────────────────────────────────────────────────────────╢ │
│ ║ [+ Zoom]  [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] [-]  Level 5 ║ │ ← Zoom Controls (Bottom)
│ ╚═══════════════════════════════════════════════════════════╝ │
└─────────────────────────────────────────────────────────────────────┘
```

---

#### 2.2 Header Bar (Top)
**Components:**
```
┌─────────────────────────────────────────────────────────────────┐
│ [← Back/Close]  Media Selector    [5 selected]  [Reset]          │
└─────────────────────────────────────────────────────────────────┘
```

**Elements:**
- **Back/Close Button** (left): Icon ← or ✕, closes modal and returns to main view (selections are auto-saved)
- **Title** (center): "Media Selector" or "Select Images"
- **Selection Counter** (right): Badge showing "X selected"
- **Reset Order Button** (right): Resets sequence to default (auto-saves immediately)
- **Note**: No "Done" button needed - selections are automatically saved in real-time as user makes changes

**Styling:**
- Background: Dark (#1a1a1a)
- Height: 60px
- Fixed position at top
- Border-bottom: 1px solid #333

---

#### 2.3 Toolbar (Below Header)
**Components:**
```
┌─────────────────────────────────────────────────────────────────┐
│ [+ Zoom]  [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] [-] Zoom Out  │
│ [🔍 Search...]  [Filter: All Items ▼]                          │
└─────────────────────────────────────────────────────────────────┘
```

**Zoom Controls:**
- **Zoom In Button** (+): Increases thumbnail size (fewer per row)
- **Zoom Slider**: Horizontal slider for precise zoom control
  - Range: 1-10 (or percentage-based)
  - Position 1 = Most zoomed out (most thumbnails per row, e.g., 6-8)
  - Position 10 = Most zoomed in (fewer thumbnails per row, e.g., 2-3)
  - Current position indicates zoom level
- **Zoom Out Button** (-): Decreases thumbnail size (more per row)

**Zoom Behavior:**
- **Zoom In** (slider right): Larger thumbnails, fewer per row (2-3 per row)
- **Zoom Out** (slider left): Smaller thumbnails, more per row (6-8 per row)
- **Dynamic Layout**: Grid automatically adjusts number of columns based on zoom level
- **Smooth Transition**: Animated resizing when zoom changes

**Search/Filter (Optional - can be moved to header or footer):**
- **Search Bar**: Text input with magnifying glass icon (can be in header if needed)
- **Filter Dropdown**: Filter by folder, date, or file type (can be in header if needed)

**Styling:**
- Background: Dark (#1e1e1e)
- Height: 60px
- Fixed position at bottom of viewport
- Padding: 15px
- Border-top: 1px solid #333

---

#### 2.4 Content Area (Main Grid)
**Layout:**
- **Scrollable**: Vertical scrolling for long lists
- **Folder/Date Headers**: Large headers grouping images
- **Responsive Grid**: Number of columns based on zoom level

**Folder/Date Headers:**
```
┌─────────────────────────────────────────────────────────────────┐
│  📁 Root Folder                          (23 images)            │
└─────────────────────────────────────────────────────────────────┘
```

**Header Styling:**
- Large, prominent (24px font, bold)
- Grey background (#2a2a2a)
- Padding: 20px vertical, 15px horizontal
- Sticky on scroll (optional): Headers stick to top when scrolling

**Image Grid:**
- **Responsive Columns**: 
  - Zoom Level 1 (out): 8 columns
  - Zoom Level 3: 6 columns
  - Zoom Level 5: 4 columns (default)
  - Zoom Level 7: 3 columns
  - Zoom Level 10 (in): 2 columns

**Thumbnail Card:**
```
┌─────────────┐
│ [☑]     [1] │  ← Checkbox (top-left), Sequence (top-right)
│  ┌───────┐  │
│  │       │  │  ← Thumbnail image
│  │ Image │  │
│  │       │  │
│  └───────┘  │
│ filename.jpg│  ← Filename
│  (2.5 MB)   │  ← File size
└─────────────┘
```

**Thumbnail Styling:**
- **Checkbox**: Top-left corner, visible when selected
- **Sequence Number**: Circular badge, top-right (only when selected)
- **Image**: Centered, maintains aspect ratio
- **Filename**: Below thumbnail, centered, truncated if too long
- **File Size**: Below filename, smaller text, grey color
- **Selected State**: Blue border (#667eea), darker background
- **Hover State**: Slight scale-up, border highlight

---

#### 2.5 Footer Bar (Optional)
**Components:**
```
┌─────────────────────────────────────────────────────────────────┐
│ [← Previous]  Page 1 of 3  [Next →]  [Select All] [Clear All]  │
└─────────────────────────────────────────────────────────────────┘
```

**Elements:**
- **Pagination** (if needed): For very large collections
- **Select All**: Checkbox to select all visible images
- **Clear All**: Button to deselect all
- **Actions**: Quick action buttons

---

### 3. Interaction Behaviors

#### 3.1 Opening Modal
1. User clicks "Open Full Screen Selector" icon
2. Modal fades in (300ms animation)
3. Current selection state is loaded from `window.appData.selectedImages`
4. Images load in grid view with current selections displayed
5. Sequence numbers and order are restored from main view state
6. Zoom level initialized to default (Level 5 = 4 columns) or saved preference

#### 3.2 Zoom Controls
**Zoom In (+):**
- Clicking increases zoom level by 1
- Thumbnails get larger
- Fewer images per row
- Smooth animation (200ms transition)

**Zoom Slider:**
- Dragging slider updates zoom level in real-time
- Thumbnail grid adjusts dynamically
- Visual feedback shows current zoom level

**Zoom Out (-):**
- Clicking decreases zoom level by 1
- Thumbnails get smaller
- More images per row
- Smooth animation (200ms transition)

**Zoom Level Mapping:**
```
Level 1:  8 columns (most zoomed out, smallest thumbnails)
Level 2:  7 columns
Level 3:  6 columns
Level 4:  5 columns
Level 5:  4 columns (default)
Level 6:  4 columns (slightly larger)
Level 7:  3 columns
Level 8:  3 columns (larger)
Level 9:  2 columns
Level 10: 2 columns (most zoomed in, largest thumbnails)
```

#### 3.3 Selection & Auto-Save
- **Click Thumbnail**: Toggles selection, **immediately syncs to main view** (`window.appData.selectedImages`)
- **Click Checkbox**: Toggles selection, **immediately syncs to main view** (same behavior)
- **Sequence Numbers**: Auto-assigned based on selection order (1, 2, 3...), **auto-saved immediately**
- **Visual Feedback**: Selected thumbnails show blue border, sequence badge
- **Selection Persists**: When zooming in/out, selections remain
- **Real-time Sync**: Every change automatically updates:
  - `window.appData.selectedImages` (ordered array with sequence numbers)
  - `window.appData.imageOrder` (ordered array of image paths)
  - Main view selection state (visible when modal is closed)
- **No Manual Save**: User can close modal at any time - all changes are already saved

#### 3.4 Auto-Save & Closing Modal
**Auto-Save Behavior:**
- **Real-time Persistence**: Every selection/deselection immediately syncs with main view state
- **No Save Button Needed**: Changes are automatically saved as they happen
- **State Synchronization**: `window.appData.selectedImages` is updated in real-time when:
  - An image is selected/deselected
  - Sequence numbers change
  - Order is reset
  - "Select All" / "Clear All" is used

**Closing Modal Options:**
1. **Back/Close Button**: Closes modal and returns to main view (selections already saved)
2. **Escape Key**: Closes modal (selections already saved)
3. **Click Outside Modal** (optional): Closes modal (selections already saved)

**Behavior:**
- Modal fades out (300ms animation)
- Returns to main view
- Selected images remain selected (already persisted)
- Sequence numbers preserved (already persisted)
- Main view immediately reflects all changes made in modal

---

### 4. Technical Implementation

#### 4.1 Component Structure
**Component Name:** `MediaBulkImageSelector`

**Files:**
- `static/js/media-bulk-image-selector.js` - Main component logic
- `static/css/media-bulk-image-selector.css` - Styles for modal
- Integration in `templates/image_to_pdf.html`

#### 4.2 State Management
**Global State:**
```javascript
window.mediaSelector = {
    isOpen: false,
    zoomLevel: 5,           // 1-10, default 5
    columns: 4,             // Calculated from zoom level
    availableImages: []     // All images to display
}

// Note: selectedImages and imageOrder are NOT stored here
// They are stored in window.appData and synced in real-time:
// - window.appData.selectedImages: Array of {path, name, folder, sequence}
// - window.appData.imageOrder: Array of image paths (ordered)
```

**Real-time Sync Functions:**
```javascript
// Called immediately when selection changes
function syncSelectionToMainView() {
    // Update window.appData.selectedImages with current selections
    // Update window.appData.imageOrder with current order
    // Main view automatically reflects changes (no page refresh needed)
}

// Called when image is selected/deselected
function onImageSelectionChange(imagePath, isSelected) {
    if (isSelected) {
        // Add to window.appData.selectedImages with sequence number
        // Update sequence numbers for all selected images
    } else {
        // Remove from window.appData.selectedImages
        // Renumber remaining images
    }
    syncSelectionToMainView(); // Immediate sync
}
```

#### 4.3 Zoom Calculation
**Function:**
```javascript
function calculateColumnsFromZoom(zoomLevel) {
    // zoomLevel: 1-10
    const columnMap = {
        1: 8, 2: 7, 3: 6, 4: 5, 5: 4,
        6: 4, 7: 3, 8: 3, 9: 2, 10: 2
    };
    return columnMap[zoomLevel] || 4;
}

function updateZoom(level) {
    window.mediaSelector.zoomLevel = level;
    window.mediaSelector.columns = calculateColumnsFromZoom(level);
    renderImageGrid(); // Re-render with new column count
}
```

#### 4.4 Grid Rendering
**Dynamic Width:**
- Width per thumbnail: `calc(100% / columns - gap)`
- Gap between thumbnails: 16px
- Responsive: Adjusts on window resize

---

### 5. Questions for Approval

**Question 1**: Should the modal remember zoom level when reopened?
- **Recommended**: Yes, store zoom preference in localStorage

**Question 2**: Should folder headers be collapsible/expandable?
- **Recommended**: Yes, for better navigation in large collections

**Question 3**: Should we support keyboard shortcuts?
- **Recommended**: Yes - Escape to close, Space to select, Arrow keys to navigate

**Question 4**: Should there be a "Select All Visible" vs "Select All" distinction?
- **Recommended**: Yes - "Select All Visible" selects only images currently on screen, "Select All" selects entire collection

**Question 5**: Should we add date-based grouping (like Apple Photos)?
- **Recommended**: Yes, group images by date taken (if metadata available) in addition to folder structure

**Question 6**: Should the modal support multi-select via Shift+Click or Ctrl+Click?
- **Recommended**: Yes - Shift+Click for range selection, Ctrl/Cmd+Click for individual toggles

**Question 7**: Should search/filter be implemented in initial version?
- **Recommended**: Defer to later version, focus on zoom and selection first

**Question 8**: Should thumbnails show loading placeholders while images load?
- **Recommended**: Yes, show skeleton loaders for better UX

---

### 6. Wireframes (Text-Based)

#### 6.1 Modal - Zoomed Out View (Level 1, 8 columns)
```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [←] Media Selector                    [5 selected] [Reset]                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ 📁 Root Folder                                              (23 images)     │
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                   │
│ │[☑]│ │[☑]│ │[☐]│ │[☐]│ │[☑]│ │[☐]│ │[☐]│ │[☐]│                   │
│ │[1] │ │[2] │ │    │ │    │ │[3] │ │    │ │    │ │    │                   │
│ │img │ │img │ │img │ │img │ │img │ │img │ │img │ │img │                   │
│ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘                   │
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                   │
│ │[☑]│ │[☐]│ │[☐]│ │[☐]│ │[☐]│ │[☐]│ │[☐]│ │[☐]│                   │
│ │[4] │ │    │ │    │ │    │ │    │ │    │ │    │ │    │                   │
│ │img │ │img │ │img │ │img │ │img │ │img │ │img │ │img │                   │
│ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘                   │
│                                                                              │
│ 📁 Subfolder 1                                            (15 images)       │
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                   │
│ │[☑]│ │[☐]│ │[☐]│ │[☐]│ │[☐]│ │[☐]│ │[☐]│ │[☐]│                   │
│ │[5] │ │    │ │    │ │    │ │    │ │    │ │    │ │    │                   │
│ │img │ │img │ │img │ │img │ │img │ │img │ │img │ │img │                   │
│ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘                   │
│                                                                              │
│ (Scrollable...)                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ [+ Zoom] [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] [-]    │
│ Level 5 (4 per row)                                                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 6.2 Modal - Default View (Level 5, 4 columns)
```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [←] Media Selector                    [5 selected] [Reset]                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ 📁 Root Folder                                              (23 images)     │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│ │ [☑]    [1] │ │ [☑]    [2] │ │ [☐]        │ │ [☐]        │               │
│ │  ┌──────┐  │ │  ┌──────┐  │ │  ┌──────┐  │ │  ┌──────┐  │               │
│ │  │      │  │ │  │      │  │ │  │      │  │ │  │      │  │               │
│ │  │ img  │  │ │  │ img  │  │ │  │ img  │  │ │  │ img  │  │               │
│ │  │      │  │ │  │      │  │ │  │      │  │ │  │      │  │               │
│ │  └──────┘  │ │  └──────┘  │ │  └──────┘  │ │  └──────┘  │               │
│ │ filename   │ │ filename   │ │ filename   │ │ filename   │               │
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘               │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│ │ [☑]    [3] │ │ [☐]        │ │ [☐]        │ │ [☐]        │               │
│ │  ┌──────┐  │ │  ┌──────┐  │ │  ┌──────┐  │ │  ┌──────┐  │               │
│ │  │      │  │ │  │      │  │ │  │      │  │ │  │      │  │               │
│ │  │ img  │  │ │  │ img  │  │ │  │ img  │  │ │  │ img  │  │               │
│ │  │      │  │ │  │      │  │ │  │      │  │ │  │      │  │               │
│ │  └──────┘  │ │  └──────┘  │ │  └──────┘  │ │  └──────┘  │               │
│ │ filename   │ │ filename   │ │ filename   │ │ filename   │               │
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘               │
│                                                                              │
│ 📁 Subfolder 1                                            (15 images)       │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│ │ [☑]    [4] │ │ [☐]        │ │ [☐]        │ │ [☐]        │               │
│ │  ┌──────┐  │ │  ┌──────┐  │ │  ┌──────┐  │ │  ┌──────┐  │               │
│ │  │      │  │ │  │      │  │ │  │      │  │ │  │      │  │               │
│ │  │ img  │  │ │  │ img  │  │ │  │ img  │  │ │  │ img  │  │               │
│ │  │      │  │ │  │      │  │ │  │      │  │ │  │      │  │               │
│ │  └──────┘  │ │  └──────┘  │ │  └──────┘  │ │  └──────┘  │               │
│ │ filename   │ │ filename   │ │ filename   │ │ filename   │               │
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘               │
│                                                                              │
│ (Scrollable...)                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ [+ Zoom] [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] [-]    │
│ Level 10 (2 per row)                                                         │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 6.3 Modal - Zoomed In View (Level 10, 2 columns)
```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [←] Media Selector                    [5 selected] [Reset]                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ 📁 Root Folder                                              (23 images)     │
│ ┌──────────────────────┐ ┌──────────────────────┐                          │
│ │    [☑]          [1]  │ │    [☑]          [2]  │                          │
│ │     ┌──────────────┐ │ │     ┌──────────────┐ │                          │
│ │     │              │ │ │     │              │ │                          │
│ │     │              │ │ │     │              │ │                          │
│ │     │   Large      │ │ │     │   Large      │ │                          │
│ │     │   Thumbnail  │ │ │     │   Thumbnail  │ │                          │
│ │     │              │ │ │     │              │ │                          │
│ │     │              │ │ │     │              │ │                          │
│ │     └──────────────┘ │ │     └──────────────┘ │                          │
│ │   filename.jpg       │ │   filename.jpg       │                          │
│ │   (2.5 MB)           │ │   (3.2 MB)           │                          │
│ └──────────────────────┘ └──────────────────────┘                          │
│ ┌──────────────────────┐ ┌──────────────────────┐                          │
│ │    [☑]          [3]  │ │    [☐]               │                          │
│ │     ┌──────────────┐ │ │     ┌──────────────┐ │                          │
│ │     │              │ │ │     │              │ │                          │
│ │     │   Large      │ │ │     │   Large      │ │                          │
│ │     │   Thumbnail  │ │ │     │   Thumbnail  │ │                          │
│ │     │              │ │ │     │              │ │                          │
│ │     └──────────────┘ │ │     └──────────────┘ │                          │
│ │   filename.jpg       │ │   filename.jpg       │                          │
│ └──────────────────────┘ └──────────────────────┘                          │
│                                                                              │
│ (Scrollable...)                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ [+ Zoom] [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] [-]    │
│ Level 1 (8 per row)                                                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### 7. Implementation Stages

#### Stage 1: Basic Modal
- [ ] Create modal container with overlay
- [ ] Add header bar with close button (auto-save, no done button needed)
- [ ] Implement open/close functionality
- [ ] Sync state with main view

#### Stage 2: Grid Layout
- [ ] Create responsive grid system
- [ ] Implement folder/date headers
- [ ] Render thumbnails with checkboxes
- [ ] Add sequence number badges

#### Stage 3: Zoom Controls
- [ ] Add zoom slider and +/- buttons
- [ ] Implement zoom level calculation
- [ ] Dynamic column adjustment
- [ ] Smooth animations

#### Stage 4: Selection & Sequence
- [ ] Toggle selection on click
- [ ] Auto-assign sequence numbers
- [ ] Visual feedback for selected items
- [ ] Sync selections with main view

#### Stage 5: Polish & Enhancements
- [ ] Keyboard shortcuts
- [ ] Loading states
- [ ] Smooth scrolling
- [ ] Performance optimization

---

## Approval Required

Please review this specification and provide feedback on:
1. Zoom level ranges (1-10, or different scale?)
2. Column mapping (8 cols max, or more?)
3. Optional features (search, filters, keyboard shortcuts)
4. Styling preferences
5. Animation preferences

