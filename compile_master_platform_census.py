import json
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")

# 1. Master Multicategory Platform Catalog (550)
cat_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
cat_data = {}
if cat_path.exists():
    with open(cat_path, "r", encoding="utf-8") as f:
        cat_data = json.load(f)

platforms_550 = cat_data.get("platforms", [])

# 2. Master Profile Manifest (100 established profiles + 135 directories)
prof_path = REPO_ROOT / "master_profile_manifest.json"
prof_data = {}
if prof_path.exists():
    with open(prof_path, "r", encoding="utf-8") as f:
        prof_data = json.load(f)

est_100 = prof_data.get("established_profiles_100", [])
dir_135 = prof_data.get("directory_135_platforms", [])

# 3. Master Cloud Signup Tracker (155)
cloud_path = REPO_ROOT / "master_cloud_signup_tracker.json"
cloud_data = {}
if cloud_path.exists():
    with open(cloud_path, "r", encoding="utf-8") as f:
        cloud_data = json.load(f)
cloud_plats = cloud_data.get("platforms", [])

# 4. Social Profiles Manifest (100)
soc_path = REPO_ROOT / "social_profiles_manifest.json"
soc_data = {}
if soc_path.exists():
    with open(soc_path, "r", encoding="utf-8") as f:
        soc_data = json.load(f)
soc_plats = soc_data.get("platforms", [])

# 5. Public Backlink Ledger
ledger_path = REPO_ROOT / "public_backlink_master_ledger.json"
ledger_data = {}
if ledger_path.exists():
    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger_data = json.load(f)
ledger_entries = ledger_data.get("entries", [])

print("================================================================================")
print("                   ADI COMMUNICATIONS PLATFORM & STACK CENSUS                   ")
print("================================================================================")
print(f"Master Catalog Total Platforms : {len(platforms_550)}")
print(f"  - Total Joined / Active      : {sum(1 for p in platforms_550 if p.get('status') == 'JOINED')}")
print(f"  - Total Pending Onboarding   : {sum(1 for p in platforms_550 if p.get('status') == 'PENDING')}")
print(f"\nEstablished Verified Profiles  : {len(est_100)}")
print(f"UK Trade & Business Directories: {len(dir_135)}")
print(f"Cloud & Developer Hosts Tracker: {len(cloud_plats)} (Joined: {sum(1 for p in cloud_plats if p.get('status') == 'JOINED')}, Pending: {sum(1 for p in cloud_plats if p.get('status') == 'PENDING')})")
print(f"Social & Decentralized Tracker : {len(soc_plats)} (Joined: {sum(1 for p in soc_plats if p.get('status') == 'JOINED')}, Pending: {sum(1 for p in soc_plats if p.get('status') == 'PENDING')})")
print(f"Live Backlink Ledger Nodes     : {len(ledger_entries)}")

print("\n================================================================================")
print("                   BREAKDOWN BY CATEGORY (MASTER 550 CATALOG)                   ")
print("================================================================================")
cat_counter = Counter(p.get("category") for p in platforms_550)
for category, total in cat_counter.most_common():
    joined = sum(1 for p in platforms_550 if p.get("category") == category and p.get("status") == "JOINED")
    pending = sum(1 for p in platforms_550 if p.get("category") == category and p.get("status") == "PENDING")
    pct = (joined / total) * 100 if total > 0 else 0
    print(f"{category:<52} Total: {total:<3} | Joined: {joined:<3} | Pending: {pending:<3} | ({pct:5.1f}%)")

print("================================================================================")
