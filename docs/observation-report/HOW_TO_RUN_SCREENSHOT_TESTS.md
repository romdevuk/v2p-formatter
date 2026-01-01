# How to Run Screenshot Tests

## Quick Start

### 1. Ensure Flask Server is Running

```bash
cd /Users/rom/Documents/nvq/apps/v2p-formatter
python run.py
```

Server should be accessible at: `http://localhost/v2p-formatter`

### 2. Install Playwright (if not already installed)

```bash
# In your virtual environment
pip install playwright
playwright install chromium
```

### 3. Run Screenshot Tests

```bash
# Run all screenshot tests (headless mode)
pytest tests/test_observation_report_screenshots.py -v -s

# Run with visible browser (recommended for first run)
HEADLESS=false pytest tests/test_observation_report_screenshots.py -v -s

# Run a specific test
pytest tests/test_observation_report_screenshots.py::TestObservationReportScreenshots::test_01_initial_load -v -s
```

## Screenshots Generated

Screenshots will be saved to:
```
test_screenshots/observation_report_workflows/
```

Expected screenshots:
1. `01_initial_load.png` - Initial page load
2. `02_qualification_dropdown.png` - Qualification dropdown
3. `03_qualification_selected.png` - After selecting qualification
4. `04_learner_selected_media_loaded.png` - After selecting learner
5. `05_media_browser.png` - Media browser view
6. `06_text_with_placeholders.png` - Text editor with placeholders
7. `07_live_preview_placeholders.png` - Live preview showing placeholders
8. `08_before_drag.png` - Before drag operation
9. `09_after_drag.png` - After drag and drop
10. `10_draft_dialog.png` - Draft load dialog
11. `11_draft_loaded.png` - After loading draft
12. `12_standards_panel.png` - Standards panel (after loading draft)

## Troubleshooting

### Playwright Not Found

```bash
pip install playwright
playwright install chromium
```

### Flask Server Not Running

Start the server:
```bash
python run.py
```

Or check if it's running:
```bash
curl http://localhost/v2p-formatter/observation-report
```

### No Screenshots Generated

1. Check that the directory exists: `test_screenshots/observation_report_workflows/`
2. Check browser console for errors (when using `HEADLESS=false`)
3. Verify page loads correctly manually

### Tests Fail

1. Check Flask server logs for errors
2. Verify qualification/learner folders exist in OUTPUT_FOLDER
3. Run with `HEADLESS=false` to see what's happening



