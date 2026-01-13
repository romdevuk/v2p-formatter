# Changelog

All notable changes to the Video to Image Formatter (v2p-formatter) project will be documented in this file.

## [2026-01-11] - Deface Module Enhancements

### Added

#### Export MP4 Videos Feature
- **Export MP4 Videos checkbox**: Added option to export defaced MP4 videos alongside PDF/DOCX documents
  - Checkbox option in "3. Output Settings" section
  - When enabled, defaced MP4 videos are copied to the output folder
  - Videos are exported with the same `deface_` prefix as other output files
  - Export links displayed in results section after document generation
  - Supports exporting multiple videos when processing multiple media items

#### Progress Simulation During Deface Processing
- **Progress bar animation**: Added progress simulation during deface processing
  - Progress bar gradually increases from 0% to 90% while waiting for API response
  - Updates every 500ms for smooth visual feedback
  - Reaches 100% when processing completes
  - Provides better user experience during longer processing operations

#### Manual Deface Modal Auto-Close
- **Automatic modal closure**: Manual deface modal now closes automatically after successful deface application
  - Modal closes immediately after manual deface is successfully applied
  - Review grid automatically updates with the new defaced image
  - User is returned to the review interface without manual close action
  - Improves workflow efficiency

### Changed

#### Separate Image and Video File Lists
- **File organization**: Separated images and videos into distinct sections with separate file lists
  - Images displayed in dedicated "Images" section with file count
  - Videos displayed in dedicated "Videos" section with file count
  - Each section has its own "Select All" checkbox functionality
  - File counts displayed per section (e.g., "(5 files)")
  - Improved organization and clarity for users

#### File Loading Function Refactoring
- **Renamed and enhanced file loading**: Refactored `loadImages()` to `loadDefaceFiles()`
  - Function now accepts qualification and learner parameters
  - Separates files by type (image/video) using backend `type` field
  - Updated rendering functions: `renderImageListDeface()` and `renderVideoListDeface()`
  - Better error handling with separate error messages per section
  - Added `updateFileCounts()` function to update file count displays

#### Session Persistence Fix
- **Flask auto-reloader disabled**: Fixed session expiration by disabling Flask's auto-reloader in debug mode
  - Added `use_reloader=False` to `app.run()` in `run.py`
  - Prevents server restarts on file changes that clear in-memory sessions
  - Sessions now persist correctly between requests during workflow
  - Debug mode remains active (only auto-reloader disabled)

### Technical Details

#### Backend Changes
- **`app/routes.py`**:
  - Added `export_mp4_videos` parameter to `generate_deface_documents` endpoint
  - Implemented MP4 video export logic that copies defaced videos to output folder
  - Added `exported_videos` array to response with video metadata and download URLs
  - Videos exported to same output folder as PDF/DOCX documents

- **`run.py`**:
  - Added `use_reloader=False` parameter to `app.run()` call
  - Prevents Flask auto-reloader from restarting server on file changes
  - Sessions persist correctly between requests

#### Frontend Changes
- **`templates/deface.html`**:
  - Added "Export MP4 Videos" checkbox in output settings section
  - Separated file display into `imageFilesList` and `videoFilesList` containers
  - Added `renderImageListDeface()` and `renderVideoListDeface()` functions
  - Added `updateFileCounts()` function for dynamic file count updates
  - Added `toggleSelectAllDeface()` function for separate image/video selection
  - Added progress simulation interval in `applyDeface()` function
  - Added `closeManualDefaceModal()` call after successful manual deface
  - Updated `loadDefaceFiles()` function to handle separate image/video lists
  - Added `toggleSection()` function for collapsible sections
  - Updated results display to show exported MP4 videos with download links

### 🎯 Benefits
- **Better Organization**: Separate image and video sections improve clarity and usability
- **Enhanced Workflow**: Auto-closing modal streamlines manual deface editing process
- **Visual Feedback**: Progress simulation provides better user experience during processing
- **Video Export**: Option to export defaced MP4 videos provides complete output package
- **Session Persistence**: Fixed session management ensures reliable workflow completion

## [2026-01-11] - Static File Serving Fix, Template Updates, and Server Configuration

### 🐛 Fixed

#### Static File MIME Type Errors and 502 Bad Gateway
- **Fixed CSS and JavaScript files being served with wrong MIME types**: Static files (CSS/JS) were being served with `application/json` or `text/html` MIME types instead of `text/css` and `application/javascript`
  - **Root Cause**: Flask route handler for static files (`/static/<path:filename>`) was interfering and returning JSON error responses, and nginx location block order was causing static files to be proxied to Flask instead of served directly
  - **Solution**: 
    - Removed Flask static file route handler (`/v2p-formatter/static/<path:filename>`) from `app/routes.py`
    - Updated nginx configuration to serve static files directly (static location block must come before app location block)
    - Static files are now served directly by nginx with correct MIME types
  - **Impact**: Static files now load correctly with proper MIME types, eliminating browser console errors and fixing 502 Bad Gateway errors
  - **Error Messages Fixed**:
    - `GET http://localhost/v2p-formatter/ 502 (Bad Gateway)`
    - `Refused to apply style from 'http://localhost/v2p-formatter/static/css/...' because its MIME type ('application/json') is not a supported stylesheet MIME type`
    - `werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'v2p_formatter.serve_static'`

#### Template Static File References
- **Fixed template errors after removing Flask static route**: Templates were still using `url_for('v2p_formatter.serve_static', ...)` which caused `BuildError` exceptions
  - **Solution**: Replaced all `url_for('v2p_formatter.serve_static', filename='...')` references with direct static paths `/v2p-formatter/static/...`
  - **Files Updated**:
    - `templates/base.html` - Updated CSS and JS references
    - `templates/observation_report.html` - Updated CSS and JS references
    - `templates/observation_media.html` - Updated JS references
    - `templates/ac_matrix.html` - Updated CSS and JS references
    - `templates/image_to_pdf.html` - Updated CSS and JS references
  - **Impact**: All templates now use direct static paths that nginx serves, eliminating Flask routing errors

### 📝 Technical Details

#### Files Modified
- `app/routes.py`:
  - Removed `/static/<path:filename>` route handler
  - Static files are now served directly by nginx, not Flask
  - Kept `/static/cache/<path:filename>` route for dynamically generated thumbnails

- `nginx-config.conf`:
  - Reordered location blocks to place `/v2p-formatter/static` before `/v2p-formatter`
  - Ensures nginx serves static files directly instead of proxying to Flask

- `templates/base.html`:
  - Changed `{{ url_for('v2p_formatter.serve_static', filename='css/style.css') }}` → `/v2p-formatter/static/css/style.css`
  - Changed all JS script references to direct paths

- `templates/observation_report.html`:
  - Updated CSS links: `observation-report.css`, `observation-report-media-browser.css`
  - Updated JS script references: `observation-report-media-browser.js`, `observation-report-live-preview.js`, `observation-report-standards.js`, `observation-report-preview-draft.js`, `observation-report-column-resizer.js`, `observation-report.js`

- `templates/observation_media.html`:
  - Updated JS script references: `live-preview.js`, `media-browser.js`, `standards.js`, `reshuffle.js`, `observation-media.js`

- `templates/ac_matrix.html`:
  - Updated CSS link: `ac-matrix.css`
  - Updated JS script references: `preview-renderer.js`, `ac-matrix.js`

- `templates/image_to_pdf.html`:
  - Updated CSS link: `media-bulk-image-selector.css`
  - Updated JS script reference: `media-bulk-image-selector.js`

#### Nginx Configuration
- Static file location block must come **before** the app location block
- Nginx serves static files directly from `/Users/rom/Documents/nvq/apps/v2p-formatter/static`
- Flask no longer handles static file requests (except cache files)

#### Server Management
- Server can be started directly: `source venv/bin/activate && python run.py`
- PM2 configuration may require full path to Python interpreter or use of `start.sh` script
- Server runs on port 5001, proxied by nginx on port 80

### 🎯 Benefits
- **Correct MIME Types**: Static files served with proper MIME types (CSS as `text/css`, JS as `application/javascript`)
- **Better Performance**: Static files served directly by nginx (no Flask overhead)
- **Reliable Access**: Fixes 502 Bad Gateway errors when accessing the app
- **No Routing Errors**: Templates no longer cause Flask BuildError exceptions
- **Consistent Behavior**: Matches the fix applied in observation-report-cursor app

### ⚠️ Action Required
After applying these changes:
1. Reload nginx configuration: `sudo nginx -s reload` or restart nginx
2. Restart the Flask server to apply route changes
3. Clear browser cache if issues persist
4. Verify static files load correctly in browser developer tools

## [2026-01-02] - Automatic PDF Generation

### Added
- **Automatic PDF Generation by Default**:
  - PDFs are now automatically generated after frame extraction completes
  - Works in both single video mode and bulk selection mode
  - No manual "Generate PDF" step required - PDFs are created immediately after frames are extracted
  - PDF generation uses current output settings (layout, images per page)

- **Enhanced PDF Results Display**:
  - Results display now matches the `image-to-pdf` page format
  - Shows "Output Filename" for each generated PDF
  - Displays "Output Folder" path with clickable "📁 Open Output Folder" link (opens in Finder)
  - Shows "File Path" as clickable link that opens the file's directory in Finder
  - Provides "📄 Open PDF" link that opens the PDF in Apple Preview
  - Supports bulk results display with numbered sections (PDF 1 of N, PDF 2 of N, etc.)

- **Bulk Mode PDF Generation**:
  - Each video in bulk selection mode automatically gets a PDF generated after its frames are extracted
  - PDF results are collected and displayed together after all videos are processed
  - Status updates show "✅ PDF Generated" for each video during batch processing
  - All PDF results are displayed in a unified results section with proper formatting

### Changed
- **Frame Extraction Workflow**:
  - Frame extraction now automatically triggers PDF generation
  - Removed need for separate "Generate PDF" button click after extraction
  - Results are displayed immediately after PDF generation completes
  - Progress indicators show both frame extraction and PDF generation status

- **Results Display Format**:
  - Updated results display to match `image-to-pdf` page styling and structure
  - File paths are now clickable and open Finder to the file location
  - PDF links use consistent "📄 Open PDF" text and open in Apple Preview
  - Output folder information is prominently displayed with Finder link

### Technical Details
- Added `generatePDFAuto()` function to automatically generate PDFs after frame extraction
- Added `showPDFResults()` function with support for single and bulk PDF results
- Modified `extractFrames()` handler to call `generatePDFAuto()` after successful extraction
- Updated `startBulkExtraction()` to generate PDFs for each video after frame extraction
- PDF results are stored in `window.appData.batchResults[i].pdfResult` for bulk mode
- Results display includes proper HTML escaping and error handling

## [2026-01-01] - Image to PDF Module Enhancements

### Added
- **Mandatory Filename Input**:
  - Added filename input field in "3. Generate Documents" section
  - Filename is required before generating documents
  - Field starts empty (no default value)
  - Frontend and backend validation ensures valid filename
  - Filename sanitization removes invalid characters
  - Input is disabled during document generation

- **Reset Selection Button**:
  - Added "Reset Selection" button in main image selection controls
  - Button styled with darker red theme (matching media selector)
  - Only visible when images are selected
  - Clears all selected images and sequence numbers
  - Re-renders image list and updates UI automatically

### Changed
- **Generate Documents Section**:
  - Section is now always visible (no longer hidden when no images selected)
  - Removed conditional display logic
  - Users can see and access the section at any time

- **Filename Default Value**:
  - Removed default "images_document" value from filename input
  - Input field now starts empty
  - Users must enter a custom filename

### Fixed
- **Scroll Position Reset**:
  - Fixed issue where selecting images at the bottom caused page to scroll to top
  - Scroll position is now preserved when image list is re-rendered
  - Uses `requestAnimationFrame` to restore scroll position after DOM update
  - Works for both vertical and horizontal scrolling

- **Image Sequence Order**:
  - Fixed output PDF/DOCX to properly follow sequence numbers (1, 2, 3, 4...)
  - Images are now sorted by sequence number before document generation
  - Sequence numbers displayed on thumbnails now match the order in output files
  - Ordering remains consistent even if images were selected in different order

- **Thumbnail Caching Performance**:
  - Fixed issue where all thumbnails were reloaded on every page render/interaction
  - Replaced timestamp-based cache-buster with file modification time in thumbnail URLs
  - Changed backend cache headers from `no-cache` to `public, max-age=31536000` (1 year)
  - Added ETag support for conditional requests (304 Not Modified responses)
  - Thumbnails now cached in browser and only reload when source files actually change
  - Significantly faster page loads and smoother interactions when selecting images
  - Reduced server load by eliminating unnecessary thumbnail regeneration

## [2026-01-01] - Media Selector Improvements

### Fixed
- **Folder Expansion in Media Selector**: 
  - Subfolders containing selected images now automatically expand when modal opens
  - Previously, all folders were collapsed by default even if they contained selected images
  - Fix ensures users can see their selected images immediately upon opening modal
  
- **Folder Toggle Functionality**:
  - Fixed issue where clicking folder headers in Media Selector modal had no effect
  - Switched from per-element event listeners to event delegation pattern for reliability
  - Removed duplicate code that was setting content.innerHTML twice
  - Added comprehensive error handling and console logging for debugging
  - Folders now correctly expand/collapse when clicking their headers

### Added
- **Reset Selection Button in Media Selector**:
  - Added "Reset Selection" button in modal header next to "Reset Order" button
  - Clears all selected images and removes sequence numbers
  - Button styled with darker red theme to differentiate from "Reset Order"
  - Updates selection counter and syncs with main view automatically
  - Provides quick way to clear all selections without closing modal

### Improved
- **Error Handling for Image Loading**:
  - Added response validation (checks `response.ok` before parsing JSON)
  - Better error messages displayed to users
  - More detailed console logging for debugging API issues
  - Handles HTTP errors and API error responses gracefully

## [2026-01-01] - Component Removal & Cleanup

### Removed
- **AC Matrix Component**: Completely removed all routes, functions, and navigation links
  - Removed `/ac-matrix` main route and all related API endpoints
  - Removed JSON file management endpoints (`/ac-matrix/json-files/*`)
  - Removed matrix analysis endpoints (`/ac-matrix/analyze`, `/ac-matrix/matrices/*`)
  - Removed navigation link from all templates
  
- **Observation Media Component**: Completely removed all routes, functions, and navigation links
  - Removed `/observation-media` standalone page route
  - Removed `/media-converter/observation-media/*` API routes
  - Removed draft management endpoints for observation media
  - Removed DOCX export functionality for observation media
  - Removed navigation link from all templates
  
- **Observation Report Component**: Completely removed all routes, functions, and navigation links
  - Removed `/observation-report` main route and all related API endpoints
  - Removed media scanning and serving endpoints (`/observation-report/media/*`)
  - Removed draft management endpoints (`/observation-report/drafts/*`)
  - Removed DOCX export and download endpoints
  - Removed file renaming functionality
  - Removed navigation link from all templates

### Changed
- **Navigation Menu**: Simplified to only show active modules
  - Removed AC Matrix, Observation Media, and Observation Report links
  - Navigation now displays only: Video to Image, Media Converter, Image to PDF
  
- **Code Cleanup**: Removed all commented-out code and orphaned functions
  - Cleaned up empty section markers
  - Removed unused function definitions without route decorators

## [2026-01-01] - Image to PDF Module Enhancements

### Added
- **Full-Screen Bulk Image Selector Modal**:
  - Apple Photos-style full-screen modal interface for bulk image selection
  - Opens via icon button (⛶) in bulk selection controls
  - Full viewport overlay with dark background (#0a0a0a)
  - Header bar with close button, selection counter, and reset order button
  - Footer bar with zoom controls (slider, +/- buttons) positioned at bottom
  - Smooth fade-in/out animations (300ms)
  
- **Dynamic Zoom Controls**:
  - 10 zoom levels (Level 1-10) controlling grid columns (2-8 columns per row)
  - Default zoom: Level 1 (8 columns per row)
  - Zoom slider and +/- buttons in footer bar
  - Zoom preference saved to localStorage
  - Smooth grid re-rendering on zoom change
  - Visual zoom level indicator showing current level and columns
  
- **Selection-Based Ordering**:
  - Click thumbnail or checkbox to select/deselect images
  - Auto-assign sequence numbers (1, 2, 3...) based on selection order
  - Sequence badges displayed on selected images (top-right corner)
  - Visual feedback: blue border (#667eea) and darker background for selected items
  - Real-time auto-save - selections sync immediately to `window.appData.selectedImages`
  - No "Done" button needed - selections persist when modal closes
  - Reset order button to restore default alphabetical order
  
- **Image Grid & Folder Structure**:
  - Images organized by folder structure (root + subfolders)
  - Folder headers with image counts
  - Subfolders collapsed by default
  - Clickable folder headers with expand/collapse icons (▶/▼)
  - Thumbnails with 100% quality (240x180px)
  - Image metadata displayed (filename, file size in MB)
  - Error handling for failed thumbnail loads
  
- **Image Sorting**:
  - Sort by Name (alphabetical) - default option
  - Sort by Date/Time (newest first)
  - Sort dropdown in main view bulk selection controls
  - Sort dropdown in modal header
  - Sort order syncs between main view and modal
  - Backend returns `modified_time` metadata for date sorting
  
- **Output File Management**:
  - Output files generated in learner folder: `/OUTPUT_FOLDER/qualification/learner/`
  - "Open Output Folder" link opens macOS Finder to the learner folder
  - PDF files open in Apple Preview instead of downloading
  - New backend endpoints:
    - `POST /open_folder` - Opens folder in macOS Finder
    - `POST /open_file` - Opens files in macOS Preview (PDFs) or default app

### Changed
- **Bulk Selection Mode**:
  - Removed "Bulk Selection Mode" toggle checkbox - bulk selection always enabled by default
  - Checkboxes always visible on images (no conditional rendering)
  - All bulk mode conditional checks removed from UI logic
  
- **Output Settings Section**:
  - Always visible by default (removed `display: none`)
  - No longer hidden when no images selected
  
- **Default Settings**:
  - Default sort order: Name (alphabetical) instead of Date/Time
  - Default output format: PDF Only instead of Both (PDF + DOCX)
  - Default zoom level: Level 1 (8 columns) instead of Level 5 (4 columns)
  
- **UI Elements**:
  - Fullscreen selector button changed to icon-only (⛶) - removed text label
  - Larger button size (40x40px minimum) with tooltip
  - Changed icon from 📺 (TV) to ⛶ (fullscreen icon)
  
- **Subfolder Display**:
  - All subfolders collapsed by default in both main view and modal
  - Click folder header to expand/collapse

### Technical
- **New Files**:
  - `static/css/media-bulk-image-selector.css` - Modal component styles
  - `static/js/media-bulk-image-selector.js` - Modal component logic (729 lines)
  
- **Backend Changes**:
  - `app/image_scanner.py`: Added `modified_time` and `modified_date` to image metadata
  - `app/routes.py`:
    - Added `POST /open_folder` endpoint using macOS `open` command
    - Added `POST /open_file` endpoint using macOS `open -a Preview` for PDFs
    - Modified `generate_image_documents` to save files in learner folder instead of first image's directory
    - Added `output_folder_path` to response for frontend display
  
- **Frontend Changes**:
  - `templates/image_to_pdf.html`: 
    - Integrated full-screen modal component
    - Added sort dropdown and fullscreen button
    - Updated selection logic to always use bulk mode
    - Added `openFolderInFinder()` and `openFileInPreview()` functions
    - Updated results display with folder link and Preview integration

## [1.8.0] - 2025-12-27

### Added
- **Bulk Video Selection Feature**:
  - Added bulk selection mode toggle allowing users to select multiple videos for batch processing
  - Checkbox-based selection UI with visual indicators for selected videos
  - "Select All" / "Deselect All" buttons for quick bulk selection
  - Selection counter badge showing number of selected videos
  - Batch mode indicators in "Time Selection" and "Output Settings" sections
  - Visual highlighting for selected videos in bulk mode

- **Bulk Frame Extraction**:
  - Sequential processing of multiple videos with same time points
  - Per-video progress tracking with status indicators (pending, processing, completed, error)
  - Overall batch progress bar showing extraction progress
  - Batch validation endpoint to check time points against all selected videos
  - Error handling per video - failed extractions don't block successful ones
  - Results summary showing successful and failed extractions

- **Bulk Document Generation**:
  - Generate PDF and/or DOCX documents for multiple videos in one operation
  - Sequential processing with progress tracking per video
  - Per-video status indicators for document generation
  - Support for "PDF only", "DOCX only", or "Both (PDF + DOCX)" output formats
  - Organized download links displayed per video after completion
  - Error handling ensures failed generations don't block successful ones
  - Results summary showing completed documents with download links

- **Auto-Generate Time Points for Bulk Mode**:
  - Auto-generate time points works in bulk mode using first selected video's duration
  - Automatically loads video info for first selected video when generating time points
  - Time points persist when switching between single and bulk modes
  - Time points persist when selecting/deselecting videos in bulk mode
  - Loading indicators during video info fetch
  - Error messages if video info cannot be loaded

- **Backend Batch Processing APIs**:
  - New endpoint: `POST /v2p-formatter/batch_video_info` - Get video info for multiple videos
  - New endpoint: `POST /v2p-formatter/validate_batch_time_points` - Validate time points against multiple videos
  - Batch validation includes warnings for time points exceeding video duration
  - Efficient batch processing with per-video error handling

### Changed
- **Time Point Selection in Bulk Mode**:
  - Same time points applied to all selected videos in batch
  - Time points validated against all videos before processing
  - Warnings shown if any time point exceeds any video's duration

- **Output Settings in Bulk Mode**:
  - Settings (resolution, layout, images per page) applied to all videos in batch
  - Batch indicator shown in settings sections when bulk mode is active

- **Video List Display**:
  - Added checkbox column when bulk mode is enabled
  - Visual indicators (checkmarks) for selected videos
  - Click handler updated to toggle selection in bulk mode instead of loading video

### Fixed
- **Thumbnail Generation (500 Errors)**:
  - Fixed 500 errors when generating thumbnails for very short videos
  - Added duration probing using `ffprobe` before thumbnail extraction
  - Adjusted time points for thumbnail extraction to never exceed video duration
  - For very short videos (`duration < 0.1s`), uses time `0` for thumbnail
  - For longer videos, uses 50% of duration or 0.05s (whichever is smaller) if requested time exceeds duration
  - Improved FFmpeg command to use input seeking for faster processing on longer videos
  - Enhanced error messages and logging for FFmpeg failures

- **Time Point Persistence**:
  - Fixed time points being cleared when entering bulk mode
  - Fixed time points being cleared when selecting videos in bulk mode
  - Fixed time points being cleared when loading video info
  - Time points now persist correctly across mode switches and video selections

- **Auto-Generate Time Points Race Condition**:
  - Fixed race condition where auto-generate would fail if video info wasn't loaded yet
  - Added async video info loading before generating time points
  - Added proper state checks and error handling

- **JavaScript Scope and Function Definition Issues**:
  - Fixed `processBulkDocumentGeneration is not defined` error
  - Fixed `batchIndicator is not defined` error
  - Fixed duplicate function definitions causing conflicts
  - Corrected IIFE structure and function scope placement
  - All bulk processing functions now properly accessible

- **Page Loading Issues**:
  - Fixed infinite loading caused by JavaScript syntax errors
  - Fixed brace mismatches and unclosed structures
  - Corrected function definitions and scope issues

### Technical Details

#### Backend Changes
- **`app/routes.py`**:
  - Added `POST /v2p-formatter/batch_video_info` endpoint:
    - Accepts array of video paths
    - Returns video info (duration, width, height, fps) for each video
    - Validates paths against OUTPUT_FOLDER
    - Per-video error handling
  - Added `POST /v2p-formatter/validate_batch_time_points` endpoint:
    - Validates time points against multiple videos
    - Returns warnings for time points exceeding video duration
    - Per-video validation with detailed results
  - Enhanced `get_video_thumbnail` endpoint:
    - Added robust path handling using `Path(file_path).resolve()`
    - Enhanced error logging with full stack traces
    - Removed dead code causing issues

- **`app/thumbnail_generator.py`**:
  - Added video duration probing using `ffprobe`
  - Adjusted `time_seconds` calculation to never exceed video duration
    - For very short videos (`duration < 0.1s`): uses time `0`
    - For longer videos: uses `max(0, min(0.05, duration * 0.5))` if requested time exceeds duration
  - Optimized FFmpeg command:
    - Input seeking (`-ss` before `-i`) for faster processing on longer videos
    - Output seeking (`-ss` after `-i`) for very short videos for accurate frame selection
  - Improved error messages and debug logging

#### Frontend Changes
- **`templates/index.html`**:
  - Added bulk selection controls:
    - Mode toggle button
    - Select All / Deselect All buttons
    - Selection counter badge
  - Modified `renderVideoList()`:
    - Added checkbox column for bulk mode
    - Added visual indicators for selected videos
    - Updated click handlers for bulk mode
  - Added bulk processing functions:
    - `toggleBulkMode()`: Enable/disable bulk selection mode
    - `toggleVideoSelection()`: Toggle individual video selection
    - `selectSingleVideo()`: Select single video (preserves time points)
    - `updateSelectionUI()`: Update UI when videos are selected (preserves time points)
    - `toggleSelectAll()`: Select/deselect all videos
    - `validateBulkTimePoints()`: Validate time points for batch
    - `processBulkExtraction()`: Sequential frame extraction for batch
    - `processBulkDocumentGeneration()`: Sequential document generation for batch
    - `startBulkDocumentGeneration()`: Main batch document generation orchestrator
    - `showBulkExtractionResults()`: Display extraction results summary
    - `showBulkDocumentGenerationResults()`: Display document generation results
  - Enhanced `generateAutoTimePoints()`:
    - Works in bulk mode using first selected video's duration
    - Loads video info asynchronously if missing
    - Preserves existing time points
    - Proper error handling and loading indicators
  - Added batch progress UI:
    - Overall batch progress bar
    - Per-video status list with icons
    - Organized results display with download links
  - Fixed time point persistence:
    - Time points preserved when entering bulk mode
    - Time points preserved when selecting videos
    - Time points preserved when loading video info
  - Initialized bulk mode state variables:
    - `window.appData.selectedVideos = []`
    - `window.appData.bulkMode = false`
    - `window.appData.batchResults = {}`
    - `window.appData.availableFiles = []`

- **Output Format Selection**:
  - Added "Both (PDF + DOCX)" option to format selector
  - Dynamic progress calculation based on selected format
  - Sequential generation of PDF and/or DOCX based on selection

#### Testing
- Created `tests/test_bulk_video_backend.py`: Comprehensive backend tests for batch endpoints
  - Tests `batch_video_info` endpoint with various scenarios
  - Tests `validate_batch_time_points` endpoint
  - Tests error handling and batch size limits
  - Tests per-video validation and warnings

#### Documentation
- Created `docs/bulk-video-selection-spec.md`: Complete specification for bulk video selection feature
- Created `docs/bulk-video-selection-development-plan.md`: Staged development plan (6 stages)
- Created `docs/bulk-video-selection-backend-review.md`: Backend endpoint review and reuse strategy
- Created `docs/bulk-video-selection-backend-complete.md`: Backend implementation summary
- Created `docs/bulk-auto-generate-time-points-spec.md`: Specification for auto-generate time points in bulk mode
- Created `docs/bulk-document-generation-spec.md`: Specification for bulk document generation

### Test Results
- ✅ **Bulk selection UI working**: Mode toggle, checkboxes, selection counter all functional
- ✅ **Bulk frame extraction working**: Sequential processing with progress tracking
- ✅ **Bulk document generation working**: Sequential PDF/DOCX generation with progress
- ✅ **Time point persistence fixed**: Time points persist across mode switches and selections
- ✅ **Auto-generate time points fixed**: Works correctly in bulk mode with proper state handling
- ✅ **Thumbnail generation fixed**: No more 500 errors for short videos
- ✅ **JavaScript errors fixed**: All scope and definition issues resolved
- ✅ **Page loading fixed**: No more infinite loading issues

---

## [1.7.0] - 2025-12-09

### Added
- **AC Matrix - Unit Selector Feature**:
  - Added ability to filter which units from JSON standards file are included in analysis
  - Unit selector appears below JSON file selector when a standards file is selected
  - Filter toggle checkbox: "Filter Units (Optional)" - when enabled, only selected units are analyzed
  - Select All / Deselect All buttons for quick unit selection management
  - Selection counter displays "Selected: X of Y units"
  - Unit checkboxes show format: "Unit {unit_id}: {unit_name}"
  - Scrollable unit list (max 300px height) for files with many units
  - All units selected by default when filter is enabled
  - Responsive design for mobile/tablet devices

- **AC Matrix - Unit Loading Endpoint**:
  - New endpoint: `GET /ac-matrix/json-files/<file_id>/units`
  - Returns list of units from selected JSON standards file
  - Enables frontend to display available units for filtering

### Changed
- **AC Matrix - Unit Filtering in Analysis**:
  - Analysis endpoint now accepts optional `selected_unit_ids` parameter
  - When provided, only selected units are included in matrix analysis
  - When filter is disabled, all units are analyzed (default behavior)
  - Backend filters units before generating matrix

- **AC Matrix - Unit Coverage Calculation**:
  - Fixed unit coverage counting to only count ACs from explicitly mapped units
  - Units now show correct coverage based on unit-AC mappings from draft text
  - Prevents unrelated units from showing partial coverage

### Fixed
- **AC Matrix - AC Extraction from Bracketed Mappings**:
  - Fixed issue where ACs inside brackets like `(129v4: 1.1, 1.2; 130v3: 1.1, 1.2)` were being counted as covered
  - AC extraction now strips bracketed unit:AC mappings before extracting ACs
  - Bracketed mappings are used for unit mapping but not for AC coverage detection
  - Handles both parentheses `()` and square brackets `[]`
  - Improved bracket matching to handle semicolon-separated mappings

- **AC Matrix - Coverage from Unit Mappings**:
  - Fixed issue where no ACs showed as covered when all ACs were only in brackets
  - System now creates coverage entries from unit-AC mappings when ACs aren't found in observation text
  - Units 129, 130, 643 now correctly show as covered based on bracket mappings
  - Units 641, 642 no longer incorrectly show partial coverage

### Technical Details

#### Backend Changes
- **`app/routes.py`**:
  - Added `GET /ac-matrix/json-files/<file_id>/units` endpoint
  - Updated `analyze_observation_report()` to accept `selected_unit_ids` parameter
  - Added unit filtering logic before matrix generation
  - Improved unit ID matching to handle variations (e.g., "129v4" matches "129v4" or "129")

- **`app/ac_matrix_analyzer.py`**:
  - Enhanced `strip_bracketed_unit_mappings()`: Improved bracket matching with balanced bracket detection
  - Updated `extract_ac_references_with_context()`: Strips brackets before extracting ACs
  - Updated `generate_matrix_bulk()`: Creates coverage from unit mappings when ACs not found in text
  - Improved unit ID matching logic for better accuracy
  - Fixed unit coverage counting to use actual mapped units only

#### Frontend Changes
- **`templates/ac_matrix.html`**:
  - Added unit selector container with filter toggle
  - Added unit checkbox list container
  - Added Select All / Deselect All buttons
  - Added selection counter display

- **`static/js/ac-matrix.js`**:
  - Added `setupUnitSelector()`: Initializes unit selector event listeners
  - Added `loadUnitsForJsonFile()`: Loads units when JSON file is selected
  - Added `renderUnitCheckboxes()`: Renders unit checkboxes with proper state
  - Added `handleFilterToggle()`: Manages filter enable/disable
  - Added `updateUnitSelection()`: Updates selected units array
  - Added `selectAllUnits()` / `deselectAllUnits()`: Quick selection controls
  - Added `updateSelectionCounter()`: Shows selection count
  - Updated `analyzeReport()`: Sends selected unit IDs to backend
  - Updated JSON file selector change handler to load units

- **`static/css/ac-matrix.css`**:
  - Added unit selector container styles
  - Added unit checkbox item styles with hover effects
  - Added selection counter styles
  - Added responsive styles for mobile/tablet
  - Dark theme consistent with existing UI

#### Testing
- Verified unit loading endpoint returns correct units
- Tested unit filtering in analysis
- Verified bracket stripping prevents false AC coverage
- Confirmed unit mappings create correct coverage entries

### Test Results
- ✅ **Unit selector displays correctly**: Units load when JSON file is selected
- ✅ **Filter toggle works**: Enables/disables unit selection
- ✅ **Unit filtering works**: Only selected units included in analysis
- ✅ **Bracket stripping works**: ACs in brackets not counted as covered
- ✅ **Unit mappings work**: Coverage created from bracket mappings
- ✅ **Coverage accuracy**: Only explicitly mapped units show coverage

---

## [1.6.0] - 2025-12-09

### Changed
- **Video to Image - File Source Location**:
  - Changed file scanning to use OUTPUT_FOLDER instead of INPUT_FOLDER
  - All endpoints (`/list_files`, `/qualifications`, `/learners`) now scan from output directory
  - File validation updated to check against OUTPUT_FOLDER
  - Updated file selector message to indicate "output folder" instead of "input folder"

- **Video to Image - File Listing Behavior**:
  - Updated `/list_files` endpoint to return all MP4 files in relevant subfolders
  - When both qualification and learner are selected: returns all MP4 files from that learner's folder and all subfolders recursively
  - Files are now properly filtered and organized by folder structure
  - Frontend updated to pass qualification and learner parameters to API

- **Output File Location**:
  - Changed generated files (images and PDFs) to be saved in the same directory as the source video file
  - Images saved to: `{video_directory}/{video_name}_frames/`
  - PDF saved to: `{video_directory}/{video_name}.pdf`
  - DOCX saved to: `{video_directory}/{video_name}.docx`
  - Updated frontend message to reflect new location behavior

- **Media Browser - File Display Order**:
  - Files in main category (directly in folder) now displayed first, before subfolder files
  - Main category files are always visible (not in collapsible sections)
  - Subfolder files displayed after main category files in collapsible sections

### Fixed
- **Media Browser - Loading State**:
  - Fixed "Loading files... forever" issue by adding proper error handling
  - Added fetch timeout (30 seconds) to prevent infinite loading
  - Fixed race condition in URL parameter initialization - now waits for learner dropdown to populate before setting learner value
  - Improved error messages to show actual error instead of staying in loading state
  - Added handling for `data.success === false` and malformed responses

- **Video to Image - File Loading**:
  - Fixed frontend not passing qualification and learner parameters to `/list_files` API
  - Updated `loadFileTree()` and `loadFiles()` functions to read parameters from dropdowns or URL
  - Fixed initialization timing to wait for dropdowns to be populated from URL parameters
  - Files now properly load when accessing page with URL parameters (e.g., `?qualification=Inter&learner=lakhmaniuk`)

### Technical Details

#### Backend Changes
- **`app/routes.py`**:
  - Updated `index()` route to use `OUTPUT_FOLDER` for listing qualifications and learners
  - Updated `/qualifications` endpoint to list from `OUTPUT_FOLDER`
  - Updated `/learners` endpoint to list from `OUTPUT_FOLDER`
  - Updated `/list_files` endpoint to scan from `OUTPUT_FOLDER` and filter by qualification/learner
  - Updated `/select_file`, `/video_file`, and `/thumbnail` endpoints to validate against `OUTPUT_FOLDER`
  - Improved `/list_files` to recursively scan all subfolders when qualification and learner are selected

- **`app/utils.py`**:
  - Updated `get_video_output_folder()`: Now creates `{video_name}_frames` folder in same directory as video
  - Updated `create_output_folder()`: Returns frames folder directly (no nested subfolder)
  - Updated `get_pdf_output_path()`: Saves PDF in same directory as video file
  - Updated `get_docx_output_path()`: Saves DOCX in same directory as video file

#### Frontend Changes
- **`static/js/file-selector.js`**:
  - Updated `loadFileTree()` to read qualification and learner from dropdowns or URL parameters
  - Added parameter passing to `/list_files` API endpoint
  - Updated loading message to say "output folder" instead of "input folder"

- **`templates/index.html`**:
  - Updated `loadFiles()` function to read qualification and learner from dropdowns or URL parameters
  - Fixed initialization timing to wait for dropdowns to be populated before loading files
  - Updated output location message to indicate files save in same directory as video

- **`static/js/observation-media.js`**:
  - Fixed error handling in fetch response - now handles `data.success === false` and malformed responses
  - Added fetch timeout wrapper to prevent infinite loading
  - Improved error messages with proper HTML escaping

- **`templates/observation_media.html`**:
  - Fixed race condition in URL parameter initialization
  - Added polling mechanism to wait for learner dropdown to populate before setting learner value
  - Added fetch timeout (30 seconds) to prevent infinite loading
  - Improved error handling with better error messages
  - Updated `displayObservationMedia()` to show main category files first

#### Testing
- Created `test_media_browser_debug.py`: Browser test with screenshots to debug media browser loading issues
- Verified API endpoints return correct data with proper parameters
- Confirmed files are saved in correct locations

### Test Results
- ✅ **Media browser loads correctly**: Files display when qualification and learner are selected
- ✅ **Error handling working**: Proper error messages shown instead of infinite loading
- ✅ **File listing working**: All MP4 files returned from relevant subfolders
- ✅ **Output location correct**: Files saved in same directory as source video
- ✅ **URL parameters working**: Page loads correctly with qualification and learner in URL

---

## [1.5.0] - 2025-12-09

### Added
- **AC Matrix Live Preview - 1:1 Match with Observation Media**:
  - Live Preview now matches Observation Media page exactly (no textarea needed)
  - Color-coded collapsible sections with media count badges
  - Media thumbnails displayed in 2-column tables within sections
  - Actual media count displayed per section (e.g., "5 media", "0 media")
  - Expand/collapse all sections functionality
  - Section state persistence using localStorage

- **Shared Preview Renderer Library**:
  - Created `static/js/preview-renderer.js` - reusable preview rendering library
  - Centralized functions for parsing sections, rendering content with media, counting media
  - Used across AC Matrix and Observation Media modules for consistency
  - Functions: `parseSections()`, `renderSections()`, `renderContentWithMedia()`, `countMediaInSection()`
  - Section state management with localStorage support

- **Standards AC Tooltips**:
  - Hover tooltips on Standards ACs (e.g., "1.1", "1.2", "1.3") showing full AC description
  - Tooltip width: 700px (or 90vw on smaller screens) - wide enough to show all text without scrolling
  - Dynamic positioning: tooltips adjust position to stay fully visible within viewport
  - Fixed positioning prevents clipping by parent containers
  - Smooth opacity transitions on hover
  - Tooltips positioned above AC by default, below if insufficient space above

- **Missing ACs Export Field**:
  - New "ACs Missing" section at bottom of AC Matrix page
  - Text field displays missing ACs in format: `draft name: unit:ac;unit:ac`
  - Copy to clipboard button for easy export
  - Auto-updates when matrix is analyzed
  - Supports both single and bulk report modes
  - Format example: `lakh-obs2: 641:1.3;641:2.1;641:3.3;642:2.1`

### Changed
- **AC Matrix Page Layout**:
  - Removed textarea for observation reports (replaced with Live Preview)
  - Live Preview now shows sections with media exactly like Observation Media page
  - Bulk reports mode sections now use event delegation for click handling
  - Unique section IDs per bulk report to prevent conflicts

- **Section Rendering**:
  - Sections in bulk reports use unique IDs (e.g., `bulk-0-section-0`, `bulk-1-section-0`)
  - Event delegation used for section clicks in bulk reports (no inline onclick handlers)
  - Single mode continues to use inline onclick handlers for compatibility

### Fixed
- **JavaScript Syntax Errors**:
  - Fixed duplicate declaration errors (`SECTION_COLORS`, `parseSections`, `renderSections`, `escapeHtml`)
  - Removed duplicate function declarations, now using shared library functions
  - All modules correctly reference `PreviewRenderer` global object

- **Section Click Functionality**:
  - Fixed sections not expanding/collapsing when clicked in bulk reports mode
  - Sections now properly toggle expand/collapse state
  - Each bulk report's sections work independently

- **Tooltip Visibility**:
  - Fixed tooltips being cut off or not visible
  - Changed to `position: fixed` for viewport-relative positioning
  - Added dynamic positioning logic to keep tooltips within viewport bounds
  - Parent containers set to `overflow: visible` to prevent clipping
  - Tooltips adjust horizontally and vertically to stay fully visible

- **Tooltip Width**:
  - Increased tooltip max-width from 350px to 700px
  - Removed scrolling requirement - all AC text visible without scrolling
  - Tooltips expand naturally to fit content up to max-width

### Technical Details

#### Frontend Changes
- **`templates/ac_matrix.html`**:
  - Removed `<textarea id="observation-report">` element
  - Added Live Preview section matching `observation_media.html` layout
  - Added "ACs Missing" section with textarea and copy button
  - Added script tag for `preview-renderer.js` library

- **`static/js/preview-renderer.js` (NEW FILE)**:
  - Shared library for preview rendering across modules
  - Exports: `SECTION_COLORS`, `parseSections()`, `renderSections()`, `renderContentWithMedia()`, `countMediaInSection()`, `escapeHtml()`, `generateReadOnlyMediaTable()`
  - Section state management with localStorage
  - Toggle section expand/collapse functionality

- **`static/js/ac-matrix.js`**:
  - Removed duplicate function declarations
  - Updated to use `PreviewRenderer` shared library functions
  - Added `generateMissingACsText()` function for missing ACs export
  - Added tooltip positioning logic with viewport boundary checks
  - Updated `renderSections()` wrapper to support inline handlers flag
  - Added event delegation for bulk report section clicks
  - Added copy button handler for missing ACs field

- **`static/css/ac-matrix.css`**:
  - Added tooltip styles with fixed positioning
  - Increased tooltip width to 700px
  - Added `overflow: visible` to parent containers
  - Added styles for missing ACs section
  - Enhanced tooltip arrow styling

- **`app/routes.py`**:
  - Updated `ac_matrix` route to include `assignments` and `selected_subfolder` in draft data
  - Passes media assignment data to template for Live Preview

#### Testing
- Added browser tests for tooltip visibility and positioning
- Added tests for section click functionality in single and bulk modes
- Verified missing ACs field format and copy functionality
- All tests passing with screenshots for verification

### Test Results
- ✅ **Tooltips fully visible**: All tooltips stay within viewport bounds
- ✅ **Section clicks working**: Sections expand/collapse correctly in both modes
- ✅ **Missing ACs format correct**: Format matches `draft name: unit:ac;unit:ac`
- ✅ **No JavaScript errors**: All duplicate declaration errors resolved
- ✅ **Live Preview 1:1 match**: Matches Observation Media page exactly

---

## [1.4.0] - 2025-01-XX

### Added
- **Preview Draft Modal - Three-Column Layout with Section Navigation and Actions**:
  - Split Document Preview into three resizable columns
  - Left column: Section navigation sidebar (200-400px resizable width)
  - Middle column: Preview content area (flexible width)
  - Right column: Settings/Actions panel (250-400px resizable width, always visible)
  - Two resizable dividers between columns with visual feedback
  - Section navigation automatically built from document sections
  - Color-coded section navigation items matching section titles
  - Click-to-scroll functionality - clicking a section navigates to it in the preview
  - Smooth scrolling with brief highlight animation when navigating to sections
  - Navigation updates automatically after undo/redo operations
  - Settings panel always visible - no need to click settings button to access controls

- **Trim Empty Paragraphs Feature**:
  - New checkbox option: "Trim empty paragraphs" in Hide Elements section
  - When enabled, automatically reduces 2+ consecutive empty paragraphs to just 1
  - Works with all hide element options (section titles, AC covered, etc.)
  - Detects paragraphs that become empty after elements are hidden
  - Iterative trimming process ensures all consecutive empty paragraphs are reduced
  - Uses `innerText` for reliable visibility detection (excludes hidden elements)
  - Handles edge cases where removal creates new empty sequences

- **Hide Elements - Bulk Select/Apply**:
  - Added "Select All" and "Deselect All" buttons for Hide Elements options
  - Removed toggle functionality - section is always visible
  - Quick way to show/hide all elements at once

- **Hide Empty Media Fields Option**:
  - New checkbox option: "Empty media fields" in Hide Elements section
  - When checked, empty placeholder tables are hidden in preview
  - Empty tables are excluded from DOCX export when option is enabled
  - Original text preserved when updating draft (empty tables remain in source)

- **Font Settings in DOCX Export**:
  - Font size and font type settings from preview are now applied to exported DOCX files
  - Font settings read from preview controls and passed to backend
  - Default: 16pt Times New Roman (if not specified)
  - All text in exported DOCX uses the selected font settings

### Changed
- **Document Preview Layout**:
  - Changed from two-column to three-column layout
  - Settings moved from dropdown menu to dedicated right column
  - Settings are now always visible and accessible (no toggle needed)
  - Removed "Settings" button from header - settings are permanently visible
  - Font Settings and Hide Elements are nested in the Actions column

- **Text Editor Placement**:
  - Moved Text Editor to independent field at bottom of page (above "Update Draft" button)
  - Text Editor and Live Preview are now completely independent sections
  - Live Preview section is full height when Text Editor is collapsed

- **Hide Elements Behavior**:
  - Hide Elements settings now only affect preview display and export
  - When updating draft, hidden elements are preserved in original text
  - Hidden elements are excluded from DOCX export when options are checked
  - Original text structure is maintained regardless of hide settings

### Fixed
- **debugOutput Function Errors**:
  - Fixed "debugOutput is not a function" errors in `file-selector.js` and `main.js`
  - Changed all `debugOutput()` calls to use `window.debugOutput()` with proper function checks
  - Updated checks from `typeof debugOutput !== 'undefined'` to `typeof window.debugOutput === 'function'`
  - Added debugger statement in `showSection()` function for debugging
  - All debug output calls now properly check if function exists before calling

- **Video Info State Synchronization**:
  - Fixed "Video info not available" error when video was already loaded
  - Synchronized `appState.videoInfo` and `window.appData.videoInfo` when video loads
  - Updated `file-selector.js` and `video-handler.js` to sync both state objects
  - Made `generateAutoTimePoints()` check both state locations for video info
  - Prevents errors when video info exists in one location but not the other

- **Text Formatting in Draft Updates**:
  - Fixed issue where updating draft from preview lost all line breaks
  - Text now preserves proper formatting with line breaks between paragraphs
  - Section titles, AC covered lines, and paragraphs maintain proper spacing
  - Placeholders remain on their own lines

- **AC Covered Line Formatting**:
  - Fixed extra blank line between paragraphs and AC covered lines in DOCX export
  - AC covered lines now appear directly after paragraphs with no blank line
  - Fixed AC covered label and values breaking across two lines
  - Label and values now stay together on single line when updating draft

- **Preview Draft Button**:
  - Fixed "Preview Draft" button not working (was throwing ReferenceError)
  - Fixed placeholder name not being defined for empty tables

- **Paragraph Number Hiding**:
  - Fixed paragraph numbers not hiding correctly when on their own line
  - Improved regex pattern to handle numbers followed by empty lines
  - Paragraph numbers now correctly detected and hidden/shown

- **Media Table Image Visibility**:
  - Fixed images not showing in media tables in preview
  - Added CSS rules to force image visibility in preview content

- **Draft Loading**:
  - Removed popup alert when loading a draft
  - Draft name now displayed silently in "Current Draft" UI element

### Technical Details

#### Frontend Changes
- **`templates/observation_media.html`**:
  - Restructured preview modal to three-column layout with two resizable dividers
  - Added Settings/Actions column on the right (always visible)
  - Moved Font Settings and Hide Elements from dropdown to Actions column
  - Removed Settings button from header
  - Added section navigation sidebar with color-coded items
  - Added "Hide empty media fields" and "Trim empty paragraphs" checkboxes to Hide Elements section
  - Added bulk select/deselect buttons for Hide Elements
  - Updated Text Editor placement and styling

- **`static/js/observation-media.js`**:
  - `extractTextFromPreview()`: Added `preserveHiddenElements` parameter
    - When `true` (Update Draft): Preserves all elements in original text
    - When `false` (Export): Removes hidden elements and empty tables
  - `generateDocxPreview()`: Added section IDs and color-coded borders
  - `buildPreviewSectionNavigation()`: Builds section navigation from preview content
  - `scrollToPreviewSection()`: Smooth scroll to section with highlight
  - `startResizePreview()`, `handleResizePreview()`, `stopResizePreview()`: Left column resizing
  - `startResizePreview2()`, `handleResizePreview2()`, `stopResizePreview2()`: Right column resizing
  - `exportObservationDocxFromPreview()`: Extracts text with hidden elements excluded
  - `selectAllHideElements()`, `deselectAllHideElements()`: Bulk operations
  - `updatePreviewDisplay()`: 
    - Added empty table hiding logic
    - Added trim empty paragraphs logic with iterative trimming
    - Uses `innerText` for reliable empty paragraph detection
    - Handles paragraphs that become empty after elements are hidden
  - Removed `togglePreviewSettings()` function (settings now always visible)
  - Improved text extraction to preserve line breaks and formatting
  - Fixed AC covered line extraction to keep label and values together
  - Added cleanup regex to remove blank lines before AC covered lines

- **`static/js/file-selector.js`**:
  - Fixed all `debugOutput()` calls to use `window.debugOutput()` with proper function checks
  - Added state synchronization: updates both `appState.videoInfo` and `window.appData.videoInfo` when video loads
  - Prevents "debugOutput is not a function" errors

- **`static/js/main.js`**:
  - Fixed all `debugOutput()` calls to use `window.debugOutput()` with proper function checks
  - Added debugger statement in `showSection()` function for debugging
  - All debug output calls now properly check if function exists before calling

- **`static/js/video-handler.js`**:
  - Added state synchronization: updates both `appState.videoInfo` and `window.appData.videoInfo` when video loads
  - Prevents "Video info not available" errors

- **`templates/index.html`**:
  - `generateAutoTimePoints()`: Now checks both `window.appData.videoInfo` and `appState.videoInfo` for video info
  - More robust video info detection prevents errors when video is loaded

#### Backend Changes
- **`app/routes.py`**:
  - `export_observation_docx()`: Added `font_size` and `font_name` parameters
  - Default values: `font_size=16`, `font_name='Times New Roman'`

- **`app/observation_docx_generator.py`**:
  - `create_observation_docx()`: Added `font_size` and `font_name` parameters
  - Sets document Normal style font to specified font name and size
  - Applies font settings to all text runs in paragraphs
  - Default font: 16pt Times New Roman

#### CSS Improvements
- Added resizer hover effects (color change on hover) for both dividers
- Section navigation item styling with hover effects
- Color-coded section title borders matching navigation

#### Testing
- Added `test_trim_empty_paragraphs.py`: Automated browser test for trim empty paragraphs functionality
  - Verifies that consecutive empty paragraphs are reduced to 1
  - Tests with section titles hidden and trim enabled
  - Takes screenshots at each step for verification
  - Confirms max consecutive empty paragraphs is ≤ 1

---

## [1.3.1] - 2025-01-XX

### Changed
- **Observation Media Page Layout Improvements**:
  - Made Live Preview and Text Editor sections fully independent with separate scrolling
  - Both sections now share space equally (50/50 split) and scroll independently
  - Fixed Live Preview scrolling to ensure all sections are visible and accessible
  - Added visible scrollbar styling for the Live Preview section (14px width, custom colors)
  - Improved flex layout so sections don't affect each other's sizing or scrolling

### Added
- **Text Editor Collapse/Expand Functionality**:
  - Text Editor section is now collapsible and collapsed by default to save screen space
  - Click on "Text Editor" header to expand/collapse the textarea
  - Smooth CSS transitions for collapse/expand animations
  - Icon indicator (▶/▼) shows collapse/expand state with rotation animation
  - When expanded, textarea properly fills available space with minimum height of 300px
  - Header remains visible when collapsed, showing placeholder/word statistics

### Fixed
- Fixed Live Preview sections being cut off - all sections now scroll properly within viewport
- Fixed scrollbar not being visible in Live Preview - added custom webkit and Firefox scrollbar styling
- Fixed textarea appearing too small (0.5 line) when editor section is expanded
- Improved CSS flex properties to ensure proper space allocation between preview and editor sections
- Fixed editor section content wrapper to properly expand when section is opened

### Technical Details

#### Frontend Changes
- **`templates/observation_media.html`**:
  - Added `.editor-section.collapsed` class for collapse/expand functionality
  - Added `.editor-section-content-wrapper` for proper content area management
  - Enhanced `.preview-section-content` with custom scrollbar styling
  - Updated flex properties for both sections to ensure independence
  - Added `toggleEditorSection()` JavaScript function for collapse/expand

- **CSS Improvements**:
  - Custom scrollbar styling: 14px width, dark theme colors (#666 thumb, #1e1e1e track)
  - Proper min-height constraints for expanded editor section (300px)
  - Smooth transitions for collapse/expand animations (0.3s ease)
  - Flex: 1 1 0 for equal space sharing between preview and editor

---

## [1.3.0] - 2025-01-XX

### Fixed
- **DOCX Media Table Formatting**: Fixed critical issues with media table layout in exported DOCX files
  - Fixed table width calculation from `Length` objects to twips conversion
  - Corrected conversion: Length → inches → twips (1 inch = 1440 twips)
  - Added sanity checks to prevent invalid width values
  - Set table layout to `fixed` to properly respect width settings
  - Ensured tables span full available page width (minus margins)
  - Default table width: 9000 twips (~6.25 inches for A4 with margins)

- **Column Width Configuration**: Fixed 2-column layout in DOCX media tables
  - Set equal column widths (50% each of available width)
  - Columns properly configured via `table.columns[0].width` and `table.columns[1].width`
  - Removed redundant cell width settings that caused conflicts
  - Columns now properly visible and correctly sized

- **Image Embedding in DOCX**: Fixed images not appearing in exported DOCX tables
  - Fixed placeholder name extraction to properly strip braces (was including `{{` and `}}`)
  - Improved path resolution to handle multiple path formats:
    - Absolute file paths (from observation media scanner)
    - Static URL paths (from frontend)
    - Relative paths with automatic resolution
    - Fallback search in OUTPUT_FOLDER when path not found
  - Images now successfully embedded in table cells with proper sizing
  - Maintains aspect ratio and fits within cell boundaries
  - Added comprehensive error handling with placeholder text for missing images

- **Placeholder Matching**: Fixed placeholder extraction in DOCX generation
  - Corrected regex pattern handling to properly extract placeholder names
  - Fixed case-insensitive matching between placeholders and assignments
  - Placeholders like `{{Image1}}` now correctly match assignment keys like `'image1'`

### Enhanced
- **Path Resolution**: Improved image path resolution in DOCX generation
  - Multiple resolution strategies: absolute paths, static URLs, OUTPUT_FOLDER search
  - Recursive filename search when direct path not found
  - Better error messages with path debugging information
  - Graceful fallback to placeholder text when images cannot be found

- **Error Handling**: Enhanced error handling and logging in DOCX generation
  - Added comprehensive logging for image processing
  - Better error messages for debugging path resolution issues
  - Placeholder text added to cells when images cannot be loaded
  - Detailed logging at each step of image processing pipeline

### Technical Details

#### Backend Changes
- **`app/observation_docx_generator.py`**:
  - `_set_table_width()`: Fixed width conversion with proper Length object handling
  - `_add_media_table_to_doc()`: Improved width calculation and column width setting
  - Enhanced image path resolution with multiple fallback strategies
  - Fixed placeholder name extraction using `.strip('{}')` method
  - Added comprehensive logging throughout image processing

- **Image Processing**:
  - Images properly sized to fit within cell boundaries
  - Maintains aspect ratio while respecting max width/height constraints
  - Supports images from various sources and path formats
  - Error handling with informative placeholder text

#### Testing
- Added `test_docx_direct.py`: Direct DOCX generation test script
- Added `test_docx_images.py`: Test script for image embedding verification
- Created `test_docx_with_browser.py`: Browser-based export testing
- All tests verify table structure, column widths, and image embedding

### Test Results
- ✅ **Tables created with correct width**: 9000 twips (~6.25 inches)
- ✅ **Equal column widths**: 4154 twips each (50% of available width)
- ✅ **Images successfully embedded**: All assigned images appear in DOCX tables
- ✅ **Path resolution working**: Handles absolute paths, static URLs, and OUTPUT_FOLDER searches
- ✅ **File size verification**: DOCX files properly sized with embedded images (~400KB with images)

---

## [1.2.0] - 2025-12-06

### Added
- **Browser Testing Environment**: Complete automated browser testing setup using Playwright
  - Created comprehensive test suite for Observation Media module (`tests/test_observation_media_drag_drop.py`)
  - Added test fixtures and configuration (`tests/conftest.py`)
  - Created test runner script (`tests/test_runner.py`)
  - Added setup script for browser testing (`setup_browser_tests.sh`)
  - Created test verification suite (`tests/test_setup_verification.py`)
  - Added reshuffle functionality tests (`tests/test_reshuffle_functionality.py`)
  - Added reshuffle unit tests (`tests/test_observation_media_reshuffle.py`)
  - Comprehensive documentation (`tests/README_BROWSER_TESTING.md`, `BROWSER_TESTING_SETUP.md`)

### Fixed
- **Server Access Issue**: Fixed 403 Forbidden errors in browser tests
  - Changed test URLs from `localhost` to `127.0.0.1` to avoid IPv6 resolution issues on macOS
  - Updated all test files to use IPv4 address instead of localhost
  - Server now accessible for automated testing
  - Root cause: macOS resolves `localhost` to IPv6 (`::1`) which hits Apple's AirPlay service instead of Flask

- **Reshuffle Functionality**: Fixed multiple issues with reshuffle mode in Observation Media module
  - Fixed draggable attribute check - now properly checks for cell content instead of relying on attribute
  - Ensured all cells with media content are made draggable when reshuffle is enabled
  - Fixed table generation to only set `draggable="true"` when media actually exists
  - Improved visual indicator application (blue dashed borders, grab cursor)
  - Enhanced console logging for reshuffle operations with detailed debugging
  - Fixed cell state management when reshuffle is disabled

### Enhanced
- **Debugging**: Added extensive debugging logs for reshuffle functionality
  - Added `[RESHUFFLE]` console logs throughout reshuffle operations
  - Logs include: mode state, button states, cell counts, visual indicator updates
  - Enhanced dialog reshuffle debugging with detailed state tracking
  - Comprehensive logging for drag-and-drop operations

### Changed
- **Test Infrastructure**: 
  - Updated Playwright API calls to use snake_case (e.g., `to_contain_text` instead of `toContainText`)
  - Improved test fixtures to handle server connectivity issues gracefully
  - Added proper test skipping when elements are hidden (expected behavior)
  - Updated test dependencies to use latest Playwright version

### Technical Details

#### Testing Infrastructure
- **New Test Files**:
  - `tests/test_observation_media_drag_drop.py`: Browser tests for drag-and-drop, dialogs, reshuffle
  - `tests/test_observation_media_reshuffle.py`: Unit tests for reshuffle logic
  - `tests/test_reshuffle_functionality.py`: Comprehensive reshuffle functionality tests
  - `tests/test_setup_verification.py`: Setup and connectivity verification tests
  - `tests/conftest.py`: Pytest fixtures for browser testing
  - `tests/test_runner.py`: Test runner script with server health checks

- **New Dependencies**:
  - `playwright>=1.40.0`: Browser automation framework
  - Updated `pytest` and related testing packages

#### Frontend Changes
- **Reshuffle Functionality** (`static/js/observation-media.js`):
  - Enhanced `toggleReshuffleMode()`: Now checks for cell content, ensures draggable state
  - Fixed `generateMediaTable()`: Only sets draggable when media exists
  - Improved visual indicator management
  - Enhanced console logging throughout

#### Documentation
- Added `BROWSER_TESTING_SETUP.md`: Complete guide for browser testing environment
- Added `SERVER_FIX_SUMMARY.md`: Documentation of server access fix
- Added `RESHUFFLE_FIX_SUMMARY.md`: Documentation of reshuffle fixes
- Added `TEST_RESULTS.md`: Test execution results and status
- Added `tests/README_BROWSER_TESTING.md`: Detailed browser testing documentation

### Test Results
- ✅ **6 browser tests passing** (5 skipped when no media assigned - expected)
- ✅ **9 reshuffle unit tests passing**
- ✅ **All test infrastructure working correctly**
- ✅ **Server accessibility verified**

---

## [1.1.0] - 2025-01-XX

### Added
- **Video Trim & Crop Actions**: Added interactive video editing capabilities to Media Converter
  - **Trim Video**: Cut video to specified time range with visual timeline interface
  - **Crop Video**: Select and crop video region with interactive overlay rectangle
  - Actions accessible by clicking video thumbnails in Media Converter
  - Full-screen overlay interface with video player and editing controls

- **Video Actions Overlay Interface**: 
  - Click video thumbnail to open interactive editing overlay
  - Video player with custom controls (play/pause, timeline scrubber, volume, fullscreen)
  - Separate action panels for Trim and Crop modes
  - Sticky action buttons bar for easy access to Apply/Cancel actions
  - Responsive design that works on desktop, tablet, and mobile

- **Visual Trim Timeline Interface**:
  - Interactive timeline bar with draggable start/end markers
  - Click anywhere on timeline to set trim points
  - Visual region highlighting showing what will be kept
  - Color-coded markers: 🟢 Green for start, 🔴 Red for end
  - Real-time duration calculation and display
  - "Set Now" buttons to use current playback position
  - Current time display for both start and end points

- **Interactive Crop Overlay**:
  - Draggable and resizable crop rectangle overlay on video
  - Corner handles for precise resizing
  - Real-time position and size updates
  - Aspect ratio presets (16:9, 4:3, 1:1, Original, Custom)
  - Center crop button for quick centering
  - Visual feedback with semi-transparent overlay

- **Enhanced Error Handling & Debugging**:
  - Comprehensive error logging in browser console
  - Detailed error messages including FFmpeg stderr/stdout
  - Request/response logging for debugging
  - Button state management during processing
  - Clear error messages with actionable information

- **Output File Management**:
  - Success messages clearly indicate output folder location
  - Download option immediately after crop/trim operations
  - File path information in success alerts
  - Clarification that original files remain unchanged

### Changed
- **Video Action Icons**: 
  - Trim button: Changed from ✂️ to ⏱️ (stopwatch icon)
  - Crop button: Kept ✂️ (scissors icon)
  - Actions panel header: Changed to 🎬 (video camera icon)

- **Video Thumbnail Interaction**:
  - Removed separate Trim/Crop buttons from video cards
  - Clicking thumbnail now opens video actions overlay
  - Added hint text: "Click thumbnail to trim or crop"

- **Trim Interface Layout**:
  - Replaced simple input fields with visual timeline interface
  - Better organized input fields with color-coded labels
  - Improved visual feedback and real-time updates
  - More intuitive drag-and-click interactions

- **Success Messages**:
  - Enhanced to clearly show output file location
  - Includes file name, size, and full path
  - Explains that files are saved to OUTPUT folder
  - Offers immediate download option

### Fixed
- **Button Visibility**: Fixed action buttons being cut off or hidden
  - Added sticky action buttons bar at bottom of panels
  - Made overlay container scrollable
  - Improved responsive layout for all screen sizes

- **Error Display**: Fixed confusing error messages
  - Added comprehensive error details in console
  - Better error messages in alerts
  - Includes FFmpeg error output for debugging

- **File Location Clarity**: Fixed confusion about where cropped/trimmed files are saved
  - Clear messaging that files go to OUTPUT folder
  - Original files remain in INPUT folder unchanged
  - Download option to access processed files immediately

### Technical Details

#### Backend Changes
- **New Modules**:
  - Enhanced `app/video_converter.py`: Added `trim_video()` and `crop_video()` functions
  - Uses FFmpeg for video processing with proper error handling

- **New Endpoints**:
  - `/media-converter/trim-video`: POST endpoint for trimming videos
  - `/media-converter/crop-video`: POST endpoint for cropping videos

- **Updated Endpoints**:
  - `/media-converter/list`: Returns video dimensions and duration for crop/trim UI
  - Enhanced error responses with FFmpeg stderr/stdout for debugging

#### Frontend Changes
- **Video Actions Overlay System**:
  - Full-screen overlay component with video player
  - Mode-based UI (none, trim, crop)
  - Real-time state management for trim/crop parameters
  - Visual timeline with interactive markers
  - Crop overlay with drag-and-resize functionality

- **Enhanced JavaScript Functions**:
  - `openVideoActionsOverlay()`: Opens overlay with video player
  - `activateTrimMode()` / `activateCropMode()`: Mode switching
  - `initTrimVisualTimeline()`: Visual timeline interactions
  - `initCropOverlay()`: Crop rectangle drag/resize handlers
  - Comprehensive error handling in `applyTrim()` and `applyCrop()`

- **Responsive Design**:
  - Scrollable overlay container
  - Sticky action buttons
  - Responsive grid layouts for input fields
  - Touch-friendly controls for mobile devices

#### Dependencies
- No new dependencies (uses existing FFmpeg requirement)

---

## [1.0.0] - 2025-11-23

### Added
- **Input/Output Folder Architecture**: Separated source files from generated output
  - Input folder: `/Users/rom/Documents/nvq/v2p-formatter-input` (read-only source MP4 files)
  - Output folder: `/Users/rom/Documents/nvq/v2p-formatter-output` (all generated files)
  - Each video gets its own subfolder in the output directory

- **File Selection System**: Replaced file upload with server-side file selector
  - Automatically scans input folder for MP4 files on page load
  - Displays files in a tree structure
  - Files are selected from the server, not uploaded

- **Time Point Selection**: Enhanced video time point selection
  - Video scrubbing/scrubbing to select time points
  - Preview thumbnails for each selected time point
  - Auto-generate time points: 5, 10, 15, 20, or custom number of evenly spaced shots
  - Visual thumbnail cards with remove functionality

- **DOCX Export**: Added Word document export capability
  - Generates DOCX files alongside PDF
  - Uses 2-column table layout with 1px black borders
  - Images maintain aspect ratio

- **Table Layout for Documents**: Implemented 2-column table layout
  - PDF: Uses ReportLab Table with 2 columns per row
  - DOCX: Uses python-docx Table with 2 columns per row
  - Single table for all rows (not separate tables per row)
  - 1px black borders on all cells
  - 5px spacing between bottom of image and table border

- **Dual Format Generation**: Generate both PDF and DOCX by default
  - Single button generates both formats simultaneously
  - Progress tracking for both files
  - Download links for both formats displayed

- **Dark Theme**: Complete dark theme implementation
  - Dark backgrounds for all sections, fields, and tables
  - Light text colors for readability
  - Dark buttons and form elements
  - Dark thumbnail preview cards
  - Consistent dark color scheme throughout

### Changed
- **Default Resolution**: Changed default image resolution from "original" to "640x480"
- **Output Structure**: All files now saved in video-specific subfolders
  - Structure: `OUTPUT_FOLDER/{video_filename}/`
  - PDF: `{video_filename}/{video_filename}.pdf`
  - DOCX: `{video_filename}/{video_filename}.docx`
  - Images: `{video_filename}/frames/1.jpg, 2.jpg, etc.`

- **UI Simplification**: 
  - Removed header section
  - Removed input/output folder information boxes
  - Merged "Image Configuration" and "PDF Configuration" into single "Output Settings" section
  - Simplified file loading (auto-loads on page load)

- **Button Labels**: 
  - Changed "Generate Document" to "Generate PDF & DOCX"
  - Updated to reflect dual format generation

### Fixed
- **Time Point Validation**: Fixed floating-point precision issues
  - Time points are now clamped to be within video duration
  - Prevents "outside video duration" errors
  - Handles edge cases at video end

- **PDF Image Scaling**: Fixed image scaling when "1 image per page" selected
  - Images now properly fill the page (95% of available space)
  - Maintains aspect ratio
  - No longer shows only 10% of image

- **File Loading**: Fixed "Loading MP4 files..." message persisting forever
  - Simplified file loading logic
  - Better error handling and user feedback

- **Thumbnail Display**: Fixed time point preview thumbnails
  - Now displays actual image previews instead of just text
  - Thumbnails load asynchronously
  - Visual cards with remove functionality

### Technical Details

#### Backend Changes
- **New Modules**:
  - `app/docx_generator.py`: DOCX document generation
  - Updated `app/pdf_generator.py`: Table-based layout
  - Updated `app/utils.py`: Subfolder management functions

- **New Endpoints**:
  - `/generate_docx`: Generate DOCX documents

- **Updated Endpoints**:
  - `/extract_frames`: Now handles array of time points directly
  - `/generate_pdf`: Returns consistent `file_path` field

#### Frontend Changes
- **Consolidated JavaScript**: Moved all core logic to inline script in `index.html`
- **Simplified File Loading**: Direct fetch calls, no complex retry logic
- **Enhanced Time Selection**: Direct onclick handlers, thumbnail previews
- **Dark Theme CSS**: Comprehensive dark theme styling

#### Dependencies
- Added `python-docx>=1.1.0` for DOCX generation

### Removed
- File upload functionality (replaced with file selector)
- Format selector dropdown (both formats generated by default)
- Input/Output folder information boxes from UI
- Header section from application interface

---

## Notes

- All generated files are saved in the output folder structure: `OUTPUT_FOLDER/{video_name}/`
- PDF and DOCX files use the video filename (without extension)
- Images are saved in a `frames/` subfolder within each video's output folder
- Default resolution is 640x480
- Both PDF and DOCX are generated automatically when clicking "Generate PDF & DOCX"

