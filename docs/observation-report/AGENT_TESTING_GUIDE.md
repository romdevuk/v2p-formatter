# Observation Report - Agent Testing Guide

**Purpose**: Automated testing procedures for agents to verify code changes

---

## 🎯 Automated Testing Workflow

### For Backend Developers (Agent-1)

**After implementing backend changes:**
```bash
# Run automated backend tests
./tests/run_observation_report_backend_tests.sh

# Or manually:
pytest tests/test_observation_report_backend.py -v
pytest tests/test_observation_report_api.py -v
```

**Test Checklist:**
- [ ] All backend unit tests pass
- [ ] API endpoints return correct responses
- [ ] Media scanning works correctly
- [ ] Draft save/load works
- [ ] DOCX generation works

---

### For Frontend Developers (Agent-2)

**After implementing frontend changes:**
```bash
# Run automated UX/QA tests
./tests/run_observation_report_qa_automated.sh

# Or manually:
pytest tests/test_observation_report_ux_qa.py -v -s
```

**Test Checklist:**
- [ ] Images load and display correctly
- [ ] Section colors are visible
- [ ] Placeholder colors are visible
- [ ] Media browser shows subfolders
- [ ] Drag-and-drop works
- [ ] Reshuffle works
- [ ] All UI elements render correctly

---

### For UX Designers (Agent-3)

**After implementing UI/styling changes:**
```bash
# Run automated visual verification
./tests/run_observation_report_qa_automated.sh

# Check visual screenshots
open test_screenshots/observation_report_ux_qa/
```

**Visual Checklist:**
- [ ] Section titles are color-coded
- [ ] Placeholder labels are color-coded
- [ ] Media browser folders are visible
- [ ] Images display correctly
- [ ] Dark theme is consistent
- [ ] All styles are applied

---

### For Testers (Agent-4)

**Before marking stage complete:**
```bash
# Run complete test suite
./tests/run_all_observation_report_tests.sh
```

**Complete Test Checklist:**
- [ ] Backend tests pass
- [ ] API tests pass
- [ ] Frontend unit tests pass
- [ ] UX/QA tests pass
- [ ] Visual verification tests pass
- [ ] Screenshots captured
- [ ] Test reports generated

---

## 🤖 Automated Test Execution

### Option 1: Shell Scripts (Recommended)

```bash
# UX/QA tests
./tests/run_observation_report_qa_automated.sh

# All tests
./tests/run_all_observation_report_tests.sh
```

### Option 2: Python Script

```bash
python tests/run_automated_tests.py
```

### Option 3: Pytest Direct

```bash
# All observation report tests
pytest tests/test_observation_report*.py -v

# Specific test suite
pytest tests/test_observation_report_ux_qa.py -v
```

---

## 📋 Pre-Test Requirements

### 1. Flask Server Running
```bash
# Start server (in separate terminal)
python run.py
```

### 2. Test Data Available
- At least one qualification folder
- At least one learner folder
- Media files in learner folders
- At least one saved draft (optional)

### 3. Dependencies Installed
```bash
pip install -r requirements.txt
playwright install chromium  # If using Playwright
```

---

## 🔍 What Gets Tested Automatically

### Visual Elements
- ✅ Images load correctly
- ✅ Section colors are visible
- ✅ Placeholder colors are visible
- ✅ Media browser displays correctly
- ✅ Standards panel displays correctly

### Functionality
- ✅ Drag-and-drop works
- ✅ Reshuffle works
- ✅ Draft save/load works
- ✅ Media assignment works
- ✅ Placeholder rendering works

### Backend
- ✅ API endpoints work
- ✅ Media scanning works
- ✅ Draft management works
- ✅ DOCX generation works

---

## 📊 Test Reports

After running tests, check:
- `reports/observation_report_ux_qa.html` - HTML test report
- `reports/observation_report_ux_qa.xml` - XML report (CI/CD)
- `test_screenshots/observation_report_ux_qa/` - Visual screenshots

---

## 🚨 Common Issues

### Flask Server Not Running
**Error**: `Flask server is not running`
**Fix**: Start server with `python run.py`

### No Test Data
**Error**: Tests fail with empty dropdowns
**Fix**: Ensure qualification/learner folders exist in OUTPUT_FOLDER

### Browser Not Found
**Error**: `playwright not found`
**Fix**: `pip install playwright && playwright install chromium`

---

## ✅ Agent Workflow

### Step 1: Make Changes
- Implement your changes
- Update code as needed

### Step 2: Run Automated Tests
```bash
./tests/run_observation_report_qa_automated.sh
```

### Step 3: Review Results
- Check test output
- Review screenshots
- Check HTML report

### Step 4: Fix Issues (if any)
- Fix any failing tests
- Re-run tests
- Verify fixes

### Step 5: Mark Complete
- All tests pass
- Screenshots look correct
- Report shows success

---

**Last Updated**: 2025-01-XX



