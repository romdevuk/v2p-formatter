// File selector for choosing MP4 files from server directory

// Make sure function is available globally
function loadFileTree() {
    console.log('📂 loadFileTree() called');
    
    if (typeof debugOutput !== 'undefined') {
        debugOutput('📂 Loading file tree...', 'info');
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
    fileTreeContent.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">Loading MP4 files from input folder...</p>';
    
    const url = '/v2p-formatter/list_files';
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
                if (typeof debugOutput !== 'undefined') {
                    debugOutput(`✅ Found ${data.count} MP4 files`, 'success');
                    if (data.input_folder) {
                        debugOutput(`📁 Input folder: ${data.input_folder}`, 'info');
                    }
                    if (data.output_folder) {
                        debugOutput(`📁 Output folder: ${data.output_folder}`, 'info');
                    }
                }
                console.log(`✅ Found ${data.count} MP4 files`);
                if (data.input_folder) {
                    console.log(`📁 Input folder: ${data.input_folder}`);
                }
                if (data.output_folder) {
                    console.log(`📁 Output folder: ${data.output_folder}`);
                }
                renderFileTree(data.files, fileTreeContent);
                fileTree.style.display = 'block';
            } else {
                if (typeof debugOutput !== 'undefined') {
                    debugOutput(`❌ Error loading files: ${data.error}`, 'error');
                }
                console.error('❌ Error:', data.error);
                fileTreeContent.innerHTML = `<p style="color: red; padding: 10px;">Error: ${data.error}</p>`;
                fileTree.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('❌ Fetch error:', error);
            fileTreeLoading.style.display = 'none';
            if (typeof debugOutput !== 'undefined') {
                debugOutput(`❌ Error: ${error.message}`, 'error');
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
    
    // Group files by folder
    const folders = {};
    files.forEach(file => {
        const folder = file.folder === 'root' ? 'Root' : file.folder;
        if (!folders[folder]) {
            folders[folder] = [];
        }
        folders[folder].push(file);
    });
    
    let html = '<div class="file-tree-list">';
    
    // Sort folders
    const sortedFolders = Object.keys(folders).sort();
    
    sortedFolders.forEach((folder, index) => {
        const escapedFolder = escapeHtml(folder);
        // Auto-expand first folder (or if only one folder)
        const shouldExpand = index === 0 || sortedFolders.length === 1;
        const displayStyle = shouldExpand ? 'block' : 'none';
        const folderIcon = shouldExpand ? '📂' : '📁';
        
        html += `<div class="file-tree-folder">`;
        html += `<div class="file-tree-folder-header" onclick="toggleFolder(this)">
            <span class="folder-icon">${folderIcon}</span>
            <strong>${escapedFolder}</strong>
            <span style="color: #666; margin-left: 10px;">(${folders[folder].length} files)</span>
        </div>`;
        html += `<div class="file-tree-folder-content" style="display: ${displayStyle}; margin-left: 20px; margin-top: 5px;">`;
        
        // Sort files by name
        folders[folder].sort((a, b) => a.name.localeCompare(b.name));
        
        folders[folder].forEach(file => {
            const escapedPath = escapeHtml(file.path).replace(/'/g, "&#39;").replace(/"/g, "&quot;");
            const escapedName = escapeHtml(file.name);
            html += `<div class="file-tree-item" onclick="selectFile('${escapedPath}', '${escapedName}')" title="${escapedPath}" style="cursor: pointer; padding: 8px; margin: 3px 0; border-radius: 4px; transition: background 0.2s; background: #f9f9f9;" onmouseover="this.style.background='#e8f0fe'" onmouseout="this.style.background='#f9f9f9'">
                <span class="file-icon">🎬</span>
                <span class="file-name" style="font-weight: 500;">${escapedName}</span>
                <span class="file-size" style="color: #666; margin-left: 8px;">(${file.size_mb} MB)</span>
            </div>`;
        });
        
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
    if (typeof debugOutput !== 'undefined') {
        debugOutput(`📁 File selected: ${fileName}`, 'info');
        debugOutput(`   Path: ${filePath}`, 'info');
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
            if (typeof debugOutput !== 'undefined') {
                debugOutput('✅ File loaded successfully!', 'success');
                debugOutput(`   Duration: ${data.duration}s`, 'info');
                debugOutput(`   Resolution: ${data.width}x${data.height}`, 'info');
            }
            console.log('File loaded:', data);
            
            appState.videoFile = { name: fileName, path: filePath };
            appState.videoPath = data.filepath;
            appState.videoInfo = data;
            
            // Show video preview
            const videoPlayer = document.getElementById('videoPlayer');
            const videoInfoDiv = document.getElementById('videoInfo');
            
            if (videoPlayer) {
                // Serve video file through Flask
                const videoUrl = `/v2p-formatter/video_file?path=${encodeURIComponent(filePath)}`;
                videoPlayer.src = videoUrl;
                console.log('Video URL:', videoUrl);
                if (typeof debugOutput !== 'undefined') {
                    debugOutput('✅ Video player source set', 'success');
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
                if (typeof debugOutput !== 'undefined') {
                    debugOutput('✅ Video info displayed', 'success');
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
            
            if (typeof debugOutput !== 'undefined') {
                debugOutput('✅✅✅ ALL SECTIONS SHOWN - READY TO USE! ✅✅✅', 'success');
            }
            console.log('All sections shown');
        } else {
            const errorMsg = data.error || 'Failed to load file';
            if (typeof debugOutput !== 'undefined') {
                debugOutput(`❌ Error: ${errorMsg}`, 'error');
            }
            console.error('Error:', errorMsg);
            showStatus(errorMsg, 'error');
        }
    })
    .catch(error => {
        if (typeof debugOutput !== 'undefined') {
            debugOutput(`❌ Error loading file: ${error.message}`, 'error');
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

