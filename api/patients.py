#!/usr/bin/python3
""" API patient specific routes """

from api import bp_api
from flask import abort, jsonify, request
from flask_login import login_required
from datetime import datetime
from models.patient import Patient
from models import storage


def get_patient_by_id(patient_id):
    """ Helper function to get patient by ID """
    patient = storage.get(Patient, patient_id)
    return patient


@bp_api.route('/get_patient/<patient_id>', strict_slashes=False)
@login_required
def get_patient(patient_id):
    """ Returns patient's updated information """
    patient = get_patient_by_id(patient_id)
    if not patient:
        abort(404)
    patient.updated_at = datetime.utcnow()
    storage.save()
    return jsonify(patient.to_dict())


@bp_api.route('/patients', methods=['POST'], strict_slashes=False)
@login_required
def post_patient():
    """ Creates a new patient """
    data = request.get_json()
    required_fields = ['firstname', 'surname', 'dob', 'tel']

    if not data:
        abort(400, description="Not a JSON")
    if not all(field in data for field in required_fields):
        abort(400, description="Missing or invalid fields")

    patient = Patient(**data)
    patient.save()
    return jsonify(patient.to_dict()), 201


@bp_api.route('/patients/<patient_id>', methods=['PUT'], strict_slashes=False)
@login_required
def put_patient(patient_id):
    """ Updates a patient's information """
    patient = get_patient_by_id(patient_id)
    if not patient:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    ignore = ['id', 'firstname', 'surname', 'dob', 'created_at', 'updated']
    for key, value in request.get_json().items():
        if key not in ignore:
            setattr(patient, key, value)

    storage.save()
    return jsonify(patient.to_dict()), 200


@bp_api.route('/patients/<patient_id>', methods=['DELETE'],
              strict_slashes=False)
@login_required
def delete_patient(patient_id):
    """ Deletes a patient who is without a case  """
    patient = get_patient_by_id(patient_id)
    if not patient:
        abort(404)

    if patient.cases:
        abort(400, description="Patient has a case")

    patient.delete()
    storage.save()
    return jsonify(patient.to_dict()), 200
