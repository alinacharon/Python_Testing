import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '20'
    })
    assert response.status_code == 200
    assert b'There is not enough space or points for your booking' in response.data
    
def test_purchase_negative_amount_places(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '-5'
    })
    assert response.status_code == 200
    assert b'The purchase quantity is invalid' in response.data