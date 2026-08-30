import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_mrpl_safety_pdf(output_filename="MRPL_Refinery_Safety_SOP_2026.pdf"):
    doc = SimpleDocTemplate(output_filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor='#003366',
        spaceAfter=8
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor='#006699',
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        spaceAfter=6
    )

    story = []

    # Document Header
    story.append(Paragraph("MANGALORE REFINERY AND PETROCHEMICALS LIMITED (MRPL)", title_style))
    story.append(Paragraph("Comprehensive Refinery Safety Standard Operating Procedure (SOP) — 2026 Sovereign Edition", section_style))
    story.append(Paragraph("Document ID: MRPL-HSE-SOP-2026-V4 | Classification: Sovereign Operational Directive | Unit: All Refinery Units", body_style))
    story.append(Spacer(1, 8))

    # Section 1: CDU Emergency Shutdown
    story.append(Paragraph("1. Emergency Shutdown Procedure — Crude Distillation Unit (CDU-1, CDU-2 & CDU-3)", section_style))
    story.append(Paragraph(
        "<b>1.1 Trigger Conditions:</b> Emergency Shutdown (ESD) of the Crude Distillation Unit must be initiated immediately upon: "
        "(a) Major loss of electrical power grid (>5 seconds), (b) Furnace tube rupture or unconfined crude charge leak, "
        "(c) Loss of cooling water circulation to overhead condenser batteries, or (d) Uncontrolled runaway column pressure > 45.0 bar.",
        body_style
    ))
    story.append(Paragraph(
        "<b>1.2 Step-by-Step Shutdown Execution:</b><br/>"
        "1. Trip the Emergency Shutdown Push Button (ESD-PB-01) at the Central Control Room (CCR) main console or DCS graphics.<br/>"
        "2. Automated Emergency Block Valves (EBVs) on crude charge pumps P-101A/B will close within 3 seconds, isolating crude feed.<br/>"
        "3. Immediately shut fuel gas and fuel oil firing valves to Atmospheric Furnaces F-101 and F-102. Inject emergency snuffing steam (15 kg/cm²) into the furnace radiant section.<br/>"
        "4. Divert column overhead vapors to the High-Pressure Flare Header by opening flare bypass control valves FV-1044 and FV-1045.<br/>"
        "5. Start emergency stripping steam to column bottoms to prevent heavy oil coking and vacuum collapse.<br/>"
        "6. Establish nitrogen blanketing at 0.5 kg/cm² on column vessels and accumulator drums once system temperature drops below 200°C.",
        body_style
    ))

    # Section 2: H2S Exposure Limits and PPE
    story.append(Paragraph("2. Hydrogen Sulfide (H2S) Toxic Gas Safety & Permissible Exposure Limits", section_style))
    story.append(Paragraph(
        "<b>2.1 Exposure Limits & Thresholds:</b> Hydrogen Sulfide (H2S) is an extremely lethal, colorless gas with a rotten-egg odor at trace levels (odor fatigue occurs above 50 ppm). "
        "The mandatory MRPL exposure benchmarks comply with OISD-GDN-166 and OSHA:<br/>"
        "• <b>Permissible Exposure Limit (TWA 8-hr):</b> 10 ppm (14 mg/m³).<br/>"
        "• <b>Short Term Exposure Limit (STEL 15-min):</b> 15 ppm (21 mg/m³).<br/>"
        "• <b>Immediately Dangerous to Life or Health (IDLH):</b> 100 ppm.<br/>"
        "• <b>Instant Fatal Lethal Range:</b> > 500 ppm causes immediate pulmonary edema, neurological paralysis, and sudden cardiac arrest.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2.2 Mandatory PPE Requirements in Sour Gas & Hydrotreating Areas:</b><br/>"
        "1. Every operator entering Sector-2 (DHDS, VGO-HDT, Sulfur Recovery Unit) MUST wear a continuously active 4-gas personal detector set to alarm at 5 ppm (warning) and 10 ppm (evacuate).<br/>"
        "2. For line breaking, sampling, or maintenance where H2S > 10 ppm may be present, personnel MUST wear a Positive Pressure Self-Contained Breathing Apparatus (SCBA) with a 30-minute composite cylinder, or airline respirator with 10-minute escape bottle.<br/>"
        "3. Air-purifying canister/cartridge respirators are strictly prohibited for H2S concentrations above 10 ppm or in confined spaces.<br/>"
        "4. In the event of an H2S alarm, workers must immediately assemble cross-wind or up-wind at Designated Muster Point C-4.",
        body_style
    ))

    # Section 3: PSV Inspection & Recertification
    story.append(Paragraph("3. Pressure Safety Valve (PSV) and Pressure Relief Valve (PRV) Compliance", section_style))
    story.append(Paragraph(
        "<b>3.1 Testing Frequency & Certification Schedule:</b> All high-pressure safety relief valves (PSVs/PRVs) across MRPL must adhere to API 576 and OISD-132:<br/>"
        "• <b>High-Pressure Critical Service (> 30 bar, toxic/sour):</b> Mandatory inspection and bench test every <b>12 months (1 year)</b>.<br/>"
        "• <b>Clean Hydrocarbon Service & Atmospheric Service:</b> Inspection and recertification every <b>24 months (2 years)</b>.<br/>"
        "• <b>Thermal Relief Valves (TRVs):</b> Tested during scheduled unit turnarounds (maximum 36 months).",
        body_style
    ))
    story.append(Paragraph(
        "<b>3.2 PSV Operating and Pop Test Tolerances:</b><br/>"
        "1. CDU-3 Primary relief valves (PRV-401 to PRV-408) must be set to trigger at exactly 42.5 bar gauge.<br/>"
        "2. Set pressure tolerance: ± 3% for set pressures above 4.8 bar.<br/>"
        "3. Cold Differential Set Pressure (CDSP) must be verified on the test bench using dry nitrogen or hydraulic test bench with certified calibrated master gauges.<br/>"
        "4. Pop test must be performed 3 consecutive times to ensure repeatability and bubble-tight seat leakage compliance before installation.",
        body_style
    ))

    # Section 4: Hot Work Permit Zone 1
    story.append(Paragraph("4. Hot Work Permit Protocols in Hazardous Zones (Zone-1 & Zone-2)", section_style))
    story.append(Paragraph(
        "<b>4.1 Zone-1 Definition and Mandatory Prerequisites:</b> Zone-1 is an area in which an explosive hydrocarbon atmosphere is likely to occur in normal operation. "
        "No hot work (welding, cutting, grinding, torch operation, unrated power tools) is permitted without a valid Grade-A Hot Work Permit signed by the Shift In-Charge and Safety Officer.",
        body_style
    ))
    story.append(Paragraph(
        "<b>4.2 Step-by-Step Hot Work Execution Requirements:</b><br/>"
        "1. <b>Gas Testing (Continuous Monitoring):</b> The atmosphere at the job site and surrounding 15-meter radius must be tested for Lower Explosive Limit (LEL), Oxygen, H2S, and CO.<br/>"
        "• LEL must be <b>0.0%</b> to start hot work. Hot work is immediately cancelled if LEL exceeds <b>1.0%</b>.<br/>"
        "• Oxygen content must be strictly between <b>19.5% and 23.5%</b>.<br/>"
        "2. <b>15-Meter Radial Clearance:</b> All combustible materials, grease, hydrocarbons, and oily rags within 15 meters must be removed. All sewer pits, drains, and catch basins within 15 meters must be covered with fire-resistant rubber sheets and sealed with wet sand.<br/>"
        "3. <b>Fire Watch & Standby Equipment:</b> A dedicated certified Fire Watch must be present throughout the work duration with two 10kg DCP extinguishers and a charged 2.5-inch fire hose connected to the refinery fire water ring at 8.0 kg/cm² pressure.<br/>"
        "4. <b>Post-Work Watch:</b> Continuous fire watch must remain on site for a minimum of 30 minutes after completion of hot work to check for smoldering embers.",
        body_style
    ))

    # Section 5: Hydrocracker & Hydrogen Unit Safety
    story.append(Paragraph("5. Hydrocracker Unit (HCU) & Hydrogen Generation Unit (HGU-2) Protocols", section_style))
    story.append(Paragraph(
        "<b>5.1 Hydrogen Hazards & High-Pressure Circulation:</b> Hydrogen burns with an invisible flame in daylight and has a 4.0% - 75.0% explosive range in air with minimal ignition energy (0.02 mJ). "
        "Thermal imaging cameras must be deployed to detect flame fronts.<br/>"
        "<b>5.2 Emergency Depressurization (EDP-01):</b> In the event of a high-pressure reactor temperature runaway (> 435°C) or major high-pressure hydrogen leak (> 140 bar), the operator must activate the Emergency Depressurization System (EDP-01). "
        "EDP-01 depressurizes the reactor loop to the flare header at a controlled rate of 7.0 bar per minute down to 20 bar, preventing catastrophic vessel embrittlement and catastrophic rupture.",
        body_style
    ))

    # Section 6: Fire Protection & Deluge Systems
    story.append(Paragraph("6. Fire Protection, AFFF Deluge Systems & Hydrocarbon Firefighting", section_style))
    story.append(Paragraph(
        "<b>6.1 Fixed Deluge System Operation:</b> All crude and LPG storage tanks are protected by medium-velocity water spray and 3% Aqueous Film-Forming Foam (AFFF) deluge systems. "
        "Minimum deluge design density is 10.2 Litres/min/m² of vessel surface area.<br/>"
        "<b>6.2 Fire Alarm Response Protocol:</b> Upon activation of an automated hydrocarbon flame detector (UV/IR) or manual call point (MCP), the deluge control valve (DV-201) trips open automatically within 5 seconds. "
        "Refinery fire pump ring mains automatically maintain 10.5 kg/cm² pressure via three diesel-driven backup turbine pumps (FP-01/02/03).",
        body_style
    ))

    # Section 7: Confined Space Entry & Vessel Isolation
    story.append(Paragraph("7. Confined Space Entry & Positive Mechanical Isolation Protocol", section_style))
    story.append(Paragraph(
        "<b>7.1 Isolation and Gas Freeing:</b> Before entering any vessel, reactor, fractionator column, or storage tank, positive mechanical isolation via spectacle blind insertion at battery limits is mandatory. "
        "Closing isolation valves alone without physical blinds or verified double-block-and-bleed is strictly prohibited under OISD-STD-105.<br/>"
        "<b>7.2 Entry Conditions:</b> (a) Oxygen: strictly 19.5% - 23.5%, (b) LEL: 0.0%, (c) Toxic gases (H2S < 5 ppm, CO < 25 ppm, Benzene < 0.5 ppm, SO2 < 2 ppm). "
        "A trained standby attendant must maintain continuous verbal and visual contact at the manhole entrance with emergency rescue winch gear.",
        body_style
    ))

    # Section 8: Electrical Lockout / Tagout (LOTO)
    story.append(Paragraph("8. Electrical Isolation & Lockout / Tagout (LOTO) Standard", section_style))
    story.append(Paragraph(
        "All mechanical and instrument maintenance on motorized machinery (pumps, compressors, blowers, fin fans) requires an authorized LOTO certificate. "
        "The Electrical Engineer must rack out the circuit breaker at the Substation 415V/6.6kV/11kV switchgear, perform live-dead-live zero voltage verification using a calibrated proximity detector, "
        "apply an individual red padlock with a unique key, and secure the danger tag bearing the technician name, work permit number, and date. "
        "Master keys must remain locked in the personal possession of the executing engineer until completion testing.",
        body_style
    ))

    # Section 9: Chemical Hazard Management & Spill Containment
    story.append(Paragraph("9. Chemical Hazard Management & Neutralization Directives", section_style))
    story.append(Paragraph(
        "<b>9.1 Caustic Soda (NaOH 50%) & Sulfuric Acid (H2SO4 98%) Protocols:</b> Storage areas must be surrounded by acid/alkali resistant dyke walls with a minimum 110% containment capacity of the largest storage vessel.<br/>"
        "• For acid spills: Neutralize immediately with sodium bicarbonate or agricultural lime until pH stabilizes between 6.5 and 8.5 before transferring to the Effluent Treatment Plant (ETP).<br/>"
        "• For caustic spills: Dilute with copiously flushed potable water and neutralize with weak acetic acid or citric acid solution.<br/>"
        "• Emergency eyewash and deluge safety showers must be tested daily and be reachable within 10 seconds (max 15 meters) from any chemical handling point.",
        body_style
    ))

    # Section 10: Shift Handover & Safety Directives
    story.append(Paragraph("10. Shift Handover, Critical Alarm Log & General Safety Directives", section_style))
    story.append(Paragraph(
        "<b>10.1 Shift Handover Compliance:</b> Formal shift handover must adhere to OSHA 1910.119 Process Safety Management standards. "
        "The outgoing Shift Supervisor must log: (a) All active work permits and hot work zones, (b) Bypassed or overridden ESD interlocks and safety trips, "
        "(c) Equipment running under maintenance deviation, and (d) Product quality tank line-ups.<br/>"
        "<b>10.2 Fall Protection & Scaffolding:</b> 100% tie-off using a dual-lanyard full-body safety harness with shock absorber is mandatory when working at heights exceeding 1.8 meters (6 feet). "
        "All scaffolding must carry a valid Green Tag signed by a certified scaffolding inspector before access.",
        body_style
    ))

    doc.build(story)
    print(f"Successfully generated comprehensive MRPL PDF manual: {output_filename}")

if __name__ == "__main__":
    generate_mrpl_safety_pdf()
