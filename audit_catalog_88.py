import os
import glob
import json
import re

videos_dir = r"C:\Users\Gary\github-cctv-seo\assets\videos"
mp4_files = sorted(glob.glob(os.path.join(videos_dir, "*.mp4")))
webp_files = sorted(glob.glob(os.path.join(videos_dir, "*_thumb.webp")))

print(f"Total MP4 files on disk: {len(mp4_files)}")
print(f"Total WebP thumbnails on disk: {len(webp_files)}")

# Load 50 catalog
with open("video_stack_50_catalog.json", "r", encoding="utf-8") as f:
    cat50_data = json.load(f)
cat50 = {v["slug"]: v for v in cat50_data.get("videos", [])}

# Parse produce_faq_multimedia.py
with open("produce_faq_multimedia.py", "r", encoding="utf-8") as f:
    content = f.read()

# Extract FAQ items from produce_faq_multimedia.py
# Look for blocks with "slug", "title", "category" or similar
faq_slugs = re.findall(r'"slug":\s*"([^"]+)"', content)
print(f"Unique slugs in produce_faq_multimedia: {len(set(faq_slugs))}")

# Check matching with disk
disk_slugs = [os.path.basename(f)[:-4] for f in mp4_files]
found_in_50 = [s for s in disk_slugs if s in cat50]
not_in_50 = [s for s in disk_slugs if s not in cat50]

print(f"Videos in 50 catalog: {len(found_in_50)}")
print(f"Videos outside 50 catalog: {len(not_in_50)}")
for s in not_in_50:
    in_faq = s in faq_slugs
    print(f"  - {s} (in produce_faq: {in_faq})")
