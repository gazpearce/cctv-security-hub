import os
import re
import json

news_dir = r"C:\Users\Gary\.gemini\antigravity\scratch\adi-communications-rebuild\news"
articles = sorted([d for d in os.listdir(news_dir) if os.path.isdir(os.path.join(news_dir, d))])

print(f"Upgrading {len(articles)} blog articles for 2026 Google AI Overviews & AI Search citability...")

def clean_ellipsis_title(raw_title, desc):
    # If title ends in '...', generate clean 2-4 word technical title
    t = raw_title.replace("...", "").strip()
    words = t.split()
    if len(words) > 5:
        # Generate punchy summary title
        return " ".join(words[:4])
    return t

count_speakable_added = 0
count_ellipsis_fixed = 0
count_bluf_upgraded = 0

for slug in articles:
    path = os.path.join(news_dir, slug, "index.html")
    if not os.path.exists(path):
        continue
    
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    modified = False

    # 1. Add SpeakableSpecification to JSON-LD Schema
    if "speakable" not in html and "SpeakableSpecification" not in html:
        # Match NewsArticle or TechArticle inside schema
        article_pattern = re.compile(r'("@type":\s*"(?:NewsArticle|TechArticle|BlogPosting)"[^{}]*?"headline":\s*"[^"]+")', re.DOTALL)
        if article_pattern.search(html):
            replacement = r'\1,\n      "speakable": {\n        "@type": "SpeakableSpecification",\n        "cssSelector": [".bluf-direct-answer", ".aio-technical-evidence", ".key-takeaways"]\n      }'
            html = article_pattern.sub(replacement, html, count=1)
            count_speakable_added += 1
            modified = True

    # 2. Fix Ellipsis Truncation in 3-Card Bento Grids
    card_pattern = re.compile(r'(<span class="text-base sm:text-lg font-black[^"]*">)([^<]*\.\.\.)(</span>\s*<p class="text-\[11px\][^"]*">)([^<]+)(</p>)')
    matches = card_pattern.findall(html)
    if matches:
        def replace_card(m):
            prefix = m.group(1)
            raw_title = m.group(2)
            mid = m.group(3)
            desc = m.group(4)
            suffix = m.group(5)
            # Create clean punchy title
            clean_title = clean_ellipsis_title(raw_title, desc)
            return f"{prefix}{clean_title}{mid}{desc}{suffix}"
        html = card_pattern.sub(replace_card, html)
        count_ellipsis_fixed += 1
        modified = True

    # 3. Ensure BLUF Answer Block has .bluf-direct-answer & AIO container classes
    # Check if there is an existing verdict block
    verdict_match = re.search(r'(<div class="[^"]*border-l-4[^"]*"[^>]*>\s*<div[^>]*>.*?<span>(?:The Verdict at a Glance|BLUF|Direct Answer)[^<]*</span>\s*</div>\s*<p class=")([^"]*)(">\s*)(.*?)(</p>\s*</div>)', html, re.DOTALL | re.IGNORECASE)
    if verdict_match:
        old_classes = verdict_match.group(2)
        old_text = verdict_match.group(4)
        if "bluf-direct-answer" not in old_classes:
            new_classes = f"bluf-direct-answer {old_classes}".strip()
            # Wrap in aio-answer-card container with data-nosnippet="false"
            old_block = verdict_match.group(0)
            new_block = old_block.replace(f'class="{old_classes}"', f'class="{new_classes}"')
            if 'data-nosnippet="false"' not in new_block:
                new_block = re.sub(r'<div class="([^"]*border-l-4[^"]*)"', r'<div class="\1 aio-answer-card" data-nosnippet="false"', new_block, count=1)
            html = html.replace(old_block, new_block, 1)
            count_bluf_upgraded += 1
            modified = True

    # 4. Handle hotel-hmo article specifically if missing BLUF block
    if slug == "hotel-hmo-anti-theft-tv-wall-mounting-guide" and "aio-answer-card" not in html:
        bluf_block = """<!-- 2026 Google AI Overview & Extractable Passage Block -->
<div class="p-6 sm:p-8 rounded-3xl bg-white border-l-4 border-l-[#FF5500] border border-black/10 shadow-lg mb-12 aio-answer-card" data-nosnippet="false">
  <div class="flex items-center gap-2 text-xs font-mono font-bold text-[#FF5500] uppercase tracking-wider mb-2">
    <span class="w-2 h-2 rounded-full bg-[#FF5500] animate-pulse"></span>
    <span>Field Engineering Direct Answer • Gary Pearce</span>
  </div>
  <p class="bluf-direct-answer text-base sm:text-lg text-[#1D1D1F] font-semibold leading-relaxed mb-3">
    For commercial hotels, B&Bs, and HMOs across the UK, televisions must be secured using heavy-duty anti-theft locking brackets from manufacturers like Peerless-AV, Vogel's, or Sanus. These commercial mounts feature hardened steel crossbars with integrated padlocks or tamper-resistant security screws to prevent guest theft, screen drop liabilities, and tampering with streaming devices.
  </p>
  <div class="aio-technical-evidence text-sm text-neutral-600 leading-relaxed font-normal border-t border-black/5 pt-3">
    Commercial installations require solid steel M6 SnapToggle hollow-wall anchors rated to 120kg load capacity per fixing point, tamper-resistant rear media cages for Chromecasts and Apple TVs, and concealed in-wall cabling meeting British public liability standards. Direct trade advice: Gary Pearce, Lead Engineer at ADI Communications (07860 244 274).
  </div>
</div>
<!-- Key Highlights Bento Grid -->
<div class="mb-14 key-takeaways">
  <div class="text-xs font-mono uppercase font-bold text-[#6A727B] mb-3 tracking-wider flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
    <span>Key Commercial Specifications & Asset Protection Highlights</span>
  </div>
  <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 font-mono">
    <div class="p-5 rounded-2xl bg-white border border-black/10 shadow-sm">
      <span class="text-[10px] text-[#6A727B] uppercase font-bold block">Asset Security</span>
      <span class="text-base sm:text-lg font-black text-[#1D1D1F] mt-1 block leading-snug">Hardened Steel Locking</span>
      <p class="text-[11px] text-[#475569] mt-2 font-sans leading-relaxed">Solid steel sliding bars with pin-Torx security screws prevent unauthorized screen removal.</p>
    </div>
    <div class="p-5 rounded-2xl bg-white border border-black/10 shadow-sm">
      <span class="text-[10px] text-[#6A727B] uppercase font-bold block">Public Liability</span>
      <span class="text-base sm:text-lg font-black text-[#FF5500] mt-1 block leading-snug">120kg Structural Load</span>
      <p class="text-[11px] text-[#475569] mt-2 font-sans leading-relaxed">M6 SnapToggle anchors ensure zero-sag durability even under repetitive guest stress.</p>
    </div>
    <div class="p-5 rounded-2xl bg-white border border-black/10 shadow-sm">
      <span class="text-[10px] text-[#6A727B] uppercase font-bold block">Media Protection</span>
      <span class="text-base sm:text-lg font-black text-emerald-600 mt-1 block leading-snug">Lockable Media Enclosures</span>
      <p class="text-[11px] text-[#475569] mt-2 font-sans leading-relaxed">Concealed ventilated steel cages protect streaming sticks and Chromecasts behind the screen.</p>
    </div>
  </div>
</div>
"""
        # Insert before <article class="prose-content">
        target = '<article class="prose-content">'
        if target in html:
            html = html.replace(target, f"{bluf_block}\n{target}", 1)
            count_bluf_upgraded += 1
            modified = True

    if modified:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

print(f"RESULTS:")
print(f" - Speakable Schema injected: {count_speakable_added} articles")
print(f" - Ellipsis titles fixed:    {count_ellipsis_fixed} articles")
print(f" - BLUF / AIO blocks tuned:   {count_bluf_upgraded} articles")
