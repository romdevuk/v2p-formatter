# Bulk Document Generation - Specification

## Problem Statement
Currently, document generation (PDF and DOCX) only works for single videos. When users select multiple videos in bulk mode and extract frames, they need to be able to generate documents for all selected videos at once with consistent settings.

## Current State
- Single video document generation works via `/generate_pdf` and `/generate_docx` endpoints
- Bulk extraction is implemented and stores results in `window.appData.batchResults`
- The "Generate PDF & DOCX" button shows up after bulk extraction, but clicking it fails with `startBulkDocumentGeneration is not defined`

## Requirements

### Functional Requirements
1. **Bulk Document Generation MUST process all successfully extracted videos**
2. **Settings MUST be applied consistently** - same layout, images per page, and output format for all videos
3. **Sequential Processing** - Process one video at a time to manage resources and provide clear progress
4. **Progress Tracking** - Show overall progress and per-video status (pending, processing, completed, error)
5. **Results Display** - Show download links for all generated documents, organized by video

### Technical Requirements
1. **Reuse Existing Endpoints** - Use `/generate_pdf` and `/generate_docx` endpoints for each video
2. **State Management** - Store document generation results in `window.appData.batchDocumentResults` or extend `window.appData.batchResults`
3. **Error Handling** - Continue processing remaining videos even if one fails
4. **User Feedback** - Display clear progress indicators and status messages

## Proposed Solution

### Architecture
```
User clicks "Generate Documents for All X Videos"
    ↓
processBulkDocumentGeneration() called
    ↓
Filter batchResults for successful extractions
    ↓
Get output settings (layout, imagesPerPage, outputFormat)
    ↓
Show batch progress UI
    ↓
For each video (sequential):
    ├─ Update status to "processing"
    ├─ Call /generate_pdf (if PDF selected)
    ├─ Call /generate_docx (if DOCX selected)
    ├─ Store results in batchResults[index].generatedDocuments
    ├─ Update status to "completed" or "error"
    └─ Update overall progress
    ↓
Show results summary with download links
```

### Implementation Details

#### 1. Function Structure
- `processBulkDocumentGeneration()` - Entry point, validates and initiates batch processing
- `startBulkDocumentGeneration(successfulResults)` - Main processing loop
- `updateBatchDocumentProgress(current, total, videoIndex, status)` - Update UI
- `showBulkDocumentGenerationResults()` - Display final results

#### 2. State Management
```javascript
window.appData.batchResults = [
    {
        videoPath: '/path/to/video.mp4',
        filename: 'video.mp4',
        status: 'completed',
        extractedImages: ['/path/img1.jpg', ...],
        generatedDocuments: {
            pdf: { file_path: '/path/output.pdf', filename: 'output.pdf' },
            docx: { file_path: '/path/output.docx', filename: 'output.docx' }
        }
    },
    ...
]
```

#### 3. UI Components
- **Progress Container**: Overall progress bar and percentage
- **Status List**: Per-video status with icons (⏳ pending, ⚙️ processing, ✅ completed, ❌ error)
- **Results Section**: Grid/list of download links organized by video

#### 4. API Calls
- `/generate_pdf`: `POST` with `{ video_path, image_paths, layout, images_per_page }`
- `/generate_docx`: `POST` with `{ video_path, image_paths, layout, images_per_page }`
- Both return `{ success: true, pdf_path/docx_path, filename }` on success

### User Flow

1. User selects multiple videos in bulk mode
2. User sets time points (auto-generate or manual)
3. User configures output settings (layout, images per page, format)
4. User clicks "Extract Frames" → Bulk extraction completes
5. "Generate Documents for All X Videos" button appears
6. User clicks button → Progress UI shows
7. System processes each video sequentially:
   - Shows "Processing video.mp4..."
   - Generates PDF (if selected)
   - Generates DOCX (if selected)
   - Updates progress
8. Results page shows all generated documents with download links

### Output Format Options
- **PDF Only**: Generate only PDF documents
- **DOCX Only**: Generate only DOCX documents  
- **Both**: Generate both PDF and DOCX documents (default)

### Error Handling
- If a video's PDF generation fails, continue with DOCX
- If all generation fails for a video, mark as error and continue
- Show error messages in results with option to retry individual videos
- Never stop entire batch due to one failure

### Edge Cases
1. **No successful extractions**: Show error, don't start generation
2. **Partial extraction success**: Only generate for videos with extracted images
3. **Very large batches**: Process sequentially to avoid memory issues
4. **Network errors**: Retry logic or clear error message

### Performance Considerations
- Sequential processing prevents overwhelming the server
- Progress updates provide user feedback during long operations
- Timeout handling for stuck operations (suggest 60 seconds per video)

## Questions for Approval

1. **Retry Logic**: Should failed document generations automatically retry, or only on user request?
   - **Recommendation**: No auto-retry, show error and allow manual retry

2. **Output Format Selection**: Should users be able to select format per-video, or same format for all?
   - **Recommendation**: Same format for all videos in batch (simpler UX)

3. **Results Storage**: Should generated documents be stored indefinitely, or cleaned up after download?
   - **Recommendation**: Keep until user explicitly clears or starts new batch

4. **Batch Size Limits**: Should there be a maximum number of videos for document generation?
   - **Recommendation**: Same limit as extraction (20 videos)

## Approval
- [x ] Approved as-is
- [ ] Approved with modifications: _________________
- [ ] Not approved, concerns: _________________

---

**Next Steps After Approval**:
1. Fix `startBulkDocumentGeneration` function definition and scope
2. Implement sequential processing loop
3. Add progress tracking UI
4. Implement error handling
5. Create results display component
6. Add comprehensive testing



