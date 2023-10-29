#!/usr/bin/python3
""" API cases routes """

from api import bp_api
from flask import abort, jsonify, request
from flask_cors import cross_origin
from datetime import date, datetime
from models.case import Case
from models.patient import Patient
from sqlalchemy import func, select
from models import storage
from models.engine.db_storage import DBStorage

db_storage = DBStorage()
session = db_storage.reload()


@bp_api.route('/get_case/<case_id>', strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def get_case(case_id):
    """ Returns patient's case """
    case = storage.get(Case, case_id)
    if not case:
        abort(404)
    return jsonify(case.to_dict())


@bp_api.route('/cases', methods=['POST'], strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def post_case():
    """ Creates a new case """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'patient_id' not in request.get_json():
        abort(400, description="Missing patient id")
    if 'optometrist_id' not in request.get_json():
        abort(400, description="Missing optometrist id")
    data = request.get_json()
    patient_id = data.get('patient_id')

    existing_case = session.query(Case).filter(
        Case.patient_id == patient_id,
        func.date(Case.created_at) == func.current_date()
    ).first()

    if not existing_case:
        case = Case(**data)
        case.save()
        return jsonify(case.to_dict())
    else:
        return jsonify(existing_case.to_dict())


@bp_api.route('/cases/prescription', methods=['GET'], strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def get_matched_patients():
    """ Gets patients' with prescription information """
    patients = session.query(Patient)\
        .filter(func.date(Patient.updated_at) == func.current_date()).all()

    matching_patients = []

    for patient in patients:
        if any((func.date(case.updated_at) == func.current_date and
               case.updated_at > case.created_at) for case in patient.cases):
            matching_patients.append(patient.to_dict())
    return jsonify(matching_patients)


@bp_api.route('/cases/queue', methods=['GET'], strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def patient_queue():
    """ Gets patients in queue """
    subquery = session.query(Case.patient_id)\
        .filter(Case.updated_at == Case.created_at).subquery()
    subquery_select = select([subquery.c.patient_id])
    patients = session.query(Patient)\
        .filter(Patient.updated_at == func.current_date())\
        .filter(Patient.id.in_(subquery_select)).all()
    patients_data = [patient.to_dict() for patient in patients]
    return jsonify(patients_data)


@bp_api.route('/medical_records/<patient_id>', methods=['POST'],
              strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def get_patient_records(patient_id):
    """ Returns the medical records of a patient """
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    start_date = data.get('start_date', date.min.isoformat())
    end_date = data.get('end_date', date.today().isoformat())
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    session = Session()
    cases = session.query(Case).filter(
        Case.patient_id == patient_id,
        Case.created_at.between(start_date, end_date)
    ).all()

    case_data = [case.to_dict() for case in cases]

    for case in case_data:
        case.pop("patient_id", None)

    return jsonify(case_data)


@bp_api.route('/cases/save/<case_id>', methods=['POST'], strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def save_case(case_id):
    """ Saves patient's medical records into a case """
    record_type_mapping = {
        'diagnoses': Diagnosis,
        'examinations': Examination,
        'histories': History,
        'tests': Test,
        'lenses': Lens,
        'drugs': Drug,
    }

    if not request.get_json():
        abort(400, description="Not a JSON")

    case = storage.get(Case, case_id)
    if not case:
        abort(404)

    data = request.get_json()
    ret = []

    if data:
        for record_type, record_data in data.items():
            if record_type in record_type_mapping:
                record_data[case_id] = case_id
                record_data['patient_id'] = case.patient_id

                RecordClass = record_type_mapping[record_type]

                record = RecordClass.query\
                    .filter_by(case_id=case_id).first()

                if record:
                    record.delete()
                    storage.save()

                record = RecordClass(**record_data)
                record.save()
                ret.append(record.to_dict())

    return jsonify(ret)


@bp_api.route('/cases/submit/<case_id>', methods=['POST'],
              strict_slashes=False)
@cross_origin(origins=["127.0.0.1"])
def submit_case(case_id):
    """Saves patient's medical records into a case"""
    record_type_mapping = {
        'diagnoses': Diagnosis,
        'examinations': Examination,
        'histories': History,
        'tests': Test,
        'lenses': Lens,
        'drugs': Drug,
    }

    if not request.get_json():
        abort(400, description="Not a JSON")

    case = storage.get(Case, case_id)
    if not case:
        abort(404)

    data = request.get_json()
    ret = []

    if data:
        for record_type, record_data in data.items():
            if record_type in record_type_mapping:
                record_data['case_id'] = case_id
                record_data['patient_id'] = case.patient_id

                RecordClass = record_type_mapping[record_type]

                record = session.query(RecordClass)\
                    .filter_by(case_id=case_id).first()

                if record:
                    for key, value in record_data.items():
                        setattr(record, key, value)
                        storage.save()
                else:
                    record = RecordClass(**record_data)
                    record.save()

                ret.append(record.to_dict())

    return jsonify(ret)
