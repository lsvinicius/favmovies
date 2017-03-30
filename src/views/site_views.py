import hashlib
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from src.model.user import User
from src.database import db
from src.omdbapi import query_omdb

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
    else:
        email = request.form['email']
        name = request.form['firstname']+ ' ' + request.form['lastname']
        password = request.form['password']
        hashed_password = hash_password(password)
        user = User(name, hashed_password, email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('site_views.login'))

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
            return redirect(url_for('site_views.login', error='Invalid login'))
        else:
            login_user(user)
            return redirect(url_for('site_views.logged'))

@site_views.route('/logged', methods=['GET'])
@login_required
def logged():
    return render_template('logged.jinja', user=User.query.get(current_user.get_id()))

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
        s = request.form['title']
        params= { 's': s }
        response = query_omdb(params)
        return render_template('search.jinja', response=response)

def hash_password(password):
    return hashlib.sha512(password.encode('utf-8')).hexdigest()
