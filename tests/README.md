# Selenium Testing Environment

This directory contains Selenium-based end-to-end tests for the Video to Image Formatter application.

## Setup

### 1. Install Dependencies

```bash
cd /Users/rom/Documents/nvq/apps/v2p-formatter
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install Chromium Browser

The tests use Chromium browser. You need Chromium installed on your system.

**macOS (Homebrew):**
```bash
brew install chromium
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install chromium-browser
```

**Linux (Fedora):**
```bash
sudo dnf install chromium
```

The tests use `webdriver-manager` which automatically downloads and manages ChromeDriver (compatible with Chromium).

### 3. Start the Application

Before running tests, make sure the Flask application is running:

```bash
source venv/bin/activate
python run.py
```

Or use the start script:
```bash
./start.sh
```

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test File

```bash
pytest tests/test_homepage.py
```

### Run Specific Test Class

```bash
pytest tests/test_homepage.py::TestHomepage
```

### Run Specific Test Method

```bash
pytest tests/test_homepage.py::TestHomepage::test_homepage_loads
```

### Run with Headless Mode

```bash
HEADLESS=true pytest tests/
```

### Check Chromium Installation

Before running tests, verify Chromium is installed:

```bash
./tests/setup_chromium.sh
```

If Chromium is not found, install it:

**macOS:**
```bash
brew install chromium
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# Fedora
sudo dnf install chromium
```

### Run with Verbose Output

```bash
pytest tests/ -v
```

### Run and Generate HTML Report

```bash
pytest tests/ --html=reports/report.html --self-contained-html
```

## Test Structure

- `conftest.py` - Pytest fixtures and configuration
- `test_homepage.py` - Homepage and basic UI tests
- `test_video_upload.py` - Video upload functionality tests
- `test_time_selection.py` - Time point selection tests
- `test_image_config.py` - Image configuration tests
- `test_pdf_config.py` - PDF configuration tests
- `test_processing.py` - Frame extraction and PDF generation tests

## Test Fixtures

### `driver`
Chrome WebDriver instance (created for each test)

### `wait`
WebDriverWait instance with 10-second timeout

### `base_url`
Base URL for the application (http://localhost/v2p-formatter)

### `flask_server`
Flask application server running in background thread

## Writing New Tests

### Basic Test Structure

```python
def test_example(driver, base_url, wait):
    """Test description"""
    driver.get(base_url)
    
    # Find element and interact
    element = wait.until(
        EC.presence_of_element_located((By.ID, "elementId"))
    )
    
    # Assert
    assert element.is_displayed()
```

### Common Patterns

**Wait for element:**
```python
element = wait.until(
    EC.presence_of_element_located((By.ID, "elementId"))
)
```

**Click element:**
```python
button = wait.until(EC.element_to_be_clickable((By.ID, "buttonId")))
button.click()
```

**Fill input:**
```python
input_field = driver.find_element(By.ID, "inputId")
input_field.clear()
input_field.send_keys("value")
```

**Select dropdown:**
```python
from selenium.webdriver.support.ui import Select
select = Select(driver.find_element(By.ID, "selectId"))
select.select_by_value("option_value")
```

## Configuration

### Environment Variables

- `HEADLESS=true` - Run tests in headless mode (no browser window)
- `BASE_URL` - Override base URL (default: http://localhost/v2p-formatter)

### Pytest Configuration

See `pytest.ini` for pytest configuration options.

## Troubleshooting

### ChromeDriver Issues

If you encounter ChromeDriver issues:
1. Make sure Chrome browser is installed
2. `webdriver-manager` should auto-download the correct version
3. Check Chrome version: `google-chrome --version` or `chromium --version`

### Tests Failing

1. **Check Flask app is running**: Tests require the Flask app to be running
2. **Check nginx is configured**: Tests access via http://localhost/v2p-formatter
3. **Check element selectors**: UI changes may require updating selectors
4. **Increase wait timeouts**: Some tests may need longer waits for slow operations

### Headless Mode Issues

If tests fail in headless mode:
- Some features may require visible browser
- Try running without headless mode first
- Check for JavaScript errors in console

## Continuous Integration

For CI/CD pipelines, use headless mode:

```bash
HEADLESS=true pytest tests/ --html=reports/report.html
```

## Best Practices

1. **Use explicit waits**: Always use `WebDriverWait` instead of `time.sleep()`
2. **Clean test data**: Clean up test files after tests
3. **Isolated tests**: Each test should be independent
4. **Meaningful assertions**: Use descriptive assertion messages
5. **Page Object Model**: Consider using POM for complex tests (future enhancement)

