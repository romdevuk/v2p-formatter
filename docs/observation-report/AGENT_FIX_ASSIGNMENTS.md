# Agent Fix Assignments - Workflow Test Issues

**Status**: 🔄 Active  
**Created**: After workflow test run  
**Priority**: HIGH

---

## 🐛 Issues Found in Workflow Test

### Issue #1: Image Loading 404 Errors 🔴 CRITICAL

**Symptom**: Many 404 errors for image resources in browser console

**Root Cause**: Media paths may not be correctly formatted for serving

**Assigned To**: 
- **Backend Developer (Agent-1)**: Fix API path handling
- **Frontend Developer (Agent-2)**: Fix image src paths

**Files to Check**:
- `app/routes.py` - `/observation-report/media/<path:file_path>` endpoint
- `app/observation_report_scanner.py` - Path storage in scan results
- `static/js/observation-report/observation-report-live-preview.js` - Image src generation

**Fix Requirements**:
1. Ensure media paths in API are relative to OUTPUT_FOLDER
2. Verify path encoding handles special characters
3. Check image src URLs match endpoint expectations

**Test**: Re-run workflow test, check browser console for 404 errors

---

### Issue #2: Standards Panel Empty When Loading Draft 🟡 MEDIUM

**Symptom**: Standards panel shows no units after loading draft

**Assigned To**: **Frontend Developer (Agent-2)**

**Files to Check**:
- `static/js/observation-report.js` - Draft loading logic
- `static/js/observation-report/observation-report-standards.js` - Standards loading

**Fix Requirements**:
1. Ensure standards data is saved with draft
2. Ensure standards load after draft is loaded
3. Verify standards_file_id or json_file_id is preserved

**Test**: Load draft, verify standards panel shows units

---

## 📋 Fix Checklist

### Backend Developer (Agent-1)
- [ ] Check media path format in `scan_media_files()` response
- [ ] Verify `/observation-report/media/<path>` endpoint handles paths correctly
- [ ] Test with actual file paths to ensure 404s are resolved
- [ ] Verify path encoding/decoding

### Frontend Developer (Agent-2)
- [ ] Check image src URL generation in `renderMediaItem()`
- [ ] Verify paths are correctly encoded
- [ ] Fix standards loading in draft load flow
- [ ] Test image loading after fixes

### UX Designer (Agent-3)
- [ ] Verify all UI elements accessible
- [ ] Check error states are visible
- [ ] Ensure loading indicators work

### Tester (Agent-4)
- [ ] Re-run workflow test after fixes
- [ ] Verify 404 errors are gone
- [ ] Check standards panel loads
- [ ] Document any remaining issues

---

## 🧪 Test After Fixes

```bash
pytest tests/test_observation_report_complete_workflow.py -v -s
```

**Success Criteria**:
- ✅ No 404 errors in browser console
- ✅ Images display correctly in preview
- ✅ Standards panel shows units after loading draft
- ✅ All workflow steps complete successfully

---

**Update Status**: After each fix, update this document



