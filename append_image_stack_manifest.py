import json
import hashlib
import os
import time

manifest_file = r"C:\Users\Gary\github-cctv-seo\image_stack_manifest.json"
with open(manifest_file, "r", encoding="utf-8") as f:
    manifest = json.load(f)

filename = "tv-aerial-signal-fault-finder.webp"
file_path = rf"C:\Users\Gary\github-cctv-seo\assets\images\{filename}"

with open(file_path, "rb") as fp:
    sha256 = hashlib.sha256(fp.read()).hexdigest()

clean_title = "TV Aerial Signal Fault Finder Promax Spectrum Analyser Diagnosis"
shield_anchor = "https://adicommunications.co.uk/news/tv-aerial-signal-fault-finder/"
desc = (
    f"{clean_title} — Professional UK installation in Yorkshire & Lancashire by Gary Pearce, "
    "lead physical security and telecommunications engineer at ADI Communications (Direct Mobile: 07860 244 274). "
    "With over 25 years hands-on field craftsmanship, £10,000,000 Public Liability Insurance, "
    "and CAI-benchmarked equipment across Yorkshire, Lancashire, and Greater Manchester.\n\n"
    "Hardware & Installation Standards:\n"
    "• High-gain CAI-benchmarked digital Freeview aerial aligned to regional transmitter (Emley Moor / Winter Hill).\n"
    "• Calibrated Promax HD Ranger DVB-T2 digital spectrum analyser verification of dBµV and Modulation Error Ratio (MER).\n"
    "• Pure copper double-screened Webro WF100 coaxial downlead with exterior silicone drip loops.\n\n"
    "Top of Stack Apex Links:\n"
    "📷 High-Resolution Trade Photo Vault (Google Drive): https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88\n"
    "📺 4K Field Masterclasses (YouTube): https://www.youtube.com/@CCTV.services\n"
    "📖 Official Google Companion Guide (Blogger DA 99): https://tvandhomesecurity.blogspot.com/\n"
    f"🔗 Technical Installation Specifications: {shield_anchor}\n\n"
    "Tags: #TVAerial #Freeview #NoSignal #CoaxRepairs #PromaxMeter #GaryPearce #ADICommunications #Yorkshire"
)

tags = ["#TVAerial", "#Freeview", "#NoSignal", "#CoaxRepairs", "#PromaxMeter", "#GaryPearce", "#ADICommunications", "#Yorkshire"]

existing = [x for x in manifest["images"] if x.get("filename") == filename]
if not existing:
    entry = {
        "filename": filename,
        "title": clean_title,
        "category": "Broadcast RF Engineering & Coax Diagnostics",
        "topic": "TV Aerial Signal Diagnostics & Coaxial Fault Finding",
        "file_size_bytes": os.path.getsize(file_path),
        "sha256": sha256,
        "description": desc,
        "google_shield_anchor": shield_anchor,
        "cdn_endpoints": {
            "type_a_jsdelivr_multicdn": f"https://cdn.jsdelivr.net/gh/gazpearce/cctv-security-hub@master/assets/images/{filename}",
            "type_a_github_raw": f"https://raw.githubusercontent.com/gazpearce/cctv-security-hub/master/assets/images/{filename}",
            "type_a_firebase_edge": f"https://gary-pearce-forensic-hub.web.app/assets/images/{filename}"
        },
        "public_viewer_pages": {
            "type_b_firebase_gallery": f"https://gary-pearce-forensic-hub.web.app/image-gallery.html#{filename.replace('.webp', '')}"
        },
        "clickable_backlink_target": {
            "type_c_rule_45_anchor": shield_anchor,
            "anchor_text": "Gary Pearce TV Aerial & Signal Fault Finder Field Guide"
        },
        "about_section_markdown": desc,
        "seo_tags": tags,
        "top_of_stack_google_url": "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88",
        "companion_blogger_url": "https://tvandhomesecurity.blogspot.com/",
        "top_of_stack_youtube_url": "https://www.youtube.com/@CCTV.services",
        "money_post_url": shield_anchor
    }
    manifest["images"].append(entry)
    manifest["total_images"] = len(manifest["images"])
    manifest["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S+01:00")
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Successfully added {filename} to image_stack_manifest.json (Total: {manifest['total_images']})")
else:
    print(f"{filename} already in image_stack_manifest.json")
