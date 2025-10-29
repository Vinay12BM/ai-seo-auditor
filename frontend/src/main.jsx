// frontend/src/main.jsx
// This file uses ReactDOM.createRoot(document.getElementById('root')) to match the HTML.

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx'; 
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);