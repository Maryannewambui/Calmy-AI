# calmy ai

# --- links ----
* **Backend - https://calmy-ai.onrender.com**

* **Frontend - https://calmy-ai-rho.vercel.app/**

* **Pitch Deck - https://www.canva.com/design/DAGi1WVdDlw/w0HL51bR8OTezKFYqZRQ1A/edit?utm_content=DAGi1WVdDlw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton**


# PROBLEM

In today's fast-paced world, stress and fatigue have become pervasive issues, adversely affecting individuals' mental and physical health. Chronic stress can lead to severe health problems such as heart disease, depression, and decreased cognitive function. 

# SOLUTION

Introducing Clamy AI, an AI-Powered Stress & Fatigue Monitoring System, a proactive approach to mental wellness. By leveraging advanced AI algorithms, our system provides real-time analysis of physiological and behavioral data, enabling early detection of stress and fatigue. Users receive personalized recommendations to manage their well-being effectively, fostering a healthier and more productive lifestyle.

# Technology Stack Selection

For a web application like Athena AI, a robust and scalable tech stack is crucial. Here's a suggested stack:

 - Frontend:
    - React: A popular JavaScript library for building dynamic and interactive user interfaces. It's component-based, making development and maintenance easier.
    - UI Library: Material UI or Ant Design for pre-built, responsive UI components, speeding up development and ensuring a consistent look and feel.
- Backend:
    - Python: A versatile and widely used language with excellent libraries for data science and web development.
    Framework: Flask is a microframework offering more flexibility. 

- Database:
    - PostgreSQL: A powerful, open-source relational database known for its reliability and scalability. It's suitable for storing structured user data, cycle information, and symptom logs.

- Libraries:
    - Keras
    - NumPy: For numerical computations.
    - Scikit-learn: For implementing various machine learning algorithms (classification, clustering, etc.).
    - TensorFloW: For more complex deep learning models if needed in the future 
    - gunicorn
    - JWT Authentication
- Deployment:
    - Render


# ## Project Structure

calmy-ai/
├── frontend/
│   └──  
| 
├── backend/
│   ├──  calmy-backend/
│   ├──  .gitignore
│   ├──  ai_model.py
│   ├──  app.py
│   ├──  hrv_model.h5
│   ├──  model.py
│   ├──  Pipfile
│   ├──  Pipfile.lock
│   ├──  Procfile
│   ├──  README.md
│   ├──  requirements.txt
│   ├──  scaler.pkl
│   ├──  seed.py
│   ├──  stress_board.py
│   ├──  stress.db
│   ├──  temp_model.h5
│   ├──  temp_scaler.pkl
│   ├──  temperature_analysis.py
│   ├──  voice_analysis.py
│   ├──  voice_model.h5
│   ├──  voice_scaler.pkl
│   ├──  __pycache__/
│   ├──  instance/
│   ├──  migrations/
    │   ├──alembic.ini
    │   ├──env.py
    │   ├──README
    │   ├──script.py.mako
│   ├──uploads/ 
|
└── README.md


## Implementation Steps

This project follows these key implementation steps:

1.  **Define the Problem and Scope:**
    * **Objective:** To develop an AI-powered web application that helps users understand and manage their stress and fatigue levels through personalized insights and recommendations.
    * **Target Users:** Individuals interested in proactively monitoring and improving their well-being, potentially early adopters of health technology.
    * **Key Metrics to Monitor:** Heart rate, voice levels, temperature levels

2.  **Data Collection:**
    * **Data Sources:** Currently utilizing simulated health data Future development will explore integration with APIs from wearable devices like Fitbit.
    * **Data Preprocessing:** Scripts handle data cleaning (e.g., handling missing values, outliers) and normalization to prepare data for model training.

3.  **Model Selection:**
    * **Task:** Anomaly detection (identifying unusual health patterns) and health recommendation (providing personalized advice).
    * **Algorithms:**
        * **Random Forest:** Used for classification tasks, such as identifying normal vs. abnormal heart rate patterns.
        * **LSTM (Long Short-Term Memory):** Employed for analyzing time-series data to predict future trends in health metrics and potential fatigue buildup.
    * **Libraries:** scikit-learn for traditional machine learning, TensorFlow for deep learning models.

4.  **Model Training and Evaluation:**
    * **Training:** Data is split into training and testing sets (e.g., 80-20 split) to train the machine learning models. 
    * **Evaluation Metrics:** Model performance is evaluated using metrics such as accuracy, precision, recall, and F1-score for classification tasks.
    * **Cross-Validation:** Techniques like cross-validation are used to ensure the models generalize well to unseen data. 

5.  **Build a User Interface:**
    * **Platform:** A web application is being developed using Flask (Python microframework) for the backend and React ViteJS for the frontend 
    * **Features:**
        * Displaying real-time (simulated for now) health metrics.
        * Showing anomaly alerts and potential recommendations.
        * Providing historical data visualization through charts and graphs.

6.  **Deployment :**
    * **RENDER** - we'll deploy the backend and postgresql
    * **VERCEL** - We will deploy the frontend / UI/UX design for customer use on vercel **

7.  **Testing and Validation:**
    * **Unit Testing:** Individual components of the application (e.g., data preprocessing functions, model inference)
    * **Integration Testing:** Ensuring that different parts of the system work together correctly (e.g., data flow from simulated source to the AI model and to the web app).
    * **User Testing:** Future plans include collecting feedback from target users to improve the system's usability and effectiveness.

8.  **Documentation and Reporting:**
    * **Documentation:** This `README.md` provides an overview of the project.

    * **Presentation:** A pitch deck has been created to showcase the project.

## Getting Started

### Prerequisites

* Python 3.8 or higher
* pip (Python package installer)

### Installation

1.  Clone the repository:
    ```bash
    git clone 
    cd calmy-ai

    ```
to go to the backend cd calmy-backend

2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  Install the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Web Application (Simulated Data)

1.  Run the Flask application:
    ```bash
    python app.py
    ```

2.  Open your web browser and go to `http://127.0.0.1:5000/` (or the address shown in your terminal).

## Running tests on the backend
1. Register a New User
📌 Endpoint: POST http://127.0.0.1:5000/register

Using cURL
Run this in your terminal:

curl -X POST http://127.0.0.1:5000/register -H "Content-Type: application/json" -d '{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword"
}'

2. Login
📌 Endpoint: POST http://127.0.0.1:5000/login
Using cURL
Run this in your terminal:

curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{
    "email": "testuser@example.com",
    "password": "testpassword"
}'

3. Fetch User Health Data (Authenticated)
📌 Endpoint: GET http://127.0.0.1:5000/health-data

Using cURL
Run this in your terminal:

curl -X GET http://127.0.0.1:5000/health-data -H "Authorization: Bearer <JWT_TOKEN>"
Replace <JWT_TOKEN> with your actual token.

4. Predict Stress from HRV
📌 Endpoint: POST http://127.0.0.1:5000/predict-stress

Using cURL
Run this in your terminal:

curl -X POST http://127.0.0.1:5000/predict-stress -H "Content-Type: application/json" -d '{
    "hrv": [50, 48, 46, 49, 47, 45, 44, 46, 48, 50]
}'

5. Predict Stress from Voice
📌 Endpoint: POST http://127.0.0.1:5000/predict-voice

Using cURL
Run this in your terminal:

curl -X POST http://127.0.0.1:5000/predict-voice -F "audio=@voice_sample.wav"
Replace voice_sample.wav with your actual audio file path.

6. Predict Stress from Temperature
📌 Endpoint: POST http://127.0.0.1:5000/predict-temp

Using cURL
Run this in your terminal:

curl -X POST http://127.0.0.1:5000/predict-temp -H "Content-Type: application/json" -d '{
    "temperature": 37.5
}'

7. Predict Combined Stress Levels
📌 Endpoint: POST http://127.0.0.1:5000/predict-combined-stress
Using cURL
Run this in your terminal:

curl -X POST http://127.0.0.1:5000/predict-combined-stress -F "hrv=50,48,46,49,47,45,44,46,48,50" -F "temperature=37.5" -F "audio=@voice_sample.wav"



## Handling Challenges

* **Data Privacy:** Strict adherence to data privacy regulations (e.g., GDPR if applicable to your user base, local Kenyan data protection laws) is a top priority. Data will be handled securely with user consent.
* **Model Accuracy:** Continuous monitoring and improvement of the AI models through ongoing data collection, fine-tuning of hyperparameters, and evaluation of performance metrics.
* **Scalability:** The system is being designed with scalability in mind, utilizing cloud-based solutions and containerization technologies to handle a growing number of users and data.

## Expected Outcomes

* A functional AI-powered health monitoring web application.
* A user-friendly interface for visualizing health data and receiving personalized recommendations.
* A well-structured codebase with documentation.
* Demonstrated application of machine learning techniques to a real-world health monitoring problem.

## Why This Project?

* **Relevance:** Addressing the critical and growing issue of stress and fatigue with a proactive and personalized AI-driven solution.
* **Skill Development:** Provides hands-on experience in data preprocessing, machine learning model development, web application development, and deployment.
* **Portfolio:** A valuable project to showcase technical skills and understanding of AI in healthcare.

## License

This project is licensed under the [MIT License](LICENSE).


