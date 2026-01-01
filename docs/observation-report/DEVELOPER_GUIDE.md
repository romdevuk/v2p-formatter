# Observation Report - Developer Guide

**Version**: 1.0  
**Last Updated**: 2025-01-XX

---

## 📋 Overview

This guide is for developers who want to understand, extend, or maintain the Observation Report module.

---

## 🏗️ Architecture Overview

### Module Structure

The Observation Report module is built with a modular architecture:

```
observation-report/
├── Backend (Python/Flask)
│   ├── observation_report_scanner.py       # Media file scanning
│   ├── observation_report_placeholder_parser.py  # Placeholder extraction
│   ├── observation_report_draft_manager.py # Draft save/load
│   └── observation_report_docx_generator.py # DOCX generation
│
├── Frontend (Vanilla JavaScript ES6+)
│   ├── observation-report-media-browser.js    # Media selection UI
│   ├── observation-report-live-preview.js     # Document preview
│   ├── observation-report-standards.js        # Standards display
│   ├── observation-report-preview-draft.js    # Preview dialog
│   ├── observation-report-column-resizer.js   # Resizable columns
│   └── observation-report.js                  # Main orchestrator
│
├── UI/CSS (Dark Theme)
│   ├── observation-report.css                    # Main styles
│   └── observation-report/
│       ├── observation-report-media-browser.css
│       ├── observation-report-live-preview.css
│       ├── observation-report-standards.css
│       ├── observation-report-preview-draft.css
│       └── observation-report-column-resizer.css
│
└── Templates (Jinja2)
    └── observation_report.html                   # Main page template
```

---

## 🔧 Backend Architecture

### Module: `observation_report_scanner.py`

**Purpose**: Scan and retrieve media files from the file system

**Key Functions**:
- `scan_media_files(qualification, learner, output_folder)` - Scan media files
- `get_media_metadata(file_path)` - Get file metadata (size, dimensions, duration)
- `generate_thumbnail_path(file_path)` - Generate thumbnail path

**Usage**:
```python
from app.observation_report_scanner import scan_media_files
from pathlib import Path

media = scan_media_files("qualification", "learner", Path("/output"))
```

### Module: `observation_report_placeholder_parser.py`

**Purpose**: Extract and validate placeholders from text

**Key Functions**:
- `extract_placeholders(text)` - Extract all placeholders from text
- `validate_placeholder(name)` - Validate placeholder name format
- `assign_placeholder_colors(placeholders)` - Assign colors to placeholders

**Usage**:
```python
from app.observation_report_placeholder_parser import extract_placeholders

placeholders = extract_placeholders("Text {{Placeholder1}} and {{Placeholder2}}")
# Returns: ['Placeholder1', 'Placeholder2']
```

### Module: `observation_report_draft_manager.py`

**Purpose**: Save and load draft data

**Key Functions**:
- `save_draft(draft_data, output_folder)` - Save draft to JSON
- `load_draft(draft_name, output_folder)` - Load draft from JSON
- `list_drafts(output_folder)` - List all drafts
- `delete_draft(draft_name, output_folder)` - Delete a draft

**Usage**:
```python
from app.observation_report_draft_manager import save_draft, load_draft

# Save
save_draft({
    'text_content': 'Text {{Placeholder1}}',
    'assignments': {},
    'header_data': {}
}, Path("/output"))

# Load
draft = load_draft("draft_name", Path("/output"))
```

### Module: `observation_report_docx_generator.py`

**Purpose**: Generate DOCX documents from draft data

**Key Functions**:
- `generate_docx(text_content, assignments, header_data, assessor_feedback, filename, output_folder, font_size, font_name)` - Generate DOCX file

**Usage**:
```python
from app.observation_report_docx_generator import generate_docx

docx_path = generate_docx(
    text_content="Text {{Placeholder1}}",
    assignments={'Placeholder1': []},
    header_data={'learner': 'Test Learner'},
    assessor_feedback="Feedback text",
    filename="report.docx",
    output_folder=Path("/output"),
    font_size=16,
    font_name="Times New Roman"
)
```

### API Routes

All routes are in `app/routes.py`:

- `GET /observation-report` - Main page
- `GET /observation-report/learners` - Get learners for qualification
- `GET /observation-report/media` - Get media files
- `GET /observation-report/drafts` - List drafts
- `POST /observation-report/drafts` - Create draft
- `GET /observation-report/drafts/<name>` - Load draft
- `PUT /observation-report/drafts/<name>` - Update draft
- `DELETE /observation-report/drafts/<name>` - Delete draft
- `POST /observation-report/export-docx` - Export DOCX
- `GET /observation-report/download-docx/<filename>` - Download DOCX

---

## 🎨 Frontend Architecture

### Standalone Library Pattern

Each frontend library is **independent** and can be used standalone:

```javascript
// Each library is self-contained
import { ObservationReportMediaBrowser } from './observation-report-media-browser.js';

const browser = new ObservationReportMediaBrowser('containerId', {
    onMediaSelected: (media) => console.log(media),
    onDragStart: (media, event) => console.log('drag start')
});
```

### Main Orchestrator

The `observation-report.js` file coordinates all libraries:

```javascript
class ObservationReport {
    constructor() {
        this.state = {
            qualification: null,
            learner: null,
            textContent: '',
            assignments: {},
            headerData: {},
            assessorFeedback: ''
        };
        
        this.initializeLibraries();
        this.setupEventHandlers();
    }
}
```

### Event-Based Communication

Libraries communicate via custom events:

```javascript
// Library A emits event
document.dispatchEvent(new CustomEvent('observation-report:media-selected', {
    detail: { media }
}));

// Library B listens
document.addEventListener('observation-report:media-selected', (event) => {
    const { media } = event.detail;
    // Handle event
});
```

---

## 📚 Library APIs

### Media Browser Library

**Class**: `ObservationReportMediaBrowser`

**Constructor**:
```javascript
new ObservationReportMediaBrowser(containerId, {
    onMediaSelected: (media) => {},
    onDragStart: (media, event) => {},
    onMediaRenamed: (media, newName) => {}
})
```

**Methods**:
- `loadMedia(qualification, learner)` - Load media files
- `updateAssignmentState(assignments)` - Update assignment states
- `selectMedia(mediaId)` - Select media item
- `clearSelection()` - Clear selection

### Live Preview Library

**Class**: `ObservationReportLivePreview`

**Constructor**:
```javascript
new ObservationReportLivePreview(containerId, {
    onMediaAssigned: (placeholderId, media, position) => {},
    onMediaRemoved: (placeholderId, position) => {},
    onMediaReordered: (placeholderId, oldIndex, newIndex) => {}
})
```

**Methods**:
- `updateContent(text, assignments, sections)` - Update preview content
- `renderPlaceholderTable(placeholder, mediaList)` - Render placeholder table
- `reorderMedia(placeholderId, oldIndex, newIndex)` - Reorder media
- `calculatePosition(row, col)` - Calculate position from row/col
- `calculateRowCol(position)` - Calculate row/col from position

### Standards Library

**Class**: `ObservationReportStandards`

**Constructor**:
```javascript
new ObservationReportStandards(containerId, {
    onAcClick: (acId) => {},
    onSectionNavigate: (sectionId) => {}
})
```

**Methods**:
- `loadStandards(jsonFileId)` - Load standards JSON
- `updateCoverage(textContent)` - Update AC coverage
- `searchStandards(keyword)` - Search ACs
- `expandAll()` - Expand all units
- `collapseAll()` - Collapse all units

### Preview Draft Library

**Class**: `ObservationReportPreviewDraft`

**Constructor**:
```javascript
new ObservationReportPreviewDraft({
    onExport: (options) => {},
    onUpdateDraft: (options) => {},
    onClose: () => {}
})
```

**Methods**:
- `open(content, assignments, sections, headerData, assessorFeedback)` - Open preview
- `close()` - Close preview
- `exportDOCX(options)` - Trigger DOCX export
- `updateDraft(options)` - Update draft

### Column Resizer Library

**Class**: `ObservationReportColumnResizer`

**Constructor**:
```javascript
new ObservationReportColumnResizer(containerId, {
    storageKey: 'column-widths',
    minWidth: 200
})
```

**Methods**:
- `addResizer(leftColumnId, rightColumnId, options)` - Add resizer between columns
- `saveWidths(storageKey)` - Save widths to localStorage
- `loadWidths(storageKey)` - Load widths from localStorage

---

## 🔌 Extension Guide

### Adding a New Media Type

1. **Update Scanner** (`observation_report_scanner.py`):
```python
SUPPORTED_NEW_TYPE_EXTENSIONS = ['.newtype']

# Add to scan_media_files function
if file_path.suffix.lower() in SUPPORTED_NEW_TYPE_EXTENSIONS:
    file_type = 'newtype'
```

2. **Update Frontend** (`observation-report-media-browser.js`):
```javascript
getMediaIcon(fileType) {
    if (fileType === 'newtype') {
        return '🎬'; // Choose appropriate icon
    }
}
```

3. **Update DOCX Generator** (`observation_report_docx_generator.py`):
```python
if media_type == 'newtype':
    # Handle newtype in DOCX generation
    pass
```

### Adding a New Placeholder Format

1. **Update Parser** (`observation_report_placeholder_parser.py`):
```python
# Modify PLACEHOLDER_PATTERN regex
NEW_PLACEHOLDER_PATTERN = re.compile(r'\{\{([A-Za-z0-9_]+)\}\}|\[\[([A-Za-z0-9_]+)\]\]')
```

### Adding a New API Endpoint

1. **Add Route** (`app/routes.py`):
```python
@app.route('/observation-report/new-endpoint', methods=['GET'])
def new_endpoint():
    return jsonify({'success': True, 'data': {}})
```

2. **Update API Reference** (`docs/observation-report/API_REFERENCE.md`)

---

## 🧪 Testing

### Running Tests

```bash
# All tests
pytest tests/test_observation_report*.py -v

# Backend only
pytest tests/test_observation_report_backend.py -v

# API only
pytest tests/test_observation_report_api.py -v

# Browser tests
pytest tests/test_observation_report_drag_drop.py -v
pytest tests/test_observation_report_reshuffle.py -v
```

### Writing Tests

See `docs/observation-report/TESTING_GUIDE.md` for test patterns and examples.

---

## 🎨 Styling Guidelines

### Dark Theme Colors

```css
:root {
    --obs-bg-primary: #1e1e1e;
    --obs-bg-secondary: #2a2a2a;
    --obs-text-primary: #e0e0e0;
    --obs-accent: #667eea;
}
```

### Component Styling

- Use CSS variables for colors
- Follow BEM-like naming: `.observation-report-component-name`
- Use transitions for interactions
- Maintain 95% viewport width

---

## 📦 Dependencies

### Backend

- Flask - Web framework
- python-docx - DOCX generation
- Pillow (PIL) - Image processing
- opencv-python (cv2) - Video processing (optional)
- mutagen - Audio metadata (optional)

### Frontend

- Vanilla JavaScript ES6+ (no frameworks)
- No external dependencies

---

## 🔒 Security Considerations

1. **Path Validation**: All file paths are validated to prevent directory traversal
2. **Input Sanitization**: Placeholder names are validated
3. **File Type Validation**: Only supported file types are processed
4. **Error Handling**: Errors are logged, not exposed to users

---

## 🐛 Debugging

### Backend Debugging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Frontend Debugging

```javascript
// Enable debug mode
window.observationReportDebug = true;

// Libraries log debug messages
console.log('[MediaBrowser]', message);
```

### Browser Console

- Check for JavaScript errors (F12)
- Monitor network requests (Network tab)
- Inspect element states (Elements tab)

---

## 📝 Code Organization

### File Naming

- Backend: `observation_report_*.py` (snake_case)
- Frontend: `observation-report-*.js` (kebab-case)
- CSS: `observation-report*.css` (kebab-case)

### Code Structure

- One file per module/library
- Clear separation of concerns
- Reusable functions/classes
- Well-documented code

---

## 🤝 Contribution Guidelines

1. **Follow Architecture**: Maintain modular structure
2. **Write Tests**: Add tests for new features
3. **Update Documentation**: Keep docs current
4. **Code Style**: Follow existing patterns
5. **Review**: Get code review before merging

---

## 📚 Additional Resources

- **User Guide**: `docs/observation-report/USER_GUIDE.md`
- **API Reference**: `docs/observation-report/API_REFERENCE.md`
- **Testing Guide**: `docs/observation-report/TESTING_GUIDE.md`
- **Specification**: `docs/observation-media-complete-specification.md`

---

**Last Updated**: 2025-01-XX  
**Version**: 1.0



