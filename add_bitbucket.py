import json
import csv

TRACKER_PATH = r"C:\Users\Gary\github-cctv-seo\master_cloud_signup_tracker.json"
CSV_PATH = r"C:\Users\Gary\github-cctv-seo\doc2_cloud_stack_100.csv"

# Add to JSON
with open(TRACKER_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

bitbucket_entry = {
    "rank": "102",
    "name": "Bitbucket Cloud (Atlassian)",
    "domain": "bitbucket.org",
    "da": 95,
    "category": "Cloud Repositories & CI/CD",
    "free_tier": "50 GB storage, 50 build mins/mo free",
    "sso_method": "Google OAuth",
    "signup_url": "https://bitbucket.org/cctvsystem/workspace/overview/",
    "status": "JOINED",
    "active_tenant_url": "https://bitbucket.org/cctvsystem/workspace/overview/"
}

data["platforms"].append(bitbucket_entry)
joined_count = sum(1 for p in data["platforms"] if p["status"] == "JOINED")
data["total_platforms"] = len(data["platforms"])
data["joined_count"] = joined_count

with open(TRACKER_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Grand Total Verified Joined now: {joined_count} (Total catalog: {data['total_platforms']})")
