# AC Matrix - Screenshot Testing Guide

## Overview
This guide outlines the screenshots to capture during Phase 8 testing to verify all functionality is working correctly.

## Screenshot Directory
Create: `docs/screenshots/ac-matrix/`

## Required Screenshots

### 1. Initial Page Load
**File**: `01-initial-page-load.png`
- Empty state with JSON file selector
- Draft loader dropdown (if drafts exist)
- Empty observation report textarea
- Analyze button (disabled state)
- Matrix section hidden

### 2. JSON File Selection
**File**: `02-json-file-selected.png`
- JSON file selected from dropdown
- Shows qualification name
- Observation report textarea ready

### 3. Draft Loading
**File**: `03-draft-loaded.png`
- Draft selected from dropdown
- "Load" button clicked
- Observation report textarea populated with draft text
- Shows section titles if present in draft

### 4. Observation Text Entered
**File**: `04-observation-text-entered.png`
- Observation report text entered (with sections and AC references)
- Example text with "SECTION:" headers
- AC references visible (e.g., "AC 1.1", "AC 2.1")

### 5. Analysis Complete - Vertical Style
**File**: `05-analysis-vertical-style.png`
- Matrix displayed in vertical style (default)
- 4-column layout visible:
  - Column 1: AC ID
  - Column 2: AC Description
  - Column 3: Status (COVERED/MISSING)
  - Column 4: Where Covered
- Coverage summary at top
- Section titles with colors (matching observation-media)
- Observation text sections visible for covered ACs
- Green rows for covered, red rows for missing

### 6. Vertical Style - Section Title Detail
**File**: `06-vertical-section-title-detail.png`
- Close-up of a covered AC row
- Section title with colored border (matching SECTION_COLORS)
- Observation text section below section title
- Clear "Where Covered" column content

### 7. Horizontal Style
**File**: `07-horizontal-style.png`
- Display style switched to "Horizontal"
- First line: All ACs in one row (e.g., "ACs: 1.1  1.2  1.3...")
- Second line: Status indicators (✓ for covered, ✗ for missing)
- ACs are clickable

### 8. Horizontal Style - Expanded Details
**File**: `08-horizontal-expanded-details.png`
- AC clicked to expand details
- Details panel showing:
  - AC ID and status
  - Section title (with color)
  - Observation text section
- Multiple ACs can be expanded

### 9. Save Matrix Dialog
**File**: `09-save-matrix-dialog.png`
- Save Matrix button clicked
- Modal dialog appears
- Matrix name input with suggested name
- Save and Cancel buttons

### 10. Matrix Saved
**File**: `10-matrix-saved.png`
- Success message after saving
- Matrix saved confirmation

### 11. Load Matrix Dropdown
**File**: `11-load-matrix-dropdown.png`
- Load Matrix button clicked
- Dropdown menu showing saved matrices
- Matrix names, dates, and file names visible

### 12. Matrix Loaded
**File**: `12-matrix-loaded.png`
- Matrix selected from dropdown
- All data restored:
  - JSON file selected
  - Observation report text populated
  - Matrix displayed with same data

### 13. Delete Matrix
**File**: `13-delete-matrix.png`
- Delete Matrix button clicked
- Confirmation prompt/dialog
- Matrix deletion confirmation

### 14. Complete Workflow
**File**: `14-complete-workflow.png`
- Full page showing:
  - JSON file selected
  - Observation report analyzed
  - Matrix displayed (vertical style)
  - All features accessible

### 15. Responsive - Desktop
**File**: `15-responsive-desktop.png`
- Full desktop view (1200px+)
- All columns visible
- Full layout

### 16. Responsive - Tablet
**File**: `16-responsive-tablet.png`
- Tablet view (768px - 1199px)
- Layout adapted
- Horizontal scrolling if needed

### 17. Responsive - Mobile
**File**: `17-responsive-mobile.png`
- Mobile view (< 768px)
- Single column layout
- Compact controls

### 18. Error States
**File**: `18-error-states.png`
- Error messages displayed:
  - No JSON file selected
  - Empty observation report
  - Invalid JSON file upload
  - Matrix not found

## Test Data for Screenshots

### Observation Report Text (with sections):
```
SECTION: Site Induction

During the site induction, AC 1.1 was covered when the site manager explained the workplace procedures. The operative demonstrated understanding of AC 1.2 by using safety equipment correctly.

SECTION: Hazard Reporting

Hazards were reported in accordance with AC 2.1 when a potential risk was identified during the work.

SECTION: Equipment Use

AC 7.1 was demonstrated when the operative used tools correctly.
```

### Expected Results:
- ACs found: 1.1, 1.2, 2.1, 7.1
- Section titles: "Site Induction" (index 0), "Hazard Reporting" (index 1), "Equipment Use" (index 2)
- Coverage: 4 out of 54 ACs (7.4%)

## Verification Checklist

For each screenshot, verify:
- [ ] Dark theme applied correctly
- [ ] Colors match observation-media (section titles)
- [ ] Text is readable
- [ ] Layout is correct
- [ ] No console errors
- [ ] All interactive elements work
- [ ] Responsive behavior correct

## Browser Testing

Test in:
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (if on Mac)

## Notes

- Screenshots should be PNG format
- Use descriptive filenames
- Capture full page or relevant sections
- Include browser console in some screenshots to show no errors
- Test with real data from `l2inter-performance.json`




