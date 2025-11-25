# File Output Location

## Input/Output Architecture

The application uses a clear separation between input and output:

- **Input Folder**: `/Users/rom/Documents/nvq/v2p-formatter-input` - Source folder for MP4 files (read-only)
- **Output Folder**: `/Users/rom/Documents/nvq/v2p-formatter-output` - All generated files saved here

## Where Files are Saved

All generated files (PDFs and images) are saved in the **Output Folder**, regardless of where the source video is located.

### Example:
- **Video file (input)**: `/Users/rom/Documents/nvq/v2p-formatter-input/css/L2 Cladding/eduards bormanis/mp4/IMG_7560.mp4`
- **PDF output**: `/Users/rom/Documents/nvq/v2p-formatter-output/IMG_7560.pdf`
- **Images output**: `/Users/rom/Documents/nvq/v2p-formatter-output/IMG_7560_frames/` containing `1.jpg`, `2.jpg`, `3.jpg`, etc.

### Naming Convention:
- The PDF filename is: `{video_filename_without_extension}.pdf`
- For example: `IMG_7560.mp4` → `IMG_7560.pdf`

### Image Output Location:
- Extracted images are saved in a subfolder: `{video_filename_without_extension}_frames/`
- For example: `IMG_7560.mp4` → `IMG_7560_frames/` folder containing `1.jpg`, `2.jpg`, etc.

## Output Folder Structure

```
/Users/rom/Documents/nvq/v2p-formatter-output/
├── IMG_7560.pdf
├── IMG_7560_frames/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── 3.jpg
├── intro.pdf
├── intro_frames/
│   ├── 1.jpg
│   └── 2.jpg
└── ...
```

## Finding Your Files

After generating files, you can:
1. **Download directly** from the web interface (download button appears after generation)
2. **Navigate to the output folder**: `/Users/rom/Documents/nvq/v2p-formatter-output`
3. **Use the file path** shown in the success message

## Benefits of This Approach

- **Clean separation**: Input files remain untouched
- **Centralized output**: All generated files in one location
- **Easy to find**: No need to search through video directories
- **Easy to clean**: Delete output folder to remove all generated files
- **No conflicts**: Won't overwrite existing files in video directories

