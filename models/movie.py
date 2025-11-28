from .db import db

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    poster = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('movies', lazy=True))

    def __repr__(self):
        return f"<Movie {self.title}> <id {self.id}>"
