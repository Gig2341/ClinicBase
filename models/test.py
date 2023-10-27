#!/usr/bin/python3
""" Holds class Test """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Test(BaseModel, Base):
    """ Representation of tests """
    __tablename__ = 'tests'
    retinoscopy = Column(String(128))
    autorefraction = Column(String(128))
    sudjective_refraction = Column(String(128))
    other_tests = Column(String(128))
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    case_id = Column(String(60), ForeignKey('cases.id'), nullable=False)
