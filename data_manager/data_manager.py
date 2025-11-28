from sqlalchemy import Sequence
from models import db, Movie, User
from .omdb import Omdb


class UserManager:

    @staticmethod
    def get(user_id: int) -> User:
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)
        ).scalar()
        return user

    @staticmethod
    def get_all() -> Sequence[User]:
        users = db.session.execute(
            db.select(User)
        ).scalars()
        return users

    @staticmethod
    def add(name: str) -> None:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()


class MovieManager:

    @staticmethod
    def get(movie_id: int) -> Movie:
        movie = db.session.execute(
            db.select(Movie).filter_by(id=movie_id)
        ).scalar()
        return movie

    @staticmethod
    def get_all(user_id: int) -> Sequence[Movie]:
        movies = db.session.execute(
            db.select(Movie).filter_by(user_id=user_id)
        ).scalars()
        return movies

    @staticmethod
    def add(title: str, user_id: int) -> None:
        movie = Omdb(title=title).movie()
        movie.user_id = user_id
        db.session.add(movie)
        db.session.commit()

    @staticmethod
    def delete(movie_id: int) -> None:
        movie = db.session.execute(
            db.select(Movie).filter_by(id=movie_id)
        ).scalar()
        db.session.delete(movie)
        db.session.commit()

    @staticmethod
    def update(movie_id: int, new_title: str) -> None:
        movie = db.session.execute(
            db.select(Movie).filter_by(id=movie_id)
        ).scalar()
        movie.title = new_title
        db.session.commit()

class DataManager:
    user = UserManager()
    movie = MovieManager()
