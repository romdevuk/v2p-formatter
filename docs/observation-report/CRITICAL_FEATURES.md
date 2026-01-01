# 🚨 Critical Features - Extra Attention Required

**Last Updated**: 2025-01-XX

---

## ⚠️ Important Notice

The following features were **major complexities** in the old observation-media module that didn't work properly. **EXTRA attention** must be paid to these features during development.

---

## 1. Drag-and-Drop Media Assignment

### Why It's Critical
- This was one of the most problematic features in the old module
- Complex state management between Media Browser and Live Preview
- Multiple scenarios to handle (single, bulk, multiple placeholders)
- Cross-browser compatibility challenges

### Key Implementation Areas

#### Frontend (Stage 2)
- **Media Browser Library**: Drag source implementation
  - Single media drag
  - Multiple media drag (bulk)
  - Drag state visual feedback
  - Prevent dragging assigned media
  
- **Live Preview Library**: Drop target implementation
  - Detect valid drop zones
  - Highlight drop zones on drag over
  - Handle drop events
  - Show selection dialog for multiple placeholders
  - Direct assignment for single placeholder

#### UX (Stage 3)
- Visual feedback during drag
- Drop zone highlighting
- Insertion indicators
- Smooth transitions

#### Testing (Stage 4)
- Comprehensive drag-and-drop testing
- Cross-browser verification
- Edge case handling
- Visual verification

### Reference Documentation
- **Specification**: Workflow 3B (lines 132-143)
- **Stage 2**: `STAGE_2_FRONTEND.md` - Drag-and-Drop section
- **Stage 3**: `STAGE_3_UX.md` - Drag-and-Drop Visual Feedback section
- **Stage 4**: `STAGE_4_TESTING.md` - Drag-and-Drop Testing section

---

## 2. Media Reshuffle/Reordering

### Why It's Critical
- Complex position calculation (2-column table layout)
- Real-time state synchronization
- Multiple reorder methods (drag-and-drop, arrow buttons)
- Persistence across draft saves/loads

### Key Implementation Areas

#### Frontend (Stage 2)
- **Live Preview Library**: Reorder implementation
  - Position-to-row/col calculation
  - Row/col-to-position calculation
  - Drag-and-drop reordering within table
  - Arrow button reordering (up/down)
  - Maintain 2-column layout
  - State synchronization

#### UX (Stage 3)
- Reordering visual feedback
- Target position indicators
- Insertion line/arrow styling
- Arrow button styling and states
- Smooth animations

#### Testing (Stage 4)
- Position calculation verification
- Layout verification
- State persistence testing
- Edge case handling

### Reference Documentation
- **Specification**: Workflow 4 (lines 160-177)
- **Stage 2**: `STAGE_2_FRONTEND.md` - Reshuffle section
- **Stage 3**: `STAGE_3_UX.md` - Reshuffle Visual Feedback section
- **Stage 4**: `STAGE_4_TESTING.md` - Reshuffle Testing section

---

## 📋 Implementation Checklist

### Drag-and-Drop
- [ ] Frontend: Media Browser drag source
- [ ] Frontend: Live Preview drop target
- [ ] Frontend: State synchronization
- [ ] Frontend: Multiple placeholder handling
- [ ] UX: Visual feedback styling
- [ ] UX: Drop zone highlighting
- [ ] Testing: Comprehensive test coverage
- [ ] Testing: Cross-browser verification

### Reshuffle
- [ ] Frontend: Position calculations
- [ ] Frontend: Drag-and-drop reorder
- [ ] Frontend: Arrow button reorder
- [ ] Frontend: Layout maintenance
- [ ] Frontend: State persistence
- [ ] UX: Visual feedback styling
- [ ] UX: Animation implementation
- [ ] Testing: Position verification
- [ ] Testing: Layout verification

---

## 🎯 Success Criteria

### Drag-and-Drop
✅ Users can drag media from browser to placeholder  
✅ Drop zones are clearly highlighted  
✅ Multiple placeholder scenario works correctly  
✅ Bulk drag-and-drop works  
✅ Visual feedback is smooth and clear  
✅ Works consistently across browsers  

### Reshuffle
✅ Users can reorder media within placeholder  
✅ Position calculations are correct  
✅ 2-column layout is maintained  
✅ Reorder persists in drafts  
✅ Visual feedback is smooth and clear  
✅ Arrow buttons work correctly  

---

## 📝 Notes for Developers

1. **Test Early and Often**: Don't wait until Stage 4 to test these features
2. **Visual Verification**: Take screenshots at each step
3. **Edge Cases**: Pay special attention to edge cases
4. **Browser Testing**: Test in all browsers throughout development
5. **State Management**: Ensure state is synchronized correctly
6. **Performance**: Test with many media items

---

## 🔗 Related Documents

- [STAGE_2_FRONTEND.md](./STAGE_2_FRONTEND.md) - Frontend implementation
- [STAGE_3_UX.md](./STAGE_3_UX.md) - UX styling
- [STAGE_4_TESTING.md](./STAGE_4_TESTING.md) - Testing requirements
- [checkpoints/stage_2_checklist.md](./checkpoints/stage_2_checklist.md) - Frontend checklist
- [checkpoints/stage_3_checklist.md](./checkpoints/stage_3_checklist.md) - UX checklist
- [checkpoints/stage_4_checklist.md](./checkpoints/stage_4_checklist.md) - Testing checklist

---

**Remember**: These features require **EXTRA attention** - don't rush them!



