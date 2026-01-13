"""
Deface processor for face anonymization in images and videos
Uses the deface command-line tool to anonymize faces in images and videos
Also supports manual deface areas for precise control
"""
import subprocess
import logging
from pathlib import Path
from typing import Optional, Tuple, List, Dict
import tempfile
import shutil

logger = logging.getLogger(__name__)


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
        
        # Build deface command - find deface in PATH (should be in venv/bin when Flask runs)
        deface_cmd_path = shutil.which('deface')
        if not deface_cmd_path:
            error_msg = 'deface command not found. Please install: pip install deface'
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
            # Generate output filename with prefix
            filename = img_path.name
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
    
    Args:
        video_path: Path to input video file
        output_dir: Directory to save anonymized video
        replacewith: Anonymization method ('blur', 'solid', 'mosaic')
        boxes: Use rectangular boxes instead of ellipses
        thresh: Detection threshold (0.0-1.0)
        scale: Downsampling size (width, height) or None
        mosaicsize: Size of mosaic tiles
        draw_scores: Show detection scores
        output_prefix: Prefix to add to output filename
    
    Returns:
        dict with 'success' (bool), 'processed' (list with single MP4 path), 'errors' (list)
    """
    try:
        if not video_path.exists():
            return {
                'success': False,
                'processed': [],
                'errors': [{'input': str(video_path), 'error': f'Video not found: {video_path}'}],
                'total': 1,
                'successful': 0,
                'failed': 1
            }
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate output filename with prefix (MP4 format)
        video_stem = video_path.stem
        output_filename = f"{output_prefix}{video_stem}.mp4"
        output_path = output_dir / output_filename
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build deface command - find deface in PATH (should be in venv/bin when Flask runs)
        deface_cmd_path = shutil.which('deface')
        if not deface_cmd_path:
            error_msg = 'deface command not found. Please install: pip install deface'
            logger.error(error_msg)
            return {
                'success': False,
                'processed': [],
                'errors': [{'input': str(video_path), 'error': error_msg}],
                'total': 1,
                'successful': 0,
                'failed': 1
            }
        
        cmd = [deface_cmd_path, str(video_path), '-o', str(output_path)]
        
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
        
        logger.info(f"Processing video with deface: {' '.join(cmd)}")
        
        # Run deface command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout for videos
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or 'Unknown error'
            logger.error(f"Deface video processing failed: {error_msg}")
            return {
                'success': False,
                'processed': [],
                'errors': [{'input': str(video_path), 'error': f'Deface processing failed: {error_msg}'}],
                'total': 1,
                'successful': 0,
                'failed': 1
            }
        
        if not output_path.exists():
            return {
                'success': False,
                'processed': [],
                'errors': [{'input': str(video_path), 'error': 'Output video file was not created'}],
                'total': 1,
                'successful': 0,
                'failed': 1
            }
        
        logger.info(f"Deface video processing successful: {output_path}")
        return {
            'success': True,
            'processed': [str(output_path)],
            'errors': [],
            'total': 1,
            'successful': 1,
            'failed': 0
        }
    
    except subprocess.TimeoutExpired:
        logger.error(f"Deface video processing timeout for {video_path}")
        return {
            'success': False,
            'processed': [],
            'errors': [{'input': str(video_path), 'error': 'Processing timeout (exceeded 10 minutes)'}],
            'total': 1,
            'successful': 0,
            'failed': 1
        }
    except Exception as e:
        logger.error(f"Error in deface_video: {e}", exc_info=True)
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
