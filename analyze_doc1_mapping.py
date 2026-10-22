import csv
from collections import Counter

with open("doc1_route_domains_directory.csv", "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(f"Total rows in doc1: {len(rows)}")
for c in set(r["category"] for r in rows):
    sub = [r for r in rows if r["category"] == c]
    joined = [r for r in sub if r["join_status"] == "JOINED"]
    pending = [r for r in sub if r["join_status"] != "JOINED"]
    print(f"Category: '{c}' -> Total: {len(sub)} (Joined: {len(joined)}, Pending: {len(pending)})")
    # Show first 3 platform names
    sample = [r["platform_name"] for r in sub[:5]]
    print(f"   Sample: {sample}")
