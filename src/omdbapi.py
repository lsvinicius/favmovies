import requests

def query_omdb(kwargs):
    response = {'Response':'False','Error':'Something went wrong.'}
    try:
        response = requests.get("http://www.omdbapi.com/?", params=kwargs)
        response = response.json()
    except requests.exceptions.RequestException as e:
        pass
    return response
