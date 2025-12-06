"""
Observation Media DOCX Generator
Generates DOCX files with embedded media in 2-column tables
"""
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import logging
from PIL import Image

logger = logging.getLogger(__name__)


def create_observation_docx(text_content: str, assignments: dict, output_path: Path) -> dict:
    """
    Create a DOCX file from observation media text and assignments.
    
    Args:
        text_content: Text content with placeholders
        assignments: Dictionary mapping placeholder names to media lists
        output_path: Path where DOCX file should be saved
        
    Returns:
        Dictionary with success status and file path
    """
    try:
        # Create document
        doc = Document()
        
        # Set page size to A4
        section = doc.sections[0]
        section.page_height = Inches(11.69)  # A4 height
        section.page_width = Inches(8.27)   # A4 width
        
        # Parse text and replace placeholders with tables
        lines = text_content.split('\n')
        
        for line in lines:
            if not line.strip():
                # Empty line - add paragraph
                doc.add_paragraph()
                continue
            
            # Check if line contains placeholders
            placeholders = _extract_placeholders_from_line(line)
            
            if placeholders:
                # Process line with placeholders
                # Split by placeholders to get text segments
                import re
                pattern = re.compile(r'(\{\{[A-Za-z0-9_]+\}\})')
                parts = pattern.split(line)
                
                current_paragraph = None
                for part in parts:
                    if not part:
                        continue
                    
                    # Check if part is a placeholder
                    placeholder_match = re.match(r'\{\{([A-Za-z0-9_]+)\}\}', part)
                    if placeholder_match:
                        # Add table for placeholder
                        placeholder_key = placeholder_match.group(1).lower()
                        assigned_media = assignments.get(placeholder_key, [])
                        _add_media_table_to_doc(doc, assigned_media)
                        current_paragraph = None  # Reset paragraph after table
                    else:
                        # Regular text - add to paragraph
                        if not current_paragraph:
                            current_paragraph = doc.add_paragraph()
                        current_paragraph.add_run(part)
            else:
                # Regular text line - add paragraph
                if line.strip():
                    doc.add_paragraph(line.strip())
        
        # Save document
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(output_path))
        
        logger.info(f"DOCX file created successfully: {output_path}")
        
        return {
            'success': True,
            'file_path': str(output_path),
            'file_name': output_path.name
        }
        
    except Exception as e:
        logger.error(f"Error creating DOCX file: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def _extract_placeholders_from_line(line: str) -> list:
    """Extract placeholder names from a line of text"""
    import re
    pattern = re.compile(r'\{\{([A-Za-z0-9_]+)\}\}')
    matches = pattern.findall(line)
    return [m.lower() for m in matches]


def _add_media_table_to_doc(doc: Document, media_list: list):
    """
    Add a 2-column table with media to the document.
    
    Args:
        doc: Document object
        media_list: List of media dictionaries with 'path', 'name', 'type'
    """
    if not media_list:
        # Empty table
        table = doc.add_table(rows=1, cols=2)
        table.style = 'Table Grid'
        _style_table(table)
        row = table.rows[0]
        _style_cell(row.cells[0])
        _style_cell(row.cells[1])
        return
    
    # Calculate number of rows needed (2 columns per row)
    num_rows = (len(media_list) + 1) // 2
    
    # Create table
    table = doc.add_table(rows=num_rows, cols=2)
    table.style = 'Table Grid'
    _style_table(table)
    
    # Fill table with media
    for i, media in enumerate(media_list):
        row_idx = i // 2
        col_idx = i % 2
        
        cell = table.rows[row_idx].cells[col_idx]
        _style_cell(cell)
        
        if media['type'] == 'image':
            # Add image
            try:
                image_path = Path(media['path'])
                if image_path.exists():
                    # Get image dimensions to fit in cell
                    img = Image.open(image_path)
                    width, height = img.size
                    
                    # Calculate size to fit in cell (max 3.5 inches width, 4.5 inches height)
                    max_width = Inches(3.3)
                    max_height = Inches(4.5)
                    
                    # Calculate aspect ratio
                    aspect_ratio = height / width
                    
                    # Calculate dimensions maintaining aspect ratio
                    # Convert pixels to inches (assuming 96 DPI)
                    width_inches = width / 96.0
                    height_inches = height / 96.0
                    aspect_ratio = height_inches / width_inches
                    
                    if width_inches > height_inches:
                        # Landscape - fit to width
                        image_width = max_width
                        image_height = image_width * aspect_ratio
                        if image_height > max_height:
                            image_height = max_height
                            image_width = image_height / aspect_ratio
                    else:
                        # Portrait - fit to height
                        image_height = max_height
                        image_width = image_height / aspect_ratio
                        if image_width > max_width:
                            image_width = max_width
                            image_height = image_width * aspect_ratio
                    
                    # Add image to cell
                    paragraph = cell.paragraphs[0]
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = paragraph.add_run()
                    run.add_picture(str(image_path), width=image_width, height=image_height)
                else:
                    # Image not found - add text
                    paragraph = cell.paragraphs[0]
                    paragraph.add_run(f"[Image not found: {media['name']}]")
            except Exception as e:
                logger.warning(f"Error adding image {media['path']}: {e}")
                paragraph = cell.paragraphs[0]
                paragraph.add_run(f"[Error loading image: {media['name']}]")
        else:
            # Video - just add filename
            paragraph = cell.paragraphs[0]
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = paragraph.add_run(media['name'])
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(0, 0, 0)


def _style_table(table):
    """Apply styling to table (black borders, 1px)"""
    tbl = table._tbl
    tblBorders = OxmlElement('w:tblBorders')
    
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '4')  # 0.5pt
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), '000000')
        tblBorders.append(border)
    
    tbl.tblPr.append(tblBorders)


def _style_cell(cell):
    """Apply styling to cell (black borders, padding)"""
    cell.vertical_alignment = 1  # Center vertically
    # Borders are handled by table styling
    # Add some padding
    tcPr = cell._element.tcPr
    if tcPr is None:
        tcPr = OxmlElement('w:tcPr')
        cell._element.append(tcPr)
    
    tcMar = OxmlElement('w:tcMar')
    for margin_name in ['top', 'left', 'bottom', 'right']:
        margin = OxmlElement(f'w:{margin_name}')
        margin.set(qn('w:w'), '144')  # 0.1 inch
        margin.set(qn('w:type'), 'dxa')
        tcMar.append(margin)
    
    tcPr.append(tcMar)

