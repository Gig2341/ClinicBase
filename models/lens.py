#!/usr/bin/python3
""" Holds class Lens """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Lens(BaseModel, Base):
    """ Representation of lenses """
    __tablename__ = 'lenses'
    lens_rx = Column(String(128), nullable=False)
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    case_id = Column(String(60), ForeignKey('cases.id'), nullable=False)
