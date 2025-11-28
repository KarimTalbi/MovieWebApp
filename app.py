import os
from pathlib import Path
from flask import Flask

from models import db, Movie, User
from data_manager import DataManager

DM = DataManager()
basedir = Path(__file__).parent.resolve()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'movies.sqlite')}"

db.init_app(app)

@app.route('/')
def home():
    pass

@app.route('/users')
def list_users():
    users = DM.user.get_all()
    return str(users)

@app.route('/users/<user_id>/movies')
def user(user_id):
    pass


@app.route('/users/<user_id>/movies/<movie_id>')
def movie(user_id):
    pass



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
