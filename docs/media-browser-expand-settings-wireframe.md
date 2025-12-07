# Media Browser Expand & Settings - Text Wireframe

## Overview
This wireframe specifies enhancements to the floating media browser panel, including:
1. Full-screen expand/collapse functionality
2. Configurable thumbnails per row setting (when collapsed)
3. Configurable thumbnail size setting

## Version
**1.0.0** - Initial Specification

---

## 1. Functional Requirements

### 1.1 Full-Screen Expand/Collapse
- **Requirement**: Media browser can expand to full screen width
- **Behavior**: Toggle between collapsed (50% width) and expanded (100% width) states
- **Trigger**: Button in media browser header
- **State Persistence**: Expanded/collapsed state saved in localStorage
- **Visual Feedback**: Clear indication of expanded vs collapsed state

### 1.2 Thumbnails Per Row Setting
- **Requirement**: User can configure how many thumbnails display per row when collapsed
- **Options**: 2, 3, 4, 5, or 6 thumbnails per row
- **Default**: 3 thumbnails per row
- **Scope**: Applies only when browser is in collapsed state
- **Storage**: Setting saved in localStorage

### 1.3 Thumbnail Size Setting
- **Requirement**: User can configure thumbnail size
- **Options**: Small, Medium, Large, or Extra Large
- **Default**: Medium
- **Scope**: Applies in both collapsed and expanded states
- **Storage**: Setting saved in localStorage

---

## 2. Text Wireframe: UI Layout

### 2.1 Media Browser Header (Collapsed State)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MEDIA BROWSER (Collapsed - 50% width)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ 📊 24 files                              [⚙️ Settings] [⬛ Expand] │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ Media Thumbnails (3 columns - configurable)                        │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │IMG │ │IMG │ │VID │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐                                              │  │
│ │ │VID │ │IMG │ │IMG │                                              │  │
│ │ └────┘ └────┘ └────┘                                              │  │
│ │                                                                     │  │
│ │ [Scroll within panel ↓]                                            │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Media Browser Header (Expanded State)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MEDIA BROWSER (Expanded - 100% width, covers right panel)              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ 📊 24 files                              [⚙️ Settings] [⬜ Collapse]│  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ Media Thumbnails (More columns - configurable)                     │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐         │  │
│ │ │IMG │ │IMG │ │VID │ │IMG │ │VID │ │IMG │ │IMG │ │VID │         │  │
│ │ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘         │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐         │  │
│ │ │VID │ │IMG │ │IMG │ │VID │ │IMG │ │IMG │ │VID │ │IMG │         │  │
│ │ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘         │  │
│ │                                                                     │  │
│ │ [Scroll within panel ↓]                                            │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Settings Panel (Modal/Dropdown)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Media Browser Settings                                     [✕ Close]   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ Thumbnails Per Row (when collapsed):                               │  │
│ │                                                                     │  │
│ │ ○ 2 columns    ○ 3 columns    ● 4 columns    ○ 5 columns    ○ 6   │  │
│ │                                                                     │  │
│ │ Current: 3 columns (applies when collapsed only)                   │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ Thumbnail Size:                                                    │  │
│ │                                                                     │  │
│ │ ○ Small (120x90)    ● Medium (240x180)    ○ Large (360x270)       │  │
│ │ ○ Extra Large (480x360)                                          │  │
│ │                                                                     │  │
│ │ Preview: ┌────┐                                                     │  │
│ │         │ IMG │  (shows current size)                               │  │
│ │         └────┘                                                      │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │                     [Cancel]  [Apply Settings]                      │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.4 Settings Panel (Inline/Compact Version)

**Alternative: Settings dropdown (less intrusive)**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MEDIA BROWSER                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ 📊 24 files                                                         │  │
│ │                                                                     │  │
│ │ ┌── Settings ─────────────────────────────────────────────┐        │  │
│ │ │ Thumbnails/Row: [3 ▼]  Size: [Medium ▼]  [⬛ Expand]   │        │  │
│ │ └──────────────────────────────────────────────────────────┘        │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│ [Thumbnail grid with applied settings]                                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Behavior Specifications

### 3.1 Expand/Collapse Button

#### Button States
```
Collapsed State:
┌────────────────────────┐
│  ⬛ Expand              │  (Icon: square/frame indicating "expand to full")
└────────────────────────┘

Expanded State:
┌────────────────────────┐
│  ⬜ Collapse            │  (Icon: overlapping squares indicating "collapse")
└────────────────────────┘
```

#### Behavior
- **Click to Expand**: 
  - Media browser expands to 100% viewport width
  - Right panel (Live Preview) is hidden/covered
  - Button changes to "Collapse"
  - Grid automatically adjusts to show more columns
  
- **Click to Collapse**: 
  - Media browser returns to 50% viewport width
  - Right panel becomes visible again
  - Button changes to "Expand"
  - Grid returns to configured columns (from settings)

#### Transitions
- Smooth width transition (e.g., 300ms ease-in-out)
- Right panel fades out/in or slides

### 3.2 Thumbnails Per Row Setting

#### Options
```
┌─────────────────────────────────────┐
│ Thumbnails Per Row (collapsed):     │
│                                      │
│ [ ] 2 columns   (wider thumbnails)  │
│ [ ] 3 columns   (default)           │
│ [•] 4 columns   (more per row)      │
│ [ ] 5 columns   (compact)           │
│ [ ] 6 columns   (very compact)      │
└─────────────────────────────────────┘
```

#### Implementation
- **CSS Grid**: Use `grid-template-columns: repeat(N, 1fr)` where N = selected value
- **Collapsed State Only**: Setting only applies when browser is collapsed (50% width)
- **Expanded State**: Automatically calculates optimal columns based on viewport width
- **Default**: 3 columns

#### Visual Impact
```
2 columns:  ┌────────┐ ┌────────┐
            │  Wide  │ │  Wide  │
            └────────┘ └────────┘

3 columns:  ┌──────┐ ┌──────┐ ┌──────┐
            │  Med │ │  Med │ │  Med │
            └──────┘ └──────┘ └──────┘

4 columns:  ┌────┐ ┌────┐ ┌────┐ ┌────┐
            │ Sm │ │ Sm │ │ Sm │ │ Sm │
            └────┘ └────┘ └────┘ └────┘
```

### 3.3 Thumbnail Size Setting

#### Options
```
┌─────────────────────────────────────┐
│ Thumbnail Size:                     │
│                                      │
│ [ ] Small      (120x90 pixels)      │
│ [•] Medium     (240x180 pixels)     │
│ [ ] Large      (360x270 pixels)     │
│ [ ] Extra Large (480x360 pixels)    │
└─────────────────────────────────────┘
```

#### Backend Impact
- **Thumbnail Generation**: Backend generates thumbnails at requested size
- **Caching**: Different cache keys for different sizes
- **Quality**: Maintains 100% quality setting
- **URL Parameter**: `/thumbnail?path=...&size=240x180`

#### Visual Sizes
```
Small (120x90):      ┌────┐
                     │    │  Tiny, many visible
                     └────┘

Medium (240x180):    ┌────────┐
                     │        │  Balanced (default)
                     │        │
                     └────────┘

Large (360x270):     ┌─────────────┐
                     │             │  Larger, fewer visible
                     │             │
                     │             │
                     └─────────────┘

Extra Large (480x360): ┌─────────────────┐
                       │                 │  Very large
                       │                 │
                       │                 │
                       │                 │
                       └─────────────────┘
```

---

## 4. Settings Panel Design Options

### 4.1 Option A: Modal Dialog (Recommended)

**Pros:**
- Clean, focused interface
- Room for previews and descriptions
- Clear separation of settings from main UI

**Cons:**
- Requires click to open/close
- More intrusive

**Layout:**
```
┌────────────────────────────────────────────┐
│  Media Browser Settings          [✕]       │
├────────────────────────────────────────────┤
│                                            │
│  [Settings content as shown above]         │
│                                            │
│  [Preview area]                            │
│                                            │
│  [Cancel] [Apply]                          │
└────────────────────────────────────────────┘
```

### 4.2 Option B: Dropdown Panel

**Pros:**
- Less intrusive
- Quick access
- No modal overlay

**Cons:**
- Less space for options
- Can feel cramped

**Layout:**
```
┌─────────────────────────────────────┐
│ 📊 24 files  [⚙️ Settings ▼]        │
│                                      │
│ ┌─────────────────────────────────┐ │
│ │ ⚙️ Settings                     │ │
│ │                                 │ │
│ │ Thumbnails/Row: [3 ▼]          │ │
│ │ Size: [Medium ▼]                │ │
│ │                                 │ │
│ │ [Apply]                         │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### 4.3 Option C: Inline Controls

**Pros:**
- Always visible
- No clicks needed
- Immediate feedback

**Cons:**
- Takes up header space
- Can feel cluttered

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│ 📊 24 files  Thumbnails: [3 ▼]  Size: [Med ▼] [⬛] │
└─────────────────────────────────────────────────────┘
```

**Recommendation**: **Option A (Modal Dialog)** for cleaner UX with preview capability

---

## 5. Expand/Collapse Behavior Details

### 5.1 Expanded State Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FULL VIEWPORT WIDTH                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ 📊 24 files              [⚙️ Settings]  [⬜ Collapse]              │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ Media Thumbnails                                                   │  │
│ │                                                                     │  │
│ │ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐         │  │
│ │ │    │ │    │ │    │ │    │ │    │ │    │ │    │ │    │         │  │
│ │ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘         │  │
│ │                                                                     │  │
│ │ (More columns based on viewport width and thumbnail size)          │  │
│ └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Collapsed State Layout

```
┌──────────────┬──────────────────────────────────────────────────────────┐
│              │                                                           │
│  MEDIA       │  LIVE PREVIEW & TEXT EDITOR                              │
│  BROWSER     │                                                           │
│  (50% width) │  (50% width)                                             │
│              │                                                           │
│ ┌──────────┐ │ ┌──────────────────────────────────────────────────────┐ │
│ │ 📊 24    │ │ │ Live Preview                                         │ │
│ │ [⚙️] [⬛]│ │ │                                                      │ │
│ └──────────┘ │ │ [Content...]                                         │ │
│              │ └──────────────────────────────────────────────────────┘ │
│ ┌──────────┐ │                                                           │
│ │ ┌──┐┌──┐│ │ ┌──────────────────────────────────────────────────────┐ │
│ │ │  ││  ││ │ │ Text Editor                                          │ │
│ │ └──┘└──┘│ │ │                                                      │ │
│ │ ┌──┐┌──┐│ │ │ [Text content...]                                    │ │
│ │ │  ││  ││ │ └──────────────────────────────────────────────────────┘ │
│ │ └──┘└──┘│ │                                                           │
│ └──────────┘ │                                                           │
│              │                                                           │
└──────────────┴──────────────────────────────────────────────────────────┘
```

### 5.3 Transition Animation

```
Collapsed → Expanded:
┌──────────────┬──────────────┐
│  50%         │  50%         │
└──────────────┴──────────────┘
        ↓ (300ms transition)
┌──────────────────────────────┐
│         100%                 │
└──────────────────────────────┘

Expanded → Collapsed:
┌──────────────────────────────┐
│         100%                 │
└──────────────────────────────┘
        ↓ (300ms transition)
┌──────────────┬──────────────┐
│  50%         │  50%         │
└──────────────┴──────────────┘
```

---

## 6. Settings Storage and Persistence

### 6.1 LocalStorage Keys

```javascript
{
  "mediaBrowser.expanded": true/false,           // Expanded state
  "mediaBrowser.thumbnailsPerRow": 3,            // 2-6 columns
  "mediaBrowser.thumbnailSize": "medium"         // small/medium/large/xlarge
}
```

### 6.2 Default Values

```javascript
{
  "mediaBrowser.expanded": false,
  "mediaBrowser.thumbnailsPerRow": 3,
  "mediaBrowser.thumbnailSize": "medium"
}
```

### 6.3 Settings Applied On

- **Page Load**: Read from localStorage and apply
- **Settings Change**: Save to localStorage immediately
- **Expand/Collapse**: Save expanded state immediately

---

## 7. Technical Implementation Details

### 7.1 CSS Grid for Columns

#### Collapsed State (User-Controlled)
```css
.observation-media-grid.collapsed {
    grid-template-columns: repeat(3, 1fr); /* From settings: 2-6 */
}
```

#### Expanded State (Auto-Calculated)
```css
.observation-media-grid.expanded {
    /* Auto-calculate based on viewport width and thumbnail size */
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
}
```

### 7.2 Thumbnail Size Mapping

```javascript
const thumbnailSizes = {
    "small": { width: 120, height: 90, size: "120x90" },
    "medium": { width: 240, height: 180, size: "240x180" },
    "large": { width: 360, height: 270, size: "360x270" },
    "xlarge": { width: 480, height: 360, size: "480x360" }
};
```

### 7.3 Backend Thumbnail URL

```javascript
// Thumbnail URL generation
const sizeStr = thumbnailSizes[selectedSize].size;
const thumbnailUrl = `/v2p-formatter/media-converter/thumbnail?path=${encodeURIComponent(media.path)}&size=${sizeStr}`;
```

### 7.4 Expand/Collapse JavaScript

```javascript
function toggleMediaBrowserExpand() {
    const leftPanel = document.querySelector('.observation-media-left-panel');
    const rightPanel = document.querySelector('.observation-media-right-panel');
    const isExpanded = leftPanel.classList.contains('expanded');
    
    if (isExpanded) {
        // Collapse: return to 50% width
        leftPanel.classList.remove('expanded');
        rightPanel.style.display = 'block';
        updateFloatingPanelOffset(); // Recalculate position
    } else {
        // Expand: go to 100% width
        leftPanel.classList.add('expanded');
        rightPanel.style.display = 'none';
        updateFloatingPanelOffset(); // Recalculate position
    }
    
    // Save state
    localStorage.setItem('mediaBrowser.expanded', !isExpanded);
}
```

---

## 8. User Experience Flow

### 8.1 First-Time User

1. **Page Loads**: Media browser appears in collapsed state (50% width)
2. **Default Settings**: 3 columns, Medium thumbnails
3. **User Clicks Expand**: Browser expands to full screen
4. **User Clicks Settings**: Settings panel opens
5. **User Changes Settings**: Changes applied immediately
6. **Settings Saved**: Preferences saved to localStorage

### 8.2 Returning User

1. **Page Loads**: Settings read from localStorage
2. **State Restored**: 
   - Expanded/collapsed state restored
   - Column count restored
   - Thumbnail size restored
3. **Immediate Application**: Settings applied on page load

### 8.3 Settings Change Flow

```
User clicks Settings button
    ↓
Settings panel opens
    ↓
User changes "Thumbnails Per Row" to 4
    ↓
Preview updates (if available)
    ↓
User clicks "Apply Settings"
    ↓
Settings saved to localStorage
    ↓
Grid layout updates immediately
    ↓
Settings panel closes
```

---

## 9. Visual Design Specifications

### 9.1 Expand/Collapse Button

```
┌──────────────────────────┐
│ Icon    Text             │
│  ⬛     Expand            │
└──────────────────────────┘

Hover State:
┌──────────────────────────┐
│ Icon    Text             │
│  ⬛     Expand            │  (Highlighted background)
└──────────────────────────┘
```

**Button Styling:**
- Background: `#555` (normal), `#667eea` (hover)
- Color: White text
- Border: 1px solid `#555`
- Border-radius: 4px
- Padding: 8px 16px
- Icon: Unicode symbols or SVG icons

### 9.2 Settings Button

```
┌──────────────────────────┐
│  ⚙️  Settings            │
└──────────────────────────┘
```

**Button Styling:**
- Same as Expand button
- Icon: Gear/settings icon (⚙️)

### 9.3 Settings Panel

**Modal Overlay:**
- Background: `rgba(0, 0, 0, 0.7)` (semi-transparent)
- Z-index: 1000 (above floating panel)

**Modal Content:**
- Background: `#2a2a2a`
- Border: 1px solid `#555`
- Border-radius: 8px
- Padding: 20px
- Width: 500px (desktop)
- Max-width: 90vw (mobile)

---

## 10. Responsive Behavior

### 10.1 Desktop (≥1024px)

- **Collapsed**: 50% width, user-controlled columns (2-6)
- **Expanded**: 100% width, auto-calculated columns
- **Settings**: Modal dialog
- **Full functionality**: All features available

### 10.2 Tablet (768px - 1023px)

- **Collapsed**: 50% width (may stack on small tablets)
- **Expanded**: 100% width
- **Settings**: Modal dialog (slightly smaller)
- **Limited columns**: Max 4-5 columns practical

### 10.3 Mobile (<768px)

- **Always Full Width**: No collapse/expand (always 100%)
- **Settings**: Full-screen modal or bottom sheet
- **Limited columns**: Max 2-3 columns practical
- **Touch-friendly**: Larger buttons and controls

---

## 11. Edge Cases and Considerations

### 11.1 Very Wide Viewport

**Scenario**: User has ultra-wide monitor (2560px+)
- **Collapsed**: Still 50% width (1280px+ is plenty)
- **Expanded**: Can show 8-10+ columns
- **Consideration**: May need max column limit or auto-sizing

### 11.2 Very Narrow Viewport

**Scenario**: User resizes window to very narrow (400px)
- **Behavior**: Always full width, max 2 columns
- **Settings**: Full-screen modal or bottom sheet
- **Consideration**: Hide expand button on very small screens

### 11.3 Many Media Files

**Scenario**: 100+ media files in grid
- **Performance**: Lazy loading or virtual scrolling may be needed
- **Grid**: Works fine with any number of files
- **Consideration**: Monitor scroll performance

### 11.4 Thumbnail Size Changes

**Scenario**: User changes thumbnail size from Medium to Large
- **Behavior**: 
  - Backend generates new thumbnails at new size
  - Cache key includes size, so new thumbnails generated
  - Grid may show fewer columns due to larger thumbnails
- **Loading**: Show loading indicators while new thumbnails generate

---

## 12. Implementation Checklist

### 12.1 Expand/Collapse Functionality

- [ ] Add expand/collapse button to media browser header
- [ ] Implement toggle functionality (JavaScript)
- [ ] Add CSS classes for expanded/collapsed states
- [ ] Implement width transitions (CSS animations)
- [ ] Hide/show right panel on expand/collapse
- [ ] Save expanded state to localStorage
- [ ] Restore expanded state on page load
- [ ] Update grid column calculation for expanded state

### 12.2 Thumbnails Per Row Setting

- [ ] Add setting option to settings panel
- [ ] Create radio buttons or dropdown (2-6 options)
- [ ] Update CSS grid columns based on selection
- [ ] Apply setting only when collapsed
- [ ] Save setting to localStorage
- [ ] Restore setting on page load
- [ ] Add visual preview (optional)

### 12.3 Thumbnail Size Setting

- [ ] Add setting option to settings panel
- [ ] Create radio buttons or dropdown (4 size options)
- [ ] Update thumbnail URL generation to include size
- [ ] Update backend to handle new size requests
- [ ] Update cache key generation to include size
- [ ] Save setting to localStorage
- [ ] Restore setting on page load
- [ ] Add size preview in settings panel

### 12.4 Settings Panel

- [ ] Design settings panel UI (modal or dropdown)
- [ ] Implement open/close functionality
- [ ] Add settings controls (radio buttons, dropdowns)
- [ ] Implement "Apply" and "Cancel" buttons
- [ ] Add settings preview (optional)
- [ ] Style settings panel to match app theme
- [ ] Make settings panel responsive

### 12.5 Testing Requirements

- [ ] Test expand/collapse on different screen sizes
- [ ] Test thumbnail size changes with many files
- [ ] Test columns setting with different thumbnail sizes
- [ ] Test settings persistence (localStorage)
- [ ] Test settings restoration on page reload
- [ ] Test responsive behavior (desktop/tablet/mobile)
- [ ] Test performance with 100+ media files
- [ ] Test transitions and animations

---

## 13. Questions for Approval

1. **Settings Panel Type**: Modal dialog or dropdown?
   - Recommendation: Modal dialog for better UX

2. **Thumbnail Sizes**: Are the 4 size options sufficient?
   - Recommendation: Start with 4, can add more later

3. **Columns in Expanded State**: Auto-calculate or user-configurable?
   - Recommendation: Auto-calculate based on viewport width

4. **Preview in Settings**: Should settings panel show live preview?
   - Recommendation: Yes, but optional (can be added later)

5. **Default Settings**: Are the defaults (3 columns, Medium size) appropriate?
   - Recommendation: Yes, these are good defaults

6. **Expand Button Position**: Top-right corner of header?
   - Recommendation: Yes, alongside Settings button

---

## 14. Approval Checklist

- [ ] Expand/collapse functionality approved
- [ ] Thumbnails per row setting approved (2-6 options)
- [ ] Thumbnail size setting approved (4 size options)
- [ ] Settings panel design approved (modal vs dropdown)
- [ ] Button placement and styling approved
- [ ] Default values approved
- [ ] Responsive behavior approved
- [ ] Implementation approach approved

---

**Document Status**: Draft - Awaiting Approval  
**Last Updated**: [Current Date]  
**Author**: AI Assistant  
**Reviewer**: [Pending]


