import os
import sys
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")
ASSETS_DIR = REPO_ROOT / "assets"
THUMBS_DIR = ASSETS_DIR / "videos" / "thumbs"
DIST_THUMBS_DIR = REPO_ROOT / "dist" / "assets" / "videos" / "thumbs"
THUMBS_DIR.mkdir(parents=True, exist_ok=True)
DIST_THUMBS_DIR.mkdir(parents=True, exist_ok=True)

CATALOG_PATH = REPO_ROOT / "video_master_185_catalog.json"

FONT_ARIAL_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_SEGOE_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_CONSOLA_BOLD = "C:/Windows/Fonts/consolab.ttf"

def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

# 1. Discover all high-res trade images
candidate_imgs = []
for root, dirs, files in os.walk(ASSETS_DIR):
    if "thumbs" in root:
        continue
    for f in files:
        if f.endswith(('.webp', '.jpg', '.png')) and not f.endswith('_exif.webp'):
            p = Path(root) / f
            try:
                with Image.open(p) as img:
                    if img.width >= 600 and img.height >= 300:
                        candidate_imgs.append(p)
            except Exception:
                pass

print(f"Discovered {len(candidate_imgs)} valid high-res trade images.")

# Load catalog
with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

videos = catalog["videos"]
print(f"Total videos to generate thumbnails for: {len(videos)}")

# Keyword score matcher
def score_image_match(img_path: Path, title: str, category: str) -> int:
    name = img_path.name.lower()
    text = (title + " " + category).lower()
    score = 0
    
    # Priority keyword scoring
    keywords = [
        "cctv", "camera", "colorvu", "night", "dark", "infrared", "turret", "dome", "bullet",
        "alarm", "ajax", "motion", "doorprotect", "hub", "siren", "keypad", "pir", "sensor",
        "starlink", "dish", "satellite", "chimney", "mount", "bracket", "cable", "cat6",
        "wifi", "wi-fi", "mesh", "bridge", "ethernet", "router", "switch",
        "tv", "aerial", "wall", "soundbar", "bracket", "mantel", "media"
    ]
    for kw in keywords:
        if kw in text and kw in name:
            score += 10
            
    # Category matches
    cat_lower = category.lower()
    if "cctv" in cat_lower and ("cctv" in name or "camera" in name or "colorvu" in name):
        score += 5
    elif "alarm" in cat_lower and ("alarm" in name or "ajax" in name or "hub" in name):
        score += 5
    elif "starlink" in cat_lower and "starlink" in name:
        score += 8
    elif ("wi-fi" in cat_lower or "cabling" in cat_lower) and ("cat6" in name or "wifi" in name or "bridge" in name):
        score += 5
    elif "tv" in cat_lower and ("tv" in name or "aerial" in name):
        score += 5
        
    return score

# Assign 100% unique background images with zero reuse
assigned_images = {}
used_images = set()

# Pass 1: Best score matching
for v in videos:
    v_id = v["id"]
    title = v["title"]
    category = v["trade_category"]
    
    # Score remaining candidates
    scored = []
    for img in candidate_imgs:
        if img not in used_images:
            s = score_image_match(img, title, category)
            scored.append((s, img))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    best_img = scored[0][1]
    assigned_images[v_id] = best_img
    used_images.add(best_img)

print(f"Assigned {len(assigned_images)} 100% UNIQUE background images across all {len(videos)} videos (Zero Duplication)!")

# Generator function
f_ch = get_font(FONT_CONSOLA_BOLD, 22)
f_title1 = get_font(FONT_ARIAL_BOLD, 46)
f_title2 = get_font(FONT_ARIAL_BOLD, 46)
f_sub = get_font(FONT_SEGOE_BOLD, 22)
f_badge = get_font(FONT_SEGOE_BOLD, 20)

for idx, v in enumerate(videos, 1):
    slug = v["slug"]
    title = v["title"]
    ch_num = v["chapter_number"]
    ch_name = v["chapter_name"]
    category = v["trade_category"]
    base_img_path = assigned_images[v["id"]]
    
    out_rel = f"assets/videos/thumbs/{slug}_thumb.webp"
    out_path = REPO_ROOT / out_rel
    dist_out_path = REPO_ROOT / "dist" / out_rel

    # 1. Base Image loaded & scaled to 1280x720
    try:
        base = Image.open(base_img_path).convert("RGBA")
    except Exception:
        base = Image.new("RGBA", (1280, 720), (10, 10, 18, 255))
        
    target_w, target_h = 1280, 720
    aspect_target = target_w / target_h
    aspect_img = base.width / base.height
    if aspect_img > aspect_target:
        new_w = int(base.height * aspect_target)
        left = (base.width - new_w) // 2
        base = base.crop((left, 0, left + new_w, base.height))
    else:
        new_h = int(base.width / aspect_target)
        top = (base.height - new_h) // 2
        base = base.crop((0, top, base.width, top + new_h))
    base = base.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # 2. Dark Cinematic Gradient Scrim (left 75% dark for high contrast text)
    scrim = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    scrim_draw = ImageDraw.Draw(scrim)
    for x in range(1280):
        alpha = int(240 - (x / 1280.0) * 125)
        scrim_draw.line([(x, 0), (x, 720)], fill=(5, 5, 10, alpha))
    
    # Top & bottom vignette
    for y in range(160):
        alpha = int(180 * (1 - y / 160.0))
        scrim_draw.line([(0, y), (1280, y)], fill=(0, 0, 0, alpha))
        scrim_draw.line([(0, 719 - y), (1280, 719 - y)], fill=(0, 0, 0, alpha))

    base = Image.alpha_composite(base, scrim)
    draw = ImageDraw.Draw(base)

    # 3. Chapter Badge Pill (Y = 40)
    badge_text = f"CHAPTER {ch_num} • {category.upper()[:32]}"
    draw.rounded_rectangle([50, 40, 50 + len(badge_text) * 12 + 45, 84], radius=8, fill=(10, 10, 18, 220), outline=(255, 85, 0, 240), width=2)
    draw.ellipse([65, 57, 77, 69], fill=(255, 85, 0, 255))
    draw.text((90, 50), badge_text, font=f_ch, fill=(255, 255, 255, 255))

    # 4. Two-Line Balanced Viral Title
    clean_title = re.sub(r'^[0-9]+\.\s*', '', title).strip()
    words = clean_title.split()
    mid = len(words) // 2
    if mid == 0: mid = 1
    line1 = " ".join(words[:mid]).upper()
    line2 = " ".join(words[mid:]).upper()

    y1 = 150
    draw.text((54, y1 + 4), line1, font=f_title1, fill=(0, 0, 0, 240))
    draw.text((50, y1), line1, font=f_title1, fill=(255, 229, 0, 255)) # Yellow

    y2 = y1 + 65
    draw.text((54, y2 + 4), line2, font=f_title2, fill=(0, 0, 0, 240))
    draw.text((50, y2), line2, font=f_title2, fill=(255, 255, 255, 255)) # White

    # 5. Question Context Banner (Y = 310)
    context_text = f"ADI COMMUNICATIONS • 25+ YRS HANDS-ON UK TRADE CRAFTSMANSHIP"
    draw.rounded_rectangle([50, 310, 950, 360], radius=8, fill=(255, 85, 0, 210))
    draw.text((65, 322), context_text, font=f_sub, fill=(255, 255, 255, 255))

    # 6. Trade Seal Card at Bottom (Y = 620 to 680)
    draw.rounded_rectangle([50, 620, 1230, 680], radius=10, fill=(10, 10, 18, 230), outline=(255, 255, 255, 40), width=1)
    draw.text((70, 638), "GARY PEARCE • ADI COMMUNICATIONS", font=f_badge, fill=(255, 255, 255, 255))
    draw.text((500, 638), "📞 DIRECT: 07860 244 274", font=f_badge, fill=(255, 160, 122, 255))
    draw.text((820, 638), "★★★★★ 9.98 / 10 RATING (84+ REVIEWS)", font=f_badge, fill=(255, 229, 0, 255))

    # 7. Play Indicator Circle on the right
    cx, cy = 1140, 260
    draw.ellipse([cx - 55, cy - 55, cx + 55, cy + 55], fill=(255, 85, 0, 220), outline=(255, 255, 255, 180), width=3)
    draw.polygon([(cx - 15, cy - 25), (cx - 15, cy + 25), (cx + 25, cy)], fill=(255, 255, 255, 255))

    # Save to WebP in both assets and dist
    rgb = base.convert("RGB")
    rgb.save(out_path, "WEBP", quality=88)
    dist_out_path.parent.mkdir(parents=True, exist_ok=True)
    rgb.save(dist_out_path, "WEBP", quality=88)

    # Update catalog entry
    v["thumb_relative_path"] = out_rel

    if idx % 25 == 0 or idx == len(videos):
        print(f"Generated {idx}/{len(videos)} thumbnails: {out_path.name}")

# Save updated catalog
with open(CATALOG_PATH, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

# Also sync to dist if exists
dist_cat = REPO_ROOT / "dist" / "video_master_185_catalog.json"
if dist_cat.parent.exists():
    with open(dist_cat, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

print(f"\nALL 185 BESPOKE THUMBNAILS SUCCESSFULLY GENERATED WITH ZERO DUPLICATION!")
