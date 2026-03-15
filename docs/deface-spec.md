# Deface Module - Specification

## Overview
Create a new "Deface" module that allows users to select images and videos from a qualification/learner folder structure, anonymize faces using the deface tool, and generate PDF/DOCX documents with anonymized images/frames and filenames displayed below each image.

## Feature Goals
- Enable selection of multiple images and videos simultaneously (bulk selection)
- Display images and videos organized by subfolders (collapsed by default)
- Anonymize faces in images using the deface tool before generating documents
- For videos: Extract frames, anonymize faces in frames, then generate documents
- Generate PDF/DOCX documents with anonymized images/frames and their filenames
- **Always save standalone defaced files** (each defaced image and each defaced MP4 video) in the output folder in addition to merged PDF/DOCX
- Maintain consistent UI/UX with existing Image to PDF module
- Provide configurable face anonymization settings
- All output files use 'deface_' prefix

---

## User Interface Requirements

### Navigation
**Add new tab to navigation:**
- Tab name: "Deface"
- Route: `/v2p-formatter/deface`
- Styling: Same as other navigation tabs (dark theme)
- Position: After "Image to PDF" tab

---

### 1. Qualification/Learner Selection Section

**Layout (same as Image to PDF):**
```
┌─────────────────────────────────────────────────────────────┐
│ Qualification/Learner Selection                              │
├─────────────────────────────────────────────────────────────┤
│ Select Qualification: [Dropdown ▼]  Select Learner: [Dropdown ▼]  [🔄 Refresh] │
└─────────────────────────────────────────────────────────────┘
```

**Behavior:**
- Same as Image to PDF module
- Qualification dropdown loads from OUTPUT_FOLDER
- Learner dropdown loads based on selected qualification
- Refresh button reloads file list
- Source: `/v2p-formatter/image-to-pdf` (same as Image to PDF module)

---

### 2. Image/Video Selection Section

**Layout (same as Image to PDF, but includes videos):**
```
┌─────────────────────────────────────────────────────────────┐
│ 1. Select Images and Videos                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ [☐] Select All                                         │ │
│ │                                                         │ │
│ │ [5] image(s) selected                                  │ │
│ │ [Reset Selection]                                      │ │
│ │                                                         │ │
│ │ Sort by: [Name ▼]  Thumbnails per row: [3 ▼]  [⛶]    │ │
│ │                                                         │ │
│ │ [Reset to Default Order]  Sequences: 1, 2, 3...        │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ File Tree (with subfolders)                            │ │
│ │                                                         │ │
│ │ ▶ 📁 subfolder1 (15 images)                            │ │
│ │ ▶ 📁 subfolder2 (8 images)                             │ │
│ │                                                         │ │
│ │ Direct images (3-column grid):                         │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │ │
│ │ │ [☑]      [1] │ │ [☑]      [2] │ │ [☐]          │   │ │
│ │ │  ┌────────┐  │ │  ┌────────┐  │ │  ┌────────┐  │   │ │
│ │ │  │ Thumb  │  │ │  │ Thumb  │  │ │  │ Thumb  │  │   │ │
│ │ │  │        │  │ │  │        │  │ │  │        │  │   │ │
│ │ │  └────────┘  │ │  └────────┘  │ │  └────────┘  │   │ │
│ │ │ image1.jpg   │ │ image2.jpg   │ │ image3.jpg   │   │ │
│ │ │ (2.5 MB)     │ │ (1.8 MB)     │ │ (3.2 MB)     │   │ │
│ │ └──────────────┘ └──────────────┘ └──────────────┘   │ │
│ └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Key Features:**
- Same as Image to PDF module
- Bulk selection mode (always enabled)
- 3-column grid layout for thumbnails
- Sequence numbers (1, 2, 3...) based on selection order
- Folder structure display (subfolders first, then root)
- Uses `/v2p-formatter/list_images` endpoint (same as Image to PDF)

---

### 3. Output Settings Section

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ 2. Output Settings                                          │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ 📦 Batch Mode: These settings will apply to all       │ │
│ │    selected images.                                    │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                              │
│ Image Settings:                                             │
│ ├─ Quality: [━━━━━━━━━━━━━━━━━━━━━━━━] 95                 │
│ └─ Max Size: [640x480 ▼]                                  │
│                                                              │
│ Deface Settings:                                            │
│ ├─ Anonymization Method: [Blur ▼]                         │
│ │   Options: Blur, Solid (Black Box), Mosaic              │
│ │                                                          │
│ ├─ [☐] Use Rectangular Boxes                             │
│ │   (Use rectangular boxes instead of ellipses)           │
│ │                                                          │
│ ├─ Detection Threshold: [━━━━━━━━━━━━━━━━━━━━━━━━] 0.2   │
│ │   Range: 0.0 - 1.0 (Lower = more sensitive)             │
│ │                                                          │
│ ├─ Detection Scale (Optional): [Original Resolution ▼]    │
│ │   Options: Original, 640x360, 1280x720                  │
│ │   (Downscale for faster processing)                     │
│ │                                                          │
│ ├─ Mosaic Size: [━━━━━━━━━━━━━━━━━━━━━━━━] 20            │
│ │   Range: 5 - 50 pixels (only for mosaic method)         │
│ │                                                          │
│ └─ [☐] Show Detection Scores                              │
│     (Display face detection confidence scores)             │
│                                                              │
│ Video Processing:                                           │
│ └─ [☐] Approve Video Processing                            │
│     (Must be checked before processing videos)              │
│     (Videos will be saved as MP4 format)                    │
│                                                              │
│ Output Format:                                              │
│ ├─ Format: [PDF Only ▼]                                   │
│ │   Options: PDF Only, Both (PDF + DOCX), DOCX Only       │
│ │                                                          │
│ ├─ Layout: [Grid ▼]                                       │
│ │   Options: Grid, Custom                                 │
│ │                                                          │
│ └─ Images per Page: [2 ▼]                                 │
│     Options: 1, 2, 4, 6, 9, 12                            │
└─────────────────────────────────────────────────────────────┘
```

**Settings:**

##### 3.1 Image Settings (same as Image to PDF)
- **Quality Slider**: 1-100 (default: 95)
- **Max Size Dropdown**: 
  - Original
  - 1920x1080
  - 1280x720
  - 640x480 (default)

##### 3.2 Deface Settings (NEW)

**Anonymization Method:**
- **Blur** (default): Applies blur filter to detected faces (ellipse or rectangle)
- **Solid (Black Box)**: Covers faces with solid black boxes
- **Mosaic**: Applies mosaic pattern to faces

**Use Rectangular Boxes:**
- Checkbox option
- When enabled: Uses rectangular boxes instead of ellipses
- Recommended for solid/mosaic methods
- Default: unchecked (uses ellipses for blur)

**Detection Threshold:**
- Slider: 0.0 - 1.0 (default: 0.2)
- Lower values = more sensitive (detects more faces, may include false positives)
- Higher values = less sensitive (only high-confidence detections)
- Recommended default: 0.2

**Detection Scale (Optional):**
- Dropdown: Original Resolution, 640x360, 1280x720
- **Default when video is selected:** 640×360 (for faster video processing; output resolution unchanged)
- Downscales input for faster face detection processing; output quality remains same as input (detection only uses scale)
- Use for high-resolution images and all videos to improve performance
- Recommended: 640×360 for video (default when videos selected), Original only when maximum detection detail is needed

**Mosaic Size:**
- Slider: 5 - 50 pixels (default: 20)
- Only visible when "Anonymization Method" = "Mosaic"
- Controls size of mosaic tiles
- Larger values = bigger tiles (more pixelated)
- Smaller values = smaller tiles (less pixelated)

**Show Detection Scores:**
- Checkbox option
- When enabled: Displays face detection confidence scores (0.0-1.0) on image
- Useful for tuning detection threshold
- Default: unchecked

##### 3.3 Video Processing (NEW)
- **Approve Video Processing**: Checkbox option
  - Must be checked before videos can be processed
  - When enabled: Videos will be processed directly and saved as MP4 format
  - Videos are anonymized using deface tool and saved as MP4 files
  - Default: unchecked (user must explicitly approve video processing)
  - **Note**: Videos must be saved as MP4 format (not frames extracted to JPEG)

##### 3.3.1 Video deface: speed and robustness (for approval)
- **Full analysis and optimization spec:** [deface-video-optimization-spec.md](./deface-video-optimization-spec.md)
- **Summary:** Video conversion can be slow because deface runs face detection on every frame (CPU-bound unless GPU packages are installed). Main levers: (1) **Detection Scale** — use 640×360 (or 1280×720) for much faster processing with unchanged output resolution; (2) **Hardware acceleration** — install `onnx onnxruntime-gpu` (Nvidia) or equivalent in the same env as the app for GPU-accelerated inference; (3) optional preflight and clearer errors for robustness.
- **Proposed UX:** When the user has selected at least one video, default or suggest “Detection Scale” to 640×360. Document GPU install in README/Deface page for users who need faster runs.

- **Implemented:** (1) When the user selects at least one **video**, "Detection Scale" defaults to **640×360** for faster processing (output resolution unchanged). (2) Per-video timeout is configurable via `config.DEFACE_VIDEO_TIMEOUT` (default 600 s; override with env `DEFACE_VIDEO_TIMEOUT`). Timeout and deface/FFmpeg failures are mapped to short user-facing messages (e.g. "Processing timed out… Try a shorter video or use Detection Scale 640×360"; "Video may be corrupt or in an unsupported format"). (3) Optional parallel video processing: set `DEFACE_MAX_CONCURRENT_VIDEOS` (or env) to 2–4 to process that many videos at once; default 1 (sequential). (4) Deface page includes a **Help** section "How Deface works (optimised)" describing detection scale, GPU acceleration, and what to expect when optimised (see [deface-video-optimization-spec.md](./deface-video-optimization-spec.md)).

##### 3.4 Output Format (same as Image to PDF)
- **Format**: PDF Only (default), Both (PDF + DOCX), DOCX Only
- **Layout**: Grid (default), Custom
- **Images per Page**: 1, 2, 4, 6, 9, 12 (default: 2)

---

### 3. Apply Deface & Review Section

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ 3. Apply Deface & Review                                    │
│                                                              │
│ [Apply Deface] Button                                       │
│                                                              │
│ (During processing — staged progression:)                  │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ Processing Deface...                                   │ │
│ │ [████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░] 42%   │ │  ← overall bar moves (item count + per-item % from CLI)
│ │ Processing 0/1 — intro.mp4 (45s) — 23%                 │ │  ← status: elapsed 5s, 10s… then % when from deface; per-file if bulk
│ │ Estimate: images take a few seconds; each video 1–2 min │ │
│ │ ▼ Show detailed steps (live log)                       │ │
│ │   [23:08:55] [deface_video] 5_run | 23% 161/706 ...    │ │
│ │   [23:08:56] [deface_video] 5_run | still processing...│ │
│ └────────────────────────────────────────────────────────┘ │
│                                                              │
│ (After processing - Review Interface:)                      │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ ✅ Deface Applied Successfully                         │ │
│ │                                                         │ │
│ │ Review anonymized media files below:                   │ │
│ │                                                         │ │
│ │ Preview Grid (3-column):                               │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │ │
│ │ │ [☑]      [1] │ │ [☑]      [2] │ │ [☐]      [3] │   │ │
│ │ │  ┌────────┐  │ │  ┌────────┐  │ │  ┌────────┐  │   │ │
│ │ │  │ Defaced│  │ │  │ Defaced│  │ │  │ Defaced│  │   │ │
│ │ │  │ Image  │  │ │  │ Image  │  │ │  │ Image  │  │   │ │
│ │ │  │        │  │ │  │        │  │ │  │        │  │   │ │
│ │ │  └────────┘  │ │  └────────┘  │ │  └────────┘  │   │ │
│ │ │ image1.jpg   │ │ image2.jpg   │ │ image3.jpg   │   │ │
│ │ │ ✓ Defaced    │ │ ✓ Defaced    │ │ ✓ Defaced    │   │ │
│ │ │ [Edit]       │ │ [Edit]       │ │ [Edit]       │   │ │
│ │ └──────────────┘ └──────────────┘ └──────────────┘   │ │
│ │                                                         │ │
│ │ [Adjust Settings & Re-apply] Button                    │ │
│ │ [Accept & Proceed to Document Generation] Button      │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                              │
│ (When [Edit] clicked - Manual Deface Interface:)           │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ Manual Deface Editor - image1.jpg                      │ │
│ │                                                         │ │
│ │ ┌───────────────────────────────────────────────────┐ │ │
│ │ │                                                   │ │ │
│ │ │         [Full-size defaced image preview]        │ │ │
│ │ │         (Click to add deface area)                │ │ │
│ │ │                                                   │ │ │
│ │ │         [Existing deface areas shown]            │ │ │
│ │ │         [Click to add new deface area]           │ │ │
│ │ │                                                   │ │ │
│ │ └───────────────────────────────────────────────────┘ │ │
│ │                                                         │ │
│ │ Deface Shape: [Square ▼]  Size: [Medium ▼]            │ │
│ │   Options: Square, Rectangular                        │ │
│ │   Size: Small, Medium, Large, Custom                  │ │
│ │                                                         │ │
│ │ Deface Method: [Blur ▼]                               │ │
│ │   Options: Blur, Solid (Black Box), Mosaic             │ │
│ │                                                         │ │
│ │ Instructions:                                          │ │
│ │   1. Click on image to place deface area              │ │
│ │   2. Drag to resize (or use size dropdown)            │ │
│ │   3. Click "Apply Deface" to add to image              │ │
│ │   4. Repeat to add multiple deface areas               │ │
│ │                                                         │ │
│ │ Active Deface Areas (2):                               │ │
│ │   • Area 1: Square, Blur (100x100px) [Remove]        │ │
│ │   • Area 2: Rectangular, Solid (150x80px) [Remove]   │ │
│ │                                                         │ │
│ │ [Clear All Deface Areas]  [Apply Deface]  [Cancel]   │ │
│ └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Bulk processing queue (for approval):**
- When multiple files are selected, processing follows a **queue**: a fixed ordered list of items in **selection order**. Order is preserved: all images first (in selection order), then all videos (in selection order). Videos may be processed in parallel (e.g. up to N workers), but **reported progression is queue-based**: the UI shows which item(s) are in progress and how many are done (e.g. "Processing 3/8 — orbital-sander.mp4 (45s) — 23%").
- Each queue item has a **state** at any moment: **Pending** (not yet started), **In progress** (current item; show name, elapsed, %), **Done** (completed).
- The **main Deface page** and the **detailed page** (Open video debug log) **MUST** both show the same queue and progression: overall bar, status line, and a **queue list** (ordered items with state). The queue list is **required** on the detailed page; optional on the main page.

**Progress display (staged progression — for approval):**
- **Overall progress bar:** Must move during processing, not appear stuck. It reflects:
  - Completed items (e.g. 2/5 done → 40% base) plus the current item’s sub-progress when the deface CLI outputs percentage or frame counts (e.g. 23% or 161/706). Formula: `(completed/total)*100 + (current_item_pct/100)*(1/total)*100`.
- **Status line** shows staged updates in this order:
  1. **Elapsed time:** First show seconds (5s, 10s, 15s …) so the user sees activity.
  2. **Percentage:** When the deface CLI reports progress (e.g. 23%), append it (e.g. ` — 23%`).
  3. **Per-file when bulk (queue):** For multiple files, show current queue position and file (e.g. `Processing 3/8 — orbital-sander.mp4 (45s) — 23%`).
- **Queue list (bulk):** When more than one item is selected, the progress block MAY show an ordered queue list (each item: ✓ done / ⟳ in progress with time and % / waiting). This list SHALL be shown on the **detailed page** (see below).
- **Detailed steps (live log):** Expandable section with timestamped lines from the server (heartbeat + deface stderr). Keeps updating so the user can see the process is running.
- **Estimate:** Static note that images take a few seconds and each video often 1–2 minutes.
- **Link to detailed page:** "Open video debug log (new tab)" so the user can open the full progression + log in a separate tab.

**Progress API (for implementation):**
- The backend exposes progress for polling (e.g. `GET /deface_video_log` with a `progress` object). To support queue-aware UIs, the API SHALL expose: `total`, `completed`, `current_item`, `current_item_pct`, `elapsed_seconds`, `status`, `phase`; and a **queue** (ordered list), e.g. a `queue` array of `{ name, state: 'pending' | 'in_progress' | 'done' }` or an `item_names` array so the UI can derive states. Both the detailed page and main page use this to render the same queue list and progression.

**Detailed page (Open video debug log — for approval):**
- The page opened via "Open video debug log (new tab)" SHALL show the **same** queue and progression as the main Deface page, plus the full live log. Required: **overall progress bar**, **status line** (queue position, current item, elapsed, %), **queue list** (ordered items with state: ✓ done / ⟳ in progress / waiting), and **live log** (timestamped lines, updating every 1.5–2 s). This gives one place for both high-level queue progression and detailed log output.

**Behavior:**
- User clicks "Apply Deface" button
- System processes selected images/videos with deface settings
- Defaced media files are displayed in a preview grid
- User can review each defaced image/video frame
- **User can click [Edit] button on any media item to open Manual Deface Editor**
- **In Manual Deface Editor (for images):**
  - User sees full-size preview of defaced image
  - User can click on image to place deface area
  - User selects shape (Square or Rectangular) and size
  - User selects deface method (Blur, Solid, Mosaic)
  - User can add multiple deface areas per image
  - User can remove individual deface areas
  - User clicks "Apply Deface" to save changes
- **In Manual Deface Editor (for videos):**
  - System extracts a frame from the defaced video at a specific time point
  - User can select time point for frame extraction (video player with seek controls)
  - User sees full-size preview of extracted frame
  - User can click on frame to place deface area (same as images)
  - User selects shape, size, and deface method
  - User can add multiple deface areas per frame
  - User can remove individual deface areas
  - User clicks "Apply Deface" to save manually defaced frame
  - System saves the manually defaced frame with reference to the time point
- User can adjust automated deface settings and click "Adjust Settings & Re-apply" to reprocess
- User clicks "Accept & Proceed to Document Generation" to continue
- Accepted defaced files (with manual edits) are stored temporarily for document generation

**Key Features:**
- Preview grid shows all defaced images/video frames
- Each item shows original filename and deface status
- **[Edit] button on each media item opens Manual Deface Editor**
- **Manual Deface Editor allows:**
  - Click-to-place deface areas on image
  - Shape selection: Square or Rectangular
  - Size selection: Small, Medium, Large, or Custom (with width/height inputs)
  - Deface method: Blur, Solid (Black Box), or Mosaic
  - Multiple deface areas per image (e.g., faces + text/wording)
  - Visual preview of deface areas before applying
  - Remove individual deface areas
  - Clear all manual deface areas
- Checkboxes allow selection of which items to include in final document
- "Adjust Settings & Re-apply" button allows user to modify automated deface settings and reprocess
- "Accept & Proceed" button unlocks Step 4 (Document Generation)

**Existing defaced files — persist on return (for approval):**
- When the user opens the Deface page with a qualification and learner (e.g. `?qualification=Deco&learner=arjom`), the app checks for **already-saved** defaced files in `OUTPUT_FOLDER/<qualification>/<learner>/deface/`.
- If any defaced files exist there (e.g. from a previous run or from Generate Documents), they are **listed in section 3 (Apply Deface & Review)** so the user can **edit or proceed again** without re-running Apply Deface.
- **Return to page:** When the user returns to the same URL (e.g. after navigating away), the converted files **must stay there**: the review grid shows the same defaced items, and the user can [Edit], [Adjust Settings & Re-apply], or [Accept & Proceed to Document Generation]. Document generation from existing files does not require a session: the backend uses the saved deface folder when `session_id` is not provided (qualification and learner are required).
- **Flow:** Page load with qual + learner → GET `/deface_existing?qualification=…&learner=…` → if `items.length > 0`, show the review grid with those items; each has an [Edit] button. Media are served from `/deface_output/<qualification>/<learner>/<filename>` (with Range support for video). Generate Documents (POST `/generate_deface_documents`) accepts either `session_id` (from a fresh Apply Deface) or `qualification` + `learner` (when using existing deface output); in the latter case the backend builds the document from files in the deface folder.
- **Wireframe:** Same as the review grid in section 3: grid of defaced items with preview and [Edit]; label can show "✓ Defaced (saved)" for items loaded from existing output.

---

### 4. Document Generation Section

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ 4. Generate Documents                                       │
│                                                              │
│ Output Filename: [____________________________] *           │
│ (Enter filename without extension)                          │
│                                                              │
│ [Generate Documents] Button                                 │
│                                                              │
│ (During processing:)                                        │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ Generating Documents...                                │ │
│ │ [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] 75% │ │
│ │ Creating PDF/DOCX from defaced images... (3/4)         │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                              │
│ (After completion:)                                         │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ ✅ Documents Generated Successfully!                   │ │
│ │                                                         │ │
│ │ Output Folder:                                         │ │
│ │ /path/to/output/qualification/learner/                 │ │
│ │ [📁 Open Output Folder]                                │ │
│ │                                                         │ │
│ │ PDF: [📄 Open PDF]                                     │ │
│ │ DOCX: [📝 Download DOCX]                               │ │
│ │                                                         │ │
│ │ Standalone defaced images (N):                         │ │
│ │   1. 🖼 deface_IMG_0607.JPG  2. 🖼 deface_intro_frame_0_00.jpg  … │
│ │ Standalone defaced videos (M):                         │ │
│ │   1. 🎬 deface_intro.mp4  …                             │ │
│ └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Output folder contents (wireframe for approval):**
All deface output is saved inside a **`deface`** subfolder under the learner folder:
```
OUTPUT_FOLDER/{qualification}/{learner}/
└── deface/
    ├── deface_{filename}.pdf      ← Merged document (if PDF requested)
    ├── deface_{filename}.docx     ← Merged document (if DOCX requested)
    ├── deface_IMG_0607.JPG        ← Standalone defaced image
    ├── deface_intro_frame_0_00.jpg ← Standalone defaced video frame (if video included)
    ├── deface_intro_frame_1_00.jpg
    ├── …
    ├── deface_intro.mp4           ← Standalone defaced video (MP4)
    └── …
```
All of the above are saved under `deface/`: merged PDF/DOCX (when requested) plus every defaced image and defaced video as standalone files.

**Approval:** Please confirm that the output folder must contain both (1) merged documents (PDF/DOCX) and (2) standalone defaced files (individual images and MP4 videos) as shown in the wireframe above.

**Behavior:**
- Only enabled after user accepts defaced files in Step 3
- User enters output filename
- User clicks "Generate Documents"
- System **always** saves standalone defaced files (each defaced image and each defaced MP4 video) to the output folder's **`deface`** subfolder with `deface_` prefix
- System generates PDF/DOCX from accepted defaced images/videos (merged documents)
  - For videos: Extracts frames from defaced MP4 videos for document generation
- Merged documents saved with 'deface_' prefix (e.g., `deface_report.pdf`, `deface_report.docx`)
- All output (standalone + merged) saved to `OUTPUT_FOLDER/{qualification}/{learner}/deface/`

**Workflow:**
1. User selects qualification and learner
2. Images and videos load from `OUTPUT_FOLDER/{qualification}/{learner}/` and subfolders
3. User selects images and/or videos (bulk selection)
4. User configures output settings (Image + Deface + Format)
5. User clicks "Apply Deface" button
6. System processes files with deface:
   - **For images**: Process directly with deface (face anonymization)
   - **For videos**: Process videos directly with deface tool (outputs MP4 format)
   - Temporary anonymized images/videos saved with 'deface_' prefix (e.g., `deface_image1.jpg`, `deface_video1.mp4`)
7. Defaced media files displayed in review interface
8. User reviews defaced files
9. User can adjust settings and re-apply deface if needed
10. User clicks "Accept & Proceed to Document Generation"
11. User enters output filename
12. User clicks "Generate Documents"
13. System generates PDF/DOCX from accepted defaced images/frames
14. Output files saved with 'deface_' prefix (e.g., `deface_report.pdf`)
15. All deface output (documents and standalone files) saved to `OUTPUT_FOLDER/{qualification}/{learner}/deface/`

**Supported File Formats:**
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- **Videos**: `.mp4`

---

## Technical Implementation

### Backend Changes

#### New Route
- **Route**: `/v2p-formatter/deface`
- **Method**: GET
- **Template**: `templates/deface.html`
- **Functionality**: 
  - Loads qualifications and learners from OUTPUT_FOLDER
  - Renders the deface interface (same structure as Image to PDF)

#### New API Endpoints

##### 1. Apply Deface (Preview)
- **Endpoint**: `POST /v2p-formatter/apply_deface`
- **Parameters**: 
  - `image_paths` (array, required): List of image and video file paths
  - `quality` (int, default: 95): JPEG quality (1-100)
  - `max_size` (string, default: '640x480'): Max image size
  - **Deface Settings:**
    - `replacewith` (string, default: 'blur'): 'blur', 'solid', or 'mosaic'
    - `boxes` (bool, default: false): Use rectangular boxes
    - `thresh` (float, default: 0.2): Detection threshold (0.0-1.0)
    - `scale` (string, optional): 'original' or 'WxH' (e.g., '640x360')
    - `mosaicsize` (int, default: 20): Mosaic tile size (5-50)
    - `draw_scores` (bool, default: false): Show detection scores
    - `approve_video_processing` (bool, default: false): Must be true to process videos (approval required)
- **Response**: 
  ```json
  {
    "success": true,
    "processed": [
      {
        "original_path": "/path/to/image1.jpg",
        "original_name": "image1.jpg",
        "defaced_path": "/path/to/deface_image1.jpg",
        "defaced_url": "/v2p-formatter/deface_temp/{session_id}/deface_image1.jpg",
        "type": "image",
        "sequence": 1,
        "manual_defaces": []
      },
      {
        "original_path": "/path/to/video1.mp4",
        "original_name": "video1.mp4",
        "defaced_path": "/path/to/deface_video1.mp4",
        "defaced_url": "/v2p-formatter/deface_temp/{session_id}/deface_video1.mp4",
        "type": "video",
        "sequence": 2,
        "manual_defaces": [],
        "manual_frames": []
      }
    ],
    "temp_dir": "/path/to/temp/dir",
    "session_id": "session_abc123"
  }
  ```
- **Note**: Creates a session and returns preview URLs for defaced images/videos. Videos are processed as MP4 format.

##### 2. Apply Manual Deface
- **Endpoint**: `POST /v2p-formatter/apply_manual_deface`
- **Parameters**: 
  - `session_id` (string, required): Session ID from apply_deface response
  - `media_id` (string, required): Index or identifier for media item
  - `deface_areas` (array, required): List of deface area definitions, each with:
    - `x` (int): X coordinate (top-left corner)
    - `y` (int): Y coordinate (top-left corner)
    - `width` (int): Width of deface area
    - `height` (int): Height of deface area
    - `shape` (string): 'square' or 'rectangular'
    - `method` (string): 'blur', 'solid', or 'mosaic'
    - `mosaicsize` (int, optional): Mosaic tile size (if method is 'mosaic')
  - `mosaicsize` (int, default: 20): Default mosaic tile size
  - `time_point` (float, optional): For videos only - time point in seconds to extract frame
- **Response (for images)**: 
  ```json
  {
    "success": true,
    "defaced_path": "/path/to/deface_image1_manual.jpg",
    "defaced_url": "/v2p-formatter/deface_temp/{session_id}/deface_image1_manual.jpg",
    "deface_areas_applied": 2,
    "time_point": null
  }
  ```
- **Response (for videos)**: 
  ```json
  {
    "success": true,
    "defaced_path": "/path/to/deface_manual_video1_frame_05_20.jpg",
    "defaced_url": "/v2p-formatter/deface_temp/{session_id}/manual_frames_{media_id}/deface_manual_video1_frame_05_20.jpg",
    "deface_areas_applied": 2,
    "time_point": 5.2
  }
  ```
- **Note**: 
  - For images: Applies manual deface areas directly to the defaced image
  - For videos: Extracts frame at specified time_point, applies manual deface, saves frame
  - For videos: `time_point` is required. Manually defaced frames are stored in `manual_frames` array

##### 3. Generate Deface Documents
- **Endpoint**: `POST /v2p-formatter/generate_deface_documents`
- **Parameters**: 
  - `image_paths` (array, required): List of image and video file paths
  - `image_order` (array, optional): Custom order of files
  - `quality` (int, default: 95): JPEG quality (1-100)
  - `max_size` (string, default: '640x480'): Max image size
  - `output_format` (string, default: 'both'): 'pdf', 'docx', or 'both'
  - `layout` (string, default: 'grid'): 'grid' or 'custom'
  - `images_per_page` (int, default: 2): Number of images per page
  - `qualification` (string, optional): Qualification name
  - `learner` (string, optional): Learner name
  - `filename` (string, required): Output filename (without extension)
  - **Deface Settings:**
    - `replacewith` (string, default: 'blur'): 'blur', 'solid', or 'mosaic'
    - `boxes` (bool, default: false): Use rectangular boxes
    - `thresh` (float, default: 0.2): Detection threshold (0.0-1.0)
    - `scale` (string, optional): 'original' or 'WxH' (e.g., '640x360')
    - `mosaicsize` (int, default: 20): Mosaic tile size (5-50)
    - `draw_scores` (bool, default: false): Show detection scores
    - `approve_video_processing` (bool, default: false): Must be true to process videos (approval required)
- **Response**: 
  ```json
  {
    "success": true,
    "pdf_path": "/path/to/deface_report.pdf",
    "pdf_url": "/v2p-formatter/download?path=...",
    "docx_path": "/path/to/deface_report.docx",
    "docx_url": "/v2p-formatter/download?path=...",
    "output_folder_path": "/path/to/output/folder/deface",
    "exported_standalone_images": [{"path": "...", "relative_path": "...", "name": "deface_IMG_0607.JPG"}, ...],
    "exported_standalone_images_count": 3,
    "exported_videos": [{"path": "...", "relative_path": "...", "name": "deface_intro.mp4"}, ...],
    "exported_videos_count": 1
  }
  ```
**Note**: All output files use 'deface_' prefix and are saved inside the **`deface`** subfolder. Standalone defaced images and defaced videos are always saved there in addition to merged PDF/DOCX (when requested). The API returns `output_folder_path` pointing to this `deface` subfolder.

#### Processing Flow

**Step 1: Apply Deface (Preview)**
1. Validate input file paths (must be within OUTPUT_FOLDER)
2. Create unique session ID for this deface operation
3. Create temporary directory for defaced images/frames (with session ID)
4. Separate images from videos (by file extension)
5. **For images:**
   - Process each image with deface tool
   - Run `deface` command-line tool with specified settings
   - Save anonymized image to temp directory with 'deface_' prefix (e.g., `deface_image1.jpg`)
6. **For videos:**
   - Process video directly with deface tool (outputs MP4 format)
   - Run `deface` command-line tool with specified settings
   - Save anonymized video to temp directory with 'deface_' prefix (e.g., `deface_video1.mp4`)
   - **Note**: Videos must be saved as MP4 format (not frames extracted to JPEG)
7. Return preview URLs and session ID
8. Store session metadata (file paths, settings) for document generation

**Step 2: Generate Documents**
1. Retrieve defaced files from session (using session_id)
2. **Standalone defaced files (always saved):**
   - Create subfolder `deface` under the learner output folder: `OUTPUT_FOLDER/{qualification}/{learner}/deface/`.
   - Copy each defaced image (and each video frame image) to this `deface` subfolder as individual files with `deface_` prefix (e.g. `deface_IMG_0607.JPG`, `deface_intro_frame_0_00.jpg`).
   - Copy each defaced video (MP4) to the same `deface` subfolder with `deface_` prefix (e.g. `deface_intro.mp4`).
   - These standalone files are saved in addition to any merged PDF/DOCX.
3. Generate PDF/DOCX from defaced images/videos (using existing `create_image_pdf` and `create_image_docx` functions)
   - For videos: Extract frames from defaced MP4 videos for document generation
4. Save merged documents to the `deface` subfolder with 'deface_' prefix (e.g., `deface_report.pdf`, `deface_report.docx`)
5. Clean up temporary defaced images/videos (after document generation)
6. Return document paths, standalone image list, and standalone video list

**Session Management:**
- Each deface operation creates a unique session
- Session stores defaced file paths, original paths, and settings
- Sessions are cleaned up after document generation or after timeout (e.g., 1 hour)
- Session ID is returned to frontend and used for document generation

#### New Module: `app/deface_processor.py`
- **Functions:**
  - `deface_image()`: Process single image with deface
  - `deface_images()`: Process multiple images with deface
  - `deface_video()`: Process video directly with deface tool (outputs MP4 format)
  - `apply_manual_deface()`: Apply manual deface areas to an image
    - Parameters: image_path, deface_areas (list of area definitions), mosaicsize
    - Returns: dict with 'success' (bool), 'output_path' (str), and optional 'error' (str)
  - `apply_manual_deface_to_video()`: Apply manual deface to a video frame
    - Parameters: video_path, time_point (float), output_dir, deface_areas (list), mosaicsize
    - Extracts frame at time_point from video, applies manual deface, saves defaced frame
    - Returns: dict with 'success' (bool), 'output_path' (str), 'time_point' (float), and optional 'error' (str)
- **Uses**: `subprocess` to call `deface` command-line tool
- **Uses**: PIL/Pillow for manual deface area processing (blur, solid box, mosaic)
- **Uses**: `app.video_processor` to extract frames from defaced MP4 videos for document generation (if needed)
- **Error Handling**: Returns success/error dict for each file
- **Video Processing**: Processes videos directly with deface tool, outputs MP4 format (videos must be saved as MP4)
- **Manual Deface Processing**:
  - Uses PIL/Pillow ImageFilter for blur effect
  - Uses PIL/Pillow ImageDraw for solid boxes
  - Uses PIL/Pillow for mosaic effect (pixelation)
  - Supports multiple deface areas per image/frame
  - Preserves image quality and format
  - **For videos**: Extracts frame at specified time point, applies manual deface, saves frame
  - **For videos**: Manually defaced frames are stored with time point references

### Frontend Changes

#### New Template: `templates/deface.html`
- Based on `templates/image_to_pdf.html`
- Same structure and JavaScript logic
- Added deface settings section
- Updated API endpoint to `/v2p-formatter/generate_deface_documents`
- Added JavaScript handlers for deface settings controls

#### JavaScript Changes
- Added deface settings to request payload
- Added event handlers for deface controls:
  - Threshold slider updates value display
  - Mosaic size slider updates value display
  - Mosaic size container visibility based on method selection
- **New Review Interface:**
  - Preview grid displays defaced images/video frames
  - Each item shows original filename, deface status, and preview image
  - "Adjust Settings & Re-apply" button sends new request to apply_deface endpoint
  - "Accept & Proceed" button stores session_id and enables document generation step
  - Progress indicator shows "Processing images/videos with deface..." during anonymization
- **Session Management:**
  - Store session_id from apply_deface response
  - Include session_id in generate_deface_documents request
  - Handle session expiration and cleanup

### Dependencies
- **New Package**: `deface>=1.5.0`
  - Command-line tool for face anonymization
  - Installed via: `pip install deface`
  - Provides face detection and anonymization capabilities

---

## User Workflow Examples

### Example 1: Basic Face Anonymization with Blur (Images)
1. User navigates to Deface tab
2. User selects qualification and learner
3. User selects 5 images (using checkboxes)
4. User configures settings:
   - Anonymization Method: Blur (default)
   - Detection Threshold: 0.2 (default)
   - Output Format: PDF Only
5. User clicks "Apply Deface" button
6. System processes images with deface (blur faces)
   - Temporary files: `deface_image1.jpg`, `deface_image2.jpg`, etc.
   - Session ID created: `session_abc123`
7. Defaced images displayed in review interface
8. User reviews defaced images
9. User clicks "Accept & Proceed to Document Generation"
10. User enters filename: "report"
11. User clicks "Generate Documents"
12. System generates PDF from defaced images (using session_abc123)
13. PDF saved as `deface_report.pdf` in output folder

### Example 1b: Basic Face Anonymization with Blur (Videos)
1. User navigates to Deface tab
2. User selects qualification and learner
3. User selects 2 videos (using checkboxes)
4. User configures settings:
   - Anonymization Method: Blur (default)
   - Detection Threshold: 0.2 (default)
   - Approve Video Processing: ✓ (checked)
   - Output Format: PDF Only
5. User clicks "Apply Deface" button
6. System processes videos with deface:
   - Processes videos directly with deface tool
   - Saves anonymized videos as MP4 format
   - Temporary files: `deface_video1.mp4`, `deface_video2.mp4`
   - Session ID created: `session_xyz789`
7. Defaced videos displayed in review interface (with video preview)
8. User reviews defaced videos
9. User clicks "Accept & Proceed to Document Generation"
10. User enters filename: "video_report"
11. User clicks "Generate Documents"
12. System extracts frames from defaced MP4 videos and generates PDF (using session_xyz789)
13. PDF saved as `deface_video_report.pdf` in output folder

### Example 2: Mosaic Anonymization with Custom Settings (with Re-apply)
1. User selects qualification and learner
2. User selects 10 images
3. User configures settings:
   - Anonymization Method: Mosaic
   - Use Rectangular Boxes: ✓ (checked)
   - Detection Threshold: 0.15 (more sensitive)
   - Mosaic Size: 15 pixels (smaller tiles)
   - Detection Scale: 640x360 (for faster processing)
   - Output Format: Both (PDF + DOCX)
4. User clicks "Apply Deface" button
5. System processes images with deface (mosaic anonymization)
   - Temporary files: `deface_image1.jpg`, `deface_image2.jpg`, etc.
   - Session ID created: `session_mosaic456`
6. Defaced images displayed in review interface
7. User reviews defaced images - notices some faces not properly anonymized
8. User adjusts settings:
   - Detection Threshold: 0.10 (more sensitive)
   - Mosaic Size: 12 pixels (smaller tiles)
9. User clicks "Adjust Settings & Re-apply"
10. System reprocesses images with new settings
    - New session ID: `session_mosaic789`
11. User reviews updated defaced images - satisfied with results
12. User clicks "Accept & Proceed to Document Generation"
13. User enters filename: "mosaic_report"
14. User clicks "Generate Documents"
15. System generates PDF and DOCX documents from defaced images (using session_mosaic789)
    - Output files: `deface_mosaic_report.pdf` and `deface_mosaic_report.docx`

### Example 3: Mixed Images and Videos with Black Box Anonymization
1. User selects qualification and learner
2. User selects 3 images and 2 videos (bulk selection)
3. User configures settings:
   - Anonymization Method: Solid (Black Box)
   - Use Rectangular Boxes: ✓ (checked)
   - Detection Threshold: 0.25 (less sensitive, fewer false positives)
   - Approve Video Processing: ✓ (checked)
   - Output Format: PDF Only
4. User clicks "Apply Deface" button
5. System processes files with deface:
   - Processes 3 images directly (black boxes)
   - Processes 2 videos directly with deface tool (saves as MP4)
   - Temporary files: `deface_image1.jpg`, `deface_image2.jpg`, `deface_image3.jpg`, `deface_video1.mp4`, `deface_video2.mp4`
   - Session ID created: `session_mixed123`
6. Defaced images and videos displayed in review interface
7. User reviews defaced media - satisfied with results
8. User clicks "Accept & Proceed to Document Generation"
9. User enters filename: "mixed_report"
10. User clicks "Generate Documents"
11. System extracts frames from defaced MP4 videos and generates PDF with all anonymized images/frames (using session_mixed123)
12. PDF saved as `deface_mixed_report.pdf` in output folder

---

## Edge Cases & Error Handling

### Edge Cases
1. **No faces detected**: Images/frames processed successfully (no changes), still shown in review
2. **No images/videos found**: Show message "No images or videos found in selected folder"
3. **Unsupported file format**: Show error message, skip that file
4. **Deface processing fails**: Show error for specific file in review interface, allow user to skip or retry
5. **Very large images**: Use detection scale option for performance
6. **Very long videos**: Video processing may take time (depends on video length and resolution)
7. **No selection**: Disable "Apply Deface" button until files selected
8. **Session expired**: Show error message, require user to re-apply deface
9. **Video processing fails**: Show error for specific video in review interface, allow user to skip or retry
10. **Video processing not approved**: Show error message if videos are selected but approval checkbox is not checked
11. **User rejects all defaced files**: Require user to adjust settings and re-apply before proceeding
12. **User accepts but no files selected in review**: Show warning, require at least one file to be selected
13. **Filename not provided**: Show error message, require filename before document generation

### Error Messages
- "Please select at least one image or video"
- "Please enter a filename"
- "No images or videos found for selected qualification/learner"
- "Error processing image with deface: [filename] - [error message]"
- "Error processing video: [filename] - [error message]"
- "Video processing requires approval. Please check 'Approve Video Processing' setting."
- "Failed to process video: [filename]"
- "Failed to apply deface: [error message]"
- "Session expired. Please re-apply deface."
- "Please accept defaced files before generating documents"
- "Please select at least one defaced file to include in document"
- "Failed to generate document: [error message]"
- "Deface processing timeout (exceeded 5 minutes per file)"
- "Failed to apply manual deface: [error message]"
- "Deface area coordinates are outside image bounds"
- "Deface area is too small (minimum 10x10 pixels)"
- "Invalid deface area definition"
- "Failed to load image for manual deface editing"

---

## Questions for Approval

1. **Deface Settings Defaults**: 
   - Anonymization Method: Blur (recommended) ✓
   - Detection Threshold: 0.2 (recommended) ✓
   - Use Rectangular Boxes: Unchecked by default (recommended) ✓
   - Detection Scale: Original by default (recommended) ✓
   - Show Detection Scores: Unchecked by default (recommended) ✓

2. **Performance Considerations**:
   - Should we limit batch size? (Recommended: No limit, but add timeout per file)
   - Should we show progress per file? (Recommended: Yes - "Processing X/Y files")
   - Should we allow cancellation? (Recommended: Future enhancement)
   - **Video processing**: Videos processed directly with deface tool, output as MP4 format. Processing time depends on video length and resolution.

3. **Output Quality**:
   - Should anonymized images replace originals? (Recommended: No - temporary files only)
   - Should we save anonymized images separately? (Recommended: No - temporary only)
   - **All output files (temporary images and final PDF/DOCX) use 'deface_' prefix** ✓

4. **Error Handling**:
   - If deface fails for some images, should we continue with others? (Recommended: Yes - show in review interface)
   - Should we show which images failed? (Recommended: Yes - in review interface with error details)
   - Should users be able to retry failed files? (Recommended: Yes - via "Adjust Settings & Re-apply")

5. **Review Interface**:
   - Should users be able to exclude specific files from document generation? (Recommended: Yes - via checkboxes in review)
   - Should users be able to re-apply deface with different settings? (Recommended: Yes - "Adjust Settings & Re-apply" button)
   - How long should defaced files be stored? (Recommended: 1 hour session timeout, cleanup after document generation)
   - Should preview images be full size or thumbnails? (Recommended: Thumbnails in grid, click to view full size)

6. **Manual Deface Interface**:
   - Should manual deface areas be visible on preview? (Recommended: Yes - red dashed rectangles) ✓
   - Should users be able to edit/remove individual deface areas? (Recommended: Yes - remove button per area) ✓
   - Should manual deface areas persist when re-applying automated deface? (Recommended: Yes - manual defaces are preserved) ✓
   - Maximum number of manual deface areas per image? (Recommended: No hard limit, but warn if >20) ✓
   - Should manual deface support drag-to-resize? (Recommended: Yes - drag corners to resize) ✓
   - Should manual deface support drag-to-move? (Recommended: Yes - drag center to move) ✓
   - **Should manual deface be supported for videos?** (Recommended: Yes - extract frames and apply manual deface) ✓
   - **How should video frames be selected for manual deface?** (Recommended: Video player with seek controls, extract frame at selected time point) ✓
   - **Should manually defaced video frames be used in document generation?** (Recommended: Yes - use manually defaced frames if available) ✓

7. **Video Processing**:
   - How should videos be processed? (Recommended: Process videos directly with deface tool, output as MP4 format) ✓
   - Should videos require approval before processing? (Recommended: Yes - approval checkbox setting) ✓
   - Should video frames be included in document generation? (Recommended: Yes - extract frames from defaced MP4 videos for document generation)
   - **Videos must be saved as MP4 format** (not frames extracted to JPEG) ✓

---

## Wireframes (Text-Based)

### Page Layout - Deface Module
```
┌────────────────────────────────────────────────────────────────────────────┐
│ Navigation Tabs                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│ [Video to Image] [Media Converter] [Image to PDF] [Deface] ← NEW          │
│                                                                             │
│ (Active tab: Deface - highlighted with purple border)                      │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ Qualification/Learner Selection                                            │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ Select Qualification: [Deco ▼]  Select Learner: [lubins ▼]  [🔄 Refresh] │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ 1. Select Images                                                           │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ [☐] Select All                                                         │ │
│ │ [10] file(s) selected (5 images, 5 videos)                            │ │
│ │ [Reset Selection]                                                     │ │
│ │                                                                        │ │
│ │ Sort by: [Name ▼]  Thumbnails per row: [3 ▼]  [⛶]                   │ │
│ │                                                                        │ │
│ │ [Reset to Default Order]  Sequences: 1, 2, 3... (by selection order) │ │
│ ├───────────────────────────────────────────────────────────────────────┤ │
│ │                                                                        │ │
│ │ ▶ 📁 session1 (12 images)                                             │ │
│ │ ▶ 📁 session2 (8 images)                                              │ │
│ │                                                                        │ │
│ │ Direct images (3-column grid):                                        │ │
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
│ │ │ cover.jpg    │ │ summary.jpg  │ │ image3.jpg   │                  │ │
│ │ │ (2.5 MB)     │ │ (1.8 MB)     │ │ (3.2 MB)     │                  │ │
│ │ └──────────────┘ └──────────────┘ └──────────────┘                  │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ 2. Output Settings                                                         │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ 📦 Batch Mode: These settings will apply to all 10 selected images.  │ │
│ ├───────────────────────────────────────────────────────────────────────┤ │
│ │                                                                        │ │
│ │ Image Settings:                                                       │ │
│ │ ├─ Quality: [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] 95  │ │
│ │ └─ Max Size: [640x480 ▼]                                             │ │
│ │                                                                        │ │
│ │ Deface Settings:                                                      │ │
│ │ ├─ Anonymization Method: [Blur ▼]                                    │ │
│ │ │   (Options: Blur, Solid (Black Box), Mosaic)                       │ │
│ │ │                                                                     │ │
│ │ ├─ [☐] Use Rectangular Boxes                                         │ │
│ │ │   Use rectangular boxes instead of ellipses (for solid/mosaic)     │ │
│ │ │                                                                     │ │
│ │ ├─ Detection Threshold: [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] 0.2 │ │
│ │ │   Lower = more sensitive (default: 0.2)                            │ │
│ │ │                                                                     │ │
│ │ ├─ Detection Scale (Optional): [Original Resolution ▼]               │ │
│ │ │   (Options: Original, 640x360, 1280x720)                           │ │
│ │ │   Downscale for faster processing (keeps output quality)           │ │
│ │ │                                                                     │ │
│ │ ├─ Mosaic Size: [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] 20 │ │
│ │ │   (Only visible when Method = Mosaic)                              │ │
│ │ │   Tile size in pixels (default: 20)                                │ │
│ │ │                                                                     │ │
│ │ └─ [☐] Show Detection Scores                                         │ │
│ │     Display face detection confidence scores                          │ │
│ │                                                                        │ │
│ │ Output Format:                                                        │ │
│ │ ├─ Format: [PDF Only ▼]                                              │ │
│ │ ├─ Layout: [Grid ▼]                                                  │ │
│ │ └─ Images per Page: [2 ▼]                                            │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ℹ️ Images will be anonymized using face detection before generating       │
│    PDF and DOCX documents. Generated files will include anonymized        │
│    images with filenames displayed below each image.                      │
│                                                                             │
│ 3. Apply Deface & Review                                                   │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ [Apply Deface] Button                                                 │ │
│ │                                                                        │ │
│ │ (Processing state:)                                                   │ │
│ │ Processing Deface...                                                  │ │
│ │ [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] 75%    │ │
│ │ Processing images/videos with deface... (3/4)                         │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ 4. Generate Documents                                                      │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ Output Filename: [anonymized_report________________] *                │ │
│ │ (Enter filename without extension)                                    │ │
│ │                                                                        │ │
│ │ [Generate Documents] Button (disabled until Step 3 accepted)         │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

### Review State (After Deface Applied)
```
┌────────────────────────────────────────────────────────────────────────────┐
│ 3. Apply Deface & Review                                                   │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ ✅ Deface Applied Successfully                                        │ │
│ │                                                                        │ │
│ │ Review anonymized media files below:                                  │ │
│ │                                                                        │ │
│ │ Preview Grid (3-column):                                              │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                   │ │
│ │ │      ┌─────┐ │ │      ┌─────┐ │ │      ┌─────┐ │                   │ │
│ │ │      │ [☑] │ │ │      │ [☑] │ │ │      │ [☐] │ │                   │ │
│ │ │      └─────┘ │ │      └─────┘ │ │      └─────┘ │                   │ │
│ │ │  ┌────────┐  │ │  ┌────────┐  │ │  ┌────────┐  │                   │ │
│ │ │  │        │  │ │  │        │  │ │  │        │  │                   │ │
│ │ │  │ Defaced│  │ │  │ Defaced│  │ │  │ Defaced│  │                   │ │
│ │ │  │ Image  │  │ │  │ Image  │  │ │  │ Image  │  │                   │ │
│ │ │  │        │  │ │  │        │  │ │  │        │  │                   │ │
│ │ │  └────────┘  │ │  └────────┘  │ │  └────────┘  │                   │ │
│ │ │           [1]│ │           [2]│ │           [3]│                   │ │
│ │ │ image1.jpg   │ │ image2.jpg   │ │ image3.jpg   │                   │ │
│ │ │ ✓ Defaced    │ │ ✓ Defaced    │ │ ✓ Defaced    │                   │ │
│ │ │ [Edit]       │ │ [Edit]       │ │ [Edit]       │                   │ │
│ │ └──────────────┘ └──────────────┘ └──────────────┘                   │ │
│ │                                                                        │ │
│ │ [Adjust Settings & Re-apply] Button                                   │ │
│ │ [Accept & Proceed to Document Generation] Button                      │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

### Manual Deface Editor (Modal/Dialog) - Image
```
┌────────────────────────────────────────────────────────────────────────────┐
│ Manual Deface Editor - image1.jpg                                    [✕]   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │                                                                        │ │
│ │                                                                        │ │
│ │         [Full-size defaced image preview - clickable]                 │ │
│ │                                                                        │ │
│ │         [Red dashed rectangles show deface areas]                     │ │
│ │         [Click to add new deface area]                                │ │
│ │                                                                        │ │
│ │                                                                        │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ Controls:                                                                   │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ Deface Shape: [Square ▼]  Size: [Medium ▼]                           │ │
│ │   Shape: Square, Rectangular                                          │ │
│ │   Size: Small (50x50), Medium (100x100), Large (200x200), Custom      │ │
│ │   Custom Size: Width: [___] Height: [___] (if Custom selected)        │ │
│ │                                                                        │ │
│ │ Deface Method: [Blur ▼]                                               │ │
│ │   Options: Blur, Solid (Black Box), Mosaic                            │ │
│ │   Mosaic Size: [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] 20  │ │
│ │   (Only visible when Method = Mosaic)                                 │ │
│ │                                                                        │ │
│ │ Instructions:                                                          │ │
│ │   1. Click on image to place deface area                              │ │
│ │   2. Drag corners to resize (or use size dropdown)                    │ │
│ │   3. Click "Add Deface Area" to add to list                          │ │
│ │   4. Repeat to add multiple deface areas                              │ │
│ │                                                                        │ │
│ │ Active Deface Areas (2):                                               │ │
│ │   • Area 1: Square, Blur (100x100px) at (150, 200) [Remove]          │ │
│ │   • Area 2: Rectangular, Solid (150x80px) at (300, 100) [Remove]    │ │
│ │                                                                        │ │
│ │ [Clear All Deface Areas]  [Apply Deface]  [Cancel]                   │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

### Manual Deface Editor (Modal/Dialog) - Video
```
┌────────────────────────────────────────────────────────────────────────────┐
│ Manual Deface Editor - video1.mp4                                    [✕]   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ Frame Selection:                                                            │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ Video Player: [▶]  [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━]   │ │
│ │ Time: [0:05.2] / [1:23.5]  [Extract Frame at Current Time]           │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │                                                                        │ │
│ │                                                                        │ │
│ │         [Extracted frame preview - clickable]                         │ │
│ │         (Frame at 5.2 seconds)                                        │ │
│ │                                                                        │ │
│ │         [Red dashed rectangles show deface areas]                     │ │
│ │         [Click to add new deface area]                                │ │
│ │                                                                        │ │
│ │                                                                        │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ Controls:                                                                   │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ Deface Shape: [Square ▼]  Size: [Medium ▼]                           │ │
│ │   Shape: Square, Rectangular                                          │ │
│ │   Size: Small (50x50), Medium (100x100), Large (200x200), Custom      │ │
│ │                                                                        │ │
│ │ Deface Method: [Blur ▼]                                               │ │
│ │   Options: Blur, Solid (Black Box), Mosaic                            │ │
│ │                                                                        │ │
│ │ Instructions:                                                          │ │
│ │   1. Use video player to select frame time point                      │ │
│ │   2. Click "Extract Frame at Current Time" to load frame              │ │
│ │   3. Click on frame to place deface area                              │ │
│ │   4. Drag corners to resize (or use size dropdown)                    │ │
│ │   5. Click "Apply Deface" to save defaced frame                       │ │
│ │                                                                        │ │
│ │ Active Deface Areas (1):                                               │ │
│ │   • Area 1: Square, Blur (100x100px) at (150, 200) [Remove]          │ │
│ │                                                                        │ │
│ │ [Clear All Deface Areas]  [Apply Deface]  [Cancel]                   │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

### Processing State (During Deface Application)
```
┌────────────────────────────────────────────────────────────────────────────┐
│ 3. Apply Deface & Review                                                   │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ [Apply Deface] Button (disabled during processing)                    │ │
│ ├───────────────────────────────────────────────────────────────────────┤ │
│ │                                                                        │ │
│ │ Processing Deface...                                                  │ │
│ │ ┌──────────────────────────────────────────────────────────────────┐ │ │
│ │ │ [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] 75% │ │ │
│ │ └──────────────────────────────────────────────────────────────────┘ │ │
│ │                                                                        │ │
│ │ Processing images/videos with deface... (8/10 files)                  │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

### Document Generation State (After Review Accepted)
```
┌────────────────────────────────────────────────────────────────────────────┐
│ 4. Generate Documents                                                      │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ Output Filename: [anonymized_report] (enabled)                        │ │
│ │                                                                        │ │
│ │ [Generate Documents] Button                                           │ │
│ ├───────────────────────────────────────────────────────────────────────┤ │
│ │                                                                        │ │
│ │ (During generation:)                                                  │ │
│ │ Generating Documents...                                               │ │
│ │ [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] 60%    │ │
│ │ Creating PDF/DOCX from defaced images... (6/10 images)                │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

### Success State (After Document Generation)
```
┌────────────────────────────────────────────────────────────────────────────┐
│ 4. Generate Documents                                                      │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ Output Filename: [anonymized_report]                                  │ │
│ │                                                                        │ │
│ │ [Generate Documents] Button                                           │ │
│ ├───────────────────────────────────────────────────────────────────────┤ │
│ │                                                                        │ │
│ │ ✅ Documents Generated Successfully!                                  │ │
│ │                                                                        │ │
│ │ Output Folder:                                                        │ │
│ │ /Users/rom/Documents/nvq/v2p-formatter-output/Deco/lubins/           │ │
│ │                                                                        │ │
│ │ [📁 Open Output Folder]                                               │ │
│ │                                                                        │ │
│ │ ───────────────────────────────────────────────────────────────────  │ │
│ │                                                                        │ │
│ │ PDF: [📄 Open PDF]                                                    │ │
│ │ DOCX: [📝 Download DOCX]                                              │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

### Deface Settings Detail (Mosaic Method Selected)
```
┌────────────────────────────────────────────────────────────────────────────┐
│ Deface Settings:                                                           │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ Anonymization Method: [Mosaic ▼]                                     │ │
│ │   Options: Blur, Solid (Black Box), Mosaic                           │ │
│ │                                                                        │ │
│ │ [☑] Use Rectangular Boxes                                            │ │
│ │   Use rectangular boxes instead of ellipses (for solid/mosaic)        │ │
│ │                                                                        │ │
│ │ Detection Threshold: [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] 0.15    │ │
│ │   Lower = more sensitive (default: 0.2)                               │ │
│ │                                                                        │ │
│ │ Detection Scale (Optional): [640x360 ▼]                               │ │
│ │   (Options: Original, 640x360, 1280x720)                              │ │
│ │   Downscale for faster processing (keeps output quality)              │ │
│ │                                                                        │ │
│ │ Mosaic Size: [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] 15    │ │
│ │   (Visible when Method = Mosaic)                                      │ │
│ │   Tile size in pixels (default: 20, range: 5-50)                      │ │
│ │                                                                        │ │
│ │ [☐] Show Detection Scores                                             │ │
│ │     Display face detection confidence scores                          │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Approval Status

- [ ] Design approved
- [ ] Layout approved
- [ ] User flow approved
- [ ] Visual design approved
- [ ] Deface settings approved
- [ ] Review interface approved
- [ ] Manual deface interface approved
- [ ] Manual deface functionality approved (click-to-place, multiple areas, shape/size selection)
- [ ] Video processing approach approved (MP4 output format)
- [ ] Video approval setting approved
- [ ] Session management approach approved
- [ ] Technical implementation approved
- [ ] Ready for implementation

**Notes for Approval:**
- Please review the specification and wireframes
- Any changes to layout, flow, or design should be noted
- Once approved, implementation will proceed
- Deface module reuses Image to PDF structure for consistency
- **IMPORTANT**: Videos must be saved as MP4 format (not frames extracted to JPEG)
- Video processing requires explicit approval via checkbox setting

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-XX  
**Author**: Development Team  
**Based on**: Image to PDF Module Specification
