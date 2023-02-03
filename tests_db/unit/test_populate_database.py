from sqlalchemy import select, inspect

from music.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['albums','artists','genres','reviews','track_genres','tracks','users']

def test_database_populate_select_all_album(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_album_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table albums
        select_statement = select([metadata.tables[name_of_album_table]])
        result = connection.execute(select_statement)

        all_album_names = []
        for row in result:
            all_album_names.append(row['title'])

        assert len(all_album_names) == 427

def test_database_populate_select_all_artist(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_artist_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table artist
        select_statement = select([metadata.tables[name_of_artist_table]])
        result = connection.execute(select_statement)

        all_artist_names = []
        for row in result:
            all_artist_names.append(row['full_name'])

        assert len(all_artist_names) == 263

def test_database_populate_select_all_genre(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genre_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[name_of_genre_table]])
        result = connection.execute(select_statement)

        all_genre = []
        for row in result:
            all_genre.append(row['genre_id'])

        assert len(all_genre) == 60

def test_database_populate_select_all_track(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_tracks_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table tracks
        select_statement = select([metadata.tables[name_of_tracks_table]])
        result = connection.execute(select_statement)

        all_tracks = []
        for row in result:
            all_tracks.append((row['track_id'], row['title']))

        assert len(all_tracks) == 2000

        assert all_tracks[0] == (2, 'Food')
