# Image to PDF Module - Specification

## Overview
Create a new "Image to PDF" module that allows users to select images from a qualification/learner folder structure, configure output settings, and generate PDF/DOCX documents with image filenames displayed below each image.

## Feature Goals
- Enable selection of multiple images simultaneously (bulk selection)
- Display images organized by subfolders (collapsed by default)
- Generate PDF/DOCX documents with images and their filenames
- Maintain consistent UI/UX with existing Video to Image module
- Support single image selection (backward compatibility)

---

## User Interface Requirements

### Navigation
**Add new tab to navigation:**
- Tab name: "Image to PDF"
- Route: `/v2p-formatter/image-to-pdf`
- Styling: Same as other navigation tabs (dark theme)

---

### 1. Qualification/Learner Selection Section

**Layout (same as Video to Image):**
```
┌─────────────────────────────────────────────────────────────┐
│ Qualification/Learner Selection                              │
├─────────────────────────────────────────────────────────────┤
│ Select Qualification: [Dropdown ▼]  Select Learner: [Dropdown ▼]  [🔄 Refresh] │
└─────────────────────────────────────────────────────────────┘
```

**Behavior:**
- Same as Video to Image module
- Qualification dropdown loads from OUTPUT_FOLDER
- Learner dropdown loads based on selected qualification
- Refresh button reloads file list

---

### 2. Image Selection Section

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ 1. Select Images                                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ Mode: [☐] Bulk Selection Mode                          │ │
│ │                                                         │ │
│ │ (Visible in bulk mode:)                                │ │
│ │ [☐] Select All                                         │ │
│ │                                                         │ │
│ │ [5] image(s) selected                                  │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ File Tree (with subfolders)                            │ │
│ │                                                         │ │
│ │ ▶ 📁 subfolder1 (15 images)                            │ │
│ │ ▶ 📁 subfolder2 (8 images)                             │ │
│ │ ▶ 📁 subfolder3 (3 images)                             │ │
│ │                                                         │ │
│ │ (When expanded:)                                        │ │
│ │ ▼ 📁 subfolder1 (15 images)                            │ │
│ │   ├─ [☐] image1.jpg                                    │ │
│ │   ├─ [☐] image2.jpg                                    │ │
│ │   ├─ [☐] image3.jpg                                    │ │
│ │   └─ ...                                                │ │
│ │                                                         │ │
│ │ Direct images (in root folder):                         │ │
│ │ ├─ [☐] root_image1.jpg                                 │ │
│ │ ├─ [☐] root_image2.jpg                                 │ │
│ │ └─ ...                                                  │ │
│ └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Key Features:**

##### 2.1 Bulk Selection Controls
- **Mode Toggle**: Checkbox to enable/disable "Bulk Selection Mode"
- **Select All Checkbox**: (Visible only in bulk mode) Selects/deselects all visible images
- **Selection Counter Badge**: Shows "X image(s) selected" (visible only in bulk mode)

##### 2.2 Folder Structure Display
- **Subfolders displayed first** (at the top)
- **Collapsed by default** (▶ icon, click to expand to ▼)
- Folder header shows: `▶ 📁 folder_name (X images)`
- When expanded, shows checkboxes and image names
- **Root folder images** displayed after subfolders (if any)

##### 2.3 Image Display
**In Single Mode:**
- Click image/name to select it immediately
- Selected image highlighted

**In Bulk Mode:**
- Checkbox visible next to each image name
- Click checkbox or image name to toggle selection
- Selected images show checkmark (✓) and highlighted background
- Visual indicators: border color change, background highlight

##### 2.4 Selection-Based Ordering (Simplified)
**Order Organizer Feature:**
- **Selection order determines sequence**: Images are assigned sequence numbers (1, 2, 3, 4, 5...) based on the order they are selected/checked
- **No drag-and-drop**: Simply tick/check images to build the sequence
- Order determines sequence in output PDF/DOCX document
- Available in bulk selection mode only

**Visual Indicators:**
- **Sequence Numbers**: Each selected image displays its sequence number (1, 2, 3...) prominently
- **Selection Order**: The order in which images are checked determines their sequence
- **Visual Grid**: Images displayed in a 3-column grid layout for easy viewing

**Ordering Behavior:**
- **First selected image** = Sequence 1
- **Second selected image** = Sequence 2
- **Third selected image** = Sequence 3
- And so on...
- When an image is deselected, remaining images are renumbered automatically
- Sequence numbers are displayed clearly on each selected image thumbnail

**Order Preservation:**
- Order is stored in selection array: `window.appData.selectedImages` (ordered array by selection order)
- Order persists when:
  - Expanding/collapsing folders
  - Re-selecting images (they maintain their sequence if already selected)
- Order is sent to backend in `generate_image_documents` endpoint as ordered array

**Thumbnail Display:**
- **Layout**: 3-column grid (3 thumbnails per row)
- **Size**: Large thumbnails for better preview
- **Quality**: 100% quality thumbnails for sharp, clear previews
- **Sequence Display**: Sequence number (1, 2, 3...) displayed prominently on each selected image

##### 2.5 Supported Image Formats
**Question 1: Which image formats should be supported?**
- Options:
  - All common formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.tiff`
  - Specific formats only (please specify)
  - **Recommended**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp` (most common) - Yes

---

### 3. Output Settings Section

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ 3. Output Settings                                          │
│                                                              │
│ (In bulk mode:)                                             │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ 📦 Batch Mode: These settings will apply to all       │ │
│ │    selected images.                                    │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                              │
│ Image Settings:                                             │
│ ├─ Quality: [━━━━━━━━━━━━━━━━━━━━━━━━] 95                 │ │
│ └─ Max Size: [640x480 ▼]                                  │ │
│                                                              │
│ Output Format:                                              │
│ ├─ Format: [Both (PDF + DOCX) ▼]                          │ │
│ ├─ Layout: [Grid ▼]                                       │ │
│ └─ Images per Page: [2 ▼]                                 │ │
│                                                              │
│ [Generate Documents] Button                                 │
└─────────────────────────────────────────────────────────────┘
```

**Settings (same as Video to Image):**
- **Quality Slider**: 1-100 (default: 95)
- **Max Size Dropdown**: 
  - Original
  - 1920x1080
  - 1280x720
  - 640x480 (default)
  - Custom (with width/height inputs)
- **Output Format**: 
  - Both (PDF + DOCX) - default
  - PDF Only
  - DOCX Only
- **Layout** (for PDF):
  - Grid (default)
  - Custom
- **Images per Page** (for PDF):
  - 1, 2, 4, 6, 9, 12 (default: 2)

**Questions:**
- **Question 2**: Should image quality/resize settings apply to images before they're added to PDF/DOCX? (Yes - recommended for consistency with Video to Image) - YES
- **Question 3**: Should we support custom layouts like Video to Image? (Yes - recommended for consistency) 

---

### 4. Image Processing & Document Generation

**Workflow:**
1. User selects qualification and learner
2. Images load from `OUTPUT_FOLDER/{qualification}/{learner}/` and subfolders
3. User selects images (single or bulk)
4. User configures output settings
5. User clicks "Generate Documents"
6. System processes images and generates PDF/DOCX

**Image Display in Output Documents:**
- Images arranged in grid layout (based on "Images per Page" setting)
- **Image filename displayed below each image** (centered, same as Video to Image)
- Filename format: Original filename without extension (e.g., "image1.jpg" → "image1")
- Font styling for filenames: Consistent with Video to Image module

**Questions:**
- **Question 4**: Should filenames show with or without extension?
  - **Recommended**: Without extension (e.g., "image1.jpg" → "image1")
- **Question 5**: Should we preserve folder structure in the document? 
  - Option A: Flatten all images into one document (recommended)
  - Option B: Group images by folder with section headers
  - **Recommended**: Option A (flatten) for simplicity
- **Question 6**: Should images be ordered by:
  - Filename (alphabetical) - recommended
  - Folder structure (subfolders first, then root) - recommended
  - Selection order (as selected by user)
  - **Recommended**: Folder structure (subfolders first, then alphabetical within each) - **UPDATED: User can override with selection-based ordering**

---

## Technical Implementation

### Backend Changes

#### New Route
- **Route**: `/v2p-formatter/image-to-pdf`
- **Method**: GET
- **Template**: `templates/image_to_pdf.html`
- **Functionality**: 
  - Loads qualifications and learners from OUTPUT_FOLDER
  - Renders the image selection interface

#### New API Endpoints

##### 1. List Images
- **Endpoint**: `GET /v2p-formatter/list_images`
- **Parameters**: 
  - `qualification` (required): Qualification name
  - `learner` (required): Learner name
- **Response**:
```json
{
  "success": true,
  "files": [
    {
      "name": "image1.jpg",
      "path": "/full/path/to/image1.jpg",
      "relative_path": "subfolder1/image1.jpg",
      "folder": "subfolder1",
      "size": 1234567
    },
    {
      "name": "image2.jpg",
      "path": "/full/path/to/image2.jpg",
      "relative_path": "image2.jpg",
      "folder": "root",
      "size": 2345678
    }
  ]
}
```

**Question 7**: Should we scan recursively into subfolders?
- **Recommended**: Yes, scan all subfolders recursively

##### 2. Generate Image PDF/DOCX
- **Endpoint**: `POST /v2p-formatter/generate_image_documents`
- **Parameters**:
```json
{
  "image_paths": ["/path/to/image1.jpg", "/path/to/image2.jpg", ...],
  "image_order": ["/path/to/image1.jpg", "/path/to/image2.jpg", ...], // Ordered array (same as image_paths if no reordering)
  "quality": 95,
  "max_width": 640,
  "max_height": 480,
  "output_format": "both", // "pdf", "docx", or "both"
  "layout": "grid", // "grid" or "custom"
  "images_per_page": 2
}
```
- **Note**: `image_order` array determines the sequence in output document. If not provided or empty, use `image_paths` order.
- **Response**:
```json
{
  "success": true,
  "pdf_path": "/path/to/output.pdf", // if PDF requested
  "docx_path": "/path/to/output.docx", // if DOCX requested
  "file_path": "/path/to/output.pdf" // primary file path
}
```

**Question 8**: Should images be processed sequentially or in parallel?
- **Recommended**: Sequential (simpler, consistent with Video to Image bulk processing)

##### 3. Batch Image Info (for bulk mode)
- **Endpoint**: `POST /v2p-formatter/batch_image_info`
- **Parameters**: 
```json
{
  "image_paths": ["/path/to/image1.jpg", ...]
}
```
- **Response**: Image dimensions, file size, format for each image

**Question 9**: Do we need batch image info endpoint, or can we use existing image processing?
- **Recommended**: Yes, useful for displaying image info before generation

---

### Frontend Changes

#### New Template
- **File**: `templates/image_to_pdf.html`
- **Structure**: Similar to `templates/index.html` but for images
- **Sections**:
  1. Navigation tabs (includes new "Image to PDF" tab)
  2. Qualification/Learner selection
  3. Image selection (with bulk mode)
  4. Output settings
  5. Generate documents button

#### JavaScript Functions (similar to Video to Image)
- `renderImageList(files)` - Render image list with folders
- `toggleBulkMode()` - Toggle bulk selection mode
- `toggleImageSelection(imagePath)` - Toggle single image selection
- `toggleSelectAll()` - Select/deselect all images
- `updateSelectionUI()` - Update UI when selection changes
- `processBulkImageGeneration()` - Process multiple images
- `processSingleImageGeneration()` - Process single image
- `generateImageDocuments()` - Main generation function
- **Selection-Based Ordering Functions:**
  - `toggleImageSelection(path, name)` - Toggle selection and assign sequence number
  - `updateSequenceNumbers()` - Update sequence numbers for all selected images (1, 2, 3...)
  - `resetOrder()` - Reset to folder/alphabetical order

#### Folder Rendering Logic
- **Folders first**: Sort and display subfolders before root images
- **Collapsed by default**: All folders start collapsed (▶ icon)
- **Expand/collapse**: Click folder header to toggle
- **Root images**: Display after all folders, directly in root

**Question 10**: Should we show image thumbnails/previews in the file tree?
- Option A: Yes, show thumbnails (better UX, more complex)
- Option B: No, just filenames (simpler, faster loading)
- **Approved**: Option A - Show thumbnails in 3-column grid layout, 100% quality (240x180 size)

---

### Backend Image Processing

#### Image Processing Functions
- **Resize images** (if max_size specified)
- **Quality adjustment** (JPEG quality)
- **Format conversion** (if needed)

#### PDF Generation
- Use same library as Video to Image (ReportLab or similar)
- Grid layout support (2, 4, 6, 9 images per page)
- Image filename below each image (centered, styled)
- Maintain aspect ratios

#### DOCX Generation
- Use same library as Video to Image (python-docx)
- Table layout (2 columns for grid layout)
- Image filename below each image (centered, styled)
- Maintain aspect ratios

**Question 11**: Should we reuse existing PDF/DOCX generation code from Video to Image module?
- **Recommended**: Yes, adapt existing code for images instead of video frames

---

## User Flow Examples

### Example 1: Single Image Selection
1. User selects "Deco" qualification → "lubins" learner
2. Images load from folder structure
3. User clicks on "image1.jpg" in "subfolder1"
4. Image selected (highlighted)
5. User configures output settings
6. User clicks "Generate Documents"
7. PDF/DOCX generated with single image and its filename

### Example 2: Bulk Selection - All Images from One Folder
1. User selects "Deco" qualification → "lubins" learner
2. Images load, folders shown collapsed
3. User enables "Bulk Selection Mode"
4. User expands "subfolder1" folder
5. User clicks "Select All" checkbox
6. All 15 images in subfolder1 are selected
7. User configures output settings (applies to all 15 images)
8. User clicks "Generate Documents"
9. Single PDF/DOCX generated with all 15 images and their filenames

### Example 3: Bulk Selection - Multiple Folders with Reordering
1. User selects qualification and learner
2. User enables bulk mode
3. User expands "subfolder1" and selects 5 images
4. User expands "subfolder2" and selects 3 images
5. User selects 2 images from root folder
6. Total: 10 images selected (shown in counter badge)
7. **User drags images to reorder:**
   - Drags "cover.jpg" (from root) to position 1
   - Drags "summary.jpg" (from root) to position 2
   - Drags selected images from subfolder1 and subfolder2 in desired order
8. User configures settings and generates documents
9. Single PDF/DOCX with all 10 images **in the order set by selection sequence (1, 2, 3...)**

---

## Edge Cases & Error Handling

### Edge Cases
1. **No images found**: Show message "No images found in selected folder"
2. **Empty folders**: Don't display empty folders in file tree
3. **Unsupported image format**: Show error message, skip that image
4. **Very large images**: Resize according to max_size setting
5. **Corrupted images**: Skip with error message, continue with others
6. **No selection**: Disable "Generate Documents" button until images selected
7. **Selection-Based Ordering Edge Cases:**
   - Deselecting images: Remaining images are automatically renumbered (sequence numbers update)
   - Reselecting previously selected images: Maintains position in sequence if already selected, or adds to end
   - "Reset Order" button: Resets to folder structure order (subfolders first, then alphabetical within each)
   - Selecting images across multiple folders: Sequence numbers assigned in order of selection, regardless of folder

### Error Messages
- "Please select at least one image"
- "No images found for selected qualification/learner"
- "Error processing image: [filename] - [error message]"
- "Failed to generate document: [error message]"

---

## Questions for Approval

1. **Image formats**: Which formats to support? (Recommended: jpg, jpeg, png, gif, webp)
2. **Image quality/resize**: Apply before PDF/DOCX generation? (Recommended: Yes)
3. **Custom layouts**: Support custom layouts? (Recommended: Yes)
4. **Filename display**: With or without extension? (Recommended: Without)
5. **Folder structure**: Flatten or group by folder? (Recommended: Flatten)
6. **Image ordering**: How to order images? (Recommended: Folder structure, then alphabetical)
7. **Recursive scanning**: Scan subfolders recursively? (Recommended: Yes)
8. **Processing**: Sequential or parallel? (Recommended: Sequential)
9. **Batch info endpoint**: Needed? (Recommended: Yes)
10. **Thumbnails**: Show thumbnails in file tree? (Approved: Yes - 3-column grid, 100% quality, 240x180 size)
11. **Code reuse**: Reuse PDF/DOCX generation code? (Recommended: Yes)
12. **Selection-based ordering**: Images are assigned sequence numbers (1, 2, 3...) based on selection order
    - **Approved**: Yes - Simplified approach, no drag-and-drop needed
    - **Approved**: Show sequence numbers prominently on selected images (circular badge)
    - **Implementation**: Sequence numbers automatically assigned when images are checked/selected

13. **Thumbnail layout**: Display images in grid format
    - **Approved**: 3-column grid layout (3 thumbnails per row)
    - **Approved**: Large thumbnails with 100% quality for clear previews

---

## Wireframes (Text-Based)

### Page Layout
```
┌────────────────────────────────────────────────────────────────────────────┐
│ Navigation Tabs                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│ [Video to Image] [Media Converter] [AC Matrix] [Observation Media]        │
│ [Observation Report] [Image to PDF] ← NEW                                  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ Qualification/Learner Selection                                            │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ Select Qualification: [Deco ▼]  Select Learner: [lubins ▼]  [🔄 Refresh] │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ 1. Select Images                                                           │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ Mode: [☑] Bulk Selection Mode                                        │ │
│ │ [☐] Select All                                                         │ │
│ │                                                                        │ │
│ │ [10] image(s) selected                                                │ │
│ │ [Reset to Default Order]  Sequences: 1, 2, 3... (by selection order) │ │
│ ├───────────────────────────────────────────────────────────────────────┤ │
│ │                                                                        │ │
│ │ ▶ 📁 session1 (12 images)                                             │ │
│ │ ▶ 📁 session2 (8 images)                                              │ │
│ │ ▶ 📁 misc (3 images)                                                  │ │
│ │                                                                        │ │
│ │ Direct images:                                                         │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                  │ │
│ │ │      ┌─────┐ │ │      ┌─────┐ │ │      ┌─────┐ │                  │ │
│ │ │      │ [☐] │ │ │      │ [☑] │ │ │      │ [☐] │ │                  │ │
│ │ │      └─────┘ │ │      └─────┘ │ │      └─────┘ │                  │ │
│ │ │  ┌────────┐  │ │  ┌────────┐  │ │  ┌────────┐  │                  │ │
│ │ │  │        │  │ │  │        │  │ │  │        │  │                  │ │
│ │ │  │ Thumb  │  │ │  │ Thumb  │  │ │  │ Thumb  │  │                  │ │
│ │ │  │        │  │ │  │        │  │ │  │        │  │                  │ │
│ │ │  └────────┘  │ │  └────────┘  │ │  └────────┘  │                  │ │
│ │ │           [1]│ │           [2]│ │              │                  │ │
│ │ │ cover.jpg    │ │ summary.jpg  │ │ image3.jpg   │                  │ │
│ │ │ (2.5 MB)     │ │ (1.8 MB)     │ │ (3.2 MB)     │                  │ │
│ │ └──────────────┘ └──────────────┘ └──────────────┘                  │ │
│ │                                                                        │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                  │ │
│ │ │ [☐]      [4] │ │ [☐]      [5] │ │ [☐]          │                  │ │
│ │ │  ┌────────┐  │ │  ┌────────┐  │ │  ┌────────┐  │                  │ │
│ │ │  │        │  │ │  │        │  │ │  │        │  │                  │ │
│ │ │  │ Thumb  │  │ │  │ Thumb  │  │ │  │ Thumb  │  │                  │ │
│ │ │  │        │  │ │  │        │  │ │  │        │  │                  │ │
│ │ │  └────────┘  │ │  └────────┘  │ │  └────────┘  │                  │ │
│ │ │ image4.jpg   │ │ image5.jpg   │ │ image6.jpg   │                  │ │
│ │ │ (2.1 MB)     │ │ (2.9 MB)     │ │ (1.5 MB)     │                  │ │
│ │ └──────────────┘ └──────────────┘ └──────────────┘                  │ │
│ │                                                                        │ │
│ │ (When folder expanded - 3-column grid:)                                │ │
│ │ ▼ 📁 session1 (12 images)                                             │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                  │ │
│ │ │      ┌─────┐ │ │      ┌─────┐ │ │      ┌─────┐ │                  │ │
│ │ │      │ [☑] │ │ │      │ [☑] │ │ │      │ [☐] │ │                  │ │
│ │ │      └─────┘ │ │      └─────┘ │ │      └─────┘ │                  │ │
│ │ │  ┌────────┐  │ │  ┌────────┐  │ │  ┌────────┐  │                  │ │
│ │ │  │        │  │ │  │        │  │ │  │        │  │                  │ │
│ │ │  │ Thumb  │  │ │  │ Thumb  │  │ │  │ Thumb  │  │                  │ │
│ │ │  │        │  │ │  │        │  │ │  │        │  │                  │ │
│ │ │  └────────┘  │ │  └────────┘  │ │  └────────┘  │                  │ │
│ │ │           [1]│ │           [2]│ │              │                  │ │
│ │ │ IMG_001.jpg  │ │ IMG_002.jpg  │ │ IMG_003.jpg  │                  │ │
│ │ │ (3.5 MB)     │ │ (2.8 MB)     │ │ (4.1 MB)     │                  │ │
│ │ └──────────────┘ └──────────────┘ └──────────────┘                  │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                  │ │
│ │ │      ┌─────┐ │ │      ┌─────┐ │ │      ┌─────┐ │                  │ │
│ │ │      │ [☑] │ │ │      │ [☐] │ │ │      │ [☐] │ │                  │ │
│ │ │      └─────┘ │ │      └─────┘ │ │      └─────┘ │                  │ │
│ │ │  ┌────────┐  │ │  ┌────────┐  │ │  ┌────────┐  │                  │ │
│ │ │  │        │  │ │  │        │  │ │  │        │  │                  │ │
│ │ │  │ Thumb  │  │ │  │ Thumb  │  │ │  │ Thumb  │  │                  │ │
│ │ │  │        │  │ │  │        │  │ │  │        │  │                  │ │
│ │ │  └────────┘  │ │  └────────┘  │ │  └────────┘  │                  │ │
│ │ │           [3]│ │              │ │              │                  │ │
│ │ │ IMG_004.jpg  │ │ IMG_005.jpg  │ │ IMG_006.jpg  │                  │ │
│ │ │ (2.3 MB)     │ │ (3.7 MB)     │ │ (1.9 MB)     │                  │ │
│ │ └──────────────┘ └──────────────┘ └──────────────┘                  │ │
│ │ ... (continues in 3-column grid)                                     │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ 3. Output Settings                                                         │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ 📦 Batch Mode: These settings will apply to all selected images.     │ │
│ │                                                                        │ │
│ │ Image Settings:                                                        │ │
│ │ Quality: [━━━━━━━━━━━━━━━━━━━━━━━━] 95                                │ │
│ │ Max Size: [640x480 ▼]                                                 │ │
│ │                                                                        │ │
│ │ Output Format:                                                         │ │
│ │ Format: [Both (PDF + DOCX) ▼]                                         │ │
│ │ Layout: [Grid ▼]                                                      │ │
│ │ Images per Page: [2 ▼]                                                │ │
│ │                                                                        │ │
│ │ [Generate Documents]                                                   │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

### Output Document Layout (PDF/DOCX)
```
┌─────────────────────────────────────────────────────────────────────┐
│ PDF/DOCX Document                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ ┌──────────────┐  ┌──────────────┐                                 │
│ │              │  │              │                                 │
│ │   Image 1    │  │   Image 2    │                                 │
│ │              │  │              │                                 │
│ └──────────────┘  └──────────────┘                                 │
│     IMG_001          IMG_002                                        │
│                                                                      │
│ ┌──────────────┐  ┌──────────────┐                                 │
│ │              │  │              │                                 │
│ │   Image 3    │  │   Image 4    │                                 │
│ │              │  │              │                                 │
│ └──────────────┘  └──────────────┘                                 │
│     IMG_003          IMG_004                                        │
│                                                                      │
│ ... (continues)                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Stages

### Stage 1: Backend - Image Scanning & Listing
- [ ] Create image scanning function (similar to video scanning)
- [ ] Create `/list_images` endpoint
- [ ] Support subfolder structure
- [ ] Return image metadata (name, path, size, folder)

### Stage 2: Backend - Image Processing
- [ ] Create image resize/quality adjustment functions
- [ ] Create batch image info endpoint (if needed)
- [ ] Handle various image formats

### Stage 3: Backend - Document Generation
- [ ] Adapt PDF generation for images (reuse existing code)
- [ ] Adapt DOCX generation for images (reuse existing code)
- [ ] Add image filename below each image
- [ ] Support grid layouts
- [ ] **Use image_order array** from request to determine image sequence in output
- [ ] If image_order not provided, use image_paths order as fallback

### Stage 4: Frontend - Basic UI
- [ ] Create `templates/image_to_pdf.html`
- [ ] Add navigation tab
- [ ] Qualification/learner selection (reuse existing)
- [ ] Basic image list display

### Stage 5: Frontend - Folder Structure & Bulk Selection
- [ ] Implement folder rendering (collapsed by default)
- [ ] Implement bulk selection mode toggle
- [ ] Implement "Select All" functionality
- [ ] Add selection counter badge
- [ ] Visual indicators for selected images
  - [x] **Selection-Based Ordering:**
  - [x] Sequence number assignment on selection (1, 2, 3...)
  - [x] Display sequence numbers on selected images (circular badge)
  - [x] Auto-renumber when images deselected
  - [x] Reset order button functionality (reset to folder/alphabetical order)
  - [x] 3-column grid layout for thumbnails
  - [x] 100% quality thumbnails (240x180 size)

### Stage 6: Frontend - Document Generation
- [ ] Implement single image generation
- [ ] Implement bulk image generation
- [ ] Progress tracking for bulk processing
- [ ] Results display with download links

### Stage 7: Testing & Polish
- [ ] Test with various image formats
- [ ] Test bulk selection with many images
- [ ] Test folder structure display
- [ ] Test document generation (PDF and DOCX)
- [ ] Verify filename display below images

---

## Open Questions Requiring Approval

Please review the questions above (Questions 1-11) and provide answers/approvals so development can proceed.

---

## Notes

- This module should feel consistent with the Video to Image module
- Reuse existing code where possible (PDF/DOCX generation, UI patterns)
- Dark theme consistent with rest of application
- Mobile-responsive design
- Error handling should be user-friendly

