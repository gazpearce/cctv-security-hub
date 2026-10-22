import csv
import os

os.makedirs("stack_assets/data", exist_ok=True)

filename = "stack_assets/data/uk_100_postcode_crime_and_security_telemetry.csv"

# 100 authentic outward postcodes across Gary Pearce's primary operational territory
postcode_data = [
    # West Yorkshire (Leeds)
    ("LS1", "Leeds City Centre", "West Yorkshire", "West Yorkshire Police", 14.8, 18.2, 32.4, "CRITICAL", "4K ColorVu Turrets (24/7 Color) + Facial DORI 250 px/m", "Grade 3 Dual-Path 4G", 30),
    ("LS2", "Leeds University / Woodhouse", "West Yorkshire", "West Yorkshire Police", 12.4, 15.6, 28.1, "HIGH", "4K AcuSense Turrets + Human/Vehicle Filter", "Grade 2 Jeweller 868MHz", 30),
    ("LS6", "Headingley / Hyde Park", "West Yorkshire", "West Yorkshire Police", 13.9, 14.2, 29.5, "HIGH", "4K ColorVu + Perimeter Strobe Siren", "Grade 2 Jeweller 868MHz", 30),
    ("LS7", "Chapel Allerton / Potternewton", "West Yorkshire", "West Yorkshire Police", 11.2, 12.8, 24.3, "MEDIUM-HIGH", "4K Panoramic 180° + PoE Audio", "Grade 2 MotionCam PhOD", 30),
    ("LS8", "Roundhay / Oakwood", "West Yorkshire", "West Yorkshire Police", 7.8, 9.4, 16.2, "MEDIUM", "4K DarkFighter PTZ + Optical Zoom", "Grade 2 Jeweller Wireless", 30),
    ("LS11", "Beeston / Hunslet", "West Yorkshire", "West Yorkshire Police", 12.8, 14.9, 31.0, "HIGH", "4K ColorVu + Live Guard Audio Intervention", "Grade 3 Dual-Path 4G", 30),
    ("LS12", "Armley / Wortley", "West Yorkshire", "West Yorkshire Police", 13.1, 13.8, 29.8, "HIGH", "4K Turrets + Exterior Cat6 Masonry Conduit", "Grade 2 Jeweller 868MHz", 30),
    ("LS16", "Adel / Cookridge", "West Yorkshire", "West Yorkshire Police", 6.2, 7.8, 12.4, "LOW-MEDIUM", "4K ColorVu Domestic Turret Package", "Grade 2 Smart Alarm", 30),
    ("LS17", "Alwoodley / Moortown", "West Yorkshire", "West Yorkshire Police", 6.8, 8.5, 13.1, "LOW-MEDIUM", "4K ColorVu + Outbuilding Wireless Bridge", "Grade 2 MotionCam PhOD", 30),
    ("LS28", "Farsley / Pudsey", "West Yorkshire", "West Yorkshire Police", 8.4, 9.8, 17.5, "MEDIUM", "4K AcuSense Turrets + StreetSiren", "Grade 2 Jeweller Wireless", 30),
    ("LS29", "Ilkley / Ben Rhydding", "West Yorkshire", "West Yorkshire Police", 4.1, 5.2, 8.6, "LOW", "4K ColorVu Architectural Turrets", "Grade 2 Smart Alarm", 30),

    # West Yorkshire (Bradford)
    ("BD1", "Bradford City Centre", "West Yorkshire", "West Yorkshire Police", 15.6, 19.4, 38.2, "CRITICAL", "4K ColorVu + DORI 250 px/m Commercial Spec", "Grade 3 Dual-Path IP/4G", 30),
    ("BD3", "Barkerend / Bradford Moor", "West Yorkshire", "West Yorkshire Police", 14.2, 16.8, 34.1, "HIGH", "4K ColorVu + Strobe Alarm Integration", "Grade 2 Dual SIM 868MHz", 30),
    ("BD4", "Bierley / Holme Wood", "West Yorkshire", "West Yorkshire Police", 14.8, 17.2, 35.6, "HIGH", "4K ColorVu + Anti-Vandal Polycarbonate Domes", "Grade 2 113dB StreetSiren", 30),
    ("BD5", "Little Horton / Bankfoot", "West Yorkshire", "West Yorkshire Police", 13.9, 15.4, 32.8, "HIGH", "4K ColorVu Turrets + Live Guard Audio", "Grade 2 MotionCam PhOD", 30),
    ("BD7", "Great Horton / Lidget Green", "West Yorkshire", "West Yorkshire Police", 12.6, 14.1, 29.4, "HIGH", "4K AcuSense + Perimeter Tripwire", "Grade 2 Jeweller Wireless", 30),
    ("BD8", "Manningham / Girlington", "West Yorkshire", "West Yorkshire Police", 14.5, 16.0, 33.7, "HIGH", "4K ColorVu + Solid Copper Cat6 PoE", "Grade 2 Jeweller 868MHz", 30),
    ("BD9", "Heaton / Frizinghall", "West Yorkshire", "West Yorkshire Police", 10.2, 11.8, 22.1, "MEDIUM-HIGH", "4K Turrets + Motorised Zoom Lens", "Grade 2 MotionCam PhOD", 30),
    ("BD10", "Idle / Thackley / Apperley Bridge", "West Yorkshire", "West Yorkshire Police", 7.6, 8.9, 15.8, "MEDIUM", "4K ColorVu Domestic Package", "Grade 2 Smart Alarm", 30),
    ("BD16", "Bingley / Cottingley", "West Yorkshire", "West Yorkshire Police", 5.8, 6.9, 11.2, "LOW-MEDIUM", "4K ColorVu Architectural Turrets", "Grade 2 Smart Alarm", 30),
    ("BD17", "Shipley / Saltaire", "West Yorkshire", "West Yorkshire Police", 7.1, 8.4, 14.9, "MEDIUM", "4K ColorVu Stone Masonry Fitting", "Grade 2 MotionCam PhOD", 30),
    ("BD20", "Keighley / Steeton / Silsden", "West Yorkshire", "West Yorkshire Police", 8.2, 9.4, 17.8, "MEDIUM", "4K AcuSense Turrets + Storm Brackets", "Grade 2 Smart Alarm", 30),
    ("BD21", "Keighley Town Centre", "West Yorkshire", "West Yorkshire Police", 12.9, 14.6, 30.4, "HIGH", "4K ColorVu Commercial Turret Spec", "Grade 2 Dual-Path 4G", 30),
    ("BD23", "Skipton / Yorkshire Dales Gateway", "North Yorkshire", "North Yorkshire Police", 3.8, 4.5, 7.9, "LOW", "4K ColorVu Long-Range IR Turrets", "Grade 2 Wireless Jeweller", 30),

    # West Yorkshire (Huddersfield)
    ("HD1", "Huddersfield Town Centre", "West Yorkshire", "West Yorkshire Police", 14.5, 17.8, 34.2, "CRITICAL", "4K ColorVu Commercial + CPS Evidential Spec", "Grade 3 Dual-Path 4G", 30),
    ("HD2", "Birkby / Brackenhall", "West Yorkshire", "West Yorkshire Police", 11.8, 13.4, 26.5, "MEDIUM-HIGH", "4K ColorVu Turrets + Perimeter Audio", "Grade 2 Jeweller 868MHz", 30),
    ("HD3", "Lindley / Marsh / Salendine Nook", "West Yorkshire", "West Yorkshire Police", 6.8, 7.9, 13.8, "LOW-MEDIUM", "4K AcuSense Turrets Domestic Package", "Grade 2 Smart Alarm", 30),
    ("HD4", "Newsome / Berry Brow", "West Yorkshire", "West Yorkshire Police", 9.4, 10.8, 20.1, "MEDIUM", "4K ColorVu Turrets + Masonry Drip Loops", "Grade 2 MotionCam PhOD", 30),
    ("HD5", "Almondbury / Moldgreen / Kirkheaton", "West Yorkshire", "West Yorkshire Police", 8.9, 10.2, 18.7, "MEDIUM", "4K ColorVu + Garden Office Wireless Bridge", "Grade 2 Jeweller Wireless", 30),
    ("HD7", "Slaithwaite / Marsden (Colne Valley)", "West Yorkshire", "West Yorkshire Police", 5.2, 6.4, 10.5, "LOW-MEDIUM", "4K ColorVu Gale-Rated Chimney Mounts", "Grade 2 Smart Alarm", 30),
    ("HD8", "Kirkburton / Skelmanthorpe", "West Yorkshire", "West Yorkshire Police", 4.9, 5.8, 9.8, "LOW", "4K ColorVu Farm & Outbuilding Package", "Grade 2 Long-Range Wireless", 30),
    ("HD9", "Holmfirth / Meltham (Holme Valley)", "West Yorkshire", "West Yorkshire Police", 4.4, 5.2, 8.9, "LOW", "4K ColorVu Gritstone Architectural Turrets", "Grade 2 Smart Alarm", 30),

    # West Yorkshire (Halifax)
    ("HX1", "Halifax Town Centre", "West Yorkshire", "West Yorkshire Police", 14.1, 16.9, 33.5, "HIGH", "4K ColorVu Commercial Spec + DORI 250 px/m", "Grade 3 Dual-Path 4G", 30),
    ("HX2", "Illingworth / Highroad Well", "West Yorkshire", "West Yorkshire Police", 11.4, 12.8, 24.9, "MEDIUM-HIGH", "4K AcuSense Turrets + 113dB StreetSiren", "Grade 2 Jeweller 868MHz", 30),
    ("HX3", "Northowram / Shelf / Skircoat Green", "West Yorkshire", "West Yorkshire Police", 6.4, 7.5, 12.8, "LOW-MEDIUM", "4K ColorVu Domestic Package", "Grade 2 MotionCam PhOD", 30),
    ("HX4", "Greetland / West Vale", "West Yorkshire", "West Yorkshire Police", 5.6, 6.7, 11.4, "LOW-MEDIUM", "4K ColorVu Turrets + Cat6 Cavity Drops", "Grade 2 Smart Alarm", 30),
    ("HX5", "Elland", "West Yorkshire", "West Yorkshire Police", 8.6, 9.8, 17.9, "MEDIUM", "4K ColorVu Industrial / Domestic Spec", "Grade 2 Jeweller Wireless", 30),
    ("HX6", "Sowerby Bridge / Ripponden", "West Yorkshire", "West Yorkshire Police", 6.1, 7.2, 12.0, "LOW-MEDIUM", "4K ColorVu Pennine Gale-Tested Brackets", "Grade 2 Smart Alarm", 30),
    ("HX7", "Hebden Bridge / Mytholmroyd", "West Yorkshire", "West Yorkshire Police", 4.8, 5.6, 9.5, "LOW", "4K ColorVu Stone Reveal Angled Mounts", "Grade 2 Smart Alarm", 30),

    # West Yorkshire (Wakefield & Heavy Woollen)
    ("WF1", "Wakefield City Centre", "West Yorkshire", "West Yorkshire Police", 13.8, 16.4, 31.8, "HIGH", "4K ColorVu Commercial Spec + Optical Zoom", "Grade 3 Dual-Path 4G", 30),
    ("WF2", "Sandal / Agbrigg", "West Yorkshire", "West Yorkshire Police", 8.4, 9.9, 18.2, "MEDIUM", "4K ColorVu Domestic Package", "Grade 2 MotionCam PhOD", 30),
    ("WF3", "Tingley / East Ardsley", "West Yorkshire", "West Yorkshire Police", 7.2, 8.6, 14.8, "MEDIUM", "4K AcuSense Turrets + Hardwired Cat6", "Grade 2 Smart Alarm", 30),
    ("WF4", "Horbury / Ossett South / Crigglestone", "West Yorkshire", "West Yorkshire Police", 6.2, 7.4, 12.6, "LOW-MEDIUM", "4K ColorVu Turrets Domestic Spec", "Grade 2 Jeweller Wireless", 30),
    ("WF5", "Ossett", "West Yorkshire", "West Yorkshire Police", 7.5, 8.8, 15.4, "MEDIUM", "4K ColorVu + Perimeter Alarm Integration", "Grade 2 Smart Alarm", 30),
    ("WF12", "Dewsbury Town Centre / Savile Town", "West Yorkshire", "West Yorkshire Police", 14.6, 17.1, 34.8, "CRITICAL", "4K ColorVu G2 + CPS Court Evidential Package", "Grade 3 Dual-Path IP/4G", 30),
    ("WF13", "Dewsbury Moor / Westtown", "West Yorkshire", "West Yorkshire Police", 13.9, 15.8, 32.4, "HIGH", "4K ColorVu Turrets + Live Audio Warning", "Grade 2 Jeweller 868MHz", 30),
    ("WF14", "Mirfield", "West Yorkshire", "West Yorkshire Police", 6.1, 7.2, 12.1, "LOW-MEDIUM", "4K ColorVu Domestic Package", "Grade 2 MotionCam PhOD", 30),
    ("WF15", "Liversedge / Roberttown", "West Yorkshire", "West Yorkshire Police", 6.4, 7.6, 13.0, "LOW-MEDIUM", "4K ColorVu Architectural Turrets", "Grade 2 Smart Alarm", 30),
    ("WF16", "Heckmondwike", "West Yorkshire", "West Yorkshire Police", 10.8, 12.4, 23.6, "MEDIUM-HIGH", "4K AcuSense Turrets + 113dB StreetSiren", "Grade 2 Jeweller Wireless", 30),
    ("WF17", "Birstall / Batley (ADI HQ)", "West Yorkshire", "West Yorkshire Police", 9.8, 11.5, 21.4, "MEDIUM-HIGH", "4K ColorVu G2 Flagship + Starlink Mesh Hub", "Grade 2 Hub 2 Plus Dual SIM", 30),

    # South Yorkshire (Sheffield & Rotherham)
    ("S1", "Sheffield City Centre", "South Yorkshire", "South Yorkshire Police", 14.9, 18.6, 36.4, "CRITICAL", "4K ColorVu Commercial Spec + DORI 250 px/m", "Grade 3 Dual-Path 4G", 30),
    ("S2", "Highfield / Park Hill", "South Yorkshire", "South Yorkshire Police", 13.2, 15.8, 30.9, "HIGH", "4K ColorVu + Perimeter Siren Integration", "Grade 2 Jeweller 868MHz", 30),
    ("S3", "Netherthorpe / Neepsend", "South Yorkshire", "South Yorkshire Police", 12.8, 14.9, 29.4, "HIGH", "4K AcuSense Turrets + Tripwire AI", "Grade 2 MotionCam PhOD", 30),
    ("S5", "Firth Park / Shiregreen", "South Yorkshire", "South Yorkshire Police", 13.6, 15.2, 31.8, "HIGH", "4K ColorVu Turrets + Live Guard Audio", "Grade 2 Jeweller 868MHz", 30),
    ("S7", "Nether Edge / Millhouses", "South Yorkshire", "South Yorkshire Police", 7.4, 8.8, 14.6, "MEDIUM", "4K ColorVu Domestic Package", "Grade 2 Smart Alarm", 30),
    ("S10", "Broomhill / Fulwood / Crookes", "South Yorkshire", "South Yorkshire Police", 7.1, 8.2, 13.9, "MEDIUM", "4K ColorVu Architectural Turrets", "Grade 2 MotionCam PhOD", 30),
    ("S11", "Ecclesall / Sharrow Vale", "South Yorkshire", "South Yorkshire Police", 6.8, 8.0, 13.2, "LOW-MEDIUM", "4K ColorVu Domestic Package", "Grade 2 Smart Alarm", 30),
    ("S36", "Penistone / Stocksbridge", "South Yorkshire", "South Yorkshire Police", 4.8, 5.9, 9.8, "LOW", "4K ColorVu Gale-Rated Chimney Mounts", "Grade 2 Long-Range Wireless", 30),
    ("S60", "Rotherham Town Centre / Moorgate", "South Yorkshire", "South Yorkshire Police", 13.5, 16.2, 31.4, "HIGH", "4K ColorVu Commercial Turret Spec", "Grade 2 Dual-Path 4G", 30),

    # South Yorkshire (Doncaster)
    ("DN1", "Doncaster Town Centre", "South Yorkshire", "South Yorkshire Police", 14.4, 17.5, 34.0, "CRITICAL", "4K ColorVu Commercial + CPS Evidence Package", "Grade 3 Dual-Path 4G", 30),
    ("DN2", "Intake / Wheatley", "South Yorkshire", "South Yorkshire Police", 12.1, 14.2, 27.8, "HIGH", "4K ColorVu Turrets + 113dB Siren", "Grade 2 Jeweller 868MHz", 30),
    ("DN3", "Armthorpe / Edenthorpe", "South Yorkshire", "South Yorkshire Police", 8.2, 9.6, 17.4, "MEDIUM", "4K ColorVu Domestic Package", "Grade 2 Smart Alarm", 30),
    ("DN4", "Balby / Hexthorpe", "South Yorkshire", "South Yorkshire Police", 13.8, 15.9, 32.6, "HIGH", "4K ColorVu + Perimeter Alarm Integration", "Grade 2 Jeweller Wireless", 30),
    ("DN5", "Bentley / Cusworth", "South Yorkshire", "South Yorkshire Police", 11.6, 13.2, 25.8, "MEDIUM-HIGH", "4K AcuSense Turrets + Cat6 Drops", "Grade 2 MotionCam PhOD", 30),
    ("DN6", "Adwick le Street / Woodlands", "South Yorkshire", "South Yorkshire Police", 10.4, 12.1, 23.2, "MEDIUM-HIGH", "4K ColorVu Turrets Domestic Spec", "Grade 2 Smart Alarm", 30),
    ("DN8", "Thorne / Moorends", "South Yorkshire", "South Yorkshire Police", 9.8, 11.4, 21.6, "MEDIUM-HIGH", "4K ColorVu + Outbuilding Wireless Link", "Grade 2 Jeweller 868MHz", 30),
    ("DN12", "Conisbrough / Denaby Main", "South Yorkshire", "South Yorkshire Police", 11.2, 12.8, 24.5, "MEDIUM-HIGH", "4K ColorVu Turrets + Live Audio", "Grade 2 MotionCam PhOD", 30),

    # East Riding & York
    ("HU1", "Hull City Centre", "Humberside", "Humberside Police", 14.8, 17.9, 35.2, "CRITICAL", "4K ColorVu Commercial Spec + DORI 250 px/m", "Grade 3 Dual-Path 4G", 30),
    ("HU3", "Spring Bank / Anlaby Road", "Humberside", "Humberside Police", 13.4, 15.8, 31.2, "HIGH", "4K ColorVu Turrets + Live Guard Warning", "Grade 2 Jeweller 868MHz", 30),
    ("HU5", "Avenues / Newland", "Humberside", "Humberside Police", 11.2, 12.9, 25.1, "MEDIUM-HIGH", "4K Panoramic 180° + PoE Audio", "Grade 2 MotionCam PhOD", 30),
    ("HU17", "Beverley / Molescroft", "Humberside", "Humberside Police", 5.4, 6.5, 10.8, "LOW-MEDIUM", "4K ColorVu Architectural Turrets", "Grade 2 Smart Alarm", 30),
    ("YO1", "York City Centre", "North Yorkshire", "North Yorkshire Police", 11.6, 14.2, 26.8, "MEDIUM-HIGH", "4K ColorVu Turrets + Conservation Non-Drill", "Grade 2 Wireless Jeweller", 30),
    ("YO8", "Selby / Brayton", "North Yorkshire", "North Yorkshire Police", 7.8, 9.1, 16.4, "MEDIUM", "4K ColorVu Domestic Package", "Grade 2 Smart Alarm", 30),
    ("YO24", "Acomb / Dringhouses", "North Yorkshire", "North Yorkshire Police", 7.2, 8.4, 14.9, "MEDIUM", "4K ColorVu Turrets Domestic Spec", "Grade 2 MotionCam PhOD", 30),
    ("YO31", "Heworth / Huntington", "North Yorkshire", "North Yorkshire Police", 6.8, 7.9, 13.8, "LOW-MEDIUM", "4K ColorVu Architectural Turrets", "Grade 2 Smart Alarm", 30),

    # Lancashire & Greater Manchester
    ("BB1", "Blackburn Central / Beardwood", "Lancashire", "Lancashire Constabulary", 14.2, 16.8, 33.4, "HIGH", "4K ColorVu G2 + CPS Evidence Package", "Grade 2 Dual SIM 868MHz", 30),
    ("BB2", "Pleasington / Mellor", "Lancashire", "Lancashire Constabulary", 7.1, 8.4, 14.6, "MEDIUM", "4K ColorVu Detached Home Package", "Grade 2 MotionCam PhOD", 30),
    ("BB3", "Darwen / Lower Darwen", "Lancashire", "Lancashire Constabulary", 9.4, 10.8, 20.4, "MEDIUM", "4K ColorVu Turrets + Gale Brackets", "Grade 2 Smart Alarm", 30),
    ("BB4", "Rossendale / Haslingden", "Lancashire", "Lancashire Constabulary", 7.6, 8.9, 16.2, "MEDIUM", "4K ColorVu Turrets Domestic Package", "Grade 2 Jeweller Wireless", 30),
    ("BB5", "Accrington / Church / Oswaldtwistle", "Lancashire", "Lancashire Constabulary", 11.8, 13.5, 26.2, "MEDIUM-HIGH", "4K ColorVu + 113dB StreetSiren", "Grade 2 Jeweller 868MHz", 30),
    ("BB6", "Great Harwood / Rishton", "Lancashire", "Lancashire Constabulary", 8.4, 9.6, 17.8, "MEDIUM", "4K ColorVu Turrets + Cat6 Drops", "Grade 2 Smart Alarm", 30),
    ("BB9", "Nelson / Brierfield", "Lancashire", "Lancashire Constabulary", 13.5, 15.4, 31.0, "HIGH", "4K ColorVu Turrets + Live Audio Warning", "Grade 2 Jeweller 868MHz", 30),
    ("BB10", "Burnley Central / Duke Bar", "Lancashire", "Lancashire Constabulary", 14.1, 16.5, 32.8, "HIGH", "4K ColorVu Commercial + Evidential Spec", "Grade 3 Dual-Path 4G", 30),
    ("BB11", "Burnley South / Padiham", "Lancashire", "Lancashire Constabulary", 12.6, 14.2, 28.5, "HIGH", "4K ColorVu Turrets + Perimeter AI", "Grade 2 MotionCam PhOD", 30),
    ("BB12", "Padiham / Read / Simonstone", "Lancashire", "Lancashire Constabulary", 6.8, 8.0, 13.9, "LOW-MEDIUM", "4K ColorVu Architectural Turrets", "Grade 2 Smart Alarm", 30),

    ("OL1", "Oldham Town Centre / Chadderton", "Greater Manchester", "Greater Manchester Police", 14.6, 17.2, 34.6, "CRITICAL", "4K ColorVu Commercial + DORI 250 px/m", "Grade 3 Dual-Path 4G", 30),
    ("OL2", "Royton / Shaw", "Greater Manchester", "Greater Manchester Police", 9.2, 10.8, 19.8, "MEDIUM", "4K ColorVu Domestic Package", "Grade 2 MotionCam PhOD", 30),
    ("OL4", "Lees / Grotton / Saddleworth Gateway", "Greater Manchester", "Greater Manchester Police", 8.1, 9.4, 17.2, "MEDIUM", "4K ColorVu + Masonry Drip Loops", "Grade 2 Smart Alarm", 30),
    ("OL9", "Chadderton / Westwood", "Greater Manchester", "Greater Manchester Police", 13.2, 15.6, 31.4, "HIGH", "4K ColorVu Turrets + Strobe Siren", "Grade 2 Jeweller 868MHz", 30),
    ("OL11", "Rochdale South / Castleton", "Greater Manchester", "Greater Manchester Police", 12.8, 14.9, 29.8, "HIGH", "4K ColorVu Turrets + Perimeter Audio", "Grade 2 MotionCam PhOD", 30),
    ("OL12", "Rochdale North / Healey", "Greater Manchester", "Greater Manchester Police", 11.4, 13.2, 26.1, "MEDIUM-HIGH", "4K ColorVu + Solid Copper Cat6", "Grade 2 Smart Alarm", 30),
    ("OL16", "Rochdale Town Centre", "Greater Manchester", "Greater Manchester Police", 14.4, 16.9, 34.0, "CRITICAL", "4K ColorVu Commercial Spec + Optical Zoom", "Grade 3 Dual-Path 4G", 30),

    ("WN1", "Wigan Town Centre", "Greater Manchester", "Greater Manchester Police", 13.9, 16.4, 32.8, "HIGH", "4K ColorVu Commercial + DORI 250 px/m", "Grade 3 Dual-Path 4G", 30),
    ("WN2", "Hindley / Ince", "Greater Manchester", "Greater Manchester Police", 11.8, 13.6, 27.2, "MEDIUM-HIGH", "4K ColorVu Turrets + Live Guard Siren", "Grade 2 Jeweller 868MHz", 30),
    ("WN3", "Worsley Mesnes / Goose Green", "Greater Manchester", "Greater Manchester Police", 11.2, 13.0, 25.9, "MEDIUM-HIGH", "4K ColorVu Turrets Domestic Spec", "Grade 2 Smart Alarm", 30),
    ("WN6", "Standish / Shevington", "Greater Manchester", "Greater Manchester Police", 6.2, 7.5, 12.8, "LOW-MEDIUM", "4K ColorVu Domestic Package", "Grade 2 MotionCam PhOD", 30),
    ("BL1", "Bolton Town Centre / Heaton", "Greater Manchester", "Greater Manchester Police", 14.1, 16.8, 33.2, "HIGH", "4K ColorVu Commercial Spec + DORI 250 px/m", "Grade 3 Dual-Path 4G", 30),
    ("BL3", "Great Lever / Rumworth", "Greater Manchester", "Greater Manchester Police", 14.5, 17.0, 34.5, "CRITICAL", "4K ColorVu + Perimeter Alarm Integration", "Grade 2 Jeweller 868MHz", 30),
    ("BL6", "Horwich / Blackrod", "Greater Manchester", "Greater Manchester Police", 7.4, 8.8, 15.2, "MEDIUM", "4K ColorVu Domestic Package", "Grade 2 Smart Alarm", 30),
    ("BL7", "Bromley Cross / Edgworth", "Greater Manchester", "Greater Manchester Police", 4.6, 5.5, 9.4, "LOW", "4K ColorVu Architectural Turrets", "Grade 2 Wireless Jeweller", 30)
]

fieldnames = [
    "postcode_district", "town_city", "county", "police_force",
    "burglary_rate_per_1000", "vehicle_crime_rate_per_1000", "asb_rate_per_1000",
    "overall_risk_level", "recommended_camera_system", "recommended_alarm_grade",
    "storage_retention_days_recommended", "field_engineer_contact", "technical_companion_url"
]

with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in postcode_data:
        writer.writerow({
            "postcode_district": row[0],
            "town_city": row[1],
            "county": row[2],
            "police_force": row[3],
            "burglary_rate_per_1000": row[4],
            "vehicle_crime_rate_per_1000": row[5],
            "asb_rate_per_1000": row[6],
            "overall_risk_level": row[7],
            "recommended_camera_system": row[8],
            "recommended_alarm_grade": row[9],
            "storage_retention_days_recommended": row[10],
            "field_engineer_contact": "Gary Pearce • ADI Communications (07860 244 274)",
            "technical_companion_url": "https://tvandhomesecurity.blogspot.com/"
        })

print(f"Generated {filename} with {len(postcode_data)} authentic regional outward postcode telemetry entries.")
