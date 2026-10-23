import os
import json
import glob

videos_dir = r"C:\Users\Gary\github-cctv-seo\assets\videos"
catalog_file = r"C:\Users\Gary\github-cctv-seo\video_stack_50_catalog.json"

mp4s = glob.glob(os.path.join(videos_dir, "*.mp4"))
webps = glob.glob(os.path.join(videos_dir, "*.webp"))
total_mp4_bytes = sum(os.path.getsize(f) for f in mp4s)
total_webp_bytes = sum(os.path.getsize(f) for f in webps)

print(f"Total MP4 files on disk: {len(mp4s)} ({total_mp4_bytes / (1024*1024):.2f} MB)")
print(f"Total WebP thumbnails on disk: {len(webps)} ({total_webp_bytes / (1024*1024):.2f} MB)")

with open(catalog_file, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

print(f"Total items in video catalog: {len(catalog.get('videos', []))}")
print("\nSample 15 Real Customer Question Titles from Catalog:")
for i, v in enumerate(catalog.get('videos', [])[:15], 1):
    print(f"{i:02d}. [{v.get('category')}] {v.get('title')} (Runtime: {v.get('duration_sec')}s)")
