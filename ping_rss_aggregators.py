#!/usr/bin/env python3
"""
ping_rss_aggregators.py
=======================
Automated RSS & WebSub ping engine for Gary Pearce / ADI Communications.
Notifies major RSS aggregators, Google WebSub hubs, and indexers whenever
new video masterclasses, blog articles, or podcast debriefs are published.
"""

import urllib.request
import urllib.parse
import xmlrpc.client
import json
import sys
from datetime import datetime

FEEDS = [
    {
        "name": "ADI Communications 185 Video Masterclasses MRSS",
        "url": "https://gary-pearce-forensic-hub.web.app/video-showcase.html",
        "feed_url": "https://gary-pearce-forensic-hub.web.app/videos-mrss.xml"
    },
    {
        "name": "ADI Communications Official Master RSS Feed (40 Articles)",
        "url": "https://adicommunications.co.uk/news/",
        "feed_url": "https://adicommunications.co.uk/rss.xml"
    },
    {
        "name": "ADI Communications Security Audio Podcast",
        "url": "https://gary-pearce-forensic-hub.web.app/podcast.xml",
        "feed_url": "https://gary-pearce-forensic-hub.web.app/podcast.xml"
    },
    {
        "name": "ADI Communications High-DA Blogger Citadel",
        "url": "https://tvandhomesecurity.blogspot.com/",
        "feed_url": "https://tvandhomesecurity.blogspot.com/feeds/posts/default"
    },
    {
        "name": "Official YouTube Channel Feed (@CCTV.services)",
        "url": "https://www.youtube.com/@CCTV.services",
        "feed_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCt7VpJGmZZ12hdg2sCgjQag"
    }
]

WEBSUB_HUBS = [
    "https://pubsubhubbub.appspot.com/",
    "https://pubsubhubbub.superfeedr.com/"
]

def ping_xmlrpc(server_url: str, title: str, site_url: str, feed_url: str) -> bool:
    try:
        server = xmlrpc.client.ServerProxy(server_url)
        # weblogUpdates.ping or weblogUpdates.extendedPing
        try:
            res = server.weblogUpdates.extendedPing(title, site_url, feed_url, feed_url)
        except Exception:
            res = server.weblogUpdates.ping(title, site_url)
        print(f"  [+] XML-RPC Ping {server_url}: {res}")
        return True
    except Exception as e:
        print(f"  [-] XML-RPC Ping failed {server_url}: {e}")
        return False

def ping_websub(hub_url: str, feed_url: str) -> bool:
    try:
        data = urllib.parse.urlencode({
            "hub.mode": "publish",
            "hub.url": feed_url
        }).encode("utf-8")
        req = urllib.request.Request(hub_url, data=data, headers={"User-Agent": "ADI-Communications-RSS-Publisher/2026"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"  [+] WebSub Hub Ping {hub_url}: HTTP {resp.status}")
            return resp.status in (200, 204)
    except Exception as e:
        print(f"  [-] WebSub Hub Ping failed {hub_url}: {e}")
        return False

def main():
    print(f"\n{'='*70}")
    print(f"ADI COMMUNICATIONS MULTI-FEED RSS & WEBSUB PING ENGINE")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")

    for f in FEEDS:
        print(f"\n[*] Broadcasting Feed: {f['name']}")
        print(f"    URL: {f['feed_url']}")

        # 1. Ping-o-Matic XML-RPC
        ping_xmlrpc("http://rpc.pingomatic.com/", f["name"], f["url"], f["feed_url"])

        # 2. Google WebSub Hubs
        for hub in WEBSUB_HUBS:
            ping_websub(hub, f["feed_url"])

    print(f"\n{'='*70}")
    print(f"[COMPLETE] All 5 primary feeds broadcast across global aggregators & hubs!")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
