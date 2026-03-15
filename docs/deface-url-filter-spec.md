# Deface page – URL filter (qualification, learner, files) and status block

**Version:** 1.0  
**Date:** 2026-03-14  
**Status:** Approved / Implemented  
**Purpose:** Spec for implementing URL-driven pre-selection and a visible status block so agents can develop the feature. When the Deface page is opened with a “create deface” link from the observation-report app (with `qualification`, `learner`, and `files`), the app must pre-select qual/learner and the requested files, and show what was executed, which files were selected, and which are missing.

---

## 1. Scope

| Area | In scope |
|------|----------|
| Deface page URL params | `qualification`, `learner`, `files` (comma-separated basenames) |
| Pre-selection behaviour | Set qualification and learner from URL; after file list loads, pre-select only the files listed in `files` |
| Status block | Visible block showing: what was executed, files selected, files missing |
| Matching rules | Case-insensitive basename match (and path fallback) so e.g. `IMG_0607.JPG` matches `IMG_0607.jpg` |

---

## 2. URL format

The observation-report app opens the Deface page with URLs of the form:

```
http://localhost/v2p-formatter/deface?qualification={qual}&learner={learner}&files={basename1}%2C{basename2}%2C...
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `qualification` | Yes | Qualification folder name (e.g. `Deco`). Pre-select in the Qualification dropdown. |
| `learner` | Yes | Learner folder name (e.g. `arjom`). Pre-select in the Learner dropdown. |
| `files` | No | Comma-separated list of **file basenames**. Commas are URL-encoded as `%2C`. Filenames may be encoded (e.g. spaces as `%20`). Examples: `IMG_0607.JPG`, `WhatsApp%20Image%202026-01-24%20at%2020.20.49.jpeg`, `orbital-sander.mp4`. |

**Example:**

```
http://localhost/v2p-formatter/deface?qualification=Deco&learner=arjom&files=IMG_0607.JPG%2CIMG_0638.JPG%2CWhatsApp%20Image%202026-01-24%20at%2020.20.49.jpeg%2CIMG_0610.JPG%2Corbital-sander.mp4%2Cmixing-2.mp4%2Cmasking-tape.mp4%2Ccaulking.mp4%2Cfilling-wall.mp4%2Cfilling.mp4%2CIMG_0618.JPG%2CIMG_0619.JPG%2CIMG_0623.JPG%2CIMG_0611.JPG%2CIMG_0613.JPG
```

---

## 3. Behaviour (what must be executed)

1. **On page load**
   - Read `qualification` and `learner` from the URL and set the Qualification and Learner dropdowns.
   - If `qualification` is set, load learners for that qualification and set `learner` when the list is ready.
   - When both qual and learner are set, load the file list (images and videos) for that qualification/learner (existing `list_images` or equivalent).

2. **When the file list has loaded and `files` is present in the URL**
   - Parse `files`: split on comma, decode each token with `decodeURIComponent`, trim, drop empty. This yields the **requested basenames** (in order).
   - For each requested basename, find the corresponding file in the loaded images or videos using **case-insensitive basename matching** (see §5). Preserve the order of the URL list when building the selected set.
   - Set the Deface app’s selection state to exactly these matched files (clear previous selection first).
   - Update the selection UI (count, “Select All” state, sequence numbers).
   - Compute **selected** (found and selected) and **missing** (requested but not found).
   - Show the **URL filter status block** (§4) with: what was executed, files selected, files missing.

3. **When `files` is not present**
   - Do not show the URL filter status block. Behaviour remains “select qual/learner only”; user selects files manually.

---

## 4. URL filter status block (required UI)

When the page was opened with a URL that includes the `files` parameter, the Deface app must display a **visible status block** so the user (and support) can see what the URL filter did.

### 4.1 When to show the block

- Show the block **only when** the `files` query parameter was present on page load and the file list for the chosen qualification/learner has been loaded (successfully or empty).
- Hide or do not render the block when there is no `files` param.

### 4.2 Placement

- Place the block **below** the Qualification/Learner selection row and **above** the “Select Images and Videos” section (e.g. above “1. Select Images and Videos” or above the bulk selection controls).
- The block should be clearly associated with “URL filter” / “Pre-selection from link” so it is not confused with general selection state.

### 4.3 Content (three parts)

The block must show:

1. **What was executed**
   - Short line stating that the URL filter was applied.
   - Include: qualification and learner from the URL, and the number of files requested from the URL.
   - Example: *“URL filter applied: qualification=Deco, learner=arjom, 18 files requested.”*

2. **Files selected**
   - Label: e.g. *“Files selected (n):”*
   - List the **basenames** of the files that were found and pre-selected (in selection order), or a short list plus “and X more” if the list is long.
   - If none were found, state *“No files from the URL were found in the file list.”*

3. **Missing**
   - Label: e.g. *“Missing (not found in folder):”*
   - List the **requested basenames** that had no match in the loaded file list.
   - If none are missing, state *“None.”* or *“All requested files were found.”*

### 4.4 Styling and behaviour

- Use a distinct container (e.g. bordered box, subtle background) so the block is easy to spot.
- Use a clear heading, e.g. *“Pre-selection from link”* or *“URL filter result”*.
- Missing files can be shown in a warning style (e.g. amber/orange) to draw attention.
- Optional: allow collapsing the block (e.g. “Show details” / “Hide details”) to save space; when collapsed, at least show a one-line summary (e.g. “18 requested, 15 selected, 3 missing”).

---

## 5. Matching rules (for implementation)

- **Requested basenames:** From the URL `files` param after splitting on comma and decoding each token. Preserve the exact string for display (e.g. `IMG_0607.JPG`).
- **Match:** A file in the loaded list (image or video) matches a requested basename if:
  - The file’s `name` (as returned by the API) equals the requested basename **ignoring case**, or
  - The file’s `path` ends with the requested basename (with `/` or `\` before it), **ignoring case**.
- **First match wins:** If the same file could match more than one requested basename (e.g. duplicate entries in the URL), match each requested basename at most once (first matching file in the list).
- **Order:** The selected set must follow the **order of the URL list** (requested basenames order), not the order of files in the loaded list.

---

## 6. Example (for approval)

**URL:**  
`http://localhost/v2p-formatter/deface?qualification=Deco&learner=arjom&files=IMG_0607.JPG%2CIMG_0638.JPG%2CWhatsApp%20Image%202026-01-24%20at%2020.20.49.jpeg%2Corbital-sander.mp4`

**Assume:** In the folder only `IMG_0607.JPG`, `IMG_0638.JPG`, and `orbital-sander.mp4` exist; the WhatsApp image is not present.

**Expected status block:**

- **What was executed:** URL filter applied: qualification=Deco, learner=arjom, 4 files requested.
- **Files selected (3):** IMG_0607.JPG, IMG_0638.JPG, orbital-sander.mp4.
- **Missing (not found in folder):** WhatsApp Image 2026-01-24 at 20.20.49.jpeg.

The grid/list must show exactly these three files as selected, in that order, with the selection count and sequence numbers updated.

---

## 7. Implementation checklist (for agent)

- [x] Read `qualification` and `learner` from URL on load; set dropdowns and load file list (existing behaviour).
- [x] When file list has loaded, if URL has `files`: parse `files` (split on `,`, decode each token, trim).
- [x] Match requested basenames to loaded files using **case-insensitive** basename (and path) matching.
- [x] Build selected set in **URL order**; set app selection state and update selection UI.
- [x] Compute lists: **selected** (matched) and **missing** (requested but no match).
- [x] Add a **URL filter status block** (below qual/learner, above file selection) visible only when `files` was present.
- [x] Block shows: (1) what was executed, (2) files selected, (3) missing.
- [x] Optional: collapse/expand for long lists; one-line summary when collapsed.

---

## 8. Success criteria

- Opening a URL with `qualification`, `learner`, and `files` pre-selects that qualification and learner and pre-selects only the requested files that exist, in URL order.
- Matching is case-insensitive so e.g. `IMG_0607.JPG` matches a file named `IMG_0607.jpg` on disk.
- The URL filter status block is visible when `files` was in the URL and shows what was executed, files selected, and missing.
- When no `files` param is present, the block is not shown and behaviour is unchanged (qual/learner only).

---

## 9. Debugging (for analysis)

When the Deface page is opened with a `files` query parameter, the app records a **trace** you can inspect to analyse URL filter behaviour.

### 9.1 Where to look

- **Debug panel (on page):** The Deface page has a debug panel below the Qualification/Learner row. Lines prefixed with `[URL filter]` or logged as "URL filter &lt;step&gt;" show the same steps. The panel also shows a hint: `window.appData.urlFilterDebugTrace`.
- **Browser console:** Open DevTools → Console. Every URL-filter step is logged with the prefix `[URL filter]`. You can filter by that string.

### 9.2 Trace array: `window.appData.urlFilterDebugTrace`

In the console, run:

```js
window.appData.urlFilterDebugTrace
```

This is an array of entries. Each entry has:

- **`step`** (string): Step name (see below).
- **`time`** (string): ISO timestamp when the step ran.
- **`data`** (object or value): Step-specific payload.

**Steps and payloads:**

| Step | When | `data` contents |
|------|------|------------------|
| `init` | Before fetching file list (when `files` is in URL). | `qualification`, `learner`, `filesParamLength`, `filesParamPreview` (first 120 chars of raw `files` param). |
| `parsed_requested` | After parsing the `files` param. | `count`, `names` (full array of requested basenames). |
| `api_files` | After receiving the file list from the API. | `images`, `videos` (counts), `nameSample` (first 10 file names from API, for casing check). |
| `result` | After matching. | `requested`, `selected`, `missing` (counts), `selectedNames`, `missingNames` (arrays). |
| `match_details` | After matching. | Array of `{ requested, matched }` (or `matched: null` if missing). Use this to see exactly which URL basename matched which API name, or which requested name had no match. |
| `result_no_files` | When the API returned no files but `files` was in the URL. | `requested`, `selected: 0`, `missing`, `reason` (`empty_list` or `api_error`). |
| `fetch_error` | When the file-list fetch failed. | `{ error: message }`. |

### 9.3 Quick analysis

- **Why is nothing selected?** Check `result` or `result_no_files`: look at `selected` and `missingNames`. Then check `match_details`: if every entry has `matched: null`, the API file names may differ (e.g. casing, or path vs basename). Compare `parsed_requested.names` with `api_files.nameSample`.
- **Why are some files missing?** In `match_details`, find entries with `matched: null`; the `requested` value is the basename that had no match. Compare with `api_files.nameSample` (and the full list from the API if needed).

---

**Document version:** 1.0  
**Date:** 2026-03-14  
**Status:** Approved / Implemented
