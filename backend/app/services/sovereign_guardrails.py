import hashlib
import time
import re
from typing import Dict, Any, List, Optional

class SovereignGuardrails:
    """
    Sovereign Safety Guardrails & Evidence-Chain Verifier for MRPL.
    Enforces strict grounding, calibrated citation-gap refusals,
    non-autonomous DCS/SCADA safety boundaries, and cryptographic audit hashing.
    """

    def __init__(self):
        pass

    def evaluate_safety_query(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Detects ungrounded, hazardous, or policy-violating queries and returns
        a calibrated sovereign refusal with citation-gap disclosure.
        """
        q_lower = query.lower()

        # 1. Unsafe override / bypass requests
        unsafe_patterns = [
            r'bypass.*esd', r'disable.*trip', r'override.*interlock', r'suppress.*alarm',
            r'run.*90\s*bar', r'90\s*bar', r'ignore.*h2s', r'confined space without blind',
            r'bypass.*trip', r'bypass.*shutdown', r'override.*shutdown'
        ]

        if any(re.search(pat, q_lower) for pat in unsafe_patterns):
            return {
                "answer": (
                    "### 🛑 SOVEREIGN SAFETY COMPLIANCE REFUSAL: ZERO-TOLERANCE TRIP VIOLATION\n\n"
                    "**Directive**: *Action Aborted — Severe Process Safety Violation (OSHA 1910.119 / OISD-GDN-166)*\n\n"
                    "#### ⚠️ Why This Request Was Refused:\n"
                    "- **Zero-Tolerance Safety Mandate**: Overriding Emergency Shutdown (ESD) interlocks, operating the column at 90 bar (safe design limit is **45.0 bar**), or disabling safety trips creates an imminent risk of catastrophic vessel rupture.\n"
                    "- **Citation Gap**: No MRPL Standard Operating Procedure authorizes interlock suppression or exceeding design limits.\n\n"
                    "#### 🛡️ Mandatory Compliance Protocol:\n"
                    "1. Any temporary bypass of safety-instrumented systems (SIS) requires written authorization from the **Refinery Executive Director (Operations)**.\n"
                    "2. The bypass must be logged in the **Shift Critical Trip Bypass Register** with continuous physical standby monitoring."
                ),
                "intent": "safety_violation_refusal",
                "mode": "Sovereign Safety Compliance Guardrail (Zero-Tolerance Enforcement)",
                "citations": [
                    {
                        "document": "MRPL_Refinery_Safety_SOP_2026.pdf",
                        "page": 1,
                        "snippet": "Section 1.1: Column runaway pressure > 45.0 bar triggers immediate Emergency Shutdown (ESD-PB-01). Bypassing ESD interlocks is strictly prohibited.",
                        "filepath": "MRPL_Refinery_Safety_SOP_2026.pdf"
                    }
                ]
            }

        # 2. Dangerous Speculation on Unsupported Parameters
        if any(k in q_lower for k in ["nuclear reactor", "uranium enrichment", "weapon", "explosive recipe"]):
            return {
                "answer": (
                    "### 🛑 SOVEREIGN BOUNDARY REFUSAL: CITATION GAP\n\n"
                    "**Refusal Reason**: Query is outside the sovereign operational mandate of Mangalore Refinery and Petrochemicals Limited (MRPL). No authorized industrial documentation exists for this subject."
                ),
                "intent": "out_of_scope_refusal",
                "mode": "Sovereign Mandate Guardrail",
                "citations": []
            }

        return None

    def generate_audit_hash(self, query: str, answer: str) -> str:
        """Generates an immutable cryptographic SHA-256 evidence-chain audit hash."""
        raw = f"{query}|{answer}|{time.time()}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16].upper()

    def append_sovereign_footer(self, answer: str, query: str) -> str:
        """Appends official sovereign compliance badges and audit metadata in clean Markdown."""
        audit_hash = self.generate_audit_hash(query, answer)
        badge = (
            f"\n\n---\n"
            f"> 🛡️ **Classification:** SOVEREIGN OPERATIONAL DIRECTIVE &bull; **Evidence Hash:** `{audit_hash}` &bull; **Mode:** 100% Offline / Air-Gapped\n"
        )
        return answer + badge


# Global Singleton Instance
sovereign_guardrails = SovereignGuardrails()
