#!/usr/bin/python3
""" Blueprint for main """

from flask import Blueprint

bp_main = Blueprint('main', __name__)

from dashboards.landing_page import routes
