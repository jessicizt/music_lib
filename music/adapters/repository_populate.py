from pathlib import Path
from music.adapters import csvdatareader

from music.adapters.repository import AbstractRepository

def load_data(data_path: Path, repo: AbstractRepository):
    album_filename = str(Path(data_path) / "raw_albums_excerpt.csv")
    track_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")
    data = csvdatareader.TrackCSVReader(albums_csv_file=album_filename,tracks_csv_file=track_filename)
    tracks = csvdatareader.TrackCSVReader(albums_csv_file=album_filename,tracks_csv_file=track_filename).read_csv_files()

    for track in tracks:
        repo.add_track(track)
        if track.artist not in repo.get_artists():
            repo.add_artist(track.artist)
        for genre in track.genres:
            if genre not in repo.get_genres():
                repo.add_genre(genre)

    dict = data.read_albums_file_as_dict()
    for album in dict.values():
            repo.add_album(album)

    rows = data.read_tracks_file()
    for row in rows:
        album_id = int(row['album_id']) if row['album_id'].isdigit() else None
        track_album = dict[album_id] if album_id in dict else None
        track.album = track_album



def populate(data_path: Path, repo: AbstractRepository):
    # Load data into the repository.
    load_data(data_path, repo)