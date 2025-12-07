# Changelog

All notable changes to the Video to Image Formatter (v2p-formatter) project will be documented in this file.

## [1.4.0] - 2025-01-XX

### Added
- **Preview Draft Modal - Two-Column Layout with Section Navigation**:
  - Split Document Preview into two resizable columns
  - Left column: Section navigation sidebar (200-400px resizable width)
  - Right column: Preview content area
  - Resizable divider between columns with visual feedback
  - Section navigation automatically built from document sections
  - Color-coded section navigation items matching section titles
  - Click-to-scroll functionality - clicking a section navigates to it in the preview
  - Smooth scrolling with brief highlight animation when navigating to sections
  - Navigation updates automatically after undo/redo operations

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
  - Restructured preview modal to two-column layout with resizable divider
  - Added section navigation sidebar with color-coded items
  - Added "Hide empty media fields" checkbox to Hide Elements section
  - Added bulk select/deselect buttons for Hide Elements
  - Updated Text Editor placement and styling

- **`static/js/observation-media.js`**:
  - `extractTextFromPreview()`: Added `preserveHiddenElements` parameter
    - When `true` (Update Draft): Preserves all elements in original text
    - When `false` (Export): Removes hidden elements and empty tables
  - `generateDocxPreview()`: Added section IDs and color-coded borders
  - `buildPreviewSectionNavigation()`: Builds section navigation from preview content
  - `scrollToPreviewSection()`: Smooth scroll to section with highlight
  - `startResizePreview()`, `handleResizePreview()`, `stopResizePreview()`: Column resizing
  - `exportObservationDocxFromPreview()`: Extracts text with hidden elements excluded
  - `selectAllHideElements()`, `deselectAllHideElements()`: Bulk operations
  - `updatePreviewDisplay()`: Added empty table hiding logic
  - Improved text extraction to preserve line breaks and formatting
  - Fixed AC covered line extraction to keep label and values together
  - Added cleanup regex to remove blank lines before AC covered lines

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
- Added resizer hover effects (color change on hover)
- Section navigation item styling with hover effects
- Color-coded section title borders matching navigation

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

