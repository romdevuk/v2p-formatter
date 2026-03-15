"""
Deface processor for face anonymization in images and videos
Uses the deface command-line tool to anonymize faces in images and videos
Also supports manual deface areas for precise control
"""
import json
import re
import subprocess
import logging
import sys
import threading
import time
from pathlib import Path
from typing import Optional, Tuple, List, Dict
import tempfile
import shutil

logger = logging.getLogger(__name__)


def _get_deface_video_timeout() -> int:
    """Per-video timeout in seconds (from config or env)."""
    try:
        from config import DEFACE_VIDEO_TIMEOUT
        return max(60, int(DEFACE_VIDEO_TIMEOUT))
    except Exception:
        return 600


def _user_facing_deface_error(stderr: str) -> str:
    """Map deface/FFmpeg stderr to a short user-facing message where possible."""
    s = (stderr or '').lower()
    if 'invalid data' in s or 'invalid argument' in s or 'could not find codec' in s:
        return 'Video may be corrupt or in an unsupported format. Try re-exporting the video or use a different file.'
    if 'no such file' in s or 'no route to host' in s:
        return 'File not found or inaccessible. Check that the file exists and is readable.'
    if 'timeout' in s or 'timed out' in s:
        return 'Processing timed out. Try a shorter video or use Detection Scale 640×360 for faster processing.'
    if 'resource temporarily unavailable' in s or 'errno' in s or 'memory' in s:
        return 'System resource limit reached. Try again or use a smaller video / lower Detection Scale.'
    if 'ffmpeg' in s and ('error' in s or 'failed' in s):
        return 'Video encoding failed. The video may be in an unsupported format or corrupt.'
    return (stderr or 'Unknown error')[:500]


def _is_retryable_error(error_message: str) -> bool:
    """True if the error suggests a transient failure worth one retry."""
    if not error_message:
        return False
    s = error_message.lower()
    if 'timeout' in s or 'timed out' in s:
        return True
    if 'resource temporarily unavailable' in s:
        return True
    if 'errno' in s and ('11' in s or 'eagain' in s or 'eintr' in s):
        return True
    return False


def _is_codec_encode_error(stderr: str) -> bool:
    """True if the error suggests hardware codec/encoding failure (e.g. nvenc not available)."""
    if not stderr:
        return False
    s = stderr.lower()
    if 'could not find codec' in s or 'codec' in s and ('not found' in s or 'not supported' in s or 'unavailable' in s):
        return True
    if 'nvenc' in s and ('error' in s or 'failed' in s or 'not' in s):
        return True
    if 'encoder' in s and ('error' in s or 'failed' in s):
        return True
    return False


def _get_execution_provider() -> Optional[str]:
    """Return DEFACE_EXECUTION_PROVIDER if set (e.g. CUDAExecutionProvider), else None."""
    try:
        from config import DEFACE_EXECUTION_PROVIDER
        return DEFACE_EXECUTION_PROVIDER
    except Exception:
        return None


def _get_ffmpeg_config(use_default_codec: bool = False) -> Optional[str]:
    """Return JSON string for --ffmpeg-config, or None to use deface default. use_default_codec=True forces libx264 (fallback)."""
    try:
        from config import DEFACE_FFMPEG_CODEC
        codec = 'libx264' if use_default_codec else (DEFACE_FFMPEG_CODEC or 'libx264')
    except Exception:
        codec = 'libx264'
    if not codec or codec.strip() == 'libx264':
        return None
    return json.dumps({'codec': codec.strip()})


def get_onnx_runtime_status() -> Dict:
    """
    Detect available ONNX Runtime execution providers (same env as deface).
    Returns dict with 'summary' (e.g. 'GPU (CUDA)' or 'CPU') and 'providers' list.
    """
    try:
        import onnxruntime as ort
        providers = ort.get_available_providers()
    except ImportError:
        return {
            'summary': 'Not installed',
            'providers': [],
            'error': 'onnxruntime not installed',
            'install_hint': 'pip install onnx onnxruntime-gpu  (optional, for faster video)',
        }
    except Exception as e:
        return {'summary': 'Unknown', 'providers': [], 'error': str(e)}
    # Prefer first non-CPU provider for label
    gpu_like = ('CUDAExecutionProvider', 'TensorrtExecutionProvider', 'DmlExecutionProvider',
                'CoreMLExecutionProvider', 'ROCMExecutionProvider', 'OpenVINOExecutionProvider')
    for p in providers:
        if p in gpu_like:
            short = p.replace('ExecutionProvider', '').replace('Dml', 'DirectML').replace('Rocm', 'ROCm')
            return {'summary': f'GPU ({short})', 'providers': providers}
    return {'summary': 'CPU', 'providers': providers}


def _video_debug(stage: str, msg: str) -> None:
    """Log to app.deface_video (file + in-memory buffer for live debug)."""
    try:
        from app.deface_video_log import append_video_log
        append_video_log(f"[deface_video] {stage} | {msg}")
    except Exception:
        logger.info(f"[deface_video] {stage} | {msg}")


def _find_deface_cmd() -> Optional[str]:
    """Find deface executable: project venv/bin, same dir as running Python, then PATH."""
    # 1) Project venv (works when app is run by Cursor/IDE using system Python)
    try:
        project_root = Path(__file__).resolve().parent.parent  # app/ -> project root
        deface_in_project_venv = project_root / 'venv' / 'bin' / 'deface'
        if deface_in_project_venv.exists():
            return str(deface_in_project_venv)
    except Exception:
        pass
    # 2) Same directory as sys.executable (e.g. venv/bin when started via ./scripts/restart.sh)
    try:
        python_dir = Path(sys.executable).resolve().parent
        deface_next_to_python = python_dir / 'deface'
        if deface_next_to_python.exists():
            return str(deface_next_to_python)
    except Exception:
        pass
    # 3) System PATH
    return shutil.which('deface')


def deface_image(
    input_path: Path,
    output_path: Path,
    replacewith: str = 'blur',
    boxes: bool = False,
    thresh: float = 0.2,
    scale: Optional[Tuple[int, int]] = None,
    mosaicsize: int = 20,
    draw_scores: bool = False
) -> dict:
    """
    Anonymize faces in an image using the deface tool
    
    Args:
        input_path: Path to input image
        output_path: Path to output image
        replacewith: Anonymization method ('blur', 'solid', 'mosaic')
        boxes: Use rectangular boxes instead of ellipses (for solid/mosaic)
        thresh: Detection threshold (0.0-1.0, default 0.2)
        scale: Downsampling size (width, height) or None for original
        mosaicsize: Size of mosaic tiles (default 20)
        draw_scores: Show detection scores (default False)
    
    Returns:
        dict with 'success' (bool) and optional 'error' (str)
    """
    try:
        if not input_path.exists():
            return {'success': False, 'error': f'Input image not found: {input_path}'}
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build deface command (venv bin same as Python, then PATH)
        deface_cmd_path = _find_deface_cmd()
        if not deface_cmd_path:
            error_msg = 'deface command not found. Please install: pip install deface (in the same env that runs the app, then restart)'
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        cmd = [deface_cmd_path, str(input_path), '-o', str(output_path)]
        
        # Add options
        if boxes:
            cmd.append('--boxes')
        
        if replacewith in ('solid', 'mosaic'):
            cmd.extend(['--replacewith', replacewith])
        
        if thresh != 0.2:  # Default threshold
            cmd.extend(['--thresh', str(thresh)])
        
        if scale:
            width, height = scale
            cmd.extend(['--scale', f'{width}x{height}'])
        
        if replacewith == 'mosaic' and mosaicsize != 20:  # Default mosaic size
            cmd.extend(['--mosaicsize', str(mosaicsize)])
        
        if draw_scores:
            cmd.append('--draw-scores')
        ep = _get_execution_provider()
        if ep:
            cmd.extend(['--execution-provider', ep])
        ffmpeg_cfg = _get_ffmpeg_config(use_default_codec=False)
        if ffmpeg_cfg:
            cmd.extend(['--ffmpeg-config', ffmpeg_cfg])
        
        logger.info(f"Running deface: {' '.join(cmd)}")
        
        # Run deface command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or 'Unknown error'
            logger.error(f"Deface failed: {error_msg}")
            return {'success': False, 'error': f'Deface processing failed: {error_msg}'}
        
        if not output_path.exists():
            return {'success': False, 'error': 'Output file was not created'}
        
        logger.info(f"Deface processing successful: {output_path}")
        return {'success': True, 'output_path': str(output_path)}
    
    except subprocess.TimeoutExpired:
        logger.error(f"Deface processing timeout for {input_path}")
        return {'success': False, 'error': 'Processing timeout (exceeded 5 minutes)'}
    except Exception as e:
        logger.error(f"Error in deface_image: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def deface_images(
    image_paths: List[Path],
    output_dir: Path,
    replacewith: str = 'blur',
    boxes: bool = False,
    thresh: float = 0.2,
    scale: Optional[Tuple[int, int]] = None,
    mosaicsize: int = 20,
    draw_scores: bool = False,
    output_prefix: str = 'deface_'
) -> dict:
    """
    Anonymize faces in multiple images
    
    Args:
        image_paths: List of input image paths
        output_dir: Directory to save anonymized images
        replacewith: Anonymization method ('blur', 'solid', 'mosaic')
        boxes: Use rectangular boxes instead of ellipses
        thresh: Detection threshold (0.0-1.0)
        scale: Downsampling size (width, height) or None
        mosaicsize: Size of mosaic tiles
        draw_scores: Show detection scores
        output_prefix: Prefix to add to output filenames
    
    Returns:
        dict with 'success' (bool), 'processed' (list of output paths), 'errors' (list)
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processed = []
    errors = []
    
    for img_path in image_paths:
        try:
            # Generate output filename with prefix (avoid double deface_ if input already has it)
            filename = img_path.name
            if filename.startswith('deface_'):
                filename = filename[7:]
            output_filename = f"{output_prefix}{filename}"
            output_path = output_dir / output_filename
            
            result = deface_image(
                img_path,
                output_path,
                replacewith=replacewith,
                boxes=boxes,
                thresh=thresh,
                scale=scale,
                mosaicsize=mosaicsize,
                draw_scores=draw_scores
            )
            
            if result.get('success'):
                processed.append(str(output_path))
            else:
                errors.append({
                    'input': str(img_path),
                    'error': result.get('error', 'Unknown error')
                })
        
        except Exception as e:
            logger.error(f"Error processing {img_path}: {e}", exc_info=True)
            errors.append({
                'input': str(img_path),
                'error': str(e)
            })
    
    return {
        'success': len(errors) == 0,
        'processed': processed,
        'errors': errors,
        'total': len(image_paths),
        'successful': len(processed),
        'failed': len(errors)
    }


def deface_video(
    video_path: Path,
    output_dir: Path,
    replacewith: str = 'blur',
    boxes: bool = False,
    thresh: float = 0.2,
    scale: Optional[Tuple[int, int]] = None,
    mosaicsize: int = 20,
    draw_scores: bool = False,
    output_prefix: str = 'deface_'
) -> dict:
    """
    Process video directly with deface tool and save as MP4 format

    Returns:
        dict with 'success' (bool), 'processed' (list with single MP4 path), 'errors' (list)
    """
    try:
        # Stage 1: Input validation
        _video_debug("1_input", f"input={video_path.name} path={video_path}")
        if not video_path.exists():
            _video_debug("1_input", "FAIL video file not found")
            return {
                'success': False,
                'processed': [],
                'errors': [{'input': str(video_path), 'error': f'Video not found: {video_path}'}],
                'total': 1,
                'successful': 0,
                'failed': 1
            }
        _video_debug("1_input", "OK file exists")

        # Preflight: check file is a valid video (fail fast with clear message)
        try:
            from app.video_processor import get_video_info
            info = get_video_info(video_path)
            if not info:
                _video_debug("1_preflight", "FAIL video not readable or unsupported format")
                return {
                    'success': False,
                    'processed': [],
                    'errors': [{'input': str(video_path), 'error': 'Video may be corrupt or in an unsupported format. Try re-exporting the video or use a different file.'}],
                    'total': 1,
                    'successful': 0,
                    'failed': 1
                }
            _video_debug("1_preflight", f"OK duration={info.get('duration')} fps={info.get('fps')}")
        except Exception as e:
            logger.warning(f"Deface preflight skip (video_processor): {e}")
            # Continue without preflight if dependency fails

        # Stage 2: Output path (avoid double deface_ if input already has it)
        output_dir.mkdir(parents=True, exist_ok=True)
        video_stem = video_path.stem
        if video_stem.startswith('deface_'):
            video_stem = video_stem[7:]
        output_filename = f"{output_prefix}{video_stem}.mp4"
        output_path = output_dir / output_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        _video_debug("2_output", f"output={output_path.name} dir={output_dir}")

        # Stage 3: Find deface command
        _video_debug("3_cmd_lookup", "finding deface executable...")
        deface_cmd_path = _find_deface_cmd()
        if not deface_cmd_path:
            _video_debug("3_cmd_lookup", "FAIL deface not found")
            error_msg = 'deface command not found. Please install: pip install deface (in the same env that runs the app, then restart)'
            logger.error(error_msg)
            return {
                'success': False,
                'processed': [],
                'errors': [{'input': str(video_path), 'error': error_msg}],
                'total': 1,
                'successful': 0,
                'failed': 1
            }
        _video_debug("3_cmd_lookup", f"OK deface={deface_cmd_path}")

        # Stage 4: Build base command (extra args for GPU/hw encode added per attempt for fallback)
        base_cmd = [deface_cmd_path, str(video_path), '-o', str(output_path)]
        if boxes:
            base_cmd.append('--boxes')
        if replacewith in ('solid', 'mosaic'):
            base_cmd.extend(['--replacewith', replacewith])
        if thresh != 0.2:
            base_cmd.extend(['--thresh', str(thresh)])
        if scale:
            width, height = scale
            base_cmd.extend(['--scale', f'{width}x{height}'])
        if replacewith == 'mosaic' and mosaicsize != 20:
            base_cmd.extend(['--mosaicsize', str(mosaicsize)])
        if draw_scores:
            base_cmd.append('--draw-scores')
        ep = _get_execution_provider()
        ffmpeg_cfg_default = _get_ffmpeg_config(use_default_codec=True)
        ffmpeg_cfg_hw = _get_ffmpeg_config(use_default_codec=False)
        _video_debug("4_build", "base_cmd built; ep=%s ffmpeg=%s" % (ep or 'auto', 'hw' if ffmpeg_cfg_hw else 'default'))

        # Stage 5: Run subprocess (with optional one retry on transient errors; hw encode fallback to libx264)
        video_timeout = _get_deface_video_timeout()
        last_failure = None
        last_stderr = None
        for attempt in range(2):
            cmd = list(base_cmd)
            if ep:
                cmd.extend(['--execution-provider', ep])
            if attempt > 0 and last_stderr and _is_codec_encode_error(last_stderr) and ffmpeg_cfg_hw:
                _video_debug("5_run", "Retrying with default codec (libx264) after hardware encode failure...")
            elif attempt > 0:
                _video_debug("5_run", "Retrying once after transient error...")
            use_ffmpeg = ffmpeg_cfg_hw if not (attempt > 0 and last_stderr and _is_codec_encode_error(last_stderr)) else ffmpeg_cfg_default
            if use_ffmpeg:
                cmd.extend(['--ffmpeg-config', use_ffmpeg])
            _video_debug("4_build", f"attempt={attempt} cmd={' '.join(cmd)}")
            _video_debug("5_run", f"starting subprocess (timeout={video_timeout}s)...")
            video_name = video_path.name
            _video_debug("5_run", f"processing {video_name} (this may take 1–2 min)...")
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stderr_lines = []
            heartbeat_stop = threading.Event()

            def read_stderr():
                for line in proc.stderr:
                    if line:
                        line = line.rstrip()
                        stderr_lines.append(line)
                        try:
                            from app.deface_video_log import append_video_log, set_deface_current_item_pct
                            append_video_log(f"[deface_video] 5_run | {line}")
                            pct_matches = list(re.finditer(r'(\d+)%', line))
                            if pct_matches:
                                set_deface_current_item_pct(int(pct_matches[-1].group(1)))
                            else:
                                frac = re.search(r'(\d+)/(\d+)\b', line)
                                if frac:
                                    cur, tot = int(frac.group(1)), int(frac.group(2))
                                    if tot > 0:
                                        set_deface_current_item_pct(int(round(100 * cur / tot)))
                        except Exception:
                            pass

            def heartbeat():
                start = time.monotonic()
                while True:
                    if heartbeat_stop.wait(timeout=5):
                        break
                    elapsed = int(time.monotonic() - start)
                    try:
                        from app.deface_video_log import append_video_log, set_deface_elapsed
                        set_deface_elapsed(elapsed)
                        append_video_log(f"[deface_video] 5_run | still processing {video_name}... ({elapsed}s elapsed)")
                    except Exception:
                        pass

            reader = threading.Thread(target=read_stderr, daemon=True)
            reader.start()
            heart = threading.Thread(target=heartbeat, daemon=True)
            heart.start()
            try:
                stdout_raw, stderr_raw = proc.communicate(timeout=video_timeout)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.communicate()
                heartbeat_stop.set()
                timeout_sec = _get_deface_video_timeout()
                mins = timeout_sec // 60
                last_failure = {
                    'success': False,
                    'processed': [],
                    'errors': [{'input': str(video_path), 'error': f'Processing timed out (exceeded {mins} minute{"s" if mins != 1 else ""}). Try a shorter video or use Detection Scale 640×360 for faster processing.'}],
                    'total': 1,
                    'successful': 0,
                    'failed': 1
                }
                if attempt == 0:
                    continue
                return last_failure
            heartbeat_stop.set()
            reader.join(timeout=2)
            combined_stderr = (stderr_raw or '') + ('\n'.join(stderr_lines) if stderr_lines else '')
            result = type('Result', (), {'returncode': proc.returncode, 'stdout': stdout_raw or '', 'stderr': combined_stderr})()

            _video_debug("5_run", f"subprocess finished returncode={result.returncode} stdout_len={len(result.stdout or '')} stderr_len={len(result.stderr or '')}")

            if result.returncode != 0:
                raw_error = result.stderr or result.stdout or 'Unknown error'
                last_stderr = raw_error
                user_msg = _user_facing_deface_error(raw_error)
                _video_debug("5_run", f"FAIL stderr={raw_error[:500]}")
                logger.error(f"Deface video processing failed: {raw_error}")
                last_failure = {
                    'success': False,
                    'processed': [],
                    'errors': [{'input': str(video_path), 'error': f'Deface processing failed: {user_msg}'}],
                    'total': 1,
                    'successful': 0,
                    'failed': 1
                }
                if _is_retryable_error(user_msg) and attempt == 0:
                    continue
                if _is_codec_encode_error(last_stderr) and ffmpeg_cfg_hw and attempt == 0:
                    continue
                return last_failure

            # Stage 6: Verify output file
            _video_debug("6_verify", f"checking output exists: {output_path}")
            if not output_path.exists():
                _video_debug("6_verify", "FAIL output file was not created")
                return {
                    'success': False,
                    'processed': [],
                    'errors': [{'input': str(video_path), 'error': 'Output video file was not created'}],
                    'total': 1,
                    'successful': 0,
                    'failed': 1
                }
            size = output_path.stat().st_size
            _video_debug("6_verify", f"OK output size={size} bytes")

            # Stage 7: Success
            _video_debug("7_done", f"success output={output_path}")
            return {
                'success': True,
                'processed': [str(output_path)],
                'errors': [],
                'total': 1,
                'successful': 1,
                'failed': 0
            }

        if last_failure:
            return last_failure

    except subprocess.TimeoutExpired as e:
        timeout_sec = getattr(e, 'timeout', _get_deface_video_timeout())
        mins = timeout_sec // 60
        _video_debug("5_run", f"FAIL timeout after {timeout_sec}s")
        logger.error(f"Deface video processing timeout for {video_path}")
        return {
            'success': False,
            'processed': [],
            'errors': [{'input': str(video_path), 'error': f'Processing timed out (exceeded {mins} minute{"s" if mins != 1 else ""}). Try a shorter video or use Detection Scale 640×360 for faster processing.'}],
            'total': 1,
            'successful': 0,
            'failed': 1
        }
    except Exception as e:
        _video_debug("exception", f"{video_path.name}: {e}")
        logger.exception(f"[deface_video] exception | {video_path.name}: {e}")
        return {
            'success': False,
            'processed': [],
            'errors': [{'input': str(video_path), 'error': str(e)}],
            'total': 1,
            'successful': 0,
            'failed': 1
        }


def apply_manual_deface(
    image_path: Path,
    output_path: Path,
    deface_areas: List[Dict],
    mosaicsize: int = 20
) -> dict:
    """
    Apply manual deface areas to an image
    
    Args:
        image_path: Path to input image (should already be defaced with automated deface)
        output_path: Path to save image with manual defaces applied
        deface_areas: List of deface area definitions, each with:
            - x (int): X coordinate (top-left corner)
            - y (int): Y coordinate (top-left corner)
            - width (int): Width of deface area
            - height (int): Height of deface area
            - shape (str): 'square' or 'rectangular'
            - method (str): 'blur', 'solid', or 'mosaic'
            - mosaicsize (int, optional): Mosaic tile size (if method is 'mosaic')
        mosaicsize: Default mosaic tile size
    
    Returns:
        dict with 'success' (bool) and optional 'error' (str)
    """
    try:
        from PIL import Image, ImageFilter, ImageDraw
        
        if not image_path.exists():
            return {'success': False, 'error': f'Input image not found: {image_path}'}
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load image
        img = Image.open(image_path)
        
        # Convert to RGB if necessary (for JPEG compatibility)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Apply each deface area
        for area in deface_areas:
            x = int(area.get('x', 0))
            y = int(area.get('y', 0))
            width = int(area.get('width', 0))
            height = int(area.get('height', 0))
            shape = area.get('shape', 'square')
            method = area.get('method', 'blur')
            area_mosaicsize = area.get('mosaicsize', mosaicsize)
            
            # Validate coordinates (ensure within image bounds)
            img_width, img_height = img.size
            x = max(0, min(x, img_width - 1))
            y = max(0, min(y, img_height - 1))
            width = max(1, min(width, img_width - x))
            height = max(1, min(height, img_height - y))
            
            # Extract region
            region = img.crop((x, y, x + width, y + height))
            
            # Apply deface method
            if method == 'blur':
                # Apply Gaussian blur
                blurred_region = region.filter(ImageFilter.GaussianBlur(radius=15))
                img.paste(blurred_region, (x, y))
            
            elif method == 'solid':
                # Draw solid black box
                draw = ImageDraw.Draw(img)
                draw.rectangle([x, y, x + width, y + height], fill='black')
            
            elif method == 'mosaic':
                # Apply mosaic effect (pixelation)
                # Downscale then upscale to create pixelation
                small_size = (max(1, width // area_mosaicsize), max(1, height // area_mosaicsize))
                if small_size[0] > 0 and small_size[1] > 0:
                    small_region = region.resize(small_size, Image.Resampling.NEAREST)
                    mosaic_region = small_region.resize((width, height), Image.Resampling.NEAREST)
                    img.paste(mosaic_region, (x, y))
                else:
                    # If too small, just use solid black
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([x, y, x + width, y + height], fill='black')
            
            else:
                logger.warning(f"Unknown deface method: {method}, skipping area")
        
        # Save image
        img.save(output_path, 'JPEG', quality=95)
        logger.info(f"Manual deface applied successfully: {output_path} with {len(deface_areas)} areas")
        
        return {'success': True, 'output_path': str(output_path)}
    
    except Exception as e:
        logger.error(f"Error in apply_manual_deface: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def apply_manual_deface_to_video(
    video_path: Path,
    time_point: float,
    output_dir: Path,
    deface_areas: List[Dict],
    mosaicsize: int = 20,
    output_prefix: str = 'deface_manual_'
) -> dict:
    """
    Extract a frame from video at specific time point, apply manual deface, and save frame
    
    Args:
        video_path: Path to defaced video file (MP4)
        time_point: Time in seconds to extract frame
        output_dir: Directory to save defaced frame
        deface_areas: List of deface area definitions (same format as apply_manual_deface)
        mosaicsize: Default mosaic tile size
        output_prefix: Prefix to add to output filename
    
    Returns:
        dict with 'success' (bool), 'output_path' (str), 'time_point' (float), and optional 'error' (str)
    """
    try:
        if not video_path.exists():
            return {'success': False, 'error': f'Video file not found: {video_path}'}
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract frame from video at time_point
        from app.video_processor import extract_frame
        import tempfile
        
        temp_extract_dir = Path(tempfile.mkdtemp())
        temp_frame_path = temp_extract_dir / 'temp_frame.jpg'
        
        try:
            # Extract frame at time_point
            if not extract_frame(video_path, time_point, temp_frame_path, quality=95, resolution=None):
                return {'success': False, 'error': f'Failed to extract frame at time {time_point}s'}
            
            if not temp_frame_path.exists():
                return {'success': False, 'error': 'Extracted frame file not created'}
            
            # Generate output filename with prefix and time point
            video_stem = video_path.stem
            if video_stem.startswith('deface_'):
                video_stem = video_stem[7:]  # Remove deface_ prefix if present
            
            # Format time point (e.g., 5.2 -> 05_20)
            time_str = f"{int(time_point)}_{int((time_point % 1) * 100):02d}"
            output_filename = f"{output_prefix}{video_stem}_frame_{time_str}.jpg"
            output_path = output_dir / output_filename
            
            # Apply manual deface to extracted frame
            result = apply_manual_deface(
                temp_frame_path,
                output_path,
                deface_areas,
                mosaicsize=mosaicsize
            )
            
            if not result.get('success'):
                return {'success': False, 'error': result.get('error', 'Failed to apply manual deface to frame')}
            
            logger.info(f"Manual deface applied to video frame at {time_point}s: {output_path}")
            return {
                'success': True,
                'output_path': str(output_path),
                'time_point': time_point
            }
        
        finally:
            # Cleanup temporary extraction directory
            if temp_extract_dir.exists():
                import shutil
                shutil.rmtree(temp_extract_dir, ignore_errors=True)
    
    except Exception as e:
        logger.error(f"Error in apply_manual_deface_to_video: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}
