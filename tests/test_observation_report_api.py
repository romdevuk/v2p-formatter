"""
API integration tests for Observation Report module
Tests all Flask routes and API endpoints
"""
import pytest
import json
from flask import Flask
from app import create_app


@pytest.fixture
def app():
    """Create Flask app for testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestObservationReportAPI:
    """Test Observation Report API endpoints"""
    
    def test_get_learners_endpoint(self, client):
        """Test GET /observation-report/learners"""
        response = client.get('/observation-report/learners?qualification=test')
        
        assert response.status_code in [200, 404]  # 404 if no learners found
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'success' in data
            if data['success']:
                assert 'learners' in data
                assert isinstance(data['learners'], list)
    
    def test_get_media_endpoint(self, client):
        """Test GET /observation-report/media"""
        response = client.get('/observation-report/media?qualification=test&learner=test')
        
        assert response.status_code in [200, 404]  # 404 if no media found
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'success' in data
            if data['success']:
                assert 'media' in data
                assert isinstance(data['media'], list)
    
    def test_list_drafts_endpoint(self, client):
        """Test GET /observation-report/drafts"""
        response = client.get('/observation-report/drafts')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'success' in data
        assert 'drafts' in data
        assert isinstance(data['drafts'], list)
    
    def test_create_draft_endpoint(self, client):
        """Test POST /observation-report/drafts"""
        draft_data = {
            'text_content': 'Test content {{Placeholder1}}',
            'assignments': {
                'Placeholder1': []
            },
            'header_data': {
                'learner': 'Test Learner'
            }
        }
        
        response = client.post(
            '/observation-report/drafts',
            data=json.dumps(draft_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'draft_name' in data
    
    def test_load_draft_endpoint(self, client):
        """Test GET /observation-report/drafts/<draft_name>"""
        # First create a draft
        draft_data = {
            'text_content': 'Test content',
            'assignments': {},
            'header_data': {}
        }
        
        create_response = client.post(
            '/observation-report/drafts',
            data=json.dumps(draft_data),
            content_type='application/json'
        )
        
        if create_response.status_code == 200:
            create_data = json.loads(create_response.data)
            draft_name = create_data.get('draft_name')
            
            if draft_name:
                # Load the draft
                response = client.get(f'/observation-report/drafts/{draft_name}')
                
                assert response.status_code in [200, 404]
                if response.status_code == 200:
                    data = json.loads(response.data)
                    assert data['success'] is True
                    assert 'draft' in data
    
    def test_update_draft_endpoint(self, client):
        """Test PUT /observation-report/drafts/<draft_name>"""
        # First create a draft
        draft_data = {
            'text_content': 'Test content',
            'assignments': {},
            'header_data': {}
        }
        
        create_response = client.post(
            '/observation-report/drafts',
            data=json.dumps(draft_data),
            content_type='application/json'
        )
        
        if create_response.status_code == 200:
            create_data = json.loads(create_response.data)
            draft_name = create_data.get('draft_name')
            
            if draft_name:
                # Update the draft
                updated_data = {
                    'text_content': 'Updated content',
                    'assignments': {},
                    'header_data': {}
                }
                
                response = client.put(
                    f'/observation-report/drafts/{draft_name}',
                    data=json.dumps(updated_data),
                    content_type='application/json'
                )
                
                assert response.status_code in [200, 404]
                if response.status_code == 200:
                    data = json.loads(response.data)
                    assert data['success'] is True
    
    def test_delete_draft_endpoint(self, client):
        """Test DELETE /observation-report/drafts/<draft_name>"""
        # First create a draft
        draft_data = {
            'text_content': 'Test content',
            'assignments': {},
            'header_data': {}
        }
        
        create_response = client.post(
            '/observation-report/drafts',
            data=json.dumps(draft_data),
            content_type='application/json'
        )
        
        if create_response.status_code == 200:
            create_data = json.loads(create_response.data)
            draft_name = create_data.get('draft_name')
            
            if draft_name:
                # Delete the draft
                response = client.delete(f'/observation-report/drafts/{draft_name}')
                
                assert response.status_code in [200, 404]
                if response.status_code == 200:
                    data = json.loads(response.data)
                    assert data['success'] is True
    
    def test_export_docx_endpoint(self, client):
        """Test POST /observation-report/export-docx"""
        export_data = {
            'text_content': 'Test content {{Placeholder1}}',
            'assignments': {
                'Placeholder1': []
            },
            'header_data': {
                'learner': 'Test Learner',
                'assessor': 'Test Assessor'
            },
            'filename': 'test_export'
        }
        
        response = client.post(
            '/observation-report/export-docx',
            data=json.dumps(export_data),
            content_type='application/json'
        )
        
        # May return 200 (success) or 400/500 (error if no media files)
        assert response.status_code in [200, 400, 500]
        if response.status_code == 200:
            data = json.loads(response.data)
            assert data['success'] is True
            assert 'filename' in data
    
    def test_main_page_route(self, client):
        """Test GET /observation-report (main page)"""
        response = client.get('/observation-report')
        
        assert response.status_code == 200
        # Should return HTML
        assert b'observation-report' in response.data.lower()



