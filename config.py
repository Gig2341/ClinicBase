#!/usr/bin/python3
""" Contains the class Config """

from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    ADMIN_NAME = getenv('ADMIN_NAME')
    ADMIN_EMAIL = getenv('ADMIN_EMAIL')
    ADMIN_ID = getenv('ADMIN_ID')
    ADMIN_PASSWORD = getenv('ADMIN_PASSWORD')
