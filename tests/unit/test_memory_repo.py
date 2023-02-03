import pytest
import os

from typing import List

from music.adapters.repository import RepositoryException
from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel import album,artist,playlist,review,genre
from music.adapters.csvdatareader import TrackCSVReader

def test_browse_tracks(in_memory_repo):
    track_list = in_memory_repo.get_tracks()
    assert len(track_list) == 2000

def test_browse_albums(in_memory_repo):
    album_set = in_memory_repo.get_albums()
    assert len(album_set) == 427

def test_browse_artists(in_memory_repo):
    artist_set = in_memory_repo.get_artists()
    assert len(artist_set) == 263

def test_browse_genres(in_memory_repo):
    genre_set = in_memory_repo.get_genres()
    assert len(genre_set) == 60

def test_get_track(in_memory_repo):
    track = in_memory_repo.get_track(2)
    assert track == Track(2,'Food')

def test_search_tracks_by_album(in_memory_repo):
    tracklist = in_memory_repo.get_tracks_by_album('Niris')
    assert len(tracklist) == 5

def test_search_tracks_by_artist(in_memory_repo):
    tracklist = in_memory_repo.get_tracks_by_artist('AWOL')
    assert len(tracklist) == 4

def test_search_tracks_by_genre(in_memory_repo):
    tracklist = in_memory_repo.get_tracks_by_genre('Hip-Hop')
    assert len(tracklist) == 41

def test_add_and_search_a_user(in_memory_repo):
    user1 = User('dave', '123456789')
    in_memory_repo.add_user(user1)
    user2 = User('bom', 'asdfwefagsaf')
    in_memory_repo.add_user(user2)
    user3 = User('lisa', '41825adfasv')
    in_memory_repo.add_user(user3)
    assert in_memory_repo.get_user('dave') is user1
    assert user2 == User('bom', 'asdfwefagsaf')
    assert user3 != User('bom', 'asdfwefagsaf')

    user = in_memory_repo.get_user('prince')
    assert user is None

def test_borwse_add_a_review_with_user(in_memory_repo):
    user1 = User('dave', '123456789')
    in_memory_repo.add_user(user1)
    add_review = review.Review(Track(2,'Food'),'Great!',3)
    in_memory_repo.add_review(add_review)
    reviews = in_memory_repo.get_reviews()
    assert reviews == [add_review]