import pytest
from server import loadClubs, loadCompetitions

def test_loadClubs():
    clubs = loadClubs()
    assert isinstance(clubs, list)
    assert len(clubs) > 0
    assert 'name' in clubs[0]
    assert 'email' in clubs[0]

def test_loadCompetitions():
    competitions = loadCompetitions()
    assert isinstance(competitions, list)
    assert len(competitions) > 0
    assert 'name' in competitions[0]
    assert 'numberOfPlaces' in competitions[0]