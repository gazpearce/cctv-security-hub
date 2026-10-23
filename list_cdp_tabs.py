import urllib.request
import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    with urllib.request.urlopen("http://localhost:9223/json/list", timeout=5) as resp:
        data = json.loads(resp.read().decode())
    pages = [d for d in data if d.get("type") == "page"]
    print(f"Total open page tabs: {len(pages)}")
    for p in pages:
        pid = p.get("id", "")
        title = (p.get("title") or "")[:45]
        url = (p.get("url") or "")[:90]
        print(f"{pid} | {title:<45} | {url}")
except Exception as e:
    print(f"Error: {e}")
