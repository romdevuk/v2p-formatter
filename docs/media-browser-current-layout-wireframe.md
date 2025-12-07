# Media Browser - Current Layout Text Wireframe

## Overview
This wireframe represents the current state of the media browser as it appears in the Observation Media page. The browser displays folders in a compact, collapsible list format.

---

## Layout Structure

### Container: Media Browser (Left Panel)
- **Position**: Left side of page (50% width when not expanded)
- **Background**: Dark gray (#2a2a2a)
- **Border**: 1px solid #555
- **Border Radius**: 6px
- **Padding**: 15px
- **Height**: Independent, full viewport height
- **Overflow**: Vertical scrolling enabled

---

## Header Section

### Media Browser Header
```
┌─────────────────────────────────────────────────┐
│ [119 files]          [⚙️ Settings] [⬜ Expand]  │
│                      [☐ Bulk Select]            │
└─────────────────────────────────────────────────┘
```

**Elements:**
- **File Count** (left): "119 files" - Total count of all media files
- **Settings Button** (right): Gear icon (⚙️) - Opens media browser settings
- **Expand Button** (right): Square icon (⬜) - Expands/collapses media browser
- **Bulk Select** (right): Checkbox (☐) - Enables bulk selection mode

**Styling:**
- Font size: 12px
- Color: #999 (gray text)
- Buttons: Small, compact, dark background

---

## Folder List Section

### Folder Entry Structure
Each folder is displayed as a single-line entry with the following structure:

```
┌─────────────────────────────────────────────────────┐
│ ▶ 📁 visit2                              (30 files) │
└─────────────────────────────────────────────────────┘
```

**Components per folder:**
1. **Collapse/Expand Icon**: ▶ (blue, right-pointing triangle when collapsed)
2. **Folder Icon**: 📁 (light gray folder icon)
3. **Folder Path/Name**: Full path or folder name (white text)
4. **File Count**: Number in parentheses, e.g., "(30 files)" (gray text, right-aligned)

**Visual Design:**
- **Background**: #1e1e1e (dark gray)
- **Border**: 1px solid #555
- **Border Left**: 2px solid #667eea (blue accent)
- **Border Radius**: 3px
- **Padding**: 4px 8px (compact, single-line)
- **Margin Bottom**: 2px between folders
- **Height**: Auto (single line, ~24-28px)
- **Hover Effect**: Background changes to #2a2a2a

---

## Folder Entry Examples

### Example 1: Root Folder
```
┌─────────────────────────────────────────────────────┐
│ ▶ 📁 visit2                              (30 files) │
└─────────────────────────────────────────────────────┘
```

### Example 2: Nested Folder
```
┌─────────────────────────────────────────────────────┐
│ ▶ 📁 visit2/post                        (32 files) │
└─────────────────────────────────────────────────────┘
```

### Example 3: Deeply Nested Folder
```
┌─────────────────────────────────────────────────────┐
│ ▶ 📁 visit2/tasks/drylining             (20 files) │
└─────────────────────────────────────────────────────┘
```

### Example 4: Another Nested Folder
```
┌─────────────────────────────────────────────────────┐
│ ▶ 📁 visit2/tasks/mp3                    (13 files) │
└─────────────────────────────────────────────────────┘
```

### Example 5: Another Nested Folder
```
┌─────────────────────────────────────────────────────┐
│ ▶ 📁 visit2/tasks/plasterboard           (24 files) │
└─────────────────────────────────────────────────────┘
```

---

## Expanded Folder State

When a folder is clicked/expanded:

### Expanded Header
```
┌─────────────────────────────────────────────────────┐
│ ▼ 📁 visit2                              (30 files) │
└─────────────────────────────────────────────────────┘
```

**Changes:**
- Icon changes from ▶ to ▼ (downward-pointing triangle)
- Border bottom appears (1px solid #555)
- Border radius changes to 3px 3px 0 0 (rounded top only)

### Expanded Content Area
```
┌─────────────────────────────────────────────────────┐
│ ▼ 📁 visit2                              (30 files) │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Media Grid - Thumbnails displayed here]          │
│  - Grid layout (columns set by settings)           │
│  - Media cards with thumbnails                     │
│  - Drag-and-drop enabled                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Content Area:**
- **Display**: Grid layout
- **Padding**: 10px
- **Gap**: 15px between items
- **Grid Columns**: Dynamic (set by user settings: 2, 3, 4, 5, or 6 columns)
- **Media Cards**: Thumbnails with file names and sizes

---

## Collapsed Folder State

When a folder is collapsed:

```
┌─────────────────────────────────────────────────────┐
│ ▶ 📁 visit2                              (30 files) │
└─────────────────────────────────────────────────────┘
```

**Characteristics:**
- Icon: ▶ (right-pointing triangle)
- No border bottom
- Full border radius: 3px (all corners rounded)
- Content area: Completely hidden (display: none, height: 0)
- **Height**: Only header height (~24-28px) - no extra space

---

## Behavior

### Click Interaction
- **Click on folder header**: Toggles expand/collapse state
- **Icon rotation**: ▶ ↔ ▼
- **Smooth transition**: 0.2s background color change on hover

### Expand/Collapse Animation
- **Expand**: Content slides down (if animation enabled)
- **Collapse**: Content hides immediately (display: none)
- **No height reserved**: Collapsed folders take minimal space

### Scrolling
- **Container**: Scrollable when content exceeds viewport
- **Scrollbar**: Custom styled (thin, dark theme)
- **Independent scrolling**: Media browser scrolls independently from Live Preview

---

## Spacing and Layout

### Vertical Spacing
- **Between folders**: 2px margin-bottom
- **Header padding**: 4px top/bottom, 8px left/right
- **Content padding**: 10px (when expanded)

### Horizontal Layout
- **Icons**: 6px gap between elements
- **Folder name**: Flexible width (flex: 1)
- **File count**: Right-aligned, fixed position

---

## Color Scheme

### Text Colors
- **Folder name**: #e0e0e0 (white/light gray)
- **File count**: #999 (medium gray)
- **Icons**: #667eea (blue accent)

### Background Colors
- **Container**: #2a2a2a (dark gray)
- **Folder header**: #1e1e1e (darker gray)
- **Folder header (hover)**: #2a2a2a (lighter gray)

### Border Colors
- **Container border**: #555 (medium gray)
- **Folder border**: #555 (medium gray)
- **Folder accent**: #667eea (blue, left border)

---

## Responsive Behavior

### Default State (50% width)
- Media browser takes 50% of container width
- Live Preview takes remaining 50%
- Both scroll independently

### Expanded State (100% width)
- Media browser expands to 100% width
- Live Preview hidden
- Full focus on media selection

---

## Requirements (FIXED - ✅ Verified)

### 1. Height When Collapsed (✅ FIXED)
**Requirement**: 
- Collapsed folders show ONLY the header line
- No extra height below the header
- Header is compact (~24px total height)
- Zero content area height when collapsed

**Implementation**:
- `.media-subfolder-section.collapsed`: Uses `display: block`, `height: auto`
- Content area: `display: none !important`, `height: 0 !important`, `line-height: 0`, `font-size: 0`
- **Result**: Collapsed folders are ~24px (header height only) ✅

### 2. Overlap When Expanded (✅ FIXED)
**Requirement**:
- Expanded folders push other folders down (no overlap)
- Each folder section is a proper block element
- Content area contained within section boundaries
- Proper spacing (2px) between folders

**Implementation**:
- Parent container `#observationMediaGrid`: Changed from `display: grid` to `display: block`
- Folder sections: `display: block`, `width: 100%`, `position: relative`, `clear: both`
- Removed `grid-column: 1 / -1` that was causing overlap
- **Result**: Folders stack vertically with 2px spacing, no overlap ✅

### 3. Layout Structure (✅ IMPLEMENTED)
- Folders are in a vertical list (block elements, not grid items)
- Each folder section is a block-level element
- Expanded content flows naturally below the header
- Collapsed content is completely hidden (display: none, height: 0)

---

## Solution Implemented

### CSS Changes Applied:
1. ✅ **Parent container**: Changed `#observationMediaGrid` from `display: grid` to `display: block`
2. ✅ **Folder sections**: Changed from grid items to block elements (`display: block`, `width: 100%`)
3. ✅ **Height management**: 
   - Collapsed: height = header height only (~24px)
   - Expanded: height = header + content (auto)
4. ✅ **No absolute positioning**: All folders in normal document flow

### JavaScript Changes Applied:
1. ✅ **Display management**: 
   - Collapsed: `content.style.display = 'none'`, `visibility: 'hidden'`, `height: '0'`
   - Expanded: `content.style.display = 'grid'`, `visibility: 'visible'`, `height: 'auto'`
2. ✅ **Height reset**: Ensures `height: 0`, `minHeight: 0`, `maxHeight: 0` when collapsed
3. ✅ **No overlap**: Content is within section boundaries, sections stack vertically

---

## Test Results (✅ VERIFIED)

### Height Test:
- ✅ Collapsed folder height: 24.4px (header: 22.4px) - **ACCEPTABLE**
- ✅ Content not visible when collapsed
- ✅ All 5 collapsed folders have proper minimal height

### Overlap Test:
- ✅ No overlap detected when first folder expanded
- ✅ Proper spacing: 2.0px between folders
- ✅ Multiple expanded folders: No overlap
- ✅ All folders properly spaced in vertical list

### Screenshots:
- ✅ `folder_test_1_all_collapsed.png` - All folders collapsed, minimal height
- ✅ `folder_test_2_first_expanded.png` - First folder expanded, no overlap
- ✅ `folder_test_3_two_expanded.png` - Two folders expanded, proper spacing

---

## Approval Notes

This wireframe represents the **current state** of the media browser. Please review and approve before implementing any changes or improvements.

**Key Features:**
- ✅ Compact single-line folder entries
- ✅ Clear visual hierarchy with icons and colors
- ✅ File count displayed for each folder
- ✅ Expand/collapse functionality
- ⚠️ Height issues when collapsed (to be fixed)
- ⚠️ Overlap issues when expanded (to be fixed)

