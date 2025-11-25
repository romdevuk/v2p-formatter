import cv2
import numpy as np
from pathlib import Path
from PIL import Image
from config import DEFAULT_IMAGE_QUALITY, RESOLUTION_PRESETS

def get_video_info(video_path):
    """
    Extract video metadata (duration, resolution, fps)
    Returns dict with duration (seconds), width, height, fps
    """
    cap = cv2.VideoCapture(str(video_path))
    
    if not cap.isOpened():
        return None
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    cap.release()
    
    return {
        'duration': duration,
        'width': width,
        'height': height,
        'fps': fps,
        'frame_count': frame_count
    }

def extract_frame(video_path, time_point, output_path, quality=95, resolution=None):
    """
    Extract a single frame at specified time point
    
    Args:
        video_path: Path to video file
        time_point: Time in seconds
        output_path: Path to save the extracted frame
        quality: JPEG quality (1-100)
        resolution: Tuple (width, height) or None for original
    """
    cap = cv2.VideoCapture(str(video_path))
    
    if not cap.isOpened():
        return False
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_number = int(time_point * fps)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    
    if not ret:
        cap.release()
        return False
    
    # Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image
    pil_image = Image.fromarray(frame_rgb)
    
    # Resize if needed
    if resolution:
        pil_image = pil_image.resize(resolution, Image.Resampling.LANCZOS)
    
    # Save as JPEG
    pil_image.save(output_path, 'JPEG', quality=quality)
    
    cap.release()
    return True

def extract_frames_at_times(video_path, time_points, output_dir, quality=95, resolution=None):
    """
    Extract frames at multiple time points
    
    Args:
        video_path: Path to video file
        time_points: List of time points in seconds
        output_dir: Directory to save frames
        quality: JPEG quality (1-100)
        resolution: Tuple (width, height) or None for original
    
    Returns:
        List of paths to extracted images
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    extracted_images = []
    
    for idx, time_point in enumerate(time_points, start=1):
        output_path = output_dir / f"{idx}.jpg"
        
        if extract_frame(video_path, time_point, output_path, quality, resolution):
            extracted_images.append(str(output_path))
    
    return extracted_images

