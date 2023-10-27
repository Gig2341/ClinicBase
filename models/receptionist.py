#!/usr/bin/python3
""" Holds class Receptionist """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from flask_login import UserMixin


class Receptionist(BaseModel, Base, UserMixin):
    """ Representation of receptionist user """
    __tablename__ = 'receptionists'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(60), nullable=False)
