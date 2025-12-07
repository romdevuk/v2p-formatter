#!/usr/bin/env python3
"""
Test script for media converter functionality
"""
import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost/v2p-formatter"

def test_list_files():
    """Test listing media files"""
    print("=" * 60)
    print("Test 1: List Media Files")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/media-converter/list")
    data = response.json()
    
    print(f"✅ Success: {data.get('success')}")
    print(f"📹 Videos found: {data.get('video_count', 0)}")
    print(f"🖼️  Images found: {data.get('image_count', 0)}")
    
    if data.get('videos'):
        print("\nVideos:")
        for v in data['videos'][:3]:
            print(f"  - {v['name']} ({v['size_mb']}MB)")
    
    if data.get('images'):
        print("\nImages:")
        for img in data['images'][:3]:
            print(f"  - {img['name']} ({img['size_mb']}MB)")
    
    return data

def test_convert_image():
    """Test converting a single image"""
    print("\n" + "=" * 60)
    print("Test 2: Convert Single Image")
    print("=" * 60)
    
    # Get files
    response = requests.get(f"{BASE_URL}/media-converter/list")
    data = response.json()
    
    if not data.get('images'):
        print("❌ No images found to convert")
        return None
    
    # Select first image
    image = data['images'][0]
    print(f"📸 Converting: {image['name']} ({image['size_mb']}MB)")
    
    # Start conversion
    convert_data = {
        'files': [{
            'path': image['path'],
            'type': image['type']
        }],
        'settings': {
            'image': {
                'resolution': '1280x720',
                'quality': 'medium',
                'maintain_aspect': True,
                'allow_stretch': False
            }
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/media-converter/convert",
        json=convert_data,
        headers={'Content-Type': 'application/json'}
    )
    
    result = response.json()
    print(f"✅ Job started: {result.get('success')}")
    
    if result.get('success'):
        job_id = result['job_id']
        print(f"📋 Job ID: {job_id}")
        
        # Poll for status
        print("\n⏳ Waiting for conversion...")
        max_wait = 60  # 60 seconds max
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            status_response = requests.get(f"{BASE_URL}/media-converter/status/{job_id}")
            status = status_response.json()
            
            if status.get('success'):
                progress = status.get('progress', 0)
                job_status = status.get('status', 'unknown')
                print(f"  Progress: {progress:.1f}% - Status: {job_status}")
                
                if job_status in ('completed', 'failed', 'cancelled'):
                    print(f"\n✅ Conversion {job_status}")
                    
                    # Show results
                    results = status.get('results', {})
                    errors = status.get('errors', {})
                    
                    if results:
                        for path, result_data in results.items():
                            if result_data.get('success'):
                                print(f"  ✅ {Path(path).name}")
                                print(f"     Size: {result_data.get('input_size_mb', 0):.2f}MB → {result_data.get('output_size_mb', 0):.2f}MB")
                                print(f"     Reduction: {result_data.get('reduction_percent', 0):.1f}%")
                                print(f"     Output: {result_data.get('output_path', 'N/A')}")
                                
                                # Verify file exists
                                output_path = Path(result_data.get('output_path', ''))
                                if output_path.exists():
                                    print(f"     ✅ Output file exists: {output_path.stat().st_size / (1024*1024):.2f}MB")
                                else:
                                    print(f"     ❌ Output file not found!")
                    
                    if errors:
                        for path, error in errors.items():
                            print(f"  ❌ {Path(path).name}: {error}")
                    
                    return status
            
            time.sleep(2)
        
        print("⏱️  Timeout waiting for conversion")
        return None
    
    else:
        print(f"❌ Error: {result.get('error')}")
        return None

def test_convert_video():
    """Test converting a single video"""
    print("\n" + "=" * 60)
    print("Test 3: Convert Single Video")
    print("=" * 60)
    
    # Get files
    response = requests.get(f"{BASE_URL}/media-converter/list")
    data = response.json()
    
    if not data.get('videos'):
        print("❌ No videos found to convert")
        return None
    
    # Select first video
    video = data['videos'][0]
    print(f"🎬 Converting: {video['name']} ({video['size_mb']}MB)")
    
    # Start conversion
    convert_data = {
        'files': [{
            'path': video['path'],
            'type': 'mov'
        }],
        'settings': {
            'video': {
                'quality': 'medium'
            }
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/media-converter/convert",
        json=convert_data,
        headers={'Content-Type': 'application/json'}
    )
    
    result = response.json()
    print(f"✅ Job started: {result.get('success')}")
    
    if result.get('success'):
        job_id = result['job_id']
        print(f"📋 Job ID: {job_id}")
        
        # Poll for status
        print("\n⏳ Waiting for conversion (this may take a while for videos)...")
        max_wait = 300  # 5 minutes max for video
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            status_response = requests.get(f"{BASE_URL}/media-converter/status/{job_id}")
            status = status_response.json()
            
            if status.get('success'):
                progress = status.get('progress', 0)
                job_status = status.get('status', 'unknown')
                print(f"  Progress: {progress:.1f}% - Status: {job_status}")
                
                if job_status in ('completed', 'failed', 'cancelled'):
                    print(f"\n✅ Conversion {job_status}")
                    
                    # Show results
                    results = status.get('results', {})
                    errors = status.get('errors', {})
                    
                    if results:
                        for path, result_data in results.items():
                            if result_data.get('success'):
                                print(f"  ✅ {Path(path).name}")
                                print(f"     Size: {result_data.get('input_size_mb', 0):.2f}MB → {result_data.get('output_size_mb', 0):.2f}MB")
                                print(f"     Reduction: {result_data.get('reduction_percent', 0):.1f}%")
                                print(f"     Output: {result_data.get('output_path', 'N/A')}")
                                
                                # Verify file exists
                                output_path = Path(result_data.get('output_path', ''))
                                if output_path.exists():
                                    print(f"     ✅ Output file exists: {output_path.stat().st_size / (1024*1024):.2f}MB")
                                else:
                                    print(f"     ❌ Output file not found!")
                    
                    if errors:
                        for path, error in errors.items():
                            print(f"  ❌ {Path(path).name}: {error}")
                    
                    return status
            
            time.sleep(3)
        
        print("⏱️  Timeout waiting for conversion")
        return None
    
    else:
        print(f"❌ Error: {result.get('error')}")
        return None

def verify_output_files():
    """Verify output files exist"""
    print("\n" + "=" * 60)
    print("Test 4: Verify Output Files")
    print("=" * 60)
    
    from config import OUTPUT_FOLDER
    
    output_path = Path(OUTPUT_FOLDER)
    if not output_path.exists():
        print(f"❌ Output folder does not exist: {output_path}")
        return
    
    # Find converted files
    mp4_files = list(output_path.rglob('*.mp4'))
    jpg_files = list(output_path.rglob('*.jpg'))
    jpeg_files = list(output_path.rglob('*.jpeg'))
    
    print(f"📁 Output folder: {output_path}")
    print(f"🎬 MP4 files found: {len(mp4_files)}")
    print(f"🖼️  JPG/JPEG files found: {len(jpg_files) + len(jpeg_files)}")
    
    if mp4_files:
        print("\nMP4 files:")
        for f in mp4_files[:5]:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  ✅ {f.name} ({size_mb:.2f}MB) - {f.parent}")
    
    if jpg_files or jpeg_files:
        print("\nImage files:")
        for f in (jpg_files + jpeg_files)[:5]:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  ✅ {f.name} ({size_mb:.2f}MB) - {f.parent}")

if __name__ == '__main__':
    print("\n🧪 Media Converter Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: List files
        file_data = test_list_files()
        
        # Test 2: Convert image (if available)
        if file_data.get('image_count', 0) > 0:
            test_convert_image()
        
        # Test 3: Convert video (if available)
        if file_data.get('video_count', 0) > 0:
            test_convert_video()
        
        # Test 4: Verify output
        verify_output_files()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server. Is Flask app running?")
        print("   Start with: python run.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()



