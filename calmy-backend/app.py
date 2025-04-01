from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from werkzeug.security import generate_password_hash, check_password_hash
from ai_model import predict_stress
from flask_cors import CORS
from werkzeug.utils import secure_filename
from voice_analysis import predict_voice_stress
from temperature_analysis import predict_temp_stress
from model import db, User, HealthData, init_db
from flask_migrate import Migrate

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://calmy_ai_user:0HmXuHMizmxCCESzJzdy26QMIFvVl598@dpg-cvlqrvh5pdvs73fcqt30-a.oregon-postgres.render.com/calmy_ai"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "supersecret")

migrate = Migrate(app, db)

# Initialize Database & JWT
db.init_app(app)
jwt = JWTManager(app)

# Create tables
init_db(app)


# Default Route
@app.route("/")
def home():
    return jsonify({"message": "Calmy AI"})

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()  # Get data from request
    
    # Validate incoming data
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check if the user already exists
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"error": "User already exists"}), 400
    
    # Hash the password
    hashed_password = generate_password_hash(password)
    
    # Create a new user instance
    new_user = User(username=username, email=email, password=hashed_password)
    
    # Add to database
    try:
        db.session.add(new_user)
        db.session.commit()
        print(f"New user added: {new_user.username}")
        # Create JWT Token
        access_token = create_access_token(identity=new_user.id)  # JWT token with user ID
        
        return jsonify({
            "message": "User registered successfully",
            "access_token": access_token  # Send the token for subsequent requests
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Login Route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Generate a JWT token for the logged-in user
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        "message": "Login successful",
        "access_token": access_token  # The token for subsequent requests
    }), 200


# Predict Stress from HRV
@app.route("/predict-stress", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        hrv_sequence = data.get("hrv")  # Expecting a list of 10 HRV values

        if not hrv_sequence or len(hrv_sequence) != 10:
            return jsonify({"error": "Invalid HRV data. Provide exactly 10 values."}), 400

        stress_level = predict_stress(hrv_sequence)
        return jsonify({"stress_level": float(stress_level)})  # Convert before returning


    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Predict Stress from Voice
@app.route("/predict-voice", methods=["POST"])
def predict_voice():
    try:
        if "audio" not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        audio = request.files["audio"]

        if audio.filename == '':
            return jsonify({"error": "No selected file"}), 400  # Handle empty file

        filename = secure_filename(audio.filename)

        if not filename:
            return jsonify({"error": "Invalid file name"}), 400  # Handle invalid names

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Ensure the file is saved properly
        try:
            audio.save(file_path)
        except Exception as e:
            return jsonify({"error": f"File save error: {str(e)}"}), 500

        # Process the saved file
        stress_level = predict_voice_stress(file_path)
        
        return jsonify({"stress_level": float(stress_level)})


    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Predict Stress from Skin Temperature
@app.route("/predict-temp", methods=["POST"])
def predict_temp():
    try:
        data = request.get_json()
        temp_value = data.get("temperature")  # Expecting a single temperature value

        if temp_value is None:
            return jsonify({"error": "Temperature value is required"}), 400

        stress_level = predict_temp_stress(temp_value)  # Predict stress level
        
        return jsonify({"stress_level": float(stress_level)})  # Use stress_level, not prediction

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fetch User's Health Data
@app.route("/health-data", methods=["GET"])
@jwt_required()  # Protect this route, only accessible if the user is authenticated
def get_health_data():
    user_id = get_jwt_identity()  # Get user ID from the JWT token
    print(f"User ID: {user_id}")
    health_data = HealthData.query.filter_by(user_id=user_id).all()
    
    # If the user has no health data
    if not health_data:
        return jsonify({"message": "No health data found"}), 404
    
    # Return health data
    return jsonify({
        "health_data": [
            {
                "timestamp": data.timestamp,
                "heart_rate": data.heart_rate,
                "hrv": data.hrv,
                "skin_temperature": data.skin_temperature,
                "voice_analysis": data.voice_analysis,
                "stress_level": data.stress_level,
                "fatigue_level": data.fatigue_level
            }
            for data in health_data
        ]
    }), 200

@app.route("/predict-combined-stress", methods=["POST"])
def predict_combined_stress():
    try:
        # Get JSON data
        data = request.form

        # Extract HRV data
        hrv_sequence = data.get("hrv")
        if isinstance(hrv_sequence, str):  # Convert only if needed
            hrv_sequence = list(map(float, hrv_sequence.split(",")))
            if len(hrv_sequence) != 10:
                return jsonify({"error": "Invalid HRV data. Provide exactly 10 values."}), 400
            hrv_stress = predict_stress(hrv_sequence)
        else:
            hrv_stress = None  # No HRV input

        # Extract Temperature data
        temp_value = data.get("temperature")
        if temp_value:
            temp_value = float(temp_value)
            temp_stress = predict_temp_stress(temp_value)
        else:
            temp_stress = None  # No temperature input

        # Extract and Process Voice Data
        if "audio" in request.files:
            audio = request.files["audio"]
            if audio.filename == '':
                return jsonify({"error": "No selected audio file"}), 400

            filename = secure_filename(audio.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio.save(file_path)

            voice_stress = predict_voice_stress(file_path)
        else:
            voice_stress = None  # No voice input

        # Combine Stress Levels (Weighted Average)
        stress_scores = [s for s in [hrv_stress, temp_stress, voice_stress] if s is not None]
        
        if not stress_scores:
            return jsonify({"error": "No valid stress data provided."}), 400

        combined_stress = sum(stress_scores) / len(stress_scores)  # Average of available stress levels

        return jsonify({
            "hrv_stress": float(hrv_stress) if hrv_stress is not None else None,
            "voice_stress": float(voice_stress) if voice_stress is not None else None,
            "temp_stress": float(temp_stress) if temp_stress is not None else None,
            "combined_stress": round(float(combined_stress), 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
