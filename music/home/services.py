from music.adapters.repository import AbstractRepository


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass

def get_albums(repo: AbstractRepository):
    albumslist=repo.get_albums()
    return albumslist

def get_artists(repo: AbstractRepository):
    artistslist=repo.get_artists()
    return artistslist

def get_genres(repo: AbstractRepository):
    genreslist=repo.get_genres();
    return genreslist