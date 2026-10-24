import urllib.request
import json

def main():
    try:
        req = urllib.request.Request("http://127.0.0.1:9223/json", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            tabs = json.loads(resp.read().decode("utf-8"))
            print(f"Total CDP targets: {len(tabs)}")
            for t in tabs:
                if t.get("type") == "page":
                    title = t.get('title', '').encode('ascii', 'replace').decode('ascii')
                    url = t.get('url', '')
                    print(f"[{t.get('id')[:8]}] {title[:40]} -> {url[:80]}")
    except Exception as e:
        print(f"CDP connection error: {e}")

if __name__ == "__main__":
    main()
