# 🛡️ PRAHARI AI (v2.3.0 Release Distribution)

Sovereign On-Premise Industrial Safety & Agentic RAG Web/Mobile/Desktop Suite
Engineered for High-Reliability Operations at Mangalore Refinery and Petrochemicals Limited (MRPL).

---

## 📦 Release Artifacts

### 🖥️ Windows Desktop
1. **`PRAHARI-AI-Setup-v2.3.0.exe`**
   - Full Windows NSIS Installer with bundled standalone backend executable.
   - Creates Desktop & Start Menu shortcuts.
   - Auto-starts the background FastAPI engine silently on boot.
   - Includes System Tray integration (`Hide`, `Show`, `API Docs`, `Quit`).
   - Features 60–120 FPS 3D Neural Human Brain Hero + ErrorBoundary resilience.

2. **`PRAHARI-AI-Portable-v2.3.0.exe`**
   - Zero-install portable edition.
   - Simply double-click to run on any Windows 10/11 64-bit machine.

---

### 📱 Android Mobile APK
1. **`PRAHARI-AI-v2.3.0.apk`**
   - Android Application Package (built via Capacitor 7).
   - Compatible with Android 8.0+ (API 26 to API 34).
   - Supports 100% offline LAN operation connected to your PC.
   - Slide-over drawer navigation, swipe gestures, voice input (`RECORD_AUDIO`), 3D Neural Human Brain, and camera/photo SOP inspection.

#### 📲 How to Install APK on Phone:
1. **Method A (Direct Transfer)**:
   - Copy `PRAHARI-AI-v2.3.0.apk` to your phone via USB cable, Google Drive, or local share.
   - Tap the `.apk` file on your phone and allow *"Install from Unknown Sources"* if prompted.
2. **Method B (ADB via USB)**:
   ```bash
   adb install PRAHARI-AI-v2.3.0.apk
   ```

#### 🌐 Connecting Mobile App to your Local PC Backend:
1. Ensure both your Phone and PC are connected to the **same Wi-Fi network**.
2. On PC, start the backend bound to all network interfaces:
   ```bat
   .\venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
   ```
3. Your mobile app will automatically communicate with the local PC backend over LAN HTTP with zero cloud dependencies.

---

## ⚡ Quick Start Shortcuts
- **Launch Desktop App**: Double-click `run_desktop.bat` in the project root.
- **Rebuild APK**: Run `build_apk.bat` in the project root.
- **API Documentation**: Open `http://127.0.0.1:8000/docs` in your browser.
