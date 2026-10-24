#!/usr/bin/env python3
"""
ping_indexnow.py
================
Automated IndexNow broadcast engine for Gary Pearce / ADI Communications.
Instantly pings Microsoft Bing, Yandex, Naver, and Seznam search engines whenever
website pages, blog articles, or sitemaps are published or updated.
"""

import urllib.request
import json
import os
from pathlib import Path
from datetime import datetime

INDEXNOW_KEY = "adi7860244274cctvseoukyorkshire"
HOST = "adicommunications.co.uk"
KEY_LOCATION = f"https://{HOST}/{INDEXNOW_KEY}.txt"

INDEXNOW_ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://yandex.com/indexnow"
]

def ensure_key_file():
    key_dirs = [
        Path(r"C:\Users\Gary\.gemini\antigravity\scratch\adi-communications-rebuild"),
        Path(r"C:\Users\Gary\.gemini\antigravity\scratch\adi-communications-rebuild\dist"),
        Path(r"C:\Users\Gary\github-cctv-seo")
    ]
    for kd in key_dirs:
        kf = kd / f"{INDEXNOW_KEY}.txt"
        with open(kf, "w", encoding="utf-8") as f:
            f.write(INDEXNOW_KEY)
    print(f"[+] IndexNow key verification file written: {INDEXNOW_KEY}.txt")

def collect_urls():
    urls = [
        f"https://{HOST}/",
        f"https://{HOST}/news/",
        f"https://{HOST}/cctv-installation/",
        f"https://{HOST}/tv-wall-mounting/",
        f"https://{HOST}/starlink-installation/",
        f"https://{HOST}/wireless-intruder-alarms/",
        f"https://{HOST}/wifi-data-cabling/",
        f"https://{HOST}/tv-aerial-installation/",
        f"https://{HOST}/rss.xml",
        f"https://{HOST}/feed.xml",
        f"https://{HOST}/assets/pdfs/2026-uk-domestic-cctv-legal-compliance-checklist.pdf",
        f"https://{HOST}/assets/pdfs/hotel-hmo-anti-theft-tv-wall-mounting-specification.pdf",
        f"https://{HOST}/assets/pdfs/starlink-90mph-pennine-gale-mounting-engineering-guide.pdf"
    ]
    
    # Add all 40 news articles
    news_dir = Path(r"C:\Users\Gary\.gemini\antigravity\scratch\adi-communications-rebuild\news")
    if news_dir.exists():
        for d in news_dir.iterdir():
            if d.is_dir():
                urls.append(f"https://{HOST}/news/{d.name}/")

    return list(dict.fromkeys(urls))

def ping_indexnow():
    ensure_key_file()
    url_list = collect_urls()
    print(f"[*] Prepared {len(url_list)} canonical URLs for IndexNow submission.")

    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": url_list[:50]  # Standard IndexNow batch
    }
    
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "ADI-Communications-IndexNow-Broadcaster/2026"
    }

    for ep in INDEXNOW_ENDPOINTS:
        try:
            req = urllib.request.Request(ep, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                print(f"[+] IndexNow Submission to {ep}: HTTP {resp.status} ({resp.reason})")
        except urllib.error.HTTPError as e:
            # HTTP 200 = Success, HTTP 202 = Accepted
            print(f"[+] IndexNow Response from {ep}: HTTP {e.code} ({e.reason})")
        except Exception as e:
            print(f"[-] IndexNow failed on {ep}: {e}")

if __name__ == "__main__":
    print(f"\n{'='*65}")
    print(f"ADI COMMUNICATIONS INDEXNOW BROADCAST ENGINE")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*65}")
    ping_indexnow()
    print(f"{'='*65}\n")
