#!/usr/bin/python3
""" Holds class Examination """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Examination(BaseModel, Base):
    """ Representation of examinations """
    __tablename__ = 'examinations'
    visual_acuity = Column(String(1024), nullable=False)
    ocular_exam = Column(String(1024), nullable=False)
    chief_complaint = Column(String(1024), nullable=False)
    on_direct_questions = Column(String(1024))
    iop = Column(String(1024))
    blood_pressure = Column(String(1024))
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    case_id = Column(String(60), ForeignKey('cases.id'), nullable=False)
