import os
import re
import json
import hashlib
import time
import requests

ASSETS_DIR = r"C:\Users\Gary\github-cctv-seo\assets\images"
MANIFEST_FILE = r"C:\Users\Gary\github-cctv-seo\image_stack_manifest.json"
FREEIMAGE_API_KEY = "6d207e02198a847aa98d0a2a901485a5"

# Load existing manifest if present
if os.path.exists(MANIFEST_FILE):
    try:
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception:
        manifest = {}
else:
    manifest = {}

if "images" not in manifest:
    manifest = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "ADI Communications — Multi-Surface Image Stacking Manifest",
        "version": "2.0.0",
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S+01:00"),
        "total_images": 0,
        "type_a_direct_urls": 0,
        "type_b_viewer_pages": 0,
        "type_c_shield_anchors": 0,
        "images": []
    }

# Build map of existing entries by filename
existing_map = {item["filename"]: item for item in manifest.get("images", [])}

images_processed = 0
new_uploads = 0

print("======================================================================")
print("STARTING MULTI-SURFACE IMAGE STACK SYNDICATOR")
print("======================================================================")

files = sorted([f for f in os.listdir(ASSETS_DIR) if f.endswith(".webp")])
print(f"Found {len(files)} trade WebP images in {ASSETS_DIR}")

for idx, filename in enumerate(files, 1):
    file_path = os.path.join(ASSETS_DIR, filename)
    file_size = os.path.getsize(file_path)
    
    with open(file_path, "rb") as fp:
        raw_bytes = fp.read()
        sha256 = hashlib.sha256(raw_bytes).hexdigest()

    # Determine topic and buffer anchor
    clean_title = filename.replace(".webp", "").replace("-", " ").title()
    clean_title = clean_title.replace("Cctv", "CCTV").replace("Uk", "UK").replace("Poe", "PoE").replace("Sim", "SIM").replace("Ai", "AI")
    
    if "starlink" in filename.lower():
        topic = "SpaceX Starlink Installation"
        shield_anchor = "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/"
        category = "Satellite & Broadband Rigging"
    elif "ajax" in filename.lower():
        topic = "Ajax Wireless Smart Alarm"
        shield_anchor = "https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/"
        category = "Intruder Security & Intrusion Detection"
    elif "cat6" in filename.lower() or "ethernet" in filename.lower() or "patch" in filename.lower():
        topic = "Data Cabling & SOHO Networking"
        shield_anchor = "https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/"
        category = "Structured Copper & Fibre Infrastructure"
    elif "aerial" in filename.lower() or "fault-finder" in filename.lower():
        topic = "TV Aerial Signal Diagnostics & Coaxial Fault Finding"
        shield_anchor = "https://adicommunications.co.uk/news/tv-aerial-signal-fault-finder/"
        category = "Broadcast RF Engineering & Coax Diagnostics"
    elif "tv" in filename.lower() or "fireplace" in filename.lower():
        topic = "Architectural TV Wall Mounting"
        shield_anchor = "https://adicommunications.co.uk/news/tv-above-fireplace-safe-installation/"
        category = "Heavy Duty AV & Thermal Protection"
    else:
        topic = "Commercial & Domestic 4K CCTV"
        shield_anchor = "https://tvandhomesecurity.blogspot.com/"
        category = "Electronic Surveillance & Police Evidence"

    trade_desc = (
        f"{clean_title} — Professional UK installation by Gary Pearce, ADI Communications (07860 244 274). "
        f"25+ years hands-on field craftsmanship, £10,000,000 Public Liability insurance, "
        f"and CAI-benchmarked hardware across Yorkshire & Lancashire. "
        f"Technical Debrief & Interactive Engineering Tools: {shield_anchor}"
    )

    jsdelivr_url = f"https://cdn.jsdelivr.net/gh/gazpearce/cctv-security-hub@master/assets/images/{filename}"
    github_raw = f"https://raw.githubusercontent.com/gazpearce/cctv-security-hub/master/assets/images/{filename}"
    firebase_cdn = f"https://gary-pearce-forensic-hub.web.app/assets/images/{filename}"

    entry = existing_map.get(filename)
    
    # If not yet uploaded to external host or missing viewer url, perform upload
    if not entry or not entry.get("external_viewer_page"):
        print(f"[{idx}/{len(files)}] Syndicating {filename} to FreeImage.Host API...")
        try:
            with open(file_path, "rb") as fp:
                r = requests.post(
                    "https://freeimage.host/api/1/upload",
                    data={
                        "key": FREEIMAGE_API_KEY,
                        "action": "upload",
                        "format": "json",
                        "title": clean_title,
                        "description": trade_desc
                    },
                    files={"source": fp},
                    timeout=20
                )
            if r.status_code == 200:
                resp_data = r.json()
                img_data = resp_data.get("image", {})
                ext_direct = img_data.get("url")
                ext_viewer = img_data.get("url_viewer")
                ext_thumb = img_data.get("thumb", {}).get("url")
                print(f"    -> Direct: {ext_direct}")
                print(f"    -> Viewer: {ext_viewer}")
                new_uploads += 1
            else:
                print(f"    -> API returned status {r.status_code}")
                ext_direct = None
                ext_viewer = None
                ext_thumb = None
        except Exception as e:
            print(f"    -> Upload exception: {e}")
            ext_direct = None
            ext_viewer = None
            ext_thumb = None
    else:
        ext_direct = entry.get("external_direct_url")
        ext_viewer = entry.get("external_viewer_page")
        ext_thumb = entry.get("external_thumb_url")

    updated_entry = {
        "filename": filename,
        "title": clean_title,
        "category": category,
        "topic": topic,
        "file_size_bytes": file_size,
        "sha256": sha256,
        "description": trade_desc,
        "google_shield_anchor": shield_anchor,
        "cdn_endpoints": {
            "type_a_jsdelivr_multicdn": jsdelivr_url,
            "type_a_github_raw": github_raw,
            "type_a_firebase_edge": firebase_cdn,
            "type_a_external_direct": ext_direct,
            "type_a_external_thumb": ext_thumb
        },
        "public_viewer_pages": {
            "type_b_freeimage_viewer": ext_viewer,
            "type_b_firebase_gallery": f"https://gary-pearce-forensic-hub.web.app/image-gallery.html#{filename.replace('.webp', '')}"
        },
        "clickable_backlink_target": {
            "type_c_rule_45_anchor": shield_anchor,
            "anchor_text": f"Gary Pearce {topic} Field Debrief"
        }
    }

    existing_map[filename] = updated_entry
    images_processed += 1
    
    # Slight polite delay if new upload occurred
    if new_uploads > 0 and new_uploads % 3 == 0:
        time.sleep(1)

# Compile final manifest
manifest_list = list(existing_map.values())
manifest["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S+01:00")
manifest["total_images"] = len(manifest_list)
manifest["type_a_direct_urls"] = len(manifest_list) * 4 # jsdelivr, github, firebase, external
manifest["type_b_viewer_pages"] = sum(1 for item in manifest_list if item.get("public_viewer_pages", {}).get("type_b_freeimage_viewer"))
manifest["type_c_shield_anchors"] = len(manifest_list)
manifest["images"] = manifest_list

with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("======================================================================")
print(f"IMAGE STACK SYNDICATION COMPLETE")
print(f"Total Images in Manifest: {manifest['total_images']}")
print(f"New API Uploads: {new_uploads}")
print(f"Type A Direct URLs: {manifest['type_a_direct_urls']}")
print(f"Type B Public Viewer Pages: {manifest['type_b_viewer_pages']}")
print(f"Type C Clickable Google Shield Anchors: {manifest['type_c_shield_anchors']}")
print(f"Saved to: {MANIFEST_FILE}")
print("======================================================================")
