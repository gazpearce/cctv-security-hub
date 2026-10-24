import os
import sys
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")
IMAGES_DIR = REPO_ROOT / "assets" / "images"
VIDEOS_DIR = REPO_ROOT / "assets" / "videos"
THUMBS_DIR = VIDEOS_DIR / "thumbs"
THUMBS_DIR.mkdir(parents=True, exist_ok=True)

FONT_ARIAL_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_SEGOE_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_CONSOLA_BOLD = "C:/Windows/Fonts/consolab.ttf"

def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

# Load all available base images
ALL_BASE_IMAGES = [
    IMAGES_DIR / f for f in os.listdir(IMAGES_DIR)
    if f.endswith('.webp') and not f.endswith('_exif.webp')
]

def find_best_base_image(title: str, category: str, index: int) -> Path:
    text = (title + " " + category).lower()
    
    # Priority keyword matching
    matches = []
    if "night vision" in text or "colorvu" in text or "dark" in text:
        matches = [f for f in ALL_BASE_IMAGES if "colorvu" in f.name or "night" in f.name]
    elif "plate" in text or "anpr" in text or "zoom" in text or "clear" in text:
        matches = [f for f in ALL_BASE_IMAGES if "panoramic" in f.name or "turret" in f.name or "cctv" in f.name]
    elif "placement" in text or "house" in text or "semi-detached" in text or "exterior" in text:
        matches = [f for f in ALL_BASE_IMAGES if "outdoor" in f.name or "home" in f.name or "masonry" in f.name]
    elif "false alert" in text or "cat" in text or "tree" in text or "pet" in text:
        matches = [f for f in ALL_BASE_IMAGES if "pet" in f.name or "pir" in f.name or "motion" in f.name]
    elif "recording" in text or "storage" in text or "usb" in text or "hard drive" in text or "nvr" in text:
        matches = [f for f in ALL_BASE_IMAGES if "hub" in f.name or "internals" in f.name or "network" in f.name]
    elif "alarm" in text or "ajax" in text or "intruder" in text or "siren" in text:
        matches = [f for f in ALL_BASE_IMAGES if "ajax" in f.name or "siren" in f.name or "keypad" in f.name]
    elif "starlink" in text or "dish" in text or "satellite" in text or "chimney" in text:
        matches = [f for f in ALL_BASE_IMAGES if "starlink" in f.name]
    elif "wi-fi" in text or "wifi" in text or "mesh" in text or "ethernet" in text or "cat6" in text or "cable" in text:
        matches = [f for f in ALL_BASE_IMAGES if "cat6" in f.name or "wifi" in f.name or "bridge" in f.name]
    elif "tv" in text or "mount" in text or "aerial" in text or "bracket" in text or "screen" in text:
        matches = [f for f in ALL_BASE_IMAGES if "tv" in f.name]

    if matches:
        return matches[index % len(matches)]
    
    # Fallback rotation
    return ALL_BASE_IMAGES[index % len(ALL_BASE_IMAGES)]

def create_bespoke_thumbnail(title: str, ch_num: int, ch_name: str, out_path: Path, index: int):
    base_img_path = find_best_base_image(title, ch_name, index)
    
    # 1. Base Image loaded & scaled to 1280x720
    try:
        base = Image.open(base_img_path).convert("RGBA")
    except Exception:
        base = Image.new("RGBA", (1280, 720), (10, 10, 18, 255))
        
    target_w, target_h = 1280, 720
    # Center crop
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
        # 0.95 opacity on left, fading to 0.45 on right
        alpha = int(240 - (x / 1280.0) * 130)
        scrim_draw.line([(x, 0), (x, 720)], fill=(5, 5, 10, alpha))
    
    # Vignette top and bottom
    for y in range(160):
        alpha = int(180 * (1 - y / 160.0))
        scrim_draw.line([(0, y), (1280, y)], fill=(0, 0, 0, alpha))
        scrim_draw.line([(0, 719 - y), (1280, 719 - y)], fill=(0, 0, 0, alpha))

    base = Image.alpha_composite(base, scrim)
    draw = ImageDraw.Draw(base)

    f_ch = get_font(FONT_CONSOLA_BOLD, 22)
    f_title1 = get_font(FONT_ARIAL_BOLD, 46)
    f_title2 = get_font(FONT_ARIAL_BOLD, 46)
    f_sub = get_font(FONT_SEGOE_BOLD, 22)
    f_badge = get_font(FONT_SEGOE_BOLD, 20)

    # 3. Chapter Badge Pill (Y = 45)
    badge_text = f"CHAPTER {ch_num} • {ch_name.upper()[:36]}"
    draw.rounded_rectangle([50, 40, 50 + len(badge_text) * 12 + 40, 84], radius=8, fill=(10, 10, 18, 220), outline=(255, 85, 0, 240), width=2)
    draw.ellipse([65, 57, 77, 69], fill=(255, 85, 0, 255))
    draw.text((90, 50), badge_text, font=f_ch, fill=(255, 255, 255, 255))

    # 4. Two-Line Balanced Viral Title
    # Clean title
    clean_title = re.sub(r'^[0-9]+\.\s*', '', title).strip()
    words = clean_title.split()
    mid = len(words) // 2
    if mid == 0: mid = 1
    line1 = " ".join(words[:mid]).upper()
    line2 = " ".join(words[mid:]).upper()

    # Drop shadows + Text (Y = 160 to 320)
    y1 = 150
    draw.text((54, y1 + 4), line1, font=f_title1, fill=(0, 0, 0, 240))
    draw.text((50, y1), line1, font=f_title1, fill=(255, 229, 0, 255)) # Yellow

    y2 = y1 + 65
    draw.text((54, y2 + 4), line2, font=f_title2, fill=(0, 0, 0, 240))
    draw.text((50, y2), line2, font=f_title2, fill=(255, 255, 255, 255)) # White

    # 5. Question Context Bar (Y = 380)
    draw.rounded_rectangle([50, 310, 950, 360], radius=8, fill=(255, 85, 0, 210))
    draw.text((65, 322), "UK TRADE FIELD ANALYSIS & FAULT DIAGNOSTICS", font=f_sub, fill=(255, 255, 255, 255))

    # 6. Trade Seal Card at Bottom (Y = 620 to 680)
    draw.rounded_rectangle([50, 620, 1230, 680], radius=10, fill=(10, 10, 18, 230), outline=(255, 255, 255, 40), width=1)
    draw.text((70, 638), "GARY PEARCE • ADI COMMUNICATIONS", font=f_badge, fill=(255, 255, 255, 255))
    draw.text((500, 638), "📞 DIRECT: 07860 244 274", font=f_badge, fill=(255, 160, 122, 255))
    draw.text((820, 638), "★★★★★ 9.98 / 10 RATING (84+ REVIEWS)", font=f_badge, fill=(255, 229, 0, 255))

    # 7. Play Indicator Circle on the right
    cx, cy = 1140, 260
    draw.ellipse([cx - 55, cy - 55, cx + 55, cy + 55], fill=(255, 85, 0, 220), outline=(255, 255, 255, 180), width=3)
    # Triangle play icon
    draw.polygon([(cx - 15, cy - 25), (cx - 15, cy + 25), (cx + 25, cy)], fill=(255, 255, 255, 255))

    # Convert to RGB and save as WebP
    rgb = base.convert("RGB")
    rgb.save(out_path, "WEBP", quality=88)

if __name__ == "__main__":
    test_out = THUMBS_DIR / "test_thumb.webp"
    create_bespoke_thumbnail(
        "Why Your CCTV Cameras Keep Disconnecting at Night — 7 Real Causes",
        1,
        "CCTV Installation & Troubleshooting",
        test_out,
        0
    )
    print(f"Test thumbnail created: {test_out} ({test_out.stat().st_size} bytes)")
