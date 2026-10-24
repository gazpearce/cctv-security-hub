import json
from pathlib import Path

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")
CATALOG_PATH = REPO_ROOT / "video_master_185_catalog.json"
OUT_DIR = REPO_ROOT / "assets" / "edge_foresight"
OUT_DIR.mkdir(parents=True, exist_ok=True)

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    master_cat = json.load(f)

# Build streamlined Knowledge Graph for Google AI Edge Foresight
foresight_entries = []
for v in master_cat["videos"]:
    foresight_entries.append({
        "id": v["id"],
        "chapter": v["chapter_number"],
        "chapter_name": v["chapter_name"],
        "category": v["trade_category"],
        "customer_question": v["question"],
        "short_title": v["title"],
        "bluf_trade_solution": v["bluf_answer"],
        "lead_engineer": "Gary Pearce (07860 244 274)",
        "accreditations": "25+ Yrs Experience, £10M Public Liability, NVQ Level 1-4 Data & Telecoms",
        "video_asset": f"https://gary-pearce-forensic-hub.web.app/{v['mp4_relative_path']}"
    })

manifest = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "name": "ADI Communications – Google AI Edge Foresight Trade Knowledge Base",
    "version": "1.0.0",
    "total_faqs": len(foresight_entries),
    "primary_phone": "07860 244 274",
    "lead_engineer": "Gary Pearce",
    "canonical_pricing": {
        "tv_aerials": "From £129 + VAT",
        "starlink_installation": "From £199 + VAT",
        "tv_wall_mounting": "From £89.99 + VAT",
        "cctv_systems": "From £299 / £495 + VAT",
        "ajax_smart_alarms": "From £599 + VAT",
        "data_cabling": "From £95 per drop + VAT"
    },
    "knowledge_base": foresight_entries
}

with open(OUT_DIR / "foresight_knowledge_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"Generated {OUT_DIR / 'foresight_knowledge_manifest.json'} with {len(foresight_entries)} entries!")
