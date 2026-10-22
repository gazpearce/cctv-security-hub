import json
import os
import re

MANIFEST_FILE = "image_stack_manifest.json"

with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Topic-based metadata map
TOPIC_MAP = {
    "starlink": {
        "topic": "SpaceX Starlink Installation",
        "category": "Satellite & Broadband Rigging",
        "apex_google": "https://tvandhomesecurity.blogspot.com/2026/10/starlink-installation-uk-chimney-mount.html",
        "apex_youtube": "https://www.youtube.com/@CCTV.services",
        "money_post": "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex-brackets/",
        "tags": ["#StarlinkInstallation", "#StarlinkUK", "#ChimneyMount", "#Pennine90mphGale", "#Eurocode1", "#GaryPearce", "#ADISatellite", "#RuralBroadband"]
    },
    "ajax": {
        "topic": "Ajax Wireless Smart Alarm",
        "category": "Intruder Security & Intrusion Detection",
        "apex_google": "https://tvandhomesecurity.blogspot.com/2026/10/ajax-smart-alarms-uk-masterclass-2026.html",
        "apex_youtube": "https://www.youtube.com/@CCTV.services",
        "money_post": "https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/",
        "tags": ["#AjaxAlarms", "#SmartAlarmsUK", "#Grade2Security", "#JewellerWireless", "#MotionCamPhOD", "#GaryPearce", "#ADISecurity", "#Blackburn"]
    },
    "cat6": {
        "topic": "Data Cabling & SOHO Networking",
        "category": "Structured Copper & Fibre Infrastructure",
        "apex_google": "https://tvandhomesecurity.blogspot.com/2026/10/how-to-get-ethernet-upstairs-without-running-cables.html",
        "apex_youtube": "https://www.youtube.com/@CCTV.services",
        "money_post": "https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/",
        "tags": ["#Cat6Cabling", "#EthernetUpstairs", "#HomeNetworking", "#SolidCopper", "#FlukeTested", "#GaryPearce", "#ADITelecoms", "#CavityWallDrop"]
    },
    "ethernet": {
        "topic": "Data Cabling & SOHO Networking",
        "category": "Structured Copper & Fibre Infrastructure",
        "apex_google": "https://tvandhomesecurity.blogspot.com/2026/10/how-to-get-ethernet-upstairs-without-running-cables.html",
        "apex_youtube": "https://www.youtube.com/@CCTV.services",
        "money_post": "https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/",
        "tags": ["#Cat6Cabling", "#EthernetUpstairs", "#HomeNetworking", "#SolidCopper", "#FlukeTested", "#GaryPearce", "#ADITelecoms", "#CavityWallDrop"]
    },
    "tv": {
        "topic": "Architectural TV Wall Mounting",
        "category": "Heavy Duty AV & Thermal Protection",
        "apex_google": "https://tvandhomesecurity.blogspot.com/2026/10/tv-mounting-above-fireplaces-in-uk.html",
        "apex_youtube": "https://www.youtube.com/@CCTV.services",
        "money_post": "https://adicommunications.co.uk/news/tv-above-fireplace-safe-installation/",
        "tags": ["#TVMounting", "#FireplaceTV", "#CorefixAnchors", "#SamsungTheFrame", "#OLEDThermalSafety", "#GaryPearce", "#ADIAudioVisual"]
    },
    "cctv": {
        "topic": "Commercial & Domestic 4K CCTV",
        "category": "Electronic Surveillance & Police Evidence",
        "apex_google": "https://tvandhomesecurity.blogspot.com/2026/10/hikvision-colorvu-vs-infrared-cctv-4k.html",
        "apex_youtube": "https://www.youtube.com/@CCTV.services",
        "money_post": "https://adicommunications.co.uk/news/hikvision-colorvu-vs-infrared-cctv/",
        "tags": ["#CCTVInstallation", "#HikvisionColorVu", "#PoliceEvidence", "#DORIStandards", "#4KCCTV", "#GaryPearce", "#ADISecurity", "#NightVision"]
    }
}

DRIVE_VAULT = "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88"

for img in data.get("images", []):
    fname = img.get("filename", "").lower()
    title = img.get("title", "")
    
    # Determine topic
    selected_topic = None
    for k in ["starlink", "ajax", "cat6", "ethernet", "tv", "cctv"]:
        if k in fname:
            selected_topic = TOPIC_MAP[k]
            break
    if not selected_topic:
        selected_topic = TOPIC_MAP["cctv"]
        
    # Extract town if in filename
    town = "Yorkshire & Lancashire"
    for t in ["shadsworth", "beardwood", "livesey", "mill-hill", "feniscowles", "rishton", "adwick", "armthorpe", "brigg", "thorne", "sheffield", "bradford", "huddersfield", "halifax", "wakefield", "york", "harrogate", "whitebirk", "leeds", "manchester", "almondbury", "brighouse", "beverley", "accrington"]:
        if t in fname:
            town = t.replace("-", " ").title()
            break

    # Build rich About & SEO Description
    about_text = (
        f"{title} — Professional UK installation in {town} by Gary Pearce, lead physical security "
        f"and telecommunications engineer at ADI Communications (Direct Mobile: 07860 244 274). "
        f"With over 25 years hands-on field craftsmanship, £10,000,000 Public Liability Insurance, "
        f"and CAI-benchmarked equipment across Yorkshire, Lancashire, and Greater Manchester.\n\n"
        f"Hardware & Installation Standards:\n"
        f"• Fully compliant with British Trade Standards (BS EN 62676-4 DORI, Eurocode 1 wind shear, or BS EN 50131 Grade 2).\n"
        f"• Discrete weatherproof cable entries, downward drip loops, and non-destructive masonry fixings.\n\n"
        f"Top of Stack Apex Links:\n"
        f"📷 High-Resolution Trade Photo Vault (Google Drive): {DRIVE_VAULT}\n"
        f"📺 4K Field Masterclasses (YouTube): {selected_topic['apex_youtube']}\n"
        f"📖 Official Google Companion Guide (Blogger DA 99): {selected_topic['apex_google']}\n"
        f"🔗 Technical Installation Specifications: {selected_topic['money_post']}\n\n"
        f"Tags: {' '.join(selected_topic['tags'])}"
    )

    img["about_section_markdown"] = about_text
    img["description"] = about_text
    img["seo_tags"] = selected_topic["tags"]
    img["top_of_stack_google_url"] = DRIVE_VAULT
    img["companion_blogger_url"] = selected_topic["apex_google"]
    img["top_of_stack_youtube_url"] = selected_topic["apex_youtube"]
    img["money_post_url"] = selected_topic["money_post"]
    img["google_shield_anchor"] = selected_topic["money_post"]
    if "clickable_backlink_target" in img:
        img["clickable_backlink_target"]["type_c_rule_45_anchor"] = selected_topic["money_post"]

with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Upgraded {len(data.get('images', []))} images in {MANIFEST_FILE} with rich About sections, tags, and Top-of-Stack Apex links.")
