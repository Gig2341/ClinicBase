#!/usr/bin/python3
""" login and authentication utils """

from dashboards import bcrypt, login_manager
from models import storage
from flask import url_for
from models.receptionist import Receptionist
from models.optometrist import Optometrist
from models.custom_user import Admin
from models.engine.db_storage import DBStorage

db_storage = DBStorage()
session = db_storage.reload()


def custom_authentication(user_email, user_pass):
    """ logic for user authentication """
    user_types = [Admin, Receptionist, Optometrist]

    for user_type in user_types:
        user = session.query(user_type).filter_by(email=user_email).first()
        if user and bcrypt.check_password_hash(user.password, user_pass):
            return user
    return None


@login_manager.user_loader
def load_user(user_id):
    """ User loader """
    user_types = [Admin, Receptionist, Optometrist]

    for user_type in user_types:
        user = storage.get(user_type, user_id)
        if user:
            return user
    return None
