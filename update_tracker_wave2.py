import json

TRACKER_PATH = r"C:\Users\Gary\github-cctv-seo\master_cloud_signup_tracker.json"

with open(TRACKER_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

platforms = data.get("platforms", [])

wave2_updates = {
    "Neon": "https://console.neon.tech/app/org-weathered-wave-08047806/welcome",
    "Hasura": "https://cloud.hasura.io/",
    "Appwrite": "https://appwrite.io/organizations/6ada17c000338d85018f",
    "Fly.io": "https://fly.io/app/sign-in"
}

joined_count = 0
for p in platforms:
    for name, tenant in wave2_updates.items():
        if name.lower() in p["name"].lower():
            p["status"] = "JOINED"
            p["active_tenant_url"] = tenant
            print(f"[UPDATED WAVE 2] {p['name']} -> JOINED ({tenant})")
    if p["status"] == "JOINED":
        joined_count += 1

data["joined_count"] = joined_count

with open(TRACKER_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Grand Total Verified Joined now: {joined_count}")
