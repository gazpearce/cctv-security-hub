#!/usr/bin/env python3
"""
render_viral_instagram_reels.py
===============================
Dedicated 9:16 Vertical (1080x1920) Viral Reel Production Engine for Gary Pearce / ADI Communications.
Encodes 2026 Instagram Reels algorithms, safe-zone engineering, and viral trade hook frameworks.

Author: Gary Pearce / ADI Communications
Repository: github-cctv-seo
"""

import os
import sys
import json
import time
import shutil
import asyncio
import subprocess
from pathlib import Path

# Ensure UTF-8 console output
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from PIL import Image, ImageDraw, ImageFont, ImageOps

REPO_ROOT = Path(__file__).resolve().parent
REELS_DIR = REPO_ROOT / "assets" / "reels"
CACHE_DIR = REPO_ROOT / ".cache" / "reels_build"

REELS_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

FONT_ARIAL_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_SEGOE_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_SEGOE_REG = "C:/Windows/Fonts/segoeui.ttf"
FONT_CONSOLA_BOLD = "C:/Windows/Fonts/consolab.ttf"


def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


# Curated 2026 Viral Trade Hook Campaigns for Instagram Reels (9:16 Vertical)
VIRAL_REELS_CAMPAIGNS = [
    {
        "id": "reel-01-stop-buying-cheap-wifi-cameras",
        "slug": "stop-buying-cheap-wifi-cctv-cameras",
        "category": "CCTV & Security Shock",
        "badge": "🚨 UK HOME SECURITY WARNING",
        "hook_line1": "STOP BUYING £30",
        "hook_line2": "WIRELESS CAMERAS!",
        "subtitle": "Why battery Wi-Fi cameras fail when an intruder arrives",
        "image_asset": "assets/images/cctv-hikvision-colorvu-vs-infrared-night-vision-comparison.webp",
        "script": (
            "Stop buying thirty pound wireless cameras from Amazon or TikTok shop. "
            "They are virtually useless when an actual burglary happens. "
            "First, burglars carry forty-pound Wi-Fi deauthers that knock wireless cameras completely offline in seconds. "
            "Second, their tiny batteries mean they sleep until motion happens, missing the first ten seconds of an intruder approach. "
            "And third, standard infrared night vision leaves the police with a useless white smudge instead of an identifiable face. "
            "Commercial hardwired Power-over-Ethernet cameras record twenty-four-seven to a secure local hard drive with zero monthly subscription fees. "
            "I'm Gary Pearce, Lead Engineer at ADI Communications with twenty-five years hands-on field experience. "
            "Call me directly on 07860 244 274 for certified trade advice across Yorkshire and Lancashire."
        ),
        "caption": (
            "🚨 STOP BUYING £30 WIRELESS CAMERAS!\n\n"
            "Here is the brutal truth every UK homeowner discovers too late: battery Wi-Fi cameras are easily defeated by cheap £40 handheld RF jammers and deauthers.\n\n"
            "Why commercial hardwired PoE CCTV wins every time:\n"
            "⚡ 100% immune to wireless jamming attacks\n"
            "⚡ 24/7 continuous local recording (zero monthly cloud subscriptions)\n"
            "⚡ Full-colour ColorVu nighttime facial identification (DORI standard compliant)\n"
            "⚡ Fitted with solid copper Cat6 cabling and waterproof drip loops\n\n"
            "Direct Trade Engineering by Gary Pearce, ADI Communications (25+ yrs experience, £10M Public Liability).\n"
            "📞 Call Gary Direct: 07860 244 274\n\n"
            "#CCTVInstallation #HomeSecurityUK #Hikvision #CrimePrevention #YorkshireTrades #SecurityInstaller #Leeds #Bradford #GaryPearce #PoECCTV"
        )
    },
    {
        "id": "reel-02-pov-cheapest-guy-on-facebook",
        "slug": "pov-cheapest-cctv-installer-facebook",
        "category": "Tradesman Reality",
        "badge": "⚡ TRADESMAN REALITY CHECK",
        "hook_line1": "POV: YOU HIRED THE",
        "hook_line2": "CHEAPEST GUY ON FB...",
        "subtitle": "Tangled unshielded cables vs laser-straight conduit",
        "image_asset": "assets/images/cctv-masonry-junction-box-mounting-accrington.webp",
        "script": (
            "POV: You hired the cheapest guy on Facebook to install your security cameras. "
            "They drill through your cavity walls without drip loops, dangle cheap copper-clad aluminium cables across your gutters, and leave vulnerable junction boxes exposed to rain rot. "
            "Six months later, water tracks into your plasterwork, cameras short out, and the installer's number is disconnected. "
            "Proper trade installation means UV-rated external solid copper Cat6, precision gritstone masonry anchors, IP67 sealed junction boxes, and ten million pounds of public liability insurance. "
            "I'm Gary Pearce, Lead Engineer at ADI Communications. With twenty-five years of Yorkshire trade craftsmanship, do the job right the first time. "
            "Call 07860 244 274."
        ),
        "caption": (
            "⚡ POV: You hired the cheapest guy on Facebook to install your CCTV...\n\n"
            "Cheap installs end up costing double. Here's what we find on rescue callouts:\n"
            "❌ No drip loops (water drains straight into cavity wall insulation)\n"
            "❌ Cheap CCA (copper-clad aluminium) that snaps and drops voltage\n"
            "❌ Unsealed junction boxes causing short circuits\n"
            "❌ Zero public liability insurance\n\n"
            "Do it once, do it right with ADI Communications.\n"
            "📞 Direct Mobile: 07860 244 274\n\n"
            "#TradesmanLife #CCTVFail #DIYFails #SecurityInstaller #YorkshireBusiness #ElectricalTrades #CCTVUK #GaryPearce"
        )
    },
    {
        "id": "reel-03-the-30-pound-alarm-jammer",
        "slug": "burglars-30-pound-alarm-jammer-trick",
        "category": "Intruder Alert",
        "badge": "⚠️ BURGLARY VULNERABILITY ALERT",
        "hook_line1": "THE £30 GADGET",
        "hook_line2": "SILENCING ALARMS!",
        "subtitle": "Why legacy 433MHz sirens fail vs Ajax Jeweller 868MHz",
        "image_asset": "assets/images/ajax-alarms-why-433mhz-fails-jeweller-defence.webp",
        "script": (
            "This is the thirty-pound radio frequency jammer that burglars are using to silence standard wireless burglar alarms. "
            "Legacy DIY alarm systems communicate on basic 433-megahertz frequencies. "
            "A pocket jammer floods the radio spectrum, blinding the sensors so the siren never sounds. "
            "That is why British homeowners are upgrading to Ajax Grade 2 Jeweller smart alarms. "
            "Ajax uses encrypted 868-megahertz multi-channel frequency hopping. "
            "If an intruder attempts to jam the frequency, the hub detects it in milliseconds, triggers the external 113-decibel sounder, and sends photo verification directly to your smartphone. "
            "I'm Gary Pearce at ADI Communications. Call me on 07860 244 274 for certified alarm installation."
        ),
        "caption": (
            "⚠️ THE £30 GADGET SILENCING CHEAP ALARMS IN 2026!\n\n"
            "Did you know legacy 433MHz DIY alarms can be blinded in seconds by basic handheld RF jammers?\n\n"
            "How Ajax Grade 2 Jeweller Defends Your Home:\n"
            "🛡️ 868MHz encrypted rolling-code frequency hopping\n"
            "🛡️ Sub-second jamming detection that triggers 113dB StreetSiren immediately\n"
            "🛡️ MotionCam PhOD photo-verification sent to your phone in 9 seconds\n"
            "🛡️ Dual 4G SIM cellular failover even if your home Wi-Fi is cut\n\n"
            "Installed by Gary Pearce, ADI Communications (25+ yrs experience, £10M Public Liability).\n"
            "📞 Direct Line: 07860 244 274\n\n"
            "#AjaxAlarms #SmartAlarms #HomeSecurityTips #BurglaryPrevention #AlarmInstaller #YorkshireHomes #SmartHomeUK"
        )
    },
    {
        "id": "reel-04-stop-drilling-chimney-starlink",
        "slug": "stop-drilling-chimneys-starlink-mount",
        "category": "Satellite Engineering",
        "badge": "🛰️ 90MPH HIGH-WIND RATED",
        "hook_line1": "STOP DRILLING INTO",
        "hook_line2": "CHIMNEY BRICKWORK!",
        "subtitle": "Non-drill stainless lashing cradles vs 90mph gales",
        "image_asset": "assets/images/starlink-gen3-chimney-mount-vs-gable-apex-engineering-uk.webp",
        "script": (
            "Stop drilling heavy expansion bolts into old chimney brickwork for your Starlink dish. "
            "Drilling into century-old lime mortar cracks brick courses, invites water leaks into your roof space, and leads to costly structural repairs. "
            "Instead, we install tensioned stainless-steel chimney lashing cradles. "
            "This spreads the wind load evenly around the chimney stack without drilling a single hole in your brickwork. "
            "Fitted with heavy-duty galvanized heavy-duty Starlink chimney brackets, it survives ninety-mile-an-hour gales without dish wobble or satellite dropouts. "
            "We pair it with external UV-rated Cat6 and weatherproof drip loops. "
            "I'm Gary Pearce, Lead Engineer at ADI Communications. For certified Starlink installation across Yorkshire, call 07860 244 274."
        ),
        "caption": (
            "🛰️ STOP DRILLING HOLES INTO YOUR CHIMNEY FOR STARLINK!\n\n"
            "Drilling rawlbolts into vintage chimney brickwork causes mortar blowouts and roof leaks during Pennine winter storms.\n\n"
            "The Certified Non-Drill Method:\n"
            "✅ Stainless tensioned wire lashing cradle (0 holes drilled into masonry)\n"
            "✅ Galvanized Pennine 90mph storm brackets to prevent dish micro-wobble\n"
            "✅ Clean UV-resistant Cat6 exterior cable run with weatherproof drip loops\n"
            "✅ Wi-Fi 7 mesh router bypass for whole-property coverage\n\n"
            "Fitted by Gary Pearce, ADI Communications (25+ yrs field experience).\n"
            "📞 Direct Mobile: 07860 244 274\n\n"
            "#StarlinkUK #StarlinkInstallation #RuralBroadband #BroadbandInstaller #YorkshireTrades #EngineeringUK #GaryPearce"
        )
    }
]


async def synthesize_voiceover(text: str, output_path: Path):
    """Synthesize voiceover using British voice en-GB-RyanNeural (£0 tokens)."""
    import edge_tts
    comm = edge_tts.Communicate(text, "en-GB-RyanNeural", rate="+3%")
    await comm.save(str(output_path))


def generate_vertical_hud_overlay(campaign: dict, output_path: Path):
    """
    Generate 1080x1920 vertical HUD overlay respecting Instagram Reels safe-zones:
    - Top exclusion: Y=0 to 220
    - Bottom exclusion: Y=1580 to 1920
    - All text strictly within Y=280 to Y=1550!
    """
    overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    f_badge = get_font(FONT_CONSOLA_BOLD, 28)
    f_hook = get_font(FONT_ARIAL_BOLD, 62)
    f_sub = get_font(FONT_SEGOE_BOLD, 28)
    f_card_title = get_font(FONT_ARIAL_BOLD, 30)
    f_card_sub = get_font(FONT_SEGOE_BOLD, 24)
    f_card_stars = get_font(FONT_SEGOE_BOLD, 22)

    # 1. Top Scrim & Pattern Interrupt Pill (Y = 280)
    draw.rounded_rectangle([60, 270, 1020, 340], radius=16, fill=(5, 5, 8, 235), outline=(255, 85, 0, 240), width=3)
    draw.ellipse([85, 293, 105, 313], fill=(255, 85, 0, 255))
    draw.text((120, 288), campaign["badge"], font=f_badge, fill=(255, 255, 255, 255))

    # 2. Massive Bold Yellow Viral Hook Headline (Y = 370 to 520)
    # Background card for extreme contrast
    draw.rounded_rectangle([60, 360, 1020, 560], radius=20, fill=(5, 5, 8, 230), outline=(255, 255, 255, 40), width=2)
    
    # Line 1 (Yellow)
    draw.text((84, 384), campaign["hook_line1"], font=f_hook, fill=(0, 0, 0, 240))
    draw.text((80, 380), campaign["hook_line1"], font=f_hook, fill=(255, 229, 0, 255))

    # Line 2 (White)
    draw.text((84, 464), campaign["hook_line2"], font=f_hook, fill=(0, 0, 0, 240))
    draw.text((80, 460), campaign["hook_line2"], font=f_hook, fill=(255, 255, 255, 255))

    # Subtitle Pill
    draw.rounded_rectangle([60, 580, 1020, 635], radius=12, fill=(255, 85, 0, 230))
    draw.text((85, 592), campaign["subtitle"].upper()[:52], font=f_sub, fill=(255, 255, 255, 255))

    # 3. Lower-Third Trade Authority Glassmorphism Card (Y = 1320 to 1540)
    draw.rounded_rectangle([60, 1310, 1020, 1530], radius=20, fill=(5, 5, 8, 240), outline=(255, 255, 255, 50), width=2)
    
    # Gary Pearce identity
    draw.text((90, 1335), "GARY PEARCE • ADI COMMUNICATIONS", font=f_card_title, fill=(255, 255, 255, 255))
    draw.text((90, 1380), "📞 DIRECT MOBILE: 07860 244 274 • 25+ YRS CRAFTSMANSHIP", font=f_card_sub, fill=(255, 160, 122, 255))
    draw.text((90, 1425), "£10M PUBLIC LIABILITY • SOLID COPPER & CAI BENCHMARKED", font=f_card_stars, fill=(200, 200, 200, 255))
    draw.text((90, 1470), "★★★★★ 9.98 / 10 RATING (84+ VERIFIED CLIENT REVIEWS)", font=f_card_stars, fill=(255, 229, 0, 255))

    overlay.save(str(output_path))


def render_vertical_reel(img_path: Path, hud_path: Path, audio_path: Path, duration: float, output_path: Path):
    """
    Render 1080x1920 vertical MP4 using FFmpeg 8.1.1:
    - Scales authentic trade photo to 1080x1920 center-crop
    - Applies subtle Ken Burns zoompan
    - Overlays Pillow 9:16 safe-zone HUD
    - Overlays live audio waveform inside the safe zone (Y = 1240)
    - Sweeping orange progress line (Y = 1535)
    """
    d_frames = int(duration * 30)
    temp_mp4 = CACHE_DIR / f"{output_path.stem}.tmp.mp4"

    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"zoompan=z='min(zoom+0.0003,1.10)':d={d_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30[bg];"
        f"[2:a]showwaves=s=320x50:mode=line:colors=0xFF5500|0xFFE500[wave];"
        f"[bg][1:v]overlay=0:0[v1];"
        f"[v1][wave]overlay=680:1240[v2];"
        f"[v2]drawbox=x=60:y=1535:w='(960)*(t/{duration:.3f})':h=5:color=0xFF5500@1.0:t=fill[vfinal]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(img_path),
        "-i", str(hud_path),
        "-i", str(audio_path),
        "-filter_complex", filter_complex,
        "-map", "[vfinal]",
        "-map", "2:a",
        "-c:v", "libx264", "-profile:v", "high", "-level", "4.2", "-pix_fmt", "yuv420p",
        "-preset", "fast", "-crf", "21",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-movflags", "+faststart",
        "-shortest",
        str(temp_mp4)
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg vertical compositing failed:\n{res.stderr[-1000:]}")

    if output_path.exists():
        output_path.unlink()
    shutil.move(str(temp_mp4), str(output_path))


async def process_campaign(c: dict) -> dict:
    slug = c["slug"]
    print(f"\n=======================================================")
    print(f"PRODUCING 9:16 VIRAL REEL: {c['hook_line1']} {c['hook_line2']}")
    print(f"Category: {c['category']}")
    print(f"=======================================================")

    img_path = REPO_ROOT / c["image_asset"]
    if not img_path.exists():
        raise FileNotFoundError(f"Missing image asset: {img_path}")

    audio_path = CACHE_DIR / f"{slug}_audio.mp3"
    hud_path = CACHE_DIR / f"{slug}_vertical_hud.png"
    mp4_out = REELS_DIR / f"{slug}.mp4"
    thumb_out = REELS_DIR / f"{slug}_vertical_thumb.webp"

    # 1. Synthesize Audio
    if not audio_path.exists():
        print("  • Synthesizing British voiceover via edge_tts (en-GB-RyanNeural)...")
        await synthesize_voiceover(c["script"], audio_path)

    # Measure exact duration
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    duration = float(res.stdout.strip())
    print(f"  • Audio Duration: {duration:.2f} seconds")

    # 2. Generate Vertical HUD Overlay
    print("  • Generating 9:16 safe-zone vertical HUD overlay...")
    generate_vertical_hud_overlay(c, hud_path)

    # 3. Render 1080x1920 MP4 Reel
    print("  • Rendering 1080x1920 vertical H.264 MP4 via FFmpeg...")
    render_vertical_reel(img_path, hud_path, audio_path, duration, mp4_out)

    # 4. Generate 1080x1920 Vertical Poster Thumbnail
    print("  • Generating 1080x1920 WebP vertical poster thumbnail...")
    base = Image.open(img_path).convert("RGBA")
    base = ImageOps.fit(base, (1080, 1920), Image.Resampling.LANCZOS)
    hud = Image.open(hud_path).convert("RGBA")
    base = Image.alpha_composite(base, hud)
    base.convert("RGB").save(str(thumb_out), "WEBP", quality=85)

    size_mb = mp4_out.stat().st_size / (1024 * 1024)
    print(f"  ✅ SUCCESS: {mp4_out.name} ({size_mb:.2f} MB, {duration:.1f}s)")

    return {
        "id": c["id"],
        "slug": slug,
        "video_path": str(mp4_out),
        "thumb_path": str(thumb_out),
        "duration_sec": duration,
        "caption": c["caption"]
    }


async def main():
    results = []
    for c in VIRAL_REELS_CAMPAIGNS:
        res = await process_campaign(c)
        results.append(res)

    manifest_path = REELS_DIR / "viral_reels_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n[DONE] All {len(results)} viral 9:16 vertical reels produced and indexed in {manifest_path}!")


if __name__ == "__main__":
    asyncio.run(main())
