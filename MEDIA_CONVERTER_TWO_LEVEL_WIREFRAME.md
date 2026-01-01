# Media Converter Two-Level Dropdown System - Text Wireframe

## Current Structure
- Media converter scans all files from INPUT_FOLDER (`/Users/rom/Documents/nvq/v2p-formatter-input`)
- Files are displayed in two sections: Videos (MOV) and Images (JPG/PNG)
- No folder filtering - shows all files recursively
- Converted files are saved to OUTPUT_FOLDER (`/Users/rom/Documents/nvq/v2p-formatter-output`)

## Proposed Structure

### Folder Hierarchy

**Input Folder Structure** (`/Users/rom/Documents/nvq/v2p-formatter-input`):
```
/Users/rom/Documents/nvq/v2p-formatter-input/
├── Qualification1/          (First level - Qualifications)
│   ├── Learner1/            (Second level - Learners)
│   │   ├── MOV files...
│   │   ├── JPG files...
│   │   └── subfolders...
│   └── Learner2/
│       └── media files...
├── Qualification2/
│   ├── Learner1/
│   └── Learner2/
└── Qualification3/
    └── Learner1/
```

**Output Folder Structure** (`/Users/rom/Documents/nvq/v2p-formatter-output`):
```
/Users/rom/Documents/nvq/v2p-formatter-output/
├── Qualification1/
│   ├── Learner1/
│   │   └── converted files...
│   └── Learner2/
│       └── converted files...
└── Qualification2/
    └── Learner1/
        └── converted files...
```

## UI Layout

### Header Section (Top Bar)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Media Converter                                                           │
│                                                                           │
│ Select Qualification: [Dropdown ▼]  Select Learner: [Dropdown ▼] [Refresh] │
│                                                                           │
│ 🔍 Search files... [Search Box]                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### File Selection Section
```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. Select Media Files                                                    │
│                                                                           │
│ [Qualification/Learner filter applied - showing files from selected path]│
│                                                                           │
│ 🎬 Video Files (MOV) (X files)                                          │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ [Select All Videos] (X files, Y MB)                                │ │
│ │ ┌─────────────────────────────────────────────────────────────────┐ │ │
│ │ │ [✓] video1.mov (path: Qualification1/Learner1/video1.mov)      │ │ │
│ │ │ [✓] video2.mov (path: Qualification1/Learner1/video2.mov)      │ │ │
│ │ └─────────────────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│ 🖼️ Image Files (JPG/PNG) (Y files)                                       │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ [Select All Images] (Y files, Z MB)                                │ │
│ │ ┌─────────────────────────────────────────────────────────────────┐ │ │
│ │ │ [✓] image1.jpg (path: Qualification1/Learner1/image1.jpg)       │ │ │
│ │ │ [✓] image2.png (path: Qualification1/Learner1/image2.png)      │ │ │
│ │ └─────────────────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│ 📊 Selection Summary                                                      │
│ Videos Selected: X of Y | Images Selected: A of B | Total: Z files       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Conversion Settings Section
```
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. Conversion Settings                                                    │
│                                                                           │
│ [Video/Image settings as currently implemented]                         │
│                                                                           │
│ Output Location: /Users/rom/Documents/nvq/v2p-formatter-output/          │
│                  Qualification1/Learner1/                                │
│                                                                           │
│ [Convert Selected Files] button                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

## Dropdown States

### State 1: No Selection
- **Qualification dropdown**: Shows "Select Qualification..." + list of all top-level folders in INPUT_FOLDER
- **Learner dropdown**: **DISABLED** (grayed out), shows "Select Learner..."
- **File lists**: **EMPTY** or shows message "Please select a qualification and learner to view files"
- **Search box**: **DISABLED**
- **Convert button**: **DISABLED**

### State 2: Qualification Selected, No Learner
- **Qualification dropdown**: Shows selected qualification name
- **Learner dropdown**: **ENABLED**, shows "Select Learner..." + list of subfolders within selected qualification
- **File lists**: **EMPTY** or shows message "Please select a learner to view files"
- **Search box**: **DISABLED**
- **Convert button**: **DISABLED**

### State 3: Both Selected
- **Qualification dropdown**: Shows selected qualification name
- **Learner dropdown**: Shows selected learner name
- **File lists**: **POPULATED** - Shows only files from `INPUT_FOLDER/{qualification}/{learner}/` (recursively)
- **Search box**: **ENABLED**
- **Convert button**: **ENABLED** (when files are selected)
- **Output path**: Shows `OUTPUT_FOLDER/{qualification}/{learner}/` as target location

## Behavior Details

### 1. Qualification Dropdown
- Lists all direct subfolders of INPUT_FOLDER
- When changed:
  - Clears learner selection
  - Disables learner dropdown
  - Clears file lists
  - Disables search box
  - Enables learner dropdown
  - Populates learner dropdown with subfolders of selected qualification

### 2. Learner Dropdown
- Initially disabled
- Enabled when qualification is selected
- Lists all direct subfolders within selected qualification
- When changed:
  - Enables search box
  - Automatically loads files from `INPUT_FOLDER/{qualification}/{learner}/`
  - Updates file counts
  - Shows files in both Video and Image sections

### 3. File Loading
- **Automatic**: Files load automatically when learner is selected (no "Load" button needed)
- **Scope**: Scans `INPUT_FOLDER/{qualification}/{learner}/` recursively
- **File types**: MOV (videos), JPG, JPEG, PNG (images)
- **Display**: Shows files grouped by type (Videos/Images) as currently implemented

### 4. File Conversion
- **Output location**: `OUTPUT_FOLDER/{qualification}/{learner}/`
- **Path preservation**: Maintains relative folder structure within learner folder
- **Example**: 
  - Input: `INPUT_FOLDER/Qual1/Learner1/subfolder/video.mov`
  - Output: `OUTPUT_FOLDER/Qual1/Learner1/subfolder/video.mp4`

### 5. Refresh Button
- Reloads files for currently selected qualification/learner
- Updates file lists
- Preserves selections

### 6. URL Parameters
- `?qualification=QualificationName` - Auto-selects qualification
- `?learner=LearnerName` - Auto-selects learner (requires qualification)
- `?qualification=X&learner=Y` - Auto-selects both and loads files

## Data Flow

### Backend Changes:

1. **New Routes**:
   - `GET /media-converter/qualifications` - Lists top-level folders in INPUT_FOLDER
   - `GET /media-converter/learners?qualification=X` - Lists subfolders within qualification
   - `GET /media-converter/list?qualification=X&learner=Y` - Lists files filtered by qualification/learner

2. **Modified Routes**:
   - `GET /media-converter/list` - Add optional `qualification` and `learner` query parameters
   - `POST /media-converter/convert` - Ensure output goes to `OUTPUT_FOLDER/{qualification}/{learner}/`

3. **New Functions**:
   - `list_input_qualifications(input_folder)` - Lists top-level folders in INPUT_FOLDER
   - `list_input_learners(input_folder, qualification)` - Lists subfolders within qualification
   - `scan_media_files_filtered(input_folder, qualification, learner)` - Scans files within specific path

### Frontend Changes:

1. **Two dropdowns** added above file selection section
2. **Cascading enable/disable logic** for dropdowns
3. **Automatic file loading** when learner is selected
4. **File filtering** - only show files from selected qualification/learner path
5. **Output path display** - show where converted files will be saved

## Example Flow

1. User opens `/media-converter` → Sees qualification dropdown enabled, learner dropdown disabled, no files shown
2. User selects "Level 3 Diploma" → Learner dropdown enables, shows learners in that qualification
3. User selects "John Smith" → Files automatically load from `INPUT_FOLDER/Level 3 Diploma/John Smith/`
4. User sees videos and images from that path
5. User selects files and converts → Files saved to `OUTPUT_FOLDER/Level 3 Diploma/John Smith/`
6. User can change qualification/learner to work with different sets of files

## Edge Cases

- **No qualifications found**: Show message "No qualifications found in input folder"
- **No learners in qualification**: Learner dropdown shows "No learners found"
- **No files in learner folder**: Show "No files found" in file sections
- **Selected qualification deleted**: Reset to state 1, show error message
- **Selected learner deleted**: Reset learner selection, show error message
- **Empty learner folder**: Show "No media files found" in file sections
- **Files in root of qualification** (not in learner subfolder): Include in file list when qualification selected but no learner? (QUESTION)

## Questions for Clarification

### Question 1: File Scope
**Should files be filtered to ONLY show files within the selected qualification/learner path, or should it also include:**
- [ ] Option A: Only files directly in `INPUT_FOLDER/{qualification}/{learner}/` (and subfolders)
- [ ] Option B: Files in `INPUT_FOLDER/{qualification}/{learner}/` AND files directly in `INPUT_FOLDER/{qualification}/` (root level)
- [X ] Option C: All files recursively from `INPUT_FOLDER/{qualification}/{learner}/` (current behavior)

### Question 2: Output Location
**When converting files, should the output structure match the input structure?**
- [ ] Option A: Yes - `INPUT_FOLDER/Qual1/Learner1/subfolder/file.mov` → `OUTPUT_FOLDER/Qual1/Learner1/subfolder/file.mp4`
- [ ] Option B: No - All files go directly to `OUTPUT_FOLDER/Qual1/Learner1/` (flatten structure)
- [X ] Option C: Preserve relative path from learner folder: `INPUT_FOLDER/Qual1/Learner1/subfolder/file.mov` → `OUTPUT_FOLDER/Qual1/Learner1/subfolder/file.mp4`

### Question 3: Default Behavior
**When page loads with no selection:**
- [ X] Option A: Show no files (empty lists) until qualification/learner selected
- [ ] Option B: Show all files from INPUT_FOLDER (current behavior) until filters applied
- [ ] Option C: Auto-select first qualification/learner if available

### Question 4: Root Level Files
**If there are files directly in `INPUT_FOLDER/{qualification}/` (not in a learner subfolder):**
- [ ] Option A: Show them when qualification is selected but no learner selected
- [ ] Option B: Only show them if there's a special "Root" learner option
- [ X] Option C: Ignore them - only show files within learner folders

### Question 5: Multiple Pages
**Should this filtering apply to:**
- [ ] `/media-converter` page only
- [ ] `/media-converter` AND `/` (root/main page) 
- [X ] All pages that use INPUT_FOLDER

---

## Approval Required

Please review this wireframe and answer the questions above:
- [ ] Structure is correct (Qualifications → Learners → Files)
- [ ] UI behavior matches expectations
- [ ] Edge cases are handled appropriately
- [ ] Questions answered
- [ ] Ready to proceed with implementation




