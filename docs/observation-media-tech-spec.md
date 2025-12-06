# Observation Media Module - Technical Specification

## Document Information
- **Version**: 1.0
- **Date**: 2025-01-XX
- **Status**: 📋 **DRAFT - AWAITING APPROVAL**
- **Based on**: observation_media_idea.md
- **Module Name**: Observation Media

---

## 1. Overview

### 1.1 Purpose
Create a module that allows users to assign photos and videos from a specific folder to placeholders within text content. The placeholders are rendered as tables (2 columns, 1 media per cell), and the final document is exported as a DOCX file.

### 1.2 Key Features
- **Media Browser**: Display thumbnails of photos/videos from output folder subfolders
- **Subfolder Selection**: User selects specific subfolder from `/Users/rom/Documents/nvq/v2p-formatter-output`
- **Placeholder System**: Text contains placeholders like `{{Site_Arrival_Induction}}` that get replaced with media tables
- **Table Format**: Each placeholder becomes a 2-column table with 1 media item per cell
- **Media Assignment**: Once assigned, media is disabled in UI to prevent duplicate assignments
- **Drag & Drop**: Reorganize media assignments and order
- **Live Preview**: See text with media tables in real-time
- **Draft System**: Save work-in-progress drafts with custom names for future editing
- **DOCX Export**: Save the final document with embedded media to output folder

### 1.3 Use Case
Users working with observation reports or documentation that require:
- Structured text content with embedded media
- Consistent table-based media presentation
- Ability to assign specific media to specific placeholders
- Professional document output (DOCX format)

---

## 2. Functional Requirements

### 2.1 Media Management

#### FR-1: Media Folder Selection
- **Requirement**: User selects a subfolder from the output folder containing media files
- **Base Path**: `/Users/rom/Documents/nvq/v2p-formatter-output`
- **Subfolder Selection**: 
  - User selects specific subfolder from dropdown/list
  - Scan selected subfolder for media files (non-recursive, only direct files)
  - Display available subfolders in output directory
- **Supported Formats**: 
  - Images: JPG, JPEG, PNG
  - Videos: MP4, MOV
- **Behavior**: 
  - List all subfolders in output directory
  - User selects one subfolder
  - Scan selected subfolder for media files
  - Display thumbnails in media browser
  - Show file metadata (name, size, dimensions, duration for videos)

#### FR-2: Media Thumbnail Display
- **Requirement**: Show visual thumbnails for all media files
- **Display Mode**: 
  - Show ALL media files (no pagination, no "load more")
  - If multiple subfolders exist, split/group media by subfolder
  - Each subfolder shown as a section with header
- **Image Thumbnails**: 
  - Generate or use existing thumbnails
  - Size: 120x90px or similar
  - Maintain aspect ratio
- **Video Thumbnails**: 
  - Extract frame at 1 second or first frame
  - Show play icon overlay
  - Display duration badge
- **Scrolling**: Vertical scrolling for media grid

#### FR-3: Media Selection & Assignment
- **Requirement**: User can select media and assign to placeholders
- **Selection Methods**:
  - Click to select media
  - Multi-select with Ctrl/Cmd + click
  - Select all / Deselect all
- **Assignment**:
  - Drag media to placeholder
  - Click placeholder, then click media
  - Right-click menu: "Assign to placeholder"
- **Assignment State**:
  - Once media is assigned to any placeholder, it becomes **disabled** in the media browser
  - Disabled media shows grayed-out appearance
  - Disabled media cannot be selected or assigned again
  - Media can only be used once (one placeholder per media item)

### 2.2 Placeholder System

#### FR-4: Placeholder Detection
- **Requirement**: Detect placeholders in text content
- **Format**: `{{Placeholder_Name}}`
- **Examples**: 
  - `{{Site_Arrival_Induction}}`
  - `{{Safety_Briefing}}`
  - `{{Equipment_Check}}`
- **Behavior**:
  - Parse text for all `{{...}}` patterns
  - Extract placeholder names
  - Create assignment interface for each placeholder

#### FR-5: Placeholder to Table Conversion
- **Requirement**: Each placeholder becomes a 2-column table
- **Table Structure**:
  - 2 columns, equal width
  - 1 media item maximum per cell
  - If video: display filename only (not embedded video)
  - If image: embed image in cell
- **Layout Rules**:
  - Images: Fit within cell, maintain aspect ratio
  - Videos: Text only (filename)
  - Empty cells: Just empty (no placeholder text or indicators)

#### FR-6: Media Order Management
- **Requirement**: User can reorganize media order within placeholders
- **Methods**:
  - Drag and drop within placeholder assignment list
  - Up/Down arrow buttons
  - Reorder controls in media list
- **Behavior**:
  - Order determines table cell placement (left to right, top to bottom)
  - First media → Row 1, Column 1
  - Second media → Row 1, Column 2
  - Third media → Row 2, Column 1
  - And so on...

### 2.3 User Interface

#### FR-7: Split-Panel Layout
- **Requirement**: Two-column interface
- **Theme**: Dark theme throughout
- **Left Panel**: Media browser and assignment controls
  - Media thumbnails grid (shows all media, grouped by subfolder if multiple)
  - Assignment status indicators
  - Media order controls
- **Right Panel**: Text editor and preview
  - Text input area (dark theme, rainbow placeholder colors)
  - Live preview of document (dark theme)
  - Placeholder assignment indicators
- **Accessibility**:
  - Font size toggle: Regular / Big
  - Quick access button in header/toolbar
  - Applies to all text in interface

#### FR-8: Text Editor
- **Requirement**: Text input area for content with placeholders
- **Theme**: Dark theme (matches overall application theme)
- **Features**:
  - Rainbow color coding for placeholders (each placeholder gets unique color)
  - Syntax highlighting for placeholders
  - Placeholder validation
  - Auto-complete for placeholder names
  - Line numbers (optional)
- **Input Methods**:
  - Direct typing
  - Paste from external source
- **Scrolling**: Vertical scrolling

#### FR-9: Live Preview
- **Requirement**: Real-time preview of document with media
- **Theme**: Dark theme (matches overall application theme)
- **Display**:
  - Rendered text with placeholder tables
  - Actual media in table cells
  - Empty cells: Just empty (no placeholder text, no indicators)
- **Update Frequency**: Real-time as user makes changes
- **Scrolling**: Vertical scrolling

### 2.4 Document Export & Draft Management

#### FR-10: DOCX Generation
- **Requirement**: Export final document as DOCX
- **Output Path**: `/Users/rom/Documents/nvq/v2p-formatter-output`
- **Content**:
  - All text content
  - Tables with embedded images
  - Video filenames as text
  - Proper formatting and styling
- **File Handling**:
  - Embed images in document
  - Include video filenames (not video files themselves)
  - Maintain table structure
  - Preserve text formatting
- **File Naming**: User-specified name in save dialog

#### FR-11: Draft Management
- **Requirement**: Save and load work-in-progress drafts with custom names
- **Save Draft**:
  - User clicks "💾 Save Draft" button
  - Dialog appears: "Enter draft name: [________]"
  - User provides custom name for draft
  - Save draft data to JSON file in `.drafts/` subfolder
  - Draft includes: text content, placeholder assignments, media order, selected subfolder
  - Success message: "Draft '{name}' saved successfully"
- **Load Draft**:
  - User clicks "📥 Load Draft" button
  - Dialog shows list of saved drafts with:
    - Draft name
    - Date created
    - Date last modified
  - User selects draft from list
  - Load draft restores: text, assignments, media order, subfolder selection
  - User can continue editing from saved state
- **Draft Storage**: 
  - Location: `/Users/rom/Documents/nvq/v2p-formatter-output/.drafts/` (hidden folder)
  - Format: JSON files named `{draft_name}.json`
  - Metadata: Creation date, last modified date
- **Draft Management**:
  - List all drafts
  - Delete draft option
  - Draft names must be unique

---

## 3. Technical Architecture

### 3.1 Backend Components

#### 3.1.1 Media Scanner Module
```python
# app/observation_media_scanner.py
- list_output_subfolders() -> List[str]  # List subfolders in output directory
- scan_media_subfolder(subfolder_name) -> List[MediaFile]  # Scan specific subfolder
- get_media_thumbnail(media_path) -> bytes
- get_media_info(media_path) -> Dict
```

**MediaFile Structure**:
```python
{
    'path': str,
    'name': str,
    'type': 'image' | 'video',
    'size': int,
    'width': int,  # for images/videos
    'height': int,  # for images/videos
    'duration': float,  # for videos only
    'thumbnail_path': str
}
```

#### 3.1.2 Placeholder Parser Module
```python
# app/placeholder_parser.py
- extract_placeholders(text) -> List[str]
- validate_placeholders(text, assigned_media) -> Dict
- render_preview(text, media_assignments) -> str (HTML)
```

#### 3.1.3 Document Generator Module
```python
# app/observation_docx_generator.py
- generate_docx(text, media_assignments, output_path, filename) -> Path
- create_media_table(media_list) -> Table
- embed_image_in_cell(cell, image_path) -> None
```

#### 3.1.4 Draft Manager Module
```python
# app/observation_draft_manager.py
- save_draft(draft_name, text, assignments, subfolder) -> bool
- load_draft(draft_name) -> Dict
- list_drafts() -> List[Dict]  # Returns list of draft metadata
- delete_draft(draft_name) -> bool
```

### 3.2 Frontend Components

#### 3.2.1 Media Browser Component
- Grid layout for thumbnails
- Selection state management
- Drag and drop handlers
- Filter/search UI

#### 3.2.2 Placeholder Assignment Component
- List of detected placeholders
- Media assignment interface
- Order management controls
- Status indicators (assigned/unassigned)

#### 3.2.3 Text Editor Component
- Textarea with syntax highlighting
- Placeholder detection and highlighting
- Auto-complete dropdown
- Validation feedback

#### 3.2.4 Preview Component
- Live rendering of document
- Table rendering with media
- Scroll synchronization (optional)

### 3.3 API Endpoints

#### 3.3.1 Media Management
```
GET  /media-converter/observation-media/subfolders
GET  /media-converter/observation-media/media/<subfolder>
GET  /media-converter/observation-media/thumbnail/<path>
GET  /media-converter/observation-media/info/<path>
```

#### 3.3.2 Placeholder Management
```
POST /media-converter/observation-media/parse-placeholders
POST /media-converter/observation-media/validate-placeholders
GET  /media-converter/observation-media/preview
```

#### 3.3.3 Document Generation
```
POST /media-converter/observation-media/generate-docx
GET  /media-converter/observation-media/download/<file_path>
```

#### 3.3.4 Draft Management
```
POST /media-converter/observation-media/save-draft
GET  /media-converter/observation-media/list-drafts
GET  /media-converter/observation-media/load-draft/<draft_name>
DELETE /media-converter/observation-media/delete-draft/<draft_name>
```

---

## 4. User Interface Design

### 4.1 Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 🎬 Observation Media                                                    │
│                                                                         │
│ ┌──────────────────────────────┬─────────────────────────────────────┐ │
│ │                              │                                     │ │
│ │   MEDIA BROWSER (Left)       │   TEXT & PREVIEW (Right)            │ │
│ │                              │                                     │ │
│ │  ┌────────────────────────┐  │  ┌───────────────────────────────┐ │ │
│ │  │ 🔍 Search: [_______]   │  │  │ 📝 Text Editor                │ │ │
│ │  └────────────────────────┘  │  │ ┌─────────────────────────────┐│ │ │
│ │                              │  │ │                             ││ │ │
│ │  ┌────────────────────────┐  │  │ │  Text with {{placeholders}}││ │ │
│ │  │ 📁 Folder: [Select...] │  │  │ │                             ││ │ │
│ │  └────────────────────────┘  │  │ │                             ││ │ │
│ │                              │  │ └─────────────────────────────┘│ │ │
│ │  ┌────────────────────────┐  │  │                                 │ │ │
│ │  │ Media Thumbnails Grid  │  │  │ ┌───────────────────────────┐ │ │ │
│ │  │                        │  │  │ │ 📄 Live Preview            │ │ │ │
│ │  │ [IMG] [IMG] [VID]      │  │  │ │                           │ │ │ │
│ │  │ [IMG] [VID] [IMG]      │  │  │ │  Rendered text with       │ │ │ │
│ │  │ [VID] [IMG] [IMG]      │  │  │ │  media tables...          │ │ │ │
│ │  │                        │  │  │ │                           │ │ │ │
│ │  └────────────────────────┘  │  │ └───────────────────────────┘ │ │ │
│ │                              │  │                                 │ │ │
│ │  ┌────────────────────────┐  │  │                                 │ │ │
│ │  │ Placeholder Assignments│  │  │                                 │ │ │
│ │  │                        │  │  │                                 │ │ │
│ │  │ {{Site_Arrival}}       │  │  │                                 │ │ │
│ │  │   [IMG] [VID] [IMG]    │  │  │                                 │ │ │
│ │  │   [↑] [↓] [Remove]     │  │  │                                 │ │ │
│ │  │                        │  │  │                                 │ │ │
│ │  │ {{Safety_Briefing}}    │  │  │                                 │ │ │
│ │  │   [No media assigned]  │  │  │                                 │ │ │
│ │  └────────────────────────┘  │  │                                 │ │ │
│ │                              │  │                                 │ │ │
│ └──────────────────────────────┴─────────────────────────────────────┘ │
│                                                                         │
│ [💾 Save as DOCX]  [🔄 Reset]  [📥 Load Template]                      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Component Details

#### 4.2.1 Media Browser Panel
- **Header**:
  - Subfolder selector dropdown (lists subfolders from output directory)
  - Refresh button
  - Media count display
  - Selected subfolder display
  - Font size toggle: [Regular] [Big]
- **Note**: Search functionality not included
- **Media Grid**:
  - Shows ALL media files (no pagination)
  - If multiple subfolders: Group by subfolder with section headers
  - Vertical scrolling
  - Example structure:
    ```
    ┌─────────────────────────────┐
    │ 📁 Subfolder: folder1       │
    │ ┌────┐ ┌────┐ ┌────┐       │
    │ │IMG │ │VID │ │IMG │       │
    │ └────┘ └────┘ └────┘       │
    ├─────────────────────────────┤
    │ 📁 Subfolder: folder2       │
    │ ┌────┐ ┌────┐              │
    │ │IMG │ │VID │              │
    │ └────┘ └────┘              │
    └─────────────────────────────┘
    ```
- **Thumbnail Grid**:
  - Responsive grid (3-4 columns)
  - Hover effects (only for unassigned media)
  - Selection indicators (checkmark overlay)
  - Drag handles (only for unassigned media)
  - **Disabled State**: 
    - Grayed-out appearance (opacity: 0.5)
    - No hover effects
    - No click/drag interaction
    - Visual indicator showing "Assigned" badge
- **Media Info**:
  - Filename
  - File size
  - Dimensions/duration
  - Assignment status badge (Assigned/Unassigned)

#### 4.2.2 Placeholder Assignment Panel
- **Placeholder List**:
  - Each placeholder as expandable card
  - Assignment status (assigned/unassigned/partial)
  - Media count indicator
- **Media Assignment Area**:
  - Drop zone for each placeholder
  - Assigned media thumbnails
  - Reorder controls (drag handles, up/down arrows)
  - Remove buttons
- **Visual Indicators**:
  - Green: Fully assigned
  - Yellow: Partially assigned
  - Red: Unassigned

#### 4.2.3 Text Editor Panel
- **Theme**: Dark theme (dark background, light text)
- **Editor**:
  - Rainbow color coding for placeholders (each unique color)
  - Syntax highlighting for placeholders
  - Line numbers (optional)
  - Word count
  - Placeholder count
  - Vertical scrolling
- **Toolbar**:
  - Font size toggle: [Regular] [Big]
  - Format buttons (bold, italic, etc.)
  - Insert placeholder button
  - Validate button
  - Clear button

#### 4.2.4 Preview Panel
- **Theme**: Dark theme (dark background, light text)
- **Rendered View**:
  - Text with tables
  - Embedded images
  - Video filenames
  - Vertical scrolling
- **Table Rendering**:
  - 2-column layout
  - Images embedded
  - Video filenames as text
  - Empty cells: Just empty (no text, no indicators)

---

## 5. Data Models

### 5.1 Media Assignment Structure
```python
{
    'placeholder_name': 'Site_Arrival_Induction',
    'media_items': [
        {
            'path': '/path/to/image1.jpg',
            'type': 'image',
            'order': 0
        },
        {
            'path': '/path/to/video1.mp4',
            'type': 'video',
            'order': 1
        },
        {
            'path': '/path/to/image2.jpg',
            'type': 'image',
            'order': 2
        }
    ]
}
```

### 5.2 Document State
```python
{
    'text_content': str,
    'selected_subfolder': str,  # Subfolder name from output directory
    'placeholders': List[str],
    'assignments': Dict[str, List[MediaItem]],
    'draft_name': str (optional),
    'created_at': datetime (optional),
    'updated_at': datetime (optional)
}
```

### 5.3 Draft Data Structure
```python
{
    'draft_name': str,
    'text_content': str,
    'selected_subfolder': str,
    'placeholders': List[str],
    'assignments': Dict[str, List[MediaItem]],
    'created_at': str,  # ISO format
    'updated_at': str   # ISO format
}
```

### 5.4 Table Generation Logic
```python
# For each placeholder with N media items:
# Generate table with 2 columns
# Fill cells left-to-right, top-to-bottom:
# 
# Media 0 → Row 0, Col 0
# Media 1 → Row 0, Col 1
# Media 2 → Row 1, Col 0
# Media 3 → Row 1, Col 1
# Media 4 → Row 2, Col 0
# etc.
```

---

## 6. Questions & Clarifications Needed

### 6.1 Folder & Media Management

**Q1: Folder Selection** ✅ **RESOLVED**
- **Answer**: Fixed path `/Users/rom/Documents/nvq/v2p-formatter-output`
- User selects specific subfolder from dropdown
- No folder browsing UI needed
- Subfolder selection saved in draft

**Q2: Media File Handling** ✅ **RESOLVED**
- **Answer**: Reference original files from output folder subfolder
- Videos: Filename only in DOCX (not embedded)
- Media files are in output folder, so they should be stable
- If file deleted: Show error in preview, disable assignment

**Q3: Media Limits** ✅ **RESOLVED**
- **Answer**: No maximum limit per placeholder
- Table grows as needed (rows added for each pair of media)
- "1 media max per cell" rule enforced (2 columns, fills left-to-right, top-to-bottom)

### 6.2 Placeholder System

**Q4: Placeholder Format**
- Are placeholders case-sensitive? (`{{Site_Arrival}}` vs `{{site_arrival}}`) = no
- Can placeholders contain spaces? (`{{Site Arrival}}` vs `{{Site_Arrival}}`) = no
- Should we support placeholder attributes? (`{{Site_Arrival|width=500}}`) = no need

**Q5: Placeholder Validation**
- What happens if text contains a placeholder but no media is assigned?
  - Show empty table?
  - Show placeholder text?
  - Show warning/error?
- Should we validate that all placeholders have media before export?

**Q6: Placeholder Naming**
- Are placeholder names user-defined or predefined?
- Should we provide a list of common placeholders?
- Can users create custom placeholders?

### 6.3 Table Layout

**Q7: Table Structure**
- Should tables have borders?
- What cell padding/spacing?
- Should images fill the entire cell or maintain aspect ratio with padding?
- What if a placeholder has an odd number of media items? (Last row has 1 cell)

**Q8: Video Handling**
- For videos in tables: Just filename text, or filename + thumbnail?
- Should video filenames be clickable links in DOCX?
- What format for video filename display? (Full path, just name, name + duration?)

**Q9: Media Ordering**
- When user drags media to reorder, does it affect:
  - Only the current placeholder?
  - All placeholders using that media?
  - Global media order?

### 6.4 Text Editor

**Q10: Text Formatting**
- Should the text editor support rich text (bold, italic, etc.)?
- Or plain text only?
- Should formatting be preserved in DOCX export?

**Q11: Template System**
- Should users be able to save/load text templates?
- Should templates include placeholder definitions?
- Should we provide default templates?

**Q12: Placeholder Insertion**
- Should users be able to insert placeholders via UI button?
- Or only by typing `{{...}}`?
- Should we provide placeholder autocomplete/suggestions?

### 6.5 Export & Output

**Q13: DOCX Styling**
- What document styling should be applied?
  - Font family, size?
  - Headers/footers?
  - Page margins?
  - Table styling?
- Should styling be customizable?

**Q14: Image Embedding**
- Should images be:
  - Embedded at full resolution?
  - Resized to fit table cells?
  - Compressed for file size?
- What maximum image dimensions in tables?

**Q15: File Naming** ✅ **RESOLVED**
- **Answer**: User-specified name when saving DOCX
- Files saved to: `/Users/rom/Documents/nvq/v2p-formatter-output`
- Drafts saved to: `/Users/rom/Documents/nvq/v2p-formatter-output/.drafts/`

### 6.6 User Experience

**Q16: Workflow** ✅ **RESOLVED**
- **Answer**: Integrated into Media Converter page as new tab
- Route: `/v2p-formatter/media-converter` with tab navigation
- Tab name: "Observation Media"
- Media comes from output folder subfolders (where Media Converter saves files)
- Draft system allows "New Document" and "Edit Existing" workflows

**Q17: Persistence** ✅ **RESOLVED**
- **Answer**: Manual save draft functionality
- User clicks "Save Draft" button
- User provides custom name for draft
- Drafts can be loaded later for editing
- Multiple drafts supported (list of saved drafts)

**Q18: Preview**
- Should preview update in real-time or on-demand?
- Should preview be scrollable independently from editor?
- Should preview show exact DOCX rendering or simplified view?

---

## 7. Staged Development Plan

### Overview
This development plan is divided into 6 stages, each with specific deliverables, acceptance criteria, and comprehensive tests. Each stage builds upon the previous one and should be completed and tested before moving to the next.

---

### Stage 1: Core Infrastructure & Basic UI
**Duration**: 3-4 days  
**Goal**: Set up basic module structure and UI layout

#### Tasks:
1. Add "Observation Media" tab to Media Converter page
2. Create route handlers for observation media endpoints
3. Implement subfolder listing from output directory (`/Users/rom/Documents/nvq/v2p-formatter-output`)
4. Set up basic split-panel UI layout (left: media browser, right: text editor & preview)
5. Implement dark theme styling
6. Add font size toggle (Regular/Big) in header

#### Deliverables:
- New tab "Observation Media" visible in Media Converter page
- Basic split-panel layout rendered
- Subfolder dropdown lists all subfolders from output directory
- Dark theme applied throughout
- Font size toggle functional

#### Tests:

**Unit Tests:**
```python
# test_observation_media_infrastructure.py

def test_list_output_subfolders():
    """Test listing subfolders from output directory"""
    # Test: Returns list of subfolder names
    # Test: Handles empty output directory
    # Test: Filters out hidden files/folders
    # Test: Returns sorted list

def test_route_observation_media_tab():
    """Test observation media tab route"""
    # Test: Route returns 200
    # Test: Template renders correctly
    # Test: Tab is visible in navigation

def test_font_size_toggle():
    """Test font size toggle functionality"""
    # Test: Toggle switches between regular and big
    # Test: Preference persists in session
    # Test: Applies to all text elements
```

**Integration Tests:**
```python
def test_subfolder_dropdown_integration():
    """Test subfolder dropdown integration"""
    # Test: Dropdown populates with actual subfolders
    # Test: Selecting subfolder triggers media scan
    # Test: Empty state handled gracefully
```

**UI Tests:**
- [ ] Tab appears in Media Converter navigation
- [ ] Split-panel layout renders correctly
- [ ] Dark theme applied to all panels
- [ ] Font size toggle visible and functional
- [ ] Subfolder dropdown visible and populated

#### Acceptance Criteria:
- ✅ Tab visible and accessible
- ✅ Basic layout structure in place
- ✅ Dark theme consistent
- ✅ Font size toggle works
- ✅ All tests pass

---

### Stage 2: Media Browser & Thumbnail Display
**Duration**: 4-5 days  
**Goal**: Display all media files with thumbnails, grouped by subfolder

#### Tasks:
1. Implement media scanner for selected subfolder
2. Add thumbnail generation/caching (reuse existing thumbnail generator)
3. Implement media grid display (all media, no pagination)
4. Group media by subfolder if multiple subfolders exist
5. Display media metadata (filename, size, dimensions/duration)
6. Implement vertical scrolling for media grid
7. Add refresh functionality

#### Deliverables:
- Media thumbnails displayed in grid
- Media grouped by subfolder with section headers
- All media visible (no pagination)
- Thumbnails for images and videos
- Metadata displayed for each media item
- Vertical scrolling functional

#### Tests:

**Unit Tests:**
```python
# test_observation_media_scanner.py

def test_scan_media_subfolder():
    """Test scanning media files from subfolder"""
    # Test: Returns list of media files (JPG, JPEG, PNG, MP4, MOV)
    # Test: Filters out non-media files
    # Test: Returns file metadata (path, name, type, size, dimensions)
    # Test: Handles empty subfolder
    # Test: Handles non-existent subfolder

def test_get_media_info():
    """Test getting media file information"""
    # Test: Returns correct file type (image/video)
    # Test: Returns dimensions for images
    # Test: Returns duration for videos
    # Test: Returns file size
    # Test: Handles corrupted files gracefully

def test_group_media_by_subfolder():
    """Test grouping media by subfolder"""
    # Test: Groups media correctly by subfolder
    # Test: Handles single subfolder (no grouping needed)
    # Test: Handles multiple subfolders
    # Test: Maintains order
```

**Integration Tests:**
```python
def test_media_browser_display():
    """Test media browser displays all media"""
    # Test: All media files displayed
    # Test: Thumbnails generated/cached correctly
    # Test: Subfolder grouping works
    # Test: Metadata displayed correctly
    # Test: Vertical scrolling functional
```

**UI Tests:**
- [ ] Media thumbnails display correctly
- [ ] All media visible (no "Load More")
- [ ] Media grouped by subfolder with headers
- [ ] Thumbnails for images and videos
- [ ] Video thumbnails show play icon and duration
- [ ] Metadata (filename, size) displayed
- [ ] Vertical scrolling works
- [ ] Refresh button updates media list

#### Acceptance Criteria:
- ✅ All media files displayed
- ✅ Thumbnails generated and cached
- ✅ Subfolder grouping functional
- ✅ No pagination ("Load More" removed)
- ✅ All tests pass

---

### Stage 3: Placeholder System & Text Editor
**Duration**: 5-6 days  
**Goal**: Implement placeholder detection, text editor with rainbow colors, and validation

#### Tasks:
1. Implement placeholder parser (detect `{{Placeholder_Name}}` patterns)
2. Create text editor component (plain text, dark theme)
3. Implement rainbow color coding for placeholders
4. Add placeholder validation (highlight unassigned placeholders)
5. Implement placeholder detection in real-time
6. Add text editor features (word count, placeholder count)
7. Implement vertical scrolling for text editor

#### Deliverables:
- Placeholder detection working
- Text editor with dark theme
- Rainbow color coding applied to placeholders
- Unassigned placeholders highlighted
- Real-time placeholder detection
- Word count and placeholder count displayed

#### Tests:

**Unit Tests:**
```python
# test_placeholder_parser.py

def test_extract_placeholders():
    """Test extracting placeholders from text"""
    # Test: Detects {{Placeholder_Name}} format
    # Test: Case-insensitive matching
    # Test: Handles underscores (no spaces)
    # Test: Returns unique placeholders
    # Test: Handles empty text
    # Test: Handles text without placeholders

def test_validate_placeholders():
    """Test placeholder validation"""
    # Test: Identifies unassigned placeholders
    # Test: Returns list of unassigned placeholder names
    # Test: Handles all placeholders assigned
    # Test: Handles no placeholders in text

def test_rainbow_color_assignment():
    """Test rainbow color assignment to placeholders"""
    # Test: Each placeholder gets unique color
    # Test: Colors cycle through palette
    # Test: Same placeholder always gets same color
    # Test: Handles many placeholders (color cycling)
```

**Integration Tests:**
```python
def test_text_editor_placeholder_detection():
    """Test real-time placeholder detection in editor"""
    # Test: Placeholders detected as user types
    # Test: Rainbow colors applied immediately
    # Test: Unassigned placeholders highlighted
    # Test: Word count updates in real-time
    # Test: Placeholder count updates in real-time
```

**UI Tests:**
- [ ] Text editor displays with dark theme
- [ ] Placeholders detected and highlighted
- [ ] Rainbow colors applied to each placeholder
- [ ] Unassigned placeholders visually highlighted
- [ ] Word count updates as user types
- [ ] Placeholder count updates as user types
- [ ] Vertical scrolling works
- [ ] Plain text only (no rich text)

#### Acceptance Criteria:
- ✅ Placeholder detection working
- ✅ Rainbow color coding functional
- ✅ Unassigned placeholders highlighted
- ✅ Real-time updates working
- ✅ All tests pass

---

### Stage 4: Media Assignment & Disabled State
**Duration**: 5-6 days  
**Goal**: Implement media assignment to placeholders with disabled state

#### Tasks:
1. Implement placeholder assignment interface
2. Add media selection (click to assign)
3. Implement drag-and-drop assignment
4. Add media disabled state when assigned
5. Implement assignment removal
6. Add visual feedback for assignments
7. Update placeholder status indicators

#### Deliverables:
- Media can be assigned to placeholders
- Assigned media becomes disabled (grayed out)
- Drag-and-drop assignment working
- Click-to-assign working
- Remove assignment functionality
- Status indicators update (✅/⚠️/❌)

#### Tests:

**Unit Tests:**
```python
# test_media_assignment.py

def test_assign_media_to_placeholder():
    """Test assigning media to placeholder"""
    # Test: Media assigned successfully
    # Test: Media marked as assigned
    # Test: Media disabled in browser
    # Test: Placeholder status updates
    # Test: Cannot assign same media twice

def test_remove_media_assignment():
    """Test removing media from placeholder"""
    # Test: Media removed from assignment
    # Test: Media re-enabled in browser
    # Test: Placeholder status updates
    # Test: Media can be reassigned

def test_media_disabled_state():
    """Test media disabled state"""
    # Test: Assigned media shows disabled appearance
    # Test: Disabled media cannot be clicked
    # Test: Disabled media cannot be dragged
    # Test: Visual indicator (grayed out, badge)
```

**Integration Tests:**
```python
def test_media_assignment_workflow():
    """Test complete media assignment workflow"""
    # Test: Select placeholder → click media → assigned
    # Test: Drag media → drop on placeholder → assigned
    # Test: Media disabled after assignment
    # Test: Remove assignment → media re-enabled
    # Test: Multiple assignments work correctly
```

**UI Tests:**
- [ ] Media can be clicked to assign
- [ ] Media can be dragged to placeholder
- [ ] Assigned media becomes disabled (grayed out)
- [ ] Disabled media shows "Assigned" badge
- [ ] Disabled media cannot be clicked/dragged
- [ ] Remove button removes assignment
- [ ] Status indicators update correctly
- [ ] Visual feedback during assignment

#### Acceptance Criteria:
- ✅ Media assignment working (click and drag)
- ✅ Disabled state functional
- ✅ Assignment removal working
- ✅ Status indicators accurate
- ✅ All tests pass

---

### Stage 5: Media Ordering & Live Preview
**Duration**: 4-5 days  
**Goal**: Implement media reordering and live preview with tables

#### Tasks:
1. Implement media ordering within placeholders
2. Add drag-and-drop reordering
3. Add up/down arrow controls
4. Implement live preview with table rendering
5. Render 2-column tables for placeholders
6. Embed images in table cells
7. Display video filenames (just name) in cells
8. Handle empty cells (just empty, no text)
9. Apply table styling (black borders, 1px, A4 format)

#### Deliverables:
- Media can be reordered within placeholders
- Live preview updates in real-time
- Tables render with 2 columns
- Images embedded in cells
- Video filenames displayed (just name)
- Empty cells remain empty
- Table styling applied (borders, A4 format)

#### Tests:

**Unit Tests:**
```python
# test_media_ordering.py

def test_reorder_media():
    """Test reordering media within placeholder"""
    # Test: Media order updates correctly
    # Test: Order determines table cell positions
    # Test: First media → Row 0, Col 0
    # Test: Second media → Row 0, Col 1
    # Test: Third media → Row 1, Col 0
    # Test: Drag-and-drop reordering works
    # Test: Up/down arrows work

def test_table_generation():
    """Test table generation for placeholders"""
    # Test: 2-column table created
    # Test: Media placed in correct cells
    # Test: Images embedded correctly
    # Test: Video filenames displayed (just name)
    # Test: Empty cells remain empty
    # Test: Table borders applied (black, 1px)
```

**Integration Tests:**
```python
def test_live_preview_updates():
    """Test live preview updates in real-time"""
    # Test: Preview updates when media assigned
    # Test: Preview updates when media reordered
    # Test: Preview updates when media removed
    # Test: Tables render correctly
    # Test: Images display in cells
    # Test: Video filenames display correctly
```

**UI Tests:**
- [ ] Media can be reordered (drag-and-drop)
- [ ] Up/down arrows work
- [ ] Live preview updates in real-time
- [ ] Tables render with 2 columns
- [ ] Images embedded in cells
- [ ] Video filenames displayed (just name, no path)
- [ ] Empty cells remain empty (no text)
- [ ] Table borders visible (black, 1px)
- [ ] A4 page format maintained

#### Acceptance Criteria:
- ✅ Media ordering functional
- ✅ Live preview updates in real-time
- ✅ Tables render correctly
- ✅ Table styling applied
- ✅ All tests pass

---

### Stage 6: DOCX Export & Draft System
**Duration**: 5-6 days  
**Goal**: Implement DOCX generation and draft save/load functionality

#### Tasks:
1. Create DOCX generator for observation documents
2. Implement table generation with media in DOCX
3. Embed images in DOCX table cells
4. Add video filenames as text in cells
5. Apply table styling (borders, A4 format)
6. Implement draft save functionality
7. Implement draft load functionality
8. Add draft list/management UI
9. Add validation before export
10. Save DOCX to output folder with user-specified name

#### Deliverables:
- DOCX export functional
- Tables with media in DOCX
- Images embedded in DOCX
- Video filenames in DOCX
- Draft save/load working
- Draft management UI
- Validation before export

#### Tests:

**Unit Tests:**
```python
# test_docx_generator.py

def test_generate_docx():
    """Test DOCX generation"""
    # Test: DOCX file created successfully
    # Test: Text content included
    # Test: Placeholders replaced with tables
    # Test: Images embedded in cells
    # Test: Video filenames included (just name)
    # Test: Table borders applied (black, 1px)
    # Test: A4 page format maintained
    # Test: Empty cells remain empty

def test_draft_save():
    """Test saving draft"""
    # Test: Draft saved to .drafts/ folder
    # Test: Draft includes all state (text, assignments, subfolder)
    # Test: Draft name unique
    # Test: Metadata saved (created_at, updated_at)
    # Test: JSON format correct

def test_draft_load():
    """Test loading draft"""
    # Test: Draft loaded successfully
    # Test: All state restored (text, assignments, subfolder)
    # Test: Media assignments restored
    # Test: Media order restored
    # Test: Handles missing draft gracefully
```

**Integration Tests:**
```python
def test_docx_export_workflow():
    """Test complete DOCX export workflow"""
    # Test: User clicks "Save as DOCX"
    # Test: Validation runs (checks unassigned placeholders)
    # Test: If validation fails: error shown
    # Test: If validation passes: DOCX generated
    # Test: File saved to output folder
    # Test: User-specified filename used
    # Test: Success message with download link

def test_draft_workflow():
    """Test complete draft workflow"""
    # Test: User saves draft with name
    # Test: Draft appears in draft list
    # Test: User loads draft
    # Test: All state restored correctly
    # Test: User can continue editing
```

**UI Tests:**
- [ ] "Save as DOCX" button functional
- [ ] Validation runs before export
- [ ] Unassigned placeholders highlighted in validation
- [ ] DOCX file generated correctly
- [ ] File saved to output folder
- [ ] Success message with download link
- [ ] "Save Draft" button functional
- [ ] Draft name dialog appears
- [ ] Draft saved successfully
- [ ] "Load Draft" button functional
- [ ] Draft list displays correctly
- [ ] Draft loads and restores state

#### Acceptance Criteria:
- ✅ DOCX export functional
- ✅ Tables with media in DOCX
- ✅ Draft save/load working
- ✅ Validation functional
- ✅ All tests pass

---

### Testing Strategy

#### Test Types:
1. **Unit Tests**: Test individual functions/modules in isolation
2. **Integration Tests**: Test interactions between components
3. **UI Tests**: Manual testing checklist for each stage
4. **End-to-End Tests**: Complete user workflows

#### Test Coverage Goals:
- Unit tests: 80%+ code coverage
- Integration tests: All major workflows
- UI tests: All user-facing features
- E2E tests: Critical user paths

#### Test Execution:
- Run tests before each commit
- Run full test suite before stage completion
- All tests must pass before moving to next stage
- Fix failing tests before proceeding

#### Test Files Structure:
```
tests/
├── test_observation_media_infrastructure.py
├── test_observation_media_scanner.py
├── test_placeholder_parser.py
├── test_media_assignment.py
├── test_media_ordering.py
├── test_docx_generator.py
├── test_draft_manager.py
└── test_integration_workflows.py
```

---

### Dependencies Between Stages

```
Stage 1 (Infrastructure)
    ↓
Stage 2 (Media Browser)
    ↓
Stage 3 (Placeholder System)
    ↓
Stage 4 (Media Assignment)
    ↓
Stage 5 (Ordering & Preview)
    ↓
Stage 6 (Export & Drafts)
```

**Note**: Each stage must be completed and tested before proceeding to the next.

---

### Risk Mitigation

1. **Thumbnail Generation Performance**: Reuse existing thumbnail generator, implement caching
2. **Large Media Lists**: Show all media but optimize rendering (virtual scrolling if needed)
3. **DOCX Generation Complexity**: Use python-docx library, test with various media counts
4. **Draft File Management**: Implement proper error handling for file operations
5. **Browser Performance**: Optimize real-time preview updates (debounce if needed)

---

### Timeline Estimate

- **Stage 1**: 3-4 days
- **Stage 2**: 4-5 days
- **Stage 3**: 5-6 days
- **Stage 4**: 5-6 days
- **Stage 5**: 4-5 days
- **Stage 6**: 5-6 days

**Total Estimated Duration**: 26-32 days (5-6 weeks)

---

### Approval Checklist

Before starting development:
- [ ] Development plan reviewed
- [ ] Timeline approved
- [ ] Test strategy approved
- [ ] Dependencies understood
- [ ] Risk mitigation plan approved
- [ ] All questions answered
- [ ] Technical spec finalized

---

## 8. Dependencies

### 8.1 Backend
- **Existing**: 
  - Flask (routing)
  - python-docx (DOCX generation)
  - Pillow (image processing)
  - Existing thumbnail generator
- **New**: 
  - None (reuse existing modules)

### 8.2 Frontend
- **Existing**:
  - Vanilla JavaScript
  - Existing CSS framework
- **New**:
  - Drag-and-drop library (optional, can use native HTML5)
  - Syntax highlighting library (optional, for text editor)

---

## 9. File Structure

```
app/
├── observation_media_scanner.py    # Subfolder listing and media scanning
├── placeholder_parser.py            # Placeholder detection/parsing
├── observation_docx_generator.py   # DOCX generation with tables
├── observation_draft_manager.py    # Draft save/load functionality
└── routes.py                        # Add observation-media routes to media-converter

templates/
└── media_converter.html             # Add Observation Media tab section

static/
├── js/
│   └── observation-media.js        # Frontend logic
└── css/
    └── observation-media.css        # Module-specific styles
```

---

## 10. Success Criteria

### 10.1 Functional
- ✅ User can select subfolder from output directory and see thumbnails
- ✅ User can assign media to placeholders
- ✅ Assigned media becomes disabled in UI (cannot be reused)
- ✅ User can reorder media within placeholders
- ✅ Live preview shows text with media tables
- ✅ Empty table cells are just empty (no placeholder text)
- ✅ User can save drafts with custom names
- ✅ User can load and edit saved drafts
- ✅ DOCX export includes all text and media tables correctly
- ✅ DOCX saved to output folder with user-specified name

### 10.2 Performance
- Thumbnail generation: < 2 seconds for 100 files
- Preview update: < 500ms after assignment change
- DOCX generation: < 10 seconds for typical document

### 10.3 Usability
- Intuitive drag-and-drop workflow
- Clear visual feedback for assignments
- Helpful error messages
- Responsive design (desktop/tablet)

---

## 11. Resolved Questions Summary

**✅ Resolved Questions**:
1. **Folder Selection (Q1)**: Fixed path `/Users/rom/Documents/nvq/v2p-formatter-output`, user selects subfolder
2. **Media File Handling (Q2)**: Reference original files, videos as filename only
3. **Media Limits (Q3)**: No maximum, table grows as needed
4. **File Naming (Q15)**: User-specified name, saved to output folder
5. **Workflow (Q16)**: Integrated as tab in Media Converter page
6. **Persistence (Q17)**: Manual save draft with custom names

**Remaining Questions** ✅ **ALL RESOLVED**:
1. **Placeholder format rules (Q4)** ✅ **RESOLVED**
   - Case sensitivity: No (case-insensitive)
   - Spaces: No (underscores only, e.g., `{{Site_Arrival}}`)
   - Attributes: No (simple format only)

2. **Table styling requirements (Q7)** ✅ **RESOLVED**
   - Borders: Yes, black, 1px
   - Image sizing: Fit within 2-column table cells
   - Page format: A4
   - Padding: Standard table cell padding

3. **Text editor capabilities (Q10)** ✅ **RESOLVED**
   - Plain text only (no rich text formatting)

4. **Validation behavior (Q5)** ✅ **RESOLVED**
   - Unassigned placeholders: Highlight them (visual indicator)

5. **Video filename display format (Q8)** ✅ **RESOLVED**
   - Just the filename (e.g., "video1.mp4", not full path or duration)

---

## 12. Implementation Details

### 12.1 Integration with Media Converter
- **Tab Addition**: Add "Observation Media" as third tab in Media Converter page
- **Route**: Same route `/v2p-formatter/media-converter`, tab-based navigation
- **Tab Structure**:
  ```
  [Video to Image] [Media Converter] [Observation Media] ← Active
  ```

### 12.2 Media Source
- **Base Path**: `/Users/rom/Documents/nvq/v2p-formatter-output` (from config)
- **Subfolder Selection**: 
  - Scan output directory for subfolders
  - Display in dropdown: "Select Subfolder..."
  - User selects one subfolder
  - Scan that subfolder for media files (non-recursive)
- **Media Files**: All JPG, JPEG, PNG, MP4, MOV files in selected subfolder

### 12.3 Media Assignment Behavior
- **One-Time Assignment**: Each media file can only be assigned to ONE placeholder
- **Disabled State**: 
  - Once assigned, media thumbnail becomes disabled (grayed out, opacity 0.5)
  - Disabled media cannot be clicked, dragged, or selected
  - Visual indicator: "Assigned" badge or icon
- **Removal**: If user removes media from placeholder, it becomes available again

### 12.4 Draft System
- **Save Draft**:
  - Button: "💾 Save Draft"
  - Opens dialog: "Enter draft name: [________]"
  - Saves to: `/Users/rom/Documents/nvq/v2p-formatter-output/.drafts/{name}.json`
  - Includes: text, subfolder selection, all assignments, media order
- **Load Draft**:
  - Button: "📥 Load Draft"
  - Shows list of saved drafts (name, date created, date modified)
  - User selects draft to load
  - Restores all state: text, subfolder, assignments
- **Draft Management**:
  - List drafts with metadata
  - Delete draft option
  - Draft files: JSON format with all document state

### 12.5 DOCX Export
- **Output Location**: `/Users/rom/Documents/nvq/v2p-formatter-output`
- **File Naming**: User provides name in save dialog
- **Content**: 
  - All text with placeholders replaced by tables
  - Images embedded in table cells
  - Video filenames as text in cells
  - Empty cells remain empty

## 13. Next Steps

1. **Review & Approval**: Review this spec and answer remaining questions
2. **Wireframe Update**: Update wireframe with new requirements (disabled media, draft system)
3. **Prototype**: Build basic prototype with core functionality
4. **Testing**: User testing with sample data
5. **Iteration**: Refine based on feedback
6. **Implementation**: Full development following approved spec

---

## Version History

- **v1.0** (2025-01-XX): Initial technical specification
  - Based on observation_media_idea.md
  - Expanded with technical details
  - Added comprehensive Q&A section

