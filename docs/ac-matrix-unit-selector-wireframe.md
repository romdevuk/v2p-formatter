# AC Matrix - Unit Selector Feature Wireframe

## Overview
Add ability to filter which units from the selected JSON standards file are included in the matrix analysis. This allows users to focus on specific units rather than analyzing all units at once.

## UI Layout

### Settings Panel (Updated)
```
┌─────────────────────────────────────────────────────────────────┐
│ Settings                                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│ JSON Standards File: [Dropdown ▼] [Add New File] [Delete File]  │
│                                                                   │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Filter Units (Optional)                                       │ │
│ │ ☐ Show only selected units                                    │ │
│ │                                                               │ │
│ │ [Select All] [Deselect All]                                  │ │
│ │                                                               │ │
│ │ ┌─────────────────────────────────────────────────────────┐ │ │
│ │ │ Unit Selection (scrollable if many units)                │ │ │
│ │ │                                                           │ │ │
│ │ │ ☑ Unit 129v4: Installing Internal Systems               │ │ │
│ │ │ ☑ Unit 130v3: Installing Internal Systems               │ │ │
│ │ │ ☐ Unit 641: Installing Internal Systems                  │ │ │
│ │ │ ☐ Unit 642: Installing Internal Systems                  │ │ │
│ │ │ ☑ Unit 643: Installing Internal Systems                  │ │ │
│ │ │ ...                                                       │ │ │
│ │ │                                                           │ │ │
│ │ └─────────────────────────────────────────────────────────┘ │ │
│ │                                                               │ │
│ │ Selected: 3 of 5 units                                        │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Component Specifications

### 1. Filter Units Toggle
- **Location**: Below JSON file selector, within Settings Panel
- **Label**: "Filter Units (Optional)"
- **Checkbox**: "Show only selected units"
  - **Default State**: Unchecked (all units included)
  - **When Checked**: Only selected units are included in analysis
  - **When Unchecked**: All units from JSON file are included (default behavior)

### 2. Unit Selection Container
- **Visibility**: 
  - Hidden by default
  - Shown when "Show only selected units" is checked
  - Also shown when JSON file is selected (even if filter is off) - shows all units with checkboxes disabled
- **Header**: "Unit Selection"
- **Max Height**: 300px with vertical scroll
- **Background**: Dark theme (#1e1e1e)
- **Border**: 1px solid #555
- **Border Radius**: 6px
- **Padding**: 15px

### 3. Unit Checkbox List
- **Format**: Each unit as a checkbox with label
- **Label Format**: `Unit {unit_id}: {unit_name}`
  - Example: `Unit 129v4: Installing Internal Systems`
- **Checkbox Style**: 
  - Standard checkbox input
  - Color: #667eea when checked
  - Spacing: 8px between checkbox and label
- **Layout**: Vertical list, one unit per line
- **Padding**: 8px per item
- **Hover Effect**: Background changes to #2a2a2a on hover

### 4. Select All / Deselect All Buttons
- **Location**: Above unit checkbox list
- **Layout**: Horizontal, side by side
- **Button Style**: 
  - Same as existing secondary buttons (#555 background)
  - Padding: 6px 12px
  - Font size: 12px
- **Behavior**:
  - **Select All**: Checks all visible units
  - **Deselect All**: Unchecks all units
  - Only affects units in the current JSON file

### 5. Selection Counter
- **Location**: Below unit checkbox list
- **Format**: "Selected: X of Y units"
- **Style**: 
  - Color: #999 (muted)
  - Font size: 0.9em
  - Updates dynamically as user selects/deselects

## Behavior and Interactions

### Initial State
1. User selects JSON standards file
2. System loads all units from JSON file
3. Unit selection container appears (but filter is OFF by default)
4. All units are visible but checkboxes are disabled (grayed out)
5. "Show only selected units" checkbox is unchecked

### When "Show only selected units" is Checked
1. Unit checkboxes become enabled
2. All units are checked by default (to maintain current behavior)
3. User can uncheck units to exclude them
4. Selection counter updates: "Selected: X of Y units"
5. When "Analyze Report" is clicked, only checked units are included

### When "Show only selected units" is Unchecked
1. Unit checkboxes become disabled (grayed out)
2. All units are included in analysis (default behavior)
3. Selection counter shows: "Selected: All units"

### Select All / Deselect All
- **Select All**: 
  - Checks all units in the list
  - Updates selection counter
- **Deselect All**: 
  - Unchecks all units
  - Updates selection counter
  - Warning: If all units are deselected, show warning when analyzing

### Analysis Behavior
- When "Analyze Report" is clicked:
  - If filter is OFF: Analyze all units (current behavior)
  - If filter is ON: Only analyze checked units
  - If filter is ON but no units checked: Show error "Please select at least one unit"

### JSON File Change
- When user changes JSON file:
  - Unit list updates to show new file's units
  - Filter checkbox resets to unchecked
  - All units from new file are shown

## Visual Design

### Colors (Dark Theme)
- **Container Background**: #1e1e1e
- **Border**: #555
- **Text**: #e0e0e0
- **Muted Text**: #999
- **Checkbox Checked**: #667eea
- **Hover Background**: #2a2a2a
- **Button Background**: #555
- **Button Hover**: #666

### Spacing
- **Container Padding**: 15px
- **Item Padding**: 8px
- **Button Spacing**: 10px between buttons
- **Section Margin**: 15px below JSON selector

### Typography
- **Section Header**: 1.2em, #667eea
- **Unit Labels**: 14px, #e0e0e0
- **Counter Text**: 12px, #999
- **Button Text**: 12px, white

## Responsive Behavior

### Desktop (>768px)
- Full width unit selection container
- Buttons side by side
- Max height 300px with scroll

### Tablet/Mobile (<768px)
- Unit selection container full width
- Buttons stack vertically
- Max height 250px with scroll
- Larger touch targets (min 44px height)

## Implementation Notes

### Data Flow
1. User selects JSON file → Load units from parsed JSON
2. User toggles filter → Enable/disable checkboxes
3. User selects units → Store selected unit IDs
4. User clicks "Analyze Report" → Filter units before analysis

### API Changes
- No backend changes needed
- Filtering happens client-side before sending to analyze endpoint
- Or: Send selected unit IDs to backend, filter there

### State Management
- Store selected unit IDs in JavaScript array
- Persist selection when JSON file changes (if same file)
- Reset when JSON file changes (if different file)

## Edge Cases

1. **No units in JSON**: Show message "No units found in this standards file"
2. **All units deselected**: Show error "Please select at least one unit"
3. **JSON file changed**: Reset filter and selection
4. **Many units (50+)**: 
   - Show scrollable list
   - Add search/filter box for units (future enhancement)
5. **Unit ID format variations**: Handle "129v4", "129", "129-4" formats

## Future Enhancements (Not in Initial Implementation)

1. **Search/Filter Units**: Text input to filter unit list
2. **Save Unit Selection**: Remember selected units per JSON file
3. **Unit Groups**: Group units by category/qualification
4. **Quick Select**: Presets like "All", "Core Units", "Optional Units"

## Approval Checklist

- [ ] UI layout and placement approved
- [ ] Toggle behavior approved
- [ ] Checkbox styling approved
- [ ] Button placement and labels approved
- [ ] Selection counter format approved
- [ ] Error handling approach approved
- [ ] Responsive behavior approved




