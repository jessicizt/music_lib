import pytest

from flask import session


def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == '/authentication/login'



def test_login_and_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'The Music Library' in response.data


def test_login_required_to_comment(client):
    response = client.post('track/2')
    assert response.headers['Location'] == '/authentication/login'


def test_comment(client, auth):
    # Login a user.
    auth.login()
    # Check that we can retrieve the comment page.
    response = client.get('track/2')
    response = client.post(
        "track/2",
        data={'comment': 'Who needs quarantine?', 'rating': 2}
    )
    assert response.headers['Location'] == '/authentication/login'


def test_tracks(client):
    response = client.get('content/tracks')
    assert response.status_code == 200
    assert b'Peel Back The Mountain Sky' in response.data


def test_search(client):
    status_code = client.get('/content/search').status_code
    assert status_code == 200
    response = client.post(
        '/content/search',
        data={'keyword': 'One Mind'}
    )
    assert b'Angels Fear To Tread' in response.data
    assert b'539' in response.data
    assert b'Sweet Words' in response.data
    assert b'545' in response.data
    





