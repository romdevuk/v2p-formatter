"""
Backend tests for bulk video selection feature
Stage 1: Validation and batch info endpoints
"""
import pytest
import json
from pathlib import Path
from app import create_app
from config import OUTPUT_FOLDER

@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_video_paths():
    """Get sample video paths for testing"""
    # This will need to be updated with actual test video paths
    # For now, return empty list - tests will be skipped if no videos
    videos = []
    if OUTPUT_FOLDER.exists():
        for mp4_file in OUTPUT_FOLDER.rglob('*.mp4'):
            videos.append(str(mp4_file))
            if len(videos) >= 3:  # Only need a few for testing
                break
    return videos

class TestBatchVideoInfo:
    """Tests for /batch_video_info endpoint"""
    
    def test_batch_video_info_no_paths(self, client):
        """Test with no video paths"""
        response = client.post('/v2p-formatter/batch_video_info',
                              json={'video_paths': []},
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_batch_video_info_invalid_format(self, client):
        """Test with invalid format (not array)"""
        response = client.post('/v2p-formatter/batch_video_info',
                              json={'video_paths': 'not-an-array'},
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_batch_video_info_exceeds_limit(self, client):
        """Test with more than 20 videos"""
        video_paths = [f'/fake/path/video_{i}.mp4' for i in range(21)]
        response = client.post('/v2p-formatter/batch_video_info',
                              json={'video_paths': video_paths},
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert '20' in data['error']
    
    @pytest.mark.skipif(not Path(OUTPUT_FOLDER).exists(), reason="No output folder")
    def test_batch_video_info_success(self, client, sample_video_paths):
        """Test successful batch video info retrieval"""
        if not sample_video_paths:
            pytest.skip("No sample videos available for testing")
        
        response = client.post('/v2p-formatter/batch_video_info',
                              json={'video_paths': sample_video_paths[:2]},
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'videos' in data
        assert 'errors' in data
        assert len(data['videos']) > 0
        assert 'duration' in data['videos'][0]
        assert 'width' in data['videos'][0]
        assert 'height' in data['videos'][0]
    
    def test_batch_video_info_missing_file(self, client):
        """Test with missing video file"""
        fake_path = str(OUTPUT_FOLDER / 'nonexistent_video.mp4')
        response = client.post('/v2p-formatter/batch_video_info',
                              json={'video_paths': [fake_path]},
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['errors']) > 0
        assert data['failed'] > 0

class TestValidateBatchTimePoints:
    """Tests for /validate_batch_time_points endpoint"""
    
    def test_validate_no_video_paths(self, client):
        """Test with no video paths"""
        response = client.post('/v2p-formatter/validate_batch_time_points',
                              json={'video_paths': [], 'time_points': [10, 20, 30]},
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_validate_no_time_points(self, client):
        """Test with no time points"""
        response = client.post('/v2p-formatter/validate_batch_time_points',
                              json={'video_paths': ['/fake/path/video.mp4'], 'time_points': []},
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_validate_invalid_time_points_format(self, client):
        """Test with invalid time points format"""
        response = client.post('/v2p-formatter/validate_batch_time_points',
                              json={'video_paths': ['/fake/path/video.mp4'], 'time_points': 'not-an-array'},
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_validate_invalid_time_points_values(self, client):
        """Test with non-numeric time points"""
        response = client.post('/v2p-formatter/validate_batch_time_points',
                              json={'video_paths': ['/fake/path/video.mp4'], 'time_points': ['not', 'numbers']},
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_validate_exceeds_limit(self, client):
        """Test with more than 20 videos"""
        video_paths = [f'/fake/path/video_{i}.mp4' for i in range(21)]
        response = client.post('/v2p-formatter/validate_batch_time_points',
                              json={'video_paths': video_paths, 'time_points': [10, 20, 30]},
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert '20' in data['error']
    
    @pytest.mark.skipif(not Path(OUTPUT_FOLDER).exists(), reason="No output folder")
    def test_validate_valid_time_points(self, client, sample_video_paths):
        """Test validation with valid time points"""
        if not sample_video_paths:
            pytest.skip("No sample videos available for testing")
        
        # Use small time points that should be valid
        time_points = [1.0, 2.0, 3.0]
        
        response = client.post('/v2p-formatter/validate_batch_time_points',
                              json={'video_paths': sample_video_paths[:2], 'time_points': time_points},
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'results' in data
        assert len(data['results']) == 2
        
        # Check that results have expected structure
        for result in data['results']:
            assert 'video_path' in result
            assert 'valid' in result
            assert 'warnings' in result
    
    @pytest.mark.skipif(not Path(OUTPUT_FOLDER).exists(), reason="No output folder")
    def test_validate_invalid_time_points(self, client, sample_video_paths):
        """Test validation with time points exceeding duration"""
        if not sample_video_paths:
            pytest.skip("No sample videos available for testing")
        
        # Use very large time points that will exceed duration
        time_points = [999999.0, 888888.0]
        
        response = client.post('/v2p-formatter/validate_batch_time_points',
                              json={'video_paths': sample_video_paths[:1], 'time_points': time_points},
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'results' in data
        assert len(data['results']) > 0
        
        # Should have warnings about invalid time points
        assert data['has_warnings'] is True
        result = data['results'][0]
        assert len(result.get('warnings', [])) > 0

class TestSequentialExtraction:
    """Tests for sequential batch extraction (Stage 2)"""
    
    @pytest.mark.skipif(not Path(OUTPUT_FOLDER).exists(), reason="No output folder")
    def test_sequential_extraction_flow(self, client, sample_video_paths):
        """Test that existing extract_frames endpoint works for sequential processing"""
        if not sample_video_paths or len(sample_video_paths) < 2:
            pytest.skip("Need at least 2 videos for sequential extraction test")
        
        time_points = [1.0, 2.0]
        quality = 95
        resolution = '640x480'
        
        # Process first video
        response1 = client.post('/v2p-formatter/extract_frames',
                               json={
                                   'video_path': sample_video_paths[0],
                                   'time_points': time_points,
                                   'quality': quality,
                                   'resolution': resolution
                               },
                               content_type='application/json')
        
        # Process second video
        response2 = client.post('/v2p-formatter/extract_frames',
                               json={
                                   'video_path': sample_video_paths[1],
                                   'time_points': time_points,
                                   'quality': quality,
                                   'resolution': resolution
                               },
                               content_type='application/json')
        
        # Both should succeed
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        
        assert data1['success'] is True
        assert data2['success'] is True
        assert 'images' in data1
        assert 'images' in data2


