# Video to Image Formatter

A web-based application that converts MP4 video files to JPEG image sequences and generates PDF documents containing those images.

## Features

- Upload MP4 videos
- Select specific time points to extract frames
- Preview frames before extraction
- Configure image quality and resolution
- Generate PDFs with configurable layouts (grid or custom)
- Save images and PDFs in organized folders

## Installation

1. Clone or navigate to the project directory:
```bash
cd v2p-formatter
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:

**Using the start script (recommended):**
```bash
./start.sh
```

**Or manually:**
```bash
source venv/bin/activate
sudo python run.py
```

**Important**: Port 80 requires administrator privileges (sudo). You will be prompted for your password.

2. Open your browser and navigate to:
```
http://localhost/v2p-formatter
```

**Note**: If you see a 404 error, make sure the Flask application is running. Check the terminal for any error messages.

**Note**: Running on port 80 requires administrator privileges. You may need to run with `sudo`:
```bash
sudo python run.py
```

Alternatively, you can use a reverse proxy (like nginx) to forward requests from port 80 to the Flask app running on a different port.

3. Follow the steps:
   - Upload an MP4 video file
   - Preview the video
   - Enter time points (e.g., `10, 25, 45, 60` or `10-20`)
   - Preview frames at selected times
   - Configure image quality and resolution
   - Configure PDF layout
   - Extract frames
   - Generate PDF

## Time Point Formats

- **Single**: `30` (extract frame at 30 seconds)
- **Multiple**: `10, 25, 45, 60` (comma-separated)
- **Range**: `10-20` (continuous range from 10 to 20 seconds)

## Output

- **Images**: Saved in a folder named `{video_filename}_frames/` with sequential naming (1.jpg, 2.jpg, ...)
- **PDF**: Saved as `{video_filename}.pdf` in the same directory as the source video

## Project Structure

```
v2p-formatter/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── routes.py            # Route handlers
│   ├── video_processor.py  # Video to image conversion
│   ├── pdf_generator.py     # PDF creation
│   ├── image_editor.py     # Image editing utilities
│   └── utils.py            # Helper functions
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   ├── video-handler.js
│   │   ├── timeline.js
│   │   └── image-preview.js
│   └── uploads/            # Temporary upload storage
├── templates/
│   ├── base.html
│   └── index.html
├── config.py               # Configuration settings
├── requirements.txt
└── README.md
```

## Dependencies

- Flask 2.3.0
- opencv-python 4.8.0.74
- Pillow 10.0.0
- reportlab 4.0.4
- numpy 1.24.3

## Configuration

Edit `config.py` to customize:
- Image quality defaults
- Resolution presets
- PDF layout options
- Upload folder location

## Testing

The project includes Selenium-based end-to-end tests. See `tests/README.md` for detailed testing documentation.

### Quick Test Run

```bash
# Make sure Flask app is running first
source venv/bin/activate
python run.py

# In another terminal, run tests
cd tests
./run_tests.sh
```

### Run Tests in Headless Mode

```bash
HEADLESS=true pytest tests/
```

## Notes

- The application processes videos synchronously for stability
- Original video files are preserved
- Output files are saved in the same directory as the source video
- No file size limits (configurable in config.py)

## License

MIT License

