#!/usr/bin/env python3
"""
build_pinterest_manifest.py
===========================
Generates 185 high-intent, LLM/GEO-optimized Pinterest Pins for Gary Pearce / ADI Communications.
Maps every video to its corresponding Pinterest board, unique 1280x720 thumbnail, rich description,
and destination URL anchoring to the Video Showcase Vault.
"""

import json
import csv
from pathlib import Path

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")
CATALOG_PATH = REPO_ROOT / "video_master_185_catalog.json"
OUT_JSON = REPO_ROOT / "pinterest_185_master_manifest.json"
OUT_CSV = REPO_ROOT / "pinterest_185_master_manifest.csv"

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

videos = catalog["videos"]

def assign_board(ch_num: int, category: str, title: str) -> str:
    text = (category + " " + title).lower()
    if ch_num in [1, 2, 10, 11] or "cctv" in text or "camera" in text or "hikvision" in text or "dahua" in text or "tapo" in text:
        return "CCTV Installation & Night Vision (UK)"
    elif ch_num in [3, 4, 16] or "alarm" in text or "ajax" in text or "intruder" in text or "sensor" in text:
        return "Ajax Smart Wireless Alarms (Grade 2)"
    elif ch_num in [9, 17] or "starlink" in text or "satellite" in text or "dish" in text:
        return "Starlink UK High-Speed Internet Mounts"
    elif ch_num in [5, 6, 12, 18] or "wi-fi" in text or "wifi" in text or "cat6" in text or "mesh" in text or "ethernet" in text or "network" in text:
        return "Whole-Home Wi-Fi 7 & Cat6 Cabling"
    elif ch_num in [7, 8, 14, 15] or "tv" in text or "mount" in text or "aerial" in text or "wall" in text or "bracket" in text:
        return "TV Wall Mounting & Media Walls"
    return "CCTV Installation & Night Vision (UK)"

pin_rows = []

for idx, v in enumerate(videos, 1):
    slug = v["slug"]
    title = v["title"]
    ch_num = v["chapter_number"]
    category = v["trade_category"]
    board = assign_board(ch_num, category, title)
    
    clean_title = f"{title[:80]} | ADI Communications"
    dest_url = f"https://gary-pearce-forensic-hub.web.app/video-showcase.html#{slug}"
    thumb_path = str(REPO_ROOT / v["thumb_relative_path"])
    
    # 2026 Pinterest & LLM SEO Description (BLUF + Technical specs + Gary Pearce credentials)
    description = (
        f"{title}.\n\n"
        f"UK Field Trade Analysis: {v['bluf_answer'][:240]}...\n\n"
        f"Key Physical Standards:\n"
        f"• CAI-benchmarked equipment & double-screened WF100 / solid copper Cat6 cabling\n"
        f"• £10,000,000 Public Liability Insurance\n"
        f"• ★★★★★ 9.98 / 10 Rating across 84+ verified reviews\n"
        f"• Gary Pearce Direct Mobile: 07860 244 274\n\n"
        f"#CCTVInstallation #HomeSecurityUK #Hikvision #AjaxAlarms #StarlinkUK #TradesmanUK #GaryPearce #YorkshireTrades"
    )
    
    pin_entry = {
        "pin_id": f"pin-{idx:03d}",
        "chapter": ch_num,
        "board_name": board,
        "title": clean_title,
        "description": description[:495],
        "destination_url": dest_url,
        "media_file": thumb_path,
        "relative_media": v["thumb_relative_path"],
        "schedule_slot_day": (idx // 8) + 1,
        "daily_slot": (idx % 8) + 1,
        "status": "READY_TO_PIN"
    }
    pin_rows.append(pin_entry)

# Write JSON manifest
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(pin_rows, f, indent=2, ensure_ascii=False)

# Write CSV manifest for bulk upload / automation
with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(pin_rows[0].keys()))
    writer.writeheader()
    writer.writerows(pin_rows)

print(f"Successfully generated Pinterest 185 Master Manifest!")
print(f"  JSON: {OUT_JSON}")
print(f"  CSV:  {OUT_CSV}")
print(f"Total Pins: {len(pin_rows)} mapped across 5 high-authority boards.")
