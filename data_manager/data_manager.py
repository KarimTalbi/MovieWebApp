"""
This module provides data management classes for interacting with the database.

It includes managers for User and Movie entities, handling all CRUD (Create, Read,
Update, Delete) operations. It also defines custom exceptions for data-related errors.
"""
from sqlalchemy import Sequence
from models import db, Movie, User
from .omdb import Omdb, MovieApiError


class UserNotFoundError(Exception):
    """Raised when a user is not found in the database."""
    pass


class MovieNotFoundError(Exception):
    """Raised when a movie is not found in the database."""
    pass


class InvalidUserName(Exception):
    """Raised when an invalid user name is provided."""
    pass


class InvalidMovieTitle(Exception):
    """Raised when an invalid movie title is provided."""
    pass


class UserManager:
    """Manages data operations for User entities."""

    @staticmethod
    def get(user_id: int) -> User:
        """
        Retrieves a user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            The User object.

        Raises:
            UserNotFoundError: If no user is found with the given ID.
        """
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)
        ).scalar()

        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        return user

    @staticmethod
    def get_all() -> Sequence[User]:
        """
        Retrieves all users from the database.

        Returns:
            A sequence of User objects.
        """
        users = db.session.execute(
            db.select(User)
        ).scalars()

        return users

    @staticmethod
    def add(name: str) -> User:
        """
        Adds a new user to the database.

        Args:
            name: The name of the new user.

        Returns:
            The newly created User object.

        Raises:
            InvalidUserName: If the provided name is empty.
        """
        if not name:
            raise InvalidUserName("User name cannot be empty")

        user = User(name=name)

        db.session.add(user)
        db.session.commit()

        return user

    def delete(self, user_id: int) -> None:
        """
        Deletes a user from the database.

        Args:
            user_id: The ID of the user to delete.
        """
        user = self.get(user_id)

        db.session.delete(user)
        db.session.commit()

    def update(self, user_id: int, new_name: str) -> None:
        """
        Updates the name of an existing user.

        Args:
            user_id: The ID of the user to update.
            new_name: The new name for the user.
        """
        user = self.get(user_id)

        user.name = new_name
        db.session.commit()


class MovieManager:
    """Manages data operations for Movie entities."""

    @staticmethod
    def get(movie_id: int) -> Movie:
        """
        Retrieves a movie by its ID.

        Args:
            movie_id: The ID of the movie to retrieve.

        Returns:
            The Movie object.

        Raises:
            MovieNotFoundError: If no movie is found with the given ID.
        """
        movie = db.session.execute(
            db.select(Movie).filter_by(id=movie_id)
        ).scalar()

        if not movie:
            raise MovieNotFoundError(f"Movie with id {movie_id} not found")

        return movie

    @staticmethod
    def get_all(user_id: int) -> Sequence[Movie]:
        """
        Retrieves all movies belonging to a specific user.

        Args:
            user_id: The ID of the user.

        Returns:
            A sequence of Movie objects.
        """
        movies = db.session.execute(
            db.select(Movie).filter_by(user_id=user_id)
        ).scalars()

        return movies

    def count(self, user_id: int) -> int:
        """
        Counts the number of movies belonging to a specific user.

        Args:
            user_id: The ID of the user.

        Returns:
            The total number of movies for the user.
        """
        movies = self.get_all(user_id)

        if not movies:
            return 0

        return len(list(movies))

    @staticmethod
    def add(title: str, user_id: int) -> Movie:
        """
        Adds a new movie for a user, fetching details from the OMDB API.

        Args:
            title: The title of the movie to add.
            user_id: The ID of the user who will own the movie.

        Returns:
            The newly created Movie object.

        Raises:
            InvalidMovieTitle: If the provided title is empty.
            MovieApiError: If the movie cannot be found or there's an API issue.
        """
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
        """
        Deletes a movie from the database.

        Args:
            movie_id: The ID of the movie to delete.
        """
        movie = self.get(movie_id)

        db.session.delete(movie)
        db.session.commit()

    def update(self, movie_id: int, new_title: str) -> None:
        """
        Updates the title of an existing movie.

        Note: This only updates the title in the local database, not the other
        details fetched from OMDB.

        Args:
            movie_id: The ID of the movie to update.
            new_title: The new title for the movie.
        """
        movie = self.get(movie_id)

        movie.title = new_title
        db.session.commit()


class DataManager:
    """A facade class that provides access to all data managers."""
    user = UserManager()
    movie = MovieManager()
