from datetime import datetime
import uuid
from . import db

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    clues = db.Column(db.PickleType, nullable=False)  # Store as a list
    fun_fact = db.Column(db.PickleType, nullable=False)
    trivia = db.Column(db.PickleType, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    score = db.Column(db.Integer, default=0)

class Challenge(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    inviter_username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    invitee_username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=True)  # For the invitee
    inviter_score = db.Column(db.Integer, nullable=False)  # Store inviter's score
    invitee_status = db.Column(db.String(20), default="pending")  # Store invitee's status: 'pending', 'accepted'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    inviter = db.relationship("User", foreign_keys=[inviter_username])
    invitee = db.relationship("User", foreign_keys=[invitee_username])

