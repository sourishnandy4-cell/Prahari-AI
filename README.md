# 🛡️ PRAHARI AI (v3.1.0 — Dual-Engine Edition)

[![Release](https://img.shields.io/github/v/release/sourishnandy4-cell/Prahari-AI?color=blue&label=Latest%20Release)](https://github.com/sourishnandy4-cell/Prahari-AI/releases/latest)
[![Platform: Web | Windows | Android](https://img.shields.io/badge/Platform-Web%20%7C%20Windows%20%7C%20Android-brightgreen)](https://github.com/sourishnandy4-cell/Prahari-AI/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Sovereign AI Virtual Assistant for Indian Standards (IS Codes), BIS Schemes & Industrial Safety**  
> *Built for Smart India Hackathon (SIH Topic 26107) & High-Reliability Operations at Mangalore Refinery and Petrochemicals Limited (MRPL).*

---

## 🌟 What's New in v3.1.0 (Dual-Engine: Online Cloud AI + Offline Neural)

1. **⚡ Google Gemini Cloud AI**: Seamless integration with **Gemini 1.5 Flash** and **Gemini 1.5 Pro**, powered directly by user-provided free Google AI Studio tokens.
2. **🔗 1-Click Free Token Fetcher & Instant Paste**: Direct link to open Google AI Studio (`https://aistudio.google.com/app/apikey`), 1-click clipboard paste button, and instant live token testing against Google Cloud.
3. **🌐 Real-Time Web Augmentation**: Real-time DuckDuckGo web search retrieving current BIS Quality Control Orders (QCOs), Gazette circulars, and consumer advisories without API keys.
4. **🔒 100% Offline Air-Gapped Mode**: Local Ollama neural engine (`llama3.2:1b` + `nomic-embed-text`) with ChromaDB dense vectorstore. Works completely offline with automatic silent failover when disconnected.
5. **🎛️ Interactive Model Switcher**: Header badge and model switcher modal for toggling between Gemini 1.5 Flash, Gemini 1.5 Pro, LLaMA 3.2 + Web, and Offline LLaMA 3.2.

---

## 🌟 Core Features (SIH Topic 26107)

1. **🏛️ Standards Document Ingestion**: Ingests Indian Standards (IS Codes) and BIS Scheme regulatory documents into a searchable hybrid knowledge base (ChromaDB + BM25 Okapi).
2. **📌 Retrieval with Verified Citations**: Every single answer names the exact Standard number (e.g., `IS 1786:2008`, `IS 10500:2012`, `IS 1417:2016`, `IS 269:2015`) and the specific Clause it originated from.
3. **🏭 Industry Q&A Portal**: Answers *"Which IS standard applies to my product?"*, *"What testing is needed under SIT?"*, and mandatory Quality Control Order (QCO) requirements.
4. **👥 Consumer Q&A Portal**: Comprehensive verification guides for authentic ISI Marks (7-digit CML numbers), Gold Hallmarks (6-digit HUID tracking via BIS Care App), and formal complaint filing.
5. **🌐 Bilingual Support (English + हिन्दी)**: Native support for English and Hindi queries and answers with automatic Devanagari script detection and one-click language toggle (`EN` / `हिन्दी`).
6. **📋 Step-by-Step Certification Guidance**: Interactive 6-step walkthrough for Scheme-I (ISI Mark) and Scheme-II (CRS) with a mandatory 8-document checklist.
7. **❓ Intelligent Follow-Up Clarifications**: Disambiguates vague queries (e.g., *"water"*, *"steel"*, *"cable"*) into targeted product sub-types.
8. **⚖️ Standards Comparison Engine**: Side-by-side technical comparison tables (e.g., `IS 10500 vs IS 14543`, `IS 1786 vs IS 2062`).
9. **🛡️ Safe Refusal Guardrails**: Automatically identifies unindexed or out-of-scope queries and refuses speculation, directing users to the official BIS National Helpline (`1800-11-1255` / `1915`) and `www.bis.gov.in`.
10. **🎙️ Voice Recognition**: Dual-language voice input via Web Speech API (`en-IN` & `hi-IN`).
11. **🔄 Zero-Retraining Ingestion**: Dynamic upload mechanism allowing new PDF standards to be ingested instantly into the live RAG vector store without model retraining.

---

## ✨ Key Capabilities

- **🛡️ 100% Offline & Air-Gapped**: Sovereign local execution with zero cloud dependencies.
- **📚 Dual-Corpus Knowledge Base**: Pre-seeded with both the **Indian Standards BIS Compendium (2026)** and the **MRPL Industrial Safety SOP (2026)**.
- **⚡ Universal Technical AI**: Solves engineering unit conversions (`bar <-> psi`, `°C <-> °F`), math problems, and script automation.
- **🌐 Real-Time Streaming (SSE)**: Token-by-token generation with interactive citation badges and latency telemetry.
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
