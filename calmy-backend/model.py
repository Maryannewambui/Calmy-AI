from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Move db here

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Ensure primary key is set
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    health_data = db.relationship('HealthData', backref='user', lazy=True)  # Ensure relationship is defined

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
def init_db(app):
    with app.app_context():  # Ensure the app context is pushed
        db.create_all()  # Create all tables
        print("Database tables created successfully.")  # Debugging log

