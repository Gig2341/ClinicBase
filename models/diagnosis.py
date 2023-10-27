#!/usr/bin/python3
""" Holds class Diagnosis """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey


class Diagnosis(BaseModel, Base):
    """ Representation of diagnoses """
    __tablename__ = 'diagnoses'
    principal_diagnosis = Column(Text, nullable=False)
    other_diagnosis_1 = Column(Text)
    other_diagnosis_2 = Column(Text)
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    case_id = Column(String(60), ForeignKey('cases.id'), nullable=False)
