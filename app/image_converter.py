"""
Image conversion module for converting JPG/PNG to JPEG
"""
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple
from PIL import Image

logger = logging.getLogger('media_converter.image_converter')


def get_image_info(image_path: Path) -> Dict:
    """
    Get image metadata using Pillow
    
    Returns:
        Dict with width, height, format, size, etc.
    """
    try:
        with Image.open(image_path) as img:
            # Apply EXIF orientation to get correct dimensions
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
            return {
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode,
                'size': image_path.stat().st_size,
                'size_mb': round(image_path.stat().st_size / (1024 * 1024), 2)
            }
    except Exception as e:
        logger.error(f"Error getting image info: {e}", exc_info=True)
        return {'error': str(e)}


def convert_image_to_jpeg(
    input_path: Path,
    output_path: Path,
    resolution: Optional[Tuple[int, int]] = None,
    quality: int = 80,
    maintain_aspect: bool = True,
    allow_stretch: bool = False
) -> Dict:
    """
    Convert JPG/PNG to JPEG using Pillow
    
    Args:
        input_path: Path to input image file
        output_path: Path to output JPEG file
        resolution: Optional tuple (width, height) for resizing
        quality: JPEG quality (1-100)
        maintain_aspect: If True, maintain aspect ratio when resizing
        allow_stretch: If True, allow stretching to exact dimensions
    
    Returns:
        Dict with success status, output_size, processing_time, etc.
    """
    import time
    start_time = time.time()
    
    # Validate input file
    if not input_path.exists():
        return {
            'success': False,
            'error': f'Input file not found: {input_path}',
            'error_type': 'FileNotFound'
        }
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Open image
        with Image.open(input_path) as img:
            # Apply EXIF orientation first (if present) to get correct orientation
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
            
            original_size = input_path.stat().st_size
            original_width, original_height = img.size
            
            # Convert RGBA to RGB if needed (for PNG with transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if resolution specified
            if resolution:
                target_width, target_height = resolution
                
                if maintain_aspect and not allow_stretch:
                    # Maintain aspect ratio
                    img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
                else:
                    # Stretch to exact dimensions
                    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Save as JPEG - EXIF orientation already applied via exif_transpose
            # The image is now correctly oriented, so saving will preserve correct orientation
            img.save(
                str(output_path),
                'JPEG',
                quality=quality,
                optimize=True
            )
        
        processing_time = time.time() - start_time
        
        # Get output file size
        if output_path.exists():
            output_size = output_path.stat().st_size
            reduction_percent = round((1 - output_size / original_size) * 100, 2) if original_size > 0 else 0
            
            # Get final dimensions
            with Image.open(output_path) as final_img:
                final_width, final_height = final_img.size
            
            logger.info(f"Conversion successful: {input_path.name} -> {output_path.name} "
                       f"({original_size / (1024*1024):.2f}MB -> {output_size / (1024*1024):.2f}MB, "
                       f"{reduction_percent}% reduction)")
            
            return {
                'success': True,
                'output_path': str(output_path),
                'output_size': output_size,
                'output_size_mb': round(output_size / (1024 * 1024), 2),
                'input_size': original_size,
                'input_size_mb': round(original_size / (1024 * 1024), 2),
                'reduction_percent': reduction_percent,
                'original_width': original_width,
                'original_height': original_height,
                'final_width': final_width,
                'final_height': final_height,
                'processing_time': round(processing_time, 2)
            }
        else:
            return {
                'success': False,
                'error': 'Output file was not created',
                'error_type': 'OutputFileNotFound',
                'processing_time': processing_time
            }
    
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error during image conversion: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__,
            'processing_time': processing_time
        }

