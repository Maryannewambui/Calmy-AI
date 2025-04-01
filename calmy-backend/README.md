# CALMY AI - BACKEND
This document contains the backend of the calmy AI

1️⃣ Tech Stack
✅ Backend Framework: Flask 
✅ AI & ML Libraries:

- TensorFlow / PyTorch for deep learning models

- scikit-learn for preprocessing and classical ML

- pandas, numpy for data handling
✅ Database: PostgreSQL 

✅ API Testing: Postman

✅ Authentication: Flask-JWT-Extended 

✅ Deployment: Render 

2️⃣ How The Backend Will Work
Data Collection (from wearable APIs & user inputs)

- Heart Rate Variability (HRV)

- Skin Temperature

- Voice Input (optional)

- User Feedback (stress levels, fatigue symptoms)

- Preprocessing & Analysis

- Normalize heart rate & skin temp data

- Extract voice features using Librosa

- Run AI models for stress & fatigue detection

AI Model Processing

LSTM (Long Short-Term Memory) for time-series analysis of HRV

CNN + RNN Hybrid for voice tone analysis

Random Forest / SVM for final classification

API Response

Returns Stress & Fatigue Score (0-100)

Provides Personalized Recommendations (e.g., breathing exercises)

3️⃣ API Data for Testing
We'll use public datasets and simulated API responses before integrating real-time wearable APIs.

Example Test Data
json
Copy
Edit
{
  "user_id": "12345",
  "timestamp": "2025-03-27T12:30:00Z",
  "heart_rate": 85,
  "hrv": 45,
  "skin_temperature": 36.5,
  "voice_input": "I am feeling really exhausted today.",
  "stress_level": null,
  "fatigue_level": null
}
Wearable Device APIs (Example Sources)
Garmin Health API - HRV, Heart Rate

Fitbit API - Stress & Heart Rate Monitoring

WHOOP API - Sleep & Recovery Metrics

For voice processing, we’ll test with:

Librosa + Pretrained NLP models for tone analysis

4️⃣ Step-by-Step Backend Development Plan
Step 1: Set Up Flask Backend (Create project structure)
Step 2: Build API Endpoints (/analyze, /recommendations)
Step 3: Integrate AI Models (LSTM for HRV, CNN for voice)
Step 4: Test API with Sample Data (Postman, Swagger)
Step 5: Connect to PostgreSQL Database
Step 6: Deploy on Render


# RENDER Deplpoyed link
https://calmy-ai.onrender.com


