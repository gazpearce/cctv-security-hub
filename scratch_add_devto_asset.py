import csv
import json
from datetime import datetime, timezone

now_iso = datetime.now(timezone.utc).isoformat()
now_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

devto_url = "https://dev.to/gary_pearce_2171c679bfd81/crown-prosecution-service-cps-cctv-evidence-standards-why-82-of-uk-footage-fails-bs-en-62676-4-3d12"

# 1. Update doc3_published_asset_links.csv
doc3_path = "doc3_published_asset_links.csv"
with open(doc3_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    d3_fieldnames = reader.fieldnames
    d3_rows = list(reader)

asset_id = f"DEVTO-ART-{len(d3_rows)+1:03d}"
d3_rows.append({
    "asset_id": asset_id,
    "parent_profile_id": "PROF-DEVTO-01",
    "platform_name": "DEV.to",
    "profile_live_url": "https://dev.to/gary_pearce_2171c679bfd81",
    "asset_title": "CPS CCTV Evidence Standards: Why 82% of UK Footage Fails BS EN 62676-4 DORI Identification",
    "asset_type": "Technical Guide / Whitepaper",
    "asset_public_url": devto_url,
    "top_of_stack_apex_url": "https://tvandhomesecurity.blogspot.com/",
    "shield_target_url": "https://tvandhomesecurity.blogspot.com/",
    "seo_tags": "CCTV Evidence, BS EN 62676-4 DORI, CPS Standards, PACE S.78, Gary Pearce",
    "seo_description_summary": "Field engineering whitepaper by Gary Pearce (ADI Communications, 07860 244 274) analyzing UK CCTV evidential standards under BS EN 62676-4 and CPIA 1996.",
    "dofollow_status": "Dofollow",
    "publication_date": now_date,
    "verification_status": "VERIFIED_200"
})

with open(doc3_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=d3_fieldnames)
    writer.writeheader()
    writer.writerows(d3_rows)

print(f"[DOC3] doc3_published_asset_links.csv updated. Total: {len(d3_rows)}")

# 2. Update public_backlink_master_ledger.csv
master_path = "public_backlink_master_ledger.csv"
with open(master_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    m_fieldnames = reader.fieldnames
    m_rows = list(reader)

m_rows.append({
    "timestamp": now_iso,
    "platform": "DEV.to",
    "category": "Blog & Editorial Networks",
    "asset_title": "CPS CCTV Evidence Standards: Why 82% of UK Footage Fails BS EN 62676-4 DORI Identification",
    "asset_type": "Technical Guide / Whitepaper",
    "public_live_url": devto_url,
    "top_of_stack_apex_url": "https://tvandhomesecurity.blogspot.com/",
    "shield_target_url": "https://tvandhomesecurity.blogspot.com/",
    "seo_tags": "CCTV Evidence, BS EN 62676-4 DORI, CPS Standards, PACE S.78, Gary Pearce",
    "seo_description": "Field engineering whitepaper by Gary Pearce (ADI Communications, 07860 244 274) analyzing UK CCTV evidential standards under BS EN 62676-4 and CPIA 1996.",
    "dofollow_status": "Dofollow",
    "indexing_method": "IndexNow / Sitemaps",
    "verified_http_status": "200",
    "responsible_agent": "stack-blog-agent"
})

with open(master_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=m_fieldnames)
    writer.writeheader()
    writer.writerows(m_rows)

print(f"[MASTER] public_backlink_master_ledger.csv updated. Total: {len(m_rows)}")
