@echo off
REM ──────────────────────────────────────────────────────────────────────────
REM  PRAHARI AI — Mobile APK Setup Helper
REM  Builds mobile bundle, syncs to Android, and provides ADB install guide
REM ──────────────────────────────────────────────────────────────────────────
title PRAHARI AI — Mobile APK Builder

cd /d "%~dp0frontend"

echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║      PRAHARI AI — Android APK Builder v2.1               ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.

REM ── Step 1: Get local IP ─────────────────────────────────────────────────
echo [1/4] Detecting your PC's local IP address for LAN backend...
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /i "IPv4"') do (
    set LOCAL_IP=%%A
    goto :found_ip
)
:found_ip
set LOCAL_IP=%LOCAL_IP: =%
echo       Your PC IP: %LOCAL_IP%
echo.
echo  ► Edit frontend\.env.mobile and set:
echo      VITE_API_BASE_URL=http://%LOCAL_IP%:8000
echo.
set /p "CONFIRM=Press ENTER after updating .env.mobile to continue..."

REM ── Step 2: Build mobile frontend ────────────────────────────────────────
echo [2/4] Building mobile frontend bundle...
call npm run build:mobile
if %errorlevel% neq 0 (
    echo [ERROR] Vite build failed!
    pause & exit /b 1
)
echo       ✓ Mobile build complete.

REM ── Step 3: Sync to Android ──────────────────────────────────────────────
echo [3/4] Syncing to Android project...
call npx cap sync android
if %errorlevel% neq 0 (
    echo [ERROR] Capacitor sync failed!
    pause & exit /b 1
)
echo       ✓ Android sync complete.

REM ── Step 4: Build debug APK ──────────────────────────────────────────────
echo [4/4] Building debug APK via Gradle...
cd android
call gradlew assembleDebug
if %errorlevel% neq 0 (
    echo [ERROR] Gradle build failed! Ensure Android SDK + JDK 17 are installed.
    echo         You can also open Android Studio: npx cap open android
    cd ..
    pause & exit /b 1
)
cd ..

echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║  ✅  APK BUILT SUCCESSFULLY!                             ║
echo  ╠══════════════════════════════════════════════════════════╣
echo  ║  APK Location:                                           ║
echo  ║  frontend\android\app\build\outputs\apk\debug\           ║
echo  ║  app-debug.apk                                           ║
echo  ╠══════════════════════════════════════════════════════════╣
echo  ║  Install on phone via USB:                               ║
echo  ║  adb install android\app\build\outputs\apk\debug\        ║
echo  ║               app-debug.apk                              ║
echo  ╠══════════════════════════════════════════════════════════╣
echo  ║  Start backend for mobile access:                        ║
echo  ║  venv\Scripts\uvicorn backend.app.main:app               ║
echo  ║       --host 0.0.0.0 --port 8000                         ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.
pause
