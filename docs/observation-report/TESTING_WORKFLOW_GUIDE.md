# Observation Report - Testing Workflow Guide

**Purpose**: Comprehensive testing guide with actual workflows, screenshots, and visual verification

---

## 🎯 Testing Approach

### Multi-Agent Testing Strategy

1. **Frontend Tester** - UI/UX verification, visual tests
2. **Integration Tester** - End-to-end workflows
3. **Functional Tester** - Feature-by-feature verification
4. **Visual Tester** - Screenshot comparisons, layout verification

---

## 📋 Pre-Testing Checklist

### Environment Setup
- [ ] Flask server running: `python run.py`
- [ ] Server accessible at: `http://localhost/v2p-formatter`
- [ ] OUTPUT_FOLDER exists: `/Users/rom/Documents/nvq/v2p-formatter-output`
- [ ] Test data available:
  - [ ] At least one qualification folder
  - [ ] At least one learner folder per qualification
  - [ ] Media files (images/videos/PDFs/audio) in learner folders
  - [ ] At least one draft saved: `learner_lakhmaniuk_obs1_20251209_194019`

### Browser Setup
- [ ] Playwright browsers installed: `playwright install chromium`
- [ ] Test screenshots directory exists: `test_screenshots/observation_report_workflows/`

---

## 🧪 Test Execution

### Run All Workflow Tests

```bash
# Navigate to project root
cd /Users/rom/Documents/nvq/apps/v2p-formatter

# Activate virtual environment
source venv/bin/activate

# Run E2E workflow tests with screenshots
pytest tests/test_observation_report_workflow_e2e.py -v -s

# Run visual verification tests
pytest tests/test_observation_report_visual_verification.py -v -s

# Run all observation report tests
pytest tests/test_observation_report*.py -v -s
```

### Run with Screenshots (Non-Headless)

```bash
# Run in visible browser (for debugging)
HEADLESS=false pytest tests/test_observation_report_workflow_e2e.py -v -s
```

### Generate HTML Report

```bash
pytest tests/test_observation_report*.py --html=reports/observation_report_test_report.html --self-contained-html
```

---

## 📸 Screenshot Verification

### Expected Screenshots

After running tests, check `test_screenshots/observation_report_workflows/`:

1. **00_initial_load.png** - Initial page load
2. **01_qualification_dropdown.png** - Qualification dropdown populated
3. **02_qualification_selected.png** - After selecting qualification
4. **03_learner_selected_media_loaded.png** - After selecting learner, media loaded
5. **04_media_browser_loaded.png** - Media browser with files
6. **05_text_entered.png** - Text editor with placeholders
7. **06_placeholders_rendered.png** - Live preview showing placeholders
8. **07_before_drag.png** - Before drag operation
9. **08_after_drag.png** - After drag operation
10. **09_media_in_placeholder.png** - Media assigned to placeholder
11. **10_before_reshuffle.png** - Before reordering
12. **11_after_arrow_reorder.png** - After arrow button reorder
13. **12_after_drag_reorder.png** - After drag reorder
14. **13_draft_dialog.png** - Draft load dialog
15. **14_draft_loaded.png** - After loading draft
16. **15_standards_loaded.png** - Standards panel with data (or empty if issue)

### Visual Verification Checklist

#### Media Browser
- [ ] Media cards display correctly
- [ ] Thumbnails show for images
- [ ] File type icons correct (image/video/PDF/audio)
- [ ] Assigned media shows checkmark
- [ ] File count displayed correctly

#### Live Preview
- [ ] Placeholders render with colored labels
- [ ] Drop zones visible (dashed borders)
- [ ] Media items display in 2-column table
- [ ] Reorder buttons visible on media items
- [ ] Sections display correctly

#### Standards Panel
- [ ] Units list visible
- [ ] AC items display correctly
- [ ] Search functionality works
- [ ] Coverage indicators show
- [ ] Section links work

---

## 🔍 Critical Feature Testing

### 1. Drag-and-Drop Testing (CRITICAL)

**Test Steps**:
1. Load page
2. Select qualification → learner
3. Enter text with placeholder: `{{TestPlaceholder}}`
4. Drag media card to drop zone
5. Verify media appears in placeholder
6. Verify media card shows assigned state

**Screenshots Required**:
- Before drag
- During drag (drag state)
- Over drop zone (drop zone highlighted)
- After drop (media in placeholder)

**Verification Points**:
- [ ] Media card opacity changes during drag
- [ ] Drop zone highlights (blue dashed border)
- [ ] Media appears in correct position
- [ ] Media card shows checkmark
- [ ] Can't drag assigned media again

### 2. Reshuffle Testing (CRITICAL)

**Test Steps**:
1. Assign 4 media items to placeholder
2. Use ↑ button to move second item up
3. Use ↓ button to move item down
4. Drag-and-drop item to different position
5. Verify 2-column layout maintained

**Screenshots Required**:
- Initial assignment (4 items in 2x2 table)
- After arrow reorder
- During drag reorder
- After drag reorder

**Verification Points**:
- [ ] Arrow buttons work correctly
- [ ] Buttons disabled on first/last item
- [ ] Drag reorder works smoothly
- [ ] Layout stays 2-column
- [ ] Position calculations correct

### 3. Draft Loading with Standards

**Test Steps**:
1. Click "Load Draft" button
2. Find draft: `learner_lakhmaniuk_obs1_20251209_194019`
3. Click "Load"
4. Verify:
   - Text content loads
   - Media assignments load
   - Header data loads
   - **Standards data loads** ⚠️ CRITICAL

**Screenshots Required**:
- Draft dialog
- After loading draft
- Standards panel (should show units/ACs)

**Verification Points**:
- [ ] Draft loads successfully
- [ ] Text content populated
- [ ] Placeholders rendered
- [ ] Media assignments restored
- [ ] **Standards panel shows data** ⚠️
- [ ] Qualification/learner selected

---

## 🐛 Known Issues to Test

### Standards Not Loading from Draft

**Issue**: When loading draft `learner_lakhmaniuk_obs1_20251209_194019`, standards don't appear.

**Testing**:
1. Load the draft
2. Check browser console for errors
3. Check Network tab for API calls:
   - `/v2p-formatter/ac-matrix/json-files/{fileId}`
4. Verify draft JSON contains:
   - `json_file_id` field
   - `standards_file_id` field
   - `standards_data` field

**Expected Fix Applied**:
- ✅ Code now checks multiple field names
- ✅ Retry logic added
- ✅ Better error logging

---

## 📊 Test Results Template

After running tests, document results:

```
Test Run: [Date]
Environment: [Browser/OS]

✅ Passing Tests:
- [List tests that passed]

❌ Failing Tests:
- [List tests that failed with errors]

⚠️ Issues Found:
- [List bugs/issues discovered]

📸 Screenshots:
- [Location of screenshot directory]
```

---

## 🚀 Quick Test Commands

```bash
# Quick smoke test (fast)
pytest tests/test_observation_report_workflow_e2e.py::TestObservationReportWorkflowsE2E::test_workflow_qualification_learner_selection -v

# Test standards loading specifically
pytest tests/test_observation_report_workflow_e2e.py::TestObservationReportWorkflowsE2E::test_workflow_load_draft_with_standards -v -s

# Visual verification
pytest tests/test_observation_report_visual_verification.py -v -s

# All tests with HTML report
pytest tests/test_observation_report*.py --html=reports/test_report.html --self-contained-html -v
```

---

## 📝 Reporting Issues

When reporting issues, include:
1. Screenshot of the issue
2. Browser console errors (F12)
3. Network tab showing failed requests
4. Steps to reproduce
5. Expected vs actual behavior

---

**Last Updated**: 2025-01-XX



