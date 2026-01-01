# Observation AC Matrix - Technical Specification

## 1. Overview

### 1.1 Purpose
The Observation AC Matrix module provides a tool for comparing observation report text against assessment criteria (ACs) defined in JSON standards files. It generates a color-coded matrix showing which ACs are covered and which are missing from the observation report.

### 1.2 Scope
- Parse JSON standards files containing qualifications, units, learning outcomes, and questions (ACs)
- Extract AC references from observation report text
- Generate visual matrix comparing found ACs against all ACs in the selected standards file
- Save, load, and delete matrix analyses
- Support multiple JSON standards files

### 1.3 Key Features
- JSON file selection and management
- AC extraction from observation report text
- Color-coded matrix display (covered vs missing)
- Unit-based organization
- Save/Load/Delete functionality for matrices
- Dark theme UI

## 2. Data Model

### 2.1 JSON Standards File Structure
```json
{
  "export_info": {
    "format": "standards_report",
    "version": "1.0",
    "exported_at": "2025-12-05T22:48:36.047211"
  },
  "qualifications": [
    {
      "qualification_name": "Level 2 NVQ Diploma in Interior Systems v3",
      "units": [
        {
          "unit_name": "Conforming to General Health, Safety and Welfare in the Workplace",
          "unit_internal_id": "641",
          "learning_outcomes": [
            {
              "learning_outcome_name": "...",
              "learning_outcome_number": "1",
              "questions": [
                {
                  "question_id": "1.1",
                  "question_name": "...",
                  "question_type": "Practical"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### 2.2 AC (Assessment Criteria) Structure
- **AC ID**: The `question_id` field (e.g., "1.1", "2.3", "7.4")
- **AC Description**: The `question_name` field
- **Unit**: Parent unit containing the AC
- **Learning Outcome**: Parent learning outcome containing the AC

### 2.3 Matrix Data Structure
```python
{
  "matrix_id": "uuid",
  "name": "Matrix Name",
  "json_file_id": "file_id",
  "json_file_name": "filename.json",
  "observation_report": "text content",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z",
  "analysis": {
    "total_ac_count": 50,
    "covered_ac_count": 35,
    "missing_ac_count": 15,
    "coverage_percentage": 70.0,
    "units": [
      {
        "unit_id": "641",
        "unit_name": "...",
        "total_ac_count": 10,
        "covered_ac_count": 7,
        "missing_ac_count": 3,
        "acs": [
          {
            "ac_id": "1.1",
            "ac_description": "...",
            "learning_outcome": "1",
            "status": "covered",  # or "missing"
            "matched_text": "AC 1.1",  # text that matched
            "section_title": "Site Induction",  # section title where AC was found (if applicable)
            "section_index": 0,  # section index for color coding (matches observation-media SECTION_COLORS)
            "observation_text_section": "During the site induction, AC 1.1 was covered when the site manager explained the procedures...",  # text section from observation report
            "observation_context_start": 45,  # character position in obs text
            "observation_context_end": 320,  # end position
            "full_section": true  # whether section is complete or truncated
          }
        ]
      }
    ]
  }
}
```

### 2.4 Saved Matrix Storage
- **Location**: `data/ac_matrices/` directory
- **Format**: JSON files named `{matrix_id}.json`
- **Index File**: `data/ac_matrices/index.json` containing metadata for all saved matrices

## 3. Backend Architecture

### 3.1 File Structure
```
app/
├── ac_matrix_parser.py      # JSON parsing and AC extraction
├── ac_matrix_analyzer.py   # AC matching and matrix generation
├── ac_matrix_storage.py    # Save/Load/Delete operations
└── routes.py               # API endpoints (add new routes)
```

### 3.2 Core Modules

#### 3.2.1 AC Matrix Parser (`ac_matrix_parser.py`)
**Purpose**: Parse JSON standards files and extract AC structure

**Functions**:
```python
def parse_standards_json(json_path: Path) -> dict:
    """
    Parse JSON standards file and return structured data.
    
    Returns:
        {
            "qualification_name": str,
            "units": [
                {
                    "unit_id": str,
                    "unit_name": str,
                    "learning_outcomes": [
                        {
                            "lo_number": str,
                            "lo_name": str,
                            "acs": [
                                {
                                    "ac_id": str,
                                    "ac_description": str,
                                    "question_type": str
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    """
    pass

def extract_all_acs(parsed_data: dict) -> list:
    """
    Extract flat list of all ACs with unit context.
    
    Returns:
        [
            {
                "ac_id": "1.1",
                "ac_description": "...",
                "unit_id": "641",
                "unit_name": "...",
                "learning_outcome": "1"
            }
        ]
    """
    pass
```

#### 3.2.2 AC Matrix Analyzer (`ac_matrix_analyzer.py`)
**Purpose**: Extract AC references from observation report and generate matrix

**Functions**:
```python
def extract_ac_references(text: str) -> set:
    """
    Extract AC IDs from observation report text.
    
    Patterns to match:
    - "AC 1.1", "AC1.1", "ac 1.1"
    - "1.1", "1.2", "2.3"
    - "ACs 1.1, 1.2, 2.3"
    - "Assessment Criteria 1.1"
    
    Returns:
        set of AC IDs (e.g., {"1.1", "1.2", "2.3"})
    """
    pass

def extract_ac_references_with_context(text: str) -> dict:
    """
    Extract AC IDs from observation report text with context.
    
    Returns:
        {
            "1.1": {
                "ac_id": "1.1",
                "matched_text": "AC 1.1",
                "context_snippet": "AC 1.1 was covered during the site induction...",
                "context_start": 45,
                "context_end": 120
            }
        }
    """
    pass

def generate_matrix(parsed_data: dict, found_acs: dict, observation_text: str) -> dict:
    """
    Generate matrix comparing found ACs against all ACs.
    
    Args:
        parsed_data: Parsed JSON standards data
        found_acs: Dict of AC IDs with context (from extract_ac_references_with_context)
        observation_text: Full observation report text
    
    Returns:
        Matrix data structure (see 2.3) with observation context included
    """
    pass

def calculate_coverage_stats(matrix_data: dict) -> dict:
    """
    Calculate coverage statistics.
    
    Returns:
        {
            "total_ac_count": int,
            "covered_ac_count": int,
            "missing_ac_count": int,
            "coverage_percentage": float
        }
    """
    pass
```

#### 3.2.3 AC Matrix Storage (`ac_matrix_storage.py`)
**Purpose**: Save, load, and delete matrix analyses

**Functions**:
```python
def save_matrix(matrix_data: dict, name: str) -> dict:
    """
    Save matrix to disk.
    
    Returns:
        {
            "success": bool,
            "matrix_id": str,
            "message": str
        }
    """
    pass

def load_matrix(matrix_id: str) -> dict:
    """
    Load matrix from disk.
    
    Returns:
        {
            "success": bool,
            "matrix_data": dict,
            "error": str (if failed)
        }
    """
    pass

def list_matrices() -> list:
    """
    List all saved matrices.
    
    Returns:
        [
            {
                "matrix_id": str,
                "name": str,
                "json_file_name": str,
                "created_at": str,
                "updated_at": str,
                "coverage_percentage": float
            }
        ]
    """
    pass

def delete_matrix(matrix_id: str) -> dict:
    """
    Delete matrix from disk.
    
    Returns:
        {
            "success": bool,
            "message": str
        }
    """
    pass
```

### 3.3 Routes

#### 3.3.1 Main Page Route
```python
@bp.route('/ac-matrix')
def ac_matrix():
    """AC Matrix main page - loads drafts server-side (no API needed)"""
    from app.draft_manager import list_drafts, load_draft
    
    # Get list of drafts for dropdown
    drafts_list = list_drafts()
    
    # Load full draft data for each draft (text_content needed)
    drafts_data = []
    for draft_info in drafts_list:
        draft_result = load_draft(draft_info['id'])
        if draft_result['success']:
            drafts_data.append({
                'id': draft_info['id'],
                'name': draft_info['name'],
                'text_content': draft_result['draft'].get('text_content', ''),
                'created_at': draft_info.get('created_at', ''),
                'updated_at': draft_info.get('updated_at', '')
            })
    
    return render_template('ac_matrix.html', drafts=drafts_data)
```

### 3.4 API Endpoints

#### 3.4.1 JSON File Management
```python
@bp.route('/ac-matrix/json-files', methods=['GET'])
def list_json_files():
    """List available JSON standards files"""
    pass

@bp.route('/ac-matrix/json-files', methods=['POST'])
def upload_json_file():
    """Upload new JSON standards file"""
    pass

@bp.route('/ac-matrix/json-files/<file_id>', methods=['DELETE'])
def delete_json_file(file_id):
    """Delete JSON standards file"""
    pass
```

#### 3.4.2 Matrix Analysis
```python
@bp.route('/ac-matrix/analyze', methods=['POST'])
def analyze_observation_report():
    """
    Analyze observation report against selected JSON file.
    
    Request:
        {
            "json_file_id": str,
            "observation_report": str
        }
    
    Response:
        {
            "success": bool,
            "matrix_data": dict,
            "error": str (if failed)
        }
    """
    pass
```

#### 3.4.3 Matrix Storage
```python
@bp.route('/ac-matrix/matrices', methods=['GET'])
def list_matrices():
    """List all saved matrices"""
    pass

@bp.route('/ac-matrix/matrices', methods=['POST'])
def save_matrix():
    """
    Save matrix analysis.
    
    Request:
        {
            "name": str,
            "json_file_id": str,
            "observation_report": str,
            "matrix_data": dict
        }
    """
    pass

@bp.route('/ac-matrix/matrices/<matrix_id>', methods=['GET'])
def load_matrix(matrix_id):
    """Load saved matrix"""
    pass

@bp.route('/ac-matrix/matrices/<matrix_id>', methods=['DELETE'])
def delete_matrix(matrix_id):
    """Delete saved matrix"""
    pass
```

## 4. Frontend Architecture

### 4.1 File Structure
```
templates/
└── ac_matrix.html          # Main template

static/
├── css/
│   └── ac-matrix.css      # Module-specific styles
└── js/
    └── ac-matrix.js       # Module JavaScript
```

### 4.2 Template Structure (`ac_matrix.html`)
```html
{% extends "base.html" %}

{% block content %}
<div class="ac-matrix-container">
    <!-- Header -->
    <header class="ac-matrix-header">
        <h1>Observation AC Matrix</h1>
        <p>Compare observation reports against assessment criteria</p>
    </header>

    <!-- Settings Panel -->
    <section class="settings-panel">
        <h2>Settings</h2>
        <div class="json-file-selector">
            <label>JSON Standards File:</label>
            <select id="json-file-selector">
                <option value="">Select a standards file...</option>
            </select>
            <button id="upload-json-btn">Add New File</button>
        </div>
    </section>

    <!-- Input Section -->
    <section class="input-section">
        <h2>Observation Report</h2>
        <div class="draft-loader">
            <label>Load from Draft:</label>
            <select id="draft-selector">
                <option value="">Select a draft...</option>
                {% for draft in drafts %}
                <option value="{{ draft.id }}" data-text-content="{{ draft.text_content|e }}">{{ draft.name }} ({{ draft.created_at[:10] }})</option>
                {% endfor %}
            </select>
            <button id="load-draft-btn" class="btn-secondary">Load</button>
        </div>
        <textarea id="observation-report" placeholder="Paste or type your observation report text here... Or load from Observation Media drafts."></textarea>
        <button id="analyze-btn" class="btn-primary">Analyze Report</button>
    </section>
    
    <!-- Draft data available in JavaScript (no API needed) -->
    <script>
        // Drafts data loaded server-side
        const draftsData = {{ drafts|tojson }};
    </script>

    <!-- Matrix Display -->
    <section class="matrix-section" id="matrix-section" style="display: none;">
        <h2>AC Coverage Matrix</h2>
        <div class="matrix-controls">
            <label>Display Style:</label>
            <select id="display-style-selector">
                <option value="vertical">Vertical</option>
                <option value="horizontal">Horizontal</option>
            </select>
        </div>
        <div class="matrix-summary" id="matrix-summary"></div>
        <div class="matrix-content" id="matrix-content"></div>
    </section>

    <!-- Actions Panel -->
    <section class="actions-panel">
        <button id="save-matrix-btn" class="btn-secondary">Save Matrix</button>
        <div class="load-matrix-dropdown">
            <button id="load-matrix-btn" class="btn-secondary">Load Matrix ▼</button>
            <div id="load-matrix-menu" class="dropdown-menu"></div>
        </div>
        <button id="delete-matrix-btn" class="btn-danger">Delete Matrix</button>
    </section>
</div>
{% endblock %}
```

### 4.3 JavaScript Module (`ac-matrix.js`)

**Constants**:
```javascript
// Section color palette (same as observation-media.js)
const SECTION_COLORS = [
    '#667eea', // Blue
    '#f093fb', // Pink
    '#4facfe', // Light Blue
    '#43e97b', // Green
    '#fa709a', // Rose
    '#fee140', // Yellow
    '#30cfd0', // Cyan
    '#a8edea', // Aqua
    '#ff9a9e', // Coral
    '#fad0c4'  // Peach
];
```

**Key Functions**:
```javascript
// Initialize module
function initACMatrix() {
    loadJSONFiles();
    setupEventListeners();
    setupDraftLoader();
}

// Load available JSON files
async function loadJSONFiles() {
    // Fetch from /ac-matrix/json-files
    // Populate dropdown
}

// Setup draft loader (drafts already loaded in page, no API needed)
function setupDraftLoader() {
    const draftSelector = document.getElementById('draft-selector');
    const loadBtn = document.getElementById('load-draft-btn');
    const textarea = document.getElementById('observation-report');
    
    loadBtn.addEventListener('click', () => {
        const selectedOption = draftSelector.options[draftSelector.selectedIndex];
        if (!selectedOption || !selectedOption.value) return;
        
        // Get text_content from data attribute (loaded server-side)
        const textContent = selectedOption.getAttribute('data-text-content');
        if (textContent) {
            // Decode HTML entities
            const textareaElement = document.createElement('textarea');
            textareaElement.innerHTML = textContent;
            textarea.value = textareaElement.value;
        }
    });
}

// Analyze observation report
async function analyzeReport() {
    const jsonFileId = document.getElementById('json-file-selector').value;
    const reportText = document.getElementById('observation-report').value;
    
    // POST to /ac-matrix/analyze
    // Display matrix results
    // Store matrix data for style switching
}

// Handle display style change
function setupDisplayStyleToggle() {
    const styleSelector = document.getElementById('display-style-selector');
    styleSelector.addEventListener('change', (e) => {
        const style = e.target.value;
        if (window.currentMatrixData) {
            renderMatrix(window.currentMatrixData, style);
        }
    });
}

// Generate matrix HTML
function renderMatrix(matrixData, displayStyle = 'vertical') {
    if (displayStyle === 'vertical') {
        renderVerticalMatrix(matrixData);
    } else if (displayStyle === 'horizontal') {
        renderHorizontalMatrix(matrixData);
    }
}

// Render vertical style matrix
function renderVerticalMatrix(matrixData) {
    // Create table for each unit
    // Columns: AC ID | AC Description | Status | Where Covered (separate column)
    // 
    // Column 4: "Where Covered" - separate column
    // For COVERED ACs:
    //   - Section title (styled with SECTION_COLORS, same as observation-media)
    //     - font-weight: bold, font-size: 14pt
    //     - color: SECTION_COLORS[section_index % SECTION_COLORS.length]
    //     - border-left: 4px solid in section color
    //     - padding-left: 10px
    //     - margin: 15px 0 10px 0
    //   - Label: "Observation Text:"
    //   - Observation text section from report
    //   - "Show more" / "Show less" if text is truncated
    //
    // For MISSING ACs:
    //   - Show "(Not covered in observation)" in the Where Covered column
    //
    // Color code rows (covered/missing)
    // Different styling (background, border) to distinguish from standard description
}

// Render horizontal style matrix
function renderHorizontalMatrix(matrixData) {
    // For each unit:
    //   First line: "Unit: [Unit Name] | ACs: 1.1  1.2  1.3  2.1..."
    //   Second line: "Status: ✓  ✓  ✗  ✓  ✗..." (aligned below each AC)
    //   
    //   Clickable ACs: Click on any AC to expand details panel below
    //   Expandable details panel shows:
    //     - AC ID and status (✓ COVERED or ✗ MISSING)
    //     - For covered ACs:
    //       - Section title (styled with SECTION_COLORS, same as observation-media)
    //       - Observation text section
    //     - For missing ACs:
    //       - "(No observation text found)"
    //   
    //   Multiple ACs can be expanded at once
    //   Color code: Green for covered (✓), Red for missing (✗)
}

// Save matrix
async function saveMatrix() {
    // Show dialog for matrix name
    // POST to /ac-matrix/matrices
}

// Load matrix
async function loadMatrix(matrixId) {
    // GET from /ac-matrix/matrices/{matrixId}
    // Restore all data and regenerate matrix
}

// Delete matrix
async function deleteMatrix(matrixId) {
    // Confirm dialog
    // DELETE to /ac-matrix/matrices/{matrixId}
}
```

### 4.4 CSS Styling (`ac-matrix.css`)
- Dark theme colors (matching existing style.css)
- Color-coded matrix rows (green for covered, red for missing)
- Responsive table layout
- Collapsible unit sections
- Button and form styling

## 5. AC Extraction Algorithm

### 5.1 Pattern Matching with Context
The system uses regex patterns to extract AC references from observation report text with context:

```python
import re

AC_PATTERNS = [
    r'\bAC\s*(\d+\.\d+)',                    # "AC 1.1", "AC1.1"
    r'\bAssessment\s+Criteria\s*(\d+\.\d+)', # "Assessment Criteria 1.1"
    r'\bACs\s*[:\-]?\s*((?:\d+\.\d+(?:\s*,\s*)?)+)', # "ACs: 1.1, 1.2, 2.3"
    r'\b(\d+\.\d+)\b',                       # Standalone "1.1", "2.3"
]

def extract_ac_references_with_context(text: str, context_window: int = 150) -> dict:
    """
    Extract AC IDs from observation report text with surrounding context and section title.
    Returns the text section from the observation report where each AC is covered.
    
    Args:
        text: Observation report text
        context_window: Number of characters before/after match to include (default 150)
    
    Returns:
        {
            "1.1": {
                "ac_id": "1.1",
                "matched_text": "AC 1.1",
                "section_title": "Site Induction",  # Section title where AC was found (if applicable)
                "section_index": 0,  # Section index for color coding (0-based, matches observation-media)
                "observation_text_section": "During the site induction, AC 1.1 was covered when the site manager explained the procedures...",
                "context_start": 45,
                "context_end": 320,
                "match_position": 50,
                "full_section": True  # Whether this is the complete section or truncated
            }
        }
    """
    found_acs = {}
    
    for pattern in AC_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            ac_id = match.group(1) if match.groups() else match.group(0)
            
            # Handle comma-separated lists
            if ',' in ac_id:
                ac_ids = [ac.strip() for ac in ac_id.split(',')]
                for ac in ac_ids:
                    if re.match(r'^\d+\.\d+$', ac):
                        add_ac_with_context(found_acs, ac, match, text, context_window)
            else:
                if re.match(r'^\d+\.\d+$', ac_id):
                    add_ac_with_context(found_acs, ac_id, match, text, context_window)
    
    return found_acs

def find_section_title(text: str, position: int) -> dict:
    """
    Find the section title that contains the given position.
    Section titles match pattern: "SECTION:" or "SECTION -" followed by title.
    Returns both title and section index for color coding.
    
    Args:
        text: Full observation report text
        position: Character position to find section for
    
    Returns:
        {
            'title': str,  # Section title (without "SECTION:" prefix) or empty string
            'index': int   # Section index (0-based) for color coding, or -1 if not found
        }
    """
    import re
    section_pattern = re.compile(r'^SECTION\s*[:-]?\s*(.+)$', re.MULTILINE | re.IGNORECASE)
    
    # Find all section titles and their positions
    sections = []
    for match in section_pattern.finditer(text):
        sections.append({
            'title': match.group(1).strip(),
            'position': match.start()
        })
    
    # Find the section that contains the position
    current_section = None
    section_index = -1
    for idx, section in enumerate(sections):
        if section['position'] <= position:
            current_section = section
            section_index = idx
        else:
            break
    
    return {
        'title': current_section['title'] if current_section else '',
        'index': section_index
    }

def add_ac_with_context(found_acs: dict, ac_id: str, match: re.Match, text: str, context_window: int):
    """
    Add AC with observation text section and section title to found_acs dict.
    Extracts the text section from the observation report where the AC is covered.
    """
    match_start = match.start()
    match_end = match.end()
    
    # Find section title for this AC (returns title and index for color coding)
    section_info = find_section_title(text, match_start)
    section_title = section_info['title']
    section_index = section_info['index']
    
    # Extract context around match - this is the text section where AC is covered
    context_start = max(0, match_start - context_window)
    context_end = min(len(text), match_end + context_window)
    
    # Get the observation text section
    observation_text_section = text[context_start:context_end].strip()
    
    # Try to extract a complete sentence or paragraph if possible
    # Look for sentence boundaries
    sentence_start = context_start
    sentence_end = context_end
    
    # Try to find sentence start (period, newline, or start of text)
    for i in range(context_start, max(0, context_start - 200), -1):
        if text[i] in '.!\n' and i < match_start:
            sentence_start = i + 1
            break
        if i == 0:
            sentence_start = 0
            break
    
    # Try to find sentence end
    for i in range(context_end, min(len(text), context_end + 200)):
        if text[i] in '.!\n':
            sentence_end = i + 1
            break
        if i == len(text) - 1:
            sentence_end = len(text)
            break
    
    # Use sentence boundaries if they provide better context
    if sentence_end - sentence_start > context_end - context_start:
        observation_text_section = text[sentence_start:sentence_end].strip()
        context_start = sentence_start
        context_end = sentence_end
    
    # If AC already found, keep the first occurrence or merge contexts
    if ac_id not in found_acs:
        found_acs[ac_id] = {
            "ac_id": ac_id,
            "matched_text": match.group(0),
            "section_title": section_title,
            "section_index": section_index,  # For color coding (matches observation-media)
            "observation_text_section": observation_text_section,
            "context_start": context_start,
            "context_end": context_end,
            "match_position": match_start,
            "full_section": (context_end - context_start) < (context_window * 3)  # Rough check if truncated
        }
    else:
        # If multiple occurrences, append to context with separator
        existing = found_acs[ac_id]
        # If different section, note it
        if section_title and section_title != existing.get("section_title", ""):
            existing["observation_text_section"] += f"\n\n[... additional occurrence in Section: {section_title} ...]\n\n" + observation_text_section
        else:
            existing["observation_text_section"] += "\n\n[... additional occurrence ...]\n\n" + observation_text_section
        existing["context_end"] = context_end  # Update to include latest
```

### 5.2 Matching Strategy
1. Extract all potential AC references using regex patterns with context
2. Validate format (must match `\d+\.\d+`)
3. For each found AC:
   - Find the section title that contains the AC (pattern: "SECTION:" or "SECTION -" followed by title)
   - Extract observation text section (surrounding text, ~150 chars before/after, or full sentence/paragraph)
   - Store section title along with text section
4. Store the complete text section from observation report where each AC was found
5. Compare against ACs in selected JSON file
6. Mark as "covered" if found (with section title and full observation text section), "missing" if not
7. Display the observation text section prominently in matrix:
   - Vertical style: Expandable panel below each covered AC row
   - Horizontal style: Right column showing the observation text section
8. Format observation text sections with:
   - Section title displayed first (if available) with same styling as observation-media:
     - Uses SECTION_COLORS array (10 colors, cycling through sections)
     - font-weight: bold, font-size: 14pt
     - color: SECTION_COLORS[section_index % SECTION_COLORS.length]
     - border-left: 4px solid in section color
     - padding-left: 10px
     - margin: 15px 0 10px 0
   - Clear labeling ("Observation Text:" or "Observation Text Section:")
   - Distinct styling (background color, border, italic) to distinguish from standard descriptions
   - Expand/collapse for long sections

## 6. Data Storage

### 6.1 Directory Structure
```
data/
├── ac_matrices/
│   ├── index.json                    # Metadata index
│   ├── {matrix_id_1}.json            # Saved matrix 1
│   ├── {matrix_id_2}.json            # Saved matrix 2
│   └── ...
└── json_standards/
    ├── {file_id_1}.json              # Standards file 1
    ├── {file_id_2}.json              # Standards file 2
    └── ...
```

### 6.2 Index File Format
```json
{
  "matrices": [
    {
      "matrix_id": "uuid",
      "name": "Matrix Name",
      "json_file_id": "file_id",
      "json_file_name": "filename.json",
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z",
      "coverage_percentage": 70.0
    }
  ]
}
```

## 7. Error Handling

### 7.1 JSON Parsing Errors
- Invalid JSON format
- Missing required fields
- Malformed AC IDs

### 7.2 Analysis Errors
- No JSON file selected
- Empty observation report
- No ACs found in report

### 7.3 Storage Errors
- File system permissions
- Disk space issues
- Corrupted index file

## 8. Testing Requirements

### 8.1 Development Approach
- **Staged Development**: Implement in phases, test each stage before proceeding
- **Screenshot Testing**: Capture screenshots at each stage for verification
- **Working State**: Each stage must be fully functional before moving to next
- **Final Release**: All features must be working and tested before release

### 8.2 Unit Tests
- JSON parsing with various file structures
- AC extraction with different text patterns (exact match only, case-insensitive)
- Matrix generation logic
- Storage operations (save/load/delete)
- Section title extraction and color coding

### 8.3 Integration Tests
- Full workflow: select file → enter report → analyze → save
- Load saved matrix and verify data integrity
- Error handling for invalid inputs
- Draft loading from observation-media

### 8.4 UI Tests with Screenshots
- Matrix rendering with various data sizes
- Color coding accuracy (verify SECTION_COLORS match observation-media)
- Responsive layout behavior (desktop, tablet, mobile)
- Save/Load/Delete workflows
- Vertical style: 4-column layout with "Where Covered" column
- Horizontal style: AC row with status row, expandable details
- Section title styling (verify matches observation-media)
- Screenshot capture at each test stage

### 8.5 Screenshot Requirements
- **Stage 1**: JSON file selection and parsing
- **Stage 2**: AC extraction and basic matrix display
- **Stage 3**: Vertical style with "Where Covered" column
- **Stage 4**: Horizontal style with expandable details
- **Stage 5**: Section title color coding
- **Stage 6**: Save/Load/Delete functionality
- **Stage 7**: Draft loading integration
- **Final**: Complete workflow end-to-end

## 9. Future Enhancements

### 9.1 Potential Features
- Export matrix to PDF/Excel
- AC highlighting in observation report text
- Multiple observation reports comparison
- AC coverage trends over time
- Search/filter functionality in matrix
- Bulk AC reference import
- AC grouping by learning outcome
- Statistics dashboard

### 9.2 Performance Optimizations
- Lazy loading for large matrices
- Client-side caching of JSON files
- Incremental matrix updates
- Virtual scrolling for large tables

## 10. Configuration

### 10.1 Config Settings
```python
# config.py additions
AC_MATRIX_DATA_DIR = BASE_DIR / 'data' / 'ac_matrices'
AC_MATRIX_JSON_STANDARDS_DIR = BASE_DIR / 'data' / 'json_standards'
AC_MATRIX_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
AC_MATRIX_ALLOWED_EXTENSIONS = {'.json'}
```

## 11. Security Considerations

### 11.1 File Upload
- Validate JSON file structure before saving
- Sanitize file names
- Limit file size
- Restrict to .json extension only

### 11.2 Path Validation
- Ensure all file operations stay within data directories
- Prevent path traversal attacks
- Validate matrix IDs (UUID format)

### 11.3 Input Sanitization
- Sanitize observation report text (XSS prevention)
- Validate matrix names
- Escape special characters in file names

## 12. Questions & Considerations

### 12.1 Design Decisions (Approved)
1. **AC ID Format**: Only "X.Y" format supported (e.g., "1.1", "2.3") - no "1.1.1" variations
2. **Multiple Qualifications**: Each JSON file contains one qualification
3. **AC Matching**: No partial matches - exact match only (e.g., "1.1" only matches "1.1", not "1.1.1" or "1")
4. **Case Sensitivity**: AC matching is case-insensitive
5. **File Management**: Users cannot edit/delete uploaded JSON files (read-only after upload)
6. **Matrix Versioning**: No version tracking for saved matrices
7. **Export Format**: No export functionality needed

### 12.2 Design Decisions (Approved)
1. **Storage Backend**: File-based storage (no database)
2. **AC Extraction**: Regex-based pattern matching (no NLP)
3. **Matrix Display**: Table format (vertical and horizontal styles)
4. **Unit Organization**: Organized by qualification (hierarchical)
5. **Real-time Analysis**: Button click to analyze (no real-time on text change)

### 12.3 Edge Cases
1. **Empty Units**: Units with no questions/ACs
2. **Duplicate AC IDs**: Same AC ID in multiple units
3. **Invalid AC Format**: ACs with non-standard IDs
4. **Very Long Reports**: Performance with 10,000+ word reports
5. **Special Characters**: AC IDs with special characters
6. **Missing Learning Outcomes**: Units without learning outcomes

;;l