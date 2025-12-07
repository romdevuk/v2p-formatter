# Floating Media Browser Panel - Text Wireframe

## Overview
This wireframe specifies the implementation of a floating/sticky media browser panel that remains visible on screen when scrolling the page down. The media browser (left panel) will stay fixed in position while the preview and text editor (right panel) can scroll independently.

## Version
**1.0.0** - Initial Specification

---

## 1. Functional Requirements

### 1.1 Floating/Sticky Behavior
- **Requirement**: Media browser panel stays fixed on screen when scrolling page vertically
- **Position**: Fixed to viewport (not page content)
- **Visibility**: Always visible when scrolling down
- **Interaction**: Media browser remains fully interactive (click, drag, scroll within panel)

### 1.2 Scroll Behavior
- **Page Scroll**: When user scrolls page down, media browser stays at same screen position
- **Panel Scroll**: Media browser panel can scroll independently (for browsing media)
- **Right Panel**: Preview and editor scroll with page content normally

### 1.3 Responsive Behavior
- **Desktop**: Floating panel works as specified
- **Tablet**: Floating panel adapts to smaller screens
- **Mobile**: May need different behavior (stack or hide) - to be determined

---

## 2. Text Wireframe: Current Layout vs. Proposed Layout

### 2.1 Current Layout (Static Split-Panel)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Navigation Tabs                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌──────────────────────────────────┬──────────────────────────────────┐ │
│ │                                  │                                  │ │
│ │   LEFT PANEL                     │   RIGHT PANEL                    │ │
│ │   Media Browser                  │   Text Editor & Preview         │ │
│ │   (50% width, scrolls with page) │   (50% width, scrolls with page)│ │
│ │                                  │                                  │ │
│ │ ┌──────────────────────────────┐ │ ┌──────────────────────────────┐ │ │
│ │ │ 📁 Subfolder: [Select... ▼] │ │ │ 📄 Live Preview              │ │ │
│ │ │ 📊 24 files                  │ │ │ ┌──────────────────────────┐ │ │ │
│ │ └──────────────────────────────┘ │ │ │                          │ │ │ │
│ │                                  │ │ │ │  Observation Report      │ │ │ │
│ │ ┌──────────────────────────────┐ │ │ │ │  Site: Construction      │ │ │ │
│ │ │ Media Thumbnails (3 columns) │ │ │ │ │                          │ │ │ │
│ │ │                              │ │ │ │ │  {{Section1}}            │ │ │ │
│ │ │ ┌────┐ ┌────┐ ┌────┐       │ │ │ │ │                          │ │ │ │
│ │ │ │IMG │ │IMG │ │VID │       │ │ │ │ │                          │ │ │ │
│ │ │ └────┘ └────┘ └────┘       │ │ │ │ │  [Scroll down...]        │ │ │ │
│ │ │                              │ │ │ │ │                          │ │ │ │
│ │ │ ┌────┐ ┌────┐ ┌────┐       │ │ │ │ │                          │ │ │ │
│ │ │ │VID │ │IMG │ │IMG │       │ │ │ │ │                          │ │ │ │
│ │ │ └────┘ └────┘ └────┘       │ │ │ │ │                          │ │ │ │
│ │ │                              │ │ │ │ │                          │ │ │ │
│ │ │ [Scroll within panel]        │ │ │ │ │                          │ │ │ │
│ │ └──────────────────────────────┘ │ │ │ └──────────────────────────┘ │ │ │
│ │                                  │ │ │                                  │ │ │
│ │                                  │ │ │ ┌──────────────────────────────┐ │ │ │
│ │                                  │ │ │ │ 📝 Text Editor               │ │ │ │
│ │                                  │ │ │ │ ┌──────────────────────────┐ │ │ │
│ │                                  │ │ │ │ │                          │ │ │ │
│ │                                  │ │ │ │ │  [Long text content...]  │ │ │ │
│ │                                  │ │ │ │ │                          │ │ │ │
│ │                                  │ │ │ │ │  [Scroll down...]        │ │ │ │
│ │                                  │ │ │ │ │                          │ │ │ │
│ │                                  │ │ │ │ └──────────────────────────┘ │ │ │
│ │                                  │ │ │ └──────────────────────────────┘ │ │ │
│ │                                  │ │ │                                  │ │ │
│ └──────────────────────────────────┴──────────────────────────────────┘ │
│                                                                          │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Actions: [Save DOCX] [Save Draft] [Load Draft]                      │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│ [Page scrolls down...]                                                   │
│                                                                          │
│ (Both panels scroll together with page)                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Proposed Layout (Floating Media Browser)

#### Initial State (No Scrolling)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Navigation Tabs                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌──────────────────────────────────┬──────────────────────────────────┐ │
│ │                                  │                                  │ │
│ │   LEFT PANEL (FLOATING)          │   RIGHT PANEL                    │ │
│ │   Media Browser                  │   Text Editor & Preview         │ │
│ │   (Sticky/Fixed position)        │   (Scrolls with page)           │ │
│ │                                  │                                  │ │
│ │ ┌──────────────────────────────┐ │ ┌──────────────────────────────┐ │ │
│ │ │ 📁 Subfolder: [Select... ▼] │ │ │ 📄 Live Preview              │ │ │
│ │ │ 📊 24 files                  │ │ │ ┌──────────────────────────┐ │ │ │
│ │ └──────────────────────────────┘ │ │ │                          │ │ │ │
│ │                                  │ │ │ │  Observation Report      │ │ │ │
│ │ ┌──────────────────────────────┐ │ │ │ │  Site: Construction      │ │ │ │
│ │ │ Media Thumbnails (3 columns) │ │ │ │ │                          │ │ │ │
│ │ │                              │ │ │ │ │  {{Section1}}            │ │ │ │
│ │ │ ┌────┐ ┌────┐ ┌────┐       │ │ │ │ │                          │ │ │ │
│ │ │ │IMG │ │IMG │ │VID │       │ │ │ │ │                          │ │ │ │
│ │ │ └────┘ └────┘ └────┘       │ │ │ │ │                          │ │ │ │
│ │ │                              │ │ │ │ │                          │ │ │ │
│ │ │ ┌────┐ ┌────┐ ┌────┐       │ │ │ │ │                          │ │ │ │
│ │ │ │VID │ │IMG │ │IMG │       │ │ │ │ │                          │ │ │ │
│ │ │ └────┘ └────┘ └────┘       │ │ │ │ │                          │ │ │ │
│ │ │                              │ │ │ │ │                          │ │ │ │
│ │ │ [Scroll within panel ↓]      │ │ │ │ │                          │ │ │ │
│ │ └──────────────────────────────┘ │ │ │ └──────────────────────────┘ │ │ │
│ │                                  │ │ │                                  │ │ │
│ │                                  │ │ │ ┌──────────────────────────────┐ │ │ │
│ │                                  │ │ │ │ 📝 Text Editor               │ │ │ │
│ │                                  │ │ │ │ ┌──────────────────────────┐ │ │ │
│ │                                  │ │ │ │ │                          │ │ │ │
│ │                                  │ │ │ │ │  [Text content...]       │ │ │ │
│ │                                  │ │ │ │ │                          │ │ │ │
│ │                                  │ │ │ │ └──────────────────────────┘ │ │ │
│ │                                  │ │ │ └──────────────────────────────┘ │ │ │
│ └──────────────────────────────────┴──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

#### After Scrolling Down
```
┌─────────────────────────────────────────────────────────────────────────┐
│ (Navigation Tabs scrolled off top)                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌──────────────────────────────────┬──────────────────────────────────┐ │
│ │                                  │                                  │ │
│ │   LEFT PANEL (FLOATING)          │   RIGHT PANEL (SCROLLED)        │ │
│ │   Media Browser                  │   Text Editor & Preview         │ │
│ │   (STILL VISIBLE - FIXED)        │   (Scrolled down with page)     │ │
│ │                                  │                                  │ │
│ │ ┌──────────────────────────────┐ │                                  │ │
│ │ │ 📁 Subfolder: [Select... ▼] │ │ (Content scrolled up)            │ │
│ │ │ 📊 24 files                  │ │                                  │ │
│ │ └──────────────────────────────┘ │ ┌──────────────────────────────┐ │ │
│ │                                  │ │ │ 📝 Text Editor               │ │ │
│ │ ┌──────────────────────────────┐ │ │ │ ┌──────────────────────────┐ │ │ │
│ │ │ Media Thumbnails (3 columns) │ │ │ │ │                          │ │ │ │
│ │ │                              │ │ │ │ │  [More text content...]  │ │ │ │
│ │ │ ┌────┐ ┌────┐ ┌────┐       │ │ │ │ │                          │ │ │ │
│ │ │ │IMG │ │IMG │ │VID │       │ │ │ │ │  [Even more content...]  │ │ │ │
│ │ │ └────┘ └────┘ └────┘       │ │ │ │ │                          │ │ │ │
│ │ │                              │ │ │ │ │                          │ │ │ │
│ │ │ ┌────┐ ┌────┐ ┌────┐       │ │ │ │ │                          │ │ │ │
│ │ │ │VID │ │IMG │ │IMG │       │ │ │ │ │                          │ │ │ │
│ │ │ └────┘ └────┘ └────┘       │ │ │ │ │                          │ │ │ │
│ │ │                              │ │ │ │ │                          │ │ │ │
│ │ │ [Scroll within panel ↓]      │ │ │ │ └──────────────────────────┘ │ │ │
│ │ └──────────────────────────────┘ │ │ └──────────────────────────────┘ │ │
│ │                                  │ │                                  │ │
│ │                                  │ │ ┌──────────────────────────────┐ │ │
│ │                                  │ │ │ Actions: [Save DOCX] ...     │ │ │
│ │                                  │ │ └──────────────────────────────┘ │ │
│ │                                  │ │                                  │ │
│ └──────────────────────────────────┴──────────────────────────────────┘ │
│                                                                          │
│ (Media browser stays fixed while page continues scrolling)              │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Behavior Specifications

### 3.1 Floating Panel Position

#### Desktop View (≥1024px width)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Navigation Tabs (can scroll off)                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌───────────┐  ┌────────────────────────────────────────────────────┐   │
│ │           │  │                                                    │   │
│ │  MEDIA    │  │  RIGHT PANEL                                      │   │
│ │  BROWSER  │  │  (Scrolls with page)                              │   │
│ │  (FIXED)  │  │                                                    │   │
│ │           │  │  ┌──────────────────────────────────────────────┐ │   │
│ │  ┌──────┐ │  │  │ Live Preview                                │ │   │
│ │  │ [IMG]│ │  │  │                                              │ │   │
│ │  │ [IMG]│ │  │  │  [Content...]                               │ │   │
│ │  │ [VID]│ │  │  │                                              │ │   │
│ │  └──────┘ │  │  │  [Scrolls down...]                          │ │   │
│ │           │  │  │                                              │ │   │
│ │  [Scroll] │  │  └──────────────────────────────────────────────┘ │   │
│ │  within   │  │                                                    │   │
│ │  panel    │  │  ┌──────────────────────────────────────────────┐ │   │
│ │           │  │  │ Text Editor                                 │ │   │
│ │           │  │  │                                              │ │   │
│ │           │  │  │  [Long text content...]                     │ │   │
│ │           │  │  │                                              │ │   │
│ │           │  │  │  [Scrolls down...]                          │ │   │
│ │           │  │  └──────────────────────────────────────────────┘ │   │
│ │           │  │                                                    │   │
│ └───────────┘  └────────────────────────────────────────────────────┘   │
│                                                                          │
│ (Page continues scrolling...)                                            │
│                                                                          │
│ ┌───────────┐                                                           │
│ │           │  (Media browser stays fixed at same screen position)     │
│ │  MEDIA    │                                                           │
│ │  BROWSER  │  [Right panel content continues scrolling...]            │
│ │  (FIXED)  │                                                           │
│ │           │                                                           │
│ └───────────┘                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Position Specifications

#### Fixed Position Details
- **Position Type**: `position: fixed` or `position: sticky`
- **Top Offset**: Distance from top of viewport (e.g., 80px below navigation)
- **Left Offset**: Distance from left edge (0px)
- **Width**: 50% of viewport width (or fixed pixel width)
- **Height**: `calc(100vh - [top offset])` - Full viewport height minus top offset
- **Z-Index**: Higher than scrolling content (e.g., z-index: 100)

#### Scroll Behavior
- **Media Browser Panel**: 
  - Fixed/sticky to viewport
  - Does NOT scroll with page
  - Can scroll internally (for browsing media thumbnails)
- **Right Panel (Preview + Editor)**:
  - Scrolls normally with page content
  - Independent scroll from media browser

---

## 4. Visual Design Specifications

### 4.1 Panel Styling

#### Media Browser Panel (Floating)
```
┌──────────────────────────────────────────┐
│ Position: Fixed                          │
│ Top: 80px (below navigation)            │
│ Left: 0px                               │
│ Width: 50% of viewport                  │
│ Height: calc(100vh - 80px)              │
│ Background: #2a2a2a                     │
│ Border: 1px solid #555                  │
│ Z-index: 100                            │
│ Overflow-y: auto (internal scroll)      │
│ Box-shadow: 0 2px 10px rgba(0,0,0,0.3) │
└──────────────────────────────────────────┘
```

#### Right Panel (Scrolling)
```
┌──────────────────────────────────────────┐
│ Position: Relative (normal flow)         │
│ Width: 50% of viewport                  │
│ Margin-left: 50% (pushes to right)      │
│ Background: #2a2a2a                     │
│ Border: 1px solid #555                  │
│ Scrolls with page content               │
└──────────────────────────────────────────┘
```

### 4.2 Spacing and Layout

#### Gap Between Panels
- **Gap**: 20px spacing between floating panel and right panel
- **Visual Separation**: Clear border or shadow to distinguish floating panel

#### Top Offset
- **Navigation Height**: ~60-80px
- **Panel Top Offset**: 80px from top of viewport
- **Calculated Height**: `calc(100vh - 80px)` for full visible height

### 4.3 Visual Indicators

#### Floating Panel Indicators
- **Shadow**: Subtle shadow to indicate floating state
- **Border**: Slightly more prominent border
- **Background**: Slightly different shade to distinguish from scrolling content

---

## 5. Technical Implementation

### 5.1 CSS Approach

#### Option A: Position Fixed (Recommended)
```css
.observation-media-left-panel {
    position: fixed;
    top: 80px;                    /* Below navigation */
    left: 0;
    width: calc(50% - 10px);      /* 50% minus half gap */
    height: calc(100vh - 80px);   /* Full height minus top offset */
    max-height: calc(100vh - 80px);
    overflow-y: auto;
    overflow-x: hidden;
    z-index: 100;
    background: #2a2a2a;
    box-shadow: 2px 0 10px rgba(0,0,0,0.3);
}

.observation-media-right-panel {
    position: relative;
    width: calc(50% - 10px);      /* 50% minus half gap */
    margin-left: calc(50% + 10px); /* Push to right, account for gap */
    background: #2a2a2a;
}
```

#### Option B: Position Sticky (Alternative)
```css
.observation-media-left-panel {
    position: sticky;
    top: 80px;
    left: 0;
    width: 50%;
    height: calc(100vh - 80px);
    max-height: calc(100vh - 80px);
    overflow-y: auto;
    align-self: flex-start;       /* Important for sticky */
    z-index: 100;
}
```

### 5.2 Container Adjustments

#### Parent Container
```css
.observation-media-container {
    display: flex;
    gap: 20px;
    position: relative;
    /* Allow right panel to scroll independently */
}
```

### 5.3 Scroll Handling

#### Independent Scrolling
- **Media Browser**: Internal scroll for thumbnails (overflow-y: auto)
- **Page Scroll**: Right panel scrolls with page
- **No Conflict**: Both scroll independently without interference

---

## 6. Edge Cases and Considerations

### 6.1 Short Content
**Scenario**: Right panel content is shorter than viewport height
- **Behavior**: Right panel displays normally, media browser still floats
- **Solution**: No special handling needed

### 6.2 Very Tall Media Browser
**Scenario**: Many media files, panel content taller than viewport
- **Behavior**: Media browser has internal scroll, stays fixed
- **Solution**: Overflow-y: auto enables internal scrolling

### 6.3 Window Resize
**Scenario**: User resizes browser window
- **Behavior**: Floating panel adjusts width/height accordingly
- **Solution**: Use viewport units (vw, vh) and calc() for responsiveness

### 6.4 Mobile/Tablet Views
**Scenario**: Small screen sizes
- **Behavior**: May need to stack panels vertically or hide media browser
- **Solution**: Media query to change layout for small screens

### 6.5 Navigation Tabs
**Scenario**: Navigation tabs also scroll off
- **Behavior**: Media browser stays fixed below where navigation was
- **Solution**: Fixed top offset (e.g., 80px) accounts for navigation height

---

## 7. User Experience Considerations

### 7.1 Benefits
- **Always Accessible**: Media browser always visible for quick access
- **Efficient Workflow**: No need to scroll back up to access media
- **Better Overview**: Can see media while editing/reading content

### 7.2 Potential Concerns
- **Screen Real Estate**: Takes up 50% of screen width
- **Small Screens**: May not work well on tablets/mobile
- **Visual Distraction**: Floating panel might be distracting

### 7.3 Mitigation Strategies
- **Responsive Design**: Adjust layout for smaller screens
- **Optional Toggle**: Consider toggle to show/hide floating panel
- **Clean Design**: Subtle styling to minimize distraction

---

## 8. Responsive Behavior

### 8.1 Desktop (≥1024px)
- **Layout**: Floating media browser (50% width) + scrolling right panel (50% width)
- **Behavior**: Full floating functionality as specified

### 8.2 Tablet (768px - 1023px)
- **Layout**: Option A - Keep floating but adjust widths
- **Layout**: Option B - Stack vertically (media browser on top, collapses)
- **Decision**: To be determined based on testing

### 8.3 Mobile (<768px)
- **Layout**: Stack vertically
- **Behavior**: Media browser at top, scrolls with page (no floating)
- **Alternative**: Collapsible/hideable media browser

---

## 9. Alternative Approaches

### 9.1 Option A: Full Floating (Recommended)
- Media browser is always fixed/floating
- Takes up 50% of screen width
- Always visible

### 9.2 Option B: Collapsible Floating
- Media browser can be collapsed/expanded
- Icon button to toggle visibility
- Saves screen space when not needed

### 9.3 Option C: Auto-Hide on Scroll
- Media browser hides when scrolling down
- Shows again when scrolling up or hovering
- More screen space for content

---

## 10. Implementation Checklist

### 10.1 Required Changes
- [ ] Update CSS for `.observation-media-left-panel` to use `position: fixed`
- [ ] Set appropriate top offset (accounting for navigation)
- [ ] Set height to `calc(100vh - [top offset])`
- [ ] Adjust `.observation-media-right-panel` margin to account for fixed panel
- [ ] Ensure internal scrolling works for media browser
- [ ] Test on different screen sizes
- [ ] Verify z-index doesn't conflict with other elements
- [ ] Test scroll behavior with long content

### 10.2 Testing Requirements
- [ ] Test with many media files (long scroll)
- [ ] Test with long text content (right panel)
- [ ] Test window resize
- [ ] Test on different screen sizes
- [ ] Test scroll performance
- [ ] Test drag-and-drop still works
- [ ] Test media assignment interactions

---

## 11. Questions for Approval

1. **Floating Behavior**: Always floating or collapsible?
   - Recommendation: Always floating (can add toggle later if needed)

2. **Top Offset**: How far from top? (accounting for navigation)
   - Recommendation: 80px (accounts for navigation tabs)

3. **Width**: Keep 50/50 split or adjust?
   - Recommendation: Keep 50/50 for consistency

4. **Mobile Behavior**: Stack vertically or hide?
   - Recommendation: Stack vertically on mobile

5. **Visual Distinction**: Should floating panel have visual indicator?
   - Recommendation: Subtle shadow and border enhancement

---

## 12. Approval Checklist

- [ ] Floating/sticky behavior approved
- [ ] Position and sizing approved (top offset, width, height)
- [ ] Scroll behavior approved (independent scrolling)
- [ ] Visual design approved (shadow, borders, styling)
- [ ] Responsive behavior approved (desktop/tablet/mobile)
- [ ] Implementation approach approved (CSS method)
- [ ] Edge cases handling approved

---

**Document Status**: Draft - Awaiting Approval  
**Last Updated**: [Current Date]  
**Author**: AI Assistant  
**Reviewer**: [Pending]


