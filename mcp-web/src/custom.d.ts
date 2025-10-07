// Fix for TypeScript not recognizing .js imports for ESM modules
declare module '@modelcontextprotocol/sdk/client/index.js' {
  export * from '@modelcontextprotocol/sdk/client/index';
}

declare module '@modelcontextprotocol/sdk/client/sse.js' {
  export * from '@modelcontextprotocol/sdk/client/sse';
}

