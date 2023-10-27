#!/usr/bin/python3
""" Blueprint for receptionist """

from flask import Blueprint

bp_recep = Blueprint('recep', __name__)

from dashboards.receptionist import routes
