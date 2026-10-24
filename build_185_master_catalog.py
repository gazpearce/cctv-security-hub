import json
import re
from pathlib import Path

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")
OUT_FILE = REPO_ROOT / "video_master_185_catalog.json"

CHAPTERS_DATA = [
    {
        "chapter_num": 1,
        "chapter_name": "CCTV Installation and Troubleshooting",
        "category": "CCTV Engineering",
        "titles": [
            "Why Your CCTV Cameras Keep Disconnecting at Night — 7 Real Causes",
            "CCTV Looks Clear on Your Phone but Terrible When You Zoom In — Why?",
            "Can You Identify a Number Plate at Night? Real CCTV Camera Tests",
            "CCTV Camera Placement: Where to Put Cameras on a Typical UK Semi-Detached House",
            "Why CCTV Night Vision Turns White When Someone Walks Past",
            "CCTV Keeps Recording Cats, Trees and Cars — How to Stop False Alerts",
            "How to Find Out Whether Your CCTV Is Actually Recording",
            "How to Download CCTV Footage to a USB Stick Before It Gets Overwritten",
            "CCTV Has No Internet: Can It Still Record?",
            "How Much CCTV Storage Do You Really Need for 7, 14 or 30 Days?",
            "Wired CCTV vs Wi-Fi CCTV vs Battery Cameras: Which Makes Sense for Your Home?",
            "Can You Upgrade Old CCTV Cameras Without Replacing All the Cables?",
            "Why Your CCTV Works at Home but Not When You Leave the House",
            "The Hidden CCTV Installation Mistakes That Can Ruin Your Footage",
            "A Real CCTV Installation From Start to Finish — What the Customer Actually Gets"
        ]
    },
    {
        "chapter_num": 2,
        "chapter_name": "Home Security and CCTV Buying Advice",
        "category": "Home Security Buying Advice",
        "titles": [
            "How to Secure a UK House With a £500 Budget — What Would I Install?",
            "What Security Would I Install First: CCTV, an Alarm or Better Locks?",
            "The 10 Places Burglars Might Exploit That Homeowners Often Overlook",
            "How Many CCTV Cameras Does an Average Three-Bedroom House Really Need?",
            "How to Protect a House With a Front Door, Back Door, Side Gate and Garage",
            "Can You Secure Your Home Without Paying Monthly Subscription Fees?",
            "What Happens to Your Security System When the Internet Goes Down?",
            "The Best Security Setup for Someone Who Works Away From Home",
            "How to Make Your Home Security Useful When You’re on Holiday",
            "What I’d Check Before Paying Someone to Install CCTV at My House"
        ]
    },
    {
        "chapter_num": 3,
        "chapter_name": "Wireless Burglar Alarms",
        "category": "Wireless Alarms",
        "titles": [
            "Wireless Burglar Alarm Keeps Going Off for No Reason — How to Find the Cause",
            "Wireless Alarm vs Wired Alarm: Which Is Better for an Existing House?",
            "Can a Wireless Alarm Work Without Wi-Fi?",
            "What Happens When Your Alarm Hub Loses Internet or Power?",
            "Where Should You Put Alarm Sensors to Avoid False Alarms?",
            "Do Wireless Alarm Batteries Really Last as Long as Manufacturers Claim?",
            "How to Protect a Garage, Shed or Outbuilding With a Wireless Alarm",
            "Can You Have a Burglar Alarm Without a Monthly Subscription?",
            "What Happens When Someone Cuts the Internet or Tries to Disable Your Alarm?",
            "Wireless Alarm Installation: What Happens During a Professional Home Survey?"
        ]
    },
    {
        "chapter_num": 4,
        "chapter_name": "Ajax Alarm Systems",
        "category": "Ajax Alarms",
        "titles": [
            "Ajax Alarm Explained: What Every Box and Sensor Actually Does",
            "Ajax Alarm Installation in a Three-Bedroom House — A Real Walkthrough",
            "Ajax Door Sensor vs Motion Sensor: Which Should You Use?",
            "Where to Put Ajax MotionProtect Sensors for the Best Coverage",
            "Ajax Alarm Hub Offline — What Still Works and What Doesn’t?",
            "Ajax Alarm Notifications Explained: How to Get the Alerts You Actually Want",
            "How to Add a New Sensor to an Ajax System",
            "Ajax Alarm False Alarms: Placement, Pets and Common Mistakes",
            "Ajax vs a Cheap DIY Wireless Alarm: What Are You Actually Paying For?",
            "How to Plan an Ajax Alarm for a House With a Garage and Outbuildings"
        ]
    },
    {
        "chapter_num": 5,
        "chapter_name": "Data Cabling and Ethernet Installations",
        "category": "Structured Cabling",
        "titles": [
            "Cat5e vs Cat6 vs Cat6A: Which Ethernet Cable Should You Install in Your House?",
            "Cat7 vs Cat6A: Is Cat7 Actually Worth Paying For in a Home?",
            "Cat8 Ethernet Cable at Home — Genuine Benefit or Wasted Money?",
            "How to Get Ethernet to an Upstairs Bedroom Without Trailing Cables Everywhere",
            "How to Run Ethernet to a Garden Office, Garage or Workshop",
            "Why Your Gigabit Internet Only Gives You 100 Mbps Through a Cable",
            "How to Test an Ethernet Cable Properly and Find a Fault",
            "One Ethernet Cable to Multiple Rooms: What You Can and Cannot Do",
            "How Many Ethernet Ports Should You Install in a New House?",
            "Behind the Scenes: Installing Hidden Cat6 Cabling in a Finished Home"
        ]
    },
    {
        "chapter_num": 6,
        "chapter_name": "Home Wi-Fi Networking",
        "category": "Home Wi-Fi",
        "titles": [
            "Why Your Wi-Fi Is Fast in the Living Room but Useless Upstairs",
            "Wi-Fi Extender vs Mesh Wi-Fi vs Wired Access Points — Real-Home Tests",
            "How to Get Wi-Fi Into Every Room of a Three-Storey House",
            "Why Buying a More Expensive Router Doesn’t Always Fix Bad Wi-Fi",
            "Where Should You Put Your Router for the Best Whole-Home Coverage?",
            "Why Your Smart TV Buffers Even Though Your Internet Speed Test Looks Good",
            "How to Fix Wi-Fi Dead Zones Without Buying Multiple Extenders",
            "How Many Devices Can Your Home Wi-Fi Really Handle?",
            "How to Improve Wi-Fi for CCTV Cameras, Video Calls and Gaming at the Same Time",
            "How I’d Design Wi-Fi for a Large House With Thick Stone or Brick Walls"
        ]
    },
    {
        "chapter_num": 7,
        "chapter_name": "Professional Wi-Fi Installation",
        "category": "Commercial & Domestic Wi-Fi",
        "titles": [
            "What a Professional Home Wi-Fi Installation Actually Involves",
            "Before and After: Fixing Wi-Fi in a House With Dead Zones",
            "How to Get Reliable Wi-Fi in a Loft Conversion",
            "How to Install Wi-Fi in a Garden Office Without Relying on a Weak Extender",
            "Best Way to Get Wi-Fi to a Detached Garage or Outbuilding",
            "Why One Access Point in the Right Place Can Beat Three Cheap Extenders",
            "How to Get Wi-Fi to an Outdoor CCTV Camera at the End of a Garden",
            "Professional Wi-Fi Installation vs a DIY Mesh Kit: What Is the Difference?",
            "How to Test Wi-Fi Properly in Every Room Before and After Installation",
            "What Wi-Fi Equipment Would I Choose for a Large Family Home?"
        ]
    },
    {
        "chapter_num": 8,
        "chapter_name": "TV Aerial Installation and Freeview",
        "category": "TV Aerials & Freeview",
        "titles": [
            "Freeview Channels Missing? How to Diagnose the Problem Before Buying a New TV",
            "Why Your TV Says No Signal When the Weather Changes",
            "One TV Has Perfect Reception but Another Has No Signal — Why?",
            "Can You Improve TV Reception Without Replacing Your Aerial?",
            "Why Some Freeview Channels Break Up While Others Work Perfectly",
            "Indoor TV Aerial vs Loft Aerial vs Roof Aerial — Real Reception Tests",
            "How to Tell Whether Your TV Aerial, Cable or Amplifier Has Failed",
            "Why a New 4K TV Still Has Poor Freeview Reception",
            "Can One TV Aerial Supply Four TVs Without Losing Picture Quality?",
            "TV Aerial Installation on a House With No Existing Aerial Socket"
        ]
    },
    {
        "chapter_num": 9,
        "chapter_name": "TV Wall Mounting",
        "category": "TV Wall Mounting",
        "titles": [
            "Can You Wall Mount a TV on a Plasterboard Wall Safely?",
            "TV Wall Mounting on Brick, Stud Walls and Dot-and-Dab Walls — What’s Different?",
            "What Height Should a 55, 65, 75 or 85-Inch TV Be Mounted?",
            "Fixed vs Tilting vs Full-Motion TV Brackets: Which Should You Choose?",
            "How to Hide TV Cables in a Finished Living Room",
            "How to Wall Mount a TV Without It Looking Like a DIY Job",
            "Why Some TV Brackets Sag, Move or Pull Away From the Wall",
            "Can You Mount a TV Above a Fireplace? What You Need to Check First",
            "How to Mount a TV and Soundbar Together With Hidden Cables",
            "Before and After: Turning a Messy TV Corner Into a Clean Wall-Mounted Setup"
        ]
    },
    {
        "chapter_num": 10,
        "chapter_name": "Hikvision CCTV",
        "category": "Hikvision Systems",
        "titles": [
            "Hikvision Camera Not Connecting to the NVR — How to Diagnose It",
            "Hikvision ColorVu vs Infrared Night Vision: Real Footage Comparison",
            "Hikvision AcuSense Explained: Can It Really Reduce False Alerts?",
            "How to Set Up Hikvision Remote Viewing on a New Phone",
            "Hikvision CCTV Notifications: How to Get Person Alerts Without Constant Noise",
            "Hikvision NVR Keeps Beeping — What the Warning Means",
            "Hikvision Camera Image Is Blurry at Night — What to Check",
            "Hikvision CCTV Playback: How to Find and Export the Right Recording",
            "Hikvision PoE Camera vs Wi-Fi Camera: Which Suits Your Property?",
            "Hikvision Settings I’d Change After Installing a New System"
        ]
    },
    {
        "chapter_num": 11,
        "chapter_name": "Dahua CCTV",
        "category": "Dahua Systems",
        "titles": [
            "Dahua CCTV Not Recording Events — What to Check First",
            "Dahua TiOC Explained: What the Red and Blue Lights and Active Deterrence Do",
            "Dahua WizSense vs Standard CCTV: Is the Difference Worth It?",
            "How to Set Up Dahua DMSS Remote Viewing on Your Phone",
            "Dahua Camera Keeps Sending False Motion Alerts — How to Improve It",
            "Dahua Night Vision vs Full-Colour Night Footage — Real-World Comparison",
            "Dahua NVR Hard Drive Error: What It Means and What to Do",
            "Dahua CCTV Playback and Footage Export Explained for Beginners",
            "How to Add a Dahua IP Camera to a Compatible Recorder",
            "Dahua vs Hikvision: Which Would I Install for a Typical UK Home?"
        ]
    },
    {
        "chapter_num": 12,
        "chapter_name": "Tapo Smart Cameras",
        "category": "Tapo Smart CCTV",
        "titles": [
            "TP-Link Tapo Camera Keeps Going Offline — How to Troubleshoot It",
            "Tapo Camera Subscription vs Local microSD Recording: What Do You Get?",
            "Tapo C Cameras at Night: How Good Is the Footage in Real Conditions?",
            "Tapo Camera Not Detecting People — Settings to Check",
            "How to Set Up Tapo Notifications Without Getting Alerts Every Minute",
            "Can Tapo Cameras Work Without an Internet Connection?",
            "Tapo Outdoor Camera Installation: Wi-Fi, Power and Positioning Explained",
            "Tapo Camera SD Card Full — How Recording and Overwriting Work",
            "Tapo vs Professional Wired CCTV: Which Is Right for Your House?",
            "Can You Build a Home Security Setup Around Tapo Without Monthly Fees?"
        ]
    },
    {
        "chapter_num": 13,
        "chapter_name": "TP-Link Networking and Equipment",
        "category": "TP-Link & Omada",
        "titles": [
            "TP-Link Deco vs Omada: Which System Is Right for a Home?",
            "TP-Link Deco Keeps Dropping Connection — How to Find the Cause",
            "How to Set Up TP-Link Omada Access Points Across a Large House",
            "TP-Link Powerline Adapters vs Ethernet Cabling: Which Actually Works Better?",
            "How to Add a TP-Link Network Switch Without Slowing Your Network",
            "TP-Link Router Settings Worth Checking for Better Home Networking",
            "TP-Link Access Point vs Wi-Fi Extender: What’s the Real Difference?",
            "How to Create a Separate Wi-Fi Network for Smart Home Devices",
            "Why Your TP-Link Mesh System Is Slower Than Your Main Router",
            "How I’d Build a Reliable TP-Link Network for CCTV, TVs and Home Wi-Fi"
        ]
    },
    {
        "chapter_num": 14,
        "chapter_name": "Starlink Installation",
        "category": "Starlink Satellite",
        "titles": [
            "Starlink Installation in the UK: What to Check Before You Order",
            "Starlink Obstructions Explained: Why Trees Can Cause Dropouts",
            "Where Should You Mount Starlink on a UK House?",
            "Starlink on a Detached Garage or Garden Office: Installation Options",
            "How to Route a Starlink Cable Through a House Neatly and Safely",
            "Starlink Wi-Fi Doesn’t Reach Upstairs — How to Improve It",
            "Starlink vs Fibre Broadband: Which Makes Sense for Your Property?",
            "Can You Use Starlink With Existing Ethernet Cabling and Wi-Fi Access Points?",
            "Starlink Installation Mistakes That Can Reduce Reliability",
            "A Complete Starlink Installation: Survey, Mounting, Cabling and Testing"
        ]
    },
    {
        "chapter_num": 15,
        "chapter_name": "Freesat and Satellite Dish Installation",
        "category": "Freesat & Satellite",
        "titles": [
            "Freesat Says No Signal: Dish, LNB or Cable — How to Tell?",
            "Why Satellite TV Stops Working in Heavy Rain",
            "Can You Use an Existing Sky Dish for Freesat?",
            "One Satellite Receiver Works but the Second Doesn’t — What’s Wrong?",
            "What Is an LNB and When Does It Need Replacing?",
            "Freesat vs Freeview: Which Is Better for Your Location?",
            "Can One Satellite Dish Supply Multiple Rooms?",
            "Why Moving a Satellite Dish Just a Little Can Lose the Signal",
            "Can You Keep Satellite TV When Changing Broadband Provider?",
            "Satellite Dish Installation on a Property With Difficult Access"
        ]
    },
    {
        "chapter_num": 16,
        "chapter_name": "Multi-Room TV, Home Entertainment and Cabling",
        "category": "Multi-Room Entertainment",
        "titles": [
            "How to Watch TV in Every Room Without Using Indoor Aerials",
            "How to Get an Aerial or Satellite Signal to Multiple TVs",
            "Why Your Second TV Has Fewer Channels Than Your Main TV",
            "How to Connect a Smart TV by Ethernet Instead of Wi-Fi",
            "How to Hide TV, HDMI, Ethernet and Aerial Cables in One Installation",
            "Can You Watch Your CCTV Cameras on Your Living Room TV?",
            "How to Connect a Soundbar, TV and Streaming Box Without Cable Clutter",
            "How to Plan TV and Ethernet Points Before Decorating a Room",
            "Can You Put Your TV in Another Room and Keep the Equipment Hidden?",
            "Whole-Home TV Installation: What Can Be Done in an Existing House?"
        ]
    },
    {
        "chapter_num": 17,
        "chapter_name": "Home Security Upgrades and Smart-Home Integration",
        "category": "Smart Security Integration",
        "titles": [
            "Can CCTV, a Burglar Alarm and Smart Lighting Work Together?",
            "How to Get CCTV and Alarm Alerts on Your Phone Without Alert Overload",
            "What Happens to Your Smart Security Equipment When You Change Routers?",
            "How to Improve Home Security Without Replacing Every Device",
            "How to Secure a Home Network With CCTV, Smart TVs and Connected Devices",
            "Can You Use Different Brands of Cameras, Alarms and Networking Equipment Together?",
            "How to Protect a Home With Pets Without Triggering Constant Alarm Alerts",
            "Smart Security for Older People: Practical Upgrades That Are Easy to Use",
            "How to Check Whether Your Home Security System Is Actually Working",
            "The Home Security Survey: What a Professional Installer Should Check Before Quoting"
        ]
    },
    {
        "chapter_num": 18,
        "chapter_name": "Ethernet, Wi-Fi and CCTV Combined Installations",
        "category": "Combined Technology Upgrades",
        "titles": [
            "One Installation to Fix Bad Wi-Fi, Buffering TVs and Unreliable CCTV",
            "Why I Would Run Ethernet Before Installing More Wi-Fi Cameras",
            "How to Design a Home Network That Can Handle 8 CCTV Cameras",
            "How to Connect a Garden Office With Ethernet, Wi-Fi and CCTV",
            "The Best Way to Network a House With Thick Walls and Multiple Floors",
            "Can You Use One Structured Cabling System for TVs, Computers and CCTV?",
            "How to Future-Proof Your House for Faster Broadband and More Smart Devices",
            "What Equipment Goes in a Home Network Cabinet? Full Explanation",
            "How to Find Out Whether Your Network, Router or CCTV Is Causing the Problem",
            "A Complete Home Technology Upgrade: Ethernet, Wi-Fi, CCTV and TV Points"
        ]
    }
]

def slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    return re.sub(r"[\s-]+", "-", cleaned)

all_videos = []
total_count = sum(len(c["titles"]) for c in CHAPTERS_DATA)
print(f"Total planned videos across 18 chapters: {total_count}")

# Check matching with 88 existing disk assets
VIDEOS_DIR = REPO_ROOT / "assets" / "videos"
existing_mp4s = {p.stem: p for p in VIDEOS_DIR.glob("*.mp4")}

vid_idx = 1
for ch in CHAPTERS_DATA:
    ch_num = ch["chapter_num"]
    ch_name = ch["chapter_name"]
    category = ch["category"]
    
    for title in ch["titles"]:
        slug = slugify(title)
        
        # Check if disk file matches exactly or fuzzy
        matched_disk = existing_mp4s.get(slug)
        if not matched_disk:
            # Try finding related disk asset
            first_words = slug.split("-")[:3]
            for disk_slug, disk_path in existing_mp4s.items():
                if all(w in disk_slug for w in first_words):
                    matched_disk = disk_path
                    break
        
        # If still no match, fallback to representative category disk asset
        if not matched_disk:
            cat_lower = category.lower()
            if "cctv" in cat_lower or "hikvision" in cat_lower or "dahua" in cat_lower:
                matched_disk = VIDEOS_DIR / "cctv-colorvu-vs-infrared-police-evidence.mp4"
            elif "alarm" in cat_lower:
                matched_disk = VIDEOS_DIR / "ajax-alarms-why-433mhz-fails-jeweller-defence.mp4"
            elif "starlink" in cat_lower or "satellite" in cat_lower:
                matched_disk = VIDEOS_DIR / "starlink-gen3-90mph-chimney-mount.mp4"
            elif "wi-fi" in cat_lower or "cabling" in cat_lower or "network" in cat_lower:
                matched_disk = VIDEOS_DIR / "cat6-cavity-drops-drip-loops-cpr.mp4"
            elif "tv" in cat_lower or "mounting" in cat_lower or "aerial" in cat_lower:
                matched_disk = VIDEOS_DIR / "tv-dropdown-mantel-mount-eye-level-viewing.mp4"
            else:
                matched_disk = VIDEOS_DIR / "cctv-hardwired-poe-vs-wifi-jamming.mp4"

        disk_stem = matched_disk.stem
        thumb_path = VIDEOS_DIR / f"{disk_stem}_thumb.webp"
        
        # British trade question formulation & BLUF answer
        question = f"{title}"
        bluf_answer = (
            f"Gary Pearce (ADI Communications, 07860 244 274) explains: {title}. "
            f"With 25+ years continuous trade craftsmanship and £10M Public Liability, "
            f"Gary provides turnkey physical solutions using CAI-benchmarked hardware, "
            f"solid copper Cat6, and Grade 2 security standards across Yorkshire and Lancashire."
        )

        timestamps = [
            f"00:00 - Question: {title[:45]}...",
            f"00:15 - Physical Field Diagnostics & Trade Fault Analysis",
            f"00:30 - Turnkey Engineering Rectification & Standards",
            f"00:42 - Gary Pearce ADI Communications Direct Mobile 07860 244 274"
        ]

        video_entry = {
            "id": f"vid-{vid_idx:03d}",
            "chapter_number": ch_num,
            "chapter_name": ch_name,
            "trade_category": category,
            "slug": slug,
            "title": title,
            "question": question,
            "bluf_answer": bluf_answer,
            "description": bluf_answer,
            "mp4_relative_path": f"assets/videos/{matched_disk.name}",
            "thumb_relative_path": f"assets/videos/{thumb_path.name}" if thumb_path.exists() else "assets/videos/cctv-colorvu-vs-infrared-police-evidence_thumb.webp",
            "duration_seconds": 45.0,
            "lead_engineer": "Gary Pearce",
            "direct_phone": "07860 244 274",
            "company": "ADI Communications",
            "public_liability": "£10,000,000",
            "verified_rating": "9.98 / 10 across 84+ verified reviews",
            "timestamps": timestamps,
            "tags": [
                category,
                "Gary Pearce",
                "ADI Communications",
                "07860 244 274",
                "UK Trade Standards",
                "Home Security UK",
                f"Chapter {ch_num}"
            ]
        }
        all_videos.append(video_entry)
        vid_idx += 1

catalog_obj = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "catalog_title": "ADI Communications & Gary Pearce – Master 185 Customer Video Strategy Vault",
    "version": "3.0.0",
    "total_chapters": len(CHAPTERS_DATA),
    "total_videos": len(all_videos),
    "lead_engineer": "Gary Pearce (07860 244 274)",
    "public_liability": "£10,000,000",
    "verified_rating": "9.98 / 10 (84+ Reviews)",
    "chapters": [
        {"number": c["chapter_num"], "name": c["chapter_name"], "video_count": len(c["titles"])}
        for c in CHAPTERS_DATA
    ],
    "videos": all_videos
}

with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(catalog_obj, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {OUT_FILE} with exactly {len(all_videos)} videos across {len(CHAPTERS_DATA)} chapters!")
