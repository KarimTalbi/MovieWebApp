"""
This module implements a Flask web application for managing movies and users.

It provides routes for listing, adding, updating, and deleting users and their associated movies.
The application uses SQLAlchemy for database interactions and handles various error conditions.
"""
from os.path import join
from pathlib import Path
from flask import Flask, request, render_template, Response
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest

from data_manager import MovieNotFoundError, InvalidUserName, UserNotFoundError, InvalidMovieTitle, MovieApiError
from models import db
from core import Post, Get, RenderedPage

basedir = Path(__file__).parent.resolve()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{join(basedir, 'data', 'movies.sqlite')}"
db.init_app(app)

POST = Post()
GET = Get()

ResponseCode = int


@app.route(
    rule='/', methods=['GET']
)
def home() -> tuple[RenderedPage, ResponseCode]:
    """
    Renders the home page with a list of users.

    Returns:
        A tuple containing the rendered template and the HTTP status code.
    """
    return GET.user.list(), 200


@app.route(
    rule='/users/add_user', methods=['GET', 'POST']
)
def user_add() -> (
        tuple[RenderedPage, ResponseCode] | Response
):
    """
    Handles user creation.

    GET: Renders the form to add a new user.
    POST: Adds a new user to the database.

    Returns:
        A tuple containing the rendered template and the HTTP status code or a response object.
    """
    if request.method == 'POST':
        return POST.user.add()

    return GET.user.add(), 200


@app.route(
    rule='/users/<int:user_id>', methods=['GET']
)
def user_details(user_id: int) -> (
        tuple[RenderedPage, ResponseCode]
):
    """
    Renders the details of a specific user.

    Args:
        user_id: The ID of the user to display.

    Returns:
        A tuple containing the rendered template and the HTTP status code.
    """
    return GET.user.details(user_id), 200


@app.route(
    rule='/users/<int:user_id>/delete', methods=['GET']
)
def user_delete(user_id: int) -> (
        Response
):
    """
    Deletes a specific user.

    Args:
        user_id: The ID of the user to delete.

    Returns:
        A response object.
    """
    return GET.user.delete(user_id)


@app.route(
    rule='/users/<int:user_id>/update', methods=['GET', 'POST']
)
def user_update(user_id: int) -> (
        tuple[RenderedPage, ResponseCode] | Response
):
    """
    Handles user updates.

    GET: Renders the form to update a user.
    POST: Updates the user's information in the database.

    Args:
        user_id: The ID of the user to update.

    Returns:
        A tuple containing the rendered template or a response object, and the HTTP status code.
    """
    if request.method == 'POST':
        return POST.user.update(user_id)

    return GET.user.update(user_id), 200


@app.route(
    rule='/users/<int:user_id>/movies', methods=['GET']
)
def movie_list(user_id: int) -> (
        tuple[RenderedPage, ResponseCode]
):
    """
    Renders the list of movies for a specific user.

    Args:
        user_id: The ID of the user.

    Returns:
        A tuple containing the rendered template and the HTTP status code.
    """
    return GET.movie.list(user_id), 200


@app.route(
    rule='/users/<int:user_id>/movies/<int:movie_id>', methods=['GET']
)
def movie_details(user_id: int, movie_id: int) -> (
        tuple[RenderedPage, ResponseCode]
):
    """
    Renders the details of a specific movie for a specific user.

    Args:
        user_id: The ID of the user.
        movie_id: The ID of the movie.

    Returns:
        A tuple containing the rendered template and the HTTP status code.
    """
    return GET.movie.details(user_id, movie_id), 200


@app.route(
    rule='/users/<int:user_id>/movies/add_movie', methods=['GET', 'POST']
)
def movie_add(user_id: int) -> (
        tuple[RenderedPage, ResponseCode] | Response
):
    """
    Handles adding a new movie for a specific user.

    GET: Renders the form to add a new movie.
    POST: Adds a new movie to the user's collection.

    Args:
        user_id: The ID of the user.

    Returns:
        A tuple containing the rendered template or a response object, and the HTTP status code.
    """
    if request.method == 'POST':
        return POST.movie.add(user_id)

    return GET.movie.add(user_id), 200


@app.route(
    rule='/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST']
)
def movie_delete(user_id: int, movie_id: int) -> (
        Response
):
    """
    Deletes a specific movie for a specific user.

    Args:
        user_id: The ID of the user.
        movie_id: The ID of the movie to delete.

    Returns:
        A response object.
    """
    return POST.movie.delete(user_id, movie_id)


@app.route(
    rule='/users/<int:user_id>/movies/<int:movie_id>/update',
    methods=['GET', 'POST']
)
def movie_update(user_id: int, movie_id: int) -> (
        tuple[RenderedPage, ResponseCode] | Response
):
    """
    Handles updating a movie for a specific user.

    GET: Renders the form to update a movie.
    POST: Updates the movie's information in the database.

    Args:
        user_id: The ID of the user.
        movie_id: The ID of the movie to update.

    Returns:
        A tuple containing the rendered template or a response object, and the HTTP status code.
    """
    if request.method == 'POST':
        return POST.movie.update(user_id, movie_id)

    return GET.movie.update(movie_id), 200


@app.errorhandler(404)
def page_not_found(e) -> (
        tuple[RenderedPage, ResponseCode]
):
    """
    Renders the 404 error page.

    Args:
        e: The error object.

    Returns:
        A tuple containing the rendered error template and the 404 status code.
    """
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.description
    )
    return temp, 404


@app.errorhandler(400)
def bad_request(e) -> (
        tuple[RenderedPage, ResponseCode]
):
    """
    Renders the 400 error page.

    Args:
        e: The error object.

    Returns:
        A tuple containing the rendered error template and the 400 status code.
    """
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.description
    )
    return temp, 400


@app.errorhandler(500)
def internal_server_error(e) -> (
        tuple[RenderedPage, ResponseCode]
):
    """
    Renders the 500 error page.

    Args:
        e: The error object.

    Returns:
        A tuple containing the rendered error template and the 500 status code.
    """
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.description
    )
    return temp, 500


@app.errorhandler(Exception)
def unhandled_exception(e) -> (
        tuple[RenderedPage, ResponseCode]
):
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.args[0]
    )
    return temp, 500


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

    app.run(debug=True)
