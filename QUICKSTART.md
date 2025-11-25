# Quick Start Guide

## Installation Steps

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure nginx (if not already done):**

Since nginx is running on port 80, you need to configure it to proxy requests to Flask. See `NGINX_SETUP.md` for detailed instructions.

Quick setup: Add this to your nginx server block:
```nginx
location /v2p-formatter {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    client_max_body_size 0;
}
```

Then test and reload nginx:
```bash
sudo nginx -t && sudo nginx -s reload
```

3. **Start the application:**

**Option 1: Use the start script (recommended)**
```bash
./start.sh
```

**Option 2: Manual start**
```bash
source venv/bin/activate
python run.py
```

The Flask app will run on port 5000, and nginx will proxy requests from port 80.

3. **Access the application:**
Once the server is running, open your browser and navigate to:
```
http://localhost/v2p-formatter
```

**Note**: If you haven't created a virtual environment yet:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. **Upload Video**: Click or drag an MP4 file to upload
2. **Preview Video**: The video will load and display its information
3. **Select Time Points**: Enter time points in one of these formats:
   - Single: `30`
   - Multiple: `10, 25, 45, 60`
   - Range: `10-20` (continuous)
4. **Preview Frames**: Click "Preview Frames" to see frames at selected times
5. **Configure Images**: Adjust quality (1-100) and resolution
6. **Configure PDF**: Choose layout (grid/custom) and images per page
7. **Extract Frames**: Click "Extract Frames" to save images
8. **Generate PDF**: Click "Generate PDF" to create PDF document

## Output

- **Images**: Saved in `{video_filename}_frames/` folder with names 1.jpg, 2.jpg, etc.
- **PDF**: Saved as `{video_filename}.pdf` in the same directory as the source video

## Troubleshooting

- **Module not found errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **Video won't upload**: Ensure the file is a valid MP4 format
- **Frames not extracting**: Check that time points are within the video duration
- **PDF not generating**: Ensure frames have been extracted first

