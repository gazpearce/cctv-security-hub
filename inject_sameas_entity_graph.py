#!/usr/bin/env python3
"""
inject_sameas_entity_graph.py
=============================
Upgrades the root JSON-LD schema on adicommunications.co.uk by injecting the
top 25+ verified high-DA entity profiles, social nodes, RSS hubs, and cloud citadels
into the Organization / LocalBusiness sameAs array.
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

TARGET_FILES = [
    Path(r"C:\Users\Gary\.gemini\antigravity\scratch\adi-communications-rebuild\index.html"),
    Path(r"C:\Users\Gary\.gemini\antigravity\scratch\adi-communications-rebuild\dist\index.html")
]

SAME_AS_NODES = [
    "https://www.google.com/search?kgmid=/g/11c545gdm0&q=ADI+Communications+LTD",
    "https://www.youtube.com/@CCTV.services",
    "https://tvandhomesecurity.blogspot.com/",
    "https://www.pinterest.com/adicommunications/",
    "https://www.instagram.com/cctv.service.uk/",
    "https://www.threads.net/@cctv.service.uk",
    "https://github.com/gazpearce",
    "https://huggingface.co/gazpearce",
    "https://feeds.feedburner.com/ADICommunicationsSecurityDebrief",
    "https://gary-pearce-forensic-hub.web.app/",
    "https://feedly.com/i/subscription/feed/https://tvandhomesecurity.blogspot.com/feeds/posts/default",
    "https://www.inoreader.com/feed/https%3A%2F%2Ftvandhomesecurity.blogspot.com%2Ffeeds%2Fposts%2Fdefault",
    "https://archive.org/details/@gary_pearce",
    "https://gravatar.com/gazpearce",
    "https://hackernoon.com/u/garypearce",
    "https://adicommunications.wordpress.com/",
    "https://adicommunications.tumblr.com/",
    "https://soundcloud.com/adi-communications",
    "https://adicommunications.bandcamp.com/",
    "https://www.flickr.com/photos/adi_communications/",
    "https://podcasters.spotify.com/pod/show/adi-communications",
    "https://podcastaddict.com/podcast/adi-communications-security-debrief",
    "https://www.podchaser.com/podcasts/adi-communications-technical-debrief",
    "https://www.listennotes.com/c/adi-communications-technical-audio-debrief/"
]

def update_html_file(file_path: Path):
    if not file_path.exists():
        print(f"[-] File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    schema_tags = soup.find_all("script", type="application/ld+json")
    
    updated = False
    for tag in schema_tags:
        try:
            data = json.loads(tag.string)
            if "@graph" in data:
                for item in data["@graph"]:
                    # Check if organization or local business
                    item_types = item.get("@type", [])
                    if isinstance(item_types, str):
                        item_types = [item_types]
                    if any(t in ["Organization", "LocalBusiness", "SecurityService", "HomeAndConstructionBusiness"] for t in item_types):
                        existing = item.get("sameAs", [])
                        if isinstance(existing, str):
                            existing = [existing]
                        # Merge without duplicates, preserving order
                        merged = list(dict.fromkeys(existing + SAME_AS_NODES))
                        item["sameAs"] = merged
                        updated = True
                if updated:
                    tag.string = json.dumps(data, indent=2, ensure_ascii=False)
                    break
        except Exception as e:
            print(f"[-] Schema parse error in {file_path}: {e}")

    if updated:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"[+] Successfully injected {len(SAME_AS_NODES)} sameAs entity nodes into {file_path}")
        return True
    else:
        print(f"[-] No matching Organization / LocalBusiness schema found in {file_path}")
        return False

def main():
    print("=" * 60)
    print("INJECTING UNIVERSAL ENTITY GRAPH NODES (sameAs)")
    print("=" * 60)
    for target in TARGET_FILES:
        update_html_file(target)

if __name__ == "__main__":
    main()
