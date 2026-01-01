# Observation Report Module - Complete Specification

## Document Purpose
This document provides a comprehensive specification for creating a **NEW** "Observation Report" module. This specification includes workflows, features, wireframes, and technology stack recommendations.

**⚠️ IMPORTANT: This is a NEW module - NO legacy code should be transferred. All code must be written fresh based on this specification.**

**Target Module URL**: `http://localhost/v2p-formatter/observation-report`

**Last Updated**: 2025-01-XX

---

## Table of Contents
1. [Overview](#overview)
2. [Workflows](#workflows)
3. [Features](#features)
4. [Text Wireframes](#text-wireframes)
5. [Technology Stack](#technology-stack)
6. [Standalone Libraries Architecture](#standalone-libraries-architecture)
7. [Data Models](#data-models)
8. [API Endpoints](#api-endpoints)
9. [File Structure](#file-structure)
10. [Key Implementation Details](#key-implementation-details)

---

## Overview

### Purpose
The Observation Report module allows users to create structured observation reports by:
- Assigning media files (photos/videos/PDFs/MP3) to placeholders within text content
- Organizing content into sections
- Managing standards and AC (Assessment Criteria) coverage
- Previewing the final document in real-time
- Exporting to DOCX format with embedded media

### Key Concepts
- **Placeholders**: Text markers like `{{Placeholder_Name}}` that get replaced with media tables
- **Media Assignment**: Linking media files to specific placeholders
- **Sections**: Content organized under "SECTION xxxx" markers
- **Drafts**: Save/load work-in-progress documents
- **Live Preview**: Real-time rendering of the final document

---

## Workflows

### Workflow 1: Initial Setup and Media Selection

```
1. User navigates to /observation-report (via top navigation tab "Observation Report")
   ↓
2. Page loads with:
   - Page width: 95% of viewport (not full width)
   - Top navigation tabs visible
   - Observation Report tab is active
   - Qualification dropdown (top-level folders)
   - Learner dropdown (disabled until qualification selected)
   - Empty media browser (left column)
   - Empty preview (center column)
   - Empty standards panel (right column)
   - 3-column resizable layout
   - Column widths restored from localStorage (if previously saved)
   ↓
3. User selects Qualification from dropdown
   ↓
4. Learner dropdown becomes enabled, populates with learners for that qualification
   ↓
5. User selects Learner
   ↓
6. Media browser scans and displays all media files from:
   /output/{qualification}/{learner}/ (recursively)
   ↓
7. Media thumbnails appear in grid layout
   - Images (JPG, JPEG, PNG): Show thumbnail with filename and size
   - Videos (MP4, MOV): Show thumbnail with play icon, duration, filename, size
   - PDFs: Show PDF icon, filename and size
   - Audio (MP3): Show audio icon, filename and size
   - All media initially available (not assigned)
```

### Workflow 2: Creating Content with Placeholders

```
1. User types text in Text Editor
   ↓
2. User adds placeholders using format: {{Placeholder_Name}}
   - Must use double curly braces
   - Use underscores (no spaces)
   - Case-insensitive
   ↓
3. System detects placeholders in real-time:
   - Extracts all {{...}} patterns
   - Assigns rainbow colors to each placeholder
   - Updates placeholder count
   - Highlights placeholders in preview
   ↓
4. User can add sections using "SECTION xxxx" format
   - Sections are detected automatically
   - Each section gets unique color
   - Sections are collapsible in preview
   ↓
5. Statistics update:
   - Placeholder count
   - Word count
   - Assigned/unassigned counts
```

### Workflow 3: Assigning Media to Placeholders

#### Method A: Click-to-Assign
```
1. User clicks on a media thumbnail card
   ↓
2. Dialog appears showing:
   - List of all placeholders found in text
   - Each placeholder shown with its color
   - Assignment status (assigned/unassigned)
   ↓
3. User selects a placeholder from the list
   ↓
4. Media is assigned to that placeholder
   ↓
5. UI updates:
   - Media card shows "✓ Assigned" badge
   - Media card becomes disabled (grayed out)
   - Preview updates to show media in placeholder table
   - Placeholder stats update
```

#### Method B: Drag-and-Drop
```
1. User drags a media thumbnail card
   ↓
2. User drops it on a placeholder table in the preview area
   ↓
3. If multiple placeholders exist, dialog appears for selection
   ↓
4. User selects placeholder
   ↓
5. Media is assigned (same updates as Method A)
```

#### Method C: Bulk Assignment
```
1. User selects multiple media cards (Ctrl/Cmd + click)
   ↓
2. User clicks "Assign Selected" or drags the group
   ↓
3. Dialog shows placeholders
   ↓
4. User selects placeholder
   ↓
5. All selected media are assigned to that placeholder
   ↓
6. All media cards update to assigned state
```

### Workflow 4: Reordering Media Within Placeholders

```
1. User has assigned multiple media to a placeholder
   ↓
2. In the preview, media appear in a 2-column table
   - Order: left-to-right, top-to-bottom
   - Position 1: Row 0, Col 0
   - Position 2: Row 0, Col 1
   - Position 3: Row 1, Col 0
   - etc.
   ↓
3. User can reorder by:
   - Dragging media within the placeholder assignment panel
   - Using up/down arrow buttons
   ↓
4. Preview updates in real-time to reflect new order
```

### Workflow 5: Header Information Entry

```
1. User expands "Header" section (collapsed by default)
   ↓
2. Form fields appear:
   - Learner (text input)
   - Assessor (text input)
   - Visit Date (date picker, format: YYYY-MM-DD)
   - Location (text input)
   - Address (text input)
   ↓
3. User fills in header fields
   ↓
4. Header data is stored in draft state
   ↓
5. In preview (if "Show header" is checked):
   - Header table appears at top
   - Shows all entered information
   - Formatted as 2-column table with 1px borders
```

### Workflow 6: Assessor Feedback Entry

```
1. User scrolls to "Assessor Feedback" textarea (below Text Editor)
   ↓
2. User enters feedback text
   ↓
3. Feedback is stored in draft state
   ↓
4. In preview (if "Show assessor feedback" is checked):
   - Feedback table appears at bottom
   - Shows feedback text in 1px border table
```

### Workflow 7: Section Management

```
1. User types "SECTION xxxx" in text editor
   - Format: "SECTION Health and Safety"
   - Format: "SECTION: Site Arrival"
   - Format: "SECTION - Equipment Check"
   ↓
2. System detects section markers
   ↓
3. Content following section marker belongs to that section
   - Until next section marker
   - Or end of document
   ↓
4. In preview:
   - Sections appear as collapsible containers
   - Each section has unique color
   - All sections collapsed by default
   - Section header shows title and expand/collapse icon
   ↓
5. User can:
   - Click section header to expand/collapse
   - Use "Expand All" / "Collapse All" buttons
   - Section state persists during editing
```

### Workflow 8: Saving Drafts

```
1. User clicks "💾 Save Draft" button
   ↓
2. Dialog appears:
   - Input field: "Enter draft name"
   - Qualification selector: [Dropdown ▼] (shows all qualifications)
   - Units selector: 
     * Option: "All Units" (default)
     * Option: "Specific Units" (shows unit list for selected qualification)
     * If "Specific Units" selected: Multi-select list of units appears
   - Shows current state summary:
     * Qualification/Learner
     * Placeholder count
     * Assigned media count
   ↓
3. User enters draft name (e.g., "Site_Report_v1")
   ↓
4. User selects qualification and units (all or specific)
   ↓
5. User clicks "Save"
   ↓
6. System saves to:
   /output/.drafts/{draft_name}.json
   ↓
7. Draft includes:
   - Text content
   - All media assignments
   - Media order for each placeholder
   - Selected qualification/learner
   - Selected units (all or specific list)
   - Header data
   - Assessor feedback
   - Standards data (if loaded)
   - Timestamps (created, modified)
   ↓
8. Success message: "Draft '{name}' saved successfully"
```

### Workflow 9: Loading Drafts

```
1. User clicks "📂 Load Draft" button
   ↓
2. Dialog appears showing:
   - List of all saved drafts
   - Each draft shows:
     * Name
     * Date created
     * Date modified
     * Qualification/Learner
     * Placeholder count
     * Media count
   ↓
3. User selects a draft
   ↓
4. User clicks "Load"
   ↓
5. System loads draft data:
   - Restores text content
   - Restores qualification/learner selection
   - Restores all media assignments
   - Restores media order
   - Restores header data
   - Restores assessor feedback
   ↓
6. UI updates:
   - Text editor populated
   - Qualification/Learner dropdowns set
   - Media browser shows assigned states
   - Preview renders with all content
   - Header fields populated
   - Assessor feedback populated
```

### Workflow 10: Standards Management

```
1. Standards panel appears in right column of main interface
   ↓
2. User loads draft (Standards data loads with draft if JSON file assigned)
   - Standards panel shows: "No draft loaded. Load a draft to view standards."
   - Or: "No JSON Standards File assigned to this draft."
   ↓
3. When draft with standards is loaded:
   - Standards panel displays all units from the JSON file
   - Each unit shows:
     * Unit header with expand/collapse icon (▶ collapsed, ▼ expanded)
     * Unit ID and title (e.g., "641: Health and Safety")
     * Unit dropdown (for filtering/selecting specific units)
   ↓
4. Unit Content (when expanded):
   - List of AC (Assessment Criteria) items
   - Each AC shows:
     * AC ID (text field displaying AC identifier, e.g., "1.1", "1.2")
     * AC Text (description of the AC)
     * Covered: section title (if AC is referenced in text)
       - Shows section name(s) where AC is mentioned
       - Section names are clickable (dotted underline, colored by section color)
       - Clicking section name opens/expands that section in Live Preview
   ↓
5. AC Coverage Detection:
   - System scans text content for AC references
   - Detects patterns like:
     * "641:1.1" (explicit unit:AC format)
     * "AC covered: 641:1.1, 1.2, 1.3" (AC covered line)
     * "Unit 641 AC 1.1" (unit AC format)
   - Matches ACs to sections where they appear
   - Updates "Covered:" line for each AC dynamically
   ↓
6. Standards Search:
   - User types keyword in search box
   - System searches AC text (not AC IDs) for keyword
   - Highlights matching keywords in AC text (yellow highlight)
   - Expands units that contain matching ACs
   - Collapses units with no matches
   - Shows "No results found" if no matches
   - Scrolls to first match automatically
   ↓
7. Clearing Search:
   - User clicks (✕) button in search box
   - OR user erases all text from search box
   - System removes all highlights
   - Restores units to previous expand/collapse state (before search)
   - All units return to their original state
   ↓
8. Unit Management:
   - User can expand/collapse individual units (click unit header)
   - "Expand All" button expands all units
   - "Collapse All" button collapses all units
   - Unit dropdown allows filtering/selecting specific units (if implemented)
   ↓
9. Section Navigation:
   - When user clicks section name in "Covered:" line:
     * Section expands in Live Preview (if collapsed)
     * Live Preview scrolls to show that section
     * Section is highlighted/emphasized
   ↓
10. Standards State:
   - Saved with draft (JSON file ID stored)
   - Loaded automatically when draft is loaded
   - Cleared when draft is cleared
   - Search state is temporary (not saved)
```

### Workflow 11: Document Preview

```
1. User clicks "👁️ Preview Draft" button
   ↓
2. Preview dialog opens (full-screen or large modal)
   - Layout: 3 columns (resizable)
   - Left: Sections list
   - Center: Preview content
   - Right: Actions panel
   - Resizer bars between columns (drag to resize)
   ↓
3. Column Resizing:
   - User can drag resizer bars to adjust column widths
   - Minimum width constraints apply
   - Column widths saved to localStorage
   - Widths restored when preview dialog is reopened
   ↓
4. Left Column - Sections:
   - List of all sections from document
   - Each section shows:
     * Section title
     * Expand/collapse icon
     * Color indicator
   - User can click section to jump to it in preview
   - User can expand/collapse sections
   ↓
4. Center Column - Preview Content:
   - Header table (if "Show header" checked)
   - Document content with sections
   - Media tables for each placeholder
   - Assessor feedback table (if "Show assessor feedback" checked)
   ↓
5. Right Column - Actions Panel:
   - Font Settings:
     * Size dropdown (default: 16pt)
     * Type dropdown (default: Times New Roman)
   - Hide Elements checkboxes:
     * Section Titles
     * AC covered
     * Image suggestion
     * Paragraph numbers
     * Empty media fields
     * Trim empty paragraphs
     * Show header
     * Show assessor feedback
   - Buttons:
     * Update Draft
     * Export DOCX
   ↓
6. User can:
   - Toggle visibility of elements
   - Change font settings
   - Scroll through preview
   - Navigate via sections list
   - Expand/collapse sections
   ↓
7. Preview updates in real-time as settings change
```

### Workflow 11: DOCX Export

```
1. User clicks "📄 Export DOCX" (in preview or main page)
   ↓
2. System uses draft name as filename (if draft is loaded)
   - If no draft loaded: Uses default name or prompts for filename
   - Filename format: {draft_name}.docx
   ↓
3. System generates DOCX (no validation required):
   - Creates document with A4 page size
   - Adds "Assessment Report" heading (if header data exists)
   - Adds header table (if header data exists)
   - Adds blank paragraph
   - Adds "Observation Report" heading (if header data exists)
   - Processes text content:
     * Replaces placeholders with 2-column tables
     * Embeds images in table cells
     * Adds video filenames as text (MP4, MOV)
     * Adds PDF filenames as text
     * Adds MP3 filenames as text
     * Handles sections (if present)
   - Adds assessor feedback table at bottom (if feedback exists)
   ↓
4. DOCX saved to:
   /output/{draft_name}.docx (or custom filename if provided)
   ↓
5. Success message with download link
   ↓
6. User can click download link to get file
```

### Workflow 12: Media Management

```
1. Media Browser displays all media from selected learner folder
   ↓
2. Media cards show:
   - Thumbnail (120x90px) or icon (for PDF/MP3)
   - Filename (editable)
   - File size
   - Type indicator (IMG/VID/PDF/MP3)
   - Duration (for videos)
   - Assignment status badge
   ↓
3. User can:
   - Click media to assign
   - Drag media to assign
   - Select multiple media (Ctrl/Cmd + click)
   - View media in full size (click thumbnail)
   - Update filename: Click on filename, edit inline, save
   ↓
4. Filename Update:
   - User clicks on filename in media card
   - Filename becomes editable (inline edit)
   - User types new name
   - User presses Enter or clicks save icon
   - System updates filename via API
   - Media card updates with new name
   - Original file is renamed on disk
   ↓
5. Assigned media:
   - Shows "✓ Assigned" badge
   - Becomes disabled (grayed out, opacity 0.5)
   - Cannot be clicked or dragged
   - Shows which placeholder it's assigned to
   ↓
6. Removing assignment:
   - User clicks "×" button on media in preview
   - Media becomes available again
   - Badge removed, card re-enabled
```

---

## Features

### Core Features

#### 1. Two-Level Folder Selection
- **Qualification Dropdown**: Lists top-level folders (qualifications)
- **Learner Dropdown**: Lists subfolders (learners) within selected qualification
- **Recursive Media Scan**: Scans all media files recursively from learner folder
- **Media Display**: Shows all media in grid layout with thumbnails
- **Supported Media Types**:
  - Images: JPG, JPEG, PNG
  - Videos: MP4, MOV
  - Documents: PDF
  - Audio: MP3

#### 2. Placeholder System
- **Detection**: Auto-detects `{{Placeholder_Name}}` patterns in text
- **Validation**: Tracks assigned/unassigned placeholders
- **Color Coding**: Each placeholder gets unique rainbow color
- **Case-Insensitive**: `{{Site_Arrival}}` = `{{site_arrival}}`
- **Format Rules**: Must use underscores, no spaces

#### 3. Media Assignment
- **Multiple Methods**: Click-to-assign, drag-and-drop, bulk assignment
- **One-Time Assignment**: Each media can only be assigned to one placeholder
- **Disabled State**: Assigned media becomes disabled in browser
- **Visual Feedback**: Badges, highlights, status indicators

#### 4. Media Ordering
- **Reordering**: Drag-and-drop or arrow buttons
- **Table Layout**: 2-column tables, left-to-right, top-to-bottom
- **Order Preview**: Shows cell positions (Row X, Col Y)

#### 5. Section System
- **Detection**: Auto-detects "SECTION xxxx" markers
- **Collapsible**: Sections can be expanded/collapsed
- **Color Coding**: Each section gets unique color
- **Default State**: All sections collapsed by default
- **Content Nesting**: All content after section marker belongs to that section

#### 6. Header System
- **Fields**: Learner, Assessor, Visit Date, Location, Address
- **Date Formatting**: Converts YYYY-MM-DD to readable format (e.g., "15 January 2025")
- **Preview Toggle**: Can show/hide header in preview
- **DOCX Export**: Always included in DOCX (regardless of preview setting)

#### 7. Assessor Feedback
- **Textarea Input**: Multi-line text input below text editor
- **Preview Display**: Shows as table at bottom of preview
- **Preview Toggle**: Can show/hide in preview
- **DOCX Export**: Always included in DOCX at bottom

#### 8. Live Preview
- **Real-Time Updates**: Updates as user makes changes
- **Table Rendering**: 2-column tables for placeholders
- **Image Embedding**: Shows actual images in preview
- **Video Display**: Shows video filenames (not embedded video)
- **Section Rendering**: Collapsible sections with color coding
- **Dark Theme**: Matches overall application theme
- **Resizable Columns**: User can resize columns horizontally by dragging resizer bars
- **Column Width Persistence**: Column widths saved to localStorage and restored on load

#### 9. Draft System
- **Save Draft**: Save current state with custom name
- **Load Draft**: Load previously saved draft
- **Draft List**: Shows all drafts with metadata
- **Delete Draft**: Remove unwanted drafts
- **State Persistence**: Saves all assignments, order, header, feedback

#### 10. DOCX Export
- **Table Generation**: Creates 2-column tables for placeholders
- **Image Embedding**: Embeds images in table cells
- **Video Filenames**: Adds video filenames as text (MP4, MOV)
- **PDF Filenames**: Adds PDF filenames as text
- **MP3 Filenames**: Adds MP3 filenames as text
- **Header Table**: Includes header information at top
- **Assessor Feedback**: Includes feedback table at bottom
- **Section Handling**: Preserves section structure
- **Styling**: A4 format, Times New Roman, configurable font size
- **Filename**: Uses draft name by default (if draft loaded)

#### 11. Standards Integration
- **Standalone Library**: Standards functionality is a separate, reusable component
- **JSON File Support**: Loads standards from JSON file (via AC Matrix JSON file ID)
- **Unit Display**: Shows units with AC (Assessment Criteria) items
- **Unit Dropdown**: Filter/select specific units (if implemented)
- **AC ID Display**: Each AC shows its ID (e.g., "1.1", "1.2") as text field
- **AC Text Display**: Shows full AC description text
- **AC Coverage Detection**: Automatically detects AC references in text content
- **Covered Section Links**: Shows which sections contain each AC, clickable to navigate
- **Search Functionality**: 
  - Searches AC text (not AC IDs)
  - Highlights matching keywords in AC text
  - Expands units with matches, collapses units without matches
  - Restores unit states when search is cleared
- **Expand/Collapse**: Units can be expanded/collapsed individually or all at once
- **Draft Integration**: Standards data (JSON file ID) saved and loaded with drafts
- **Preview Integration**: Clicking section name in "Covered:" opens/expands section in Live Preview

### UI Features

#### 1. Page Layout
- **Page Width**: 95% of viewport width (not full width)
- **Centering**: Page content centered horizontally
- **Navigation**: Top navigation tabs (Video to Image, Media Converter, AC Matrix, **Observation Report**)
- **Active Tab**: "Observation Report" tab highlighted when module is active
- **Responsive**: Maintains 95% width on all screen sizes

#### 2. Dark Theme
- **Consistent dark theme throughout interface**
- **Base Colors**:
  - Background: `#1e1e1e`
  - Text: `#e0e0e0`
  - Panels: `#2a2a2a`
  - Borders: `#555` or `#444`
  - Hover states: `#333` or `#3a3a3a`
  
- **Text Input Fields**:
  - Background: `#1e1e1e`
  - Text color: `#e0e0e0`
  - Border: `1px solid #555`
  - Focus border: `#667eea` (or accent color)
  - Placeholder text: `#999` or `#666`
  
- **Textarea Fields**:
  - Background: `#1e1e1e`
  - Text color: `#e0e0e0`
  - Border: `1px solid #555`
  - Focus border: `#667eea` (or accent color)
  - Placeholder text: `#999` or `#666`
  - Scrollbar: Dark theme (thumb: `#555`, track: `#1e1e1e`)
  
- **Dropdown/Select Fields**:
  - Background: `#1e1e1e`
  - Text color: `#e0e0e0`
  - Border: `1px solid #555`
  - Focus border: `#667eea`
  - Option background: `#1e1e1e`
  - Option text: `#e0e0e0`
  - Dropdown arrow icon: `#e0e0e0`
  
- **Icons**:
  - Default color: `#e0e0e0`
  - Hover color: `#fff` or accent color
  - Disabled state: `#666` or `#555`
  - Active state: Accent color (e.g., `#667eea`)
  - Icons in buttons: Match button text color
  
- **Buttons**:
  - Primary button background: `#667eea` (or accent color)
  - Primary button text: `#fff`
  - Secondary button background: `#2a2a2a`
  - Secondary button text: `#e0e0e0`
  - Button border: `1px solid #555`
  - Hover state: Lighter background or accent color
  
- **Checkboxes/Radio Buttons**:
  - Background: `#1e1e1e`
  - Border: `1px solid #555`
  - Checked color: Accent color (e.g., `#667eea`)
  - Label text: `#e0e0e0`
  
- **Scrollbars**:
  - Track background: `#1e1e1e` or `#2a2a2a`
  - Thumb background: `#555`
  - Thumb hover: `#666`
  - Width: 8-12px
  
- **Links**:
  - Default color: `#667eea` (or accent color)
  - Hover color: Lighter shade or `#fff`
  - Visited: Slightly muted accent color
  
- **Placeholder Text** (in inputs/textarea):
  - Color: `#999` or `#666`
  - Opacity: 0.7
  
- **Disabled Elements**:
  - Background: `#1a1a1a` or `#0d0d0d`
  - Text: `#666` or `#555`
  - Border: `#333`
  - Opacity: 0.5
  - Cursor: `not-allowed`
  
- **Focus States**:
  - Outline: `2px solid #667eea` (or accent color)
  - Background: Slightly lighter (`#2a2a2a`)
  
- **Error States**:
  - Border color: `#ff6b6b` (red)
  - Text color: `#ff6b6b`
  - Background: `#2a1e1e` (slight red tint)
  
- **Success States**:
  - Border color: `#00b894` (green)
  - Text color: `#00b894`
  - Background: `#1e2a1e` (slight green tint)

#### 3. Font Size Toggle
- Two sizes: Regular (Aa) and Big (AA)
- Applies to all text in interface
- Persists user preference

#### 4. Collapsible Sections
- Header section (collapsed by default, at bottom)
- Text Editor section (collapsed by default, at bottom)
- Assessor Feedback section (collapsed by default, at bottom)
- Standards panel (in right column, always visible when draft loaded)
- Sections in preview (collapsed by default)

#### 5. Media Browser
- Grid layout (responsive columns)
- Thumbnail display (images/videos) or icon (PDF/MP3)
- File metadata (size, type, duration)
- Assignment status indicators
- Editable filenames (inline editing)
- Settings panel (filter, view options)
- Expand/collapse controls

#### 6. Statistics Display
- Placeholder count
- Word count
- Assigned count
- Unassigned count
- Updates in real-time

#### 7. Preview Actions Panel
- Font settings (size, type)
- Hide/show elements checkboxes
- Update Draft button
- Export DOCX button

#### 8. Resizable Columns
- **Main Interface**: 3-column layout (Media Browser | Live Preview | Standards)
  - Resizer bars between columns
  - Drag to resize horizontally
  - Minimum width constraints (200px for left/middle, 250px for right)
  - Column widths saved to localStorage
  - Widths restored on page load
- **Preview Dialog**: 3-column layout (Sections | Preview Content | Actions)
  - Resizer bars between columns
  - Drag to resize horizontally
  - Column widths saved to localStorage
  - Widths restored when preview dialog is reopened

---

## Text Wireframes

### Main Interface Layout (3-Column Layout - Resizable)

**Note**: 
- Page width: **95% of viewport** (centered, not full width)
- User can resize columns horizontally by dragging the resizer bars between columns
- Column widths are saved to localStorage and restored on page load
- Module accessible via top navigation tab "Observation Report"

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Navigation: [Video to Image] [Media Converter] [AC Matrix] [Observation Report] ← Active │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ Observation Report                                                       │
│ (Page width: 95% of viewport, centered)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Top Controls                                                         │ │
│ │                                                                     │ │
│ │ Select Qualification: [Dropdown ▼]  Select Learner: [Dropdown ▼]   │ │
│ │ [🔄 Refresh]                                                        │ │
│ │                                                                     │ │
│ │ Text Size: [Aa] [AA]  [📂 Load Draft]                             │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌──────────────────║──────────────────────║──────────────────────────┐ │
│ │                  ║                      ║                          │ │
│ │   LEFT COLUMN    ║   CENTER COLUMN      ║   RIGHT COLUMN          │ │
│ │   Media Browser  ║   Live Preview       ║   Standards             │ │
│ │   (resizable)    ║   (resizable)        ║   (resizable)           │ │
│ │                  ║                      ║                          │ │
│ │                  ║  [Resizer bars -     ║                          │ │
│ │                  ║   drag to resize]    ║                          │ │
│ │                  │                      │                          │ │
│ │ ┌──────────────┐ │ ┌──────────────────┐ │ ┌────────────────────┐ │ │
│ │ │ Media Header │ │ │ Live Preview      │ │ │ Standards          │ │ │
│ │ │ 24 files     │ │ │                  │ │ │                    │ │ │
│ │ │ [⚙️] [⬛]   │ │ │ ┌────────────────┐│ │ │ [▼ Expand All]     │ │ │
│ │ └──────────────┘ │ │ │                ││ │ │ [▶ Collapse All]  │ │ │
│ │                  │ │ │ │ Rendered      ││ │ │                    │ │ │
│ │ ┌──────────────┐ │ │ │ │ content with  ││ │ │ [🔍 Search...]     │ │ │
│ │ │ Media Grid   │ │ │ │ │ media tables  ││ │ │                    │ │ │
│ │ │              │ │ │ │ │              ││ │ │ ┌────────────────┐│ │ │
│ │ │ ┌────┐ ┌────┐│ │ │ │ │              ││ │ │ │ Unit: [All ▼]   ││ │ │
│ │ │ │IMG │ │VID ││ │ │ │ │              ││ │ │ │ [▼ Expand All] ││ │ │
│ │ │ │ ✓  │ │ ⏯  ││ │ │ │ │              ││ │ │ │ [▶ Collapse All]││ │ │
│ │ │ └────┘ └────┘│ │ │ │ │              ││ │ │ │ [🔍 Search...] [✕]││ │ │
│ │ │ photo1 video1│ │ │ │ │              ││ │ │ │                    ││ │ │
│ │ │              │ │ │ │ │              ││ │ │ │ ▶ 641: Health... ││ │ │
│ │ │ [Scroll ↓]   │ │ │ │ └────────────────┘│ │ │ │                    ││ │ │
│ │ └──────────────┘ │ │ │                  │ │ │ │ ▼ 642: Site Arrival││ │ │
│ │                  │ │ │                  │ │ │ │   1.1  AC text...  ││ │ │
│ │                  │ │ │                  │ │ │ │   Covered: Section 1││ │ │
│ │                  │ │ │                  │ │ │ │   1.2  AC text...  ││ │ │
│ │                  │ │ │                  │ │ │ │   Covered:          ││ │ │
│ │                  │ │ │                  │ │ │                    │ │ │
│ │                  │ │ │                  │ │ │ [Scroll ↓]         │ │ │
│ │                  │ │ │                  │ │ └────────────────────┘ │ │
│ └──────────────────┴─┴────────────────────┴─┴──────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ▶ Header (Collapsed)                                                 │ │
│ │   [Click to expand - shows Learner, Assessor, Visit Date, etc.]     │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ▶ Text Editor (Collapsed)                                            │ │
│ │   [Click to expand - shows text editor with placeholders]            │ │
│ │   Stats: Placeholders: 3 | Words: 45 | Assigned: 2 | Unassigned: 1  │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ▶ Assessor Feedback (Collapsed)                                      │ │
│ │   [Click to expand - shows textarea for feedback]                    │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Actions:                                                             │ │
│ │ [💾 Save Draft] [👁️ Preview Draft]                                 │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

### Header Section (Expanded)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ▼ Header                                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ Learner:      [________________________]                                │
│ Assessor:     [________________________]                               │
│ Visit Date:   [YYYY-MM-DD]                                             │
│ Location:     [________________________]                               │
│ Address:      [________________________]                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Text Editor Section (Expanded)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ▼ Text Editor                                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ (Dark theme background: #1e1e1e, Light text: #e0e0e0)             │ │
│ │                                                                     │ │
│ │ 1  Observation Report                                              │ │
│ │ 2                                                                   │ │
│ │ 3  Site: Construction Site A                                        │ │
│ │ 4  Date: 2025-01-15                                                 │ │
│ │ 5                                                                   │ │
│ │ 6  SECTION Health and Safety                                       │ │
│ │ 7                                                                   │ │
│ │ 8  {{Site_Arrival_Induction}}  ← Red color (#ff6b6b)              │ │
│ │ 9                                                                   │ │
│ │10  The site arrival process was conducted...                        │ │
│ │11                                                                   │ │
│ │12  {{Safety_Briefing}}  ← Cyan color (#4ecdc4)                    │ │
│ │13                                                                   │ │
│ │14  Safety procedures were explained...                             │ │
│ │                                                                     │ │
│ │ [Scroll ↓]                                                           │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ Placeholders: 3  |  Assigned: 2  |  Unassigned: 1  |  Words: 45        │
└─────────────────────────────────────────────────────────────────────────┘
```

### Preview Dialog (Full Screen - 3 Columns - Resizable)

**Note**: User can resize columns horizontally by dragging the resizer bars between columns. Column widths are saved to localStorage and restored when preview dialog is reopened.

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 📄 Document Preview                                    [✕ Close]        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ┌──────────────────║──────────────────────────────║────────────────────┐ │
│ │                  ║                              ║                    │ │
│ │   LEFT COLUMN    ║   CENTER COLUMN              ║   RIGHT COLUMN     │ │
│ │   Sections       ║   Preview Content            ║   Actions          │ │
│ │   (resizable)    ║   (resizable)                ║   (resizable)      │ │
│ │                  ║                              ║                    │ │
│ │                  ║  [Resizer bars -             ║                    │ │
│ │                  ║   drag to resize]            ║                    │ │
│ │                  │                              │                    │ │
│ │ ┌──────────────┐ │ ┌──────────────────────────┐ │ ┌────────────────┐ │ │
│ │ │ Sections     │ │ │ Preview Content          │ │ │ ⚙️ Actions     │ │ │
│ │ │              │ │ │                          │ │ │                │ │ │
│ │ │ ▶ Section 1  │ │ │ ┌──────────────────────┐ │ │ │ Font Settings: │ │ │
│ │ │ ▶ Section 2  │ │ │ │ Header Table         │ │ │ │   Size: [16pt] │ │ │
│ │ │ ▶ Section 3  │ │ │ │ ┌──────┬──────────┐ │ │ │ │   Type: [TNR]  │ │ │
│ │ │              │ │ │ │ │Learner│ John Doe│ │ │ │ │                │ │ │
│ │ │ [Click to    │ │ │ │ ├──────┼──────────┤ │ │ │ │ Hide Elements: │ │ │
│ │ │  jump to     │ │ │ │ │Assess│ Jane S.  │ │ │ │ │   ☐ Section    │ │ │
│ │ │  section]    │ │ │ │ └──────┴──────────┘ │ │ │ │   ☐ AC covered  │ │ │
│ │ │              │ │ │ └──────────────────────┘ │ │ │ │   ☐ Image sug │ │ │
│ │ │              │ │ │                          │ │ │ │   ☐ Para nums │ │ │
│ │ │              │ │ │ SECTION: 1 – Health...    │ │ │ │   ☐ Empty med │ │ │
│ │ │              │ │ │                          │ │ │ │   ☐ Trim para │ │ │
│ │ │              │ │ │ ┌──────────┬──────────┐ │ │ │ │   ☑ Show head │ │ │
│ │ │              │ │ │ │ [Image]  │ video.mp4│ │ │ │ │   ☑ Show feed │ │ │
│ │ │              │ │ │ ├──────────┼──────────┤ │ │ │ │                │ │ │
│ │ │              │ │ │ │ [Image]  │ [Image]  │ │ │ │ │ [Update Draft] │ │ │
│ │ │              │ │ │ └──────────┴──────────┘ │ │ │ │ [Export DOCX]  │ │ │
│ │ │              │ │ │                          │ │ │ │                │ │ │
│ │ │              │ │ │ Text content here...     │ │ │ │                │ │ │
│ │ │              │ │ │                          │ │ │ │                │ │ │
│ │ │              │ │ │ ┌──────────────────────┐ │ │ │ │                │ │ │
│ │ │              │ │ │ │ Assessor Feedback     │ │ │ │                │ │ │
│ │ │              │ │ │ │ [Feedback text...]    │ │ │ │                │ │ │
│ │ │              │ │ │ └──────────────────────┘ │ │ │ │                │ │ │
│ │ │              │ │ │                          │ │ │ │                │ │ │
│ │ │ [Scroll ↓]   │ │ │ [Scroll ↓]               │ │ │ │ [Scroll ↓]     │ │ │
│ │ └──────────────┘ │ └──────────────────────────┘ │ └────────────────┘ │ │
│ └──────────────────┴──────────────────────────────┴────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

### Media Assignment Dialog

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Assign Media to Placeholder                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ Select placeholder:                                                     │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ☑ {{Site_Arrival_Induction}}  ✅ 3 media assigned                  │ │
│ │   Color: #ff6b6b (Red)                                             │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ ○ {{Safety_Briefing}}  ⚠️ 1 media assigned                        │ │
│ │   Color: #4ecdc4 (Cyan)                                            │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ ○ {{Equipment_Check}}  ❌ No media assigned                       │ │
│ │   Color: #45b7d1 (Blue)                                            │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ Media to assign:                                                        │
│ ┌────┐ ┌────┐ ┌────┐                                                  │
│ │IMG │ │VID │ │IMG │                                                  │
│ └────┘ └────┘ └────┘                                                  │
│ photo1 video1 photo2                                                   │
│                                                                         │
│ ┌──────────┐  ┌──────────┐                                            │
│ │  Cancel  │  │  Assign  │                                            │
│ └──────────┘  └──────────┘                                            │
└─────────────────────────────────────────────────────────────────────────┘
```

### Save Draft Dialog

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 💾 Save Draft                                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ Enter draft name:                                                        │
│ ┌───────────────────────────────────────────────────────────────────┐ │
│ │ Site_Report_v1                                                      │ │
│ └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ Current state:                                                          │
│ • Qualification: Inter                                                  │
│ • Learner: John_Doe                                                     │
│ • Placeholders: 3 found                                                │
│ • Assigned: 2 placeholders                                              │
│ • Media items: 5 assigned                                               │
│                                                                         │
│ ┌──────────┐  ┌──────────┐                                            │
│ │  Cancel  │  │   Save   │                                            │
│ └──────────┘  └──────────┘                                            │
└─────────────────────────────────────────────────────────────────────────┘
```

### Load Draft Dialog

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 📂 Load Draft                                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ Select a draft to load:                                                 │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ☑ Site_Report_v1                                                    │ │
│ │   Created: 2025-01-15 10:30  |  Modified: 2025-01-15 14:30        │ │
│ │   Qualification: Inter  |  Learner: John_Doe                      │ │
│ │   3 placeholders, 5 media items                                     │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ ○ Site_Report_v2                                                    │ │
│ │   Created: 2025-01-15 15:00  |  Modified: 2025-01-15 15:45        │ │
│ │   Qualification: Fire  |  Learner: Jane_Smith                     │ │
│ │   2 placeholders, 3 media items                                     │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ ○ Safety_Check_Draft                                                │ │
│ │   Created: 2025-01-14 09:00  |  Modified: 2025-01-14 12:00        │ │
│ │   Qualification: Deco  |  Learner: Bob_Johnson                   │ │
│ │   1 placeholder, 2 media items                                     │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐                             │
│ │  Cancel  │  │  Delete  │  │   Load   │                             │
│ └──────────┘  └──────────┘  └──────────┘                             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Architecture Philosophy

**Modular Standalone Libraries**: For high efficiency and maintainability, the following components should be implemented as **standalone, reusable libraries**:

1. **Media Browser Library** - Standalone component for media file browsing and selection
2. **Live Preview Library** - Standalone component for real-time document preview rendering
3. **Standards Library** - Standalone component for standards/AC management (already exists, can be reused)
4. **Preview Draft Library** - Standalone component for preview dialog functionality

**Benefits of Standalone Libraries**:
- **Reusability**: Can be used in other modules
- **Testability**: Each library can be tested independently
- **Maintainability**: Changes to one library don't affect others
- **Performance**: Optimized, focused code for each component
- **Modularity**: Easy to swap implementations or add features

### Backend

#### Framework & Core
- **Flask**: Python web framework
  - Version: Latest stable
  - Purpose: Routing, request handling, template rendering
  - Routes: `/observation-report` (main page), `/observation-report/*` (API routes)
  - Navigation: Add "Observation Report" tab to top navigation (alongside Video to Image, Media Converter, AC Matrix)

#### Python Libraries
- **python-docx**: DOCX file generation
  - Purpose: Create Word documents with tables, images, formatting
  - Usage: `app/observation_docx_generator.py`
  
- **Pillow (PIL)**: Image processing
  - Purpose: Image manipulation, thumbnail generation, dimension extraction
  - Usage: Image embedding in DOCX, thumbnail generation

- **Pathlib**: File system operations
  - Purpose: Path handling, file scanning
  - Usage: Media file scanning, draft management

#### Backend Modules (NEW - No Legacy Code)
```
app/
├── observation_report_scanner.py      # NEW: Media file scanning
├── observation_report_docx_generator.py  # NEW: DOCX generation
├── observation_report_placeholder_parser.py  # NEW: Placeholder parsing
├── observation_report_draft_manager.py  # NEW: Draft save/load
└── routes.py                          # NEW: Add /observation-report/* routes
```

**⚠️ Note**: All backend modules must be NEW implementations. Do NOT copy from observation_media modules.

### Frontend - Standalone Libraries Architecture

#### Core Technologies
- **HTML5**: Markup structure
- **CSS3**: Styling, dark theme, responsive layout
- **Vanilla JavaScript**: No frameworks, pure JS
- **Modular ES6 Modules**: Each component as a standalone library

#### Standalone Library Structure

The frontend should be organized as **standalone, reusable libraries**:

```
static/
├── js/
│   ├── observation-report/
│   │   ├── observation-report-media-browser.js    # NEW: Standalone Media Browser Library
│   │   ├── observation-report-live-preview.js     # NEW: Standalone Live Preview Library
│   │   ├── observation-report-standards.js         # NEW: Standalone Standards Library
│   │   ├── observation-report-preview-draft.js   # NEW: Standalone Preview Draft Library
│   │   └── observation-report-column-resizer.js  # NEW: Standalone Column Resizer Library
│   └── observation-report.js                      # NEW: Main orchestrator (uses libraries)
└── css/
    ├── observation-report/
    │   ├── observation-report-media-browser.css   # NEW: Media Browser styles
    │   ├── observation-report-live-preview.css   # NEW: Live Preview styles
    │   ├── observation-report-standards.css       # NEW: Standards styles
    │   ├── observation-report-preview-draft.css # NEW: Preview Draft styles
    │   └── observation-report-column-resizer.css # NEW: Column Resizer styles
    └── observation-report.css                     # NEW: Main module styles
```

#### Library Specifications

**1. Media Browser Library (`observation-report-media-browser.js`)**
- **Purpose**: Standalone component for browsing and selecting media files
- **API**: 
  ```javascript
  class ObservationReportMediaBrowser {
    constructor(containerId, options)
    loadMedia(qualification, learner)
    onMediaSelect(callback)
    updateAssignmentState(assignments)
    // ... other methods
  }
  ```
- **Features**: 
  - Media grid display
  - Thumbnail generation
  - Assignment state management
  - Filename editing
  - Drag-and-drop support
- **Dependencies**: None (standalone)
- **Reusability**: Can be used in any module requiring media selection

**2. Live Preview Library (`observation-report-live-preview.js`)**
- **Purpose**: Standalone component for real-time document preview
- **API**:
  ```javascript
  class ObservationReportLivePreview {
    constructor(containerId, options)
    updateContent(text, assignments, sections)
    renderPlaceholderTable(placeholder, mediaList)
    updateSectionStates(sections)
    // ... other methods
  }
  ```
- **Features**:
  - Real-time preview rendering
  - Placeholder table generation
  - Section rendering with collapsible behavior
  - Media embedding (images, video/PDF/MP3 filenames)
- **Dependencies**: None (standalone)
- **Reusability**: Can be used in any module requiring document preview

**3. Standards Library (`observation-report-standards.js`)**
- **Purpose**: Standalone component for standards/AC management
- **Status**: NEW implementation (do not reuse existing standards.js)
- **API**:
  ```javascript
  class ObservationReportStandards {
    constructor(containerId, options)
    loadStandards(jsonFileId)
    searchStandards(keyword)
    expandUnit(unitId)
    onSectionClick(callback)
    // ... other methods
  }
  ```
- **Features**:
  - Unit/AC display
  - Search functionality
  - AC coverage detection
  - Section navigation
- **Dependencies**: None (standalone)
- **Reusability**: Already designed as standalone, can be reused

**4. Preview Draft Library (`observation-report-preview-draft.js`)**
- **Purpose**: Standalone component for preview dialog functionality
- **API**:
  ```javascript
  class ObservationReportPreviewDraft {
    constructor(options)
    open(content, assignments, sections)
    updateSettings(settings)
    exportDOCX(callback)
    // ... other methods
  }
  ```
- **Features**:
  - 3-column resizable layout
  - Section navigation
  - Preview rendering
  - Actions panel
  - Font settings
  - Element visibility toggles
- **Dependencies**: LivePreview library, ColumnResizer library
- **Reusability**: Can be used in any module requiring document preview dialog

**5. Column Resizer Library (`column-resizer.js`)**
- **Purpose**: Standalone utility for resizable column layouts
- **API**:
  ```javascript
  class ColumnResizer {
    constructor(containerId, options)
    addResizer(leftColumn, rightColumn, options)
    saveWidths(storageKey)
    loadWidths(storageKey)
    // ... other methods
  }
  ```
- **Features**:
  - Drag-to-resize functionality
  - Minimum width constraints
  - localStorage persistence
  - Multiple column support
- **Dependencies**: None (standalone)
- **Reusability**: Can be used in any module requiring resizable layouts

#### Client-Side Processing (API-Free Design)
- **Placeholder Extraction**: Regex pattern matching (in LivePreview library)
- **Placeholder Validation**: Client-side validation (in LivePreview library)
- **Color Assignment**: Rainbow color palette assignment (in LivePreview library)
- **Preview Generation**: Real-time HTML rendering (in LivePreview library)
- **State Management**: Module-scoped state objects (not global)
- **Media Assignment Tracking**: In-memory data structures (in MediaBrowser library)

#### Library Integration Pattern
```javascript
// Main orchestrator pattern
import { MediaBrowser } from './libs/media-browser.js';
import { LivePreview } from './libs/live-preview.js';
import { Standards } from './libs/standards.js';
import { PreviewDraft } from './libs/preview-draft.js';
import { ColumnResizer } from './libs/column-resizer.js';

// Initialize libraries
const mediaBrowser = new MediaBrowser('mediaBrowserContainer', {...});
const livePreview = new LivePreview('livePreviewContainer', {...});
const standards = new Standards('standardsContainer', {...});
const previewDraft = new PreviewDraft({...});

// Connect libraries via events/callbacks
mediaBrowser.onMediaSelect((media) => {
  // Handle media selection
});

livePreview.onPlaceholderUpdate((placeholder, media) => {
  // Update assignments
});
```

#### No External Dependencies
- No jQuery
- No React/Vue/Angular
- No Bootstrap/Material UI
- Pure vanilla JavaScript (ES6+ modules)
- Standalone libraries with clear APIs

### Data Storage

#### File System
- **Draft Storage**: JSON files in `/output/.drafts/`
- **Media Files**: Located in `/output/{qualification}/{learner}/`
- **DOCX Output**: Saved to `/output/`

#### Data Formats
- **Drafts**: JSON format
  ```json
  {
    "draft_name": "string",
    "text_content": "string",
    "qualification": "string",
    "learner": "string",
    "assignments": {},
    "header_data": {},
    "assessor_feedback": "string",
    "created_at": "ISO datetime",
    "updated_at": "ISO datetime"
  }
  ```

- **Media Metadata**: In-memory JavaScript objects
- **API Responses**: JSON format

### Configuration

#### Paths (from `config.py`)
- `OUTPUT_FOLDER`: Base output directory
- `MEDIA_CONVERTER_INPUT_FOLDER`: Media converter input (if different)
- Draft path: `{OUTPUT_FOLDER}/.drafts/`
- DOCX output: `{OUTPUT_FOLDER}/`

### Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- HTML5 drag-and-drop support required
- ES6+ JavaScript features

---

## Data Models

### Media File Object
```javascript
{
  path: "/full/path/to/file.jpg",
  name: "file.jpg",
  type: "image" | "video" | "pdf" | "audio",
  size: 1234567,  // bytes
  width: 1920,    // pixels (images/videos)
  height: 1080,   // pixels (images/videos)
  duration: 30.5, // seconds (videos/audio only)
  thumbnail_path: "/path/to/thumbnail.jpg",  // null for PDF/MP3
  qualification: "Inter",
  learner: "John_Doe",
  subfolder: "folder1"  // if nested
}
```

### Placeholder Assignment
```javascript
{
  "placeholder_name_lowercase": [
    {
      path: "/path/to/media1.jpg",
      type: "image",
      order: 0  // Position in table (0 = Row 0, Col 0)
    },
    {
      path: "/path/to/video1.mp4",
      type: "video",
      order: 1  // Position in table (1 = Row 0, Col 1)
    }
  ]
}
```

### Draft Data Structure
```json
{
  "draft_name": "Site_Report_v1",
  "text_content": "Full text with {{placeholders}}...",
  "qualification": "Inter",
  "learner": "John_Doe",
  "units": "all" | ["641", "642", "643"],  // "all" or array of specific unit codes
  "assignments": {
    "site_arrival_induction": [
      {
        "path": "/path/to/image1.jpg",
        "type": "image",
        "order": 0
      },
      {
        "path": "/path/to/video1.mp4",
        "type": "video",
        "order": 1
      },
      {
        "path": "/path/to/document.pdf",
        "type": "pdf",
        "order": 2
      },
      {
        "path": "/path/to/audio.mp3",
        "type": "audio",
        "order": 3
      }
    ]
  },
  "header_data": {
    "learner": "John Doe",
    "assessor": "Jane Smith",
    "visit_date": "2025-01-15",
    "location": "Site A",
    "address": "123 Main St"
  },
  "assessor_feedback": "Feedback text here...",
  "standards_data": {},  // Standards JSON data if loaded
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T14:30:00Z"
}
```

### Section Data Structure
```javascript
{
  id: "section-0",
  title: "Health and Safety",
  color: "#667eea",
  content: "Text content...",
  placeholders: ["site_arrival_induction", "safety_briefing"],
  isExpanded: false,
  index: 0
}
```

---

## API Endpoints

**⚠️ Note**: All API endpoints use `/observation-report/*` routes (NEW routes)

### Media Management
```
GET  /observation-report/learners
     Query params: qualification
     Returns: List of learners for qualification

GET  /observation-report/media
     Query params: qualification, learner
     Returns: List of media files with metadata
```

### Draft Management
```
GET    /observation-report/drafts
       Returns: List of all drafts with metadata

POST   /observation-report/drafts
       Body: { draft_name, text_content, assignments, qualification, units, ... }
       Creates new draft

GET    /observation-report/drafts/<draft_id>
       Returns: Draft data

PUT    /observation-report/drafts/<draft_id>
       Body: { text_content, assignments, ... }
       Updates existing draft

DELETE /observation-report/drafts/<draft_id>
       Deletes draft
```

### DOCX Export
```
POST   /observation-report/export-docx
       Body: {
         text_content,
         assignments,
         filename (optional, defaults to draft_name),
         font_size,
         font_name,
         header_data,
         assessor_feedback
       }
       Returns: { success, file_name, download_url }

GET    /observation-report/download-docx/<filename>
       Downloads generated DOCX file
```

### File Operations
```
POST   /observation-report/rename-file
       Body: { old_path, new_name }
       Renames media file
       Returns: { success, new_path }
```

---

## File Structure

### ⚠️ IMPORTANT: NEW Module Structure - No Legacy Code

All files must be **NEW implementations**. Do NOT copy or transfer code from any existing modules.

### Backend Files (NEW)
```
app/
├── observation_report_scanner.py      # NEW: Media scanning logic
├── observation_report_docx_generator.py  # NEW: DOCX generation
├── observation_report_placeholder_parser.py  # NEW: Placeholder utilities
├── observation_report_draft_manager.py  # NEW: Draft management
└── routes.py                          # NEW: Add /observation-report/* routes
```

### Frontend Files (NEW - Standalone Libraries)

**⚠️ IMPORTANT**: All library files use unique names with `observation-report-` prefix to avoid conflicts with existing files.

```
static/
├── js/
│   ├── observation-report/
│   │   ├── observation-report-media-browser.js    # NEW: Standalone Media Browser Library
│   │   ├── observation-report-live-preview.js     # NEW: Standalone Live Preview Library
│   │   ├── observation-report-standards.js        # NEW: Standalone Standards Library
│   │   ├── observation-report-preview-draft.js   # NEW: Standalone Preview Draft Library
│   │   └── observation-report-column-resizer.js  # NEW: Standalone Column Resizer Library
│   └── observation-report.js                     # NEW: Main orchestrator
└── css/
    ├── observation-report/
    │   ├── observation-report-media-browser.css   # NEW: Media Browser styles
    │   ├── observation-report-live-preview.css   # NEW: Live Preview styles
    │   ├── observation-report-standards.css       # NEW: Standards styles
    │   ├── observation-report-preview-draft.css   # NEW: Preview Draft styles
    │   └── observation-report-column-resizer.css # NEW: Column Resizer styles
    └── observation-report.css                     # NEW: Main module styles
```

**Note**: Files are organized in `observation-report/` subdirectory to keep them separate from existing files.

### Templates (NEW)
```
templates/
└── observation_report.html           # NEW: Main HTML template
    - Includes top navigation with "Observation Report" tab
    - Page container with 95% width, centered
    - 3-column resizable layout
```

### CSS Requirements

**Page Layout CSS**:
```css
.observation-report-container {
    width: 95%;
    max-width: 95%;
    margin: 0 auto;  /* Center horizontally */
    padding: 20px;
    background: #1e1e1e;  /* Dark theme background */
    color: #e0e0e0;  /* Dark theme text */
}

/* Top Navigation */
.top-navigation {
    background: #2a2a2a;  /* Dark theme panel */
    border-bottom: 1px solid #555;
}

.top-navigation .tab-observation-report {
    color: #e0e0e0;
    background: #2a2a2a;
}

.top-navigation .tab-observation-report.active {
    background: #1e1e1e;
    color: #667eea;  /* Accent color for active tab */
    border-bottom: 2px solid #667eea;
}

/* Dark Theme - Text Inputs */
.observation-report-container input[type="text"],
.observation-report-container input[type="date"],
.observation-report-container input[type="number"] {
    background: #1e1e1e;
    color: #e0e0e0;
    border: 1px solid #555;
    padding: 8px 12px;
    border-radius: 4px;
}

.observation-report-container input::placeholder {
    color: #999;
    opacity: 0.7;
}

.observation-report-container input:focus {
    outline: none;
    border-color: #667eea;
    background: #2a2a2a;
}

/* Dark Theme - Textarea */
.observation-report-container textarea {
    background: #1e1e1e;
    color: #e0e0e0;
    border: 1px solid #555;
    padding: 8px 12px;
    border-radius: 4px;
    resize: vertical;
}

.observation-report-container textarea::placeholder {
    color: #999;
    opacity: 0.7;
}

.observation-report-container textarea:focus {
    outline: none;
    border-color: #667eea;
    background: #2a2a2a;
}

/* Dark Theme - Scrollbar */
.observation-report-container ::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

.observation-report-container ::-webkit-scrollbar-track {
    background: #1e1e1e;
}

.observation-report-container ::-webkit-scrollbar-thumb {
    background: #555;
    border-radius: 5px;
}

.observation-report-container ::-webkit-scrollbar-thumb:hover {
    background: #666;
}

/* Dark Theme - Select/Dropdown */
.observation-report-container select {
    background: #1e1e1e;
    color: #e0e0e0;
    border: 1px solid #555;
    padding: 8px 12px;
    border-radius: 4px;
}

.observation-report-container select:focus {
    outline: none;
    border-color: #667eea;
    background: #2a2a2a;
}

.observation-report-container select option {
    background: #1e1e1e;
    color: #e0e0e0;
}

/* Dark Theme - Icons */
.observation-report-container .icon {
    color: #e0e0e0;
}

.observation-report-container .icon:hover {
    color: #fff;
}

.observation-report-container .icon.active {
    color: #667eea;  /* Accent color */
}

/* Dark Theme - Buttons */
.observation-report-container button {
    background: #2a2a2a;
    color: #e0e0e0;
    border: 1px solid #555;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
}

.observation-report-container button:hover {
    background: #333;
    border-color: #667eea;
}

.observation-report-container button.primary {
    background: #667eea;
    color: #fff;
    border-color: #5568d3;
}

.observation-report-container button.primary:hover {
    background: #5568d3;
}

/* Dark Theme - Checkboxes */
.observation-report-container input[type="checkbox"] {
    accent-color: #667eea;
    background: #1e1e1e;
    border: 1px solid #555;
}

/* Dark Theme - Disabled Elements */
.observation-report-container input:disabled,
.observation-report-container textarea:disabled,
.observation-report-container select:disabled,
.observation-report-container button:disabled {
    background: #1a1a1a;
    color: #666;
    border-color: #333;
    opacity: 0.5;
    cursor: not-allowed;
}
```

### Configuration
```
config.py                            # Paths, settings (may need new constants)
```

### Navigation Integration

**Top Navigation Structure**:
- Add "Observation Report" tab to existing navigation
- Tab order: Video to Image | Media Converter | AC Matrix | **Observation Report**
- Active tab highlighting
- Tab links to `/observation-report`

### Library Dependencies

**⚠️ IMPORTANT**: All library files use unique names to avoid conflicts with existing files.

**Standalone Libraries** (no dependencies between them):
- `observation-report-media-browser.js` - Independent
- `observation-report-live-preview.js` - Independent
- `observation-report-standards.js` - Independent (NEW implementation)
- `observation-report-column-resizer.js` - Independent

**Libraries with Dependencies**:
- `observation-report-preview-draft.js` - Uses `observation-report-live-preview.js` and `observation-report-column-resizer.js`

**Main Orchestrator**:
- `observation-report.js` - Uses all libraries, coordinates interactions

---

## Standalone Libraries Architecture

### Overview

For high efficiency and maintainability, the Observation Report module should be built using **standalone, reusable libraries**. Each major component should be a self-contained library with a clear API.

### Library Design Principles

1. **Independence**: Each library should work independently
2. **Clear API**: Well-defined public interface
3. **Event-Driven**: Libraries communicate via events/callbacks
4. **No Global State**: Each library manages its own state
5. **Testable**: Each library can be unit tested independently
6. **Reusable**: Libraries can be used in other modules

### Library Communication Pattern

```javascript
// Event-driven communication between libraries
// All libraries use ObservationReport prefix to avoid conflicts
this.mediaBrowser.on('mediaSelected', (media) => {
  // Media selected - update assignments
  assignmentManager.addMedia(media);
  // Notify preview to update
  this.livePreview.updateAssignments(assignmentManager.getAssignments());
});

this.livePreview.on('placeholderClick', (placeholder) => {
  // Placeholder clicked - show assignment dialog
  showAssignmentDialog(placeholder);
});

this.standards.on('sectionClick', (sectionId) => {
  // Section clicked in standards - expand in preview
  this.livePreview.expandSection(sectionId);
});
```

### Library Specifications

#### 1. Media Browser Library

**File**: `static/js/observation-report/observation-report-media-browser.js`

**Purpose**: Standalone component for browsing and selecting media files

**API**:
```javascript
class ObservationReportMediaBrowser {
  constructor(containerId, options = {})
  
  // Methods
  loadMedia(qualification, learner)  // Load media for qualification/learner
  updateAssignmentState(assignments)  // Update which media is assigned
  setMediaList(mediaList)             // Set media list programmatically
  refresh()                           // Refresh media display
  
  // Events
  on(event, callback)                 // Subscribe to events
  off(event, callback)                // Unsubscribe from events
  
  // Events emitted:
  // - 'mediaSelect': (media) => void
  // - 'mediaDeselect': (media) => void
  // - 'mediaDragStart': (media) => void
  // - 'filenameUpdate': (media, newName) => void
}
```

**Features**:
- Media grid display with thumbnails
- Assignment state visualization (disabled/grayed out)
- Filename inline editing
- Drag-and-drop support
- Multi-select support
- File type indicators (IMG/VID/PDF/MP3)
- Scrollable grid layout

**Dependencies**: None

**Reusability**: Can be used in any module requiring media file selection

---

#### 2. Live Preview Library

**File**: `static/js/observation-report/observation-report-live-preview.js`

**Purpose**: Standalone component for real-time document preview rendering

**API**:
```javascript
class ObservationReportLivePreview {
  constructor(containerId, options = {})
  
  // Methods
  updateContent(text, assignments, sections)  // Update preview content
  renderPlaceholderTable(placeholder, mediaList)  // Render single placeholder table
  updateSectionStates(sections)              // Update section expand/collapse states
  expandSection(sectionId)                    // Expand specific section
  collapseSection(sectionId)                  // Collapse specific section
  scrollToSection(sectionId)                  // Scroll to section
  
  // Events
  on(event, callback)
  off(event, callback)
  
  // Events emitted:
  // - 'placeholderClick': (placeholder) => void
  // - 'sectionToggle': (sectionId, isExpanded) => void
  // - 'mediaRemove': (placeholder, mediaPath) => void
}
```

**Features**:
- Real-time preview rendering
- Placeholder detection and highlighting
- 2-column table generation for placeholders
- Section rendering with collapsible behavior
- Media embedding (images embedded, videos/PDFs/MP3s as filenames)
- Dark theme support
- Rainbow color coding for placeholders

**Dependencies**: None

**Reusability**: Can be used in any module requiring document preview

---

#### 3. Standards Library

**File**: `static/js/observation-report/observation-report-standards.js`

**Purpose**: Standalone component for standards/AC management

**Status**: NEW implementation (do not reuse existing standards.js)

**API**:
```javascript
class ObservationReportStandards {
  constructor(containerId, options = {})
  
  // Methods
  loadStandards(jsonFileId)          // Load standards from JSON file
  searchStandards(keyword)            // Search AC text
  clearSearch()                       // Clear search and restore states
  expandUnit(unitId)                  // Expand specific unit
  collapseUnit(unitId)                // Collapse specific unit
  expandAllUnits()                    // Expand all units
  collapseAllUnits()                   // Collapse all units
  updateCoverage(textContent)          // Update AC coverage based on text
  
  // Events
  on(event, callback)
  off(event, callback)
  
  // Events emitted:
  // - 'sectionClick': (sectionId) => void  // When section name clicked in "Covered:"
  // - 'unitToggle': (unitId, isExpanded) => void
}
```

**Features**:
- Unit/AC display with expand/collapse
- AC ID and AC text display
- AC coverage detection from text content
- "Covered:" section links (clickable to navigate to preview section)
- Search functionality with keyword highlighting
- Unit dropdown for filtering (if implemented)

**Dependencies**: None

**Reusability**: Already designed as standalone, can be reused

---

#### 4. Preview Draft Library

**File**: `static/js/observation-report/observation-report-preview-draft.js`

**Purpose**: Standalone component for preview dialog functionality

**API**:
```javascript
class ObservationReportPreviewDraft {
  constructor(options = {})
  
  // Methods
  open(content, assignments, sections, headerData, assessorFeedback)  // Open preview dialog
  close()                             // Close preview dialog
  updateContent(content, assignments)  // Update preview content
  updateSettings(settings)             // Update font settings, visibility toggles
  exportDOCX(options)                 // Trigger DOCX export
  updateDraft(options)                // Update draft
  
  // Events
  on(event, callback)
  off(event, callback)
  
  // Events emitted:
  // - 'close': () => void
  // - 'exportDOCX': (options) => void
  // - 'updateDraft': (options) => void
  // - 'settingsChange': (settings) => void
}
```

**Features**:
- 3-column resizable layout (Sections | Preview | Actions)
- Section navigation
- Preview content rendering
- Actions panel (font settings, visibility toggles)
- DOCX export trigger
- Draft update trigger

**Dependencies**: 
- `ObservationReportLivePreview` library (for preview rendering)
- `ObservationReportColumnResizer` library (for resizable layout)

**Reusability**: Can be used in any module requiring document preview dialog

---

#### 5. Column Resizer Library

**File**: `static/js/observation-report/observation-report-column-resizer.js`

**Purpose**: Standalone utility for resizable column layouts

**API**:
```javascript
class ObservationReportColumnResizer {
  constructor(containerId, options = {})
  
  // Methods
  addResizer(leftColumnId, rightColumnId, options)  // Add resizer between two columns
  saveWidths(storageKey)                            // Save column widths to localStorage
  loadWidths(storageKey)                            // Load column widths from localStorage
  resetWidths()                                     // Reset to default widths
  
  // Events
  on(event, callback)
  off(event, callback)
  
  // Events emitted:
  // - 'resize': (leftWidth, rightWidth) => void
}
```

**Features**:
- Drag-to-resize functionality
- Minimum width constraints
- localStorage persistence
- Multiple column support (can handle 3+ columns)
- Smooth resize animation

**Dependencies**: None

**Reusability**: Can be used in any module requiring resizable layouts

---

### Main Orchestrator Pattern

**File**: `static/js/observation-report.js`

**Purpose**: Coordinates all libraries and manages module-level state

**Pattern**:
```javascript
import { ObservationReportMediaBrowser } from './observation-report/observation-report-media-browser.js';
import { ObservationReportLivePreview } from './observation-report/observation-report-live-preview.js';
import { ObservationReportStandards } from './observation-report/observation-report-standards.js';
import { ObservationReportPreviewDraft } from './observation-report/observation-report-preview-draft.js';
import { ObservationReportColumnResizer } from './observation-report/observation-report-column-resizer.js';

class ObservationReport {
  constructor() {
    // Initialize libraries
    this.mediaBrowser = new ObservationReportMediaBrowser('mediaBrowserContainer', {...});
    this.livePreview = new ObservationReportLivePreview('livePreviewContainer', {...});
    this.standards = new ObservationReportStandards('standardsContainer', {...});
    this.previewDraft = new ObservationReportPreviewDraft({...});
    this.columnResizer = new ObservationReportColumnResizer('mainContainer', {...});
    
    // Module-level state
    this.state = {
      assignments: {},
      textContent: '',
      sections: [],
      headerData: {},
      assessorFeedback: ''
    };
    
    // Connect libraries
    this.setupEventHandlers();
  }
  
  setupEventHandlers() {
    // Media browser events
    this.mediaBrowser.on('mediaSelect', (media) => {
      this.handleMediaSelect(media);
    });
    
    // Live preview events
    this.livePreview.on('placeholderClick', (placeholder) => {
      this.handlePlaceholderClick(placeholder);
    });
    
    // Standards events
    this.standards.on('sectionClick', (sectionId) => {
      this.livePreview.expandSection(sectionId);
    });
    
    // ... more event handlers
  }
  
  // Module-level methods
  handleMediaSelect(media) { /* ... */ }
  handlePlaceholderClick(placeholder) { /* ... */ }
  // ... other methods
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  window.observationReport = new ObservationReport();
});
```

### Benefits of Standalone Libraries

1. **High Efficiency**:
   - Each library is optimized for its specific purpose
   - No unnecessary code in each library
   - Better performance through focused implementations

2. **Maintainability**:
   - Changes to one library don't affect others
   - Clear boundaries between components
   - Easier to debug and fix issues

3. **Testability**:
   - Each library can be unit tested independently
   - Mock dependencies easily
   - Test libraries in isolation

4. **Reusability**:
   - Libraries can be used in other modules
   - Standards library already reusable
   - Media Browser can be used in other contexts

5. **Scalability**:
   - Easy to add new features to specific libraries
   - Can swap implementations without affecting others
   - Can add new libraries as needed

---

## Key Implementation Details

### Page Layout & Navigation

#### Page Width Requirement
- **Page Width**: Must be **95% of viewport width** (not 100%)
- **Centering**: Page content must be centered horizontally
- **Implementation**:
  ```css
  .observation-report-container {
    width: 95%;
    max-width: 95%;
    margin: 0 auto;
    padding: 20px;
  }
  ```
- **Responsive**: Maintains 95% width on all screen sizes

#### Top Navigation Integration
- **Navigation Tab**: Add "Observation Report" to top navigation
- **Tab Order**: Video to Image | Media Converter | AC Matrix | **Observation Report**
- **Active State**: Highlight "Observation Report" tab when module is active
- **Route**: Tab links to `/observation-report`
- **Implementation**: Add tab to existing navigation structure in base template

### Placeholder Pattern
- **Regex**: `/\{\{([A-Za-z0-9_]+)\}\}/g`
- **Rules**: 
  - Must use double curly braces
  - Alphanumeric and underscores only
  - Case-insensitive matching
  - No spaces allowed

### Color Palette
```javascript
const PLACEHOLDER_COLORS = [
  '#ff6b6b',  // Red
  '#4ecdc4',  // Cyan
  '#45b7d1',  // Blue
  '#f9ca24',  // Yellow
  '#6c5ce7',  // Purple
  '#a29bfe',  // Lavender
  '#fd79a8',  // Pink
  '#00b894',  // Green
];
```

### Table Layout Logic
- **2-column tables** for each placeholder
- **Cell assignment**: Left-to-right, top-to-bottom
  - Position 0 → Row 0, Col 0
  - Position 1 → Row 0, Col 1
  - Position 2 → Row 1, Col 0
  - Position 3 → Row 1, Col 1
  - etc.

### Section Detection
- **Pattern**: `SECTION xxxx` (case-insensitive)
- **Variations**: `SECTION: xxxx`, `SECTION - xxxx`
- **Content**: All text after section marker until next section or end

### DOCX Styling
- **Page Size**: A4 (8.27" × 11.69")
- **Font**: Times New Roman (default), configurable
- **Font Size**: 16pt (default), configurable
- **Table Borders**: 1px solid black
- **Margins**: 1 inch (default)

---

## Summary

This specification documents the complete requirements for creating a **NEW "Observation Report" module**. This is a **fresh implementation** - no legacy code should be transferred.

### Key Points:
- **NEW Module**: All code must be written fresh
- **Standalone Libraries**: Components should be implemented as reusable libraries
- **No Legacy Code**: Do NOT copy code from any existing modules
- **Modular Architecture**: High efficiency through standalone, testable components

### Specification Includes:
- **13 detailed workflows** covering all user interactions (including Standards workflow)
- **11 core features** with implementation details (including Standards integration)
- **Text wireframes** for all major UI components (3-column resizable layout)
- **Complete technology stack** (backend and frontend)
- **Standalone library architecture** recommendations
- **Data models** for all data structures (including PDF/MP3 support)
- **API endpoints** for server communication
- **File structure** for new module organization

### Key Features:
- **Page Layout**: 95% viewport width (centered, not full width)
- **Navigation**: Added as "Observation Report" tab in top navigation
- **Media Support**: PDF and MP3 support (filenames only in tables, similar to videos)
- **Draft System**: Qualification and units selection (all units or specific units)
- **DOCX Export**: No validation requirement; filename follows draft name
- **Media Management**: Filename editing capability
- **Standards Integration**: Standalone Standards library with full workflow
- **Resizable Layout**: 3-column layout (Media Browser | Live Preview | Standards) - user resizable
- **Preview Window**: 3-column resizable layout (Sections | Preview | Actions)
- **Collapsible Fields**: Header, Text Editor, and Assessor Feedback are separate collapsed sections at bottom

### Standalone Libraries Recommended:
1. **Media Browser Library** - For media file browsing and selection
2. **Live Preview Library** - For real-time document preview rendering
3. **Standards Library** - For standards/AC management (may already exist)
4. **Preview Draft Library** - For preview dialog functionality
5. **Column Resizer Library** - For resizable column layouts

This document serves as a comprehensive reference for understanding the module and can be used as a blueprint for creating similar modules (e.g., "Observation Report").

---

**Document Status**: Complete Specification
**Version**: 1.0
**Created**: 2025-01-XX

