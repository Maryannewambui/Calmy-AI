from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from ai_model import predict_stress
from flask_cors import CORS
from werkzeug.utils import secure_filename
from voice_analysis import predict_voice_stress
from temperature_analysis import predict_temp_stress

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/stress_db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "supersecret")

# Initialize Database & JWT
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Default Route
@app.route("/")
def home():
    return jsonify({"message": "Calmy AI"})

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
            "hrv_stress": hrv_stress,
            "voice_stress": voice_stress,
            "temp_stress": temp_stress,
            "combined_stress": round(float(combined_stress), 2)  # Round for readability
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
