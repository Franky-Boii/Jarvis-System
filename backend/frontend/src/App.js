import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [logs, setLogs] = useState([]);
  const [agents, setAgents] = useState([
    { name: 'JARVIS', status: 'Standby', role: 'Prime Orchestrator' },
    { name: 'FRIDAY', status: 'Offline', role: 'Daily Intelligence' },
    { name: 'ZEUS', status: 'Offline', role: 'Lead Generation Pipeline' },
    { name: 'STARK', status: 'Offline', role: 'Project Tracker' }
  ]);

  useEffect(() => {
    // Connect to the Python FastAPI backend
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      setLogs(prev => [...prev, "[SYSTEM]: WebSocket Protocol Initialized. Awaiting commands..."]);
      // Bring the prime orchestrator online when the connection is live
      setAgents(prev => prev.map(a => a.name === 'JARVIS' ? { ...a, status: 'Online' } : a));
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLogs(prev => [...prev, `[${data.agent}]: ${data.message}`]);
      
      // Dynamically update agent network status if the backend targets them
      setAgents(prev => prev.map(a => 
        a.name === data.agent ? { ...a, status: data.status } : a
      ));
    };

    return () => ws.close();
  }, []);

  return (
    <div className="dashboard">
      <div className="header">
        <h1>J.A.R.V.I.S PROTOCOL</h1>
        <p>System Diagnostics & Agent Routing</p>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Agent Designation</th>
              <th>Operational Role</th>
              <th>Network Status</th>
            </tr>
          </thead>
          <tbody>
            {agents.map((agent, index) => (
              <tr key={index}>
                <td className="agent-name">{agent.name}</td>
                <td>{agent.role}</td>
                <td className={`status-${agent.status}`}>{agent.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="logs-container">
        <h3>Live Terminal Output</h3>
        <div className="logs">
          {logs.map((log, index) => (
             <div key={index} className="log-entry">{log}</div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;