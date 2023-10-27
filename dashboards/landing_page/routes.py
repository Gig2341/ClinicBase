#!/usr/bin/python3
""" routes for main """

from flask import render_template
from dashboards.landing_page import bp_main


@bp_main.route("/")
@bp_main.route("/home")
def home():
    return render_template('index.html')


@bp_main.route("/about")
def about():
    return render_template('about.html')


@bp_main.route("/contact")
def contact():
    return render_template('contact.html')
