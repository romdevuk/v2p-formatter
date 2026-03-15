# Deface video conversion — speed and robustness (spec for approval)

This document analyses why video deface conversion is slow, proposes optimisations to make it faster and more robust, and specifies changes for approval. It incorporates research from the [deface GitHub repo](https://github.com/ORB-HD/deface) and observed production behaviour.

---

## 0. Observed performance (real run)

From a typical run on a **~30 second video** (e.g. `intro.mp4`):

- **Frames processed:** 706 (e.g. ~23.5 fps × 30 s).
- **Throughput:** ~2.5–3.1 frames/second (e.g. `335/706 [02:31<02:06, 2.92it/s]`).
- **Total time:** **~4 minutes** (e.g. 235+ seconds) for a 30 s clip.
- **Bottleneck:** Face detection runs on **every frame** on CPU; with “Detection Scale” = **Original**, inference is at full resolution (e.g. 1080p), which is the slowest configuration.

So a short video can take several minutes because the tool is designed to process every frame at full (or scaled) resolution with no frame skipping. The sections below explain why and what to do.

---

## 1. Current behaviour

- **Tool:** The app runs the `deface` CLI (PyPI package) as a subprocess per video. Deface uses a CenterFace ONNX model for face detection and processes **every frame** of the video: decode frame → run detection → apply blur/box/mosaic → encode frame.
- **Options passed today:** input path, `-o` output path, `--thresh`, `--scale` (if not “original”), `--replacewith`, `--boxes`, `--mosaicsize`, `--draw-scores`. Timeout 600 s per video.
- **Observation:** Conversion often takes “too much time” (e.g. **~4 min for a 30 s video** at default settings), and users want it faster and more reliable.

---

## 2. Why it’s slow — analysis

| Bottleneck | Description | Impact |
|------------|-------------|--------|
| **1. Face detection (inference)** | CenterFace runs once per frame on CPU by default. No GPU acceleration unless optional `onnxruntime-gpu` (or similar) is installed. | **High** — dominates runtime for many videos. |
| **2. Detection resolution** | If `--scale` is “original”, detection runs at full frame size (e.g. 1920×1080). More pixels ⇒ more work per frame. | **High** — smaller scale (e.g. 640×360) greatly reduces inference cost; output resolution is unchanged. |
| **3. Number of frames** | Longer videos and higher FPS ⇒ more frames ⇒ linear increase in work. | **High** — fixed by tool design (every frame). |
| **4. Video decode/encode** | FFmpeg (via imageio-ffmpeg) decodes input and encodes output. Default codec is `libx264` (software). | **Medium** — can be noticeable on long/high-res videos; hardware encoding (e.g. NVENC) would reduce encode time where available. |
| **5. Single-threaded pipeline** | One subprocess per video; no parallelism across videos except at the apply_deface route level (sequential per video). | **Medium** — acceptable for “one video at a time”; multi-video runs are already sequential. |

**Summary:** The main levers are (a) **inference speed** (GPU vs CPU, and detection scale), and (b) **detection scale** (we already pass it; default “original” is slowest). Encode is secondary but relevant for robustness and perceived speed.

### 2.1 Why a “short” video still takes minutes

- Deface processes **every frame**; it has **no built-in frame-skip** (no `--step-frames` or “every Nth frame” in the [official CLI](https://github.com/ORB-HD/deface)).
- So for a 30 s video at ~24 fps you get ~720 frames; at ~3 it/s on CPU that’s **~240 s (~4 min)**.
- **Detection scale** and **hardware acceleration** are the only practical levers without forking deface or pre-processing the video (e.g. lowering FPS before deface would change output and add complexity).

### 2.2 Options from deface GitHub / README

| Option / approach | Effect | In our app |
|-------------------|--------|------------|
| **`--scale WxH`** | Downscale input for **detection only**; output resolution unchanged. README: “640×360” for 360p detection is much faster. | Supported in UI (“Detection Scale”); default is “Original” (slowest). |
| **`onnxruntime-gpu`** | GPU inference (Nvidia). README: “significantly improve the overall processing speed.” | Not installed by default; document for users. |
| **`onnxruntime-directml`** | GPU on Windows (non-Nvidia). | Document for Windows users. |
| **`onnxruntime-openvino`** | CPU optimization. README: “accelerate inference even on CPU-only systems by a few percent.” | Optional; document. |
| **`--execution-provider` / `--ep`** | Override ONNX provider (e.g. `CUDAExecutionProvider`). Deface auto-selects fastest if not set. | Not exposed; optional future config for power users. |
| **`--ffmpeg-config`** | e.g. `{"codec": "h264_nvenc"}` for hardware encode. | Not used; optional future enhancement. |
| **Frame skipping** | Process every Nth frame. | **Not available** in upstream deface; would require upstream change or a custom pipeline. |

---

## 3. Proposed optimisations

**Quick wins (for approval):**

1. **Default “Detection Scale” to 640×360 when any video is selected** — single biggest gain with no loss of output resolution; README-recommended for performance.
2. **Document GPU install** — `pip install onnx onnxruntime-gpu` (same env as app) for Nvidia; can give a large speedup (often 5–10× or more on suitable hardware).
3. **UI hint** — Short “Performance” note on Deface page: use 640×360 for video and/or install GPU packages for faster processing.

### 3.1 Detection scale (faster, robust)

- **Current:** UI has “Detection Scale”: Original, 640×360, 1280×720. Value is passed to deface as `--scale WxH` when not “original”. Default is “Original”.
- **Proposal:**
  - **Default for video:** When the selection includes **video**, default “Detection Scale” to **640×360** (or add a separate “Video detection scale” default). Rationale: large speedup with no change to output resolution; deface docs recommend 640×360 for speed.
  - **Optional:** Add a “Fast” preset in the UI (e.g. “Fast (640×360)” selected by default when any video is selected) and keep “Original” / “1280×720” for quality when the user prefers it.
- **Robustness:** Keep passing scale through to the CLI; validate scale string (e.g. `WxH` with positive integers) before calling deface.

**Spec (for approval):**
- Add UI/UX rule: when the user has selected at least one **video**, suggest or default “Detection Scale” to **640×360** (with clear label that output resolution is unchanged).
- Document in app/spec that “Original” is slowest for video and 640×360 is the recommended speed/quality trade-off.

### 3.2 Hardware acceleration (faster)

- **Current:** Deface uses ONNX for the face model. If `onnxruntime-gpu` (or `onnxruntime-directml`, `onnxruntime-openvino`) is installed in the same environment, deface can use it; we do not install or recommend it.
- **Proposal:**
  - **Document** in project README and/or Deface section: for faster video deface, install optional deps in the **same env** as the app, e.g.  
    `pip install onnx onnxruntime-gpu` (Nvidia), or `onnxruntime-directml` (Windows), or `onnxruntime-openvino` (CPU). Restart the app after installing.
  - **Optional (future):** In the Deface UI, show a short “Performance” note: “For faster video processing, install GPU support: pip install onnx onnxruntime-gpu (same env as this app).”
  - **Optional (future):** At startup or first video run, detect whether ONNX Runtime is using a GPU and show a one-line message in the Deface page or debug log (e.g. “Using ONNX GPU” vs “Using CPU”).

**Spec (for approval):**
- Document hardware acceleration in the deface spec and README as the primary way to get faster video conversion.
- No change to deface CLI invocation by default (deface auto-selects the fastest available execution provider).
- **Implemented:** Config/env `DEFACE_EXECUTION_PROVIDER` (e.g. `CUDAExecutionProvider`) is passed to deface as `--execution-provider` when set.

### 3.3 FFmpeg / encoding (faster where supported, robust)

- **Current:** Deface uses default FFmpeg config (e.g. `libx264`). We do not pass `--ffmpeg-config`.
- **Proposal:**
  - **Optional (future):** Allow an optional “Use hardware encoding” (or “Prefer hardware encoding”) when available: pass `--ffmpeg-config '{"codec": "h264_nvenc"}'` (or equivalent) only when we know the environment supports it (e.g. config flag or auto-detect). This reduces encode time; decoding is still done by the tool.
  - **Robustness:** Do not change default encoding unless we add a clear option and fallback (e.g. fall back to libx264 if nvenc fails). For approval we only **spec** this as an optional enhancement; implementation can follow later.

**Spec (approved / implemented):**
- Env `DEFACE_FFMPEG_CODEC`: default `libx264`; set to `h264_nvenc` for Nvidia GPU encoding. App passes `--ffmpeg-config` to deface and falls back to software encoding (no override) if hardware encode fails.

### 3.4 Robustness (timeouts, errors, validation)

- **Current:** 600 s timeout per video; errors from deface are surfaced; no pre-check of video file or deface capability.
- **Proposal:**
  - **Keep** 600 s timeout; consider making it configurable (e.g. env or config) for very long videos.
  - **Preflight (optional):** Before starting deface on a video, optionally run a quick validation (e.g. that the file exists, is readable, and has a valid container/format) so we fail fast with a clear message instead of failing late in the pipeline.
  - **Clear errors:** Map common deface/FFmpeg errors to user-facing messages (e.g. “Video may be corrupt or in an unsupported format”; “Processing timed out; try a shorter video or lower Detection Scale”).
  - **Retries (optional):** For transient failures (e.g. “Resource temporarily unavailable”), consider one automatic retry before surfacing error.

**Spec (for approval):**
- Document timeout (600 s) and option to make it configurable.
- Add to spec: optional preflight validation and clearer error messages for deface video failures.
- Optional: one retry on transient-like errors.

### 3.5 Frame skipping (not in upstream)

- **Upstream deface** (ORB-HD/deface) has **no option** to process every Nth frame (no `--step-frames` or equivalent). Every frame is decoded, detected, anonymized, and encoded.
- **Implication:** We cannot reduce work by “processing every 5th frame” without either (a) requesting or contributing such a feature upstream, or (b) building a custom pipeline (e.g. extract every Nth frame → deface → recombine), which would affect output quality/sync and complexity.
- **Spec (for approval):** Rely on **detection scale** and **hardware acceleration** as the approved levers. Frame skipping is out of scope unless upstream adds support or we explicitly scope a custom solution later.

---

## 4. Implementation plan (for approval)

| Priority | Item | Change |
|----------|------|--------|
| **P0** | Default scale for video | When selection includes video, default “Detection Scale” to 640×360 (or show a “Fast (recommended for video)” option and select it by default when videos are selected). |
| **P0** | Docs | Add “Video deface: speed and robustness” section to deface spec: recommend 640×360 for speed; document optional `onnx onnxruntime-gpu` (and others) for hardware acceleration; note timeout and optional preflight/errors. |
| **P1** | README / Deface UI hint | In README and/or Deface page, add one short sentence: for faster video deface, install `onnx onnxruntime-gpu` (or appropriate package) in the same env and restart. |
| **P2** | Robustness | Optional preflight check for video file; clearer error messages for timeout and common deface/FFmpeg errors; optional single retry. |
| **P2** | Encoding | **Implemented:** Set `DEFACE_FFMPEG_CODEC=h264_nvenc` for Nvidia GPU encoding; fallback to libx264 on failure. |
| **P2** | Parallel videos | **Implemented:** Set `DEFACE_MAX_CONCURRENT_VIDEOS=2` (or 3–4) in config/env to run that many deface subprocesses at once. Default 1 (sequential). |
| **P2** | Execution-provider override | **Implemented:** Set `DEFACE_EXECUTION_PROVIDER` (e.g. `CUDAExecutionProvider`) in config/env to pass `--execution-provider` to deface. |

---

## 5. Approval checklist

- [x] **Observed performance:** Spec documents real-world numbers (~30 s video → 706 frames → ~4 min at default settings) and root cause (every-frame CPU inference, scale=original).
- [x] **Default or suggested scale for video:** When the user has selected at least one video, default or strongly suggest “Detection Scale” 640×360 (with note that output resolution is unchanged).
- [x] **Documentation:** Deface spec (and optionally README) updated with: why video is slow, recommendation to use 640×360 for speed, and optional GPU/ONNX packages for hardware acceleration.
- [x] **UI/UX:** No mandatory change to existing “Detection Scale” options; only default/suggestion when videos are selected (and optional “Performance” hint for GPU install).
- [x] **GitHub / upstream:** Spec reflects that (a) deface has no frame-skip option; (b) main levers are `--scale` and hardware acceleration per official README; (c) optional `--execution-provider` and `--ffmpeg-config` are documented and implemented.
- [x] **Robustness:** Preflight (valid video check via get_video_info) and one retry on transient errors implemented in deface_processor; timeout and errors documented; configurable timeout via DEFACE_VIDEO_TIMEOUT.
- [x] **Encoding:** Optional hardware encoding via `DEFACE_FFMPEG_CODEC` (e.g. `h264_nvenc`) with fallback to libx264 on failure.

---

## 6. References

- Deface PyPI: https://pypi.org/project/deface/
- Deface GitHub: https://github.com/ORB-HD/deface
- Deface README (usage, `--scale`, hardware acceleration, `--ffmpeg-config`, `--execution-provider`): https://github.com/ORB-HD/deface (see README: “High-resolution media and performance”, “Hardware acceleration”, and `deface -h` for full CLI).
- ONNX Runtime execution providers: https://onnxruntime.ai/docs/execution-providers/
- Current app: `app/deface_processor.py` (`deface_video`), `app/routes.py` (`apply_deface`), Deface UI (Detection Scale dropdown in `templates/deface.html`).
