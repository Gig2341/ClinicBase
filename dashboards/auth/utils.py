#!/usr/bin/python3
""" login and authentication utils """

from dashboards import bcrypt, login_manager
from models import storage
from flask import session, redirect, url_for
from datetime import datetime, timedelta
from models.receptionist import Receptionist
from models.optometrist import Optometrist
from models.custom_user import User

dbsession = storage._DBStorage__session


def custom_authentication(app, user_email, user_pass):
    admin_email = app.config.get('ADMIN_EMAIL')
    admin_password = app.config.get('ADMIN_PASSWORD')
    admin_id = app.config.get('ADMIN_ID')
    admin_name = app.config.get('ADMIN_NAME')
    if user_email == admin_email and user_pass == admin_password:
        custom_admin = User(
            id=admin_id,
            name=admin_name,
            email=admin_email,
            password=admin_password
        )
        session.permanent = True
        session['permanent_session_lifetime'] = timedelta(minutes=30)
        session['custom_user'] = {
                                  'user_data': custom_admin,
                                  'last_activity': datetime.now()
        }
        return custom_admin

    user = dbsession.query(Optometrist, Receptionist)\
        .filter_by(email=user_email).first()
    if user and bcrypt.check_password_hash(user.password, user_pass):
        return user
    return None


def check_inactivity(session_key, max_inactive_min=10):
    if session_key in session:
        user_data = session[session_key]['user_data']
        last_activity = session[session_key]['last_activity']
        current_time = datetime.now()
        inactive_min = (current_time - last_activity).total_seconds() / 60

        if inactive_min > max_inactive_min:
            session.pop(session_key)
            return True
    return False


@login_manager.user_loader
def load_user(user_id):
    return dbsession.query(Optometrist, Receptionist).get(user_id)
