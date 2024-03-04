from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    """
    Model class representing a note.

    Attributes:
        id (int): The unique identifier of the note.
        data (str): The content of the note.
        date (datetime): The date and time when the note was created.
        user_id (int): The foreign key referencing the user who created the note.
    """
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    """
    Model class representing a user.

    Attributes:
        id (int): The unique identifier of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        notes (relationship): The relationship between the user and their notes.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')