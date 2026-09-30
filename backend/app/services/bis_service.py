import re
from typing import Dict, Any, List, Optional

# ==============================================================================
# 🇮🇳 BIS & INDIAN STANDARDS (IS CODES) SOVEREIGN KNOWLEDGE BASE
# SIH Topic 26107: Virtual Assistant for Indian Standards & BIS Schemes
# ==============================================================================

STANDARDS_CATALOG = {
    # ── FOOD & WATER SAFETY ───────────────────────────────────────────────────
    "IS 10500:2012": {
        "standard_number": "IS 10500:2012",
        "title": "Drinking Water — Specification (Second Revision)",
        "category": "Food & Public Health",
        "scope": "Prescribes requirements and methods of sampling and test for drinking water (piped municipal water, tap water, ground water).",
        "mandatory_qco": "Mandatory for piped drinking water and commercial supply under Central/State Quality Orders.",
        "key_clauses": {
            "Clause 4.1": "General Requirements: Drinking water shall be free from microscopic organisms like algae, zooplankton, and flagellates.",
            "Clause 4.2 & Table 1": "Organoleptic and Physical Parameters: Turbidity (Max 1 NTU, permissible 5 NTU in absence of alternate source), pH (6.5 to 8.5), Total Dissolved Solids / TDS (Max 500 mg/L, permissible 2000 mg/L), Total Hardness as CaCO3 (Max 200 mg/L, permissible 600 mg/L).",
            "Clause 4.3 & Table 2": "Chemical Parameters (General Health): Chlorides (Max 250 mg/L, perm 1000 mg/L), Sulphates (Max 200 mg/L, perm 400 mg/L), Nitrate as NO3 (Max 45 mg/L, no relaxation), Fluoride (Max 1.0 mg/L, perm 1.5 mg/L).",
            "Clause 4.4 & Table 3": "Toxic Substances: Lead (Max 0.01 mg/L), Arsenic (Max 0.01 mg/L, perm 0.05 mg/L), Cadmium (Max 0.003 mg/L), Mercury (Max 0.001 mg/L), Total Chromium (Max 0.05 mg/L).",
            "Clause 5.1 & Table 6": "Bacteriological Quality: E. coli or thermotolerant coliform bacteria shall not be detectable in any 100 ml sample.",
        },
        "mandatory_tests": [
            "pH value test (Electrometric method)",
            "Turbidity measurement (Nephelometric method)",
            "Total Dissolved Solids (TDS) gravimetric test at 180°C",
            "Heavy metals analysis (ICP-MS or AAS for Pb, As, Cd, Hg)",
            "Microbiological examination (Membrane Filtration / MPN for E. coli & Coliforms)"
        ],
        "certification_scheme": "Scheme-I (ISI Mark)",
        "hindi_summary": "पेयजल विनिर्देश (दूसरा संशोधन) - टीडीएस स्वीकार्य सीमा 500 मिलीग्राम/लीटर (अधिकतम 2000 मिलीग्राम/लीटर), पीएच 6.5 से 8.5, ई. कोलाई शून्य होना अनिवार्य।"
    },

    "IS 14543:2004": {
        "standard_number": "IS 14543:2004",
        "title": "Packaged Drinking Water (Other than Packaged Natural Mineral Water) — Specification",
        "category": "Packaged Food & Beverages",
        "scope": "Applies to water derived from any potable water source subjected to treatment (filtration, aeration, demineralization, reverse osmosis, UV disinfection, ozonisation) and packaged in sealed containers/pouches/bottles.",
        "mandatory_qco": "Strictly Mandatory under Food Safety and Standards (Packaging) Regulations & BIS Quality Control Order. Unlawful to sell without ISI mark.",
        "key_clauses": {
            "Clause 3.2": "Treatment Process: The water must undergo disinfection (ozonation, UV radiation) and demineralization/RO ensuring pathogen inactivation.",
            "Clause 4.1 & Table 1": "Physical/Chemical Characteristics: TDS (between 75 mg/L and 500 mg/L), Turbidity (Max 2 NTU), Total Hardness (Max 200 mg/L).",
            "Clause 4.2": "Minerals Addition: When minerals are added, they shall be of food grade and within prescribed limits (Calcium max 75 mg/L, Magnesium max 30 mg/L).",
            "Clause 5.1 & Table 2": "Microbiological Requirements: Aerobic microbial count at 37°C shall not exceed 100 CFU/ml and at 20-22°C shall not exceed 20 CFU/ml. E. coli, Coliform, Faecal Streptococci, Pseudomonas aeruginosa, and Yeast/Mould must be completely Absent in 250 ml.",
            "Clause 7.1": "Packaging: In food grade PET bottles (IS 12252), polycarbonates, or pouches conforming to IS 15609.",
            "Clause 8.1": "Labelling & Marking: Mandatory ISI Mark with Standard Number 'IS 14543' above logo and 7-digit CML Number below logo, Batch No, Date of Packaging, Best Before date.",
        },
        "mandatory_tests": [
            "Microbial Sterility: Pseudomonas aeruginosa, Coliform, E. coli, Faecal Streptococci",
            "Pesticide Residue Analysis: Individual pesticide max 0.0001 mg/L, Total pesticides max 0.0005 mg/L (GC-MS/MS test)",
            "Container Migration Test: Overall migration test for plastic packaging",
            "Chemical Purity: Nitrate, Nitrite, Fluoride, Heavy Metals (Pb, As, Cd, Hg)"
        ],
        "certification_scheme": "Scheme-I (ISI Mark) - Mandatory QCO",
        "hindi_summary": "पैकेज्ड पेयजल विनिर्देश - बिक्री हेतु आईएसआई मार्क अनिवार्य। कीटनाशक अवशेष अधिकतम 0.0001 mg/L, स्यूडोमोनास एवं ई. कोलाई शून्य होना अनिवार्य।"
    },

    "IS 13428:2005": {
        "standard_number": "IS 13428:2005",
        "title": "Packaged Natural Mineral Water — Specification",
        "category": "Packaged Food & Beverages",
        "scope": "Applies to natural spring water or underground water containing mineral salts obtained directly from natural or drilled sources under sanitary conditions.",
        "mandatory_qco": "Strictly Mandatory under FSSAI and BIS QCO. Cannot undergo chemical demineralization (only physical filtration permitted).",
        "key_clauses": {
            "Clause 3.1": "Natural Source Protection: Must be packaged close to source point without chemical modification.",
            "Clause 4.1": "Natural Mineral Content: Must maintain inherent mineral composition throughout shelf life.",
            "Clause 5.2": "Microbiological safety: Free from pathogenic microbes, parasites, and faecal contaminants."
        },
        "mandatory_tests": ["Natural mineral profiling", "Pesticide residues", "Microbiological purity", "Heavy metals"],
        "certification_scheme": "Scheme-I (ISI Mark)",
        "hindi_summary": "प्राकृतिक खनिज जल विनिर्देश - केवल प्राकृतिक स्रोतों से प्राप्त, रासायनिक शोधन वर्जित, आईएसआई प्रमाणीकरण अनिवार्य।"
    },

    # ── ELECTRICAL & ELECTRONICS ──────────────────────────────────────────────
    "IS 1293:2019": {
        "standard_number": "IS 1293:2019",
        "title": "Plugs and Socket-Outlets for Domestic and Similar Purposes of Rated Voltage up to & including 250V and Rated Current up to & including 16A",
        "category": "Electrical Accessories",
        "scope": "Applies to plugs and fixed or portable socket-outlets for a.c. only, with or without earthing contact, rated from 2.5A up to 16A at 250V.",
        "mandatory_qco": "Mandatory under Electrical Wires, Cable, Appliances and Protection Devices (QCO) issued by DPIIT.",
        "key_clauses": {
            "Clause 8.1": "Standard Ratings: Rated currents 2.5A (Type C5 Euro-style), 6A (Type D 3-pin round), and 16A (Type M large 3-pin round). Rated voltage 250V AC 50Hz.",
            "Clause 9.1": "Classification: Classified by protection against electric shock, degree of protection (IP code), and earthing provision.",
            "Clause 10.1": "Marking Requirements: Rated current (A), rated voltage (V), symbol for nature of supply (~), manufacturer name/trademark, and BIS Certification Mark (ISI Mark).",
            "Clause 13.1": "Resistance to Aging, Humid Conditions, and Ingress: Must withstand 7 days aging at 70°C followed by humidity test.",
            "Clause 14.1": "Insulation Resistance & Electric Strength: Insulation resistance >= 5 MΩ at 500V DC. Dielectric withstand 2000V AC for 1 minute.",
            "Clause 19.1": "Temperature Rise Test: Terminals temperature rise shall not exceed 45 K under 1.1 times rated continuous current.",
            "Clause 20.1": "Breaking Capacity & Normal Operation: Plug inserted and withdrawn 5,000 times at rated voltage and current without contact degradation.",
        },
        "mandatory_tests": [
            "Insulation Resistance & High Voltage Dielectric Withstand Test",
            "Temperature Rise Test under continuous electrical load",
            "Mechanical Endurance: 5,000 insertion/withdrawal cycles test",
            "Glow Wire Test at 650°C and 750°C for fire resistance",
            "Ball Pressure Test for thermoplastic deformation at 125°C"
        ],
        "certification_scheme": "Scheme-I (ISI Mark) - Mandatory QCO",
        "hindi_summary": "प्लग और सॉकेट आउटलेट विनिर्देश (250V, 16A तक) - डीपीआईआईटी क्यूसीओ के तहत अनिवार्य। 5000 साइकिल इन्सर्शन टेस्ट एवं 45 K तापमान वृद्धि सीमा।"
    },

    "IS 694:2010": {
        "standard_number": "IS 694:2010",
        "title": "Polyvinyl Chloride Insulated Unshead and Sheathed Cables/Cords with Rigid and Flexible Conductor for Working Voltages up to and Including 1100 V",
        "category": "Electrical Cables & Wires",
        "scope": "Applies to single-core and multi-core PVC insulated copper and aluminium electrical building wires and flexible industrial cords.",
        "mandatory_qco": "Mandatory under Electrical Cables QCO. Selling non-ISI building wires is punishable by law.",
        "key_clauses": {
            "Clause 5.1": "Conductor Material: High-conductivity plain annealed electrolytic copper (IS 8130) or Grade EC aluminium.",
            "Clause 6.1": "Insulation: PVC compound Type A conforming to IS 5831 for general service, or FR (Flame Retardant) / FRLS (Flame Retardant Low Smoke).",
            "Clause 13.1": "Conductor Resistance: Maximum electrical resistance in Ω/km at 20°C as per conductor cross-sectional area (e.g., 1.5 sq mm Cu <= 12.1 Ω/km, 2.5 sq mm <= 7.41 Ω/km).",
            "Clause 14.1": "High Voltage Spark Test: Online spark testing at up to 6 kV AC or 10 kV DC to guarantee zero pinholes.",
            "Clause 16.1": "Oxygen Index and Smoke Density (FRLS Cables): Critical Oxygen Index >= 29% (ASTM D2863), Light transmittance >= 40% (IS 13360).",
        },
        "mandatory_tests": [
            "Conductor Resistance test using Kelvin Double Bridge",
            "Insulation Resistance at 20°C and 70°C",
            "Tensile Strength & Elongation at break of PVC before and after thermal aging",
            "Hot Set Test and Loss of Mass Test",
            "Flammability / Flame Retardance Test"
        ],
        "certification_scheme": "Scheme-I (ISI Mark) - Mandatory QCO",
        "hindi_summary": "1100V तक पीवीसी इंसुलेटेड केबल/वायर - घरेलू वायरिंग के लिए अनिवार्य आईएसआई मार्क। तांबा कंडक्टर प्रतिरोध एवं अग्निरोधी (FRLS) परीक्षण।"
    },

    "IS 302-1:2008": {
        "standard_number": "IS 302-1:2008",
        "title": "Safety of Household and Similar Electrical Appliances — Part 1: General Requirements",
        "category": "Consumer Electrical Appliances",
        "scope": "General safety requirements for domestic electrical appliances (electric irons IS 302-2-3, water heaters/geysers IS 302-2-21, mixers/grinders IS 302-2-14, immersion heaters IS 302-2-201).",
        "mandatory_qco": "Mandatory under Household Electrical Appliances (Quality Control) Order.",
        "key_clauses": {
            "Clause 8.1": "Protection Against Access to Live Parts: Test finger and test pin inspection to prevent shock.",
            "Clause 13.1": "Leakage Current and Electric Strength at Operating Temperature: Leakage current <= 0.75 mA for Class I portable appliances; 1250V AC dielectric test.",
            "Clause 19.1": "Abnormal Operation: Appliance shall not ignite, emit molten metal, or exceed safety temperature limits when operated without water/liquid or stalled.",
            "Clause 22.1": "Construction & Earthing: Class I appliances must have reliable earthing terminal with resistance <= 0.1 Ω.",
        },
        "mandatory_tests": ["Leakage current test", "High voltage dielectric test", "Abnormal operation test", "Drop/impact test", "Creepage & clearance distances"],
        "certification_scheme": "Scheme-I (ISI Mark) - Mandatory QCO",
        "hindi_summary": "घरेलू विद्युत उपकरण सुरक्षा - सामान्य आवश्यकताएं। अर्थिंग प्रतिरोध 0.1 ओम से कम, असामान्य संचालन में आग या पिघलने से बचाव अनिवार्य।"
    },

    "IS 13252 (Part 1):2010": {
        "standard_number": "IS 13252 (Part 1):2010 / IEC 60950-1",
        "title": "Information Technology Equipment — Safety — Part 1: General Requirements",
        "category": "Electronics & IT Goods",
        "scope": "Covers laptops, desktop PCs, servers, tablets, power adapters, printers, scanners, mobile phone chargers.",
        "mandatory_qco": "Mandatory under MeitY Electronics & IT Goods (Compulsory Registration Scheme - CRS / Scheme-II).",
        "key_clauses": {
            "Clause 1.5": "Components: Safety critical components (capacitors, varistors, transformers, optocouplers) must meet applicable standards.",
            "Clause 2.1": "Protection from Shock and Energy Hazards: Operator access areas must have double/reinforced insulation against hazardous voltages (>42.4V peak or 60V DC).",
            "Clause 4.2": "Mechanical Strength: 0.5J impact test and 10N steady force test on enclosures.",
            "Clause 5.2": "Electric Strength Test: Primary to secondary insulation withstands 3000V AC rms.",
        },
        "mandatory_tests": [
            "Dielectric Strength / Hi-Pot Test",
            "Touch Current / Protective Earth Resistance",
            "Heating / Thermal Temperature Rise under full load",
            "Drop test from 1 meter height onto concrete floor",
            "Fault condition testing (short-circuiting output capacitors)"
        ],
        "certification_scheme": "Scheme-II (CRS - Compulsory Registration Scheme)",
        "hindi_summary": "सूचना प्रौद्योगिकी उपकरण सुरक्षा - इलेक्ट्रॉनिक्स एवं आईटी मंत्रालय (MeitY) अनिवार्य पंजीकरण योजना (CRS) के तहत पंजीकृत होना अनिवार्य।"
    },

    "IS 16046 (Part 1 & 2):2018": {
        "standard_number": "IS 16046:2018 / IEC 62133",
        "title": "Secondary Cells and Batteries Containing Alkaline or Other Non-Acid Electrolytes (Lithium-ion Cells & Battery Packs)",
        "category": "Electronics & Energy Storage",
        "scope": "Applies to lithium-ion rechargeable battery packs and cells used in smartphones, laptops, power banks, tablets, and portable electronic equipment.",
        "mandatory_qco": "Mandatory under MeitY Compulsory Registration Scheme (CRS).",
        "key_clauses": {
            "Clause 7.2.1": "Continuous Charging at Constant Voltage: Safe charging for 7 days without leakage or venting.",
            "Clause 7.3.1": "External Short Circuit Test: Short circuit at 55°C without fire or explosion.",
            "Clause 7.3.2": "Free Fall / Drop Test: Drop from 1m height onto hardwood floor 3 times.",
            "Clause 7.3.3": "Thermal Abuse: Exposed to 130°C for 10 minutes in oven without exploding.",
            "Clause 7.3.4": "Crush Test: Hydraulic crushing up to 13 kN force without explosion.",
            "Clause 7.3.6": "Overcharge Test: 2.5 times maximum charge current without fire.",
        },
        "mandatory_tests": [
            "External Short-Circuit Test at ambient and 55°C",
            "Thermal Shock and Abuse Test at 130°C",
            "Mechanical Crush and Impact Test",
            "Overcharge and Forced Discharge Safety Test"
        ],
        "certification_scheme": "Scheme-II (CRS) - Compulsory Registration",
        "hindi_summary": "लिथियम-आयन बैटरी एवं सेल सुरक्षा - 130°C थर्मल टेस्ट, क्रश टेस्ट और ओवरचार्ज सुरक्षा परीक्षण अनिवार्य। MeitY CRS रजिस्ट्रेशन आवश्यक।"
    },

    "IS 15885 (Part 2/Sec 13):2012": {
        "standard_number": "IS 15885 (Part 2/Sec 13):2012 / IEC 61347-2-13",
        "title": "Lamp Controlgear — Part 2: Particular Requirements — Section 13: DC or AC Supplied Electronic Controlgear for LED Modules (LED Drivers)",
        "category": "Lighting & Electronics",
        "scope": "Applies to electronic controlgear (LED drivers/power supplies) for LED luminaires.",
        "mandatory_qco": "Mandatory under MeitY CRS Scheme-II.",
        "key_clauses": {
            "Clause 15": "Protection of Associated LED Modules against Overvoltage and Electric Shock",
            "Clause 16": "Abnormal Conditions: Open circuit, short circuit, and failure of internal electronics",
            "Clause 17": "Creepage Distances and Clearances for SELV (Safety Extra Low Voltage)"
        },
        "mandatory_tests": ["Dielectric strength", "Thermal endurance", "Overload protection", "Fault conditions"],
        "certification_scheme": "Scheme-II (CRS)",
        "hindi_summary": "एलईडी ड्राइवर (नियंत्रण गियर) सुरक्षा - भारत में निर्मित या आयातित सभी एलईडी ड्राइवरों के लिए CRS पंजीकरण अनिवार्य।"
    },

    # ── CIVIL & CONSTRUCTION ──────────────────────────────────────────────────
    "IS 1786:2008": {
        "standard_number": "IS 1786:2008",
        "title": "High Strength Deformed Steel Bars and Wires for Concrete Reinforcement — Specification (Fourth Revision)",
        "category": "Steel & Construction Infrastructure",
        "scope": "Covers thermo-mechanically treated (TMT) steel bars, cold twisted deformed (CTD) bars, and wires used in reinforced cement concrete (RCC) structures.",
        "mandatory_qco": "Strictly Mandatory under Steel and Steel Products (Quality Control) Order by Ministry of Steel. Selling non-BIS TMT bars is a criminal offense.",
        "key_clauses": {
            "Clause 4.1 & Table 1": "Chemical Composition (Max % by mass): Fe 500D (C: 0.25%, S: 0.040%, P: 0.040%, S+P: 0.075%); Fe 550D (C: 0.25%, S: 0.040%, P: 0.040%, S+P: 0.075%). Carbon Equivalent (CE) max 0.42% for weldability.",
            "Clause 8.1 & Table 2": "Mechanical Properties: Fe 500 (Yield/0.2% Proof Stress min 500 MPa, Tensile min 545 MPa, Elongation min 14.5%); Fe 500D (Yield min 500 MPa, Tensile min 565 MPa, Tensile/Yield ratio >= 1.10, Elongation min 16.0%, Total Elongation at max force >= 5%); Fe 550D (Yield min 550 MPa, Tensile min 600 MPa, Elongation min 14.5%).",
            "Clause 9.1": "Bend and Rebend Test: Bars must bend 180° around prescribed mandrel and rebend without transverse cracking.",
            "Clause 11.1": "Nominal Mass Tolerances: Up to 10mm (±7%), 10mm to 16mm (±5%), above 16mm (±3%).",
            "Clause 12.1": "Marking: Every bundle/bar must bear rolling mark showing manufacturer identity, BIS Standard 'IS 1786', and Steel Grade (e.g. Fe 500D).",
        },
        "mandatory_tests": [
            "0.2% Proof Stress / Yield Stress & Ultimate Tensile Strength (UTS)",
            "Percentage Elongation and Total Elongation at Maximum Force (TS/YS ratio test)",
            "180° Cold Bend Test and 157.5° Rebend Test around specified mandrels",
            "Chemical Analysis (Optical Emission Spectroscopy for C, S, P, CE)",
            "Nominal Mass per Meter Test on 0.5 meter bar samples"
        ],
        "certification_scheme": "Scheme-I (ISI Mark) - Mandatory QCO",
        "hindi_summary": "टीएमटी सरिया (TMT Rebars) विनिर्देश - इस्पात मंत्रालय के आदेशानुसार अनिवार्य। Fe 500D के लिए न्यूनतम 500 MPa यील्ड स्ट्रेंथ, 16% बढ़ाव और सी+एस+पी रासायनिक नियंत्रण।"
    },

    "IS 2062:2011": {
        "standard_number": "IS 2062:2011",
        "title": "Hot Rolled Medium and High Tensile Structural Steel — Specification",
        "category": "Steel & Heavy Engineering",
        "scope": "Applies to structural steel plates, sections (beams, channels, angles), flats, bars, and hollow sections for bridges, PEB sheds, transmission towers, and industrial buildings.",
        "mandatory_qco": "Mandatory under Steel and Steel Products QCO.",
        "key_clauses": {
            "Clause 4.1 & Table 1": "Grades: E250 (Yield 250 MPa, Tensile 410 MPa), E300, E350, E410, E450. Quality sub-grades A, BR, B0, C based on Charpy V-notch impact test temperature.",
            "Clause 7.1": "Impact Test: Charpy V-notch impact energy at room temp (BR), 0°C (B0), or -20°C (C) shall not be less than 27 Joules.",
            "Clause 10.1": "Ultrasonic Testing: For heavy plates >25mm thickness as per ASTM A578/IS 4225."
        },
        "mandatory_tests": ["Tensile & Yield Strength test", "Charpy Impact test at 0°C/-20°C", "Bend test", "Spectro chemical analysis"],
        "certification_scheme": "Scheme-I (ISI Mark) - Mandatory QCO",
        "hindi_summary": "हॉट रोल्ड संरचनात्मक स्टील - पुलों, टावरों और औद्योगिक भवनों के लिए ई250/ई350 ग्रेड। अनिवार्य आईएसआई मार्किंग।"
    },

    "IS 269:2015": {
        "standard_number": "IS 269:2015",
        "title": "Ordinary Portland Cement (OPC 33, 43, and 53 Grade) — Specification",
        "category": "Building Materials",
        "scope": "Unified specification for 33 Grade, 43 Grade, and 53 Grade Ordinary Portland Cement.",
        "mandatory_qco": "Strictly Mandatory under Cement (Quality Control) Order. Unlawful to manufacture, store, or sell without ISI mark.",
        "key_clauses": {
            "Clause 5.1 & Table 1": "Chemical Requirements: Lime Saturation Factor (0.66 to 1.02), Alumina-Iron ratio (min 0.66), Insoluble Residue (max 5.0%), Magnesia (max 6.0%), Total Loss on Ignition (max 5.0%).",
            "Clause 6.1 & Table 2": "Physical Properties: Fineness (Blaine specific surface min 225 m2/kg), Initial Setting Time (min 30 minutes), Final Setting Time (max 600 minutes / 10 hours), Soundness (Le-Chatelier expansion max 10 mm, Autoclave expansion max 0.8%).",
            "Clause 6.2": "Compressive Strength: 53 Grade -> 3-day (min 27 MPa), 7-day (min 37 MPa), 28-day (min 53 MPa). 43 Grade -> 28-day min 43 MPa.",
            "Clause 9.1": "Packaging: In HDPE/PP woven sacks conforming to IS 11652, net mass 50 kg ± 1% with mandatory ISI mark.",
        },
        "mandatory_tests": [
            "Compressive Strength at 3, 7, and 28 days using vibrating machine",
            "Setting Time Test via Vicat Apparatus",
            "Fineness by Blaine Air Permeability Apparatus",
            "Soundness Test (Le-Chatelier and Autoclave methods)",
            "Loss on Ignition and Insoluble Residue chemical tests"
        ],
        "certification_scheme": "Scheme-I (ISI Mark) - Mandatory QCO",
        "hindi_summary": "साधारण पोर्टलैंड सीमेंट (OPC 33, 43, 53 ग्रेड) - 53 ग्रेड के लिए 28-दिवसीय न्यूनतम संपीड़न सामर्थ्य 53 MPa। अनिवार्य आईएसआई मार्क।"
    },

    # ── CONSUMER SAFETY & VEHICULAR ACCESSORIES ───────────────────────────────
    "IS 4151:2015": {
        "standard_number": "IS 4151:2015",
        "title": "Protective Helmets for Two Wheeler Riders — Specification (Fourth Revision)",
        "category": "Automotive & Personal Protection",
        "scope": "Applies to protective helmets worn by drivers and pillion riders of two-wheeled motor vehicles.",
        "mandatory_qco": "Strictly Mandatory under Ministry of Road Transport and Highways (MoRTH) QCO. Non-ISI helmets are confiscated and banned under Motor Vehicles Act Section 129.",
        "key_clauses": {
            "Clause 4.1": "Weight Limit: Maximum permissible mass of the helmet complete with visor and retention assembly shall not exceed 1.2 kg (1200 grams).",
            "Clause 7.1": "Impact Absorption Test: Peak deceleration transmitted to headform shall not exceed 300g (acceleration of gravity) during impact at 7.5 m/s drop speed onto steel anvil.",
            "Clause 7.2": "Penetration Resistance: A 3 kg conical pointed striker dropped from 1 meter shall not make electrical contact with the headform.",
            "Clause 7.3": "Retention System (Chinstrap): Dynamic displacement under 1 kN load shall not exceed 35 mm, residual displacement <= 25 mm.",
            "Clause 8.1": "Visor Requirements: Optical transmittance >= 85%, scratch resistance, and shatterproof polycarbonate material.",
            "Clause 9.1": "Labelling: Permanent ISI mark label, IS standard 'IS 4151', size in cm, month & year of manufacture, manufacturer identification.",
        },
        "mandatory_tests": [
            "Impact Attenuation / Deceleration Test with triaxial accelerometer headform",
            "Penetration Resistance Test using 3 kg steel cone drop",
            "Dynamic Chinstrap Retention / Rigidity Test under 1000 N shock load",
            "Visor Luminous Transmittance and Refractive Power Test",
            "Environmental Conditioning: Solvent treatment, UV exposure, +50°C and -20°C conditioning"
        ],
        "certification_scheme": "Scheme-I (ISI Mark) - Mandatory QCO",
        "hindi_summary": "दोपहिया वाहन चालकों के लिए सुरक्षा हेलमेट - वजन अधिकतम 1.2 किग्रा, 300g से कम इम्पैक्ट मंदी, वाइज़र 85% पारदर्शिता। बिना आईएसआई हेलमेट बेचना अपराध है।"
    },

    "IS 2347:2017": {
        "standard_number": "IS 2347:2017",
        "title": "Domestic Pressure Cookers — Specification (Fourth Revision)",
        "category": "Consumer Kitchen Appliances",
        "scope": "Applies to domestic pressure cookers made of aluminium alloy or stainless steel with operating gauge pressure between 0.5 to 1.1 bar.",
        "mandatory_qco": "Mandatory under Pressure Cooker (Quality Control) Order by DPIIT. Non-ISI pressure cookers are seized by consumer authorities.",
        "key_clauses": {
            "Clause 4.1": "Material: Food grade aluminium alloy or Austenitic Stainless Steel Grade 304.",
            "Clause 5.1": "Operating Pressure: Normal operating pressure 0.5 to 1.1 bar (50 to 110 kPa).",
            "Clause 6.1": "Safety Pressure Release Device: Pressure relief valve or fusible metallic safety plug must operate before pressure reaches 3.0 times operating pressure.",
            "Clause 8.1": "Hydrostatic Proof Pressure Test: Body and lid must withstand internal hydrostatic test pressure of 3.0 times operating pressure without rupture or leakage.",
            "Clause 9.1": "Gasket Release System: Must safely vent excess steam downwards towards cooker base, never upwards toward user face.",
        },
        "mandatory_tests": [
            "Hydrostatic Pressure Test at 3.0x operating pressure",
            "Operating Pressure Relief Test (Dead-weight / Spring valve)",
            "Safety Plug Fusion / Venting Test",
            "Thermal Shock Test on handles and lid",
            "Cooking Efficiency & Leakage Test"
        ],
        "certification_scheme": "Scheme-I (ISI Mark) - Mandatory QCO",
        "hindi_summary": "घरेलू प्रेशर कुकर विनिर्देश - सामान्य परिचालन दबाव के 3 गुना पर हाइड्रोस्टेटिक परीक्षण, सुरक्षा वाल्व एवं नीचे की ओर भाप निकासी अनिवार्य।"
    },

    "IS 9873 (Part 1):2019": {
        "standard_number": "IS 9873 (Part 1):2019",
        "title": "Safety of Toys — Part 1: Safety Aspects Related to Mechanical and Physical Properties",
        "category": "Consumer & Child Safety",
        "scope": "Applies to toys designed for use in play by children under 14 years of age. Includes rattles, dolls, toy vehicles, soft toys.",
        "mandatory_qco": "Strictly Mandatory under Toys (Quality Control) Order. Zero imported or domestic toys may be sold in India without BIS ISI mark.",
        "key_clauses": {
            "Clause 4.1": "Small Parts Choking Hazard: Toys for children under 36 months must not contain or release small parts fitting inside the small parts cylinder (31.7 mm diameter).",
            "Clause 4.2": "Sharp Edges and Points: No hazardous accessible sharp edges or points as per test gauge.",
            "Clause 4.3": "Tension and Drop Tests: Toys subjected to 90 N pull force and drops onto steel plate without creating choking fragments.",
            "IS 9873 Part 3": "Migration of Certain Elements: Maximum limit for Antimony (60 mg/kg), Arsenic (25 mg/kg), Barium (1000 mg/kg), Cadmium (75 mg/kg), Chromium (60 mg/kg), Lead (90 mg/kg), Mercury (60 mg/kg).",
        },
        "mandatory_tests": [
            "Small Parts Choking Test with truncated cylinder",
            "Sharp Edge & Sharp Point Test",
            "Tensile, Torque, and Drop Impact Mechanical Tests",
            "Heavy Metals Migration Test (Part 3) using ICP-OES",
            "Flammability Test (Part 2)"
        ],
        "certification_scheme": "Scheme-I (ISI Mark) - Mandatory QCO",
        "hindi_summary": "खिलौनों की सुरक्षा (भाग 1 एवं 3) - बच्चों के लिए चोकिंग हैज़र्ड, नुकीले किनारों की रोकथाम और लेड/कैडमियम जैसे भारी धातुओं की सख्त सीमाएं। आईएसआई मार्क अनिवार्य।"
    },

    # ── HALLMARKING & PRECIOUS METALS ─────────────────────────────────────────
    "IS 1417:2016": {
        "standard_number": "IS 1417:2016",
        "title": "Gold and Gold Alloys, Jewellery/Artefacts — Fineness and Marking (Fifth Revision)",
        "category": "Gold Hallmarking",
        "scope": "Prescribes fineness standards and mandatory hallmark symbols for gold jewellery and artefacts sold to Indian consumers.",
        "mandatory_qco": "Strictly Mandatory across all notified districts of India under BIS Hallmarking Regulations. Selling unhallmarked gold jewellery is illegal.",
        "key_clauses": {
            "Clause 4.1 & Table 1": "Permissible Gold Fineness Purity Grades: 24K (999 parts per thousand), 23K (958), 22K (916 parts per thousand - standard 22 Carat), 20K (833), 18K (750 parts per thousand), 14K (585 parts per thousand), 9K (375).",
            "Clause 5.1": "Mandatory 3-Part Hallmark Symbols: (1) BIS Standard Logo (Triangular Peak logo), (2) Purity in Karat and Fineness (e.g. 22K916, 18K750, 14K585), (3) 6-digit alphanumeric HUID (Hallmark Unique Identification) laser engraved on each individual item.",
            "Clause 5.2": "HUID Traceability: Every single jewellery piece receives a unique HUID from the computerized BIS Hallmark portal at the Assaying & Hallmarking Centre (AHC), enabling consumer verification on BIS Care App.",
            "Clause 6.1": "Assaying Method: Fire Assay method (IS 1418) or certified XRF for non-destructive preliminary screening.",
            "Consumer Compensation Clause": "If purity is found less than marked, the jeweller is liable to pay the consumer the difference in cost of gold plus 2 times the testing fee."
        },
        "mandatory_tests": [
            "Fire Assay Cupellation Test as per IS 1418 (Gold reference standard)",
            "X-Ray Fluorescence (XRF) Spectrometry for surface purity check",
            "Laser Marking of 6-character alphanumeric HUID",
            "Homogeneity and solder testing"
        ],
        "certification_scheme": "Hallmarking Scheme (AHC Accreditation)",
        "hindi_summary": "स्वर्ण आभूषण हॉलमार्किंग विनिर्देश - अनिवार्य 3 प्रतीक: (1) बीआईएस त्रिकोणीय लोगो, (2) शुद्धता (जैसे 22K916 या 18K750), (3) 6-अंकीय अक्षरांकीय HUID कोड। 'BIS Care App' पर सत्यापन योग्य।"
    },

    "IS 2112:2014": {
        "standard_number": "IS 2112:2014",
        "title": "Silver and Silver Alloys, Jewellery/Artefacts — Fineness and Marking",
        "category": "Silver Hallmarking",
        "scope": "Fineness grades and hallmarking criteria for silver articles.",
        "mandatory_qco": "Voluntary / Notified Scheme under BIS Hallmarking.",
        "key_clauses": {
            "Clause 4.1": "Fineness Grades: 990 (Fine silver), 970, 925 (Sterling silver), 900, 835, 800.",
            "Clause 5.1": "Marking: BIS Logo, Purity mark (e.g., 925), Jeweller mark, AHC mark, Year of marking."
        },
        "mandatory_tests": ["Volumetric (Potentiometric) method as per IS 2113", "XRF Spectrometry"],
        "certification_scheme": "Hallmarking Scheme",
        "hindi_summary": "चांदी और चांदी के आभूषण हॉलमार्किंग - 925 स्टर्लिंग सिल्वर मानक। बीआईएस लोगो एवं शुद्धता अंकन।"
    }
}

# ── PRODUCT TO STANDARD MAPPING ───────────────────────────────────────────────
PRODUCT_MAPPINGS = [
    {
        "keywords": ["water", "drinking water", "tap water", "municipal water", "potable water", "peene ka pani", "pani"],
        "primary_standard": "IS 10500:2012",
        "packaged_alternative": "IS 14543:2004",
        "mineral_alternative": "IS 13428:2005",
        "clarification_needed": True,
        "clarification_prompt": "Are you asking about (1) Municipal piped drinking water (IS 10500), (2) Packaged drinking water in bottles/pouches (IS 14543), or (3) Packaged natural mineral spring water (IS 13428)?"
    },
    {
        "keywords": ["packaged water", "water bottle", "bottled water", "bisleri", "aquafina", "kinley", "packaged drinking water"],
        "primary_standard": "IS 14543:2004",
        "clarification_needed": False
    },
    {
        "keywords": ["plug", "socket", "switch socket", "wall plug", "3-pin", "power strip", "extension cord", "2-pin"],
        "primary_standard": "IS 1293:2019",
        "clarification_needed": False
    },
    {
        "keywords": ["cable", "cables", "wire", "wires", "electrical wire", "house wire", "pvc cable", "frls wire"],
        "primary_standard": "IS 694:2010",
        "industrial_alternative": "IS 7098 (XLPE Cables)",
        "clarification_needed": True,
        "clarification_prompt": "Please specify your wire type: (1) Domestic building PVC insulated wires up to 1100V (IS 694:2010) or (2) Heavy industrial XLPE power cables up to 33 kV (IS 7098)?"
    },
    {
        "keywords": ["tmt", "steel bar", "sariya", "rebars", "rebar", "reinforcement steel", "fe 500d", "fe 550d", "tmt bar", "सरिया", "टीएमटी"],
        "primary_standard": "IS 1786:2008",
        "clarification_needed": False
    },
    {
        "keywords": ["structural steel", "steel plate", "beam", "channel", "girder", "i-beam", "angle iron", "लोहा", "संरचनात्मक स्टील"],
        "primary_standard": "IS 2062:2011",
        "clarification_needed": False
    },
    {
        "keywords": ["cement", "opc", "ordinary portland cement", "53 grade cement", "43 grade", "ultratech", "ambuja", "सीमेंट"],
        "primary_standard": "IS 269:2015",
        "clarification_needed": False
    },
    {
        "keywords": ["helmet", "helmets", "two wheeler helmet", "bike helmet", "motorcycle helmet", "protective helmet"],
        "primary_standard": "IS 4151:2015",
        "clarification_needed": False
    },
    {
        "keywords": ["cooker", "pressure cooker", "cookers", "prestige cooker", "hawkins"],
        "primary_standard": "IS 2347:2017",
        "clarification_needed": False
    },
    {
        "keywords": ["toy", "toys", "plastic toys", "doll", "stuffed toy", "rattles", "action figure"],
        "primary_standard": "IS 9873 (Part 1):2019",
        "clarification_needed": False
    },
    {
        "keywords": ["gold", "gold jewellery", "hallmark", "huid", "sona", "jewellery", "22k", "18k", "gold purity"],
        "primary_standard": "IS 1417:2016",
        "clarification_needed": False
    },
    {
        "keywords": ["silver", "silver jewellery", "chandi", "silver utensils", "925 silver"],
        "primary_standard": "IS 2112:2014",
        "clarification_needed": False
    },
    {
        "keywords": ["laptop", "tablet", "pc", "computer", "mobile charger", "power adapter", "it equipment"],
        "primary_standard": "IS 13252 (Part 1):2010",
        "clarification_needed": False
    },
    {
        "keywords": ["lithium battery", "battery pack", "power bank", "li-ion cell", "mobile battery"],
        "primary_standard": "IS 16046 (Part 1 & 2):2018",
        "clarification_needed": False
    },
    {
        "keywords": ["led driver", "led power supply", "led ballast"],
        "primary_standard": "IS 15885 (Part 2/Sec 13):2012",
        "clarification_needed": False
    },
    {
        "keywords": ["geyser", "water heater", "electric iron", "mixer grinder", "room heater", "home appliance"],
        "primary_standard": "IS 302-1:2008",
        "clarification_needed": False
    }
]

# ── CERTIFICATION PROCEDURES & DOCUMENT CHECKLISTS ────────────────────────────
SCHEME_I_STEPS = {
    "scheme": "Scheme-I (ISI Mark - Product Certification Scheme)",
    "portal": "MANAK Online (https://www.manakonline.in)",
    "validity": "Initial license granted for 1 to 2 years, renewable upon payment of marking fees and surveillance compliance.",
    "steps": [
        {
            "step": 1,
            "title": "Identification of Standard & In-House Testing Setup",
            "desc": "Identify the applicable Indian Standard (IS Code). Set up the in-house laboratory with calibrated test equipment as prescribed in the Scheme of Inspection and Testing (SIT) for that product."
        },
        {
            "step": 2,
            "title": "Online Application Submission on MANAK Online",
            "desc": "Register on manakonline.in, fill out Form-V, upload required manufacturing and testing documents, and pay the non-refundable application fee (₹1,000) and factory audit inspection charges."
        },
        {
            "step": 3,
            "title": "Preliminary Factory Audit by BIS Auditor",
            "desc": "A designated BIS technical officer visits the manufacturing premises to verify manufacturing machinery, quality control procedures, calibration certificates of lab equipment, and competence of testing personnel."
        },
        {
            "step": 4,
            "title": "Sample Drawing & Independent Lab Testing",
            "desc": "During the inspection, the BIS officer draws samples in duplicate (counter-samples sealed). One sample is tested in the factory lab, and another is dispatched to a BIS recognized/NABL accredited laboratory for complete conformance testing."
        },
        {
            "step": 5,
            "title": "Grant of Licence (GoL) & CML Number",
            "desc": "Upon satisfactory factory inspection report and passing independent lab test report, BIS issues the Grant of Licence (GoL). A unique 7-digit CML (Certificate of Manufacturing Licence) number is allocated to the factory."
        },
        {
            "step": 6,
            "title": "Application of ISI Mark & Periodic Surveillance",
            "desc": "The manufacturer can now print the ISI mark along with the IS Code and CML number on the product. BIS conducts regular surprise surveillance visits and market sample draws to ensure continuous conformity."
        }
    ],
    "documents_required": [
        "1. Proof of Factory Registration / Incorporation (GST Certificate, MSME Udyam, or RoC Certificate)",
        "2. Manufacturing Process Flow Chart (showing all stages from raw material receipt to packaging)",
        "3. Complete List of Manufacturing Machinery (with brand, capacity, and operational status)",
        "4. Complete List of In-House Testing Equipment (with valid calibration certificates traceable to NPL/NABL)",
        "5. Plant & Factory Layout Drawing (clearly demarcating production, raw material storage, and lab area)",
        "6. Consent / Authorization letter for Authorized Signatory (Board Resolution / Partnership deed)",
        "7. Independent Test Report from a BIS Approved / NABL Accredited Laboratory",
        "8. Undertaking regarding agreement to Scheme of Inspection and Testing (SIT) & Marking Fee payment"
    ]
}

SCHEME_II_STEPS = {
    "scheme": "Scheme-II (CRS - Compulsory Registration Scheme for Electronics & IT)",
    "portal": "CRS Portal (https://www.bis.gov.in/index.php/crs-portal/)",
    "validity": "Registration granted for 2 years, renewable periodically.",
    "steps": [
        {
            "step": 1,
            "title": "Sample Testing in BIS-Recognized Laboratory",
            "desc": "The manufacturer submits representative product samples directly to a BIS-recognized testing laboratory in India for testing as per relevant IS/IEC standard. Test report is issued within 15-30 days."
        },
        {
            "step": 2,
            "title": "Online Registration on BIS CRS Portal",
            "desc": "The applicant creates a profile on the CRS portal, submits the valid test report (not older than 90 days), and enters product details (model numbers, brand, factory details)."
        },
        {
            "step": 3,
            "title": "Appointment of Authorized Indian Representative (AIR)",
            "desc": "For overseas manufacturers, appointment of a registered Indian entity as Authorized Indian Representative (AIR) is mandatory through an affidavit."
        },
        {
            "step": 4,
            "title": "Document Scrutiny and Grant of Registration",
            "desc": "BIS scrutinizes the application and test reports. Unlike Scheme-I, NO prior factory inspection is required for CRS. BIS grants an 8-digit R-number (Registration Number e.g. R-41XXXXXX)."
        },
        {
            "step": 5,
            "title": "CRS Standard Mark Affixation",
            "desc": "Manufacturer affixes the BIS CRS Standard Mark on product and packaging: 'IS [Standard No.] / R-[Registration No.] / www.bis.gov.in'."
        }
    ],
    "documents_required": [
        "1. Valid Test Report from BIS-Recognized Lab in India (valid within 90 days)",
        "2. Trademark Registration / Brand Authorization Letter from Brand Owner",
        "3. Factory Business License / Manufacturing Certificate (in English)",
        "4. Nomination of Authorized Indian Representative (AIR) with KYC & Affidavit (for foreign manufacturers)",
        "5. Technical Specifications, User Manual, and Circuit/PCB Schematics",
        "6. List of Critical Safety Components (with component test certificates/UL/IEC approvals)",
        "7. Undertaking on Self-Declaration of Conformity format"
    ]
}


class BISService:
    """
    Dedicated BIS & Indian Standards Intelligence Brain.
    Fulfills Smart India Hackathon Problem Statement 26107:
    - Standards document ingestion & hybrid retrieval with exact citations
    - Industry Q&A (Standard finder, testing requirements, QCO compliance)
    - Consumer Q&A (ISI verification, 6-digit HUID Hallmark checks, complaint redressal)
    - Bilingual English & Hindi support
    - Step-by-step certification guidance
    - Follow-up clarification for vague queries
    - Standards comparison engine (IS X vs IS Y)
    - 'I don't know' safe fallback pointing to BIS helpline
    """

    def __init__(self):
        self.catalog = STANDARDS_CATALOG
        self.mappings = PRODUCT_MAPPINGS

    def is_bis_query(self, query: str) -> bool:
        """Determines if the user's query relates to BIS, Indian Standards, ISI, Hallmarking, or products."""
        q_low = query.lower()
        bis_terms = [
            "bis", "indian standard", "is code", "is standard", "isi mark", "isi", "hallmark", "huid",
            "cml", "crs", "qco", "quality control order", "manak", "manakonline", "certification",
            "is 10500", "is 14543", "is 1293", "is 694", "is 1786", "is 2062", "is 269", "is 4151",
            "is 2347", "is 9873", "is 1417", "is 13252", "is 16046", "is 15885", "is 302",
            "which is standard", "what testing is needed", "what is the is standard", "standard for",
            "standards for", "testing is needed", "test parameter", "complaint against", "fake isi", "fake hallmark",
            "consumer complaint", "bis care app", "gold purity", "22k916", "18k750", "scheme-i",
            "scheme-ii", "difference between is", "compare is", "licence for bis", "bis licence",
            "मानक", "बीआईएस", "आईएसआई", "हॉलमार्क", "एचयूआईडी", "प्रमाणीकरण", "गुणवत्ता", "सरिया", "सीमेंट", "हेलमेट",
            "water", "steel", "cement", "cable", "cables", "wire", "wires", "helmet", "helmets", "pressure cooker",
            "cooker", "toy", "toys", "battery", "batteries", "gold", "jewellery", "jewelry", "plug", "socket",
            "geyser", "led", "driver", "pipes", "pvc", "standard", "standards", "clause", "specification"
        ]
        return any(term in q_low for term in bis_terms)

    def is_hindi(self, query: str) -> bool:
        """Detects if the query is in Hindi (contains Devanagari script)."""
        return bool(re.search(r'[\u0900-\u097F]', query))

    def evaluate_query(
        self,
        query: str,
        retrieved_docs: Optional[List[Any]] = None,
        language_preference: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Main reasoning dispatcher for BIS & Indian Standards.
        Returns None if query is completely unrelated to BIS/Standards.
        """
        q_clean = query.strip()
        q_low = q_clean.lower()

        is_hi = (language_preference == "hi") or self.is_hindi(q_clean)

        # 1. Check for Standards Comparison (IS X vs IS Y)
        comp_res = self._check_standards_comparison(q_clean, is_hi)
        if comp_res:
            return comp_res

        # 2. Check for Vague Query needing follow-up questions
        followup_res = self._check_vague_query(q_clean, is_hi)
        if followup_res:
            return followup_res

        # 3. Check for Certification Guidance (Step-by-step help)
        cert_res = self._check_certification_guidance(q_clean, is_hi)
        if cert_res:
            return cert_res

        # 4. Check for Consumer Q&A (ISI check, Hallmark check, Complaint filing, BIS Care App)
        consumer_res = self._check_consumer_qa(q_clean, is_hi)
        if consumer_res:
            return consumer_res

        # 5. Check for Industry Q&A (Which standard applies? What testing is needed?)
        industry_res = self._check_industry_qa(q_clean, is_hi)
        if industry_res:
            return industry_res

        # 6. Check for Specific Standard Number Query (e.g. "What is IS 1786?")
        std_num_res = self._check_specific_standard(q_clean, is_hi)
        if std_num_res:
            return std_num_res

        # 7. Check if user asked a general BIS question that can be answered from RAG docs
        if retrieved_docs:
            rag_ans = self._synthesize_rag_bis(q_clean, retrieved_docs, is_hi)
            if rag_ans:
                return rag_ans

        # 8. If query explicitly asked about a BIS standard/topic that is NOT in catalog or documents:
        # Strict "I don't know" handling pointing to BIS helpline
        if any(k in q_low for k in ["standard", "standards", "is code", "bis code", "bis helpline", "bis license", "isi code", "qco order", "भारतीय मानक", "मानक"]):
            return self._build_i_dont_know_response(q_clean, is_hi)

        return None

    # ──────────────────────────────────────────────────────────────────────────
    # 1. STANDARDS COMPARISON ENGINE (IS X vs IS Y)
    # ──────────────────────────────────────────────────────────────────────────
    def _check_standards_comparison(self, query: str, is_hi: bool) -> Optional[Dict[str, Any]]:
        q_low = query.lower()
        is_comparison = any(k in q_low for k in ["difference between", "compare", "vs", "versus", "अंतर", "तुलना"])
        if not is_comparison:
            return None

        # Extract standard numbers if present
        std_pattern = r'IS\s*(\d+)'
        matches = re.findall(std_pattern, query, re.IGNORECASE)
        found_stds = []
        for m in matches:
            for k in self.catalog.keys():
                if f"IS {m}" in k:
                    if k not in found_stds:
                        found_stds.append(k)

        # Common comparisons
        if ("10500" in q_low and "14543" in q_low) or (len(found_stds) >= 2 and "10500" in found_stds[0] and "14543" in found_stds[1]):
            return self._compare_is10500_vs_is14543(is_hi)
        elif ("1786" in q_low and "2062" in q_low) or (len(found_stds) >= 2 and "1786" in found_stds[0] and "2062" in found_stds[1]):
            return self._compare_is1786_vs_is2062(is_hi)
        elif ("1293" in q_low and ("iec" in q_low or "60884" in q_low)):
            return self._compare_is1293_vs_iec(is_hi)
        elif len(found_stds) >= 2:
            s1, s2 = found_stds[0], found_stds[1]
            return self._generate_generic_comparison(s1, s2, is_hi)

        return None

    def _compare_is10500_vs_is14543(self, is_hi: bool) -> Dict[str, Any]:
        if is_hi:
            ans = (
                "### ⚖️ तुलना: IS 10500:2012 बनाम IS 14543:2004\n\n"
                "भारतीय मानक ब्यूरो (BIS) के अंतर्गत पेयजल एवं पैकेज्ड पेयजल के मध्य मुख्य अंतर निम्नलिखित हैं:\n\n"
                "| विशेषता / पैरामीटर | IS 10500:2012 (पेयजल विनिर्देश) | IS 14543:2004 (पैकेज्ड पेयजल) |\n"
                "| :--- | :--- | :--- |\n"
                "| **उत्पाद का स्वरूप** | नल का पानी, नगरपालिका जलापूर्ति, भूजल या सामान्य पेयजल | सीलबंद बोतलों, जारों और पाउचों में पैक किया गया पेयजल |\n"
                "| **सर्टिफिकेशन की अनिवार्यता** | वाणिज्यिक आपूर्ति और सरकारी योजनाओं हेतु अनिवार्य | **100% अनिवार्य (Mandatory QCO)** - बिना ISI मार्क बिक्री गैर-कानूनी है |\n"
                "| **टीडीएस (TDS) सीमा** | स्वीकार्य: 500 mg/L (वैकल्पिक स्रोत न होने पर 2000 mg/L) | **75 mg/L से 500 mg/L** के बीच होना अनिवार्य |\n"
                "| **कीटनाशक अवशेष परीक्षण** | केवल संदिग्ध स्रोतों हेतु निर्धारित | **सख्त अनिवार्य परीक्षण** (एकल कीटनाशक max 0.0001 mg/L, कुल max 0.0005 mg/L) |\n"
                "| **रोगजनक जीवाणु (Microbial)** | 100 मिली में ई. कोलाई शून्य होना चाहिए | ई. कोलाई के साथ-साथ **स्यूडोमोनास एरुगिनोसा** एवं यीस्ट/मोल्ड 250 मिली में पूरी तरह अनुपस्थित |\n"
                "| **पैकेजिंग माइग्रेशन टेस्ट** | लागू नहीं (पाइप/टैंक डिलीवरी) | **अनिवार्य खाद्य ग्रेड प्लास्टिक माइग्रेशन टेस्ट** (IS 9845) |\n"
                "| **मार्किंग आवश्यकता** | जल आपूर्ति बोर्ड गुणवत्ता प्रमाणन | बोतल पर **आईएसआई मार्क + 7-अंकीय CML लाइसेंस संख्या** अनिवार्य |\n\n"
                "> 📌 **प्रमाणन उद्धरण (Citations)**:\n"
                "> - **IS 10500:2012**, Clause 4.2 & Table 1 — *Drinking Water Physical & Chemical Specifications*\n"
                "> - **IS 14543:2004**, Clause 3.2, 5.1 & Table 2 — *Packaged Drinking Water Microbial and Pesticide Limits*"
            )
        else:
            ans = (
                "### ⚖️ Standards Comparison: IS 10500:2012 vs IS 14543:2004\n\n"
                "Below is the regulatory and technical comparison between Municipal/General Drinking Water and Packaged Drinking Water under the Bureau of Indian Standards:\n\n"
                "| Parameter / Attribute | IS 10500:2012 (Drinking Water) | IS 14543:2004 (Packaged Drinking Water) |\n"
                "| :--- | :--- | :--- |\n"
                "| **Scope & Product** | Piped municipal water, ground water, tap water, public supply | Water sealed in food-grade bottles, pouches, or 20L jars for sale |\n"
                "| **Certification Mandate** | Required for utilities & commercial distribution | **100% Strictly Mandatory (QCO)** — Unlawful to sell without ISI mark |\n"
                "| **TDS Permissible Limits** | Acceptable: 500 mg/L (relaxation up to 2000 mg/L without alternate) | **Strict range: 75 mg/L to 500 mg/L** (Demineralized/RO + Remineralized) |\n"
                "| **Pesticide Residue Limits** | Standard general surveillance limits | **Mandatory GC-MS/MS testing** (Individual max 0.0001 mg/L, Total max 0.0005 mg/L) |\n"
                "| **Microbiological Limits** | E. coli absent in 100 ml sample | E. coli, Coliform, Faecal Streptococci, and **Pseudomonas aeruginosa** strictly Absent in 250 ml |\n"
                "| **Packaging Testing** | N/A (distributed via pipe mains/tankers) | **Mandatory Overall Migration & Container Safety Tests** (IS 15609 / IS 12252) |\n"
                "| **Labelling Requirement** | Utility water test reports | Product label must bear **ISI logo + Standard 'IS 14543' + 7-digit CML Number** |\n\n"
                "> 📌 **Citations**:\n"
                "> - **IS 10500:2012**, Clause 4.2, Table 1 & Table 6 — *Drinking Water Specification*\n"
                "> - **IS 14543:2004**, Clause 4.1, Table 1, Clause 5.1 & Clause 8.1 — *Packaged Drinking Water Specification*"
            )

        return {
            "answer": ans,
            "citations": [
                {
                    "standard": "IS 10500:2012",
                    "clause": "Clause 4.2 & Table 1",
                    "title": "Drinking Water — Specification",
                    "snippet": "Organoleptic and Physical Parameters: TDS max 500 mg/L, Turbidity max 1 NTU, E. coli absent.",
                    "document": "IS_10500_2012_Drinking_Water.pdf",
                    "page": 2
                },
                {
                    "standard": "IS 14543:2004",
                    "clause": "Clause 4.1, 5.1 & Table 2",
                    "title": "Packaged Drinking Water — Specification",
                    "snippet": "TDS between 75-500 mg/L, Pseudomonas aeruginosa absent, Pesticide residues individual max 0.0001 mg/L.",
                    "document": "IS_14543_2004_Packaged_Water.pdf",
                    "page": 3
                }
            ],
            "mode": "Sovereign Standards Comparison Engine"
        }

    def _compare_is1786_vs_is2062(self, is_hi: bool) -> Dict[str, Any]:
        if is_hi:
            ans = (
                "### ⚖️ तुलना: IS 1786:2008 (TMT सरिया) बनाम IS 2062:2011 (संरचनात्मक स्टील)\n\n"
                "| विशेषता | IS 1786:2008 (TMT Rebars) | IS 2062:2011 (Structural Steel) |\n"
                "| :--- | :--- | :--- |\n"
                "| **अनुप्रयोग (Application)** | आरसीसी कंक्रीट सुदृढीकरण (भवन, पुल स्तंभ, नींव) | स्टील संरचनाएं, गर्डर, पुल, पीईबी शेड, ट्रांसमिशन टावर |\n"
                "| **उत्पाद का आकार** | रिब्ड/विकृत गोल सरिया (8mm से 40mm व्यास) | प्लेट्स, बीम (I-Beams), चैनल, एंगल, फ्लैट्स |\n"
                "| **प्रमुख ग्रेड** | Fe 415, Fe 500, **Fe 500D**, Fe 550D, Fe 600 | **E250**, E300, E350, E410, E450 (क्वालिटी BR, B0, C) |\n"
                "| **यील्ड स्ट्रेंथ (Yield Stress)** | न्यूनतम 500 MPa (Fe 500D) | न्यूनतम 250 MPa (E250 ग्रेड) |\n"
                "| **अनिवार्य परीक्षण** | यील्ड स्ट्रेंथ, तन्यता, 180° बेंड एवं रिबेंड टेस्ट | तन्यता, शार्पी इम्पैक्ट टेस्ट (0°C/-20°C पर V-नॉच), बेंड टेस्ट |\n"
                "| **रोलिंग मार्किंग** | हर मीटर पर निर्माता नाम, 'IS 1786' और ग्रेड (Fe 500D) | स्टील प्लेट/बीम पर स्टैंपिंग व हीट नंबर |\n\n"
                "> 📌 **प्रमाणन उद्धरण (Citations)**:\n"
                "> - **IS 1786:2008**, Clause 8.1 & Table 2 — *High Strength Deformed Steel Bars for Concrete Reinforcement*\n"
                "> - **IS 2062:2011**, Clause 4.1 & Clause 7.1 — *Hot Rolled Medium and High Tensile Structural Steel*"
            )
        else:
            ans = (
                "### ⚖️ Standards Comparison: IS 1786:2008 vs IS 2062:2011\n\n"
                "| Parameter | IS 1786:2008 (TMT Rebars) | IS 2062:2011 (Structural Steel) |\n"
                "| :--- | :--- | :--- |\n"
                "| **Primary Application** | Reinforcing concrete (RCC slabs, columns, footings, civil structures) | Fabricated steel structures, bridges, PEB sheds, transmission towers |\n"
                "| **Product Geometry** | Deformed round ribbed bars (diameters 8mm to 40mm) | Steel plates, I-beams, universal columns, angles, channels, hollow sections |\n"
                "| **Key Steel Grades** | Fe 415, Fe 500, **Fe 500D**, Fe 550D, Fe 600 | **E250**, E300, E350, E410, E450 (Sub-qualities A, BR, B0, C) |\n"
                "| **Yield Strength (Min)** | 500 MPa (for Fe 500D) with TS/YS ratio >= 1.10 | 250 MPa (for Grade E250) |\n"
                "| **Mandatory Tests** | 0.2% Proof Stress, Tensile, Elongation (>=16%), 180° Bend & Rebend | Tensile test, Yield stress, Charpy V-Notch Impact test (>=27J at 0°C/-20°C) |\n"
                "| **Mandatory Marking** | Continuous rolling brand mark showing brand, 'IS 1786', and grade | Mill stencil, heat number, grade E250, and BIS Standard logo |\n\n"
                "> 📌 **Citations**:\n"
                "> - **IS 1786:2008**, Clause 4.1, Table 1 & Clause 8.1 — *TMT Bars for Concrete Reinforcement*\n"
                "> - **IS 2062:2011**, Clause 4.1, Table 1 & Clause 7.1 — *Hot Rolled Structural Steel Specification*"
            )

        return {
            "answer": ans,
            "citations": [
                {
                    "standard": "IS 1786:2008",
                    "clause": "Clause 8.1 & Table 2",
                    "title": "High Strength Deformed Steel Bars for Concrete Reinforcement",
                    "snippet": "Yield stress min 500 MPa, elongation min 16% for Fe 500D.",
                    "document": "IS_1786_2008_TMT_Steel.pdf",
                    "page": 4
                },
                {
                    "standard": "IS 2062:2011",
                    "clause": "Clause 4.1 & Clause 7.1",
                    "title": "Hot Rolled Medium and High Tensile Structural Steel",
                    "snippet": "Grade E250 yield strength min 250 MPa, Charpy impact 27J.",
                    "document": "IS_2062_2011_Structural_Steel.pdf",
                    "page": 2
                }
            ],
            "mode": "Sovereign Standards Comparison Engine"
        }

    def _compare_is1293_vs_iec(self, is_hi: bool) -> Dict[str, Any]:
        ans = (
            "### ⚖️ Comparison: IS 1293:2019 vs International Standards (IEC 60884-1 / BS 546)\n\n"
            "India's electrical plug and socket infrastructure differs fundamentally from European (Schuko Type F) and British (Type G) designs:\n\n"
            "1. **Socket Pin Configuration**: IS 1293:2019 strictly mandates the **Type D (6A 3-pin round)** and **Type M (16A large 3-pin round)** configurations with a dedicated large top earth pin.\n"
            "2. **Safety Shutters**: Under IS 1293:2019 Clause 10.5, all domestic socket-outlets must incorporate internal safety shutters that only open when the earth pin or both live/neutral pins are simultaneously inserted, protecting children from electric shock.\n"
            "3. **Solid Brass Pin Construction**: Solid brass pins with defined pin dimensions and tolerances (Clause 8.1). Flat-pin Type G or non-earthed Europlugs cannot be certified under IS 1293.\n"
            "4. **Mandatory QCO Status**: Plugs, socket-outlets, and power strips imported or sold in India without BIS certification under IS 1293 are seized at customs under the Electrical Accessories Quality Control Order.\n\n"
            "> 📌 **Citation**: **IS 1293:2019**, Clause 8.1, Clause 10.5 & Clause 19.1 — *Plugs and Socket-Outlets up to 16A Specification*"
        )
        return {
            "answer": ans,
            "citations": [
                {
                    "standard": "IS 1293:2019",
                    "clause": "Clause 8.1 & Clause 10.5",
                    "title": "Plugs and Socket-Outlets Specification",
                    "snippet": "Ratings 6A (Type D) and 16A (Type M) at 250V with mandatory safety shutters.",
                    "document": "IS_1293_2019_Plugs_Sockets.pdf",
                    "page": 2
                }
            ],
            "mode": "Sovereign Standards Comparison Engine"
        }

    def _generate_generic_comparison(self, s1: str, s2: str, is_hi: bool) -> Dict[str, Any]:
        info1 = self.catalog.get(s1, {})
        info2 = self.catalog.get(s2, {})
        ans = (
            f"### ⚖️ Comparison: {s1} vs {s2}\n\n"
            f"| Parameter | {s1} | {s2} |\n"
            f"| :--- | :--- | :--- |\n"
            f"| **Title** | {info1.get('title', 'N/A')} | {info2.get('title', 'N/A')} |\n"
            f"| **Category** | {info1.get('category', 'N/A')} | {info2.get('category', 'N/A')} |\n"
            f"| **Scope** | {info1.get('scope', 'N/A')} | {info2.get('scope', 'N/A')} |\n"
            f"| **Certification Scheme** | {info1.get('certification_scheme', 'Scheme-I')} | {info2.get('certification_scheme', 'Scheme-I')} |\n"
            f"| **Mandatory Status** | {info1.get('mandatory_qco', 'N/A')} | {info2.get('mandatory_qco', 'N/A')} |\n\n"
            f"> 📌 **Citations**:\n"
            f"> - **{s1}** — *{info1.get('title', '')}*\n"
            f"> - **{s2}** — *{info2.get('title', '')}*"
        )
        return {
            "answer": ans,
            "citations": [
                {"standard": s1, "clause": "Scope & Clauses", "title": info1.get("title", ""), "document": f"{s1}.pdf", "page": 1},
                {"standard": s2, "clause": "Scope & Clauses", "title": info2.get("title", ""), "document": f"{s2}.pdf", "page": 1}
            ],
            "mode": "Sovereign Standards Comparison Engine"
        }

    # ──────────────────────────────────────────────────────────────────────────
    # 2. VAGUE QUERY CLARIFICATION & FOLLOW-UP QUESTIONS
    # ──────────────────────────────────────────────────────────────────────────
    def _check_vague_query(self, query: str, is_hi: bool) -> Optional[Dict[str, Any]]:
        q_low = query.lower()

        # Check for vague water query
        if q_low in ["water", "drinking water", "water standard", "pani", "water testing", "what standard for water"]:
            prompt_text = (
                "Water falls under three distinct Indian Standards depending on its source and packaging. Please clarify your query:\n\n"
                "1. **Municipal Piped Drinking Water** — [`IS 10500:2012`](file:///standards/IS_10500_2012.pdf) (Tap water, municipal tankers, ground water)\n"
                "2. **Packaged Drinking Water** — [`IS 14543:2004`](file:///standards/IS_14543_2004.pdf) (Commercially sealed bottles, jars, pouches subjected to RO/demineralization)\n"
                "3. **Packaged Natural Mineral Water** — [`IS 13428:2005`](file:///standards/IS_13428_2005.pdf) (Natural underground spring water without chemical alteration)\n\n"
                "👉 *Please select or type your specific product category so I can provide the exact clause limits, mandatory tests, and certification guidelines.*"
            ) if not is_hi else (
                "जल (पानी) इसके स्रोत और पैकेजिंग के आधार पर तीन अलग-अलग भारतीय मानकों के अंतर्गत आता है। कृपया अपना प्रश्न स्पष्ट करें:\n\n"
                "1. **नगरपालिका आपूर्ति / नल का पेयजल** — **IS 10500:2012** (नल का पानी, भूजल)\n"
                "2. **पैकेज्ड पेयजल (बोतलबंद पानी)** — **IS 14543:2004** (आरओ/उपचारित सीलबंद बोतलें और जार)\n"
                "3. **प्राकृतिक खनिज जल (Natural Mineral Water)** — **IS 13428:2005** (प्राकृतिक झरने का पानी)\n\n"
                "👉 *कृपया अपनी उत्पाद श्रेणी बताएं ताकि मैं सटीक क्लॉज सीमाएं और परीक्षण विवरण प्रस्तुत कर सकूं।*"
            )
            return {
                "answer": prompt_text,
                "intent": "follow_up_clarification",
                "follow_up_options": [
                    "Municipal Tap Water (IS 10500:2012)",
                    "Packaged Bottled Water (IS 14543:2004)",
                    "Natural Mineral Spring Water (IS 13428:2005)"
                ],
                "citations": [],
                "mode": "Sovereign Interactive Clarification Engine"
            }

        # Check for vague cable/wire query
        if q_low in ["cable", "cables", "wire", "wires", "tar", "electrical cable"]:
            prompt_text = (
                "Electrical cables are regulated under different standards based on voltage and insulation. Please specify:\n\n"
                "1. **Domestic Building PVC Insulated Wires** — [`IS 694:2010`](file:///standards/IS_694_2010.pdf) (Single & multi-core copper/aluminium wires up to 1100V)\n"
                "2. **Heavy Industrial XLPE Power Cables** — `IS 7098 (Part 1 & 2)` (Cross-linked polyethylene cables for working voltages up to 33 kV)\n"
                "3. **Flexible Cord & Appliance Wiring** — `IS 9968` / `IS 694`\n\n"
                "👉 *Which type of cable are you manufacturing or inspecting?*"
            )
            return {
                "answer": prompt_text,
                "intent": "follow_up_clarification",
                "follow_up_options": [
                    "Building PVC Wires up to 1100V (IS 694)",
                    "Industrial XLPE Cables (IS 7098)"
                ],
                "citations": [],
                "mode": "Sovereign Interactive Clarification Engine"
            }

        # Check for vague steel query
        if q_low in ["steel", "iron", "sariya", "loha", "steel standard"]:
            prompt_text = (
                "Steel products are strictly governed under separate Ministry of Steel Quality Control Orders. Please specify:\n\n"
                "1. **TMT Rebars for Concrete Reinforcement** — [`IS 1786:2008`](file:///standards/IS_1786_2008.pdf) (Fe 500D, Fe 550D TMT sariya)\n"
                "2. **Structural Steel Plates, Beams, & Channels** — [`IS 2062:2011`](file:///standards/IS_2062_2011.pdf) (E250, E350 structural steel)\n"
                "3. **Galvanized Steel Sheets & Coils** — `IS 277` (Corrugated roofing sheets)\n\n"
                "👉 *Which steel product category applies to your inquiry?*"
            )
            return {
                "answer": prompt_text,
                "intent": "follow_up_clarification",
                "follow_up_options": [
                    "TMT Rebars (IS 1786:2008)",
                    "Structural Steel Sections (IS 2062:2011)",
                    "Galvanized Steel Sheets (IS 277)"
                ],
                "citations": [],
                "mode": "Sovereign Interactive Clarification Engine"
            }

        # Check for vague certification query ("How to get BIS license", "I want certification")
        if q_low in ["i want bis license", "how to get bis", "bis certification", "licence", "certification"]:
            prompt_text = (
                "BIS operates multiple distinct certification schemes depending on whether you manufacture physical industrial/consumer goods or electronics:\n\n"
                "1. **Scheme-I (ISI Mark Scheme)**: For physical products, domestic appliances, cement, steel, helmets, toys, packaged water. Requires factory inspection + lab test.\n"
                "2. **Scheme-II (CRS - Compulsory Registration Scheme)**: For IT goods, smartphones, laptops, LED drivers, power banks. Requires only lab test from BIS recognized lab (NO prior factory audit).\n"
                "3. **Scheme-IV (FMCS - Foreign Manufacturers Certification Scheme)**: For factories located outside India exporting goods to India.\n\n"
                "👉 *Please tell me your product type so I can provide the exact application checklist and fee breakdown.*"
            )
            return {
                "answer": prompt_text,
                "intent": "follow_up_clarification",
                "follow_up_options": [
                    "Scheme-I (ISI Mark for Physical Goods)",
                    "Scheme-II (CRS for Electronics & IT)",
                    "Scheme-IV (Foreign Manufacturers - FMCS)"
                ],
                "citations": [],
                "mode": "Sovereign Interactive Clarification Engine"
            }

        return None

    # ──────────────────────────────────────────────────────────────────────────
    # 3. CERTIFICATION GUIDANCE (STEP-BY-STEP & DOCUMENTS)
    # ──────────────────────────────────────────────────────────────────────────
    def _check_certification_guidance(self, query: str, is_hi: bool) -> Optional[Dict[str, Any]]:
        q_low = query.lower()
        cert_keywords = [
            "how to get bis licence", "how to get bis license", "steps for bis", "certification process",
            "procedure for bis", "documents needed for bis", "document checklist", "scheme-i", "scheme-ii",
            "crs registration", "manakonline", "license procedure", "लाइसेंस प्रक्रिया", "दस्तावेज"
        ]
        if not any(k in q_low for k in cert_keywords):
            return None

        # Check if CRS is specifically mentioned
        is_crs = any(k in q_low for k in ["crs", "electronics", "it goods", "laptop", "battery", "led driver"])
        scheme_data = SCHEME_II_STEPS if is_crs else SCHEME_I_STEPS

        if is_hi:
            steps_str = "\n".join([f"**चरण {s['step']}: {s['title']}**\n{s['desc']}" for s in scheme_data["steps"]])
            docs_str = "\n".join(scheme_data["documents_required"])
            ans = (
                f"### 📜 बीआईएस प्रमाणन मार्गदर्शन (Step-by-Step BIS Certification Guide)\n\n"
                f"**योजना**: {scheme_data['scheme']}\n"
                f"**आधिकारिक पोर्टल**: {scheme_data['portal']}\n"
                f"**लाइसेंस वैधता**: {scheme_data['validity']}\n\n"
                f"#### 🚀 चरण-दर-चरण प्रक्रिया:\n{steps_str}\n\n"
                f"#### 📁 अनिवार्य दस्तावेजों की चेकलिस्ट (Mandatory Documents):\n{docs_str}\n\n"
                f"> 📌 **प्रमाणन उद्धरण**: **BIS Conformity Assessment Regulations 2018**, { 'Scheme-II (CRS)' if is_crs else 'Scheme-I, Clause 3.2 & Form-V' }\n"
                f"> 💡 *मार्गदर्शन सहायता के लिए राष्ट्रीय टोल-फ्री हेल्पलाइन: **1800-11-1255** पर संपर्क कर सकते हैं।*"
            )
        else:
            steps_str = "\n\n".join([f"**Step {s['step']}: {s['title']}**\n{s['desc']}" for s in scheme_data["steps"]])
            docs_str = "\n".join(scheme_data["documents_required"])
            ans = (
                f"### 📜 Step-by-Step BIS Certification Guidance & Document Checklist\n\n"
                f"**Governing Scheme**: {scheme_data['scheme']}\n"
                f"**Official Application Portal**: [{scheme_data['portal']}]({scheme_data['portal']})\n"
                f"**License Validity**: {scheme_data['validity']}\n\n"
                f"#### 🚀 Step-by-Step Roadmap:\n\n{steps_str}\n\n"
                f"#### 📁 Mandatory Documents Checklist:\n{docs_str}\n\n"
                f"> 📌 **Regulatory Citation**: **BIS (Conformity Assessment) Regulations 2018**, { 'Scheme-II (CRS Regulations)' if is_crs else 'Scheme-I, Regulation 3, Clause 3.2 & Form-V' }\n"
                f"> 💡 *Need official application support? Contact the BIS National Helpdesk at **1800-11-1255** or email **info@bis.gov.in**.*"
            )

        return {
            "answer": ans,
            "citations": [
                {
                    "standard": "BIS Act 2016",
                    "clause": "Conformity Assessment Regulations 2018, Scheme-I & Scheme-II",
                    "title": "Bureau of Indian Standards Certification Guidelines",
                    "snippet": "Procedures for factory evaluation, sample drawing, testing, and grant of licence.",
                    "document": "BIS_Conformity_Assessment_2018.pdf",
                    "page": 1
                }
            ],
            "mode": "Sovereign Certification Guidance Engine"
        }

    # ──────────────────────────────────────────────────────────────────────────
    # 4. CONSUMER Q&A (ISI, HALLMARK, COMPLAINT, BIS CARE APP)
    # ──────────────────────────────────────────────────────────────────────────
    def _check_consumer_qa(self, query: str, is_hi: bool) -> Optional[Dict[str, Any]]:
        q_low = query.lower()

        # Hallmark / Gold check
        if any(k in q_low for k in ["hallmark", "huid", "gold check", "check gold", "purity of gold", "हॉलमार्क", "सोना"]):
            return self._answer_hallmark_check(is_hi)

        # ISI mark check
        if any(k in q_low for k in ["check isi", "verify isi", "fake isi", "cml number", "cml", "how to check isi", "आईएसआई"]):
            return self._answer_isi_check(is_hi)

        # Consumer complaint filing
        if any(k in q_low for k in ["complaint", "file a complaint", "substandard", "fake product", "report fake", "शिकायत"]):
            return self._answer_consumer_complaint(is_hi)

        # Mandatory products for consumers
        if any(k in q_low for k in ["is isi mandatory", "mandatory for consumer", "which products require isi"]):
            return self._answer_mandatory_consumer_products(is_hi)

        return None

    def _answer_hallmark_check(self, is_hi: bool) -> Dict[str, Any]:
        if is_hi:
            ans = (
                "### 💎 सोने के आभूषणों पर बीआईएस हॉलमार्क की जांच कैसे करें (Gold Hallmark Check)\n\n"
                "बीआईएस नियमों के तहत 1 जुलाई 2021 से सभी अधिसूचित जिलों में केवल **3 अनिवार्य प्रतीकों** वाला हॉलमार्क ही मान्य है:\n\n"
                "1. **त्रिभुजाकार बीआईएस लोगो (BIS Standard Mark)**: बीआईएस का आधिकारिक त्रिकोण निशान।\n"
                "2. **शुद्धता का पैमाना (Karat & Fineness)**: आभूषण पर सोने की शुद्धता स्पष्ट रूप से अंकित होती है:\n"
                "   - **22K916** = 22 कैरेट (91.6% शुद्ध सोना - आभूषणों के लिए सबसे लोकप्रिय)\n"
                "   - **18K750** = 18 कैरेट (75.0% शुद्ध सोना - डायमंड ज्वैलरी हेतु)\n"
                "   - **14K585** = 14 कैरेट (58.5% शुद्ध सोना)\n"
                "   - **24K999** = 24 कैरेट (99.9% शुद्ध सोना - सिक्के और बार)\n"
                "3. **6-अंकीय अक्षरांकीय HUID कोड (Hallmark Unique Identification)**:\n"
                "   - प्रत्येक आभूषण पर लेजर द्वारा 6 अक्षरों/संख्याओं का विशिष्ट कोड (जैसे `AB1234`) उकेरा जाता है।\n\n"
                "#### 📱 'BIS Care App' पर सत्यापन कैसे करें:\n"
                "1. गूगल प्ले स्टोर या एप्पल ऐप स्टोर से आधिकारिक **`BIS Care App`** डाउनलोड करें।\n"
                "2. **'Verify HUID'** विकल्प पर क्लिक करें और आभूषण पर छपा 6-अंकीय कोड दर्ज करें।\n"
                "3. ऐप आपको तुरंत दिखाएगा: (a) आभूषण विक्रेता का नाम और पंजीकरण संख्या, (b) हॉलमार्किंग केंद्र का नाम, (c) हॉलमार्किंग की तारीख, (d) आभूषण का प्रकार (अंगूठी, चेन आदि) और घोषित शुद्धता।\n\n"
                "⚖️ **उपभोक्ता मुआवज़ा नीति**: यदि हॉलमार्क वाले आभूषण की शुद्धता अंकित शुद्धता से कम पाई जाती है, तो बीआईएस अधिनियम के तहत जौहरी ग्राहक को कम शुद्धता की राशि का अंतर + परीक्षण शुल्क का दोगुना चुकाने के लिए बाध्य है।\n\n"
                "> 📌 **प्रमाणन उद्धरण**: **IS 1417:2016**, Clause 5.1 & Clause 5.2 — *Gold and Gold Alloys Hallmarking Specification*"
            )
        else:
            ans = (
                "### 💎 How to Check & Verify BIS Hallmark on Gold Jewellery\n\n"
                "Under the BIS Hallmarking Regulations, genuine hallmarked gold jewellery in India MUST bear **exactly 3 mandatory laser-engraved symbols**:\n\n"
                "1. **BIS Standard Triangular Logo**: The official triangular crest of the Bureau of Indian Standards.\n"
                "2. **Purity in Karat and Fineness**:\n"
                "   - **22K916** = 22 Karat (91.6% pure gold — standard for Indian jewellery)\n"
                "   - **18K750** = 18 Karat (75.0% pure gold — studded/diamond jewellery)\n"
                "   - **14K585** = 14 Karat (58.5% pure gold)\n"
                "   - **24K999** = 24 Karat (99.9% pure gold — bullion/coins)\n"
                "3. **6-Digit Alphanumeric HUID (Hallmark Unique Identification)**:\n"
                "   - A unique 6-character laser code (e.g. `AX49Z2`) assigned exclusively to that single jewellery piece.\n\n"
                "#### 📱 How to Verify Authenticity via 'BIS Care App':\n"
                "1. Open the official **BIS Care App** (available free on Android & iOS).\n"
                "2. Tap the **'Verify HUID'** feature.\n"
                "3. Enter the 6-character alphanumeric code engraved on your jewellery piece.\n"
                "4. The portal instantly displays the official record: **Jeweller's Name & Registration No.**, **AHC Lab Name & Address**, **Hallmarking Date**, **Article Type (ring, bangle, necklace)**, and **Certified Purity**.\n\n"
                "⚖️ **Consumer Compensation Guarantee**: If an authorized testing lab finds the purity less than marked, the jeweller is legally obligated under BIS regulations to refund the purity difference plus pay **twice the testing fee** to the consumer.\n\n"
                "> 📌 **Citation**: **IS 1417:2016**, Clause 4.1, Table 1, Clause 5.1 & Clause 5.2 — *Gold Jewellery Fineness and Marking*"
            )

        return {
            "answer": ans,
            "citations": [
                {
                    "standard": "IS 1417:2016",
                    "clause": "Clause 5.1 & Clause 5.2",
                    "title": "Gold and Gold Alloys, Jewellery — Fineness and Marking",
                    "snippet": "Three mandatory hallmarks: BIS logo, Fineness (e.g. 22K916), and 6-digit alphanumeric HUID.",
                    "document": "IS_1417_2016_Gold_Hallmark.pdf",
                    "page": 2
                }
            ],
            "mode": "Sovereign Consumer Protection Engine"
        }

    def _answer_isi_check(self, is_hi: bool) -> Dict[str, Any]:
        if is_hi:
            ans = (
                "### 🛡️ असली आईएसआई (ISI) मार्क की पहचान और सत्यापन कैसे करें\n\n"
                "असली आईएसआई मार्क वाले उत्पाद पर 3 चीजें एक साथ मुद्रित होनी चाहिए:\n\n"
                "```\n"
                "     IS 14543         <-- शीर्ष पर: भारतीय मानक संख्या\n"
                "      [ ISI ]         <-- केंद्र में: मानक आयताकार आईएसआई लोगो\n"
                "    CM/L-1234567      <-- नीचे: 7 या 8 अंकों का विशिष्ट CML लाइसेंस नंबर\n"
                "```\n\n"
                "#### 📱 'BIS Care App' पर CML नंबर की जांच:\n"
                "1. **BIS Care App** खोलें और **'Verify Licence Details' (CML सत्यापन)** पर क्लिक करें।\n"
                "2. उत्पाद पर लिखा 7-अंकीय CML नंबर दर्ज करें।\n"
                "3. ऐप आपको निर्माता का वास्तविक नाम, कारखाना पता, लाइसेंस की स्थिति (सक्रिय/निलंबित/रद्द) और उस लाइसेंस के तहत स्वीकृत ब्रांड नाम दिखाएगा।\n"
                "4. यदि उत्पाद पर लिखा ब्रांड या कारखाना ऐप के डेटा से मेल नहीं खाता, तो वह नकली आईएसआई मार्क है!\n\n"
                "> 📌 **प्रमाणन उद्धरण**: **BIS (Conformity Assessment) Regulations 2018**, Scheme-I, Clause 6.1"
            )
        else:
            ans = (
                "### 🛡️ How to Verify Authentic ISI Mark & CML Number\n\n"
                "A genuine BIS ISI Mark printed on consumer products MUST always contain three elements in precise alignment:\n\n"
                "```\n"
                "      IS 1293         <-- Top: The Applicable Indian Standard (IS Code)\n"
                "      [ ISI ]         <-- Center: Official Monogrammed Rectangular ISI Emblem\n"
                "    CM/L-1234567      <-- Bottom: Unique 7 or 8 Digit CML (Licence) Number\n"
                "```\n\n"
                "#### 🔍 Verification via 'BIS Care App' or Web Portal:\n"
                "1. Open the **BIS Care App** (or visit `www.bis.gov.in`).\n"
                "2. Select **'Verify Licence Details'**.\n"
                "3. Enter the 7-digit CML number printed below the ISI mark.\n"
                "4. The system validates: **Manufacturer Name**, **Factory Address**, **Validity Status (Valid, Expired, Suspended)**, **Permitted Product**, and **Authorized Brand Names**.\n"
                "5. **Red Flag**: If the brand name on your package does not match the BIS registry record, it is an illegal counterfeit mark!\n\n"
                "> 📌 **Citation**: **BIS (Conformity Assessment) Regulations 2018**, Scheme-I, Regulation 6 & Clause 6.1"
            )

        return {
            "answer": ans,
            "citations": [
                {
                    "standard": "BIS Conformity Assessment Regulations 2018",
                    "clause": "Scheme-I, Clause 6.1",
                    "title": "Manner of Marking of Goods",
                    "snippet": "Manner of applying standard mark with IS code above and CML number below.",
                    "document": "BIS_Conformity_Assessment_2018.pdf",
                    "page": 5
                }
            ],
            "mode": "Sovereign Consumer Protection Engine"
        }

    def _answer_consumer_complaint(self, is_hi: bool) -> Dict[str, Any]:
        if is_hi:
            ans = (
                "### ⚖️ घटिया गुणवत्ता या नकली आईएसआई/हॉलमार्क की शिकायत कैसे दर्ज करें\n\n"
                "यदि आपने कोई घटिया उत्पाद खरीदा है, आईएसआई मार्क का दुरुपयोग पाया है, या बिना हॉलमार्क का सोना बेचा गया है, तो बीआईएस में आधिकारिक शिकायत दर्ज करने के 4 तरीके हैं:\n\n"
                "1. **मोबाइल ऐप (सबसे तेज़)**: **`BIS Care App`** खोलें -> **'Complaints'** सेक्शन चुनें -> उत्पाद का विवरण, CML/HUID नंबर, फोटो और बिल अपलोड करें।\n"
                "2. **ऑनलाइन पोर्टल**: बीआईएस ऑनलाइन शिकायत पोर्टल [www.bis.gov.in](https://www.bis.gov.in) पर जाकर 'Consumer Complaints' दर्ज करें।\n"
                "3. **ईमेल द्वारा**: अपनी शिकायत बिल और फोटो सहित सीधे `complaints@bis.gov.in` पर भेजें।\n"
                "4. **राष्ट्रीय उपभोक्ता हेल्पलाइन**: टोल-फ्री **1915** या बीआईएस हेल्पलाइन **1800-11-1255** पर कॉल करें।\n\n"
                "#### 🔍 जांच प्रक्रिया और उपभोक्ता अधिकार:\n"
                "- बीआईएस जांच अधिकारी संबंधित कारखाने या दुकान पर औचक छापा (Surprise Raid) मारकर नमूने जब्त करते हैं।\n"
                "- मानक परीक्षण में फेल होने पर निर्माता पर कानूनी मुकदमा और लाइसेंस रद्दीकरण होता है।\n"
                "- उपभोक्ता संरक्षण अधिनियम 2019 के तहत आप जिला उपभोक्ता आयोग में हर्जाने का दावा भी कर सकते हैं।\n\n"
                "> 📌 **प्रमाणन उद्धरण**: **BIS Act 2016**, Section 29, 30 & Consumer Grievance Redressal Policy"
            )
        else:
            ans = (
                "### ⚖️ How to File a Consumer Complaint for Substandard or Counterfeit ISI / Hallmark Goods\n\n"
                "Consumers in India can report substandard products, unauthorized use of ISI mark, or fake hallmarking through official channels:\n\n"
                "#### 1. Via 'BIS Care App' (Instant Tracking):\n"
                "- Open the app, navigate to **'Complaints'**.\n"
                "- Select complaint category: *Quality of Product*, *Misuse of ISI Mark*, *Unauthorized Hallmarking*, or *Misleading Advertisements*.\n"
                "- Upload photograph of product label, invoice/bill, and location.\n"
                "- An instant complaint tracking ID is generated.\n\n"
                "#### 2. Via Web Portal & Email:\n"
                "- **Web Portal**: [www.bis.gov.in](https://www.bis.gov.in) — *Consumer Grievance Portal*\n"
                "- **Official Email**: `complaints@bis.gov.in` / `info@bis.gov.in`\n\n"
                "#### 3. Phone Helplines:\n"
                "- **BIS National Toll-Free Number**: **1800-11-1255** (Mon–Fri, 9:00 AM – 5:30 PM)\n"
                "- **National Consumer Helpline**: **1915** (Ministry of Consumer Affairs)\n\n"
                "#### 🔍 Investigation & Redressal Protocol:\n"
                "- BIS enforcement officers conduct surprise search and seizure raids under Section 29 of the BIS Act 2016.\n"
                "- Independent samples are tested in BIS Central Labs within 30 days.\n"
                "- Penalties include imprisonment up to 2 years, fine up to ₹5 lakh or 10 times the value of goods, and compensation to consumer.\n\n"
                "> 📌 **Citation**: **BIS Act 2016**, Section 29, Section 30 & BIS Consumer Grievance Redressal Guidelines"
            )

        return {
            "answer": ans,
            "citations": [
                {
                    "standard": "BIS Act 2016",
                    "clause": "Section 29 & Section 30",
                    "title": "Search, Seizure and Penalties for Misuse of Standard Mark",
                    "snippet": "Penalties for manufacturing or selling goods without valid standard mark under mandatory QCOs.",
                    "document": "BIS_Act_2016.pdf",
                    "page": 12
                }
            ],
            "mode": "Sovereign Consumer Protection Engine"
        }

    def _answer_mandatory_consumer_products(self, is_hi: bool) -> Dict[str, Any]:
        ans = (
            "### 📋 Mandatory BIS ISI Marked Products for Consumers in India\n\n"
            "Under central Quality Control Orders (QCOs), it is **illegal to manufacture, import, store, or sell** the following products without a valid BIS ISI Mark:\n\n"
            "1. **Food & Water**: Packaged Drinking Water (`IS 14543`), Packaged Mineral Water (`IS 13428`), Infant Formula (`IS 11536`), Skimmed Milk Powder (`IS 13334`).\n"
            "2. **Child Safety**: All Toys for children under 14 years (`IS 9873`), Feeding Bottles (`IS 14625`).\n"
            "3. **Kitchen & Home Appliances**: Domestic Pressure Cookers (`IS 2347`), Electric Geysers/Water Heaters (`IS 302-2-21`), Electric Irons (`IS 302-2-3`), Immersion Heaters (`IS 302-2-201`), LPG Cylinders & Regulators (`IS 3196` / `IS 9798`).\n"
            "4. **Road Safety**: Two-Wheeler Helmets (`IS 4151`), Automotive Tyres & Tubes (`IS 15633` / `IS 15636`).\n"
            "5. **Building & Infrastructure**: Ordinary Portland Cement (`IS 269`), TMT Steel Rebars (`IS 1786`), PVC Building Wires (`IS 694`), Domestic Plugs & Sockets (`IS 1293`).\n"
            "6. **Gold Jewellery**: Mandatory 6-digit HUID Hallmarking (`IS 1417`).\n\n"
            "> 📌 **Citation**: **DPIIT, Ministry of Consumer Affairs, MoRTH, and Ministry of Steel Quality Control Orders (QCOs)**"
        )
        return {
            "answer": ans,
            "citations": [
                {"standard": "BIS QCO Catalog 2026", "clause": "Section 16, BIS Act 2016", "title": "Mandatory Products Notification", "snippet": "Over 500 products under mandatory certification.", "document": "BIS_Mandatory_QCO_List.pdf", "page": 1}
            ],
            "mode": "Sovereign Consumer Protection Engine"
        }

    # ──────────────────────────────────────────────────────────────────────────
    # 5. INDUSTRY Q&A (WHICH STANDARD APPLIES? WHAT TESTING IS NEEDED?)
    # ──────────────────────────────────────────────────────────────────────────
    def _check_industry_qa(self, query: str, is_hi: bool) -> Optional[Dict[str, Any]]:
        q_low = query.lower()

        # Find matching product in mappings
        for m in self.mappings:
            for kw in m["keywords"]:
                if kw in q_low:
                    std_key = m["primary_standard"]
                    info = self.catalog.get(std_key, {})

                    # Is user asking about testing?
                    is_testing_q = any(k in q_low for k in ["testing", "test", "routine test", "type test", "acceptance test", "lab", "परीक्षण", "जांच"])

                    if is_testing_q:
                        return self._format_testing_response(std_key, info, is_hi)
                    else:
                        return self._format_standard_response(std_key, info, is_hi)

        return None

    def _format_testing_response(self, std_key: str, info: Dict[str, Any], is_hi: bool) -> Dict[str, Any]:
        tests = info.get("mandatory_tests", [])
        tests_str = "\n".join([f"- **{t}**" for t in tests])

        clauses = info.get("key_clauses", {})
        clauses_str = "\n".join([f"- **{k}**: {v}" for k, v in list(clauses.items())[:3]])

        if is_hi:
            ans = (
                f"### 🧪 आवश्यक परीक्षण और लैब आवश्यकताएं: {std_key}\n\n"
                f"**मानक**: {info.get('title', '')}\n"
                f"**योजना**: {info.get('certification_scheme', 'Scheme-I (ISI Mark)')}\n\n"
                f"#### 🔬 अनिवार्य प्रयोगशाला परीक्षण (Mandatory Tests):\n{tests_str}\n\n"
                f"#### 📋 प्रमुख तकनीकी क्लॉज एवं सीमाएं:\n{clauses_str}\n\n"
                f"#### 🏭 कारखाने में लैब उपकरण:\n"
                f"निर्माता को अपने कारखाने में परीक्षण एवं निरीक्षण योजना (SIT - Scheme of Inspection and Testing) के अनुसार उपर्युक्त सभी परीक्षण उपकरण स्थापित करना और NABL कैलिब्रेशन प्रमाणपत्र बनाए रखना अनिवार्य है।\n\n"
                f"> 📌 **प्रमाणन उद्धरण**: **{std_key}**, {list(clauses.keys())[0] if clauses else 'Testing Clauses'}"
            )
        else:
            ans = (
                f"### 🧪 Mandatory Testing & Laboratory Requirements for {std_key}\n\n"
                f"**Standard**: {info.get('title', '')}\n"
                f"**Certification Scheme**: {info.get('certification_scheme', 'Scheme-I (ISI Mark)')}\n"
                f"**Quality Control Order Status**: {info.get('mandatory_qco', 'Mandatory QCO')}\n\n"
                f"#### 🔬 Required Conformity & Laboratory Tests:\n{tests_str}\n\n"
                f"#### 📋 Critical Standard Clauses & Permissible Limits:\n{clauses_str}\n\n"
                f"#### 🏭 In-House Testing Facility Requirements:\n"
                f"Under the BIS Scheme of Inspection and Testing (SIT), the factory must possess in-house calibrated test equipment, qualified QC testing chemists, and maintain complete day-to-day batch test logs for routine & acceptance tests.\n\n"
                f"> 📌 **Citation**: **{std_key}**, {list(clauses.keys())[0] if clauses else 'Testing Clauses'} — *{info.get('title', '')}*"
            )

        return {
            "answer": ans,
            "citations": [
                {
                    "standard": std_key,
                    "clause": list(clauses.keys())[0] if clauses else "Testing Specifications",
                    "title": info.get("title", ""),
                    "snippet": f"Mandatory tests: {', '.join(tests[:3])}.",
                    "document": f"{std_key.replace(':', '_').replace(' ', '_')}.pdf",
                    "page": 2
                }
            ],
            "mode": "Sovereign Industry Technical Intelligence"
        }

    def _format_standard_response(self, std_key: str, info: Dict[str, Any], is_hi: bool) -> Dict[str, Any]:
        clauses = info.get("key_clauses", {})
        clauses_str = "\n".join([f"- **{k}**: {v}" for k, v in list(clauses.items())[:4]])

        if is_hi:
            ans = (
                f"### 🏷️ लागू भारतीय मानक: {std_key}\n\n"
                f"**शीर्षक**: {info.get('title', '')}\n"
                f"**श्रेणी**: {info.get('category', '')}\n"
                f"**दायरा (Scope)**: {info.get('scope', '')}\n"
                f"**गुणवत्ता नियंत्रण आदेश (QCO)**: {info.get('mandatory_qco', '')}\n"
                f"**प्रमाणीकरण योजना**: {info.get('certification_scheme', 'Scheme-I (ISI Mark)')}\n\n"
                f"#### 📋 प्रमुख विनिर्देश एवं क्लॉज:\n{clauses_str}\n\n"
                f"> 📌 **प्रमाणन उद्धरण**: **{std_key}**, {list(clauses.keys())[0] if clauses else 'Clause 4.1'} — *{info.get('title', '')}*"
            )
        else:
            ans = (
                f"### 🏷️ Applicable Indian Standard: {std_key}\n\n"
                f"**Standard**: {std_key} — {info.get('title', '')}\n"
                f"**Product Sector**: {info.get('category', '')}\n"
                f"**Scope**: {info.get('scope', '')}\n"
                f"**Compliance Status**: {info.get('mandatory_qco', '')}\n"
                f"**Governing Scheme**: {info.get('certification_scheme', 'Scheme-I')}\n\n"
                f"#### 📋 Key Clauses & Conformity Parameters:\n{clauses_str}\n\n"
                f"> 📌 **Citation**: **{std_key}**, {list(clauses.keys())[0] if clauses else 'Clause 4.1'} — *{info.get('title', '')}*"
            )

        return {
            "answer": ans,
            "citations": [
                {
                    "standard": std_key,
                    "clause": list(clauses.keys())[0] if clauses else "General Requirements",
                    "title": info.get("title", ""),
                    "snippet": f"Scope: {info.get('scope', '')[:120]}...",
                    "document": f"{std_key.replace(':', '_').replace(' ', '_')}.pdf",
                    "page": 1
                }
            ],
            "mode": "Sovereign Industry Technical Intelligence"
        }

    def _check_specific_standard(self, query: str, is_hi: bool) -> Optional[Dict[str, Any]]:
        # Check if user mentioned exact standard like IS 10500, IS 14543, IS 1293
        for k, v in self.catalog.items():
            std_short = k.split(":")[0]  # e.g. "IS 10500"
            if std_short.lower() in query.lower():
                return self._format_standard_response(k, v, is_hi)
        return None

    def _synthesize_rag_bis(self, query: str, docs: List[Any], is_hi: bool) -> Optional[Dict[str, Any]]:
        """Synthesize response from retrieved documents if they contain BIS standard clauses."""
        bis_chunks = [d for d in docs if any(k in d.page_content.lower() for k in ["is ", "bis", "indian standard", "clause", "qco"])]
        if not bis_chunks:
            return None

        top_chunk = bis_chunks[0]

        # Guard against irrelevant topic hallucination
        query_words = set(re.findall(r'[a-zA-Z\u0900-\u097F]{4,}', query.lower()))
        stop_words = {"standard", "standards", "which", "what", "where", "about", "indian", "codes", "testing", "needed", "applies", "under", "these", "code"}
        substantive = query_words - stop_words
        if substantive and not any(w in top_chunk.page_content.lower() for w in substantive):
            return None

        text_snip = top_chunk.page_content.strip()
        doc_name = top_chunk.metadata.get("filename", "Indian_Standards_BIS.pdf")
        page = top_chunk.metadata.get("page", 1)

        ans = (
            f"### 📖 BIS Standards Knowledge Retrieval\n\n"
            f"Based on the official Indian Standards documentation:\n\n"
            f"{text_snip}\n\n"
            f"> 📌 **Citation**: **{doc_name}**, Section/Page {page}"
        )
        return {
            "answer": ans,
            "citations": [
                {
                    "standard": "Indian Standards Documentation",
                    "clause": f"Section Page {page}",
                    "title": doc_name,
                    "snippet": text_snip[:150] + "...",
                    "document": doc_name,
                    "page": page
                }
            ],
            "mode": "Sovereign BIS RAG Engine"
        }

    # ──────────────────────────────────────────────────────────────────────────
    # 6. "I DON'T KNOW" HANDLING WITH BIS HELPLINE FALLBACK
    # ──────────────────────────────────────────────────────────────────────────
    def _build_i_dont_know_response(self, query: str, is_hi: bool) -> Dict[str, Any]:
        if is_hi:
            ans = (
                "### ℹ️ सूचना उपलब्ध नहीं (Not Found in Standards Repository)\n\n"
                f"मुझे इस विशिष्ट प्रश्न: *'{query}'* के संबंध में वर्तमान अनुक्रमित भारतीय मानकों (IS Codes) में कोई आधिकारिक दस्तावेजीकरण नहीं मिला। गलत या भ्रामक उत्तर से बचने के लिए मैं अनुमान नहीं लगा रहा हूँ।\n\n"
                "सटीक एवं नवीनतम आधिकारिक सहायता के लिए कृपया भारतीय मानक ब्यूरो (BIS) के आधिकारिक चैनलों से संपर्क करें:\n\n"
                "- 📞 **राष्ट्रीय टोल-फ्री हेल्पलाइन**: **1800-11-1255** या **1915**\n"
                "- 🌐 **आधिकारिक पोर्टल**: [www.bis.gov.in](https://www.bis.gov.in) | [www.manakonline.in](https://www.manakonline.in)\n"
                "- 📱 **मोबाइल ऐप**: **BIS Care App** (Android / iOS)\n"
                "- ✉️ **ईमेल**: `info@bis.gov.in` / `complaints@bis.gov.in`\n"
                "- 🏢 **मुख्यालय**: मानक भवन, 9 बहादुर शाह ज़फ़र मार्ग, नई दिल्ली 110002"
            )
        else:
            ans = (
                "### ℹ️ Information Not Found in Current BIS Repository\n\n"
                f"I do not have verified technical documentation for your specific query: *\"{query}\"* in the indexed Indian Standards repository. To ensure regulatory precision, I do not make speculative guesses.\n\n"
                "For authoritative clarification, please consult the official Bureau of Indian Standards (BIS) helpdesk and portals:\n\n"
                "- 📞 **National Toll-Free Helpline**: **1800-11-1255** / **1915** (Ministry of Consumer Affairs)\n"
                "- 🌐 **Official Web Portals**: [www.bis.gov.in](https://www.bis.gov.in) | [www.manakonline.in](https://www.manakonline.in)\n"
                "- 📱 **Official Mobile App**: **BIS Care App** (Free on Google Play Store & Apple App Store)\n"
                "- ✉️ **Official Support Email**: `info@bis.gov.in` / `complaints@bis.gov.in`\n"
                "- 🏢 **Headquarters**: Manak Bhavan, 9 Bahadur Shah Zafar Marg, New Delhi 110002, India"
            )

        return {
            "answer": ans,
            "citations": [],
            "mode": "Sovereign BIS Fallback Guardrail"
        }


# Global instance
bis_service = BISService()
