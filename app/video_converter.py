"""
Video conversion module for converting MOV to MP4
"""
import subprocess
import logging
from pathlib import Path
from typing import Dict, Optional
import shutil

logger = logging.getLogger('media_converter.video_converter')


def check_ffmpeg_installed() -> bool:
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_video_info(video_path: Path) -> Dict:
    """
    Get video metadata using FFprobe
    
    Returns:
        Dict with duration, width, height, bitrate, codec, etc.
    """
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', str(video_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return {'error': 'Failed to get video info', 'stderr': result.stderr}
        
        import json
        data = json.loads(result.stdout)
        
        # Get video stream
        video_stream = next((s for s in data.get('streams', []) if s.get('codec_type') == 'video'), None)
        audio_stream = next((s for s in data.get('streams', []) if s.get('codec_type') == 'audio'), None)
        
        info = {
            'duration': float(data.get('format', {}).get('duration', 0)),
            'size': int(data.get('format', {}).get('size', 0)),
            'bitrate': int(data.get('format', {}).get('bit_rate', 0)),
        }
        
        if video_stream:
            info['width'] = int(video_stream.get('width', 0))
            info['height'] = int(video_stream.get('height', 0))
            info['codec'] = video_stream.get('codec_name', 'unknown')
            # Calculate FPS from frame rate string (e.g., "30/1" = 30.0)
            fps_str = video_stream.get('r_frame_rate', '0/1')
            try:
                if '/' in fps_str:
                    num, den = map(float, fps_str.split('/'))
                    info['fps'] = num / den if den > 0 else 0
                else:
                    info['fps'] = float(fps_str)
            except (ValueError, ZeroDivisionError):
                info['fps'] = 0
        
        if audio_stream:
            info['audio_codec'] = audio_stream.get('codec_name', 'unknown')
            info['audio_bitrate'] = int(audio_stream.get('bit_rate', 0))
        
        return info
    except Exception as e:
        logger.error(f"Error getting video info: {e}", exc_info=True)
        return {'error': str(e)}


def convert_mov_to_mp4(
    input_path: Path,
    output_path: Path,
    quality_preset: str = 'medium',
    custom_settings: Optional[Dict] = None
) -> Dict:
    """
    Convert MOV to MP4 using FFmpeg
    
    Args:
        input_path: Path to input MOV file
        output_path: Path to output MP4 file
        quality_preset: 'low', 'medium', or 'high'
        custom_settings: Optional dict with custom settings (bitrate, crf, scale, etc.)
    
    Returns:
        Dict with success status, output_size, processing_time, etc.
    """
    import time
    start_time = time.time()
    
    # Check FFmpeg is installed
    if not check_ffmpeg_installed():
        return {
            'success': False,
            'error': 'FFmpeg is not installed. Please install FFmpeg to convert videos.',
            'error_type': 'FFmpegNotFound'
        }
    
    # Validate input file
    if not input_path.exists():
        return {
            'success': False,
            'error': f'Input file not found: {input_path}',
            'error_type': 'FileNotFound'
        }
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get preset settings
    from config import VIDEO_QUALITY_PRESETS
    
    if custom_settings:
        settings = custom_settings
    else:
        settings = VIDEO_QUALITY_PRESETS.get(quality_preset, VIDEO_QUALITY_PRESETS['medium'])
    
    # Build FFmpeg command
    cmd = ['ffmpeg', '-i', str(input_path), '-y']  # -y to overwrite
    
    # Video codec
    cmd.extend(['-c:v', settings.get('codec', 'libx264')])
    
    # Bitrate
    if 'bitrate' in settings:
        cmd.extend(['-b:v', settings['bitrate']])
    
    # CRF (Constant Rate Factor)
    if 'crf' in settings:
        cmd.extend(['-crf', str(settings['crf'])])
    
    # Preset
    if 'preset' in settings:
        cmd.extend(['-preset', settings['preset']])
    
    # Scale (if specified) - preserve aspect ratio
    if settings.get('scale'):
        # Use force_original_aspect_ratio=decrease to maintain aspect ratio
        # This ensures vertical videos aren't squeezed
        scale_filter = f"scale={settings['scale']}:force_original_aspect_ratio=decrease"
        cmd.extend(['-vf', scale_filter])
    
    # Audio codec (preserve audio)
    cmd.extend(['-c:a', 'aac', '-b:a', '128k'])
    
    # Output file
    cmd.append(str(output_path))
    
    # Log command
    logger.debug(f"FFmpeg command: {' '.join(cmd)}")
    
    try:
        # Run FFmpeg
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        processing_time = time.time() - start_time
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or 'Unknown FFmpeg error'
            logger.error(f"FFmpeg conversion failed: {error_msg}")
            return {
                'success': False,
                'error': f'FFmpeg conversion failed: {error_msg}',
                'error_type': 'FFmpegError',
                'ffmpeg_stderr': result.stderr,
                'ffmpeg_stdout': result.stdout,
                'processing_time': processing_time
            }
        
        # Get output file size
        if output_path.exists():
            output_size = output_path.stat().st_size
            input_size = input_path.stat().st_size
            reduction_percent = round((1 - output_size / input_size) * 100, 2) if input_size > 0 else 0
            
            logger.info(f"Conversion successful: {input_path.name} -> {output_path.name} "
                       f"({input_size / (1024*1024):.2f}MB -> {output_size / (1024*1024):.2f}MB, "
                       f"{reduction_percent}% reduction)")
            
            return {
                'success': True,
                'output_path': str(output_path),
                'output_size': output_size,
                'output_size_mb': round(output_size / (1024 * 1024), 2),
                'input_size': input_size,
                'input_size_mb': round(input_size / (1024 * 1024), 2),
                'reduction_percent': reduction_percent,
                'processing_time': round(processing_time, 2)
            }
        else:
            return {
                'success': False,
                'error': 'Output file was not created',
                'error_type': 'OutputFileNotFound',
                'processing_time': processing_time
            }
    
    except subprocess.TimeoutExpired:
        processing_time = time.time() - start_time
        logger.error(f"FFmpeg conversion timed out after {processing_time:.2f} seconds")
        return {
            'success': False,
            'error': 'Conversion timed out (exceeded 1 hour)',
            'error_type': 'Timeout',
            'processing_time': processing_time
        }
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error during conversion: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__,
            'processing_time': processing_time
        }


def trim_video(
    input_path: Path,
    output_path: Path,
    start_time: float,
    end_time: float,
    quality_preset: str = 'medium',
    custom_settings: Optional[Dict] = None
) -> Dict:
    """
    Trim video to specified time range using FFmpeg
    
    Args:
        input_path: Path to input video file
        output_path: Path to output video file
        start_time: Start time in seconds
        end_time: End time in seconds
        quality_preset: 'low', 'medium', or 'high'
        custom_settings: Optional dict with custom settings
    
    Returns:
        Dict with success status, output_size, processing_time, etc.
    """
    import time
    start_time_processing = time.time()
    
    # Check FFmpeg is installed
    if not check_ffmpeg_installed():
        return {
            'success': False,
            'error': 'FFmpeg is not installed. Please install FFmpeg to trim videos.',
            'error_type': 'FFmpegNotFound'
        }
    
    # Validate input file
    if not input_path.exists():
        return {
            'success': False,
            'error': f'Input file not found: {input_path}',
            'error_type': 'FileNotFound'
        }
    
    # Validate time range
    if start_time < 0:
        return {
            'success': False,
            'error': 'Start time must be >= 0',
            'error_type': 'InvalidTimeRange'
        }
    
    if end_time <= start_time:
        return {
            'success': False,
            'error': 'End time must be greater than start time',
            'error_type': 'InvalidTimeRange'
        }
    
    # Get video info to validate duration
    video_info = get_video_info(input_path)
    if 'error' in video_info:
        return {
            'success': False,
            'error': f'Failed to get video info: {video_info["error"]}',
            'error_type': 'VideoInfoError'
        }
    
    duration = video_info.get('duration', 0)
    if end_time > duration:
        logger.warning(f"End time {end_time}s exceeds video duration {duration}s, clamping to duration")
        end_time = duration
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get preset settings
    from config import VIDEO_QUALITY_PRESETS
    
    if custom_settings:
        settings = custom_settings
    else:
        settings = VIDEO_QUALITY_PRESETS.get(quality_preset, VIDEO_QUALITY_PRESETS['medium'])
    
    # Calculate duration
    duration_seconds = end_time - start_time
    
    # Build FFmpeg command
    cmd = ['ffmpeg', '-i', str(input_path), '-y']  # -y to overwrite
    
    # Trim: use -ss (start) and -t (duration) for accurate trimming
    cmd.extend(['-ss', str(start_time)])
    cmd.extend(['-t', str(duration_seconds)])
    
    # Video codec
    cmd.extend(['-c:v', settings.get('codec', 'libx264')])
    
    # Bitrate
    if 'bitrate' in settings:
        cmd.extend(['-b:v', settings['bitrate']])
    
    # CRF (Constant Rate Factor)
    if 'crf' in settings:
        cmd.extend(['-crf', str(settings['crf'])])
    
    # Preset
    if 'preset' in settings:
        cmd.extend(['-preset', settings['preset']])
    
    # Scale (if specified) - preserve aspect ratio
    if settings.get('scale'):
        scale_filter = f"scale={settings['scale']}:force_original_aspect_ratio=decrease"
        cmd.extend(['-vf', scale_filter])
    
    # Audio codec (preserve audio)
    cmd.extend(['-c:a', 'aac', '-b:a', '128k'])
    
    # Avoid re-encoding if possible (copy codec for faster processing)
    # But we'll re-encode to ensure compatibility
    
    # Output file
    cmd.append(str(output_path))
    
    # Log command
    logger.debug(f"FFmpeg trim command: {' '.join(cmd)}")
    
    try:
        # Run FFmpeg
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        processing_time = time.time() - start_time_processing
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or 'Unknown FFmpeg error'
            logger.error(f"FFmpeg trim failed: {error_msg}")
            return {
                'success': False,
                'error': f'FFmpeg trim failed: {error_msg}',
                'error_type': 'FFmpegError',
                'ffmpeg_stderr': result.stderr,
                'ffmpeg_stdout': result.stdout,
                'processing_time': processing_time
            }
        
        # Get output file size
        if output_path.exists():
            output_size = output_path.stat().st_size
            input_size = input_path.stat().st_size
            reduction_percent = round((1 - output_size / input_size) * 100, 2) if input_size > 0 else 0
            
            logger.info(f"Trim successful: {input_path.name} -> {output_path.name} "
                       f"({start_time}s-{end_time}s, {input_size / (1024*1024):.2f}MB -> {output_size / (1024*1024):.2f}MB)")
            
            return {
                'success': True,
                'output_path': str(output_path),
                'output_size': output_size,
                'output_size_mb': round(output_size / (1024 * 1024), 2),
                'input_size': input_size,
                'input_size_mb': round(input_size / (1024 * 1024), 2),
                'reduction_percent': reduction_percent,
                'processing_time': round(processing_time, 2),
                'trimmed_duration': duration_seconds
            }
        else:
            return {
                'success': False,
                'error': 'Output file was not created',
                'error_type': 'OutputFileNotFound',
                'processing_time': processing_time
            }
    
    except subprocess.TimeoutExpired:
        processing_time = time.time() - start_time_processing
        logger.error(f"FFmpeg trim timed out after {processing_time:.2f} seconds")
        return {
            'success': False,
            'error': 'Trim timed out (exceeded 1 hour)',
            'error_type': 'Timeout',
            'processing_time': processing_time
        }
    except Exception as e:
        processing_time = time.time() - start_time_processing
        logger.error(f"Error during trim: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__,
            'processing_time': processing_time
        }


def crop_video(
    input_path: Path,
    output_path: Path,
    x: int,
    y: int,
    width: int,
    height: int,
    quality_preset: str = 'medium',
    custom_settings: Optional[Dict] = None
) -> Dict:
    """
    Crop video to specified region using FFmpeg
    
    Args:
        input_path: Path to input video file
        output_path: Path to output video file
        x: X coordinate of crop start (left edge)
        y: Y coordinate of crop start (top edge)
        width: Crop width in pixels
        height: Crop height in pixels
        quality_preset: 'low', 'medium', or 'high'
        custom_settings: Optional dict with custom settings
    
    Returns:
        Dict with success status, output_size, processing_time, etc.
    """
    import time
    start_time_processing = time.time()
    
    # Check FFmpeg is installed
    if not check_ffmpeg_installed():
        return {
            'success': False,
            'error': 'FFmpeg is not installed. Please install FFmpeg to crop videos.',
            'error_type': 'FFmpegNotFound'
        }
    
    # Validate input file
    if not input_path.exists():
        return {
            'success': False,
            'error': f'Input file not found: {input_path}',
            'error_type': 'FileNotFound'
        }
    
    # Validate crop parameters
    if width <= 0 or height <= 0:
        return {
            'success': False,
            'error': 'Crop width and height must be > 0',
            'error_type': 'InvalidCropParams'
        }
    
    if x < 0 or y < 0:
        return {
            'success': False,
            'error': 'Crop coordinates must be >= 0',
            'error_type': 'InvalidCropParams'
        }
    
    # Get video info to validate dimensions
    video_info = get_video_info(input_path)
    if 'error' in video_info:
        return {
            'success': False,
            'error': f'Failed to get video info: {video_info["error"]}',
            'error_type': 'VideoInfoError'
        }
    
    video_width = video_info.get('width', 0)
    video_height = video_info.get('height', 0)
    
    if x + width > video_width:
        return {
            'success': False,
            'error': f'Crop region exceeds video width ({video_width}px)',
            'error_type': 'InvalidCropParams'
        }
    
    if y + height > video_height:
        return {
            'success': False,
            'error': f'Crop region exceeds video height ({video_height}px)',
            'error_type': 'InvalidCropParams'
        }
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get preset settings
    from config import VIDEO_QUALITY_PRESETS
    
    if custom_settings:
        settings = custom_settings
    else:
        settings = VIDEO_QUALITY_PRESETS.get(quality_preset, VIDEO_QUALITY_PRESETS['medium'])
    
    # Build FFmpeg command
    cmd = ['ffmpeg', '-i', str(input_path), '-y']  # -y to overwrite
    
    # Crop filter: crop=width:height:x:y
    crop_filter = f"crop={width}:{height}:{x}:{y}"
    
    # Combine with scale filter if needed
    filters = [crop_filter]
    if settings.get('scale'):
        scale_filter = f"scale={settings['scale']}:force_original_aspect_ratio=decrease"
        filters.append(scale_filter)
    
    # Apply video filters
    if filters:
        cmd.extend(['-vf', ','.join(filters)])
    
    # Video codec
    cmd.extend(['-c:v', settings.get('codec', 'libx264')])
    
    # Bitrate
    if 'bitrate' in settings:
        cmd.extend(['-b:v', settings['bitrate']])
    
    # CRF (Constant Rate Factor)
    if 'crf' in settings:
        cmd.extend(['-crf', str(settings['crf'])])
    
    # Preset
    if 'preset' in settings:
        cmd.extend(['-preset', settings['preset']])
    
    # Audio codec (preserve audio)
    cmd.extend(['-c:a', 'aac', '-b:a', '128k'])
    
    # Output file
    cmd.append(str(output_path))
    
    # Log command
    logger.debug(f"FFmpeg crop command: {crop_filter}")
    
    try:
        # Run FFmpeg
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        processing_time = time.time() - start_time_processing
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or 'Unknown FFmpeg error'
            logger.error(f"FFmpeg crop failed: {error_msg}")
            return {
                'success': False,
                'error': f'FFmpeg crop failed: {error_msg}',
                'error_type': 'FFmpegError',
                'ffmpeg_stderr': result.stderr,
                'ffmpeg_stdout': result.stdout,
                'processing_time': processing_time
            }
        
        # Get output file size
        if output_path.exists():
            output_size = output_path.stat().st_size
            input_size = input_path.stat().st_size
            reduction_percent = round((1 - output_size / input_size) * 100, 2) if input_size > 0 else 0
            
            logger.info(f"Crop successful: {input_path.name} -> {output_path.name} "
                       f"({width}x{height} @ {x},{y}, {input_size / (1024*1024):.2f}MB -> {output_size / (1024*1024):.2f}MB)")
            
            return {
                'success': True,
                'output_path': str(output_path),
                'output_size': output_size,
                'output_size_mb': round(output_size / (1024 * 1024), 2),
                'input_size': input_size,
                'input_size_mb': round(input_size / (1024 * 1024), 2),
                'reduction_percent': reduction_percent,
                'processing_time': round(processing_time, 2),
                'crop_width': width,
                'crop_height': height
            }
        else:
            return {
                'success': False,
                'error': 'Output file was not created',
                'error_type': 'OutputFileNotFound',
                'processing_time': processing_time
            }
    
    except subprocess.TimeoutExpired:
        processing_time = time.time() - start_time_processing
        logger.error(f"FFmpeg crop timed out after {processing_time:.2f} seconds")
        return {
            'success': False,
            'error': 'Crop timed out (exceeded 1 hour)',
            'error_type': 'Timeout',
            'processing_time': processing_time
        }
    except Exception as e:
        processing_time = time.time() - start_time_processing
        logger.error(f"Error during crop: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__,
            'processing_time': processing_time
        }

