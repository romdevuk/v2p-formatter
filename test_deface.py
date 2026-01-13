#!/usr/bin/env python3
"""
Test script for deface functionality with dummy data
"""
import sys
from pathlib import Path
import tempfile
import shutil
from PIL import Image
import numpy as np

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

def create_dummy_image(output_path, width=640, height=480):
    """Create a dummy test image"""
    # Create a simple test image with colored rectangles
    img = Image.new('RGB', (width, height), color='white')
    pixels = np.array(img)
    
    # Add some colored rectangles to make it more interesting
    pixels[100:200, 100:200] = [255, 0, 0]  # Red square
    pixels[300:400, 300:400] = [0, 255, 0]  # Green square
    
    img = Image.fromarray(pixels)
    img.save(output_path, 'JPEG', quality=95)
    print(f"✓ Created dummy image: {output_path}")

def test_deface_command():
    """Test if deface command is available"""
    import subprocess
    import shutil
    import os
    
    # Try multiple methods to find deface
    deface_cmd = None
    
    # Method 1: which('deface')
    deface_cmd = shutil.which('deface')
    
    # Method 2: Check user's Python bin directory
    if not deface_cmd:
        user_bin = os.path.expanduser('~/Library/Python/3.9/bin/deface')
        if os.path.exists(user_bin):
            deface_cmd = user_bin
    
    if not deface_cmd:
        print("✗ deface command not found - please install: pip install deface")
        print("  Or install in venv: source venv/bin/activate && pip install deface")
        return False
    
    try:
        result = subprocess.run([deface_cmd, '--help'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 or 'usage:' in result.stdout.lower() or 'usage:' in result.stderr.lower():
            print(f"✓ deface command is available at: {deface_cmd}")
            return True
        else:
            print(f"✗ deface command returned error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"✗ Error running deface command: {e}")
        return False

def test_deface_image():
    """Test deface_image function with dummy image"""
    from app.deface_processor import deface_image
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    try:
        # Create dummy input image
        input_image = temp_dir / 'test_input.jpg'
        create_dummy_image(input_image)
        
        # Create output path
        output_image = temp_dir / 'test_output.jpg'
        
        print(f"\n[TEST] Testing deface_image function...")
        print(f"  Input: {input_image}")
        print(f"  Output: {output_image}")
        
        result = deface_image(
            input_image,
            output_image,
            replacewith='blur',
            boxes=False,
            thresh=0.2
        )
        
        if result.get('success'):
            print(f"✓ deface_image succeeded: {result.get('output_path')}")
            if output_image.exists():
                print(f"✓ Output file exists: {output_image}")
                return True
            else:
                print(f"✗ Output file does not exist: {output_image}")
                return False
        else:
            print(f"✗ deface_image failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"✗ Exception in test_deface_image: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)

def test_deface_images():
    """Test deface_images function with dummy images"""
    from app.deface_processor import deface_images
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    output_dir = temp_dir / 'output'
    try:
        # Create dummy input images
        input_images = []
        for i in range(2):
            img_path = temp_dir / f'test_input_{i}.jpg'
            create_dummy_image(img_path)
            input_images.append(img_path)
        
        print(f"\n[TEST] Testing deface_images function...")
        print(f"  Input images: {[str(p) for p in input_images]}")
        print(f"  Output dir: {output_dir}")
        
        result = deface_images(
            input_images,
            output_dir,
            replacewith='blur',
            boxes=False,
            thresh=0.2,
            output_prefix='deface_'
        )
        
        print(f"  Result: success={result.get('success')}, processed={len(result.get('processed', []))}, errors={len(result.get('errors', []))}")
        
        if result.get('processed'):
            print(f"✓ deface_images succeeded: {len(result['processed'])} images processed")
            for p in result['processed']:
                if Path(p).exists():
                    print(f"  ✓ {p}")
                else:
                    print(f"  ✗ Missing: {p}")
            return True
        else:
            print(f"✗ deface_images failed")
            if result.get('errors'):
                print(f"  Errors:")
                for err in result['errors']:
                    print(f"    - {err}")
            return False
            
    except Exception as e:
        print(f"✗ Exception in test_deface_images: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    print("=" * 60)
    print("Deface Functionality Test")
    print("=" * 60)
    
    # Test 1: Check if deface command exists
    print("\n[TEST 1] Checking if deface command is available...")
    if not test_deface_command():
        print("\n❌ FAILED: deface command not found")
        print("Please install deface: pip install deface")
        return 1
    
    # Test 2: Test deface_image function
    print("\n[TEST 2] Testing deface_image function...")
    if not test_deface_image():
        print("\n❌ FAILED: deface_image test failed")
        return 1
    
    # Test 3: Test deface_images function
    print("\n[TEST 3] Testing deface_images function...")
    if not test_deface_images():
        print("\n❌ FAILED: deface_images test failed")
        return 1
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED")
    print("=" * 60)
    return 0

if __name__ == '__main__':
    sys.exit(main())
