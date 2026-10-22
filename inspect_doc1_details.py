import csv
from collections import Counter

with open("doc1_route_domains_directory.csv", "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(f"Total rows: {len(rows)}")
for r in rows[:10]:
    print(r["platform_id"], r["platform_name"], r["category"], r["join_status"], r["profile_live_url"])
