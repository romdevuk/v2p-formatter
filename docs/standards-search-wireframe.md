# Standards Search Feature - Wireframe Specification

## Overview
Add a search bar to the Standards column that allows users to search for keywords or phrases within AC descriptions. When a search is performed, units containing matching ACs are automatically expanded, and the matching text is highlighted.

## Placement

### Search Bar Location
```
┌─────────────────────────────────────────────────────────┐
│ Standards                                    [Expand All]│
│                                          [Collapse All]  │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 🔍 [Search standards...]                    [Clear] │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Search Bar Details:**
- **Position**: Below the Standards header, above the unit list
- **Style**: Full-width input field with search icon
- **Placeholder**: "Search standards..."
- **Clear Button**: Appears when text is entered, clears search and resets view
- **Background**: #2a2a2a (matches header)
- **Border**: 1px solid #555
- **Padding**: 10px 15px

## Search Behavior

### When User Types
1. **Real-time Search**: Search happens as user types (no need to press Enter)
2. **Auto-expand Units**: Units containing matching ACs are automatically expanded
3. **Highlight Matches**: Matching text in AC descriptions is highlighted
4. **Case-insensitive**: Search is case-insensitive by default
5. **Partial Match**: Matches partial words/phrases (e.g., "health" matches "health and safety")

### When Search is Active
- **Expanded Units**: Only units with matching ACs remain expanded
- **Collapsed Units**: Units without matches remain collapsed
- **Highlighting**: Matching text is highlighted with a background color
- **Scroll to First Match**: Optionally scroll to first matching AC

### When Search is Cleared
- **Reset Expansion**: All units return to their previous state (collapsed by default)
- **Remove Highlights**: All highlighting is removed
- **Show All Units**: All units are visible again

## Visual Design

### Search Bar
```
┌─────────────────────────────────────────────────────────┐
│ 🔍 Search standards...                           [Clear] │
└─────────────────────────────────────────────────────────┘
```

**Styling:**
- **Input Field**:
  - Background: #1e1e1e
  - Border: 1px solid #555
  - Border-radius: 4px
  - Padding: 8px 12px
  - Font-size: 14px
  - Color: #e0e0e0
  - Placeholder color: #999
- **Search Icon**: 🔍 (emoji or icon font) positioned on the left
- **Clear Button**: 
  - Visible only when search has text
  - Style: Small "×" or "Clear" button
  - Position: Right side of input
  - Color: #999, hover: #e0e0e0

### Highlighted Text
```
┌─────────────────────────────────────────────────────────┐
│ Unit 641: Conforming to General Health, Safety...       │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 1.1                                                   │ │
│ │ Explain the main [health] and safety responsibilities│ │
│ │ of employers and employees...                         │ │
│ │ Covered:                                             │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Highlight Styling:**
- **Background Color**: #FFD700 (Gold/Yellow) or #667eea (Theme color with opacity)
- **Text Color**: #000 (black) or #e0e0e0 (light) depending on contrast
- **Padding**: 2px 4px
- **Border-radius**: 2px
- **Font-weight**: Normal (not bold, to distinguish from AC ID)

### Example: Search Results Display
```
┌─────────────────────────────────────────────────────────┐
│ Standards                                    [Expand All]│
│                                          [Collapse All]  │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 🔍 health                                    [Clear] │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ▼ Unit 641: Conforming to General Health, Safety...     │
│   ┌───────────────────────────────────────────────────┐ │
│   │ 1.1                                                 │ │
│   │ Explain the main [health] and safety...            │ │
│   │ Covered:                                           │ │
│   └───────────────────────────────────────────────────┘ │
│   ┌───────────────────────────────────────────────────┐ │
│   │ 1.2                                                 │ │
│   │ Use [health] and safety control equipment...        │ │
│   │ Covered:                                           │ │
│   └───────────────────────────────────────────────────┘ │
│                                                          │
│ ▶ Unit 642: Installing Interior Systems                 │
│   (No matches - remains collapsed)                       │
└─────────────────────────────────────────────────────────┘
```

## Search Functionality

### Search Scope
- **Searches**: AC descriptions (question_name field)
- **Does NOT search**: AC IDs, unit names, unit IDs
- **Search Mode**: Full-text search within AC descriptions

### Matching Logic
- **Case-insensitive**: "Health" matches "health", "HEALTH", "Health" (always case-insensitive)
- **Partial word match**: "health" matches "health and safety", "healthcare"
- **Phrase match**: "health and safety" matches exact phrase (case-insensitive)
- **Multiple words**: "health safety" matches text containing both words (AND logic, case-insensitive)
- **Exact phrase with quotes**: "health and safety" (with quotes) matches exact phrase only

### Expansion Logic
- **Auto-expand**: Units containing at least one matching AC are expanded
- **Preserve state**: When search is cleared, restore previous expand/collapse state
- **Scroll to match**: Optionally scroll to first matching AC in expanded unit

## User Interactions

### Typing in Search Bar
1. User types "health"
2. System searches all AC descriptions
3. Units with matching ACs expand automatically
4. Matching text is highlighted in yellow/gold
5. Units without matches remain collapsed

### Clearing Search
1. User clicks "Clear" button or clears input
2. All highlighting is removed
3. Units return to default state (collapsed)
4. Search bar is cleared

### Keyboard Shortcuts (Optional)
- **Escape**: Clear search
- **Enter**: No action (search is real-time)
- **Ctrl+F / Cmd+F**: Focus search bar

## States

### Empty State (No Search)
- Search bar shows placeholder: "Search standards..."
- Clear button hidden
- All units in default state (collapsed)
- No highlighting

### Active Search State
- Search bar shows entered text
- Clear button visible
- Matching units expanded
- Matching text highlighted
- Non-matching units collapsed

### No Results State
- Search bar shows entered text
- Clear button visible
- All units collapsed
- Message: "No results found for '[search term]'"
- Message style: #999, centered, padding: 20px

## Implementation Details

### Search Algorithm
```javascript
function searchStandards(searchTerm) {
    if (!searchTerm || searchTerm.trim() === '') {
        // Clear search
        clearSearch();
        return;
    }
    
    const trimmedTerm = searchTerm.trim();
    const isExactPhrase = trimmedTerm.startsWith('"') && trimmedTerm.endsWith('"');
    const term = isExactPhrase 
        ? trimmedTerm.slice(1, -1).toLowerCase() 
        : trimmedTerm.toLowerCase();
    
    const units = document.querySelectorAll('.standards-unit');
    let hasMatches = false;
    
    units.forEach(unit => {
        const acs = unit.querySelectorAll('.standards-ac-text');
        let unitHasMatch = false;
        
        acs.forEach(acElement => {
            const acText = acElement.textContent.toLowerCase();
            let matches = false;
            
            if (isExactPhrase) {
                // Exact phrase match (case-insensitive)
                matches = acText.includes(term);
            } else {
                // Multiple words: all must be present (AND logic, case-insensitive)
                const words = term.split(/\s+/).filter(w => w.length > 0);
                matches = words.every(word => acText.includes(word));
            }
            
            if (matches) {
                unitHasMatch = true;
                highlightText(acElement, term, isExactPhrase);
            }
        });
        
        if (unitHasMatch) {
            expandUnit(unit);
            hasMatches = true;
        } else {
            collapseUnit(unit);
        }
    });
    
    if (!hasMatches) {
        showNoResultsMessage(trimmedTerm);
    }
}
```

### Highlight Function
- Wrap matching text in `<mark>` or `<span>` with highlight class
- Preserve original text structure
- Handle multiple matches in same AC description
- Escape HTML to prevent XSS

### Performance Considerations
- **Debounce**: Debounce search input (300ms delay) to avoid excessive searching
- **Virtual scrolling**: For large numbers of ACs, consider virtual scrolling
- **Lazy highlighting**: Only highlight visible ACs, highlight others on scroll

## Styling Details

### Search Bar Container
- **Background**: #2a2a2a
- **Border-bottom**: 1px solid #555
- **Padding**: 12px 15px
- **Margin-bottom**: 10px

### Highlight CSS Class
```css
.standards-search-highlight {
    background-color: #FFD700;
    color: #000;
    padding: 2px 4px;
    border-radius: 2px;
    font-weight: normal;
}
```

### No Results Message
- **Text**: "No results found for '[search term]'"
- **Style**: 
  - Color: #999
  - Font-size: 14px
  - Text-align: center
  - Padding: 20px
  - Font-style: italic

## Accessibility

### Keyboard Navigation
- **Tab**: Focus search bar
- **Escape**: Clear search
- **Enter**: No action (search is real-time)

### Screen Reader Support
- **ARIA Label**: "Search standards by keyword or phrase"
- **ARIA Live Region**: Announce search results count
- **ARIA Described By**: Link to help text explaining search behavior

## Questions for Clarification

1. **Search Scope**: Should search also include:
   - Unit names? no
   - AC IDs? no
   - Section names (from "Covered:" line)? no

2. **Search Mode**: Should it support:
   - Exact phrase matching (quotes)? yes
   - Boolean operators (AND, OR)? no
   - Regular expressions? no

3. **Highlight Color**: Preferred highlight color?
   - Gold/Yellow (#FFD700)? yes
   - Theme color (#667eea)?
   - Custom color?

4. **Debounce Delay**: What delay for real-time search?
   - 300ms (recommended)? yes
   - 500ms?
   - Other?

5. **Scroll Behavior**: Should it:
   - Auto-scroll to first match?
   - Scroll to first match in viewport?
   - No auto-scroll? no

6. **Search Persistence**: Should search term: = no need;
   - Persist when switching drafts?
   - Clear when draft changes?
   - Save to localStorage?

---

## Approved Specifications

### Answers to Clarification Questions:
1. **Search Scope**: ✅ Search AC descriptions only (no unit names, AC IDs, or section names)
2. **Search Mode**: ✅ Supports exact phrase matching with quotes (no boolean operators, no regex)
3. **Highlight Color**: ✅ Gold/Yellow (#FFD700)
4. **Debounce Delay**: ✅ 300ms
5. **Scroll Behavior**: ✅ Auto-scroll to first match
6. **Search Persistence**: ✅ No persistence needed (clears when draft changes)
7. **Case Sensitivity**: ✅ Always case-insensitive

### Key Features:
- ✅ **Case-insensitive search**: Always searches without regard to case
- ✅ **Real-time search**: Updates as user types (300ms debounce)
- ✅ **Auto-expand units**: Units with matching ACs automatically expand
- ✅ **Highlight matches**: Matching text highlighted in gold (#FFD700)
- ✅ **Exact phrase support**: Quotes enable exact phrase matching
- ✅ **Auto-scroll**: Scrolls to first match when search is performed
- ✅ **Clear button**: Appears when search has text, clears search and resets view

---

**Status**: ✅ **APPROVED FOR DEVELOPMENT**

**Approval Date**: 2025-01-XX  
**Implementation**: Ready to implement  
**Testing**: Ready for user testing

