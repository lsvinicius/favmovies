import requests
from requests.auth import HTTPBasicAuth

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
        pass
    return response

def favmovies_call(user, method='GET', params=None):
    response = {'Response':False, 'Error':'Something went wrong.'}
    try:
        if method == 'GET':
            response = requests.get(FULL_ADDRESS+'/'+user.get_id())
        elif method == 'POST':
            response = requests.post(FULL_ADDRESS+'/'+user.get_id(), data={'movies':params})
        response = response.json()
    except requests.exceptions.RequestException as e:
        pass
    print(response)
    return response
