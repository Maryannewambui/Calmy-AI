import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import signup from './components/Signup';
import login from './components/Login';
import Home from './components/Home';
import tester from './components/Tester';

import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<signup />} />
        <Route path="/login" element={<login />} />
        <Route path="/tester" element={<tester />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
