from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from src.model.user import User
from src.model.movie import Movie
from src.database import db
from src.omdbapi import query_omdb

favmovies = Blueprint('favmovies', __name__, template_folder='templates')

@favmovies.route('/favmovies', methods=['GET'])
@login_required
def favmovies_get():
    return jsonify(favmovies=[movie.serialize for movie in current_user.movies])

@favmovies.route('/favmovies', methods=['POST'])
@login_required
def favmovies_post():
    checked_movies = request.form.getlist('movies')
    added_movies = []
    for imdbID in checked_movies:
        result = query_omdb({'i': imdbID})
        movie = Movie(imdbID=result['imdbID'],
                      title=result['Title'], plot=result['Plot'], type=result['Type'], poster=result['Poster'])
        if current_user.get_movie_by_imdbID(movie.imdbID) is None:
            current_user.movies.append(movie)
            added_movies.append(movie)
    db.session.add(current_user)
    db.session.commit()
    return jsonify(added_movies=[movie.serialize for movie in added_movies])

@favmovies.route('/favmovies/<id>', methods=['PUT'])
@login_required
def favmovies_put(id):
    pass

@favmovies.route('/favmovies/<id>', methods=['DELETE'])
@login_required
def favmovies_delete(id):
    pass
