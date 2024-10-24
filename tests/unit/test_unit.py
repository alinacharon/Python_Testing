import pytest
from unittest.mock import patch, Mock
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_showSummary_club_found(client):
    test_clubs = [
        {
            'name': 'Test Club',
            'email': 'test@club.com',
            'points': '100'
        }
    ]
    
    test_competitions = [
        {
            'name': 'Test Competition',
            'date': '2024-01-01',
            'numberOfPlaces': '25'
        }
    ]
    
    with patch('server.clubs', test_clubs):
        with patch('server.competitions', test_competitions):
            response = client.post(
                '/showSummary',
                data={'email': 'test@club.com'},
                follow_redirects=True
            )
            
            assert response.status_code == 200
            assert b'Welcome, test@club.com' in response.data
            assert b'Points available: 100' in response.data
            assert b'Test Competition' in response.data
            assert b'Number of Places: 25' in response.data

def test_showSummary_club_not_found(client):
    with patch('server.clubs', []):
        response = client.post(
            '/showSummary',
            data={'email': 'unknown@club.com'}
        )
        
        assert response.status_code == 302
        assert response.location == '/'

def test_showSummary_get_request(client):
    response = client.get('/showSummary')
    assert response.status_code == 405

def test_showSummary_session_data(client):
    test_clubs = [
        {
            'name': 'Test Club',
            'email': 'test@club.com',
            'points': '100'
        }
    ]
    
    test_competitions = [
        {
            'name': 'Test Competition',
            'date': '2024-01-01',
            'numberOfPlaces': '25'
        }
    ]
    
    with patch('server.clubs', test_clubs):
        with patch('server.competitions', test_competitions):
            with client.session_transaction() as session:
                session['email'] = 'test@club.com'
            
            response = client.post(
                '/showSummary',
                data={'email': 'test@club.com'},
                follow_redirects=True
            )
            
            assert response.status_code == 200
            assert b'Welcome, test@club.com' in response.data
            assert b'Points available: 100' in response.data