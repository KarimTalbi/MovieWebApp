"""
This module defines controller classes for handling HTTP GET and POST requests
related to users and movies. It separates the logic for processing requests
from the routing definitions in the main Flask application.
"""
from flask import render_template, request, redirect, url_for, Response
from data_manager import DataManager

DM = DataManager()
RenderedPage = str


class UserPost:
    """Handles POST requests for user-related actions."""

    @staticmethod
    def add() -> Response:
        """
        Adds a new user based on form data and redirects to the user's detail page.

        Returns:
            A Flask redirect response.
        """
        user = DM.user.add(
            name=request.form.get('username')
        )
        resp = redirect(url_for(
            endpoint='user_details', user_id=user.id
        ))
        return resp

    @staticmethod
    def update(user_id: int) -> Response:
        """
        Updates an existing user's name based on form data and redirects
        to the user's detail page.

        Args:
            user_id: The ID of the user to update.

        Returns:
            A Flask redirect response.
        """
        DM.user.update(
            user_id=user_id, new_name=request.form.get('username')
        )
        resp = redirect(url_for(
            endpoint='user_details', user_id=user_id
        ))
        return resp


class MoviePost:
    """Handles POST requests for movie-related actions."""

    @staticmethod
    def add(user_id: int) -> Response:
        """
        Adds a new movie for a user based on form data and redirects to the
        new movie's detail page.

        Args:
            user_id: The ID of the user adding the movie.

        Returns:
            A Flask redirect response.
        """
        movie = DM.movie.add(
            title=request.form.get('title'),
            user_id=user_id
        )
        resp = redirect(url_for(
            endpoint='movie_details',
            user_id=user_id,
            movie_id=movie.id
        ))
        return resp

    @staticmethod
    def delete(user_id: int, movie_id: int) -> Response:
        """
        Deletes a movie and redirects to the user's movie list.

        Args:
            user_id: The ID of the user who owns the movie.
            movie_id: The ID of the movie to delete.

        Returns:
            A Flask redirect response.
        """
        DM.movie.delete(movie_id)
        resp = redirect(url_for(
            endpoint='movie_list',
            user_id=user_id
        ))
        return resp

    @staticmethod
    def update(user_id: int, movie_id: int) -> Response:
        """
        Updates a movie's title based on form data and redirects to the
        movie's detail page.

        Args:
            user_id: The ID of the user who owns the movie.
            movie_id: The ID of the movie to update.

        Returns:
            A Flask redirect response.
        """
        DM.movie.update(
            movie_id=movie_id,
            new_title=request.form.get('new_title')
        )
        resp = redirect(url_for(
            endpoint='movie_details',
            user_id=user_id,
            movie_id=movie_id
        ))
        return resp


class Post:
    """Aggregates all POST request controller classes."""
    user = UserPost()
    movie = MoviePost()


class UserGet:
    """Handles GET requests for user-related pages."""

    @staticmethod
    def list() -> RenderedPage:
        """
        Renders the home page with a list of all users.

        Returns:
            The rendered HTML page as a string.
        """
        temp = render_template(
            template_name_or_list='home.html', users=DM.user.get_all()
        )
        return temp

    @staticmethod
    def add() -> RenderedPage:
        """
        Renders the page for adding a new user.

        Returns:
            The rendered HTML page as a string.
        """
        temp = render_template(
            template_name_or_list='add_user.html'
        )
        return temp

    @staticmethod
    def details(user_id: int) -> RenderedPage:
        """
        Renders the detail page for a specific user, including their movie count.

        Args:
            user_id: The ID of the user.

        Returns:
            The rendered HTML page as a string.
        """
        user = DM.user.get(user_id)
        temp = render_template(
            template_name_or_list='user.html',
            user=user,
            movies_count=DM.movie.count(user_id)
        )
        return temp

    @staticmethod
    def delete(user_id: int) -> Response:
        """
        Deletes a user and redirects to the home page.

        Args:
            user_id: The ID of the user to delete.

        Returns:
            A Flask redirect response.
        """
        DM.user.delete(user_id)
        resp = redirect(url_for(
            endpoint='home')
        )
        return resp

    @staticmethod
    def update(user_id: int) -> RenderedPage:
        """
        Renders the page for updating a user's information.

        Args:
            user_id: The ID of the user to update.

        Returns:
            The rendered HTML page as a string.
        """
        temp = render_template(
            template_name_or_list='update_user.html',
            user=DM.user.get(user_id)
        )
        return temp


class MovieGet:
    """Handles GET requests for movie-related pages."""

    @staticmethod
    def list(user_id: int) -> RenderedPage:
        """
        Renders the list of movies for a specific user.

        Args:
            user_id: The ID of the user.

        Returns:
            The rendered HTML page as a string.
        """
        user = DM.user.get(user_id)
        temp = render_template(
            template_name_or_list='movies.html',
            movies=DM.movie.get_all(user_id),
            user=user
        )
        return temp

    @staticmethod
    def details(user_id: int, movie_id: int) -> RenderedPage:
        """
        Renders the detail page for a specific movie.

        Args:
            user_id: The ID of the user who owns the movie.
            movie_id: The ID of the movie.

        Returns:
            The rendered HTML page as a string.
        """
        user = DM.user.get(user_id)
        movie = DM.movie.get(movie_id)
        temp = render_template(
            template_name_or_list='movie.html',
            movie=movie,
            user=user
        )
        return temp

    @staticmethod
    def add(user_id: int) -> RenderedPage:
        """
        Renders the page for adding a new movie.

        Args:
            user_id: The ID of the user who will own the new movie.

        Returns:
            The rendered HTML page as a string.
        """
        temp = render_template(
            template_name_or_list='add_movie.html',
            user=DM.user.get(user_id)
        )
        return temp

    @staticmethod
    def update(movie_id: int) -> RenderedPage:
        """
        Renders the page for updating a movie's information.

        Args:
            movie_id: The ID of the movie to update.

        Returns:
            The rendered HTML page as a string.
        """
        temp = render_template(
            template_name_or_list='update_movie.html',
            movie=DM.movie.get(movie_id)
        )
        return temp


class Get:
    """Aggregates all GET request controller classes."""
    user = UserGet()
    movie = MovieGet()
