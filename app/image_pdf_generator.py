"""
PDF generator for images with filenames displayed below each image
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, Image as RLImage, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from pathlib import Path


def create_image_pdf(images, image_names, output_path, layout='grid', images_per_page=2, quality=95, max_width=None, max_height=None):
    """
    Create PDF with images and filenames displayed below each image
    
    Args:
        images: List of image file paths (in order)
        image_names: List of filenames (without extension) to display below each image
        output_path: Path to save PDF
        layout: 'grid' or 'custom' (currently only grid supported)
        images_per_page: Number of images per page (1, 2, 4, 6, 9, 12) - determines grid layout
        quality: JPEG quality (1-100) - used when processing images
        max_width: Max image width in pixels (None = original)
        max_height: Max image height in pixels (None = original)
    """
    from reportlab.platypus import SimpleDocTemplate
    from PIL import Image as PILImage
    import tempfile
    import os
    
    # Process images if resizing needed
    processed_images = []
    temp_files = []
    
    for img_path in images:
        try:
            img_path_obj = Path(img_path)
            if not img_path_obj.exists():
                print(f"Warning: Image not found: {img_path}")
                continue
            
            # Open image to check/process
            pil_img = PILImage.open(img_path)
            
            # Resize if needed
            if max_width or max_height:
                if max_width and max_height:
                    pil_img.thumbnail((max_width, max_height), PILImage.Resampling.LANCZOS)
                elif max_width:
                    ratio = max_width / pil_img.width
                    new_height = int(pil_img.height * ratio)
                    pil_img = pil_img.resize((max_width, new_height), PILImage.Resampling.LANCZOS)
                elif max_height:
                    ratio = max_height / pil_img.height
                    new_width = int(pil_img.width * ratio)
                    pil_img = pil_img.resize((new_width, max_height), PILImage.Resampling.LANCZOS)
            
            # Save processed image temporarily if needed
            if max_width or max_height or quality != 95:
                temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                pil_img.save(temp_file.name, 'JPEG', quality=quality)
                processed_images.append(temp_file.name)
                temp_files.append(temp_file.name)
            else:
                processed_images.append(str(img_path_obj))
                
        except Exception as e:
            print(f"Error processing image {img_path}: {e}")
            continue
    
    # Determine grid layout based on images_per_page
    if images_per_page == 1:
        cols = 1
    elif images_per_page == 2:
        cols = 2
    elif images_per_page == 4:
        cols = 2  # 2x2 grid
    elif images_per_page == 6:
        cols = 3  # 3x2 grid
    elif images_per_page == 9:
        cols = 3  # 3x3 grid
    elif images_per_page == 12:
        cols = 3  # 3x4 grid
    else:
        cols = 2  # Default to 2 columns
    
    rows_per_page = images_per_page // cols
    
    # Calculate image size based on columns
    page_width = A4[0]
    page_height = A4[1]
    margins = 0.5 * inch * 2  # Left + right
    usable_width = page_width - margins
    col_width = usable_width / cols
    image_width = (col_width * 0.9)  # 90% of column width for padding
    
    doc = SimpleDocTemplate(str(output_path), pagesize=A4,
                            leftMargin=0.5*inch, rightMargin=0.5*inch,
                            topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Create styles for filename text
    styles = getSampleStyleSheet()
    filename_style = ParagraphStyle(
        'FilenameStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=12
    )
    
    elements = []
    
    # Build pages
    for page_start in range(0, len(processed_images), images_per_page):
        page_images = processed_images[page_start:page_start + images_per_page]
        page_names = image_names[page_start:page_start + images_per_page] if len(image_names) > page_start else []
        
        # Create table data for this page
        table_data = []
        for row in range(rows_per_page):
            row_data = []
            for col in range(cols):
                idx = row * cols + col
                if idx < len(page_images):
                    try:
                        # Get image
                        img = RLImage(page_images[idx], width=image_width, height=image_width, kind='proportional')
                        
                        # Get filename (strip extension if present in name)
                        filename = page_names[idx] if idx < len(page_names) else Path(page_images[idx]).stem
                        
                        # Create a list containing image and filename paragraph
                        cell_content = [img, Spacer(1, 3), Paragraph(filename, filename_style)]
                        row_data.append(cell_content)
                    except Exception as e:
                        print(f"Error loading image {page_images[idx]}: {e}")
                        filename = page_names[idx] if idx < len(page_names) else Path(page_images[idx]).stem
                        row_data.append([Paragraph(f"Error: {filename}", filename_style)])
                else:
                    row_data.append([])  # Empty cell
            
            if any(row_data):  # Only add row if it has content
                table_data.append(row_data)
        
        if table_data:
            # Create table
            col_widths = [col_width] * cols
            table = Table(table_data, colWidths=col_widths)
            
            # Style the table
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 1px black borders
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Top alignment
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            
            elements.append(table)
            
            # Add page break if not last page
            if page_start + images_per_page < len(processed_images):
                elements.append(Spacer(1, 0.2*inch))
    
    # Build PDF
    doc.build(elements)
    
    # Clean up temp files
    for temp_file in temp_files:
        try:
            os.unlink(temp_file)
        except:
            pass
    
    return str(output_path)

