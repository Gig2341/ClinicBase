#!/usr/bin/python3
""" API eployees speficic routes """

from flask import abort, jsonify, request
from flask_login import login_required
from dashboards import bcrypt
from api import bp_api
from models.optometrist import Optometrist
from models.receptionist import Receptionist
from models import storage


def get_employee_by_id(employee_id):
    """" Get employee handler """
    employee = storage.get(Receptionist, employee_id)
    if not employee:
        employee = storage.get(Optometrist, employee_id)
    return employee


@bp_api.route('/get_employee/<employee_id>', strict_slashes=False)
@login_required
def get_employee(employee_id):
    """ Returns employee's updated information """
    employee = get_employee_by_id(employee_id)
    if not employee:
        abort(404)
    return jsonify(employee.to_dict())


@bp_api.route('/employee', methods=['POST'], strict_slashes=False)
@login_required
def post_employee():
    """Creates a new employee"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    required_fields = ['name', 'email', 'password', 'role']
    if not all(field in data for field in required_fields):
        abort(400, description="Missing or invalid fields")

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
    else:
        abort(400, description="Invalid role")

    password = data['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    employee.password = hashed_password

    employee.save()
    return jsonify(employee.to_dict()), 201


@bp_api.route('/employees/<employee_id>', methods=['PUT'],
              strict_slashes=False)
@login_required
def put_employee(employee_id):
    """ Updates an employee's information """
    employee = get_employee_by_id(employee_id)
    if not employee:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore = ['id', 'name', 'password', 'created_at', 'updated']

    for key, value in data.items():
        if key not in ignore:
            setattr(employee, key, value)

    if 'password' in data:
        password = data['password']
        hashed_password = bcrypt.generate_password_hash(password)\
            .decode('utf-8')
        data['password'] = hashed_password

    storage.save()
    return jsonify(employee.to_dict()), 200


@bp_api.route('/employees/<employee_id>', methods=['DELETE'],
              strict_slashes=False)
@login_required
def delete_employee(employee_id):
    """ Deletes a receptionist or an optometrist who is without a case """
    employee = get_employee_by_id(employee_id)
    if not employee:
        abort(404)

    if isinstance(employee, Optometrist) and employee.cases:
        abort(400, description="Optometrist has a case")

    employee.delete()
    storage.save()
    return jsonify(employee.to_dict()), 200
