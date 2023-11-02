#!/usr/bin/python3
""" routes for optometrists """

from flask import render_template
from dashboards.optometrist import bp_optom
from flask_login import login_required, current_user


@bp_optom.route("/optom", strict_slashes=False)
@login_required
def dashboard_optom():
    """" route for optometrist dashboard """
    return render_template('optom.html')
