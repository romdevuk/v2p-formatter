// Global state
let appState = {
    videoFile: null,
    videoPath: null,
    videoInfo: null,
    timePoints: [],
    extractedImages: [],
    pdfPath: null
};

// Debug output function - use global one if available, otherwise define fallback
if (typeof window.debugOutput === 'undefined') {
    window.debugOutput = function(message, type = 'info') {
        console.log(`[DEBUG ${type.toUpperCase()}]`, message);
        const debugDiv = document.getElementById('debugOutput');
        const debugMessages = document.getElementById('debugMessages');
        if (debugDiv && debugMessages) {
            debugDiv.style.display = 'block';
            const timestamp = new Date().toLocaleTimeString();
            const color = type === 'error' ? 'red' : type === 'success' ? 'green' : type === 'info' ? 'blue' : 'black';
            const msg = document.createElement('div');
            msg.style.color = color;
            msg.style.marginBottom = '2px';
            msg.style.padding = '2px 0';
            msg.innerHTML = `[${timestamp}] ${message}`;
            debugMessages.appendChild(msg);
            debugMessages.scrollTop = debugMessages.scrollHeight;
        }
    };
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    console.log('Video to Image Formatter initialized');
    if (typeof window.debugOutput === 'function') {
        window.debugOutput('=== Application Initialized ===', 'success');
        window.debugOutput('DOM Content Loaded event fired', 'info');
    }
    
    // Set up choose file button - only if on the main video upload page
    const chooseFileBtn = document.getElementById('chooseFileBtn');
    const videoInput = document.getElementById('videoInput');
    
    // Check if we're on a page with video upload functionality
    // If not, silently skip initialization (e.g., observation-media page)
    if (!chooseFileBtn || !videoInput) {
        // Not an error - this page doesn't have video upload functionality
        if (typeof window.debugOutput === 'function') {
            window.debugOutput('Video upload elements not found - skipping initialization (expected on some pages)', 'info');
        }
        return;
    }
    
    if (typeof window.debugOutput === 'function') {
        window.debugOutput(`Button found: ${!!chooseFileBtn}`, 'success');
        window.debugOutput(`Input found: ${!!videoInput}`, 'success');
    }
    
    // Method 1: Add click event listener
    chooseFileBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        if (typeof window.debugOutput === 'function') {
            window.debugOutput('🔘 Choose File button clicked (addEventListener)', 'info');
        }
        console.log('Button clicked, triggering file input...');
        
        try {
            videoInput.click();
            if (typeof window.debugOutput === 'function') {
                window.debugOutput('✅ File input click() called successfully', 'success');
            }
        } catch (error) {
            if (typeof window.debugOutput === 'function') {
                window.debugOutput(`❌ Error clicking file input: ${error.message}`, 'error');
            }
            console.error('Error:', error);
        }
    });
    
    if (typeof window.debugOutput === 'function') {
        window.debugOutput('✅ Choose File button event listener attached', 'success');
    }
    
    // Test file input
    if (typeof window.debugOutput === 'function') {
        window.debugOutput('Testing file input...', 'info');
    }
    try {
        if (typeof window.debugOutput === 'function') {
            window.debugOutput(`Input type: ${videoInput.type}`, 'info');
            window.debugOutput(`Input accept: ${videoInput.accept}`, 'info');
            window.debugOutput(`Input style.display: ${videoInput.style.display}`, 'info');
        }
    } catch (err) {
        if (typeof window.debugOutput === 'function') {
            window.debugOutput(`Error testing input: ${err.message}`, 'error');
        }
    }
});

// Utility functions
function showSection(sectionId) {
    debugger; // Debug breakpoint
    const section = document.getElementById(sectionId);
    if (section) {
        section.style.display = 'block';
        if (typeof window.debugOutput === 'function') {
            window.debugOutput(`✅ Section shown: ${sectionId}`, 'success');
        }
    } else {
        if (typeof window.debugOutput === 'function') {
            window.debugOutput(`❌ Section not found: ${sectionId}`, 'error');
        }
    }
}

function hideSection(sectionId) {
    document.getElementById(sectionId).style.display = 'none';
}

function showStatus(message, type = 'success') {
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.textContent = message;
    statusDiv.className = `status-message ${type}`;
}

function showProgress(percent, text) {
    const container = document.getElementById('progressContainer');
    const fill = document.getElementById('progressFill');
    const textEl = document.getElementById('progressText');
    
    container.style.display = 'block';
    fill.style.width = percent + '%';
    textEl.textContent = text;
}

function hideProgress() {
    document.getElementById('progressContainer').style.display = 'none';
}

function showResults(message, type = 'success', links = []) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.className = `results ${type}`;
    
    let html = `<p><strong>${message}</strong></p>`;
    if (links.length > 0) {
        html += '<ul style="margin-top: 10px;">';
        links.forEach(link => {
            html += `<li><a href="${link.url}" target="_blank">${link.text}</a></li>`;
        });
        html += '</ul>';
    }
    
    resultsDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
}

// Open file in macOS Preview (for PDFs) or default app
function openFileInPreview(filePath) {
    fetch('/v2p-formatter/open_file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: filePath })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('File opened in Preview:', filePath);
        } else {
            console.error('Failed to open file:', data.error);
            alert('Failed to open file: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error opening file:', error);
        alert('Error opening file: ' + error.message);
    });
}

// Open folder in macOS Finder
function openFolderInFinder(folderPath) {
    fetch('/v2p-formatter/open_folder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: folderPath })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Folder opened in Finder:', folderPath);
        } else {
            console.error('Failed to open folder:', data.error);
            alert('Failed to open folder: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error opening folder:', error);
        alert('Error opening folder: ' + error.message);
    });
}

