# Browser Testing Environment - Setup Complete ✅

## Status
✅ **Playwright installed and working**  
✅ **Chromium browser installed**  
✅ **Test framework configured**  
✅ **Test files created and fixed**

## Quick Start

### 1. Start Flask Server
```bash
python app.py
# Server should run on http://localhost:5000
```

### 2. Run All Browser Tests
```bash
pytest tests/test_observation_media_drag_drop.py -v
```

### 3. Run Setup Verification
```bash
pytest tests/test_setup_verification.py -v
```

### 4. Run Specific Test
```bash
pytest tests/test_observation_media_drag_drop.py::TestObservationMediaDragDrop::test_reshuffle_mode_toggle -v
```

## Test Files Created

1. **`tests/test_observation_media_drag_drop.py`** - Main browser tests
   - Page loading tests
   - Media grid tests
   - Bulk select tests
   - Dialog opening/closing tests
   - Reshuffle mode tests
   - Drag-and-drop tests
   - Console log verification
   - Full workflow tests

2. **`tests/test_setup_verification.py`** - Setup verification tests
   - Playwright installation check
   - Browser navigation test
   - Server connectivity check
   - Page loading test

3. **`tests/conftest.py`** - Pytest fixtures
   - Browser fixtures
   - Page fixtures with console logging

4. **`tests/test_runner.py`** - Test runner script
   - Server health checks
   - Configurable test execution

## Running Tests

### Basic Usage
```bash
# Run all browser tests
pytest tests/test_observation_media_drag_drop.py -v

# Run with visible browser (for debugging)
HEADLESS=false pytest tests/test_observation_media_drag_drop.py -v

# Run with slow motion (for debugging)
SLOW_MO=500 pytest tests/test_observation_media_drag_drop.py -v

# Generate HTML report
pytest tests/test_observation_media_drag_drop.py --html=reports/browser_test_report.html
```

### Using Test Runner
```bash
# Check server and run tests
python tests/test_runner.py

# Run with visible browser
python tests/test_runner.py --headed

# Run with slow motion
python tests/test_runner.py --slow-mo 500

# Custom server URL
python tests/test_runner.py --url http://localhost:8000
```

## What Gets Tested

### ✅ Reshuffle Functionality
- Reshuffle button exists and is clickable
- Reshuffle mode toggles correctly
- Visual indicators are applied
- Console logs are generated

### ✅ Dialog Functionality
- Dialog opens when clicking media
- Dialog has correct content
- Dialog closes with cancel button
- Thumbnails are displayed

### ✅ Drag and Drop
- Thumbnails are draggable
- Drop zones accept drops
- Drag events fire correctly

### ✅ Page Elements
- Text editor is functional
- Media grid displays
- Preview area works
- All controls are accessible

## Debugging

### View Browser Actions
```bash
HEADLESS=false pytest tests/test_observation_media_drag_drop.py -v
```

### Slow Down Actions
```bash
SLOW_MO=1000 pytest tests/test_observation_media_drag_drop.py -v
```

### Pause Test Execution
Add `page.pause()` in test code to pause and inspect:
```python
def test_example(page):
    page.goto("http://localhost:5000/v2p-formatter/observation-media")
    page.pause()  # Browser will pause here
```

### Check Console Logs
Tests automatically capture console messages. Check test output for:
- `[RESHUFFLE]` logs
- `[DIALOG]` logs
- `[DRAG]` logs
- `[ATTACH]` logs

## Files Modified/Created

### New Files
- `requirements-test.txt` - Test dependencies
- `tests/test_observation_media_drag_drop.py` - Main browser tests
- `tests/test_setup_verification.py` - Setup verification
- `tests/conftest.py` - Pytest fixtures
- `tests/test_runner.py` - Test runner script
- `setup_browser_tests.sh` - Setup script
- `tests/README_BROWSER_TESTING.md` - Detailed documentation
- `BROWSER_TESTING_SETUP.md` - This file

### Modified Files
- `static/js/observation-media.js` - Added extensive debugging logs

## Next Steps

1. **Start the Flask server** in one terminal
2. **Run the tests** in another terminal:
   ```bash
   pytest tests/test_observation_media_drag_drop.py -v
   ```
3. **Review the test results** - Tests will show what's working and what needs attention
4. **Fix any issues** found by the tests
5. **Re-run tests** to verify fixes

## Troubleshooting

### Server Not Running
```bash
# Start server first
python app.py
```

### Tests Timeout
- Increase timeout in test code
- Check server is responding
- Verify URL is correct

### Elements Not Found
- Run with `HEADLESS=false` to see what's happening
- Check browser console for JavaScript errors
- Verify page is fully loaded

### Playwright Not Found
```bash
pip install playwright
python -m playwright install chromium
```

## Success Criteria

✅ Playwright installed  
✅ Chromium browser installed  
✅ Test framework working  
✅ Tests can navigate to pages  
✅ Tests can interact with elements  
✅ Tests can verify console logs  
✅ Tests can perform drag-and-drop  

**All setup complete! Ready for automated testing!** 🎉

