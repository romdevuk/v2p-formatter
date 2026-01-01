# Orchestrator Instructions - Complete Workflow Testing

**For**: All Agents  
**Created**: 2025-01-XX  
**Priority**: HIGH

---

## 🎯 Mission

Test and fix the complete Observation Report workflow:
1. Open existing draft
2. Add media to placeholders
3. Fill header data
4. Add assessor feedback
5. Save draft
6. Export to DOCX

---

## 👥 Agent Team Assignments

### Backend Developer (Agent-1)
**Priority Tasks:**
1. ✅ FIXED: Added `relative_path` to media file responses
2. ✅ FIXED: Improved path handling in media serving endpoint
3. ⏳ TODO: Verify image serving works (test with actual files)
4. ⏳ TODO: Check DOCX export endpoint

**Files to Review:**
- `app/observation_report_scanner.py` - Media scanning
- `app/routes.py` - `/observation-report/media/<path>` endpoint
- `app/routes.py` - `/observation-report/export-docx` endpoint

**Test Command:**
```bash
# Test media serving directly
curl "http://localhost/v2p-formatter/observation-report/media/{qualification}/{learner}/filename.jpg"
```

---

### Frontend Developer (Agent-2)
**Priority Tasks:**
1. ✅ FIXED: Updated image src to use `relative_path`
2. ✅ FIXED: Fixed path encoding in image URLs
3. ⏳ TODO: Fix standards loading when draft is loaded
4. ⏳ TODO: Verify export DOCX button works

**Files to Review:**
- `static/js/observation-report.js` - Draft loading, standards trigger
- `static/js/observation-report/observation-report-live-preview.js` - Image rendering
- `static/js/observation-report/observation-report-preview-draft.js` - Export functionality

**Test Steps:**
1. Load draft
2. Check browser console for standards loading
3. Verify standards panel shows units

---

### UX Designer (Agent-3)
**Priority Tasks:**
1. ⏳ TODO: Verify all UI elements are visible and accessible
2. ⏳ TODO: Check preview dialog layout during workflow
3. ⏳ TODO: Verify export button visibility and clickability
4. ⏳ TODO: Check error states display correctly

**Test Steps:**
1. Go through complete workflow manually
2. Take screenshots at each step
3. Document any UI/UX issues

---

### Tester (Agent-4)
**Priority Tasks:**
1. ✅ DONE: Created complete workflow test
2. ✅ DONE: Initial test run (PASSED)
3. ⏳ TODO: Re-run test after fixes
4. ⏳ TODO: Verify 404 errors are gone
5. ⏳ TODO: Verify standards load correctly
6. ⏳ TODO: Document any remaining issues

**Test Command:**
```bash
pytest tests/test_observation_report_complete_workflow.py -v -s
```

**Check:**
- Browser console for errors
- Screenshots for visual verification
- Test output for failures

---

## 🧪 Running the Test

### Automated:
```bash
./tests/run_observation_report_complete_workflow.sh
```

### Manual:
```bash
pytest tests/test_observation_report_complete_workflow.py -v -s
```

---

## ✅ Success Criteria

All workflow steps must:
1. ✅ Open draft successfully
2. ✅ Display draft content (text, placeholders, sections)
3. ✅ Load media files in media browser
4. ✅ Allow media assignment via drag-and-drop
5. ✅ Allow header data entry
6. ✅ Allow feedback entry
7. ✅ Save draft successfully
8. ✅ Export DOCX successfully
9. ✅ No console errors (404s, etc.)
10. ✅ Standards panel shows units after loading draft

---

## 📋 Fix Checklist

### Image Loading (404 Errors)
- [x] Backend: Add relative_path to media responses
- [x] Frontend: Use relative_path for image src
- [ ] Test: Verify images load without 404 errors
- [ ] Test: Verify thumbnails load in media browser

### Standards Loading
- [ ] Frontend: Ensure standards load after draft load
- [ ] Frontend: Verify standards data is saved with draft
- [ ] Test: Verify standards panel shows units

### DOCX Export
- [ ] Backend: Verify export endpoint works
- [ ] Frontend: Verify export button triggers correctly
- [ ] Test: Verify DOCX file is generated and downloadable

---

## 📊 Current Status

**Last Test**: ✅ PASSED
**Issues Remaining**:
1. Image 404 errors (FIXING)
2. Standards panel empty (TO FIX)

**Screenshots**: `test_screenshots/observation_report_complete_workflow/`

---

**All Agents**: Work on your assigned tasks and update status when complete!



