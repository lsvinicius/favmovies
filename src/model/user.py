from src.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    password = db.Column(db.String(128))
    email = db.Column(db.String(200), unique=True)

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def __str__(self):
        return self.email + ' ' + self.password
