# Live Preview - Media Quantity Display Wireframe

## Overview
This wireframe specifies how to display the media quantity (number of media items) added to each section in the Live Preview.

## Version
**1.0.0** - Initial Specification

---

## 1. Functional Requirements

### 1.1 Media Quantity Display
- **Location**: Display media quantity in each section header in the Live Preview
- **Calculation**: Count all media items assigned to all placeholders within that section
- **Update**: Update in real-time as media is assigned/removed/reordered
- **Format**: Show count with clear label (e.g., "3 media", "5 items", "Media: 3")

### 1.2 Display Logic
- **Zero Media**: Show "0 media" or "(no media)" or hide if zero (to be decided)
- **One Media**: Show "1 media"
- **Multiple Media**: Show "X media" (e.g., "3 media", "5 media")
- **Real-time Updates**: Count updates immediately when:
  - Media is assigned to a placeholder within the section
  - Media is removed from a placeholder within the section
  - Media is reordered (count doesn't change, but should remain accurate)

### 1.3 Visual Design
- **Position**: Right side of section header, before the expand/collapse icon
- **Style**: Subtle, informative (not too prominent)
- **Color**: Match section color or use neutral color (#999 or similar)
- **Font Size**: Slightly smaller than section title (12-14px vs 16px)

---

## 2. Text Wireframe: Section Header with Media Quantity

### 2.1 Current Section Header Structure (Before)
```
┌─────────────────────────────────────────────────────────┐
│ ▼ Health and Safety                            [▶]     │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Proposed Section Header Structure (After)

#### Option A: Media count after title, before icon
```
┌─────────────────────────────────────────────────────────┐
│ ▼ Health and Safety  (3 media)                  [▶]     │
└─────────────────────────────────────────────────────────┘
```

#### Option B: Media count on the right, before icon
```
┌─────────────────────────────────────────────────────────┐
│ ▼ Health and Safety                           3 media [▶]│
└─────────────────────────────────────────────────────────┘
```

#### Option C: Media count with badge style (recommended)
```
┌─────────────────────────────────────────────────────────┐
│ ▼ Health and Safety                    [3 media]  [▶]   │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Wireframe Specifications

### 3.1 Section Header Layout (Option C - Recommended)

#### Expanded Section with Media
```
┌─────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ ▼ Health and Safety                    [3 media]         ▼      │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ │ Text content here...                                             │
│ │                                                                  │
│ │ ┌─────────────────────────────────────────────────────────┐    │
│ │ │ [Media Table for {{placeholder1}}]                      │    │
│ │ │ [Image] [Image]                                         │    │
│ │ └─────────────────────────────────────────────────────────┘    │
│ │                                                                  │
│ │ More text...                                                     │
│ │                                                                  │
│ │ ┌─────────────────────────────────────────────────────────┐    │
│ │ │ [Media Table for {{placeholder2}}]                      │    │
│ │ │ [Video]                                                  │    │
│ │ └─────────────────────────────────────────────────────────┘    │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

#### Collapsed Section with Media
```
┌─────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ ▶ Health and Safety                    [3 media]         ▶      │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

#### Section with Zero Media
```
┌─────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ ▶ Equipment Check                    [0 media]          ▶      │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Multiple Sections Example

```
┌─────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ ▶ Health and Safety                    [3 media]         ▶      │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ ▶ Site Arrival                          [5 media]        ▶      │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ ▶ Equipment Check                    [0 media]          ▶      │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.3 Section Header Components Breakdown

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│ [▼/▶ Icon]  [Section Title]    [Media Count Badge]    [▼/▶ Icon]  │
│                                                                     │
│   ↓              ↓                      ↓                    ↓      │
│ Expand/      Title text         "3 media" or          Expand/       │
│ Collapse                         "0 media"            Collapse      │
│ Icon                             (badge style)        Icon          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Visual Design Specifications

### 4.1 Media Count Badge Style

#### Badge Design
- **Background**: Section color with 30% opacity or neutral gray (#555)
- **Border**: 1px solid section color or #777
- **Text Color**: Section color or #e0e0e0 (light text)
- **Font Size**: 12px (smaller than section title)
- **Font Weight**: Regular (not bold)
- **Padding**: 4px 8px
- **Border Radius**: 4px
- **Margin**: 0 10px (spacing from title and icon)

#### Badge States
- **Has Media (1+)**: Normal badge style
- **Zero Media**: 
  - Option 1: Show "[0 media]" (grayed out)
  - Option 2: Hide completely (show nothing)
  - Option 3: Show "(no media)" in lighter color

### 4.2 Color Coding
- **Badge Background**: `rgba(sectionColor, 0.3)` or `#555`
- **Badge Border**: Section color or `#777`
- **Badge Text**: Section color or `#e0e0e0`
- **Zero Media Badge**: `#666` (grayed out) or hidden

### 4.3 Typography
- **Section Title**: 16px, bold, section color
- **Media Count**: 12px, regular, section color or #e0e0e0
- **Icon**: 16px, section color

---

## 5. Technical Implementation

### 5.1 Media Count Calculation

```javascript
function countMediaInSection(section, assignments) {
    // Extract placeholders from section content
    const sectionPlaceholders = extractPlaceholders(section.content);
    
    // Count media items assigned to all placeholders in this section
    let totalCount = 0;
    sectionPlaceholders.forEach(placeholder => {
        const placeholderKey = placeholder.toLowerCase();
        if (assignments[placeholderKey]) {
            totalCount += assignments[placeholderKey].length;
        }
    });
    
    return totalCount;
}
```

### 5.2 Section Header HTML Structure

```html
<div class="observation-section-header" onclick="toggleSection('section-0')" 
     style="background: #667eea20; border: 1px solid #667eea;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <span class="observation-section-icon" style="color: #667eea; font-size: 16px;">▼</span>
        <span style="color: #667eea; font-weight: bold; font-size: 16px;">Health and Safety</span>
    </div>
    <div style="display: flex; align-items: center; gap: 10px;">
        <span class="section-media-count" 
              style="background: #667eea30; border: 1px solid #667eea; color: #667eea; 
                     padding: 4px 8px; border-radius: 4px; font-size: 12px;">
            3 media
        </span>
        <span class="observation-section-icon" style="color: #667eea; font-size: 16px;">▼</span>
    </div>
</div>
```

### 5.3 CSS Classes

```css
.section-media-count {
    background: rgba(var(--section-color), 0.3);
    border: 1px solid var(--section-color);
    color: var(--section-color);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: normal;
    white-space: nowrap;
}

.section-media-count.zero-media {
    color: #999;
    background: rgba(153, 153, 153, 0.2);
    border-color: #666;
}

/* Hide zero media count (optional) */
.section-media-count.zero-media.hidden {
    display: none;
}
```

---

## 6. User Experience Considerations

### 6.1 Visibility
- **At a Glance**: Users can quickly see which sections have media assigned
- **Empty Sections**: Easy to identify sections that still need media
- **Progress Tracking**: Visual indicator of work completion per section

### 6.2 Information Hierarchy
- **Primary**: Section title (most prominent)
- **Secondary**: Expand/collapse icon (interactive element)
- **Tertiary**: Media count (informational, less prominent)

### 6.3 Real-time Updates
- Count updates immediately when:
  - Media assigned to placeholder in section
  - Media removed from placeholder in section
  - Media reordered (count stays same, but should refresh)
- No page refresh required
- Smooth visual updates (no flickering)

---

## 7. Examples

### 7.1 Example 1: Section with Multiple Placeholders

**Section Content:**
```
SECTION Health and Safety
I arrived to the project on agreed time.
{{site_arrival_table}}
{{induction_table}}
All safety procedures were followed.
```

**Media Assignments:**
- `site_arrival_table`: 2 images, 1 video = 3 media
- `induction_table`: 1 image = 1 media
- **Total**: 4 media

**Section Header Display:**
```
┌─────────────────────────────────────────────────────────┐
│ ▼ Health and Safety                    [4 media]  ▼     │
└─────────────────────────────────────────────────────────┘
```

### 7.2 Example 2: Section with No Placeholders

**Section Content:**
```
SECTION Introduction
This is the introduction text.
No placeholders here.
```

**Media Assignments:**
- No placeholders = 0 media

**Section Header Display:**
```
┌─────────────────────────────────────────────────────────┐
│ ▼ Introduction                          [0 media]  ▼     │
└─────────────────────────────────────────────────────────┘
```

Or if hiding zero media:
```
┌─────────────────────────────────────────────────────────┐
│ ▼ Introduction                                  ▼       │
└─────────────────────────────────────────────────────────┘
```

### 7.3 Example 3: Multiple Sections with Varying Media

**Live Preview Display:**
```
┌─────────────────────────────────────────────────────────┐
│ ▶ Introduction                           [0 media]  ▶    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ▼ Health and Safety                    [3 media]   ▼     │
│ │                                                       │
│ │ Text content...                                       │
│ │ [Media tables...]                                     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ▶ Site Arrival                          [5 media]   ▶    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ▶ Equipment Check                      [0 media]   ▶     │
└─────────────────────────────────────────────────────────┘
```

---

## 8. Alternative Display Options

### 8.1 Option 1: Simple Text (No Badge)
```
▼ Health and Safety  (3 media)                          ▼
```
- Pros: Simple, clean
- Cons: Less visually distinct

### 8.2 Option 2: Icon + Count
```
▼ Health and Safety                    📷 3              ▼
```
- Pros: More visual, icon indicates media type
- Cons: Icon might be confusing (images vs videos)

### 8.3 Option 3: Detailed Breakdown (Not Recommended)
```
▼ Health and Safety                    [3 img, 1 vid]    ▼
```
- Pros: More information
- Cons: Cluttered, too much detail

### 8.4 Option 4: Badge Style (Recommended)
```
▼ Health and Safety                    [3 media]         ▼
```
- Pros: Clear, clean, matches UI style
- Cons: None

---

## 9. Implementation Checklist

### 9.1 Required Changes
- [ ] Modify `renderSections()` function to calculate media count per section
- [ ] Add media count calculation function `countMediaInSection()`
- [ ] Update section header HTML to include media count badge
- [ ] Add CSS styling for media count badge
- [ ] Ensure real-time updates when media assignments change
- [ ] Handle zero media state (show/hide decision)

### 9.2 Testing Requirements
- [ ] Test with sections containing multiple placeholders
- [ ] Test with sections containing zero placeholders
- [ ] Test with sections containing placeholders with no media
- [ ] Test real-time updates when assigning media
- [ ] Test real-time updates when removing media
- [ ] Test real-time updates when reordering media
- [ ] Test with multiple sections
- [ ] Test with empty sections
- [ ] Verify count accuracy matches actual media assignments

---

## 10. Questions for Approval

1. **Zero Media Display**: Should we show "[0 media]" or hide it completely?
   - Recommendation: Show "[0 media]" in grayed-out style for consistency

2. **Badge Position**: Right side before icon, or after title?
   - Recommendation: Right side before icon (Option C)

3. **Badge Style**: Badge background or plain text?
   - Recommendation: Badge style for better visibility

4. **Terminology**: "media", "items", or "files"?
   - Recommendation: "media" (matches existing terminology)

5. **Color**: Match section color or neutral?
   - Recommendation: Match section color for consistency

---

## 11. Approval Checklist

- [ ] Media quantity display location approved
- [ ] Display format approved (badge style, position, text)
- [ ] Zero media handling approved (show/hide)
- [ ] Visual design approved (colors, typography, spacing)
- [ ] Technical approach approved
- [ ] Terminology approved ("media" vs "items" vs "files")
- [ ] Real-time update behavior approved

---

**Document Status**: Draft - Awaiting Approval  
**Last Updated**: [Current Date]  
**Author**: AI Assistant  
**Reviewer**: [Pending]





