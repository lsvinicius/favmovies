from src.database import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    imdbID = db.Column(db.String(100), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    plot = db.Column(db.String(10000), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    poster = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.String(10000))

    @property
    def serialize(self):
        return {
            'imdbID': self.imdbID,
            'title': self.title,
            'plot': self.plot,
            'type': self.type,
            'poster': self.poster,
            'user_id': self.user_id,
            'comment': self.comment
        }

    def __str__(self):
        return self.title
