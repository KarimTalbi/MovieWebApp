import os
from pathlib import Path
from flask import Flask, request, render_template, abort
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest

from data_manager.data_manager import MovieNotFoundError, InvalidUserName, UserNotFoundError, InvalidMovieTitle
from data_manager.omdb import MovieApiError
from models import db
from core import Post, Get

basedir = Path(__file__).parent.resolve()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'movies.sqlite')}"
db.init_app(app)

POST = Post()
GET = Get()


@app.route(
    rule='/',
    methods=['GET']
)
def home():
    return GET.user.list()


@app.route(
    rule='/users/add_user',
    methods=['GET', 'POST']
)
def user_add():
    if request.method == 'POST':
        return POST.user.add()
    return GET.user.add()


@app.route(
    rule='/users/<int:user_id>',
    methods=['GET']
)
def user_details(user_id):
    return GET.user.details(user_id)


@app.route(
    rule='/users/<int:user_id>/delete',
    methods=['GET']
)
def user_delete(user_id):
    return GET.user.delete(user_id)


@app.route(
    rule='/users/<int:user_id>/update',
    methods=['GET', 'POST']
)
def user_update(user_id):
    if request.method == 'POST':
        return POST.user.update(user_id)
    return GET.user.update(user_id)


@app.route(
    rule='/users/<int:user_id>/movies',
    methods=['GET']
)
def movie_list(user_id):
    return GET.movie.list(user_id)


@app.route(
    rule='/users/<int:user_id>/movies/<int:movie_id>',
    methods=['GET']
)
def movie_details(user_id, movie_id):
    return GET.movie.details(user_id, movie_id)


@app.route(
    rule='/users/<int:user_id>/movies/add_movie',
    methods=['GET', 'POST']
)
def movie_add(user_id):
    if request.method == 'POST':
        return POST.movie.add(user_id)
    return GET.movie.add(user_id)


@app.route(
    rule='/users/<int:user_id>/movies/<int:movie_id>/delete',
    methods=['POST']
)
def movie_delete(user_id, movie_id):
    return POST.movie.delete(user_id, movie_id)


@app.route(
    rule='/users/<int:user_id>/movies/<int:movie_id>/update',
    methods=['GET', 'POST']
)
def movie_update(user_id, movie_id):
    if request.method == 'POST':
        return POST.movie.update(user_id, movie_id)
    return GET.movie.update(movie_id)


@app.errorhandler(404)
def page_not_found(e):
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.description
    )
    return temp, 404


@app.errorhandler(400)
def bad_request(e):
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.description
    )
    return temp, 400


@app.errorhandler(BadRequest)
def bad_request_error(e):
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.description
    )
    return temp, 400


@app.errorhandler(500)
def internal_server_error(e):
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.description
    )
    return temp, 500


@app.errorhandler(SQLAlchemyError)
def database_error(e):
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.args[0]
    )
    return temp, 500


@app.errorhandler(MovieApiError)
def movie_api_error(e):
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.args[0]
    )
    return temp, 500


@app.errorhandler(UserNotFoundError)
def user_not_found_error(e):
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.args[0]
    )
    return temp, 404


@app.errorhandler(MovieNotFoundError)
def movie_not_found_error(e):
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.args[0]
    )
    return temp, 404


@app.errorhandler(InvalidUserName)
def invalid_user_name(e):
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.args[0]
    )
    return temp, 400


@app.errorhandler(InvalidMovieTitle)
def invalid_movie_title(e):
    temp = render_template(
        template_name_or_list='error.html',
        error_description=e.args[0]
    )
    return temp, 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
