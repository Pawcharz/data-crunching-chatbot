import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { SSEClientTransport } from '@modelcontextprotocol/sdk/client/sse.js';

export class MCPClient {
  private client: Client;
  private connected = false;
  private serverUrl: string;

  constructor(serverUrl: string) {
    this.serverUrl = serverUrl;
    this.client = new Client(
      { name: 'AdminAssistant', version: '1.0.0' },
      { capabilities: {} }
    );
  }

  async connect() {
    const transport = new SSEClientTransport(new URL(this.serverUrl));
    await this.client.connect(transport);
    this.connected = true;
  }

  async disconnect() {
    await this.client.close();
    this.connected = false;
  }

  isConnected() {
    return this.connected;
  }

  // Call any tool
  async callTool(name: string, args?: any) {
    return await this.client.callTool({ name, arguments: args });
  }

  // List available tools
  async listTools() {
    return await this.client.listTools();
  }

  // List available resources
  async listResources() {
    return await this.client.listResources();
  }

  // Read a resource
  async readResource(uri: string) {
    return await this.client.readResource({ uri });
  }
} 