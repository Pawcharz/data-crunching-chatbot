import React, { createContext, useContext, useState } from 'react';
import { MCPClient } from './client';

const MCPContext = createContext<MCPClient | null>(null);

interface MCPProviderProps {
  serverUrl: string;
  children: React.ReactNode;
}

export const MCPProvider: React.FC<MCPProviderProps> = ({ serverUrl, children }) => {
  const [client] = useState(() => new MCPClient(serverUrl));

  return (
    <MCPContext.Provider value={client}>
      {children}
    </MCPContext.Provider>
  );
};

export const useMCP = () => {
  const client = useContext(MCPContext);
  if (!client) throw new Error('useMCP must be used within MCPProvider');
  return client;
}; 