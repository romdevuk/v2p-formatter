"""
Unit tests for Observation Media Infrastructure (Stage 1)
"""
import unittest
import tempfile
import shutil
from pathlib import Path
from app.observation_media_scanner import list_output_subfolders, scan_media_subfolder, get_media_info
from app.placeholder_parser import extract_placeholders, validate_placeholders, assign_placeholder_colors, get_placeholder_colors


class TestObservationMediaScanner(unittest.TestCase):
    """Test observation media scanner functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.output_folder = self.temp_dir / "output"
        self.output_folder.mkdir()
        
        # Create test subfolders
        self.subfolder1 = self.output_folder / "folder1"
        self.subfolder2 = self.output_folder / "folder2"
        self.subfolder1.mkdir()
        self.subfolder2.mkdir()
        
        # Create test media files
        (self.subfolder1 / "test1.jpg").write_bytes(b"fake jpg")
        (self.subfolder1 / "test2.png").write_bytes(b"fake png")
        (self.subfolder1 / "test3.mp4").write_bytes(b"fake mp4")
        (self.subfolder2 / "test4.jpg").write_bytes(b"fake jpg")
        
        # Create hidden folder (should be ignored)
        (self.output_folder / ".hidden").mkdir()
        
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_list_output_subfolders(self):
        """Test listing subfolders from output directory"""
        subfolders = list_output_subfolders(self.output_folder)
        
        # Should return sorted list of subfolders
        self.assertIsInstance(subfolders, list)
        self.assertEqual(len(subfolders), 2)
        self.assertEqual(subfolders, ["folder1", "folder2"])
        self.assertNotIn(".hidden", subfolders)
    
    def test_list_output_subfolders_empty(self):
        """Test listing subfolders from empty directory"""
        empty_dir = Path(tempfile.mkdtemp())
        subfolders = list_output_subfolders(empty_dir)
        self.assertEqual(subfolders, [])
        shutil.rmtree(empty_dir)
    
    def test_list_output_subfolders_nonexistent(self):
        """Test listing subfolders from non-existent directory"""
        nonexistent = Path("/nonexistent/path/12345")
        subfolders = list_output_subfolders(nonexistent)
        self.assertEqual(subfolders, [])
    
    def test_scan_media_subfolder(self):
        """Test scanning media files from subfolder"""
        media_files = scan_media_subfolder(self.output_folder, "folder1")
        
        self.assertIsInstance(media_files, list)
        self.assertEqual(len(media_files), 3)
        
        # Check file types
        types = [f['type'] for f in media_files]
        self.assertIn('image', types)
        self.assertIn('video', types)
        
        # Check all files have required fields
        for media in media_files:
            self.assertIn('path', media)
            self.assertIn('name', media)
            self.assertIn('type', media)
            self.assertIn('size', media)
    
    def test_scan_media_subfolder_empty(self):
        """Test scanning empty subfolder"""
        empty_subfolder = self.output_folder / "empty"
        empty_subfolder.mkdir()
        
        media_files = scan_media_subfolder(self.output_folder, "empty")
        self.assertEqual(media_files, [])
    
    def test_scan_media_subfolder_nonexistent(self):
        """Test scanning non-existent subfolder"""
        media_files = scan_media_subfolder(self.output_folder, "nonexistent")
        self.assertEqual(media_files, [])
    
    def test_get_media_info_image(self):
        """Test getting media info for image file"""
        image_path = self.subfolder1 / "test1.jpg"
        info = get_media_info(image_path)
        
        self.assertIsNotNone(info)
        self.assertEqual(info['type'], 'image')
        self.assertEqual(info['name'], 'test1.jpg')
        self.assertIn('size', info)
        self.assertIn('width', info)
        self.assertIn('height', info)
    
    def test_get_media_info_video(self):
        """Test getting media info for video file"""
        video_path = self.subfolder1 / "test3.mp4"
        info = get_media_info(video_path)
        
        self.assertIsNotNone(info)
        self.assertEqual(info['type'], 'video')
        self.assertEqual(info['name'], 'test3.mp4')
        self.assertIn('size', info)


class TestPlaceholderParser(unittest.TestCase):
    """Test placeholder parser functionality"""
    
    def test_extract_placeholders(self):
        """Test extracting placeholders from text"""
        text = "This is {{Site_Arrival_Induction}} and {{Safety_Briefing}}"
        placeholders = extract_placeholders(text)
        
        self.assertEqual(len(placeholders), 2)
        self.assertIn('site_arrival_induction', placeholders)
        self.assertIn('safety_briefing', placeholders)
    
    def test_extract_placeholders_case_insensitive(self):
        """Test placeholder extraction is case-insensitive"""
        text = "{{Site_Arrival}} and {{site_arrival}}"
        placeholders = extract_placeholders(text)
        
        # Should return unique placeholders (normalized to lowercase)
        self.assertEqual(len(placeholders), 1)
        self.assertIn('site_arrival', placeholders)
    
    def test_extract_placeholders_empty(self):
        """Test extracting placeholders from empty text"""
        placeholders = extract_placeholders("")
        self.assertEqual(placeholders, [])
    
    def test_extract_placeholders_no_placeholders(self):
        """Test extracting placeholders from text without placeholders"""
        text = "This is just regular text"
        placeholders = extract_placeholders(text)
        self.assertEqual(placeholders, [])
    
    def test_extract_placeholders_underscores_only(self):
        """Test that placeholders only accept underscores (no spaces)"""
        text = "{{Site Arrival}}"  # Space - should not match
        placeholders = extract_placeholders(text)
        self.assertEqual(placeholders, [])
        
        text2 = "{{Site_Arrival}}"  # Underscore - should match
        placeholders2 = extract_placeholders(text2)
        self.assertEqual(len(placeholders2), 1)
    
    def test_validate_placeholders(self):
        """Test placeholder validation"""
        text = "{{Placeholder1}} and {{Placeholder2}}"
        assignments = {
            'placeholder1': ['media1.jpg']
            # placeholder2 not in assignments
        }
        
        validation = validate_placeholders(text, assignments)
        
        self.assertIn('all_placeholders', validation)
        self.assertIn('assigned', validation)
        self.assertIn('unassigned', validation)
        self.assertIn('is_valid', validation)
        self.assertEqual(validation['total_count'], 2)
        self.assertEqual(validation['assigned_count'], 1)
        self.assertEqual(validation['unassigned_count'], 1)
        self.assertFalse(validation['is_valid'])
    
    def test_validate_placeholders_all_assigned(self):
        """Test validation when all placeholders are assigned"""
        text = "{{Placeholder1}} and {{Placeholder2}}"
        assignments = {
            'placeholder1': ['media1.jpg'],
            'placeholder2': ['media2.jpg']
        }
        
        validation = validate_placeholders(text, assignments)
        self.assertTrue(validation['is_valid'])
        self.assertEqual(validation['unassigned_count'], 0)
    
    def test_get_placeholder_colors(self):
        """Test getting placeholder color palette"""
        colors = get_placeholder_colors()
        
        self.assertIsInstance(colors, list)
        self.assertGreater(len(colors), 0)
        # Check all are valid hex colors
        for color in colors:
            self.assertTrue(color.startswith('#'))
            self.assertEqual(len(color), 7)
    
    def test_assign_placeholder_colors(self):
        """Test assigning colors to placeholders"""
        placeholders = ['placeholder1', 'placeholder2', 'placeholder3']
        color_map = assign_placeholder_colors(placeholders)
        
        self.assertEqual(len(color_map), 3)
        self.assertIn('placeholder1', color_map)
        self.assertIn('placeholder2', color_map)
        self.assertIn('placeholder3', color_map)
        
        # Each placeholder should have a unique color (or cycle through)
        colors = get_placeholder_colors()
        for placeholder, color in color_map.items():
            self.assertIn(color, colors)


if __name__ == '__main__':
    unittest.main()

