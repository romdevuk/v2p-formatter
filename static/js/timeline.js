// Time point selection and validation

const previewFramesBtn = document.getElementById('previewFramesBtn');
const timeInput = document.getElementById('timeInput');

if (previewFramesBtn) {
    previewFramesBtn.addEventListener('click', previewFrames);
}

function previewFrames() {
    const timeInputValue = timeInput.value.trim();
    if (!timeInputValue) {
        showStatus('Please enter time points', 'error');
        return;
    }
    
    if (!appState.videoPath) {
        showStatus('Please upload a video first', 'error');
        return;
    }
    
    // Parse time points
    const timePoints = parseTimeInput(timeInputValue);
    if (!timePoints || timePoints.length === 0) {
        showStatus('Invalid time format. Use: 30 or 10,25,45 or 10-20', 'error');
        return;
    }
    
    // Validate time points are within video duration
    if (appState.videoInfo) {
        const maxTime = appState.videoInfo.duration;
        const invalidTimes = timePoints.filter(t => t < 0 || t > maxTime);
        if (invalidTimes.length > 0) {
            showStatus(`Time points outside video duration (max: ${maxTime.toFixed(2)}s): ${invalidTimes.join(', ')}`, 'error');
            return;
        }
    }
    
    appState.timePoints = timePoints;
    
    // Show preview
    showFramePreviews(timePoints);
}

function parseTimeInput(input) {
    const timePoints = [];
    input = input.trim();
    
    // Handle range (e.g., '10-20')
    if (input.includes('-') && !input.includes(',')) {
        const parts = input.split('-');
        if (parts.length === 2) {
            const start = parseFloat(parts[0]);
            const end = parseFloat(parts[1]);
            if (!isNaN(start) && !isNaN(end) && start <= end) {
                for (let i = Math.floor(start); i <= Math.ceil(end); i++) {
                    timePoints.push(i);
                }
                return timePoints;
            }
        }
    }
    
    // Handle comma-separated values
    const parts = input.split(',');
    for (const part of parts) {
        const time = parseFloat(part.trim());
        if (!isNaN(time)) {
            timePoints.push(time);
        } else {
            return null;
        }
    }
    
    return timePoints.length > 0 ? timePoints : null;
}

function showFramePreviews(timePoints) {
    const previewDiv = document.getElementById('framePreview');
    previewDiv.innerHTML = '<p>Loading previews...</p>';
    
    // Limit to first 12 previews for performance
    const previewTimes = timePoints.slice(0, 12);
    
    Promise.all(previewTimes.map(time => loadFramePreview(time)))
        .then(images => {
            previewDiv.innerHTML = '';
            images.forEach((imgData, index) => {
                if (imgData) {
                    const item = document.createElement('div');
                    item.className = 'frame-preview-item';
                    item.innerHTML = `
                        <img src="${imgData.url}" alt="Frame at ${previewTimes[index]}s">
                        <p>${previewTimes[index]}s</p>
                    `;
                    previewDiv.appendChild(item);
                }
            });
            
            if (timePoints.length > 12) {
                const more = document.createElement('p');
                more.textContent = `... and ${timePoints.length - 12} more frames`;
                more.style.textAlign = 'center';
                more.style.marginTop = '10px';
                previewDiv.appendChild(more);
            }
        })
        .catch(error => {
            console.error('Preview error:', error);
            previewDiv.innerHTML = '<p style="color: red;">Failed to load previews</p>';
        });
}

function loadFramePreview(timePoint) {
    return fetch('/v2p-formatter/preview_frame', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            video_path: appState.videoPath,
            time_point: timePoint
        })
    })
    .then(response => {
        if (response.ok) {
            return response.blob().then(blob => ({
                url: URL.createObjectURL(blob),
                time: timePoint
            }));
        }
        return null;
    });
}

