import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_login import LoginManager
from src import database, custom_log
from src.views.site_views import site_views
from src.model.user import User
import os

def create_frontend_app():
    frontend_app = Flask(__name__)
    custom_log.init_logger(frontend_app.logger)
    frontend_app.register_blueprint(site_views)
    frontend_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    frontend_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return frontend_app

#logging
logger_handler = RotatingFileHandler('frontend.log', maxBytes=1000000, backupCount=1)
logger_handler.setLevel(logging.INFO)
#frontend initialization
frontend_app = create_frontend_app()
frontend_app.logger.addHandler(logger_handler)
#init database
database.db.init_app(frontend_app)
#login_manager initialization
login_manager = LoginManager()
login_manager.setup_app(frontend_app)
login_manager.login_view = 'site_views.login'

@frontend_app.before_first_request
def setup_database():
    database.db.drop_all()
    database.db.create_all()

@frontend_app.errorhandler(404)
@frontend_app.errorhandler(401)
@frontend_app.errorhandler(403)
@frontend_app.errorhandler(500)
def http_error_handler(error):
    frontend_app.logger.info('http_error_handler: {}'.format(error.code))
    return render_template('error.jinja', error=error), error.code

@frontend_app.errorhandler(400)
def bad_request_handler(error):
    frontend_app.logger.info('bad_request_handler: {}'.format(error))
    return render_template('bad_request.jinja', error=error.description), error.code

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

if __name__ == '__main__':
    frontend_app.secret_key = os.urandom(24)
    frontend_app.run(debug=True, port=5000)
