import os
import glob
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")
VIDEOS_DIR = REPO_ROOT / "assets" / "videos"
CAT_50_PATH = REPO_ROOT / "video_stack_50_catalog.json"
FAQ_CAT_PATH = REPO_ROOT / "faq_multimedia_metadata_catalog.json"
OUT_CATALOG = REPO_ROOT / "video_master_88_catalog.json"

# Load source catalogs
with open(CAT_50_PATH, "r", encoding="utf-8") as f:
    cat50 = json.load(f).get("videos", [])

with open(FAQ_CAT_PATH, "r", encoding="utf-8") as f:
    faq_data = json.load(f)
    faq_items = faq_data.get("faqs", [])

# Build lookups by slug
lookup_50 = {v["slug"]: v for v in cat50}
lookup_faq = {v["slug"]: v for v in faq_items}

# Custom priority metadata for the 4 newly rendered ones
custom_meta = {
    "how-many-cctv-cameras-does-your-house-actually-need": {
        "title": "How Many CCTV Cameras Does Your House Actually Need?",
        "question": "How many CCTV cameras does an average UK home actually need to eliminate blind spots?",
        "category": "CCTV Engineering",
        "description": "Gary Pearce breaks down camera positioning, blind spots, entry points, and realistic coverage for UK detached and semi-detached properties under BS EN 62676-4 standards.",
        "script_narration": "How many CCTV cameras does your house actually need? The most common mistake UK homeowners make is installing eight cheap wide-angle cameras and still having massive blind spots. In this video, I break down realistic coverage for a typical UK semi-detached and detached house. For 90 percent of properties, three to four strategically placed 4K turret cameras give complete 360-degree perimeter defence without wasting storage. You need one covering the driveway and vehicle approach, one covering the front doorway at eye-level identification height, one covering the rear patio or bifold doors, and one down the side access passage. I'm Gary Pearce, Lead Engineer at ADI Communications, with 25 years hands-on field experience. Call me directly on 07860 244 274 for a bespoke site survey.",
        "timestamps": [
            "00:00 - The common 8-camera mistake and real blind spots",
            "00:10 - Driveway, vehicle approach, and front door positioning",
            "00:22 - Rear patio, bifold doors, and side passage security",
            "00:34 - Gary Pearce ADI Communications direct mobile 07860 244 274"
        ]
    },
    "hikvision-vs-dahua-vs-tapo-which-cctv-should-you-buy": {
        "title": "Hikvision vs Dahua vs Tapo: Which CCTV Should You Buy?",
        "question": "Hikvision vs Dahua vs Tapo: which security camera system is right for your home and budget?",
        "category": "CCTV Engineering",
        "description": "Direct commercial comparison of commercial hardwired PoE systems (Hikvision AcuSense & Dahua WizSense) against consumer Wi-Fi cameras (TP-Link Tapo) covering subscriptions, police evidence, and reliability.",
        "script_narration": "Hikvision vs Dahua vs Tapo: which CCTV system should you actually buy? If you want an inexpensive quick fix for monitoring a pet indoors, TP-Link Tapo Wi-Fi cameras are great value under fifty pounds. But if you need reliable perimeter security for your home or business, wireless cameras face serious Wi-Fi dropouts and jamming risks. Hikvision ColorVu and Dahua WizSense are commercial-grade hardwired Power-over-Ethernet systems. They record 24/7 directly to a local hard drive with zero monthly subscription fees, and deliver court-admissible facial identification at night under UK DORI standards. I'm Gary Pearce, Lead Engineer at ADI Communications. With 25 years trade experience, call me on 07860 244 274 for certified trade advice.",
        "timestamps": [
            "00:00 - Consumer Wi-Fi cameras vs commercial PoE systems",
            "00:12 - Why Wi-Fi cameras struggle with dropouts and latency",
            "00:24 - Hikvision ColorVu & Dahua WizSense 24/7 local recording",
            "00:36 - Gary Pearce ADI Communications direct mobile 07860 244 274"
        ]
    },
    "tapo-cameras-what-can-you-do-without-a-subscription": {
        "title": "Tapo Cameras: What Can You Do Without a Subscription?",
        "question": "Can you use TP-Link Tapo cameras without paying a monthly cloud subscription fee?",
        "category": "Smart Security & Doorbells",
        "description": "Full breakdown of Tapo camera features available using local MicroSD card storage versus Tapo Care cloud subscriptions, including AI detection and RTSP stream integration.",
        "script_narration": "Tapo cameras: what can you actually do without paying a monthly subscription? The good news is that TP-Link Tapo cameras operate very well without a subscription if you insert a high-end MicroSD card. You get live remote viewing in the Tapo app, instant motion notifications, two-way audio, and local event playback completely free. You also retain basic AI detection for humans and vehicles on most newer models. What you lose without the subscription is off-site cloud backup if someone steals the camera, rich photo notifications on your lock screen, and unlimited 30-day cloud video history. I'm Gary Pearce at ADI Communications. For hardwired NVR installations that never charge a monthly fee, call 07860 244 274.",
        "timestamps": [
            "00:00 - Free features with local MicroSD card storage",
            "00:14 - What features require a Tapo Care cloud subscription",
            "00:26 - Integrating Tapo cameras into local NVR recorders via RTSP",
            "00:36 - Gary Pearce ADI Communications direct mobile 07860 244 274"
        ]
    },
    "five-mistakes-to-avoid-choosing-home-security-installer": {
        "title": "5 Mistakes to Avoid When Choosing a Home Security Installer",
        "question": "What are the 5 critical mistakes homeowners make when hiring a CCTV or alarm installer?",
        "category": "Home Security Buying Advice",
        "description": "Trade advice from Gary Pearce on vetting security installers: avoiding vague quotes, unbranded clone hardware, poor cable routing, lack of public liability insurance, and high-pressure subscription contracts.",
        "script_narration": "Here are five critical mistakes to avoid when choosing a home security installer in the UK. Mistake one: accepting vague quotes that don't specify the exact camera model numbers, lens focal lengths, or NVR hard drive size. Mistake two: hiring someone without verifiable public liability insurance—always demand to see at least two million pounds of cover; at ADI Communications we carry ten million pounds. Mistake three: letting an installer drill through cavity insulation without installing proper weatherproof drip loops. Mistake four: getting locked into perpetual monthly subscription fees when you can own your hardware outright. And mistake five: using unvetted sub-contractors. I'm Gary Pearce, lead engineer at ADI Communications with 25 years hands-on experience. Call me directly on 07860 244 274.",
        "timestamps": [
            "00:00 - Mistake 1: Vague quotes without exact model specifications",
            "00:11 - Mistake 2: Insufficient public liability insurance verification",
            "00:22 - Mistake 3: Cable routing, drip loops, and masonry seals",
            "00:32 - Mistake 4: Avoiding perpetual cloud subscription traps",
            "00:40 - Gary Pearce ADI Communications direct mobile 07860 244 274"
        ]
    }
}

# Find all MP4 files on disk
mp4_files = sorted(VIDEOS_DIR.glob("*.mp4"))
print(f"Found {len(mp4_files)} MP4 files on disk.")

master_catalog = []

for mp4_path in mp4_files:
    slug = mp4_path.stem
    thumb_path = VIDEOS_DIR / f"{slug}_thumb.webp"
    has_thumb = thumb_path.exists()
    file_size_mb = round(mp4_path.stat().st_size / (1024 * 1024), 2)

    # Get duration via ffprobe
    try:
        res = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(mp4_path)
        ], capture_output=True, text=True, check=True)
        duration_sec = round(float(res.stdout.strip()), 1)
    except Exception:
        duration_sec = 45.0

    # Match metadata
    if slug in lookup_50:
        src = lookup_50[slug]
        title = src.get("title", slug.replace("-", " ").title())
        question = src.get("question", title)
        category = src.get("trade_category", src.get("category", "Field Engineering"))
        description = src.get("description", src.get("script_narration", "")[:250])
        script = src.get("script_narration", "")
        timestamps = src.get("timestamps", [
            f"00:00 - Introduction & Physical Problem Analysis",
            f"00:15 - Technical Engineering Standards & Field Installation",
            f"00:30 - ADI Communications Gary Pearce Direct Mobile 07860 244 274"
        ])
    elif slug in lookup_faq:
        src = lookup_faq[slug]
        title = src.get("title", slug.replace("-", " ").title())
        question = src.get("question", title)
        category = src.get("service_name", src.get("category", "Physical Security"))
        description = src.get("bluf_answer", src.get("description", ""))
        script = src.get("script_narration", src.get("bluf_answer", ""))
        timestamps = [
            f"00:00 - Question: {question[:50]}...",
            f"00:14 - Physical Field Diagnostics & Standards",
            f"00:28 - Turnkey Trade Rectification",
            f"00:38 - Gary Pearce ADI Communications 07860 244 274"
        ]
    elif slug in custom_meta:
        src = custom_meta[slug]
        title = src["title"]
        question = src["question"]
        category = src["category"]
        description = src["description"]
        script = src["script_narration"]
        timestamps = src["timestamps"]
    else:
        # Fallback heuristic
        title = slug.replace("-", " ").title()
        question = f"How does a professional installer solve {title.lower()}?"
        category = "Field Engineering"
        description = f"Technical field analysis and trade engineering standard for {title} by Gary Pearce, ADI Communications (07860 244 274)."
        script = description
        timestamps = [
            f"00:00 - Problem Overview & Safety Standards",
            f"00:20 - Physical Trade Solution & Testing",
            f"00:35 - Gary Pearce Direct Mobile 07860 244 274"
        ]

    entry = {
        "id": f"vid-{len(master_catalog)+1:03d}",
        "slug": slug,
        "title": title,
        "question": question,
        "trade_category": category,
        "duration_seconds": duration_sec,
        "file_size_mb": file_size_mb,
        "mp4_relative_path": f"assets/videos/{slug}.mp4",
        "thumb_relative_path": f"assets/videos/{slug}_thumb.webp",
        "has_thumbnail": has_thumb,
        "lead_engineer": "Gary Pearce",
        "company": "ADI Communications",
        "direct_phone": "07860 244 274",
        "public_liability_insurance": "£10,000,000",
        "verified_rating": "9.98 / 10 across 84+ reviews",
        "youtube_apex_channel": "https://www.youtube.com/@CCTV.services",
        "description": description,
        "script_narration": script,
        "timestamps": timestamps,
        "tags": [
            category,
            "Gary Pearce",
            "ADI Communications",
            "07860 244 274",
            "UK Trade Standards",
            "Home Security UK"
        ]
    }
    master_catalog.append(entry)

# Write master catalog
out_obj = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "catalog_title": "ADI Communications & Gary Pearce – Master 88 Customer Problem-Solving Video Vault",
    "version": "2.0.0",
    "total_videos": len(master_catalog),
    "total_size_mb": round(sum(v["file_size_mb"] for v in master_catalog), 2),
    "lead_engineer": "Gary Pearce (07860 244 274)",
    "public_liability": "£10,000,000",
    "verified_rating": "9.98 / 10 (84+ Reviews)",
    "categories": sorted(list(set(v["trade_category"] for v in master_catalog))),
    "videos": master_catalog
}

with open(OUT_CATALOG, "w", encoding="utf-8") as f:
    json.dump(out_obj, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {OUT_CATALOG} with {len(master_catalog)} videos!")
print(f"Total Video Vault Size: {out_obj['total_size_mb']} MB")
print(f"Categories ({len(out_obj['categories'])}): {', '.join(out_obj['categories'])}")
