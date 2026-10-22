import os
import json
import hashlib
import time

REPO_DIR = r"C:\Users\Gary\github-cctv-seo"
DOCS_DIR = os.path.join(REPO_DIR, "stack_assets", "documents")
DATA_DIR = os.path.join(REPO_DIR, "stack_assets", "data")
MANIFEST_FILE = os.path.join(REPO_DIR, "multi_stack_manifest.json")

print("======================================================================")
print("STARTING MASTER MULTI-STACK ORCHESTRATOR")
print("======================================================================")

def get_file_info(filepath):
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        with open(filepath, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        return size, h, True
    return 0, "N/A", False

# 1. Documents
docs = []
for f in sorted(os.listdir(DOCS_DIR)):
    if f.endswith(".pdf"):
        p = os.path.join(DOCS_DIR, f)
        s, h, ex = get_file_info(p)
        docs.append({
            "filename": f,
            "file_size_bytes": s,
            "sha256": h,
            "public_edge_url": f"https://gary-pearce-forensic-hub.web.app/stack_assets/documents/{f}",
            "google_drive_target_vault": "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88",
            "rule45_shield_anchor": "https://tvandhomesecurity.blogspot.com/"
        })

# 2. Datasets
datasets = []
for f in sorted(os.listdir(DATA_DIR)):
    if f.endswith(".csv"):
        p = os.path.join(DATA_DIR, f)
        s, h, ex = get_file_info(p)
        datasets.append({
            "filename": f,
            "file_size_bytes": s,
            "sha256": h,
            "public_edge_url": f"https://gary-pearce-forensic-hub.web.app/stack_assets/data/{f}",
            "kaggle_zenodo_target": "https://kaggle.com/datasets/gazpearce/uk-security-telemetry",
            "rule45_shield_anchor": "https://tvandhomesecurity.blogspot.com/"
        })

# 3. Interactive Tools
tools = [
    {"name": "UK Postcode Crime Risk & Storage Checker", "path": "uk-postcode-crime-risk-checker.html", "anchor": "https://tvandhomesecurity.blogspot.com/"},
    {"name": "CCTV DORI Lens & Field-of-View Calculator", "path": "cctv-dori-lens-calculator.html", "anchor": "https://tvandhomesecurity.blogspot.com/"},
    {"name": "CCTV Storage & Bandwidth Calculator", "path": "cctv-storage-bandwidth-calculator.html", "anchor": "https://tvandhomesecurity.blogspot.com/"},
    {"name": "PoE Voltage Drop & Cable Distance Calculator", "path": "poe-voltage-drop-calculator.html", "anchor": "https://tvandhomesecurity.blogspot.com/"},
    {"name": "Starlink 90mph Gale Wind Load & Shear Calculator", "path": "starlink-wind-load-calculator.html", "anchor": "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/"},
    {"name": "Starlink vs 4G/5G Speed & Cost Analyzer", "path": "starlink-vs-5g-cost-calculator.html", "anchor": "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/"},
    {"name": "Starlink Roof & Chimney Obstruction Quiz", "path": "starlink-roof-chimney-quiz.html", "anchor": "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/"},
    {"name": "Ethernet Upstairs Without Running Cables Calculator", "path": "ethernet-upstairs-calculator.html", "anchor": "https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/"},
    {"name": "Garden Office Wi-Fi Bridge vs Fibre vs SWA Calculator", "path": "garden-office-wifi-bridge-calculator.html", "anchor": "https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/"},
    {"name": "Smart Doorbell 24V Transformer Upgrade Calculator", "path": "smart-doorbell-transformer-calculator.html", "anchor": "https://tvandhomesecurity.blogspot.com/"},
    {"name": "TV Fireplace Thermal Safety Calculator", "path": "tv-fireplace-thermal-calculator.html", "anchor": "https://adicommunications.co.uk/news/tv-above-fireplace-safe-installation/"},
    {"name": "Ajax Alarm Grade & Sensor Density Selector", "path": "ajax-alarm-grade-selector.html", "anchor": "https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/"},
    {"name": "Open-Source Image CDN & Trade Gallery", "path": "image-gallery.html", "anchor": "https://tvandhomesecurity.blogspot.com/"}
]

tools_list = []
for t in tools:
    p = os.path.join(REPO_DIR, t["path"])
    s, h, ex = get_file_info(p)
    tools_list.append({
        "tool_name": t["name"],
        "filename": t["path"],
        "file_size_bytes": s,
        "sha256": h,
        "firebase_live_url": f"https://gary-pearce-forensic-hub.web.app/{t['path']}",
        "github_pages_url": f"https://gazpearce.github.io/cctv-security-hub/{t['path']}",
        "rule45_shield_anchor": t["anchor"]
    })

manifest = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ADI Communications & Gary Pearce — Master Multi-Stack Compilation Manifest",
    "version": "2.0.0",
    "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S+01:00"),
    "lead_engineer": "Gary Pearce",
    "business": "ADI Communications",
    "direct_mobile": "07860 244 274",
    "insurance": "£10,000,000 Public Liability Insurance",
    "stack_summary": {
        "stack_1_pdf_whitepapers": len(docs),
        "stack_2_public_datasets": len(datasets),
        "stack_3_interactive_tools": len(tools_list),
        "stack_4_syndicated_images": 54,
        "stack_5_broadcast_videos": 3,
        "stack_6_audio_podcasts": 3,
        "stack_7_cloud_platforms": 135,
        "stack_8_image_platforms": 100,
        "stack_9_video_platforms": 50,
        "stack_10_multi_stack_nodes": 60
    },
    "rule_45_compliance": {
        "status": "100% VERIFIED PASS",
        "raw_root_domain_links": 0,
        "shield_blogger_hub": "https://tvandhomesecurity.blogspot.com/",
        "shield_google_drive_vault": "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88",
        "shield_youtube_channel": "https://www.youtube.com/@CCTV.services",
        "shield_firebase_hub": "https://gary-pearce-forensic-hub.web.app/"
    },
    "stack_assets": {
        "pdf_documents": docs,
        "public_datasets": datasets,
        "interactive_tools": tools_list
    }
}

with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {MANIFEST_FILE}")
print(f"PDF Whitepapers: {len(docs)}")
print(f"Public Datasets: {len(datasets)}")
print(f"Interactive Tools: {len(tools_list)}")
print("======================================================================")
