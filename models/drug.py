#!/usr/bin/python3
""" Holds class Drug """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey


class Drug(BaseModel, Base):
    """ Representation of drugs """
    __tablename__ = 'drugs'
    drug = Column(Text, nullable=False)
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    case_id = Column(String(60), ForeignKey('cases.id'), nullable=False)
