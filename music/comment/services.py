from music.adapters.repository import AbstractRepository
from music.domainmodel import review
from music.domainmodel.review import Review
from music.domainmodel.user import User


class NonExistentArticleException(Exception):
    pass


class UnknownUserException(Exception):
    pass

def get_track(trackid: int, repo: AbstractRepository):
    target_track = repo.get_track(trackid)
    return target_track

def add_review(review: Review, repo: AbstractRepository):
    repo.add_review(review)

def get_reviews(repo: AbstractRepository):
    reviews = repo.get_reviews()
    return reviews

def get_user(user_name: User, repo: AbstractRepository):
    user = repo.get_user(user_name)
    return user