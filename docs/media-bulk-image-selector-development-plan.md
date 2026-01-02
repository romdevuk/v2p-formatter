# Media Bulk Image Selector - Development Plan

## Overview
Develop the full-screen modal component for bulk image selection with zoom controls, auto-save, and real-time sync with main view.

## Development Stages

### Backend Stages

#### Stage 1: Backend API Review & Enhancement (If Needed)
**Objective**: Verify existing endpoints support the modal requirements

**Tasks**:
- [ ] Review `/list_images` endpoint - ensure it returns all necessary data
- [ ] Verify image metadata includes folder paths, file sizes, etc.
- [ ] Check if folder structure is properly organized
- [ ] Ensure thumbnail generation works efficiently for bulk display
- [ ] Test with large image collections (100+ images)

**Deliverables**:
- Document any API enhancements needed
- Performance testing results

**Testing**:
- Test `/list_images` with various folder structures
- Verify response format matches frontend expectations
- Check thumbnail generation performance

---

#### Stage 2: Backend Optimization (If Needed)
**Objective**: Optimize backend for modal performance

**Tasks**:
- [ ] Implement image metadata caching (if needed)
- [ ] Optimize thumbnail generation for bulk requests
- [ ] Add pagination support (if collection is very large)
- [ ] Implement folder structure optimization

**Deliverables**:
- Optimized endpoints
- Performance benchmarks

**Testing**:
- Load testing with large collections
- Response time measurements

---

### Frontend Stages

#### Stage 3: Basic Modal Structure
**Objective**: Create the full-screen modal container with basic layout

**Tasks**:
- [ ] Create `static/css/media-bulk-image-selector.css` with modal styles
- [ ] Create `static/js/media-bulk-image-selector.js` component file
- [ ] Implement modal container with overlay (dark background, full viewport)
- [ ] Add header bar with close button and selection counter
- [ ] Add footer bar structure (for zoom controls)
- [ ] Implement open/close modal functionality
- [ ] Add fade-in/out animations
- [ ] Add entry point button in main view ("Open Full Screen Selector" icon)

**Deliverables**:
- Modal opens/closes smoothly
- Header and footer bars visible
- Integration with `templates/image_to_pdf.html`

**Testing**:
- Modal opens from main view
- Modal closes with close button
- Escape key closes modal
- Smooth animations

---

#### Stage 4: Image Grid & Folder Structure
**Objective**: Display images in organized grid with folder grouping

**Tasks**:
- [ ] Load images from `/list_images` endpoint
- [ ] Render folder structure (root folder + subfolders)
- [ ] Implement folder/date headers (sticky on scroll optional)
- [ ] Create responsive image grid system
- [ ] Display thumbnails with checkboxes
- [ ] Show image filenames and file sizes
- [ ] Handle loading states (skeleton loaders)

**Deliverables**:
- Images displayed in organized grid
- Folder structure visible
- Thumbnails load correctly

**Testing**:
- Images load from API
- Folder structure displays correctly
- Root folder images show properly
- Subfolder images grouped correctly

---

#### Stage 5: Selection & Sequence Logic
**Objective**: Implement selection with sequence numbers and auto-save

**Tasks**:
- [ ] Implement click-to-select/deselect functionality
- [ ] Auto-assign sequence numbers (1, 2, 3...) based on selection order
- [ ] Display sequence badges on selected images
- [ ] Visual feedback (blue border, darker background) for selected items
- [ ] **Real-time sync with `window.appData.selectedImages`**
- [ ] **Auto-save on every selection change**
- [ ] Implement "Reset Order" button
- [ ] Handle sequence renumbering when images are deselected
- [ ] Ensure selections persist when zooming

**Deliverables**:
- Selection works with visual feedback
- Sequence numbers auto-assigned
- Real-time sync with main view state
- Auto-save on every change

**Testing**:
- Select/deselect images
- Verify sequence numbers assign correctly
- Check `window.appData.selectedImages` updates immediately
- Verify main view reflects changes when modal closes
- Test sequence renumbering on deselect

---

#### Stage 6: Zoom Controls & Dynamic Layout
**Objective**: Implement zoom slider and dynamic grid adjustment

**Tasks**:
- [ ] Add zoom slider to footer bar
- [ ] Add zoom in/out buttons (+/-)
- [ ] Implement zoom level calculation (1-10 levels)
- [ ] Map zoom levels to column counts (8 cols → 2 cols)
- [ ] Dynamic grid width calculation based on columns
- [ ] Smooth transitions when zoom changes
- [ ] Save zoom preference to localStorage (optional)
- [ ] Update grid layout on zoom change
- [ ] Maintain selection state during zoom

**Deliverables**:
- Zoom controls functional at bottom of modal
- Dynamic grid adjusts columns (2-8 columns)
- Smooth animations on zoom change

**Testing**:
- Zoom slider works
- Zoom in/out buttons work
- Grid adjusts columns correctly
- Selection preserved during zoom
- Smooth animations

---

#### Stage 7: State Management & Auto-Save
**Objective**: Ensure real-time sync and auto-save work correctly

**Tasks**:
- [ ] Implement `syncSelectionToMainView()` function
- [ ] Implement `onImageSelectionChange()` with immediate sync
- [ ] Update `window.appData.selectedImages` in real-time
- [ ] Update `window.appData.imageOrder` in real-time
- [ ] Ensure main view updates immediately when modal closes
- [ ] Load existing selections when modal opens
- [ ] Preserve state when closing/reopening modal
- [ ] Test edge cases (select all, clear all, reset order)

**Deliverables**:
- Real-time sync working
- Auto-save on every change
- State persists across modal open/close
- Main view reflects changes immediately

**Testing**:
- Select images → check `window.appData` updates
- Close modal → verify main view shows selections
- Reopen modal → verify selections restored
- Test with existing selections from main view

---

#### Stage 8: Polish & Enhancements
**Objective**: Add polish and optional enhancements

**Tasks**:
- [ ] Keyboard shortcuts (Escape to close, Space to select, Arrow keys to navigate)
- [ ] Select All / Clear All functionality (optional)
- [ ] Search/filter (optional - defer to later)
- [ ] Loading placeholders (skeleton loaders)
- [ ] Error handling for failed image loads
- [ ] Performance optimization (lazy loading, virtualization for very large collections)
- [ ] Accessibility improvements (ARIA labels, keyboard navigation)

**Deliverables**:
- Polished UI/UX
- Keyboard shortcuts working
- Error handling in place
- Performance optimized

**Testing**:
- Keyboard shortcuts work
- Error states handled gracefully
- Performance with large collections
- Accessibility testing

---

## Implementation Order

1. **Backend**: Stages 1-2 (if needed)
2. **Frontend**: Stages 3-8 (in sequence)

## Testing Strategy

### Unit Tests
- Selection logic functions
- Sequence number assignment
- Zoom calculation
- State sync functions

### Integration Tests
- Modal open/close
- Selection sync with main view
- Auto-save functionality
- Zoom controls

### E2E Tests (Playwright)
- Complete selection workflow
- Modal open → select images → close → verify selections
- Zoom controls → verify grid adjustment
- State persistence across sessions

## Dependencies

- Existing `/list_images` endpoint
- Existing thumbnail generation (`/thumbnail`)
- `window.appData.selectedImages` state structure
- Image to PDF module (`templates/image_to_pdf.html`)

## Notes

- Auto-save is critical - no manual save needed
- Real-time sync must update `window.appData` immediately
- Zoom controls must be at bottom of window (as per spec)
- No "Done" button - selections auto-save


