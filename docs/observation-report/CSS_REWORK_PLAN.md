# CSS Rework Plan - Live Preview Styles

## Overview
Complete rework of live preview CSS from scratch, following spec exactly. Work in stages with tests at each stage.

## Stage 1: Analyze Spec Requirements ✅
**Status**: In Progress

### Requirements from Spec:
1. **Dark Theme**:
   - Background: `#1e1e1e`
   - Text: `#e0e0e0`
   - Secondary background: `#2a2a2a`
   - Borders: `#555`

2. **Live Preview**:
   - Real-time updates
   - Dark theme matches overall application
   - Sections collapsible, collapsed by default
   - Section color coding (rainbow colors)
   - Placeholder color coding (rainbow colors)
   - 2-column tables for placeholders
   - Text formatting: preserve newlines

3. **Sections**:
   - Collapsed by default
   - Clickable headers with toggle icon
   - Unique color per section
   - Content nested inside

4. **Placeholders**:
   - Rainbow color coding
   - 2-column table layout
   - Drop zones for empty cells
   - Media items in cells

## Stage 2: Remove Old CSS
**Status**: Pending
- Backup current CSS file
- Create new clean CSS file
- Remove all inline styles from template (keep only minimal overrides)

## Stage 3: Base Styles
**Status**: Pending
- Container styles
- Color variables
- Typography
- Base layout

## Stage 4: Component Styles
**Status**: Pending
- Sections (collapsible)
- Placeholders (tables, colors)
- Media items
- Drop zones
- Text content

## Stage 5: Visual Regression Tests
**Status**: Pending
- Screenshot tests for each component
- Compare against spec
- Test dark theme
- Test color coding
- Test collapsible sections

## Stage 6: Spec Verification
**Status**: Pending
- Review all styles against spec
- Ensure no deviations
- Final approval before release



