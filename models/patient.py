#!/usr/bin/python3
""" Holds class Patient """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.orm import relationship


class Patient(BaseModel, Base):
    """ Representation of patients """
    __tablename__ = 'patients'
    firstname = Column(String(60), nullable=False)
    surname = Column(String(60), nullable=False)
    dob = Column(Date, nullable=False)
    tel = Column(String(20), nullable=False)
    occupation = Column(String(128))
    insurance = Column(String(128))
    cases = relationship("Case", backref="patient", cascade="delete")
    diagnoses = relationship("Diagnosis", backref="patient", cascade="delete")
    examinations = relationship("Examination", backref="patient",
                                cascade="delete")
    histories = relationship("History", backref="patient", cascade="delete")
    tests = relationship("Test", backref="patient", cascade="delete")
    lenses = relationship("Lens", backref="patient", cascade="delete")
    drugs = relationship("Drug", backref="patient", cascade="delete")
