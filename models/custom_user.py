#!/usr/bin/python3
"""Defines a dummy User class."""

from flask_login import UserMixin


class User(UserMixin):
    """ Represent a custom User Class for admin session creation """

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
