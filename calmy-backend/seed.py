from app import app, db

# Initialize Database
with app.app_context():
    db.create_all()
