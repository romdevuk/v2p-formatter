# Video to Image Formatter - Specification Questions

## Technical Stack & Architecture

1. **Technology Stack Preference**
   - What technology stack would you prefer? (e.g., Python with Flask/FastAPI, Node.js with Express, React frontend, etc.)
   user python and flask; no api needed;
   - Should this be a web application, desktop application, or CLI tool?
   web app; browser based localhost/v2p-formatter
   - Do you have any existing infrastructure or preferences we should align with? -  n/a

2. **Deployment Environment**
   - Where will this application be deployed? (Local, cloud, on-premise)
   localhost/v2p-formatter
   - What are the expected usage patterns? (Single user, multiple users, concurrent processing)
   single user;

## User Interface & Experience

3. **Time Frame Selection Method**
   - How should users pick time frames? (e.g., start/end time inputs, visual timeline scrubber, click-to-select frames)
   = provide text interface examples to choose from;
   - Should users be able to preview frames before selecting them?
   =yes;
   - Can users select multiple non-contiguous time ranges, or only one range at a time?
   =only continues;
   - What time format should be used? (e.g., seconds, MM:SS, HH:MM:SS)
   =seconds;

4. **Video Upload & Processing**
   - What is the maximum video file size we should support?
   =any
   - Should there be progress indicators during video processing?
   =yes;
   - Should the application support video preview before processing?
   =yes
   - Do we need to support multiple video formats, or is MP4 the only requirement?
   mp4 only;

## Image Output Settings

5. **Image Quality & Format**
   - What image quality/resolution should be used? (e.g., original video resolution, specific dimensions, quality percentage)
   provide the option to choose from;
   - Should users be able to configure image quality settings?
   -yes'
   - Is JPG the only format needed, or should we support PNG, WebP, etc.?
   jpeg only;
   - What should be the naming convention for images? (e.g., `1.jpg`, `image_1.jpg`, `frame_001.jpg`)
   use 1,2,3;

6. **Frame Extraction**
   - How should frames be extracted? (e.g., one frame per second, specific intervals, only at selected time points)
   selected time points;
   - If a user selects a time range (e.g., 10:00-10:05), should we extract:
     =no need;
     - All frames in that range?
     - One frame per second?
     - Only frames at specific intervals?
     - Only the start and end frames?
    

## PDF Generation

7. **PDF Configuration**
   - What should be the PDF layout? (e.g., one image per page, multiple images per page in a grid)
   provide options(grid, x images per page )
   - What page size should be used? (A4, Letter, custom)
   =    A4;
   - Should images be scaled to fit the page, or maintain aspect ratio?
   =aspect radio;
   - Should there be any headers, footers, or captions in the PDF?
   no;
   - What should be the PDF filename? (e.g., based on video name, timestamp, custom); follow mp4 filename;

## File Management

8. **Output Organization**
   - Where should output folders be created? (Same directory as video, user-specified location, default downloads folder)
   the same directory;
   - Should the folder name be based on the video filename, timestamp, or user-defined? video filename;
   - Should we preserve the original video file, or can it be deleted after processing? preserve it;
   - Do we need to handle cleanup of temporary files? no need;

## Error Handling & Validation

9. **Error Scenarios**
   - How should we handle invalid video files? debugging report;
   - What should happen if the selected time range is outside the video duration? it cant happen;
   - How should we handle processing failures or interruptions? debugging;
   - Should there be validation for file types before upload? yes;

## Performance & Scalability

10. **Processing Requirements**
    - Are there any performance requirements? (e.g., processing time limits, memory constraints) no need;
    - Should processing happen synchronously or asynchronously? choose the most stable one;
    - Do we need to support batch processing of multiple videos? no need;

## Additional Features

11. **Optional Features**
    - Should users be able to download individual images or only the full set? the images will be saved in the PDF file;
    - Do we need a history/log of processed videos? no need;
    - Should there be any image editing capabilities? (e.g., crop, resize, filters) = yes;
    - Do we need user authentication or is this a single-user tool? no need;

---

replied all questions;
the core architecture should be flexible for further expansion/customisation;
use MVP approach;
create new file final-spec.md with final tech implementation details;
Please answer these questions so we can create a comprehensive technical specification document.

