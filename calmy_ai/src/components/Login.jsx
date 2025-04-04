import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import banner from '../assets/banner.jpg';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('https://calmy-ai.onrender.com/login', { email, password });
      if (response.status === 200) {
        localStorage.setItem('token', response.data.token);
        navigate('/'); // Redirect to the home page
      }
        } catch (err) {
      setError('Invalid email or password');
        }
      };
        
      
      return (
        <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundImage: 'url("https://source.unsplash.com/1600x900/?nature,calm")',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
        >
      <div
        style={{
          width: '400px',
          padding: '30px',
          borderRadius: '12px',
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          boxShadow: '0 8px 16px rgba(0, 0, 0, 0.2)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <img
        src={banner}
        alt="Banner"	
        style={{ width: '100px', height: '100px', objectFit: 'contain' }}
          />
        </div>
        <h2 style={{ textAlign: 'center', color: '#007BFF', fontFamily: 'Arial, sans-serif' }}>Welcome Back</h2>
        {error && <p style={{ color: 'red', textAlign: 'center', fontWeight: 'bold' }}>{error}</p>}
        <form onSubmit={handleLogin}>
          <div style={{ marginBottom: '20px' }}>
        <label
          htmlFor="email"
          style={{
            display: 'block',
            marginBottom: '8px',
            color: '#333',
            fontWeight: 'bold',
            fontFamily: 'Arial, sans-serif',
          }}
        >
          Email
        </label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{
            width: '100%',
            padding: '12px',
            borderRadius: '6px',
            border: '1px solid #ccc',
            fontSize: '16px',
          }}
        />
          </div>
          <div style={{ marginBottom: '20px' }}>
        <label
          htmlFor="password"
          style={{
            display: 'block',
            marginBottom: '8px',
            color: '#333',
            fontWeight: 'bold',
            fontFamily: 'Arial, sans-serif',
          }}
        >
          Password
        </label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{
            width: '100%',
            padding: '12px',
            borderRadius: '6px',
            border: '1px solid #ccc',
            fontSize: '16px',
          }}
        />
          </div>
          <button
        type="submit"
        style={{
          width: '100%',
          padding: '12px',
          backgroundColor: '#007BFF',
          color: '#fff',
          border: 'none',
          borderRadius: '6px',
          fontSize: '16px',
          fontWeight: 'bold',
          cursor: 'pointer',
          transition: 'background-color 0.3s',
        }}
        onMouseOver={(e) => (e.target.style.backgroundColor = '#0056b3')}
        onMouseOut={(e) => (e.target.style.backgroundColor = '#007BFF')}
          >
        Login
          </button>
        </form>
        <p style={{ textAlign: 'center', marginTop: '15px', color: '#555', fontSize: '14px' }}></p>
          Don't have an account? <a href="/register" style={{ color: '#007BFF', textDecoration: 'none' }}>Sign up</a>
        
      </div>
        </div>
      );
    };
    export default Login;

