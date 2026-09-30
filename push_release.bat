@echo off
set "PATH=C:\Users\AZIZ\AppData\Local\Programs\Git\cmd;C:\Users\AZIZ\AppData\Local\Programs\gh;%PATH%"
title PRAHARI AI - Push ^& Publish v3.0.0
cd /d "%~dp0"

echo.
echo ================================================================
echo   PRAHARI AI - Push Changes ^& Publish Release v3.0.0
echo   SIH Topic 26107 (Indian Standards ^& BIS Schemes Edition)
echo ================================================================
echo.

echo [1/3] Checking GitHub authentication status...
gh auth status >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Choose your authentication method:
    echo   [1] Browser Login with One-Time Code (Recommended)
    echo   [2] Paste a GitHub Personal Access Token (PAT)
    echo.
    set /p "AUTH_CHOICE=Select (1 or 2, default is 1): "
    if "%AUTH_CHOICE%"=="2" (
        echo.
        echo Please paste your GitHub Personal Access Token (requires 'repo' scope):
        set /p "GITHUB_PAT=Token: "
        echo %GITHUB_PAT%| gh auth login --with-token
    ) else (
        echo.
        echo [*] Starting GitHub web browser login...
        gh auth login --hostname github.com -p https --web
    )
)

echo.
echo [2/3] Configuring git credential helper and pushing commits ^& tag...
call gh auth setup-git
git push origin main
git push origin v3.0.0

echo.
echo [3/3] Publishing official GitHub Release v3.0.0 with installer assets...
gh release create v3.0.0 "release\PRAHARI-AI-Setup-v3.0.0.exe" "release\PRAHARI-AI-Portable-v3.0.0.exe" --title "v3.0.0: SIH 26107 - AI Virtual Assistant for Indian Standards & BIS Schemes" --notes-file RELEASE_NOTES.md

echo.
echo ================================================================
echo   SUCCESS! Release v3.0.0 has been successfully published:
echo   https://github.com/sourishnandy4-cell/Prahari-AI/releases/tag/v3.0.0
echo ================================================================
echo.
pause
