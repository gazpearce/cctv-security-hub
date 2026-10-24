import urllib.request
import ssl
import json
import re

endpoints = [
    ("Main Production Domain", "https://adicommunications.co.uk/"),
    ("Core CCTV Service", "https://adicommunications.co.uk/cctv-installation/"),
    ("Core TV Aerial Service", "https://adicommunications.co.uk/tv-aerial-installation/"),
    ("Core TV Wall Mounting", "https://adicommunications.co.uk/tv-wall-mounting/"),
    ("Core Ajax Alarms Service", "https://adicommunications.co.uk/ajax-alarm/"),
    ("Core Starlink Service", "https://adicommunications.co.uk/starlink-internet-installation/"),
    ("Production Sitemap", "https://adicommunications.co.uk/sitemap.xml"),
    ("Production Robots.txt", "https://adicommunications.co.uk/robots.txt"),
    ("Forensic Hub Calculator Directory", "https://gary-pearce-forensic-hub.web.app/tools/"),
    ("DORI Lens Calculator", "https://gary-pearce-forensic-hub.web.app/tools/cctv-dori-lens-calculator.html"),
    ("Wind Load Calculator", "https://gary-pearce-forensic-hub.web.app/tools/starlink-wind-load-calculator.html"),
    ("PoE Budget Calculator", "https://gary-pearce-forensic-hub.web.app/tools/poe-switch-budget-calculator.html"),
    ("Forensic Whitepaper PDF", "https://gary-pearce-forensic-hub.web.app/assets/research/cctv-dori-optical-engineering-whitepaper.pdf"),
    ("Starlink Wind Whitepaper PDF", "https://gary-pearce-forensic-hub.web.app/assets/research/starlink-wind-load-fixing-whitepaper.pdf"),
    ("Staged Firebase Domain (Bandwidth Restricted)", "https://adi-communications-uk.web.app/")
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("================================================================================")
print("LIVE PRODUCTION ENDPOINT DIAGNOSTIC REPORT")
print("================================================================================\n")

for label, url in endpoints:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            status = resp.status
            content_type = resp.headers.get('Content-Type', 'unknown')
            server = resp.headers.get('Server', 'unknown')
            body = resp.read(2048).decode('utf-8', errors='ignore')
            title_match = re.search(r'<title>(.*?)</title>', body, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else '(No title tag)'
            if 'pdf' in content_type:
                title = '(Binary PDF Document)'
            elif 'xml' in content_type:
                title = '(XML Sitemap)'
            elif 'text/plain' in content_type:
                title = '(Robots.txt)'
            print(f"[{status} OK] {label}")
            print(f"  URL: {url}")
            print(f"  Type: {content_type} | Server: {server}")
            print(f"  Title / Content: {title[:75]}\n")
    except urllib.error.HTTPError as e:
        print(f"[{e.code} {e.reason}] {label}")
        print(f"  URL: {url}")
        print(f"  Details: HTTP error encountered\n")
    except Exception as e:
        print(f"[ERR] {label}")
        print(f"  URL: {url}")
        print(f"  Details: {str(e)[:80]}\n")
