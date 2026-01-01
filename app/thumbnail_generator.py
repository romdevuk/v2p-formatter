"""
Thumbnail generation for media files
"""
import logging
from pathlib import Path
from PIL import Image
import subprocess
import io
import hashlib

logger = logging.getLogger('media_converter.thumbnail')


def get_thumbnail_cache_path(file_path: Path, size: tuple = (120, 90)) -> Path:
    """
    Get cache path for thumbnail
    
    Args:
        file_path: Path to source file
        size: Thumbnail size (width, height)
    
    Returns:
        Path to cached thumbnail
    """
    from config import BASE_DIR
    
    # Create cache directory
    cache_dir = BASE_DIR / 'static' / 'cache' / 'thumbnails'
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate cache key from file path and modification time
    file_stat = file_path.stat()
    cache_key = f"{file_path}_{file_stat.st_mtime}_{size[0]}x{size[1]}"
    cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
    
    return cache_dir / f"{cache_hash}.jpg"


def generate_image_thumbnail(image_path: Path, size: tuple = (120, 90)) -> bytes:
    """
    Generate thumbnail from image file
    
    Args:
        image_path: Path to image file
        size: Thumbnail size (width, height)
    
    Returns:
        Thumbnail image bytes (JPEG)
    """
    try:
        with Image.open(image_path) as img:
            # Apply EXIF orientation first (if present) to get correct orientation
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
            
            # Convert to RGB if needed
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to exact size using high-quality resampling
            # Calculate target size maintaining aspect ratio
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # If image is smaller than target, upscale using LANCZOS for better quality
            if img.size[0] < size[0] or img.size[1] < size[1]:
                # Calculate scaling to fill target size while maintaining aspect
                scale = max(size[0] / img.size[0], size[1] / img.size[1])
                new_size = (int(img.size[0] * scale), int(img.size[1] * scale))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                # Crop to exact size if needed
                if img.size[0] > size[0] or img.size[1] > size[1]:
                    left = (img.size[0] - size[0]) // 2
                    top = (img.size[1] - size[1]) // 2
                    img = img.crop((left, top, left + size[0], top + size[1]))
            
            # Save to bytes - EXIF orientation already applied via exif_transpose
            # The image is now correctly oriented, so saving will preserve correct orientation
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=100, optimize=False, subsampling=0)  # 100% quality, no chroma subsampling for best quality
            return output.getvalue()
    
    except Exception as e:
        logger.error(f"Error generating image thumbnail: {e}", exc_info=True)
        raise


def generate_video_thumbnail(video_path: Path, size: tuple = (120, 90), time_seconds: float = 1.0) -> bytes:
    """
    Extract frame from video and generate thumbnail
    
    Args:
        video_path: Path to video file
        size: Thumbnail size (width, height)
        time_seconds: Time in seconds to extract frame (default: 1.0)
    
    Returns:
        Thumbnail image bytes (JPEG)
    """
    try:
        # Check if video file exists
        if not video_path.exists():
            raise Exception(f"Video file not found: {video_path}")
        
        # Get video duration first to ensure time_seconds is valid
        try:
            probe_cmd = [
                'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', str(video_path)
            ]
            probe_result = subprocess.run(probe_cmd, capture_output=True, timeout=5, text=True)
            if probe_result.returncode == 0 and probe_result.stdout.strip():
                duration_str = probe_result.stdout.strip()
                try:
                    duration = float(duration_str)
                    if duration > 0:
                        if time_seconds >= duration or duration < 0.1:
                            # For very short videos or if requested time is past end, use time 0
                            time_seconds = 0.0
                            logger.info(f"Very short video ({duration}s) or time past end, using time 0")
                        elif time_seconds > duration * 0.9:
                            # If time is very close to end, use middle of video
                            time_seconds = duration * 0.5
                            logger.info(f"Time close to end ({duration}s), using middle: {time_seconds}s")
                except ValueError:
                    logger.warning(f"Could not parse duration '{duration_str}', using provided time")
        except FileNotFoundError:
            logger.warning("ffprobe not found, cannot check video duration")
        except Exception as e:
            logger.warning(f"Could not probe video duration, using provided time: {e}")
        
        # Use FFmpeg to extract frame with high quality settings
        # Scale to at least 2x the target size first, then downscale for better quality
        scale_width = max(size[0] * 2, 1280)  # At least 1280px wide for quality
        scale_height = max(size[1] * 2, 960)   # At least 960px tall for quality
        
        # For very short videos or time 0, use input seeking (after -i) for accuracy
        # For longer videos, seek before input (-ss before -i) for faster processing
        if time_seconds == 0.0 or time_seconds < 0.1:
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-ss', str(time_seconds),
                '-vframes', '1',
                '-vf', f'scale={scale_width}:{scale_height}:force_original_aspect_ratio=decrease',
                '-f', 'image2pipe',
                '-vcodec', 'mjpeg',
                '-q:v', '2',
                '-'
            ]
        else:
            # For longer videos, seek before input for faster processing
            cmd = [
                'ffmpeg',
                '-ss', str(time_seconds),
                '-i', str(video_path),
                '-vframes', '1',
                '-vf', f'scale={scale_width}:{scale_height}:force_original_aspect_ratio=decrease',
                '-f', 'image2pipe',
                '-vcodec', 'mjpeg',
                '-q:v', '2',
                '-'
            ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=10
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.decode() if result.stderr else "Unknown FFmpeg error"
            logger.error(f"FFmpeg error for {video_path} at {time_seconds}s: {error_msg}")
            raise Exception(f"FFmpeg failed: {error_msg}")
        
        # Open the extracted frame with Pillow to ensure it's JPEG
        frame_data = result.stdout
        if not frame_data or len(frame_data) == 0:
            logger.error(f"No frame data extracted from {video_path} at {time_seconds}s")
            raise Exception(f"No frame data extracted from video at {time_seconds}s - video might be too short or corrupted")
        
        with Image.open(io.BytesIO(frame_data)) as img:
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to exact target size using high-quality resampling
            # Use LANCZOS for best quality when downscaling
            img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Save to bytes with maximum quality
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=95, optimize=False, subsampling=0)  # No chroma subsampling for best quality
            return output.getvalue()
    
    except Exception as e:
        logger.error(f"Error generating video thumbnail: {e}", exc_info=True)
        raise


def generate_pdf_thumbnail(pdf_path: Path, size: tuple = (120, 90), page: int = 0) -> bytes:
    """
    Generate thumbnail from PDF file (first page)
    
    Args:
        pdf_path: Path to PDF file
        size: Thumbnail size (width, height)
        page: Page number to use (default: 0 for first page)
    
    Returns:
        Thumbnail image bytes (JPEG)
    """
    try:
        # Try using pdf2image (requires poppler)
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(pdf_path, first_page=page+1, last_page=page+1, dpi=150)
            if images:
                img = images[0]
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Create thumbnail (preserves aspect ratio)
                img.thumbnail(size, Image.Resampling.LANCZOS)
                # Save to bytes
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=100, optimize=True)
                return output.getvalue()
        except ImportError:
            logger.warning("pdf2image not available, using PDF placeholder")
        except Exception as e:
            logger.warning(f"Error using pdf2image: {e}, using PDF placeholder")
        
        # Fallback: Create a PDF icon placeholder
        img = Image.new('RGB', size, color=(255, 255, 255))  # White background
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Draw a simple PDF icon
        # Draw a document shape
        margin = 5
        doc_width = size[0] - 2 * margin
        doc_height = size[1] - 2 * margin
        draw.rectangle(
            [margin, margin, margin + doc_width, margin + doc_height],
            outline=(200, 0, 0),  # Red outline
            width=2
        )
        
        # Draw text "PDF"
        try:
            font_size = min(size[0], size[1]) // 4
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            font = ImageFont.load_default()
        
        text = "PDF"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (size[0] - text_width) // 2
        text_y = (size[1] - text_height) // 2
        draw.text((text_x, text_y), text, fill=(200, 0, 0), font=font)
        
        # Save to bytes
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=100, optimize=True)
        return output.getvalue()
    
    except Exception as e:
        logger.error(f"Error generating PDF thumbnail: {e}", exc_info=True)
        raise


def generate_audio_thumbnail(size: tuple = (120, 90)) -> bytes:
    """
    Generate placeholder thumbnail for audio files
    
    Args:
        size: Thumbnail size (width, height)
    
    Returns:
        Thumbnail image bytes (JPEG)
    """
    try:
        # Create a simple audio icon placeholder
        img = Image.new('RGB', size, color=(50, 50, 50))  # Dark gray background
        
        # Draw a simple audio waveform icon
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Draw audio waveform bars
        center_x, center_y = size[0] // 2, size[1] // 2
        bar_width = 3
        bar_spacing = 2
        num_bars = 5
        
        for i in range(num_bars):
            x = center_x - (num_bars * (bar_width + bar_spacing)) // 2 + i * (bar_width + bar_spacing)
            bar_height = (i + 1) * (size[1] // 8)
            draw.rectangle(
                [x, center_y - bar_height // 2, x + bar_width, center_y + bar_height // 2],
                fill=(100, 150, 255)  # Light blue color
            )
        
        # Save to bytes
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=100, optimize=True)
        return output.getvalue()
    
    except Exception as e:
        logger.error(f"Error generating audio thumbnail: {e}", exc_info=True)
        raise


def get_thumbnail(file_path: Path, file_type: str, size: tuple = (120, 90), use_cache: bool = True) -> bytes:
    """
    Get thumbnail for a file (with caching)
    
    Args:
        file_path: Path to file
        file_type: 'mov', 'mp4', 'mp3', 'jpg', 'jpeg', 'png', or 'pdf'
        size: Thumbnail size (width, height)
        use_cache: Whether to use cache
    
    Returns:
        Thumbnail image bytes (JPEG)
    """
    # Check cache first
    if use_cache:
        cache_path = get_thumbnail_cache_path(file_path, size)
        if cache_path.exists():
            try:
                return cache_path.read_bytes()
            except Exception as e:
                logger.warning(f"Error reading cache: {e}")
    
    # Generate thumbnail
    if file_type in ('mov', 'mp4'):
        thumbnail_data = generate_video_thumbnail(file_path, size)
    elif file_type == 'mp3':
        thumbnail_data = generate_audio_thumbnail(size)
    elif file_type in ('jpg', 'jpeg', 'png', 'gif', 'webp'):
        thumbnail_data = generate_image_thumbnail(file_path, size)
    elif file_type == 'pdf':
        thumbnail_data = generate_pdf_thumbnail(file_path, size)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    # Save to cache
    if use_cache:
        try:
            cache_path.write_bytes(thumbnail_data)
        except Exception as e:
            logger.warning(f"Error writing cache: {e}")
    
    return thumbnail_data

