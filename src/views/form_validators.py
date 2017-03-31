import re
from validate_email import validate_email
from werkzeug.exceptions import HTTPException
from flask import abort

def valid_register_form(form):
    is_valid = True
    is_valid = validate_email(form.get('email')) and is_valid
    if not is_valid:
        abort(400, {'description':'Invalid email'})
    regex = r'^[^\W\d]+$'
    firstname = form.get('firstname')
    lastname = form.get('lastname')
    password = form.get('password')
    if firstname:
        is_valid = re.search(regex, firstname.strip(), re.UNICODE) and is_valid
    else:
        is_valid = False

    if not is_valid:
        abort(400, {'description':'Invalid firstname'})

    if lastname:
        is_valid = re.search(regex, lastname.strip(), re.UNICODE) and is_valid
    else:
        is_valid = False

    if not is_valid:
        abort(400, {'description':'Invalid lastname'})

    if password:
        is_valid = len(password) > 0 and is_valid
    else:
        is_valid = False

    if not is_valid:
        abort(400, {'description': 'Invalid password'})

    return is_valid
