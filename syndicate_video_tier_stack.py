#!/usr/bin/env python3
"""
syndicate_video_tier_stack.py
=============================
Master Multi-Tier Video Stacking Engine for ADI Communications & Gary Pearce.

Enforces Gary Pearce's Strict Linking Law:
1. Tier 1 (Apex): YouTube links directly to ADI website buffer/service pages & Blogger.
2. Tier 2 (Top-Level Platforms - Dailymotion, Vimeo, Internet Archive, Wistia):
   Links directly to ADI website buffer pages AND links up to the YouTube video/channel.
3. Tier 3 (Low-Level / Alt Platforms - Rumble, PeerTube, Bitchute, Odysee, DTube):
   Links EXCLUSIVELY to the YouTube video & channel. Zero links to adicommunications.co.uk.

Outputs ready-to-import CSV and JSON manifests for all platforms and runs
automated mathematical verification.
"""

import os
import json
import csv
from datetime import datetime, timezone

REPO_DIR = r"C:\Users\Gary\github-cctv-seo"
SYNDICATION_DIR = os.path.join(REPO_DIR, "syndication")
os.makedirs(SYNDICATION_DIR, exist_ok=True)

# Master Video Catalog with real YouTube IDs
VIDEOS = [
    {
        "id": "vid-01",
        "youtube_id": "dOFIxVqMxCM",
        "youtube_url": "https://www.youtube.com/watch?v=dOFIxVqMxCM",
        "youtube_short": "https://youtu.be/dOFIxVqMxCM",
        "title": "Starlink Gen 3 & Mini UK Installation: 90mph Gale Chimney Mounts, Bypass & Speed Test",
        "topic": "SpaceX Starlink Satellite Rigging",
        "category": "Broadband Infrastructure & Telecommunications",
        "duration_seconds": 45,
        "website_buffer": "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/",
        "blogger_shield": "https://tvandhomesecurity.blogspot.com/2026/10/starlink-installation-uk-chimney-mount.html",
        "timestamps": [
            "00:00 - Introduction by Gary Pearce (25+ Yrs Yorkshire Field Experience)",
            "00:08 - Starlink Gen 3 Dish Obstruction Survey & 110° Northern Orbital Cone",
            "00:18 - Non-Drill Chimney Lashing Kits vs Pennine 90mph Gale Brackets",
            "00:28 - UV-Rated Cat6 Exterior Drops, Drip Loops & Weatherproof Grommets",
            "00:38 - Gen 3 Router Bypass Mode & Whole-Home Wi-Fi 7 Mesh Integration"
        ],
        "tags": [
            "Starlink Installation UK", "SpaceX Starlink Gen 3", "Starlink Mini",
            "Non-Drill Chimney Mount", "90mph Gale Tested", "Gary Pearce",
            "ADI Communications", "Wi-Fi 7 Mesh", "West Yorkshire Broadband"
        ]
    },
    {
        "id": "vid-02",
        "youtube_id": "l-HN4BuzBGQ",
        "youtube_url": "https://www.youtube.com/watch?v=l-HN4BuzBGQ",
        "youtube_short": "https://youtu.be/l-HN4BuzBGQ",
        "title": "Ajax Smart Alarms UK Masterclass 2026: Why Legacy 433MHz Bells Fail & MotionCam PhOD",
        "topic": "Ajax Wireless Intrusion Detection",
        "category": "Physical Security & Smart Intruder Alarms",
        "duration_seconds": 46,
        "website_buffer": "https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/",
        "blogger_shield": "https://tvandhomesecurity.blogspot.com/2026/10/ajax-smart-alarms-uk-masterclass-2026.html",
        "timestamps": [
            "00:00 - Introduction by Gary Pearce (25+ Yrs Yorkshire Trade Experience)",
            "00:10 - Why Legacy 433MHz Alarms Are Jammed & Bypassed in Minutes",
            "00:22 - Ajax Jeweller 868MHz Frequency Hopping & Encrypted Rolling Code",
            "00:32 - StreetSiren Masonry Mounting & 90mph Gale Wind Testing",
            "00:40 - Hub 2 Plus Dual Micro-SIM Cellular Failover & Ethernet Integration"
        ],
        "tags": [
            "Ajax Smart Alarms", "Grade 2 Intruder Alarm", "Jeweller 868MHz",
            "Anti-Jamming Security", "MotionCam PhOD", "StreetSiren 113dB",
            "Gary Pearce", "ADI Communications", "Leeds Alarm Installation"
        ]
    },
    {
        "id": "vid-03",
        "youtube_id": "50q89TsNN3w",
        "youtube_url": "https://www.youtube.com/watch?v=50q89TsNN3w",
        "youtube_short": "https://youtu.be/50q89TsNN3w",
        "title": "Hikvision ColorVu vs Infrared CCTV UK: Night Vision, DORI Standards & 4K Police Evidence",
        "topic": "4K Ultra-HD Surveillance & Court Admissibility",
        "category": "Commercial & Domestic CCTV Engineering",
        "duration_seconds": 46,
        "website_buffer": "https://adicommunications.co.uk/news/hikvision-colorvu-vs-infrared-cctv-4k/",
        "blogger_shield": "https://tvandhomesecurity.blogspot.com/2026/10/hikvision-colorvu-vs-infrared-cctv-4k.html",
        "timestamps": [
            "00:00 - CCTV Night Vision Reality: Infrared Fogging & Spiderweb Glare",
            "00:12 - ColorVu 24/7 Full Colour Video with F1.0 Super-Aperture",
            "00:25 - DORI Admissibility Standards: 250 Pixels/Metre for Court Evidence",
            "00:38 - Hardwired PoE Cat6 vs Vulnerable Wi-Fi Jamming Attacks"
        ],
        "tags": [
            "Hikvision ColorVu", "4K CCTV UK", "Police Evidence CCTV",
            "BS EN 62676-4 DORI", "F1.0 Super Aperture", "PoE Data Cabling",
            "Gary Pearce", "ADI Communications", "Bradford CCTV Specialist"
        ]
    }
]

YOUTUBE_CHANNEL = "https://www.youtube.com/@CCTV.services"
GARY_PHONE = "07860 244 274"
GARY_TRADE = "Gary Pearce • ADI Communications (25+ Years Hands-On UK Security & Telecom Engineer, £10M Public Liability)"

def build_top_level_description(video, platform_name):
    """Tier 2: Links to website buffer AND Apex YouTube video."""
    desc = f"{video['title']}\n\n"
    desc += f"Official {platform_name} broadcast by {GARY_TRADE}. Direct mobile: {GARY_PHONE}.\n\n"
    desc += "Key Engineering Chapters:\n" + "\n".join(video['timestamps']) + "\n\n"
    desc += "Trade Standards & Verification:\n"
    desc += "• CAI-benchmarked equipment & double-screened WF100 / solid copper Cat6 cabling\n"
    desc += "• NVQ Level 1-4 Data Cabling, Fibre Optics & Electrical Standards\n"
    desc += "• ★★★★★ 9.98 / 10 Rating across 84+ verified reviews\n\n"
    desc += f"• Full 4K Masterclass on YouTube: {video['youtube_url']}\n"
    desc += f"• Official YouTube Channel: {YOUTUBE_CHANNEL}\n"
    desc += f"• Technical Field Notes & Calculators: {video['website_buffer']}\n"
    desc += f"• Google Shield Blogger Specification: {video['blogger_shield']}\n"
    desc += f"\nTelephone Enquiries: {GARY_PHONE} (Gary Pearce)"
    return desc

def build_low_level_description(video, platform_name):
    """Tier 3: Links EXCLUSIVELY to YouTube. Zero links to adicommunications.co.uk."""
    desc = f"{video['title']}\n\n"
    desc += f"Decentralized {platform_name} mirror by {GARY_TRADE}. Direct mobile: {GARY_PHONE}.\n\n"
    desc += "Key Engineering Chapters:\n" + "\n".join(video['timestamps']) + "\n\n"
    desc += "Trade Standards & Verification:\n"
    desc += "• CAI-benchmarked equipment & double-screened WF100 / solid copper Cat6 cabling\n"
    desc += "• NVQ Level 1-4 Data Cabling, Fibre Optics & Electrical Standards\n"
    desc += "• ★★★../../ 9.98 / 10 Rating across 84+ verified reviews\n\n"
    desc += "--- OFFICIAL VIDEO SOURCE ---\n"
    desc += f"Watch the original full 4K masterclass on YouTube:\n{video['youtube_url']}\n\n"
    desc += f"Subscribe to the Official YouTube Entity Channel:\n{YOUTUBE_CHANNEL}\n\n"
    desc += f"Engineer Direct Telephone: {GARY_PHONE} (Gary Pearce)"
    return desc

def generate_tier_manifests():
    print("======================================================================")
    print("GENERATING MULTI-TIER VIDEO STACK MANIFESTS")
    print("======================================================================")

    # 1. Tier 2 Top-Level Platforms
    top_platforms = [
        {"name": "DailyMotion", "dir": "dailymotion", "da": 95},
        {"name": "Vimeo", "dir": "vimeo", "da": 97},
        {"name": "Wistia", "dir": "wistia", "da": 92},
        {"name": "Internet Archive", "dir": "archive_org", "da": 98}
    ]

    for plat in top_platforms:
        plat_dir = os.path.join(SYNDICATION_DIR, plat["dir"])
        os.makedirs(plat_dir, exist_ok=True)
        
        items = []
        csv_rows = []
        for vid in VIDEOS:
            desc = build_top_level_description(vid, plat["name"])
            entry = {
                "video_id": vid["id"],
                "youtube_source": vid["youtube_url"],
                "title": vid["title"],
                "tier": "Tier 2 (Top-Level)",
                "platform": plat["name"],
                "da": plat["da"],
                "outbound_website_link": vid["website_buffer"],
                "outbound_youtube_link": vid["youtube_url"],
                "tags": ", ".join(vid["tags"]),
                "description": desc,
                "phone": GARY_PHONE
            }
            items.append(entry)
            csv_rows.append({
                "Video ID": vid["id"],
                "YouTube Source": vid["youtube_url"],
                "Title": vid["title"],
                "Tier": "Tier 2",
                "Platform": plat["name"],
                "Website Link": vid["website_buffer"],
                "YouTube Link": vid["youtube_url"],
                "Tags": ", ".join(vid["tags"]),
                "Description": desc
            })

        # Save JSON
        json_path = os.path.join(plat_dir, f"{plat['dir']}_video_manifest.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "platform": plat["name"],
                "tier": "Tier 2 (Top-Level)",
                "da": plat["da"],
                "linking_rule": "Links to Website Buffer AND Apex YouTube Video",
                "total_videos": len(items),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "videos": items
            }, f, indent=2)

        # Save CSV
        csv_path = os.path.join(plat_dir, f"{plat['dir']}_video_manifest.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
            writer.writeheader()
            writer.writerows(csv_rows)

        print(f"[TIER 2] Generated {plat['name']} manifests: {json_path}")

    # 2. Tier 3 Low-Level Platforms
    low_platforms = [
        {"name": "Rumble", "dir": "rumble", "da": 90},
        {"name": "PeerTube", "dir": "peertube", "da": 82},
        {"name": "Bitchute", "dir": "bitchute", "da": 78},
        {"name": "Odysee", "dir": "odysee", "da": 84},
        {"name": "DTube", "dir": "dtube", "da": 75}
    ]

    for plat in low_platforms:
        plat_dir = os.path.join(SYNDICATION_DIR, plat["dir"])
        os.makedirs(plat_dir, exist_ok=True)
        
        items = []
        csv_rows = []
        for vid in VIDEOS:
            desc = build_low_level_description(vid, plat["name"])
            entry = {
                "video_id": vid["id"],
                "youtube_source": vid["youtube_url"],
                "title": vid["title"],
                "tier": "Tier 3 (Low-Level)",
                "platform": plat["name"],
                "da": plat["da"],
                "outbound_website_link": "NONE (RULE ENFORCED: YOUTUBE ONLY)",
                "outbound_youtube_link": vid["youtube_url"],
                "tags": ", ".join(vid["tags"]),
                "description": desc,
                "phone": GARY_PHONE
            }
            items.append(entry)
            csv_rows.append({
                "Video ID": vid["id"],
                "YouTube Source": vid["youtube_url"],
                "Title": vid["title"],
                "Tier": "Tier 3",
                "Platform": plat["name"],
                "Website Link": "NONE",
                "YouTube Link": vid["youtube_url"],
                "Tags": ", ".join(vid["tags"]),
                "Description": desc
            })

        # Save JSON
        json_path = os.path.join(plat_dir, f"{plat['dir']}_video_manifest.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "platform": plat["name"],
                "tier": "Tier 3 (Low-Level)",
                "da": plat["da"],
                "linking_rule": "Links EXCLUSIVELY to Apex YouTube Video & Channel (Zero Website Links)",
                "total_videos": len(items),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "videos": items
            }, f, indent=2)

        # Save CSV
        csv_path = os.path.join(plat_dir, f"{plat['dir']}_video_manifest.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
            writer.writeheader()
            writer.writerows(csv_rows)

        print(f"[TIER 3] Generated {plat['name']} manifests: {json_path}")

    # 3. Master Consolidated Video Stacking Registry
    master_manifest_path = os.path.join(REPO_DIR, "video_stack_master_tiers.json")
    all_platforms = top_platforms + low_platforms
    with open(master_manifest_path, "w", encoding="utf-8") as f:
        json.dump({
            "title": "ADI Communications — Master Multi-Tier Video Stacking Registry",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "apex_youtube_channel": YOUTUBE_CHANNEL,
            "total_platforms": len(all_platforms),
            "tier_summary": {
                "tier_1_apex": ["YouTube (@CCTV.services, DA 100)"],
                "tier_2_top_level": [f"{p['name']} (DA {p['da']})" for p in top_platforms],
                "tier_3_low_level": [f"{p['name']} (DA {p['da']})" for p in low_platforms]
            },
            "linking_invariants": {
                "tier_1_apex": "Links to adicommunications.co.uk & tvandhomesecurity.blogspot.com",
                "tier_2_top_level": "Links to adicommunications.co.uk/news/... & youtube.com",
                "tier_3_low_level": "Links to youtube.com ONLY (0 raw website links)"
            },
            "videos": VIDEOS
        }, f, indent=2)
    print(f"\n[MASTER] Generated consolidated tier registry: {master_manifest_path}")

def run_empirical_verification():
    print("\n======================================================================")
    print("RUNNING EMPIRICAL AUDIT OF VIDEO STACK LINKING RULES")
    print("======================================================================")

    # Verify Tier 2 files
    top_dirs = ["dailymotion", "vimeo", "wistia", "archive_org"]
    for td in top_dirs:
        j_path = os.path.join(SYNDICATION_DIR, td, f"{td}_video_manifest.json")
        assert os.path.exists(j_path), f"Missing Tier 2 manifest: {j_path}"
        with open(j_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for v in data["videos"]:
            assert "youtube.com" in v["description"], f"Tier 2 missing YouTube link in {td}"
            assert "adicommunications.co.uk" in v["description"], f"Tier 2 missing Website link in {td}"
        print(f"[PASS] Tier 2 {td}: Contains both YouTube and Website buffer links cleanly.")

    # Verify Tier 3 files
    low_dirs = ["rumble", "peertube", "bitchute", "odysee", "dtube"]
    for ld in low_dirs:
        j_path = os.path.join(SYNDICATION_DIR, ld, f"{ld}_video_manifest.json")
        assert os.path.exists(j_path), f"Missing Tier 3 manifest: {j_path}"
        with open(j_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for v in data["videos"]:
            assert "youtube.com" in v["description"], f"Tier 3 missing YouTube link in {ld}"
            assert "adicommunications.co.uk" not in v["description"], (
                f"VIOLATION: Tier 3 platform {ld} contains direct website link!"
            )
        print(f"[PASS] Tier 3 {ld}: Strictly YouTube ONLY — Zero website links detected.")

    print("\n>>> ALL VIDEO STACK TIER AUDITS PASSED WITH 100% PERFECTION! <<<")

if __name__ == "__main__":
    generate_tier_manifests()
    run_empirical_verification()
