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
    debugOutput('=== Application Initialized ===', 'success');
    debugOutput('DOM Content Loaded event fired', 'info');
    
    // Set up choose file button - try multiple ways
    const chooseFileBtn = document.getElementById('chooseFileBtn');
    const videoInput = document.getElementById('videoInput');
    
    debugOutput(`Button found: ${!!chooseFileBtn}`, chooseFileBtn ? 'success' : 'error');
    debugOutput(`Input found: ${!!videoInput}`, videoInput ? 'success' : 'error');
    
    if (!chooseFileBtn) {
        debugOutput('❌ ERROR: Choose File button not found!', 'error');
        return;
    }
    
    if (!videoInput) {
        debugOutput('❌ ERROR: Video input element not found!', 'error');
        return;
    }
    
    // Method 1: Add click event listener
    chooseFileBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        debugOutput('🔘 Choose File button clicked (addEventListener)', 'info');
        console.log('Button clicked, triggering file input...');
        
        try {
            videoInput.click();
            debugOutput('✅ File input click() called successfully', 'success');
        } catch (error) {
            debugOutput(`❌ Error clicking file input: ${error.message}`, 'error');
            console.error('Error:', error);
        }
    });
    
    debugOutput('✅ Choose File button event listener attached', 'success');
    
    // Test file input
    debugOutput('Testing file input...', 'info');
    try {
        debugOutput(`Input type: ${videoInput.type}`, 'info');
        debugOutput(`Input accept: ${videoInput.accept}`, 'info');
        debugOutput(`Input style.display: ${videoInput.style.display}`, 'info');
    } catch (err) {
        debugOutput(`Error testing input: ${err.message}`, 'error');
    }
});

// Utility functions
function showSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.style.display = 'block';
        if (typeof debugOutput !== 'undefined') {
            debugOutput(`✅ Section shown: ${sectionId}`, 'success');
        }
    } else {
        if (typeof debugOutput !== 'undefined') {
            debugOutput(`❌ Section not found: ${sectionId}`, 'error');
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

