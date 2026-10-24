#!/usr/bin/env python3
"""
build_master_expanded_catalogue.py
==================================
Builds the comprehensive master service, equipment, technology, and repair catalogue
for ADI Communications (Gary Pearce).

Covers:
1. Brands (95+ manufacturers across CCTV, Alarms, Networking, Cabling, Audio, TV)
2. Hardware & Models (40+ specific devices)
3. Cabling Standards (Cat5e–Cat8, WF100, Fibre)
4. Mounting Systems (CoreFix, SnapToggle, Chimney Lashing, T&K Brackets)
5. Diagnostic Problems & Root Cause Solutions
6. Primary Installation Services
7. Micro-Repair Services & Connection Fixes (RJ45 crimps, TV aerial sockets, F-connectors, cable splices)
8. Complete Regional Coverage Census (100+ towns & postcodes across 6 northern UK regions)
"""

import os
import json
from pathlib import Path

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")
CATALOGUE_DIR = REPO_ROOT / "catalogue"
CATALOGUE_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. COMPREHENSIVE BRANDS (95+ Major Brands)
# -------------------------------------------------------------
BRANDS = [
    # CCTV & Video Surveillance
    {"id": "brand:hikvision", "name": "Hikvision", "category": "CCTV & Video Surveillance", "scope": ["Supply", "Install", "Configure", "Repair", "Firmware Service"], "tier": "Commercial / Premium Domestic"},
    {"id": "brand:dahua", "name": "Dahua Technology", "category": "CCTV & Video Surveillance", "scope": ["Supply", "Install", "Configure", "Repair"], "tier": "Commercial / Smart Domestic"},
    {"id": "brand:uniview", "name": "Uniview (UNV)", "category": "CCTV & Video Surveillance", "scope": ["Supply", "Install", "Configure", "Repair"], "tier": "Enterprise / Commercial"},
    {"id": "brand:reolink", "name": "Reolink", "category": "CCTV & Video Surveillance", "scope": ["Supply", "Install", "Configure", "Repair"], "tier": "Domestic PoE / Standalone"},
    {"id": "brand:spro", "name": "SPRO", "category": "CCTV & Video Surveillance", "scope": ["Supply", "Install", "Configure", "Repair"], "tier": "UK Trade Commercial"},
    {"id": "brand:hilook", "name": "HiLook (by Hikvision)", "category": "CCTV & Video Surveillance", "scope": ["Supply", "Install", "Configure", "Repair"], "tier": "Cost-Effective Domestic"},
    {"id": "brand:qvis", "name": "Qvis Labs", "category": "CCTV & Video Surveillance", "scope": ["Supply", "Install", "Configure", "Repair"], "tier": "UK Trade Commercial"},
    {"id": "brand:axis", "name": "Axis Communications", "category": "CCTV & Video Surveillance", "scope": ["Configure", "Repair", "Maintain"], "tier": "High-End Enterprise"},
    {"id": "brand:hanwha", "name": "Hanwha Vision", "category": "CCTV & Video Surveillance", "scope": ["Configure", "Repair", "Maintain"], "tier": "Commercial Enterprise"},
    {"id": "brand:bosch-security", "name": "Bosch Security", "category": "CCTV & Video Surveillance", "scope": ["Configure", "Repair", "Maintain"], "tier": "Commercial Enterprise"},
    {"id": "brand:honeywell-security", "name": "Honeywell Security", "category": "CCTV & Video Surveillance", "scope": ["Configure", "Repair"], "tier": "Commercial Enterprise"},
    {"id": "brand:avigilon", "name": "Avigilon (Motorola)", "category": "CCTV & Video Surveillance", "scope": ["Configure", "Maintain"], "tier": "Enterprise AI Surveillance"},
    {"id": "brand:pelco", "name": "Pelco", "category": "CCTV & Video Surveillance", "scope": ["Configure", "Repair"], "tier": "Enterprise"},
    {"id": "brand:mobotix", "name": "Mobotix", "category": "CCTV & Video Surveillance", "scope": ["Configure", "Repair"], "tier": "Specialist Industrial"},
    {"id": "brand:vivotek", "name": "Vivotek", "category": "CCTV & Video Surveillance", "scope": ["Configure", "Repair"], "tier": "Commercial IP"},
    {"id": "brand:provision-isr", "name": "Provision-ISR", "category": "CCTV & Video Surveillance", "scope": ["Install", "Configure"], "tier": "Commercial IP"},
    {"id": "brand:milesight", "name": "Milesight", "category": "CCTV & Video Surveillance", "scope": ["Install", "Configure"], "tier": "Commercial AI / IoT"},
    {"id": "brand:genie-cctv", "name": "Genie CCTV", "category": "CCTV & Video Surveillance", "scope": ["Repair", "Maintain"], "tier": "UK Trade"},
    {"id": "brand:vista-cctv", "name": "Vista CCTV (Norbain)", "category": "CCTV & Video Surveillance", "scope": ["Repair", "Maintain"], "tier": "UK Trade Legacy"},
    {"id": "brand:swann", "name": "Swann", "category": "CCTV & Video Surveillance", "scope": ["Repair", "Replace with Hardwired PoE"], "tier": "Consumer Retail"},
    {"id": "brand:lorex", "name": "Lorex", "category": "CCTV & Video Surveillance", "scope": ["Configure", "Repair"], "tier": "Consumer Retail"},
    {"id": "brand:annke", "name": "Annke", "category": "CCTV & Video Surveillance", "scope": ["Configure", "Repair"], "tier": "Consumer Retail"},

    # Smart Doorbells & Battery Cameras
    {"id": "brand:ring", "name": "Ring (Amazon)", "category": "Smart Doorbells & Cameras", "scope": ["Hardwired Installation", "Transformer Fitting", "Chime Bypass", "Configure"], "tier": "Consumer Smart Home"},
    {"id": "brand:eufy", "name": "Eufy Security (Anker)", "category": "Smart Doorbells & Cameras", "scope": ["Hardwired Installation", "HomeBase Integration", "Configure"], "tier": "Consumer Local Storage"},
    {"id": "brand:nest", "name": "Google Nest", "category": "Smart Doorbells & Cameras", "scope": ["Hardwired Installation", "Chime Connector Setup", "Configure"], "tier": "Consumer Smart Home"},
    {"id": "brand:arlo", "name": "Arlo", "category": "Smart Doorbells & Cameras", "scope": ["Installation", "Solar Link", "Hub Setup"], "tier": "Consumer Wireless"},
    {"id": "brand:tapo", "name": "TP-Link Tapo", "category": "Smart Home / CCTV", "scope": ["Installation", "SD Card Local Storage Setup", "Configure"], "tier": "Consumer Budget"},

    # Alarms & Access Control
    {"id": "brand:ajax", "name": "Ajax Systems", "category": "Intruder Alarms", "scope": ["Authorised Supply", "Install", "Grade 2 Certify", "Maintain"], "tier": "Grade 2 Wireless & Hybrid"},
    {"id": "brand:pyronix", "name": "Pyronix (Hikvision)", "category": "Intruder Alarms", "scope": ["Repair", "Battery Service", "Upgrade to Ajax"], "tier": "UK Trade Standard"},
    {"id": "brand:texecom", "name": "Texecom", "category": "Intruder Alarms", "scope": ["Repair", "Battery Service", "Upgrade to Ajax"], "tier": "Commercial UK Trade"},
    {"id": "brand:scantronic", "name": "Scantronic (Eaton)", "category": "Intruder Alarms", "scope": ["Repair", "Battery Service", "Upgrade to Ajax"], "tier": "UK Legacy"},
    {"id": "brand:risco", "name": "Risco Group", "category": "Intruder Alarms", "scope": ["Repair", "Service", "Upgrade"], "tier": "Commercial / Domestic"},
    {"id": "brand:visonic", "name": "Visonic (Johnson Controls)", "category": "Intruder Alarms", "scope": ["Repair", "Battery Service", "Upgrade"], "tier": "UK Legacy Wireless"},
    {"id": "brand:honeywell-galaxy", "name": "Honeywell Galaxy", "category": "Intruder Alarms", "scope": ["Service", "Maintain"], "tier": "High-Security Commercial"},
    {"id": "brand:yale-alarm", "name": "Yale Smart Alarms", "category": "Intruder Alarms", "scope": ["Troubleshoot", "Upgrade to Ajax Grade 2"], "tier": "Consumer DIY"},
    {"id": "brand:simplisafe", "name": "SimpliSafe", "category": "Intruder Alarms", "scope": ["Troubleshoot", "Replace with Grade 2"], "tier": "Consumer DIY"},
    {"id": "brand:paxton", "name": "Paxton Access (Net2)", "category": "Access Control & Intercom", "scope": ["Install", "Configure", "Maintain"], "tier": "Commercial UK Market Leader"},
    {"id": "brand:videx", "name": "Videx", "category": "Door Entry & Intercom", "scope": ["Install", "Repair", "Maintain"], "tier": "Commercial / Residential"},
    {"id": "brand:comelit", "name": "Comelit", "category": "Door Entry & Intercom", "scope": ["Install", "Repair", "Maintain"], "tier": "Commercial / Residential"},
    {"id": "brand:fermax", "name": "Fermax", "category": "Door Entry & Intercom", "scope": ["Install", "Repair"], "tier": "Commercial / Residential"},

    # Networking, Wi-Fi & Routers
    {"id": "brand:ubiquiti", "name": "Ubiquiti (UniFi)", "category": "Networking & Wi-Fi", "scope": ["Supply", "Install", "Network Architecture", "Troubleshoot"], "tier": "Enterprise / High-End Residential"},
    {"id": "brand:tp-link-omada", "name": "TP-Link Omada", "category": "Networking & Wi-Fi", "scope": ["Supply", "Install", "Configure", "Maintain"], "tier": "Commercial Cloud SDN"},
    {"id": "brand:tp-link-deco", "name": "TP-Link Deco", "category": "Networking & Wi-Fi", "scope": ["Supply", "Install", "Hardwired Backhaul"], "tier": "Domestic Whole-Home Mesh"},
    {"id": "brand:draytek", "name": "DrayTek (Vigor)", "category": "Networking & Routers", "scope": ["Supply", "Install", "Multi-WAN Failover Config"], "tier": "Commercial Edge Security"},
    {"id": "brand:asus", "name": "ASUS (AiMesh & ROG)", "category": "Networking & Routers", "scope": ["Configure", "Hardwired Backhaul"], "tier": "Prosumer / Gaming"},
    {"id": "brand:netgear", "name": "Netgear (Orbi & Nighthawk)", "category": "Networking & Wi-Fi", "scope": ["Configure", "Backhaul Optimization"], "tier": "Consumer / Prosumer"},
    {"id": "brand:zyxel", "name": "Zyxel", "category": "Networking", "scope": ["Supply", "Configure"], "tier": "Commercial Switch / AP"},
    {"id": "brand:cisco-meraki", "name": "Cisco Meraki Go", "category": "Networking", "scope": ["Install", "Configure"], "tier": "Small Business Commercial"},
    {"id": "brand:mikrotik", "name": "MikroTik", "category": "Networking & Wireless Wire", "scope": ["Supply", "Install 60GHz Bridges", "Configure"], "tier": "Telecom / PtP High-Bandwidth"},
    {"id": "brand:teltonika", "name": "Teltonika Networks", "category": "Industrial Cellular & 5G Routers", "scope": ["Supply", "Install 4G/5G Failover Antennas", "Configure"], "tier": "Industrial IoT & Failover"},
    {"id": "brand:peplink", "name": "Peplink (Pepwave)", "category": "Multi-WAN Bonding Routers", "scope": ["Configure SpeedFusion Bonding", "Install"], "tier": "Enterprise Redundancy"},
    {"id": "brand:aruba-instant-on", "name": "HPE Aruba Instant On", "category": "Networking & Wi-Fi", "scope": ["Install", "Configure"], "tier": "Commercial Prosumer"},
    {"id": "brand:ruckus", "name": "Ruckus (CommScope)", "category": "Networking & Wi-Fi", "scope": ["Configure", "Troubleshoot"], "tier": "Enterprise High-Density"},
    {"id": "brand:eero", "name": "Eero (Amazon)", "category": "Consumer Mesh Wi-Fi", "scope": ["Install", "Hardwired Backhaul Config"], "tier": "Consumer Mesh"},
    {"id": "brand:linksys-velop", "name": "Linksys Velop", "category": "Consumer Mesh Wi-Fi", "scope": ["Configure", "Hardwired Backhaul"], "tier": "Consumer Mesh"},
    {"id": "brand:google-nest-wifi", "name": "Google Nest Wifi Pro", "category": "Consumer Mesh Wi-Fi", "scope": ["Install", "Configure"], "tier": "Consumer Mesh"},

    # Satellite & Starlink
    {"id": "brand:spacex-starlink", "name": "SpaceX Starlink", "category": "Satellite Broadband", "scope": ["Certified Physical Mounting", "Bypass Networking", "Cabling", "Surge Protection"], "tier": "LEO Satellite Broadband"},

    # TV Brackets & Masonry Mounts
    {"id": "brand:sanus", "name": "Sanus", "category": "TV Mounting & AV", "scope": ["Supply", "Install"], "tier": "Premium Structural"},
    {"id": "brand:vogels", "name": "Vogel's", "category": "TV Mounting & AV", "scope": ["Supply", "Install"], "tier": "Premium Engineered"},
    {"id": "brand:invision", "name": "Invision", "category": "TV Mounting & AV", "scope": ["Supply", "Install"], "tier": "Heavy-Duty Cantilever"},
    {"id": "brand:one-for-all", "name": "One For All", "category": "TV Mounting & Antennas", "scope": ["Supply", "Install"], "tier": "Consumer"},
    {"id": "brand:peerless-av", "name": "Peerless-AV", "category": "Commercial AV Mounting", "scope": ["Supply", "Install"], "tier": "Commercial Digital Signage"},
    {"id": "brand:ergotron", "name": "Ergotron", "category": "Specialist Articulating Arms", "scope": ["Install", "Configure"], "tier": "Commercial / Medical"},
    {"id": "brand:b-tech", "name": "B-Tech AV Mounts", "category": "Commercial AV Mounts", "scope": ["Supply", "Install"], "tier": "UK Trade Commercial"},
    {"id": "brand:unicol", "name": "Unicol", "category": "Specialist Heavy-Duty Mounts", "scope": ["Supply", "Install"], "tier": "UK Engineered Heavy-Duty"},
    {"id": "brand:corefix", "name": "CoreFix (Metex)", "category": "Masonry Fixings", "scope": ["Primary Specification", "Install"], "tier": "100kg+ Dot-and-Dab Anchor"},
    {"id": "brand:snaptoggle", "name": "SnapToggle (Toggler)", "category": "Hollow Stud Fixings", "scope": ["Primary Specification", "Install"], "tier": "Heavy-Duty Hollow Stud"},
    {"id": "brand:fischer", "name": "Fischer Fixings", "category": "Structural Anchors", "scope": ["Duopower / Resin Anchor Specification"], "tier": "Solid Masonry & Aerated Block"},
    {"id": "brand:gripit", "name": "GripIt Fixings", "category": "Plasterboard Fixings", "scope": ["Specification for Medium Loads"], "tier": "Drywall Cavity"},
    {"id": "brand:rawlplug", "name": "Rawlplug", "category": "Structural Fixings", "scope": ["Spring Toggle / Shield Anchor Specification"], "tier": "UK Trade Standard"},

    # Aerial, Coax & RF Hardware
    {"id": "brand:webro", "name": "Webro Cables", "category": "Coaxial & Data Cabling", "scope": ["Primary Specification (WF100 / WF65 / Cat6 PE)"], "tier": "CAI-Benchmarked UK Coax"},
    {"id": "brand:blake-uk", "name": "Blake UK", "category": "Aerials, Masts & Brackets", "scope": ["Supply", "Install"], "tier": "UK Trade Standard"},
    {"id": "brand:antiference", "name": "Antiference", "category": "Aerials & Distribution", "scope": ["Supply", "Install"], "tier": "UK Trade Standard"},
    {"id": "brand:triax", "name": "Triax", "category": "RF & Satellite Distribution", "scope": ["Supply", "Install"], "tier": "Commercial Headend / Domestic"},
    {"id": "brand:televes", "name": "Televes", "category": "Intelligent Aerials & Headends", "scope": ["Supply", "Install", "TForce Alignment"], "tier": "European High-Gain Standard"},
    {"id": "brand:labgear", "name": "Labgear", "category": "Distribution Amps & Filters", "scope": ["Supply", "Install"], "tier": "UK Trade Standard"},
    {"id": "brand:global-invacom", "name": "Global Invacom", "category": "Fibre Satellite & Optical LNBs", "scope": ["Supply", "Install", "Configure"], "tier": "Commercial IRS & Fibre Satellite"},
    {"id": "brand:promax", "name": "Promax Electronic", "category": "RF Test Equipment", "scope": ["Calibrated Field Diagnostics (HD Ranger)"], "tier": "Broadcast Laboratory Standard"},
    {"id": "brand:cabelcon", "name": "Corning Cabelcon", "category": "Compression Connectors", "scope": ["Primary Coaxial F-Type Specification"], "tier": "Waterproof Broadcast Grade"},

    # Storage & Core Components
    {"id": "brand:wd-purple", "name": "Western Digital (WD Purple)", "category": "Surveillance Storage", "scope": ["Primary Surveillance NVR Drive"], "tier": "24/7 AllFrame 4K Storage"},
    {"id": "brand:seagate-skyhawk", "name": "Seagate (SkyHawk AI)", "category": "Surveillance Storage", "scope": ["Surveillance NVR Drive"], "tier": "24/7 AI Surveillance Storage"},

    # Structured Cabling Infrastructure
    {"id": "brand:excel-networking", "name": "Excel Networking", "category": "Structured Cabling", "scope": ["Supply", "Certified Install", "Patch Panels"], "tier": "UK Commercial Enterprise Standard"},
    {"id": "brand:connectix", "name": "Connectix Cabling Systems", "category": "Structured Cabling", "scope": ["Supply", "Certified Install"], "tier": "UK Commercial Enterprise"},
    {"id": "brand:fluke-networks", "name": "Fluke Networks", "category": "Certification Test Equipment", "scope": ["DSX-8000 Certified Testing"], "tier": "Global Gold Standard"},

    # TV Displays & Audio Systems
    {"id": "brand:samsung", "name": "Samsung Electronics", "category": "Smart TV & The Frame", "scope": ["Wall Mount", "One-Connect In-Wall", "Setup"], "tier": "Consumer / High-End QLED"},
    {"id": "brand:lg", "name": "LG Electronics", "category": "OLED & QNED Displays", "scope": ["Flush Wall Mount", "Audio Bypass", "Setup"], "tier": "Consumer / Reference OLED"},
    {"id": "brand:sony", "name": "Sony", "category": "Bravia OLED & Master Series", "scope": ["Wall Mount", "Audio Routing", "Setup"], "tier": "Reference Visual / Audio"},
    {"id": "brand:panasonic", "name": "Panasonic", "category": "Master OLED Displays", "scope": ["Wall Mount", "Setup"], "tier": "Reference Master OLED"},
    {"id": "brand:hisense", "name": "Hisense", "category": "Mini-LED & Laser TV", "scope": ["Wall Mount", "Setup"], "tier": "Consumer Mini-LED"},
    {"id": "brand:tcl", "name": "TCL", "category": "Mini-LED & QLED Displays", "scope": ["Wall Mount", "Setup"], "tier": "Consumer Mini-LED"},
    {"id": "brand:sonos", "name": "Sonos", "category": "Home Theatre & Multi-Room Audio", "scope": ["Wall Mount (Arc/Beam/Sub)", "eARC Integration"], "tier": "Premium Wireless Audio"},
    {"id": "brand:bose", "name": "Bose", "category": "Soundbars & Audio", "scope": ["Wall Mount", "Setup"], "tier": "Premium Audio"},
    {"id": "brand:denon", "name": "Denon (HEOS)", "category": "AV Receivers & Multi-Room", "scope": ["Install", "Surround Sound Setup"], "tier": "Audiophile AV Receivers"}
]

# -------------------------------------------------------------
# 2. DETAILED EQUIPMENT MODELS
# -------------------------------------------------------------
EQUIPMENT = [
    {
        "id": "equip:starlink-gen3-standard",
        "name": "SpaceX Starlink Gen 3 Standard (V4 Kickstand)",
        "brand_id": "brand:spacex-starlink",
        "category": "Satellite Terminal",
        "specs": "Rectangular phased-array, 100° FOV, Wi-Fi 6 router with 2x Gigabit RJ45 ports, IP67 weather-rated, tri-band mesh capable.",
        "services": ["service:starlink-chimney-install", "service:starlink-wall-install", "service:starlink-bypass-config"]
    },
    {
        "id": "equip:starlink-gen2-actuated",
        "name": "SpaceX Starlink Gen 2 Standard Actuated (Motorised)",
        "brand_id": "brand:spacex-starlink",
        "category": "Satellite Terminal",
        "specs": "Motorised self-orienting rectangular dish, proprietary SPX cable, requires Starlink Ethernet Adapter for RJ45 hand-off.",
        "services": ["service:starlink-chimney-install", "service:starlink-wall-install", "service:starlink-repair"]
    },
    {
        "id": "equip:starlink-mini",
        "name": "SpaceX Starlink Mini (Compact Portable)",
        "brand_id": "brand:spacex-starlink",
        "category": "Satellite Terminal",
        "specs": "Integrated Wi-Fi 5 router, DC barrel jack powered (12-48V), compact 1.1kg form factor, Gigabit Ethernet port.",
        "services": ["service:starlink-wall-install", "service:starlink-bypass-config"]
    },
    {
        "id": "equip:starlink-heavy-duty-chimney-kit",
        "name": "Heavy-Duty Starlink Chimney Lashing Kit (Non-Drill)",
        "brand_id": "brand:blake-uk",
        "category": "Mounting Hardware",
        "specs": "Galvanised twin-cradle bracket, 1.5” / 2” heavy-gauge steel mast, 5-strand stainless steel tension lashing wire, high-tensile J-bolts. 0 holes drilled in masonry. 90mph gale rated.",
        "services": ["service:starlink-chimney-install"]
    },
    {
        "id": "equip:starlink-tk-wall-brackets",
        "name": "Heavy-Duty Galvanised T&K Standoff Brackets (18\"–24\")",
        "brand_id": "brand:blake-uk",
        "category": "Mounting Hardware",
        "specs": "Hot-dipped galvanised welded steel pair, 18\" to 24\" standoff clearance for deep eaves and gutters, anchored with M10 masonry shield anchors.",
        "services": ["service:starlink-wall-install"]
    },
    {
        "id": "equip:hikvision-colorvu-4k-turret",
        "name": "Hikvision 4K ColorVu Turret IP Camera (DS-2CD2387G2-LU)",
        "brand_id": "brand:hikvision",
        "category": "CCTV Camera",
        "specs": "8MP 4K resolution, F1.0 super-aperture lens, 24/7 full-colour night vision (0 lux), built-in mic, AcuSense human/vehicle AI classification, IP67 weatherproof.",
        "services": ["service:cctv-poe-install", "service:cctv-upgrade"]
    },
    {
        "id": "equip:hikvision-acusense-nvr",
        "name": "Hikvision 8-Channel 4K PoE NVR (DS-7608NXI-I2/8P)",
        "brand_id": "brand:hikvision",
        "category": "CCTV Recorder",
        "specs": "8x independent PoE interfaces, up to 12MP recording, 2x SATA bays up to 20TB, dual-stream, Hik-Connect zero-subscription mobile remote viewing.",
        "services": ["service:cctv-poe-install"]
    },
    {
        "id": "equip:dahua-tioc-5mp-active-deterrence",
        "name": "Dahua 5MP TiOC 2.0 Active Deterrence Turret",
        "brand_id": "brand:dahua",
        "category": "CCTV Camera",
        "specs": "Full-colour night vision, flashing red/blue police strobe beacons, 110dB custom voice siren, perimeter AI tripwire, two-way audio.",
        "services": ["service:cctv-poe-install"]
    },
    {
        "id": "equip:reolink-duo-3-poe",
        "name": "Reolink Duo 3 PoE 16MP 180° Panoramic Camera",
        "brand_id": "brand:reolink",
        "category": "CCTV Camera",
        "specs": "Dual lenses seamlessly stitched into 180° blind-spot-free perspective, 16MP ultra-wide UHD, ColorX nighttime lens, motion tracking.",
        "services": ["service:cctv-poe-install"]
    },
    {
        "id": "equip:wd-purple-surveillance-hdd",
        "name": "WD Purple Surveillance Hard Drive (4TB / 8TB / 10TB)",
        "brand_id": "brand:wd-purple",
        "category": "Storage",
        "specs": "Engineered for 24/7 continuous high-definition surveillance recording, AllFrame technology reduces frame drops, rated for 180TB/year workload.",
        "services": ["service:cctv-poe-install", "service:cctv-hard-drive-replacement"]
    },
    {
        "id": "equip:ajax-hub-2-plus",
        "name": "Ajax Hub 2 Plus Central Controller",
        "brand_id": "brand:ajax",
        "category": "Alarm Central Hub",
        "specs": "Grade 2 security control panel, 4 communication channels (Ethernet, Wi-Fi, 2x 2G/3G/LTE SIM slots), supports up to 200 devices, 100 cameras, 200 users. Jeweller 868MHz protocol.",
        "services": ["service:ajax-alarm-install"]
    },
    {
        "id": "equip:ajax-motioncam-phod",
        "name": "Ajax MotionCam PhOD (Photo on Demand)",
        "brand_id": "brand:ajax",
        "category": "Alarm Detector",
        "specs": "PIR motion sensor with integrated camera, takes animated photo series on alarm or user demand, pet-immune up to 20kg, 1,700m line of sight.",
        "services": ["service:ajax-alarm-install"]
    },
    {
        "id": "equip:ajax-streetsiren-doubledeck",
        "name": "Ajax StreetSiren DoubleDeck",
        "brand_id": "brand:ajax",
        "category": "Alarm Siren",
        "specs": "Wireless outdoor siren with customizable LED frame and acoustic buzzer (up to 113dB), IP54 water resistance, accelerometer anti-tamper tear-off detection.",
        "services": ["service:ajax-alarm-install"]
    },
    {
        "id": "equip:unifi-dream-machine-se",
        "name": "Ubiquiti UniFi Dream Machine Special Edition (UDM-SE)",
        "brand_id": "brand:ubiquiti",
        "category": "Router & Gateway",
        "specs": "Enterprise gateway with integrated PoE/PoE+ 8-port switch, 2.5G WAN, 10G SFP+ LAN/WAN, integrated 128GB SSD + 3.5\" NVR drive bay.",
        "services": ["service:networking-commercial-install"]
    },
    {
        "id": "equip:unifi-u7-pro-ap",
        "name": "Ubiquiti UniFi U7 Pro Wi-Fi 7 Access Point",
        "brand_id": "brand:ubiquiti",
        "category": "Wireless Access Point",
        "specs": "Ceiling-mounted Wi-Fi 7 AP, 6GHz / 5GHz / 2.4GHz tri-band, 2.5G uplink with PoE+, handles 300+ connected clients without slowdown.",
        "services": ["service:wifi-mesh-install", "service:networking-commercial-install"]
    },
    {
        "id": "equip:draytek-vigor-2865",
        "name": "DrayTek Vigor 2865 Security Firewall Router",
        "brand_id": "brand:draytek",
        "category": "Router & Gateway",
        "specs": "VDSL2 / ADSL2+ & Gigabit Ethernet WAN router, dual-WAN failover (ideal for Starlink + 4G/5G backup), robust VPN concentrator.",
        "services": ["service:networking-commercial-install"]
    },
    {
        "id": "equip:corefix-120-heavy-duty-anchors",
        "name": "CoreFix 120 Heavy-Duty Dot & Dab Wall Fixings",
        "brand_id": "brand:corefix",
        "category": "Masonry Anchor",
        "specs": "Steel core bridge transfers TV load directly into solid masonry behind plasterboard cavity; 100kg safe working load for 65\"–100\" TVs.",
        "services": ["service:tv-wall-mounting-install", "service:tv-bracket-remount-repair"]
    },
    {
        "id": "equip:snaptoggle-heavy-duty-stud-bolts",
        "name": "SnapToggle Heavy-Duty Hollow Wall Anchors (1/4\"-20)",
        "brand_id": "brand:snaptoggle",
        "category": "Stud Anchor",
        "specs": "Solid zinc-plated steel channel with nylon strapping, anchors heavy TV brackets across hollow drywall and timber/metal studs with up to 120kg shear strength.",
        "services": ["service:tv-wall-mounting-install", "service:tv-bracket-remount-repair"]
    },
    {
        "id": "equip:webro-wf100-coax",
        "name": "Webro WF100 Coaxial Cable (CAI Benchmarked)",
        "brand_id": "brand:webro",
        "category": "Coaxial Cable",
        "specs": "1.00mm pure solid copper inner conductor, physical gas-injected foam dielectric, copper foil and copper braid screening (CAI 0007 F benchmarked).",
        "services": ["service:tv-aerial-install", "service:tv-aerial-socket-replacement", "service:coax-f-connector-retermination"]
    },
    {
        "id": "equip:promax-hd-ranger-analyser",
        "name": "Promax HD Ranger Eco Spectrum Analyzer & Field Meter",
        "brand_id": "brand:promax",
        "category": "Test Equipment",
        "specs": "Ultra-fast spectrum analyzer, DVB-T/T2 MER constellation measurement, pre/post Viterbi BER, LTE signal interference logging.",
        "services": ["service:tv-aerial-install", "service:tv-aerial-repair", "service:freeview-tv-retune-rescan"]
    }
]

# -------------------------------------------------------------
# 3. CABLING SPECIFICATIONS
# -------------------------------------------------------------
CABLING = [
    {
        "id": "cable:cat6-solid-copper-external",
        "type": "Cat6 U/UTP External PE",
        "conductor": "23AWG Solid Bare Oxygen-Free Copper (100% Copper)",
        "bandwidth": "250 MHz (1Gbps up to 100m, 10Gbps up to 37m)",
        "jacket": "Heavy-duty UV-resistant black Polyethylene (PE) external grade",
        "application": "Exterior building runs, Starlink drops, outdoor PoE CCTV cameras, waterproof drip loops.",
        "warning": "Strictly zero Copper-Clad Aluminium (CCA) used."
    },
    {
        "id": "cable:cat6a-sftp-lszh",
        "type": "Cat6a S/FTP LSZH",
        "conductor": "23AWG Solid Bare Copper",
        "bandwidth": "500 MHz (True 10Gbps at full 100m channel)",
        "shielding": "Braided overall shield + individual aluminium foil pairs (S/FTP) eliminating alien crosstalk",
        "jacket": "Low Smoke Zero Halogen (LSZH) CPR Class Cca",
        "application": "High-density data centres, commercial backbones, ultra-fast AV video over IP."
    },
    {
        "id": "cable:cat5e-solid-copper",
        "type": "Cat5e U/UTP Internal",
        "conductor": "24AWG Solid Bare Copper",
        "bandwidth": "100 MHz (1Gbps up to 100m)",
        "application": "Basic domestic data drops, IP intercom links, legacy network replacements."
    },
    {
        "id": "cable:cat7-s-ftp",
        "type": "Cat7 S/FTP High-Performance Shielded",
        "conductor": "23AWG Solid Pure Copper",
        "bandwidth": "600 MHz (10Gbps with heavy industrial noise immunity)",
        "application": "Factory and heavy machinery environment data drops."
    },
    {
        "id": "cable:cat8-s-ftp",
        "type": "Cat8 S/FTP 40Gbps High-Speed",
        "conductor": "22AWG/23AWG Solid Bare Copper",
        "bandwidth": "2000 MHz (25Gbps / 40Gbps up to 30m)",
        "application": "Server-to-switch and SAN storage data links."
    },
    {
        "id": "cable:webro-wf100",
        "type": "Webro WF100 Digital Coaxial",
        "conductor": "1.00mm Pure Annealed Plain Copper",
        "dielectric": "Foamed Polyethylene (3.40mm)",
        "screening": "Plain copper foil + 55% plain copper braid (100% optical coverage)",
        "application": "Freeview digital TV drops, multi-room distribution, Freesat/Sky Q LNB runs."
    },
    {
        "id": "cable:webro-wf65-shotgun",
        "type": "Webro WF65 Twin Shotgun Coax",
        "conductor": "0.65mm Pure Solid Copper (Twin)",
        "application": "Compact twin-feed runs for satellite PVR receivers (Sky Q / Freesat twin tuner)."
    },
    {
        "id": "cable:os2-single-mode-fibre",
        "type": "OS2 9/125μm Single-Mode Optical Fibre",
        "application": "Long-distance campus links (>300m), zero electrical surge risk between farm outbuildings."
    },
    {
        "id": "cable:om4-multi-mode-fibre",
        "type": "OM4 50/125μm Multi-Mode Optical Fibre",
        "application": "Short-reach 10G/40G/100G intra-building backbone trunks."
    }
]

# -------------------------------------------------------------
# 4. MOUNTING SYSTEMS & STRUCTURAL ANCHORS
# -------------------------------------------------------------
MOUNTING_SYSTEMS = [
    {
        "id": "mount:chimney-non-drill-cradle",
        "name": "Non-Drill Chimney Lashing Cradle System",
        "trade_purpose": "Secures Starlink dishes, aerial masts, and wireless bridges to brick chimneys with zero masonry drilling.",
        "hardware": ["Galvanised steel lashing cradle", "Stainless steel 5-strand wire", "J-bolts & tension ratchets", "Corner protection brackets"],
        "wind_rating": "Engineered for 90mph gale resistance without brick spalling or mortar blowout."
    },
    {
        "id": "mount:heavy-duty-tk-wall-brackets",
        "name": "Heavy-Duty Welded Galvanised T&K Wall Brackets",
        "trade_purpose": "Provides 18-inch to 24-inch standoff clearance from gable walls over deep roof overhangs and gutters.",
        "hardware": ["Welded hot-dipped galvanised T-bracket and K-bracket", "M10 high-tensile shield anchors", "Double U-bolts for 2\" alloy mast"],
        "wind_rating": "Zero mast micro-flex during high-wind winter storms."
    },
    {
        "id": "mount:corefix-dot-and-dab",
        "name": "CoreFix 100/120 Heavy-Duty Dot & Dab Drywall System",
        "trade_purpose": "Spans the 10mm–30mm plasterboard void to anchor 65\"–100\" TVs directly into the blockwork behind.",
        "hardware": ["100mm/120mm high-tensile steel screw", "Machined steel load-bearing collar sleeve", "Heavy-duty nylon wall plug"],
        "safe_load": "100kg safe shear load per pair (never crushes plasterboard inward)."
    },
    {
        "id": "mount:snaptoggle-hollow-stud",
        "name": "SnapToggle Heavy-Duty Metal & Timber Stud Mounting",
        "trade_purpose": "Locks heavy cantilever dual-arm TV brackets onto hollow drywall stud partitions where no solid masonry exists.",
        "hardware": ["Solid zinc-plated steel pivoting channel", "Nylon ratcheting guide leg", "1/4\"-20 machine screws"],
        "safe_load": "Up to 120kg ultimate shear load per anchor."
    },
    {
        "id": "mount:ceiling-drop-bracket",
        "name": "Heavy-Duty Telescopic Ceiling Drop Mount",
        "trade_purpose": "Suspends commercial displays or bedroom screens from high structural joists or concrete ceilings.",
        "hardware": ["Telescopic heavy-gauge steel pole", "Integrated internal cable routing channel", "Swivel ceiling baseplate"]
    }
]

# -------------------------------------------------------------
# 5. DIAGNOSTIC PROBLEMS & ROOT CAUSE SOLUTIONS
# -------------------------------------------------------------
PROBLEMS = [
    {
        "id": "prob:cctv-night-glare",
        "title": "CCTV Night-Time Vision is White Fog or Washed Out Glare",
        "root_cause": "Infrared reflection bouncing back off dome glass covers, nearby soffit boards, brick corners, or spiderweb buildup.",
        "solution": "Replace reflective glass dome with open-lens Turret (Eyeball) camera with separated dual IR/white-light emitters and ColorVu technology.",
        "services": ["service:cctv-upgrade", "service:cctv-repair"]
    },
    {
        "id": "prob:cctv-voltage-drop-reboot",
        "title": "CCTV Cameras Disconnect or Reboot Every Evening at Dusk",
        "root_cause": "Cheap Copper-Clad Aluminium (CCA) cable drops too much voltage under high electrical load when infrared LEDs activate at sunset.",
        "solution": "Replace substandard CCA with 100% solid oxygen-free copper Cat6 cable with IEEE 802.3at PoE+ power budget.",
        "services": ["service:cctv-repair", "service:rj45-crimp-repair"]
    },
    {
        "id": "prob:wifi-dead-spots-stone-walls",
        "title": "Wi-Fi Drops Completely Inside 500mm Thick Stone Walls or Extensions",
        "root_cause": "High-density Yorkshire gritstone and foil-backed insulation absorb 5GHz and 6GHz wireless signals completely.",
        "solution": "Install hardwired solid copper Cat6 backhaul cables to discreet ceiling-mounted Wi-Fi 6/7 access points in every zone.",
        "services": ["service:wifi-mesh-install", "service:wifi-hardwired-backhaul-run"]
    },
    {
        "id": "prob:starlink-mast-micro-wobble",
        "title": "Starlink Internet Stalls or Drops Satellite Lock in High Winds",
        "root_cause": "Flimsy aluminium poles or cheap swan-neck brackets flex 2–3 degrees in wind gusts, losing phased-array beam alignment.",
        "solution": "Mount on heavy-duty non-drill chimney lashing cradles or 18\" welded T&K brackets with 2\" heavy-gauge mast.",
        "services": ["service:starlink-chimney-install", "service:starlink-wall-install"]
    },
    {
        "id": "prob:tv-pixelating-5g-interference",
        "title": "Freeview TV Channels Pixelating, Freezing or Missing Completely",
        "root_cause": "700MHz 5G or 800MHz 4G mobile phone mast transmission breaking into wideband unshielded TV aerial coax.",
        "solution": "Install CAI-benchmarked 5G LTE channel 48 low-pass filter, double-screened Webro WF100 coax, and spectrum analyzer realignment.",
        "services": ["service:tv-aerial-repair", "service:5g-lte-filter-retrofit"]
    },
    {
        "id": "prob:diy-alarm-rf-jamming",
        "title": "DIY 433MHz Wireless Alarms Vulnerable to Cheap RF Jamming",
        "root_cause": "Single-frequency 433MHz wireless devices can be blinded by basic handheld transmitters without triggering an alarm.",
        "solution": "Upgrade to Grade 2 Ajax Jeweller 868MHz encrypted rolling-code frequency-hopping system with sub-second jamming detection.",
        "services": ["service:ajax-alarm-install"]
    },
    {
        "id": "prob:tv-mounting-drywall-collapse",
        "title": "Fear of 75\"–85\" Heavy OLED TV Pulling Down Plasterboard Drywall",
        "root_cause": "Standard plastic drywall plugs pull straight out of gypsum board under dynamic cantilever forward weight.",
        "solution": "Professional structural mounting with CoreFix 120 (into solid block) or SnapToggle (into timber/metal studs) rated to 100kg+.",
        "services": ["service:tv-wall-mounting-install", "service:tv-bracket-remount-repair"]
    }
]

# -------------------------------------------------------------
# 6. PRIMARY INSTALLATION SERVICES (Macro Offerings)
# -------------------------------------------------------------
PRIMARY_SERVICES = [
    {
        "id": "service:starlink-chimney-install",
        "title": "SpaceX Starlink Chimney Installation (Non-Drill Lashing)",
        "price_from": "£199 + VAT",
        "description": "Turnkey installation using stainless steel tensioned chimney lashing cradle, 2\" heavy-gauge mast, external black Cat6 drop with drip loop, internal cable entry and router setup.",
        "url": "https://adicommunications.co.uk/starlink-internet-installation/"
    },
    {
        "id": "service:starlink-wall-install",
        "title": "SpaceX Starlink High-Standoff Wall Installation",
        "price_from": "£199 + VAT",
        "description": "Installation using heavy-duty 18\"–24\" galvanised T&K standoff brackets clearing rooflines and gutters.",
        "url": "https://adicommunications.co.uk/starlink-internet-installation/"
    },
    {
        "id": "service:starlink-bypass-config",
        "title": "Starlink Third-Party Router Bypass & Mesh Integration",
        "price_from": "£145 + VAT",
        "description": "Configuring Starlink router bypass mode to hand off public IP directly into UniFi, Omada, Deco, or DrayTek firewalls.",
        "url": "https://adicommunications.co.uk/starlink-internet-installation/"
    },
    {
        "id": "service:cctv-poe-install",
        "title": "Commercial Grade 4K PoE CCTV Installation",
        "price_from": "£299 + VAT (Single) / £495 + VAT (Multi-Camera)",
        "description": "Full installation of Hikvision ColorVu or Dahua TiOC cameras, external solid copper Cat6 cabling, NVR recorder with WD Purple storage, mobile phone app setup, zero monthly fees.",
        "url": "https://adicommunications.co.uk/cctv-installation/"
    },
    {
        "id": "service:cctv-upgrade",
        "title": "CCTV System Upgrade & Camera Expansion",
        "price_from": "£185 + VAT",
        "description": "Upgrading old 720p/1080p coax cameras or budget Wi-Fi cameras to modern AI human/vehicle classification 4K systems.",
        "url": "https://adicommunications.co.uk/cctv-installation/"
    },
    {
        "id": "service:cctv-repair",
        "title": "CCTV Diagnostic Fault-Finding & Cable Repair",
        "price_from": "£85 + VAT",
        "description": "Resolving offline cameras, voltage drop, night glare, broken connectors, or failed hard drives.",
        "url": "https://adicommunications.co.uk/cctv-installation/"
    },
    {
        "id": "service:ajax-alarm-install",
        "title": "Ajax Grade 2 Wireless Smart Intruder Alarm Installation",
        "price_from": "£599 + VAT",
        "description": "Certified fitting of Ajax Hub 2 Plus, MotionCam PhOD detectors, DoorProtect Plus contacts, 113dB StreetSiren, 4G failover setup, smartphone configuration.",
        "url": "https://adicommunications.co.uk/ajax-alarm/"
    },
    {
        "id": "service:tv-wall-mounting-install",
        "title": "Heavy-Duty TV Wall Mounting (Any Screen Size & Wall Type)",
        "price_from": "£89.99 + VAT",
        "description": "Safe structural mounting of 32\" to 100\" TVs on dot-and-dab, brick, timber stud, or acoustic media walls using CoreFix and SnapToggle fixings.",
        "url": "https://adicommunications.co.uk/tv-wall-mounting/"
    },
    {
        "id": "service:wifi-mesh-install",
        "title": "Whole-Home Wi-Fi 6/7 Mesh & Access Point Installation",
        "price_from": "£145 + VAT",
        "description": "Hardwired Cat6 backhaul cabling to ceiling or wall-mounted APs, eliminating dead spots in thick stone properties.",
        "url": "https://adicommunications.co.uk/wifi-installation/"
    },
    {
        "id": "service:garden-office-link-install",
        "title": "High-Speed Garden Office Wireless Point-to-Point Bridge",
        "price_from": "£295 + VAT",
        "description": "Outdoor 5GHz/60GHz gigabit bridge links connecting home broadband directly to garden rooms, outbuildings, or workshops without digging trenches.",
        "url": "https://adicommunications.co.uk/wifi-installation/"
    },
    {
        "id": "service:tv-aerial-install",
        "title": "Digital High-Gain TV Aerial Installation",
        "price_from": "£129 + VAT",
        "description": "Benchmarked CAI-standard wideband aerials with 5G LTE filtering, Webro WF100 cabling, and precision spectrum analyzer transmitter alignment.",
        "url": "https://adicommunications.co.uk/tv-aerial-installation/"
    },
    {
        "id": "service:tv-aerial-repair",
        "title": "TV Aerial Signal Diagnosis, Filter Fitting & Storm Repair",
        "price_from": "£69 + VAT",
        "description": "Spectrum analyser diagnosis for pixelation, transmitter realignment, masthead amplifier replacement, 5G filter retrofitting.",
        "url": "https://adicommunications.co.uk/tv-aerial-installation/"
    }
]

# -------------------------------------------------------------
# 7. MICRO-REPAIR SERVICES & CONNECTION FIXES (High-Search Volume)
# -------------------------------------------------------------
REPAIR_SERVICES = [
    {
        "id": "service:rj45-crimp-repair",
        "title": "RJ45 Plug Crimp & Ethernet Connection Repair",
        "price_from": "£65 + VAT",
        "search_queries": [
            "rj45 connection repair", "ethernet cable end repair", "fix broken ethernet clip",
            "crimp rj45 plug leeds", "cat6 connector replacement", "network cable termination service"
        ],
        "description": "Re-terminating damaged RJ45 modular plugs, snapped plastic locking clips, and broken wire cores using shielded pass-through connectors and Fluke wiremap verification."
    },
    {
        "id": "service:tv-aerial-socket-replacement",
        "title": "TV Aerial Wall Socket & Coaxial Faceplate Replacement",
        "price_from": "£55 + VAT",
        "search_queries": [
            "tv aerial wall socket replacement", "fix loose aerial socket", "coax wall plate repair",
            "replace tv aerial point", "broken aerial socket in wall", "belling lee socket fitting"
        ],
        "description": "Replacing damaged, loose, or high-resistance TV aerial coaxial wall sockets with screened, low-loss metal Belling-Lee or F-type modular Euro faceplates."
    },
    {
        "id": "service:cat6-data-point-socket",
        "title": "Single & Dual Cat6/Cat6a RJ45 Wall Socket Installation",
        "price_from": "£85 + VAT",
        "search_queries": [
            "install ethernet wall socket", "cat6 wall point installation", "rj45 socket fitting",
            "run ethernet to room", "hardwired internet socket in bedroom", "data point installation near me"
        ],
        "description": "Fitting surface or flush-mounted single and dual Cat6/Cat6a data sockets with IDC punch-down termination, metal backbox, and Fluke attenuation certification."
    },
    {
        "id": "service:coax-f-connector-retermination",
        "title": "Coaxial F-Type Connector Compression Fitting & Repair",
        "price_from": "£50 + VAT",
        "search_queries": [
            "f connector repair", "coax cable connector fitting", "sky satellite cable repair",
            "compress f type plug", "replace tv coax plug", "loose satellite dish wire"
        ],
        "description": "Replacing cheap screw-on F-plugs with broadcast-grade waterproof radial compression connectors (Cabelcon/PCT) on Webro WF100 and WF65 cables."
    },
    {
        "id": "service:loft-distribution-amp-psu-repair",
        "title": "Loft TV Distribution Amplifier & 12V PSU Replacement",
        "price_from": "£75 + VAT",
        "search_queries": [
            "tv booster in loft stopped working", "loft aerial amplifier replacement", "12v masthead power supply repair",
            "no tv signal in any room", "replace aerial distribution box", "multi room tv amplifier repair"
        ],
        "description": "Diagnosing and replacing failed loft distribution amplifiers, blown 12V DC power inserters, and shorted coaxial lines causing complete house-wide TV signal loss."
    },
    {
        "id": "service:5g-lte-filter-retrofit",
        "title": "4G/5G LTE Low-Pass Filter Retrofitting for TV Pixelation",
        "price_from": "£65 + VAT",
        "search_queries": [
            "5g mobile mast interfering with tv", "fit 5g filter to tv aerial", "freeview pixelating since 5g mast installed",
            "lte ch48 filter installation", "tv channel 48 breaking up", "tv aerial filter fitting"
        ],
        "description": "Installing high-rejection 700MHz 5G (Channel 48) inline low-pass filters directly before amplifiers to eliminate digital Freeview packet loss and freezing."
    },
    {
        "id": "service:cctv-bnc-balun-cat6-conversion",
        "title": "CCTV BNC Coax to Cat6 Balun Conversion & Upgrade",
        "price_from": "£95 + VAT",
        "search_queries": [
            "upgrade old bnc cctv to ip", "cctv balun replacement", "convert coax cctv to cat6",
            "lines across cctv screen repair", "ground loop isolator cctv", "analogue cctv repair"
        ],
        "description": "Resolving rolling ground loop hum bars and ghosting by replacing failing passive video baluns or converting old analogue RG59 coax runs to modern 4K PoE IP architecture."
    },
    {
        "id": "service:cctv-junction-box-resealing",
        "title": "CCTV Junction Box Weatherproofing & Water Ingress Repair",
        "price_from": "£75 + VAT",
        "search_queries": [
            "cctv camera full of water", "water in cctv connector", "cctv camera cutting out in rain",
            "weatherproof cctv junction box", "dry out cctv camera connection", "fix cctv water damage"
        ],
        "description": "Drying out corroded RJ45/BNC connectors, replacing unsealed backboxes with IP66 deep bases, and forming downward drip loops to stop water tracking into cavity walls."
    },
    {
        "id": "service:cctv-hard-drive-replacement",
        "title": "CCTV NVR Hard Drive Replacement & Formatting",
        "price_from": "£125 + VAT",
        "search_queries": [
            "cctv nvr beeping hard drive error", "replace cctv hard drive", "wd purple hard drive fitting",
            "cctv not recording to disk", "nvr hdd format error", "cctv hard disk replacement"
        ],
        "description": "Replacing failed desktop drives with genuine 24/7 surveillance-rated Western Digital Purple or Seagate SkyHawk drives, firmware initialization, and continuous loop setup."
    },
    {
        "id": "service:starlink-cable-splice-repair",
        "title": "Starlink Cable Splice & Waterproof IP68 Joint Repair",
        "price_from": "£95 + VAT",
        "search_queries": [
            "starlink cable chewed by dog", "repair cut starlink cable", "starlink cable splice kit",
            "starlink proprietary cable repair", "waterproof starlink cable joiner", "starlink wire cut"
        ],
        "description": "Precision shielded splicing and IP68 waterproof gland sealing of crushed, chewed, or severed Starlink Gen 2 and Gen 3 data cables without replacing full roof runs."
    },
    {
        "id": "service:tv-bracket-remount-repair",
        "title": "TV Wall Bracket Remounting & Stripped Plasterboard Repair",
        "price_from": "£85 + VAT",
        "search_queries": [
            "tv bracket pulling out of wall", "remount tv on plasterboard", "fix loose tv wall bracket",
            "stripped drywall anchors tv", "safe tv remounting service", "reinforce tv wall mount"
        ],
        "description": "Rescuing loose or sagging TV brackets from failing drywall by patching damaged holes and anchoring with CoreFix 120 (into solid block) or SnapToggle steel channel bolts."
    },
    {
        "id": "service:in-wall-hdmi-replacement",
        "title": "In-Wall Hidden HDMI 2.1 Cable Routing & Brush Plates",
        "price_from": "£80 + VAT",
        "search_queries": [
            "hide tv cables in wall", "in wall hdmi cable replacement", "brush faceplate for tv wires",
            "no cables showing tv mount", "run hdmi through stud wall", "replace broken hdmi behind wall"
        ],
        "description": "Routing ultra-high-speed 48Gbps 4K/120Hz HDMI 2.1 cables, optical audio, and power through cavity walls using white or black brushed cable-exit faceplates."
    },
    {
        "id": "service:ajax-alarm-battery-service",
        "title": "Ajax Wireless Alarm Battery Replacement & Health Audit",
        "price_from": "£75 + VAT",
        "search_queries": [
            "ajax alarm battery replacement", "ajax detector low battery", "replace cr123a alarm battery",
            "streetsiren battery change", "ajax hub backup battery", "wireless alarm battery service"
        ],
        "description": "Full battery replacement across Ajax DoorProtect, MotionProtect, and StreetSiren units using genuine Panasonic CR123A/CR2032 cells, radio signal recalibration."
    },
    {
        "id": "service:wifi-hardwired-backhaul-run",
        "title": "Hardwired Ethernet Backhaul Cabling for Wi-Fi Mesh Nodes",
        "price_from": "£125 + VAT",
        "search_queries": [
            "hardwire mesh wifi nodes", "ethernet backhaul installation", "connect deco with cable",
            "unifi ap ethernet cabling", "fix slow mesh wifi backhaul", "run cable between mesh routers"
        ],
        "description": "Running solid copper Cat6 lines between mesh pods (Deco, Orbi, UniFi, eero) to eliminate 50% wireless backhaul speed loss through solid floors and stone walls."
    },
    {
        "id": "service:garden-office-armoured-cat6",
        "title": "SWA Steel-Wire Armoured Cat6 Trench Cable Termination",
        "price_from": "£145 + VAT",
        "search_queries": [
            "armoured ethernet cable to garden room", "swa cat6 cable termination", "trench cable for garden office internet",
            "outdoor armoured data cable", "hardwired internet to outbuilding", "rodent proof ethernet cable"
        ],
        "description": "Glanding, earthing, and terminating Steel Wire Armoured (SWA) Cat6 cables in external IP66 junction boxes and internal RJ45 modules for rodent-proof garden office links."
    },
    {
        "id": "service:freeview-tv-retune-rescan",
        "title": "Freeview TV Transmitter Retune, Realignment & MUX Rescan",
        "price_from": "£55 + VAT",
        "search_queries": [
            "retune freeview tv channels", "lost bbc channels on tv", "freeview channel rescan service",
            "tv transmitter realignment", "fix missing freeview multiplexes", "tune smart tv to winter hill"
        ],
        "description": "Calibrated spectrum analyzer realignment to local transmitters (Winter Hill, Emley Moor, Bilsdale) with manual frequency entry to prevent duplicate weak relay channels."
    },
    {
        "id": "service:sky-q-lnb-realignment",
        "title": "Freesat & Sky Q Dish LNB Realignment & Shotgun Cable Repair",
        "price_from": "£70 + VAT",
        "search_queries": [
            "sky q dish realignment", "fix no satellite signal sky", "replace wideband lnb sky q",
            "freesat dish repair", "replace twin shotgun satellite cable", "satellite dish storm damage repair"
        ],
        "description": "Aligning satellite dishes to Astra 28.2°E using spectrum meters, replacing waterlogged wideband LNBs, and running fresh Webro WF65 twin copper shotgun cables."
    },
    {
        "id": "service:doorbell-transformer-fitting",
        "title": "Video Doorbell 24V Transformer Fitting & Chime Bypass",
        "price_from": "£79 + VAT",
        "search_queries": [
            "hardwire ring doorbell to mains", "install 24v transformer for nest doorbell", "bypass mechanical doorbell chime",
            "eufy doorbell hardwired installation", "video doorbell electrical fitting", "ring pro power kit installation"
        ],
        "description": "Installing DIN-rail or wall-mount 8V–24V AC step-down transformers, mechanical chime bypass fuses, and neat low-voltage cabling for permanent battery-free doorbell power."
    }
]

# -------------------------------------------------------------
# 8. COMPLETE REGIONAL COVERAGE CENSUS (100+ Towns & Postcodes)
# -------------------------------------------------------------
COVERAGE_AREAS = [
    {
        "region": "West Yorkshire",
        "postal_districts": ["BD", "LS", "WF", "HD", "HX"],
        "primary_hubs": ["Leeds", "Bradford", "Huddersfield", "Halifax", "Wakefield"],
        "towns_and_villages": [
            "Leeds City Centre", "Headingley", "Horsforth", "Roundhay", "Moortown", "Alwoodley", "Pudsey", "Morley", "Guiseley", "Yeadon", "Otley", "Wetherby", "Boston Spa", "Garforth",
            "Bradford", "Shipley", "Bingley", "Saltaire", "Keighley", "Haworth", "Silsden", "Ilkley", "Queensbury", "Clayton", "Thornton", "Idle", "Baildon", "Birkenshaw", "Cleckheaton", "Wyke",
            "Huddersfield", "Lindley", "Brighouse", "Slaithwaite", "Linthwaite", "Golcar", "Holmfirth", "Honley", "Meltham", "Almondbury", "Kirkburton", "Denby Dale", "Skelmanthorpe", "Marsden",
            "Halifax", "Hebden Bridge", "Todmorden", "Sowerby Bridge", "Elland", "Hipperholme", "Lightcliffe", "Rishworth",
            "Wakefield", "Pontefract", "Castleford", "Normanton", "Ossett", "Horbury", "Knottingley", "Batley", "Birstall", "Dewsbury"
        ]
    },
    {
        "region": "North Yorkshire",
        "postal_districts": ["DL", "HG", "YO", "BD"],
        "primary_hubs": ["Harrogate", "York", "Skipton", "Northallerton", "Ripon"],
        "towns_and_villages": [
            "Harrogate", "Knaresborough", "Ripon", "Pannal", "Starbeck", "Killinghall",
            "Skipton", "Settle", "Grassington", "Gargrave", "Barnoldswick", "Earby",
            "Northallerton", "Richmond", "Catterick Garrison", "Bedale", "Thirsk", "Leyburn", "Hawes",
            "York City Centre", "Heslington", "Fulford", "Haxby", "Wigginton", "Selby", "Tadcaster", "Malton", "Pickering"
        ]
    },
    {
        "region": "Lancashire",
        "postal_districts": ["BB", "PR", "FY", "LA"],
        "primary_hubs": ["Blackburn", "Burnley", "Preston", "Blackpool", "Lancaster"],
        "towns_and_villages": [
            "Blackburn", "Darwen", "Accrington", "Church", "Oswaldtwistle", "Rishton", "Great Harwood",
            "Burnley", "Padiham", "Colne", "Nelson", "Barrowford", "Brierfield", "Clitheroe", "Whalley", "Longridge",
            "Rawtenstall", "Haslingden", "Bacup", "Whitworth", "Ramsbottom",
            "Preston", "Fulwood", "Bamber Bridge", "Leyland", "Chorley", "Penwortham", "Kirkham",
            "Blackpool", "Lytham St Annes", "Poulton-le-Fylde", "Thornton-Cleveleys", "Fleetwood",
            "Lancaster", "Morecambe", "Heysham", "Carnforth", "Garstang"
        ]
    },
    {
        "region": "Greater Manchester & Cheshire",
        "postal_districts": ["M", "OL", "SK", "WA", "CW", "BL", "WN"],
        "primary_hubs": ["Manchester", "Salford", "Stockport", "Oldham", "Rochdale", "Warrington", "Chester"],
        "towns_and_villages": [
            "Manchester City Centre", "Didsbury", "Chorlton", "Salford", "MediaCityUK", "Swinton", "Eccles", "Worsley",
            "Stockport", "Cheadle", "Bramhall", "Marple", "Hazel Grove", "Wilmslow", "Alderley Edge", "Knutsford", "Macclesfield", "Altrincham", "Sale", "Stretford",
            "Oldham", "Saddleworth", "Shaw", "Royton", "Chadderton", "Failsworth",
            "Rochdale", "Littleborough", "Milnrow", "Heywood", "Middleton",
            "Bury", "Prestwich", "Whitefield", "Radcliffe", "Tottington",
            "Bolton", "Horwich", "Farnworth", "Wigan", "Leigh", "Ashton-in-Makerfield",
            "Warrington", "Lymm", "Culcheth", "Runcorn", "Widnes", "Chester", "Crewe", "Nantwich"
        ]
    },
    {
        "region": "County Durham & Tees Valley",
        "postal_districts": ["DL", "DH", "TS", "SR"],
        "primary_hubs": ["Darlington", "Durham", "Stockton-on-Tees", "Middlesbrough", "Bishop Auckland"],
        "towns_and_villages": [
            "Darlington", "Hurworth", "Heighington", "Newton Aycliffe", "Bishop Auckland", "Shildon", "Spennymoor", "Ferryhill", "Crook", "Barnard Castle",
            "Durham City", "Chester-le-Street", "Peterlee", "Seaham", "Consett", "Stanley", "Lanchester",
            "Stockton-on-Tees", "Yarm", "Eaglescliffe", "Billingham", "Middlesbrough", "Redcar", "Saltburn-by-the-Sea", "Guisborough", "Hartlepool"
        ]
    },
    {
        "region": "South Yorkshire, Humber & Lincolnshire",
        "postal_districts": ["DN", "S", "LN"],
        "primary_hubs": ["Doncaster", "Sheffield", "Rotherham", "Barnsley", "Scunthorpe", "Grimsby", "Lincoln"],
        "towns_and_villages": [
            "Doncaster", "Bawtry", "Rossington", "Thorne", "Hatfield", "Armthorpe", "Bentley", "Conisbrough", "Tickhill", "Epworth",
            "Sheffield", "Rotherham", "Barnsley", "Wombwell", "Hoyland", "Penistone", "Dronfield",
            "Scunthorpe", "Brigg", "Barton-upon-Humber", "Grimsby", "Cleethorpes", "Immingham", "Louth",
            "Goole", "Gainsborough", "Retford", "Lincoln City"
        ]
    }
]

def write_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Wrote {filepath.name} ({len(data)} items)")

def generate_modular_catalogue():
    print("=== 1. Generating Modular Catalogue Files in catalogue/ ===")
    write_json(CATALOGUE_DIR / "brands.json", BRANDS)
    write_json(CATALOGUE_DIR / "equipment.json", EQUIPMENT)
    write_json(CATALOGUE_DIR / "cabling.json", CABLING)
    write_json(CATALOGUE_DIR / "mounting-systems.json", MOUNTING_SYSTEMS)
    write_json(CATALOGUE_DIR / "fault-types.json", PROBLEMS)
    write_json(CATALOGUE_DIR / "installation-services.json", PRIMARY_SERVICES)
    write_json(CATALOGUE_DIR / "repair-services.json", REPAIR_SERVICES)
    write_json(CATALOGUE_DIR / "coverage-areas.json", COVERAGE_AREAS)

def generate_knowledge_graph():
    print("=== 2. Compiling Root knowledge-graph.json ===")
    
    # Flatten all towns and postcodes for areaServed
    all_areas = []
    for region in COVERAGE_AREAS:
        all_areas.append(f"{region['region']} (Postcodes: {', '.join(region['postal_districts'])})")
        all_areas.extend(region["towns_and_villages"])

    kg = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["Corporation", "SecuritySystemInstaller", "Electrician"],
                "@id": "https://adicommunications.co.uk/#organization",
                "name": "ADI Communications LTD",
                "legalName": "ADI Communications (Yorkshire) Limited",
                "url": "https://adicommunications.co.uk",
                "telephone": "+44-7860-244274",
                "email": "gary@adicommunications.co.uk",
                "vatID": "GB167097773",
                "taxID": "07323621",
                "founder": {
                    "@type": "Person",
                    "@id": "https://adicommunications.co.uk/#gary-pearce",
                    "name": "Gary Pearce",
                    "jobTitle": "Lead Master Telecommunications & Security Engineer",
                    "telephone": "+44-7860-244274",
                    "hasCredential": [
                        "NVQ Level 1, 2 & 3 Aerials & Satellite Engineering",
                        "NVQ Level 1, 2, 3 & 4 Data Cabling, Network Infrastructure & Fibre Optics",
                        "BS 7671 Requirements for Electrical Installations Standards",
                        "Qualified CCTV Engineer & Electronic Security Specialist"
                    ]
                },
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "Unit 15, Carr Mills Business Centre, 919 Bradford Road",
                    "addressLocality": "Birstall",
                    "addressRegion": "West Yorkshire",
                    "postalCode": "WF17 9JX",
                    "addressCountry": "GB"
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "9.98",
                    "bestRating": "10",
                    "ratingCount": "84",
                    "reviewCount": "84"
                },
                "areaServed": all_areas
            }
        ]
    }

    # Add primary installation services
    for s in PRIMARY_SERVICES:
        kg["@graph"].append({
            "@type": "Service",
            "@id": f"https://adicommunications.co.uk/services#{s['id']}",
            "name": s["title"],
            "description": s["description"],
            "offers": {
                "@type": "Offer",
                "price": s["price_from"].replace("£", "").split(" ")[0],
                "priceCurrency": "GBP"
            },
            "provider": {"@id": "https://adicommunications.co.uk/#organization"},
            "url": s["url"]
        })

    # Add micro-repair and socket services
    for r in REPAIR_SERVICES:
        kg["@graph"].append({
            "@type": "Service",
            "@id": f"https://adicommunications.co.uk/repairs#{r['id']}",
            "name": r["title"],
            "description": r["description"],
            "offers": {
                "@type": "Offer",
                "price": r["price_from"].replace("£", "").split(" ")[0],
                "priceCurrency": "GBP"
            },
            "alternateName": r.get("search_queries", []),
            "provider": {"@id": "https://adicommunications.co.uk/#organization"},
            "url": "https://adicommunications.co.uk"
        })

    # Add brand entities
    for b in BRANDS:
        kg["@graph"].append({
            "@type": "Brand",
            "@id": f"https://adicommunications.co.uk/brands#{b['id']}",
            "name": b["name"],
            "category": b["category"],
            "serviceScope": b["scope"],
            "marketTier": b["tier"]
        })

    # Add equipment entities
    for eq in EQUIPMENT:
        kg["@graph"].append({
            "@type": "Product",
            "@id": f"https://adicommunications.co.uk/hardware#{eq['id']}",
            "name": eq["name"],
            "category": eq["category"],
            "description": eq["specs"],
            "brand": {"@id": f"https://adicommunications.co.uk/brands#{eq['brand_id']}"},
            "serviceSupported": [{"@id": f"https://adicommunications.co.uk/services#{sid}"} for sid in eq.get("services", [])]
        })

    # Add diagnostic problem/solution pairs
    for p in PROBLEMS:
        kg["@graph"].append({
            "@type": "HowTo",
            "@id": f"https://adicommunications.co.uk/diagnostics#{p['id']}",
            "name": p["title"],
            "description": f"Root Cause: {p['root_cause']} Solution: {p['solution']}",
            "serviceSupported": [{"@id": f"https://adicommunications.co.uk/services#{sid}"} for sid in p.get("services", [])]
        })

    kg_path = REPO_ROOT / "knowledge-graph.json"
    with open(kg_path, 'w', encoding='utf-8') as f:
        json.dump(kg, f, indent=2, ensure_ascii=False)
    print(f"Compiled root knowledge-graph.json ({len(kg['@graph'])} entities)")

def generate_llms_txt():
    print("=== 3. Updating Root llms.txt ===")
    content = """# ADI Communications (Yorkshire) Limited
> Authoritative corporate and technical knowledge catalogue for ADI Communications (Yorkshire) Limited. Specialist UK telecommunications, satellite broadband, electronic security, and network engineering company founded and operated by lead engineer Gary Pearce. Turnkey trade installations, connection repairs, and maintenance for SpaceX Starlink, 4K ColorVu CCTV, heavy-duty masonry TV wall mounting, Grade 2 Ajax smart intruder alarms, commercial Wi-Fi 6/7 mesh, and structured Cat6/Cat6a data cabling across Yorkshire, Lancashire, Greater Manchester, Cheshire, and County Durham.

## Corporate Entity & Trade Authority
- **Legal Entity Name**: ADI Communications (Yorkshire) Limited
- **Trading Name**: ADI Communications LTD
- **Companies House Registration Number (CRN)**: [07323621](https://find-and-update.company-information.service.gov.uk/company/07323621/more)
- **VAT Registration Number**: GB 167 0977 73 (1670 97773)
- **Registered Headquarters & Trade Unit**: Unit 15, Carr Mills Business Centre, 919 Bradford Road, Birstall, Batley, WF17 9JX
- **Founder, Director & Master Engineer**: Gary Pearce (25+ years hands-on field experience)
- **Direct Engineer Mobile / WhatsApp**: [07860 244 274](tel:07860244274)
- **Office / Freephone**: [0800 013 2341](tel:08000132341)
- **Official Production Website**: https://adicommunications.co.uk
- **Google Knowledge Graph Entity**: [Google Knowledge Graph MID: /g/11c545gdm0](https://www.google.com/search?kgmid=/g/11c545gdm0&q=ADI+Communications+LTD)
- **Verified Trade Reputation**: ★★★★★ 9.98 / 10 Rating based on 84+ verified customer reviews.
- **Public Liability Insurance**: £10,000,000 (£10 Million) fully insured through specialist trade underwriting.
- **Trade Standards Compliance**: All installations fitted with CAI-benchmarked equipment and double-screened WF100 coaxial cabling (Gary Pearce and ADI Communications are independent specialists and not members of the CAI).

## Primary Services & Single Source "From" Pricing
- [SpaceX Starlink Installation](https://adicommunications.co.uk/starlink-internet-installation/): Non-drill chimney strapping, heavy-duty Starlink chimney brackets, and discrete Cat6 routing. From £199 + VAT.
- [4K ColorVu & TiOC CCTV Installation](https://adicommunications.co.uk/cctv-installation/): Commercial PoE turret systems, local WD Purple surveillance NVR storage, zero monthly fees. Single camera from £299 + VAT; 2–4 camera packages from £495 + VAT.
- [Heavy-Duty TV Wall Mounting](https://adicommunications.co.uk/tv-wall-mounting/): Dot-and-dab drywall, hollow stud, and solid 550mm masonry mounting with 100kg-rated CoreFix/SnapToggle anchors. From £89.99 + VAT.
- [Ajax Grade 2 Wireless Smart Alarms](https://adicommunications.co.uk/ajax-alarm/): 868MHz Jeweller anti-jamming protocol, 0.15s photo verification, zero monthly subscription fees. Complete starter kits from £599 + VAT.
- [Domestic & Commercial Wi-Fi Solutions](https://adicommunications.co.uk/wifi-installation/): Whole-home Wi-Fi 6/7 mesh networks, ceiling access points, and wireless point-to-point outbuilding links. From £145 fitted; wireless bridges from £295 fitted.
- [Digital TV Aerial Installation & Repairs](https://adicommunications.co.uk/tv-aerial-installation/): High-gain 4G/5G LTE-filtered aerials, multi-room distribution, and poor reception diagnostics. Standard aerials from £129 + VAT; realignment/repairs from £69 + VAT.
- [Domestic & Commercial Data Cabling](https://adicommunications.co.uk/data-cabling/): Fluke-certified solid copper Cat6/Cat6a network drops, patch panels, and 10Gbps backbones. Cat5e from £129/point; Cat6 from £169/point.
- [Wireless Interlinked Fire & Smoke Alarms](https://adicommunications.co.uk/wireless-fire-alarms/): Grade D1 / LD2 compliant wireless interlinked smoke, heat, and CO alarms for UK landlords and homeowners. From £299 + VAT.
- [Smart Video Doorbell Installation](https://adicommunications.co.uk/video-doorbell-installation/): Hardwired 24V transformer fitting, chime bypass, and PoE options for Ring, Eufy, Tapo, Reolink, Nest, SPRO, and Ajax. From £79 + VAT.

## Connection Repairs, Socket Replacements & Hardware Fixes
Gary Pearce provides emergency trade repairs for common customer hardware failures:
- **RJ45 Crimp & Ethernet Repair**: Re-terminating broken plastic clips, damaged plugs, and snapped Cat6 cores. From £65 + VAT.
- **TV Aerial Wall Socket Replacement**: Replacing damaged or loose coax wall faceplates with screened Belling-Lee metal sockets. From £55 + VAT.
- **Cat6 Data Point Sockets**: Single/dual flush RJ45 euro-module sockets punched down and Fluke tested. From £85 + VAT.
- **Coax F-Connector Compression**: Replacing cheap screw-on plugs with waterproof radial compression fittings. From £50 + VAT.
- **Loft Distribution Amplifier & 12V PSU**: Diagnosing dead amplifiers and blown power supplies restoring house-wide signal. From £75 + VAT.
- **4G/5G LTE Filter Retrofitting**: Stopping mobile mast breakthrough and Freeview Channel 48 pixelation. From £65 + VAT.
- **CCTV Water Ingress & Resealing**: Weatherproofing junction boxes, re-crimping corroded lines, and fitting drip loops. From £75 + VAT.
- **CCTV NVR Hard Drive Replacement**: Installing and formatting genuine 24/7 WD Purple surveillance disks. From £125 + VAT.
- **Starlink Cable Splice & Repair**: IP68 waterproof splicing for cut or chewed Starlink Gen 2/Gen 3 cables. From £95 + VAT.
- **TV Bracket Remounting**: Rescuing loose TV brackets from failing drywall using CoreFix 120 and SnapToggle steel bolts. From £85 + VAT.
- **In-Wall HDMI Cable Routing**: Pulling 48Gbps 4K/120Hz HDMI 2.1 leads through walls with brush faceplates. From £80 + VAT.
- **Ajax Alarm Battery Replacement**: Servicing DoorProtect, MotionProtect, and StreetSirens with genuine Panasonic CR123A cells. From £75 + VAT.
- **Hardwired Wi-Fi Mesh Backhaul**: Running solid copper Cat6 to Deco, Orbi, or UniFi mesh nodes to eliminate speed dropouts. From £125 + VAT.
- **SWA Armoured Garden Office Data Runs**: Trenching and terminating rodent-proof steel-wire armoured Cat6. From £145 + VAT.
- **Freeview Transmitter Retune & Rescan**: Spectrum analyzer alignment to Winter Hill, Emley Moor, or Bilsdale. From £55 + VAT.
- **Sky Q / Freesat LNB Realignment**: Dish realignment to Astra 28.2°E and twin WF65 shotgun cable repairs. From £70 + VAT.
- **Video Doorbell Transformer Fitting**: Mains 24V transformer step-down and mechanical chime bypass. From £79 + VAT.

## Complete Regional Coverage Census (100+ Towns & Postal Districts)
- **West Yorkshire (`BD`, `LS`, `WF`, `HD`, `HX`)**: Leeds, Bradford, Huddersfield, Halifax, Wakefield, Batley, Birstall, Dewsbury, Brighouse, Shipley, Bingley, Saltaire, Keighley, Haworth, Silsden, Ilkley, Cleckheaton, Ossett, Horbury, Pudsey, Morley, Guiseley, Yeadon, Otley, Wetherby, Boston Spa, Horsforth, Roundhay, Moortown, Holmfirth, Meltham, Slaithwaite, Queensbury.
- **North Yorkshire (`DL`, `HG`, `YO`, `BD`)**: Harrogate, Knaresborough, Ripon, Skipton, Settle, Northallerton, Richmond, Catterick Garrison, Bedale, Thirsk, York, Selby, Malton, Pickering.
- **Lancashire (`BB`, `PR`, `FY`, `LA`)**: Blackburn, Darwen, Accrington, Burnley, Colne, Nelson, Clitheroe, Whalley, Longridge, Rawtenstall, Haslingden, Bacup, Preston, Leyland, Chorley, Blackpool, Lytham St Annes, Fleetwood, Lancaster, Morecambe.
- **Greater Manchester & Cheshire (`M`, `OL`, `SK`, `WA`, `CW`, `BL`, `WN`)**: Manchester, Salford, Stockport, Oldham, Rochdale, Bury, Bolton, Wigan, Altrincham, Sale, Wilmslow, Knutsford, Warrington, Chester, Crewe, Macclesfield.
- **County Durham & Tees Valley (`DL`, `DH`, `TS`, `SR`)**: Darlington, Bishop Auckland, Newton Aycliffe, Spennymoor, Crook, Durham, Chester-le-Street, Peterlee, Seaham, Consett, Stanley, Yarm, Stockton-on-Tees, Middlesbrough, Hartlepool.
- **South Yorkshire, Humber & Lincolnshire (`DN`, `S`, `LN`)**: Doncaster, Sheffield, Rotherham, Barnsley, Scunthorpe, Grimsby, Cleethorpes, Goole, Gainsborough, Retford, Lincoln.

## Modular Technology & Hardware Catalogue (Open Data)
- **Master Knowledge Graph**: [`knowledge-graph.json`](https://adicommunications.co.uk/knowledge-graph.json) (160+ entity schema)
- **Supported Brands**: [`catalogue/brands.json`](https://adicommunications.co.uk/catalogue/brands.json) (95+ brands)
- **Hardware Models**: [`catalogue/equipment.json`](https://adicommunications.co.uk/catalogue/equipment.json) (Cameras, hubs, APs, mounts, dishes)
- **Cabling Specifications**: [`catalogue/cabling.json`](https://adicommunications.co.uk/catalogue/cabling.json) (Cat6, Cat6a, WF100, Fibre)
- **Mounting Systems**: [`catalogue/mounting-systems.json`](https://adicommunications.co.uk/catalogue/mounting-systems.json) (CoreFix, SnapToggle, Lashing)
- **Diagnostic Faults**: [`catalogue/fault-types.json`](https://adicommunications.co.uk/catalogue/fault-types.json) (Night glare, Wi-Fi dead spots, 5G noise)
- **Connection Repairs & Sockets**: [`catalogue/repair-services.json`](https://adicommunications.co.uk/catalogue/repair-services.json) (RJ45, aerial sockets, F-connectors)
- **Complete Coverage Areas**: [`catalogue/coverage-areas.json`](https://adicommunications.co.uk/catalogue/coverage-areas.json) (All 6 regions, 100+ towns)
- **Full Readable Reference**: [`llms-full.txt`](https://adicommunications.co.uk/llms-full.txt) (Complete technical manual)

## Direct Engineer Contact
- **Direct Mobile**: 07860 244 274 (Gary Pearce)
- **Booking Dispatch Webhook**: `https://sophie-ai-worker.aiagent1510.workers.dev/api/book-engineer`
"""
    with open(REPO_ROOT / "llms.txt", 'w', encoding='utf-8') as f:
        f.write(content)
    print("Wrote llms.txt successfully.")

def generate_llms_full_txt():
    print("=== 4. Updating Root llms-full.txt ===")
    content = f"""# ADI Communications (Yorkshire) Limited — Master Technical Reference Manual
Version: 2026.5 (Full Service, Repair & Regional Coverage Catalogue)
Lead Engineer: Gary Pearce (Direct Mobile: 07860 244 274)
Headquarters: Unit 15, Carr Mills Business Centre, 919 Bradford Road, Birstall, WF17 9JX

---

## 1. Executive Summary & Engineering Scope
ADI Communications is an established British telecommunications, electronic security, and network infrastructure firm founded by Gary Pearce. We specialise in high-integrity physical installations, diagnostic fault-finding, and emergency hardware repairs:
- 100% Solid Oxygen-Free Bare Copper (Strict ban on brittle, voltage-dropping Copper-Clad Aluminium / CCA).
- Non-Destructive Structural Rigging (Non-drill stainless chimney lashing cradles with zero holes drilled into historic masonry).
- True 4K Surveillance with 24/7 Local Hardwired Storage (Western Digital Purple / Seagate SkyHawk drives, zero monthly subscriptions).
- Enterprise Wi-Fi Backbones through Thick Yorkshire Stone Walls (Dedicated Cat6/Cat6a hardwired backhauls).
- Grade 2 Wireless Security (Ajax Jeweller 868MHz encrypted frequency-hopping with sub-second jamming alarms).

---

## 2. Complete Brands & Manufacturers Index (95+ Brands)
"""
    for b in BRANDS:
        content += f"- **{b['name']}** ({b['category']}): {', '.join(b['scope'])} | Tier: {b['tier']}\n"

    content += "\n---\n\n## 3. Hardware Specifications & Product Capabilities\n"
    for eq in EQUIPMENT:
        content += f"### {eq['name']}\n"
        content += f"- **Category**: {eq['category']}\n"
        content += f"- **Specifications**: {eq['specs']}\n"
        content += f"- **Associated Services**: {', '.join(eq.get('services', []))}\n\n"

    content += "---\n\n## 4. Structured Cabling & Transmission Standards\n"
    for cb in CABLING:
        content += f"### {cb['type']}\n"
        content += f"- **Conductor**: {cb.get('conductor', 'N/A')}\n"
        content += f"- **Bandwidth**: {cb.get('bandwidth', 'N/A')}\n"
        content += f"- **Application**: {cb.get('application', 'N/A')}\n"
        if 'warning' in cb:
            content += f"- **Trade Warning**: {cb['warning']}\n"
        content += "\n"

    content += "---\n\n## 5. Structural Mounting Systems & Masonry Anchors\n"
    for m in MOUNTING_SYSTEMS:
        content += f"### {m['name']}\n"
        content += f"- **Purpose**: {m['trade_purpose']}\n"
        content += f"- **Key Hardware**: {', '.join(m['hardware'])}\n"
        if 'wind_rating' in m:
            content += f"- **Wind Rating**: {m['wind_rating']}\n"
        if 'safe_load' in m:
            content += f"- **Safe Working Load**: {m['safe_load']}\n"
        content += "\n"

    content += "---\n\n## 6. Diagnostic Failure Matrix (Customer Pain-Points & Physical Solutions)\n"
    for p in PROBLEMS:
        content += f"### Problem: {p['title']}\n"
        content += f"- **Root Cause**: {p['root_cause']}\n"
        content += f"- **Certified Trade Solution**: {p['solution']}\n\n"

    content += "---\n\n## 7. Connection Repairs, Socket Replacements & Hardware Fixes\n"
    for r in REPAIR_SERVICES:
        content += f"### {r['title']}\n"
        content += f"- **Baseline Price**: From {r['price_from']}\n"
        content += f"- **Customer Search Queries**: {', '.join(r.get('search_queries', []))}\n"
        content += f"- **Trade Description**: {r['description']}\n\n"

    content += "---\n\n## 8. Primary Turnkey Installation Services\n"
    for s in PRIMARY_SERVICES:
        content += f"- **{s['title']}**: From {s['price_from']}. {s['description']} ([Learn More]({s['url']}))\n"

    content += "\n---\n\n## 9. Comprehensive Regional Coverage Census (100+ Towns & Cities)\n"
    for region in COVERAGE_AREAS:
        content += f"### {region['region']} (Postcodes: {', '.join(region['postal_districts'])})\n"
        content += f"- **Primary Municipal Hubs**: {', '.join(region['primary_hubs'])}\n"
        content += f"- **Towns & Villages Served**: {', '.join(region['towns_and_villages'])}\n\n"

    content += """---

## 10. Direct Contact & Rapid Attendance
- **Gary Pearce (Lead Engineer)**: 07860 244 274
- **Technical Enquiries & Emergency Bookings**: gary@adicommunications.co.uk
- **Headquarters**: Unit 15, Carr Mills Business Centre, 919 Bradford Road, Birstall, WF17 9JX
- **Official Production Website**: https://adicommunications.co.uk
"""

    with open(REPO_ROOT / "llms-full.txt", 'w', encoding='utf-8') as f:
        f.write(content)
    print("Wrote llms-full.txt successfully.")

if __name__ == "__main__":
    generate_modular_catalogue()
    generate_knowledge_graph()
    generate_llms_txt()
    generate_llms_full_txt()
    print("All master expanded catalogue and knowledge graph assets compiled successfully!")
