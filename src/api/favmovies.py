from flask import Blueprint, request, jsonify
from src.model.user import User
from src.model.movie import Movie
from src.database import db
from src.api_consumption import query_omdb

favmovies = Blueprint('favmovies', __name__, template_folder='templates')

@favmovies.route('/restful/favmovies/<user_id>', methods=['GET'])
def favmovies_get(user_id):
    user = User.query.get(user_id)
    return jsonify(favmovies=[movie.serialize for movie in user.movies])

@favmovies.route('/restful/favmovies/<user_id>', methods=['POST'])
def favmovies_post(user_id):
    user = User.query.get(user_id)
    checked_movies = request.form.getlist('movies')
    added_movies = []
    print(checked_movies)
    for imdbID in checked_movies:
        result = query_omdb({'i': imdbID})
        if result.get('Response'):
            movie = Movie(imdbID=result['imdbID'],
                          title=result['Title'], plot=result['Plot'], type=result['Type'], poster=result['Poster'], year=result['Year'])
            if user.get_movie_by_imdbID(movie.imdbID) is None:
                user.movies.append(movie)
                added_movies.append(movie)
    db.session.add(user)
    db.session.commit()
    return jsonify(added_movies=[movie.serialize for movie in added_movies])

@favmovies.route('/restful/favmovies/<id>', methods=['PUT'])
def favmovies_put(id):
    pass

@favmovies.route('/restful/favmovies/<id>', methods=['DELETE'])
def favmovies_delete(id):
    pass
