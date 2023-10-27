#!/usr/bin/python3
""" Holds class History """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class History(BaseModel, Base):
    """ Representation of histories """
    __tablename__ = 'histories'
    p_ocular_hx = Column(String(128), nullable=False, default="None")
    p_medical_hx = Column(String(128), nullable=False, default="None")
    f_ocular_hx = Column(String(128), nullable=False, default="None")
    f_medical_hx = Column(String(128), nullable=False, default="None")
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    case_id = Column(String(60), ForeignKey('cases.id'), nullable=False)
