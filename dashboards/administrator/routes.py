#!/usr/bin/python3
""" routes for admin """

from flask import render_template
from dashboards.administrator import bp_admin


@bp_admin.route("/admin")
def admin():
    return render_template('admin.html')
