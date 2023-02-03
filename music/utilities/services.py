from typing import Iterable
import random

from music.adapters.repository import AbstractRepository

def get_random_tracks(quantity, repo: AbstractRepository):
    track_count = 2000

    if quantity >= track_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of tracks.
        quantity = track_count - 1

    # Pick distinct and random tracks.
    random_ids = random.sample(range(1, track_count), quantity)
    tracks = repo.get_tracks_by_id(random_ids)

    return tracks