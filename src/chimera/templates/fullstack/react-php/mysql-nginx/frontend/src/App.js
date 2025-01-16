import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8094';

const App = () => {
  const [dbStatus, setDbStatus] = useState('Checking...');
  const [dbVersion, setDbVersion] = useState('');

  useEffect(() => {
    const checkDatabaseStatus = async () => {
      try {
        const response = await fetch(`${API_URL}/api/db-status`, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          credentials: 'omit'
        });
        
        const data = await response.json();
        if (data.success) {
          setDbStatus('Connected');
          setDbVersion(data.version);
        } else {
          setDbStatus('Disconnected');
        }
      } catch (error) {
        console.error('Error:', error);
        setDbStatus('Error connecting to database');
      }
    };

    checkDatabaseStatus();
  }, []);

  return (
    <div className="app-container">
      <h1>ChimeraStack React + PHP Development Environment</h1>

      <section className="stack-overview">
        <h2>Stack Overview</h2>
        <table className="status-table">
          <thead>
            <tr>
              <th>Component</th>
              <th>Details</th>
              <th>Access</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Frontend</td>
              <td>React</td>
              <td>
                <a href="http://localhost:3003" target="_blank" rel="noopener noreferrer">
                  localhost:3003
                </a>
              </td>
            </tr>
            <tr>
              <td>Backend API</td>
              <td>Nginx + PHP-FPM</td>
              <td>
                <a href={`${API_URL}/api`} target="_blank" rel="noopener noreferrer">
                  localhost:8094/api
                </a>
              </td>
            </tr>
            <tr>
              <td>Database</td>
              <td>MySQL</td>
              <td>localhost:3306</td>
            </tr>
            <tr>
              <td>Database GUI</td>
              <td>phpMyAdmin</td>
              <td>
                <a href="http://localhost:8095" target="_blank" rel="noopener noreferrer">
                  localhost:8095
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <section className="quick-links">
        <h2>Quick Links</h2>
        <ul>
          <li>
            <a href={`${API_URL}/api`} target="_blank" rel="noopener noreferrer">
              API Status
            </a>
          </li>
          <li>
            <a href="http://localhost:8095" target="_blank" rel="noopener noreferrer">
              phpMyAdmin
            </a>
          </li>
        </ul>
      </section>

      <section>
        <h2>Database Connection Status</h2>
        <div className={`status-indicator ${dbStatus === 'Connected' ? 'status-success' : 'status-error'}`}>
          {dbStatus === 'Connected'
            ? `✔ Connected to MySQL Server ${dbVersion}`
            : `✖ ${dbStatus}`}
        </div>
      </section>
    </div>
  );
};

export default App;
