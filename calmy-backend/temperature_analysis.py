import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import StandardScaler
import joblib

# Initialize scaler for normalization
scaler = StandardScaler()

# Function to Train Temperature Model
def train_temp_model():
    np.random.seed(42)

    # Simulated Data (Skin Temperature in Celsius)
    temp_data = np.random.normal(loc=36.5, scale=0.5, size=(500, 1))  # Normal Temp = 36.5°C
    stress_labels = np.array([1 if t > 37.5 or t < 36.0 else 0 for t in temp_data])  # 1 = stressed, 0 = normal

    # Normalize Features
    temp_data = scaler.fit_transform(temp_data)

    # Define Model
    model = Sequential([
        Dense(10, activation='relu', input_shape=(1,)),  
        Dense(5, activation='relu'),
        Dense(1, activation='sigmoid')  # Output: stress probability (0-1)
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train Model
    model.fit(temp_data, stress_labels, epochs=10, batch_size=16, verbose=1)

    # Save Model & Scaler
    model.save("temp_model.h5")
    joblib.dump(scaler, "temp_scaler.pkl")
    print("Temperature Model & Scaler Saved!")

# Function to Predict Stress from Skin Temperature
def predict_temp_stress(temp_value):
    model = tf.keras.models.load_model("temp_model.h5")
    scaler = joblib.load("temp_scaler.pkl")

    # Normalize Input
    temp_value = np.array([[temp_value]])
    temp_value = scaler.transform(temp_value)

    # Predict Stress Level
    stress_level = model.predict(temp_value)[0][0]
    return stress_level  # Output between 0-1 (low to high stress)

# Train Model (Run Once)
if __name__ == "__main__":
    train_temp_model()
