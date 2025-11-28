from sqlalchemy import ScalarResult, Row, Sequence
from ..models import db, Movie, User, UserMovie
from omdb_api import Omdb


class Manager:

    @staticmethod
    def _get(model: db.Model, model_id: int) -> ScalarResult:
        return db.session.execute(
            db.select(model).filter_by(id=model_id)
        ).scalar()

    @staticmethod
    def _get_all(model: db.Model) -> ScalarResult:
        return db.session.execute(
            db.select(model)
        ).scalars()

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

    def get_all(self) -> Sequence[Row]:
        return self._get_all(User).all()

    def add(self, name: str) -> None:
        self._add(User(name=name))

    def delete(self, user_id: int) -> None:
        user = self.get(user_id)
        self._delete(user)

    def update(self, user_id: int, new_name: str) -> None:
        user = self._get(User, user_id)
        self._update(user, new_name)


class MovieManager(Manager):

    def add(self, title: str) -> None:
        movie = Omdb(title=title).movie()
        self._add(movie)

    def delete(self, movie_id: int) -> None:
        movie = self._get(Movie, movie_id)
        self._delete(movie)

    def get(self, movie_id: int) -> Row:
        return self._get(Movie, movie_id).one()

    def get_all(self) -> Sequence[Row]:
        return self._get_all(Movie)


class UserMovieManager(Manager):

    @staticmethod
    def _getter(movie_id: int, user_id: int) -> ScalarResult:
        return db.session.execute(
            db.select(UserMovie).filter_by(movie_id=movie_id, user_id=user_id)
        ).scalar()

    def get(self, movie_id: int, user_id: int) -> Row:
        return self._getter(movie_id, user_id).one()

    @staticmethod
    def get_all(user_id: int) -> Sequence[Row]:
        return db.session.execute(
            db.select(UserMovie).filter_by(user_id=user_id)
        ).scalars().all()

    def add(self, movie_id: int, user_id: int) -> None:
        movie = self._get(Movie, movie_id).one()
        user = self._get(User, user_id).one()
        user_movie = UserMovie(
            movie_id=movie.id,
            user_id=user.id,
            custom_movie_name=movie.title
        )
        self._add(user_movie)

    def delete(self, movie_id: int, user_id: int) -> None:
        user_movie = self._getter(movie_id, user_id)
        self._delete(user_movie)

    def update(self, movie_id: int, user_id: int, new_name: str) -> None:
        user_movie = self._getter(movie_id, user_id)
        self._update(user_movie, new_name)


class DataManager:
    user = UserManager()
    movie = MovieManager()
    user_movie = UserMovieManager()
