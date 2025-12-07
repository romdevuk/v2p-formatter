"""
Test DOCX generation with actual image files
"""
import sys
from pathlib import Path
from app.observation_docx_generator import create_observation_docx
from config import OUTPUT_FOLDER
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def find_test_images():
    """Find actual image files in OUTPUT_FOLDER"""
    images = []
    if OUTPUT_FOLDER.exists():
        for ext in ['.jpg', '.jpeg', '.png']:
            images.extend(list(OUTPUT_FOLDER.rglob(f'*{ext}')))
            if len(images) >= 4:
                break
    return images[:4]  # Return up to 4 images

def test_with_real_images():
    """Test DOCX generation with real image files"""
    
    print("="*60)
    print("DOCX Image Test - Using Real Image Files")
    print("="*60)
    
    # Find real images
    images = find_test_images()
    
    if not images:
        print(f"\n⚠ No images found in {OUTPUT_FOLDER}")
        print("  Creating test with placeholder paths...")
        
        # Create test with non-existent paths to test error handling
        text_content = """Test document with images.

{{Image1}}

Text between.

{{Image2}}

Final text."""
        
        assignments = {
            'image1': [
                {
                    'path': '/nonexistent/path/image1.jpg',
                    'name': 'image1.jpg',
                    'type': 'image'
                }
            ],
            'image2': []
        }
        
        output_path = OUTPUT_FOLDER / "test_images_placeholder.docx"
        result = create_observation_docx(text_content, assignments, output_path)
        
        if result['success']:
            print(f"\n✓ Created DOCX with placeholders: {output_path.name}")
        else:
            print(f"\n✗ Failed: {result.get('error')}")
        
        return
    
    print(f"\n✓ Found {len(images)} image(s)")
    for img in images:
        print(f"  - {img.name} ({img.parent.name}/)")
    
    # Create test content
    # Note: Need {{{{ for literal {{ in f-strings, or use regular string
    text_content = f"""Test document with {len(images)} images.

{{{{Image1}}}}

Text between images.

{{{{Image2}}}}

Final section."""
    
    assignments = {
        'image1': [
            {
                'path': str(images[0]),
                'name': images[0].name,
                'type': 'image'
            }
        ]
    }
    
    if len(images) > 1:
        assignments['image2'] = [
            {
                'path': str(img),
                'name': img.name,
                'type': 'image'
            }
            for img in images[1:3]  # Use up to 2 more images
        ]
    else:
        assignments['image2'] = []
    
    output_path = OUTPUT_FOLDER / "test_with_real_images.docx"
    
    print(f"\n✓ Creating DOCX: {output_path.name}")
    print(f"  Image1: {assignments['image1'][0]['name']}")
    if assignments['image2']:
        print(f"  Image2: {', '.join([m['name'] for m in assignments['image2']])}")
    
    result = create_observation_docx(text_content, assignments, output_path)
    
    if result['success']:
        file_size = output_path.stat().st_size
        print(f"\n✓ DOCX created successfully!")
        print(f"  File: {output_path.name}")
        print(f"  Size: {file_size} bytes")
        
        # Analyze structure
        from zipfile import ZipFile
        import xml.etree.ElementTree as ET
        
        with ZipFile(output_path, 'r') as zip_file:
            doc_xml = zip_file.read('word/document.xml')
            root = ET.fromstring(doc_xml)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            images_in_docx = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip',
                                         {'': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
            print(f"  Images in DOCX: {len(images_in_docx)}")
            
            if len(images_in_docx) > 0:
                print("  ✓ Images successfully added!")
            else:
                print("  ✗ No images found in DOCX")
    else:
        print(f"\n✗ Failed: {result.get('error')}")

if __name__ == '__main__':
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    test_with_real_images()

