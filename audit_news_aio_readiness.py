import os, re, json

news_dir = r"C:\Users\Gary\.gemini\antigravity\scratch\adi-communications-rebuild\news"
articles = sorted([d for d in os.listdir(news_dir) if os.path.isdir(os.path.join(news_dir, d))])

report = []
for a in articles:
    p = os.path.join(news_dir, a, "index.html")
    if not os.path.exists(p):
        continue
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()
    
    has_schema = "application/ld+json" in html
    has_speakable = "SpeakableSpecification" in html or "speakable" in html
    has_verdict = bool(re.search(r'(Verdict at a Glance|BLUF|Executive Verdict|Direct Answer)', html, re.I))
    has_bento = "grid-cols-1 sm:grid-cols-3" in html
    ellipsis_count = len(re.findall(r'<span class="text-base sm:text-lg font-black[^"]*">[^<]*\.\.\.</span>', html))
    word_count = len(re.findall(r'\b\w+\b', html))
    
    report.append({
        "slug": a,
        "has_schema": has_schema,
        "has_speakable": has_speakable,
        "has_verdict": has_verdict,
        "has_bento": has_bento,
        "ellipsis_count": ellipsis_count,
        "word_count": word_count
    })

print(f"Total articles audited: {len(report)}")
no_verdict = [r['slug'] for r in report if not r['has_verdict']]
no_speakable = [r['slug'] for r in report if not r['has_speakable']]
has_ellipsis = [r['slug'] for r in report if r['ellipsis_count'] > 0]

print(f"Articles without Verdict: {len(no_verdict)}")
if no_verdict:
    print(" -", no_verdict)
print(f"Articles without Speakable Schema: {len(no_speakable)}")
print(f"Articles with Ellipsis in Bento Cards: {len(has_ellipsis)}")
