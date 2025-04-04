import React, { useState } from 'react';
import axios from 'axios';

const Tester = () => {
  const [popupType, setPopupType] = useState(null); // To track which popup to show
  const [hrvValues, setHrvValues] = useState([]);
  const [temperature, setTemperature] = useState('');
  const [voiceFile, setVoiceFile] = useState(null);
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false); // Add loading state

  const handleSubmit = async () => {
    try {
      setLoading(true); // Show loading spinner
      let result;
      if (popupType === 'heartRate') {
        if (hrvValues.length !== 10) {
          alert('Please enter exactly 10 HRV values.');
          return;
        }
        result = await axios.post('https://calmy-ai.onrender.com/predict-stress', { hrv: hrvValues });
      } else if (popupType === 'voice') {
        if (!voiceFile) {
          alert('Please upload a voice file.');
          return;
        }
        const formData = new FormData();
        formData.append('audio', voiceFile);
        result = await axios.post('https://calmy-ai.onrender.com/predict-voice', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
      } else if (popupType === 'temperature') {
        if (!temperature) {
          alert('Please enter your temperature.');
          return;
        }
        result = await axios.post('https://calmy-ai.onrender.com/predict-temp', { temperature });
      } else if (popupType === 'fullCheck') {
        if (hrvValues.length !== 10 || !voiceFile || !temperature) {
          alert('Please provide all inputs (HRV, voice file, and temperature).');
          return;
        }
        const formData = new FormData();
        formData.append('hrv', hrvValues.join(','));
        formData.append('audio', voiceFile);
        formData.append('temperature', temperature);
        result = await axios.post('https://calmy-ai.onrender.com/predict-combined-stress', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
      }
      setResponse(result.data);
      setPopupType(null); // Close popup after submission
    } catch (error) {
      alert('An error occurred. Please try again.');
    } finally {
      setLoading(false); // Hide loading spinner
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Stress and Fatigue Tester</h1>
      <div style={styles.buttonSection}>
        <button style={styles.button} onClick={() => setPopupType('heartRate')}>Heart Rate Check</button>
        <button style={styles.button} onClick={() => setPopupType('voice')}>Voice Check</button>
        <button style={styles.button} onClick={() => setPopupType('temperature')}>Temp Check</button>
        <button style={styles.button} onClick={() => setPopupType('fullCheck')}>Full Check</button>
      </div>

      {popupType && (
        <div style={styles.popup}>
          <div style={styles.popupContent}>
            {popupType === 'heartRate' && (
              <>
                <h3 style={styles.popupTitle}>Enter 10 HRV Values</h3>
                <textarea
                  style={styles.textarea}
                  placeholder="Enter 10 values separated by commas"
                  onChange={(e) => setHrvValues(e.target.value.split(',').map(Number))}
                />
              </>
            )}
            {popupType === 'voice' && (
              <>
                <h3 style={styles.popupTitle}>Upload Voice Recording (WAV)</h3>
                <input type="file" accept=".wav" onChange={(e) => setVoiceFile(e.target.files[0])} />
              </>
            )}
            {popupType === 'temperature' && (
              <>
                <h3 style={styles.popupTitle}>Enter Your Temperature</h3>
                <input
                  type="number"
                  step="0.1"
                  placeholder="Enter temperature"
                  style={styles.input}
                  onChange={(e) => setTemperature(e.target.value)}
                />
              </>
            )}
            {popupType === 'fullCheck' && (
              <>
                <h3 style={styles.popupTitle}>Full Check</h3>
                <textarea
                  style={styles.textarea}
                  placeholder="Enter 10 HRV values separated by commas"
                  onChange={(e) => setHrvValues(e.target.value.split(',').map(Number))}
                />
                <input type="file" accept=".wav" onChange={(e) => setVoiceFile(e.target.files[0])} />
                <input
                  type="number"
                  step="0.1"
                  placeholder="Enter temperature"
                  style={styles.input}
                  onChange={(e) => setTemperature(e.target.value)}
                />
              </>
            )}
            <div style={styles.popupButtons}>
              <button style={styles.submitButton} onClick={handleSubmit}>Submit</button>
              <button style={styles.cancelButton} onClick={() => setPopupType(null)}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      {loading && <div style={styles.spinner}></div>} {/* Add spinner */}

      <div style={styles.responseSection}>
        <h3 style={styles.responseTitle}>Response</h3>
        {response && (
          <div>
            <p style={styles.responseText}>Stress Level: {response.stress_level}</p>
            <p style={styles.responseText}>
              Recommendation:{' '}
              {response.stress_level < 0.5
                ? 'Your stress level is low. Keep maintaining a healthy lifestyle!'
                : 'Your stress level is high. Consider taking a break, meditating, or consulting a professional.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    padding: '20px',
    backgroundColor: '#f5f5f5',
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  title: {
    fontSize: '2rem',
    color: '#333',
    marginBottom: '20px',
  },
  buttonSection: {
    display: 'flex',
    gap: '15px',
    marginBottom: '30px',
  },
  button: {
    padding: '10px 20px',
    fontSize: '1rem',
    color: '#fff',
    backgroundColor: '#007BFF',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  },
  popup: {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  popupContent: {
    backgroundColor: '#fff',
    padding: '20px',
    borderRadius: '10px',
    width: '400px',
    textAlign: 'center',
  },
  popupTitle: {
    fontSize: '1.2rem',
    marginBottom: '15px',
  },
  textarea: {
    width: '100%',
    height: '80px',
    marginBottom: '15px',
    padding: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  },
  input: {
    width: '100%',
    padding: '10px',
    marginBottom: '15px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  },
  popupButtons: {
    display: 'flex',
    justifyContent: 'space-between',
  },
  submitButton: {
    padding: '10px 20px',
    backgroundColor: '#28a745',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  cancelButton: {
    padding: '10px 20px',
    backgroundColor: '#dc3545',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  responseSection: {
    marginTop: '30px',
    padding: '20px',
    backgroundColor: '#fff',
    borderRadius: '10px',
    width: '80%',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },
  responseTitle: {
    fontSize: '1.5rem',
    marginBottom: '15px',
    color: '#333',
  },
  responseText: {
    fontSize: '1rem',
    color: '#555',
  },
  spinner: {
    border: '4px solid #f3f3f3',
    borderTop: '4px solid #007BFF',
    borderRadius: '50%',
    width: '40px',
    height: '40px',
    animation: 'spin 1s linear infinite',
    margin: '20px auto',
  },
  '@keyframes spin': {
    '0%': { transform: 'rotate(0deg)' },
    '100%': { transform: 'rotate(360deg)' },
  },
};

export default Tester;
