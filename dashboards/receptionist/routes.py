#!/usr/bin/python3
""" routes for receptionist """

from flask import render_template
from dashboards.receptionist import bp_recep


@bp_recep.route("/recep")
def recep():
    return render_template('recep.html')
