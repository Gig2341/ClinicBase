#!/usr/bin/python3
""" Flask Application """

from models import storage
from dashboards import create_app


app = create_app()
app.app_context().push()


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
