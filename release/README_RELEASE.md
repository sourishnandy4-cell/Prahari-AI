# 🛡️ PRAHARI AI (v3.0.0 Release Distribution)

**Sovereign Virtual Assistant for Indian Standards (IS Codes), BIS Schemes & Industrial Safety**  
*Built for Smart India Hackathon (SIH Topic 26107) & High-Reliability Operations at MRPL.*

---

## 📦 Release Artifacts (v3.0.0)

### 🖥️ Windows Desktop
1. **`PRAHARI-AI-Setup-v3.0.0.exe`** (248.9 MB)
   - **SHA-256**: `F7AC74D3A5472DC5A1FC0E1DD7552CF50170A278CE5B1F83F151157A22477A88`
   - Full Windows NSIS Installer bundling the complete standalone PyInstaller Python backend, SQLite vectorstore, offline ChromaDB, and Chromium desktop shell.
   - Dual-mode portal: **🏭 Industry** (Standard finder, SIT parameters, QCOs) & **👥 Consumer** (ISI CML, Gold Hallmark HUID, Complaints).
   - Native Bilingual UI: One-click English / हिन्दी switch with automatic Devanagari script detection.
   - Integrated offline hybrid retrieval engine with exact clause citation.
   - Voice input recognition via Web Speech API (`en-IN` / `hi-IN`).
   - Creates Desktop & Start Menu shortcuts with silent background startup.

2. **`PRAHARI-AI-Portable-v3.0.0.exe`** (248.5 MB)
   - **SHA-256**: `06D988AC8676B706487579A0599721780C6B2E1434D27A8FA724F5D630FE95A5`
   - Zero-installation portable edition bundling the complete standalone backend.
   - Simply double-click to launch immediately on any Windows 10/11 64-bit PC without installation.

---

### 📱 Android Mobile APK
1. **`PRAHARI-AI-v2.7.0.apk`**
   - Android Application Package (built via Capacitor 7).
   - Compatible with Android 8.0+ (API 26 to API 34).
   - Supports 100% offline LAN operation connected to your PC.
   - Slide-over drawer navigation, swipe gestures, voice input (`RECORD_AUDIO`), 3D Neural Human Brain, and camera/photo SOP inspection.

#### 📲 How to Install APK on Phone:
1. **Method A (Direct Transfer)**:
   - Copy `PRAHARI-AI-v2.7.0.apk` to your phone via USB cable, Google Drive, or local share.
   - Tap the `.apk` file on your phone and allow *"Install from Unknown Sources"* if prompted.
2. **Method B (ADB via USB)**:
   ```bash
   adb install PRAHARI-AI-v2.7.0.apk
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
