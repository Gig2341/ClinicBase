#!/usr/bin/python3
"""Defines a dummy User class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from flask_login import UserMixin


class Admin(BaseModel, Base, UserMixin):
    """ Represent a custom User for admin session creation """
    __tablename__ = 'administrator'
    email = Column(String(128), nullable=False)
    password = Column(String(60), nullable=False)
