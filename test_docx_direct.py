"""
Direct test for DOCX media table formatting
Tests the DOCX generator directly without browser automation
"""
import sys
from pathlib import Path
from app.observation_docx_generator import create_observation_docx
from zipfile import ZipFile
import xml.etree.ElementTree as ET

OUTPUT_FOLDER = Path('/Users/rom/Documents/nvq/v2p-formatter-output')

def test_docx_generation():
    """Test DOCX generation with sample content"""
    
    print("="*60)
    print("DOCX Media Table Formatting Test")
    print("="*60)
    
    # Test 1: Empty placeholders
    print("\n1. Testing empty placeholders...")
    output_path = OUTPUT_FOLDER / "test_empty_tables.docx"
    text_content = """Test document with empty placeholders.

{{Image1}}

Text between.

{{Image2}}

Final text."""
    
    assignments = {
        'image1': [],
        'image2': []
    }
    
    result = create_observation_docx(text_content, assignments, output_path)
    
    if result['success']:
        print(f"   ✓ Created: {output_path.name}")
        verify_docx_structure(output_path, "Empty tables test")
    else:
        print(f"   ✗ Failed: {result.get('error')}")
        return False
    
    # Test 2: With actual images (if available)
    print("\n2. Testing with media assignments...")
    
    # Find some images in the output folder
    images = []
    if OUTPUT_FOLDER.exists():
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            images.extend(list(OUTPUT_FOLDER.rglob(ext)))
            if len(images) >= 4:  # Need at least 2 for testing
                break
    
    if len(images) >= 2:
        output_path2 = OUTPUT_FOLDER / "test_with_images.docx"
        text_content2 = """Test document with images.

{{Image1}}

{{Image2}}

Final section."""
        
        assignments2 = {
            'image1': [
                {
                    'path': str(images[0]),
                    'name': images[0].name,
                    'type': 'image'
                }
            ],
            'image2': [
                {
                    'path': str(images[1]),
                    'name': images[1].name,
                    'type': 'image'
                },
                {
                    'path': str(images[2]) if len(images) > 2 else str(images[0]),
                    'name': images[2].name if len(images) > 2 else images[0].name,
                    'type': 'image'
                }
            ]
        }
        
        result2 = create_observation_docx(text_content2, assignments2, output_path2)
        
        if result2['success']:
            print(f"   ✓ Created: {output_path2.name}")
            verify_docx_structure(output_path2, "With images test")
        else:
            print(f"   ✗ Failed: {result2.get('error')}")
    else:
        print("   ⚠ Skipped: No images found in output folder")
    
    print("\n" + "="*60)
    print("Test Complete")
    print("="*60)
    return True


def verify_docx_structure(docx_path: Path, test_name: str):
    """Verify DOCX file structure and table formatting"""
    
    if not docx_path.exists():
        print(f"   ✗ File does not exist: {docx_path}")
        return
    
    file_size = docx_path.stat().st_size
    print(f"   File size: {file_size} bytes")
    
    if file_size == 0:
        print(f"   ✗ File is empty!")
        return
    
    try:
        with ZipFile(docx_path, 'r') as zip_file:
            # Read document.xml
            doc_xml = zip_file.read('word/document.xml')
            root = ET.fromstring(doc_xml)
            
            # Define namespace
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            # Find all tables
            tables = root.findall('.//w:tbl', ns)
            print(f"   Tables found: {len(tables)}")
            
            for i, table in enumerate(tables):
                print(f"\n   Table {i+1} Analysis:")
                
                # Get table properties
                tbl_pr = table.find('w:tblPr', ns)
                if tbl_pr is not None:
                    # Check table width
                    tbl_width = tbl_pr.find('w:tblW', ns)
                    if tbl_width is not None:
                        width_val = tbl_width.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w')
                        width_type = tbl_width.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type')
                        print(f"      Width: {width_val} twips ({width_type})")
                    
                    # Check table alignment
                    jc = tbl_pr.find('w:jc', ns)
                    if jc is not None:
                        align = jc.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                        print(f"      Alignment: {align}")
                
                # Get rows and check structure
                rows = table.findall('.//w:tr', ns)
                print(f"      Rows: {len(rows)}")
                
                if rows:
                    first_row = rows[0]
                    cells = first_row.findall('.//w:tc', ns)
                    print(f"      Columns: {len(cells)}")
                    
                    # Check column widths in first row
                    col_widths = []
                    for j, cell in enumerate(cells):
                        tc_pr = cell.find('w:tcPr', ns)
                        if tc_pr is not None:
                            tc_width = tc_pr.find('w:tcW', ns)
                            if tc_width is not None:
                                width_val = tc_width.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w')
                                width_type = tc_width.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type')
                                col_widths.append((width_val, width_type))
                                print(f"         Column {j+1} width: {width_val} ({width_type})")
                    
                    # Verify columns are equal width
                    if len(col_widths) == 2:
                        if col_widths[0][0] == col_widths[1][0]:
                            print(f"      ✓ Columns have equal widths")
                        else:
                            print(f"      ✗ Columns have different widths!")
                            print(f"         Issue: Column widths don't match")
                    
                    # Check for images
                    images_found = 0
                    for cell in cells:
                        blips = cell.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip', 
                                            {'': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
                        if blips:
                            images_found += len(blips)
                    
                    print(f"      Images in table: {images_found}")
            
            # Count paragraphs
            paragraphs = root.findall('.//w:p', ns)
            print(f"\n   Total paragraphs: {len(paragraphs)}")
            
            # Count images
            all_images = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip',
                                     {'': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
            print(f"   Total images: {len(all_images)}")
            
    except Exception as e:
        print(f"   ✗ Error analyzing DOCX: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    success = test_docx_generation()
    sys.exit(0 if success else 1)


