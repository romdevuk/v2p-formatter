# Automated Testing for Observation Report

**Purpose**: Enable agents to automatically run tests without manual intervention

---

## 🤖 How Agents Run Tests

### Method 1: Automated Scripts (Recommended)

Agents can execute these commands:

```bash
# Run UX/QA tests automatically
./tests/run_observation_report_qa_automated.sh

# Run all tests automatically
./tests/run_all_observation_report_tests.sh
```

These scripts:
- ✅ Check if Flask server is running
- ✅ Activate virtual environment if needed
- ✅ Run all relevant tests
- ✅ Generate reports automatically
- ✅ Exit with proper status codes

---

### Method 2: Python Test Runner

```bash
python tests/run_automated_tests.py
```

---

### Method 3: Direct Pytest

```bash
# All observation report tests
pytest tests/test_observation_report*.py -v

# Specific test suite
pytest tests/test_observation_report_ux_qa.py -v
```

---

## 📋 Agent Workflow

### After Code Changes:

1. **Run Automated Tests**
   ```bash
   ./tests/run_observation_report_qa_automated.sh
   ```

2. **Check Results**
   - Review test output
   - Check exit code (0 = success, 1 = failure)
   - Review screenshots in `test_screenshots/`

3. **Fix Issues** (if any)
   - Fix failing tests
   - Re-run tests
   - Verify fixes

4. **Continue**
   - All tests pass → Mark task complete
   - Tests fail → Fix and retry

---

## ✅ What Gets Tested

### Automatically Tested:

- ✅ **Images**: Load and display correctly
- ✅ **Colors**: Section and placeholder colors visible
- ✅ **Media Browser**: Subfolders displayed
- ✅ **Standards**: Units displayed
- ✅ **Functionality**: Drag-drop, reshuffle, assignments
- ✅ **Backend**: API endpoints, media scanning, drafts

### Test Reports Generated:

- `reports/observation_report_ux_qa.html` - HTML report
- `reports/observation_report_ux_qa.xml` - XML report (CI/CD)
- `test_screenshots/observation_report_ux_qa/` - Visual screenshots

---

## 🔧 Prerequisites

### Before Tests Can Run:

1. **Flask Server Running**
   ```bash
   python run.py
   ```

2. **Test Data Available**
   - Qualification folders in OUTPUT_FOLDER
   - Learner folders with media files
   - Optional: Saved drafts

3. **Dependencies Installed**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

---

## 🚨 Error Handling

The automated scripts will:
- ✅ Check Flask server before running
- ✅ Exit with error if server not running
- ✅ Show clear error messages
- ✅ Generate reports even if tests fail

---

## 📊 CI/CD Integration

These scripts are designed for:
- ✅ Automated agent execution
- ✅ CI/CD pipeline integration
- ✅ Pre-commit hooks
- ✅ Continuous testing

Exit codes:
- `0` = All tests passed
- `1` = Some tests failed

---

**Agents**: Just run `./tests/run_observation_report_qa_automated.sh` after making changes!



