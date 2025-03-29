import numpy as np
import librosa
import librosa.display
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import StandardScaler
import joblib
from tensorflow.keras.losses import MeanSquaredError

import os

# Initialize scaler for feature normalization
scaler = StandardScaler()

# Function to Extract Audio Features
def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=22050)  # Load audio file
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # Extract 13 MFCC features
    mean_mfcc = np.mean(mfcc, axis=1)  # Get mean values
    return mean_mfcc

# Define LSTM Model
def build_voice_model():
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(13, 1)),  # 13 MFCC features
        LSTM(50),
        Dense(25, activation='relu'),
        Dense(1, activation='sigmoid')  # Output: stress probability (0-1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Train Model (Using Simulated Data)
def train_voice_model():
    np.random.seed(42)

    # Generate Dummy MFCC Data (500 samples)
    voice_data = np.random.rand(500, 13)  # 13 MFCCs per sample
    stress_labels = np.random.randint(0, 2, 500)  # 0 = normal, 1 = stressed

    # Normalize Features
    voice_data = scaler.fit_transform(voice_data)

    # Reshape for LSTM (samples, time steps, features)
    voice_data = np.reshape(voice_data, (500, 13, 1))

    # Build & Train Model
    model = build_voice_model()
    model.fit(voice_data, stress_labels, epochs=10, batch_size=16, verbose=1)

    # Save model & scaler
    model.save("voice_model.h5")
    joblib.dump(scaler, "voice_scaler.pkl")
    print("Voice Model & Scaler Saved!")

# Predict Stress from Voice
def predict_voice_stress(audio_file):
    model_path = os.path.join(os.path.dirname(__file__), "voice_model.h5")
    scaler_path = os.path.join(os.path.dirname(__file__), "voice_scaler.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}")

    custom_objects = {"mse": MeanSquaredError()}
    model = tf.keras.models.load_model(model_path, custom_objects=custom_objects)
    scaler = joblib.load(scaler_path)

    # Extract Features
    features = extract_features(audio_file)

    # Normalize
    features = scaler.transform([features])

    # Reshape for LSTM
    features = np.reshape(features, (1, 13, 1))

    # Predict
    stress_level = model.predict(features)[0][0]
    return float(stress_level)  # Output between 0-1 (low to high stress)
# Train Model
if __name__ == "__main__":
    train_voice_model()
