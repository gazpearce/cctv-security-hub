import os
import json
from pathlib import Path

REPO_ROOT = Path("C:/Users/Gary/github-cctv-seo")
REGISTRY_PATH = REPO_ROOT / "used_media_registry.json"
IMAGES_DIR = REPO_ROOT / "assets" / "images"

# Initial known used images from previous posts/reels
INITIAL_USED = [
    "cctv-hikvision-colorvu-vs-infrared-night-vision-comparison.webp",
    "cctv-masonry-junction-box-mounting-accrington.webp",
    "ajax-alarms-why-433mhz-fails-jeweller-defence.webp",
    "starlink-gen3-chimney-mount-vs-gable-apex-engineering-uk.webp",
    "cctv-camera-outdoor-weatherproof-blackburn.webp",
    "ajax-hub2-central-panel-whitebirk.webp",
    "starlink-dish-mounting-bracket-darwen.webp"
]

def init_registry():
    if not REGISTRY_PATH.exists():
        data = {
            "version": "1.0",
            "last_updated": "",
            "used_images": INITIAL_USED,
            "posts_log": []
        }
    else:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            for img in INITIAL_USED:
                if img not in data["used_images"]:
                    data["used_images"].append(img)
    
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Registry initialized with {len(data['used_images'])} recorded images.")

def get_next_unused_image(category_filter=None):
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    used_set = set(data.get("used_images", []))
    all_files = [f for f in os.listdir(IMAGES_DIR) if f.endswith(('.webp', '.jpg', '.png')) and not f.endswith('_exif.jpg')]
    
    candidates = [f for f in all_files if f not in used_set]
    if category_filter:
        filtered = [f for f in candidates if category_filter.lower() in f.lower()]
        if filtered:
            candidates = filtered
            
    if not candidates:
        raise RuntimeError("No unused images left in pool!")
        
    chosen = candidates[0]
    return chosen

def mark_image_used(image_filename, campaign_id, platform):
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if image_filename not in data["used_images"]:
        data["used_images"].append(image_filename)
    data["posts_log"].append({
        "timestamp": os.path.getmtime(IMAGES_DIR / image_filename) if (IMAGES_DIR / image_filename).exists() else None,
        "image": image_filename,
        "campaign_id": campaign_id,
        "platform": platform
    })
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Marked {image_filename} as used for {platform} ({campaign_id}).")

if __name__ == "__main__":
    init_registry()
    img = get_next_unused_image("wifi")
    print(f"Next unused Wi-Fi image: {img}")
    img_cctv = get_next_unused_image("cctv")
    print(f"Next unused CCTV image: {img_cctv}")
