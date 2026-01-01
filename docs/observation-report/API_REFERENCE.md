# Observation Report - API Reference

**Version**: 1.0  
**Base URL**: `/observation-report`  
**Last Updated**: 2025-01-XX

---

## 📋 Overview

This document describes all API endpoints for the Observation Report module. All endpoints return JSON responses.

---

## 🔐 Authentication

Currently, no authentication is required. All endpoints are publicly accessible.

---

## 📡 Endpoints

### Main Page

#### `GET /observation-report`

Returns the main Observation Report page (HTML).

**Response**: HTML page

---

### Learners

#### `GET /observation-report/learners`

Get list of learners for a qualification.

**Query Parameters**:
- `qualification` (string, required) - Qualification name

**Example Request**:
```
GET /observation-report/learners?qualification=Level%202%20Cladding
```

**Example Response**:
```json
{
  "success": true,
  "learners": [
    "John Doe",
    "Jane Smith"
  ]
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Qualification not found"
}
```

---

### Media Files

#### `GET /observation-report/media`

Get media files for a qualification and learner.

**Query Parameters**:
- `qualification` (string, required) - Qualification name
- `learner` (string, required) - Learner name

**Example Request**:
```
GET /observation-report/media?qualification=Level%202%20Cladding&learner=John%20Doe
```

**Example Response**:
```json
{
  "success": true,
  "media": [
    {
      "filename": "image1.jpg",
      "file_path": "/path/to/image1.jpg",
      "file_type": "image",
      "size": 1024000,
      "relative_path": "qualification/learner/image1.jpg",
      "thumbnail_path": "qualification/learner/image1_thumb.jpg"
    }
  ]
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Media files not found"
}
```

---

### Media File Serving

#### `GET /observation-report/media/<path:file_path>`

Serve a media file.

**URL Parameters**:
- `file_path` (path, required) - Relative path to media file

**Example Request**:
```
GET /observation-report/media/qualification/learner/image1.jpg
```

**Response**: Binary file (image/video/pdf/audio)

---

### Drafts

#### `GET /observation-report/drafts`

List all saved drafts.

**Example Request**:
```
GET /observation-report/drafts
```

**Example Response**:
```json
{
  "success": true,
  "drafts": [
    {
      "draft_name": "draft_20250115_123456",
      "updated_at": "2025-01-15T12:34:56"
    }
  ]
}
```

---

#### `POST /observation-report/drafts`

Create a new draft.

**Request Body**:
```json
{
  "text_content": "Text content with {{Placeholder1}}",
  "assignments": {
    "Placeholder1": [
      {
        "filename": "image1.jpg",
        "position": 0
      }
    ]
  },
  "header_data": {
    "learner": "John Doe",
    "assessor": "Jane Smith",
    "visit_date": "2025-01-15",
    "location": "Site A",
    "address": "123 Main St"
  },
  "assessor_feedback": "Feedback text"
}
```

**Example Response**:
```json
{
  "success": true,
  "draft_name": "draft_20250115_123456"
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Failed to save draft"
}
```

---

#### `GET /observation-report/drafts/<draft_name>`

Load a draft by name.

**URL Parameters**:
- `draft_name` (string, required) - Draft name

**Example Request**:
```
GET /observation-report/drafts/draft_20250115_123456
```

**Example Response**:
```json
{
  "success": true,
  "draft": {
    "text_content": "Text content with {{Placeholder1}}",
    "assignments": {
      "Placeholder1": [
        {
          "filename": "image1.jpg",
          "position": 0
        }
      ]
    },
    "header_data": {
      "learner": "John Doe",
      "assessor": "Jane Smith"
    },
    "assessor_feedback": "Feedback text",
    "updated_at": "2025-01-15T12:34:56"
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Draft not found"
}
```

---

#### `PUT /observation-report/drafts/<draft_name>`

Update an existing draft.

**URL Parameters**:
- `draft_name` (string, required) - Draft name

**Request Body**: Same as POST `/observation-report/drafts`

**Example Response**:
```json
{
  "success": true,
  "draft_name": "draft_20250115_123456"
}
```

---

#### `DELETE /observation-report/drafts/<draft_name>`

Delete a draft.

**URL Parameters**:
- `draft_name` (string, required) - Draft name

**Example Request**:
```
DELETE /observation-report/drafts/draft_20250115_123456
```

**Example Response**:
```json
{
  "success": true
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Draft not found"
}
```

---

### DOCX Export

#### `POST /observation-report/export-docx`

Generate and export a DOCX document.

**Request Body**:
```json
{
  "text_content": "Text content with {{Placeholder1}}",
  "assignments": {
    "Placeholder1": [
      {
        "filename": "image1.jpg",
        "file_path": "/path/to/image1.jpg",
        "position": 0
      }
    ]
  },
  "header_data": {
    "learner": "John Doe",
    "assessor": "Jane Smith",
    "visit_date": "2025-01-15",
    "location": "Site A",
    "address": "123 Main St"
  },
  "assessor_feedback": "Feedback text",
  "filename": "observation_report.docx",
  "font_size": 16,
  "font_name": "Times New Roman"
}
```

**Example Response**:
```json
{
  "success": true,
  "filename": "observation_report.docx"
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Failed to generate DOCX"
}
```

---

#### `GET /observation-report/download-docx/<filename>`

Download a generated DOCX file.

**URL Parameters**:
- `filename` (string, required) - DOCX filename

**Example Request**:
```
GET /observation-report/download-docx/observation_report.docx
```

**Response**: Binary file (application/vnd.openxmlformats-officedocument.wordprocessingml.document)

---

### File Operations

#### `POST /observation-report/rename-file`

Rename a media file.

**Request Body**:
```json
{
  "old_path": "qualification/learner/old_name.jpg",
  "new_name": "new_name.jpg"
}
```

**Example Response**:
```json
{
  "success": true,
  "new_path": "qualification/learner/new_name.jpg"
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "File not found or rename failed"
}
```

---

## 📊 Response Format

### Success Response

All successful responses follow this format:
```json
{
  "success": true,
  "data": { /* response data */ }
}
```

### Error Response

All error responses follow this format:
```json
{
  "success": false,
  "error": "Error message"
}
```

---

## 🚨 Error Codes

| HTTP Status | Meaning |
|------------|---------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 404 | Not Found (resource doesn't exist) |
| 500 | Internal Server Error |

---

## 📝 Request/Response Examples

### Complete Workflow Example

1. **Get Learners**:
```bash
GET /observation-report/learners?qualification=Level%202%20Cladding
```

2. **Get Media**:
```bash
GET /observation-report/media?qualification=Level%202%20Cladding&learner=John%20Doe
```

3. **Save Draft**:
```bash
POST /observation-report/drafts
Content-Type: application/json

{
  "text_content": "{{Placeholder1}}",
  "assignments": {"Placeholder1": []},
  "header_data": {},
  "assessor_feedback": ""
}
```

4. **Export DOCX**:
```bash
POST /observation-report/export-docx
Content-Type: application/json

{
  "text_content": "{{Placeholder1}}",
  "assignments": {"Placeholder1": [{"filename": "image1.jpg", "position": 0}]},
  "header_data": {"learner": "John Doe"},
  "assessor_feedback": "",
  "filename": "report.docx"
}
```

5. **Download DOCX**:
```bash
GET /observation-report/download-docx/report.docx
```

---

## 🔧 Development Notes

- All endpoints use JSON for request/response bodies (except file serving)
- File paths are validated to prevent directory traversal
- Draft names are auto-generated with timestamps
- DOCX files are generated server-side and stored temporarily

---

**Last Updated**: 2025-01-XX  
**Version**: 1.0



