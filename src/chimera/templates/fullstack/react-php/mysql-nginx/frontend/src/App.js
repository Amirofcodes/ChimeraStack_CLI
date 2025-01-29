import React, { useState, useEffect } from "react";
import "./App.css";

const API_URL = process.env.REACT_APP_API_URL;
const FRONTEND_PORT = process.env.REACT_APP_PORT;
const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT;
const PHPMYADMIN_PORT = process.env.REACT_APP_PHPMYADMIN_PORT;
const MYSQL_PORT = process.env.REACT_APP_MYSQL_PORT;

const App = () => {
  const [dbStatus, setDbStatus] = useState("Checking...");
  const [dbVersion, setDbVersion] = useState("");
  const [dbConfig, setDbConfig] = useState(null);

  useEffect(() => {
    const checkDatabaseStatus = async () => {
      try {
        const response = await fetch(`${API_URL}/api/db-status`, {
          method: "GET",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          credentials: "omit",
        });

        const data = await response.json();
        if (data.success) {
          setDbStatus("Connected");
          setDbVersion(data.version);
          setDbConfig(data.config);
        } else {
          setDbStatus(`Error: ${data.error}`);
          setDbConfig(data.config);
        }
      } catch (error) {
        console.error("Error:", error);
        setDbStatus("Error connecting to database");
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
              <td>localhost:{FRONTEND_PORT}</td>
            </tr>
            <tr>
              <td>Backend API</td>
              <td>Nginx + PHP-FPM</td>
              <td>localhost:{BACKEND_PORT}</td>
            </tr>
            <tr>
              <td>Database</td>
              <td>MySQL</td>
              <td>localhost:{MYSQL_PORT}</td>
            </tr>
            <tr>
              <td>Database GUI</td>
              <td>phpMyAdmin</td>
              <td>
                <a
                  href={`http://localhost:${PHPMYADMIN_PORT}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  localhost:{PHPMYADMIN_PORT}
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
            <a
              href={`${API_URL}/api`}
              target="_blank"
              rel="noopener noreferrer"
            >
              API Status
            </a>
          </li>
          <li>
            <a
              href={`http://localhost:${PHPMYADMIN_PORT}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              phpMyAdmin
            </a>
          </li>
        </ul>
      </section>

      <section>
        <h2>Database Connection Status</h2>
        <div
          className={`status-indicator ${
            dbStatus === "Connected" ? "status-success" : "status-error"
          }`}
        >
          {dbStatus === "Connected" ? (
            <>
              ✓ Connected to MySQL Server {dbVersion}
              <br />
              Database: {dbConfig?.database}
              <br />
              User: {dbConfig?.user}
            </>
          ) : (
            <>
              ✖ {dbStatus}
              {dbConfig && (
                <div className="config-debug">
                  <pre>{JSON.stringify(dbConfig, null, 2)}</pre>
                </div>
              )}
            </>
          )}
        </div>
      </section>
    </div>
  );
};

export default App;