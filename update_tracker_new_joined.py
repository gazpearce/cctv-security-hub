import json

TRACKER_PATH = r"C:\Users\Gary\github-cctv-seo\master_cloud_signup_tracker.json"

with open(TRACKER_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

platforms = data.get("platforms", [])

newly_joined = {
    "Render": "https://dashboard.render.com/",
    "Zeabur": "https://zeabur.com/projects",
    "Convex": "https://dashboard.convex.dev/",
    "Supabase": "https://supabase.com/dashboard/organizations"
}

joined_count = 0
for p in platforms:
    for name, tenant in newly_joined.items():
        if name.lower() in p["name"].lower():
            p["status"] = "JOINED"
            p["active_tenant_url"] = tenant
            print(f"[UPDATED] {p['name']} -> JOINED ({tenant})")
    if p["status"] == "JOINED":
        joined_count += 1

data["joined_count"] = joined_count

with open(TRACKER_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Total Joined now: {joined_count}")
