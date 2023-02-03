from typing import Text
from sqlalchemy import (
    Table, MetaData, Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel import album,artist,track,review,user,genre

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.track_id')),
    Column('review_text', String(1024), nullable=False),
    Column('rating', Integer, nullable=False)
)

tracks_table = Table(
    'tracks', metadata,
    # Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', Integer, unique=True, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('track_url',String(255), nullable=True),
    Column('track_duration', Integer, nullable=True),
    Column('album_id',  ForeignKey('albums.album_id')),
    Column('artist_id', ForeignKey('artists.artist_id'))
)

albums_table = Table(
    'albums', metadata,
    Column('album_id', Integer, nullable=False, primary_key=True),
    Column('title', String(255), nullable=False)
)

artists_table = Table(
    'artists', metadata,
    # Column('id', Integer, primary_key=True, autoincrement=True),
    Column('artist_id', Integer, nullable=False, primary_key=True),
    Column('full_name', String(255), nullable=False)
)

genres_table = Table(
    'genres', metadata,
    # Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_id', Integer, nullable=False,primary_key=True),
    Column('genre_name', String(255), nullable=False)
)

track_genres_table = Table(
    'track_genres',metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.track_id')),
    Column('genre_id', ForeignKey('genres.genre_id'))
)

def map_model_to_tables():
    mapper(user.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password
    })

    mapper(review.Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating
    })

    mapper(track.Track, tracks_table, properties={
        '_Track__track_id': tracks_table.c.track_id,
        '_Track__title': tracks_table.c.title,
        '_Track__track_duration': tracks_table.c.track_duration,
        '_Track__track_url':tracks_table.c.track_url,
        '_Track__reviews': relationship(review.Review, backref='_Review__track'),
        '_Track__album': relationship(album.Album),
        '_Track__artist': relationship(artist.Artist),
        '_Track__genres': relationship(genre.Genre, secondary=track_genres_table)
                                    #    back_populates='_Genre__tagged_track')
    })

    mapper(album.Album, albums_table, properties={
        '_Album__album_id': albums_table.c.album_id,
        '_Album__title': albums_table.c.title,
    })

    mapper(artist.Artist, artists_table, properties={
        '_Artist__artist_id': artists_table.c.artist_id,
        '_Artist__full_name': artists_table.c.full_name
    })

    mapper(genre.Genre, genres_table, properties={
        '_Genre__genre_id': genres_table.c.genre_id,
        '_Genre__name': genres_table.c.genre_name,
        # '_Genre__tagged_track': relationship(track.Track,secondary=track_genres_table,back_populates="_Track__geners")
    })  