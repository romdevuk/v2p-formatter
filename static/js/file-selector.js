// File selector for choosing MP4 files from server directory

// Make sure function is available globally
function loadFileTree() {
    console.log('📂 loadFileTree() called');
    
    if (typeof window.debugOutput === 'function') {
        window.debugOutput('📂 Loading file tree...', 'info');
    }
    
    const fileTree = document.getElementById('fileTree');
    const fileTreeContent = document.getElementById('fileTreeContent');
    const fileTreeLoading = document.getElementById('fileTreeLoading');
    
    if (!fileTree || !fileTreeContent || !fileTreeLoading) {
        console.error('❌ File tree elements not found');
        console.error('  fileTree:', !!fileTree);
        console.error('  fileTreeContent:', !!fileTreeContent);
        console.error('  fileTreeLoading:', !!fileTreeLoading);
        return;
    }
    
    console.log('✅ File tree elements found, starting fetch...');
    
    // Show loading state
    fileTree.style.display = 'block';
    if (fileTreeLoading) {
        fileTreeLoading.style.display = 'block';
    }
    fileTreeContent.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">Loading MP4 files from output folder...</p>';
    
    // Get qualification and learner from dropdowns or URL parameters
    const qualificationSelect = document.getElementById('qualificationSelect');
    const learnerSelect = document.getElementById('learnerSelect');
    const urlParams = new URLSearchParams(window.location.search);
    const qualification = (qualificationSelect && qualificationSelect.value) || urlParams.get('qualification') || '';
    const learner = (learnerSelect && learnerSelect.value) || urlParams.get('learner') || '';
    
    // Build URL with parameters
    let url = '/v2p-formatter/list_files';
    if (qualification && learner) {
        url += `?qualification=${encodeURIComponent(qualification)}&learner=${encodeURIComponent(learner)}`;
    }
    console.log('🌐 Fetching:', url);
    
    fetch(url)
        .then(response => {
            console.log('📡 Response received:', response.status, response.statusText);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('📊 Data received:', data);
            if (fileTreeLoading) {
                fileTreeLoading.style.display = 'none';
            }
            
            if (data.success) {
                if (typeof window.debugOutput === 'function') {
                    window.debugOutput(`✅ Found ${data.count} MP4 files`, 'success');
                    if (data.input_folder) {
                        window.debugOutput(`📁 Input folder: ${data.input_folder}`, 'info');
                    }
                    if (data.output_folder) {
                        window.debugOutput(`📁 Output folder: ${data.output_folder}`, 'info');
                    }
                }
                console.log(`✅ Found ${data.count} MP4 files`);
                if (data.input_folder) {
                    console.log(`📁 Input folder: ${data.input_folder}`);
                }
                if (data.output_folder) {
                    console.log(`📁 Output folder: ${data.output_folder}`);
                }
                // Store files for re-rendering
                if (typeof window.appData !== 'undefined') {
                    window.appData.availableFiles = data.files;
                }
                renderFileTree(data.files, fileTreeContent);
                fileTree.style.display = 'block';
            } else {
                if (typeof window.debugOutput === 'function') {
                    window.debugOutput(`❌ Error loading files: ${data.error}`, 'error');
                }
                console.error('❌ Error:', data.error);
                fileTreeContent.innerHTML = `<p style="color: red; padding: 10px;">Error: ${data.error}</p>`;
                fileTree.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('❌ Fetch error:', error);
            fileTreeLoading.style.display = 'none';
            if (typeof window.debugOutput === 'function') {
                window.debugOutput(`❌ Error: ${error.message}`, 'error');
            }
            fileTreeContent.innerHTML = `<p style="color: red; padding: 10px;">Error loading files: ${error.message}<br>Please check that the Flask server is running.</p>`;
            fileTree.style.display = 'block';
        });
}

function renderFileTree(files, container) {
    if (files.length === 0) {
        container.innerHTML = '<p style="color: #666; padding: 10px;">No MP4 files found in input folder</p>';
        return;
    }
    
    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Get sort and thumbnail settings - default to 3 per row
    const sortBy = (typeof window.appData !== 'undefined' && window.appData.sortBy) ? window.appData.sortBy : 'name';
    let thumbnailsPerRow = 3; // Default to 3
    if (typeof window.appData !== 'undefined' && window.appData.thumbnailsPerRow) {
        const parsed = parseInt(window.appData.thumbnailsPerRow);
        if (!isNaN(parsed) && parsed > 0) {
            thumbnailsPerRow = parsed;
        }
    }
    // Ensure minimum of 3 per row (force default)
    if (thumbnailsPerRow < 3 || isNaN(thumbnailsPerRow)) {
        thumbnailsPerRow = 3;
    }
    
    // Group files by folder
    const folders = {};
    files.forEach(file => {
        const folder = file.folder === 'root' ? 'Root' : file.folder;
        if (!folders[folder]) {
            folders[folder] = [];
        }
        folders[folder].push(file);
    });
    
    let html = '<div class="file-tree-list" style="width: 100%;">';
    
    // Sort folders
    const sortedFolders = Object.keys(folders).sort();
    
    sortedFolders.forEach((folder, index) => {
        const escapedFolder = escapeHtml(folder);
        // Auto-expand first folder (or if only one folder)
        const shouldExpand = index === 0 || sortedFolders.length === 1;
        const displayStyle = shouldExpand ? 'block' : 'none';
        const folderIcon = shouldExpand ? '📂' : '📁';
        
        html += `<div class="file-tree-folder">`;
        html += `<div class="file-tree-folder-header" onclick="toggleFolder(this)" style="cursor: pointer; padding: 10px; margin: 5px 0; background: #2a2a2a; border-radius: 4px; display: flex; align-items: center; gap: 10px;">
            <span class="folder-icon">${folderIcon}</span>
            <strong style="color: #e0e0e0;">${escapedFolder}</strong>
            <span style="color: #666; margin-left: 10px;">(${folders[folder].length} files)</span>
        </div>`;
        html += `<div class="file-tree-folder-content" style="display: ${displayStyle}; margin-top: 5px; width: 100%;">`;
        
        // Sort files based on sortBy setting
        if (sortBy === 'date') {
            // Sort by date (if available) or name as fallback
            folders[folder].sort((a, b) => {
                const dateA = a.modified_time || a.created_time || 0;
                const dateB = b.modified_time || b.created_time || 0;
                if (dateA !== dateB) {
                    return dateB - dateA; // Newest first
                }
                return a.name.localeCompare(b.name);
            });
        } else {
            // Sort by name (default)
            folders[folder].sort((a, b) => a.name.localeCompare(b.name));
        }
        
        // Render files in thumbnail grid layout - always use grid, never list
        // Use CSS Grid for more reliable layout - FORCE 3 columns by default
        // If thumbnailsPerRow is not explicitly set to 4, use 3
        const gridColumns = (thumbnailsPerRow === 4) ? 4 : 3;
        html += `<div class="video-grid-container" style="display: grid !important; grid-template-columns: repeat(${gridColumns}, 1fr) !important; gap: 16px !important; margin: 0 !important; width: 100% !important; box-sizing: border-box !important;">`;
        
        folders[folder].forEach(file => {
            const escapedPath = escapeHtml(file.path).replace(/'/g, "\\'").replace(/"/g, '&quot;');
            const escapedName = escapeHtml(file.name);
            const cacheKey = file.modified_time ? `m=${Math.floor(file.modified_time)}` : `t=${new Date().getTime()}`;
            const thumbnailUrl = `/v2p-formatter/thumbnail?path=${encodeURIComponent(file.path)}&size=240x180&${cacheKey}`;
            
            html += `<div class="video-item" 
                         data-path="${escapedPath}" 
                         data-name="${escapedName}"
                         onclick="selectFile('${escapedPath}', '${escapedName}')"
                         style="padding: 12px; border-radius: 8px; cursor: pointer; 
                                background: #1e1e1e; 
                                border: 2px solid #555;
                                width: 100%;
                                box-sizing: border-box;
                                position: relative; transition: all 0.2s;"
                         onmouseover="this.style.background='#2a2a2a'; this.style.borderColor='#667eea';"
                         onmouseout="this.style.background='#1e1e1e'; this.style.borderColor='#555';"
                         title="${escapedPath}">
                    <div style="width: 100%; padding-top: 75%; background: #1a1a1a; border-radius: 4px; overflow: hidden; position: relative; margin-bottom: 8px;">
                        <img src="${thumbnailUrl}" 
                             alt="${escapedName}"
                             style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain;"
                             onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
                             onload="this.nextElementSibling.style.display='none';">
                        <div style="display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; flex-direction: column; align-items: center; justify-content: center; color: #999; font-size: 11px; background: #1a1a1a;">
                            <span style="font-size: 2em;">🎬</span>
                        </div>
                    </div>
                    <div style="padding: 0 4px;">
                        <div style="color: #e0e0e0; font-weight: 500; font-size: 13px; word-break: break-word; text-align: center; margin-bottom: 4px;">${escapedName}</div>
                        <div style="color: #666; font-size: 11px; text-align: center;">(${(file.size_mb || 0).toFixed(2)} MB)</div>
                    </div>
                </div>`;
        });
        
        html += '</div>'; // Close grid container
        html += `</div></div>`;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

function toggleFolder(element) {
    const content = element.nextElementSibling;
    if (content.style.display === 'none') {
        content.style.display = 'block';
        element.querySelector('.folder-icon').textContent = '📂';
    } else {
        content.style.display = 'none';
        element.querySelector('.folder-icon').textContent = '📁';
    }
}

function selectFile(filePath, fileName) {
    if (typeof window.debugOutput === 'function') {
        window.debugOutput(`📁 File selected: ${fileName}`, 'info');
        window.debugOutput(`   Path: ${filePath}`, 'info');
    }
    console.log('File selected:', fileName, filePath);
    
    showStatus('Loading video info...', 'success');
    
    fetch('/v2p-formatter/select_file', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            file_path: filePath
        })
    })
    .then(response => {
        console.log('Select file response:', response.status);
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || `HTTP ${response.status}`);
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            if (typeof window.debugOutput === 'function') {
                window.debugOutput('✅ File loaded successfully!', 'success');
                window.debugOutput(`   Duration: ${data.duration}s`, 'info');
                window.debugOutput(`   Resolution: ${data.width}x${data.height}`, 'info');
            }
            console.log('File loaded:', data);
            
            appState.videoFile = { name: fileName, path: filePath };
            appState.videoPath = data.filepath;
            appState.videoInfo = data;
            
            // Also sync to window.appData for compatibility with index.html functions
            if (typeof window.appData !== 'undefined') {
                window.appData.videoPath = data.filepath;
                window.appData.videoInfo = data;
            }
            
            // Show video preview
            const videoPlayer = document.getElementById('videoPlayer');
            const videoInfoDiv = document.getElementById('videoInfo');
            
            if (videoPlayer) {
                // Serve video file through Flask
                const videoUrl = `/v2p-formatter/video_file?path=${encodeURIComponent(filePath)}`;
                videoPlayer.src = videoUrl;
                console.log('Video URL:', videoUrl);
                if (typeof window.debugOutput === 'function') {
                    window.debugOutput('✅ Video player source set', 'success');
                }
            } else {
                console.error('Video player element not found');
            }
            
            // Display video info
            if (videoInfoDiv) {
                videoInfoDiv.innerHTML = `
                    <div class="video-info-item">
                        <strong>Duration</strong>
                        <span>${data.duration.toFixed(2)}s</span>
                    </div>
                    <div class="video-info-item">
                        <strong>Resolution</strong>
                        <span>${data.width}x${data.height}</span>
                    </div>
                    <div class="video-info-item">
                        <strong>FPS</strong>
                        <span>${data.fps.toFixed(2)}</span>
                    </div>
                    <div class="video-info-item">
                        <strong>Filename</strong>
                        <span>${data.filename}</span>
                    </div>
                `;
                if (typeof window.debugOutput === 'function') {
                    window.debugOutput('✅ Video info displayed', 'success');
                }
            }
            showStatus('Video loaded successfully!', 'success');
            
            // Show all sections
            showSection('timeSection');
            showSection('outputSettingsSection');
            showSection('processingSection');
            
            // Initialize time selector after video is loaded
            setTimeout(function() {
                if (typeof initTimeSelector === 'function') {
                    initTimeSelector();
                } else if (window.initTimeSelector) {
                    window.initTimeSelector();
                }
            }, 1000);
            
            if (typeof window.debugOutput === 'function') {
                window.debugOutput('✅✅✅ ALL SECTIONS SHOWN - READY TO USE! ✅✅✅', 'success');
            }
            console.log('All sections shown');
        } else {
            const errorMsg = data.error || 'Failed to load file';
            if (typeof window.debugOutput === 'function') {
                window.debugOutput(`❌ Error: ${errorMsg}`, 'error');
            }
            console.error('Error:', errorMsg);
            showStatus(errorMsg, 'error');
        }
    })
    .catch(error => {
        if (typeof window.debugOutput === 'function') {
            window.debugOutput(`❌ Error loading file: ${error.message}`, 'error');
        }
        console.error('Error loading file:', error);
        showStatus('Failed to load file: ' + error.message, 'error');
    });
}

// Make it available globally immediately
if (typeof window !== 'undefined') {
    window.loadFileTree = loadFileTree;
    console.log('✅ loadFileTree function registered globally on window');
} else {
    // Fallback for non-browser environments
    console.log('✅ loadFileTree function defined');
}

