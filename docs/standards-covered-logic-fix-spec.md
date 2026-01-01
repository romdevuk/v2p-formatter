# Standards "Covered" Logic Fix - Specification

## Problem Statement

The current "Covered" logic in the standards search feature incorrectly identifies sections where an AC is covered. 

### Reported Issue
- **AC**: 129v4:5.1
- **Incorrectly shown as covered in**: 
  - Section 5 – INSTALLATION OF DRYLINING SYSTEMS
  - Section 9 – COMPLETION OF WORK AND HANDOVER
- **Actual status**: When manually checked, 129v4:5.1 is NOT actually listed in the "AC covered:" lines of these sections
- **Expected behavior**: 129v4:5.1 should only be shown as covered in sections where it's explicitly listed in an "AC covered:" line

## Root Cause Analysis

The issue is in Pattern 5 of the AC coverage detection logic (lines 6578-6592 in `static/js/observation-media.js`). The problems are:

1. **Overly greedy regex pattern**: The pattern `AC\\s+covered\\s*[:.]?\\s*.*?${escapedUnitId}\\s*[:.]\\s*[\\d.]+(?:\\s*,\\s*[\\d.]+)*` uses `.*?` which can match across multiple "AC covered:" lines, causing false positives.

2. **Incorrect shorthand matching**: The shorthand check `(?:^|,)\\s*${escapedAcId}\\b` can match AC IDs that appear in different unit contexts. For example, checking for "5.1" might match "5.1" from a different unit's AC covered list.

3. **Lack of proper list parsing**: The code doesn't properly parse the AC list format to ensure the AC is actually in that specific list, not just mentioned elsewhere in the section.

## Requirements

### 1. Accurate Pattern Matching

The logic must:
- Only match ACs that are **explicitly listed** in a specific "AC covered:" line
- Preserve unit context for shorthand ACs (e.g., "5.1" only applies to the unit mentioned in that line)
- Not match ACs from different units even if they have the same AC number
- Handle multiple "AC covered:" lines in the same section correctly

### 2. Supported Formats

The logic must correctly handle these formats:

#### Format 1: Explicit unit:AC format
```
AC covered: 129v4:5.1, 129v4:5.2, 129v4:5.3
```
- Match: 129v4:5.1 ✅
- Match: 129v4:5.2 ✅
- No match: 129v4:9.1 ❌

#### Format 2: Shorthand format (ACs after unit prefix)
```
AC covered: 129v4:5.1, 5.2, 5.3
```
- Match: 129v4:5.1 ✅
- Match: 129v4:5.2 ✅ (shorthand)
- Match: 129v4:5.3 ✅ (shorthand)
- No match: 129v4:9.1 ❌

#### Format 3: Multiple unit blocks
```
AC covered: 129v4:5.1, 5.2; 129v4:9.1, 9.2
```
- Match: 129v4:5.1 ✅ (from first block)
- Match: 129v4:5.2 ✅ (shorthand from first block)
- Match: 129v4:9.1 ✅ (from second block)
- Match: 129v4:9.2 ✅ (shorthand from second block)
- No match: 129v4:5.1 when checking second block ❌

#### Format 4: Mixed explicit and shorthand
```
AC covered: 129v4:5.1, 5.2, 129v4:5.3
```
- Match: 129v4:5.1 ✅
- Match: 129v4:5.2 ✅ (shorthand)
- Match: 129v4:5.3 ✅ (explicit)

#### Format 5: Multiple "AC covered:" lines in same section
```
Some text here.
AC covered: 129v4:5.1, 5.2
More text.
AC covered: 129v4:9.1, 9.2
```
- When checking 129v4:5.1: Only match first "AC covered:" line ✅
- When checking 129v4:9.1: Only match second "AC covered:" line ✅

### 3. Edge Cases to Handle

1. **Different units with same AC number**:
   ```
   AC covered: 641:5.1, 5.2; 129v4:5.1, 5.2
   ```
   - When checking 641:5.1: Match ✅
   - When checking 129v4:5.1: Match ✅
   - When checking 641:5.1, don't match 129v4:5.1 ❌

2. **AC ID appears in text but not in AC covered list**:
   ```
   The learner demonstrated AC 129v4:5.1 during installation.
   AC covered: 129v4:9.1, 9.2
   ```
   - When checking 129v4:5.1: No match ❌ (mentioned in text but not in AC covered list)

3. **Partial AC ID matches**:
   ```
   AC covered: 129v4:5.1, 5.10, 5.11
   ```
   - When checking 129v4:5.1: Match ✅
   - When checking 129v4:5.10: Match ✅ (not 5.1)
   - When checking 129v4:5.11: Match ✅ (not 5.1)

## Implementation Specification

### Algorithm

For each AC (unitId:acId), check each section:

1. **Find all "AC covered:" lines** in the section:
   - Pattern: `AC\s+covered\s*[:.]?\s*` (case-insensitive)
   - Extract the entire line or until next "AC covered:" or end of section

2. **For each "AC covered:" line**:
   a. **Parse the AC list**:
      - Split by semicolons (`;`) to get unit blocks
      - For each block, identify the unit ID (if present)
      - Extract all ACs (both explicit and shorthand)
   
   b. **Check if AC matches**:
      - **Explicit match**: Check if `${unitId}:${acId}` appears in the block
      - **Shorthand match**: Only if the block starts with `${unitId}:`, check if `${acId}` appears as shorthand
      - Use word boundaries (`\b`) to prevent partial matches (e.g., 5.1 matching 5.10)

3. **If match found**: Add section to coveredSections and break (don't check other patterns)

4. **If no match**: Continue to other patterns (Patterns 1-4 remain unchanged)

### Regex Patterns

#### Pattern 5 (Fixed): "AC covered:" line detection
```javascript
// Find all "AC covered:" lines
const acCoveredLinePattern = /AC\s+covered\s*[:.]?\s*([^\n]*?)(?=\n\s*AC\s+covered\s*[:.]?\s*|$)/gi;
```

#### Pattern 5 (Fixed): Parse AC list from a line
```javascript
function parseAcCoveredLine(line, targetUnitId, targetAcId) {
    // Remove "AC covered:" prefix
    const acList = line.replace(/^AC\s+covered\s*[:.]?\s*/i, '').trim();
    
    // Split by semicolons to get unit blocks
    const blocks = acList.split(';').map(b => b.trim()).filter(b => b.length > 0);
    
    for (const block of blocks) {
        // Check if this block contains our unit
        const unitMatch = block.match(new RegExp(`(${escapeRegex(targetUnitId)})\\s*[:.]\\s*`, 'i'));
        
        if (unitMatch) {
            // This block is for our unit
            const unitPrefix = unitMatch[1];
            const acsInBlock = block.substring(unitMatch.index + unitMatch[0].length);
            
            // Extract all ACs from this block (explicit and shorthand)
            const acPattern = new RegExp(`(?:${escapeRegex(unitPrefix)}\\s*[:.]\\s*)?([\\d.]+)\\b`, 'g');
            const acMatches = [...acsInBlock.matchAll(acPattern)];
            
            // Check for explicit match: unitId:acId
            if (new RegExp(`${escapeRegex(targetUnitId)}\\s*[:.]\\s*${escapeRegex(targetAcId)}\\b`, 'i').test(block)) {
                return true;
            }
            
            // Check for shorthand match: acId after unitId:
            const shorthandPattern = new RegExp(`(?:^|,|;)\\s*${escapeRegex(targetAcId)}\\b`, 'i');
            if (shorthandPattern.test(acsInBlock)) {
                return true;
            }
        } else {
            // This block doesn't mention our unit, skip it
            continue;
        }
    }
    
    return false;
}
```

### Helper Function: Escape Regex Special Characters

```javascript
function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
```

### Complete Pattern 5 Implementation

```javascript
// Pattern 5: "AC covered: 641:1.1, 1.2, 1.3" format - check if AC is in the list
if (!matches) {
    // Find all "AC covered:" lines in the section
    const acCoveredLinePattern = /AC\s+covered\s*[:.]?\s*([^\n]*?)(?=\n\s*AC\s+covered\s*[:.]?\s*|$)/gi;
    const acCoveredLines = [];
    let match;
    
    while ((match = acCoveredLinePattern.exec(sectionContent)) !== null) {
        acCoveredLines.push(match[0]); // Full line including "AC covered:"
    }
    
    // Check each "AC covered:" line
    for (const acCoveredLine of acCoveredLines) {
        if (parseAcCoveredLine(acCoveredLine, unitId, acId)) {
            matches = true;
            break;
        }
    }
}
```

## Testing Requirements

### Test Cases

1. **Test Case 1: Explicit format**
   - Input: Section contains "AC covered: 129v4:5.1, 129v4:5.2"
   - Check: 129v4:5.1
   - Expected: ✅ Match

2. **Test Case 2: Shorthand format**
   - Input: Section contains "AC covered: 129v4:5.1, 5.2, 5.3"
   - Check: 129v4:5.2
   - Expected: ✅ Match

3. **Test Case 3: Multiple units**
   - Input: Section contains "AC covered: 129v4:5.1, 5.2; 129v4:9.1, 9.2"
   - Check: 129v4:5.1
   - Expected: ✅ Match
   - Check: 129v4:9.1
   - Expected: ✅ Match
   - Check: 129v4:5.1 (should not match second block)
   - Expected: ✅ Still matches (from first block)

4. **Test Case 4: AC mentioned in text but not in AC covered**
   - Input: Section contains "The learner demonstrated AC 129v4:5.1" and "AC covered: 129v4:9.1, 9.2"
   - Check: 129v4:5.1
   - Expected: ❌ No match (Pattern 5 should not match, but Pattern 1 might)

5. **Test Case 5: Partial AC ID match prevention**
   - Input: Section contains "AC covered: 129v4:5.1, 5.10, 5.11"
   - Check: 129v4:5.1
   - Expected: ✅ Match
   - Check: 129v4:5.10
   - Expected: ✅ Match (not 5.1)
   - Check: 129v4:5.11
   - Expected: ✅ Match (not 5.1)

6. **Test Case 6: Multiple AC covered lines**
   - Input: Section contains:
     ```
     AC covered: 129v4:5.1, 5.2
     Some text.
     AC covered: 129v4:9.1, 9.2
     ```
   - Check: 129v4:5.1
   - Expected: ✅ Match (first line only)
   - Check: 129v4:9.1
   - Expected: ✅ Match (second line only)

7. **Test Case 7: Different units with same AC number**
   - Input: Section contains "AC covered: 641:5.1, 5.2; 129v4:5.1, 5.2"
   - Check: 641:5.1
   - Expected: ✅ Match
   - Check: 129v4:5.1
   - Expected: ✅ Match
   - Check: 641:5.1 (should not match 129v4:5.1)
   - Expected: ✅ Only matches 641:5.1

## Implementation Notes

1. **Word Boundaries**: Always use `\b` in regex patterns to prevent partial matches (e.g., 5.1 matching 5.10).

2. **Case Insensitivity**: All regex patterns should use the `i` flag for case-insensitive matching.

3. **Whitespace Handling**: The patterns should handle various whitespace scenarios (spaces, tabs, newlines).

4. **Performance**: The parsing should be efficient and not cause performance issues with large sections.

5. **Backward Compatibility**: Patterns 1-4 remain unchanged to maintain backward compatibility.

## Validation

After implementation, validate with the reported issue:
- **Issue**: 129v4:5.1 incorrectly shown as covered in sections 5 and 9
- **Expected**: 129v4:5.1 should only be shown as covered in sections where it's actually listed in an "AC covered:" line
- **Verification**: Manually check each section's "AC covered:" lines to confirm the AC is actually listed

---

**Status**: ⏳ **AWAITING APPROVAL**

**Created**: 2025-01-XX  
**Author**: AI Assistant  
**Review Required**: Yes

