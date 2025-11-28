from sqlalchemy import ScalarResult, Row, Sequence
from models import db, Movie, User
from omdb import Omdb


class Manager:

    @staticmethod
    def _get(model: db.Model, model_id: int) -> ScalarResult:
        return db.session.execute(
            db.select(model).filter_by(id=model_id)
        ).scalar()

    @staticmethod
    def _add(model: db.Model) -> None:
        db.session.add(model)
        db.session.commit()

    @staticmethod
    def _delete(model: db.Model) -> None:
        db.session.delete(model)
        db.session.commit()

    @staticmethod
    def _update(model: db.Model, new_name: str) -> None:
        model.name = new_name
        db.session.commit()


class UserManager(Manager):

    def get(self, user_id: int) -> Row:
        return self._get(User, user_id).one()

    @staticmethod
    def get_all() -> Sequence[Row]:
        users = db.session.execute(
            db.select(User)
        ).scalars()
        return users.all()

    def add(self, name: str) -> None:
        self._add(User(name=name))

    def delete(self, user_id: int) -> None:
        user = self.get(user_id)
        self._delete(user)

    def update(self, user_id: int, new_name: str) -> None:
        user = self._get(User, user_id)
        self._update(user, new_name)


class MovieManager(Manager):

    def get(self, movie_id: int) -> Row:
        return self._get(Movie, movie_id).one()

    @staticmethod
    def get_all(user_id: int) -> Sequence[Row]:
        movies = db.session.execute(
            db.select(Movie).filter_by(user_id=user_id)
        ).scalars()
        return movies.all()

    def add(self, title: str, user_id: int) -> None:
        movie = Omdb(title=title).movie()
        movie.user_id = user_id
        self._add(movie)

    def delete(self, movie_id: int) -> None:
        movie = self._get(Movie, movie_id)
        self._delete(movie)

    def update(self, movie_id: int, new_title: str) -> None:
        movie = self._get(Movie, movie_id)
        self._update(movie, new_title)


class DataManager:
    user = UserManager()
    movie = MovieManager()
