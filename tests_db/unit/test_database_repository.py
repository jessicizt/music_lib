from datetime import date, datetime

import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.adapters.repository import RepositoryException
from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user1 = User('dave', '123456789')
    repo.add_user(user1)
    user2 = User('bom', 'asdfwefagsaf')
    repo.add_user(user2)
    user3 = User('lisa', '41825adfasv')
    repo.add_user(user3)
    assert repo.get_user('dave') is user1
    assert user2 == User('bom', 'asdfwefagsaf')
    assert user3 != User('bom', 'asdfwefagsaf')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_add_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = Track(1,"Just")
    repo.add_track(track)

    assert repo.get_track(1) == track

def test_repository_can_retrieve_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track(2)
    assert track.title == 'Food'

def test_repository_does_not_retrieve_a_non_existent_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track(1)
    assert track is None

def test_repostory_can_retrieve_all_tracks(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks()
    assert len(tracks) == 2000

def test_repository_can_retrieve_articles_by_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks_by_album('Niris')
    assert tracks

def test_repository_can_retrieve_articles_by_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks_by_artist('AWOL')
    assert tracks

def test_repository_can_retrieve_articles_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks_by_genre('Hip-Hop')
    assert tracks

def test_repository_can_retrieve_albums(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    albums = repo.get_albums()
    assert len(albums) == 427

def test_repository_can_retrieve_artists(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artists = repo.get_artists()
    assert len(artists) == 263

def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genres = repo.get_genres()
    assert len(genres) == 60    

def test_repository_can_get_first_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_first_track()
    assert track.title == 'Food'

def test_repository_can_get_last_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_last_track()
    assert track.title == 'yet to be titled'

def test_repository_can_get_track_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks_by_id([10, 20, 30])

    assert len(tracks) == 3
    assert tracks[
               0].title == 'Freeway'
    assert tracks[1].title == "Spiritual Level"
    assert tracks[2].title == 'Too Happy'

def test_repository_does_not_retrieve_track_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_tracks_by_id([10, 15])

    assert len(articles) == 1
    assert articles[
               0].title == 'Freeway'

def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_tracks_by_id([0, 12])

    assert len(articles) == 0

def test_repository_can_add_a_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album = Album(6,"Flower")
    repo.add_album(album)

    assert album in repo.get_albums()

def test_repository_can_add_a_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist = Artist(9,"BTS")
    repo.add_artist(artist)

    assert artist in repo.get_artists()

def test_repository_can_add_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre(27,"Minority Music")
    repo.add_genre(genre)

    assert genre in repo.get_genres()

def test_repository_can_add_a_comment(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track(2)
    comment = Review(track,"Trump's onto it!", 4)

    repo.add_review(comment)

    assert comment in repo.get_reviews()

