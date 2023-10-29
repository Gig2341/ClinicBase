#!/usr/bin/python3
""" routes for optometrists """

from flask import render_template
from dashboards.optometrist import bp_optom


@bp_optom.route("/optom")
def optom():
    return render_template('optom.html')
