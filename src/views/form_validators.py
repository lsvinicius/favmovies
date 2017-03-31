import re
from validate_email import validate_email
from werkzeug.exceptions import HTTPException
from flask import abort
from src.model.movie import user

def valid_register_form(form):
    is_valid = True
    is_valid = validate_email(form.get('email')) and is_valid
    if is_valid:
        user = User.query.filter_by(email:form.get('email'))
        if user:
            abort(400, {'description':'User already registered'})
    else:
        abort(400, {'description':'Invalid email'})

    regex = r'^[^\W\d]+$'
    firstname = form.get('firstname')
    if firstname:
        is_valid = re.search(regex, firstname.strip(), re.UNICODE) and is_valid
    else:
        abort(400, {'description':'Invalid firstname'})

    lastname = form.get('lastname')
    if lastname:
        is_valid = re.search(regex, lastname.strip(), re.UNICODE) and is_valid
    else:
        abort(400, {'description':'Invalid lastname'})

    password = form.get('password')
    if password:
        is_valid = len(password) > 0 and is_valid
    else:
        abort(400, {'description': 'Invalid password'})

    return is_valid
