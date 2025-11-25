// Video upload and preview handling

// Get elements (will be initialized in initVideoHandler)
let videoInput, uploadArea, videoPlayer, videoInfoDiv;

// Initialize when DOM is ready
function initVideoHandler() {
    debugOutput('=== Initializing video handler ===', 'info');
    
    const videoInput = document.getElementById('videoInput');
    const uploadArea = document.getElementById('uploadArea');
    
    if (!videoInput) {
        debugOutput('❌ ERROR: videoInput element not found!', 'error');
        console.error('videoInput element not found');
        return;
    } else {
        debugOutput('✅ videoInput element found', 'success');
    }
    
    if (!uploadArea) {
        debugOutput('❌ ERROR: uploadArea element not found!', 'error');
        console.error('uploadArea element not found');
        return;
    } else {
        debugOutput('✅ uploadArea element found', 'success');
    }
    
    // File input change - use multiple methods to ensure it works
    debugOutput('Attaching file input change listener...', 'info');
    
    // Method 1: addEventListener
    videoInput.addEventListener('change', function(e) {
        debugOutput('📁 File input CHANGE event fired!', 'success');
        console.log('🔄 File input changed');
        console.log('   Files count:', e.target.files.length);
        console.log('   Event type:', e.type);
        
        if (e.target.files && e.target.files.length > 0) {
            const file = e.target.files[0];
            debugOutput(`📄 File selected: ${file.name}`, 'success');
            debugOutput(`   Size: ${(file.size / 1024 / 1024).toFixed(2)} MB`, 'info');
            debugOutput(`   Type: ${file.type}`, 'info');
            console.log('   Selected file:', file.name);
            handleFileSelect(file);
        } else {
            debugOutput('⚠️ No file in files array', 'error');
            console.warn('⚠️  No file selected');
        }
    });
    
    // Method 2: Also add onchange as backup
    videoInput.onchange = function(e) {
        debugOutput('📁 File input ONCHANGE fired!', 'success');
        if (this.files && this.files.length > 0) {
            handleFileSelect(this.files[0]);
        }
    };
    
    debugOutput('✅ File input change listeners attached (both addEventListener and onchange)', 'success');
    
    // Test if we can access the input
    try {
        debugOutput(`File input accept attribute: ${videoInput.accept}`, 'info');
        debugOutput(`File input type: ${videoInput.type}`, 'info');
    } catch (err) {
        debugOutput(`Error accessing input: ${err.message}`, 'error');
    }
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
        debugOutput('File dragged over upload area', 'info');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        console.log('📦 File dropped');
        debugOutput('File dropped on upload area', 'info');
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        console.log('   Dropped files count:', files.length);
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
    debugOutput('Drag and drop listeners attached', 'success');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initVideoHandler);
} else {
    initVideoHandler();
}

function handleFileSelect(file) {
    debugOutput(`=== FILE SELECTED: ${file.name} ===`, 'success');
    console.log('📁 File selected:', file.name, 'Size:', file.size, 'Type:', file.type);
    
    // Get elements
    videoPlayer = document.getElementById('videoPlayer');
    videoInfoDiv = document.getElementById('videoInfo');
    
    if (!videoPlayer) {
        debugOutput('❌ ERROR: videoPlayer element not found!', 'error');
    }
    if (!videoInfoDiv) {
        debugOutput('❌ ERROR: videoInfoDiv element not found!', 'error');
    }
    
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.mp4')) {
        debugOutput(`❌ Invalid file type: ${file.name} (must be .mp4)`, 'error');
        console.error('❌ Invalid file type:', file.name);
        showStatus('Please select an MP4 file', 'error');
        return;
    }
    
    debugOutput('✅ File type validated', 'success');
    debugOutput('📤 Starting upload...', 'info');
    console.log('✅ File type validated, starting upload...');
    showStatus('Uploading video...', 'success');
    
    const formData = new FormData();
    formData.append('video', file);
    
    const fileSizeMB = (file.size / 1024 / 1024).toFixed(2);
    debugOutput(`📤 Sending upload request (${fileSizeMB} MB)`, 'info');
    debugOutput(`   URL: /v2p-formatter/upload`, 'info');
    console.log('📤 Sending upload request to /v2p-formatter/upload');
    console.log('   File size:', file.size, 'bytes');
    console.log('   File type:', file.type);
    
    // Show progress
    showStatus('Uploading video... Please wait...', 'success');
    
    fetch('/v2p-formatter/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        debugOutput(`📥 Response received: ${response.status} ${response.statusText}`, response.ok ? 'success' : 'error');
        console.log('📥 Response received:', response.status, response.statusText);
        console.log('   Response headers:', Object.fromEntries(response.headers.entries()));
        
        if (!response.ok) {
            debugOutput(`❌ Upload failed: ${response.status} ${response.statusText}`, 'error');
            console.error('❌ Response not OK:', response.status, response.statusText);
            return response.text().then(text => {
                debugOutput(`❌ Error details: ${text.substring(0, 200)}`, 'error');
                console.error('   Response body:', text);
                showStatus(`Upload failed: ${response.status} ${response.statusText}`, 'error');
                throw new Error(`Upload failed: ${response.status} ${response.statusText}`);
            });
        }
        
        debugOutput('✅ Response OK, parsing JSON...', 'info');
        return response.json();
    })
    .then(data => {
        debugOutput('📊 Response data received', 'info');
        console.log('📊 Response data:', data);
        
        if (data.success) {
            debugOutput('✅✅✅ UPLOAD SUCCESSFUL! ✅✅✅', 'success');
            console.log('✅ Upload successful!');
            console.log('   Video path:', data.filepath);
            console.log('   Duration:', data.duration, 's');
            console.log('   Resolution:', data.width + 'x' + data.height);
            
            appState.videoFile = file;
            appState.videoPath = data.filepath;
            appState.videoInfo = data;
            
            debugOutput(`Video duration: ${data.duration}s`, 'info');
            debugOutput(`Resolution: ${data.width}x${data.height}`, 'info');
            
            // Show video preview
            debugOutput('🎬 Setting up video preview...', 'info');
            console.log('🎬 Setting up video preview...');
            const videoURL = URL.createObjectURL(file);
            console.log('   Video URL:', videoURL);
            
            if (videoPlayer) {
                videoPlayer.src = videoURL;
                debugOutput('✅ Video player source set', 'success');
            } else {
                debugOutput('❌ Video player element not found!', 'error');
            }
            
            displayVideoInfo(data);
            debugOutput('✅ Video info displayed', 'success');
            
            showStatus('Video uploaded successfully!', 'success');
            
            debugOutput('👁️  Showing all sections...', 'info');
            console.log('👁️  Showing sections...');
            showSection('previewSection');
            showSection('timeSection');
            showSection('configSection');
            showSection('pdfSection');
            showSection('processingSection');
            
            debugOutput('✅✅✅ ALL SECTIONS SHOWN - READY TO USE! ✅✅✅', 'success');
            console.log('✅ All sections shown');
        } else {
            debugOutput(`❌ Upload failed: ${data.error || 'Unknown error'}`, 'error');
            console.error('❌ Upload failed:', data.error);
            showStatus(data.error || 'Upload failed', 'error');
        }
    })
    .catch(error => {
        debugOutput(`❌❌❌ UPLOAD ERROR ❌❌❌`, 'error');
        debugOutput(`Error: ${error.message}`, 'error');
        debugOutput(`Type: ${error.name}`, 'error');
        console.error('❌ Upload error:', error);
        console.error('   Error name:', error.name);
        console.error('   Error message:', error.message);
        console.error('   Error stack:', error.stack);
        showStatus('Upload failed: ' + error.message, 'error');
    });
}

function displayVideoInfo(info) {
    videoInfoDiv.innerHTML = `
        <div class="video-info-item">
            <strong>Duration</strong>
            <span>${info.duration.toFixed(2)}s</span>
        </div>
        <div class="video-info-item">
            <strong>Resolution</strong>
            <span>${info.width}x${info.height}</span>
        </div>
        <div class="video-info-item">
            <strong>FPS</strong>
            <span>${info.fps.toFixed(2)}</span>
        </div>
        <div class="video-info-item">
            <strong>Filename</strong>
            <span>${info.filename}</span>
        </div>
    `;
}

// Quality slider update
const qualitySlider = document.getElementById('qualitySlider');
const qualityValue = document.getElementById('qualityValue');

if (qualitySlider) {
    qualitySlider.addEventListener('input', (e) => {
        qualityValue.textContent = e.target.value;
    });
}

// Extract frames button
const extractFramesBtn = document.getElementById('extractFramesBtn');
if (extractFramesBtn) {
    extractFramesBtn.addEventListener('click', extractFrames);
}

function extractFrames() {
    // Get time points from selected time points
    let timePoints = '';
    if (typeof getTimePointsString === 'function') {
        timePoints = getTimePointsString();
    } else if (typeof selectedTimePoints !== 'undefined' && selectedTimePoints.length > 0) {
        timePoints = selectedTimePoints.join(', ');
    }
    
    if (!timePoints || timePoints.trim() === '') {
        showStatus('Please select at least one time point from the video', 'error');
        return;
    }
    
    if (!appState.videoPath) {
        showStatus('Please select a video first', 'error');
        return;
    }
    
    const quality = parseInt(document.getElementById('qualitySlider').value);
    const resolution = document.getElementById('resolutionSelect').value;
    
    showProgress(0, 'Extracting frames...');
    
    fetch('/v2p-formatter/extract_frames', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            video_path: appState.videoPath,
            time_points: timePoints,
            quality: quality,
            resolution: resolution
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            appState.extractedImages = data.images;
            showProgress(100, 'Frames extracted successfully!');
            
            setTimeout(() => {
                hideProgress();
                showResults(
                    `Successfully extracted ${data.count} frames`,
                    'success',
                    [{ url: data.output_dir, text: 'View output folder' }]
                );
                document.getElementById('generatePdfBtn').style.display = 'block';
            }, 1000);
        } else {
            hideProgress();
            showResults(data.error || 'Failed to extract frames', 'error');
        }
    })
    .catch(error => {
        hideProgress();
        console.error('Extraction error:', error);
        showResults('Failed to extract frames: ' + error.message, 'error');
    });
}

// Generate PDF button
const generatePdfBtn = document.getElementById('generatePdfBtn');
if (generatePdfBtn) {
    generatePdfBtn.addEventListener('click', generatePDF);
}

function generatePDF() {
    if (!appState.extractedImages || appState.extractedImages.length === 0) {
        showStatus('Please extract frames first', 'error');
        return;
    }
    
    const layout = document.getElementById('layoutSelect').value;
    const imagesPerPage = parseInt(document.getElementById('imagesPerPage').value);
    
    showProgress(0, 'Generating PDF...');
    
    fetch('/v2p-formatter/generate_pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            video_path: appState.videoPath,
            image_paths: appState.extractedImages,
            layout: layout,
            images_per_page: imagesPerPage
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            appState.pdfPath = data.pdf_path;
            showProgress(100, 'PDF generated successfully!');
            
            setTimeout(() => {
                hideProgress();
                showResults(
                    'PDF generated successfully!',
                    'success',
                    [{ url: `/v2p-formatter/download?path=${encodeURIComponent(data.pdf_path)}`, text: `Download ${data.filename}` }]
                );
            }, 1000);
        } else {
            hideProgress();
            showResults(data.error || 'Failed to generate PDF', 'error');
        }
    })
    .catch(error => {
        hideProgress();
        console.error('PDF generation error:', error);
        showResults('Failed to generate PDF: ' + error.message, 'error');
    });
}

