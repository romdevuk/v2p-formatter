# Two-Level Dropdown System - Text Wireframe

## Current Structure
- Single dropdown showing all subfolders (learners) from OUTPUT_FOLDER
- Media browser shows immediately when subfolder is selected

## Proposed Structure

### Folder Hierarchy
```
/Users/rom/Documents/nvq/v2p-formatter-output/
├── Qualification1/          (First level - Qualifications)
│   ├── Learner1/            (Second level - Learners)
│   │   ├── media files...
│   │   └── subfolders...
│   └── Learner2/
│       └── media files...
├── Qualification2/
│   ├── Learner1/
│   └── Learner2/
└── Qualification3/
    └── Learner1/
```

### UI Layout

#### Header Section (Top Bar)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ [Current Draft Display] (if draft loaded)                               │
│                                                                           │
│ Select Qualification: [Dropdown ▼]  Select Learner: [Dropdown ▼] [Load] │
│                                                                           │
│ [Text Size: Aa AA]  [Load Draft]                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Dropdown States

**State 1: No Selection**
- Qualification dropdown: Shows "Select Qualification..." + list of all top-level folders
- Learner dropdown: **DISABLED** (grayed out), shows "Select Learner..."
- Load button: **DISABLED**
- Media browser: Shows message "Please select a qualification and learner"

**State 2: Qualification Selected, No Learner**
- Qualification dropdown: Shows selected qualification name
- Learner dropdown: **ENABLED**, shows "Select Learner..." + list of subfolders within selected qualification
- Load button: **DISABLED** (waiting for learner selection)
- Media browser: Shows message "Please select a learner"

**State 3: Both Selected**
- Qualification dropdown: Shows selected qualification name
- Learner dropdown: Shows selected learner name
- Load button: **ENABLED**
- Media browser: **ACTIVE** - Shows media files from: `OUTPUT_FOLDER/Qualification/Learner/`

### Behavior Details

1. **Qualification Dropdown**
   - Lists all direct subfolders of OUTPUT_FOLDER
   - When changed:
     - Clears learner selection
     - Disables learner dropdown
     - Clears media browser
     - Enables learner dropdown
     - Populates learner dropdown with subfolders of selected qualification

2. **Learner Dropdown**
   - Initially disabled
   - Enabled when qualification is selected
   - Lists all direct subfolders within selected qualification
   - When changed:
     - Enables Load button
     - Media browser remains empty until Load is clicked

3. **Load Button**
   - Only enabled when both qualification and learner are selected
   - On click:
     - Loads media from: `OUTPUT_FOLDER/{qualification}/{learner}/`
     - Displays media browser with files
     - Updates file count
     - Shows subfolders and root files as currently implemented

4. **Refresh Button**
   - Reloads page
   - Preserves selections via URL parameters: `?qualification=X&learner=Y`

5. **URL Parameters**
   - `?qualification=QualificationName` - Auto-selects qualification
   - `?learner=LearnerName` - Auto-selects learner (requires qualification)
   - `?qualification=X&learner=Y` - Auto-selects both and loads media

### Data Flow

**Backend Changes:**
1. `list_qualifications()` - Lists top-level folders in OUTPUT_FOLDER
2. `list_learners(qualification)` - Lists subfolders within qualification
3. `scan_media_subfolder(qualification, learner)` - Scans media in learner folder

**Frontend Changes:**
1. Two separate dropdowns instead of one
2. Cascading enable/disable logic
3. Load button only enabled when both selected
4. Media browser path: `OUTPUT_FOLDER/{qualification}/{learner}/`

### Example Flow

1. User opens page → Sees qualification dropdown enabled, learner dropdown disabled
2. User selects "Level 3 Diploma" → Learner dropdown enables, shows learners in that qualification
3. User selects "John Smith" → Load button enables
4. User clicks Load → Media browser shows files from `.../Level 3 Diploma/John Smith/`
5. User can browse, assign media, etc. as before

### Edge Cases

- **No qualifications found**: Show message "No qualifications found in output folder"
- **No learners in qualification**: Learner dropdown shows "No learners found"
- **Selected qualification deleted**: Reset to state 1, show error message
- **Selected learner deleted**: Reset learner selection, show error message
- **Empty learner folder**: Show "No media files found" in media browser

---

## Approval Required

Please review this wireframe and confirm:
- [ ] Structure is correct (Qualifications → Learners → Media)
- [ ] UI behavior matches expectations
- [ ] Edge cases are handled appropriately
- [ ] Ready to proceed with implementation




