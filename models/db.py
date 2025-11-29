"""
This module initializes the SQLAlchemy database object.

This central `db` object is used throughout the application to interact
with the database, define models, and execute queries. It is initialized
here to prevent circular import issues.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
