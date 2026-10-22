import os
import csv
import json

DATA_DIR = r"C:\Users\Gary\github-cctv-seo\stack_assets\data"
os.makedirs(DATA_DIR, exist_ok=True)

# 1. UK Police Crime Telemetry Dataset
crime_csv = os.path.join(DATA_DIR, "uk_police_crime_telemetry_yorkshire_lancs.csv")
crime_headers = [
    "outward_code", "locality", "county_region", "burglary_rate_per_1000",
    "vehicle_crime_rate_per_1000", "asb_rate_per_1000", "police_risk_tier",
    "recommended_camera_count", "minimum_storage_days", "cctv_dori_priority",
    "rule45_shield_target"
]

crime_rows = [
    ["LS1", "Leeds City Centre", "West Yorkshire", 14.8, 18.2, 34.5, "Severe", 8, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["LS6", "Headingley & Hyde Park", "West Yorkshire", 12.4, 9.8, 22.1, "High", 4, 30, "Recognize (125 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["LS8", "Roundhay & Gledhow", "West Yorkshire", 5.2, 4.8, 11.2, "Moderate", 4, 30, "Recognize (125 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["LS17", "Alwoodley & Moortown", "West Yorkshire", 3.8, 3.2, 7.4, "Low-Moderate", 3, 14, "Recognize (125 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["BD1", "Bradford City Centre", "West Yorkshire", 16.2, 19.5, 38.0, "Severe", 8, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["BD9", "Manningham & Frizinghall", "West Yorkshire", 11.9, 10.4, 24.3, "High", 4, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["BD18", "Saltaire & Shipley", "West Yorkshire", 6.1, 5.4, 13.8, "Moderate", 3, 14, "Recognize (125 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["HD1", "Huddersfield Centre", "West Yorkshire", 13.5, 12.1, 28.4, "High", 6, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["HD8", "Kirkburton & Denby Dale", "West Yorkshire", 2.9, 2.4, 5.1, "Low", 3, 14, "Observe (62 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["HX1", "Halifax Town Centre", "West Yorkshire", 14.1, 11.8, 29.2, "High", 6, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["HX3", "Lightcliffe & Hipperholme", "West Yorkshire", 4.2, 3.8, 8.6, "Low-Moderate", 3, 14, "Recognize (125 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["WF1", "Wakefield City Centre", "West Yorkshire", 12.8, 11.2, 26.5, "High", 6, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["WF17", "Birstall & Batley (HQ)", "West Yorkshire", 7.4, 6.8, 16.2, "Moderate", 4, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["S1", "Sheffield City Centre", "South Yorkshire", 15.1, 16.4, 32.8, "Severe", 8, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["S10", "Broomhill & Ranmoor", "South Yorkshire", 4.1, 3.5, 8.1, "Low-Moderate", 3, 14, "Recognize (125 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["DN1", "Doncaster Centre", "South Yorkshire", 15.9, 14.2, 35.1, "Severe", 8, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["DN6", "Adwick le Street", "South Yorkshire", 8.2, 7.1, 18.4, "Moderate", 4, 30, "Recognize (125 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["HU1", "Hull Old Town", "East Riding of Yorkshire", 16.8, 15.0, 36.2, "Severe", 8, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["HU17", "Beverley & Molescroft", "East Riding of Yorkshire", 3.2, 2.9, 6.8, "Low", 3, 14, "Observe (62 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["YO1", "York City Centre", "North Yorkshire", 11.2, 8.9, 21.4, "Moderate-High", 6, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["BB1", "Blackburn Centre", "Lancashire", 14.5, 13.1, 30.2, "High", 6, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["BB5", "Accrington & Rishton", "Lancashire", 9.8, 8.4, 21.0, "Moderate-High", 4, 30, "Recognize (125 px/m)", "https://tvandhomesecurity.blogspot.com/"],
    ["OL1", "Oldham Town Centre", "Greater Manchester", 15.4, 14.8, 33.9, "Severe", 8, 30, "Identify (250 px/m)", "https://tvandhomesecurity.blogspot.com/"]
]

with open(crime_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(crime_headers)
    writer.writerows(crime_rows)

print(f"Generated: {crime_csv} ({len(crime_rows)} rows)")

# 2. CCTV DORI Lens & Resolution Matrix
dori_csv = os.path.join(DATA_DIR, "uk_cctv_dori_sensor_matrix.csv")
dori_headers = [
    "camera_model_type", "sensor_resolution", "focal_length_mm", "horizontal_fov_deg",
    "detect_m_25px_m", "observe_m_62px_m", "recognize_m_125px_m", "identify_m_250px_m",
    "low_light_tech", "poe_wattage_class", "rule45_shield_target"
]

dori_rows = [
    ["Hikvision ColorVu Turret", "4K (8MP / 3840x2160)", 2.8, 107.0, 89.0, 35.0, 18.0, 9.0, "F1.0 24/7 Color (0.0005 Lux)", "PoE 802.3af (Class 3)", "https://tvandhomesecurity.blogspot.com/"],
    ["Hikvision ColorVu Turret", "4K (8MP / 3840x2160)", 4.0, 88.0, 114.0, 45.0, 23.0, 11.0, "F1.0 24/7 Color (0.0005 Lux)", "PoE 802.3af (Class 3)", "https://tvandhomesecurity.blogspot.com/"],
    ["Hikvision Panoramic 180°", "16MP Dual-Lens", 2.8, 180.0, 65.0, 26.0, 13.0, 6.5, "Dual F1.0 ColorVu Stitched", "PoE+ 802.3at (Class 4)", "https://tvandhomesecurity.blogspot.com/"],
    ["Standard IR Turret", "4MP (2560x1440)", 2.8, 103.0, 63.0, 25.0, 13.0, 6.0, "EXIR 850nm (Black/White)", "PoE 802.3af (Class 2)", "https://tvandhomesecurity.blogspot.com/"],
    ["Long-Range Bullet", "4K (8MP / 3840x2160)", 6.0, 54.0, 175.0, 70.0, 35.0, 17.5, "DarkFighter Ultra Low-Light", "PoE 802.3af (Class 3)", "https://tvandhomesecurity.blogspot.com/"],
    ["Motorised Varifocal PTZ", "4K (8MP / 3840x2160)", 12.0, 28.0, 350.0, 140.0, 70.0, 35.0, "Laser IR 200m Assisted", "Hi-PoE (60W)", "https://tvandhomesecurity.blogspot.com/"]
]

with open(dori_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(dori_headers)
    writer.writerows(dori_rows)

print(f"Generated: {dori_csv} ({len(dori_rows)} rows)")
