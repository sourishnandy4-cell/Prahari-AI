@echo off
title PRAHARI AI - Offline AI Models Auto-Setup
cd /d "%~dp0"

echo.
echo  ================================================================
echo    PRAHARI AI — Automated Offline Neural AI Engine Setup
echo    Installs Ollama ^& Downloads LLaMA 3.2 for 100%% Dynamic Generation
echo  ================================================================
echo.

REM 1. Check if Ollama is installed
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Step 1/3: Ollama is not detected. Installing Ollama for Windows...
    winget install Ollama.Ollama --accept-source-agreements --accept-package-agreements --silent
    if %errorlevel% neq 0 (
        echo [!] Winget install failed. Attempting direct browser download...
        start https://ollama.com/download/OllamaSetup.exe
        echo Please complete the Ollama installer window and re-run this script.
        pause
        exit /b 1
    )
    REM Refresh environment PATH
    set "PATH=%LOCALAPPDATA%\Programs\Ollama;%PATH%"
) else (
    echo [✓] Step 1/3: Ollama is already installed.
)

REM 2. Ensure Ollama service is running
echo.
echo [*] Step 2/3: Starting local Ollama service...
tasklist /fi "imagename eq ollama.exe" | findstr /i "ollama.exe" >nul 2>&1
if %errorlevel% neq 0 (
    start /B "" "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" serve >nul 2>&1
    timeout /t 3 /nobreak >nul
)
echo [✓] Ollama service active at http://localhost:11434

REM 3. Pull LLaMA 3.2 and Embedding Models
echo.
echo [*] Step 3/3: Downloading offline neural AI models (this may take a few minutes)...
echo     Downloading 'llama3.2' (Meta's state-of-the-art offline generative model)...
ollama pull llama3.2

echo.
echo     Downloading 'nomic-embed-text' (dense semantic vector model)...
ollama pull nomic-embed-text

echo.
echo  ================================================================
echo    🎉 SUCCESS! Offline Neural AI Engine is fully installed.
echo    PRAHARI AI will now generate 100%% dynamic, non-pre-fed answers.
echo  ================================================================
echo.
pause
