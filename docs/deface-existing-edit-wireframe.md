# Deface — existing output available for ongoing edit (wireframe for approval)

When the user opens the Deface page with a qualification and learner, any **already-saved** defaced files are shown so they can continue editing or proceed to document generation without re-running Apply Deface. **When the user returns to the same page** (e.g. `http://localhost/v2p-formatter/deface?qualification=Deco&learner=arjom`), the converted files **must stay there** so they can edit or proceed again. See also [deface-spec.md](./deface-spec.md) and [deface-output-how-it-works.md](./deface-output-how-it-works.md).

---

## 1. Entry and return to page

- User opens e.g. `http://localhost/v2p-formatter/deface?qualification=Deco&learner=arjom`.
- Page loads with qualification and learner pre-selected; section 1 (Select Images and Videos) loads the file list as usual.
- **Return to page:** If the user navigates away and later returns to the same URL, the app loads existing defaced files for that qualification+learner and shows them in section 3 so the user can **edit or proceed again**. Converted files persist in `OUTPUT_FOLDER/<qualification>/<learner>/deface/` and are always shown when present.

---

## 2. Load existing defaced

- Frontend calls **GET** `/deface_existing?qualification=Deco&learner=arjom`.
- Backend scans `OUTPUT_FOLDER/Deco/arjom/deface/` and returns:
  ```json
  { "items": [
    { "original_name": "intro.mp4", "defaced_url": "/v2p-formatter/deface_output/Deco/arjom/deface_intro.mp4", "type": "video", "sequence": 1, "from_existing": true }
  ]}
  ```
- If `items.length > 0`:
  - Set `appData.defacedItems = items` (no session ID).
  - Show **section 3 (Apply Deface & Review)** and the review grid.
  - Scroll to section 3 so the user sees “Defaced files available to edit”.
  - Enable **Generate Documents** so the user can go straight to document generation if they don’t need to edit.

---

## 3. Wireframe — review grid with existing items

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. Apply Deface & Review                                                │
│ Applies to all selected images and videos from section 1.               │
│                                                                         │
│ [Apply Deface]                                                          │
│                                                                         │
│ ✅ Deface Applied Successfully (or: Defaced files available to edit)   │
│ Review anonymized media files below:                                   │
│                                                                         │
│ ┌──────────────────┐ ┌──────────────────┐                             │
│ │ [video preview]   │ │ [image preview]   │                             │
│ │ deface_intro.mp4 │ │ deface_photo.jpg  │                             │
│ │ ✓ Defaced (saved)│ │ ✓ Defaced (saved) │                             │
│ │ [Edit]           │ │ [Edit]           │                             │
│ └──────────────────┘ └──────────────────┘                             │
│                                                                         │
│ [Adjust Settings & Re-apply]  [Accept & Proceed to Document Generation] │
└─────────────────────────────────────────────────────────────────────────┘
```

- Items loaded from **existing** output show label **"✓ Defaced (saved)"**.
- [Edit] opens the Manual Deface Editor; backend must support editing from persisted path when there is no session (future enhancement if needed).

---

## 4. Serving existing files

- **URL pattern:** `/v2p-formatter/deface_output/<qualification>/<learner>/<filename>`
- **Source:** `OUTPUT_FOLDER/<qualification>/<learner>/deface/<filename>`
- **Video:** Range requests supported (206) so video plays and seeks without `ERR_CONTENT_LENGTH_MISMATCH`.
- **Security:** Resolve path and ensure file is under the deface dir for that qual/learner.

---

## 5. Approval checklist

- [x] Page with `?qualification=…&learner=…` loads existing defaced list.
- [x] **Return to page:** Converted files stay visible so user can edit or proceed again.
- [x] Review grid shows with existing items; each has [Edit].
- [x] Media served from `/deface_output/…` with Range support for video.
- [x] Generate Documents works from existing deface folder (no session) when qualification+learner are sent.
- [x] Spec and wireframe match implementation.
