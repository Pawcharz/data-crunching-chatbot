// --------------------
// EventTarget and Event polyfill
// Polyfills for MCP SDK in React Native
import { EventTarget, defineEventAttribute } from 'event-target-shim';
import RNEventSource from 'eventsource';

// --- Polyfill Event class ---
if (typeof global.Event === 'undefined') {
  global.Event = class {
    type: string;
    constructor(type: string, _options?: any) {
      this.type = type;
    }
  };
}

// --- Polyfill EventTarget ---
if (typeof global.EventTarget === 'undefined') {
  global.EventTarget = EventTarget;
  defineEventAttribute(global.EventTarget.prototype, 'onopen');
  defineEventAttribute(global.EventTarget.prototype, 'onmessage');
  defineEventAttribute(global.EventTarget.prototype, 'onerror');
  defineEventAttribute(global.EventTarget.prototype, 'onclose');
}

// --- Polyfill EventSource ---
if (typeof global.EventSource === 'undefined') {
  global.EventSource = RNEventSource;
}
// --------------------

import { AppRegistry } from 'react-native';
import App from './App';
import { name as appName } from './app.json';

AppRegistry.registerComponent(appName, () => App);
