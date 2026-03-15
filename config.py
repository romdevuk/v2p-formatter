import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Input and Output folders
INPUT_FOLDER = Path('/Users/rom/Documents/nvq/v2p-formatter-input')  # Source folder for MP4 files
OUTPUT_FOLDER = Path('/Users/rom/Documents/nvq/v2p-formatter-output')  # Output folder for generated files

# Upload configuration (legacy, not used with file selector)
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
MAX_CONTENT_LENGTH = None  # No limit
ALLOWED_EXTENSIONS = {'mp4'}

# Ensure output directory exists
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Image settings
DEFAULT_IMAGE_QUALITY = 95
DEFAULT_RESOLUTION = '640x480'
RESOLUTION_PRESETS = {
    'original': None,
    '1920x1080': (1920, 1080),
    '1280x720': (1280, 720),
    '640x480': (640, 480)
}

# PDF settings
DEFAULT_PDF_LAYOUT = 'grid'
DEFAULT_IMAGES_PER_PAGE = 4
PDF_PAGE_SIZE = 'A4'
PDF_GRID_OPTIONS = {
    '1x1': (1, 1),
    '2x2': (2, 2),
    '3x3': (3, 3),
    '4x4': (4, 4)
}

# Ensure upload directory exists
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Media Converter Settings
MEDIA_CONVERTER_INPUT_FOLDER = INPUT_FOLDER  # Same as main input
MEDIA_CONVERTER_OUTPUT_FOLDER = OUTPUT_FOLDER  # Same as main output

# Video Conversion Presets (optimized for file size reduction)
VIDEO_QUALITY_PRESETS = {
    'low': {
        'bitrate': '500k',
        'crf': 28,  # Higher CRF = smaller file, lower quality
        'scale': '1280:720',  # Downscale to reduce size
        'codec': 'libx264',
        'preset': 'fast'
    },
    'medium': {
        'bitrate': '1000k',
        'crf': 23,
        'scale': '1920:1080',  # Keep HD or downscale if larger
        'codec': 'libx264',
        'preset': 'medium'
    },
    'high': {
        'bitrate': '2000k',
        'crf': 18,
        'scale': None,  # Keep original resolution
        'codec': 'libx264',
        'preset': 'slow'
    }
}

# Image Conversion Presets
IMAGE_RESOLUTION_PRESETS = {
    'original': None,
    '1920x1080': (1920, 1080),
    '1280x720': (1280, 720),
    '640x480': (640, 480)
}

IMAGE_QUALITY_PRESETS = {
    'low': 60,      # Smaller file, lower quality
    'medium': 80,   # Balanced
    'high': 95      # Larger file, best quality
}

# Processing Settings
MAX_CONCURRENT_CONVERSIONS = 2  # Process 2 files in parallel
CONVERSION_TIMEOUT = 3600  # 1 hour timeout per file

# Deface video: timeout per video in seconds (env DEFACE_VIDEO_TIMEOUT overrides). Increase for very long videos.
DEFACE_VIDEO_TIMEOUT = int(os.environ.get('DEFACE_VIDEO_TIMEOUT', '600'))

# Deface video: max videos processed in parallel (1 = sequential; 2–4 = faster for batches; use with care on CPU/GPU).
DEFACE_MAX_CONCURRENT_VIDEOS = int(os.environ.get('DEFACE_MAX_CONCURRENT_VIDEOS', '1'))

# Deface: optional ONNX execution provider (e.g. CUDAExecutionProvider for Nvidia GPU). Empty = let deface auto-select.
DEFACE_EXECUTION_PROVIDER = (os.environ.get('DEFACE_EXECUTION_PROVIDER') or '').strip() or None

# Deface video: FFmpeg codec for output encoding. Default libx264; set to h264_nvenc for Nvidia GPU encoding (faster when available).
DEFACE_FFMPEG_CODEC = (os.environ.get('DEFACE_FFMPEG_CODEC') or 'libx264').strip()

# Debug Settings
DEBUG_MODE = True
DEBUG_LOG_LEVEL = 'DEBUG'
DEBUG_CONSOLE_OUTPUT = True
DEBUG_UI_PANEL = True

# AC Matrix Settings
AC_MATRIX_DATA_DIR = BASE_DIR / 'data' / 'ac_matrices'
AC_MATRIX_JSON_STANDARDS_DIR = BASE_DIR / 'data' / 'json_standards'
AC_MATRIX_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
AC_MATRIX_ALLOWED_EXTENSIONS = {'.json'}

# Ensure AC Matrix data directories exist
AC_MATRIX_DATA_DIR.mkdir(parents=True, exist_ok=True)
AC_MATRIX_JSON_STANDARDS_DIR.mkdir(parents=True, exist_ok=True)

