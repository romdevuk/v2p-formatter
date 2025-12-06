"""
Image rotation module for rotating original images
"""
import logging
from pathlib import Path
from PIL import Image

logger = logging.getLogger('media_converter.image_rotator')


def rotate_image(image_path: Path, angle: int) -> dict:
    """
    Rotate an image file in place
    
    Args:
        image_path: Path to image file
        angle: Rotation angle in degrees (90, -90, 180, etc.)
    
    Returns:
        Dict with success status and details
    """
    import time
    start_time = time.time()
    
    # Validate input file
    if not image_path.exists():
        return {
            'success': False,
            'error': f'File not found: {image_path}',
            'error_type': 'FileNotFound'
        }
    
    try:
        # Open image
        with Image.open(image_path) as img:
            original_size = image_path.stat().st_size
            
            # Apply EXIF orientation first (if present) to get actual pixel orientation
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
            
            # Rotate image
            # PIL rotate: positive = counterclockwise, negative = clockwise
            # So -90 = clockwise (right), 90 = counterclockwise (left)
            rotated_img = img.rotate(-angle, expand=True)
            
            # Save rotated image (overwrite original)
            # Preserve original format
            img_format = img.format or 'JPEG'
            if img_format == 'JPEG' or image_path.suffix.lower() in ('.jpg', '.jpeg'):
                rotated_img = rotated_img.convert('RGB')
                # Remove EXIF orientation tag when saving (since we've already applied rotation to pixels)
                try:
                    exif = rotated_img.getexif() if hasattr(rotated_img, 'getexif') else None
                    if exif:
                        # Create new EXIF dict without orientation tag
                        exif_dict = dict(exif)
                        exif_dict.pop(274, None)  # Remove orientation tag (274)
                        # Save with updated EXIF (without orientation)
                        if exif_dict:
                            from PIL.ExifTags import TAGS
                            new_exif = Image.Exif()
                            for tag_id, value in exif_dict.items():
                                if tag_id != 274:  # Skip orientation tag
                                    new_exif[tag_id] = value
                            rotated_img.save(str(image_path), 'JPEG', quality=95, exif=new_exif)
                        else:
                            rotated_img.save(str(image_path), 'JPEG', quality=95)
                    else:
                        rotated_img.save(str(image_path), 'JPEG', quality=95)
                except Exception as e:
                    logger.warning(f"Could not update EXIF: {e}, saving without EXIF")
                    rotated_img.save(str(image_path), 'JPEG', quality=95)
            elif img_format == 'PNG' or image_path.suffix.lower() == '.png':
                # Preserve transparency if present
                if rotated_img.mode == 'RGBA':
                    rotated_img.save(str(image_path), 'PNG')
                else:
                    rotated_img = rotated_img.convert('RGB')
                    rotated_img.save(str(image_path), 'PNG')
            else:
                # Default to JPEG
                rotated_img = rotated_img.convert('RGB')
                try:
                    exif = rotated_img.getexif() if hasattr(rotated_img, 'getexif') else None
                    if exif:
                        exif_dict = dict(exif)
                        exif_dict.pop(274, None)  # Remove orientation tag
                        if exif_dict:
                            new_exif = Image.Exif()
                            for tag_id, value in exif_dict.items():
                                if tag_id != 274:
                                    new_exif[tag_id] = value
                            rotated_img.save(str(image_path), 'JPEG', quality=95, exif=new_exif)
                        else:
                            rotated_img.save(str(image_path), 'JPEG', quality=95)
                    else:
                        rotated_img.save(str(image_path), 'JPEG', quality=95)
                except Exception as e:
                    logger.warning(f"Could not update EXIF: {e}, saving without EXIF")
                    rotated_img.save(str(image_path), 'JPEG', quality=95)
        
        processing_time = time.time() - start_time
        new_size = image_path.stat().st_size
        
        # Clear thumbnail cache for this file (since it changed)
        from app.thumbnail_generator import get_thumbnail_cache_path
        cache_path = get_thumbnail_cache_path(image_path, (120, 90))
        if cache_path.exists():
            try:
                cache_path.unlink()
                logger.debug(f"Cleared thumbnail cache: {cache_path}")
            except Exception as e:
                logger.warning(f"Could not clear thumbnail cache: {e}")
        
        logger.info(f"Rotated image: {image_path.name} by {angle}° "
                   f"({original_size / (1024*1024):.2f}MB -> {new_size / (1024*1024):.2f}MB)")
        
        return {
            'success': True,
            'file_path': str(image_path),
            'angle': angle,
            'original_size': original_size,
            'new_size': new_size,
            'processing_time': round(processing_time, 2)
        }
    
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error rotating image {image_path}: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__,
            'processing_time': processing_time
        }

