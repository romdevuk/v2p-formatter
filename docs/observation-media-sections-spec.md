# Observation Media - Section Enhancement Specification

## Overview

This specification describes an enhancement to the Observation Media module's Live Preview feature. When text contains section markers (e.g., "SECTION xxxx"), the preview will automatically organize content into collapsible, color-coded sections.

## Version
**1.0.0** - Initial Specification

---

## 1. Functional Requirements

### 1.1 Section Detection
- **Pattern Recognition**: The system must detect section markers in the following formats:
  - `SECTION xxxx` (case-insensitive)
  - `SECTION: xxxx`
  - `SECTION - xxxx`
  - `SECTION xxxx:` (with optional colon)
  - Whitespace variations are allowed (e.g., `SECTION  xxxx`, `SECTION\nxxxx`)

- **Section Title Extraction**: 
  - The text following "SECTION" (after optional colon/dash) becomes the section title
  - Leading/trailing whitespace is trimmed
  - Example: `SECTION Health and Safety` → title: "Health and Safety"
  - Example: `SECTION: Site Arrival` → title: "Site Arrival"

### 1.2 Content Nesting
- **Content Assignment**: All text and placeholders following a section marker belong to that section until:
  - Another section marker is encountered, OR
  - End of document is reached

- **Nested Structure**: 
  - Sections can contain:
    - Plain text
    - Placeholders (with their assigned media tables)
    - Multiple paragraphs
    - Multiple placeholders

### 1.3 Section Display

#### 1.3.1 Visual Structure
- Each section appears as a collapsible container in the Live Preview
- Section header displays:
  - Section title
  - Expand/collapse icon (▼ expanded, ▶ collapsed)
  - Color-coded border/background
  - Section number (optional, for reference)

#### 1.3.2 Color Coding
- Each section receives a unique color from a predefined palette
- Colors are assigned sequentially and consistently (same section always gets same color)
- Color palette (rainbow-inspired, distinct colors):
  1. `#667eea` (Blue)
  2. `#f093fb` (Pink)
  3. `#4facfe` (Light Blue)
  4. `#43e97b` (Green)
  5. `#fa709a` (Rose)
  6. `#fee140` (Yellow)
  7. `#30cfd0` (Cyan)
  8. `#a8edea` (Aqua)
  9. `#ff9a9e` (Coral)
  10. `#fad0c4` (Peach)
  - If more than 10 sections, colors cycle/repeat

#### 1.3.3 Collapsible Behavior
- **Default State**: All sections are collapsed by default
- **Expand/Collapse**: 
  - Click on section header to toggle
  - Smooth animation (200-300ms transition)
  - Icon rotates/updates to indicate state
- **Content Visibility**:
  - Collapsed: Only header visible
  - Expanded: Full content (text + placeholders + media tables) visible

### 1.4 Section Header Styling
- **Header Design**:
  - Background: Section color with 20% opacity
  - Border: 2px solid section color (left border or full border)
  - Padding: 12px 15px
  - Font: Bold, 16px
  - Cursor: pointer
  - Hover effect: Slight background darkening (10% increase in opacity)

- **Icon**:
  - Position: Right side of header
  - Size: 16px
  - Color: Section color or white (for contrast)
  - Animation: Smooth rotation/transition

### 1.5 Content Area Styling
- **Expanded Content**:
  - Background: Dark theme (#1e1e1e or slightly lighter)
  - Padding: 15px
  - Border: 1px solid section color (subtle, 30% opacity)
  - Margin: 5px 0

### 1.6 Text Without Sections
- If no section markers are detected:
  - Display content normally (as current implementation)
  - No section containers
  - No color coding
  - Standard preview behavior

---

## 2. Technical Requirements

### 2.1 Section Parsing
- **Algorithm**:
  1. Scan text for section markers using regex
  2. Extract section titles
  3. Determine content boundaries (text between section markers)
  4. Build section tree structure
  5. Assign colors sequentially

- **Regex Pattern** (case-insensitive):
  ```
  /^SECTION\s*[:-]?\s*(.+)$/im
  ```

### 2.2 Data Structure
```javascript
{
  sections: [
    {
      id: "section-0",
      title: "Health and Safety",
      color: "#667eea",
      content: "text content...",
      placeholders: [...],
      isExpanded: false,
      index: 0
    },
    ...
  ],
  hasSections: true
}
```

### 2.3 Preview Rendering
- **Process**:
  1. Parse text for sections
  2. If sections found:
     - Render section containers
     - Apply color coding
     - Render nested content (text + placeholders)
     - Set all sections to collapsed
  3. If no sections:
     - Render standard preview (current behavior)

### 2.4 State Management
- **Section State**:
  - Track expanded/collapsed state per section
  - Store in JavaScript object: `{ sectionId: boolean }`
  - Persist during preview updates (if section structure unchanged)

- **Color Assignment**:
  - Calculate hash or use index-based assignment
  - Ensure consistency across preview updates

---

## 3. UI/UX Design

### 3.1 Section Header Layout
```
┌─────────────────────────────────────────────────┐
│ ▼ Health and Safety                    [Color] │
└─────────────────────────────────────────────────┘
```

### 3.2 Expanded Section
```
┌─────────────────────────────────────────────────┐
│ ▼ Health and Safety                    [Color] │
├─────────────────────────────────────────────────┤
│                                                 │
│ Text content here...                           │
│                                                 │
│ ┌─────────────────────────────────────────┐   │
│ │ [Media Table for {{placeholder}}]      │   │
│ └─────────────────────────────────────────┘   │
│                                                 │
│ More text...                                    │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 3.3 Collapsed Section
```
┌─────────────────────────────────────────────────┐
│ ▶ Health and Safety                    [Color] │
└─────────────────────────────────────────────────┘
```

### 3.4 Multiple Sections
```
┌─────────────────────────────────────────────────┐
│ ▶ Health and Safety                    [Blue]  │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│ ▶ Site Arrival                          [Pink] │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│ ▶ Equipment Check                      [Green] │
└─────────────────────────────────────────────────┘
```

### 3.5 Interaction
- **Click on Header**: Toggle expand/collapse
- **Hover on Header**: Highlight effect
- **Visual Feedback**: 
  - Icon animation
  - Smooth height transition
  - Color emphasis on hover

---

## 4. Implementation Details

### 4.1 Functions to Add/Modify

#### 4.1.1 `parseSections(text)`
- **Purpose**: Parse text and extract sections
- **Input**: String (text content)
- **Output**: Array of section objects
- **Logic**:
  1. Split text by section markers
  2. Extract titles and content
  3. Assign colors
  4. Return structured data

#### 4.1.2 `renderSections(sections, assignments, colorMap)`
- **Purpose**: Generate HTML for sections
- **Input**: Sections array, media assignments, placeholder colors
- **Output**: HTML string
- **Logic**:
  1. Iterate through sections
  2. Generate section header HTML
  3. Generate section content HTML (with placeholders)
  4. Apply color styling
  5. Set collapsed state

#### 4.1.3 `toggleSection(sectionId)`
- **Purpose**: Toggle section expand/collapse
- **Input**: Section ID
- **Logic**:
  1. Update state object
  2. Toggle CSS class
  3. Animate transition
  4. Update icon

#### 4.1.4 `assignSectionColors(sections)`
- **Purpose**: Assign colors to sections
- **Input**: Sections array
- **Output**: Sections array with colors assigned
- **Logic**:
  1. Use predefined color palette
  2. Assign sequentially
  3. Return updated sections

### 4.2 CSS Classes
```css
.observation-section {
  margin: 10px 0;
  border-radius: 6px;
  overflow: hidden;
}

.observation-section-header {
  padding: 12px 15px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.2s;
}

.observation-section-header:hover {
  /* Hover effect */
}

.observation-section-content {
  padding: 15px;
  transition: max-height 0.3s ease;
}

.observation-section-content.collapsed {
  max-height: 0;
  padding: 0 15px;
  overflow: hidden;
}

.observation-section-icon {
  transition: transform 0.3s ease;
}

.observation-section-icon.collapsed {
  transform: rotate(-90deg);
}
```

### 4.3 State Management
```javascript
window.observationSectionStates = {
  'section-0': false,  // collapsed
  'section-1': false,  // collapsed
  // ...
};
```

---

## 5. Examples

### 5.1 Example Text Input
```
This is introduction text before any sections.

SECTION Health and Safety
I arrived to the project on agreed time. The weather was sunny.
I met Ivan at the gate where he followed security rules.
{{site_arrival_and_induction_table}}

AC covered: 641:1.1, 1.2, 1.3, 2.1, 4.1; 642:1.1
Image suggestion: learner signing in and wearing PPE.

SECTION Equipment Inspection
Before starting work, I inspected all equipment.
{{equipment_check_table}}

All tools were in good condition.
```

### 5.2 Expected Preview Output
- **Collapsed State** (default):
  - "This is introduction text before any sections." (normal text, no section)
  - ▶ Health and Safety [Blue border]
  - ▶ Equipment Inspection [Pink border]

- **Expanded State** (after clicking):
  - "This is introduction text before any sections." (normal text)
  - ▼ Health and Safety [Blue border]
    - Content: "I arrived to the project..."
    - Media table for `{{site_arrival_and_induction_table}}`
    - "AC covered: 641:1.1..."
  - ▶ Equipment Inspection [Pink border]

---

## 6. Edge Cases

### 6.1 Multiple Section Markers
- If multiple section markers appear on consecutive lines, treat as separate sections
- Empty sections (no content) are still displayed but with minimal height

### 6.2 Section at Start/End
- Section at document start: Content before first section is displayed normally
- Section at document end: All content after last section marker belongs to that section

### 6.3 Nested Sections (Not Supported)
- If "SECTION" appears within section content, treat as literal text (not a new section)
- Only top-level sections are supported

### 6.4 Special Characters in Titles
- HTML entities are escaped
- Special characters in titles are preserved
- Long titles are truncated with ellipsis if needed (optional)

### 6.5 Placeholders Spanning Sections
- Placeholders belong to the section they appear in
- If placeholder appears between sections, it belongs to the previous section

---

## 7. Performance Considerations

### 7.1 Parsing Performance
- Section parsing should be efficient (O(n) where n is text length)
- Cache parsed sections if text hasn't changed

### 7.2 Rendering Performance
- Use CSS transitions for animations (GPU-accelerated)
- Lazy render collapsed sections (optional optimization)

### 7.3 State Persistence
- Section states persist during text edits (if section structure unchanged)
- Reset states if section structure changes

---

## 8. Accessibility

### 8.1 Keyboard Navigation
- Tab to section headers
- Enter/Space to toggle expand/collapse
- Focus indicators visible

### 8.2 Screen Readers
- Section headers have `role="button"` and `aria-expanded` attributes
- Section content has `aria-hidden` when collapsed

### 8.3 Color Contrast
- Ensure section colors meet WCAG AA contrast requirements
- Provide alternative indicators (icons, borders) for color-blind users

---

## 9. Testing Requirements

### 9.1 Unit Tests
- Section parsing with various formats
- Color assignment consistency
- State management (expand/collapse)

### 9.2 Integration Tests
- Preview rendering with sections
- Interaction with placeholders
- State persistence

### 9.3 UI Tests
- Expand/collapse functionality
- Color coding display
- Animation smoothness

---

## 10. Future Enhancements (Out of Scope)

- Nested sections (sections within sections)
- Section numbering
- Export sections to separate DOCX pages
- Section search/filter
- Custom section colors
- Drag-and-drop section reordering

---

## 11. Approval Checklist

- [ ] Section detection pattern approved
- [ ] Color palette approved
- [ ] Collapsed-by-default behavior approved
- [ ] UI/UX design approved
- [ ] Technical approach approved
- [ ] Edge cases handling approved

---

## 12. Questions for Clarification

1. Should sections be numbered automatically (e.g., "1. Health and Safety")? no need
2. Should there be a "Expand All" / "Collapse All" button? yes
3. Should section states persist across page refreshes (via localStorage)? yes
4. Should the section marker format be configurable? no need
5. Should empty sections (no content) be hidden or shown? keep it as is

---

**Document Status**: Draft - Awaiting Approval
**Last Updated**: [Current Date]
**Author**: AI Assistant
**Reviewer**: [Pending]

