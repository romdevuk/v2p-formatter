# Observation AC Matrix - Development Plan

## Overview
Staged development approach with testing and screenshots at each phase. All features must be working before final release.

## Development Principles
1. **Staged Development**: Complete each phase fully before moving to next
2. **Test with Screenshots**: Capture screenshots at each stage for verification
3. **Working State**: Each stage must be fully functional
4. **Final Release**: All features tested and working

## Phase Breakdown

### Phase 1: Backend Core (Foundation)
**Status**: Not Started  
**Estimated Time**: 2-3 days

**Tasks**:
- [ ] Create `app/ac_matrix_parser.py`
  - Parse JSON standards files (one qualification per file)
  - Extract units, learning outcomes, questions (ACs)
  - Handle AC ID format validation (X.Y only)
- [ ] Create `app/ac_matrix_analyzer.py`
  - Extract AC references from observation text (regex, exact match, case-insensitive)
  - Extract section titles with context
  - Generate matrix data structure
- [ ] Create `app/ac_matrix_storage.py`
  - File-based storage (no database)
  - Save/Load/Delete matrix operations
- [ ] Add configuration in `config.py`
  - `AC_MATRIX_DATA_DIR`
  - `AC_MATRIX_JSON_STANDARDS_DIR`
- [ ] Create data directories
- [ ] Unit tests for core functions

**Screenshots Required**:
- JSON file parsed successfully (console/log output)
- ACs extracted from sample observation text (console/log output)
- Matrix data structure generated correctly

**Acceptance Criteria**:
- Can parse provided JSON file (`l2inter-performance.json`)
- Can extract ACs from observation text (exact match, case-insensitive)
- Can generate matrix data structure
- All unit tests passing

---

### Phase 2: Backend - Section Title Extraction
**Status**: Not Started  
**Estimated Time**: 1 day

**Tasks**:
- [ ] Implement `find_section_title()` function
  - Pattern: "SECTION:" or "SECTION -" followed by title
  - Return title and section index (for color coding)
- [ ] Integrate section title extraction into AC extraction
- [ ] Store section index in AC data
- [ ] Test with various section formats

**Screenshots Required**:
- Section titles extracted with correct indices
- Section title matching different patterns

**Acceptance Criteria**:
- Section titles extracted correctly
- Section indices match observation-media color coding
- Handles sections without titles gracefully

---

### Phase 3: API Endpoints
**Status**: Not Started  
**Estimated Time**: 2 days

**Tasks**:
- [ ] Add route `/ac-matrix` in `app/routes.py`
  - Load drafts server-side (no API needed)
  - Pass drafts to template
- [ ] Add route `/ac-matrix/json-files` (GET) - List JSON files
- [ ] Add route `/ac-matrix/json-files` (POST) - Upload JSON file
- [ ] Add route `/ac-matrix/analyze` (POST) - Analyze observation report
- [ ] Add route `/ac-matrix/matrices` (GET) - List saved matrices
- [ ] Add route `/ac-matrix/matrices` (POST) - Save matrix
- [ ] Add route `/ac-matrix/matrices/<matrix_id>` (GET) - Load matrix
- [ ] Add route `/ac-matrix/matrices/<matrix_id>` (DELETE) - Delete matrix
- [ ] Error handling and validation
- [ ] API integration tests

**Screenshots Required**:
- API responses in browser dev tools
- JSON file list endpoint working
- Matrix analysis endpoint working
- Save/Load/Delete endpoints working

**Acceptance Criteria**:
- All endpoints return correct responses
- Error handling works for invalid inputs
- Drafts loaded server-side correctly
- All integration tests passing

---

### Phase 4: Frontend - Basic UI
**Status**: Not Started  
**Estimated Time**: 2 days

**Tasks**:
- [ ] Create `templates/ac_matrix.html`
  - Extend base.html
  - Settings panel with JSON file selector
  - Draft loader dropdown
  - Observation report textarea
  - Analyze button
  - Matrix display section (initially hidden)
  - Actions panel (Save/Load/Delete)
- [ ] Create `static/css/ac-matrix.css`
  - Dark theme styling
  - Consistent with existing app styles
- [ ] Create `static/js/ac-matrix.js`
  - Initialize module
  - Setup event listeners
  - Draft loader functionality (no API)
  - Basic structure for matrix rendering

**Screenshots Required**:
- Basic UI layout
- JSON file selector dropdown
- Draft loader dropdown populated
- Observation report textarea
- Dark theme styling applied

**Acceptance Criteria**:
- Page loads correctly
- All UI elements visible and styled
- Draft loader shows drafts from observation-media
- No console errors

---

### Phase 5: Frontend - Vertical Style Matrix
**Status**: Not Started  
**Estimated Time**: 3 days

**Tasks**:
- [ ] Implement `renderVerticalMatrix()` function
- [ ] Create 4-column table structure:
  - Column 1: AC ID
  - Column 2: AC Description
  - Column 3: Status (Covered/Missing)
  - Column 4: Where Covered
- [ ] Implement section title styling
  - Use SECTION_COLORS array (same as observation-media)
  - font-weight: bold, font-size: 14pt
  - border-left: 4px solid in section color
  - padding-left: 10px
  - margin: 15px 0 10px 0
- [ ] Display observation text section
- [ ] Color coding: Green for covered, Red for missing
- [ ] Handle missing ACs (show "(Not covered in observation)")
- [ ] Unit grouping and collapsible sections

**Screenshots Required**:
- Vertical style matrix with sample data
- Section titles with correct colors
- Covered ACs showing "Where Covered" column
- Missing ACs showing "(Not covered in observation)"
- Color coding visible (green/red)

**Acceptance Criteria**:
- 4-column table displays correctly
- Section titles styled like observation-media
- Observation text sections visible
- Color coding accurate
- Units can be expanded/collapsed

---

### Phase 6: Frontend - Horizontal Style Matrix
**Status**: Not Started  
**Estimated Time**: 2 days

**Tasks**:
- [ ] Implement `renderHorizontalMatrix()` function
- [ ] First line: All ACs in one row (e.g., "ACs: 1.1  1.2  1.3...")
- [ ] Second line: Status indicators (✓ for covered, ✗ for missing)
- [ ] Make ACs clickable
- [ ] Expandable details panel on AC click
- [ ] Show section title and observation text in details
- [ ] Handle multiple expanded ACs
- [ ] Display style toggle functionality

**Screenshots Required**:
- Horizontal style matrix showing AC row and status row
- Expanded AC details showing section title and observation text
- Multiple ACs expanded simultaneously
- Style toggle switching between vertical and horizontal

**Acceptance Criteria**:
- ACs displayed in one row
- Status indicators aligned below ACs
- Clicking AC expands details
- Section titles styled correctly in details
- Can switch between vertical and horizontal styles

---

### Phase 7: Frontend - Save/Load/Delete
**Status**: Not Started  
**Estimated Time**: 2 days

**Tasks**:
- [ ] Implement Save Matrix dialog
  - Matrix name input
  - Save button
  - Cancel button
- [ ] Implement Load Matrix dropdown
  - List saved matrices
  - Show matrix name, date, coverage percentage
  - Load selected matrix
- [ ] Implement Delete Matrix functionality
  - Confirmation dialog
  - Delete button
- [ ] Test save/load/delete workflows
- [ ] Verify data persistence

**Screenshots Required**:
- Save Matrix dialog
- Load Matrix dropdown with saved matrices
- Matrix loaded successfully (data restored)
- Delete confirmation dialog
- Matrix deleted successfully

**Acceptance Criteria**:
- Can save matrix with custom name
- Can load saved matrix (all data restored)
- Can delete saved matrix
- Data persists across page reloads

---

### Phase 8: Integration & Final Testing
**Status**: Not Started  
**Estimated Time**: 3-4 days

**Tasks**:
- [ ] End-to-end workflow testing
  - Select JSON file
  - Load draft from observation-media
  - Enter/load observation report
  - Analyze report
  - View matrix (both styles)
  - Save matrix
  - Load saved matrix
- [ ] Draft loading integration
  - Verify drafts loaded server-side
  - Test loading draft text into textarea
- [ ] Display style verification
  - Vertical style: 4-column layout
  - Horizontal style: AC row + status row
- [ ] Section title color coding verification
  - Compare with observation-media colors
  - Verify SECTION_COLORS array matches
- [ ] Responsive layout testing
  - Desktop (1200px+)
  - Tablet (768px - 1199px)
  - Mobile (< 768px)
- [ ] Error handling testing
  - Invalid JSON files
  - Empty observation reports
  - Missing ACs
  - Edge cases
- [ ] Performance testing
  - Large JSON files
  - Long observation reports
  - Many saved matrices
- [ ] Documentation updates
- [ ] Final code review

**Screenshots Required**:
- Complete workflow (select file → load draft → analyze → view matrix → save)
- Vertical style with real data
- Horizontal style with real data
- Section title colors matching observation-media
- Responsive layouts (desktop, tablet, mobile)
- Error states
- **Final Screenshot**: All features working together

**Acceptance Criteria**:
- Complete workflow works end-to-end
- Both display styles work correctly
- Section title colors match observation-media
- Responsive layouts work on all screen sizes
- Error handling works for all edge cases
- Performance acceptable with large datasets
- All tests passing
- No console errors
- Ready for release

---

## Testing Checklist

### Unit Tests
- [ ] JSON parsing (one qualification per file)
- [ ] AC extraction (exact match, case-insensitive)
- [ ] Section title extraction
- [ ] Matrix generation
- [ ] Storage operations (save/load/delete)

### Integration Tests
- [ ] Full workflow
- [ ] Draft loading
- [ ] Matrix persistence
- [ ] Error handling

### UI Tests
- [ ] Vertical style rendering
- [ ] Horizontal style rendering
- [ ] Section title styling
- [ ] Color coding
- [ ] Responsive layouts
- [ ] Save/Load/Delete workflows

### Screenshot Documentation
- [ ] Phase 1: Backend core working
- [ ] Phase 2: Section titles extracted
- [ ] Phase 3: API endpoints working
- [ ] Phase 4: Basic UI
- [ ] Phase 5: Vertical style matrix
- [ ] Phase 6: Horizontal style matrix
- [ ] Phase 7: Save/Load/Delete
- [ ] Phase 8: Complete workflow

## Release Criteria

Before final release, all of the following must be true:
- [ ] All phases completed
- [ ] All tests passing
- [ ] All screenshots captured
- [ ] No console errors
- [ ] No broken functionality
- [ ] Responsive layouts working
- [ ] Error handling complete
- [ ] Documentation updated
- [ ] Code reviewed

## Notes

- Each phase must be fully functional before moving to next
- Screenshots should be saved in `docs/screenshots/ac-matrix/` directory
- Test with real data from `l2inter-performance.json`
- Verify section title colors match observation-media exactly
- Ensure all edge cases handled gracefully




