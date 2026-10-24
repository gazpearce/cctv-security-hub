import os
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")
EV_DIR = REPO_ROOT / "assets" / "evidence" / "social_profiles"

# Load catalog
cat_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
with open(cat_path, "r", encoding="utf-8") as f:
    cat = json.load(f)

# Load social profiles manifest
soc_path = REPO_ROOT / "social_profiles_manifest.json"
with open(soc_path, "r", encoding="utf-8") as f:
    soc = json.load(f)

evidence_folders = {}
for d in os.listdir(EV_DIR):
    sub = EV_DIR / d
    if sub.is_dir():
        pngs = sorted([f.name for f in sub.glob("*.png")])
        if pngs:
            evidence_folders[d.lower()] = [str(sub / p) for p in pngs]

print(f"Total evidence folders found: {len(evidence_folders)}")

# Match and upgrade catalog
cat_platforms = cat.get("platforms", [])
newly_joined_cat = 0

for p in cat_platforms:
    if p.get("status") == "PENDING":
        pname_clean = re.sub(r'[^a-zA-Z0-9]', '', p.get("name", "").lower())
        pdomain_clean = re.sub(r'[^a-zA-Z0-9]', '', p.get("domain", "").lower())
        pid_clean = re.sub(r'[^a-zA-Z0-9]', '', p.get("platform_id", "").lower())

        matched_folder = None
        for fld in evidence_folders:
            fld_clean = re.sub(r'[^a-zA-Z0-9]', '', fld)
            # Avoid generic matches
            if len(pname_clean) > 3 and (pname_clean in fld_clean or fld_clean.endswith(pname_clean)):
                matched_folder = fld
                break
            elif len(pdomain_clean) > 4 and pdomain_clean in fld_clean:
                matched_folder = fld
                break
            elif pid_clean and pid_clean in fld_clean:
                matched_folder = fld
                break

        if matched_folder and "microblog" not in pname_clean: # safety
            p["status"] = "JOINED"
            p["verified_evidence"] = evidence_folders[matched_folder]
            p["last_verified"] = datetime.now(timezone.utc).isoformat()
            newly_joined_cat += 1

# Match and upgrade social_profiles_manifest.json
soc_platforms = soc.get("platforms", [])
newly_joined_soc = 0

for p in soc_platforms:
    if p.get("status") != "JOINED":
        pname_clean = re.sub(r'[^a-zA-Z0-9]', '', p.get("name", "").lower())
        pdomain_clean = re.sub(r'[^a-zA-Z0-9]', '', p.get("domain", "").lower())
        pid_clean = re.sub(r'[^a-zA-Z0-9]', '', (p.get("id") or "").lower())

        matched_folder = None
        for fld in evidence_folders:
            fld_clean = re.sub(r'[^a-zA-Z0-9]', '', fld)
            if len(pname_clean) > 3 and (pname_clean in fld_clean or fld_clean.endswith(pname_clean)):
                matched_folder = fld
                break
            elif len(pdomain_clean) > 4 and pdomain_clean in fld_clean:
                matched_folder = fld
                break
            elif pid_clean and pid_clean in fld_clean:
                matched_folder = fld
                break

        if matched_folder:
            p["status"] = "JOINED"
            p["checkpoints"] = evidence_folders[matched_folder]
            p["last_verified"] = datetime.now(timezone.utc).isoformat()
            newly_joined_soc += 1

# Recompute totals for catalog
total_joined_cat = sum(1 for p in cat_platforms if p.get("status") == "JOINED")
total_pending_cat = sum(1 for p in cat_platforms if p.get("status") == "PENDING")
cat["total_joined"] = total_joined_cat
cat["total_pending"] = total_pending_cat
cat["last_updated"] = datetime.now(timezone.utc).isoformat()

with open(cat_path, "w", encoding="utf-8") as f:
    json.dump(cat, f, indent=2)

# Recompute totals for social manifest
total_joined_soc = sum(1 for p in soc_platforms if p.get("status") == "JOINED")
total_pending_soc = sum(1 for p in soc_platforms if p.get("status") != "JOINED")
soc["joined_count"] = total_joined_soc
soc["queued_count"] = total_pending_soc
soc["last_updated"] = datetime.now(timezone.utc).isoformat()

with open(soc_path, "w", encoding="utf-8") as f:
    json.dump(soc, f, indent=2)

print("SYNC COMPLETED:")
print(f" - Catalog: {newly_joined_cat} newly verified joined -> Total Joined: {total_joined_cat}, Total Pending: {total_pending_cat}")
print(f" - Social Manifest: {newly_joined_soc} newly verified joined -> Total Joined: {total_joined_soc}, Total Queued: {total_pending_soc}")
