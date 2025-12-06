# Browser Testing Setup for Observation Media

This document explains how to set up and run automated browser tests for the Observation Media module.

## Prerequisites

1. **Python environment** with pytest installed
2. **Playwright browsers** installed
3. **Flask server** running (or use test server)

## Installation

### 1. Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

Or install all browsers:
```bash
playwright install
```

## Configuration

### Environment Variables

Set these environment variables before running tests:

```bash
# Base URL for the application (default: http://localhost:5000)
export TEST_BASE_URL="http://localhost:5000"

# Run in headless mode (default: true)
export HEADLESS="true"

# Add slow motion for debugging (default: 0ms)
export SLOW_MO="500"  # 500ms delay between actions
```

### Running the Flask Server

Before running tests, start the Flask server:

```bash
# In one terminal
python app.py
# or
flask run
```

Or use the test server fixture (if implemented).

## Running Tests

### Run All Browser Tests

```bash
pytest tests/test_observation_media_drag_drop.py -v
```

### Run Specific Test

```bash
pytest tests/test_observation_media_drag_drop.py::TestObservationMediaDragDrop::test_reshuffle_mode_toggle -v
```

### Run with Browser Visible (for debugging)

```bash
HEADLESS=false pytest tests/test_observation_media_drag_drop.py -v
```

### Run with Slow Motion (for debugging)

```bash
SLOW_MO=500 pytest tests/test_observation_media_drag_drop.py -v
```

### Generate HTML Report

```bash
pytest tests/test_observation_media_drag_drop.py --html=reports/browser_test_report.html
```

## Test Coverage

The browser tests cover:

1. **Page Loading**: Verifies the observation media page loads correctly
2. **Media Grid**: Checks that media grid is displayed
3. **Bulk Select**: Tests bulk select mode toggle
4. **Dialog Opening**: Verifies placeholder selection dialog opens
5. **Reshuffle Mode**: Tests reshuffle button and mode toggle
6. **Drag and Drop**: Tests drag-and-drop functionality in dialog
7. **Console Logs**: Verifies debugging logs are generated
8. **Text Editor**: Tests text editor functionality
9. **Full Workflow**: Tests complete user workflow

## Debugging Failed Tests

### 1. Run with Browser Visible

```bash
HEADLESS=false pytest tests/test_observation_media_drag_drop.py::TestName::test_name -v
```

### 2. Add Screenshots

Tests automatically take screenshots on failure (if configured).

### 3. Check Console Logs

The tests capture console messages. Check test output for browser console errors.

### 4. Use Slow Motion

```bash
SLOW_MO=1000 pytest tests/test_observation_media_drag_drop.py -v
```

### 5. Add Breakpoints

Add `page.pause()` in test code to pause execution and inspect:

```python
def test_example(page):
    page.goto("http://localhost:5000/v2p-formatter/observation-media")
    page.pause()  # Browser will pause here
    # ... rest of test
```

## Continuous Integration

For CI/CD, add to your pipeline:

```yaml
# Example GitHub Actions
- name: Install Playwright
  run: playwright install chromium

- name: Run Browser Tests
  run: pytest tests/test_observation_media_drag_drop.py --html=reports/browser_test_report.html
  env:
    TEST_BASE_URL: "http://localhost:5000"
    HEADLESS: "true"
```

## Troubleshooting

### Browsers Not Found

```bash
playwright install chromium
```

### Port Already in Use

Change the Flask port or set `TEST_BASE_URL` to a different port.

### Tests Timeout

Increase timeout in test code:
```python
page.wait_for_selector("#element", timeout=30000)  # 30 seconds
```

### Elements Not Found

- Check that the Flask server is running
- Verify the page URL is correct
- Check browser console for JavaScript errors
- Run with `HEADLESS=false` to see what's happening

## Adding New Tests

1. Add test methods to `TestObservationMediaDragDrop` class
2. Use Playwright's API for interactions:
   - `page.locator()` - Find elements
   - `expect()` - Assertions
   - `page.click()`, `page.fill()` - Interactions
   - `element.drag_to()` - Drag and drop
3. Use `time.sleep()` for delays if needed
4. Use `pytest.skip()` for conditional tests

Example:
```python
def test_new_feature(self, page_with_observation_media):
    page = page_with_observation_media
    element = page.locator("#myElement")
    expect(element).toBeVisible()
    element.click()
```

