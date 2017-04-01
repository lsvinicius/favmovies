from flask_login import UserMixin
from src.database import db
from src.model.movie import Movie


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    movies = db.relationship('Movie', backref='user', lazy='dynamic')

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def get_movie_by_imdbID(self, imdbID):
        result = self.movies.filter_by(imdbID=imdbID).first()
        return result

    def __str__(self):
        return self.email + ' ' + self.password
