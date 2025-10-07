import React, { useEffect, useState } from 'react';
import './App.css';
import { useMCP } from './mcp';

function App() {
  const mcpClient = useMCP();
  const [connected, setConnected] = useState(false);
  const [tools, setTools] = useState<any[]>([]);
  const [resources, setResources] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const connectAndFetch = async () => {
      try {
        await mcpClient.connect();
        setConnected(true);
        
        const toolsList = await mcpClient.listTools();
        setTools(toolsList.tools || []);
        
        const resourcesList = await mcpClient.listResources();
        setResources(resourcesList.resources || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to connect');
      }
    };

    connectAndFetch();

    return () => {
      mcpClient.disconnect();
    };
  }, [mcpClient]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>MCP Web Client</h1>
        
        {error && (
          <div style={{ color: 'red', padding: '10px', background: '#fee' }}>
            Error: {error}
          </div>
        )}
        
        {connected ? (
          <div style={{ color: 'green' }}>✓ Connected to MCP Server</div>
        ) : (
          <div style={{ color: 'orange' }}>Connecting...</div>
        )}
        
        <div style={{ marginTop: '30px', textAlign: 'left', maxWidth: '800px' }}>
          <h2>Available Tools ({tools.length})</h2>
          <ul>
            {tools.map((tool, idx) => (
              <li key={idx}>
                <strong>{tool.name}</strong>: {tool.description}
              </li>
            ))}
          </ul>
          
          <h2>Available Resources ({resources.length})</h2>
          <ul>
            {resources.map((resource, idx) => (
              <li key={idx}>
                <strong>{resource.name}</strong>: {resource.uri}
              </li>
            ))}
          </ul>
        </div>
      </header>
    </div>
  );
}

export default App;
