import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>{{ project_name }}</h1>
        <p>
          Welcome to your ChimeraStack React application!
        </p>
        <div className="card">
          <h2>🚀 Quick Start</h2>
          <p>Edit <code>src/App.tsx</code> and save to reload.</p>
        </div>

        <div className="card">
          <h2>📋 Project Information</h2>
          <ul>
            <li><strong>Project Name:</strong> {{ project_name }}</li>
            <li><strong>Running on Port:</strong> {{ ports.frontend }}</li>
            <li><strong>ChimeraStack Version:</strong> v{{ cli_version }}</li>
          </ul>
        </div>
      </header>
    </div>
  );
}

export default App;
