# How and Where Deface Files Are Saved

This document explains how the Deface module works and where it saves output files. Use it when building a new app that needs to understand or integrate with deface output.

---

## 1. Configuration: Base Output Folder

- **Config file:** `config.py`
- **Variable:** `OUTPUT_FOLDER`
- **Default (example):** `Path('/Users/rom/Documents/nvq/v2p-formatter-output')`

All deface output is written under this folder. The app also **reads** source images and videos from the same hierarchy (qualification/learner subfolders).

```python
# config.py
OUTPUT_FOLDER = Path('/Users/rom/Documents/nvq/v2p-formatter-output')
```

---

## 2. Where Output Files Are Written

Output path is chosen in this order:

### 2.1 When qualification and learner are provided (normal case)

- **Path pattern:** All deface files are written inside a **`deface`** subfolder: `{OUTPUT_FOLDER}/{qualification}/{learner}/deface/`
- **Example:** `OUTPUT_FOLDER/Deco/arjom/deface/`
- **Code:** `app/routes.py` → `generate_deface_documents()`:
  - `qualification = data.get('qualification', '')`
  - `learner = data.get('learner', '')`
  - If both set: `output_dir = OUTPUT_FOLDER / qualification / learner`, then `deface_dir = output_dir / 'deface'`
  - Both directories are created if missing: `output_dir.mkdir(...)`, `deface_dir.mkdir(parents=True, exist_ok=True)`
  - All deface output (standalone images, videos, PDF, DOCX) is written to `deface_dir`.

### 2.2 Fallback when qualification/learner are missing

- **Path:** `{first_processed_file_parent}/deface/` if the first file’s parent exists, else `{OUTPUT_FOLDER}/deface/`.
- The app always creates and uses a **`deface`** subfolder for writing; it never writes deface files directly into the learner (or fallback) folder.

So in practice, deface output goes to **`OUTPUT_FOLDER/<qualification>/<learner>/deface/`** when the UI sends qualification and learner (e.g. from the Deface page dropdowns).

---

## 3. What Gets Saved (File Types and Names)

For every “Generate Documents” run, the app can write:

### 3.1 Standalone defaced images (always when there are images/frames)

- **What:** Each defaced image (or video frame image) as a separate file.
- **Naming:** `deface_{name}{suffix}` (e.g. `deface_IMG_0607.JPG`, `deface_intro_frame_0_00.jpg`).
- **Uniqueness:** If a file with that name already exists, the app appends `_1`, `_2`, … before the extension.
- **Location:** Inside the **`deface`** subfolder (e.g. `output_dir/deface/`).
- **Code:** `app/routes.py` → `generate_deface_documents()` → block “Always export standalone defaced images”:
  - Iterates `defaced_images` and `image_names`.
  - For each: `dest = deface_dir / out_name` with `out_name = f"deface_{name}{suffix}"`, then `shutil.copy2(src, dest)`.

### 3.2 Standalone defaced videos (always when there are videos)

- **What:** Each defaced video as a single MP4 file.
- **Naming:** `deface_{original_name}` (e.g. `deface_intro.mp4`). If the original name already starts with `deface_`, it is kept as-is.
- **Location:** Inside the **`deface`** subfolder.
- **Code:** Same function → “Always export standalone defaced videos”:
  - For each video in `processed_items` with `type == 'video'`:
  - `output_video_path = deface_dir / output_name` with `output_name = f'deface_{original_name}'` (or original name if already prefixed), then `shutil.copy2(defaced_video_path, output_video_path)`.

### 3.3 Merged documents (only when requested via output format)

- **PDF:** Only if output format is `pdf`, `both`, or `mp4+pdf`.
  - **Path:** `deface_dir / f"deface_{filename}.pdf"` (i.e. inside the `deface` subfolder)
  - **Example:** `OUTPUT_FOLDER/Deco/arjom/deface/deface_report.pdf`
- **DOCX:** Only if output format is `docx` or `both`.
  - **Path:** `deface_dir / f"deface_{filename}.docx"`
  - **Example:** `OUTPUT_FOLDER/Deco/arjom/deface/deface_report.docx`

The **filename** (without extension) is the value from the “Output Filename” field in the UI; the app adds the `deface_` prefix and the extension.

---

## 4. Output Format Options (what gets written)

| Format (value)   | Standalone images | Standalone videos | PDF | DOCX |
|------------------|-------------------|--------------------|-----|------|
| `media`          | Yes               | Yes                | No  | No   |
| `pdf`            | Yes               | Yes                | Yes | No   |
| `both`           | Yes               | Yes                | Yes | Yes  |
| `docx`           | Yes               | Yes                | No  | Yes  |
| `mp4`            | No*               | Yes                | No  | No   |
| `mp4+pdf`        | Yes               | Yes                | Yes | No   |

\*For `mp4`, the code path does not build the “defaced images” list used for standalone image export; only videos are exported.

So:

- **“Media only”** (`media`): only standalone defaced image files + defaced video files in the `deface` subfolder; no PDF/DOCX.
- **Where deface files are saved:** always in the **`deface`** subfolder, e.g. `OUTPUT_FOLDER/<qualification>/<learner>/deface/` (or fallback `…/deface/`).

---

## 5. API Response: Paths Your App Can Use

After calling `POST /v2p-formatter/generate_deface_documents`, the JSON response includes:

- **`output_folder_path`:** Absolute path to the **`deface`** subfolder where all deface files were written (e.g. `OUTPUT_FOLDER/Deco/arjom/deface`).
- **`exported_standalone_images`:** List of `{ path, relative_path, name }` for each saved image.
- **`exported_videos`:** List of `{ path, relative_path, name, url }` for each saved video.
- **`pdf_path` / `docx_path`:** Present only if that document was generated.

So a new app can:

1. Use `output_folder_path` as the single “root” where deface output for that run lives.
2. Use `exported_standalone_images` and `exported_videos` to get exact file paths and names without scanning the directory.

---

## 6. Quick Reference: Paths and Code Locations

| What | Where it’s defined / used |
|------|---------------------------|
| Base output root | `config.py` → `OUTPUT_FOLDER` |
| Learner output dir | `app/routes.py` → `generate_deface_documents()` → `output_dir = OUTPUT_FOLDER / qualification / learner` (or fallback) |
| Deface subfolder | Same function → `deface_dir = output_dir / 'deface'`, `deface_dir.mkdir(...)` — all deface files go here |
| Standalone image export | Same function → “Always export standalone defaced images” → `dest = deface_dir / out_name` |
| Standalone video export | Same function → “Always export standalone defaced videos” → `output_video_path = deface_dir / output_name` |
| PDF path | `deface_dir / f"deface_{filename}.pdf"` |
| DOCX path | `deface_dir / f"deface_{filename}.docx"` |
| API `output_folder_path` | `str(deface_dir)` (the deface subfolder) |
| Default format (UI) | `templates/deface.html` → `<select id="outputFormat">` → option `value="media"` with `selected` |

---

## 7. Summary for a New App

- **Where:** Deface files are saved under **`OUTPUT_FOLDER`**, in the subfolder **`<qualification>/<learner>/deface/`** when both are provided (e.g. from the Deface UI). The app creates the `deface` subfolder and writes all deface output there.
- **What:** Standalone defaced images (one file per image/frame) and defaced videos (one MP4 per video) are always written when available; PDF/DOCX are optional and only for certain output formats.
- **How to know exactly what was saved:** Use the `generate_deface_documents` response: `output_folder_path`, `exported_standalone_images`, and `exported_videos`.
