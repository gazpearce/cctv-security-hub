import csv
import json
import os

CSV_PATH = r"C:\Users\Gary\github-cctv-seo\doc2_cloud_stack_100.csv"
TRACKER_PATH = r"C:\Users\Gary\github-cctv-seo\master_cloud_signup_tracker.json"

JOINED_KEYWORDS = [
    "firebase", "github pages", "gitlab pages", "surge.sh", "vercel",
    "amazon s3", "aws amplify", "google drive", "dropbox", "puter",
    "railway", "docker hub", "hugging face", "grafana"
]

def build_tracker():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    tracker = []
    joined_count = 0

    for r in rows:
        name = r.get("Platform Name", "").strip()
        name_lower = name.lower()
        
        is_joined = any(k in name_lower for k in JOINED_KEYWORDS)
        
        status = "JOINED" if is_joined else "PENDING"
        if is_joined:
            joined_count += 1
            
        entry = {
            "rank": r.get("Rank", "").strip(),
            "name": name,
            "domain": r.get("Domain", "").strip(),
            "da": int(r.get("DA", "0")) if r.get("DA", "").isdigit() else 0,
            "category": r.get("Category", "").strip(),
            "free_tier": r.get("Free Allowance / Tier", "").strip(),
            "sso_method": r.get("1-Click Join Method (SSO)", "").strip(),
            "signup_url": r.get("Official Signup / Cloud URL", "").strip(),
            "status": status,
            "active_tenant_url": ""
        }
        
        # Populate known tenants
        if "grafana" in name_lower:
            entry["active_tenant_url"] = "https://purplemyrtle460.grafana.net/"
        elif "firebase" in name_lower:
            entry["active_tenant_url"] = "https://gary-pearce-forensic-hub.web.app/"
        elif "github" in name_lower:
            entry["active_tenant_url"] = "https://gazpearce.github.io/starlink-mount-finder/"
        elif "gitlab" in name_lower:
            entry["active_tenant_url"] = "https://gitlab.com/aiagent1510/cctv-security-hub"
        elif "surge" in name_lower:
            entry["active_tenant_url"] = "https://adi-starlink-mount-finder.surge.sh/"
        elif "google drive" in name_lower:
            entry["active_tenant_url"] = "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88"
        elif "vercel" in name_lower:
            entry["active_tenant_url"] = "team_T65tTPrZdtl0Eu3WRO4Z6Si3 (cctv-blog)"
        elif "amazon" in name_lower or "aws" in name_lower:
            entry["active_tenant_url"] = "admin@adicommunications.co.uk"
            
        tracker.append(entry)

    with open(TRACKER_PATH, "w", encoding="utf-8") as f:
        json.dump({"total_platforms": len(tracker), "joined_count": joined_count, "platforms": tracker}, f, indent=2)

    print(f"Master Cloud Signup Tracker generated! Total: {len(tracker)}, Joined: {joined_count}")

if __name__ == "__main__":
    build_tracker()
