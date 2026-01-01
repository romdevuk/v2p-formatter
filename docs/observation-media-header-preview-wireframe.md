# Observation Media - Header in Document Preview - Wireframe Specification

## Overview
Add header section to Document Preview window that displays header fields (learner, assessor, visit date, location, address) as a table at the top of the document. The header is hidden by default and can be toggled via a setting in the Actions panel.

Also add assessor feedback field (textarea) under the text editor field. In Document Preview, show assessor feedback at the bottom in a 1px border table. The assessor feedback can be shown/hidden via a setting in the Actions panel.

## Document Preview Layout

### With Header Hidden (Default)
```
┌─────────────────────────────────────────────────────────────┐
│ 📄 Document Preview                                    [✕]  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌──────────────────┐  ┌─────────────────────────────────┐ │
│ │ Sections         │  │ Preview Content                  │ │
│ │                  │  │                                  │ │
│ │ ▶ Section 1      │  │ SECTION: 1 – Introduction       │ │
│ │ ▶ Section 2      │  │                                  │ │
│ │ ▶ Section 3      │  │ Some text content here...        │ │
│ │                  │  │                                  │ │
│ │                  │  │ [More content...]                │ │
│ └──────────────────┘  └─────────────────────────────────┘ │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ⚙️ Actions                                              │ │
│ │                                                          │ │
│ │ Font Settings:                                          │ │
│ │   Size: [16pt ▼]  Type: [Times New Roman ▼]           │ │
│ │                                                          │ │
│ │ Hide Elements:                                          │ │
│ │   ☐ Section Titles                                     │ │
│ │   ☐ AC covered                                         │ │
│ │   ☐ Image suggestion                                   │ │
│ │   ☐ Paragraph numbers                                  │ │
│ │   ☐ Empty media fields                                 │ │
│ │   ☐ Trim empty paragraphs                              │ │
│ │   ☑ Show header                                        │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### With Header Shown
```
┌─────────────────────────────────────────────────────────────┐
│ 📄 Document Preview                                    [✕]  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌──────────────────┐  ┌─────────────────────────────────┐ │
│ │ Sections         │  │ Preview Content                  │ │
│ │                  │  │                                  │ │
│ │ ▶ Section 1      │  │ ┌─────────────────────────────┐ │ │
│ │ ▶ Section 2      │  │ │ Header Table (1px borders)  │ │ │
│ │ ▶ Section 3      │  │ │ ┌──────┬──────────────────┐ │ │ │
│ │                  │  │ │ │Learner│ John Doe         │ │ │ │
│ │                  │  │ │ ├──────┼──────────────────┤ │ │ │
│ │                  │  │ │ │Assess│ Jane Smith       │ │ │ │
│ │                  │  │ │ ├──────┼──────────────────┤ │ │ │
│ │                  │  │ │ │Visit │ 2025-01-15       │ │ │ │
│ │                  │  │ │ ├──────┼──────────────────┤ │ │ │
│ │                  │  │ │ │Locat │ Site A           │ │ │ │
│ │                  │  │ │ ├──────┼──────────────────┤ │ │ │
│ │                  │  │ │ │Addres│ 123 Main St      │ │ │ │
│ │                  │  │ │ └──────┴──────────────────┘ │ │ │
│ │                  │  │ └─────────────────────────────┘ │ │ │
│ │                  │  │                                  │ │ │
│ │                  │  │ SECTION: 1 – Introduction       │ │ │
│ │                  │  │                                  │ │ │
│ │                  │  │ Some text content here...        │ │ │
│ │                  │  │                                  │ │ │
│ │                  │  │ ┌─────────────────────────────┐ │ │ │
│ │                  │  │ │ Assessor Feedback Table      │ │ │ │
│ │                  │  │ │ ┌──────────────────────────┐ │ │ │ │
│ │                  │  │ │ │ Assessor Feedback        │ │ │ │ │
│ │                  │  │ │ ├──────────────────────────┤ │ │ │ │
│ │                  │  │ │ │ [Feedback text here...] │ │ │ │ │
│ │                  │  │ │ └──────────────────────────┘ │ │ │ │
│ │                  │  │ └─────────────────────────────┘ │ │ │
│ └──────────────────┘  └─────────────────────────────────┘ │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ⚙️ Actions                                              │ │
│ │                                                          │ │
│ │ Font Settings:                                          │ │
│ │   Size: [16pt ▼]  Type: [Times New Roman ▼]           │ │
│ │                                                          │ │
│ │ Hide Elements:                                          │ │
│ │   ☐ Section Titles                                     │ │
│ │   ☐ AC covered                                         │ │
│ │   ☐ Image suggestion                                   │ │
│ │   ☐ Paragraph numbers                                  │ │
│ │   ☐ Empty media fields                                 │ │
│ │   ☐ Trim empty paragraphs                              │ │
│ │   ☐ Show header                                        │ │
│ │   ☐ Show assessor feedback                            │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Header Table Design

### Table Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Header Table (1px solid borders, all cells)                 │
├──────────────┬──────────────────────────────────────────────┤
│ Learner      │ [Value from headerLearner field]             │
├──────────────┼──────────────────────────────────────────────┤
│ Assessor     │ [Value from headerAssessor field]            │
├──────────────┼──────────────────────────────────────────────┤
│ Visit Date   │ [Value from headerVisitDate field]          │
├──────────────┼──────────────────────────────────────────────┤
│ Location     │ [Value from headerLocation field]            │
├──────────────┼──────────────────────────────────────────────┤
│ Address      │ [Value from headerAddress field]             │
└──────────────┴──────────────────────────────────────────────┘
```

### Table Styling
- **Border**: 1px solid #000 (black) on all cells
- **Border collapse**: Collapsed borders
- **Width**: 100% of preview content width
- **Cell padding**: 8px vertical, 12px horizontal
- **Left column width**: ~150px (fixed)
- **Right column**: Remaining width
- **Font**: Same as preview content (Times New Roman, 16pt default)
- **Background**: White (for document preview)
- **Text alignment**: Left column (labels) - left aligned, Right column (values) - left aligned

## DOCX Export Format

### When Exporting to DOCX (Header Always Included)
```
Assessment Report

┌─────────────────────────────────────────────────────────────┐
│ Header Table (1px borders)                                  │
├──────────────┬──────────────────────────────────────────────┤
│ Learner      │ John Doe                                     │
├──────────────┼──────────────────────────────────────────────┤
│ Assessor     │ Jane Smith                                    │
├──────────────┼──────────────────────────────────────────────┤
│ Visit Date   │ 15 January 2025                              │
├──────────────┼──────────────────────────────────────────────┤
│ Location     │ Site A                                       │
├──────────────┼──────────────────────────────────────────────┤
│ Address      │ 123 Main Street, City, Country               │
└──────────────┴──────────────────────────────────────────────┘

[Blank paragraph - 1 empty line]

Observation Report

[Rest of document content - sections, text, etc.]
```

### DOCX Export Details
- **"Assessment Report"**: 
  - Font: Times New Roman, 18pt, Bold
  - Alignment: Center
  - Spacing: 12pt after
  
- **Header Table**:
  - Always included in DOCX export (regardless of preview setting)
  - 1px solid black borders on all cells
  - Same structure as preview
  
- **Blank Paragraph**:
  - One empty paragraph (12pt spacing) between header table and "Observation Report"
  
- **"Observation Report"**:
  - Font: Times New Roman, 18pt, Bold
  - Alignment: Center
  - Spacing: 12pt before, 12pt after

## Settings Panel

### Actions Panel - Hide Elements Section
```
┌─────────────────────────────────────────────────────────┐
│ ⚙️ Actions                                              │
│                                                          │
│ Font Settings:                                          │
│   Size: [16pt ▼]  Type: [Times New Roman ▼]           │
│                                                          │
│ Hide Elements:                                          │
│   ☐ Section Titles                                     │
│   ☐ AC covered                                         │
│   ☐ Image suggestion                                   │
│   ☐ Paragraph numbers                                  │
│   ☐ Empty media fields                                 │
│   ☐ Trim empty paragraphs                              │
│   ☐ Show header                                        │ ← NEW
│                                                          │
│ [Update Draft] [Export DOCX]                           │
└─────────────────────────────────────────────────────────┘
```

### Show Header Checkbox Behavior
- **Default state**: Unchecked (header hidden)
- **When checked**: Header table appears at top of preview content
- **When unchecked**: Header table is hidden from preview
- **DOCX export**: Header is ALWAYS included regardless of checkbox state
- **Label**: "Show header" (checkbox text)

## Implementation Details

### Preview Content Structure
```html
<div id="draftPreviewContent">
    <!-- Header Table (conditionally shown) -->
    <div id="previewHeaderTable" style="display: none;">
        <table class="preview-header-table">
            <tr>
                <td>Learner</td>
                <td id="previewHeaderLearner"></td>
            </tr>
            <tr>
                <td>Assessor</td>
                <td id="previewHeaderAssessor"></td>
            </tr>
            <tr>
                <td>Visit Date</td>
                <td id="previewHeaderVisitDate"></td>
            </tr>
            <tr>
                <td>Location</td>
                <td id="previewHeaderLocation"></td>
            </tr>
            <tr>
                <td>Address</td>
                <td id="previewHeaderAddress"></td>
            </tr>
        </table>
    </div>
    
    <!-- Document Content -->
    <div id="previewDocumentContent">
        <!-- Sections, text, etc. -->
    </div>
</div>
```

### CSS for Header Table
```css
.preview-header-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 12pt;
    font-family: 'Times New Roman', serif;
    font-size: 16pt;
}

.preview-header-table td {
    border: 1px solid #000;
    padding: 8px 12px;
    vertical-align: top;
}

.preview-header-table td:first-child {
    width: 150px;
    font-weight: normal;
    background-color: #f5f5f5;
}

.preview-header-table td:last-child {
    /* Value column */
}
```

### JavaScript Functions

1. **Update Preview Display**:
   - Check "Show header" checkbox state
   - Show/hide header table accordingly
   - Update header field values from input fields

2. **Format Visit Date**:
   - Convert date input (YYYY-MM-DD) to readable format (DD Month YYYY)
   - Example: "2025-01-15" → "15 January 2025"

3. **DOCX Export**:
   - Always include header table
   - Add "Assessment Report" heading above table
   - Add blank paragraph
   - Add "Observation Report" heading below table
   - Then include document content

## User Flow

### Viewing Preview with Header
1. User fills in header fields (learner, assessor, etc.)
2. User opens Document Preview
3. User checks "Show header" checkbox in Actions panel
4. Header table appears at top of preview content
5. User can uncheck to hide header (for preview only)

### Exporting to DOCX
1. User clicks "Export DOCX" button
2. DOCX is generated with:
   - "Assessment Report" heading
   - Header table (always included)
   - Blank paragraph
   - "Observation Report" heading
   - Document content
3. Header is included regardless of preview checkbox state

## Edge Cases

### Empty Header Fields
- If a header field is empty, show empty cell (not "N/A" or placeholder)
- Table structure remains the same

### Date Format
- Display date in preview: "15 January 2025" (readable format)
- Store date in draft: "2025-01-15" (ISO format)
- Export to DOCX: "15 January 2025" (readable format)

### Long Text in Fields
- Table cells wrap text automatically
- No horizontal scrolling
- Maintains table structure

## Visual Design

### Preview (Dark Theme)
- Header table background: #1e1e1e (matches preview background)
- Header table borders: #555 (subtle, matches theme)
- Header table text: #e0e0e0 (light text)
- Label column background: #2a2a2a (slightly lighter)

### DOCX Export (Print-Ready)
- Header table background: White
- Header table borders: Black (#000, 1px solid)
- Header table text: Black
- Label column background: Light gray (#f5f5f5) - optional, for better readability

## Assessor Feedback Section

### Text Editor Page Layout
```
┌─────────────────────────────────────────────────────────────┐
│ Observation Media                                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ [Header Section - Collapsed]                                │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Text Editor                                              │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ [Text content area...]                             │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Assessor Feedback                                        │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ [Textarea for feedback...]                          │ │ │
│ │ │                                                      │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Assessor Feedback Table Design

#### Table Structure (Preview)
```
┌─────────────────────────────────────────────────────────────┐
│ Assessor Feedback Table (1px solid borders, all cells)     │
├──────────────────────────────────────────────────────────────┤
│ Assessor Feedback                                            │
├──────────────────────────────────────────────────────────────┤
│ [Feedback text content here...]                             │
│                                                              │
│ [Multi-line text wraps automatically]                        │
└──────────────────────────────────────────────────────────────┘
```

#### Table Styling
- **Border**: 1px solid #555 (preview) / #000 (DOCX) on all cells
- **Border collapse**: Collapsed borders
- **Width**: 100% of preview content width
- **Cell padding**: 8px vertical, 12px horizontal
- **Font**: Same as preview content (Times New Roman, 16pt default)
- **Background**: #1e1e1e (preview) / White (DOCX)
- **Text alignment**: Left aligned
- **Min height**: 100px (preview) / Auto (DOCX)
- **Text wrapping**: Automatic

### DOCX Export Format (Assessor Feedback)

#### When Exporting to DOCX (Assessor Feedback Always Included at Bottom)
```
[Document content...]

[Blank paragraph - 1 empty line]

┌─────────────────────────────────────────────────────────────┐
│ Assessor Feedback Table (1px borders)                       │
├──────────────────────────────────────────────────────────────┤
│ Assessor Feedback                                            │
├──────────────────────────────────────────────────────────────┤
│ [Feedback text content here...]                             │
│                                                              │
│ [Multi-line text wraps automatically]                        │
└──────────────────────────────────────────────────────────────┘
```

### Preview Content Structure (Updated)
```html
<div id="draftPreviewContent">
    <!-- Header Table (conditionally shown) -->
    <div id="previewHeaderTable" style="display: none;">
        <table class="preview-header-table">
            <!-- Header rows... -->
        </table>
    </div>
    
    <!-- Document Content -->
    <div id="previewDocumentContent">
        <!-- Sections, text, etc. -->
    </div>
    
    <!-- Assessor Feedback Table (conditionally shown) -->
    <div id="previewAssessorFeedback" style="display: none;">
        <table class="preview-assessor-feedback-table">
            <tr>
                <td>Assessor Feedback</td>
            </tr>
            <tr>
                <td id="previewAssessorFeedbackContent"></td>
            </tr>
        </table>
    </div>
</div>
```

### CSS for Assessor Feedback Table
```css
.preview-assessor-feedback-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    font-family: 'Times New Roman', serif;
    font-size: 16pt;
    border: 1px solid #555;
}

.preview-assessor-feedback-table td {
    border: 1px solid #555;
    padding: 8px 12px;
    vertical-align: top;
    color: #e0e0e0;
    background-color: #1e1e1e;
}

.preview-assessor-feedback-table tr:first-child td {
    font-weight: normal;
    background-color: #2a2a2a;
}

.preview-assessor-feedback-table tr:last-child td {
    min-height: 100px;
    white-space: pre-wrap;
    word-wrap: break-word;
}
```

### JavaScript Functions (Updated)

1. **Update Preview Display**:
   - Check "Show header" checkbox state
   - Show/hide header table accordingly
   - Check "Show assessor feedback" checkbox state
   - Show/hide assessor feedback table accordingly
   - Update header field values from input fields
   - Update assessor feedback content from textarea

2. **Format Visit Date**:
   - Convert date input (YYYY-MM-DD) to readable format (DD Month YYYY)
   - Example: "2025-01-15" → "15 January 2025"

3. **DOCX Export**:
   - Always include header table at top
   - Add "Assessment Report" heading above header table
   - Add blank paragraph
   - Add "Observation Report" heading below header table
   - Include document content
   - Add blank paragraph
   - Always include assessor feedback table at bottom

### User Flow (Updated)

#### Viewing Preview with Assessor Feedback
1. User fills in assessor feedback textarea
2. User opens Document Preview
3. User checks "Show assessor feedback" checkbox in Actions panel
4. Assessor feedback table appears at bottom of preview content
5. User can uncheck to hide assessor feedback (for preview only)

#### Exporting to DOCX
1. User clicks "Export DOCX" button
2. DOCX is generated with:
   - "Assessment Report" heading
   - Header table (always included)
   - Blank paragraph
   - "Observation Report" heading
   - Document content
   - Blank paragraph
   - Assessor feedback table (always included at bottom)
3. Both header and assessor feedback are included regardless of preview checkbox states

### Edge Cases (Updated)

#### Empty Assessor Feedback
- If assessor feedback is empty, show empty cell (not "N/A" or placeholder)
- Table structure remains the same
- Table is still included in DOCX export (empty)

#### Long Text in Assessor Feedback
- Text wraps automatically within table cell
- No horizontal scrolling
- Maintains table structure
- Preserves line breaks and formatting

## Accessibility

- Table has proper structure with `<table>`, `<tr>`, `<td>` elements
- Labels are in first column, values in second column
- Screen readers can navigate table structure
- Checkbox has proper label association
- Textarea has proper label association

---

**Status**: ⏳ **AWAITING APPROVAL**

**Created**: 2025-01-XX  
**Author**: AI Assistant  
**Review Required**: Yes

