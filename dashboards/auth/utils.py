#!/usr/bin/python3
""" login and authentication utils """

from dashboards import bcrypt, login_manager
from models import storage
from flask import session, redirect, url_for
from datetime import datetime, timedelta
from models.receptionist import Receptionist
from models.optometrist import Optometrist
from models.custom_user import User
from models.engine.db_storage import DBStorage

db_storage = DBStorage()
dbsession = db_storage.reload()


def custom_authentication(app, user_email, user_pass):
    """ logic for user authentication """
    admin_email = app.config.get('ADMIN_EMAIL')
    admin_password = app.config.get('ADMIN_PASSWORD')
    admin_id = app.config.get('ADMIN_ID')
    admin_name = app.config.get('ADMIN_NAME')
    if user_email == admin_email and user_pass == admin_password:
        custom_admin = User(admin_id, admin_name,
                            admin_email, admin_password)
        session.permanent = True
        session['permanent_session_lifetime'] = timedelta(minutes=30)
        session['custom_user'] = {
                                  'user_data': custom_admin,
                                  'last_activity': datetime.now()
        }
        return custom_admin

    user = dbsession.query(Receptionist).filter_by(email=user_email).first()
    if not user:
        user = dbsession.query(Optometrist).filter_by(email=user_email).first()
    if user and bcrypt.check_password_hash(user.password, user_pass):
        return user
    return None


def check_inactivity(session_key, max_inactive_min=10):
    """ Checks inactivity in custom session """
    if session_key in session:
        user_data = session[session_key]['user_data']
        last_activity = session[session_key]['last_activity']
        current_time = datetime.now()
        inactive_min = (current_time - last_activity).total_seconds() / 60

        if inactive_min > max_inactive_min:
            session.pop(session_key)
            return True
    return False


def is_accessible_user(user, page):
    """ logic to check if the user can access the given page """
    if isinstance(user, Receptionist) and 'receptionist' in page:
        return True
    if isinstance(user, Optometrist) and 'optometrist' in page:
        return True
    if isinstance(user, User) and 'administrator' in page:
        return True

    return False


def get_user_default_page(user):
    """ logic to determine the default page for each user type """
    if isinstance(user, Receptionist):
        return url_for('receptionist.recep')
    if isinstance(user, Optometrist):
        return url_for('optometrist.optom')
    return url_for('administrator.admin')


@login_manager.user_loader
def load_user(user_id):
    """ User loader """
    if 'custom_user' in session:
        user_data = session['custom_user']['user_data']
        return user_data

    user = storage.get(Receptionist, user_id)
    if not user:
        user = storage.get(Optometrist, user_id)
    return user
