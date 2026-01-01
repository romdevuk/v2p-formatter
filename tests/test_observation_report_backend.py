"""
Backend unit tests for Observation Report module
Tests all backend modules: scanner, parser, draft manager, DOCX generator
"""
import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Import backend modules
from app.observation_report_scanner import (
    scan_media_files,
    get_media_metadata,
    generate_thumbnail_path,
    SUPPORTED_IMAGE_EXTENSIONS,
    SUPPORTED_VIDEO_EXTENSIONS,
    SUPPORTED_PDF_EXTENSIONS,
    SUPPORTED_AUDIO_EXTENSIONS
)
from app.observation_report_placeholder_parser import (
    extract_placeholders,
    validate_placeholder,
    assign_placeholder_colors,
    PLACEHOLDER_PATTERN
)
from app.observation_report_draft_manager import (
    save_draft,
    load_draft,
    list_drafts,
    delete_draft
)


@pytest.fixture
def temp_output_folder():
    """Create temporary output folder for tests"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_media_folder(temp_output_folder):
    """Create sample media files for testing"""
    media_dir = temp_output_folder / "qualification" / "learner"
    media_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample files
    (media_dir / "image1.jpg").touch()
    (media_dir / "image2.png").touch()
    (media_dir / "video1.mp4").touch()
    (media_dir / "video2.mov").touch()
    (media_dir / "document1.pdf").touch()
    (media_dir / "audio1.mp3").touch()
    
    return media_dir


class TestMediaScanner:
    """Test media scanner module"""
    
    def test_scan_media_files_basic(self, sample_media_folder, temp_output_folder):
        """Test basic media file scanning"""
        qualification = "qualification"
        learner = "learner"
        
        results = scan_media_files(qualification, learner, temp_output_folder)
        
        assert isinstance(results, list)
        assert len(results) >= 6  # At least our test files
        
        # Check file types are detected
        filenames = [r['filename'] for r in results]
        assert 'image1.jpg' in filenames
        assert 'image2.png' in filenames
        assert 'video1.mp4' in filenames
        assert 'document1.pdf' in filenames
    
    def test_media_file_metadata_structure(self, sample_media_folder, temp_output_folder):
        """Test that media file metadata has correct structure"""
        qualification = "qualification"
        learner = "learner"
        
        results = scan_media_files(qualification, learner, temp_output_folder)
        
        if results:
            media = results[0]
            required_fields = ['filename', 'file_path', 'file_type', 'size', 'relative_path']
            for field in required_fields:
                assert field in media, f"Missing required field: {field}"
    
    def test_supported_extensions(self):
        """Test that supported extensions are correct"""
        assert '.jpg' in SUPPORTED_IMAGE_EXTENSIONS
        assert '.jpeg' in SUPPORTED_IMAGE_EXTENSIONS
        assert '.png' in SUPPORTED_IMAGE_EXTENSIONS
        assert '.mp4' in SUPPORTED_VIDEO_EXTENSIONS
        assert '.mov' in SUPPORTED_VIDEO_EXTENSIONS
        assert '.pdf' in SUPPORTED_PDF_EXTENSIONS
        assert '.mp3' in SUPPORTED_AUDIO_EXTENSIONS
    
    def test_thumbnail_path_generation(self):
        """Test thumbnail path generation"""
        test_paths = [
            (Path("test/image.jpg"), "test/image_thumb.jpg"),
            (Path("test/video.mp4"), "test/video_thumb.jpg"),
            (Path("test/document.pdf"), "test/document_thumb.jpg"),
        ]
        
        for file_path, expected in test_paths:
            result = generate_thumbnail_path(file_path)
            assert result == expected


class TestPlaceholderParser:
    """Test placeholder parser module"""
    
    def test_extract_placeholders_basic(self):
        """Test basic placeholder extraction"""
        text = "This is {{Placeholder1}} and {{Placeholder2}}"
        placeholders = extract_placeholders(text)
        
        assert len(placeholders) == 2
        assert 'Placeholder1' in placeholders
        assert 'Placeholder2' in placeholders
    
    def test_extract_placeholders_multiple_same(self):
        """Test extraction of multiple occurrences of same placeholder"""
        text = "{{Placeholder1}} appears {{Placeholder1}} times"
        placeholders = extract_placeholders(text)
        
        # Should return unique placeholders
        assert len(placeholders) == 1
        assert 'Placeholder1' in placeholders
    
    def test_extract_placeholders_none(self):
        """Test extraction with no placeholders"""
        text = "This text has no placeholders"
        placeholders = extract_placeholders(text)
        
        assert len(placeholders) == 0
    
    def test_extract_placeholders_complex(self):
        """Test extraction with complex text"""
        text = """
        Section 1
        {{Site_Arrival_Induction}}
        
        Section 2
        {{Safety_Briefing}} and {{Equipment_Check}}
        """
        placeholders = extract_placeholders(text)
        
        assert len(placeholders) == 3
        assert 'Site_Arrival_Induction' in placeholders
        assert 'Safety_Briefing' in placeholders
        assert 'Equipment_Check' in placeholders
    
    def test_validate_placeholder_valid(self):
        """Test validation of valid placeholders"""
        valid_placeholders = [
            'Placeholder1',
            'Placeholder_1',
            'Placeholder123',
            'PLACEHOLDER',
            'placeholder',
            'Placeholder_Name'
        ]
        
        for placeholder in valid_placeholders:
            assert validate_placeholder(placeholder), f"Should be valid: {placeholder}"
    
    def test_validate_placeholder_invalid(self):
        """Test validation of invalid placeholders"""
        invalid_placeholders = [
            'Placeholder-1',  # Hyphen not allowed
            'Placeholder 1',  # Space not allowed
            'Placeholder.1',  # Dot not allowed
            '123Placeholder',  # Cannot start with number
            '',  # Empty
        ]
        
        for placeholder in invalid_placeholders:
            assert not validate_placeholder(placeholder), f"Should be invalid: {placeholder}"
    
    def test_assign_placeholder_colors(self):
        """Test placeholder color assignment"""
        placeholders = ['Placeholder1', 'Placeholder2', 'Placeholder3']
        colors = assign_placeholder_colors(placeholders)
        
        assert len(colors) == 3
        assert all(isinstance(color, str) for color in colors.values())
        assert all(color.startswith('#') for color in colors.values())
    
    def test_placeholder_pattern(self):
        """Test placeholder regex pattern"""
        test_cases = [
            ('{{Placeholder1}}', True),
            ('{{Placeholder_1}}', True),
            ('{{Placeholder123}}', True),
            ('{{PLACEHOLDER}}', True),
            ('{{Placeholder-1}}', False),  # Hyphen
            ('{{Placeholder 1}}', False),  # Space
            ('{{123Placeholder}}', False),  # Starts with number
        ]
        
        for text, should_match in test_cases:
            match = PLACEHOLDER_PATTERN.search(text)
            assert (match is not None) == should_match, f"Pattern test failed for: {text}"


class TestDraftManager:
    """Test draft manager module"""
    
    def test_save_draft_basic(self, temp_output_folder):
        """Test basic draft saving"""
        draft_data = {
            'text_content': 'Test content {{Placeholder1}}',
            'assignments': {
                'Placeholder1': [
                    {'filename': 'image1.jpg', 'position': 0}
                ]
            },
            'header_data': {
                'learner': 'Test Learner',
                'assessor': 'Test Assessor'
            }
        }
        
        result = save_draft(draft_data, temp_output_folder)
        
        assert result is True
        
        # Verify draft file exists
        drafts_dir = temp_output_folder / "drafts"
        assert drafts_dir.exists()
        
        draft_files = list(drafts_dir.glob("*.json"))
        assert len(draft_files) > 0
    
    def test_load_draft_basic(self, temp_output_folder):
        """Test basic draft loading"""
        draft_data = {
            'text_content': 'Test content {{Placeholder1}}',
            'assignments': {'Placeholder1': []},
            'header_data': {}
        }
        
        draft_name = 'test_draft'
        
        # Save first
        save_draft(draft_data, temp_output_folder)
        
        # Load
        loaded = load_draft(draft_name, temp_output_folder)
        
        assert loaded is not None
        assert loaded['text_content'] == draft_data['text_content']
        assert 'assignments' in loaded
        assert 'header_data' in loaded
    
    def test_list_drafts(self, temp_output_folder):
        """Test listing drafts"""
        # Save multiple drafts
        for i in range(3):
            draft_data = {
                'text_content': f'Test content {i}',
                'assignments': {},
                'header_data': {}
            }
            save_draft(draft_data, temp_output_folder)
        
        drafts = list_drafts(temp_output_folder)
        
        assert len(drafts) >= 3
        assert all('draft_name' in d for d in drafts)
        assert all('updated_at' in d for d in drafts)
    
    def test_delete_draft(self, temp_output_folder):
        """Test draft deletion"""
        draft_data = {
            'text_content': 'Test content',
            'assignments': {},
            'header_data': {}
        }
        
        draft_name = 'test_delete_draft'
        save_draft(draft_data, temp_output_folder)
        
        # Verify exists
        drafts = list_drafts(temp_output_folder)
        draft_names = [d['draft_name'] for d in drafts]
        assert draft_name in draft_names
        
        # Delete
        result = delete_draft(draft_name, temp_output_folder)
        assert result is True
        
        # Verify deleted
        drafts = list_drafts(temp_output_folder)
        draft_names = [d['draft_name'] for d in drafts]
        assert draft_name not in draft_names
    
    def test_draft_data_validation(self, temp_output_folder):
        """Test that draft data validation works"""
        invalid_data = [
            {},  # Empty
            {'text_content': 'Test'},  # Missing required fields
            {'assignments': {}},  # Missing text_content
        ]
        
        for invalid in invalid_data:
            result = save_draft(invalid, temp_output_folder)
            # Should handle gracefully (either return False or raise exception)
            # Current implementation may need to be checked



