#!/usr/bin/python3
""" Flask Application API """

from flask import Blueprint, make_response, jsonify
from flask_cors import CORS

bp_api = Blueprint('api', __name__, url_prefix='/api')
cors = CORS(bp_api, resources={r"/api/v1/*": {"origins": "*"}})


@bp_api.errorhandler(404)
def not_found(error):
    """ 404 Error """
    return make_response(jsonify({'error': "Not found"}), 404)

"""from app.api import users, errors, tokens"""
