#!/usr/bin/python3
""" Holds class Case """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Case(BaseModel, Base):
    """ Representation of cases """
    __tablename__ = 'cases'
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    optometrist_id = Column(String(60), ForeignKey('optometrists.id'),
                            nullable=False)
    diagnoses = relationship("Diagnosis", backref="case", cascade="delete")
    examinations = relationship("Examination", backref="case",
                                cascade="delete")
    histories = relationship("History", backref="case", cascade="delete")
    tests = relationship("Test", backref="case", cascade="delete")
    lenses = relationship("Lens", backref="case", cascade="delete")
    drugs = relationship("Drug", backref="case", cascade="delete")
