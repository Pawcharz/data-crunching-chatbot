import React, { useState } from 'react';
import { View, Button, Text, StyleSheet } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { MCPProvider, useMCP } from './src/mcp';

function AppContent() {
  const client = useMCP();
  const [status, setStatus] = useState('Disconnected');

  const handleConnect = async () => {
    try {
      setStatus('Connecting...');
      await client.connect();
      setStatus('Connected');
    } catch (error: any) {
      setStatus(`Error: ${error.message || error}`);
      console.error('Connection error:', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.status}>{status}</Text>
      <Button title="Connect to MCP" onPress={handleConnect} />
    </View>
  );
}

function App() {
  return (
    <SafeAreaProvider>
      <MCPProvider serverUrl="http://localhost:3000">
        <AppContent />
      </MCPProvider>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  status: {
    fontSize: 18,
    marginBottom: 20,
  },
});

export default App;
