import json, re

slugs = ['8k-cctv-camera-price-guide-uk', 'how-to-save-cctv-footage-for-police-uk', 'is-hikvision-banned-uk-homeowners', 'uk-home-security-faq-guide', 'why-battery-wireless-cctv-fails-uk']

for s in slugs:
    p = f"C:\\Users\\Gary\\.gemini\\antigravity\\scratch\\adi-communications-rebuild\\news\\{s}\\index.html"
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()

    blocks = re.findall(r'<script type=["\']application/ld\+json["\']>(.*?)</script>', html, re.DOTALL)
    print(f"=== {s}: {len(blocks)} ld+json blocks ===")
    
    # We will find the JSON-LD script block that has Article/TechArticle/NewsArticle/BlogPosting or inject speakable into the main article object
    modified = False
    new_html = html

    def inject_speakable_json(m):
        raw_json = m.group(1).strip()
        try:
            data = json.loads(raw_json)
            # Find article object
            target = None
            if isinstance(data, dict):
                if "@graph" in data:
                    for item in data["@graph"]:
                        if any(t in str(item.get("@type")) for t in ["Article", "TechArticle", "NewsArticle", "BlogPosting"]):
                            target = item
                            break
                elif any(t in str(data.get("@type")) for t in ["Article", "TechArticle", "NewsArticle", "BlogPosting"]):
                    target = data

            if target and "speakable" not in target:
                target["speakable"] = {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [".bluf-direct-answer", ".aio-technical-evidence", ".key-takeaways"]
                }
                return f'<script type="application/ld+json">\n{json.dumps(data, indent=2)}\n</script>'
        except Exception as e:
            print("Error parsing json:", e)
        return m.group(0)

    new_html = re.sub(r'<script type=["\']application/ld\+json["\']>(.*?)</script>', inject_speakable_json, new_html, flags=re.DOTALL)
    if new_html != html:
        with open(p, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"Injected speakable into {s}!")
    else:
        print(f"Could not inject into {s}, investigating...")
