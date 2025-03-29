from app import db
from datetime import datetime

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Health Data Model
class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    heart_rate = db.Column(db.Float, nullable=False)
    hrv = db.Column(db.Float, nullable=False)
    skin_temperature = db.Column(db.Float, nullable=False)
    voice_analysis = db.Column(db.String(255), nullable=True)
    stress_level = db.Column(db.Float, nullable=True)
    fatigue_level = db.Column(db.Float, nullable=True)

# Create Tables
def init_db():
    db.create_all()
