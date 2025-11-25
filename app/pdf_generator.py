from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, Image as RLImage
from reportlab.lib import colors
from pathlib import Path

def create_pdf(images, output_path, layout='grid', images_per_page=4):
    """
    Create PDF with images in a 2-column table layout
    
    Args:
        images: List of image file paths
        output_path: Path to save PDF
        layout: 'grid' or 'custom' (ignored, always uses 2-column table)
        images_per_page: Number of images per page (ignored, always 2 columns)
    """
    from reportlab.platypus import SimpleDocTemplate
    
    doc = SimpleDocTemplate(str(output_path), pagesize=A4,
                            leftMargin=0.5*inch, rightMargin=0.5*inch,
                            topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Build table data: 2 columns per row
    table_data = []
    for i in range(0, len(images), 2):
        row = []
        # First column
        if i < len(images):
            try:
                img1 = RLImage(images[i], width=3.5*inch, height=3.5*inch, kind='proportional')
                row.append(img1)
            except Exception as e:
                print(f"Error loading image {images[i]}: {e}")
                row.append("")
        else:
            row.append("")
        
        # Second column (if exists)
        if i + 1 < len(images):
            try:
                img2 = RLImage(images[i + 1], width=3.5*inch, height=3.5*inch, kind='proportional')
                row.append(img2)
            except Exception as e:
                print(f"Error loading image {images[i + 1]}: {e}")
                row.append("")
        else:
            row.append("")  # Empty cell for odd number of images
        
        table_data.append(row)
    
    # Create table with 2 columns
    table = Table(table_data, colWidths=[3.5*inch, 3.5*inch])
    
    # Style the table with 1px black borders
    # 5px = 5/72 inch ≈ 0.069 inch (ReportLab uses points, 1 point = 1/72 inch)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # All borders: 1px black
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Horizontal alignment
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # 5px spacing at bottom
    ]))
    
    # Build PDF
    elements = [table]
    doc.build(elements)
    
    return str(output_path)
