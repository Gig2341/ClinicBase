from api import bp_api
from flask import abort, jsonify, request, make_response
from flask_login import current_user, login_required
from models import storage
from models.engine.db_storage import DBStorage
from models.case import Case
from models.patient import Patient
from models.diagnosis import Diagnosis
from models.examination import Examination
from models.history import History
from models.test import Test
from models.lens import Lens
from models.drug import Drug
from datetime import datetime
from sqlalchemy import func, select, and_
from sqlalchemy.orm import aliased
import uuid
from operator import attrgetter

db_storage = DBStorage()
session = db_storage.reload()


@bp_api.route('/get_case/<case_id>', strict_slashes=False)
@login_required
def get_case(case_id):
    """ Returns patient's case """
    case = storage.get(Case, case_id)
    if not case:
        abort(404)
    return jsonify(case.to_dict())


@bp_api.route('/cases/<patient_id>', strict_slashes=False)
@login_required
def new_case(patient_id):
    """ Creates a new case """
    data = {
        'optometrist_id': current_user.id,
        'patient_id': patient_id
    }

    existing_case = session.query(Case).filter(
        Case.patient_id == patient_id,
        func.date(Case.created_at) == datetime.utcnow().date()
    ).first()

    if not existing_case:
        case = Case(**data)
        case.save()
        return jsonify(case.to_dict())
    else:
        return jsonify(existing_case.to_dict())


@bp_api.route('/cases/completed', methods=['GET'], strict_slashes=False)
@login_required
def get_completed_cases():
    """ Gets completed cases with prescription information """
    patients = session.query(Patient)\
        .filter(func.date(Patient.updated_at) == datetime.utcnow().date())\
        .all()

    matching_cases = []

    for patient in patients:
        for case in patient.cases:
            if (
                func.date(case.updated_at) == datetime.utcnow().date()
                and case.updated_at > case.created_at
            ):
                matching_cases.append(case)

    matching_cases.sort(key=attrgetter("updated_at"), reverse=True)
    recent_case = matching_cases[:5]
    response = make_response(jsonify([case.to_dict() for case in recent_case]))
    response.headers['ETag'] = str(uuid.uuid4())
    return response


@bp_api.route('/cases/queue', methods=['GET'], strict_slashes=False)
@login_required
def patient_queue():
    """ Gets patients in queue """
    case_alias = aliased(Case)

    patients_with_cases = (
        session.query(Patient, case_alias)
        .outerjoin(case_alias, and_(
            case_alias.patient_id == Patient.id,
            case_alias.updated_at == case_alias.created_at
        ))
        .filter(func.date(Patient.updated_at) == datetime.utcnow().date())
        .all()
    )

    patients_without_cases = [
        patient for patient, case in patients_with_cases if case is None
    ]

    patients_data = [patient.to_dict() for patient in patients_without_cases]

    response = make_response(jsonify(patients_data))
    response.headers['ETag'] = str(uuid.uuid4())
    return response


@bp_api.route('/medical_records/<patient_id>', strict_slashes=False)
@login_required
def get_patient_records(patient_id):
    """ Returns the medical records of a patient """
    cases = session.query(Case).filter(
        Case.patient_id == patient_id
    ).order_by(Case.updated_at.desc()).all()

    case_data = [case.to_dict() for case in cases]
    for case in case_data:
        case.pop("patient_id", None)

    response = make_response(jsonify(case_data))
    response.headers['ETag'] = str(uuid.uuid4())
    return response


@bp_api.route('/cases/save/<case_id>', methods=['POST'], strict_slashes=False)
@login_required
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
                record_data['case_id'] = case_id
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
@login_required
def submit_case(case_id):
    """ Submit patient's medical records into a case for closure """
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

    case.updated_at = datetime.utcnow()
    storage.save()

    return jsonify(ret)
