# Testing Guide

## Running Tests

### Complete Workflow Tests
Tests the full application workflow with Selenium:
```bash
cd /Users/rom/Documents/nvq/apps/v2p-formatter
source venv/bin/activate
pytest tests/test_complete_workflow.py -v --html=tests/reports/test_report.html --self-contained-html
```

### File Verification Tests
Verifies that PDF and JPG files are created correctly:
```bash
pytest tests/test_file_verification.py -v --html=tests/reports/file_verification_report.html --self-contained-html
```

### Run All Tests
```bash
./tests/run_all_tests.sh
```

## Test Scenarios

### Scenario 1: Single Frame Extraction
- Load file tree
- Select a video file
- Extract single frame at time point 5 seconds
- Generate PDF
- Verify files created

### Scenario 2: Multiple Frames Extraction
- Select video file
- Extract frames at multiple time points (5, 10, 15, 20 seconds)
- Generate PDF with multiple frames
- Verify files created

### Scenario 3: Verify Files Created
- Complete workflow
- Verify JPG files (1.jpg, 2.jpg, 3.jpg) exist
- Verify PDF file exists
- Check file locations

### Scenario 4: Different Video File
- Test with a different video file
- Verify application works with various files

## Test Reports

Test reports are generated in `tests/reports/`:
- `test_report.html` - Complete workflow test results
- `file_verification_report.html` - File verification results

Open reports in a browser:
```bash
open tests/reports/test_report.html
```

## Expected Output Files

After successful tests, you should find:

1. **PDF Files**: In the same directory as the video file
   - Example: `/Users/rom/Documents/nvq/visited/css/L2 Cladding/eduards bormanis/mp4/IMG_7560.pdf`

2. **JPG Files**: In a `_frames` subdirectory
   - Example: `/Users/rom/Documents/nvq/visited/css/L2 Cladding/eduards bormanis/mp4/IMG_7560_frames/1.jpg`
   - Files are numbered: 1.jpg, 2.jpg, 3.jpg, etc.

## Troubleshooting

### Tests Fail with Timeout
- Ensure Flask app is running: `python run.py`
- Check that nginx is configured correctly
- Verify the application is accessible at `http://localhost/v2p-formatter/`

### File Tree Not Loading
- The file scan can take time (756 files)
- Tests wait up to 30 seconds for file tree to load
- Check browser console for JavaScript errors

### Files Not Found
- Run file verification test to check existing files
- Verify video files exist in `/Users/rom/Documents/nvq/visited`
- Check file permissions

