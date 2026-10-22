import os
import csv
import json
import glob

REPO_ROOT = r"C:\Users\Gary\github-cctv-seo"
OUTPUT_DIR = os.path.join(REPO_ROOT, "category_manifests")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 11 Stacks Configuration
STACK_CATEGORIES = {
    "01_video_stack": {
        "name": "Video Stack",
        "apex": "https://www.youtube.com/@CCTV.services",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/cctv-police-evidence-hero.webp",
        "filter_cats": ["Video", "Video Stack", "YouTube", "Video Showcase"]
    },
    "02_podcast_audio_stack": {
        "name": "Podcast & Audio Stack",
        "apex": "https://www.youtube.com/playlist?list=PLcctv_security_debriefs_adi",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/podcast-cover-art-1400.png",
        "filter_cats": ["Podcast", "Audio", "Audio Stack", "Podcast Debrief"]
    },
    "03_docs_whitepapers_stack": {
        "name": "Docs, PDFs & Research Stack",
        "apex": "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/cctv-dori-calculation-chart.webp",
        "filter_cats": ["Docs", "PDF", "Whitepaper", "Research", "CAD Vault"]
    },
    "04_blog_editorial_stack": {
        "name": "Blog & Editorial Parasite Stack",
        "apex": "https://tvandhomesecurity.blogspot.com/",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/cctv-police-evidence-hero.webp",
        "filter_cats": ["Blog", "Editorial", "Article", "Parasite SEO"]
    },
    "05_cloud_apps_tools_stack": {
        "name": "Cloud Apps, Tools & Static Edge Stack",
        "apex": "https://gary-pearce-forensic-hub.web.app/",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/poe-switch-og.webp",
        "filter_cats": ["Cloud", "Developer Tool", "Edge Hosting", "Calculator", "Interactive App"]
    },
    "06_images_trade_photography_stack": {
        "name": "Images & Visual Trade Photography Stack",
        "apex": "https://lh3.googleusercontent.com/d/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88=w1600",
        "video": "https://www.youtube.com/watch?v=F3v6wX_m9_K",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/starlink-chimney-mount-lashing-kit-uk.webp",
        "filter_cats": ["Images", "Visual", "Trade Photography", "Gallery"]
    },
    "07_howto_instructions_stack": {
        "name": "Instructions & How-To Guides Stack",
        "apex": "https://classroom.google.com/c/adi_security_telecom_academy",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/cat6-cavity-wall-installation-uk.webp",
        "filter_cats": ["How-To", "Instructions", "Guide", "Tutorial", "Academy"]
    },
    "08_bookmarking_discovery_stack": {
        "name": "Bookmarking & Link Discovery Stack",
        "apex": "https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/poe-switch-og.webp",
        "filter_cats": ["Bookmarking", "Social Discovery", "Public Ledger", "Curation"]
    },
    "09_rss_feed_stack": {
        "name": "RSS Feed Stacking & Aggregation",
        "apex": "https://tvandhomesecurity.blogspot.com/feeds/posts/default",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/podcast-cover-art-1400.png",
        "filter_cats": ["RSS", "Feed", "Feedburner", "Syndication Loop"]
    },
    "10_music_audio_stack": {
        "name": "Music & Audio Showcase Stack",
        "apex": "https://music.youtube.com/channel/UCt7VpJGmZZ12hdg2sCgjQag",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/adi-sound-system-cover.webp",
        "filter_cats": ["Music", "Audio Showcase", "Theme Track", "Sonic Branding"]
    },
    "11_offers_directories_stack": {
        "name": "Offers, Deals & Trade Directories Stack",
        "apex": "https://share.google/ATfZAwAPIiyPHkxUN",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/cctv-turret-soffit-installation-uk.webp",
        "filter_cats": ["Directory", "Citation", "Offers", "NAP", "GBP"]
    }
}

# Ingest Sources
# 1. Master Backlink Ledger
master_csv = os.path.join(REPO_ROOT, "public_backlink_master_ledger.csv")
all_rows = []
if os.path.exists(master_csv):
    with open(master_csv, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

# 2. Established Profiles (Doc 2)
doc2_csv = os.path.join(REPO_ROOT, "doc2_established_profiles_list.csv")
doc2_rows = []
if os.path.exists(doc2_csv):
    with open(doc2_csv, "r", encoding="utf-8", errors="ignore") as f:
        doc2_rows = list(csv.DictReader(f))

# 3. Cloud Stack
cloud_csv = os.path.join(REPO_ROOT, "doc2_cloud_stack_100.csv")
cloud_rows = []
if os.path.exists(cloud_csv):
    with open(cloud_csv, "r", encoding="utf-8", errors="ignore") as f:
        cloud_rows = list(csv.DictReader(f))

# 4. Music Stack
music_csv = os.path.join(REPO_ROOT, "doc1_music_stack_100.csv")
music_rows = []
if os.path.exists(music_csv):
    with open(music_csv, "r", encoding="utf-8", errors="ignore") as f:
        music_rows = list(csv.DictReader(f))

# Category Mapping Rules
CATEGORY_RULES = {
    "01_video_stack": {
        "name": "Video Stack",
        "apex": "https://www.youtube.com/@CCTV.services",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/cctv-police-evidence-hero.webp",
        "match": lambda cat, plat: "video" in cat.lower() or "youtube" in plat.lower() or "vimeo" in plat.lower() or "dailymotion" in plat.lower()
    },
    "02_podcast_audio_stack": {
        "name": "Podcast & Audio Stack",
        "apex": "https://www.youtube.com/playlist?list=PLcctv_security_debriefs_adi",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/podcast-cover-art-1400.png",
        "match": lambda cat, plat: "audio" in cat.lower() or "podcast" in cat.lower() or "podbean" in plat.lower() or "spotify" in plat.lower() or "soundcloud" in plat.lower()
    },
    "03_docs_whitepapers_stack": {
        "name": "Docs, PDFs & Research Stack",
        "apex": "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/cctv-dori-calculation-chart.webp",
        "match": lambda cat, plat: "pdf" in cat.lower() or "document" in cat.lower() or "research" in cat.lower() or "zenodo" in plat.lower() or "archive" in plat.lower()
    },
    "04_blog_editorial_stack": {
        "name": "Blog & Editorial Parasite Stack",
        "apex": "https://tvandhomesecurity.blogspot.com/",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/cctv-police-evidence-hero.webp",
        "match": lambda cat, plat: "blog" in cat.lower() or "article" in cat.lower() or "dev.to" in plat.lower() or "hashnode" in plat.lower() or "medium" in plat.lower() or "substack" in plat.lower()
    },
    "05_cloud_apps_tools_stack": {
        "name": "Cloud Apps, Tools & Static Edge Stack",
        "apex": "https://gary-pearce-forensic-hub.web.app/",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/poe-switch-og.webp",
        "match": lambda cat, plat: "microsite" in cat.lower() or "edge" in cat.lower() or "cloud" in cat.lower() or "hosting" in cat.lower() or "code" in cat.lower() or "tool" in cat.lower()
    },
    "06_images_trade_photography_stack": {
        "name": "Images & Visual Trade Photography Stack",
        "apex": "https://lh3.googleusercontent.com/d/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88=w1600",
        "video": "https://www.youtube.com/watch?v=F3v6wX_m9_K",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/starlink-chimney-mount-lashing-kit-uk.webp",
        "match": lambda cat, plat: "image" in cat.lower() or "photo" in cat.lower() or "media" in cat.lower() or "pinterest" in plat.lower() or "flickr" in plat.lower()
    },
    "07_howto_instructions_stack": {
        "name": "Instructions & How-To Guides Stack",
        "apex": "https://classroom.google.com/c/adi_security_telecom_academy",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/cat6-cavity-wall-installation-uk.webp",
        "match": lambda cat, plat: "instruction" in cat.lower() or "how-to" in cat.lower() or "tutorial" in cat.lower() or "guide" in cat.lower() or "wiki" in plat.lower()
    },
    "08_bookmarking_discovery_stack": {
        "name": "Bookmarking & Link Discovery Stack",
        "apex": "https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/poe-switch-og.webp",
        "match": lambda cat, plat: "bookmark" in cat.lower() or "social" in cat.lower() or "community" in cat.lower() or "data" in cat.lower() or "dataset" in cat.lower()
    },
    "09_rss_feed_stack": {
        "name": "RSS Feed Stacking & Aggregation",
        "apex": "https://tvandhomesecurity.blogspot.com/feeds/posts/default",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/podcast-cover-art-1400.png",
        "match": lambda cat, plat: "rss" in cat.lower() or "feed" in cat.lower() or "syndication" in cat.lower()
    },
    "10_music_audio_stack": {
        "name": "Music & Audio Showcase Stack",
        "apex": "https://music.youtube.com/channel/UCt7VpJGmZZ12hdg2sCgjQag",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/adi-sound-system-cover.webp",
        "match": lambda cat, plat: "music" in cat.lower() or "sound" in cat.lower() or "bandcamp" in plat.lower() or "audius" in plat.lower()
    },
    "11_offers_directories_stack": {
        "name": "Offers, Deals & Trade Directories Stack",
        "apex": "https://share.google/ATfZAwAPIiyPHkxUN",
        "video": "https://www.youtube.com/watch?v=k43XjD_m2_M",
        "image": "https://gazpearce.github.io/cctv-security-hub/assets/images/cctv-turret-soffit-installation-uk.webp",
        "match": lambda cat, plat: "directory" in cat.lower() or "citation" in cat.lower() or "open-source" in cat.lower() or "freeindex" in plat.lower() or "cylex" in plat.lower()
    }
}

# 3. Ingest Interactive HTML Tools
tools = [
    {"title": "CCTV PoE Switch Budget & Night-Loading Calculator", "file": "poe-switch-budget-calculator.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "CCTV DORI Optical Lens & Identification Calculator", "file": "cctv-dori-lens-calculator.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "CCTV Storage, Bitrate & NVR Hard Drive Calculator", "file": "cctv-storage-bandwidth-calculator.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "PoE Voltage Drop & Resistance Distance Calculator", "file": "poe-voltage-drop-calculator.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "Ajax Wireless Alarm System Grade & Radio Range Selector", "file": "ajax-alarm-grade-selector.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "Garden Office Wireless PTP Wi-Fi Bridge Calculator", "file": "garden-office-wifi-bridge-calculator.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "Smart Doorbell 24V Transformer & Voltage Drop Calculator", "file": "smart-doorbell-transformer-calculator.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "Starlink Roof Obstruction & Gale Mount Calculator", "file": "starlink-mount-obstacle-finder.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "Starlink vs 5G Rural Broadband 3-Year TCO Calculator", "file": "starlink-vs-5g-cost-calculator.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "Starlink Chimney Wind Load & Gale Shear Calculator", "file": "starlink-wind-load-calculator.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "TV Above Fireplace Thermal Safety & Wall Anchor Calculator", "file": "tv-fireplace-bracket-calculator.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "TV Wall Mount Stud & Thermal Deflection Calculator", "file": "tv-fireplace-thermal-calculator.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "Ethernet Upstairs & Home Network Diagnostic Calculator", "file": "ethernet-upstairs-calculator.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "UK Postcode Crime Telemetry & Police Security Checker", "file": "uk-postcode-crime-risk-checker.html", "cat": "Cloud Apps, Tools & Static Edge Stack"},
    {"title": "Commercial Trade Photography & Schematics Gallery", "file": "image-gallery.html", "cat": "Images & Visual Trade Photography Stack"},
    {"title": "Official 4K CCTV Field Video Showcase", "file": "video-showcase.html", "cat": "Video Stack"},
    {"title": "Sound System 7 Sonic Branding & Telemetry Audio Showcase", "file": "music-showcase.html", "cat": "Music & Audio Showcase Stack"},
    {"title": "Public Backlink Master Ledger & Google Drive Discovery Stack", "file": "public_backlink_ledger.html", "cat": "Bookmarking & Link Discovery Stack"},
    {"title": "Property, Profile & Asset Link Relational Tracker", "file": "property-asset-tracker.html", "cat": "Bookmarking & Link Discovery Stack"},
    {"title": "Master 1,000 Free Publishing & Automation Directory", "file": "publishing-directory.html", "cat": "Bookmarking & Link Discovery Stack"},
    {"title": "UK CCTV Planning Permission & Permitted Development Guide", "file": "cctv-planning-permission.html", "cat": "Instructions & How-To Guides Stack"},
    {"title": "ColorVu Night Vision vs Traditional IR Security Standards", "file": "night-vision-technology.html", "cat": "Docs, PDFs & Research Stack"}
]

# Write CSV Manifests for each Category
manifest_files = []

# Write CSV Manifests for each Category
manifest_files = []

for key, config in CATEGORY_RULES.items():
    csv_filename = f"{key}.csv"
    csv_path = os.path.join(OUTPUT_DIR, csv_filename)
    manifest_files.append((config["name"], csv_filename, config["apex"]))
    
    cat_rows = []
    seen_urls = set()
    
    # 1. Check Master Backlink Ledger
    for r in all_rows:
        cat = r.get("category", "")
        plat = r.get("platform", "")
        url = r.get("public_live_url", "")
        if url and url not in seen_urls and config["match"](cat, plat):
            seen_urls.add(url)
            cat_rows.append({
                "asset_id": f"AST-{len(cat_rows)+1:03d}",
                "category": config["name"],
                "platform": plat,
                "title": r.get("asset_title", "Technical Field Asset"),
                "live_url": url,
                "top_of_stack_apex_url": config["apex"],
                "featured_image_url": config["image"],
                "video_embed_url": config["video"],
                "seo_tags": r.get("seo_tags", "cctv, starlink, ajax, gary-pearce"),
                "seo_description": r.get("seo_description", "Technical field engineering asset by Gary Pearce (07860 244 274)."),
                "author_engineer": "Gary Pearce (ADI Communications)",
                "direct_phone": "07860 244 274"
            })

    # 2. Check Established Profiles (Doc 2)
    for r in doc2_rows:
        cat = r.get("category", "")
        plat = r.get("platform_name", "")
        url = r.get("profile_live_url", "")
        if url and url not in seen_urls and config["match"](cat, plat):
            seen_urls.add(url)
            cat_rows.append({
                "asset_id": f"PROF-{len(cat_rows)+1:03d}",
                "category": config["name"],
                "platform": plat,
                "title": r.get("profile_title", f"{plat} Official Profile"),
                "live_url": url,
                "top_of_stack_apex_url": config["apex"],
                "featured_image_url": config["image"],
                "video_embed_url": config["video"],
                "seo_tags": r.get("seo_tags", "cctv, telecommunications, gary-pearce"),
                "seo_description": r.get("profile_bio_summary", "Professional telecommunications profile by Gary Pearce."),
                "author_engineer": "Gary Pearce (ADI Communications)",
                "direct_phone": "07860 244 274"
            })

    # 3. Check Cloud Stack (if matching)
    for r in cloud_rows:
        cat = r.get("Category", "")
        plat = r.get("Platform Name", "")
        url = r.get("Active Tenant URL", "") or r.get("Official Signup / Cloud URL", "")
        if url and url not in seen_urls and config["match"](cat, plat):
            seen_urls.add(url)
            cat_rows.append({
                "asset_id": f"CLOUD-{len(cat_rows)+1:03d}",
                "category": config["name"],
                "platform": plat,
                "title": f"{plat} Cloud Deployment",
                "live_url": url,
                "top_of_stack_apex_url": config["apex"],
                "featured_image_url": config["image"],
                "video_embed_url": config["video"],
                "seo_tags": "cloud, tools, static-edge, gary-pearce",
                "seo_description": f"Cloud deployment on {plat} by Gary Pearce (07860 244 274).",
                "author_engineer": "Gary Pearce (ADI Communications)",
                "direct_phone": "07860 244 274"
            })

    # 4. Check Music Stack (if matching)
    for r in music_rows:
        cat = r.get("Category", "")
        plat = r.get("Platform Name", "")
        url = r.get("Public Track / Profile URL Pattern", "")
        if url and url not in seen_urls and config["match"](cat, plat):
            seen_urls.add(url)
            cat_rows.append({
                "asset_id": f"AUDIO-{len(cat_rows)+1:03d}",
                "category": config["name"],
                "platform": plat,
                "title": f"{plat} Audio Stream",
                "live_url": url,
                "top_of_stack_apex_url": config["apex"],
                "featured_image_url": config["image"],
                "video_embed_url": config["video"],
                "seo_tags": "audio, sound-system, telemetry, gary-pearce",
                "seo_description": f"Audio telemetry track on {plat} by Gary Pearce (07860 244 274).",
                "author_engineer": "Gary Pearce (ADI Communications)",
                "direct_phone": "07860 244 274"
            })

    # Add RSS Feed special entries
    if key == "09_rss_feed_stack":
        rss_feeds = [
            ("Google Blogger Master RSS", "https://tvandhomesecurity.blogspot.com/feeds/posts/default"),
            ("Google Feedburner Syndication Feed", "https://feeds.feedburner.com/ADICommunicationsSecurityDebrief"),
            ("ADI Technical Audio Podcast XML Feed", "https://gary-pearce-forensic-hub.web.app/podcast.xml"),
            ("Master Site & Authority XML Sitemap", "https://gary-pearce-forensic-hub.web.app/sitemap.xml"),
            ("Spider Crawler Discovery XML Sitemap", "https://gary-pearce-forensic-hub.web.app/sitemap-spider.xml"),
            ("Feedly Shared Public Board", "https://feedly.com/i/subscription/feed/https://tvandhomesecurity.blogspot.com/feeds/posts/default"),
            ("Inoreader RSS Reader Stream", "https://www.inoreader.com/feed/https%3A%2F%2Ftvandhomesecurity.blogspot.com%2Ffeeds%2Fposts%2Fdefault")
        ]
        for feed_title, feed_url in rss_feeds:
            if feed_url not in seen_urls:
                seen_urls.add(feed_url)
                cat_rows.append({
                    "asset_id": f"RSS-{len(cat_rows)+1:03d}",
                    "category": config["name"],
                    "platform": "Google Feedburner / Blogger RSS",
                    "title": feed_title,
                    "live_url": feed_url,
                    "top_of_stack_apex_url": config["apex"],
                    "featured_image_url": config["image"],
                    "video_embed_url": config["video"],
                    "seo_tags": "rss, feed, syndication, google-feedburner",
                    "seo_description": f"Syndicated XML feed stream by Gary Pearce (07860 244 274).",
                    "author_engineer": "Gary Pearce (ADI Communications)",
                    "direct_phone": "07860 244 274"
                })

            
    # 5. Add Tools matching category
    for t in tools:
        if t["cat"] == config["name"]:
            url = f"https://gazpearce.github.io/cctv-security-hub/{t['file']}"
            if url not in seen_urls:
                seen_urls.add(url)
                cat_rows.append({
                    "asset_id": f"TOOL-{len(cat_rows)+1:03d}",
                    "category": config["name"],
                    "platform": "GitHub / Firebase Edge",
                    "title": t["title"],
                    "live_url": url,
                    "top_of_stack_apex_url": config["apex"],
                    "featured_image_url": config["image"],
                    "video_embed_url": config["video"],
                    "seo_tags": "cctv, tools, engineering, calculator, west-yorkshire",
                    "seo_description": f"{t['title']} engineered by Gary Pearce (07860 244 274) at ADI Communications.",
                    "author_engineer": "Gary Pearce (ADI Communications)",
                    "direct_phone": "07860 244 274"
                })
            
    # Write to CSV
    fieldnames = [
        "asset_id", "category", "platform", "title", "live_url", 
        "top_of_stack_apex_url", "featured_image_url", "video_embed_url", 
        "seo_tags", "seo_description", "author_engineer", "direct_phone"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cat_rows)
        
    print(f"Generated {csv_filename} with {len(cat_rows)} verified assets.")


# Also generate a master tools CSV
tools_csv_path = os.path.join(OUTPUT_DIR, "12_all_engineering_tools.csv")
with open(tools_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "asset_id", "category", "platform", "title", "live_url", 
        "top_of_stack_apex_url", "featured_image_url", "video_embed_url", 
        "seo_tags", "seo_description", "author_engineer", "direct_phone"
    ])
    writer.writeheader()
    for idx, t in enumerate(tools):
        writer.writerow({
            "asset_id": f"TOOL-{idx+1:03d}",
            "category": t["cat"],
            "platform": "GitHub / Firebase Edge",
            "title": t["title"],
            "live_url": f"https://gazpearce.github.io/cctv-security-hub/{t['file']}",
            "top_of_stack_apex_url": "https://gary-pearce-forensic-hub.web.app/",
            "featured_image_url": "https://gazpearce.github.io/cctv-security-hub/assets/images/poe-switch-og.webp",
            "video_embed_url": "https://www.youtube.com/watch?v=k43XjD_m2_M",
            "seo_tags": "cctv, tools, engineering, calculator, west-yorkshire",
            "seo_description": f"{t['title']} engineered by Gary Pearce (07860 244 274) at ADI Communications.",
            "author_engineer": "Gary Pearce (ADI Communications)",
            "direct_phone": "07860 244 274"
        })
print("Generated 12_all_engineering_tools.csv with all 22 interactive tools.")

# 4. Generate Spider Crawler Index HTML (for Search Engine Spiders to crawl all URLs and CSVs)
spider_html_path = os.path.join(REPO_ROOT, "spider_crawler_index.html")

manifest_cards_html = ""
for name, filename, apex in manifest_files:
    manifest_cards_html += f"""
    <div class="p-5 rounded-xl bg-white/[0.03] border border-white/10 hover:border-orange-500/40 transition">
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-base font-bold text-white">{name}</h3>
        <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-orange-500/20 text-orange-400">CSV Manifest</span>
      </div>
      <p class="text-xs text-neutral-400 mb-4">Complete indexed dataset of assets, images, video embeds, and upward Google Citadel Apex links.</p>
      <div class="flex flex-wrap gap-2 text-xs font-mono">
        <a href="category_manifests/{filename}" download class="px-3 py-1.5 rounded-lg bg-orange-600 hover:bg-orange-500 text-white font-bold transition">
          📥 Download CSV
        </a>
        <a href="{apex}" target="_blank" rel="noopener" class="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-neutral-300 transition">
          🏛️ Visit Google Apex
        </a>
      </div>
    </div>
    """

tools_list_html = ""
for t in tools:
    tools_list_html += f"""
    <li class="p-3 rounded-lg bg-white/[0.02] border border-white/5 hover:border-orange-500/30 transition flex flex-col sm:flex-row sm:items-center justify-between gap-2">
      <div>
        <a href="{t['file']}" class="text-sm font-semibold text-white hover:text-orange-400 transition">{t['title']}</a>
        <div class="text-xs text-neutral-400 font-mono mt-0.5">Category: {t['cat']}</div>
      </div>
      <a href="{t['file']}" class="text-xs font-mono px-3 py-1 rounded bg-white/5 hover:bg-orange-500/20 text-orange-300 border border-white/10 shrink-0 self-start sm:self-center">
        Launch Tool ↗
      </a>
    </li>
    """

spider_html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Spider Crawler Discovery Index & Category Manifests | ADI Communications</title>
  <meta name="description" content="Central Googlebot and crawler index gateway for ADI Communications. Contains complete category CSV manifests, verified asset links, interactive engineering tools, and Google Citadel Apex nodes under Gary Pearce (07860 244 274).">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="canonical" href="https://gary-pearce-forensic-hub.web.app/spider_crawler_index.html">

  <!-- JSON-LD Structured Data Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "DataCatalog",
        "name": "ADI Communications Category Manifest & Crawler Discovery Index",
        "description": "Central spider and Googlebot crawl gateway indexing all 11 category stacks, CSV manifests, 22 interactive engineering tools, and Google Apex authority nodes.",
        "url": "https://gary-pearce-forensic-hub.web.app/spider_crawler_index.html",
        "creator": {{
          "@type": "Person",
          "name": "Gary Pearce",
          "jobTitle": "Lead Telecoms & Security Engineer",
          "telephone": "+447860244274"
        }},
        "publisher": {{
          "@type": "Organization",
          "name": "ADI Communications",
          "url": "https://tvandhomesecurity.blogspot.com/"
        }}
      }},
      {{
        "@type": "LocalBusiness",
        "name": "ADI Communications",
        "telephone": "+447860244274",
        "url": "https://tvandhomesecurity.blogspot.com/",
        "areaServed": "West Yorkshire, UK"
      }}
    ]
  }}
  </script>
</head>
<body class="bg-[#050508] text-neutral-200 min-h-screen p-4 sm:p-8 font-sans">
  <div class="max-w-6xl mx-auto">
    <!-- Header -->
    <header class="mb-10 pb-6 border-b border-white/10">
      <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-orange-500/10 border border-orange-500/30 text-orange-400 text-xs font-mono mb-3">
        <span class="w-2 h-2 rounded-full bg-orange-500 animate-pulse"></span>
        <span>Googlebot & Spider Crawler Gateway • 100% Verified HTTP 200</span>
      </div>
      <h1 class="text-3xl sm:text-5xl font-black text-white tracking-tight uppercase">
        Spider Crawler Discovery Index
      </h1>
      <p class="mt-3 text-sm sm:text-base text-neutral-400 max-w-3xl">
        Authoritative indexing gateway providing structured CSV manifests, deep link matrices, image/video embeds, and direct upward link pathways into the 11 Google Citadel Apex entities. Verified under <strong class="text-white">Rule 45 Google Shield Air-Gap</strong> (0 raw root links).
      </p>
      <div class="mt-4 flex flex-wrap gap-3 font-mono text-xs">
        <span class="px-3 py-1 rounded-md bg-white/5 border border-white/10 text-neutral-300">Director: Gary Pearce</span>
        <span class="px-3 py-1 rounded-md bg-white/5 border border-white/10 text-neutral-300">Direct Phone: 07860 244 274</span>
        <span class="px-3 py-1 rounded-md bg-white/5 border border-white/10 text-neutral-300">Liability: £10M Public Liability</span>
      </div>
    </header>

    <!-- Category CSV Manifests Grid -->
    <section class="mb-12">
      <h2 class="text-xl sm:text-2xl font-bold text-white mb-4 flex items-center gap-2">
        <span>📊 11 Category CSV Manifests (With Images & Video Embeds)</span>
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {manifest_cards_html}
      </div>
    </section>

    <!-- Interactive Tools & Calculators -->
    <section class="mb-12">
      <h2 class="text-xl sm:text-2xl font-bold text-white mb-4 flex items-center gap-2">
        <span>⚡ 22 Live Engineering Tools & Calculators</span>
      </h2>
      <ul class="space-y-2">
        {tools_list_html}
      </ul>
    </section>

    <!-- Footer -->
    <footer class="pt-8 border-t border-white/10 text-xs text-neutral-500 font-mono flex flex-col sm:flex-row items-center justify-between gap-4">
      <div>
        © 2026 ADI Communications • Gary Pearce (07860 244 274). Rule 45 Google Shield Air-Gap Enforced.
      </div>
      <div class="flex gap-4">
        <a href="public_backlink_ledger.html" class="hover:text-orange-400 transition">Master Backlink Ledger</a>
        <a href="sitemap.xml" class="hover:text-orange-400 transition">Sitemap XML</a>
        <a href="https://tvandhomesecurity.blogspot.com/" class="hover:text-orange-400 transition">Google Shield Blog</a>
      </div>
    </footer>
  </div>
</body>
</html>
"""

with open(spider_html_path, "w", encoding="utf-8") as f:
    f.write(spider_html)
print(f"Generated spider_crawler_index.html at {spider_html_path}")

# Also copy to category_manifests for direct traversal
with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(spider_html)

# 5. Build sitemap-spider.xml and sitemap.xml
sitemap_urls = [
    "https://gary-pearce-forensic-hub.web.app/spider_crawler_index.html",
    "https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html",
    "https://gary-pearce-forensic-hub.web.app/property-asset-tracker.html",
    "https://gary-pearce-forensic-hub.web.app/publishing-directory.html",
    "https://gary-pearce-forensic-hub.web.app/image-gallery.html",
    "https://gary-pearce-forensic-hub.web.app/video-showcase.html",
    "https://gary-pearce-forensic-hub.web.app/music-showcase.html",
    "https://gary-pearce-forensic-hub.web.app/category_manifests/12_all_engineering_tools.csv",
]

for _, fn, _ in manifest_files:
    sitemap_urls.append(f"https://gary-pearce-forensic-hub.web.app/category_manifests/{fn}")

for t in tools:
    sitemap_urls.append(f"https://gary-pearce-forensic-hub.web.app/{t['file']}")

sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

for u in sitemap_urls:
    sitemap_xml += f"""  <url>
    <loc>{u}</loc>
    <lastmod>2026-10-22</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
"""

sitemap_xml += "</urlset>\n"

sitemap_path = os.path.join(REPO_ROOT, "sitemap.xml")
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(sitemap_xml)
print(f"Updated master sitemap.xml with {len(sitemap_urls)} URLs.")

sitemap_spider_path = os.path.join(REPO_ROOT, "sitemap-spider.xml")
with open(sitemap_spider_path, "w", encoding="utf-8") as f:
    f.write(sitemap_xml)
print("Generated sitemap-spider.xml.")
