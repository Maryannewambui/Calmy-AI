import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.losses import MeanSquaredError

import joblib

# Scaling data for better LSTM performance
scaler = MinMaxScaler(feature_range=(0, 1))

# Define LSTM Model
def build_hrv_model():
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(10, 1)),  # 10 time steps
        LSTM(50),
        Dense(25, activation='relu'),
        Dense(1, activation='sigmoid')  # Output: stress level (0 to 1)
    ])
    model.compile(optimizer='adam', loss=MeanSquaredError())
    return model

# Train the model (Dummy Data for Testing)
def train_hrv_model():
    # Generate Simulated HRV Data
    np.random.seed(42)
    hrv_data = np.random.randint(40, 100, (500, 10))  # 500 samples, 10 HRV values each
    stress_labels = np.random.randint(0, 2, 500)  # Binary stress labels (0 = normal, 1 = stress)

    # Normalize data
    hrv_data = scaler.fit_transform(hrv_data)

    # Reshape for LSTM input (samples, time steps, features)
    hrv_data = np.reshape(hrv_data, (500, 10, 1))

    # Build and Train Model
    model = build_hrv_model()
    model.fit(hrv_data, stress_labels, epochs=10, batch_size=16, verbose=1)

    # Save model & scaler
    model.save("hrv_model.h5")
    joblib.dump(scaler, "scaler.pkl")
    print("Model & Scaler Saved!")

# Load Model & Make Predictions
def predict_stress(hrv_sequence):
    model = tf.keras.models.load_model("hrv_model.h5")
    scaler = joblib.load("scaler.pkl")

    # Normalize input
    hrv_sequence = scaler.transform([hrv_sequence])

    # Reshape for LSTM
    hrv_sequence = np.reshape(hrv_sequence, (1, 10, 1))

    # Predict stress level
    stress_level = model.predict(hrv_sequence)[0][0]
    return float(stress_level)  # Output between 0-1 (low to high stress)

def predict_hrv_stress(hrv_value):
    return predict_stress([hrv_value] * 10)

# Train Model (Run once)
if __name__ == "__main__":
    train_hrv_model()
