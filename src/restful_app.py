import sys
import re
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from src import database, custom_log, settings
from src.api.favmovies import favmovies


def create_restful_app(database_uri='sqlite:////tmp/default.db'):
    restful_app = Flask(__name__)
    custom_log.init_logger(restful_app.logger)
    restful_app.register_blueprint(favmovies)
    restful_app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    restful_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return restful_app

# logging
logger_handler = RotatingFileHandler('restful.log', maxBytes=1000000,
                                     backupCount=1)
logger_handler.setLevel(logging.INFO)
# restful initialization
restful_app = create_restful_app()
restful_app.logger.addHandler(logger_handler)


@restful_app.errorhandler(404)
@restful_app.errorhandler(401)
@restful_app.errorhandler(403)
@restful_app.errorhandler(500)
@restful_app.errorhandler(400)
def http_error_handler(error):
    return jsonify(error)

if __name__ == '__main__':
    mode = None
    if len(sys.argv) == 2:
        mode = sys.argv[1]
    mode = settings.get_init_mode(mode)
    if settings.init(mode):
        restful_app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI
        database.db.init_app(restful_app)
        restful_app.run(debug=True, port=int(settings.RESTFUL_PORT))
    else:
        print('FAILED TO INITIALIZE RESTFUL API!!!')
