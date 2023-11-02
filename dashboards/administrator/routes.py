#!/usr/bin/python3
""" routes for admin """

from flask import render_template
from dashboards.administrator import bp_admin
from flask_login import current_user, login_required


@bp_admin.route("/admin", strict_slashes=False)
@login_required
def dashboard_admin():
    """ route for administrators dashboard """
    return render_template('admin.html')
