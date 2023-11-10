#!/usr/bin/python3
""" Handle the user session routes """

from dashboards.auth import bp_auth
from flask import request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, current_user
from dashboards.auth.utils import custom_authentication, redirect_dashboard


@bp_auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """ handles session login """
    if current_user.is_authenticated:
        return redirect_dashboard(current_user)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = custom_authentication(email, password)
        if user:
            login_user(user, remember=True)
            flash('Login successful.', 'success')
            return redirect_dashboard(user)
        else:
            flash('Login failed. Please check your credentials.', 'danger')

    return render_template('login.html')


@bp_auth.route('/logout', strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
