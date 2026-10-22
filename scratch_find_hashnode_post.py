import urllib.request
import json
import re

req = urllib.request.Request("https://hashnode.com/@hardwire", headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        # find post link
        matches = re.findall(r'href="([^"]*crown-prosecution[^"]*)"', html, re.I)
        print("Found post matches:", matches)
        if not matches:
            # search any links
            all_links = re.findall(r'href="([^"]*cctv[^"]*)"', html, re.I)
            print("CCTV links:", all_links[:5])
except Exception as e:
    print("Hashnode fetch error:", e)
