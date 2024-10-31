import pytest
from unittest.mock import patch
from server import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def test_clubs():
    return [
        {
            'name': 'Test Club',
            'email': 'test@club.com',
            'points': '100'
        }
    ]


@pytest.fixture
def test_competitions():
    return [
        {
            'name': 'Test Competition',
            'date': '2024-01-01',
            'numberOfPlaces': '25'
        }
    ]


def test_showSummary_get_request(client):
    response = client.get('/showSummary')
    assert response.status_code == 405


def test_showSummary_session_data(client, test_clubs, test_competitions):
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


def test_showSummary_club_found(client, test_clubs, test_competitions):
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


def test_showSummary_club_not_found(client, test_clubs):
    with patch('server.clubs', test_clubs):
        response = client.post(
            '/showSummary',
            data={'email': 'unknown@club.com'}
        )

        assert response.status_code == 302
        assert response.location == '/'

@patch('builtins.open', side_effect=FileNotFoundError)
def test_load_clubs_file_not_found(mock_open):
    with patch('os.path.exists', return_value=False):
        with patch('server.flash') as mock_flash:
            clubs = loadClubs()
            assert len(clubs) == 0
            mock_flash.assert_called_once_with("No data of clubs found.")
            
@patch('builtins.open', side_effect=FileNotFoundError)
def test_load_competition_file_not_found(mock_open):
    with patch('os.path.exists', return_value=False):
        with patch('server.flash') as mock_flash:
            competitions = loadCompetitions()
            assert len(competitions) == 0
            mock_flash.assert_called_once_with("No data of competitions found.")        