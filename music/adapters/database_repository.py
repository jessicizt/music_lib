from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.track import Track

from music.domainmodel.user import User
from music.adapters.repository import AbstractRepository

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def get_albums(self) -> set():
        albums = self._session_cm.session.query(Album).all()
        return albums

    def add_album(self, album: Album):
        with self._session_cm as scm:
            scm.session.merge(album)
            scm.commit()

    def get_artists(self) -> set():
        artists = self._session_cm.session.query(Artist).all()
        return artists

    def add_artist(self, artist: Artist):
        with self._session_cm as scm:
            scm.session.merge(artist)
            scm.commit()

    def get_genres(self) -> set():
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.merge(track)
            scm.commit()

    def get_track(self, track_id: int) -> Track:
        track = None
        try:
            track = self._session_cm.session.query(Track).filter(Track._Track__track_id == track_id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return track

    def get_tracks(self) -> list():
        tracks = self._session_cm.session.query(Track).all()
        return tracks

    def get_track_by_name(self, name: str) -> List[Track]:
        track = None
        match_tracks = list()
        for track in self.get_tracks():
            if track.title == name:
                match_tracks.append(track)
        return match_tracks

    def get_tracks_by_album(self, title: str) -> List[Track]:
        target_album = None
        match_tracks = list()
        for album in self.get_albums():
            if album.title == title:
                target_album = album
                
        for trackitem in self.get_tracks():
            if trackitem.album == target_album:
                match_tracks.append(trackitem)
        return match_tracks

    def get_tracks_by_artist(self, full_name: str) -> List[Track]:
        target_artist = None
        match_tracks = list()
        for artist in self.get_artists():
            if artist.full_name == full_name:
                target_artist = artist

        for trackitem in self.get_tracks():
            if trackitem.artist == target_artist:
                match_tracks.append(trackitem)
        return match_tracks

    def get_tracks_by_genre(self, genre_name: str) -> List[Track]:
        target_genre = None
        match_tracks = list()
        for genre in self.get_genres():
            if genre.name == genre_name:
                target_genre = genre

        for trackitem in self.get_tracks():
            if target_genre in trackitem.genres:
                match_tracks.append(trackitem)

        return match_tracks

    def get_first_track(self):
        track = self._session_cm.session.query(Track).first()
        return track

    def get_last_track(self):
        track = self._session_cm.session.query(Track).order_by(desc(Track._Track__track_id)).first()
        return track

    def get_tracks_by_id(self, id_list: List[int]):
        tracks = self._session_cm.session.query(Track).filter(Track._Track__track_id.in_(id_list)).all()
        return tracks
        
    def get_reviews(self) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()
            

