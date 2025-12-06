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

# Debug Settings
DEBUG_MODE = True
DEBUG_LOG_LEVEL = 'DEBUG'
DEBUG_CONSOLE_OUTPUT = True
DEBUG_UI_PANEL = True

