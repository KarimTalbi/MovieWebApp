from flask import render_template, request, redirect, url_for
from data_manager import DataManager

DM = DataManager()


class UserPost:

    @staticmethod
    def add():
        user = DM.user.add(
            name=request.form.get('username')
        )
        resp = redirect(url_for(
            endpoint='user_details', user_id=user.id
        ))
        return resp

    @staticmethod
    def update(user_id):
        DM.user.update(
            user_id=user_id, new_name=request.form.get('username')
        )
        resp = redirect(url_for(
            endpoint='user_details', user_id=user_id
        ))
        return resp


class MoviePost:

    @staticmethod
    def add(user_id):
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
    def delete(user_id, movie_id):
        DM.movie.delete(movie_id)
        resp = redirect(url_for(
            endpoint='movie_list',
            user_id=user_id
        ))
        return resp

    @staticmethod
    def update(user_id, movie_id):
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
    user = UserPost()
    movie = MoviePost()


class UserGet:

    @staticmethod
    def list():
        temp = render_template(
            template_name_or_list='home.html', users=DM.user.get_all()
        )
        return temp

    @staticmethod
    def add():
        temp = render_template(
            template_name_or_list='add_user.html'
        )
        return temp

    @staticmethod
    def details(user_id: int):
        user = DM.user.get(user_id)
        temp = render_template(
            template_name_or_list='user.html',
            user=user,
            movies_count=DM.movie.count(user_id)
        )
        return temp

    @staticmethod
    def delete(user_id):
        DM.user.delete(user_id)
        resp = redirect(url_for(
            endpoint='home')
        )
        return resp

    @staticmethod
    def update(user_id):
        temp = render_template(
            template_name_or_list='update_user.html',
            user=DM.user.get(user_id)
        )
        return temp


class MovieGet:

    @staticmethod
    def list(user_id):
        user = DM.user.get(user_id)
        temp = render_template(
            template_name_or_list='movies.html',
            movies=DM.movie.get_all(user_id),
            user=user
        )
        return temp

    @staticmethod
    def details(user_id, movie_id):
        user = DM.user.get(user_id)
        movie = DM.movie.get(movie_id)
        temp = render_template(
            template_name_or_list='movie.html',
            movie=movie,
            user=user
        )
        return temp

    @staticmethod
    def add(user_id):
        temp = render_template(
            template_name_or_list='add_movie.html',
            user=DM.user.get(user_id)
        )
        return temp

    @staticmethod
    def update(movie_id):
        temp = render_template(
            template_name_or_list='update_movie.html',
            movie=DM.movie.get(movie_id)
        )
        return temp


class Get:
    user = UserGet()
    movie = MovieGet()
