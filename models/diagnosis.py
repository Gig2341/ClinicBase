#!/usr/bin/python3
""" Holds class Diagnosis """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Diagnosis(BaseModel, Base):
    """ Representation of diagnoses """
    __tablename__ = 'diagnoses'
    principal_diagnosis = Column(String(1024), nullable=False)
    other_diagnosis_1 = Column(String(1024))
    other_diagnosis_2 = Column(String(1024))
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    case_id = Column(String(60), ForeignKey('cases.id'), nullable=False)
