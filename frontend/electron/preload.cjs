/**
 * PRAHARI AI — Electron Preload Script
 * Safely exposes IPC bridges to the renderer process via contextBridge.
 * Node.js APIs are NOT directly available in the renderer — all access
 * goes through this explicit allowlist.
 */

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('prahari', {
  /** Get the Electron app version */
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),

  /** Get the backend API base URL (http://127.0.0.1:8000) */
  getBackendUrl: () => ipcRenderer.invoke('get-backend-url'),

  /** Check if the backend is currently healthy */
  checkBackendHealth: () => ipcRenderer.invoke('check-backend-health'),

  /** Platform identifier: 'win32' | 'darwin' | 'linux' */
  platform: process.platform,

  /** True when running inside Electron */
  isElectron: true,
});
