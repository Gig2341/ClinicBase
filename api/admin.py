#!/usr/bin/python3
""" API for creatind admin """

from dashboards import bcrypt
from api import bp_api
from flask import abort, jsonify, request
from flask_cors import cross_origin
from models.custom_user import Admin
from models import storage


@bp_api.route('/create_admin', methods=['POST'], strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def create_admin():
    """Creates a new employee"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")

    password = data['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    data['password'] = hashed_password
    admin = Admin(**data)
    admin.save()
    return jsonify(admin.to_dict()), 201
