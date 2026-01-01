# Observation AC Matrix - Wireframe

## Overview
The Observation AC Matrix module allows users to compare observation report text against assessment criteria (ACs) from JSON standards files. It displays a color-coded matrix showing which ACs are covered and which are missing.

## Page Layout

### Header Section
```
┌─────────────────────────────────────────────────────────────────┐
│  Observation AC Matrix                                          │
│  Compare observation reports against assessment criteria         │
└─────────────────────────────────────────────────────────────────┘
```

### Settings Panel (Top Section)
```
┌─────────────────────────────────────────────────────────────────┐
│  Settings                                                        │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ JSON Standards File: [Dropdown ▼]                          │ │
│  │                                                             │ │
│  │ Available Files:                                            │ │
│  │ • Level 2 NVQ Diploma in Interior Systems v3              │ │
│  │ • [Add New File] [Upload]                                  │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Input Section
```
┌─────────────────────────────────────────────────────────────────┐
│  Observation Report                                              │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Load from Draft: [Select Draft ▼] [Load]                   │ │
│  └───────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │ [Text Area - Multi-line input for observation report]      │ │
│  │                                                             │ │
│  │ Paste or type observation report text with AC references   │ │
│  │ (e.g., "AC 1.1, 1.2, 2.1 were covered...")                │ │
│  │                                                             │ │
│  │ Or load from Observation Media drafts                      │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────┘ │
│  [Analyze Report]                                               │
└─────────────────────────────────────────────────────────────────┘
```

### Matrix Display Section
```
┌─────────────────────────────────────────────────────────────────┐
│  AC Coverage Matrix                                              │
│  Display Style: [Vertical ▼] [Horizontal]                        │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Summary: 35 of 50 ACs covered (70%)                       │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [VERTICAL STYLE - Default]                                     │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Unit: Conforming to General Health, Safety...              │ │
│  │ ┌──────────┬──────────────────────────────┬─────────────┬──────────────────────────────┐ │ │
│  │ │ AC ID    │ AC Description               │ Status      │ Where Covered                │ │ │
│  │ ├──────────┼──────────────────────────────┼─────────────┼──────────────────────────────┤ │ │
│  │ │ 1.1      │ Comply with information...   │ [COVERED]   │ Section: Site Induction      │ │ │
│  │ │          │                              │             │ Observation Text:            │ │ │
│  │ │          │                              │             │ "During the site induction,  │ │ │
│  │ │          │                              │             │  AC 1.1 was covered when the │ │ │
│  │ │          │                              │             │  site manager explained..."  │ │ │
│  │ ├──────────┼──────────────────────────────┼─────────────┼──────────────────────────────┤ │ │
│  │ │ 1.2      │ Use health and safety...     │ [COVERED]   │ Section: Safety Equipment    │ │ │
│  │ │          │                              │             │ Observation Text:            │ │ │
│  │ │          │                              │             │ "AC 1.2 was demonstrated     │ │ │
│  │ │          │                              │             │  when the operative used     │ │ │
│  │ │          │                              │             │  the safety equipment..."    │ │ │
│  │ ├──────────┼──────────────────────────────┼─────────────┼──────────────────────────────┤ │ │
│  │ │ 1.3      │ Comply with statutory...     │ [MISSING]   │ (Not covered in observation) │ │ │
│  │ ├──────────┼──────────────────────────────┼─────────────┼──────────────────────────────┤ │ │
│  │ │ 2.1      │ Report any hazards...        │ [COVERED]   │ Section: Hazard Reporting    │ │ │
│  │ │          │                              │             │ Observation Text:            │ │ │
│  │ │          │                              │             │ "Hazards were reported in     │ │ │
│  │ │          │                              │             │  accordance with AC 2.1 when │ │ │
│  │ │          │                              │             │  a potential risk was..."     │ │ │
│  │ ├──────────┼──────────────────────────────┼─────────────┼──────────────────────────────┤ │ │
│  │ │ 3.1      │ Interpret and comply...      │ [MISSING]   │ (Not covered in observation) │ │ │
│  │ └──────────┴──────────────────────────────┴─────────────┴──────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [HORIZONTAL STYLE]                                             │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Unit: Conforming to General Health, Safety...              │ │
│  │ ┌───────────────────────────────────────────────────────┐ │ │
│  │ │ ACs: 1.1  1.2  1.3  2.1  3.1  3.2  3.3  3.4  3.5  4.1 │ │ │
│  │ │ Status: ✓  ✓  ✗  ✓  ✗  ✗  ✗  ✗  ✗  ✗                │ │ │
│  │ └───────────────────────────────────────────────────────┘ │ │
│  │                                                             │ │
│  │ Click on AC to view details:                                │ │
│  │ ┌───────────────────────────────────────────────────────┐ │ │
│  │ │ AC 1.1 - ✓ COVERED                                   │ │ │
│  │ │ Section: Site Induction                              │ │ │
│  │ │ Observation Text:                                    │ │ │
│  │ │ "During the site induction, AC 1.1 was covered when  │ │ │
│  │ │  the site manager explained the procedures..."        │ │ │
│  │ └───────────────────────────────────────────────────────┘ │ │
│  │                                                             │ │
│  │ ┌───────────────────────────────────────────────────────┐ │ │
│  │ │ AC 1.2 - ✓ COVERED                                   │ │ │
│  │ │ Section: Safety Equipment                             │ │ │
│  │ │ Observation Text:                                    │ │ │
│  │ │ "AC 1.2 was demonstrated when the operative used     │ │ │
│  │ │  the safety equipment correctly..."                   │ │ │
│  │ └───────────────────────────────────────────────────────┘ │ │
│  │                                                             │ │
│  │ ┌───────────────────────────────────────────────────────┐ │ │
│  │ │ AC 1.3 - ✗ MISSING                                   │ │ │
│  │ │ (No observation text found)                          │ │ │
│  │ └───────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Actions Panel
```
┌─────────────────────────────────────────────────────────────────┐
│  Actions                                                         │
│  [Save Matrix] [Load Matrix ▼] [Delete Matrix]                 │
│                                                                  │
│  Save Matrix:                                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Matrix Name: [________________]                            │ │
│  │ [Save] [Cancel]                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Color Coding

### Status Colors (Dark Theme)
- **Covered AC**: Green background (#2d5a2d) with green border (#4a8a4a), white text
- **Missing AC**: Red background (#5a2d2d) with red border (#8a4a4a), white text
- **Table Header**: Dark gray (#333) with light gray text (#ccc)
- **Table Row (hover)**: Slightly lighter background (#2a2a2a)

## Detailed Component Specifications

### 1. JSON File Selector Dropdown
- **Location**: Settings panel, top of page
- **Functionality**:
  - Dropdown list of available JSON standards files
  - Shows qualification name and version
  - "Add New File" button opens file upload dialog
  - Selected file is used for matrix generation
- **Default State**: Empty selection with placeholder "Select a standards file..."

### 2. Observation Report Text Field
- **Location**: Input section, below settings
- **Specifications**:
  - **Draft Loader**: Dropdown to select from Observation Media drafts + "Load" button
    - Drafts are loaded server-side and passed to template (no API calls)
    - Dropdown populated with draft names and creation dates
    - On "Load", JavaScript extracts `text_content` from selected draft (already in page)
    - Populates textarea with `text_content` from draft
  - Large multi-line textarea (minimum 10 rows)
  - Placeholder text: "Paste or type your observation report text here. The system will automatically detect AC references (e.g., 1.1, 2.3, etc.) Or load from Observation Media drafts."
  - Auto-resize or scrollable
  - Dark theme styling: dark background (#1e1e1e), light text (#e0e0e0)
- **Action Button**: "Analyze Report" - triggers AC extraction and matrix generation

### 3. AC Coverage Matrix
- **Display Style Toggle**: Dropdown/buttons to switch between "Vertical" and "Horizontal" styles
- **Layout Options**:
  - **Vertical Style (Default)**: Traditional table layout
  - **Horizontal Style**: Side-by-side comparison of Standard ACs vs Observation ACs
- **Table Structure (Vertical)**:
  - **Column 1**: AC ID (e.g., "1.1", "2.3")
  - **Column 2**: AC Description (full question name)
  - **Column 3**: Status (Covered/Missing badge)
  - **Column 4**: "Where Covered" - separate column showing:
    - **For covered ACs**:
      - Section title (styled with SECTION_COLORS, same as observation-media)
      - Observation text section from report
    - **For missing ACs**: "(Not covered in observation)" indicator
- **Table Structure (Horizontal)**:
  - **First Line**: Unit name, then all ACs in one line (e.g., "ACs: 1.1  1.2  1.3  2.1...")
  - **Second Line**: Status for each AC (✓ for covered, ✗ for missing) aligned below each AC
  - **Expandable Details**: Click on any AC to expand and view:
    - AC ID and status
    - Section title (if covered, styled with SECTION_COLORS)
    - Observation text section (if covered)
    - Or "Missing" indicator (if not covered)
- **Unit Grouping**: Each unit displayed in separate collapsible section
- **Expandable Units**: Click unit header to expand/collapse
- **Visual Indicators**:
  - Covered: Green badge with checkmark icon
  - Missing: Red badge with X icon
- **Observation Text Section Display**: 
  - **For Covered ACs**: Shows the actual text section from observation report where AC was found
  - **Section Title**: Displays the section title with same color coding and style as observation-media page
    - Section titles are identified by pattern: "SECTION:" or "SECTION -" followed by title
    - Uses same SECTION_COLORS palette as observation-media (10 colors, cycling through sections)
    - Styling matches observation-media:
      - Font: bold, 14pt
      - Color: section color from SECTION_COLORS array (based on section index)
      - Border-left: 4px solid in section color
      - Padding-left: 10px
      - Margin: 15px 0 10px 0
    - Shows which section of the observation report contains the AC
  - Displayed in a highlighted box/panel below the AC row (Vertical) or in right column (Horizontal)
  - Shows surrounding context (e.g., 100-150 characters before and after the AC reference)
  - Format: Section title (styled with color) followed by "Observation Text:" and the text section
  - Styled differently (e.g., background color, border, italic font) to distinguish from standard AC description
  - Truncated with "..." if too long, with "Show more" / "Show less" toggle
  - Click to expand/collapse full context
  - **For Missing ACs**: Shows "(No observation text found)" or similar indicator
- **Summary Statistics**: 
  - At top of matrix: "X of Y ACs covered (Z%)"
  - Per unit: "X of Y ACs covered in this unit"

### 4. Save Matrix Dialog
- **Trigger**: "Save Matrix" button
- **Fields**:
  - Matrix Name (text input, required)
  - Auto-suggest based on current date/time
- **Saved Data**:
  - Selected JSON file reference
  - Observation report text
  - Matrix analysis results
  - Timestamp

### 5. Load Matrix Dropdown
- **Trigger**: "Load Matrix" button with dropdown
- **Display**: List of saved matrices with:
  - Matrix name
  - Date saved
  - JSON file used
- **Action**: Clicking a matrix loads all data and regenerates display

### 6. Delete Matrix
- **Trigger**: "Delete Matrix" button
- **Confirmation**: Modal dialog "Are you sure you want to delete this matrix?"
- **Action**: Removes saved matrix from storage

## Responsive Behavior

### Desktop (1200px+)
- Full width matrix tables
- Side-by-side layout for settings and input
- All columns visible in matrix

### Tablet (768px - 1199px)
- Stacked layout for settings and input
- Matrix tables scroll horizontally if needed
- Collapsible units default to collapsed

### Mobile (< 768px)
- Single column layout
- Matrix tables scroll horizontally
- Units default to collapsed
- Compact button layout

## User Flow

1. **Initial State**:
   - Settings panel visible
   - JSON file dropdown empty
   - Text field empty
   - Matrix section hidden

2. **Select JSON File**:
   - User selects file from dropdown
   - File is loaded and parsed
   - Units and ACs are extracted

3. **Enter Observation Report**:
   - User pastes/types observation report text
   - Text is stored in state

4. **Analyze Report**:
   - User clicks "Analyze Report"
   - System extracts AC references from text (regex pattern matching)
   - Matrix is generated comparing found ACs vs. all ACs in JSON
   - Matrix section becomes visible with results

5. **Review Matrix**:
   - User reviews covered/missing ACs
   - Can expand/collapse units
   - Can modify observation report and re-analyze

6. **Save Matrix** (Optional):
   - User clicks "Save Matrix"
   - Enters matrix name
   - Matrix is saved to local storage/database

7. **Load Matrix** (Optional):
   - User clicks "Load Matrix"
   - Selects saved matrix from list
   - All data is restored and matrix regenerated

## Accessibility Features

- Keyboard navigation for all interactive elements
- ARIA labels for screen readers
- High contrast color scheme
- Focus indicators on interactive elements
- Alt text for status icons
- Semantic HTML structure

## Dark Theme Color Palette

- Background: #1a1a1a (body), #2a2a2a (container), #1e1e1e (sections)
- Text: #e0e0e0 (primary), #ccc (secondary), #999 (muted)
- Borders: #444 (default), #667eea (accent)
- Covered AC: #2d5a2d (background), #4a8a4a (border)
- Missing AC: #5a2d2d (background), #8a4a4a (border)
- Buttons: #667eea (primary), #764ba2 (hover)
- Input fields: #1e1e1e (background), #444 (border), #e0e0e0 (text)

