"""
Simple test to verify video upload works
"""
import pytest
import requests
from pathlib import Path


def test_upload_video_file_direct():
    """Test video upload via direct API call"""
    video_path = Path("/Users/rom/Documents/nvq/visited/css/L2 INTER/ ivan myhal /mp4/plasterboard-formingopening-multitool.mp4")
    
    assert video_path.exists(), f"Video file not found: {video_path}"
    
    with open(video_path, 'rb') as f:
        files = {'video': (video_path.name, f, 'video/mp4')}
        response = requests.post(
            'http://localhost:5000/v2p-formatter/upload',
            files=files,
            timeout=60
        )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    assert response.status_code == 200, f"Upload failed: {response.text}"
    data = response.json()
    assert data.get('success') == True, f"Upload not successful: {data}"
    print(f"✅ Upload successful! Duration: {data.get('duration')}s")

