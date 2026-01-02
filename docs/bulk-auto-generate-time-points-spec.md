# Auto-Generate Time Points for Bulk Batch Selection - Specification

## Problem Statement
When users select videos in bulk mode and choose auto-generate time points (e.g., "5 shots"), the time points are not being generated correctly. The `selectedTimes` array remains empty, causing extraction to fail.

## Root Causes Identified
1. **Timing Issue**: When entering bulk mode, `videoInfo` is cleared, but video info loading is asynchronous
2. **Race Condition**: User can select "5 shots" before video info is loaded
3. **State Management**: Video info and time points are stored in multiple places (`firstVideo.info`, `window.appData.videoInfo`)
4. **No Feedback**: User doesn't know if video info is loading or if generation failed

## Requirements

### Functional Requirements
1. **Auto-generate MUST work immediately after selecting videos in bulk mode**
2. **Video info MUST be loaded automatically when videos are selected (if not already loaded)**
3. **Time points MUST be generated reliably when user selects a number from dropdown**
4. **Time points MUST persist through all state changes (mode switches, video selection, etc.)**
5. **User MUST see clear feedback during video info loading**

### Technical Requirements
1. **Synchronous Loading**: Video info should be loaded immediately when videos are selected, not lazily
2. **Single Source of Truth**: Use `window.appData.videoInfo` as primary source, with fallbacks
3. **Explicit State**: Clear separation between "loading", "ready", and "error" states
4. **Error Handling**: Proper error messages if video info cannot be loaded
5. **No Race Conditions**: Ensure video info is loaded before allowing time point generation

## Proposed Solution

### Architecture
```
User selects videos in bulk mode
    ↓
updateSelectionUI() called
    ↓
Check if first video has info
    ↓
If not: Load video info IMMEDIATELY (synchronous feeling, but async under hood)
    ↓
Store in: window.appData.videoInfo AND firstVideo.info
    ↓
Show sections (timeSection, etc.)
    ↓
User selects "5 shots" from dropdown
    ↓
Check: Is videoInfo loaded? YES → Generate immediately
                                NO → Show error/wait message
    ↓
Generate time points using videoInfo.duration
    ↓
Store in: window.appData.selectedTimes
    ↓
Update UI to show time points
```

### Implementation Details

#### 1. Video Info Loading (updateSelectionUI)
- When videos are selected and count > 0:
  - If first video has no info → Load immediately via fetch
  - Wait for response (show loading indicator)
  - Store in `window.appData.videoInfo` and `firstVideo.info`
  - Then show sections

#### 2. Auto-Generate Time Points (generateAutoTimePoints)
- Check: `window.appData.videoInfo` exists and has duration
- If not: Check `firstVideo.info`
- If still not: Error - "Please wait for video info to load"
- If yes: Call `generateAutoTimePointsWithDuration(numShots, duration)`

#### 3. State Management
- `window.appData.videoInfo`: Primary source of video duration (set when first video is loaded)
- `firstVideo.info`: Backup (for reference)
- `window.appData.selectedTimes`: Time points array (never cleared unintentionally)

#### 4. UI Feedback
- Show loading indicator when loading video info
- Disable dropdown while loading
- Show success message when time points are generated
- Show error message if generation fails

### Edge Cases
1. **Very short videos (< 0.1s)**: Generate at time 0 only
2. **No videos selected**: Show error, don't generate
3. **Video info load fails**: Show error, allow manual time entry
4. **Multiple rapid clicks**: Ignore duplicate generation requests

### Testing Requirements
1. Select videos → Wait 1 second → Select "5 shots" → Should work
2. Select videos → Immediately select "5 shots" → Should wait for video info, then generate
3. Select "5 shots" without videos → Should show error
4. Generate time points → Switch modes → Time points should persist

## Questions for Approval

1. **Loading Indicator**: Should we show a spinner/loading text while video info loads?
2. **Error Handling**: If video info fails to load, should we:
   - Show error and allow manual time entry?
   - Retry automatically?
   - Both?

3. **Timing**: How long should we wait for video info to load before showing error? (suggested: 5 seconds)

4. **User Experience**: Should we auto-select a default number of shots (e.g., 5) when videos are loaded in bulk mode?

## Approval
- [ ] Approved as-is
- [ ] Approved with modifications: _________________
- [ ] Not approved, concerns: _________________

---

**Next Steps After Approval**:
1. Implement video info loading in `updateSelectionUI`
2. Rework `generateAutoTimePoints` with proper state checks
3. Add loading indicators and error handling
4. Add comprehensive testing
5. Deploy and verify



