#!/usr/bin/python3
""" Flask application instance """

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    login_manager.init_app(app)

    from api import bp_api
    from dashboards.auth import bp_auth
    from dashboards.landing_page import bp_main
    from dashboards.administrator import bp_admin
    from dashboards.receptionist import bp_recep
    from dashboards.optometrist import bp_optom
    app.register_blueprint(bp_api)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_recep)
    app.register_blueprint(bp_optom)

    return app
