#!/usr/bin/python3
""" Blueprint for administrator """

from flask import Blueprint

bp_admin = Blueprint('admin', __name__)

from dashboards.administrator import routes
