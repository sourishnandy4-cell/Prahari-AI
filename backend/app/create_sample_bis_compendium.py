import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_bis_compendium_pdf(output_filename="Indian_Standards_BIS_Compendium_2026.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor='#1a365d',
        spaceAfter=8
    )

    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor='#2b6cb0',
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        spaceAfter=5
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("BUREAU OF INDIAN STANDARDS (BIS)", title_style))
    story.append(Paragraph("National Compendium of Indian Standards, Certification Schemes, and Consumer Guidance — 2026 Edition", section_style))
    story.append(Paragraph("Document ID: BIS-QCO-MANAK-2026-V1 | Regulatory Authority: Ministry of Consumer Affairs, Food & Public Distribution | Classification: Official Technical Standard", body_style))
    story.append(Spacer(1, 10))

    # Chapter 1: BIS Act & Schemes
    story.append(Paragraph("1. Statutory Framework and Conformity Assessment Schemes", section_style))
    story.append(Paragraph(
        "<b>1.1 Statutory Authority:</b> Established under the Bureau of Indian Standards Act 2016, BIS is the National Standards Body of India responsible for the harmonious development of standardisation, marking, and quality certification of goods.<br/>"
        "<b>1.2 Scheme-I (Product Certification / ISI Mark):</b> Governed by BIS (Conformity Assessment) Regulations 2018. Applicable to physical consumer and industrial goods (cements, steel, electrical appliances, helmets, water, toys). Requires both factory infrastructure audit, in-house laboratory inspection, and independent sample testing in BIS labs. Successful applicants receive a Grant of Licence (GoL) and a 7-digit CM/L license number.<br/>"
        "<b>1.3 Scheme-II (Compulsory Registration Scheme - CRS):</b> Administered in collaboration with MeitY for electronics, IT equipment, solar inverters, and lithium-ion batteries. Manufacturers submit test reports from BIS-recognized labs to obtain an 8-digit R-number (Registration No.) without preliminary factory audit.<br/>"
        "<b>1.4 Scheme-IV (Foreign Manufacturers Certification Scheme - FMCS):</b> Dedicated certification scheme permitting overseas manufacturers to use the ISI Mark on goods exported into India, subject to overseas factory inspection and clearance.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Chapter 2: Water Standards
    story.append(Paragraph("2. Indian Standards for Water Safety: IS 10500:2012 vs IS 14543:2004", section_style))
    story.append(Paragraph(
        "<b>2.1 IS 10500:2012 (Drinking Water Specification):</b> Prescribes requirements for piped municipal drinking water and groundwater supplies.<br/>"
        "• <i>Clause 4.2 & Table 1:</i> Turbidity acceptable max 1 NTU (permissible 5 NTU in absence of alternate source); pH 6.5 to 8.5; Total Dissolved Solids (TDS) max 500 mg/L (permissible 2000 mg/L); Total Hardness max 200 mg/L (permissible 600 mg/L).<br/>"
        "• <i>Clause 4.4 & Table 3:</i> Heavy metals: Lead max 0.01 mg/L, Arsenic max 0.01 mg/L, Cadmium max 0.003 mg/L, Mercury max 0.001 mg/L.<br/>"
        "• <i>Clause 5.1 & Table 6:</i> Bacteriological Quality: E. coli or thermotolerant coliforms shall not be detectable in any 100 ml sample.<br/>"
        "<b>2.2 IS 14543:2004 (Packaged Drinking Water):</b> Mandatory under Food Safety and Standards Regulations and BIS Quality Control Orders for all commercially bottled/packaged water.<br/>"
        "• <i>Clause 4.1 & Table 1:</i> TDS strictly between 75 mg/L and 500 mg/L; Turbidity max 2 NTU.<br/>"
        "• <i>Clause 5.1 & Table 2:</i> Microorganisms: Aerobic microbial count at 37°C <= 100 CFU/ml; E. coli, Coliform, Faecal Streptococci, Pseudomonas aeruginosa, and Yeast/Mould must be completely Absent in 250 ml.<br/>"
        "• <i>Pesticide Residues (Clause 5.3):</i> Individual pesticide max 0.0001 mg/L, total pesticides max 0.0005 mg/L.<br/>"
        "• <i>Clause 8.1 (Marking):</i> Product package must bear the ISI Mark, IS 14543, and unique 7-digit CML Number.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Chapter 3: Electrical Safety
    story.append(Paragraph("3. Electrical Safety Standards: IS 1293:2019 & IS 694:2010", section_style))
    story.append(Paragraph(
        "<b>3.1 IS 1293:2019 (Plugs and Socket-Outlets up to 16A at 250V):</b> Mandatory under Electrical Accessories QCO.<br/>"
        "• <i>Clause 8.1:</i> Standard ratings: 2.5A, 6A (Type D 3-pin round), and 16A (Type M large 3-pin round) at 250V AC 50Hz.<br/>"
        "• <i>Clause 10.5:</i> Domestic socket-outlets must incorporate child-safety shutters that only open upon simultaneous live/neutral insertion or earth pin entry.<br/>"
        "• <i>Clause 14.1 & 19.1:</i> Insulation resistance >= 5 MΩ at 500V DC; Dielectric strength 2000V AC for 1 min; Temperature rise <= 45 K under 1.1x rated current.<br/>"
        "• <i>Clause 20.1:</i> Mechanical endurance: 5,000 cycles insertion/withdrawal at rated load.<br/>"
        "<b>3.2 IS 694:2010 (PVC Insulated Cables for Working Voltages up to 1100V):</b> Mandatory for building wiring.<br/>"
        "• <i>Clause 5.1 & 6.1:</i> Electrolytic copper (IS 8130) or Grade EC aluminium conductor insulated with Type A / FR / FRLS PVC compound.<br/>"
        "• <i>Clause 13.1:</i> Conductor resistance: 1.5 sq mm copper <= 12.1 Ω/km; 2.5 sq mm <= 7.41 Ω/km at 20°C.<br/>"
        "• <i>Clause 14.1 & 16.1:</i> High voltage spark test at 6 kV AC; FRLS Oxygen Index >= 29%, smoke density transmittance >= 40%.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Chapter 4: Steel & Construction
    story.append(Paragraph("4. Construction Infrastructure Standards: IS 1786:2008 & IS 269:2015", section_style))
    story.append(Paragraph(
        "<b>4.1 IS 1786:2008 (High Strength Deformed Steel Bars - TMT Rebars):</b> Mandatory under Steel QCO.<br/>"
        "• <i>Clause 4.1 & Table 1:</i> Chemical limits for Fe 500D: Carbon max 0.25%, Sulphur max 0.040%, Phosphorus max 0.040%, S+P max 0.075%, Carbon Equivalent (CE) max 0.42%.<br/>"
        "• <i>Clause 8.1 & Table 2:</i> Mechanical properties for Fe 500D: 0.2% Proof Stress min 500 MPa, Tensile strength min 565 MPa, TS/YS ratio >= 1.10, Elongation min 16.0%, Total elongation at max force >= 5%.<br/>"
        "• <i>Clause 9.1 & 12.1:</i> 180° Cold bend and 157.5° rebend tests without fracture. Continuous rolling brand mark with 'IS 1786' and grade.<br/>"
        "<b>4.2 IS 269:2015 (Ordinary Portland Cement - OPC 33, 43, 53 Grade):</b> Mandatory under Cement QCO.<br/>"
        "• <i>Clause 6.1 & Table 2:</i> Blaine Fineness >= 225 m²/kg; Initial setting time min 30 min, Final setting time max 600 min; Soundness: Le-Chatelier expansion max 10 mm, Autoclave max 0.8%.<br/>"
        "• <i>Clause 6.2 (Compressive Strength):</i> 53 Grade: 3-day >= 27 MPa, 7-day >= 37 MPa, 28-day >= 53 MPa.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Chapter 5: Personal & Consumer Safety
    story.append(Paragraph("5. Personal and Child Safety: Helmets, Cookers, Toys, and Electronics", section_style))
    story.append(Paragraph(
        "<b>5.1 IS 4151:2015 (Protective Helmets for Two Wheeler Riders):</b> Mandatory under MoRTH QCO.<br/>"
        "• Maximum mass <= 1.2 kg (1200 g); Peak headform impact deceleration <= 300g at 7.5 m/s drop speed; 3 kg steel cone penetration test; Chinstrap retention displacement <= 35 mm under 1 kN load.<br/>"
        "<b>5.2 IS 2347:2017 (Domestic Pressure Cookers):</b> Mandatory under DPIIT QCO.<br/>"
        "• Food-grade aluminium alloy or SS304; Normal operating pressure 0.5 to 1.1 bar; Hydrostatic proof pressure test at 3.0 times operating pressure without rupture; Safety valve/plug must relieve excess pressure safely downwards.<br/>"
        "<b>5.3 IS 9873 (Parts 1-9) (Safety of Toys):</b> Strictly Mandatory under Toys QCO.<br/>"
        "• Small parts choking test (31.7 mm cylinder) for children under 3 years; Sharp points/edges test; Heavy metals migration limits (Part 3): Lead max 90 mg/kg, Cadmium max 75 mg/kg, Arsenic max 25 mg/kg.<br/>"
        "<b>5.4 Electronics under CRS:</b> IS 13252:2010 (IT Equipment Safety), IS 16046:2018 (Lithium-ion Batteries - 130°C thermal abuse and crush tests), IS 15885:2012 (LED Drivers).",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Chapter 6: Gold Hallmarking
    story.append(Paragraph("6. Precious Metals: Mandatory Gold Hallmarking (IS 1417:2016)", section_style))
    story.append(Paragraph(
        "<b>6.1 Legal Mandate:</b> Mandatory across all notified districts of India under BIS Hallmarking Regulations 2018.<br/>"
        "<b>6.2 Mandatory 3-Part Hallmark Symbols:</b><br/>"
        "1. <b>BIS Triangular Crest Logo</b>: Official seal of Bureau of Indian Standards.<br/>"
        "2. <b>Purity in Karat and Fineness</b>: 22K916 (91.6% gold), 18K750 (75.0% gold), 14K585 (58.5% gold), or 24K999 (99.9% gold bullion).<br/>"
        "3. <b>6-Digit Alphanumeric HUID (Hallmark Unique Identification)</b>: Unique computerized laser mark (e.g. AB1234) providing complete digital traceability.<br/>"
        "<b>6.3 Consumer Verification via BIS Care App:</b> Consumers can enter the 6-digit HUID in the BIS Care App to instantly view the Jeweller Name, Hallmarking Centre (AHC) details, Date of Hallmarking, Article Type, and Declared Purity.<br/>"
        "<b>6.4 Consumer Compensation Policy:</b> If tested purity is lower than marked, the jeweller is legally required to refund the value difference plus pay twice the testing fee to the consumer.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Chapter 7: Certification Procedure & Documents
    story.append(Paragraph("7. Step-by-Step Licensing Procedure & Documents Required (MANAK Online)", section_style))
    story.append(Paragraph(
        "<b>7.1 Six-Step Licensing Roadmap (Scheme-I):</b><br/>"
        "1. Standard Identification & In-house Laboratory Setup conforming to Scheme of Inspection and Testing (SIT).<br/>"
        "2. Online Application on MANAK Online (manakonline.in) with Form-V, plant layout, machinery list, and application fee.<br/>"
        "3. Preliminary Factory Audit by BIS Technical Auditor verifying manufacturing machinery, QC systems, and test calibration.<br/>"
        "4. Sample Drawing & Testing: One sample tested in factory lab, counter-sample tested at NABL/BIS accredited laboratory.<br/>"
        "5. Grant of Licence (GoL) and allocation of 7-digit CM/L number upon satisfactory test reports.<br/>"
        "6. Regular Post-Licence Surveillance: Surprise factory audits and market surveillance sample draws.<br/>"
        "<b>7.2 Mandatory Document Checklist:</b> (1) Factory Registration / Incorporation Certificate (GST/MSME/RoC), (2) Manufacturing Process Flow Chart, (3) Machinery List with capacities, (4) Testing Equipment List with valid calibration certificates, (5) Factory Layout Plan, (6) Authorized Signatory nomination, (7) Independent Test Report from BIS recognized lab, (8) Acceptance of Scheme of Inspection and Testing (SIT).",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Chapter 8: Consumer Redressal & Contacts
    story.append(Paragraph("8. Consumer Grievance Redressal and Official BIS Channels", section_style))
    story.append(Paragraph(
        "<b>8.1 Filing Complaints:</b> Consumers encountering substandard ISI products or fake hallmarking can lodge grievances via: (a) 'BIS Care App' (Complaints section with photo/bill upload), (b) Web Portal www.bis.gov.in, (c) Email complaints@bis.gov.in, or (d) National Consumer Helpline 1915.<br/>"
        "<b>8.2 Enforcement & Raids:</b> BIS conducts surprise search and seizure operations under Section 29 of the BIS Act 2016 against manufacturers using fake ISI or unhallmarked gold. Violators face imprisonment up to 2 years and heavy fines.<br/>"
        "<b>8.3 Official Contact Details:</b><br/>"
        "• National Toll-Free Helpline: 1800-11-1255 / 1915<br/>"
        "• Headquarters: Manak Bhavan, 9 Bahadur Shah Zafar Marg, New Delhi 110002<br/>"
        "• Official Portals: www.bis.gov.in | www.manakonline.in",
        body_style
    ))

    doc.build(story)
    print(f"[BIS Compendium] Successfully generated: {output_filename}")
    return output_filename

if __name__ == "__main__":
    generate_bis_compendium_pdf()
