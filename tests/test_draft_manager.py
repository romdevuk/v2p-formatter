"""
Unit tests for Draft Manager
"""
import unittest
import tempfile
import shutil
import json
from pathlib import Path
from app.draft_manager import save_draft, load_draft, list_drafts, delete_draft, update_draft, DRAFTS_FOLDER


class TestDraftManager(unittest.TestCase):
    """Test draft manager functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Use a temporary directory for drafts during testing
        import app.draft_manager as dm
        self.original_drafts_folder = dm.DRAFTS_FOLDER
        self.temp_dir = Path(tempfile.mkdtemp())
        dm.DRAFTS_FOLDER = self.temp_dir
        dm.DRAFTS_FOLDER.mkdir(parents=True, exist_ok=True)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import app.draft_manager as dm
        shutil.rmtree(self.temp_dir)
        dm.DRAFTS_FOLDER = self.original_drafts_folder
    
    def test_save_draft(self):
        """Test saving a draft"""
        import app.draft_manager as dm
        result = dm.save_draft(
            "Test Draft",
            "Test content with {{Placeholder1}}",
            {'placeholder1': [{'path': '/test.jpg', 'name': 'test.jpg', 'type': 'image'}]},
            "subfolder1"
        )
        
        self.assertTrue(result['success'])
        self.assertIn('draft_id', result)
        self.assertEqual(result['draft_name'], 'Test Draft')
        
        # Verify file was created
        draft_files = list(dm.DRAFTS_FOLDER.glob('*.json'))
        self.assertEqual(len(draft_files), 1)
    
    def test_load_draft(self):
        """Test loading a draft"""
        import app.draft_manager as dm
        # Save a draft first
        save_result = dm.save_draft(
            "Test Draft",
            "Test content",
            {'placeholder1': []},
            "subfolder1"
        )
        
        draft_id = save_result['draft_id']
        load_result = dm.load_draft(draft_id)
        
        self.assertTrue(load_result['success'])
        self.assertIn('draft', load_result)
        self.assertEqual(load_result['draft']['name'], 'Test Draft')
        self.assertEqual(load_result['draft']['text_content'], 'Test content')
    
    def test_list_drafts(self):
        """Test listing drafts"""
        import app.draft_manager as dm
        # Save multiple drafts
        dm.save_draft("Draft 1", "Content 1", {}, None)
        dm.save_draft("Draft 2", "Content 2", {}, None)
        
        drafts = dm.list_drafts()
        
        self.assertGreaterEqual(len(drafts), 2)
        draft_names = [d['name'] for d in drafts]
        self.assertIn('Draft 1', draft_names)
        self.assertIn('Draft 2', draft_names)
    
    def test_delete_draft(self):
        """Test deleting a draft"""
        import app.draft_manager as dm
        # Save a draft
        save_result = dm.save_draft("Test Draft", "Content", {}, None)
        draft_id = save_result['draft_id']
        
        # Delete it
        delete_result = dm.delete_draft(draft_id)
        
        self.assertTrue(delete_result['success'])
        
        # Verify it's gone
        load_result = dm.load_draft(draft_id)
        self.assertFalse(load_result['success'])
    
    def test_update_draft(self):
        """Test updating a draft"""
        import app.draft_manager as dm
        # Save a draft
        save_result = dm.save_draft("Test Draft", "Original content", {}, None)
        draft_id = save_result['draft_id']
        
        # Update it
        update_result = dm.update_draft(draft_id, "Updated content", {'p1': []}, "subfolder2")
        
        self.assertTrue(update_result['success'])
        
        # Verify update
        load_result = dm.load_draft(draft_id)
        self.assertEqual(load_result['draft']['text_content'], 'Updated content')
        self.assertEqual(load_result['draft']['selected_subfolder'], 'subfolder2')


if __name__ == '__main__':
    unittest.main()

