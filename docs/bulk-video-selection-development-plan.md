# Bulk Video Selection - Staged Development Plan

## Overview
This document outlines the staged development approach for implementing bulk video selection feature.

## Development Stages

### Stage 1: Backend - Batch Extraction Validation ✅
**Goal**: Add backend support for validating batch video processing and time point validation per video.

**Tasks**:
- [ ] Create endpoint to validate time points against video duration
- [ ] Create endpoint to get video info for multiple videos at once
- [ ] Add validation logic for time points per video
- [ ] Return warnings for invalid time points (exceeding duration)

**API Endpoints**:
- `POST /v2p-formatter/validate_batch_time_points` - Validate time points for multiple videos
- `POST /v2p-formatter/batch_video_info` - Get info for multiple videos

**Testing**:
- [ ] Unit tests for time point validation
- [ ] Test with videos of different durations
- [ ] Test with invalid time points
- [ ] Test with empty video list

---

### Stage 2: Backend - Batch Document Generation Support ✅
**Goal**: Ensure existing endpoints can handle batch processing (multiple sequential requests).

**Tasks**:
- [ ] Review existing `/extract_frames` endpoint (should work as-is)
- [ ] Review existing `/generate_pdf` and `/generate_docx` endpoints (should work as-is)
- [ ] Add any necessary error handling improvements
- [ ] Document batch processing approach (sequential requests)

**Testing**:
- [ ] Test sequential extraction for 3 videos
- [ ] Test sequential document generation for 3 videos
- [ ] Test error recovery (one video fails, others continue)

---

### Stage 3: Backend - Error Handling and Validation Per Video ✅
**Goal**: Ensure robust error handling for batch operations.

**Tasks**:
- [ ] Improve error messages for missing/corrupted videos
- [ ] Add validation for disk space availability
- [ ] Add timeout handling for long operations
- [ ] Ensure partial failures don't stop batch processing

**Testing**:
- [ ] Test with missing video file
- [ ] Test with corrupted video file
- [ ] Test with insufficient disk space scenario
- [ ] Test timeout handling

---

### Stage 4: Frontend - Bulk Selection UI Components ✅
**Goal**: Implement UI for bulk video selection.

**Tasks**:
- [ ] Add bulk selection mode toggle
- [ ] Add checkboxes to video cards (visible in bulk mode)
- [ ] Implement "Select All" functionality
- [ ] Add visual indicators for selected videos
- [ ] Add selection count badge
- [ ] Handle mode switching (clear selections when switching)

**Testing**:
- [ ] Manual UI testing: Toggle bulk mode
- [ ] Manual UI testing: Select/deselect videos
- [ ] Manual UI testing: Select All
- [ ] Visual regression: Selected video styling

---

### Stage 5: Frontend - Batch Processing Logic and Progress Tracking ✅
**Goal**: Implement batch processing with progress tracking.

**Tasks**:
- [ ] Update state management for bulk mode
- [ ] Implement batch extraction logic (sequential processing)
- [ ] Implement batch document generation logic
- [ ] Add progress tracking per video
- [ ] Update UI for batch mode indicators
- [ ] Update button labels for bulk mode

**Testing**:
- [ ] Test batch extraction with 3 videos
- [ ] Test batch document generation with 3 videos
- [ ] Test progress tracking accuracy
- [ ] Test cancellation (if implemented)

---

### Stage 6: Frontend - Results Display and Error Handling ✅
**Goal**: Display batch results with proper error handling.

**Tasks**:
- [ ] Create results summary display
- [ ] Show per-video status (✅/❌)
- [ ] Display download links grouped by video
- [ ] Show error messages for failed videos
- [ ] Add retry functionality for failed videos (optional)

**Testing**:
- [ ] Test results display with all successes
- [ ] Test results display with partial failures
- [ ] Test download links functionality
- [ ] Test error message display

---

## Testing Strategy

### Backend Tests (Stages 1-3)
**Location**: `tests/test_bulk_video_backend.py`

**Test Cases**:
1. `test_validate_batch_time_points_valid` - Valid time points for all videos
2. `test_validate_batch_time_points_invalid` - Some videos have invalid time points
3. `test_batch_video_info_success` - Get info for multiple videos
4. `test_batch_video_info_missing_file` - Handle missing video files
5. `test_sequential_extraction` - Extract frames for multiple videos sequentially
6. `test_sequential_generation` - Generate documents for multiple videos sequentially
7. `test_partial_failure_handling` - One video fails, others succeed

### Frontend Tests (Stages 4-6)
**Location**: `tests/test_bulk_video_frontend.py`

**Test Cases** (Playwright):
1. `test_bulk_mode_toggle` - Toggle between single and bulk mode
2. `test_video_selection` - Select/deselect videos in bulk mode
3. `test_select_all` - Select all videos functionality
4. `test_batch_extraction_flow` - Complete batch extraction flow
5. `test_batch_generation_flow` - Complete batch document generation flow
6. `test_progress_tracking` - Verify progress updates correctly
7. `test_results_display` - Verify results are displayed correctly
8. `test_error_handling` - Verify error messages appear correctly

---

## Implementation Order

1. ✅ **Stage 1**: Backend validation APIs
2. ✅ **Stage 2**: Backend batch processing support (review existing endpoints)
3. ✅ **Stage 3**: Backend error handling improvements
4. ✅ **Stage 4**: Frontend bulk selection UI
5. ✅ **Stage 5**: Frontend batch processing logic
6. ✅ **Stage 6**: Frontend results display

---

## Success Criteria per Stage

### Stage 1 Success
- ✅ Validation endpoint returns correct warnings for invalid time points
- ✅ Batch video info endpoint returns info for all requested videos
- ✅ All tests pass

### Stage 2 Success
- ✅ Existing endpoints handle sequential batch requests correctly
- ✅ No breaking changes to single video processing
- ✅ All tests pass

### Stage 3 Success
- ✅ Error handling works correctly for various failure scenarios
- ✅ Partial failures don't stop batch processing
- ✅ All tests pass

### Stage 4 Success
- ✅ Bulk selection mode toggle works
- ✅ Videos can be selected/deselected
- ✅ Visual indicators are clear
- ✅ Mode switching works correctly

### Stage 5 Success
- ✅ Batch processing completes successfully
- ✅ Progress tracking shows accurate status
- ✅ UI updates correctly during processing

### Stage 6 Success
- ✅ Results display correctly
- ✅ Download links work
- ✅ Error messages are clear

---

## Rollout Plan

1. **Development**: Complete all stages
2. **Internal Testing**: Test with 5-10 videos
3. **User Acceptance**: Test with real use cases
4. **Deployment**: Deploy to production

---

## Notes

- Backend changes should be backward compatible (single video mode still works)
- Frontend should gracefully handle mode switching
- All tests should pass before moving to next stage
- Document any API changes


