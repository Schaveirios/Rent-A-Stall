import os
from functools import wraps
from flask import abort, flash
from models import Users, dbase
from flask_login import current_user

def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_role() not in roles:
                abort(403)
                flash('Authentication error, please check your details and try again', 'error')
            return f(*args, **kwargs)

        return wrapped

    return wrapper

def get_role():
    role = Users.query.filter_by(roleID=current_user.roleID).first()
    return role.roleID
