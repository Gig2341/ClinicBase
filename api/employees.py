#!/usr/bin/python3
""" API eployees speficic routes """

from dashboards import bcrypt
from api import bp_api
from flask import abort, jsonify, request
from flask_cors import cross_origin
from models.optometrist import Optometrist
from models.receptionist import Receptionist
from models import storage


@bp_api.route('/get_employee/<employee_id>', strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def get_employee(employee_id):
    """ Returns employee's updated information """
    employee = storage.get(Receptionist, employee_id)
    if not employee:
        employee = storage.get(Optometrist, employee_id)
    if not employee:
        abort(404)
    return jsonify(employee.to_dict())


@bp_api.route('/employee', methods=['POST'], strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def post_employee():
    """Creates a new employee"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    if 'role' not in data:
        abort(400, description="Missing role")

    password = data['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    data['password'] = hashed_password

    role = data.get('role').lower()
    if role == "receptionist":
        data.pop('role', None)
        data.pop('license', None)
        employee = Receptionist(**data)
    elif role == "optometrist":
        if 'license' not in data:
            abort(400, description="Missing license")
        data.pop('role', None)
        employee = Optometrist(**data)
    employee.save()
    return jsonify(employee.to_dict()), 201


@bp_api.route('/employees/<employee_id>', methods=['PUT'],
              strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def put_employee(employee_id):
    """ Updates an employee's  information """
    employee = storage.get(Receptionist, employee_id)
    if not employee:
        employee = storage.get(Optometrist, employee_id)
    if not employee:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()    
    ignore = ['id', 'name', 'created_at', 'updated']

    if 'password' in data:
        password = data['password']
        hashed_password = bcrypt.generate_password_hash(password)\
            .decode('utf-8')
        data['password'] = hashed_password

    for key, value in data.items():
        if key not in ignore:
            setattr(employee, key, value)
    storage.save()
    return jsonify(employee.to_dict()), 200


@bp_api.route('/employees/<employee_id>', methods=['DELETE'],
              strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def delete_employee(employee_id):
    """ Deletes a recept or an optom who is without a case  """
    employee = storage.get(Receptionist, employee_id)
    if not employee:
        employee = storage.get(Optometrist, employee_id)
    if not employee:
        abort(404)
    if isinstance(employee, Optometrist) and hasattr(employee, 'cases'):
        abort(400, description="Optom has a case")
    employee.delete()
    storage.save()
    return jsonify({}), 200
