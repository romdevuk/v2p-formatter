# AC Matrix - Bulk Reports Format Wireframe

## Overview
This document describes the new format for displaying AC coverage when analyzing multiple reports/drafts. The format uses a row-based matrix where:
- **Row 1**: All ACs from the standards (reference row)
- **Row 2+**: ACs covered by each draft/report (one row per draft)

## Format Structure

### Unit Display

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Unit 641: Conforming to General Health, Safety and Welfare in the Workplace │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ Standards ACs:  [1.1] [1.2] [1.3] [2.1] [2.2] [3.1] [3.2] [3.3] [3.4] ... │
│                                                                               │
│ My Draft:       [✓]   [✓]   [✓]   [✓]   [✗]   [✓]   [✓]   [✗]   [✗]   ... │
│                                                                               │
│ 2ndobsMy Draft: [✓]   [✓]   [✗]   [✓]   [✓]   [✗]   [✓]   [✓]   [✓]   ... │
│                                                                               │
│ Report 3:       [✓]   [✗]   [✓]   [✗]   [✓]   [✓]   [✗]   [✓]   [✗]   ... │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Detailed View (Clicking on an AC)

When clicking on an AC in any row:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ AC 1.1 - ✓ COVERED                                                          │
│ From Report: My Draft                                                       │
│                                                                               │
│ Section: Site Induction                                                      │
│ Observation Text:                                                            │
│ "During the site induction, AC 1.1 was covered when the site manager       │
│  explained the procedures..."                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Visual Design

### Row Structure

1. **Standards Row (Row 1)**
   - Background: Dark gray (#1e1e1e)
   - Text: Light gray (#e0e0e0)
   - AC IDs: Displayed as clickable badges
   - Purpose: Reference row showing all possible ACs

2. **Draft/Report Rows (Row 2+)**
   - Background: Slightly lighter (#2a2a2a)
   - Draft name: Left-aligned, colored (#667eea)
   - Status icons: 
     - ✓ (green) for covered
     - ✗ (red) for missing/not covered
   - Alignment: Status icons align directly under corresponding AC IDs from Row 1

### Layout Details

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Unit Header                                                                   │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Standards ACs:                                                          │ │
│ │ [1.1] [1.2] [1.3] [2.1] [2.2] [3.1] [3.2] [3.3] [3.4] [3.5] [4.1] ... │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ My Draft:                                                                │ │
│ │ [✓]  [✓]  [✓]  [✓]  [✗]  [✓]  [✓]  [✗]  [✗]  [✗]  [✓]  ...          │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ 2ndobsMy Draft:                                                          │ │
│ │ [✓]  [✓]  [✗]  [✓]  [✓]  [✗]  [✓]  [✓]  [✓]  [✓]  [✓]  ...          │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│ (Clicking on any ✓ or ✗ expands details panel below)                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Interaction

1. **Clicking on Standards AC (Row 1)**
   - Shows details for the first occurrence of that AC (if covered)
   - Or shows "Not covered in any report" if missing

2. **Clicking on Status Icon (Row 2+)**
   - Shows details for that specific AC occurrence in that specific draft
   - Displays: AC ID, Report name, Section title, Observation text

3. **Expand All / Collapse All**
   - Expands/collapses all detail panels at once

## Color Coding

- **Standards Row ACs**: Light gray (#e0e0e0), clickable
- **Covered Status (✓)**: Green (#4a8a4a)
- **Missing Status (✗)**: Red (#8a4a4a)
- **Draft Name**: Purple/Blue (#667eea)
- **Section Titles**: Rotating colors from SECTION_COLORS array

## Responsive Behavior

- ACs wrap to multiple lines if needed
- Status icons maintain alignment with AC IDs above
- Horizontal scrolling if too many ACs to fit

## Example with Real Data

```
Unit 641: Conforming to General Health, Safety and Welfare in the Workplace

Standards ACs:  1.1  1.2  1.3  2.1  2.2  3.1  3.2  3.3  3.4  3.5  4.1  5.1

My Draft:       ✓    ✓    ✓    ✓    ✗    ✓    ✓    ✗    ✗    ✗    ✓    ✗

2ndobsMy Draft: ✓    ✓    ✗    ✓    ✓    ✗    ✓    ✓    ✓    ✓    ✓    ✓

Report 3:       ✓    ✗    ✓    ✗    ✓    ✓    ✗    ✓    ✗    ✓    ✗    ✓
```

## Implementation Notes

1. **Data Structure**
   - First, get all ACs from standards (Row 1)
   - For each draft/report, create a row showing coverage status
   - Missing ACs show ✗, covered ACs show ✓

2. **Alignment**
   - Status icons must align directly under their corresponding AC IDs
   - Use flexbox or grid for consistent spacing

3. **Details Panel**
   - Unique ID per AC occurrence: `details-{unitId}-{acId}-{reportName}`
   - Shows report name, section title, and observation text

4. **Single Report Mode**
   - If only one report, still show standards row + one report row
   - Format remains consistent

## Questions for Approval

1. Should missing ACs (✗) be clickable to show "Not covered" message?
2. Should the standards row ACs be clickable, and if so, what should they show?
3. Should we show a summary row at the bottom showing combined coverage?
4. Should draft names be editable/clickable to rename them?




