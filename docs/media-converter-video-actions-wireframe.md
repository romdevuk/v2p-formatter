# Media Converter - Video Actions (Trim & Crop) UX Wireframe

## Overview
When a user clicks on a video thumbnail in the Media Converter, an interactive video preview overlay appears with trim and crop actions. The interface is designed to be intuitive, user-friendly, and provide visual feedback during editing operations.

---

## Text Wireframe: Video Actions Interface

### Initial State (Thumbnail View)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                                                                     │ │
│ │                    VIDEO THUMBNAIL                                  │ │
│ │                    (Click to open actions)                          │ │
│ │                                                                     │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ ☑ 🎬 video1.mov                                                         │
│    📁 /input/folder1/video1.mov                                         │
│    📊 245.3 MB  |  🕐 00:05:32  |  📐 1920x1080                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Expanded State (Video Preview with Actions Overlay)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                                                                     │ │
│ │                    VIDEO PLAYER                                     │ │
│ │                    (Playing/Paused)                                 │ │
│ │                                                                     │ │
│ │  ┌─────────────────────────────────────────────────────────────┐  │ │
│ │  │ ⏯ [Play/Pause]  [00:15 / 05:32]  [Volume]  [Fullscreen]    │  │ │
│ │  │ ──────────────────────────────────────────────────────────── │  │ │
│ │  │ ●─────────────────────────○─────────────────────────────── │  │ │
│ │  │ 0:00                      2:45                             5:32 │  │ │
│ │  └─────────────────────────────────────────────────────────────┘  │ │
│ │                                                                     │ │
│ │  ┌─────────────────────────────────────────────────────────────┐  │ │
│ │  │ ✂️ Video Actions                                              │  │ │
│ │  │                                                               │  │ │
│ │  │ [ Trim Video ]  [ Crop Video ]  [ Close ]                    │  │ │
│ │  └─────────────────────────────────────────────────────────────┘  │ │
│ │                                                                     │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ ☑ 🎬 video1.mov                                                         │
│    📁 /input/folder1/video1.mov                                         │
│    📊 245.3 MB  |  🕐 00:05:32  |  📐 1920x1080                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Component Specifications

### 1. Video Preview Overlay

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                                                                 │ │
│  │              VIDEO PLAYER (Centered, Max 80% viewport)          │ │
│  │                                                                 │ │
│  │  ┌─────────────────────────────────────────────────────────┐  │ │
│  │  │ Video Controls Bar (Bottom overlay)                     │  │ │
│  │  └─────────────────────────────────────────────────────────┘  │ │
│  │                                                                 │ │
│  │  ┌─────────────────────────────────────────────────────────┐  │ │
│  │  │ Actions Panel (Bottom, below controls)                   │  │ │
│  │  └─────────────────────────────────────────────────────────┘  │ │
│  │                                                                 │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  [X Close] (Top-right corner)                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Video Controls Bar
```
┌─────────────────────────────────────────────────────────────────────────┐
│ ⏯ [Play/Pause]  │  [00:15 / 05:32]  │  🔊 [Volume]  │  ⛶ [Fullscreen] │
│ ────────────────────────────────────────────────────────────────────── │
│ ●─────────────────────────○─────────────────────────────────────────── │
│ 0:00                      2:45                                       5:32 │
│ [Start Trim]              [End Trim]                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

**Components:**
- **Play/Pause Button**: Toggle video playback
- **Time Display**: Current time / Total duration (MM:SS format)
- **Progress Scrubber**: Interactive timeline with draggable handle
- **Volume Control**: Mute/Unmute toggle
- **Fullscreen Button**: Expand video to fullscreen
- **Trim Markers**: Visual indicators for trim start/end points (when trim mode active)

---

### 2. Actions Panel

#### Default State (Actions Selection)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ ✂️ Video Actions                                                         │
│                                                                         │
│ ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│ │                  │  │                  │  │                  │     │
│ │   ✂️ Trim        │  │   ✂️ Crop        │  │   ✕ Close        │     │
│ │                  │  │                  │  │                  │     │
│ │  Cut video to    │  │  Select region   │  │  Close preview   │     │
│ │  time range      │  │  to keep         │  │                   │     │
│ │                  │  │                  │  │                  │     │
│ └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Trim Mode Active
```
┌─────────────────────────────────────────────────────────────────────────┐
│ ✂️ Trim Video                                                           │
│                                                                         │
│ ┌───────────────────────────────────────────────────────────────────┐ │
│ │ Timeline with Trim Range Selection                                │ │
│ │                                                                   │ │
│ │ ──[●]───────────────────[●]─────────────────────────────────── │ │
│ │ Start                    End                                      │ │
│ │ 00:15                    02:45                                     │ │
│ └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ Start Time: [00:15]  End Time: [02:45]  Duration: 02:30                │
│                                                                         │
│ ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│ │   Set Start      │  │   Set End        │  │   Reset         │     │
│ │   (Current Pos)  │  │   (Current Pos)  │  │                  │     │
│ └──────────────────┘  └──────────────────┘  └──────────────────┘     │
│                                                                         │
│ ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│ │   Cancel        │  │   Preview Trim   │  │   Apply Trim    │     │
│ └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

**Trim Controls:**
- **Timeline Visualization**: Shows full video with highlighted trim region
- **Start/End Markers**: Draggable handles on timeline
- **Set Start/End Buttons**: Set trim points to current playback position
- **Time Inputs**: Manual entry for precise timing
- **Duration Display**: Shows calculated trimmed duration
- **Preview Trim**: Play only the trimmed section
- **Apply Trim**: Execute trim operation and save
- **Reset**: Clear trim selection
- **Cancel**: Exit trim mode

#### Crop Mode Active
```
┌─────────────────────────────────────────────────────────────────────────┐
│ ✂️ Crop Video                                                           │
│                                                                         │
│ ┌───────────────────────────────────────────────────────────────────┐ │
│ │ Video Preview with Crop Overlay                                    │ │
│ │                                                                   │ │
│ │  ┌─────────────────────────────────────────────────────────────┐ │ │
│ │  │                                                               │ │ │
│ │  │  ┌───────────────────────────────────────────────────────┐  │ │ │
│ │  │  │                                                       │  │ │ │
│ │  │  │         CROP REGION (Resizable/Draggable)            │  │ │ │
│ │  │  │                                                       │  │ │ │
│ │  │  └───────────────────────────────────────────────────────┘  │ │ │
│ │  │                                                               │ │ │
│ │  └─────────────────────────────────────────────────────────────┘ │ │
│ └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ Position: X [  0]  Y [  0]  Size: Width [1920]  Height [1080]          │
│                                                                         │
│ ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│ │   Center Crop    │  │   Reset          │  │   Aspect Ratio   │     │
│ │                  │  │                  │  │   [16:9 ▼]       │     │
│ └──────────────────┘  └──────────────────┘  └──────────────────┘     │
│                                                                         │
│ ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│ │   Cancel        │  │   Preview Crop   │  │   Apply Crop    │     │
│ └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

**Crop Controls:**
- **Interactive Crop Overlay**: Resizable and draggable rectangle on video
- **Position Inputs**: X, Y coordinates (top-left corner)
- **Size Inputs**: Width and Height in pixels
- **Center Crop Button**: Center crop region in video
- **Aspect Ratio Presets**: 16:9, 4:3, 1:1, Original, Custom
- **Reset Button**: Clear crop selection
- **Preview Crop**: Show cropped region only
- **Apply Crop**: Execute crop operation and save
- **Cancel**: Exit crop mode

---

## User Interaction Flow

### Flow 1: Trim Video
```
1. User clicks video thumbnail
   ↓
2. Video preview overlay appears with video playing
   ↓
3. User clicks "Trim Video" button
   ↓
4. Trim mode activates:
   - Timeline shows trim markers
   - Video controls remain active
   - Trim panel appears below video
   ↓
5. User sets trim points:
   Option A: Drag markers on timeline
   Option B: Play video, click "Set Start" / "Set End" at desired times
   Option C: Manually enter times in input fields
   ↓
6. User clicks "Preview Trim" to see trimmed section
   ↓
7. User clicks "Apply Trim"
   ↓
8. Processing indicator appears
   ↓
9. Success message with output file path
   ↓
10. Overlay closes, file list refreshes
```

### Flow 2: Crop Video
```
1. User clicks video thumbnail
   ↓
2. Video preview overlay appears with video playing
   ↓
3. User clicks "Crop Video" button
   ↓
4. Crop mode activates:
   - Crop overlay rectangle appears on video
   - Video controls remain active
   - Crop panel appears below video
   ↓
5. User adjusts crop region:
   Option A: Drag corners/edges of overlay rectangle
   Option B: Drag entire rectangle to reposition
   Option C: Enter values in position/size inputs
   Option D: Select aspect ratio preset
   ↓
6. User clicks "Preview Crop" to see cropped region
   ↓
7. User clicks "Apply Crop"
   ↓
8. Processing indicator appears
   ↓
9. Success message with output file path
   ↓
10. Overlay closes, file list refreshes
```

---

## Visual Design Specifications

### Color Scheme
- **Background Overlay**: `rgba(0, 0, 0, 0.85)` - Dark semi-transparent
- **Video Container**: `#1e1e1e` - Dark background
- **Controls Bar**: `rgba(0, 0, 0, 0.9)` - Near-black with transparency
- **Actions Panel**: `#2a2a2a` - Dark gray
- **Primary Buttons**: `#667eea` - Purple accent
- **Secondary Buttons**: `#2a2a2a` - Dark gray
- **Text**: `#e0e0e0` - Light gray
- **Trim Markers**: `#51cf66` - Green for active
- **Crop Overlay**: `rgba(102, 126, 234, 0.3)` - Purple with transparency
- **Crop Border**: `#667eea` - Purple solid

### Typography
- **Headers**: 18px, bold, `#e0e0e0`
- **Labels**: 14px, regular, `#e0e0e0`
- **Inputs**: 14px, regular, `#e0e0e0`
- **Buttons**: 14px, medium, white/purple
- **Time Display**: 12px, monospace, `#999`

### Spacing
- **Panel Padding**: 20px
- **Button Spacing**: 10px gap
- **Section Margin**: 15px between sections
- **Input Field Height**: 40px
- **Button Height**: 40px

### Interactive Elements

#### Buttons
- **Primary Action**: Purple background (`#667eea`), white text, rounded corners (4px)
- **Secondary Action**: Dark gray background (`#2a2a2a`), light text, border
- **Hover State**: Slightly lighter background, scale 1.02
- **Active State**: Slightly darker background
- **Disabled State**: 50% opacity, no pointer events

#### Input Fields
- **Background**: `#2a2a2a`
- **Border**: `1px solid #555`
- **Focus State**: Border color `#667eea`, outline none
- **Placeholder**: `#999`

#### Timeline Scrubber
- **Track**: `#555` background, 6px height
- **Progress**: `#667eea` gradient, 6px height
- **Handle**: White circle, 14px diameter, shadow
- **Hover**: Handle scales to 16px
- **Active**: Handle scales to 18px

---

## Responsive Behavior

### Desktop (≥1024px)
- Video preview: Max 80% viewport width, maintains aspect ratio
- Actions panel: Full width below video
- Controls: Horizontal layout, all visible

### Tablet (768px - 1023px)
- Video preview: Max 90% viewport width
- Actions panel: Full width, stacked buttons if needed
- Controls: Horizontal layout, slightly smaller

### Mobile (<768px)
- Video preview: Full width minus padding
- Actions panel: Full width, buttons stack vertically
- Controls: Simplified, essential controls only
- Trim/Crop overlays: Touch-optimized with larger hit areas

---

## Accessibility Features

1. **Keyboard Navigation**:
   - Tab through all interactive elements
   - Enter/Space to activate buttons
   - Arrow keys to adjust scrubber position
   - Escape to close overlay

2. **Screen Reader Support**:
   - ARIA labels on all buttons
   - Live regions for status updates
   - Descriptive button text

3. **Visual Feedback**:
   - Clear focus indicators
   - High contrast text
   - Loading states for async operations

4. **Error Handling**:
   - Clear error messages
   - Validation feedback on inputs
   - Graceful degradation if video fails to load

---

## Technical Implementation Notes

### Video Player Integration
- Use HTML5 `<video>` element with controls
- Custom controls overlay for better UX
- Support for common video formats (MP4, MOV)

### Trim Implementation
- Use FFmpeg `-ss` (start) and `-t` (duration) flags
- Validate trim points against video duration
- Show preview of trimmed section before applying

### Crop Implementation
- Use FFmpeg `crop` filter: `crop=width:height:x:y`
- Validate crop region against video dimensions
- Maintain aspect ratio option
- Show preview of cropped region before applying

### State Management
- Track current mode: `none`, `trim`, `crop`
- Store trim/crop parameters in state
- Reset state when closing overlay
- Persist settings during preview

### Performance Considerations
- Lazy load video preview (only when thumbnail clicked)
- Debounce input changes for real-time updates
- Show loading indicators during processing
- Handle large video files gracefully

---

## Approval Checklist

- [ ] Video preview overlay design approved
- [ ] Trim interface layout approved
- [ ] Crop interface layout approved
- [ ] Color scheme approved
- [ ] Typography approved
- [ ] Interaction flow approved
- [ ] Responsive behavior approved
- [ ] Accessibility features approved

---

## Version History

- **v1.0** (2024): Initial wireframe design
  - Video preview overlay
  - Trim and crop action interfaces
  - User interaction flows
  - Visual design specifications


