# Media Converter Module - Feature Specification

## Overview

Add a new **Media Converter** module to the Video to Image Formatter application. This module will be accessible via a TAB interface, allowing users to convert media files from the input folder to optimized formats in the output folder.

## Core Functionality

### Supported Input Formats
- **Video**: `.mov` files
- **Image**: `.jpg` / `.jpeg` files

### Conversion Operations

#### 1. Video Conversion (MOV → MP4)
- Convert `.mov` files to `.mp4` format
- Provide compression options for smaller file sizes:
  - **Low Quality** (smallest size, lower quality)
  - **Medium Quality** (balanced size/quality)
  - **High Quality** (larger size, best quality)
  - **Custom** (user-defined bitrate/quality settings)

#### 2. Image Conversion (JPG → JPEG)
- Convert `.jpg` files to `.jpeg` format (standardization)
- Provide compression and resolution options:
  - **Resolution presets**: 
    - Original resolution
    - 1920x1080 (Full HD)
    - 1280x720 (HD)
    - 640x480 (SD)
    - Custom resolution (user-defined width x height)
  - **Quality/Compression levels**:
    - Low (smallest size, lower quality)
    - Medium (balanced)
    - High (larger size, best quality)
    - Custom (user-defined quality percentage)

### File Processing
- Scan input folder recursively (including subfolders) for supported media files
- Process files individually or in batch
- Preserve subfolder structure in output folder
- Maintain original filenames (with format extension change)

## UI/UX Design

### Tab Navigation
- Add a tab system to the main interface:
  - **Tab 1**: "Video to Image" (current functionality)
  - **Tab 2**: "Media Converter" (new module)

### Media Converter Interface

#### File Selection Section

**Text Wireframe:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 📁 File Selection                                                       │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 🔍 Search files... [________________________]  🔄 Refresh          │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 🎬 Video Files (MOV)                                    [▼ Expand] │ │
│ │ ┌───────────────────────────────────────────────────────────────┐   │ │
│ │ │ ☑ Select All Videos (12 files, 2.4 GB total)                │   │ │
│ │ └───────────────────────────────────────────────────────────────┘   │ │
│ │                                                                     │ │
│ │ ┌───────────────────────────────────────────────────────────────┐ │ │
│ │ │ ☑ 🎬 video1.mov                                                │ │ │
│ │ │    📁 /input/folder1/video1.mov                                │ │ │
│ │ │    📊 245.3 MB  |  🕐 00:05:32  |  📐 1920x1080                │ │ │
│ │ └───────────────────────────────────────────────────────────────┘ │ │
│ │                                                                     │ │
│ │ ┌───────────────────────────────────────────────────────────────┐ │ │
│ │ │ ☐ 🎬 video2.mov                                                │ │ │
│ │ │    📁 /input/folder1/subfolder/video2.mov                      │ │ │
│ │ │    📊 189.7 MB  |  🕐 00:03:15  |  📐 1280x720                 │ │ │
│ │ └───────────────────────────────────────────────────────────────┘ │ │
│ │                                                                     │ │
│ │ ┌───────────────────────────────────────────────────────────────┐ │ │
│ │ │ ☑ 🎬 video3.mov                                                │ │ │
│ │ │    📁 /input/folder2/video3.mov                                │ │ │
│ │ │    📊 512.1 MB  |  🕐 00:12:45  |  📐 3840x2160                │ │ │
│ │ └───────────────────────────────────────────────────────────────┘ │ │
│ │                                                                     │ │
│ │ ... (9 more files)                                                │ │
│ │                                                                     │ │
│ │ [Show All 12 files]  or  [Load More...]                           │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 🖼️ Image Files (JPG)                                    [▼ Expand] │ │
│ │ ┌───────────────────────────────────────────────────────────────┐   │ │
│ │ │ ☑ Select All Images (47 files, 156.8 MB total)              │   │ │
│ │ └───────────────────────────────────────────────────────────────┘   │ │
│ │                                                                     │ │
│ │ ┌───────────────────────────────────────────────────────────────┐ │ │
│ │ │ ☑ 🖼️ photo1.jpg                                                │ │ │
│ │ │    📁 /input/images/photo1.jpg                                 │ │ │
│ │ │    📊 3.2 MB  |  📐 4000x3000                                  │ │ │
│ │ └───────────────────────────────────────────────────────────────┘ │ │
│ │                                                                     │ │
│ │ ┌───────────────────────────────────────────────────────────────┐ │ │
│ │ │ ☐ 🖼️ photo2.jpg                                                │ │ │
│ │ │    📁 /input/images/folder1/photo2.jpg                         │ │ │
│ │ │    📊 2.1 MB  |  📐 1920x1080                                  │ │ │
│ │ └───────────────────────────────────────────────────────────────┘ │ │
│ │                                                                     │ │
│ │ ... (45 more files)                                               │ │
│ │                                                                     │ │
│ │ [Show All 47 files]  or  [Load More...]                          │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 📊 Selection Summary                                               │ │
│ │ • Videos Selected: 3 of 12                                         │ │
│ │ • Images Selected: 1 of 47                                         │ │
│ │ • Total Selected: 4 files                                          │ │
│ │ • Total Size: 752.6 MB                                             │ │
│ │                                                                     │ │
│ │ [Clear Selection]  [Select All Files]                             │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

**Detailed UI Specifications:**

1. **Section Header**
   - Title: "📁 File Selection"
   - Search bar at top with placeholder "🔍 Search files..."
   - Refresh button (🔄) to rescan input folder

2. **File Type Groups (Collapsible Sections)**
   - **Video Files (MOV) Section**
     - Header: "🎬 Video Files (MOV)" with expand/collapse toggle (▼/▶)
     - Shows count: "(12 files)"
     - Collapsible to save space when many files
   
   - **Image Files (JPG) Section**
     - Header: "🖼️ Image Files (JPG)" with expand/collapse toggle (▼/▶)
     - Shows count: "(47 files)"
     - Collapsible to save space when many files

3. **Select All Per Type**
   - Checkbox: "☑ Select All Videos" / "☑ Select All Images"
   - Shows file count and total size for that type
   - Toggles all files in that section

4. **Individual File Cards**
   - **Checkbox** (☑/☐) for selection
   - **Icon**: 🎬 for videos, 🖼️ for images
   - **Filename** (bold, prominent)
   - **File Path** (smaller text, monospace font, truncated with ellipsis if long)
   - **Metadata** (horizontal layout):
     - 📊 File size (MB/GB)
     - 🕐 Duration (for videos only, HH:MM:SS format)
     - 📐 Resolution (width x height)
   - **Hover effect**: Highlight on hover
   - **Selected state**: Different background color

5. **Pagination/Loading**
   - For sections with many files (>20), show first 20
   - "Show All X files" button to expand
   - Or "Load More..." for infinite scroll
   - Scrollable container (max-height: 600px) with custom scrollbar

6. **Selection Summary Box**
   - Fixed at bottom of file selection area
   - Shows:
     - Videos selected: X of Y
     - Images selected: X of Y
     - Total selected: X files
     - Total size: X MB/GB
   - Action buttons:
     - "Clear Selection" - deselect all
     - "Select All Files" - select everything

7. **Styling (Dark Theme)**
   - Background: #1e1e1e (dark gray)
   - File cards: #2a2a2a with #555 border
   - Selected cards: #333 with #667eea border
   - Text: #e0e0e0 (light gray)
   - Metadata: #999 (darker gray)
   - Icons: Color-coded (blue for videos, green for images)
   - Hover: Background #333, border #667eea

8. **Responsive Behavior**
   - On smaller screens, file cards stack vertically
   - Metadata wraps to multiple lines if needed
   - Search bar remains at top, always visible
   - Summary box can be sticky/fixed at bottom

9. **Empty States**
   - If no MOV files: "No MOV files found in input folder"
   - If no JPG files: "No JPG files found in input folder"
   - If no files at all: "No media files found. Add MOV or JPG files to the input folder."

10. **Loading State**
    - While scanning: "🔍 Scanning input folder for media files..."
    - Spinner animation
    - Disable interaction until scan completes

#### Conversion Settings Section

**For Video Files (MOV → MP4):**
- Quality preset selector (Low/Medium/High/Custom)
- If Custom:
  - Bitrate input (kbps)
  - Codec selector (H.264, H.265/HEVC)
  - Frame rate option (maintain original or set custom)
- Preview estimated output size

**For Image Files (JPG → JPEG):**
- Resolution preset selector (Original/1920x1080/1280x720/640x480/Custom)
- If Custom:
  - Width input (pixels)
  - Height input (pixels)
  - Maintain aspect ratio checkbox
- Quality/Compression selector (Low/Medium/High/Custom)
- If Custom:
  - Quality percentage slider (1-100%)

#### Batch Processing Options
- Process all selected files with same settings
- Process each file type with different settings
- Show progress bar for batch operations
- Display conversion status for each file (pending/processing/completed/failed)

#### Output Section
- Display conversion results:
  - Original file path
  - Converted file path
  - Original size vs. converted size
  - Compression ratio/space saved
  - Processing time
- Provide download links for converted files
- Show success/error messages per file

## Technical Implementation

### Backend Components

#### New Routes (`app/routes.py`)
- `GET /v2p-formatter/media-converter/list` - List all media files (MOV, JPG)
- `POST /v2p-formatter/media-converter/convert` - Convert selected files
- `GET /v2p-formatter/media-converter/status/<job_id>` - Check conversion status
- `GET /v2p-formatter/media-converter/download/<path>` - Download converted file

#### New Modules

**`app/media_converter.py`**
- `scan_media_files(input_folder)` - Scan for MOV and JPG files recursively
- `convert_mov_to_mp4(input_path, output_path, quality_preset, custom_settings)` - Video conversion
- `convert_jpg_to_jpeg(input_path, output_path, resolution, quality)` - Image conversion
- `get_file_info(file_path)` - Get file metadata (size, duration, resolution, etc.)

**`app/video_converter.py`** (if needed)
- Video conversion logic using FFmpeg or OpenCV
- Quality preset definitions
- Bitrate calculation

**`app/image_converter.py`** (if needed)
- Image conversion logic using Pillow
- Resolution resizing
- Quality/compression handling

### Frontend Components

#### New Template (`templates/media_converter.html`)
- Tab navigation component
- File list display
- Settings forms
- Progress indicators
- Results table

#### JavaScript (`static/js/media_converter.js`)
- File scanning and display
- Settings form handling
- AJAX calls for conversion
- Progress tracking
- Results display

### Dependencies
- **FFmpeg** (for video conversion) - may need `ffmpeg-python` or subprocess calls
- **Pillow** (already in use for images)
- Consider: `moviepy` for video processing (alternative to FFmpeg)

## Configuration

### New Config Settings (`config.py`)
```python
# Media Converter Settings
MEDIA_CONVERTER_INPUT_FOLDER = INPUT_FOLDER  # Same as main input
MEDIA_CONVERTER_OUTPUT_FOLDER = OUTPUT_FOLDER  # Same as main output

# Video Conversion Presets
VIDEO_QUALITY_PRESETS = {
    'low': {'bitrate': '500k', 'crf': 28},
    'medium': {'bitrate': '1000k', 'crf': 23},
    'high': {'bitrate': '2000k', 'crf': 18}
}

# Image Conversion Presets
IMAGE_QUALITY_PRESETS = {
    'low': 60,
    'medium': 80,
    'high': 95
}
```

## Questions for Clarification

### 1. Video Conversion (MOV → MP4)
- **Q1.1**: Should we support other video formats as input (e.g., `.avi`, `.mkv`, `.m4v`), or only `.mov`? = mov only; however other formats will be supported in future;
- **Q1.2**: For "low size" options, what is the target file size reduction? (e.g., 50% smaller, 70% smaller?) = yes the file size must be reduced;
- **Q1.3**: Should we maintain the original video resolution, or allow downscaling for smaller file sizes? = the key is to refuze the file size;
- **Q1.4**: Do you want to preserve audio tracks in the converted MP4 files? = yes;
- **Q1.5**: Should we support batch conversion with different quality settings per file, or one setting for all selected files? = one setting;

### 2. Image Conversion (JPG → JPEG)
- **Q2.1**: Since JPG and JPEG are essentially the same format (just different extensions), do you want:
  - Option A: Just rename `.jpg` to `.jpeg` and optionally compress/resize? keep initial file extension ;
  - Option B: Actually re-encode the image with different compression settings?
- **Q2.2**: For "low size" options, what quality percentage should "Low" preset use? (e.g., 60%, 70%?)
- **Q2.3**: When resizing images, should we:
  - Always maintain aspect ratio? = yes;
  - Allow stretching/cropping to exact dimensions? = yes
  - Provide both options?
- **Q2.4**: Should we support other image formats as input (e.g., `.png`, `.bmp`, `.tiff`), or only `.jpg`? = add png; more formats potentially will come;

### 3. File Organization
- **Q3.1**: Should converted files be saved in the same subfolder structure as input, or in a flat structure? = the same as subfolder;
  - Example: `input/folder1/video.mov` → `output/folder1/video.mp4` (preserve structure)
  - Or: `input/folder1/video.mov` → `output/video.mp4` (flat)
- **Q3.2**: Should we create a separate subfolder for converted files (e.g., `output/converted/`), or save directly in output root? = save in output root;
- **Q3.3**: If a file with the same name already exists in output, should we:
  - Overwrite it?
  - Add a suffix (e.g., `video_1.mp4`)? = yes;
  - Skip conversion?

### 4. User Interface
- **Q4.1**: Should the tab navigation be horizontal tabs at the top, or vertical tabs on the side? = horizontal at the top;
- **Q4.2**: Do you want a separate page/route for the media converter, or tabs within the same page? = separate;
- **Q4.3**: Should users be able to process video and image files simultaneously, or separately? = simultaniosly;
- **Q4.4**: Do you want a preview of the converted file before finalizing, or direct conversion? = yes;

### 5. Processing & Performance
- **Q5.1**: Should conversion happen:
  - Synchronously (user waits for completion)? 
  - Asynchronously (background jobs with status updates)? = this one ok;
- **Q5.2**: For batch processing, should we:
  - Process files sequentially (one at a time)?
  - Process files in parallel (multiple files simultaneously)? - what ever is more efficient;
- **Q5.3**: Should there be a file size limit for conversion? (e.g., skip files larger than 500MB) = no need;
- **Q5.4**: Do you want progress indicators for individual file conversion, or just overall batch progress? = overall;

### 6. Error Handling
- **Q6.1**: If a file conversion fails, should we:
  - Continue processing other files?
  - Stop the entire batch? = stop;
- **Q6.2**: Should we log conversion errors to a file, or just display them in the UI? = add debugging;
- **Q6.3**: Should we validate files before conversion (e.g., check if file is corrupted, check codec support)?  = yes;

### 7. Additional Features
- **Q7.1**: Do you want to add metadata preservation (e.g., EXIF data for images, creation date)? = no
- **Q7.2**: Should we provide a "test conversion" option that converts a small sample to preview quality? = no
- **Q7.3**: Do you want conversion history/logs to track what was converted and when? = no
- **Q7.4**: Should we add an option to delete original files after successful conversion? = no;

## Implementation Priority

### Phase 1: Core Functionality (MVP)
1. Tab navigation system
2. File scanning and display (MOV, JPG)
3. Basic MOV → MP4 conversion (single quality preset)
4. Basic JPG → JPEG conversion (single quality/resolution preset)
5. Single file conversion
6. Output to correct folder structure

### Phase 2: Enhanced Features
1. Multiple quality presets
2. Custom quality/resolution settings
3. Batch processing
4. Progress indicators
5. Results display with file size comparison

### Phase 3: Advanced Features
1. Parallel processing
2. Preview functionality
3. Conversion history
4. Advanced error handling
5. Metadata preservation

## Notes

- The media converter will use the same `INPUT_FOLDER` and `OUTPUT_FOLDER` as the main application
- Consider using FFmpeg via subprocess for video conversion (more control and better compression)
- Pillow (already in dependencies) can handle image conversion and resizing
- Ensure dark theme consistency across the new interface
- Follow the same file structure preservation logic as the main video-to-image converter

