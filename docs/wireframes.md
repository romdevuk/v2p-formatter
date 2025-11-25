# Video to Image Formatter - Interface Wireframes

## Overview
This document describes the user interface design for the Video to Image Formatter application. The interface is organized into sequential steps that guide users through the video processing workflow.

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────┐
│  MAIN CONTENT AREA                                           │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  STEP 1: SELECT VIDEO                                 │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  File Tree (Auto-loaded)                        │ │ │
│  │  │  ┌───────────────────────────────────────────┐   │ │ │
│  │  │  │ 📁 css/L2 Cladding                       │   │ │ │
│  │  │  │   └─ 📁 eduards bormanis                 │   │ │ │
│  │  │  │      └─ 📁 mp4                            │   │ │ │
│  │  │  │         🎬 IMG_7560.mp4 (12.5 MB)        │   │ │ │
│  │  │  │         🎬 intro.mp4 (8.2 MB)            │   │ │ │
│  │  │  │  📁 cob/L2 Interior                       │   │ │ │
│  │  │  │   └─ ...                                  │   │ │ │
│  │  │  └───────────────────────────────────────────┘   │ │ │
│  │  │  [Files organized by folder structure]           │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  STEP 2: SELECT TIME POINTS FROM VIDEO                 │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  [Video Player with Timeline]                   │ │ │
│  │  │  ┌───────────────────────────────────────────┐   │ │ │
│  │  │  │                                           │   │ │ │
│  │  │  │         Video Player Area                  │   │ │ │
│  │  │  │         (User can scroll/scrub video)      │   │ │ │
│  │  │  │                                           │   │ │ │
│  │  │  └───────────────────────────────────────────┘   │ │ │
│  │  │  [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━]    │ │ │
│  │  │  Timeline: 0:00 ──────────────────────── 0:32    │ │ │
│  │  │                                                  │ │ │
│  │  │  Selected Time Points:                           │ │ │
│  │  │  [5.2s] [10.5s] [15.8s] [20.3s]                 │ │ │
│  │  │  [+ Add Current Time] Button                     │ │ │
│  │  │  [Clear All] Button                              │ │ │
│  │  │                                                  │ │ │
│  │  │  Duration: 32.19s | Resolution: 640x480          │ │ │
│  │  │  FPS: 29.98 | Filename: IMG_7560.mp4            │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  STEP 3: OUTPUT SETTINGS                                │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  Image Settings:                                 │ │ │
│  │  │  Quality: [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] 95 │ │ │
│  │  │  Resolution: [Dropdown: Original ▼]            │ │ │
│  │  │    • Original                                   │ │ │
│  │  │    • 1920x1080                                  │ │ │
│  │  │    • 1280x720                                   │ │ │
│  │  │    • 640x480                                    │ │ │
│  │  │                                                  │ │ │
│  │  │  PDF Settings:                                  │ │ │
│  │  │  Layout: [Dropdown: Grid ▼]                     │ │ │
│  │  │    • Grid                                        │ │ │
│  │  │    • Custom                                     │ │ │
│  │  │                                                  │ │ │
│  │  │  Images per Page: [Dropdown: 4 ▼]              │ │ │
│  │  │    • 1                                           │ │ │
│  │  │    • 4                                           │ │ │
│  │  │    • 6                                           │ │ │
│  │  │    • 9                                           │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  STEP 4: PROCESS                                        │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  [Extract Frames] Button                        │ │ │
│  │  │                                                  │ │ │
│  │  │  Progress Bar:                                  │ │ │
│  │  │  [████████████████████░░░░░░░░] 60%            │ │ │
│  │  │  Extracting frames...                           │ │ │
│  │  │                                                  │ │ │
│  │  │  Results:                                       │ │ │
│  │  │  ✅ Frames extracted successfully!              │ │ │
│  │  │  [Generate PDF] Button                          │ │ │
│  │  │                                                  │ │ │
│  │  │  ✅ PDF generated successfully!                 │ │ │
│  │  │  [Download PDF] Link                            │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

---

## Step-by-Step Interface Description

### Step 1: Select Video

**Layout:**
- **Title**: "1. Select Video"
- **File Tree Container**: 
  - Automatically loads and displays all MP4 files from **Input Folder** (`/Users/rom/Documents/nvq/v2p-formatter-input`)
  - Files organized in a hierarchical folder structure
  - Each folder can be expanded/collapsed by clicking
  - Each file shows: 🎬 icon, filename, file size in MB
  - Files are clickable to select
- **Info Note**: 
  - "All generated files will be saved to: `/Users/rom/Documents/nvq/v2p-formatter-output`"

**Behavior:**
- Files load automatically when page opens
- Loading indicator shows "Scanning input directory for MP4 files..."
- Once loaded, file tree is visible with all folders and files
- Clicking a file selects it and proceeds to Step 2
- All output files (images and PDFs) will be created in the **Output Folder**

**Visual Elements:**
- Folder icon: 📁 (closed) / 📂 (open)
- File icon: 🎬
- File size displayed in parentheses: (12.5 MB)
- Hover effect on files (background color change)
- Scrollable container (max-height: 500px)

---

### Step 2: Select Time Points from Video

**Layout:**
- **Title**: "2. Select Time Points from Video"
- **Video Player**: HTML5 video element with full controls and timeline
- **Timeline**: Visual timeline showing current position and duration
- **Selected Time Points Display**: Shows all selected time points as chips/badges
- **Add Time Button**: "+ Add Current Time" button to add current video position
- **Clear All Button**: Button to clear all selected time points
- **Video Info Panel**: 
  - Duration: X.XXs
  - Resolution: WIDTHxHEIGHT
  - FPS: X.XX
  - Filename: filename.mp4

**Behavior:**
- Section appears after file selection
- Video loads automatically from selected file
- User can play/pause/seek video using standard HTML5 video controls
- User can scrub timeline by clicking/dragging on progress bar
- User can use keyboard shortcuts (spacebar to play/pause, arrow keys to seek)
- Click "+ Add Current Time" to capture current video position as time point
- Selected time points appear as removable chips/badges below video
- Each chip shows time in seconds (e.g., "5.20s")
- User can remove individual time points by clicking X on chip
- User can clear all time points with "Clear All" button
- Time points are automatically sorted in ascending order
- Video info displays below player (duration, resolution, FPS, filename)

---

### Step 3: Output Settings

**Layout:**
- **Title**: "3. Output Settings"
- **Image Settings Section**:
  - **Quality Slider**: Range slider (1-100), default 95
  - **Resolution Dropdown**: 
    - Original
    - 1920x1080
    - 1280x720
    - 640x480
- **PDF Settings Section**:
  - **Layout Dropdown**: Grid / Custom
  - **Images per Page Dropdown**: 1, 4, 6, 9

**Behavior:**
- Quality value updates as slider moves
- Resolution selection affects output image size
- Layout selection affects PDF arrangement
- Images per page determines grid layout
- All settings apply to output generation

---

### Step 4: Process

**Layout:**
- **Title**: "4. Process"
- **Extract Frames Button**: Primary action button
- **Progress Bar**: Shows extraction progress
- **Results Area**: Displays success/error messages
- **Generate PDF Button**: Appears after frames extracted
- **Download Link**: Appears after PDF generated

**Behavior:**
- Click "Extract Frames" to start processing
- Progress bar shows percentage and status text
- Results area shows success message and file count
- "Generate PDF" button appears after successful extraction
- Click "Generate PDF" to create PDF
- Download link appears after PDF generation
- Click link to download PDF file

---

## Visual Design Elements

### Colors
- **Primary**: Purple gradient (#667eea to #764ba2)
- **Background**: White for content areas, gradient background for page
- **Borders**: Light gray (#ddd)
- **Text**: Dark gray (#333) for body text
- **Success**: Green for success messages
- **Error**: Red for error messages
- **Time Point Chips**: Purple (#667eea) background, white text

### Typography
- **Section Titles**: Medium, bold, dark text (h2 elements)
- **Body**: Regular weight, readable size
- **Time Point Chips**: Medium weight, white text on colored background
- **File Names**: Monospace font for file tree

### Spacing
- **Section Gap**: 30px between sections
- **Padding**: 20-30px inside containers
- **Border Radius**: 6-12px for rounded corners
- **Margins**: Consistent spacing throughout

### Interactive Elements
- **Buttons**: 
  - Primary: Purple gradient, white text, rounded corners
  - Secondary: Light background, dark text
  - Hover: Slight darkening/lightening
- **Input Fields**: 
  - White background, border, rounded corners
  - Focus: Border color change
- **File Items**: 
  - Hover: Light blue background (#e8f0fe)
  - Cursor: Pointer
- **Folders**: 
  - Clickable header
  - Expand/collapse animation
- **Time Point Chips**:
  - Purple background (#667eea), white text
  - Hover: Darker purple (#764ba2)
  - Clickable to remove (X icon)
  - Rounded corners (20px border-radius)
- **Video Player**:
  - Full HTML5 video controls
  - Timeline scrubbable
  - Responsive sizing

---

## Responsive Design

### Desktop (Default)
- Full width layout
- All sections visible in sequence
- File tree: 500px max height, scrollable
- Video player: Responsive width

### Mobile (Future)
- Stacked sections
- Smaller file tree
- Touch-friendly buttons
- Simplified navigation

---

## User Flow

1. **Page Loads** 
   - No header displayed
   - Files automatically load and display in file tree
   - Loading indicator shows "Scanning directories for MP4 files..."

2. **User Clicks File** 
   - Video loads with full HTML5 player controls
   - Video info displays (duration, resolution, FPS, filename)
   - Step 2 section becomes visible

3. **User Scrolls/Scrubs Video** 
   - User plays video or scrubs timeline to find desired frames
   - Video player shows current time position
   - User can pause at any moment

4. **User Adds Time Points** 
   - User clicks "+ Add Current Time" button at desired moments
   - Time point added to selected list (displayed as chip)
   - User can add multiple time points
   - User can remove individual time points by clicking X on chip
   - User can clear all with "Clear All" button

5. **User Configures Output Settings** 
   - Adjusts image quality slider (1-100)
   - Selects resolution from dropdown
   - Selects PDF layout (Grid/Custom)
   - Selects images per page (1, 4, 6, 9)

6. **User Clicks Extract Frames** 
   - Processing starts
   - Progress bar shows extraction progress
   - Selected time points sent to backend

7. **Frames Extracted** 
   - Success message displayed
   - Number of frames extracted shown
   - "Generate PDF" button appears

8. **User Clicks Generate PDF** 
   - PDF generation starts
   - Progress indicator shows
   - PDF created with selected settings

9. **PDF Ready** 
   - Success message displayed
   - Download link appears
   - PDF saved in **Output Folder**: `/Users/rom/Documents/nvq/v2p-formatter-output/{video_name}.pdf`
   - Images saved in: `/Users/rom/Documents/nvq/v2p-formatter-output/{video_name}_frames/`

10. **User Downloads PDF** 
    - Click download link
    - PDF file downloads from output folder
    - Process complete
    - All files remain in output folder for future access

---

## Accessibility Considerations

- **Keyboard Navigation**: All interactive elements accessible via keyboard
- **Screen Readers**: Proper ARIA labels and semantic HTML
- **Color Contrast**: WCAG AA compliant
- **Focus Indicators**: Visible focus states for all interactive elements
- **Alt Text**: Icons and images have descriptive text

---

## Technical Implementation Notes

- **Input/Output Architecture**:
  - **Input Folder**: `/Users/rom/Documents/nvq/v2p-formatter-input` - Source folder for MP4 files
  - **Output Folder**: `/Users/rom/Documents/nvq/v2p-formatter-output` - All generated files saved here
  - Video files are read from input folder (not copied)
  - All extracted images and PDFs are created in output folder
  - Output structure: `{output_folder}/{video_name}_frames/` for images, `{output_folder}/{video_name}.pdf` for PDFs

- **File Tree**: 
  - Rendered via JavaScript (`file-selector.js`)
  - Automatically loads on page load
  - Organized by folder structure from **Input Folder**
  - Files scanned server-side via `/v2p-formatter/list_files` endpoint
  
- **Video Player**: 
  - HTML5 video element with full controls
  - Video served via Flask route `/v2p-formatter/video_file?path=...`
  - User can play, pause, seek, and scrub timeline
  
- **Time Point Selection**:
  - Managed by `time-selector.js`
  - "+ Add Current Time" button captures `videoPlayer.currentTime`
  - Time points stored in `selectedTimePoints` array
  - Displayed as removable chips
  - Converted to comma-separated string for API calls
  
- **Output Settings**:
  - Combined Image and PDF settings in single section
  - Quality slider (1-100) with live value display
  - Resolution dropdown with presets
  - PDF layout and images-per-page options
  
- **Progress Updates**: Real-time via JavaScript fetch
- **File Downloads**: Direct download links to generated files
- **Error Handling**: User-friendly error messages with debugging info

---

## Approval Status

- [ ] Design approved
- [ ] Layout approved
- [ ] User flow approved
- [ ] Visual design approved
- [ ] Ready for implementation

**Notes for Approval:**
- Please review the wireframe and provide feedback
- Any changes to layout, flow, or design should be noted
- Once approved, implementation will proceed

---

**Document Version**: 2.0  
**Last Updated**: 2024-11-23  
**Author**: Development Team

## Change Log

### Version 2.0 (2024-11-23)
- Removed header section from layout
- Updated Step 2 to focus on video scrubbing and time point selection
- Merged Steps 4 & 5 into single "Output Settings" section (now Step 3)
- Updated step numbering: 1, 2, 3, 4 (was 1, 2, 3, 4, 5, 6)
- Added time point chip design specifications
- Updated user flow to reflect video scrubbing workflow
- Enhanced technical implementation notes

### Version 1.0 (2024-11-23)
- Initial wireframe document created

