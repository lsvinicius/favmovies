import requests
from src.custom_log import custom_logger
#Restful API address config
HOST_ADDRESS = 'localhost'
PORT = '5001'
HTTP_ADDRESS = 'http://' + HOST_ADDRESS + ':' + PORT
FAVMOVIES_RESTFUL_PATH = '/restful/favmovies'
FULL_ADDRESS = HTTP_ADDRESS+FAVMOVIES_RESTFUL_PATH

def query_omdb(params):
    response = {'Response':False,'Error':'Something went wrong.'}
    try:
        response = requests.get("http://www.omdbapi.com/?", params=params)
        response = response.json()
    except requests.exceptions.RequestException as e:
        custom_logger('query_omdb: exception raised {}'.format(e))
    return response

def favmovies_call(user, method='GET', params=None):
    response = {'Response':False, 'Error':'Something went wrong.'}
    request_address = FULL_ADDRESS+'/'+user.get_id()
    try:
        if method == 'GET':
            if params is None:
                response = requests.get(request_address)
            else:
                response = requests.get(request_address+'/'+params['imdbID'])
        elif method == 'POST':
            response = requests.post(request_address, data={'movies':params})
        elif method == 'PUT':
            response = requests.put(request_address+'/'+params['imdbID'], data=params)
        elif method == 'DELETE':
            response = requests.delete(request_address+'/'+params['imdbID'])
        response = response.json()
    except requests.exceptions.RequestException as e:
        custom_logger('favmovies_call: exception raised {}'.format(e))
    return response
