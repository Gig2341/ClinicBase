#!/usr/bin/python3
""" routes for receptionist """

from flask import render_template
from dashboards.receptionist import bp_recep
from flask_login import login_required, current_user


@bp_recep.route("/recep", strict_slashes=False)
@login_required
def dashboard_recep():
    """ route for receptionist dashboard """
    return render_template('recep.html')
