#!/usr/bin/python3
""" login and authentication utils """

from dashboards import bcrypt, login_manager
from models import storage
from flask import redirect, url_for
from models.receptionist import Receptionist
from models.optometrist import Optometrist
from models.custom_user import Admin
from models.engine.db_storage import DBStorage

db_storage = DBStorage()
session = db_storage.reload()


def custom_authentication(user_email, user_pass):
    """ logic for user authentication """
    user = session.query(Admin).filter_by(email=user_email).first()
    if not user:
        user = session.query(Receptionist).filter_by(email=user_email).first()
    if not user:
        user = session.query(Optometrist).filter_by(email=user_email).first()
    if user and bcrypt.check_password_hash(user.password, user_pass):
        return user
    return None


@login_manager.user_loader
def load_user(user_id):
    """ User loader """
    user = storage.get(Admin, user_id)
    if not user:
        user = storage.get(Receptionist, user_id)
    if not user:
        user = storage.get(Optometrist, user_id)
    return user
