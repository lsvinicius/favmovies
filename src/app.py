from flask import Flask
from flask_login import LoginManager
from src.database import db
from src.views.site_views import site_views
from src.model.user import User
import os

app = Flask(__name__)
app.register_blueprint(site_views)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'site_views.login'

@app.before_first_request
def setup_database():
    db.drop_all()
    db.create_all()

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
