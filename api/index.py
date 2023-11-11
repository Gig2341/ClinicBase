#!/usr/bin/python3
""" API index routes """

from api import bp_api
from flask_login import login_required
from flask import abort, jsonify, request, make_response
import uuid
from datetime import date, datetime
from models.case import Case
from models.patient import Patient
from models.engine.db_storage import DBStorage

storage = DBStorage()
session = storage.reload()


@bp_api.route('/status', methods=['GET'], strict_slashes=False)
@login_required
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@bp_api.route('/patient_count', methods=['POST'], strict_slashes=False)
@login_required
def patient_count():
    """ Returns the number of patients within a specified time """
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    start_date = data.get('start_date', date.min.isoformat())
    end_date = data.get('end_date', date.today().isoformat())
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    today = datetime.today()
    if start_date > today:
        start_date = today
    if end_date > today:
        end_date = today

    patient_count = session.query(Patient)\
        .filter(Patient.updated_at.between(start_date, end_date)).count()

    response = make_response(jsonify({'patient_count': patient_count}))
    response.headers['ETag'] = str(uuid.uuid4())
    return response


@bp_api.route('/case_count', methods=['POST'], strict_slashes=False)
@login_required
def case_count():
    """ Returns the number of cases within a specified time """
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    start_date = data.get('start_date', date.min.isoformat())
    end_date = data.get('end_date', date.today().isoformat())
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    today = datetime.today()
    if start_date > today:
        start_date = today
    if end_date > today:
        end_date = today

    case_count = session.query(Case)\
        .filter(Case.updated_at.between(start_date, end_date)).count()

    response = make_response(jsonify({'case_count': case_count}))
    response.headers['ETag'] = str(uuid.uuid4())
    return response
