import os, re, json

news_dir = r"C:\Users\Gary\.gemini\antigravity\scratch\adi-communications-rebuild\news"
articles = [d for d in os.listdir(news_dir) if os.path.isdir(os.path.join(news_dir, d))]

card_pattern = re.compile(
    r'<span class="text-base sm:text-lg font-black[^"]*">([^<]+)</span>\s*<p class="text-\[11px\][^"]*">([^<]+)</p>'
)

for a in articles[:5]:
    p = os.path.join(news_dir, a, "index.html")
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    matches = card_pattern.findall(content)
    print(f"=== {a} ({len(matches)} cards) ===")
    for title, desc in matches:
        print(f"  Title: {title.strip()}")
        print(f"  Desc:  {desc.strip()[:60]}...")
