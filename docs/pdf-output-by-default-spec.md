# PDF Output by Default - Specification

## Overview
Modify the main Video to Image Formatter page (`/v2p-formatter/`) to automatically generate PDF output after frame extraction, similar to the Image to PDF module. The PDF generation should happen automatically without requiring a separate button click, and the results should display file path links and an Apple Preview link.

## Feature Goals
- Automatically generate PDF after successful frame extraction
- Display file path in results
- Provide link to open PDF in Apple Preview
- Provide download link for the PDF
- Maintain consistent UI/UX with Image to PDF module

---

## User Interface Requirements

### Current Flow (Before)
1. User selects video
2. User selects time points
3. User clicks "Extract Frames" → Frames extracted
4. User clicks "Generate PDF" → PDF generated
5. Results show download link only

### New Flow (After)
1. User selects video
2. User selects time points
3. User clicks "Extract Frames" → Frames extracted → **PDF automatically generated**
4. Results show:
   - Output folder path
   - File path
   - Link to open in Apple Preview
   - Download link

---

## Results Display Section

### Text Wireframe (Single PDF)

```
┌─────────────────────────────────────────────────────────────┐
│ Results Section                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ✅ PDF Generated Successfully!                              │
│                                                              │
│ Output Filename: video_name.pdf                             │
│                                                              │
│ Output Folder:                                               │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ /path/to/output/folder/qualification/learner          │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                              │
│ [📁 Open Output Folder]                                     │
│                                                              │
│ ─────────────────────────────────────────────────────────── │
│                                                              │
│ File Path: /path/to/output/.../video.pdf                    │
│ (clickable - opens Finder to file location)                  │
│                                                              │
│ PDF: 📄 Open PDF (opens in Apple Preview)                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Text Wireframe (Bulk PDFs)

```
┌─────────────────────────────────────────────────────────────┐
│ Results Section                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ✅ 3 PDFs Generated Successfully!                            │
│                                                              │
│ PDF 1 of 3                                                   │
│ ─────────────────────────────────────────────────────────── │
│ Output Filename: video1_name.pdf                            │
│                                                              │
│ Output Folder:                                               │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ /path/to/output/folder/qualification/learner          │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                              │
│ [📁 Open Output Folder]                                     │
│                                                              │
│ ─────────────────────────────────────────────────────────── │
│                                                              │
│ File Path: /path/to/output/.../video1.pdf                   │
│ (clickable - opens Finder to file location)                  │
│                                                              │
│ PDF: 📄 Open PDF (opens in Apple Preview)                   │
│                                                              │
│ ─────────────────────────────────────────────────────────── │
│                                                              │
│ PDF 2 of 3                                                   │
│ ─────────────────────────────────────────────────────────── │
│ Output Filename: video2_name.pdf                            │
│ ...                                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Visual Wireframe (ASCII Art - Single PDF)

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  ✅ PDF Generated Successfully!                             │
│                                                              │
│  Output Filename: video_name.pdf                            │
│                                                              │
│  Output Folder:                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ /Users/rom/Documents/nvq/v2p-formatter-output/       │  │
│  │   Qualification1/Learner1                            │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  [📁 Open Output Folder]                                    │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  File Path: /Users/rom/.../Learner1/video_name.pdf          │
│  (clickable link - opens Finder to file location)           │
│                                                              │
│  PDF: 📄 Open PDF (opens in Apple Preview)                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Visual Wireframe (ASCII Art - Bulk PDFs)

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  ✅ 3 PDFs Generated Successfully!                          │
│                                                              │
│  PDF 1 of 3                                                  │
│  ────────────────────────────────────────────────────────  │
│  Output Filename: video1_name.pdf                            │
│                                                              │
│  Output Folder:                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ /Users/rom/Documents/nvq/v2p-formatter-output/       │  │
│  │   Qualification1/Learner1                            │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  [📁 Open Output Folder]                                    │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  File Path: /Users/rom/.../Learner1/video1_name.pdf         │
│  (clickable link - opens Finder to file location)           │
│                                                              │
│  PDF: 📄 Open PDF (opens in Apple Preview)                  │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  PDF 2 of 3                                                  │
│  ────────────────────────────────────────────────────────  │
│  Output Filename: video2_name.pdf                            │
│  ...                                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### HTML Structure

```html
<div style="padding: 20px; background: #2a2a2a; border-radius: 6px; margin-top: 20px;">
    <h3 style="color: #e0e0e0; margin-top: 0;">✅ PDF Generated Successfully!</h3>
    
    <!-- Output Folder Section -->
    <p style="margin-bottom: 15px;"><strong style="color: #e0e0e0;">Output Folder:</strong></p>
    <p style="margin-bottom: 15px; padding: 10px; background: #1e1e1e; border-radius: 4px; 
       word-break: break-all; font-family: monospace; color: #999; font-size: 12px;">
        {output_folder_path}
    </p>
    <p style="margin-bottom: 20px;">
        <a href="#" onclick="openFolderInFinder('{output_folder_path}'); return false;" 
           style="color: #667eea; text-decoration: underline; font-weight: 500; cursor: pointer;">
            📁 Open Output Folder
        </a>
    </p>
    <hr style="border: none; border-top: 1px solid #555; margin: 15px 0;">
    
    <!-- Output Filename Section -->
    <p style="color: #e0e0e0; margin-bottom: 15px;">
        <strong>Output Filename:</strong> 
        <span style="color: #999; font-family: monospace;">{filename}</span>
    </p>
    
    <!-- File Path Section (clickable to open Finder) -->
    <p style="color: #e0e0e0; margin-bottom: 10px;">
        <strong>File Path:</strong> 
        <a href="#" onclick="openFolderInFinder('{file_directory}'); return false;" 
           style="color: #667eea; text-decoration: underline; cursor: pointer;">
            {file_path}
        </a>
    </p>
    
    <!-- PDF Links Section -->
    <p style="color: #e0e0e0; margin-bottom: 10px;">
        <strong>PDF:</strong> 
        <a href="#" onclick="openFileInPreview('{pdf_relative_path}'); return false;" 
           style="color: #667eea; text-decoration: underline; cursor: pointer;">
            📄 Open PDF
        </a>
    </p>
</div>
```

---

## Technical Implementation

### Backend Changes

#### Route: `/v2p-formatter/generate_pdf`
**Updated Response Format:**
```json
{
    "success": true,
    "file_path": "/absolute/path/to/file.pdf",
    "pdf_path": "/absolute/path/to/file.pdf",
    "pdf_relative_path": "qualification/learner/file.pdf",
    "filename": "file.pdf",
    "output_folder_path": "/absolute/path/to/output/folder"
}
```

**Changes:**
- Added `pdf_relative_path` field (relative to OUTPUT_FOLDER)
- Added `output_folder_path` field (parent directory of PDF)

### Frontend Changes

#### Automatic PDF Generation
- Modify `extractFrames()` function to automatically call PDF generation after successful extraction
- Remove manual "Generate PDF" button requirement (keep button for manual regeneration if needed)

#### Results Display
- Create new `showPDFResults()` function to display:
  - Output Filename (displayed prominently)
  - Output folder path (with "Open Output Folder" link)
  - File path (clickable link that opens Finder to file location)
  - "Open PDF" link (opens in Apple Preview)
  - Support for bulk results (multiple PDFs) with numbered sections

#### Helper Functions
- Add `openFileInPreview(filePath)` function (calls `/v2p-formatter/open_file` endpoint)
- Add `openFolderInFinder(folderPath)` function (calls `/v2p-formatter/open_folder` endpoint)
- Add `escapeHtml(text)` utility function for safe HTML rendering

---

## User Experience Flow

### Step-by-Step Process

1. **User selects video**
   - Selects qualification and learner
   - Selects video file from file tree

2. **User selects time points**
   - Uses video player to navigate
   - Adds time points using time selector

3. **User clicks "Extract Frames"**
   - Progress bar shows "Extracting frames..."
   - Frames are extracted to output folder
   - Progress bar updates to "Frames extracted successfully!"
   - **Automatically proceeds to PDF generation**

4. **PDF Generation (Automatic)**
   - Progress bar shows "Generating PDF..."
   - PDF is created from extracted frames
   - Progress bar updates to "PDF generated successfully!"

5. **Results Display**
   - Results section appears with:
     - Success message (or count for bulk operations)
     - Output Filename (name of generated PDF)
     - Output folder path (clickable to open in Finder)
     - File path (clickable link that opens Finder to file location)
     - "Open PDF" link (opens PDF in macOS Preview)
     - For bulk operations: numbered sections for each PDF (PDF 1 of N, PDF 2 of N, etc.)

---

## API Endpoints Used

### Existing Endpoints
- `POST /v2p-formatter/extract_frames` - Extract frames from video
- `POST /v2p-formatter/generate_pdf` - Generate PDF from images
- `POST /v2p-formatter/open_file` - Open file in macOS Preview
- `POST /v2p-formatter/open_folder` - Open folder in macOS Finder
- `GET /v2p-formatter/download?path={path}` - Download file

---

## Styling Guidelines

### Colors
- Background: `#2a2a2a` (dark gray)
- Text: `#e0e0e0` (light gray)
- Links: `#667eea` (purple/blue)
- Code/Paths: `#999` (medium gray) on `#1e1e1e` background
- Borders: `#555` (medium gray)

### Typography
- Headings: Bold, `#e0e0e0`
- Body text: `#e0e0e0`
- File paths: Monospace, `12px`, `#999`
- Links: Underlined, `#667eea`

### Spacing
- Section padding: `20px`
- Paragraph margin: `10px-15px`
- List item margin: `8px`

---

## Testing Checklist

- [ ] Frame extraction triggers automatic PDF generation
- [ ] PDF generation completes successfully
- [ ] Results display shows output folder path
- [ ] Results display shows file path
- [ ] "Open Output Folder" link opens Finder correctly
- [ ] "Open in Apple Preview" link opens PDF in Preview
- [ ] Download link downloads PDF correctly
- [ ] Error handling works if PDF generation fails
- [ ] Progress indicators show correctly during extraction and generation
- [ ] UI matches Image to PDF module styling

---

## Notes

- The manual "Generate PDF" button should still be available for regeneration if needed
- The automatic PDF generation uses default layout settings (grid, 4 images per page)
- File paths are displayed in monospace font for readability
- All file operations are validated to ensure paths are within OUTPUT_FOLDER for security

