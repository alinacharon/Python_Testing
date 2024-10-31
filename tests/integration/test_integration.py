import pytest
from urllib.parse import urlparse
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data


def test_showSummary_valid_email(client):
    response = client.post(
        '/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'Welcome, john@simplylift.co' in response.data


def test_showSummary_invalid_email(client):
    response = client.post('/showSummary', data={'email': 'invalid@email.com'})
    assert response.status_code == 302
    assert urlparse(response.headers['Location']).path == '/'


def test_book(client):
    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    assert b'Booking for Spring Festival' in response.data


def test_book_invalid_club(client):
    response = client.get('/book/Spring Festival/Invalid Club')
    assert response.status_code == 302
    assert urlparse(response.headers['Location']).path == '/'


def test_purchase_places(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '2'
    })
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data


def test_purchase_too_much_places(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Fall Classic',
        'club': 'Simply Lift',
        'places': '10'
    })
    assert response.status_code == 200
    assert b'There are not enough spaces or points for your booking' in response.data


def test_purchase_negative_amount_places(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '-5'
    })
    assert response.status_code == 200
    assert b'The number of places for booking is invalid' in response.data
    
def test_purchase_more_than_allowed_places(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '13'
    })
    assert response.status_code == 200
    assert b'You can&#39;t book more than 12 places.' in response.data


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302
    assert urlparse(response.headers['Location']).path == '/'
