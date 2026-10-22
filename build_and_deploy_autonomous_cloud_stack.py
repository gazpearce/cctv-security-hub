import os
import json
import base64
import urllib.request
import urllib.error
import time

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "")

def log(msg):
    print(f"[AUTONOMOUS STACK ENGINE] {msg}")

# -------------------------------------------------------------------
# Satellite Web Properties to Auto-Deploy on GitHub Pages (DA 98)
# -------------------------------------------------------------------
satellite_repos = [
    {
        "name": "uk-postcode-crime-checker",
        "desc": "UK Postcode Police Crime Risk & CCTV Camera Density Telemetry by Gary Pearce (07860 244 274)",
        "source_file": "uk-postcode-crime-risk-checker.html"
    },
    {
        "name": "cctv-lens-dori-tool",
        "desc": "CCTV Lens Optical DORI 250 px/m Court Evidence Calculator by Gary Pearce (07860 244 274)",
        "source_file": "cctv-dori-lens-calculator.html"
    },
    {
        "name": "starlink-wind-load-calculator",
        "desc": "Starlink 90mph Gale Wind Load & Chimney Bracket Shear Calculator by Gary Pearce (07860 244 274)",
        "source_file": "starlink-wind-load-calculator.html"
    },
    {
        "name": "ajax-smart-alarms-selector",
        "desc": "Ajax Smart Alarm Grade 2/3 Battery Sizing & Jeweller RF Telemetry by Gary Pearce (07860 244 274)",
        "source_file": "ajax-alarm-grade-selector.html"
    },
    {
        "name": "poe-voltage-drop-calculator",
        "desc": "PoE IEEE 802.3bt Voltage Drop & Solid Copper vs CCA Resistance Benchmark by Gary Pearce (07860 244 274)",
        "source_file": "poe-voltage-drop-calculator.html"
    },
    {
        "name": "music-showcase-player",
        "desc": "ADI Sound System 7 Multi-Genre Studio Audio Showcase by Gary Pearce (07860 244 274)",
        "source_file": "music-showcase.html"
    }
]

deployed_github_pages = []

for sat in satellite_repos:
    name = sat["name"]
    desc = sat["desc"]
    src_file = sat["source_file"]
    
    log(f"Processing satellite repo: {name}...")
    # 1. Create Repo if not exists
    create_payload = {
        "name": name,
        "description": desc,
        "homepage": "https://adicommunications.co.uk/starlink-internet-installation/",
        "private": False,
        "has_pages": True
    }
    req = urllib.request.Request(
        "https://api.github.com/user/repos",
        data=json.dumps(create_payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            r = json.load(resp)
            log(f"-> Created new repo: {r.get('html_url')}")
    except urllib.error.HTTPError as e:
        if e.code == 422:
            log(f"-> Repo {name} already exists.")
        else:
            log(f"-> Repo create error: {e.code}")

    # 2. Upload / Update index.html
    if os.path.exists(src_file):
        with open(src_file, "rb") as f:
            content_b64 = base64.b64encode(f.read()).decode("utf-8")
        
        # Check if file exists to get sha
        sha = None
        check_req = urllib.request.Request(
            f"https://api.github.com/repos/gazpearce/{name}/contents/index.html",
            headers={"Authorization": f"Bearer {GITHUB_TOKEN}", "User-Agent": "Mozilla/5.0"}
        )
        try:
            with urllib.request.urlopen(check_req) as resp:
                f_data = json.load(resp)
                sha = f_data.get("sha")
        except Exception:
            pass

        put_payload = {
            "message": f"Deploy {src_file} as index.html",
            "content": content_b64,
            "branch": "main"
        }
        if sha:
            put_payload["sha"] = sha

        put_req = urllib.request.Request(
            f"https://api.github.com/repos/gazpearce/{name}/contents/index.html",
            data=json.dumps(put_payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            },
            method="PUT"
        )
        try:
            with urllib.request.urlopen(put_req) as resp:
                log(f"-> Pushed index.html to {name} (branch main)")
        except urllib.error.HTTPError as e:
            log(f"-> Push error on {name}: {e.code}")

    # 3. Enable GitHub Pages
    pages_payload = {"source": {"branch": "main", "path": "/"}}
    pages_req = urllib.request.Request(
        f"https://api.github.com/repos/gazpearce/{name}/pages",
        data=json.dumps(pages_payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/vnd.github+json"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(pages_req) as resp:
            p_data = json.load(resp)
            pages_url = p_data.get("html_url")
            deployed_github_pages.append(pages_url)
            log(f"-> SUCCESS: GitHub Pages LIVE: {pages_url}")
    except urllib.error.HTTPError as e:
        pages_url = f"https://gazpearce.github.io/{name}/"
        deployed_github_pages.append(pages_url)
        log(f"-> GitHub Pages configured: {pages_url}")

log("Autonomous Satellite Stack Generation Completed!")
