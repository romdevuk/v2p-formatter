# Bulk Video Selection Feature - Specification

## Overview
Add bulk video selection capability to the Video to Image Formatter (`/v2p-formatter/`) page. When videos are bulk selected, users can apply the same time points, output settings, and output format to all selected videos in a batch operation.

## Feature Goals
- Enable selection of multiple videos simultaneously
- Apply identical processing settings (time points, output settings, format) to all selected videos
- Process videos in batch mode
- Maintain backward compatibility with single video selection

---

## User Interface Requirements

### 1. Video Selection Section
**Location**: Section 1 - "Select Video"

#### Current State
- Videos displayed as individual cards with thumbnails
- Clicking a video card selects that single video
- Single video selection shows video player, time selection, and settings

#### Proposed Changes

##### 1.1 Bulk Selection Controls
**Add to top of video list:**
- **"Select All" checkbox** - Selects/deselects all visible videos
- **Bulk selection mode toggle** - Toggle between "Single Video Mode" (default) and "Bulk Selection Mode"
  - In Bulk Selection Mode: Clicking video cards adds/removes them from selection (checkbox-style)
  - In Single Video Mode: Clicking a video card selects it immediately (current behavior)

##### 1.2 Visual Indicators for Selected Videos
**In Bulk Selection Mode:**
- Selected videos show:
  - Checkmark icon (✓) in top-right corner of thumbnail
  - Highlighted border (e.g., #667eea color)
  - Background color change (e.g., slightly lighter background)
- Selection count badge: "X videos selected" displayed above video list

##### 1.3 Video Card Enhancements
**Add to each video card:**
- Checkbox (visible only in Bulk Selection Mode)
- Visual feedback on hover/selection
- Click area clearly indicates selection vs. immediate action

---

### 2. Time Points Selection Section
**Location**: Section 2 - "Select Time Points from Video"

#### Current Behavior
- Shows video player for currently selected video
- Time points are added for that specific video

#### Proposed Behavior for Bulk Mode

##### 2.1 Bulk Mode Indicator
- **Header change**: "2. Select Time Points from Video (Batch Mode)"
- **Info message**: "Time points will be applied to all X selected videos"

##### 2.2 Video Player Behavior
- **Option A (Recommended)**: Show preview video (first selected video) for reference
  - Display message: "Preview: [Video Name]. Time points will apply to all selected videos."
  - Video player is for reference only (cannot change selected video)

- **Option B**: Show thumbnail carousel of all selected videos
  - Allows quick visual confirmation of selected videos
  - More complex UI

##### 2.3 Time Point Selection
- Time points work exactly as current implementation
- When "Extract Frames" is clicked, same time points applied to ALL selected videos

---

### 3. Output Settings Section
**Location**: Section 3 - "Output Settings"

#### Current Behavior
- Settings apply to currently selected video

#### Proposed Behavior for Bulk Mode
- **Header change**: "3. Output Settings (Batch Mode)"
- **Info message**: "These settings will apply to all X selected videos"
- Settings work identically to single video mode
- All selected videos will use:
  - Same quality setting
  - Same resolution
  - Same output format (PDF/DOCX)
  - Same layout options (if PDF)

---

### 4. Processing Section
**Location**: Section 4 - "Process"

#### Current Behavior
- "Extract Frames" button processes single video
- "Generate PDF & DOCX" button generates documents for single video

#### Proposed Behavior for Bulk Mode

##### 4.1 Button Labels
- **Single Mode**: "Extract Frames" / "Generate PDF & DOCX"
- **Bulk Mode**: "Extract Frames for All X Videos" / "Generate Documents for All X Videos"

##### 4.2 Progress Tracking
**Enhanced progress display:**
- Overall progress: "Processing video 3 of 10..."
- Per-video progress: Show current video name
- Progress bar shows overall completion (0-100% across all videos)
- Individual video status indicators:
  - ✅ Completed
  - ⏳ Processing
  - ⏸️ Pending
  - ❌ Error

##### 4.3 Results Display
**After batch completion:**
- Summary: "Successfully processed X of Y videos"
- List of all generated files:
  - Grouped by video
  - Download links for each PDF/DOCX
  - Error messages for failed videos (if any)

---

## Technical Implementation

### 1. State Management

#### Global State Updates
```javascript
window.appData = {
    // Existing
    videoPath: null,        // Single video mode
    videoInfo: null,
    selectedTimes: [],
    extractedImages: [],
    
    // New for bulk mode
    bulkMode: false,        // true = bulk selection mode
    selectedVideos: [],     // Array of {path, name, info}
    currentBatchIndex: 0,   // Current video being processed
    batchResults: []        // Results for each video
};
```

### 2. UI Components

#### 2.1 Bulk Selection Toggle
- Toggle switch: "Single Video Mode" ↔ "Bulk Selection Mode"
- Default: Single Video Mode (backward compatible)

#### 2.2 Video Selection Handler
```javascript
function handleVideoClick(filePath, fileName) {
    if (window.appData.bulkMode) {
        // Toggle selection
        toggleVideoSelection(filePath, fileName);
    } else {
        // Current behavior: immediate selection
        selectSingleVideo(filePath, fileName);
    }
}
```

#### 2.3 Selection Management
- Array of selected video paths
- Visual updates on selection/deselection
- Validation: minimum 1 video required for bulk processing

### 3. Batch Processing Flow

#### 3.1 Extract Frames (Bulk)
```
1. Validate: At least one video selected, time points defined
2. For each selected video:
   a. Load video
   b. Extract frames at time points
   c. Store extracted images array
   d. Update progress
3. Show completion summary
```

#### 3.2 Generate Documents (Bulk)
```
1. Validate: Frames extracted for all videos
2. For each video with extracted frames:
   a. Generate PDF (if PDF format selected)
   b. Generate DOCX (if DOCX format selected)
   c. Store file paths
   d. Update progress
3. Show results with download links
```

### 4. Backend API Changes

#### 4.1 Extract Frames Endpoint
**Current**: `/v2p-formatter/extract_frames` (single video)

**New**: Support batch processing
- Option A: Multiple POST requests (one per video) - simpler, no backend changes
- Option B: New endpoint `/v2p-formatter/extract_frames_batch` - more efficient

**Recommended**: Option A (multiple requests) for simplicity

#### 4.2 Generate Documents Endpoint
**Current**: `/v2p-formatter/generate_pdf`, `/v2p-formatter/generate_docx` (single video)

**Same approach**: Multiple requests (one per video)

### 5. Error Handling

#### Scenarios
- Video file missing or corrupted
- Insufficient disk space
- Time points outside video duration
- Processing timeout

#### Handling
- Continue processing remaining videos
- Log errors per video
- Display error summary in results
- Allow retry for failed videos

---

## User Flow Examples

### Flow 1: Bulk Process 5 Videos with Same Settings
1. Toggle to "Bulk Selection Mode"
2. Select 5 videos (checkboxes or clicks)
3. Confirm selection: "5 videos selected"
4. Section 2 appears: "Select Time Points from Video (Batch Mode)"
5. Select time points (applies to all 5 videos)
6. Configure output settings (applies to all 5 videos)
7. Click "Extract Frames for All 5 Videos"
8. Progress: "Processing video 1 of 5...", "Processing video 2 of 5...", etc.
9. Click "Generate Documents for All 5 Videos"
10. Results: List of all generated PDFs/DOCX with download links

### Flow 2: Switch Back to Single Video Mode
1. User in Bulk Selection Mode
2. Toggle back to "Single Video Mode"
3. Selected videos cleared (or convert first selection to active video)
4. UI reverts to single video behavior

---

## Edge Cases & Considerations

### 1. Video Compatibility
- **Issue**: Different videos may have different durations
- **Solution**: Validate time points against each video's duration before processing
- **Fallback**: Auto-adjust time points that exceed video duration (clamp to duration)

### 2. Large Batch Sizes
- **Issue**: Processing 50+ videos could take hours
- **Solution**: 
  - Show estimated time remaining
  - Allow cancellation
  - Process in smaller batches (optional)

### 3. Partial Failures
- **Issue**: Some videos succeed, others fail
- **Solution**: 
  - Continue processing all videos
  - Show detailed results per video
  - Allow selective retry

### 4. Resource Management
- **Issue**: Processing multiple videos simultaneously could overwhelm system
- **Solution**: Process sequentially (one video at a time)

---

## Visual Design Specifications

### Colors
- Selected video border: `#667eea` (accent color)
- Selected video background: `#2a3a4a` (slightly lighter than `#2a2a2a`)
- Checkmark icon: `#4ade80` (green)
- Bulk mode indicator: `#fbbf24` (yellow/amber) badge

### Icons
- ✓ Checkmark (selected)
- ☐ Empty checkbox (unselected)
- 🔄 Batch processing indicator
- ⚠️ Warning icon (bulk mode info)

### Typography
- Bulk mode indicator: Bold, 14px
- Selection count: Bold, 16px
- Info messages: Italic, 13px, color `#999`

---

## Implementation Phases

### Phase 1: UI - Bulk Selection
- [ ] Add bulk selection mode toggle
- [ ] Add checkboxes to video cards
- [ ] Implement selection state management
- [ ] Visual feedback for selected videos
- [ ] "Select All" functionality

### Phase 2: UI - Batch Mode Indicators
- [ ] Update section headers for bulk mode
- [ ] Add info messages
- [ ] Update button labels
- [ ] Progress display enhancements

### Phase 3: Processing Logic
- [ ] Batch extraction logic
- [ ] Batch document generation
- [ ] Progress tracking per video
- [ ] Error handling per video

### Phase 4: Results & Testing
- [ ] Results summary display
- [ ] Download links per video
- [ ] Error reporting
- [ ] Testing with various batch sizes
- [ ] Edge case testing

---

## Questions for Approval

### 1. Video Player in Bulk Mode
**Question**: In bulk selection mode, should the video player:
- **Option A**: Show first selected video as preview (recommended)
- **Option B**: Show thumbnail carousel of all selected videos
- **Option C**: Hide video player entirely (only show time points UI)

**Recommendation**: Option A (simpler, cleaner) - yes

### 2. Time Points Validation
**Question**: Should time points be validated against each video's duration:
- **Before processing starts** (show warnings for invalid time points per video)
- **During processing** (auto-adjust invalid time points)

**Recommendation**: Validate before processing, show warnings, allow user to adjust - yes

### 3. Concurrent vs Sequential Processing
**Question**: Process videos:
- **Sequentially** (one at a time) - recommended for simplicity and resource management
- **Concurrently** (multiple at once) - faster but more complex

**Recommendation**: Sequential (one video at a time) - yes

### 4. Batch Size Limits
**Question**: Should there be a maximum number of videos that can be selected at once?
- **Option A**: No limit
- **Option B**: Limit to X videos (e.g., 20) with warning

**Recommendation**: Option B - Limit to 20 videos with warning message - yes

### 5. Default Mode
**Question**: Should bulk selection mode:
- **Option A**: Be opt-in (toggle to enable) - recommended
- **Option B**: Be default with option to switch to single mode

**Recommendation**: Option A (backward compatible, less disruptive)  - yes

### 6. Switching Modes
**Question**: When switching from bulk mode back to single mode:
- **Option A**: Clear all selections (start fresh)
- **Option B**: Keep first selected video as active

**Recommendation**: Option A (clearer UX) - yes

---

## Success Criteria

### Functional Requirements
✅ Users can select multiple videos simultaneously
✅ Selected videos have clear visual indicators
✅ Time points apply to all selected videos
✅ Output settings apply to all selected videos
✅ Batch processing completes successfully
✅ Progress tracking shows per-video status
✅ Results display all generated files with download links
✅ Error handling works correctly (partial failures)

### Performance Requirements
✅ Batch of 10 videos completes within reasonable time (< 30 minutes for typical videos)
✅ UI remains responsive during batch processing
✅ Progress updates every 2-5 seconds

### UX Requirements
✅ Bulk selection is intuitive and discoverable
✅ Mode switching is clear and non-destructive
✅ Users understand which mode they're in
✅ Error messages are clear and actionable

---

## Documentation Updates Required

- [ ] Update user guide with bulk selection instructions
- [ ] Add screenshots/wireframes to documentation
- [ ] Update API documentation (if new endpoints added)
- [ ] Add troubleshooting guide for batch processing

---

## Appendix: Wireframe Sketches

### Video Selection with Bulk Mode
```
┌─────────────────────────────────────────────────────┐
│ 1. Select Video                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│ [Single Video Mode] ←→ [Bulk Selection Mode]  🔄   │
│                                                     │
│ [☐ Select All]  Videos Selected: 3                │
│                                                     │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐              │
│ │ [✓] 🎬  │ │ [✓] 🎬  │ │ [✓] 🎬  │              │
│ │ Video 1 │ │ Video 2 │ │ Video 3 │              │
│ └─────────┘ └─────────┘ └─────────┘              │
│                                                     │
│ ┌─────────┐ ┌─────────┐                            │
│ │ [ ] 🎬  │ │ [ ] 🎬  │                            │
│ │ Video 4 │ │ Video 5 │                            │
│ └─────────┘ └─────────┘                            │
└─────────────────────────────────────────────────────┘
```

### Batch Processing Progress
```
┌─────────────────────────────────────────────────────┐
│ Processing video 3 of 10                            │
├─────────────────────────────────────────────────────┤
│ [████████░░░░░░░░░░] 30%                           │
│                                                     │
│ Current: video_003.mp4                             │
│                                                     │
│ Status:                                            │
│ ✅ video_001.mp4 - Completed                       │
│ ✅ video_002.mp4 - Completed                       │
│ ⏳ video_003.mp4 - Processing...                   │
│ ⏸️ video_004.mp4 - Pending                        │
│ ⏸️ video_005.mp4 - Pending                        │
│ ...                                                │
└─────────────────────────────────────────────────────┘
```

---

**Document Version**: 1.0  
**Created**: 2025-01-XX  
**Status**: Pending Approval  
**Author**: Development Team

**Next Steps**: Review spec, answer questions, approve design, proceed with implementation


