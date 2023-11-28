#!/usr/bin/python3
""" routes for main """

from flask import render_template
from dashboards.landing_page import bp_main


@bp_main.route("/", strict_slashes=False)
@bp_main.route("/home", strict_slashes=False)
def home():
    """ route for homepage """
    return render_template('home.html', current_page='home')


@bp_main.route("/about", strict_slashes=False)
def about():
    """ route for about page """
    return render_template('about.html', current_page='about')


@bp_main.route("/contact", strict_slashes=False)
def contact():
    """ route for contact page """
    return render_template('contact.html', current_page='contact')
