#!/usr/bin/python3
""" API patient specific routes """

from api import bp_api
from flask import abort, jsonify, request
from flask_cors import cross_origin
from datetime import datetime
from models.patient import Patient
from models import storage


@bp_api.route('/get_patient/<patient_id>', strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def get_patient(patient_id):
    """ Returns patient's updated information """
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404)
    patient.updated_at = datetime.utcnow()
    storage.save()
    return jsonify(patient.to_dict())


@bp_api.route('/patients', methods=['POST'], strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def post_patient():
    """ Creates a new patient """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'firstname' not in request.get_json():
        abort(400, description="Missing firstname")
    if 'surname' not in request.get_json():
        abort(400, description="Missing surname")
    if 'dob' not in request.get_json():
        abort(400, description="Missing date of birth")
    if 'tel' not in request.get_json():
        abort(400, description="Missing telephone number")
    data = request.get_json()
    patient = Patient(**data)
    patient.save()
    return jsonify(patient.to_dict()), 201


@bp_api.route('/patients/<patient_id>', methods=['PUT'], strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def put_patient(patient_id):
    """ Updates a patient's information """
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'firstname', 'surname', 'dob', 'created_at', 'updated']
    for key, value in request.get_json().items():
        if key not in ignore:
            setattr(patient, key, value)
    storage.save()
    return jsonify(patient.to_dict()), 200


@bp_api.route('/patients/<patient_id>', methods=['DELETE'],
              strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def delete_patient(patient_id):
    """ Deletes a patient who is without a case  """
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404)
    if patient.cases:
        abort(400, description="Patient has a case")
    patient.delete()
    storage.save()
    return jsonify({}), 200
