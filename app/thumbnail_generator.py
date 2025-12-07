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
            
            # Create thumbnail (preserves aspect ratio)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Save to bytes
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=100, optimize=True)
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
        # Use FFmpeg to extract frame
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-ss', str(time_seconds),
            '-vframes', '1',
            '-vf', f'scale={size[0]}:{size[1]}:force_original_aspect_ratio=decrease',
            '-f', 'image2pipe',
            '-vcodec', 'mjpeg',
            '-'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=10
        )
        
        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr.decode()}")
            raise Exception(f"FFmpeg failed: {result.stderr.decode()}")
        
        # Open the extracted frame with Pillow to ensure it's JPEG
        frame_data = result.stdout
        if not frame_data:
            raise Exception("No frame data extracted")
        
        with Image.open(io.BytesIO(frame_data)) as img:
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Ensure it's the right size (FFmpeg may not respect exact size)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Save to bytes
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=100, optimize=True)
            return output.getvalue()
    
    except Exception as e:
        logger.error(f"Error generating video thumbnail: {e}", exc_info=True)
        raise


def get_thumbnail(file_path: Path, file_type: str, size: tuple = (120, 90), use_cache: bool = True) -> bytes:
    """
    Get thumbnail for a file (with caching)
    
    Args:
        file_path: Path to file
        file_type: 'mov', 'jpg', 'jpeg', or 'png'
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
    elif file_type in ('jpg', 'jpeg', 'png'):
        thumbnail_data = generate_image_thumbnail(file_path, size)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    # Save to cache
    if use_cache:
        try:
            cache_path.write_bytes(thumbnail_data)
        except Exception as e:
            logger.warning(f"Error writing cache: {e}")
    
    return thumbnail_data

