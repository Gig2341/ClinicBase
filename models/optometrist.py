#!/usr/bin/python3
""" Holds class Optometrist """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Optometrist(BaseModel, Base, UserMixin):
    """ Representation of optometrists """
    __tablename__ = 'optometrists'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(60), nullable=False)
    license = Column(String(128), nullable=False)
    cases = relationship("Case", backref="optometrist", cascade="delete")
