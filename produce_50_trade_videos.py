#!/usr/bin/env python3
"""
produce_50_trade_videos.py
==========================
Autonomous Video Production & Rendering Pipeline for Gary Pearce / ADI Communications.
Produces 50 1080p MP4 engineering videos and 50 1600x900 WebP thumbnails using
FFmpeg 8.1.1, edge_tts (zero voice token spend, £0), and Pillow.

Author: Gary Pearce / ADI Communications
Repository: github-cctv-seo
"""

import os
import sys
import json
import time
import shutil
import asyncio
import argparse
import subprocess
from pathlib import Path

# Ensure UTF-8 console output on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from PIL import Image, ImageDraw, ImageFont, ImageOps

REPO_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = REPO_ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
VIDEOS_DIR = ASSETS_DIR / "videos"
CACHE_DIR = REPO_ROOT / ".cache" / "video_build"

VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

CATALOG_PATH = REPO_ROOT / "video_stack_50_catalog.json"

FONT_ARIAL_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_SEGOE_REG = "C:/Windows/Fonts/segoeui.ttf"
FONT_SEGOE_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_CONSOLA_BOLD = "C:/Windows/Fonts/consolab.ttf"


def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    """Load TrueType font or fallback to default if path missing."""
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def get_audio_duration(audio_path: Path) -> float:
    """Measure exact audio duration in seconds via ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


async def synthesize_voiceover(text: str, output_path: Path):
    """Synthesize voiceover audio using edge_tts with British voice en-GB-RyanNeural (£0 tokens)."""
    import edge_tts
    comm = edge_tts.Communicate(text, "en-GB-RyanNeural", rate="+0%")
    await comm.save(str(output_path))


def generate_thumbnail(img_path: Path, title: str, subtitle: str, category: str, output_path: Path):
    """
    Synthesize 1600x900 WebP thumbnail with:
    - Lanczos center crop of authentic photographic trade asset
    - Deep obsidian (#050508) gradient scrim ensuring AAA contrast
    - Orange telemetry beacon pill ('● 4K UK FIELD MASTERCLASS')
    - Category badge
    - Balanced Arial Bold title block with drop shadow
    - Technical standards subhead in peach (#FFA07A)
    - Gary Pearce trade credentials footer (07860 244 274, 9.98/10 rating, 0 Checkatrade)
    """
    base = Image.open(img_path).convert("RGBA")
    base = ImageOps.fit(base, (1600, 900), Image.Resampling.LANCZOS)

    scrim = Image.new("RGBA", (1600, 900), (0, 0, 0, 0))
    draw_scrim = ImageDraw.Draw(scrim)
    for y in range(900):
        for x in range(0, 1600, 20):
            alpha = int(min(235, max(40, 140 * (1 - x / 1600.0) + 120 * (y / 900.0))))
            draw_scrim.rectangle([x, y, x + 20, y + 1], fill=(5, 5, 8, alpha))
    base = Image.alpha_composite(base, scrim)
    draw = ImageDraw.Draw(base)

    f_title = get_font(FONT_ARIAL_BOLD, 44)
    f_sub = get_font(FONT_SEGOE_BOLD, 24)
    f_mono = get_font(FONT_CONSOLA_BOLD, 22)
    f_foot = get_font(FONT_SEGOE_REG, 22)
    f_foot_bold = get_font(FONT_SEGOE_BOLD, 22)

    # 1. Telemetry pill (top-left)
    draw.rounded_rectangle([80, 70, 520, 120], radius=12, fill=(5, 5, 8, 210), outline=(255, 85, 0, 220), width=2)
    draw.ellipse([100, 88, 114, 102], fill=(255, 85, 0, 255))
    draw.text((128, 83), "4K UK FIELD MASTERCLASS", font=f_mono, fill=(255, 255, 255, 240))

    # 2. Category badge (top-right)
    draw.rounded_rectangle([1140, 70, 1520, 120], radius=12, fill=(5, 5, 8, 190), outline=(255, 255, 255, 40), width=1)
    draw.text((1165, 84), category.upper()[:24], font=f_sub, fill=(255, 255, 255, 220))

    # 3. Title block (balanced 2 lines)
    words = title.upper().split()
    mid = len(words) // 2
    l1 = " ".join(words[:mid])
    l2 = " ".join(words[mid:])

    draw.text((82, 172), l1, font=f_title, fill=(0, 0, 0, 220))
    draw.text((80, 170), l1, font=f_title, fill=(255, 255, 255, 255))
    draw.text((82, 237), l2, font=f_title, fill=(0, 0, 0, 220))
    draw.text((80, 235), l2, font=f_title, fill=(255, 255, 255, 255))

    # 4. Technical standards subhead
    draw.text((80, 315), subtitle.upper()[:90], font=f_sub, fill=(255, 160, 122, 255))

    # 5. Gary Pearce trade footer card
    draw.rounded_rectangle([80, 780, 1520, 840], radius=14, fill=(5, 5, 8, 230), outline=(255, 255, 255, 40), width=1)
    draw.text((110, 795), "GARY PEARCE • ADI COMMUNICATIONS • 07860 244 274", font=f_foot_bold, fill=(255, 255, 255, 255))
    draw.text((1060, 796), "★★★★★ 9.98 / 10 • 84+ REVIEWS", font=f_foot, fill=(255, 160, 122, 255))

    base.convert("RGB").save(str(output_path), "WEBP", quality=85)


def generate_hud_overlay(title: str, category: str, output_path: Path):
    """
    Generate transparent 1920x1080 HUD overlay PNG with:
    - Top telemetry pill with pulsing amber beacon
    - Lower-third cybernetic obsidian glassmorphism card
    - Gary Pearce trade credentials and star rating
    """
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    f_title = get_font(FONT_ARIAL_BOLD, 28)
    f_sub = get_font(FONT_SEGOE_REG, 20)
    f_sub_bold = get_font(FONT_SEGOE_BOLD, 20)
    f_mono = get_font(FONT_CONSOLA_BOLD, 20)

    # Top telemetry pill
    draw.rounded_rectangle([80, 50, 480, 100], radius=10, fill=(5, 5, 8, 210), outline=(255, 85, 0, 220), width=2)
    draw.ellipse([98, 68, 112, 82], fill=(255, 85, 0, 255))
    draw.text((125, 65), "4K UK FIELD MASTERCLASS", font=f_mono, fill=(255, 255, 255, 240))

    # Lower-third HUD card
    draw.rounded_rectangle([80, 890, 1840, 1010], radius=12, fill=(5, 5, 8, 225), outline=(255, 255, 255, 30), width=1)
    draw.text((110, 910), title.upper()[:75], font=f_title, fill=(255, 255, 255, 255))
    draw.text((110, 955), "GARY PEARCE • ADI COMMUNICATIONS • 07860 244 274 • 25+ YRS EXPERIENCE", font=f_sub_bold, fill=(255, 160, 122, 255))
    draw.text((1480, 955), "★★★★★ 9.98 / 10 (84+ REVIEWS)", font=f_sub, fill=(255, 160, 122, 220))

    overlay.save(str(output_path))


def render_video(img_path: Path, hud_path: Path, audio_path: Path, duration: float, output_path: Path):
    """
    Execute FFmpeg 8.1.1 compositing filtergraph:
    - Pre-scale and crop single input image to 1920x1080 without -loop 1
    - Apply zoompan Ken Burns push (1.00x -> 1.08x) for exactly d_frames = int(duration * 30)
    - Overlay transparent Pillow HUD PNG
    - Overlay native audio waveform (showwaves) oscillating at [1540, 905]
    - Overlay dynamic progress bar (drawbox) sweeping along [80, 1006]
    - Encode to H.264 High Profile 1080p 30fps + AAC 48kHz stereo + faststart
    - Atomic write pattern via cache temp file
    """
    d_frames = int(duration * 30)
    temp_mp4 = CACHE_DIR / f"{output_path.stem}.tmp.mp4"

    filter_complex = (
        f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
        f"zoompan=z='min(zoom+0.0002,1.08)':d={d_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30[bg];"
        f"[2:a]showwaves=s=260x50:mode=line:colors=0xFF5500|0xFFA07A[wave];"
        f"[bg][1:v]overlay=0:0[v1];"
        f"[v1][wave]overlay=1540:905[v2];"
        f"[v2]drawbox=x=80:y=1006:w='(1760)*(t/{duration:.3f})':h=4:color=0xFF5500@1.0:t=fill[vfinal]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(img_path),
        "-i", str(hud_path),
        "-i", str(audio_path),
        "-filter_complex", filter_complex,
        "-map", "[vfinal]",
        "-map", "2:a",
        "-c:v", "libx264", "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p",
        "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-movflags", "+faststart",
        "-shortest",
        str(temp_mp4)
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg compositing failed for {output_path.name}:\n{res.stderr[-1000:]}")

    # Atomic move to final destination in assets/videos/
    if output_path.exists():
        output_path.unlink()
    shutil.move(str(temp_mp4), str(output_path))


async def process_video_item(v: dict, force: bool = False, dry_run: bool = False) -> dict:
    """Process a single video entry: audio synthesis, thumbnail, HUD overlay, and FFmpeg render."""
    vid_id = v["video_id"]
    slug = v["slug"]
    title = v["title"]
    category = v["trade_category"]
    script = v["script_narration"]
    standards = " • ".join(v.get("technical_standards", v.get("hardware_standards", [])))

    img_rel = v["matching_image_asset"]
    img_path = REPO_ROOT / img_rel
    if not img_path.exists():
        raise FileNotFoundError(f"Missing image asset for {vid_id}: {img_path}")

    thumb_path = REPO_ROOT / v.get("thumbnail_path", f"assets/videos/{slug}_thumb.webp")
    video_path = REPO_ROOT / v.get("video_path", f"assets/videos/{slug}.mp4")

    # Cache paths
    audio_path = CACHE_DIR / f"{slug}_audio.mp3"
    hud_path = CACHE_DIR / f"{slug}_hud.png"

    print(f"\n[{vid_id}] {title[:60]}...")
    print(f"  • Discipline: {category}")
    print(f"  • Image Asset: {img_rel}")

    if dry_run:
        print(f"  [DRY-RUN] Verified image asset exists ({img_path.stat().st_size} bytes)")
        print(f"  [DRY-RUN] Script word count: {len(script.split())} words")
        return {"video_id": vid_id, "status": "DRY_RUN_PASS"}

    t_start = time.time()

    # Step 1: Synthesize Audio
    if not audio_path.exists() or force:
        print("  • Synthesizing British voiceover via edge_tts (en-GB-RyanNeural)...")
        await synthesize_voiceover(script, audio_path)
    else:
        print("  • Using cached audio voiceover...")

    duration = get_audio_duration(audio_path)
    print(f"  • Audio Duration: {duration:.2f}s ({audio_path.stat().st_size} bytes)")

    # Step 2: Generate 1600x900 WebP Thumbnail
    if not thumb_path.exists() or force:
        print("  • Synthesizing 1600x900 WebP thumbnail with obsidian scrim...")
        generate_thumbnail(img_path, title, standards, category, thumb_path)
        print(f"  • Thumbnail ready: {thumb_path.name} ({thumb_path.stat().st_size} bytes)")
    else:
        print("  • Thumbnail already exists, skipping synthesis.")

    # Step 3: Generate 1920x1080 Transparent HUD Overlay
    if not hud_path.exists() or force:
        generate_hud_overlay(title, category, hud_path)

    # Step 4: Render 1080p MP4 Video with FFmpeg
    if not video_path.exists() or force:
        print(f"  • Rendering 1080p MP4 via FFmpeg 8.1.1 (zoompan + showwaves + drawbox)...")
        t_render = time.time()
        render_video(img_path, hud_path, audio_path, duration, video_path)
        t_render_elapsed = time.time() - t_render
        print(f"  • Video rendered in {t_render_elapsed:.2f}s: {video_path.name} ({video_path.stat().st_size} bytes)")
    else:
        print("  • Video file already exists, skipping render.")

    # Clean up temporary HUD PNG to keep disk tidy
    if hud_path.exists():
        hud_path.unlink()

    t_total = time.time() - t_start
    print(f"  [OK] {vid_id} complete in {t_total:.2f}s")

    return {
        "video_id": vid_id,
        "duration_sec": round(duration, 1),
        "video_size": video_path.stat().st_size,
        "thumb_size": thumb_path.stat().st_size,
        "status": "SUCCESS"
    }


async def main_async():
    parser = argparse.ArgumentParser(description="Produce 50 UK Trade Engineering Videos for Gary Pearce / ADI Communications.")
    parser.add_argument("--dry-run", action="store_true", help="Validate assets and manifest without rendering")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of videos to produce")
    parser.add_argument("--topic", type=str, default=None, help="Specific video_id (e.g. VID-001) or slug to produce")
    parser.add_argument("--force", action="store_true", help="Force re-rendering even if output exists")
    args = parser.parse_args()

    if not CATALOG_PATH.exists():
        print(f"Error: Catalog manifest missing at {CATALOG_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    videos = catalog_data.get("videos", [])
    print(f"Loaded {len(videos)} video definitions from {CATALOG_PATH.name}")

    if args.topic:
        target = args.topic.strip().lower()
        videos = [v for v in videos if v["video_id"].lower() == target or v["slug"].lower() == target]
        if not videos:
            print(f"Error: Topic '{args.topic}' not found in catalog", file=sys.stderr)
            sys.exit(1)

    if args.limit:
        videos = videos[:args.limit]

    print(f"Target execution count: {len(videos)} video(s)")
    if args.dry_run:
        print("[MODE: DRY-RUN ACTIVATED]")

    t_batch_start = time.time()
    results = []

    for i, v in enumerate(videos, 1):
        print(f"\n{'='*70}")
        print(f"PROGRESS: [{i}/{len(videos)}] ({int(i/len(videos)*100)}%)")
        print(f"{'='*70}")
        res = await process_video_item(v, force=args.force, dry_run=args.dry_run)
        results.append(res)

    t_batch_elapsed = time.time() - t_batch_start
    print(f"\n{'='*70}")
    print(f"BATCH PRODUCTION COMPLETE: {len(results)} items in {t_batch_elapsed:.2f}s")
    print(f"{'='*70}")

    # If not dry run, update catalog with precise durations
    if not args.dry_run and not args.topic and not args.limit:
        dur_map = {r["video_id"]: r["duration_sec"] for r in results if "duration_sec" in r}
        for v in catalog_data["videos"]:
            vid = v["video_id"]
            if vid in dur_map:
                v["duration_sec"] = dur_map[vid]
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog_data, f, indent=2, ensure_ascii=False)
        print("Synchronized catalog duration_sec fields with exact audio durations.")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
