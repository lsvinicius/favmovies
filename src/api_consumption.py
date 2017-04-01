import requests
from src.custom_log import custom_logger
from src import settings

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
    request_address = settings.FULL_ADDRESS+'/'+user.get_id()
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
