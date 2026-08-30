const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  appVersion: '1.0.0',
  mode: 'Air-Gapped Sovereign Desktop Application'
});
