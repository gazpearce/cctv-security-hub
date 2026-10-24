import json

def main():
    with open("master_multicategory_platform_catalog.json", "r", encoding="utf-8") as f:
        cat = json.load(f)
    rss_platforms = [p for p in cat.get("platforms", []) if p.get("stack_key") == "rss"]
    print(f"Total RSS Platforms in Catalog: {len(rss_platforms)}")
    for p in rss_platforms:
        print(f"[{p.get('platform_id')}] {p.get('name')} | Domain: {p.get('domain')} | DA: {p.get('da')} | Tier: {p.get('tier')} | Status: {p.get('status')}")

if __name__ == "__main__":
    main()
