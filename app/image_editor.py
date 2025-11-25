from PIL import Image
from pathlib import Path

def crop_image(image_path, x, y, width, height, output_path=None):
    """
    Crop an image
    
    Args:
        image_path: Path to source image
        x, y: Top-left corner coordinates
        width, height: Crop dimensions
        output_path: Path to save cropped image (overwrites original if None)
    """
    img = Image.open(image_path)
    cropped = img.crop((x, y, x + width, y + height))
    
    output = output_path if output_path else image_path
    cropped.save(output, 'JPEG', quality=95)
    return str(output)

def resize_image(image_path, width, height, maintain_aspect=True, output_path=None):
    """
    Resize an image
    
    Args:
        image_path: Path to source image
        width, height: Target dimensions
        maintain_aspect: If True, maintain aspect ratio
        output_path: Path to save resized image (overwrites original if None)
    """
    img = Image.open(image_path)
    
    if maintain_aspect:
        img.thumbnail((width, height), Image.Resampling.LANCZOS)
    else:
        img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    output = output_path if output_path else image_path
    img.save(output, 'JPEG', quality=95)
    return str(output)

def apply_filter(image_path, filter_type, output_path=None):
    """
    Apply a filter to an image
    
    Args:
        image_path: Path to source image
        filter_type: Filter name ('blur', 'sharpen', 'edge_enhance', 'emboss')
        output_path: Path to save filtered image (overwrites original if None)
    """
    from PIL import ImageFilter
    
    img = Image.open(image_path)
    
    filter_map = {
        'blur': ImageFilter.BLUR,
        'sharpen': ImageFilter.SHARPEN,
        'edge_enhance': ImageFilter.EDGE_ENHANCE,
        'emboss': ImageFilter.EMBOSS,
    }
    
    if filter_type in filter_map:
        img = img.filter(filter_map[filter_type])
    
    output = output_path if output_path else image_path
    img.save(output, 'JPEG', quality=95)
    return str(output)

def adjust_quality(image_path, quality, output_path=None):
    """
    Adjust JPEG quality of an image
    
    Args:
        image_path: Path to source image
        quality: JPEG quality (1-100)
        output_path: Path to save image (overwrites original if None)
    """
    img = Image.open(image_path)
    output = output_path if output_path else image_path
    img.save(output, 'JPEG', quality=quality)
    return str(output)

