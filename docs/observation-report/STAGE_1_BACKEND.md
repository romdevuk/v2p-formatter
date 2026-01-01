# Stage 1: Backend Foundation

**Status**: ⏳ Pending  
**Owner**: Backend Developer (Agent-1)  
**Estimated Duration**: 2-3 days  
**Dependencies**: Stage 0 Complete

---

## 📋 Objectives

Implement all backend functionality for the Observation Report module:
- Media file scanning
- Draft management (save/load/delete)
- DOCX generation
- Placeholder parsing utilities
- API endpoints

**⚠️ IMPORTANT**: All code must be NEW - no legacy code from old modules. The old observation-media module did not work properly and must be completely avoided.

---

## 📁 Files to Create

### 1. Media Scanner Module
**File**: `app/observation_report_scanner.py`  
**Purpose**: Scan media files from qualification/learner folders

**Requirements**:
- Scan `/output/{qualification}/{learner}/` recursively
- Support: JPG, JPEG, PNG, MP4, MOV, PDF, MP3
- Extract metadata: size, dimensions (images/videos), duration (videos/audio)
- Generate thumbnail paths for images/videos
- Return structured media file objects

**Key Functions**:
```python
def scan_media_files(qualification: str, learner: str) -> List[MediaFile]
def get_media_metadata(file_path: Path) -> Dict
def generate_thumbnail_path(file_path: Path) -> Optional[str]
```

### 2. Placeholder Parser Module
**File**: `app/observation_report_placeholder_parser.py`  
**Purpose**: Extract and validate placeholders from text

**Requirements**:
- Extract `{{Placeholder_Name}}` patterns (case-insensitive)
- Validate format (alphanumeric + underscore only)
- Assign rainbow colors to placeholders
- Track placeholder statistics

**Key Functions**:
```python
def extract_placeholders(text: str) -> List[str]
def validate_placeholder(name: str) -> bool
def assign_placeholder_colors(placeholders: List[str]) -> Dict[str, str]
```

### 3. Draft Manager Module
**File**: `app/observation_report_draft_manager.py`  
**Purpose**: Save, load, list, and delete drafts

**Requirements**:
- Save drafts to `/output/.drafts/{draft_name}.json`
- Load draft from JSON file
- List all drafts with metadata
- Delete draft files
- Validate draft structure

**Key Functions**:
```python
def save_draft(draft_data: Dict) -> bool
def load_draft(draft_name: str) -> Dict
def list_drafts() -> List[Dict]
def delete_draft(draft_name: str) -> bool
```

### 4. DOCX Generator Module
**File**: `app/observation_report_docx_generator.py`  
**Purpose**: Generate DOCX files from draft data

**Requirements**:
- Create A4 page size documents
- Add header table (if header data exists)
- Process text content with placeholder replacement
- Create 2-column tables for placeholders
- Embed images in table cells
- Add video/PDF/MP3 filenames as text
- Add assessor feedback table at bottom
- Support font settings (size, type)

**Key Functions**:
```python
def generate_docx(
    text_content: str,
    assignments: Dict,
    header_data: Dict,
    assessor_feedback: str,
    filename: str,
    font_size: int = 16,
    font_name: str = "Times New Roman"
) -> Path
```

### 5. Routes Integration
**File**: `app/routes.py` (add new routes)  
**Purpose**: Add Observation Report API endpoints

**New Routes**:
```python
# Media Management
GET  /observation-report/learners?qualification=...
GET  /observation-report/media?qualification=...&learner=...

# Draft Management
GET    /observation-report/drafts
POST   /observation-report/drafts
GET    /observation-report/drafts/<draft_name>
PUT    /observation-report/drafts/<draft_name>
DELETE /observation-report/drafts/<draft_name>

# DOCX Export
POST   /observation-report/export-docx
GET    /observation-report/download-docx/<filename>

# File Operations
POST   /observation-report/rename-file
```

---

## ✅ Implementation Checklist

### Media Scanner
- [ ] Implement recursive file scanning
- [ ] Support all media types (JPG, JPEG, PNG, MP4, MOV, PDF, MP3)
- [ ] Extract file metadata
- [ ] Generate thumbnail paths
- [ ] Return structured data

### Placeholder Parser
- [ ] Implement placeholder extraction regex
- [ ] Validate placeholder format
- [ ] Assign rainbow colors
- [ ] Return placeholder statistics

### Draft Manager
- [ ] Implement save draft functionality
- [ ] Implement load draft functionality
- [ ] Implement list drafts functionality
- [ ] Implement delete draft functionality
- [ ] Validate JSON structure

### DOCX Generator
- [ ] Create A4 document structure
- [ ] Add header table
- [ ] Process placeholders → tables
- [ ] Embed images
- [ ] Add video/PDF/MP3 filenames
- [ ] Add assessor feedback table
- [ ] Support font customization

### Routes
- [ ] Add all media management routes
- [ ] Add all draft management routes
- [ ] Add DOCX export routes
- [ ] Add file operation routes
- [ ] Test all routes

### Testing
- [ ] Unit tests for scanner
- [ ] Unit tests for parser
- [ ] Unit tests for draft manager
- [ ] Unit tests for DOCX generator
- [ ] Integration tests for routes

---

## 🧪 Testing Requirements

Create test files:
- `tests/test_observation_report_scanner.py`
- `tests/test_observation_report_placeholder_parser.py`
- `tests/test_observation_report_draft_manager.py`
- `tests/test_observation_report_docx_generator.py`
- `tests/test_observation_report_routes.py`

All tests must pass before stage completion.

---

## 📚 Reference Documentation

- **Specification**: `docs/observation-media-complete-specification.md`
  - Section: API Endpoints (lines 1416-1475)
  - Section: Data Models (lines 1318-1412)
  - Section: Key Implementation Details (lines 2089-2156)

- **Working Code Patterns**: Reference `app/routes.py` for Flask route patterns, `app/file_scanner.py` for file scanning patterns, `app/docx_generator.py` for DOCX generation patterns (general patterns only - all code must be NEW)

---

## 🎯 Completion Criteria

Stage 1 is complete when:
- [ ] All backend modules created and functional
- [ ] All API endpoints responding correctly
- [ ] Draft save/load working
- [ ] DOCX generation working with sample data
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] Code reviewed and documented

---

## 📝 Notes

- Use `python-docx` library for DOCX generation (already in requirements)
- Use `Pillow` for image processing (already in requirements)
- All paths should use `config.py` constants (OUTPUT_FOLDER, etc.)
- Follow existing code patterns for error handling and logging

---

## ✅ Stage 1 Gate

**Ready to proceed to Stage 2** when:
- All checklist items complete
- Progress tracker updated
- Orchestrator approval received

