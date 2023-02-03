from bisect import bisect_left, insort_left
import csv
from datetime import datetime
from pathlib import Path

from typing import List

from werkzeug.security import generate_password_hash
from music.adapters import csvdatareader

from music.adapters.repository import AbstractRepository,RepositoryException
from music.domainmodel import album,artist,track,user,review,genre

class MemoryRepository(AbstractRepository):
    # Tracks are categorized by album or artist or genre, not id. id is assumed unique.


    def __init__(self):
        self.__tracks = list()
        self.__tracks_index = dict()
        self.__albums = set()
        self.__artists = set()
        self.__genres = set()
        self.__users = list()
        self.__reviews = list()

    def add_user(self, user: user.User):
        self.__users.append(user)

    def get_user(self, user_name) -> user.User:
        return next((user for user in self.__users if user.user_name == user_name), None)  # type: ignore

    def add_album(self, album: album.Album):
        self.__albums.add(album)

    def get_albums(self) -> set():  # type: ignore
        return self.__albums
    
    def add_artist(self, artist: artist.Artist):
        self.__artists.add(artist)

    def get_artists(self) -> set():  # type: ignore
        return self.__artists

    def add_genre(self, genre: genre.Genre):
        self.__genres.add(genre)

    def get_genres(self) -> set():  # type: ignore
        return self.__genres
    
    def add_track(self, track: track.Track):
        insort_left(self.__tracks, track)
        self.__tracks_index[track.track_id] = track

    def get_track(self, id: int) -> track.Track:
        track = None

        try:
            track = self.__tracks_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return track  # type: ignore

    def get_tracks(self) -> list():  # type: ignore
        return self.__tracks

    def get_tracks_by_album(self, title: str) -> List[track.Track]:
        target_album = None
        match_tracks = list()
        for album in self.__albums:
            if album.title == title:
                target_album = album
                
        for trackitem in self.__tracks:
            if trackitem.album == target_album:
                match_tracks.append(trackitem)
        return match_tracks

    def get_tracks_by_artist(self, full_name: str) -> List[track.Track]:
        target_artist = None
        match_tracks = list()
        for artist in self.__artists:
            if artist.full_name == full_name:
                target_artist = artist

        for trackitem in self.__tracks:
            if trackitem.artist == target_artist:
                match_tracks.append(trackitem)
        return match_tracks

    def get_tracks_by_genre(self, genre_name: str) -> List[track.Track]:
        target_genre = None
        match_tracks = list()
        for genre in self.__genres:
            if genre.name == genre_name:
                target_genre = genre

        for trackitem in self.__tracks:
            if target_genre in trackitem.genres:
                match_tracks.append(trackitem)

        return match_tracks

    def get_first_track(self):
        track = None

        if len(self.__tracks) > 0:
            track = self.__tracks[0]
        return track

    def get_last_track(self):
        track = None

        if len(self.__tracks) > 0:
            track = self.__tracks[-1]
        return track

    def get_tracks_by_id(self, id_list):
        existing_ids = [id for id in id_list if id in self.__tracks_index]

        tracks = [self.__tracks_index[id] for id in existing_ids]
        return tracks

    def add_review(self, review: review.Review):
        self.__reviews.append(review)
            
    def get_reviews(self) -> List[review.Review]:
        return self.__reviews
