from flask import Blueprint, request, jsonify
from src.model.user import User
from src.model.movie import Movie
from src.database import db
from src.api_consumption import query_omdb

favmovies = Blueprint('favmovies', __name__, template_folder='templates')
MOVIE_NOT_FOUND = {'Response':'Movie not found'}
USER_NOT_FOUND = {'Response':'User not found'}

@favmovies.route('/restful/favmovies/<user_id>', methods=['GET'])
def favmovies_get(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(favmovies=[movie.serialize for movie in user.movies])
    else:
        return jsonify(USER_NOT_FOUND)

@favmovies.route('/restful/favmovies/<user_id>/<imdbID>', methods=['GET'])
def favmovies_get_single(user_id, imdbID):
    user = User.query.get(user_id)
    if user:
        movie = user.get_movie_by_imdbID(imdbID)
        if movie:
            return jsonify(movie.serialize) if movie is not None else jsonify({})
        else:
            return jsonify(MOVIE_NOT_FOUND)
    else:
        return jsonify(USER_NOT_FOUND)

@favmovies.route('/restful/favmovies/<user_id>', methods=['POST'])
def favmovies_post(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify(USER_NOT_FOUND)
    checked_movies = request.form.getlist('movies')
    added_movies = []
    for imdbID in checked_movies:
        result = query_omdb({'i': imdbID})
        if result.get('Response') == "True":
            movie = Movie(imdbID=result['imdbID'],
                          title=result['Title'], plot=result['Plot'], type=result['Type'], poster=result['Poster'], year=result['Year'], comment='')
            if user.get_movie_by_imdbID(movie.imdbID) is None:
                user.movies.append(movie)
                added_movies.append(movie)
    db.session.commit()
    return jsonify(added_movies=[movie.serialize for movie in added_movies])

@favmovies.route('/restful/favmovies/<user_id>/<imdbID>', methods=['PUT'])
def favmovies_put(user_id, imdbID):
    user = User.query.get(user_id)
    if user:
        movie = user.get_movie_by_imdbID(imdbID)
        if movie:
            movie.comment = request.form['comment']
            db.session.commit()
            return jsonify({'Response':'Updated successfully'})
        else:
            return jsonify(MOVIE_NOT_FOUND)
    else:
        return jsonify(USER_NOT_FOUND)

@favmovies.route('/restful/favmovies/<user_id>/<imdbID>', methods=['DELETE'])
def favmovies_delete(user_id, imdbID):
    user = User.query.get(user_id)
    if user:
        movie = user.get_movie_by_imdbID(imdbID)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return jsonify({'Response':'Deleted successfully'})
        else:
            return jsonify(MOVIE_NOT_FOUND)
    else:
            return jsonify(USER_NOT_FOUND)
