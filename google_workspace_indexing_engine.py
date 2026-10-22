import os
import sys
import time
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

REPO_ROOT = r"C:\Users\Gary\github-cctv-seo"
SITEMAP_PATH = os.path.join(REPO_ROOT, "sitemap.xml")
SPIDER_SITEMAP_PATH = os.path.join(REPO_ROOT, "sitemap-spider.xml")

SITEMAP_PUBLIC_URLS = [
    "https://gary-pearce-forensic-hub.web.app/sitemap.xml",
    "https://gary-pearce-forensic-hub.web.app/sitemap-spider.xml",
    "https://gary-pearce-forensic-hub.web.app/podcast.xml",
    "https://tvandhomesecurity.blogspot.com/feeds/posts/default"
]

def load_all_urls():
    urls = []
    if os.path.exists(SITEMAP_PATH):
        try:
            tree = ET.parse(SITEMAP_PATH)
            root = tree.getroot()
            for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                if elem.text:
                    urls.append(elem.text.strip())
        except Exception as e:
            print(f"[INDEX-ENGINE] Error reading sitemap: {e}")
    return sorted(list(set(urls)))

def ping_search_engines(sitemap_url):
    results = {}
    
    # 1. Google Sitemap Ping
    google_ping = f"https://www.google.com/ping?sitemap={urllib.parse.quote(sitemap_url)}"
    try:
        req = urllib.request.Request(google_ping, headers={"User-Agent": "ADI-Communications-Indexer/2026.1"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            results["Google"] = resp.status
            print(f"  -> Google Ping: HTTP {resp.status} for {sitemap_url}")
    except Exception as e:
        results["Google"] = str(e)
        print(f"  -> Google Ping note: {e}")

def submit_indexnow(urls):
    """Submits URLs directly to IndexNow protocol (Bing, Yandex, Seznam, Naver)."""
    api_url = "https://api.indexnow.org/indexnow"
    key = "6a2b8e3d4c1f5a9b8e2c4d1a5f9b8e2c"
    host = "gary-pearce-forensic-hub.web.app"
    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": urls[:100]
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(api_url, data=data, headers={"Content-Type": "application/json; charset=utf-8"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            print(f"  -> IndexNow Protocol Broadcast: HTTP {resp.status} (Submitted {len(urls[:100])} URLs)")
            return True
    except Exception as e:
        print(f"  -> IndexNow note: {e}")
        return False


def ping_pingomatic(blog_title, blog_url, rss_url):
    """Pings Ping-o-Matic XML-RPC gateway to broadcast to Google Blog Search, Weblogs, Feedburner."""
    rpc_url = "http://rpc.pingomatic.com/"
    xml_data = f"""<?xml version="1.0"?>
    <methodCall>
      <methodName>weblogUpdates.extendedPing</methodName>
      <params>
        <param><value>{blog_title}</value></param>
        <param><value>{blog_url}</value></param>
        <param><value>{rss_url}</value></param>
      </params>
    </methodCall>"""
    try:
        req = urllib.request.Request(
            rpc_url, 
            data=xml_data.encode("utf-8"), 
            headers={"Content-Type": "text/xml", "User-Agent": "ADI-Communications-Ping/2026"}
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            is_ok = "flerror" in body and "<boolean>0</boolean>" in body
            print(f"  -> Ping-o-Matic XML-RPC Broadcast: {'SUCCESS (Flerror 0)' if is_ok else 'SENT'}")
            return True
    except Exception as e:
        print(f"  -> Ping-o-Matic note: {e}")
        return False

def check_cdp_search_console():
    """Checks if Google Search Console or Google Workspace tab is active on CDP port 9223."""
    cdp_url = "http://127.0.0.1:9223/json"
    try:
        req = urllib.request.Request(cdp_url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            tabs = json.loads(resp.read().decode("utf-8"))
            gsc_tabs = [t for t in tabs if "search.google.com/search-console" in t.get("url", "")]
            if gsc_tabs:
                print(f"[INDEX-ENGINE] Active Google Search Console session detected ({len(gsc_tabs)} tabs).")
                return True
            else:
                print("[INDEX-ENGINE] CDP active (port 9223). GSC not open in foreground, relying on Sitemap pings.")
                return False
    except Exception:
        return False

def run_indexing_cycle():
    print(f"\n==================================================")
    print(f"  ADI Communications Google Workspace Indexing Engine")
    print(f"  Director: Gary Pearce · 07860 244 274 · West Yorkshire")
    print(f"  Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"==================================================")
    
    urls = load_all_urls()
    print(f"[INDEX-ENGINE] Total URLs indexed for Googlebot spidering: {len(urls)}")
    
    # 1. Ping Sitemaps
    print("\n[1/4] Pinging Search Engines with Sitemaps & Spider Crawl Index:")
    for sm in SITEMAP_PUBLIC_URLS:
        ping_search_engines(sm)
        
    # 2. IndexNow Protocol
    print("\n[2/4] Broadcasting to IndexNow Protocol (Bing, Yandex, Seznam, Naver):")
    submit_indexnow(urls)

    # 3. Ping-o-Matic RPC
    print("\n[3/4] Broadcasting via Ping-o-Matic XML-RPC Gateway:")
    ping_pingomatic(
        "ADI Communications Technical Field Debrief",
        "https://gary-pearce-forensic-hub.web.app/spider_crawler_index.html",
        "https://tvandhomesecurity.blogspot.com/feeds/posts/default"
    )
    
    # 4. CDP Verification
    print("\n[4/4] Checking Google Workspace & CDP Session:")
    check_cdp_search_console()
    
    # Write indexing log
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_urls_indexed": len(urls),
        "sitemaps_pinged": SITEMAP_PUBLIC_URLS,
        "status": "COMPLETED_HTTP_PINGS_ACTIVE"
    }
    log_path = os.path.join(REPO_ROOT, "workspace_indexing_audit.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
        
    print(f"\n[INDEX-ENGINE] Cycle Complete. Log saved to workspace_indexing_audit.log\n")

if __name__ == "__main__":
    run_indexing_cycle()
