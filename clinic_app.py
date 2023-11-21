#!/usr/bin/python3
""" Flask Application """

from models import storage
from dashboards import create_app
from flask import render_template

app = create_app()


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    return render_template('custom_404.html'), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
