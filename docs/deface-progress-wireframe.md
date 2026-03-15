# Deface progress UI — wireframe (for approval)

This wireframe defines the **Apply Deface** progress display so the overall bar and status line show clear, staged progression (no "stuck" appearance). For **bulk** selection it defines a **queue** and **queue list** so progression is explicit in both the main page and the detailed page. See also **Progress display (staged progression)** and **Bulk processing queue** in [deface-spec.md](./deface-spec.md).

---

## 1. Queue model (bulk — for approval)

When multiple files are selected, processing is a **queue** in **selection order** (images first, then videos). Each item has a **state**:

| State         | Display (main and detailed page)     | Example |
|---------------|--------------------------------------|---------|
| **Pending**   | Grey text or "waiting"               | `3. mixing-2.mp4 — waiting` |
| **In progress** | Spinner + name + elapsed + %      | `4. orbital-sander.mp4 — 45s — 23%` |
| **Done**      | Checkmark + name                     | `1. IMG_0607.JPG — ✓ done` |

- **Queue list:** Ordered list of all items (1..N) with the state above. Optional on the main Deface page; **required** on the detailed page so the detailed page is a full mirror of progression.
- **Progress API:** Backend SHALL expose an ordered list (e.g. `queue: [{ name, state }]` or `item_names: [...]`) so both UIs can render the same queue. Status line and bar use `completed`, `current_item`, `current_item_pct`, `elapsed_seconds` as today.

---

## 2. Section: "3. Apply Deface & Review" (main page)

During processing, the following block is visible. For **bulk**, an optional queue list (see §1) can be shown under the status line.

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Processing Deface...                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│ [████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 42%       │  ← Overall bar (queue position + per-item % from CLI)
├─────────────────────────────────────────────────────────────────────────┤
│ Processing 3/8 — orbital-sander.mp4 (45s) — 23%                        │  ← Status line (see §3): queue position, current file, elapsed, %
├─────────────────────────────────────────────────────────────────────────┤
│ Estimate: images take a few seconds; each video often 1–2 minutes.     │
├─────────────────────────────────────────────────────────────────────────┤
│ Queue (optional on main page):                                          │
│   1. IMG_0607.JPG        — ✓ done    2. IMG_0638.JPG — ✓ done           │
│   3. mixing-2.mp4        — ✓ done    4. orbital-sander.mp4 — ⟳ 45s 23% │
│   5. masking-tape.mp4    — waiting   6. caulking.mp4 — waiting  ...     │
├─────────────────────────────────────────────────────────────────────────┤
│ ▼ Show detailed steps (live log)                                        │
│   [23:08:55.123] [deface_video] 5_run | 23% 161/706 [00:55<04:11, ...]  │
│   [23:08:55.456] [deface_video] 5_run | still processing orbital...     │
│   ...                                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│ Open video debug log (new tab) — full log + same queue progression.     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Status line — staged progression (for approval)

The single status line under the bar must update in a clear order so the user sees that work is progressing:

| Stage        | What is shown | Example |
|-------------|----------------|---------|
| **Elapsed** | Seconds (5s, 10s, 15s …) for current item | `Processing 0/1 — intro.mp4 (5s)` then `(10s)`, `(15s)` … |
| **%**       | When deface CLI reports progress, append percentage | `Processing 0/1 — intro.mp4 (45s) — 23%` |
| **Per-file (bulk / queue)** | When multiple files: queue position and filename | `Processing 3/8 — orbital-sander.mp4 (45s) — 23%` |

Rules:
- Always show elapsed seconds for the current item when available (5s, 10s, …).
- When the backend parses percentage (or frame count) from deface stderr, show it (e.g. ` — 23%`).
- For bulk (queue), show `Processing <current>/<total> — filename` (e.g. `Processing 3/8 — orbital-sander.mp4 (45s) — 23%`).

---

## 4. Overall progress bar (for approval)

- The **bar must move** during processing (no "stuck" appearance).
- **Formula:**  
  `overall_pct = (completed_items / total_items) * 100 + (current_item_pct / 100) * (1 / total_items) * 100`
- **Examples:**
  - 1 video, 0% from CLI → 0%; 23% from CLI → 23%; 100% → complete.
  - 3 items, 1 done, current at 50% → 33.33 + 16.67 ≈ 50%.
- The backend derives `current_item_pct` from deface CLI stderr (e.g. `23%` or `161/706`). The UI polls progress and updates the bar every 1.5s.

---

## 5. Detailed steps (live log)

- Expandable section ("Show detailed steps (live log)").
- Content: timestamped lines from the server (heartbeat messages + deface stderr).
- Updates every 1.5s while processing so the user sees continuous activity.
- Link to "Open video debug log (new tab)" for full log and **same queue progression** on the detailed page.

---

## 6. Detailed page: "Open video debug log (new tab)" (for approval)

The page opened via **Open video debug log (new tab)** SHALL show the **same** queue and progression as the main page, **per-file progress**, **URL to each completed file**, and the full live log. Layout:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Video deface debug log (live)                                           │
│ Open this page in a new tab when you click Apply Deface. Refreshes 1.5s. │
├─────────────────────────────────────────────────────────────────────────┤
│ [████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 42%       │  ← Same overall bar as main page
├─────────────────────────────────────────────────────────────────────────┤
│ Processing 4/8 — orbital-sander.mp4 (45s) — 23%                         │  ← Status line: current file, elapsed, %
├─────────────────────────────────────────────────────────────────────────┤
│ Queue — files and their progress (required):                             │
│   1. IMG_0607.JPG        — ✓ done  [View defaced]  ← link to defaced   │
│   2. IMG_0638.JPG        — ✓ done  [View defaced]  ← link to defaced   │
│   3. mixing-2.mp4        — ✓ done  [View defaced]  ← link to defaced   │
│   4. orbital-sander.mp4 — ⟳ 45s — 23%  (in progress)                   │
│   5. masking-tape.mp4    — waiting                                       │
│   6. caulking.mp4       — waiting   ...                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ Live log:                                                                │
│   [23:08:55.123] [deface_video] 5_run | 23% 161/706 [00:55<04:11, ...]  │
│   [23:08:55.456] [deface_video] 5_run | still processing orbital...     │
│   ...                                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│ Last update: 23:09:01                                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

- **Required on this page:**
  - **Overall progress bar** (same formula as main page).
  - **Status line** (current queue position, current file name, elapsed, %).
  - **Queue list:** One row per file in order. For each file show:
    - **Done:** ✓ and a **link (URL)** to the defaced file so the user can open/view it as soon as it’s ready. URL is the defaced preview (e.g. `/v2p-formatter/deface_temp/<session_id>/...`).
    - **In progress:** File name and **per-file progress** (elapsed time and % from deface CLI).
    - **Pending:** File name and “waiting”.
  - **Live log** (timestamped lines, updating every 1.5–2 s).
- Backend exposes `queue: [{ name, state, url? }]`; `url` is set for each item when state is `done` (defaced file URL for that item).

---

## 7. Debugging (for approval)

To verify progress accuracy and troubleshoot, the **detailed page** SHALL provide an optional **Debug** section:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ▼ Show debug (raw progress API)                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ (when expanded:)                                                         │
│ Last poll: 23:09:01  |  Poll interval: 1.5s                              │
│ Raw progress (GET /deface_video_log):                                    │
│ {                                                                        │
│   "total": 8, "completed": 4, "status": "processing",                    │
│   "current_item": "orbital-sander.mp4", "current_item_pct": 23,          │
│   "elapsed_seconds": 45, "phase": "videos", "item_names": [...],         │
│   "queue": [ { "name": "IMG_0607.JPG", "state": "done", "url": "/v2p..." }|, ... ]
│ }                                                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

- **Toggle:** "▼ Show debug (raw progress API)" / "▲ Hide debug" so the detailed page can show the last poll’s **progress** object as JSON.
- **Contents:** Last successful poll timestamp, poll interval (1.5s), and full `progress` object from the API (formatted). This allows checking that `completed`, `queue`, `url`s, and per-item state match expectations.
- **Placement:** Below the live log on the detailed page (optional, collapsed by default).

---

## 8. Approval checklist (implemented / for approval)

- [x] Overall bar moves during processing (no stuck appearance).
- [x] Status line shows elapsed (5s, 10s, …) then % when available, then per-file (queue position) for bulk.
- [x] Detailed steps section updates live on main page.
- [x] **Queue:** Bulk processing is a queue; progression is queue-based (position + per-item %).
- [x] **Queue list:** Shown on main page (optional) and on detailed page (required).
- [x] **Detailed page:** Shows same bar, status line, queue list (with per-file progress and URL when done), and live log.
- [x] **Per-file progress:** Queue rows show elapsed and % for item in progress; done rows show link to defaced file.
- [x] **Debugging:** Detailed page has optional "Show debug (raw progress API)" with last poll time and full progress JSON.
- [x] Spec (deface-spec.md) and this wireframe match.

**Implementation:** Backend parses deface stderr for `\d+%` or `\d+/\d+`, exposes `current_item_pct` and `queue: [{ name, state, url? }]` in `/deface_video_log` progress. As each item completes, backend appends its defaced URL to progress so `queue[i].url` is set for done items. UI polls every 1.5s, shows status line with elapsed + %, and renders queue with links (url) for done items and elapsed/% for the item in progress.
