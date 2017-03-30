from flask import Flask
from src.database import db
from src.api.favmovies import favmovies

app = Flask(__name__)
app.register_blueprint(favmovies)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
