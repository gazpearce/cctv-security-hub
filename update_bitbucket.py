import json

TRACKER_PATH = r"C:\Users\Gary\github-cctv-seo\master_cloud_signup_tracker.json"

with open(TRACKER_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

for p in data["platforms"]:
    name = p["name"].lower()
    if "bitbucket" in name:
        p["status"] = "JOINED"
        p["active_tenant_url"] = "https://bitbucket.org/cctvsystem/workspace/overview/"
        print(f"[JOINED] {p['name']} -> {p['active_tenant_url']}")
    elif "deno" in name:
        p["status"] = "JOINED"
        p["active_tenant_url"] = "https://console.deno.com/aiagent1510"
        print(f"[JOINED] {p['name']} -> {p['active_tenant_url']}")

joined_count = sum(1 for p in data["platforms"] if p["status"] == "JOINED")
data["joined_count"] = joined_count

with open(TRACKER_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Grand Total Verified Joined now: {joined_count}")
