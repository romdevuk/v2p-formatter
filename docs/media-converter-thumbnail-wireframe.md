# Media Converter - Thumbnail Preview UI Wireframe

## Overview
Add thumbnail previews to the file selector so users can visually identify files before selection. This will show image thumbnails for JPG/PNG files and video frame thumbnails for MOV files.

---

## Text Wireframe: File Selection with Thumbnails

### Current Design (Without Thumbnails)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ ☑ 🎬 video1.mov                                                         │
│    📁 /input/folder1/video1.mov                                         │
│    📊 245.3 MB  |  🕐 00:05:32  |  📐 1920x1080                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Proposed Design (With Thumbnails)

#### Option 1: Horizontal Layout (Recommended)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ ┌──────┐  ☑ 🎬 video1.mov                                              │
│ │      │     📁 /input/folder1/video1.mov                              │
│ │ THUMB│     📊 245.3 MB  |  🕐 00:05:32  |  📐 1920x1080              │
│ │      │                                                                 │
│ └──────┘                                                                 │
│  120x90                                                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Option 2: Vertical Layout (Alternative)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ ┌──────────────────────────────────────┐                                │
│ │                                      │                                │
│ │           THUMBNAIL                  │                                │
│ │         (240x180px)                  │                                │
│ │                                      │                                │
│ └──────────────────────────────────────┘                                │
│ ☑ 🎬 video1.mov                                                         │
│    📁 /input/folder1/video1.mov                                         │
│    📊 245.3 MB  |  🕐 00:05:32  |  📐 1920x1080                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed UI Specifications

### File Card Layout (Option 1 - Horizontal - RECOMMENDED)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ┌──────────┐  ┌───────────────────────────────────────────────────────┐ │
│ │          │  │ ☑ 🎬 video1.mov                                       │ │
│ │          │  │    📁 /input/folder1/video1.mov                       │ │
│ │ THUMBNAIL│  │    📊 245.3 MB  |  🕐 00:05:32  |  📐 1920x1080       │ │
│ │  120x90  │  │                                                       │ │
│ │          │  │    [Hover: Show larger preview]                       │ │
│ │          │  │                                                       │ │
│ └──────────┘  └───────────────────────────────────────────────────────┘ │
│    Fixed      Flexible width (rest of card)                              │
│   120x90px                                                                │
└─────────────────────────────────────────────────────────────────────────┘
```

### File Card Layout (Option 2 - Vertical - Alternative)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                                                                     │ │
│ │                    THUMBNAIL PREVIEW                                │ │
│ │                      (240x180px)                                    │ │
│ │                    [Aspect ratio preserved]                         │ │
│ │                                                                     │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ☑ 🎬 video1.mov                                                     │ │
│ │    📁 /input/folder1/video1.mov                                     │ │
│ │    📊 245.3 MB  |  🕐 00:05:32  |  📐 1920x1080                     │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Component Specifications

### 1. Thumbnail Display

#### For Image Files (JPG/PNG)
- **Source**: Use the actual image file
- **Size**: 120x90px (horizontal) or 240x180px (vertical)
- **Aspect Ratio**: Preserved (fit within bounds, maintain ratio)
- **Loading**: Show placeholder/spinner while loading
- **Error**: Show broken image icon if load fails

#### For Video Files (MOV)
- **Source**: Extract frame at 1 second (or first frame)
- **Size**: 120x90px (horizontal) or 240x180px (vertical)
- **Aspect Ratio**: Preserved (fit within bounds, maintain ratio)
- **Loading**: Show placeholder/spinner while extracting
- **Error**: Show video icon placeholder if extraction fails
- **Indicator**: Small play icon overlay (▶) to indicate video

### 2. Thumbnail Container

```
┌─────────────────────────────────────────────────────────┐
│ Thumbnail Container (120x90px)                          │
│                                                          │
│ ┌──────────────────────────────────────────────────────┐ │
│ │                                                      │ │
│ │              [THUMBNAIL IMAGE]                      │ │
│ │         (Aspect ratio preserved, centered)          │ │
│ │                                                      │ │
│ └──────────────────────────────────────────────────────┘ │
│                                                          │
│ Background: #1a1a1a (darker than card)                 │
│ Border: 1px solid #444                                   │
│ Border-radius: 4px                                       │
│ Overflow: hidden (crop if needed)                        │
│                                                          │
│ Loading State:                                           │
│   - Spinner animation in center                         │
│   - Background: #1a1a1a                                 │
│                                                          │
│ Error State:                                             │
│   - Icon: 🖼️ (images) or 🎬 (videos)                   │
│   - Text: "Preview unavailable"                         │
│   - Background: #2a2a2a                                 │
└─────────────────────────────────────────────────────────┘
```

### 3. Hover Preview (Optional Enhancement)

```
On hover over thumbnail:
┌─────────────────────────────────────────────────────────┐
│                    [LARGER PREVIEW]                     │
│                                                          │
│ ┌──────────────────────────────────────────────────────┐ │
│ │                                                      │ │
│ │                                                      │ │
│ │            LARGER THUMBNAIL                          │ │
│ │              (400x300px)                             │ │
│ │                                                      │ │
│ │                                                      │ │
│ └──────────────────────────────────────────────────────┘ │
│                                                          │
│ Position: Above or to the side of thumbnail             │
│ Background: #1e1e1e with shadow                         │
│ Border: 2px solid #667eea                               │
│ Z-index: High (appears above other elements)            │
└─────────────────────────────────────────────────────────┘
```

---

## Complete File Card Example (Horizontal Layout)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ┌──────────┐  ┌───────────────────────────────────────────────────────┐ │
│ │          │  │ ☑ 🎬 IMG_9558.MOV                                    │ │
│ │   [VID]  │  │    📁 /Users/rom/Documents/nvq/v2p-formatter-input/ │ │
│ │  THUMB   │  │    IMG_9558.MOV                                      │ │
│ │  120x90  │  │    📊 115.42 MB  |  🕐 00:02:15  |  📐 1920x1080    │ │
│ │   ▶️     │  │                                                       │ │
│ └──────────┘  └───────────────────────────────────────────────────────┘ │
│                                                                         │
│ Hover effect: Border color changes to #667eea                          │
│ Selected: Background #333, border #667eea                              │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ ┌──────────┐  ┌───────────────────────────────────────────────────────┐ │
│ │          │  │ ☑ 🖼️ IMG_9555.JPG                                    │ │
│ │  [IMG]   │  │    📁 /Users/rom/Documents/nvq/v2p-formatter-input/  │ │
│ │ THUMB    │  │    IMG_9555.JPG                                       │ │
│ │  120x90  │  │    📊 3.94 MB  |  📐 4000x3000                        │ │
│ │          │  │                                                       │ │
│ └──────────┘  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Details

### Backend Requirements

#### New Route: `/media-converter/thumbnail/<path:file_path>`
- **Purpose**: Serve thumbnail for a file
- **For Images**: Return resized image (120x90 or 240x180)
- **For Videos**: Extract frame at 1 second, return as image
- **Caching**: Cache thumbnails to avoid re-extraction
- **Response**: Image data (JPEG/PNG)

#### Thumbnail Generation
```python
# For images
def generate_image_thumbnail(image_path, size=(120, 90)):
    """Generate thumbnail from image file"""
    # Use Pillow to resize image
    # Return thumbnail bytes

# For videos  
def generate_video_thumbnail(video_path, size=(120, 90), time_seconds=1):
    """Extract frame from video and generate thumbnail"""
    # Use FFmpeg or OpenCV to extract frame
    # Resize to thumbnail size
    # Return thumbnail bytes
```

### Frontend Requirements

#### Thumbnail Loading
```javascript
function loadThumbnail(filePath, fileType) {
    // Show loading spinner
    // Fetch thumbnail from backend
    // Display thumbnail or error state
    // Cache thumbnail URL
}
```

#### Thumbnail Display
```html
<div class="file-thumbnail">
    <img src="/v2p-formatter/media-converter/thumbnail?path=..." 
         alt="Preview" 
         onerror="showThumbnailError()"
         onload="hideThumbnailLoader()">
    <div class="thumbnail-loader">Loading...</div>
    <div class="thumbnail-error">Preview unavailable</div>
</div>
```

---

## Layout Comparison

### Option 1: Horizontal (Recommended)
**Pros:**
- More compact, shows more files in viewport
- Better for scanning many files
- Thumbnail doesn't dominate the card
- Easier to see file details alongside thumbnail

**Cons:**
- Smaller thumbnail size
- Less prominent visual preview

### Option 2: Vertical
**Pros:**
- Larger, more prominent thumbnails
- Better visual identification
- More space for thumbnail detail

**Cons:**
- Takes more vertical space
- Fewer files visible at once
- May require more scrolling

---

## Responsive Behavior

### Desktop (>1024px)
- **Horizontal Layout**: Thumbnail 120x90px, full file details
- **Hover Preview**: Show larger preview on hover

### Tablet (768px - 1024px)
- **Horizontal Layout**: Thumbnail 100x75px, condensed file details
- **Hover Preview**: Optional (may be too small)

### Mobile (<768px)
- **Vertical Layout**: Thumbnail 200x150px, stacked layout
- **No Hover Preview**: Touch devices don't support hover
- **Simplified Details**: Show only essential info

---

## Loading States

### Initial Load
```
┌──────────┐
│          │
│   ⏳     │  Loading spinner animation
│          │
└──────────┘
```

### Loaded
```
┌──────────┐
│          │
│ [IMAGE]  │  Actual thumbnail displayed
│          │
└──────────┘
```

### Error
```
┌──────────┐
│          │
│   🖼️     │  Icon placeholder
│  Error   │  "Preview unavailable"
│          │
└──────────┘
```

---

## Styling Specifications

### Thumbnail Container
- **Width**: 120px (horizontal) or 240px (vertical)
- **Height**: 90px (horizontal) or 180px (vertical)
- **Background**: #1a1a1a (darker than card background)
- **Border**: 1px solid #444
- **Border-radius**: 4px
- **Overflow**: hidden
- **Object-fit**: contain (preserve aspect ratio)
- **Margin**: 8px right (horizontal) or 8px bottom (vertical)

### Thumbnail Image
- **Max-width**: 100%
- **Max-height**: 100%
- **Object-fit**: contain (fit within bounds, preserve ratio)
- **Display**: block

### Loading Spinner
- **Color**: #667eea
- **Size**: 24px
- **Animation**: Rotating
- **Position**: Center of thumbnail container

### Error State
- **Icon**: 🖼️ (images) or 🎬 (videos)
- **Text**: "Preview unavailable"
- **Color**: #999
- **Font-size**: 11px
- **Position**: Center of thumbnail container

---

## Performance Considerations

### Thumbnail Caching
- **Backend Cache**: Store generated thumbnails in cache directory
- **Cache Key**: File path + modification time
- **Cache Duration**: Until file is modified
- **Cache Location**: `static/cache/thumbnails/`

### Lazy Loading
- **Load on Scroll**: Only load thumbnails for visible files
- **Load on Selection**: Load thumbnail when file is selected
- **Progressive Loading**: Load thumbnails in batches

### Thumbnail Size Optimization
- **Small Size**: 120x90px for list view (fast loading)
- **Large Size**: 400x300px for hover preview (on demand)
- **Format**: JPEG for smaller file size
- **Quality**: 75% (balance between quality and size)

---

## User Experience Flow

### 1. Initial Page Load
```
User opens media converter page
  ↓
Files are scanned and listed
  ↓
Thumbnails start loading (lazy load, visible files first)
  ↓
Placeholder shown while loading
  ↓
Thumbnail appears when ready
```

### 2. File Selection
```
User hovers over file card
  ↓
Card highlights (border color change)
  ↓
(Optional) Larger preview appears
  ↓
User clicks to select
  ↓
Card shows selected state
```

### 3. Thumbnail Loading States
```
File card rendered
  ↓
Thumbnail request sent
  ↓
Loading spinner shown
  ↓
Thumbnail received → Display
  OR
Error occurred → Show error state
```

---

## Accessibility

### Alt Text
- **Images**: Use filename as alt text
- **Videos**: Use "Video thumbnail: [filename]"
- **Error State**: "Preview unavailable for [filename]"

### Keyboard Navigation
- **Tab**: Navigate between file cards
- **Enter/Space**: Select/deselect file
- **Arrow Keys**: Navigate between files (optional enhancement)

### Screen Readers
- **Announce**: "File [name], [size], [type], thumbnail [loaded/loading/error]"
- **Selection**: "File [name] selected/unselected"

---

## Questions for Approval

1. **Layout Preference**: 
   - Option 1 (Horizontal) - More compact, better for many files
   - Option 2 (Vertical) - Larger thumbnails, more visual

2. **Thumbnail Size**:
   - Small (120x90px) - Faster loading, more files visible
   - Medium (180x135px) - Better detail, balanced
   - Large (240x180px) - Best detail, fewer files visible

3. **Hover Preview**:
   - Include larger preview on hover? (Yes/No)
   - If yes, what size? (400x300px recommended)

4. **Loading Strategy**:
   - Load all thumbnails immediately? (May be slow)
   - Lazy load (only visible files)? (Recommended)
   - Load on selection only? (Fastest initial load)

5. **Video Thumbnail**:
   - Extract frame at 1 second? (Recommended)
   - Extract first frame? (Faster, may be black)
   - Extract frame at 10% of duration? (More representative)

6. **Error Handling**:
   - Show error icon? (Recommended)
   - Show placeholder image? (Alternative)
   - Hide thumbnail area? (Minimal)

---

## Recommended Implementation

Based on best practices, I recommend:

✅ **Option 1 (Horizontal Layout)** - More practical for file browsing
✅ **Thumbnail Size: 120x90px** - Good balance of detail and performance
✅ **Lazy Loading** - Load thumbnails as files become visible
✅ **Hover Preview: 400x300px** - Show larger preview on hover
✅ **Video Frame: 1 second** - Avoids black frames, shows content
✅ **Error State: Icon + Message** - Clear feedback when preview unavailable
✅ **Caching** - Cache thumbnails to avoid regeneration

---

**End of Wireframe**



