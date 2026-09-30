## 🛡️ PRAHARI AI v3.1.0 — Dual-Engine (Google Gemini Cloud AI + Sovereign Offline LLaMA 3.2)

**Official SIH 26107 Edition with Real-Time Web Intelligence & User-Token Powered Cloud AI**

### 🌟 What's New in v3.1.0:

1. **⚡ Google Gemini Cloud AI Integration**:
   - Support for **Google Gemini 1.5 Flash** (sub-second cloud intelligence, 1M context window) and **Google Gemini 1.5 Pro** (deep multi-standard reasoning).
   - Powered directly by the user's free Google AI Studio token.

2. **🔗 1-Click Free Token Retrieval & Clipboard Paste**:
   - Direct 1-click button to open Google AI Studio (`https://aistudio.google.com/app/apikey`) for free key generation (15 RPM / 1,500 requests/day, no credit card needed).
   - Integrated `2. Paste Key` button reading clipboard automatically with `navigator.clipboard.readText()`.
   - `3. Test Key` button offering instant live validation with Google's API endpoint.

3. **🌐 Dynamic Online Web Augmentation**:
   - Integrated live DuckDuckGo web search retrieving real-time BIS Quality Control Orders (QCOs), Gazette circulars, and consumer advisories.
   - 0% canned responses — 100% dynamic neural AI generation.

4. **🔒 Verified 100% Offline Air-Gapped Mode**:
   - Powered by local Ollama engine with `llama3.2` and `nomic-embed-text` dense vector embeddings in ChromaDB.
   - Automatic silent failover: if internet connection drops or token quota is exhausted, PRAHARI AI seamlessly switches to local offline neural processing without errors or interruption.

5. **🎛️ Interactive Model Switcher & Header Badge**:
   - Header badge displaying the active engine (`[ ⚡ Gemini Flash ▼ ]`, `[ 🌐 LLaMA + Web ▼ ]`, or `[ 🔒 Offline LLaMA ▼ ]`).
   - Settings modal allowing on-the-fly model switching, configuration persistence in `data/ai_config.json`, and live connectivity indicators.

---

## 🛡️ PRAHARI AI v3.0.0 — SIH Topic 26107 Release

**AI Virtual Assistant for Indian Standards (IS Codes), BIS Schemes & Industrial Safety**

This major release transforms PRAHARI AI into a dedicated Virtual Assistant for **Smart India Hackathon (SIH 2024 - Problem Statement 26107)**, under the aegis of the **Bureau of Indian Standards (BIS)** and the **Ministry of Consumer Affairs, Food & Public Distribution**, while fully retaining existing industrial safety capabilities for MRPL refinery operations.

---

### 🌟 Key Features & Regulatory Grounding

#### 1. 🏛️ Comprehensive Standards Document Ingestion
- Pre-seeded with the **Indian Standards BIS Compendium (2026)**, covering 17 critical standards across 6 domains:
  - **Civil Infrastructure**: `IS 1786:2008` (TMT Rebars, Fe 500D), `IS 2062:2011` (Structural Steel), `IS 269:2015` (OPC Cement 33/43/53 Grade).
  - **Electrical Accessories**: `IS 1293:2019` (Plugs & Sockets up to 16A), `IS 694:2010` (PVC Building Wires up to 1100V).
  - **Electronics & IT (CRS)**: `IS 13252:2010` (IT Equipment), `IS 16046:2018` (Lithium Batteries/Power Banks), `IS 15885:2012` (LED Drivers).
  - **Food & Drinking Water**: `IS 10500:2012` (Drinking Water), `IS 14543:2004` (Packaged Water), `IS 13428:2005` (Natural Mineral Water).
  - **Consumer Safety**: `IS 4151:2015` (Motorcycle Helmets), `IS 2347:2017` (Pressure Cookers), `IS 9873:2019` (Safety of Toys), `IS 302:2008` (Electrical Appliances).
  - **Precious Metals & Hallmarking**: `IS 1417:2016` (Gold Fineness 22K/18K/14K & HUID), `IS 2112:2014` (Silver).

#### 2. 📌 Retrieval with Exact Clause Citations
- Every response quotes the **Standard Number** (e.g. `IS 1786:2008`) and the specific **Clause / Table** (e.g. `Clause 4.1 & Table 1`, `Clause 8.1 & Table 2`).
- Answers are accompanied by interactive citation badges (`🏷️ IS Standard` and `📌 Clause Tag`).

#### 3. 🏭 Industry Q&A Portal
- **Standard Finder**: Fast product-to-standard mapping for manufacturers and suppliers.
- **Testing Requirements**: Retrieves mandatory Scheme of Inspection and Testing (SIT) parameters (0.2% Proof Stress, Tensile/Yield ratios, 180° Bend & Rebend tests, Spectrometric chemical analysis).
- **QCO Compliance**: Identifies mandatory Quality Control Orders issued by the Ministry of Steel, MeitY, DPIIT, and Ministry of Heavy Industries.

#### 4. 👥 Consumer Q&A Portal
- **ISI Mark Verification**: Verification steps for the 7-digit CML licence number using the official **BIS Care App**.
- **Gold Hallmark Verification**: Verification guide for the 3 mandatory hallmarks (BIS Logo, Fineness `22K916`, and the 6-digit alphanumeric HUID laser mark).
- **Grievance Redressal**: Step-by-step guidance for filing formal complaints regarding substandard products or counterfeit marks via the portal, BIS Care App, and National Toll-Free Helpline **1915**.

#### 5. 🌐 Native Bilingual Support (English + हिन्दी)
- Automatic detection of Hindi (Devanagari script) queries and localized responses with Hindi clause references.
- One-click language toggle (`EN` / `हिन्दी`) directly in the chat interface.

#### 6. 📋 Step-by-Step Certification Guidance
- Structured 6-step roadmap for **Scheme-I (ISI Mark)** on MANAK Online and **Scheme-II (CRS)** for electronic goods.
- Complete checklist of 8 mandatory documents (Factory registration, machinery list, lab equipment calibration certificates, process flow chart, etc.).

#### 7. ❓ Interactive Follow-Up Clarifications
- Automatically identifies ambiguous or broad product queries (e.g., *"water"*, *"steel"*, *"cable"*) and presents one-tap clarification pills.

#### 8. ⚖️ Standards Comparison Engine
- Side-by-side technical comparison tables for differing standards (e.g., `IS 10500 vs IS 14543`, `IS 1786 vs IS 2062`).

#### 9. 🛡️ Safe Refusal Guardrails
- If a queried product or standard does not exist in regulatory documentation, the agent strictly refuses to speculate, directing users to the BIS Helpline (`1800-11-1255` / `1915`) and `www.bis.gov.in`.

#### 10. 🎙️ Voice Recognition for Accessibility
- Native speech-to-text input supporting both Indian English (`en-IN`) and Indian Hindi (`hi-IN`).

#### 11. 🔄 Zero-Retraining Dynamic Ingestion
- Upload new standard PDFs via the API (`/api/bis/standards/upload`) or UI modal without needing to retrain or restart the engine.

#### 12. 🔒 100% Offline & Sovereign
- Fully functional in air-gapped environments without any cloud API dependencies.
- Existing MRPL refinery safety SOPs (CDU emergency shutdowns, H2S toxic gas limits, PSV pop-test tolerances) remain 100% preserved and accessible.

---

### 📦 Release Assets & Binaries

| Asset Name | Format | Size | SHA-256 Checksum |
| :--- | :--- | :--- | :--- |
| **`PRAHARI-AI-Setup-v3.0.0.exe`** | Windows Installer (NSIS) | ~248.9 MB | `F7AC74D3A5472DC5A1FC0E1DD7552CF50170A278CE5B1F83F151157A22477A88` |
| **`PRAHARI-AI-Portable-v3.0.0.exe`** | Portable Standalone Exe | ~248.5 MB | `06D988AC8676B706487579A0599721780C6B2E1434D27A8FA724F5D630FE95A5` |

*Both binaries bundle the complete offline Python runtime, PyInstaller standalone backend, SQLite vectorstore, pre-seeded BIS Compendium (17 Indian Standards), and Chromium desktop shell.*

---
*Created for Smart India Hackathon (SIH 2024 - PS 26107) • Bureau of Indian Standards & MRPL Aegis Team*

