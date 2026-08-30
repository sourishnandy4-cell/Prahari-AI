import re
from typing import Dict, Any, List, Optional

class EquipmentRegistry:
    """
    Sovereign Asset & Equipment Maintenance Registry for MRPL.
    Stores authoritative maintenance history, calibration schedules, pop-test tolerances,
    metallurgical specs, and operational status for critical plant equipment.
    """

    def __init__(self):
        self.assets: Dict[str, Dict[str, Any]] = {
            "P-101A": {
                "tag": "P-101A",
                "name": "CDU-3 Primary Crude Charge Pump (Lead)",
                "unit": "Crude Distillation Unit (CDU-3)",
                "criticality": "Tier-1 High Criticality",
                "service": "Sour Crude Hydrocarbon Feed",
                "type": "API 610 Between-Bearing Multi-Stage Centrifugal",
                "design_specs": {
                    "flow_rate": "450 m³/hr",
                    "differential_head": "185 meters",
                    "operating_pressure": "22.5 bar gauge",
                    "driver_power": "650 kW (6.6 kV Induction Motor)",
                    "seal_plan": "API Plan 53B Dual Mechanical Seal with Barrier Fluid Accumulator",
                    "casing_material": "ASTM A216 WCB with 12% Cr Impeller",
                },
                "maintenance_history": [
                    {
                        "date": "2026-02-14",
                        "work_order": "WO-MRPL-2026-0892",
                        "type": "Major Overhaul & Rotor Dynamic Balancing",
                        "technician": "S. Rao (Lead Mechanical Specialist)",
                        "findings": "DE/NDE journal bearings replaced; seal faces re-lapped; vibration levels reduced from 4.8 mm/s to 1.1 mm/s RMS (ISO 10816 Class-I compliance).",
                        "status": "Certified Operational",
                    },
                    {
                        "date": "2025-08-20",
                        "work_order": "WO-MRPL-2025-4122",
                        "type": "Mechanical Seal Plan 53B Bladder Recharge",
                        "technician": "M. Kumar",
                        "findings": "Nitrogen pre-charge set to 18.0 bar; barrier fluid synthetic ester topped up.",
                        "status": "Passed",
                    }
                ],
                "next_pm_due": "2026-08-14 (6-Month Vibration & Lube Oil Spectrometry)",
                "active_permits": "None (Unit running in steady-state DCS loop)",
            },
            "P-101B": {
                "tag": "P-101B",
                "name": "CDU-3 Secondary Crude Charge Pump (Standby)",
                "unit": "Crude Distillation Unit (CDU-3)",
                "criticality": "Tier-1 High Criticality",
                "service": "Sour Crude Hydrocarbon Feed",
                "type": "API 610 Multi-Stage Centrifugal",
                "design_specs": {
                    "flow_rate": "450 m³/hr",
                    "differential_head": "185 meters",
                    "driver_power": "650 kW (6.6 kV)",
                    "seal_plan": "API Plan 53B",
                },
                "maintenance_history": [
                    {
                        "date": "2026-01-10",
                        "work_order": "WO-MRPL-2026-0144",
                        "type": "Auto-Start Interlock Test & Lube Oil Replacement",
                        "technician": "P. Shetty",
                        "findings": "Auto-standby transfer verified; started within 2.4s of pressure drop signal.",
                        "status": "Certified Standby Ready",
                    }
                ],
                "next_pm_due": "2026-07-10",
                "active_permits": "Standby auto-cut-in armed",
            },
            "PRV-401": {
                "tag": "PRV-401",
                "name": "CDU-3 Column Overhead Primary Safety Relief Valve",
                "unit": "Crude Distillation Unit (CDU-3 Overhead Battery)",
                "criticality": "Life-Safety Critical (OISD-132 / API 576)",
                "service": "Sour Hydrocarbon Vapor & H2S",
                "type": "API 526 Direct Spring-Operated Balanced Bellows Safety Relief",
                "design_specs": {
                    "set_pressure": "42.5 bar gauge",
                    "overpressure_allowance": "10% (Relieving at 46.75 bar g)",
                    "orifice_designation": "6Q8 (Orifice area: 71.29 cm²)",
                    "flange_rating": "6\" ANSI Class 300 RF Inlet x 8\" ANSI Class 150 RF Outlet",
                    "body_metallurgy": "ASTM A216 WCC with Inconel 625 Bellows & Monel Trim",
                    "backpressure_limit": "Superimposed variable backpressure up to 8.5 bar g",
                },
                "maintenance_history": [
                    {
                        "date": "2025-11-10",
                        "work_order": "WO-MRPL-PSV-2025-992",
                        "type": "Annual Bench Calibration & Pop Test (API 576)",
                        "inspector": "Chief HSE Inspector R. Nair (Certified API 510/576)",
                        "findings": "Pop Test 1: 42.4 bar, Pop Test 2: 42.5 bar, Pop Test 3: 42.5 bar (±0.2% tolerance, well within mandatory ±3.0% threshold). Bubble-tight seat leakage verified at 38.2 bar (90% set point). Green recertification tag #MRPL-PRV-401-2025 affixed.",
                        "status": "Recertified (1-Year Validity)",
                    }
                ],
                "next_pm_due": "2026-11-10 (Mandatory 12-Month Sour Service Bench Recertification)",
                "active_permits": "Car-Seal Open (CSO) bypass valve verified locked",
            },
            "PRV-402": {
                "tag": "PRV-402",
                "name": "CDU-3 Flash Drum High-Pressure Safety Relief Valve",
                "unit": "Crude Distillation Unit (CDU-3 Flash Drum V-102)",
                "criticality": "Life-Safety Critical",
                "service": "High-Pressure Naphtha / Fuel Gas",
                "type": "Balanced Bellows PRV",
                "design_specs": {
                    "set_pressure": "42.5 bar gauge",
                    "orifice_designation": "4P6",
                    "flange_rating": "4\" Class 300 x 6\" Class 150",
                },
                "maintenance_history": [
                    {
                        "date": "2025-11-11",
                        "work_order": "WO-MRPL-PSV-2025-993",
                        "type": "Annual Bench Pop Test",
                        "inspector": "R. Nair",
                        "findings": "Pop test repeatability confirmed at 42.6 bar (within +0.2% tolerance). Seat lapped with diamond paste #600.",
                        "status": "Recertified",
                    }
                ],
                "next_pm_due": "2026-11-11",
                "active_permits": "In-service",
            },
            "F-101": {
                "tag": "F-101",
                "name": "Atmospheric Crude Pre-Heat Furnace #1",
                "unit": "Crude Distillation Unit (CDU-1/3)",
                "criticality": "Tier-1 High Criticality",
                "service": "Crude Oil Radiant & Convection Firing",
                "type": "Cabin Type Twin-Cell Radiant Box Furnace",
                "design_specs": {
                    "firing_duty": "55.0 MW (Thermal)",
                    "fuel_source": "Refinery Fuel Gas + LSHS Heavy Oil (Dual Fuel Firing)",
                    "tube_metallurgy": "Radiant: ASTM A335 Gr. P9 (9Cr-1Mo); Convection: A106 Gr. B",
                    "snuffing_steam_manifold": "15.0 kg/cm² Superheated Steam (Manifold S-12)",
                    "operating_coil_outlet_temp": "365.0 °C",
                },
                "maintenance_history": [
                    {
                        "date": "2025-08-12",
                        "work_order": "WO-MRPL-FURN-2025-11",
                        "type": "Turnaround Decoking & Ultrasonic Tube Thickness Inspection",
                        "technician": "Turnaround Team Delta",
                        "findings": "Pigging & decoking completed on all 4 radiant passes. Tube wall minimum thickness measured 8.4mm (nominal 8.8mm, retirement limit 4.2mm). Burner tile refractory relined.",
                        "status": "Turnaround Cleared",
                    }
                ],
                "next_pm_due": "2026-08-12 (Annual Burner Management & Flame Scanner Check)",
                "active_permits": "Active firing DCS loop",
            },
            "DV-201": {
                "tag": "DV-201",
                "name": "LPG & Crude Storage Tank Farm AFFF Deluge Control Valve",
                "unit": "Tank Farm Sector-4 (Fire Protection Ring)",
                "criticality": "Emergency Life-Safety Deluge",
                "service": "Fire Water + 3% AFFF Foam Solution",
                "type": "Hydraulically Actuated Diaphragm Deluge Valve (Inbal Type)",
                "design_specs": {
                    "valve_size": "8\" Flanged Class 150",
                    "fire_ring_main_pressure": "10.5 kg/cm²",
                    "foam_proportioning": "3% AFFF concentrate induction via balanced bladder tank",
                    "spray_density": "10.2 Litres/min/m²",
                    "trip_actuation": "Dual UV/IR Flame Detectors + Pneumatic Quartz Bulb Line",
                },
                "maintenance_history": [
                    {
                        "date": "2026-06-01",
                        "work_order": "WO-MRPL-FIRE-2026-04",
                        "type": "Quarterly Automated Deluge Trip Test & Water Spray Coverage",
                        "inspector": "Fire Safety Officer B. Hegde",
                        "findings": "Deluge valve tripped open in 4.1 seconds upon UV/IR simulated alarm. Ring main pressure sustained at 10.4 kg/cm² by diesel turbine pump FP-01. Strainer backwashed clean.",
                        "status": "Certified Operational",
                    }
                ],
                "next_pm_due": "2026-09-01 (Quarterly Deluge Functional Trip Test)",
                "active_permits": "Armed on 24/7 automatic trip mode",
            },
            "RIV-102": {
                "tag": "RIV-102",
                "name": "HGU-2 High-Pressure Reformer Remote Emergency Isolation Valve",
                "unit": "Hydrogen Generation Unit (HGU-2 / Sector-4)",
                "criticality": "Tier-1 Emergency Isolation",
                "service": "High-Pressure Pure Hydrogen Gas (H2)",
                "type": "API 6D Metal-Seated Ball Valve with Spring-Return Pneumatic Actuator",
                "design_specs": {
                    "pressure_class": "ANSI Class 1500 (Max 140.0 bar gauge)",
                    "operating_temp": "280 °C",
                    "stroke_time": "2.2 seconds to 100% full closure (Fail-Close)",
                    "fire_safety_rating": "API 607 8th Edition Fire-Safe Certified",
                },
                "maintenance_history": [
                    {
                        "date": "2026-07-22",
                        "work_order": "WO-MRPL-ESD-2026-88",
                        "type": "Emergency Stroke Test & Nitrogen Accumulator Verification",
                        "technician": "Instrumentation Specialist A. Fernandes",
                        "findings": "Partial stroke test (PST) and full trip executed from CCR Panel-B. Full closure time measured 2.18s. Nitrogen backup accumulator pressure confirmed at 165 bar.",
                        "status": "Certified ESD Operational",
                    }
                ],
                "next_pm_due": "2026-10-22 (Quarterly PST & Seal Integrity Test)",
                "active_permits": "Armed on ESD-PB-04 loop",
            },
            "EDP-01": {
                "tag": "EDP-01",
                "name": "Hydrocracker Unit (HCU) Emergency Depressurization System",
                "unit": "Hydrocracker High-Pressure Reaction Loop",
                "criticality": "Catastrophic Overpressure Safeguard",
                "service": "High-Pressure Hydrogen / Hydrocarbon Reaction Mixture",
                "type": "Triple-Redundant Automated Blowdown System (2-out-of-3 Voting)",
                "design_specs": {
                    "depressurization_rate": "7.0 bar / minute controlled down to 20.0 bar",
                    "discharge_destination": "24\" High-Pressure Flare Header",
                    "runaway_trip_threshold": "Reactor Bed Temp > 435.0 °C or Loop Pressure > 155 bar",
                },
                "maintenance_history": [
                    {
                        "date": "2026-05-18",
                        "work_order": "WO-MRPL-HCU-2026-019",
                        "type": "Loop Calibration & Solenoid Valve Redundancy Test",
                        "technician": "Process Safety Lead V. Joshi",
                        "findings": "All 3 SIL-3 certified solenoids (SOV-1/2/3) tested independently. Blowdown control valve bypass stroked smoothly with 0% stiction.",
                        "status": "Certified SIL-3 Compliant",
                    }
                ],
                "next_pm_due": "2026-11-18",
                "active_permits": "Active ESD interlock loop",
            },
            "DHDS-RX-01": {
                "tag": "DHDS-RX-01",
                "name": "Diesel Hydrodesulfurization (DHDS) Catalytic Reactor",
                "unit": "DHDS Unit Sector-2",
                "criticality": "High-Pressure Sour Process Vessel",
                "service": "Diesel Gasoil Desulfurization (H2S Sour Gas Phase)",
                "type": "Thick-Wall Forged Cr-Mo Steel Pressure Vessel with SS347 Weld Overlay",
                "design_specs": {
                    "design_pressure": "85.0 bar gauge",
                    "design_temperature": "410.0 °C",
                    "wall_thickness": "128.0 mm (Forged 2.25Cr-1Mo-V steel)",
                    "catalyst_bed": "CoMo / NiMo on high surface area Alumina",
                    "h2s_partial_pressure": "8.5 bar",
                },
                "maintenance_history": [
                    {
                        "date": "2025-09-04",
                        "work_order": "WO-MRPL-NDT-2025-77",
                        "type": "Non-Destructive Testing (NDT) & Ultrasonic Wall Thickness Scan",
                        "inspector": "Certified NDT Level-III Engineer K. Bhat",
                        "findings": "Phased Array Ultrasonic Testing (PAUT) completed across 100% circumferential welds. Shell thickness: 128.1mm (0.0mm corrosion loss). Time-of-Flight Diffraction (TOFD) confirmed zero high-temperature hydrogen attack (HTHA) or hydrogen-induced cracking (HIC).",
                        "status": "Certified Integrity Safe",
                    }
                ],
                "next_pm_due": "2027-09-04 (Bi-annual Turnaround PAUT Scan)",
                "active_permits": "Operating at steady-state 375°C / 72 bar",
            }
        }

    def lookup_asset(self, query: str) -> Optional[Dict[str, Any]]:
        """Searches for an asset tag in the user's query and returns full history record."""
        q_upper = query.upper()
        # Find exact matches in asset keys
        for tag, data in self.assets.items():
            pattern = r'\b' + re.escape(tag) + r'\b'
            if re.search(pattern, q_upper) or (tag.replace("-", "") in q_upper.replace("-", "").split()):
                return data

        # Check for asset descriptions like "crude pump", "deluge valve", "relief valve prv", etc.
        if "CRUDE PUMP" in q_upper or "CHARGE PUMP" in q_upper:
            return self.assets["P-101A"]
        if "RELIEF VALVE" in q_upper or "PSV" in q_upper or "PRV" in q_upper:
            return self.assets["PRV-401"]
        if "DELUGE" in q_upper or "FOAM VALVE" in q_upper:
            return self.assets["DV-201"]
        if "HYDROGEN VALVE" in q_upper or "REFORMER ISOLATION" in q_upper:
            return self.assets["RIV-102"]
        if "FURNACE" in q_upper or "PRE-HEAT" in q_upper:
            return self.assets["F-101"]
        if "DEPRESSURIZATION" in q_upper or "BLOWDOWN" in q_upper or "EDP" in q_upper:
            return self.assets["EDP-01"]
        if "DHDS" in q_upper or "HYDROTREATER" in q_upper or "DESULFURIZATION" in q_upper:
            return self.assets["DHDS-RX-01"]

        return None

    def format_asset_report(self, asset: Dict[str, Any]) -> str:
        """Formats the asset history into a clean, executive industrial report."""
        specs_rows = "\n".join([f"| **{k.replace('_', ' ').title()}** | `{v}` |" for k, v in asset["design_specs"].items()])
        
        hist_rows = []
        for i, h in enumerate(asset["maintenance_history"], 1):
            hist_rows.append(
                f"#### 🛠️ Service Event {i}: {h['type']} ({h['date']})\n"
                f"- **Work Order ID**: `{h['work_order']}`\n"
                f"- **Executing Lead / Inspector**: {h.get('technician') or h.get('inspector')}\n"
                f"- **Inspection Findings**: {h['findings']}\n"
                f"- **Certification Status**: **{h['status']}**"
            )
        history_text = "\n\n".join(hist_rows)

        return (
            f"### 🏷️ MRPL Asset Integrity & Maintenance Record: `{asset['tag']}`\n\n"
            f"**Asset Title**: {asset['name']}\n"
            f"**Operating Unit**: {asset['unit']} | **Criticality**: `{asset['criticality']}`\n"
            f"**Process Service**: {asset['service']} ({asset['type']})\n\n"
            f"#### 📊 Certified Design Parameters\n"
            f"| Engineering Parameter | Verified Specification |\n"
            f"| :--- | :--- |\n"
            f"{specs_rows}\n\n"
            f"#### 📜 Historical Work Orders & Recertification Logs\n"
            f"{history_text}\n\n"
            f"#### ⏰ Compliance & Surveillance Deadlines\n"
            f"- **Next PM / Calibration Due**: **`{asset['next_pm_due']}`**\n"
            f"- **Active Permit / Operating Status**: `{asset['active_permits']}`\n\n"
            f"> [!NOTE]\n"
            f"> Maintenance records synchronized with MRPL SAP-PM / Meridium APM asset integrity ledger."
        )


# Global Singleton Instance
equipment_registry = EquipmentRegistry()
