# Observation Report - User Guide

**Version**: 1.0  
**Last Updated**: 2025-01-XX

---

## 📋 Overview

The Observation Report module allows you to create professional observation reports with embedded media. You can assign images, videos, PDFs, and audio files to placeholders in your text, reorder media, and export the final report as a DOCX document.

---

## 🚀 Getting Started

### Accessing the Module

1. Navigate to the application
2. Click on the **"Observation Report"** tab in the top navigation
3. You'll see the Observation Report interface with three main columns:
   - **Left**: Media Browser
   - **Center**: Live Preview
   - **Right**: Standards

---

## 📖 Workflows

### Workflow 1: Initial Setup and Media Selection

**Steps:**
1. **Select Qualification**: Choose a qualification from the dropdown at the top
2. **Select Learner**: Choose a learner from the learner dropdown (populated after qualification selection)
3. **Select Standards**: Choose a standards file from the standards dropdown
4. **Media Browser**: The left column will display all available media files for the selected learner

**Tips:**
- Media files are organized by qualification and learner
- Supported file types: JPG, JPEG, PNG (images), MP4, MOV (videos), PDF (documents), MP3 (audio)

---

### Workflow 2: Creating Content with Placeholders

**Steps:**
1. **Expand Text Editor**: Click on the **"Text Editor"** section header (at bottom of page) to expand it
2. **Enter Text**: Type your observation report text in the text editor
3. **Add Placeholders**: Use the format `{{Placeholder_Name}}` to mark where media should appear
   - Example: `{{Site_Arrival_Induction}}`
   - Placeholder names can contain letters, numbers, and underscores
   - Placeholder names cannot start with numbers
4. **View Live Preview**: As you type, the center column shows a live preview of how your document will look
5. **Check Statistics**: The text editor header shows:
   - Number of placeholders found
   - Word count
   - Number of assigned/unassigned placeholders

**Example:**
```
Section 1: Health and Safety

{{Site_Arrival_Induction}}

The site arrival process was conducted properly.

{{Safety_Briefing}}

Safety procedures were explained clearly.
```

**Tips:**
- Placeholders are case-sensitive: `{{Placeholder1}}` and `{{placeholder1}}` are different
- Each placeholder is assigned a unique color in the preview
- Placeholders appear highlighted in the text editor

---

### Workflow 3A: Assigning Media (Click-to-Assign)

**Steps:**
1. **Select Media**: Click on a media card in the Media Browser (left column)
2. **Single Placeholder**: If your text has only one placeholder, the media is assigned immediately
3. **Multiple Placeholders**: If your text has multiple placeholders, a dialog appears:
   - Select which placeholder to assign to
   - Click "Assign" to confirm
   - Click "Cancel" to cancel

**Tips:**
- Assigned media cards are marked with a checkmark (✓)
- Assigned media cards cannot be dragged again
- You can assign the same media to multiple placeholders by clicking it multiple times

---

### Workflow 3B: Assigning Media (Drag-and-Drop)

**Steps:**
1. **Find Media**: Locate the media card you want to assign in the Media Browser
2. **Drag**: Click and hold on the media card
3. **Drop**: Drag it over to a placeholder drop zone in the Live Preview (center column)
4. **Release**: Release the mouse button to drop
5. **Assignment Complete**: The media appears in the placeholder, and the media card is marked as assigned

**Visual Feedback:**
- While dragging, the media card becomes semi-transparent
- Valid drop zones are highlighted with a blue dashed border
- Invalid drop zones show a red dashed border

**Tips:**
- You can drag media directly into empty placeholder cells
- Drop zones appear as dashed borders in placeholder tables

---

### Workflow 3C: Assigning Media (Bulk Assignment)

**Steps:**
1. **Select Multiple Media**: 
   - **Windows/Linux**: Hold `Ctrl` and click multiple media cards
   - **Mac**: Hold `Cmd` and click multiple media cards
2. **Drag All**: Click and drag any selected media card
3. **Drop**: Drop into a placeholder drop zone
4. **All Assigned**: All selected media items are assigned to the placeholder in order

**Tips:**
- Selected media cards are highlighted
- All selected media are assigned when you drop
- The order of assignment matches the order you selected them

---

### Workflow 4: Reordering Media Within Placeholders

**Two Methods:**

#### Method 1: Arrow Buttons

**Steps:**
1. **Find Media Item**: Locate the media item in the Live Preview placeholder table
2. **Use Arrows**: Click the **↑** (up) or **↓** (down) buttons on the media item
3. **Reorder**: The media moves up or down in the placeholder
4. **Disabled States**: 
   - The up arrow is disabled on the first item
   - The down arrow is disabled on the last item

#### Method 2: Drag-and-Drop Within Table

**Steps:**
1. **Start Drag**: Click and hold on a media item in the placeholder table
2. **Drag**: Move it over another media item
3. **Drop**: Release to swap positions or insert
4. **Visual Feedback**: 
   - The item being dragged is highlighted
   - Target positions show an insertion line
   - The table layout (2 columns) is maintained

**Tips:**
- Media is arranged in a 2-column table layout
- Position 0 = Top-left, Position 1 = Top-right, Position 2 = Second row left, etc.
- The order is preserved when you save drafts and export

---

### Workflow 5: Header Information Entry

**Steps:**
1. **Expand Header Section**: Click on the **"Header"** section header (at bottom of page)
2. **Fill Fields**:
   - **Learner**: Enter learner name
   - **Assessor**: Enter assessor name
   - **Visit Date**: Select date from date picker
   - **Location**: Enter location
   - **Address**: Enter address
3. **Auto-Save**: Header data is saved automatically as you type

**Tips:**
- Header information appears in exported DOCX documents
- All fields are optional

---

### Workflow 6: Assessor Feedback Entry

**Steps:**
1. **Expand Assessor Feedback Section**: Click on the **"Assessor Feedback"** section header
2. **Enter Feedback**: Type your feedback in the textarea
3. **Auto-Save**: Feedback is saved automatically

**Tips:**
- Assessor feedback appears at the end of exported DOCX documents
- This section is separate from the main observation text

---

### Workflow 7: Section Management

**About Sections:**
- Sections are automatically detected when text starts with `SECTION` keyword
- Example: `SECTION Health and Safety` creates a section titled "Health and Safety"
- Sections appear in the Live Preview with section headers
- Sections can be expanded/collapsed in the preview

**Tips:**
- Sections help organize long documents
- Section headers appear in the exported DOCX

---

### Workflow 8: Saving Drafts

**Steps:**
1. **Click Save Draft**: Click the **"💾 Save Draft"** button at the bottom
2. **Enter Name**: Enter a name for your draft in the dialog
3. **Confirm**: Click "Save" or press Enter
4. **Success**: You'll see a confirmation message

**What Gets Saved:**
- Text content with placeholders
- Media assignments
- Header information
- Assessor feedback
- Media order/positioning

**Tips:**
- Draft names should be descriptive
- Drafts are saved locally on the server
- You can save multiple drafts

---

### Workflow 9: Loading Drafts

**Steps:**
1. **Click Load Draft**: Click the **"📂 Load Draft"** button at the top
2. **Select Draft**: Click on a draft from the list
3. **Load**: Click "Load" on the draft item
4. **Loaded**: All content, assignments, and settings are restored

**What Gets Loaded:**
- Text content
- Media assignments
- Header information
- Assessor feedback
- Qualification and learner selections (if available)

**Tips:**
- Drafts show the date/time they were last updated
- You can delete drafts by clicking the delete button (if available)

---

### Workflow 10: Standards Management

**Steps:**
1. **Select Standards**: Choose a standards file from the standards dropdown at the top
2. **View Standards**: The right column displays units and assessment criteria (ACs)
3. **Search**: Use the search box to find specific ACs
4. **Expand/Collapse**: Click unit headers to expand/collapse
5. **View Coverage**: ACs that are covered (linked to sections) are highlighted

**Tips:**
- Standards are read from JSON files
- Coverage is automatically detected based on section links
- You can navigate to sections from the standards panel

---

### Workflow 11: Document Preview

**Steps:**
1. **Click Preview Draft**: Click the **"👁️ Preview Draft"** button at the bottom
2. **Preview Opens**: A full-screen preview dialog opens
3. **Three Columns**:
   - **Left**: Section navigation
   - **Center**: Preview content (formatted as DOCX will appear)
   - **Right**: Actions panel
4. **Actions Panel**:
   - **Font Settings**: Adjust font size and font family
   - **Visibility Toggles**: Show/hide sections, placeholders
   - **Export DOCX**: Click to export
   - **Update Draft**: Save changes back to draft

**Tips:**
- Preview shows exactly how the DOCX will look
- You can adjust settings and see live preview updates
- Use section navigation to jump to specific sections

---

### Workflow 11 (duplicate): DOCX Export

**Steps:**
1. **From Preview**: Click **"Export DOCX"** in the preview dialog
   - Or from main page, click **"👁️ Preview Draft"** then export
2. **From Actions Panel**: In preview, click **"Export DOCX"** button
3. **Enter Filename**: Enter a filename for the DOCX (default: "observation_report.docx")
4. **Export**: Click "Export" or press Enter
5. **Download**: The DOCX file downloads to your computer

**What Gets Exported:**
- Header information (learner, assessor, date, location, address)
- Formatted text content with media embedded
- Media files in 2-column tables within placeholders
- Images: Embedded directly in document
- Videos/PDFs/Audio: Filenames displayed (files linked)
- Assessor feedback at the end
- Sections with headers

**Tips:**
- DOCX files are generated on the server
- Large documents may take a moment to generate
- Media files must be accessible for embedding

---

### Workflow 12: Media Management

**Rename Files:**
- Click on a filename in a media card
- Edit the name inline
- Press Enter to save

**View Media Info:**
- Hover over media cards to see file size
- Images show thumbnails
- Videos show duration (if available)

**Filter Media:**
- Use the media browser header controls
- Search by filename (if search available)

---

## 🎨 Interface Guide

### Top Controls

- **Qualification Dropdown**: Select qualification
- **Learner Dropdown**: Select learner (enabled after qualification)
- **Standards Dropdown**: Select standards file
- **Load Draft Button**: Open draft load dialog
- **Refresh Button**: Refresh media browser

### Three-Column Layout

- **Left Column (Media Browser)**: Browse and select media files
- **Center Column (Live Preview)**: See document preview with placeholders
- **Right Column (Standards)**: View assessment criteria and units
- **Resizable**: Drag the borders between columns to resize

### Bottom Sections

- **Header Section**: Enter header information
- **Text Editor Section**: Write observation text with placeholders
- **Assessor Feedback Section**: Enter assessor feedback

### Action Buttons

- **Save Draft**: Save current work as draft
- **Preview Draft**: Open full-screen preview dialog

---

## 🔧 Keyboard Shortcuts

- **Ctrl/Cmd + Click**: Select multiple media items
- **Enter**: Save inline edits (filename changes)
- **Esc**: Cancel dialogs

---

## ❓ Troubleshooting

### Media Not Loading

**Problem**: Media browser is empty  
**Solution**: 
- Check that qualification and learner are selected
- Verify media files exist in the correct folder structure
- Click "Refresh" button

### Placeholders Not Showing

**Problem**: Placeholders don't appear in preview  
**Solution**:
- Check placeholder format: `{{Placeholder_Name}}`
- Ensure placeholder name is alphanumeric with underscores only
- Check that placeholder doesn't start with a number
- Refresh the page if needed

### Drag-and-Drop Not Working

**Problem**: Can't drag media to placeholders  
**Solution**:
- Ensure media card is not already assigned (check for checkmark)
- Verify you're dragging to a valid drop zone (blue dashed border)
- Try refreshing the page
- Check browser console for errors

### Reorder Not Working

**Problem**: Arrow buttons or drag reorder not working  
**Solution**:
- Ensure there are at least 2 media items in the placeholder
- Check that you're not trying to move first item up or last item down
- Refresh the page if needed

### DOCX Export Fails

**Problem**: Export button doesn't work or file doesn't download  
**Solution**:
- Check that all required fields are filled
- Verify media files are accessible
- Check browser console for errors
- Try again after a moment (server may be processing)

### Draft Not Loading

**Problem**: Draft doesn't appear or doesn't load  
**Solution**:
- Verify draft exists in the list
- Check that all required data is present
- Try refreshing the page
- Contact administrator if issue persists

---

## 📝 Tips & Best Practices

### Creating Effective Reports

1. **Plan Your Structure**: Think about sections before writing
2. **Use Descriptive Placeholders**: `{{Site_Arrival_Induction}}` is better than `{{Placeholder1}}`
3. **Assign Media Strategically**: Group related media together
4. **Review Preview**: Always preview before exporting
5. **Save Frequently**: Save drafts often to avoid losing work

### Placeholder Best Practices

- Use clear, descriptive names
- Use underscores instead of spaces
- Keep names consistent throughout document
- Don't use special characters

### Media Organization

- Organize media files logically in folders
- Use descriptive filenames
- Keep file sizes reasonable for faster loading
- Ensure all media is accessible

---

## 🆘 Support

If you encounter issues:

1. **Check Troubleshooting**: Review the troubleshooting section above
2. **Browser Console**: Check browser console for error messages (F12)
3. **Contact Support**: Report issues to your system administrator
4. **Documentation**: Refer to this guide and other documentation

---

## 📚 Additional Resources

- **Developer Guide**: See `docs/observation-report/DEVELOPER_GUIDE.md`
- **API Reference**: See `docs/observation-report/API_REFERENCE.md`
- **Specification**: See `docs/observation-media-complete-specification.md`

---

**Last Updated**: 2025-01-XX  
**Version**: 1.0



