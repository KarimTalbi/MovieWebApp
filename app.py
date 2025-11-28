import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for

from models import db, Movie, User
from data_manager import DataManager

basedir = Path(__file__).parent.resolve()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'movies.sqlite')}"

db.init_app(app)
DM = DataManager()


@app.route('/')
def home():
    """
    Home page: shows all users.
    """
    users = DM.user.get_all()
    return render_template('home.html', users=users)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Handle both displaying the add user form and processing it.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            DM.user.add(username)
        return redirect(url_for('home'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    Lists all movies for a specific user.
    """
    user = DM.user.get(user_id)
    if not user:
        return render_template('error.html', error="User not found"), 404
    movies = DM.movie.get_all(user_id)
    return render_template('movies.html', movies=movies, user=user)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    """
    Shows details for a specific movie.
    """
    movie = DM.movie.get(movie_id)
    if not movie:
        return render_template('error.html', error="Movie not found"), 404
    return render_template('movie.html', movie=movie)


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    """
    Handle displaying the add movie form and processing it.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            DM.movie.add(title=title)
            return redirect(url_for('home'))  # Or wherever you want to redirect
    return render_template('add_movie.html')


@app.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    """
    Deletes a movie.
    """
    movie = DM.movie.get(movie_id)
    if movie:
        # Assuming movie object has a user associated with it to redirect back
        user_id = movie.user_id
        DM.movie.delete(movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('error.html', error="Movie not found"), 404


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
