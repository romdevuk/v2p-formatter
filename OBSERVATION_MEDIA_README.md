# Observation Media Module

## Overview
The Observation Media module allows users to assign photo/video media to placeholders within a text document, with live preview and DOCX export functionality.

## Features

### ✅ Core Features
- **Media Browser**: Browse media files from subfolders in the output directory
- **Placeholder System**: Detect and highlight placeholders in text (format: `{{Placeholder_Name}}`)
- **Media Assignment**: Drag-and-drop or click-to-assign media to placeholders
- **Live Preview**: Real-time preview with 2-column tables showing assigned media
- **DOCX Export**: Export final document with embedded images and video filenames
- **Draft System**: Save and load drafts with all state (text, assignments, subfolder)

### ✅ UI Features
- **Dark Theme**: Consistent dark theme throughout
- **Font Size Toggle**: Switch between regular and big font sizes
- **Rainbow Colors**: Each placeholder gets a unique color for easy identification
- **Validation**: Visual feedback for unassigned placeholders
- **Disabled State**: Assigned media becomes disabled and shows "✓ Assigned" badge

## Architecture

### API-Free Design
The module is designed to be **API-free** for most operations:
- All data is embedded in the page on load (server-side rendering)
- Placeholder parsing, validation, and preview generation are client-side
- Only DOCX export and draft management use API calls (necessary for file operations)

### File Structure
```
app/
├── observation_media_scanner.py    # Scan media files from subfolders
├── placeholder_parser.py           # Parse and validate placeholders
├── observation_docx_generator.py  # Generate DOCX files
├── draft_manager.py                # Save/load drafts
└── routes.py                        # API routes (export, drafts)

static/js/
└── observation-media.js            # Client-side logic (API-free)

templates/
└── media_converter.html            # UI template with embedded data
```

## Usage

### 1. Access the Module
Navigate to: `http://localhost/v2p-formatter/media-converter`
Click on the **"Observation Media"** tab

### 2. Select Subfolder
- Choose a subfolder from the dropdown
- Media files from that subfolder will be displayed in the grid

### 3. Enter Text with Placeholders
- Type your text in the text editor
- Use placeholders like: `{{Site_Arrival_Induction}}`
- Placeholders must:
  - Use double curly braces: `{{}}`
  - Use underscores (no spaces): `{{Placeholder_Name}}`
  - Be case-insensitive

### 4. Assign Media to Placeholders
**Method 1: Drag and Drop**
- Drag a media card from the grid
- Drop it on a placeholder table in the preview area
- Select the placeholder from the dialog

**Method 2: Click to Assign**
- Click on a media card
- Select the placeholder from the dialog

### 5. Reorder Media (Optional)
- Drag media within a placeholder table to reorder
- Media will be arranged in 2-column tables (left to right, top to bottom)

### 6. Save Draft (Optional)
- Click "💾 Save Draft"
- Enter a name for your draft
- Draft saves: text content, assignments, selected subfolder

### 7. Export DOCX
- Click "📄 Export DOCX"
- Enter filename (optional)
- File will be downloaded automatically
- Saved to: `/Users/rom/Documents/nvq/v2p-formatter-output/`

## Placeholder Format

### Valid Placeholders
```
{{Site_Arrival}}
{{Safety_Briefing}}
{{Equipment_Check}}
{{Placeholder_Name}}
```

### Invalid Placeholders
```
{{Site Arrival}}     ❌ Spaces not allowed
{{Site-Arrival}}     ❌ Hyphens not allowed
{Site_Arrival}       ❌ Single braces
{{SiteArrival}}      ✅ Valid (no separator needed)
```

## Media Assignment Rules

1. **One Media Per Cell**: Maximum 1 media item per table cell
2. **2-Column Layout**: Tables always have 2 columns
3. **Disabled After Assignment**: Once assigned, media cannot be reassigned
4. **Remove Assignment**: Click the "×" button on media in preview to remove

## Draft System

### Save Draft
- Saves current state:
  - Text content
  - All media assignments
  - Selected subfolder
- Stored in: `/Users/rom/Documents/nvq/v2p-formatter-output/.drafts/`
- Format: JSON files with timestamps

### Load Draft
- Lists all saved drafts
- Shows: name, last updated, subfolder, placeholder count
- Restores full state when loaded

### Delete Draft
- Delete unwanted drafts from the load dialog

## DOCX Export

### Output Format
- **Page Size**: A4
- **Tables**: 2 columns, black borders (1px)
- **Images**: Embedded with aspect ratio maintained
- **Videos**: Filename displayed as text (not embedded video)
- **Empty Cells**: Remain empty

### File Location
Exported files are saved to:
```
/Users/rom/Documents/nvq/v2p-formatter-output/
```

## Configuration

### Media Input Path
```
/Users/rom/Documents/nvq/v2p-formatter-output/<subfolder>/
```

### Draft Storage Path
```
/Users/rom/Documents/nvq/v2p-formatter-output/.drafts/
```

### DOCX Output Path
```
/Users/rom/Documents/nvq/v2p-formatter-output/
```

## Technical Details

### Client-Side Processing (API-Free)
- Placeholder extraction
- Placeholder validation
- Color assignment (rainbow palette)
- Preview generation
- Media assignment tracking
- Statistics calculation

### Server-Side Processing
- Media file scanning
- Thumbnail generation
- DOCX file generation
- Draft file management

### Data Flow
1. **Page Load**: Server scans subfolders and media, embeds data in template
2. **User Interaction**: All processing happens client-side
3. **Export**: Client sends data to server for DOCX generation
4. **Drafts**: Client sends/retrieves draft data from server

## Testing

Run infrastructure tests:
```bash
python -m pytest tests/test_observation_media_infrastructure.py -v
```

Run route tests:
```bash
python -m pytest tests/test_observation_media_routes.py -v
```

## Troubleshooting

### Media Not Showing
- Check that subfolder exists in output directory
- Verify media files are in correct format (jpg, png, mp4, mov)
- Refresh the page to reload media data

### Placeholders Not Detected
- Ensure format is correct: `{{Placeholder_Name}}`
- No spaces allowed (use underscores)
- Case-insensitive but must match exactly

### DOCX Export Fails
- Check that all image paths are valid
- Ensure output directory is writable
- Check server logs for detailed error messages

### Drafts Not Loading
- Verify `.drafts/` folder exists in output directory
- Check file permissions
- Ensure draft files are valid JSON

## Future Enhancements

Potential improvements:
- Auto-save drafts periodically
- Draft versioning
- Export to PDF
- Batch media assignment
- Media search/filter
- Placeholder templates

