import pytest

from music.authentication.services import AuthenticationException
from music.comment import services as comment_services
from music.authentication import services as auth_services
from music.content import services as content_services
from music.domainmodel import review
from music.domainmodel.track import Track


def test_user(in_memory_repo):
    new_user_name1 = 'jz'
    new_password1 = 'abcd1A23'
    new_user_name2 = 'thorke'
    new_password2 = 'abcd1234'

    auth_services.add_user(new_user_name1, new_password1, in_memory_repo)
    auth_services.add_user(new_user_name2, new_password2, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name1, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name1

    assert user_as_dict['password'].startswith('pbkdf2:sha256:')
    assert auth_services.get_user(new_user_name1,in_memory_repo)

def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)

def test_get_tracks(in_memory_repo):
    track_ids = [2,3,4]
    target_tracks = content_services.get_tracks_by_id(track_ids,in_memory_repo)
    assert str(target_tracks) == '[<Track Food, track id = 2>, <Track Electric Ave, track id = 3>]'

def test_add_review_and_get_reiviews(in_memory_repo):
    add_review = review.Review(Track(2,'Food'),'Great!',3)
    in_memory_repo.add_review(add_review)
    reviews = in_memory_repo.get_reviews()
    assert reviews == [add_review]

def test_get_tracks_by_album(in_memory_repo):
    match_tracks = content_services.get_tracks_by_album('30th Anniversary Blah Blah Blah',in_memory_repo)
    assert Track(333,'Blah intro') in match_tracks
    assert Track(335,'Bored') in match_tracks
    assert Track(2,'food') not in match_tracks

def test_get_tracks_by_artist(in_memory_repo):
    match_tracks = content_services.get_tracks_by_artist('EKG',in_memory_repo)
    assert Track(615,'Immaterial, side A') in match_tracks
    assert Track(616,'Immaterial, side B') in match_tracks
    assert Track(2,'food') not in match_tracks

def test_get_tracks_by_genre(in_memory_repo):
    match_tracks = content_services.get_tracks_by_genre('Rock',in_memory_repo)
    assert Track(250,'Smoovebiz') in match_tracks
    assert Track(253,'New Life') in match_tracks
    assert Track(2,'food') not in match_tracks
