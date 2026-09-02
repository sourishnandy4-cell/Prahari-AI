/**
 * PRAHARI AI — Electron Main Process
 * Full-featured desktop shell with:
 * - Auto-launch of bundled FastAPI backend (aegis_backend.exe)
 * - Backend health polling with animated splash screen while waiting
 * - Native application menu (File, View, Help)
 * - System tray icon with show/hide/quit actions
 * - Window state persistence (size, position)
 * - Graceful backend process kill on quit
 */

const { app, BrowserWindow, ipcMain, Menu, Tray, nativeImage, shell, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

let mainWindow = null;
let splashWindow = null;
let tray = null;
let backendProcess = null;
let isQuitting = false;

const BACKEND_PORT = 8000;
const BACKEND_HEALTH_URL = `http://127.0.0.1:${BACKEND_PORT}/api/ping`;
const MAX_WAIT_MS = 6000;    // 6s max wait for backend
const POLL_INTERVAL_MS = 400; // poll every 400ms

// Ensure single instance
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.show();
      mainWindow.focus();
    }
  });
}

// ── Window state persistence ──────────────────────────────────────────────────
const STATE_FILE = path.join(app.getPath('userData'), 'window-state.json');

function loadWindowState() {
  try {
    if (fs.existsSync(STATE_FILE)) {
      return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
    }
  } catch {}
  return { width: 1380, height: 900, x: undefined, y: undefined };
}

function saveWindowState() {
  if (!mainWindow) return;
  try {
    const bounds = mainWindow.getBounds();
    fs.writeFileSync(STATE_FILE, JSON.stringify(bounds));
  } catch {}
}

// ── Backend health check ──────────────────────────────────────────────────────
function checkBackendHealth() {
  return new Promise((resolve) => {
    const req = http.get(BACKEND_HEALTH_URL, { timeout: 1500 }, (res) => {
      resolve(res.statusCode === 200);
    });
    req.on('error', () => resolve(false));
    req.on('timeout', () => { req.destroy(); resolve(false); });
  });
}

// ── Poll backend until ready or timeout ──────────────────────────────────────
function waitForBackend() {
  return new Promise((resolve) => {
    let elapsed = 0;

    const poll = async () => {
      const ok = await checkBackendHealth();
      if (ok) {
        resolve(true);
        return;
      }
      elapsed += POLL_INTERVAL_MS;
      if (elapsed >= MAX_WAIT_MS) {
        resolve(false); // timed out — open anyway
        return;
      }
      setTimeout(poll, POLL_INTERVAL_MS);
    };

    poll();
  });
}

// ── Start bundled FastAPI backend ─────────────────────────────────────────────
async function startBackend() {
  // Check if backend is already active on port 8000
  const alreadyRunning = await checkBackendHealth();
  if (alreadyRunning) {
    console.log('[Aegis Desktop] FastAPI backend is already running on port 8000.');
    return;
  }

  const isDev = !app.isPackaged;
  const projectRoot = path.resolve(__dirname, '../..');

  // Candidate executable paths in priority order
  const candidates = [
    // 1. Packaged folder PyInstaller output in resources
    path.join(process.resourcesPath, 'backend', 'aegis_backend', 'aegis_backend.exe'),
    path.join(process.resourcesPath, 'backend', 'aegis_backend.exe'),
    path.join(process.resourcesPath, 'aegis_backend', 'aegis_backend.exe'),
    // 2. Local dist PyInstaller build
    path.join(projectRoot, 'dist', 'aegis_backend', 'aegis_backend.exe'),
    // 3. Project virtual environment Python
    path.join(projectRoot, 'venv', 'Scripts', 'python.exe'),
  ];

  let backendExecutable = null;
  let args = [];
  let workingDir = projectRoot;

  for (const p of candidates) {
    if (fs.existsSync(p)) {
      backendExecutable = p;
      if (p.endsWith('python.exe')) {
        args = ['-m', 'uvicorn', 'backend.app.main:app', '--host', '127.0.0.1', '--port', String(BACKEND_PORT)];
        process.env.PYTHONPATH = projectRoot;
      } else {
        args = [];
        workingDir = path.dirname(p);
      }
      break;
    }
  }

  if (!backendExecutable) {
    // 4. System Python fallback
    backendExecutable = 'python';
    args = ['-m', 'uvicorn', 'backend.app.main:app', '--host', '127.0.0.1', '--port', String(BACKEND_PORT)];
    process.env.PYTHONPATH = projectRoot;
    console.log('[Aegis Desktop] Using system Python fallback to launch backend.');
  } else {
    console.log(`[Aegis Desktop] Launching backend from: ${backendExecutable}`);
  }

  try {
    backendProcess = spawn(backendExecutable, args, {
      cwd: workingDir,
      detached: false,
      stdio: 'pipe',
      windowsHide: true,
    });

    backendProcess.stdout?.on('data', (d) => {
      const msg = d.toString().trim();
      if (msg) console.log(`[Backend] ${msg}`);
    });

    backendProcess.stderr?.on('data', (d) => {
      const msg = d.toString().trim();
      if (msg) console.warn(`[Backend STDERR] ${msg}`);
    });

    backendProcess.on('error', (err) => {
      console.error('[Aegis Desktop] Backend spawn error:', err);
    });

    backendProcess.on('exit', (code) => {
      console.log(`[Aegis Desktop] Backend exited with code ${code}`);
      if (!isQuitting && mainWindow) {
        mainWindow.webContents.executeJavaScript(
          `window.__AEGIS_BACKEND_DIED = true; console.warn('Backend process exited unexpectedly');`
        ).catch(() => {});
      }
    });

    console.log(`[Aegis Desktop] Backend process started (PID: ${backendProcess.pid})`);
  } catch (err) {
    console.error('[Aegis Desktop] Failed to start backend:', err);
  }
}

// ── Splash window ─────────────────────────────────────────────────────────────
function createSplashWindow() {
  splashWindow = new BrowserWindow({
    width: 480,
    height: 330,
    frame: false,
    transparent: false,
    resizable: false,
    center: true,
    alwaysOnTop: true,
    backgroundColor: '#070a12',
    webPreferences: { nodeIntegration: false, contextIsolation: true },
  });

  splashWindow.loadFile(path.join(__dirname, 'splash.html'));
  splashWindow.once('ready-to-show', () => splashWindow.show());
}

// ── Check Vite dev server ───────────────────────────────────────────────────
function checkViteDevServer() {
  return new Promise((resolve) => {
    const devUrl = process.env.VITE_DEV_SERVER_URL || 'http://localhost:5173';
    const req = http.get(devUrl, { timeout: 1200 }, (res) => {
      resolve(res.statusCode < 500);
    });
    req.on('error', () => resolve(false));
    req.on('timeout', () => { req.destroy(); resolve(false); });
  });
}

// ── Main app window ───────────────────────────────────────────────────────────
async function createMainWindow() {
  const state = loadWindowState();

  mainWindow = new BrowserWindow({
    width: state.width || 1380,
    height: state.height || 900,
    x: state.x,
    y: state.y,
    minWidth: 1024,
    minHeight: 700,
    frame: true,
    autoHideMenuBar: true,
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
    backgroundColor: '#070a12',
    show: false, // show only after backend is ready
    icon: path.join(__dirname, '../public/icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: true,
    },
  });

  mainWindow.setMenuBarVisibility(false);
  mainWindow.removeMenu();

  // Load the app: check if dev server is running, otherwise fallback to local dist/index.html
  const distIndexPath = path.join(__dirname, '../dist/index.html');
  const hasDevServer = !app.isPackaged && (await checkViteDevServer());

  if (hasDevServer) {
    const devUrl = process.env.VITE_DEV_SERVER_URL || 'http://localhost:5173';
    console.log(`[Aegis Desktop] Connecting to Vite dev server: ${devUrl}`);
    mainWindow.loadURL(devUrl);
  } else if (fs.existsSync(distIndexPath)) {
    console.log(`[Aegis Desktop] Loading local dist bundle: ${distIndexPath}`);
    mainWindow.loadFile(distIndexPath);
  } else {
    console.warn(`[Aegis Desktop] Neither dev server nor dist/index.html found. Trying default URL.`);
    mainWindow.loadURL('http://localhost:5173');
  }

  // Graceful fallback if URL fails to load
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription, validatedURL) => {
    console.warn(`[Aegis Desktop] did-fail-load: ${validatedURL} -> ${errorDescription} (${errorCode})`);
    if (validatedURL.startsWith('http') && fs.existsSync(distIndexPath)) {
      console.log(`[Aegis Desktop] Switching to local dist bundle on failure.`);
      mainWindow.loadFile(distIndexPath);
    }
  });

  // Once loaded, show window and close splash
  const revealWindow = () => {
    if (splashWindow && !splashWindow.isDestroyed()) {
      try { splashWindow.close(); } catch {}
      splashWindow = null;
    }
    if (mainWindow && !mainWindow.isDestroyed()) {
      if (!mainWindow.isVisible()) {
        mainWindow.show();
      }
      mainWindow.focus();
    }
  };

  mainWindow.once('ready-to-show', revealWindow);
  // Fail-safe: guaranteed window display within 2s even if ready-to-show lags
  setTimeout(revealWindow, 2000);

  // Persist window state on resize/move
  mainWindow.on('resize', saveWindowState);
  mainWindow.on('move', saveWindowState);

  // Clean exit on window close
  mainWindow.on('close', () => {
    isQuitting = true;
    saveWindowState();
    killBackendProcess();
  });

  mainWindow.on('closed', () => { mainWindow = null; });

  // Open external links in system browser, not Electron
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  return mainWindow;
}

// ── System Tray ───────────────────────────────────────────────────────────────
function createTray() {
  const iconPath = path.join(__dirname, '../public/icon.png');
  const trayIcon = nativeImage.createFromPath(iconPath).resize({ width: 16, height: 16 });
  tray = new Tray(trayIcon);
  tray.setToolTip('PRAHARI AI — Sovereign Safety Intelligence');

  const updateMenu = () => {
    const contextMenu = Menu.buildFromTemplate([
      {
        label: 'PRAHARI AI',
        enabled: false,
        icon: trayIcon,
      },
      { type: 'separator' },
      {
        label: mainWindow?.isVisible() ? 'Hide Window' : 'Show Window',
        click: () => {
          if (mainWindow?.isVisible()) mainWindow.hide();
          else { mainWindow?.show(); mainWindow?.focus(); }
          updateMenu();
        },
      },
      {
        label: 'Open API Docs',
        click: () => shell.openExternal(`http://127.0.0.1:${BACKEND_PORT}/docs`),
      },
      { type: 'separator' },
      {
        label: 'Quit PRAHARI AI',
        click: () => {
          isQuitting = true;
          app.quit();
        },
      },
    ]);
    tray.setContextMenu(contextMenu);
  };

  updateMenu();

  tray.on('double-click', () => {
    if (mainWindow) { mainWindow.show(); mainWindow.focus(); }
  });

  tray.on('click', () => {
    if (mainWindow?.isVisible()) mainWindow.hide();
    else { mainWindow?.show(); mainWindow?.focus(); }
    updateMenu();
  });
}

// ── Native Application Menu ───────────────────────────────────────────────────
function buildAppMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'New Chat',
          accelerator: 'CmdOrCtrl+K',
          click: () => mainWindow?.webContents.executeJavaScript(
            `document.dispatchEvent(new KeyboardEvent('keydown', { key: 'k', ctrlKey: true, bubbles: true }))`
          ),
        },
        { type: 'separator' },
        {
          label: 'Open API Docs in Browser',
          click: () => shell.openExternal(`http://127.0.0.1:${BACKEND_PORT}/docs`),
        },
        { type: 'separator' },
        { role: 'quit', label: 'Quit PRAHARI AI' },
      ],
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' },
        { type: 'separator' },
        {
          label: 'Toggle DevTools',
          accelerator: 'CmdOrCtrl+Shift+I',
          click: () => mainWindow?.webContents.toggleDevTools(),
        },
      ],
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'PRAHARI AI Documentation',
          click: () => shell.openExternal('https://github.com/sourishnandy4-cell/Aegis-AI'),
        },
        {
          label: 'FastAPI Backend Docs',
          click: () => shell.openExternal(`http://127.0.0.1:${BACKEND_PORT}/docs`),
        },
        { type: 'separator' },
        {
          label: 'About PRAHARI AI',
          click: () => dialog.showMessageBox(mainWindow, {
            type: 'info',
            title: 'About PRAHARI AI',
            message: 'PRAHARI AI — Sovereign Industrial Safety Intelligence',
            detail: 'Version 2.7.4\nBuilt for MRPL Refinery\n\n100% Offline / Air-Gapped\nPowered by Sovereign AI + ChromaDB + BM25',
            buttons: ['OK'],
          }),
        },
      ],
    },
  ];

  // Disable native menu bar for clean modern window UI
  Menu.setApplicationMenu(null);
}

// ── IPC handlers ──────────────────────────────────────────────────────────────
ipcMain.handle('get-app-version', () => app.getVersion());
ipcMain.handle('get-backend-url', () => `http://127.0.0.1:${BACKEND_PORT}`);
ipcMain.handle('check-backend-health', () => checkBackendHealth());

// ── App lifecycle ─────────────────────────────────────────────────────────────
app.whenReady().then(async () => {
  Menu.setApplicationMenu(null);
  createSplashWindow();
  await startBackend();

  console.log('[Aegis Desktop] Waiting for backend to be ready...');
  const backendReady = await waitForBackend();

  if (backendReady) {
    console.log('[Aegis Desktop] Backend is ready! Opening main window.');
  } else {
    console.warn('[Aegis Desktop] Backend did not respond in time — opening window anyway.');
  }

  await createMainWindow();
  createTray();

  app.on('activate', async () => {
    if (BrowserWindow.getAllWindows().length === 0) await createMainWindow();
    else { mainWindow?.show(); mainWindow?.focus(); }
  });
});

// ── Process termination helper ───────────────────────────────────────────────
function killBackendProcess() {
  if (backendProcess && backendProcess.pid) {
    const pid = backendProcess.pid;
    console.log(`[Aegis Desktop] Terminating backend process tree (PID: ${pid})...`);
    if (process.platform === 'win32') {
      try {
        const { execSync } = require('child_process');
        execSync(`taskkill /F /T /PID ${pid} 2>nul`);
      } catch (e) {
        try { backendProcess.kill('SIGKILL'); } catch {}
      }
    } else {
      try { backendProcess.kill('SIGKILL'); } catch {}
    }
    backendProcess = null;
  }

  // Ensure no orphaned aegis_backend process lingers on Windows
  if (process.platform === 'win32') {
    try {
      const { execSync } = require('child_process');
      execSync('taskkill /F /IM aegis_backend.exe 2>nul');
    } catch {}
  }
}

app.on('before-quit', () => {
  isQuitting = true;
  saveWindowState();
  killBackendProcess();
});

app.on('window-all-closed', () => {
  // On macOS, standard behavior is to keep app running until Cmd+Q
  if (process.platform !== 'darwin') {
    isQuitting = true;
    killBackendProcess();
    app.quit();
  }
});

app.on('quit', () => {
  killBackendProcess();
});

process.on('exit', () => {
  killBackendProcess();
});

process.on('SIGINT', () => {
  killBackendProcess();
  process.exit(0);
});

process.on('SIGTERM', () => {
  killBackendProcess();
  process.exit(0);
});

