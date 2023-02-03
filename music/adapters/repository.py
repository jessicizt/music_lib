import abc
from typing import List

from music.domainmodel import album,artist,track,playlist,user,review,genre

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):


    @abc.abstractmethod
    def add_user(self, user: user.User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> user.User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_album(self, album: album.Album):
        """" Adds a Album to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_albums(self) -> set():  # type: ignore
        """ Returns the Album named title from the repository.

        If there is no Album with the given title, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_artist(self, artist: artist.Artist):
        """" Adds a Artist to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_artists(self) -> set():  # type: ignore
        """ Returns the Artist named full_name from the repository.

        If there is no Artist with the given full_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: genre.Genre):
        """" Adds a Genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> set():  # type: ignore
        """ Returns the Genre named genre_name from the repository.

        If there is no Genre with the given genre_name, this method returns empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track: track.Track):
        """" Adds a Track to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track(self, id: int) -> track.Track:
        """ Returns Track with id from the repository.

        If there is no Track with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_by_name(self, name: str) -> List[track.Track]:
        """ Returns Track with name from the repository.

        If there is no Track with the given name, this method returns empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks(self) -> List[track.Track]:
        """Returns the list of Track from the repository.

        If there is no track with the list, this method returns None.
        """

    @abc.abstractmethod
    def get_tracks_by_album(self, title: str) -> List[track.Track]:
        """ Returns a list of Tracks, whose have same album name, from the repository.

        If there are not Tracks that are tagged by album, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_artist(self, full_name: str) -> List[track.Track]:
        """ Returns a list of Tracks, whose is from same artist, from the repository.

        If there are not Tracks that are pulishied by artist, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_genre(self, genre_name: str) -> List[track.Track]:
        """ Returns a list of Tracks, whose is from same genre, from the repository.

        If there are not Tracks that are tagged by genre, this method returns an empty list.
        """
        raise NotImplementedError
        
    @abc.abstractmethod
    def get_first_track(self) -> track.Track:
        """ Returns the first Article, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_track(self) -> track.Track:
        """ Returns the last Article, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_id(self, id_list):
        """ Returns a list of Articles, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError
        
    @abc.abstractmethod
    def add_review(self, review: review.Review):
        """ Adds a Review to the repository.

        If the Review doesn't have directional links with a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if user.User.user_name is None or review not in user.User.reviews:  # type: ignore
            raise RepositoryException('Review not correctly attached to a User')

    @abc.abstractmethod
    def get_reviews(self) -> List[review.Review]:
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

    