# Media Converter Module - Final Development Specification

## Document Information
- **Version**: 1.0
- **Date**: 2024
- **Status**: ✅ **APPROVED FOR DEVELOPMENT**
- **Based on**: Requirements gathered from media-converter.md Q&A
- **Approval Date**: 2024

---

## 1. Overview

### 1.1 Purpose
Add a new **Media Converter** module to the Video to Image Formatter application that allows users to convert media files (MOV videos and JPG/PNG images) to optimized formats (MP4 and JPEG) with file size reduction as the primary goal.

### 1.2 Key Requirements
- **Primary Goal**: Reduce file sizes while maintaining acceptable quality
- **Input Formats**: `.mov` (videos), `.jpg`/`.jpeg` and `.png` (images)
- **Output Formats**: `.mp4` (videos), `.jpeg` (images - keep original extension)
- **Architecture**: Separate page/route with horizontal tab navigation
- **Processing**: Asynchronous with background jobs and status updates
- **File Organization**: Preserve input subfolder structure in output root

---

## 2. Supported Formats & Conversions

### 2.1 Video Conversion (MOV → MP4)
- **Input**: `.mov` files only (other formats may be added in future)
- **Output**: `.mp4` files
- **Requirements**:
  - Reduce file size (primary objective)
  - Preserve audio tracks
  - One quality setting applies to all selected files
  - May downscale resolution to reduce file size

### 2.2 Image Conversion (JPG/PNG → JPEG)
- **Input**: `.jpg`, `.jpeg`, and `.png` files
- **Output**: `.jpeg` files (keep original extension: `.jpg` → `.jpg`, `.png` → `.jpeg`)
- **Requirements**:
  - Reduce file size through compression and/or resizing
  - Support both aspect ratio preservation AND stretching/cropping
  - One quality/resolution setting applies to all selected files
  - More formats may be added in future

---

## 3. User Interface Design

### 3.1 Navigation Structure
- **Tab Navigation**: Horizontal tabs at the top of the page
- **Tab 1**: "Video to Image" (existing functionality)
- **Tab 2**: "Media Converter" (new module)
- **Route**: Separate page/route (`/v2p-formatter/media-converter`)

### 3.2 File Selection Section

#### Layout Structure
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
│ │ ... (more files)                                                  │ │
│ │ [Show All 12 files]  or  [Load More...]                           │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 🖼️ Image Files (JPG/PNG)                                [▼ Expand] │ │
│ │ ┌───────────────────────────────────────────────────────────────┐   │ │
│ │ │ ☑ Select All Images (47 files, 156.8 MB total)              │   │ │
│ │ └───────────────────────────────────────────────────────────────┘   │ │
│ │                                                                     │ │
│ │ ┌───────────────────────────────────────────────────────────────┐ │ │
│ │ │ ☑ 🖼️ photo1.jpg                                                │ │ │
│ │ │    📁 /input/images/photo1.jpg                                 │ │ │
│ │ │    📊 3.2 MB  |  📐 4000x3000                                  │ │ │
│ │ └───────────────────────────────────────────────────────────────┘ │ │
│ │ ... (more files)                                                  │ │
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

#### UI Specifications
1. **Search Bar**: Filter files by name/path
2. **Refresh Button**: Rescan input folder
3. **Collapsible Sections**: Video and Image sections can be expanded/collapsed
4. **Select All Per Type**: Checkbox to select all files in each category
5. **File Cards**: Show checkbox, icon, filename, path, size, duration (videos), resolution
6. **Pagination**: Show first 20 files, "Show All" or "Load More" for rest
7. **Selection Summary**: Fixed box showing selection counts and total size
8. **Dark Theme**: Consistent with existing application (#1e1e1e background, #2a2a2a cards)

### 3.3 Conversion Settings Section

#### Video Settings (MOV → MP4)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ 🎬 Video Conversion Settings                                            │
│                                                                         │
│ Quality Preset: [Low ▼]                                                │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Low Quality: Smallest file size, lower quality                      │ │
│ │ Medium Quality: Balanced size/quality                               │ │
│ │ High Quality: Larger file size, best quality                         │ │
│ │ Custom: User-defined settings                                       │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ [If Custom selected]                                                    │
│ Bitrate (kbps): [1000____]                                             │
│ Codec: [H.264 ▼]                                                       │
│ Frame Rate: [Maintain Original ▼]                                     │
│                                                                         │
│ Estimated Output Size: ~150 MB (38% reduction)                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Image Settings (JPG/PNG → JPEG)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ 🖼️ Image Conversion Settings                                            │
│                                                                         │
│ Resolution Preset: [1280x720 ▼]                                        │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Original: Keep original resolution                                 │ │
│ │ 1920x1080: Full HD                                                  │ │
│ │ 1280x720: HD                                                        │ │
│ │ 640x480: SD                                                         │ │
│ │ Custom: User-defined dimensions                                     │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ [If Custom selected]                                                    │
│ Width (px): [1920____]                                                 │
│ Height (px): [1080____]                                                │
│ ☑ Maintain Aspect Ratio                                                │
│ ☐ Allow Stretching/Cropping                                            │
│                                                                         │
│ Quality Preset: [Medium ▼]                                             │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Low: Smallest size, lower quality (60%)                            │ │
│ │ Medium: Balanced (80%)                                              │ │
│ │ High: Larger size, best quality (95%)                               │ │
│ │ Custom: User-defined percentage                                    │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ [If Custom selected]                                                    │
│ Quality (%): [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] 85%   │
│                                                                         │
│ Estimated Output Size: ~1.2 MB (62% reduction)                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.4 Processing & Results Section

#### Processing Interface
```
┌─────────────────────────────────────────────────────────────────────────┐
│ ⚙️ Conversion Progress                                                  │
│                                                                         │
│ Overall Progress: [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] │
│ 75% Complete (3 of 4 files)                                            │
│                                                                         │
│ Status: Processing...                                                   │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ✅ video1.mov → video1.mp4                                          │ │
│ │    Original: 245.3 MB → Converted: 98.1 MB (60% reduction)         │ │
│ │    Time: 12.3s                                                      │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ ✅ photo1.jpg → photo1.jpg                                          │ │
│ │    Original: 3.2 MB → Converted: 1.1 MB (66% reduction)             │ │
│ │    Time: 0.8s                                                       │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ ⏳ video2.mov → video2.mp4 (Processing...)                          │ │
│ │    Progress: [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] │ │
│ │    45% Complete                                                     │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ ⏸️ photo2.jpg → photo2.jpg (Pending)                               │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ [Cancel Conversion]                                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Results Display
- Show each file's conversion status (Pending/Processing/Completed/Failed)
- Display original vs. converted file size
- Show compression ratio/space saved percentage
- Display processing time per file
- Provide download links for completed conversions
- Show error messages for failed conversions

### 3.5 Preview Functionality
- **Preview Button**: Available after conversion completes
- **Preview Modal**: Show converted file (video player for MP4, image viewer for JPEG)
- **Action Buttons**: "Download", "Convert Another", "Close"

---

## 4. Technical Architecture

### 4.1 Backend Routes

#### New Routes in `app/routes.py`
```python
# Media Converter Routes
@bp.route('/media-converter')
def media_converter():
    """Media converter main page"""
    return render_template('media_converter.html')

@bp.route('/media-converter/list', methods=['GET'])
def list_media_files():
    """List all MOV, JPG, JPEG, and PNG files in input folder"""
    # Returns: {success: bool, files: [{type, name, path, size, ...}], ...}

@bp.route('/media-converter/convert', methods=['POST'])
def convert_media():
    """Start conversion job (asynchronous)"""
    # Returns: {success: bool, job_id: str, message: str}

@bp.route('/media-converter/status/<job_id>', methods=['GET'])
def conversion_status(job_id):
    """Get conversion job status"""
    # Returns: {status: str, progress: float, files: [{status, ...}], ...}

@bp.route('/media-converter/cancel/<job_id>', methods=['POST'])
def cancel_conversion(job_id):
    """Cancel running conversion job"""
    # Returns: {success: bool, message: str}

@bp.route('/media-converter/preview/<path:file_path>', methods=['GET'])
def preview_converted_file(file_path):
    """Serve converted file for preview"""
    # Returns: File response

@bp.route('/media-converter/download/<path:file_path>', methods=['GET'])
def download_converted_file(file_path):
    """Download converted file"""
    # Returns: File download response
```

### 4.2 Backend Modules

#### `app/media_converter.py`
```python
def scan_media_files(input_folder: Path) -> dict:
    """Scan recursively for MOV, JPG, JPEG, PNG files"""
    # Returns: {videos: [...], images: [...]}

def get_file_info(file_path: Path) -> dict:
    """Get file metadata (size, duration, resolution, etc.)"""
    # Returns: {size, duration, width, height, ...}

def validate_file(file_path: Path, file_type: str) -> tuple[bool, str]:
    """Validate file before conversion"""
    # Returns: (is_valid, error_message)

def get_output_path(input_path: Path, output_base: Path, new_extension: str) -> Path:
    """Generate output path preserving subfolder structure"""
    # Handles duplicate files by adding suffix (_1, _2, etc.)
```

#### `app/video_converter.py`
```python
def convert_mov_to_mp4(
    input_path: Path,
    output_path: Path,
    quality_preset: str,
    custom_settings: dict = None
) -> dict:
    """Convert MOV to MP4 using FFmpeg"""
    # Returns: {success: bool, output_size: int, processing_time: float, ...}

def get_video_info(video_path: Path) -> dict:
    """Get video metadata using FFmpeg"""
    # Returns: {duration, width, height, bitrate, codec, ...}
```

#### `app/image_converter.py`
```python
def convert_image_to_jpeg(
    input_path: Path,
    output_path: Path,
    resolution: tuple = None,
    quality: int = 80,
    maintain_aspect: bool = True,
    allow_stretch: bool = False
) -> dict:
    """Convert JPG/PNG to JPEG using Pillow"""
    # Returns: {success: bool, output_size: int, processing_time: float, ...}

def get_image_info(image_path: Path) -> dict:
    """Get image metadata using Pillow"""
    # Returns: {width, height, format, size, ...}
```

#### `app/conversion_job.py` (New - for async processing)
```python
class ConversionJob:
    """Manages asynchronous conversion jobs"""
    def __init__(self, job_id: str, files: list, settings: dict):
        ...
    
    def start(self):
        """Start conversion in background thread"""
        ...
    
    def get_status(self) -> dict:
        """Get current job status"""
        ...
    
    def cancel(self):
        """Cancel running conversion"""
        ...
```

### 4.3 Frontend Components

#### `templates/media_converter.html`
- Main template for media converter page
- Includes file selection, settings, progress, and results sections
- Dark theme styling consistent with main app

#### `static/js/media_converter.js`
```javascript
// File scanning and display
function loadMediaFiles() { ... }
function renderFileList(files) { ... }
function filterFiles(searchTerm) { ... }

// Selection management
function toggleFileSelection(fileId) { ... }
function selectAllFiles(type) { ... }
function clearSelection() { ... }

// Settings management
function updateVideoSettings() { ... }
function updateImageSettings() { ... }
function estimateOutputSize() { ... }

// Conversion control
function startConversion() { ... }
function checkConversionStatus(jobId) { ... }
function cancelConversion(jobId) { ... }

// Results display
function updateProgress(data) { ... }
function showResults(results) { ... }
function previewFile(filePath) { ... }
```

#### `static/css/media_converter.css` (if needed)
- Additional styles specific to media converter
- Or extend existing `style.css`

### 4.4 Configuration

#### Updates to `config.py`
```python
# Media Converter Settings
MEDIA_CONVERTER_INPUT_FOLDER = INPUT_FOLDER  # Same as main input
MEDIA_CONVERTER_OUTPUT_FOLDER = OUTPUT_FOLDER  # Same as main output

# Video Conversion Presets (optimized for file size reduction)
VIDEO_QUALITY_PRESETS = {
    'low': {
        'bitrate': '500k',
        'crf': 28,  # Higher CRF = smaller file, lower quality
        'scale': '1280:720',  # Downscale to reduce size
        'codec': 'libx264',
        'preset': 'fast'
    },
    'medium': {
        'bitrate': '1000k',
        'crf': 23,
        'scale': '1920:1080',  # Keep HD or downscale if larger
        'codec': 'libx264',
        'preset': 'medium'
    },
    'high': {
        'bitrate': '2000k',
        'crf': 18,
        'scale': None,  # Keep original resolution
        'codec': 'libx264',
        'preset': 'slow'
    }
}

# Image Conversion Presets
IMAGE_RESOLUTION_PRESETS = {
    'original': None,
    '1920x1080': (1920, 1080),
    '1280x720': (1280, 720),
    '640x480': (640, 480)
}

IMAGE_QUALITY_PRESETS = {
    'low': 60,      # Smaller file, lower quality
    'medium': 80,   # Balanced
    'high': 95      # Larger file, best quality
}

# Processing Settings
MAX_CONCURRENT_CONVERSIONS = 2  # Process 2 files in parallel
CONVERSION_TIMEOUT = 3600  # 1 hour timeout per file
```

---

## 5. File Organization & Path Handling

### 5.1 Input Scanning
- Scan `INPUT_FOLDER` recursively using `rglob('*.mov')`, `rglob('*.jpg')`, etc.
- Preserve relative path structure from input folder

### 5.2 Output Path Generation
- **Preserve subfolder structure**: `input/folder1/sub/video.mov` → `output/folder1/sub/video.mp4`
- **Save in output root**: No `converted/` subfolder, save directly in output
- **Handle duplicates**: If file exists, add suffix: `video_1.mp4`, `video_2.mp4`, etc.
- **Extension handling**:
  - Videos: `.mov` → `.mp4`
  - Images: `.jpg` → `.jpg` (keep extension), `.png` → `.jpeg`

### 5.3 Path Validation
- Validate all input paths are within `INPUT_FOLDER`
- Validate all output paths are within `OUTPUT_FOLDER`
- Prevent path traversal attacks

---

## 6. Processing Logic

### 6.1 Asynchronous Processing
- Use background threads or Celery (if needed) for conversion jobs
- Store job status in memory (or Redis/database for persistence)
- Poll job status from frontend every 2-3 seconds

### 6.2 Batch Processing
- Process files **in parallel** (most efficient approach)
- Limit concurrent conversions (e.g., 2 at a time) to avoid resource exhaustion
- Process videos and images simultaneously if both are selected

### 6.3 Error Handling
- **Stop on failure**: If any file fails, stop entire batch
- **Validation**: Check files before conversion (corrupted, codec support, etc.)
- **Error logging**: Log errors to console and display in UI
- **Debug output**: Include detailed error messages for troubleshooting

### 6.4 Progress Tracking
- Track overall batch progress (X of Y files completed)
- Show individual file status (Pending/Processing/Completed/Failed)
- Update UI in real-time via status polling

---

## 7. Video Conversion Details

### 7.1 FFmpeg Integration
- Use FFmpeg via subprocess (ensure FFmpeg is installed)
- Command structure:
```bash
ffmpeg -i input.mov \
  -c:v libx264 \
  -b:v {bitrate} \
  -crf {crf_value} \
  -preset {preset} \
  -vf scale={width}:{height} \
  -c:a aac \
  -b:a 128k \
  -y output.mp4
```

### 7.2 Quality Presets
- **Low**: Maximum compression, downscale to 720p, CRF 28
- **Medium**: Balanced, keep HD or downscale 4K, CRF 23
- **High**: Minimal compression, keep original resolution, CRF 18

### 7.3 Audio Preservation
- Always include audio track: `-c:a aac -b:a 128k`
- Preserve original audio if possible, re-encode if needed

---

## 8. Image Conversion Details

### 8.1 Pillow Integration
- Use existing Pillow dependency
- Convert PNG to JPEG (RGBA → RGB conversion)
- Re-encode JPG with new quality settings

### 8.2 Resolution Handling
- **Maintain Aspect Ratio**: Calculate dimensions preserving ratio
- **Allow Stretching**: Resize to exact dimensions (may distort)
- **Cropping**: If aspect ratio differs, center crop to fit

### 8.3 Quality/Compression
- Use JPEG quality parameter (1-100)
- Lower quality = smaller file size
- Presets: Low (60%), Medium (80%), High (95%)

---

## 9. Dependencies

### 9.1 New Dependencies
```txt
ffmpeg-python>=0.2.0  # Optional: Python wrapper for FFmpeg
# OR use subprocess with system FFmpeg installation
```

### 9.2 System Requirements
- **FFmpeg**: Must be installed on system (check with `ffmpeg -version`)
- Installation:
  - macOS: `brew install ffmpeg`
  - Linux: `apt-get install ffmpeg` or `yum install ffmpeg`
  - Windows: Download from ffmpeg.org

### 9.3 Existing Dependencies (Already in use)
- Pillow (for image processing)
- Flask (for web framework)

---

## 10. Implementation Phases

### Phase 1: Core Infrastructure (MVP)
1. ✅ Create new route `/media-converter`
2. ✅ Create `media_converter.html` template with basic layout
3. ✅ Implement file scanning (`scan_media_files`)
4. ✅ Implement file list display with selection
5. ✅ Basic video conversion (MOV → MP4, single preset)
6. ✅ Basic image conversion (JPG → JPEG, single preset)
7. ✅ Output path generation with subfolder preservation
8. ✅ Duplicate file handling (add suffix)

### Phase 2: Settings & Batch Processing
1. ✅ Quality preset selectors (Low/Medium/High/Custom)
2. ✅ Resolution preset selectors for images
3. ✅ Custom settings inputs
4. ✅ Batch file selection and processing
5. ✅ Asynchronous job system
6. ✅ Progress tracking and status updates
7. ✅ Results display with file size comparison

### Phase 3: Enhanced Features
1. ✅ Preview functionality
2. ✅ Parallel processing (2 files at a time)
3. ✅ Error handling and validation
4. ✅ Search and filter functionality
5. ✅ File pagination/load more
6. ✅ Dark theme styling
7. ✅ Debug output and error logging

### Phase 4: Polish & Optimization
1. ✅ Performance optimization
2. ✅ UI/UX improvements
3. ✅ Comprehensive error messages
4. ✅ Loading states and animations
5. ✅ Responsive design

---

## 11. Debugging & Logging Requirements

### 11.1 Debug Output System

#### Frontend Debug Console
- **Location**: Similar to existing debug output in main app
- **Display**: Fixed debug panel at bottom of page (collapsible)
- **Format**: 
  ```
  ┌─────────────────────────────────────────────────────────┐
  │ 🔍 Debug Output                          [Clear] [Hide] │
  ├─────────────────────────────────────────────────────────┤
  │ [INFO] 2024-01-15 10:30:45 - Scanning media files...   │
  │ [SUCCESS] Found 12 MOV files, 47 JPG files            │
  │ [ERROR] Failed to convert video1.mov: FFmpeg error...   │
  │ [DEBUG] Conversion job started: job_abc123             │
  └─────────────────────────────────────────────────────────┘
  ```

#### Debug Message Types
- **INFO**: General information (file scanning, job started, etc.)
- **SUCCESS**: Successful operations (file converted, job completed)
- **ERROR**: Errors and failures (conversion failed, validation error)
- **DEBUG**: Detailed debugging info (FFmpeg commands, file paths, etc.)
- **WARNING**: Warnings (large file size, low disk space)

#### Frontend JavaScript Debugging
```javascript
// Debug logging function (similar to existing app)
function debug(message, type = 'info') {
    const timestamp = new Date().toISOString();
    const logEntry = `[${type.toUpperCase()}] ${timestamp} - ${message}`;
    
    // Console output
    console.log(logEntry);
    
    // UI debug panel
    const debugPanel = document.getElementById('debugMessages');
    if (debugPanel) {
        const entry = document.createElement('div');
        entry.className = `debug-${type}`;
        entry.textContent = logEntry;
        debugPanel.appendChild(entry);
        debugPanel.scrollTop = debugPanel.scrollHeight;
    }
}

// Usage examples
debug('Scanning media files...', 'info');
debug('Found 12 MOV files', 'success');
debug('FFmpeg command: ' + command, 'debug');
debug('Conversion failed: ' + error, 'error');
```

### 11.2 Backend Logging

#### Python Logging Configuration
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logger for media converter
logger = logging.getLogger('media_converter')
logger.setLevel(logging.DEBUG)

# File handler (rotating, max 10MB, keep 5 backups)
file_handler = RotatingFileHandler(
    'logs/media_converter.log',
    maxBytes=10*1024*1024,
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
```

#### Logging Points
- **File Scanning**: Log each file found, scan duration, total files
- **File Validation**: Log validation results, errors
- **Conversion Start**: Log job ID, file paths, settings
- **FFmpeg Commands**: Log full FFmpeg command for debugging
- **FFmpeg Output**: Capture and log stderr/stdout from FFmpeg
- **Progress Updates**: Log progress percentage, current file
- **Conversion Complete**: Log output size, compression ratio, duration
- **Errors**: Log full error traceback, file paths, settings
- **Path Operations**: Log all path validations and generations

#### Example Log Output
```
2024-01-15 10:30:45 - media_converter - INFO - Starting media file scan
2024-01-15 10:30:46 - media_converter - DEBUG - Scanning: /input/folder1
2024-01-15 10:30:47 - media_converter - INFO - Found 12 MOV files, 47 JPG files
2024-01-15 10:31:00 - media_converter - INFO - Starting conversion job: job_abc123
2024-01-15 10:31:00 - media_converter - DEBUG - Converting: /input/video1.mov
2024-01-15 10:31:00 - media_converter - DEBUG - FFmpeg command: ffmpeg -i input.mov -c:v libx264 ...
2024-01-15 10:31:15 - media_converter - INFO - Conversion complete: video1.mp4 (245MB -> 98MB, 60% reduction)
2024-01-15 10:31:20 - media_converter - ERROR - Conversion failed: video2.mov - FFmpeg error: Invalid codec
```

### 11.3 Error Debugging

#### Error Information to Log
- **File Path**: Full path of file being processed
- **Error Type**: Exception class name
- **Error Message**: Full error message
- **Stack Trace**: Complete traceback
- **Context**: Settings used, job ID, user actions
- **System Info**: FFmpeg version, available disk space, memory

#### Error Response Format
```python
{
    "success": False,
    "error": "Conversion failed",
    "error_type": "FFmpegError",
    "error_message": "Invalid codec: unsupported_video_codec",
    "file_path": "/input/video1.mov",
    "job_id": "job_abc123",
    "debug_info": {
        "ffmpeg_command": "ffmpeg -i ...",
        "ffmpeg_stderr": "...",
        "settings": {...}
    }
}
```

### 11.4 Debug Mode Toggle

#### Configuration
```python
# config.py
DEBUG_MODE = True  # Enable detailed debugging
DEBUG_LOG_LEVEL = 'DEBUG'  # DEBUG, INFO, WARNING, ERROR
DEBUG_CONSOLE_OUTPUT = True  # Show debug in browser console
DEBUG_UI_PANEL = True  # Show debug panel in UI
```

#### Frontend Debug Panel
- Toggle visibility (show/hide)
- Clear logs button
- Filter by log level (INFO, SUCCESS, ERROR, DEBUG, WARNING)
- Export logs button (download as text file)
- Auto-scroll to latest log entry

---

## 12. Selenium Testing Requirements

### 12.1 Test Structure

#### Test File Organization
```
tests/
├── conftest.py                    # Shared fixtures (existing)
├── test_media_converter.py        # Main media converter tests
├── test_media_converter_ui.py    # UI interaction tests
├── test_media_converter_workflow.py  # End-to-end workflow tests
└── reports/
    └── media_converter_report.html  # Test reports
```

### 12.2 Test Fixtures (Extend Existing)

#### Additional Fixtures in `conftest.py`
```python
@pytest.fixture
def media_converter_url(base_url):
    """URL for media converter page"""
    return f"{base_url}/v2p-formatter/media-converter"

@pytest.fixture
def test_media_files():
    """Create test media files for conversion"""
    # Create test MOV and JPG files in input folder
    # Return list of file paths
    pass

@pytest.fixture(autouse=True)
def cleanup_converted_files():
    """Cleanup converted files after each test"""
    yield
    # Remove converted files from output folder
    pass
```

### 12.3 Test Scenarios

#### Test File: `test_media_converter.py`

**Test Class 1: File Scanning & Display**
```python
class TestMediaFileScanning:
    """Test file scanning and display functionality"""
    
    def test_scan_media_files(self, driver, media_converter_url, wait):
        """Test that media files are scanned and displayed"""
        # Navigate to media converter page
        # Wait for file scan to complete
        # Verify MOV files section appears
        # Verify JPG/PNG files section appears
        # Verify file counts are correct
        # Verify file paths are displayed
    
    def test_file_search_filter(self, driver, media_converter_url, wait):
        """Test file search/filter functionality"""
        # Enter search term
        # Verify only matching files are shown
        # Clear search
        # Verify all files are shown again
    
    def test_collapsible_sections(self, driver, media_converter_url, wait):
        """Test collapsible file type sections"""
        # Click collapse button for video section
        # Verify section collapses
        # Click expand button
        # Verify section expands
    
    def test_select_all_files(self, driver, media_converter_url, wait):
        """Test select all functionality"""
        # Click "Select All Videos"
        # Verify all video files are selected
        # Click "Select All Images"
        # Verify all image files are selected
        # Verify selection summary updates
```

**Test Class 2: File Selection**
```python
class TestFileSelection:
    """Test file selection functionality"""
    
    def test_select_individual_file(self, driver, media_converter_url, wait):
        """Test selecting individual files"""
        # Click checkbox on a file
        # Verify file is selected
        # Verify selection summary updates
    
    def test_deselect_file(self, driver, media_converter_url, wait):
        """Test deselecting files"""
        # Select a file
        # Deselect the file
        # Verify file is deselected
        # Verify selection summary updates
    
    def test_clear_selection(self, driver, media_converter_url, wait):
        """Test clear selection button"""
        # Select multiple files
        # Click "Clear Selection"
        # Verify all files are deselected
```

**Test Class 3: Conversion Settings**
```python
class TestConversionSettings:
    """Test conversion settings configuration"""
    
    def test_video_quality_preset(self, driver, media_converter_url, wait):
        """Test video quality preset selection"""
        # Select video files
        # Change quality preset to "Low"
        # Verify preset is selected
        # Change to "Medium"
        # Verify preset is selected
        # Change to "High"
        # Verify preset is selected
    
    def test_video_custom_settings(self, driver, media_converter_url, wait):
        """Test video custom settings"""
        # Select "Custom" quality preset
        # Verify custom settings inputs appear
        # Enter bitrate value
        # Select codec
        # Verify settings are saved
    
    def test_image_resolution_preset(self, driver, media_converter_url, wait):
        """Test image resolution preset selection"""
        # Select image files
        # Change resolution preset
        # Verify preset is selected
    
    def test_image_custom_resolution(self, driver, media_converter_url, wait):
        """Test image custom resolution"""
        # Select "Custom" resolution
        # Enter width and height
        # Toggle "Maintain Aspect Ratio"
        # Verify settings are saved
    
    def test_image_quality_preset(self, driver, media_converter_url, wait):
        """Test image quality preset"""
        # Select quality preset
        # Verify preset is selected
        # Select "Custom"
        # Adjust quality slider
        # Verify value updates
```

#### Test File: `test_media_converter_workflow.py`

**Test Class: Complete Workflow**
```python
class TestMediaConverterWorkflow:
    """Test complete conversion workflows"""
    
    def test_convert_single_video(self, driver, media_converter_url, wait, test_media_files):
        """Test converting a single MOV file to MP4"""
        # Navigate to media converter
        # Wait for files to load
        # Select a MOV file
        # Select quality preset (e.g., "Medium")
        # Click "Start Conversion"
        # Wait for conversion to complete
        # Verify progress updates
        # Verify success message
        # Verify converted file exists in output
        # Verify file size reduction
    
    def test_convert_single_image(self, driver, media_converter_url, wait, test_media_files):
        """Test converting a single JPG file"""
        # Select a JPG file
        # Select resolution preset
        # Select quality preset
        # Start conversion
        # Wait for completion
        # Verify converted file exists
        # Verify file size reduction
    
    def test_convert_multiple_videos(self, driver, media_converter_url, wait, test_media_files):
        """Test batch video conversion"""
        # Select multiple MOV files
        # Select quality preset
        # Start conversion
        # Monitor progress for all files
        # Verify all files are converted
        # Verify all output files exist
    
    def test_convert_multiple_images(self, driver, media_converter_url, wait, test_media_files):
        """Test batch image conversion"""
        # Select multiple JPG files
        # Select resolution and quality
        # Start conversion
        # Monitor progress
        # Verify all conversions complete
    
    def test_convert_videos_and_images_simultaneously(self, driver, media_converter_url, wait, test_media_files):
        """Test converting videos and images at the same time"""
        # Select both video and image files
        # Configure video settings
        # Configure image settings
        # Start conversion
        # Monitor progress for both types
        # Verify all conversions complete
    
    def test_conversion_progress_tracking(self, driver, media_converter_url, wait, test_media_files):
        """Test progress tracking during conversion"""
        # Start conversion
        # Verify progress bar updates
        # Verify individual file status updates
        # Verify overall progress percentage
        # Verify completion status
    
    def test_preview_converted_file(self, driver, media_converter_url, wait, test_media_files):
        """Test preview functionality"""
        # Complete a conversion
        # Click preview button
        # Verify preview modal opens
        # Verify file is displayed (video player or image)
        # Close preview modal
    
    def test_download_converted_file(self, driver, media_converter_url, wait, test_media_files):
        """Test downloading converted files"""
        # Complete a conversion
        # Click download link
        # Verify file download starts
        # Verify downloaded file exists
    
    def test_cancel_conversion(self, driver, media_converter_url, wait, test_media_files):
        """Test canceling a conversion"""
        # Start conversion
        # Click cancel button
        # Verify conversion stops
        # Verify cancel message appears
        # Verify partial files are cleaned up
```

#### Test File: `test_media_converter_ui.py`

**Test Class: UI Elements**
```python
class TestMediaConverterUI:
    """Test UI elements and interactions"""
    
    def test_tab_navigation(self, driver, base_url, wait):
        """Test tab navigation between modules"""
        # Navigate to main app
        # Click "Media Converter" tab
        # Verify media converter page loads
        # Click "Video to Image" tab
        # Verify main page loads
    
    def test_dark_theme_consistency(self, driver, media_converter_url, wait):
        """Test dark theme is applied consistently"""
        # Navigate to media converter
        # Verify background colors match dark theme
        # Verify text colors are light
        # Verify buttons match dark theme
        # Verify file cards match dark theme
    
    def test_responsive_layout(self, driver, media_converter_url, wait):
        """Test responsive layout on different screen sizes"""
        # Set window size to mobile (375x667)
        # Verify layout adapts
        # Set window size to tablet (768x1024)
        # Verify layout adapts
        # Set window size to desktop (1920x1080)
        # Verify layout is optimal
    
    def test_empty_state_messages(self, driver, media_converter_url, wait):
        """Test empty state messages"""
        # Clear input folder (or use empty test folder)
        # Navigate to media converter
        # Verify "No media files found" message appears
    
    def test_loading_states(self, driver, media_converter_url, wait):
        """Test loading indicators"""
        # Navigate to page
        # Verify "Scanning files..." message appears
        # Wait for files to load
        # Verify loading message disappears
```

### 12.4 Error Handling Tests

**Test Class: Error Scenarios**
```python
class TestMediaConverterErrors:
    """Test error handling scenarios"""
    
    def test_corrupted_file_error(self, driver, media_converter_url, wait):
        """Test handling corrupted files"""
        # Select a corrupted MOV file
        # Start conversion
        # Verify error message appears
        # Verify conversion stops
        # Verify error is logged in debug panel
    
    def test_ffmpeg_not_installed_error(self, driver, media_converter_url, wait):
        """Test FFmpeg not installed error"""
        # Mock FFmpeg not found
        # Start conversion
        # Verify clear error message appears
        # Verify installation instructions shown
    
    def test_insufficient_disk_space(self, driver, media_converter_url, wait):
        """Test insufficient disk space error"""
        # Mock low disk space
        # Start conversion
        # Verify error message appears
        # Verify conversion stops
    
    def test_duplicate_file_handling(self, driver, media_converter_url, wait, test_media_files):
        """Test duplicate file name handling"""
        # Convert a file
        # Convert same file again
        # Verify suffix is added (_1, _2, etc.)
        # Verify both files exist in output
```

### 12.5 Test Data Setup

#### Test Media Files
- **Location**: `tests/test_data/`
- **Files Needed**:
  - `test_video.mov` - Small test video (5-10 seconds, ~10MB)
  - `test_image.jpg` - Test JPG image (~1MB)
  - `test_image.png` - Test PNG image (~1MB)
  - `corrupted.mov` - Corrupted video file for error testing

#### Test Helper Functions
```python
# tests/helpers.py
def create_test_media_files(input_folder):
    """Create test media files in input folder"""
    pass

def cleanup_test_files(output_folder):
    """Clean up test output files"""
    pass

def get_test_file_path(filename):
    """Get path to test file"""
    pass
```

### 12.6 Test Execution

#### Running Tests
```bash
# Run all media converter tests
pytest tests/test_media_converter*.py -v

# Run specific test file
pytest tests/test_media_converter.py -v

# Run specific test class
pytest tests/test_media_converter.py::TestMediaFileScanning -v

# Run with HTML report
pytest tests/test_media_converter*.py \
    -v \
    --html=tests/reports/media_converter_report.html \
    --self-contained-html

# Run in headless mode
HEADLESS=true pytest tests/test_media_converter*.py -v
```

#### Test Script
```bash
#!/bin/bash
# tests/run_media_converter_tests.sh

echo "=========================================="
echo "Running Media Converter Selenium Tests"
echo "=========================================="

cd "$(dirname "$0")/.."
source venv/bin/activate

mkdir -p tests/reports

pytest tests/test_media_converter*.py \
    -v \
    --html=tests/reports/media_converter_report.html \
    --self-contained-html \
    --capture=no \
    -s

echo ""
echo "📊 Test report: tests/reports/media_converter_report.html"
```

### 12.7 Test Coverage Requirements

#### Minimum Coverage
- **File Scanning**: 100% (all scenarios)
- **File Selection**: 100% (individual, bulk, clear)
- **Settings Configuration**: 100% (all presets, custom)
- **Conversion Workflow**: 80% (main scenarios)
- **Error Handling**: 80% (common errors)
- **UI Elements**: 70% (critical elements)

#### Test Checklist
- [ ] File scanning and display
- [ ] File search/filter
- [ ] File selection (individual, bulk, clear)
- [ ] Collapsible sections
- [ ] Video quality presets
- [ ] Video custom settings
- [ ] Image resolution presets
- [ ] Image custom resolution
- [ ] Image quality presets
- [ ] Single video conversion
- [ ] Single image conversion
- [ ] Batch video conversion
- [ ] Batch image conversion
- [ ] Simultaneous video and image conversion
- [ ] Progress tracking
- [ ] Preview functionality
- [ ] Download functionality
- [ ] Cancel conversion
- [ ] Tab navigation
- [ ] Dark theme consistency
- [ ] Error handling (corrupted files, FFmpeg errors, etc.)
- [ ] Duplicate file handling
- [ ] Empty state messages
- [ ] Loading states

---

## 13. Testing Requirements (Original Section - Now Expanded Above)

### 13.1 Unit Tests
- File scanning functionality
- Path generation and validation
- Video conversion logic
- Image conversion logic
- Duplicate file handling

### 13.2 Integration Tests
- End-to-end conversion workflow
- Batch processing
- Error handling
- File organization

### 13.3 Manual Testing Checklist
- [ ] Scan and display MOV files
- [ ] Scan and display JPG/PNG files
- [ ] Select files (individual and bulk)
- [ ] Apply conversion settings
- [ ] Start conversion job
- [ ] Monitor progress
- [ ] View results
- [ ] Preview converted files
- [ ] Download converted files
- [ ] Handle duplicate files
- [ ] Preserve subfolder structure
- [ ] Error handling (corrupted files, etc.)
- [ ] Cancel conversion
- [ ] Dark theme consistency

---

## 14. Error Scenarios & Handling

### 12.1 File Validation Errors
- **Corrupted file**: Validate before conversion, show error, stop batch
- **Unsupported codec**: Check codec support, show error message
- **File too large**: No limit, but log warning if >1GB

### 12.2 Conversion Errors
- **FFmpeg failure**: Capture stderr, display error, stop batch
- **Pillow failure**: Capture exception, display error, stop batch
- **Disk space**: Check available space, show error if insufficient

### 12.3 System Errors
- **FFmpeg not installed**: Show clear error message with installation instructions
- **Permission denied**: Check file permissions, show error
- **Path traversal attempt**: Reject and log security warning

---

## 15. Security Considerations

### 13.1 Path Validation
- Always validate input paths are within `INPUT_FOLDER`
- Always validate output paths are within `OUTPUT_FOLDER`
- Prevent path traversal (`../` attacks)

### 13.2 File Type Validation
- Verify file extensions match actual file types
- Validate file headers (magic numbers) before processing

### 13.3 Resource Limits
- Set timeout for conversions (1 hour max)
- Limit concurrent conversions (2 at a time)
- Monitor memory usage

---

## 16. Future Enhancements (Out of Scope for MVP)

- Support for additional video formats (AVI, MKV, M4V)
- Support for additional image formats (BMP, TIFF)
- Metadata preservation (EXIF, creation dates)
- Conversion history/logs
- Test conversion/preview before full conversion
- Delete original files after conversion
- Advanced codec options (H.265/HEVC)
- Custom FFmpeg filter chains

---

## 17. Notes & Considerations

- **File Size Reduction**: Primary goal - all presets should reduce file size
- **Quality Balance**: Find balance between size reduction and acceptable quality
- **Performance**: Parallel processing for efficiency, but limit concurrency
- **User Experience**: Clear progress indicators, error messages, and results
- **Consistency**: Follow existing app patterns (dark theme, file structure, etc.)
- **Debugging**: Comprehensive logging for troubleshooting

---

## Appendix A: FFmpeg Command Examples

### Low Quality (Maximum Compression)
```bash
ffmpeg -i input.mov \
  -c:v libx264 \
  -b:v 500k \
  -crf 28 \
  -preset fast \
  -vf scale=1280:720 \
  -c:a aac \
  -b:a 128k \
  -y output.mp4
```

### Medium Quality (Balanced)
```bash
ffmpeg -i input.mov \
  -c:v libx264 \
  -b:v 1000k \
  -crf 23 \
  -preset medium \
  -vf scale=1920:1080 \
  -c:a aac \
  -b:a 128k \
  -y output.mp4
```

### High Quality (Minimal Compression)
```bash
ffmpeg -i input.mov \
  -c:v libx264 \
  -b:v 2000k \
  -crf 18 \
  -preset slow \
  -c:a aac \
  -b:a 128k \
  -y output.mp4
```

---

## Appendix B: Image Conversion Examples

### Resize with Aspect Ratio
```python
from PIL import Image

img = Image.open('input.jpg')
img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
img.save('output.jpg', 'JPEG', quality=80)
```

### Resize with Stretching
```python
img = Image.open('input.jpg')
img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
img.save('output.jpg', 'JPEG', quality=80)
```

---

---

## 18. Approval & Sign-off

### 18.1 Approval Status
✅ **APPROVED FOR DEVELOPMENT**

### 18.2 Approval Criteria Met
- ✅ All requirements clarified and documented
- ✅ UI/UX wireframes approved
- ✅ Technical architecture defined
- ✅ Debugging requirements specified
- ✅ Selenium test specifications complete
- ✅ Error handling scenarios documented
- ✅ Security considerations addressed

### 18.3 Development Readiness
- **Backend Architecture**: Defined and ready
- **Frontend Design**: Wireframes approved
- **Testing Strategy**: Comprehensive Selenium tests specified
- **Debugging Strategy**: Logging and debug output defined
- **Dependencies**: Identified and documented
- **File Organization**: Structure and paths defined

### 18.4 Next Steps
1. Begin Phase 1 implementation (Core Infrastructure)
2. Set up debugging and logging infrastructure
3. Create Selenium test framework for media converter
4. Implement file scanning functionality
5. Implement basic conversion functionality
6. Add UI components and interactions
7. Integrate with existing application

---

**End of Specification**

