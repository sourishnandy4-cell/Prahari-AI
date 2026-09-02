# 🛡️ PRAHARI AI (Aegis Sovereign Intelligence)

[![Release](https://img.shields.io/github/v/release/sourishnandy4-cell/Aegis-AI?color=blue&label=Latest%20Release)](https://github.com/sourishnandy4-cell/Aegis-AI/releases/latest)
[![Android](https://img.shields.io/badge/Platform-Android%20%7C%20Windows-brightgreen)](https://github.com/sourishnandy4-cell/Aegis-AI/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Sovereign On-Premise Industrial Safety & Agentic RAG Web Application**
> *Engineered for High-Reliability Operations at Mangalore Refinery and Petrochemicals Limited (MRPL).*

---

## 📦 Downloads & Releases (v2.7.3)

| Platform | Package | Size | Direct Download |
| :--- | :--- | :--- | :--- |
| 📱 **Android Mobile** | `PRAHARI-AI-v2.7.3.apk` | 70.1 MB | [📥 Download APK](https://github.com/sourishnandy4-cell/Aegis-AI/releases/download/v2.7.3/PRAHARI-AI-v2.7.3.apk) |
| 🖥️ **Windows (Installer)** | `PRAHARI-AI-Setup-v2.7.3.exe` | 261.6 MB | [📥 Download Setup](https://github.com/sourishnandy4-cell/Aegis-AI/releases/download/v2.7.3/PRAHARI-AI-Setup-v2.7.3.exe) |
| ⚡ **Windows (Portable)** | `PRAHARI-AI-Portable-v2.7.3.exe` | 261.2 MB | [📥 Download Portable](https://github.com/sourishnandy4-cell/Aegis-AI/releases/download/v2.7.3/PRAHARI-AI-Portable-v2.7.3.exe) |

*Full release notes and checksums are available on the [GitHub Releases Page](https://github.com/sourishnandy4-cell/Aegis-AI/releases/tag/v2.7.3).*

---

## 🌟 Overview

**PRAHARI AI** is a sovereign, 100% offline industrial safety and general intelligence web application. It combines **Dense Semantic Retrieval** (ChromaDB) with **Sparse Lexical Search** (BM25 Okapi) using **Reciprocal Rank Fusion (RRF)**, powered by a dual-engine architecture:
1. **Local LLM Engine** (Ollama: `llama3.2`, `mistral`, `qwen2.5`, `phi3`)
2. **Sovereign Offline Intelligence Brain** (100% air-gapped fallback for general queries, calculations, code assistance, and SOP grounding)

---

## ✨ Key Features

- **🛡️ 100% Offline & Air-Gapped**: Zero external cloud API calls required. Complete data sovereignty and security.
- **⚡ Universal Technical AI**: Answers general knowledge, calculations (`bar <-> psi`, `°C <-> °F`, percentages), and programming questions (Python, JavaScript, SQL, Bash, Regex).
- **📚 Predefined SOP Knowledge**: Pre-seeded with a comprehensive 10-section MRPL 2026 Industrial Safety Manual:
  - Crude Distillation Unit (CDU-1/2/3) Emergency Shutdown Procedures
  - Hydrogen Sulfide ($H_2S$) Toxic Gas Exposure Limits (TWA, STEL, IDLH, SCBA, Muster C-4)
  - Pressure Safety Valve (PSV/PRV) Recertification & Pop Test Tolerances (API 576, OISD-132)
  - Zone-1 & Zone-2 Hot Work & Confined Space Permits
  - Hydrocracker Unit (HCU) & Hydrogen Unit Emergency Depressurization (EDP-01)
  - Fire Protection, AFFF 3% Deluge Systems & Fire Ring Mains
  - Confined Space Entry & Spectacle Blind Isolation (OISD-STD-105)
  - Electrical Lockout / Tagout (LOTO) Standards
  - Chemical Hazard Management & Neutralization (Caustic Soda 50%, Sulfuric Acid 98%)
  - Shift Handover Compliance (OSHA 1910.119) & Fall Protection
- **🌐 Real-Time Streaming (SSE)**: Character-by-character / word-by-word token generation with source citations and latency telemetry.
- **🎨 Modern Web UI**: Built with React 18, Vite, Tailwind CSS, Framer Motion, and a 3D WebGL Neural Canvas.
- **🎙️ Voice Recognition**: Built-in speech-to-text transcription via Web Speech API.
- **📂 Document Manager**: Upload, inspect, delete, and re-index operational PDF manuals on the fly.

---

## 🛠️ Architecture & Tech Stack

```
   ┌───────────────────────────────────────────────────────────┐
   │                     PRAHARI WEB UI                        │
   │      React 18 • Vite • Tailwind CSS • Three.js 3D         │
   └─────────────────────────────┬─────────────────────────────┘
                                 │ HTTP / SSE Stream
                                 ▼
   ┌───────────────────────────────────────────────────────────┐
   │                 FASTAPI SOVEREIGN BACKEND                 │
   │  ┌───────────────────────┐     ┌───────────────────────┐  │
   │  │  Local Ollama Engine  │     │   Sovereign Offline   │  │
   │  │ (llama3.2, nomic-emb) │ ◄-► │   Intelligence Brain  │  │
   │  └───────────────────────┘     └───────────────────────┘  │
   │                             │                             │
   │            ┌────────────────┴────────────────┐            │
   │            ▼                                 ▼            │
   │  ┌────────────────────┐            ┌───────────────────┐  │
   │  │ ChromaDB (Vectors) │            │ BM25 Okapi Search │  │
   │  └────────────────────┘            └───────────────────┘  │
   │            └────────────────┬────────────────┘            │
   │                             ▼                             │
   │             Reciprocal Rank Fusion (RRF)                  │
   └─────────────────────────────┬─────────────────────────────┘
                                 │
                                 ▼
                    [ SQLite Persistence Layer ]
                   (Chat Sessions & Doc Catalog)
```

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons, Framer Motion, Three.js
- **Backend**: FastAPI, Uvicorn, LangChain, ChromaDB, Rank-BM25, ReportLab, Pydantic v2
- **Database**: SQLite (WAL mode) + ChromaDB On-Disk Vector Store

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- *(Optional)* [Ollama](https://ollama.com/) with `llama3.2` and `nomic-embed-text`

### 2. Backend Setup
```bash
# Clone the repository
git clone https://github.com/sourishnandy4-cell/Aegis-AI.git
cd Aegis-AI

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Frontend Setup
```bash
cd frontend

# Install npm dependencies
npm install

# Start Vite development server
npm run dev
```

Visit **`http://localhost:5173`** in your browser.
API Swagger Docs are available at **`http://localhost:8000/docs`**.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | System root status & mode |
| `GET` | `/api/health` | Healthcheck & system telemetry |
| `POST` | `/api/chat` | Standard JSON RAG query |
| `GET` | `/api/stream` | Server-Sent Events (SSE) token stream |
| `GET` | `/api/sessions` | List persistent chat sessions |
| `POST` | `/api/sessions` | Create a new chat session |
| `GET` | `/api/documents` | List indexed PDF manuals |
| `POST` | `/api/documents/upload` | Upload & index a new SOP manual |
| `DELETE`| `/api/documents/{id}` | Delete a document from catalog & vectors |

---

## 🔒 Security & Compliance

- **Air-Gapped Ready**: Operates without external internet access.
- **Process Safety Standards**: Adheres to **OISD-GDN-166**, **OISD-132**, **API 576/520**, and **OSHA 1910.119**.
- **Optional API Key Guard**: Enable `API_KEY` in `.env` to protect endpoints.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
