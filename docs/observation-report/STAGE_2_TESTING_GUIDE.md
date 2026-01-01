# 🧪 Stage 2: Frontend Libraries - Testing Guide

**Purpose**: Manual testing guide for implemented libraries  
**Target**: Frontend Developer (Agent-2), Tester (Agent-4)

---

## 📋 Pre-Testing Setup

### 1. Backend API Verification
Ensure backend APIs are running and accessible:
```bash
# Test media API
curl "http://localhost:5000/observation-report/media?qualification=Inter&learner=John_Doe"

# Test learners API
curl "http://localhost:5000/observation-report/learners?qualification=Inter"
```

### 2. HTML Test Page
Create a simple HTML test page to test libraries in isolation:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Observation Report - Library Tests</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .container { margin: 20px 0; border: 1px solid #ccc; padding: 20px; }
        #mediaBrowser { min-height: 300px; }
        #livePreview { min-height: 400px; }
    </style>
</head>
<body>
    <h1>Observation Report Library Tests</h1>
    
    <div class="container">
        <h2>Media Browser</h2>
        <div id="mediaBrowser"></div>
    </div>
    
    <div class="container">
        <h2>Live Preview</h2>
        <div id="livePreview"></div>
    </div>
    
    <script src="/static/js/observation-report/observation-report-media-browser.js"></script>
    <script src="/static/js/observation-report/observation-report-live-preview.js"></script>
    <script>
        // Initialize libraries
        const mediaBrowser = new ObservationReportMediaBrowser('mediaBrowser');
        const livePreview = new ObservationReportLivePreview('livePreview');
        
        // Test loading
        mediaBrowser.loadMedia('Inter', 'John_Doe');
        
        // Set up event listeners
        mediaBrowser.on('mediaDragStart', (data) => {
            console.log('Drag started:', data);
        });
        
        livePreview.on('mediaAssignment', (data) => {
            console.log('Media assigned:', data);
            mediaBrowser.updateAssignmentState(data.assignments);
        });
    </script>
</body>
</html>
```

---

## 🧪 Test Cases

### Media Browser Library Tests

#### Test 1: Initialization
**Steps**:
1. Load test page
2. Check if Media Browser container initializes
3. Check console for errors

**Expected**:
- ✅ Container renders with header and grid
- ✅ No console errors
- ✅ "Media Browser" header visible

#### Test 2: Load Media
**Steps**:
1. Call `mediaBrowser.loadMedia('Inter', 'John_Doe')`
2. Wait for API response
3. Check media grid

**Expected**:
- ✅ Media cards appear in grid
- ✅ Thumbnails display (for images)
- ✅ File type icons show (for non-images)
- ✅ Filenames visible
- ✅ Media count shows correct number

#### Test 3: Single Media Drag
**Steps**:
1. Select a media item
2. Drag it to Live Preview drop zone
3. Drop on placeholder

**Expected**:
- ✅ Media card becomes draggable
- ✅ Drag visual feedback appears
- ✅ Drop zone highlights on drag over
- ✅ Media appears in placeholder table after drop

#### Test 4: Bulk Media Drag
**Steps**:
1. Select multiple media items (checkboxes)
2. Drag one selected item
3. Drop on placeholder

**Expected**:
- ✅ All selected items drag together
- ✅ Multiple items appear in placeholder table
- ✅ Items positioned correctly in 2-column layout

#### Test 5: Filename Editing
**Steps**:
1. Click on filename in media card
2. Edit filename
3. Press Enter or click away

**Expected**:
- ✅ Filename becomes editable
- ✅ API call to rename file
- ✅ Filename updates on success
- ✅ Error message on failure

#### Test 6: Assignment State
**Steps**:
1. Assign media to placeholder
2. Update assignment state: `mediaBrowser.updateAssignmentState(assignments)`
3. Check media cards

**Expected**:
- ✅ Assigned media becomes non-draggable
- ✅ Visual indicator (e.g., checkmark) appears
- ✅ Media count updates

---

### Live Preview Library Tests

#### Test 7: Placeholder Extraction
**Steps**:
1. Set text content with placeholders: `{{Placeholder1}}` and `{{Placeholder2}}`
2. Call `livePreview.updateContent(text, {}, [])`

**Expected**:
- ✅ Placeholders are highlighted
- ✅ Each placeholder gets unique color
- ✅ Colors match rainbow palette

#### Test 8: Placeholder Table Rendering
**Steps**:
1. Assign media to placeholder
2. Check table rendering

**Expected**:
- ✅ 2-column table created
- ✅ Media items appear in correct cells
- ✅ Images display in cells
- ✅ Filenames show for non-images

#### Test 9: Drop Zone Highlighting
**Steps**:
1. Drag media from Media Browser
2. Hover over drop zone

**Expected**:
- ✅ Drop zone highlights (border/background change)
- ✅ Visual feedback is clear
- ✅ Highlight disappears on drag leave

#### Test 10: Media Assignment (Single)
**Steps**:
1. Drag single media to placeholder
2. Drop on empty placeholder

**Expected**:
- ✅ Media appears in placeholder table
- ✅ Table structure maintained (2 columns)
- ✅ Assignment event emitted
- ✅ Media Browser updates (assigned state)

#### Test 11: Media Assignment (Multiple Placeholders)
**Steps**:
1. Have text with multiple placeholders
2. Drag multiple media items
3. Drop (should show selection dialog)

**Expected**:
- ✅ Selection dialog appears
- ✅ Can select target placeholder
- ✅ Media assigned to selected placeholder

#### Test 12: Media Reordering (Arrow Buttons)
**Steps**:
1. Assign multiple media items to placeholder
2. Click "Up" button on second item
3. Click "Down" button

**Expected**:
- ✅ Items swap positions
- ✅ Order updates in assignments
- ✅ Table re-renders correctly
- ✅ Position calculations correct

#### Test 13: Media Reordering (Drag-and-Drop)
**Steps**:
1. Assign multiple media items
2. Drag item to different position
3. Drop

**Expected**:
- ✅ Item moves to new position
- ✅ Other items adjust
- ✅ 2-column layout maintained
- ✅ Order persists

#### Test 14: Media Removal
**Steps**:
1. Click "×" button on media item
2. Confirm removal

**Expected**:
- ✅ Media removed from placeholder
- ✅ Other items reorder if needed
- ✅ Table updates
- ✅ Media Browser updates (unassigned)

#### Test 15: Section Rendering
**Steps**:
1. Set text with `SECTION Header:` format
2. Check section rendering

**Expected**:
- ✅ Section headers appear
- ✅ Expand/collapse toggle works
- ✅ Section content shows/hides
- ✅ Placeholders within sections render

#### Test 16: Position Calculations
**Steps**:
1. Test position → row/col conversion
2. Test row/col → position conversion

**Test Cases**:
- Position 0 → Row 0, Col 0 ✅
- Position 1 → Row 0, Col 1 ✅
- Position 2 → Row 1, Col 0 ✅
- Position 3 → Row 1, Col 1 ✅
- Position 5 → Row 2, Col 1 ✅

**Expected**:
- ✅ All calculations correct
- ✅ Round-trip conversion works

---

## 🔗 Integration Tests

### Test 17: End-to-End Workflow
**Steps**:
1. Load media in Media Browser
2. Load text content in Live Preview
3. Drag media to placeholder
4. Reorder media
5. Remove media
6. Save draft

**Expected**:
- ✅ All operations work smoothly
- ✅ State synchronized between libraries
- ✅ No errors or inconsistencies

---

## ⚠️ Known Issues to Test

1. **Image Serving**: Test if images load correctly
   - May need route handler in backend
   - Test with different image paths

2. **Placeholder Dialog**: Test multiple placeholder selection
   - Currently uses `prompt()` - basic but functional

3. **Large Media Lists**: Test performance with 50+ media items
   - Check rendering speed
   - Check drag performance

---

## 📊 Test Results Template

```
Test #: [Number]
Name: [Test Name]
Status: [✅ Pass | ❌ Fail | ⚠️ Partial]
Notes: [Any observations]
```

---

## ✅ Completion Criteria

All tests should pass before proceeding to:
- Remaining library implementation
- Stage 3 (UX) integration
- Stage 4 (Full testing)

---

**Created**: 2025-01-XX  
**Last Updated**: 2025-01-XX



