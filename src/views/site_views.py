from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
from flask_login import login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from src.model.user import User
from src.database import db
from src.password import hash_password
from src.api_consumption import query_omdb, favmovies_call
from src.views.form_validators import valid_register_form
from src.custom_log import custom_logger
from src import settings
site_views = Blueprint('site_views', __name__, template_folder='templates')

@site_views.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('site_views.logged'))
    else:
        return render_template('index.jinja')

@site_views.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('site_views.logged'))
    elif request.method=='GET':
        return render_template('register.jinja')
    elif valid_register_form(request.form):
        email = request.form['email']
        name = request.form['firstname'].strip()+ ' ' + request.form['lastname'].strip()
        password = request.form['password']
        hashed_password = hash_password(password)
        user = User(name, hashed_password, email)
        db.session.add(user)
        db.session.commit()
        custom_logger('register: user {} add'.format(user.email))
        return redirect(url_for('site_views.login'))
    else:
        custom_logger('register: invalid form register, redirecting to register page. this probably means there is a bad request not aborted by valid_register_form', lvl=logging.DEBUG)
        return redirect(url_for('site_views.register'))

@site_views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('site_views.logged'))
    if request.method=='GET':
        return render_template('login.jinja')
    else:
        email = request.form['email']
        password = hash_password(request.form['password'])
        user = User.query.filter_by(email=email, password=password).first()
        if user is None:
            abort(400, {'description':'Invalid login'})
        else:
            login_user(user)
            return redirect(url_for('site_views.logged'))

@site_views.route('/logged', methods=['GET'])
@login_required
def logged():
    return render_template('logged.jinja', user=current_user)

@site_views.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('site_views.index'))

@site_views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'GET':
        return render_template('search.jinja', response=None)
    else:
        s = request.form.get('title')
        if s is None or s == '':
            abort(400, {'description':'Invalid title to be searched'})
        params= { 's': s }
        response = query_omdb(params)
        return render_template('search.jinja', response=response)

@site_views.route('/favmovies', methods=['GET', 'POST'])
@site_views.route('/favmovies/<imdbID>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def favmovies(imdbID=None):
    custom_logger('favmovies: client issued {} request'.format(request.method))
    if request.method == 'GET':
        if imdbID is None:
            custom_logger('favmovies: client issued GET request for movies list')
            response = favmovies_call(user=current_user)
            return render_template('favmovies.jinja', response=response, address=settings.HOST_ADDRESS, frontend_port=settings.FRONTEND_PORT)
        else:
            custom_logger('favmovies: client issued GET request for single movie')
            response = favmovies_call(user=current_user, params={'imdbID':imdbID})
            return render_template('favmovie_single.jinja', address=settings.HOST_ADDRESS, frontend_port = settings.FRONTEND_PORT, movie=response)
    elif request.method == 'POST':
        response = favmovies_call(user=current_user, method='POST', params=request.form.getlist('movies'))
        return redirect(url_for('site_views.logged'))
    elif request.method == 'PUT': #called via ajax
        comment = request.form['comment']
        response = favmovies_call(user=current_user, method='PUT',
                                  params={'imdbID':imdbID, 'comment':comment})
        return response['Response']
    elif request.method == 'DELETE': #called via ajax
        response = favmovies_call(user=current_user, method='DELETE', params={'imdbID':imdbID})
        return response['Response']
