from music.adapters.repository import AbstractRepository


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass

def get_tracks_by_album(title: str, repo: AbstractRepository):
    match_tracks = repo.get_tracks_by_album(title)
    return match_tracks

def get_tracks_by_artist(full_name: str, repo: AbstractRepository):
    match_tracks = repo.get_tracks_by_artist(full_name)
    return match_tracks

def get_tracks_by_genre(genre_name: str, repo: AbstractRepository):
    match_tracks = repo.get_tracks_by_genre(genre_name)
    return match_tracks

def get_tracks(repo: AbstractRepository):
    trackslist = repo.get_tracks()
    return trackslist

def get_tracks_by_id(id_list, repo: AbstractRepository):
    tracks = repo.get_tracks_by_id(id_list)
    return tracks

def get_tracks_by_name(name: str, repo: AbstractRepository):
    match_track = repo.get_track_by_name(name)
    return match_track