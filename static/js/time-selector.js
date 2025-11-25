// Time selector - SIMPLE VERSION FROM SCRATCH

// Global state
window.timeSelectorState = {
    selectedTimes: [],
    initialized: false
};

// Simple add time function
function addCurrentTime() {
    console.log('🖱️ Add Current Time button clicked');
    
    const video = document.getElementById('videoPlayer');
    if (!video) {
        alert('Video player not found');
        console.error('❌ Video player element not found');
        return;
    }
    
    const currentTime = video.currentTime;
    console.log(`⏱️ Current time: ${currentTime.toFixed(2)}s`);
    
    if (isNaN(currentTime) || currentTime < 0) {
        alert('Video not ready. Please wait for video to load.');
        return;
    }
    
    const rounded = Math.round(currentTime * 100) / 100;
    
    // Check if already exists
    if (window.timeSelectorState.selectedTimes.includes(rounded)) {
        console.log(`⚠️ Time ${rounded.toFixed(2)}s already added`);
        return;
    }
    
    // Add to array
    window.timeSelectorState.selectedTimes.push(rounded);
    window.timeSelectorState.selectedTimes.sort((a, b) => a - b);
    
    console.log(`✅ Added time: ${rounded.toFixed(2)}s`);
    console.log('All times:', window.timeSelectorState.selectedTimes);
    
    // Update display
    updateTimeDisplay();
}

// Remove time
function removeTime(time) {
    window.timeSelectorState.selectedTimes = window.timeSelectorState.selectedTimes.filter(t => t !== time);
    updateTimeDisplay();
    console.log(`🗑️ Removed time: ${time.toFixed(2)}s`);
}

// Clear all
function clearAllTimes() {
    window.timeSelectorState.selectedTimes = [];
    updateTimeDisplay();
    console.log('🗑️ Cleared all times');
}

// Update display
function updateTimeDisplay() {
    const container = document.getElementById('timePointsList');
    if (!container) {
        console.error('❌ timePointsList container not found');
        return;
    }
    
    const times = window.timeSelectorState.selectedTimes;
    
    if (times.length === 0) {
        container.innerHTML = '<p style="color: #666; font-style: italic; padding: 10px;">No time points selected. Click "+ Add Current Time" to add.</p>';
        return;
    }
    
    let html = '';
    times.forEach(time => {
        html += `<span onclick="removeTime(${time})" style="
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 10px 16px;
            border-radius: 25px;
            font-size: 15px;
            cursor: pointer;
            margin: 6px;
            font-weight: 500;
            transition: all 0.2s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        " onmouseover="this.style.background='#5568d3'; this.style.transform='scale(1.1)'" 
           onmouseout="this.style.background='#667eea'; this.style.transform='scale(1)'"
           title="Click to remove">
            ${time.toFixed(2)}s
            <span style="margin-left: 8px; font-size: 18px; font-weight: bold;">×</span>
        </span>`;
    });
    
    container.innerHTML = html;
    console.log(`✅ Display updated with ${times.length} time(s)`);
}

// Get times as string for API
function getTimePointsString() {
    return window.timeSelectorState.selectedTimes.join(', ');
}

// Get times as array
function getTimePointsArray() {
    return [...window.timeSelectorState.selectedTimes];
}

// Initialize - SIMPLE VERSION
function initTimeSelector() {
    console.log('🚀 Initializing time selector...');
    
    const addBtn = document.getElementById('addCurrentTimeBtn');
    const clearBtn = document.getElementById('clearAllTimesBtn');
    
    if (!addBtn) {
        console.error('❌ addCurrentTimeBtn not found');
        return false;
    }
    
    if (!clearBtn) {
        console.error('❌ clearAllTimesBtn not found');
        return false;
    }
    
    // Remove any existing listeners by replacing buttons
    const newAddBtn = addBtn.cloneNode(true);
    addBtn.parentNode.replaceChild(newAddBtn, addBtn);
    
    const newClearBtn = clearBtn.cloneNode(true);
    clearBtn.parentNode.replaceChild(newClearBtn, clearBtn);
    
    // Get fresh references
    const freshAddBtn = document.getElementById('addCurrentTimeBtn');
    const freshClearBtn = document.getElementById('clearAllTimesBtn');
    
    // Add click handlers - DIRECT, NO COMPLEX LOGIC
    freshAddBtn.onclick = function(e) {
        e.preventDefault();
        e.stopPropagation();
        addCurrentTime();
        return false;
    };
    
    freshClearBtn.onclick = function(e) {
        e.preventDefault();
        e.stopPropagation();
        clearAllTimes();
        return false;
    };
    
    // Initial display update
    updateTimeDisplay();
    
    window.timeSelectorState.initialized = true;
    console.log('✅ Time selector initialized successfully');
    
    return true;
}

// Make functions global
window.addCurrentTime = addCurrentTime;
window.removeTime = removeTime;
window.clearAllTimes = clearAllTimes;
window.updateTimeDisplay = updateTimeDisplay;
window.getTimePointsString = getTimePointsString;
window.getTimePointsArray = getTimePointsArray;
window.initTimeSelector = initTimeSelector;

// Auto-initialize when DOM ready
(function() {
    function tryInit() {
        if (initTimeSelector()) {
            console.log('✅ Auto-initialized successfully');
        } else {
            console.log('⏳ Not ready yet, will retry...');
            setTimeout(tryInit, 500);
        }
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(tryInit, 1000);
        });
    } else {
        setTimeout(tryInit, 1000);
    }
})();

// Also try when time section becomes visible
const checkSection = setInterval(function() {
    const section = document.getElementById('timeSection');
    if (section && section.style.display !== 'none' && !window.timeSelectorState.initialized) {
        console.log('👁️ Time section visible, initializing...');
        initTimeSelector();
    }
}, 1000);

// Stop checking after 30 seconds
setTimeout(function() {
    clearInterval(checkSection);
}, 30000);
