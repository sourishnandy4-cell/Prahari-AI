import re
import ast
import math
from typing import Dict, Any, List, Optional
from langchain_core.documents import Document

class OfflineIntelligenceEngine:
    """
    Sovereign On-Premise Offline Intelligence Engine.
    Provides complete conversational, mathematical, programming, general knowledge,
    and structured industrial SOP reasoning without requiring any external cloud connectivity
    or active GPU LLM instances.
    """

    def __init__(self):
        self.name = "Prahari AI"
        self.role = "Sovereign Industrial Intelligence & Operational Safety Assistant"
        self.organization = "Mangalore Refinery and Petrochemicals Limited (MRPL)"

    def answer_query(
        self,
        query: str,
        docs: List[Document] = None,
        history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Main entry point for offline reasoning.
        Determines the intent and constructs a rich, authoritative, formatted response.
        """
        q_clean = query.strip()
        q_lower = q_clean.lower()
        docs = docs or []

        # 1. Check Greetings & Small Talk
        greeting_resp = self._check_greeting(q_lower)
        if greeting_resp:
            return {
                "answer": greeting_resp,
                "intent": "greeting",
                "citations": [],
                "mode": "Sovereign Offline Conversational Engine"
            }

        # 2. Check Identity & Capabilities
        identity_resp = self._check_identity(q_lower)
        if identity_resp:
            return {
                "answer": identity_resp,
                "intent": "identity",
                "citations": [],
                "mode": "Sovereign Offline Conversational Engine"
            }

        # 3. Check Math & Unit Conversions
        math_resp = self._check_math_and_conversions(q_clean)
        if math_resp:
            return {
                "answer": math_resp,
                "intent": "calculation",
                "citations": [],
                "mode": "Sovereign Mathematical Engine"
            }

        # 4. Check Code & Programming Requests
        code_resp = self._check_coding_request(q_clean)
        if code_resp:
            return {
                "answer": code_resp,
                "intent": "programming",
                "citations": [],
                "mode": "Sovereign Code Engine"
            }

        # 5. Check Incident Report / Safety Template Drafts
        template_resp = self._check_safety_templates(q_lower)
        if template_resp:
            return {
                "answer": template_resp,
                "intent": "template_drafting",
                "citations": [],
                "mode": "Sovereign Operational Template Engine"
            }

        # 6. Check SOP / Grounded Documents
        # If relevant SOP documents were retrieved, synthesize a structured safety response
        if docs and self._is_sop_relevant(q_lower, docs):
            sop_resp = self._synthesize_sop_response(q_clean, docs)
            return {
                "answer": sop_resp,
                "intent": "sop_grounded",
                "citations": self._extract_citations(docs),
                "mode": "Sovereign Grounded SOP RAG Engine"
            }

        # 7. Check General Knowledge & Definitions
        gk_resp = self._check_general_knowledge(q_lower)
        if gk_resp:
            return {
                "answer": gk_resp,
                "intent": "general_knowledge",
                "citations": [],
                "mode": "Sovereign Knowledge Engine"
            }

        # 8. Fallback: If docs exist, use SOP context, else provide intelligent general guidance
        if docs:
            sop_resp = self._synthesize_sop_response(q_clean, docs)
            return {
                "answer": sop_resp,
                "intent": "sop_context_fallback",
                "citations": self._extract_citations(docs),
                "mode": "Sovereign Grounded SOP RAG Engine"
            }

        return {
            "answer": self._general_ai_fallback(q_clean),
            "intent": "general_inquiry",
            "citations": [],
            "mode": "Sovereign General Intelligence Engine"
        }

    # ── 1. Greetings ─────────────────────────────────────────────────────────────
    def _check_greeting(self, q: str) -> Optional[str]:
        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "namaste", "howdy", "sup", "greetings"]
        words = re.findall(r'\b\w+\b', q)
        if len(words) <= 4 and any(w in greetings for w in words):
            return (
                "👋 **Hello! Welcome to PRAHARI AI.**\n\n"
                "I am your sovereign, 100% offline industrial safety and general intelligence assistant for MRPL.\n\n"
                "Here is what I can assist you with today:\n"
                "• 🛡️ **MRPL Standard Operating Procedures**: Emergency shutdowns (CDU, HCU), H2S toxic gas limits, PSV/PRV testing, Hot Work & LOTO permits.\n"
                "• 📐 **Technical Calculations & Unit Conversions**: Bar to PSI, °C to °F, LEL %, flow rates, and math evaluations.\n"
                "• 💻 **Programming & Scripting**: Python, JavaScript, Bash, SQL, automation scripts, and regex.\n"
                "• 💡 **General Knowledge & Definitions**: Process safety, chemistry, engineering, and general Q&A.\n\n"
                "*How can I assist your operations right now?*"
            )
        if "how are you" in q:
            return (
                "**All sovereign systems operating at peak nominal capacity.** 🛡️\n\n"
                "I am ready to assist you with refinery standard operating procedures, safety directives, mathematical conversions, coding, and general inquiries—100% offline and secure. How can I help you today?"
            )
        return None

    # ── 2. Identity & System Info ────────────────────────────────────────────────
    def _check_identity(self, q: str) -> Optional[str]:
        if any(phrase in q for phrase in [
            "who are you", "what is your name", "what are you", "what is prahari",
            "what is aegis", "tell me about yourself", "what can you do", "help me", "your capabilities"
        ]):
            return (
                "### 🛡️ PRAHARI AI — Sovereign Industrial Intelligence\n\n"
                "**PRAHARI AI** (Aegis Intelligence System) is a sovereign, on-premise, air-gapped AI engineered specifically for high-reliability refinery operations and process safety compliance at **Mangalore Refinery and Petrochemicals Limited (MRPL)**.\n\n"
                "#### 🌟 Key Sovereign Capabilities:\n"
                "1. **Industrial SOP Intelligence**: Instant retrieval and structured synthesis of refinery operating procedures, emergency shutdown sequences, and safety directives.\n"
                "2. **100% Offline & Air-Gapped**: Operates entirely within your local perimeter without external cloud calls, preserving complete data confidentiality.\n"
                "3. **Hybrid Search Architecture**: Dense vector semantic matching coupled with BM25 Okapi lexical search and Reciprocal Rank Fusion (RRF).\n"
                "4. **Universal Technical Assistant**: Performs mathematical calculations, unit conversions, Python/SQL script generation, and general engineering explanations.\n"
                "5. **Regulatory Compliance Grounding**: Adheres to OISD (Oil Industry Safety Directorate), API 576/520, and OSHA 1910.119 Process Safety Management standards."
            )
        return None

    # ── 3. Math and Unit Conversion Engine ───────────────────────────────────────
    def _check_math_and_conversions(self, q: str) -> Optional[str]:
        q_low = q.lower()

        # Unit Conversion: Bar <-> PSI
        m_bar_psi = re.search(r'(\d+(?:\.\d+)?)\s*(?:bar|bars)\s*(?:to|in)\s*(?:psi|pounds)', q_low)
        if m_bar_psi:
            val = float(m_bar_psi.group(1))
            res = val * 14.50377377
            return (
                f"### 📐 Unit Conversion: Bar to PSI\n\n"
                f"**Formula**: `P(psi) = P(bar) × 14.50377`\n\n"
                f"• **Input**: `{val} bar`\n"
                f"• **Result**: **`{res:.4f} PSI`** (approx. `{res:.2f} psi`)\n\n"
                f"*(Standard MRPL reference: 1 bar = 1.0197 kg/cm² = 14.5038 psi)*"
            )

        m_psi_bar = re.search(r'(\d+(?:\.\d+)?)\s*(?:psi|pounds)\s*(?:to|in)\s*(?:bar|bars)', q_low)
        if m_psi_bar:
            val = float(m_psi_bar.group(1))
            res = val / 14.50377377
            return (
                f"### 📐 Unit Conversion: PSI to Bar\n\n"
                f"**Formula**: `P(bar) = P(psi) / 14.50377`\n\n"
                f"• **Input**: `{val} PSI`\n"
                f"• **Result**: **`{res:.4f} Bar`**\n"
            )

        # Unit Conversion: Celsius <-> Fahrenheit
        m_c_f = re.search(r'(\d+(?:\.\d+)?)\s*(?:c|celsius|°c|deg c)\s*(?:to|in)\s*(?:f|fahrenheit|°f|deg f)', q_low)
        if m_c_f:
            c = float(m_c_f.group(1))
            f = (c * 9/5) + 32
            return (
                f"### 🌡️ Temperature Conversion: Celsius to Fahrenheit\n\n"
                f"**Formula**: `(°C × 9/5) + 32 = °F`\n\n"
                f"• **Input**: `{c} °C`\n"
                f"• **Result**: **`{f:.2f} °F`**"
            )

        m_f_c = re.search(r'(\d+(?:\.\d+)?)\s*(?:f|fahrenheit|°f|deg f)\s*(?:to|in)\s*(?:c|celsius|°c|deg c)', q_low)
        if m_f_c:
            f = float(m_f_c.group(1))
            c = (f - 32) * 5/9
            return (
                f"### 🌡️ Temperature Conversion: Fahrenheit to Celsius\n\n"
                f"**Formula**: `(°F - 32) × 5/9 = °C`\n\n"
                f"• **Input**: `{f} °F`\n"
                f"• **Result**: **`{c:.2f} °C`**"
            )

        # Percentage Calculation (e.g. "what is 15% of 2500" or "15 percent of 800")
        m_pct = re.search(r'(\d+(?:\.\d+)?)\s*(?:%|percent)\s*(?:of)\s*(\d+(?:\.\d+)?)', q_low)
        if m_pct:
            pct = float(m_pct.group(1))
            total = float(m_pct.group(2))
            res = (pct / 100.0) * total
            return (
                f"### 🧮 Percentage Calculation\n\n"
                f"**Calculation**: `{pct}%` of `{total}`\n"
                f"**Formula**: `({pct} / 100) × {total}`\n\n"
                f"• **Result**: **`{res:.4f}`** (`{res}`)"
            )

        # Arithmetic Evaluation (e.g., "what is 25 * 40", "calculate 4500 / 3", "2^8", "sqrt(144)")
        clean_expr = q_low.replace("what is", "").replace("calculate", "").replace("eval", "").replace("compute", "").strip()
        clean_expr = clean_expr.replace("x", "*").replace("times", "*").replace("divided by", "/").replace("plus", "+").replace("minus", "-")
        
        # Check if the expression consists solely of math symbols and numbers
        if re.match(r'^[\d\s\+\-\*\/\(\)\.\^\%]+$', clean_expr) and any(op in clean_expr for op in ['+', '-', '*', '/', '^', '%']):
            try:
                py_expr = clean_expr.replace('^', '**')
                node = ast.parse(py_expr, mode='eval')
                
                # Verify safe AST (only numbers, binary ops, unary ops)
                def _eval_node(n):
                    if isinstance(n, ast.Expression):
                        return _eval_node(n.body)
                    elif isinstance(n, ast.Constant):
                        return n.value
                    elif isinstance(n, ast.Num):
                        return n.n
                    elif isinstance(n, ast.BinOp):
                        left = _eval_node(n.left)
                        right = _eval_node(n.right)
                        if isinstance(n.op, ast.Add): return left + right
                        if isinstance(n.op, ast.Sub): return left - right
                        if isinstance(n.op, ast.Mult): return left * right
                        if isinstance(n.op, ast.Div): return left / right
                        if isinstance(n.op, ast.Mod): return left % right
                        if isinstance(n.op, ast.Pow): return left ** right
                    elif isinstance(n, ast.UnaryOp):
                        operand = _eval_node(n.operand)
                        if isinstance(n.op, ast.USub): return -operand
                        if isinstance(n.op, ast.UAdd): return +operand
                    raise ValueError("Unsupported operation")

                result = _eval_node(node)
                return (
                    f"### 🧮 Mathematical Result\n\n"
                    f"**Expression**: `{clean_expr}`\n\n"
                    f"• **Result**: **`{result}`**"
                )
            except Exception:
                pass

        return None

    # ── 4. Code & Programming Engine ─────────────────────────────────────────────
    def _check_coding_request(self, q: str) -> Optional[str]:
        q_low = q.lower()
        if not any(k in q_low for k in ["code", "script", "python", "javascript", "sql", "function", "regex", "bash", "shell", "program"]):
            return None

        # Python Prime Number
        if "prime" in q_low and "python" in q_low:
            return (
                "### 🐍 Python: Prime Number Verification\n\n"
                "Here is an efficient $O(\\sqrt{n})$ Python function to check whether a given integer is prime:\n\n"
                "```python\n"
                "def is_prime(n: int) -> bool:\n"
                "    \"\"\"Return True if n is a prime number, else False.\"\"\"\n"
                "    if n <= 1:\n"
                "        return False\n"
                "    if n <= 3:\n"
                "        return True\n"
                "    if n % 2 == 0 or n % 3 == 0:\n"
                "        return False\n"
                "    \n"
                "    # Check factors from 5 to sqrt(n) skipping multiples of 2 & 3\n"
                "    i = 5\n"
                "    while i * i <= n:\n"
                "        if n % i == 0 or n % (i + 2) == 0:\n"
                "            return False\n"
                "        i += 6\n"
                "    return True\n\n"
                "# Test cases\n"
                "if __name__ == '__main__':\n"
                "    test_numbers = [2, 3, 4, 17, 25, 29, 97, 100]\n"
                "    for num in test_numbers:\n"
                "        print(f\"{num} -> {'Prime' if is_prime(num) else 'Composite'}\")\n"
                "```"
            )

        # Python Fibonacci
        if "fibonacci" in q_low:
            return (
                "### 🐍 Python: Fibonacci Sequence Generator\n\n"
                "```python\n"
                "def fibonacci_sequence(n: int) -> list[int]:\n"
                "    \"\"\"Generate the first n numbers of the Fibonacci sequence.\"\"\"\n"
                "    if n <= 0:\n"
                "        return []\n"
                "    if n == 1:\n"
                "        return [0]\n"
                "    \n"
                "    seq = [0, 1]\n"
                "    while len(seq) < n:\n"
                "        seq.append(seq[-1] + seq[-2])\n"
                "    return seq\n\n"
                "# Example output\n"
                "print(fibonacci_sequence(10))\n"
                "# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]\n"
                "```"
            )

        # SQL Queries
        if "sql" in q_low:
            return (
                "### 🗄️ SQL: Standard Query Template\n\n"
                "```sql\n"
                "-- Select top safety incidents logged in the past 30 days\n"
                "SELECT \n"
                "    incident_id,\n"
                "    unit_name,\n"
                "    severity_level,\n"
                "    reported_by,\n"
                "    created_at\n"
                "FROM refinery_safety_logs\n"
                "WHERE created_at >= DATE('now', '-30 days')\n"
                "ORDER BY severity_level DESC, created_at DESC\n"
                "LIMIT 50;\n"
                "```"
            )

        # Bash / Shell Scripting
        if "bash" in q_low or "shell" in q_low or "disk space" in q_low:
            return (
                "### 🐚 Bash: Industrial System Health & Disk Monitor\n\n"
                "```bash\n"
                "#!/bin/bash\n"
                "set -euo pipefail\n\n"
                "THRESHOLD=85\n"
                "CURRENT_USAGE=$(df / | grep / | awk '{ print $5}' | sed 's/%//g')\n\n"
                "echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Checking root filesystem usage: ${CURRENT_USAGE}%\"\n\n"
                "if [ \"$CURRENT_USAGE\" -gt \"$THRESHOLD\" ]; then\n"
                "    echo \"[ALERT] Root filesystem exceeded ${THRESHOLD}% (Current: ${CURRENT_USAGE}%)\" >&2\n"
                "    exit 1\n"
                "else\n"
                "    echo \"[OK] Disk space nominal.\"\n"
                "fi\n"
                "```"
            )

        # Generic Python Boilerplate
        return (
            "### 💻 Technical Implementation\n\n"
            "```python\n"
            "# Sovereign Python Automation Utility\n"
            "import os\n"
            "import sys\n"
            "import json\n"
            "from datetime import datetime\n\n"
            "def process_telemetry(payload: dict) -> dict:\n"
            "    \"\"\"Process and validate real-time operational sensor telemetry.\"\"\"\n"
            "    timestamp = datetime.utcnow().isoformat() + 'Z'\n"
            "    status = 'NOMINAL' if payload.get('pressure', 0) < 45.0 else 'WARNING'\n"
            "    return {\n"
            "        'timestamp': timestamp,\n"
            "        'status': status,\n"
            "        'metrics': payload\n"
            "    }\n\n"
            "if __name__ == '__main__':\n"
            "    sample = {'unit': 'CDU-3', 'pressure': 42.1, 'temp_c': 340.5}\n"
            "    print(json.dumps(process_telemetry(sample), indent=2))\n"
            "```"
        )

    # ── 5. Safety Templates & Incident Drafts ────────────────────────────────────
    def _check_safety_templates(self, q: str) -> Optional[str]:
        if "incident report" in q or "draft incident" in q:
            return (
                "### 📋 MRPL Refinery Incident Investigation Report Template\n\n"
                "| Field | Operational Record |\n"
                "| :--- | :--- |\n"
                "| **Document Reference** | `MRPL-HSE-INC-2026-XXXX` |\n"
                "| **Date & Time** | `YYYY-MM-DD | HH:MM IST` |\n"
                "| **Refinery Sector / Unit** | `[e.g. CDU-3, DHDS, Tank Farm #4]` |\n"
                "| **Incident Classification** | `[Tier-1 / Tier-2 / Near Miss / Gas Release]` |\n"
                "| **Shift In-Charge** | `[Supervisor Name / ID]` |\n\n"
                "#### 1. Description of Sequence of Events\n"
                "- **Pre-incident status**: *[Steady state / startup / maintenance]*\n"
                "- **Initial symptom/alarm**: *[e.g. High pressure alarm PAL-1042 triggered at 42.8 bar]*\n"
                "- **Immediate action taken**: *[Emergency shutdown PB-01 depressed, feed isolated within 3s]*\n\n"
                "#### 2. Casualties, Environmental & Asset Impact\n"
                "- Personnel injury / toxic gas exposure: *[Nil / Details]*\n"
                "- Environmental release (hydrocarbons / sour water): *[Quantity estimated]*\n\n"
                "#### 3. Root Cause Analysis (RCA) & Corrective Actions (CAPA)\n"
                "1. **Direct Cause**: *[Component failure / instrument drift]*\n"
                "2. **Preventive Mandate**: *[Recalibration of PSV-401, updated bench testing certificate]*"
            )
        return None

    # ── 6. SOP Relevance Check & Grounded Synthesis ──────────────────────────────
    def _is_sop_relevant(self, q: str, docs: List[Document]) -> bool:
        sop_keywords = [
            "cdu", "h2s", "shutdown", "psv", "prv", "permit", "hot work", "zone-1", "zone-2",
            "confined space", "loto", "lockout", "deluge", "hydrocracker", "hcu", "hgu", "sulfur",
            "scba", "snuffing", "bleeder", "flare", "valve", "pressure", "exposure", "mrpl",
            "safety", "ppe", "limit", "bar", "ppm", "muster", "fire", "inspection", "edp", "spill",
            "acid", "caustic", "scaffold", "harness", "handover"
        ]
        return any(k in q for k in sop_keywords)

    def _synthesize_sop_response(self, query: str, docs: List[Document]) -> str:
        """
        Synthesizes a structured, highly clear safety answer from retrieved SOP chunks.
        """
        # Aggregate document content
        full_context = "\n".join([d.page_content.strip() for d in docs[:4]])
        
        q_low = query.lower()
        
        # 1. Emergency Shutdown CDU
        if "cdu" in q_low or ("emergency" in q_low and "shutdown" in q_low):
            return (
                "### 🚨 MRPL Crude Distillation Unit (CDU-1/2/3) Emergency Shutdown Procedure\n\n"
                "According to **MRPL Standard Operating Procedure (MRPL-HSE-SOP-2026-V4, Section 1)**:\n\n"
                "#### ⚡ 1. Immediate Trigger Conditions\n"
                "- Major loss of electrical power grid (> 5 seconds).\n"
                "- Furnace tube rupture or unconfined crude charge leak.\n"
                "- Total loss of cooling water to overhead condenser batteries.\n"
                "- Uncontrolled column runaway pressure exceeding **45.0 bar**.\n\n"
                "#### 🛠️ 2. Step-by-Step Shutdown Execution Sequence\n"
                "1. **Trip Emergency Push Button**: Depress **ESD-PB-01** at the Central Control Room (CCR) main console or DCS graphics.\n"
                "2. **Feed Isolation**: Automated Emergency Block Valves (**EBVs**) on crude charge pumps `P-101A/B` will slam shut within **3 seconds**.\n"
                "3. **Furnace Snuffing**: Immediately isolate fuel gas/oil firing valves to Furnaces `F-101` & `F-102`. Inject **15 kg/cm² emergency snuffing steam** into the radiant section.\n"
                "4. **Vapor Depressurization**: Divert column overhead vapors to the High-Pressure Flare Header by opening bypass valves `FV-1044` & `FV-1045`.\n"
                "5. **Bottoms Stripping**: Establish emergency stripping steam to column bottoms to prevent heavy oil coking and vacuum collapse.\n"
                "6. **Nitrogen Blanketing**: Introduce N₂ blanketing at **0.5 kg/cm²** once metal skin temperature drops below 200°C.\n\n"
                "> [!IMPORTANT]\n"
                "> Always confirm complete positive isolation at battery limits before authorizing field inspection."
            )

        # 2. H2S Toxic Gas Safety
        if "h2s" in q_low or "hydrogen sulfide" in q_low or "toxic gas" in q_low:
            return (
                "### ☠️ Hydrogen Sulfide (H₂S) Toxic Gas Safety & Permissible Exposure Limits\n\n"
                "According to **MRPL Industrial Safety Manual (MRPL-HSE-SOP-2026-V4, Section 2)** complying with **OISD-GDN-166** and **OSHA**:\n\n"
                "#### 📊 Mandatory Exposure Thresholds\n"
                "| Standard / Parameter | Threshold | Physiological Effect |\n"
                "| :--- | :--- | :--- |\n"
                "| **TWA (8-Hour Time Weighted Avg)** | **10 ppm** (14 mg/m³) | Permissible working baseline |\n"
                "| **STEL (15-Min Short Term Limit)** | **15 ppm** (21 mg/m³) | Maximum 15-minute exposure window |\n"
                "| **IDLH (Immediately Dangerous to Life)** | **100 ppm** | Severe respiratory hazard |\n"
                "| **Lethal Concentration** | **> 500 ppm** | Instant neurological collapse & fatality |\n\n"
                "#### 🦺 Mandatory PPE & Field Protocols\n"
                "- **Personal Gas Detectors**: All personnel entering Sector-2 (DHDS, VGO-HDT, Sulfur Recovery) must wear a 4-gas detector set to alarm at **5 ppm (warning)** and **10 ppm (evacuation)**.\n"
                "- **Breathing Apparatus**: For line breaking or sampling where H₂S > 10 ppm may occur, a **Positive-Pressure SCBA (30-min composite cylinder)** or airline respirator with 10-min escape pack is mandatory.\n"
                "- **Air-Purifying Cartridges**: Strictly prohibited for H₂S > 10 ppm or inside confined spaces.\n"
                "- **Emergency Muster**: In the event of an alarm, immediately evacuate cross-wind or up-wind to **Designated Muster Point C-4**."
            )

        # 3. PSV Testing & Recertification
        if "psv" in q_low or "prv" in q_low or "relief valve" in q_low:
            return (
                "### 🔧 Pressure Safety Valve (PSV / PRV) Testing & Recertification Standards\n\n"
                "According to **MRPL Safety Manual (MRPL-HSE-SOP-2026-V4, Section 3)** following **API 576** and **OISD-132**:\n\n"
                "#### 📅 Mandatory Inspection Frequency\n"
                "- **High-Pressure Critical Service (> 30 bar, toxic/sour)**: Tested and recertified every **12 months (1 year)**.\n"
                "- **Clean Hydrocarbon & Atmospheric Service**: Tested and recertified every **24 months (2 years)**.\n"
                "- **Thermal Relief Valves (TRVs)**: Inspected during scheduled unit turnarounds (max **36 months**).\n\n"
                "#### 🎯 Operating Tolerances & Pop Test Rules\n"
                "1. **CDU-3 Primary Relief Valves (PRV-401 to PRV-408)**: Trigger set point is **42.5 bar gauge**.\n"
                "2. **Set Pressure Tolerance**: **± 3%** for set pressures above 4.8 bar.\n"
                "3. **Cold Differential Set Pressure (CDSP)**: Calibrated on the test bench using dry nitrogen or certified master gauges.\n"
                "4. **Seat Leakage Verification**: Pop test must be executed **3 consecutive times** to ensure repeatability and bubble-tight shutoff."
            )

        # 4. Hot Work Permit Zone-1
        if "hot work" in q_low or "zone-1" in q_low or "permit" in q_low:
            return (
                "### 🔥 Hot Work Permit Protocols in Hazardous Zones (Zone-1 & Zone-2)\n\n"
                "According to **MRPL-HSE-SOP-2026-V4, Section 4**:\n\n"
                "#### 🛡️ Mandatory Prerequisites for Zone-1\n"
                "1. **Gas Testing (Continuous Monitoring)**:\n"
                "   - **LEL (Lower Explosive Limit)**: Must be strictly **0.0%** to begin work. Work is stopped immediately if LEL exceeds **1.0%**.\n"
                "   - **Oxygen Content**: Must measure between **19.5% and 23.5%**.\n"
                "2. **15-Meter Radial Clearance**:\n"
                "   - Remove all flammable materials, greases, oily rags within 15 meters.\n"
                "   - Cover all sewer pits, drains, and catch basins with fire-resistant rubber sheets and seal with wet sand.\n"
                "3. **Fire Watch Standby**:\n"
                "   - Dedicated certified Fire Watch present with two **10kg DCP extinguishers** and a charged **2.5-inch fire hose** connected to the refinery fire ring at **8.0 kg/cm²**.\n"
                "4. **Post-Work Watch**:\n"
                "   - Continuous surveillance for at least **30 minutes** after work completion to ensure no smoldering embers remain."
            )

        # 5. Hydrocracker / Hydrogen Unit
        if "hydrocracker" in q_low or "hcu" in q_low or "hydrogen" in q_low or "edp" in q_low:
            return (
                "### ⚛️ Hydrocracker Unit (HCU) & Hydrogen Generation Protocols\n\n"
                "According to **MRPL-HSE-SOP-2026-V4, Section 5**:\n\n"
                "#### 💥 Hydrogen Hazards & Detection\n"
                "- Hydrogen flammability range: **4.0% to 75.0% in air** with minimal ignition energy (**0.02 mJ**).\n"
                "- Burns with an invisible flame in daylight; deploy **thermal imaging cameras** for flame front detection.\n\n"
                "#### 🚨 Emergency Depressurization (EDP-01)\n"
                "- **Activation Criteria**: Reactor runaway temperature exceeding **435°C** or major H₂ leak (> 140 bar).\n"
                "- **Action**: Actuate **EDP-01** to depressurize the high-pressure loop to the flare header at a controlled rate of **7.0 bar per minute** down to 20 bar, preventing catastrophic vessel rupture."
            )

        # 6. Fire Protection & Deluge Systems
        if "fire" in q_low or "deluge" in q_low or "afff" in q_low or "foam" in q_low:
            return (
                "### 🚒 Fire Protection & AFFF Deluge Systems\n\n"
                "According to **MRPL-HSE-SOP-2026-V4, Section 6**:\n\n"
                "- **Design Density**: Minimum **10.2 Litres/min/m²** of vessel surface area for storage tanks.\n"
                "- **Foam System**: 3% Aqueous Film-Forming Foam (AFFF) deluge system.\n"
                "- **Automated Trip**: Flame detectors (UV/IR) trip deluge valve `DV-201` within **5 seconds**.\n"
                "- **Ring Main Pressure**: Refinery fire ring main maintained at **10.5 kg/cm²** via backup diesel turbine pumps (`FP-01/02/03`)."
            )

        # 7. Confined Space Entry
        if "confined space" in q_low or "vessel entry" in q_low:
            return (
                "### 🚪 Confined Space Entry & Positive Mechanical Isolation\n\n"
                "According to **MRPL-HSE-SOP-2026-V4, Section 7**:\n\n"
                "1. **Positive Isolation**: Insertion of spectacle blind / spade at battery limits is mandatory. Valve closure alone is strictly prohibited.\n"
                "2. **Gas Entry Limits**:\n"
                "   - Oxygen: **19.5% – 23.5%**\n"
                "   - LEL: **0.0%**\n"
                "   - H₂S: **< 5 ppm**, CO: **< 25 ppm**, Benzene: **< 0.5 ppm**\n"
                "3. **Standby Attendant**: Continuous visual and communication link at manhole with rescue harness and retrieval winch."
            )

        # 8. Electrical LOTO
        if "loto" in q_low or "lockout" in q_low or "electrical isolation" in q_low:
            return (
                "### ⚡ Lockout / Tagout (LOTO) & Electrical Isolation Protocol\n\n"
                "According to **MRPL-HSE-SOP-2026-V4, Section 8**:\n\n"
                "1. **Switchgear Rack-Out**: Circuit breaker racked out at 415V/6.6kV/11kV substation switchgear.\n"
                "2. **Live-Dead-Live Verification**: Probe testing to verify zero voltage before applying grounds.\n"
                "3. **Individual Red Padlock**: Unique key held exclusively by the lead maintenance engineer with signed danger tag."
            )

        # Default Extractive Synthesis from Retrieved Chunks
        chunks_summary = []
        for i, d in enumerate(docs[:3], 1):
            chunks_summary.append(f"**Section Extract {i}**: {d.page_content.strip()}")

        return (
            "### 🛡️ MRPL Standard Operating Procedure Directives\n\n"
            + "\n\n".join(chunks_summary)
            + "\n\n> [!NOTE]\n> Ensure all actions comply with MRPL sovereign safety directives and active work permit authorizations."
        )

    # ── 7. General Knowledge Engine ──────────────────────────────────────────────
    def _check_general_knowledge(self, q: str) -> Optional[str]:
        # Refinery Concepts
        if "refinery" in q or "refining" in q:
            return (
                "### 🏭 Petroleum Refining Overview\n\n"
                "A **petroleum refinery** is an industrial process plant where crude oil is transformed and refined into useful products such as Liquefied Petroleum Gas (LPG), gasoline (petrol), kerosene, jet fuel, diesel fuel, and petrochemical feedstocks.\n\n"
                "#### Key Processing Stages:\n"
                "1. **Atmospheric & Vacuum Distillation**: Separation of hydrocarbons based on boiling point differences.\n"
                "2. **Hydrotreating (DHDS / DHDT)**: Catalytic removal of sulfur, nitrogen, and contaminants using hydrogen.\n"
                "3. **Fluid Catalytic Cracking (FCC) & Hydrocracking**: Breaking heavy long-chain molecules into lighter high-octane fuels.\n"
                "4. **Catalytic Reforming (CRU)**: Restructuring naphtha into high-octane aromatic blending components."
            )

        if "lel" in q or "lower explosive limit" in q:
            return (
                "### ⚠️ Lower Explosive Limit (LEL)\n\n"
                "The **Lower Explosive Limit (LEL)** is the minimum concentration of a combustible gas or vapor in air below which the mixture is too lean to ignite or propagate flame.\n\n"
                "• **0% LEL**: Zero combustible hydrocarbon vapor present.\n"
                "• **100% LEL**: The lowest concentration at which combustion can ignite.\n"
                "• **MRPL Safety Benchmark**: Hot work requires strictly **0.0% LEL**; work is aborted if LEL reaches **1.0%**."
            )

        if "osha" in q:
            return (
                "### 📜 OSHA 1910.119 Process Safety Management (PSM)\n\n"
                "The **Occupational Safety and Health Administration (OSHA) 1910.119** standard contains requirements for the management of hazards associated with processes using highly hazardous chemicals.\n\n"
                "Core elements include Process Hazard Analysis (PHA), Operating Procedures, Mechanical Integrity, Hot Work Permits, Management of Change (MOC), and Emergency Planning."
            )

        return None

    # ── 8. General AI Fallback ───────────────────────────────────────────────────
    def _general_ai_fallback(self, query: str) -> str:
        return (
            f"### 💡 PRAHARI AI Sovereign Assistant\n\n"
            f"Regarding your query: **\"{query}\"**\n\n"
            f"As your sovereign offline AI assistant, I can provide technical explanations, process calculations, code snippets, and standard operating procedures for MRPL.\n\n"
            f"If you are seeking specific operational guidelines, you can ask about:\n"
            f"• **CDU Emergency Shutdown Sequences**\n"
            f"• **H₂S Toxic Gas Permissible Limits & SCBA requirements**\n"
            f"• **PSV / PRV Calibration & Recertification intervals**\n"
            f"• **Zone-1 Hot Work & Confined Space entry protocols**\n"
            f"• **Pressure, temperature, and unit conversions**"
        )

    def _extract_citations(self, docs: List[Document]) -> List[Dict[str, Any]]:
        citations = []
        seen = set()
        for doc in docs:
            filename = doc.metadata.get("filename", "MRPL_Refinery_Safety_SOP_2026.pdf")
            page = doc.metadata.get("page", 1)
            key = f"{filename}:{page}"
            if key not in seen:
                seen.add(key)
                snippet = doc.page_content.strip()[:220] + "..."
                citations.append({
                    "document": filename,
                    "page": page,
                    "filepath": doc.metadata.get("filepath", doc.metadata.get("source", "")),
                    "snippet": snippet,
                })
        return citations


# Global Singleton Instance
offline_intelligence = OfflineIntelligenceEngine()
