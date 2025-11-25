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

