from ..models import db, Movie, User
from omdb_api import Omdb


class UserManager:

    @staticmethod
    def add(name: str):
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def delete(user_id: int):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def update(user_id: int, new_name: str):
        user = User.query.get(user_id)
        user.name = new_name
        db.session.update(user)
        db.session.commit()

    @staticmethod
    def get(user_id: int):
        return db.session.get(User, user_id)

    @staticmethod
    def get_all():
        return db.session.get_all(User)


class MovieManager:
    def __init__(self, user: User):
        self.user_id = user.id

    def add(self, title: str):
        movie = Omdb(
            title=title,
            user_id=self.user_id
        ).movie
        db.session.add(movie)
        db.session.commit()

    def delete(self, movie_id: int):
        pass


    def update(self, movie_id: int):
        pass

    def get(self):
        pass

    def get_all(self):
        pass
