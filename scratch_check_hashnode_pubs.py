import urllib.request
import re

urls = [
    "https://cctv-and-alarms.hashnode.dev/",
    "https://aiagent1510.hashnode.dev/",
    "https://hardwire.hashnode.dev/"
]

for u in urls:
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[{resp.status}] {u}")
            html = resp.read().decode('utf-8', errors='ignore')
            m = re.findall(r'href="([^"]*crown-prosecution[^"]*)"', html)
            if m:
                print("  -> Found post link:", m)
    except Exception as e:
        print(f"[FAIL] {u}: {e}")
