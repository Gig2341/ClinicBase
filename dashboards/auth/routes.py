#!/usr/bin/python3
""" Handle the user session routes """

from dashboards.auth import bp_auth
from flask import (request, redirect, url_for, flash, render_template,
                   )current_app
from flask_login import login_user, logout_user, current_user
from dashboards.auth.utils import (custom_authentication, check_inactivity,
                                   is_accessible_user, get_user_default_page)


@bp_auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """ handles session login """
    if current_user.is_authenticated:
        redirect_to = get_user_default_page(current_user)
        return redirect(redirect_to)

    next_page = request.args.get('next')
    redirect_to = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = custom_authentication(current_app, email, password)

        if user:
            login_user(user, remember=True)
            flash('Login successful.', 'success')

            if next_page and is_accessible_user(user, next_page):
                redirect_to = next_page

            if not redirect_to:
                redirect_to = get_user_default_page(user)

            return redirect(redirect_to)
        else:
            flash('Login failed. Please check your credentials.', 'danger')

    return render_template('login.html')


@bp_auth.route('/logout', strict_slashes=False)
def logout():
    """ handles session logout """
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))


@bp_auth.before_request
def before_request():
    """ handles expiration of custom session """
    if check_inactivity('custom_user'):
        logout_user()
        return redirect(url_for('auth.login'))
