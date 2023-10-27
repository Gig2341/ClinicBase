#!/usr/bin/python3
""" Blueprint for optometrist """

from flask import Blueprint

bp_optom = Blueprint('optom', __name__)

from dashboards.optometrist import routes
