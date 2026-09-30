@echo off
set "PATH=C:\Users\AZIZ\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64;C:\Users\AZIZ\AppData\Local\Programs\Git\cmd;%PATH%"
REM ──────────────────────────────────────────────────────────────────────────
REM  PRAHARI AI — Desktop App Launcher (Development Mode)
REM  Starts backend + Electron desktop shell together
REM ──────────────────────────────────────────────────────────────────────────
title PRAHARI AI Desktop

cd /d "%~dp0"

echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║  PRAHARI AI — Indian Standards (BIS) & Industrial Safety  ║
echo  ║       Desktop Application Launcher v3.0.0 (SIH 26107)    ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.

REM ── Check and build frontend if needed ────────────────────────────────────
if not exist "frontend\dist\index.html" (
    echo [Build] Building optimized frontend bundle for desktop...
    cd frontend
    call npm run build
    cd ..
)

REM ── Locate Python executable ───────────────────────────────────────────────
set PYTHON_EXE=python
if exist "venv\Scripts\python.exe" (
    set PYTHON_EXE=venv\Scripts\python.exe
)

REM ── Start FastAPI backend (if not already running) ─────────────────────────
echo [1/2] Starting FastAPI Sovereign Backend on port 8000...
start /B "" %PYTHON_EXE% -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

REM ── Wait 2 seconds for backend to initialize ──────────────────────────────
echo [2/2] Initializing backend...
timeout /t 2 /nobreak >nul

REM ── Launch Electron Desktop App ───────────────────────────────────────────
echo [3/2] Launching PRAHARI AI Desktop window...
cd frontend
call npx electron .

REM ── Cleanup: kill backend on port 8000 when Electron closes ─────────────────
echo.
echo [Done] PRAHARI AI closed. Shutting down backend on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do taskkill /f /pid %%a 2>nul
echo [Done] All application processes stopped.

