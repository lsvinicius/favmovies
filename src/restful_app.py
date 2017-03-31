from flask import Flask
from src import database
from src.api.favmovies import favmovies

def create_app():
    app = Flask(__name__)
    app.register_blueprint(favmovies)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


app = create_app()
database.db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
