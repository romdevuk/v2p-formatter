# Video to Image Formatter - Final Technical Specification

## 1. Project Overview

### 1.1 Purpose
A web-based application that converts MP4 video files to JPEG image sequences and generates PDF documents containing those images. Users can select specific time points from videos to extract frames, configure image quality, and customize PDF layouts.

### 1.2 MVP Scope
- Single video upload and processing
- Time point selection for frame extraction
- Image quality/resolution configuration
- Basic image editing (crop, resize, filters)
- PDF generation with configurable layouts
- Local file storage in same directory as source video

### 1.3 Architecture Principles
- **Flexible & Extensible**: Modular design allowing easy addition of features
- **MVP Approach**: Core functionality first, expandable later
- **Stability First**: Synchronous processing for reliability
- **Single User**: No authentication or multi-user features required

## 2. Technology Stack

### 2.1 Backend
- **Framework**: Flask (Python 3.8+)
- **Video Processing**: OpenCV (cv2) or FFmpeg-python
- **Image Processing**: Pillow (PIL)
- **PDF Generation**: ReportLab or fpdf2
- **File Handling**: Python standard library (os, pathlib, shutil)

### 2.2 Frontend
- **HTML/CSS/JavaScript**: Vanilla JS for MVP (can be upgraded to framework later)
- **UI Components**: Custom components for video player, timeline, image preview
- **Styling**: CSS3 with modern, responsive design

### 2.3 Development Environment
- **Python Version**: 3.8 or higher
- **Package Management**: pip with requirements.txt
- **Development Server**: Flask development server
- **URL Base**: `localhost/v2p-formatter`

## 3. Application Architecture

### 3.1 Project Structure
```
v2p-formatter/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── routes.py                # Route handlers
│   ├── video_processor.py      # Video to image conversion
│   ├── pdf_generator.py         # PDF creation logic
│   ├── image_editor.py          # Image editing utilities
│   └── utils.py                 # Helper functions
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js              # Main application logic
│   │   ├── video-handler.js     # Video upload/preview
│   │   ├── timeline.js          # Time selection interface
│   │   └── image-preview.js     # Frame preview
│   └── uploads/                 # Temporary upload storage
├── templates/
│   ├── base.html
│   └── index.html               # Main interface
├── requirements.txt
├── config.py                    # Configuration settings
└── README.md
```

### 3.2 Core Modules

#### 3.2.1 Video Processor (`video_processor.py`)
**Responsibilities:**
- Extract frames at specified time points
- Convert frames to JPEG format
- Handle video metadata extraction (duration, resolution)
- Save images with sequential naming (1.jpg, 2.jpg, ...)

**Key Functions:**
```python
def extract_frame(video_path, time_point, output_path, quality=95)
def get_video_info(video_path)
def extract_frames_at_times(video_path, time_points, output_dir, quality)
```

#### 3.2.2 PDF Generator (`pdf_generator.py`)
**Responsibilities:**
- Generate PDF with extracted images
- Support multiple layout options (grid, x images per page)
- Maintain aspect ratio
- A4 page size

**Key Functions:**
```python
def create_pdf(images, output_path, layout='grid', images_per_page=4)
def add_image_to_pdf(pdf, image_path, position, size)
```

#### 3.2.3 Image Editor (`image_editor.py`)
**Responsibilities:**
- Crop images
- Resize images
- Apply filters
- Adjust quality/resolution

**Key Functions:**
```python
def crop_image(image_path, x, y, width, height)
def resize_image(image_path, width, height, maintain_aspect=True)
def apply_filter(image_path, filter_type)
def adjust_quality(image_path, quality, output_path)
```

## 4. User Interface Specification

### 4.1 Main Page Layout
1. **Video Upload Section**
   - File input for MP4 selection
   - Drag-and-drop zone
   - File validation feedback
   - Video preview player

2. **Video Information Display**
   - Video duration (in seconds)
   - Video resolution
   - File size

3. **Time Selection Interface**
   - Text input examples for time points:
     - Single time: `30` (extract frame at 30 seconds)
     - Multiple times: `10, 25, 45, 60` (comma-separated)
     - Range: `10-20` (extract frames at 10, 11, 12...20 seconds)
   - Visual timeline scrubber (optional enhancement)
   - Frame preview area showing selected frames

4. **Image Configuration Section**
   - Quality slider (1-100)
   - Resolution dropdown:
     - Original
     - 1920x1080
     - 1280x720
     - 640x480
   - Image editing options (crop, resize, filters)

5. **PDF Configuration Section**
   - Layout options:
     - Grid (2x2, 3x3, 4x4)
     - Images per page (1, 2, 4, 6, 9)
   - Preview option

6. **Processing Controls**
   - "Extract Frames" button
   - "Generate PDF" button
   - Progress indicator
   - Download links for output

### 4.2 User Flow
1. User uploads MP4 file
2. Video preview loads, duration/resolution displayed
3. User enters time points (e.g., "10, 25, 45, 60")
4. User previews frames at selected times
5. User configures image quality/resolution
6. User optionally edits images
7. User configures PDF layout
8. User clicks "Extract Frames" → images saved to folder
9. User clicks "Generate PDF" → PDF created
10. User downloads PDF and/or accesses image folder

## 5. Functional Requirements

### 5.1 Video Upload & Validation
- **FR-1**: Accept MP4 files only
- **FR-2**: Validate file extension before upload
- **FR-3**: Support any file size (no limits)
- **FR-4**: Display video preview in browser
- **FR-5**: Extract and display video metadata (duration, resolution)

### 5.2 Time Point Selection
- **FR-6**: Accept time points in seconds format
- **FR-7**: Support multiple input formats:
  - Single: `30`
  - Multiple: `10, 25, 45, 60`
  - Range: `10-20` (continuous)
- **FR-8**: Validate time points are within video duration
- **FR-9**: Preview frames at selected time points before extraction
- **FR-10**: Only support continuous time ranges (no gaps)

### 5.3 Frame Extraction
- **FR-11**: Extract frames at exact time points specified
- **FR-12**: Save images as JPEG format
- **FR-13**: Name images sequentially: 1.jpg, 2.jpg, 3.jpg, ...
- **FR-14**: Save images in folder named after video file (without extension)
- **FR-15**: Create folder in same directory as source video
- **FR-16**: Preserve original video file

### 5.4 Image Configuration
- **FR-17**: Allow quality adjustment (1-100)
- **FR-18**: Provide resolution options (original, preset sizes)
- **FR-19**: Support image editing:
  - Crop
  - Resize
  - Basic filters

### 5.5 PDF Generation
- **FR-20**: Generate PDF with extracted images
- **FR-21**: Support layout options:
  - Grid layouts (2x2, 3x3, 4x4)
  - Custom images per page (1, 2, 4, 6, 9)
- **FR-22**: Use A4 page size
- **FR-23**: Maintain image aspect ratio
- **FR-24**: No headers, footers, or captions
- **FR-25**: Name PDF after video file (e.g., `video.mp4` → `video.pdf`)
- **FR-26**: Save PDF in same directory as video

### 5.6 Processing & Feedback
- **FR-27**: Display progress indicators during processing
- **FR-28**: Show processing status messages
- **FR-29**: Handle errors gracefully with debugging information
- **FR-30**: Provide download links for generated files

## 6. Technical Implementation Details

### 6.1 Video Processing
**Library Choice**: OpenCV (cv2) - stable and well-documented

**Frame Extraction Logic:**
```python
# Pseudocode
1. Load video using cv2.VideoCapture
2. For each time point:
   a. Set video position to time_point
   b. Read frame
   c. Convert BGR to RGB if needed
   d. Apply quality/resolution settings
   e. Save as JPEG with sequential number
3. Close video capture
```

### 6.2 PDF Generation
**Library Choice**: ReportLab - flexible and supports image layouts

**PDF Layout Logic:**
- Calculate image size based on page size (A4) and layout
- Maintain aspect ratio when scaling
- Position images according to grid or custom layout
- Add images sequentially to PDF pages

### 6.3 File Management
- **Upload Storage**: Temporary storage in `static/uploads/` during processing
- **Output Location**: Same directory as source video file
- **Folder Naming**: `{video_filename}_frames/` for images
- **PDF Naming**: `{video_filename}.pdf`

### 6.4 Error Handling
- **Invalid Files**: Return error message with debugging info
- **Time Validation**: Prevent selection outside video duration
- **Processing Errors**: Log errors, display user-friendly messages
- **File System Errors**: Handle permissions, disk space issues

### 6.5 Processing Mode
**Synchronous Processing**: 
- Most stable approach for MVP
- Simpler error handling
- Direct feedback to user
- Can be upgraded to async later if needed

## 7. Configuration

### 7.1 Application Config (`config.py`)
```python
UPLOAD_FOLDER = 'static/uploads'
MAX_CONTENT_LENGTH = None  # No limit
ALLOWED_EXTENSIONS = {'mp4'}
DEFAULT_IMAGE_QUALITY = 95
DEFAULT_RESOLUTION = 'original'
DEFAULT_PDF_LAYOUT = 'grid'
DEFAULT_IMAGES_PER_PAGE = 4
PDF_PAGE_SIZE = 'A4'
```

## 8. Dependencies

### 8.1 Python Packages
```
Flask==2.3.0
opencv-python==4.8.0.74
Pillow==10.0.0
reportlab==4.0.4
numpy==1.24.3
```

## 9. Future Expansion Points

### 9.1 Architecture Flexibility
- **Modular Design**: Each processor (video, image, PDF) is separate module
- **Plugin System**: Easy to add new image formats, filters, layouts
- **Configuration-Driven**: Settings in config file for easy customization
- **API-Ready**: Structure allows adding REST API layer later if needed

### 9.2 Potential Enhancements
- Multiple video batch processing
- Additional image formats (PNG, WebP)
- Advanced image editing (brightness, contrast, saturation)
- Custom PDF templates
- Video format support expansion
- Cloud storage integration
- User authentication and history
- Async processing for large files

## 10. Testing Strategy (MVP)

### 10.1 Manual Testing
- Upload various MP4 file sizes
- Test time point selection formats
- Verify image extraction accuracy
- Test PDF generation with different layouts
- Validate error handling

### 10.2 Test Cases
1. Valid MP4 upload → video preview loads
2. Invalid file type → error message shown
3. Time points within duration → frames extracted
4. Time points outside duration → validation error
5. Image quality settings → output matches settings
6. PDF generation → PDF created with correct layout
7. File organization → files saved in correct locations

## 11. Deployment

### 11.1 Local Development
```bash
# Setup
pip install -r requirements.txt
python app/__init__.py

# Access
http://localhost:5000/v2p-formatter
```

### 11.2 Production Considerations (Future)
- WSGI server (Gunicorn)
- Reverse proxy (Nginx)
- Environment variables for configuration
- Logging setup
- Error monitoring

## 12. Security Considerations

### 12.1 MVP Security
- File type validation (MP4 only)
- File size monitoring (optional)
- Sanitize file names
- Prevent path traversal attacks
- Secure file upload handling

## 13. Performance Considerations

### 13.1 MVP Performance
- Synchronous processing (stable, simple)
- Progress indicators for user feedback
- Efficient video frame extraction
- Optimized image compression
- Memory management for large videos

## 14. Documentation Requirements

### 14.1 Code Documentation
- Docstrings for all functions
- Module-level documentation
- Inline comments for complex logic

### 14.2 User Documentation
- README with setup instructions
- Usage guide for time point selection
- Configuration options explanation

---

## Approval Checklist

- [ ] Architecture aligns with requirements
- [ ] Technology stack approved
- [ ] UI/UX flow acceptable
- [ ] Feature scope appropriate for MVP
- [ ] Expansion points identified
- [ ] Implementation approach clear

---

**Document Version**: 1.0  
**Date**: 2024  
**Status**: Ready for Review

