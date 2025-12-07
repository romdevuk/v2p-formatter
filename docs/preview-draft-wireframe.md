# Preview Draft Modal - Text Wireframe

## Overview
This wireframe describes the enhanced Preview Draft modal with full-size window, undo functionality, and improved layout.

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Document Preview                          [Undo] [Redo] [✕ Close]       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │  Preview Content (Editable, Scrollable)                             │ │
│  │                                                                     │ │
│  │  [Document content with sections, placeholders, tables, etc.]      │ │
│  │                                                                     │ │
│  │  - Text is editable (contenteditable)                              │ │
│  │  - Tables with images/media                                        │ │
│  │  - Empty tables have delete buttons                                │ │
│  │                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
├─────────────────────────────────────────────────────────────────────────┤
│  Font Settings:                                                           │
│  ┌──────────────────────┐  ┌──────────────────────┐                     │
│  │ Size: [12pt ▼]      │  │ Type: [Times ▼]      │                     │
│  └──────────────────────┘  └──────────────────────┘                     │
├─────────────────────────────────────────────────────────────────────────┤
│  ▼ Hide Elements (Collapsed by default)                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ ☐ Section Titles                                                     │ │
│  │ ☐ AC covered (hides only "AC covered:" label, keeps AC values)      │ │
│  │ ☐ Image suggestion                                                   │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────┤
│  [Close]                                              [Update Draft]     │
│                                                      [Export DOCX]      │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Header Bar
- **Title**: "Document Preview"
- **Undo Button**: Top right, before redo button
  - Icon: ↶ or "Undo"
  - Action: Undo last change in preview content
  - Disabled when no changes to undo
- **Redo Button**: Top right, between undo and close
  - Icon: ↷ or "Redo"
  - Action: Redo last undone change in preview content
  - Disabled when no changes to redo
- **Close Button**: Top right (X)
  - Closes modal without saving

### 2. Preview Content Area
- **Full window size**: Takes up maximum available space
- **Editable**: Content is contenteditable
- **Scrollable**: Vertical scroll when content exceeds viewport
- **Background**: White (#ffffff)
- **Padding**: 40px
- **Font**: Applied from font settings (default: Times New Roman, 12pt)

### 3. Font Settings Section
- **Always visible** (not collapsible)
- **Font Size**: Dropdown with options (10pt, 11pt, 12pt, 13pt, 14pt, 16pt, 18pt)
- **Font Type**: Dropdown with options (Times New Roman, Arial, Courier New, Georgia, Verdana, Calibri)
- **Layout**: Two columns side by side
- **Position**: Above "Hide Elements" section

### 4. Hide Elements Section
- **Collapsed by default**: Shows only header with ▼ icon
- **Header**: "Hide Elements" with expand/collapse toggle
- **When expanded**: Shows three checkboxes:
  - ☐ Section Titles
  - ☐ AC covered (hides only the "AC covered:" label, keeps AC values visible)
  - ☐ Image suggestion
- **Position**: Below Font Settings, above bottom actions

### 5. Bottom Actions Bar
- **Left side**: Close button
- **Right side**: Two buttons stacked vertically or side by side:
  - **Update Draft**: Saves changes made in preview back to draft
  - **Export DOCX**: Exports current content to DOCX file

## Behavior

### Undo/Redo Functionality
- Tracks changes made in editable preview content
- Stores history of edits (text changes, deletions) in two stacks:
  - **Undo stack**: History of changes (for undoing)
  - **Redo stack**: History of undone changes (for redoing)
- **Undo button**:
  - Enabled when there are changes to undo
  - Disabled when undo stack is empty
  - Clicking undoes the last change and moves it to redo stack
- **Redo button**:
  - Enabled when there are undone changes to redo
  - Disabled when redo stack is empty
  - Clicking redoes the last undone change and moves it back to undo stack
- **History management**:
  - Limited to reasonable number (e.g., 50 states per stack)
  - New edits clear the redo stack (can't redo after new edit)
  - Each significant change (text edit, table deletion) creates a new state

### Update Draft
- Extracts text content from editable preview
- Removes HTML formatting but preserves structure
- Updates the current draft with modified content
- Shows success/error message
- Closes modal after successful update

### Delete Empty Table
- No confirmation dialog
- Immediately removes table when delete button clicked
- Updates undo history

### Window Sizing
- **Full size**: Modal takes up 95-98% of viewport width and height
- **Responsive**: Adjusts to screen size
- **Max dimensions**: 95vw × 95vh (or similar)

## State Management

### Undo/Redo History
- **Undo stack**: Array of content states (for undoing)
- **Redo stack**: Array of undone states (for redoing)
- **State management**:
  - New edit: Push current state to undo stack, clear redo stack
  - Undo: Pop from undo stack, push to redo stack, restore state
  - Redo: Pop from redo stack, push to undo stack, restore state
- Limited to reasonable number (e.g., 50 states per stack)
- Each significant change (text edit, table deletion) creates a new state

### Preview State
- Current content (editable HTML)
- Font settings (size, type)
- Hide/show settings (section titles, AC covered label only, image suggestion)
- Applied immediately when changed
- **Note**: "AC covered" checkbox hides only the label "AC covered:" but keeps the AC values (e.g., "AC1, AC2, AC3") visible

## User Flow

1. User clicks "Preview Draft"
2. Modal opens full-size with current draft content
3. User can:
   - Edit text directly in preview
   - Change font settings (applied immediately)
   - Toggle hide/show elements (collapsed by default)
   - Delete empty tables (no confirmation)
   - Undo/Redo recent changes
4. User clicks "Update Draft" to save changes
5. Draft is updated with modified content
6. User can export DOCX or close modal

## Technical Notes

- Modal uses flexbox for layout
- Preview content area is flex: 1 (takes remaining space)
- Undo/Redo uses MutationObserver or input event tracking
- Two-stack approach: undo stack and redo stack
- New edits clear redo stack (standard undo/redo behavior)
- Update Draft extracts textContent or innerText from editable div
- Font settings applied via CSS styles
- Hide/show uses CSS display: none/block

