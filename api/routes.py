#!/usr/bin/python3
""" API routes """

from api import bp_api
from flask import abort, jsonify, request
from flask_cors import cross_origin
from models.case import Case
from models.diagnosis import Diagnosis
from models.drug import Drug
from models.examination import Examination
from models.history import History
from models.lens import Lens
from models.optometrist import Optometrist
from models.patient import Patient
from models.receptionist import Receptionist
from models.test import Test
from models import storage


@bp_api.route('/your_route')
@cross_origin(origins=["0.0.0.0"])
def your_route_function():
    # route logic here
    pass
