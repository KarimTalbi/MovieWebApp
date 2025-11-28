import os
from pathlib import Path
from flask import Flask

from models import db, Movie, User, UserMovie

basedir = Path(__file__).parent.resolve()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'movies.sqlite')}"

db.init_app(app)

with app.app_context():
    db.drop_all()
