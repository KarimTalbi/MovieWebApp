from sqlalchemy import Sequence
from models import db, Movie, User
from .omdb import Omdb


class UserNotFoundError(Exception):
    pass


class MovieNotFoundError(Exception):
    pass


class InvalidUserName(Exception):
    pass


class InvalidMovieTitle(Exception):
    pass


class UserManager:

    @staticmethod
    def get(user_id: int) -> User:

        user = db.session.execute(
            db.select(User).filter_by(id=user_id)
        ).scalar()

        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        return user

    @staticmethod
    def get_all() -> Sequence[User]:

        users = db.session.execute(
            db.select(User)
        ).scalars()

        return users

    @staticmethod
    def add(name: str) -> None:

        if not name:
            raise InvalidUserName("User name cannot be empty")

        user = User(name=name)

        db.session.add(user)
        db.session.commit()

        return user

    def delete(self, user_id: int) -> None:

        user = self.get(user_id)

        db.session.delete(user)
        db.session.commit()

    def update(self, user_id: int, new_name: str) -> None:

        user = self.get(user_id)

        user.name = new_name
        db.session.commit()


class MovieManager:

    @staticmethod
    def get(movie_id: int) -> Movie:

        movie = db.session.execute(
            db.select(Movie).filter_by(id=movie_id)
        ).scalar()

        if not movie:
            raise MovieNotFoundError(f"Movie with id {movie_id} not found")

        return movie

    @staticmethod
    def get_all(user_id: int) -> Sequence[Movie]:

        movies = db.session.execute(
            db.select(Movie).filter_by(user_id=user_id)
        ).scalars()

        return movies

    def count(self, user_id: int) -> int:

        movies = self.get_all(user_id)

        if not movies:
            return 0

        return len(list(movies))

    @staticmethod
    def add(title: str, user_id: int) -> Movie:

        if not title:
            raise InvalidMovieTitle("Movie title cannot be empty")

        movie = Omdb(
            title=title
        ).movie()

        movie.user_id = user_id

        db.session.add(movie)
        db.session.commit()

        return movie

    def delete(self, movie_id: int) -> None:

        movie = self.get(movie_id)

        db.session.delete(movie)
        db.session.commit()

    def update(self, movie_id: int, new_title: str) -> None:

        movie = self.get(movie_id)

        movie.title = new_title
        db.session.commit()


class DataManager:
    user = UserManager()
    movie = MovieManager()
