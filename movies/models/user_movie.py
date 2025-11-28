from db import db

class UserMovie(db.Model):
    __tablename__ = 'usermovies'

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie = db.relationship('Movie', backref=db.backref('usermovies', lazy=True))
    user = db.relationship('User', backref=db.backref('usermovies', lazy=True))
    name = db.Column(db.String(128))

    def __repr__(self):
        return f"<movie_id {self.movie_id}> <user_id {self.user_id}>"

