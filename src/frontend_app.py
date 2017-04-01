import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_login import LoginManager
from src import database, custom_log, settings
from src.views.site_views import site_views
from src.model.user import User

def create_frontend_app(database_uri='sqlite:////tmp/default.db'):
    frontend_app = Flask(__name__)
    custom_log.init_logger(frontend_app.logger)
    frontend_app.register_blueprint(site_views)
    frontend_app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    frontend_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return frontend_app

#logging
logger_handler = RotatingFileHandler('frontend.log', maxBytes=1000000, backupCount=1)
logger_handler.setLevel(logging.INFO)
#frontend initialization
frontend_app = create_frontend_app()
frontend_app.logger.addHandler(logger_handler)
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
    mode = None
    if len(sys.argv) == 2:
        mode = sys.argv[1]
    mode = settings.get_init_mode(mode)
    frontend_app.secret_key = os.urandom(24)
    if settings.init(mode):
        frontend_app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI
        database.db.init_app(frontend_app)
        frontend_app.run(debug=True, port=int(settings.FRONTEND_PORT))
    else:
        print("FAILED TO INITIALIZE FRONTEND!!!")
