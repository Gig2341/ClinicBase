#!/usr/bin/python3
""" Holds class Examination """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey


class Examination(BaseModel, Base):
    """ Representation of examinations """
    __tablename__ = 'examinations'
    visual_acuity = Column(Text, nullable=False)
    ocular_exam = Column(Text, nullable=False)
    chief_complaint = Column(Text, nullable=False)
    on_direct_questions = Column(Text)
    iop = Column(Text)
    blood_pressure = Column(Text)
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    case_id = Column(String(60), ForeignKey('cases.id'), nullable=False)
