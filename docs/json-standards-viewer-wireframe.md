# JSON Standards Viewer - Wireframe Specification (UPDATED)

## Overview
Add a third column "Standards" next to the Live Preview section in the observation-media page. This creates a three-column resizable layout: **Media Browser | Live Preview | Standards**. The Standards column displays the JSON Standards File content associated with the current draft, organized by unit, with color-coded ACs (Assessment Criteria).

## Layout Structure

### Three-Column Resizable Layout
```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Observation Media Page                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ┌───────────────┐ │ ┌───────────────┐ │ ┌───────────────┐                │
│ │ Media Browser │ │ │ Live Preview  │ │ │ Standards     │                │
│ │               │ │ │               │ │ │               │                │
│ │ [Header]      │ │ │ [Header]      │ │ │ [Header]      │                │
│ │               │ │ │               │ │ │               │                │
│ │ [Content]     │ │ │ [Content]     │ │ │ [Content]     │                │
│ │               │ │ │               │ │ │               │                │
│ │               │ │ │               │ │ │               │                │
│ └───────────────┘ │ └───────────────┘ │ └───────────────┘                │
│       ↕           │       ↕           │                                    │
│   Resizable       │   Resizable       │                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Column Structure
- **Column 1**: Media Browser (existing)
- **Column 2**: Live Preview (existing)
- **Column 3**: Standards (NEW)
- **Resizers**: Vertical dividers between columns that can be dragged to resize
- **Default Widths**: Equal distribution (33.33% each) or configurable defaults

## Standards Column Structure

### Header Section
```
┌─────────────────────────────────────────────────────────┐
│ Standards                                    [Expand All]│
│                                          [Collapse All]  │
└─────────────────────────────────────────────────────────┘
```

**Header Components:**
- **Title**: "Standards"
- **Controls**:
  - "Expand All" button (expands all collapsed units)
  - "Collapse All" button (collapses all units)
- **Style**: Match existing Live Preview header style

### Content Section (Scrollable - Vertical)
```
┌─────────────────────────────────────────────────────────┐
│ ▶ Unit 641: Conforming to General Health, Safety...     │
│                                                          │
│ ▶ Unit 642: Installing Interior Systems                  │
│                                                          │
│ ▼ Unit 643: [Expanded Unit Example]                     │
│   ┌───────────────────────────────────────────────────┐ │
│   │ 1.1. Explain the main health and safety...         │ │
│   │ 1.2. Identify the main health and safety...         │ │
│   │ 2.1. Carry out risk assessments...                  │ │
│   │ 2.2. Implement control measures...                  │ │
│   └───────────────────────────────────────────────────┘ │
│                                                          │
│ ▶ Unit 644: Another Unit Name                           │
│                                                          │
│ [Scrollable content - vertical scrolling enabled]        │
└─────────────────────────────────────────────────────────┘
```

## Unit Display Format

### Unit Header (Collapsed by Default)
- **Format**: `▶ Unit {unit_id}: {unit_name}`
- **Collapsed Icon**: ▶
- **Expanded Icon**: ▼
- **Style**:
  - Background: #2a2a2a
  - Border: 1px solid #444
  - Padding: 12px 15px
  - Margin-bottom: 8px
  - Border-radius: 4px
  - Cursor: pointer
  - Border-left: 4px solid [unit color]
- **Click Behavior**: Toggles expand/collapse of unit content

### Unit Content (Shown when Expanded)
- **ACs**: Displayed directly under unit (NO Learning Outcomes displayed)
- **Format**: `{ac_id}. {ac_text}` (no "AC" prefix, no "Description:" label)

### AC Display Format
- **Format**: `{ac_id}. {ac_text}` (NO "AC" prefix)
- **NO "Description:" label** - just AC ID followed by text
- **Example**: `1.1. Explain the main health and safety responsibilities of employers and employees in the workplace, including...`
- **Style**:
  - Background: #1a1a1a
  - Border: 1px solid #333
  - Border-left: 3px solid [AC type color]
  - Padding: 10px 12px
  - Margin: 6px 0
  - Border-radius: 3px
- **AC ID**: Bold, color: #667eea
- **AC Text**: #e0e0e0

## Styling (No Color Coding)

### Visual Hierarchy
- **Unit Border**: 1px solid #444 (no color coding)
- **AC Border**: 1px solid #333 (no color coding)
- All units and ACs use consistent gray borders

## Resizable Columns

### Resizer Implementation
- **Location**: Between each column pair
- **Width**: 4px
- **Background**: #444 (visible divider) or transparent (invisible handle)
- **Cursor**: `col-resize` when hovering
- **Visual Feedback**: Show resize indicator line when dragging

### Resize Behavior
- **Drag to Resize**: Click and drag resizer to adjust column widths
- **Minimum Width**: Each column has a minimum width (e.g., 200px or 15%)
- **Maximum Width**: Each column has a maximum width (e.g., 60%)
- **Persistence**: Save column widths to localStorage
- **Snap Points**: Optional snap-to-grid or equal-width button

### Default Widths
- **Option 1**: Equal distribution (33.33% each)
- **Option 2**: Media Browser: 30%, Live Preview: 40%, Standards: 30%
- **Option 3**: User-configurable defaults

## Data Loading

### JSON File Association
- **Source**: Load JSON file from draft's `json_file_id`
- **If No Draft**: Show empty state message: "No draft loaded. Load a draft to view standards."
- **If Draft Has No JSON File**: Show message: "No JSON Standards File assigned to this draft."
- **Loading State**: Show loading spinner/message while fetching JSON file

### API Endpoint
- **Endpoint**: `/v2p-formatter/ac-matrix/json-files/{file_id}`
- **Method**: GET
- **Response**: Full JSON standards file structure

### Auto-Refresh
- **On Draft Load**: Automatically load associated JSON file
- **On Draft Clear**: Clear standards content
- **On Draft Update**: Reload JSON file if `json_file_id` changed

## Expand/Collapse Controls

### Expand All Button
- **Action**: Expands all collapsed units
- **State**: Changes to "Collapse All" when all units are expanded
- **Style**: Match existing button styles

### Collapse All Button
- **Action**: Collapses all expanded units
- **State**: Changes to "Expand All" when all units are collapsed
- **Style**: Match existing button styles

### Individual Unit Toggle
- **Click Unit Header**: Toggles that unit's expanded/collapsed state
- **Icon Update**: Changes from ▶ to ▼ when expanded

## Empty States

### No Draft Loaded
```
┌─────────────────────────────────────────────────────────┐
│ Standards                                                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   No draft loaded. Load a draft to view standards.      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### No JSON File Assigned
```
┌─────────────────────────────────────────────────────────┐
│ Standards                                                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   No JSON Standards File assigned to this draft.        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Loading State
```
┌─────────────────────────────────────────────────────────┐
│ Standards                                                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Loading standards...                                  │
│   [Spinner]                                             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Styling Details

### Column Container
- **Display**: Flexbox or CSS Grid
- **Height**: 100% of available viewport height
- **Background**: #1e1e1e (dark theme)
- **Gap**: 0px (resizers provide spacing)

### Standards Column
- **Background**: #1e1e1e
- **Border**: 1px solid #555 (right border only, or match other columns)
- **Overflow**: Hidden (header fixed, content scrollable)

### Header
- **Background**: #2a2a2a
- **Border-bottom**: 1px solid #555
- **Padding**: 12px 15px
- **Display**: Flex, justify-content: space-between

### Content Area
- **Height**: calc(100% - header height)
- **Overflow-y**: Auto
- **Padding**: 15px
- **Background**: #1e1e1e

### Unit Sections
- **Default State**: Collapsed
- **Spacing**: 8px margin-bottom between units
- **Hover Effect**: Slight background color change on hover

### AC Cards
- **Font Size**: 14px
- **Line Height**: 1.5
- **Word Wrap**: Break long text
- **Hover Effect**: Slight border color change

## Responsive Behavior

### Minimum Column Widths
- **Media Browser**: 200px minimum
- **Live Preview**: 250px minimum
- **Standards**: 250px minimum

### Mobile/Tablet
- **Breakpoint**: Below 1200px width
- **Behavior**: Stack columns vertically or hide Standards column
- **Alternative**: Toggle Standards column visibility

## Implementation Notes

### Resizable Columns Library
- **Option 1**: Custom JavaScript implementation with mouse events
- **Option 2**: Use existing library (e.g., Split.js, react-resizable-panels)
- **Option 3**: CSS Grid with resize handles

### State Management
- **Column Widths**: Store in localStorage
- **Unit Expanded State**: Store in localStorage (optional)
- **Current JSON File**: Track in JavaScript state

### Performance
- **Lazy Rendering**: Only render expanded units
- **Virtual Scrolling**: For large numbers of ACs (if needed)
- **Debounce Resize**: Debounce resize events for smooth performance

## Data Structure

### JSON File Structure (from API)
```json
{
  "qualifications": [
    {
      "qualification_name": "...",
      "units": [
        {
          "unit_id": "641",
          "unit_name": "Conforming to General Health, Safety...",
          "learning_outcomes": [
            {
              "learning_outcome_number": "1",
              "learning_outcome_name": "Understand health and safety...",
              "questions": [
                {
                  "question_id": "1.1",
                  "question_name": "Explain the main health...",
                  "question_type": "Practical"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### Rendering Logic
1. Extract units from JSON structure
2. For each unit:
   - Create unit header (collapsed by default)
   - On expand, render ACs directly (skip Learning Outcomes)
   - Extract all ACs from all learning outcomes within the unit
   - Format: `AC {question_id}. {question_name}`

## Summary of Changes from Original Wireframe

1. **Layout**: Changed from modal to third column
2. **Resizable**: Added resizable column functionality (horizontal resizing)
3. **Vertical Scrolling**: Content areas scroll vertically
4. **No JSON Selector**: Only shows JSON from draft (no dropdown)
5. **AC Format**: Changed from "Description: ..." to "AC ID. Text"
6. **Default State**: Units collapsed by default
7. **Expand/Collapse**: Added expand/collapse all controls
8. **No Learning Outcomes**: Removed Learning Outcomes - ACs displayed directly under units

## Approved Specifications

### Answers to Clarification Questions:
1. **Learning Outcomes**: ❌ NO Learning Outcomes needed - ACs displayed directly under units
2. **Column Default Widths**: ✅ Equal distribution (33.33% each)
3. **Resizer Visibility**: ✅ Visible dividers
4. **Unit Color Assignment**: ✅ Consistent colors based on unit_id
5. **AC Text**: ✅ Full text shown (no truncation)

### Key Features:
- ✅ **Horizontal Resizing**: Columns can be resized by dragging dividers
- ✅ **Vertical Scrolling**: Content areas scroll vertically when content exceeds viewport
- ✅ **No Learning Outcomes**: ACs displayed directly under units (no LO grouping)
- ✅ **AC Format**: `{id}. {text}` (no "AC" prefix, no "Description:" label)
- ✅ **Units Collapsed by Default**: All units start collapsed
- ✅ **Expand/Collapse All**: Buttons in header to control all units
- ✅ **No Color Coding**: All units and ACs use consistent gray styling
- ✅ **Auto-load**: Standards load automatically when draft with JSON file is loaded

---

**Status**: ✅ **APPROVED FOR DEVELOPMENT**

**Approval Date**: 2025-01-XX  
**Implementation**: Complete  
**Testing**: Ready for user testing
