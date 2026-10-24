import os
import json
import hashlib
import time
import requests

file_path = r"C:\Users\Gary\github-cctv-seo\assets\images\tv-aerial-signal-fault-finder.webp"
manifest_file = r"C:\Users\Gary\github-cctv-seo\image_stack_manifest.json"
key = "6d207e02198a847aa98d0a2a901485a5"

filename = "tv-aerial-signal-fault-finder.webp"
clean_title = "TV Aerial Signal Fault Finder Promax Spectrum Analyser Diagnosis"
shield_anchor = "https://adicommunications.co.uk/news/tv-aerial-signal-fault-finder/"
trade_desc = (
    f"{clean_title} — Professional UK installation & diagnostics by Gary Pearce, ADI Communications (07860 244 274). "
    f"25+ years hands-on field craftsmanship, £10,000,000 Public Liability insurance, "
    f"and CAI-benchmarked hardware across Yorkshire & Lancashire. "
    f"Technical Debrief & Interactive Engineering Tools: {shield_anchor}"
)

with open(file_path, "rb") as fp:
    sha256 = hashlib.sha256(fp.read()).hexdigest()

with open(file_path, "rb") as fp:
    r = requests.post(
        "https://freeimage.host/api/1/upload",
        data={
            "key": key,
            "action": "upload",
            "format": "json",
            "title": clean_title,
            "description": trade_desc
        },
        files={"source": fp},
        timeout=30
    )

print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    img = data.get("image", {})
    direct = img.get("url")
    viewer = img.get("url_viewer")
    thumb = img.get("thumb", {}).get("url")
    print("Direct:", direct)
    print("Viewer:", viewer)
    print("Thumb:", thumb)

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    img_list = manifest.get("images", [])
    entry = {
        "id": f"IMG-STACK-{len(img_list)+1:04d}",
        "filename": filename,
        "clean_title": clean_title,
        "topic": "TV Aerial Signal Diagnostics & Coaxial Fault Finding",
        "category": "Broadcast RF Engineering & Coax Diagnostics",
        "sha256": sha256,
        "size_bytes": os.path.getsize(file_path),
        "shield_buffer_anchor": shield_anchor,
        "trade_description": trade_desc,
        "surfaces": {
            "jsdelivr_cdn": f"https://cdn.jsdelivr.net/gh/gazpearce/cctv-security-hub@master/assets/images/{filename}",
            "github_raw": f"https://raw.githubusercontent.com/gazpearce/cctv-security-hub/master/assets/images/{filename}",
            "firebase_cdn": f"https://gary-pearce-forensic-hub.web.app/assets/images/{filename}",
            "freeimage_direct": direct,
            "freeimage_viewer": viewer,
            "freeimage_thumb": thumb
        },
        "external_viewer_page": viewer
    }
    img_list.append(entry)
    manifest["images"] = img_list
    manifest["total_images"] = len(img_list)
    manifest["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S+01:00")

    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("Manifest successfully updated with image stack entry!")
else:
    print("Upload error:", r.text[:300])
