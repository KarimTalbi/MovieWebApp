from .db import db

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    release_year = db.Column(db.Integer)
    rated = db.Column(db.String(16))
    rating = db.Column(db.Float)
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
        return f"Movie. {self.title} - ID: {self.id}"
