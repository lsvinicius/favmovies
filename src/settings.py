import configparser
from src.custom_log import custom_logger


def get_init_mode(mode):
    if mode == 'TEST':
        return mode
    else:
        return 'DEFAULT'


# Restful API address config
def init(mode='DEFAULT'):
    global HOST_ADDRESS
    global RESTFUL_PORT
    global FRONTEND_PORT
    global HTTP_ADDRESS
    global FAVMOVIES_RESTFUL_PATH
    global FULL_ADDRESS
    global DATABASE_URI
    config = configparser.ConfigParser()
    config.read('config.ini')
    section = None
    try:
        if mode == 'DEFAULT':
            section = config['default']
        elif mode == 'TEST':
            section = config['test']
    except KeyError:
        custom_logger('settings initialization not completed')

    if section:
        HOST_ADDRESS = section.get('host_address', 'localhost')
        RESTFUL_PORT = section.get('restful_port', '5001')
        FRONTEND_PORT = section.get('frontend_port', '5000')
        FAVMOVIES_RESTFUL_PATH = section.get('restful_path',
                                             '/restful/favmovies')
        DATABASE_URI = section.get('database_uri', 'sqlite:////tmp/default.db')
        HTTP_ADDRESS = 'http://' + HOST_ADDRESS + ':' + RESTFUL_PORT
        FULL_ADDRESS = HTTP_ADDRESS+FAVMOVIES_RESTFUL_PATH
        return True
    else:
        return False
