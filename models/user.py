"""
This module defines the SQLAlchemy data models for the application,
including the User model.
"""
from .db import db


class User(db.Model):
    """
    Represents a user in the database.

    Attributes:
        id (int): The primary key for the user.
        name (str): The name of the user.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the User object.
        """
        return f"User: {self.name} - ID: {self.id}"
