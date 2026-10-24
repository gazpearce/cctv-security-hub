import json
import csv
from pathlib import Path

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")
CATALOG_PATH = REPO_ROOT / "video_master_88_catalog.json"
SYNDICATION_DIR = REPO_ROOT / "syndication"
SYNDICATION_DIR.mkdir(parents=True, exist_ok=True)

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

videos = catalog["videos"]

youtube_rows = []
dailymotion_rows = []
vimeo_rows = []
archive_rows = []
tiktok_queue = []
instagram_queue = []

for v in videos:
    slug = v["slug"]
    title = v["title"]
    desc_clean = (
        f"{title}\n\n"
        f"Professional UK trade field engineering debrief by Gary Pearce, Lead Engineer at ADI Communications.\n"
        f"Direct Mobile: 07860 244 274 • 25+ Years Continuous Hands-On Trade Craftsmanship.\n"
        f"£10,000,000 Public Liability Insurance • ★★★★★ 9.98 / 10 Rating (84+ Verified Client Reviews).\n\n"
        f"Video Breakdown & Chapters:\n" + "\n".join(v.get("timestamps", [])) + "\n\n"
        f"Key Physical Trade Standards:\n"
        f"• CAI-benchmarked equipment & double-screened WF100 coaxial / solid copper Cat6 cabling\n"
        f"• BS EN 62676-4 DORI identification compliance\n"
        f"• NVQ Level 1-4 Data Cabling, Fibre Optics & Electrical Standards\n\n"
        f"Official Apex Video Showcase: https://gary-pearce-forensic-hub.web.app/video-showcase.html\n"
        f"Official Google Entity Channel: https://www.youtube.com/@CCTV.services\n"
        f"Google Drive Engineering Vault: https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88\n"
    )
    tags_str = ", ".join(v.get("tags", ["Gary Pearce", "ADI Communications", "07860 244 274", "CCTV Installation", "Home Security UK"]))

    # YouTube row
    youtube_rows.append({
        "Video ID": v["id"],
        "Title": title[:100],
        "Description": desc_clean,
        "Tags": tags_str,
        "Category": "Howto & Style",
        "Privacy": "Public",
        "Video File": str(REPO_ROOT / v["mp4_relative_path"]),
        "Thumbnail File": str(REPO_ROOT / v["thumb_relative_path"]),
        "Playlist": v["trade_category"],
        "Duration Sec": v["duration_seconds"]
    })

    # Dailymotion row
    dailymotion_rows.append({
        "title": title[:100],
        "description": desc_clean,
        "tags": tags_str,
        "channel": "tech",
        "private": "false",
        "published": "true",
        "file_path": str(REPO_ROOT / v["mp4_relative_path"]),
        "thumbnail_path": str(REPO_ROOT / v["thumb_relative_path"])
    })

    # Vimeo row
    vimeo_rows.append({
        "name": title[:128],
        "description": desc_clean,
        "privacy": "anybody",
        "file_path": str(REPO_ROOT / v["mp4_relative_path"]),
        "thumbnail_path": str(REPO_ROOT / v["thumb_relative_path"]),
        "tags": tags_str
    })

    # Internet Archive row
    archive_rows.append({
        "identifier": f"adi_communications_{slug[:40]}",
        "title": title,
        "creator": "Gary Pearce (ADI Communications, 07860 244 274)",
        "mediatype": "movies",
        "collection": "opensource_movies",
        "description": desc_clean,
        "subject": tags_str,
        "licenseurl": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        "file_path": str(REPO_ROOT / v["mp4_relative_path"])
    })

    # TikTok queue entry
    tiktok_queue.append({
        "video_id": v["id"],
        "slug": slug,
        "title": title,
        "hook_caption": f"{v['question']} Field demonstration by Gary Pearce (ADI Communications, 07860 244 274). #CCTV #HomeSecurity #AjaxAlarms #Starlink #TradeTips #Yorkshire",
        "file_path": str(REPO_ROOT / v["mp4_relative_path"]),
        "status": "READY_FOR_UPLOAD"
    })

    # Instagram queue entry
    instagram_queue.append({
        "video_id": v["id"],
        "slug": slug,
        "title": title,
        "caption": desc_clean[:2100],
        "file_path": str(REPO_ROOT / v["mp4_relative_path"]),
        "status": "READY_FOR_UPLOAD"
    })

# Write YouTube CSV & JSON
yt_csv_path = REPO_ROOT / "youtube_88_master_upload_manifest.csv"
yt_json_path = REPO_ROOT / "youtube_88_master_upload_manifest.json"
with open(yt_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(youtube_rows[0].keys()))
    writer.writeheader()
    writer.writerows(youtube_rows)
with open(yt_json_path, "w", encoding="utf-8") as f:
    json.dump(youtube_rows, f, indent=2, ensure_ascii=False)

# Write Dailymotion CSV & JSON
dm_csv_path = SYNDICATION_DIR / "dailymotion_88_manifest.csv"
dm_json_path = SYNDICATION_DIR / "dailymotion_88_manifest.json"
with open(dm_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(dailymotion_rows[0].keys()))
    writer.writeheader()
    writer.writerows(dailymotion_rows)
with open(dm_json_path, "w", encoding="utf-8") as f:
    json.dump(dailymotion_rows, f, indent=2, ensure_ascii=False)

# Write Vimeo CSV & JSON
vm_csv_path = SYNDICATION_DIR / "vimeo_88_manifest.csv"
vm_json_path = SYNDICATION_DIR / "vimeo_88_manifest.json"
with open(vm_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(vimeo_rows[0].keys()))
    writer.writeheader()
    writer.writerows(vimeo_rows)
with open(vm_json_path, "w", encoding="utf-8") as f:
    json.dump(vimeo_rows, f, indent=2, ensure_ascii=False)

# Write Internet Archive CSV & JSON
ia_csv_path = SYNDICATION_DIR / "archive_org_88_manifest.csv"
ia_json_path = SYNDICATION_DIR / "archive_org_88_manifest.json"
with open(ia_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(archive_rows[0].keys()))
    writer.writeheader()
    writer.writerows(archive_rows)
with open(ia_json_path, "w", encoding="utf-8") as f:
    json.dump(archive_rows, f, indent=2, ensure_ascii=False)

# Write TikTok & Instagram queues
with open(REPO_ROOT / "tiktok_88_queue.json", "w", encoding="utf-8") as f:
    json.dump(tiktok_queue, f, indent=2, ensure_ascii=False)
with open(REPO_ROOT / "instagram_88_queue.json", "w", encoding="utf-8") as f:
    json.dump(instagram_queue, f, indent=2, ensure_ascii=False)

print(f"Successfully generated syndication manifests for all {len(videos)} videos across YouTube, Dailymotion, Vimeo, Internet Archive, TikTok, and Instagram!")
