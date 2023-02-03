import pytest


from sqlalchemy.exc import IntegrityError

from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.review import Review
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre

def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks VALUES (139, "Shine A Light", "http://freemusicarchive.org/music/Abominog/mp3_1_1535", 230, 60, 5 )'
    )
    row = empty_session.execute('SELECT track_id from tracks').fetchone()
    return row[0]


def insert_album(empty_session):
    empty_session.execute(
        'INSERT INTO albums (album_id, title) VALUES (13, "X")'
    )
    row = empty_session.execute('SELECT album_id from albums').fetchone()
    return row[0]

def insert_artist(empty_session):
    empty_session.execute(
        'INSERT INTO artists (artist_id, full_name) VALUES (8, "Epik High")'
    )
    row = empty_session.execute('SELECT artist_id from artists').fetchone()
    return row[0]

def insert_genre(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_id, genre_name) VALUES (3, "Kpop")'
    )
    row = empty_session.execute('SELECT genre_id from genres').fetchone()
    return row[0]

def insert_reviewed_track(empty_session):
    track_key = insert_track(empty_session)

    empty_session.execute(
        'INSERT INTO reviews (track_id, review_text, rating) VALUES '
        '(:track_id, "Comment 1", 2),'
        '(:track_id, "Comment 2", 3)',
        {'track_id': track_key}
    )

    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]


def make_track():
    track = Track(139,"Shine A Light")
    return track


def make_user():
    user = User("Andrew", "111")
    return user


def make_ablum():
    album = Album(13,"X")
    return album

def make_artist():
    artist = Artist(8,"Epik High")
    return artist

def make_genre():
    genre = Genre(3,"Kpop")
    return genre

def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew", "1234"))
    users.append(("cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("andrew", "1234"),
        User("cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_track(empty_session):
    track_key = insert_track(empty_session)
    expected_track = make_track()
    fetched_track = empty_session.query(Track).one()

    assert expected_track == fetched_track
    assert track_key == fetched_track.track_id


def test_loading_of_album(empty_session):
    album_key = insert_album(empty_session)
    expected_album = make_ablum()
    fetched_album = empty_session.query(Album).one()

    assert expected_album == fetched_album
    assert album_key == fetched_album.album_id

def test_loading_of_genre(empty_session):
    genre_key = insert_genre(empty_session)
    expected_genre = make_genre()
    fetched_genre = empty_session.query(Genre).one()

    assert expected_genre == fetched_genre
    assert genre_key == fetched_genre.genre_id

def test_loading_of_artist(empty_session):
    artist_key = insert_artist(empty_session)
    expected_artist = make_artist()
    fetched_artist = empty_session.query(Artist).one()

    assert expected_artist == fetched_artist
    assert artist_key == fetched_artist.artist_id

def test_saving_of_review(empty_session):
    track_key = insert_track(empty_session)

    rows = empty_session.query(Track).all()
    track = rows[0]

    comment_text = "Some comment text."
    review = Review(track, comment_text, 4)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT track_id, review_text, rating FROM reviews'))

    assert rows == [(track_key, comment_text, 4)]


def test_saving_of_track(empty_session):
    track = make_track()
    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT track_id, title FROM tracks'))
    assert rows == [(139,"Shine A Light")]

def test_saving_of_album(empty_session):
    album = make_ablum()
    empty_session.add(album)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT album_id, title FROM albums'))
    assert rows == [(13,"X")]

def test_saving_of_artist(empty_session):
    artist = make_artist()
    empty_session.add(artist)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT artist_id, full_name FROM artists'))
    assert rows == [(8,"Epik High")]

def test_saving_of_genre(empty_session):
    genre = make_genre()
    empty_session.add(genre)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT genre_id, genre_name FROM genres'))
    assert rows == [(3,"Kpop")]
