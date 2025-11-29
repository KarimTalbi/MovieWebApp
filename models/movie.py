"""
This module defines the SQLAlchemy data models for the application,
including the Movie model.
"""
from .db import db


class Movie(db.Model):
    """
    Represents a movie in the database.

    Attributes:
        id (int): The primary key for the movie.
        title (str): The title of the movie.
        release_year (int): The year the movie was released.
        rated (str): The MPAA rating (e.g., PG, R).
        rating (float): The IMDb rating score.
        runtime (str): The duration of the movie.
        genre (str): The genre(s) of the movie.
        director (str): The director(s) of the movie.
        actors (str): The main actors in the movie.
        plot (str): A brief summary of the movie's plot.
        imdb_id (str): The unique IMDb identifier.
        poster (str): A URL to the movie's poster image.
        user_id (int): The foreign key linking to the user who added the movie.
        user (User): The relationship to the User object.
    """
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    release_year = db.Column(db.String(12))
    rated = db.Column(db.String(16))
    rating = db.Column(db.String(12))
    runtime = db.Column(db.String(16))
    genre = db.Column(db.String(128))
    director = db.Column(db.String(128))
    actors = db.Column(db.String(256))
    plot = db.Column(db.Text)
    imdb_id = db.Column(db.String(16))
    poster = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('movies', lazy=True))

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the Movie object.
        """
        return f"Movie. {self.title} - ID: {self.id}"
