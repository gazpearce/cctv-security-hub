import json
import csv

tracker_path = "master_cloud_signup_tracker.json"
csv_path = "doc2_cloud_stack_100.csv"

# 1. Update JSON
with open(tracker_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for p in data["platforms"]:
    if p["name"] == "Medium":
        p["status"] = "JOINED"
        p["active_tenant_url"] = "https://medium.com/@garypearce.homesecurity"
    elif p["name"] == "Notion Sites":
        p["status"] = "JOINED"
        p["active_tenant_url"] = "https://app.notion.com/p/Wireless-CCTV-Jamming-UK-Why-Battery-Cameras-Fail-3f8c143c1cca81248b75f79a5ca3b277"

joined_count = sum(1 for p in data["platforms"] if p.get("status") == "JOINED")
data["joined_count"] = joined_count

with open(tracker_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Updated JSON. Total platforms: {len(data['platforms'])}, Joined: {joined_count}")

# 2. Update CSV
rows = []
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for r in reader:
        name = r.get("Platform Name", "")
        if name == "Medium":
            r["Status"] = "JOINED"
            r["Active Tenant URL"] = "https://medium.com/@garypearce.homesecurity"
        elif name == "Notion Sites":
            r["Status"] = "JOINED"
            r["Active Tenant URL"] = "https://app.notion.com/p/Wireless-CCTV-Jamming-UK-Why-Battery-Cameras-Fail-3f8c143c1cca81248b75f79a5ca3b277"
        rows.append(r)

with open(csv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

csv_joined = sum(1 for r in rows if r.get("Status") == "JOINED")
print(f"Updated CSV. Total rows: {len(rows)}, Joined: {csv_joined}")
assert joined_count == csv_joined, f"Parity mismatch: JSON {joined_count} vs CSV {csv_joined}"
print("100% Mathematical Parity confirmed between JSON and CSV!")
