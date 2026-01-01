# Observation Report - Testing Guide

**Status**: ✅ Test Suite Created  
**Owner**: Tester (Agent-4)  
**Date**: 2025-01-XX

---

## 📋 Overview

This guide covers all testing resources for the Observation Report module.

---

## 🧪 Test Files

### Backend Tests

1. **`tests/test_observation_report_backend.py`**
   - Unit tests for all backend modules
   - Media scanner tests
   - Placeholder parser tests
   - Draft manager tests
   - DOCX generator tests

**Run:**
```bash
pytest tests/test_observation_report_backend.py -v
```

### API Tests

2. **`tests/test_observation_report_api.py`**
   - Integration tests for all Flask API endpoints
   - Tests all `/observation-report/*` routes
   - Draft operations (save/load/update/delete)
   - Media operations
   - DOCX export

**Run:**
```bash
pytest tests/test_observation_report_api.py -v
```

### Browser Tests (Critical Features)

3. **`tests/test_observation_report_drag_drop.py`** ⚠️ **CRITICAL**
   - Single media drag-and-drop
   - Bulk drag-and-drop
   - Visual feedback testing
   - Invalid zone handling
   - Assigned media prevention

**Run:**
```bash
pytest tests/test_observation_report_drag_drop.py -v
```

4. **`tests/test_observation_report_reshuffle.py`** ⚠️ **CRITICAL**
   - Arrow button reordering
   - Drag-and-drop reordering
   - Position calculations
   - Visual feedback
   - Disabled states

**Run:**
```bash
pytest tests/test_observation_report_reshuffle.py -v
```

### End-to-End Workflows

5. **`tests/test_observation_report_workflows.py`**
   - Complete workflow tests
   - Workflow 1: Initial Setup
   - Workflow 2: Content Creation
   - Workflow 3A: Click-to-Assign
   - Workflow 3B: Drag-and-Drop
   - Workflow 4: Reordering
   - Workflow 5: Header Information
   - Workflow 8: Save Draft
   - Workflow 9: Load Draft
   - Workflow 11: Preview

**Run:**
```bash
pytest tests/test_observation_report_workflows.py -v
```

---

## 🚀 Running Tests

### Prerequisites

1. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install pytest playwright
```

2. **Install Playwright browsers:**
```bash
playwright install chromium
```

3. **Start Flask server:**
```bash
python run.py
```

### Run All Tests

```bash
pytest tests/test_observation_report*.py -v
```

### Run Specific Test Category

```bash
# Backend only
pytest tests/test_observation_report_backend.py -v

# API only
pytest tests/test_observation_report_api.py -v

# Critical features only
pytest tests/test_observation_report_drag_drop.py tests/test_observation_report_reshuffle.py -v

# Workflows only
pytest tests/test_observation_report_workflows.py -v
```

### Run with HTML Report

```bash
pytest tests/test_observation_report*.py --html=reports/observation_report_test_report.html --self-contained-html
```

### Run in Headless Mode

```bash
HEADLESS=true pytest tests/test_observation_report*.py -v
```

---

## ⚠️ Critical Test Areas

### Drag-and-Drop Testing

**Priority**: **HIGH** - This was a major complexity in the old module

**Test Coverage:**
- ✅ Single media drag to placeholder
- ✅ Bulk drag-and-drop
- ✅ Visual feedback during drag
- ✅ Drop zone highlighting
- ✅ Assigned media prevention
- ✅ Invalid zone handling

**Test File**: `tests/test_observation_report_drag_drop.py`

### Reshuffle Testing

**Priority**: **HIGH** - This was a major complexity in the old module

**Test Coverage:**
- ✅ Arrow button reordering (up/down)
- ✅ Drag-and-drop reordering within table
- ✅ Position calculations (2-column layout)
- ✅ Visual feedback
- ✅ Disabled states (first/last item)
- ✅ Layout maintenance

**Test File**: `tests/test_observation_report_reshuffle.py`

---

## 📊 Test Coverage Goals

### Backend
- [ ] Media Scanner: > 80%
- [ ] Placeholder Parser: > 80%
- [ ] Draft Manager: > 80%
- [ ] DOCX Generator: > 80%

### API
- [ ] All endpoints tested
- [ ] Error handling tested
- [ ] Edge cases covered

### Frontend
- [ ] Critical features: 100%
- [ ] All workflows: 100%
- [ ] Visual feedback: 100%

---

## 🐛 Known Issues / Limitations

### Test Dependencies

1. **Test Data Required**: Tests require actual media files in the output folder structure
   - Location: `{OUTPUT_FOLDER}/{qualification}/{learner}/`
   - Files: JPG, PNG, MP4, MOV, PDF, MP3

2. **Server Must Be Running**: Browser tests require Flask server running

3. **Timing Sensitive**: Some tests use `time.sleep()` - may need adjustment for slower systems

### Future Improvements

1. **Mock Test Data**: Create fixtures with mock media files
2. **Parallel Execution**: Run tests in parallel for speed
3. **Visual Regression**: Add screenshot comparison tests
4. **Performance Benchmarks**: Add performance timing tests

---

## 📝 Test Results

### Latest Run

**Date**: _TBD_  
**Status**: _TBD_  
**Coverage**: _TBD_  
**Pass Rate**: _TBD_

---

## 🔍 Debugging Tests

### Enable Verbose Output

```bash
pytest tests/test_observation_report*.py -v -s
```

### Run Single Test

```bash
pytest tests/test_observation_report_drag_drop.py::TestDragAndDrop::test_single_media_drag_to_placeholder -v -s
```

### Capture Screenshots on Failure

Tests automatically capture screenshots on failure in `test_screenshots/` directory.

### View Browser (Non-Headless)

```bash
HEADLESS=false pytest tests/test_observation_report_drag_drop.py -v -s
```

---

## ✅ Test Checklist

### Backend Tests
- [ ] All unit tests passing
- [ ] All edge cases covered
- [ ] Error handling verified

### API Tests
- [ ] All endpoints tested
- [ ] All status codes verified
- [ ] Error responses verified

### Browser Tests
- [ ] All drag-and-drop tests passing
- [ ] All reshuffle tests passing
- [ ] All workflow tests passing
- [ ] Visual feedback verified
- [ ] Cross-browser tested (Chrome, Firefox, Safari, Edge)

---

## 📚 Reference

- **Test Specification**: `docs/observation-report/STAGE_4_TESTING.md`
- **Critical Features**: `docs/observation-report/CRITICAL_FEATURES.md`
- **Test Checklist**: `docs/observation-report/checkpoints/stage_4_checklist.md`

---

**Status**: ✅ Test Suite Created and Ready for Execution



