#!/usr/bin/python3
""" Blueprint for authentication """

from flask import Blueprint

bp_auth = Blueprint('auth', __name__)

from dashboards.auth import routes
