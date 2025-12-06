"""
Integration tests for Observation Media Routes (Stage 1)
"""
import unittest
import tempfile
import shutil
import sys
from pathlib import Path
from flask import Flask

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from config import OUTPUT_FOLDER


class TestObservationMediaRoutes(unittest.TestCase):
    """Test observation media API routes"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create temporary test structure
        self.temp_dir = Path(tempfile.mkdtemp())
        test_subfolder = self.temp_dir / "test_folder"
        test_subfolder.mkdir()
        (test_subfolder / "test.jpg").write_bytes(b"fake jpg")
    
    def tearDown(self):
        """Clean up test fixtures"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_list_subfolders_route(self):
        """Test listing subfolders route"""
        with self.app.app_context():
            response = self.client.get('/v2p-formatter/media-converter/observation-media/subfolders')
            
            self.assertEqual(response.status_code, 200, f"Response: {response.get_data(as_text=True)}")
            data = response.get_json()
            self.assertIn('success', data)
            self.assertIn('subfolders', data)
            self.assertIsInstance(data['subfolders'], list)
    
    def test_get_media_route(self):
        """Test getting media files from subfolder"""
        # First, we need to create a real subfolder in OUTPUT_FOLDER for testing
        test_subfolder = OUTPUT_FOLDER / "test_observation_media"
        test_subfolder.mkdir(exist_ok=True)
        test_file = test_subfolder / "test.jpg"
        test_file.write_bytes(b"fake jpg")
        
        try:
            response = self.client.get(f'/v2p-formatter/media-converter/observation-media/media/test_observation_media')
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('success', data)
            self.assertIn('media', data)
            self.assertIn('count', data)
            self.assertIsInstance(data['media'], list)
        finally:
            # Cleanup
            if test_file.exists():
                test_file.unlink()
            if test_subfolder.exists():
                test_subfolder.rmdir()
    
    def test_get_media_route_invalid_subfolder(self):
        """Test getting media with invalid subfolder name"""
        # Flask will return 404 for paths with ../ before route handler is called
        # So we test with a different invalid pattern
        response = self.client.get('/v2p-formatter/media-converter/observation-media/media/invalid%2Fsubfolder')
        
        # Flask URL decoding might handle this, so we check for either 400 or 404
        self.assertIn(response.status_code, [400, 404])
        if response.status_code == 400:
            data = response.get_json()
            self.assertIn('error', data)
    
    def test_parse_placeholders_route(self):
        """Test parsing placeholders route"""
        response = self.client.post(
            '/v2p-formatter/media-converter/observation-media/parse-placeholders',
            json={'text': '{{Placeholder1}} and {{Placeholder2}}'},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('success', data)
        self.assertIn('placeholders', data)
        self.assertIn('color_map', data)
        self.assertEqual(len(data['placeholders']), 2)
    
    def test_parse_placeholders_route_empty(self):
        """Test parsing placeholders with empty text"""
        response = self.client.post(
            '/v2p-formatter/media-converter/observation-media/parse-placeholders',
            json={'text': ''},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['count'], 0)
    
    def test_validate_placeholders_route(self):
        """Test validating placeholders route"""
        response = self.client.post(
            '/v2p-formatter/media-converter/observation-media/validate-placeholders',
            json={
                'text': '{{Placeholder1}} and {{Placeholder2}}',
                'assignments': {'placeholder1': ['media1.jpg']}
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('success', data)
        self.assertIn('validation', data)
        self.assertIn('is_valid', data['validation'])
        self.assertFalse(data['validation']['is_valid'])  # placeholder2 not assigned


if __name__ == '__main__':
    unittest.main()

