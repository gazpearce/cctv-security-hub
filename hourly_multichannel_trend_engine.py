#!/usr/bin/env python3
"""
hourly_multichannel_trend_engine.py
===================================
Master 2026 Autonomous Social Trend & Video Publishing Engine for Gary Pearce / ADI Communications.
Coordinates hourly production & publishing across Instagram Reels, Meta Threads, and TikTok
with 100% unique imagery (ZERO reuse), £0 voice token cost (Rule 28), and Rule 45 Google Shield compliance.

Direct Mobile: 07860 244 274 • 25+ Years Hands-on Craftsmanship
"""

import os
import sys
import json
import time
import asyncio
import subprocess
import urllib.request
import websockets
import base64
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

REPO_ROOT = Path(__file__).resolve().parent
REELS_DIR = REPO_ROOT / "assets" / "reels"
CACHE_DIR = REPO_ROOT / ".cache" / "hourly_reels"
AUDIT_LOG = REPO_ROOT / "hourly_trend_audit.json"
REGISTRY_SCRIPT = REPO_ROOT / "media_registry.py"

REELS_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

from PIL import Image, ImageDraw, ImageFont
import media_registry

FONT_ARIAL_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_SEGOE_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_CONSOLA_BOLD = "C:/Windows/Fonts/consolab.ttf"

def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

# 14 Curated High-Intent Customer Pain-Point Campaigns for Today (09:00 - 22:00)
HOURLY_CAMPAIGNS = [
    {
        "hour": 9,
        "id": "cctv-night-vision-glare",
        "category": "cctv",
        "topic": "Why CCTV Night Vision Looks Terrible",
        "badge": "🚨 NIGHT VISION TRAP",
        "hook_line1": "WHY CCTV NIGHT",
        "hook_line2": "LOOKS LIKE MUD!",
        "subtitle": "Infrared glare & spiderwebs vs ColorVu 24/7",
        "script": (
            "Why does your CCTV footage look clear during the day but like blurry mud at night? "
            "First, cheap cameras use basic infrared LEDs. When someone walks past, the glare bounces off their face, washing out all identification. "
            "Second, spiders love warm infrared rings, spinning webs that blind the lens with white reflections. "
            "Commercial Hikvision ColorVu cameras don't use blinding infrared. "
            "They use advanced F1.0 super-apertures that capture crisp full-colour facial details in near total darkness. "
            "I'm Gary Pearce at ADI Communications with twenty-five years hands-on field experience. "
            "Call me directly on 07860 244 274 for certified trade advice."
        ),
        "ig_caption": (
            "🚨 WHY CCTV NIGHT VISION LOOKS LIKE MUD!\n\n"
            "Here's why standard infrared cameras fail British homeowners:\n"
            "❌ IR overexposure: white glare washes out intruder faces\n"
            "❌ Spiders build webs directly over hot IR ring lights\n"
            "❌ Black and white footage cannot prove clothing color in court\n\n"
            "Upgrade to Hikvision ColorVu 24/7 full-colour CCTV.\n"
            "📞 Call Gary Direct: 07860 244 274\n\n"
            "#CCTVInstallation #NightVision #HikvisionColorVu #HomeSecurityUK #CrimePrevention #YorkshireTrades #GaryPearce"
        ),
        "threads_post": (
            "Quick question for UK homeowners:\n\n"
            "Why do so many CCTV cameras show clear pictures at noon, but turn into a useless white blur the moment someone walks past at midnight?\n\n"
            "Infrared glare and spiderwebs ruin 70% of night footage. F1.0 ColorVu sensors capture full-colour faces with £0 cloud fees.\n\n"
            "Have you ever checked your night vision?"
        ),
        "tiktok_tags": "#CCTVInstallation #HomeSecurityUK #Hikvision #NightVision #Yorkshire #Tradesman #CrimePrevention"
    },
    {
        "hour": 10,
        "id": "wifi-dead-spots-stone-walls",
        "category": "cat6",
        "topic": "Why Wi-Fi Mesh Fails Through Thick Walls",
        "badge": "📶 WI-FI SPEED MYTH",
        "hook_line1": "WHY MESH WI-FI",
        "hook_line2": "FAILS STONE WALLS!",
        "subtitle": "Why wireless repeaters drop 80% speed",
        "script": (
            "Why does your expensive mesh Wi-Fi system still drop signal in your kitchen or attic? "
            "Here is the physics: fifty-centimetre Yorkshire gritstone and foil-backed insulation absorb high-frequency five-gigahertz Wi-Fi like a brick wall. "
            "Every wireless mesh hop cuts your bandwidth in half. "
            "The permanent trade fix is a discreet external solid copper Cat6 backbone with hardwired ceiling access points. "
            "You get full gigabit speeds in every single room with zero lag. "
            "I'm Gary Pearce, Lead Engineer at ADI Communications. "
            "Call 07860 244 274 for professional data cabling."
        ),
        "ig_caption": (
            "📶 WHY MESH WI-FI FAILS IN UK HOMES!\n\n"
            "Foil-backed insulation, cavity walls, and stone fireplaces destroy wireless signals.\n"
            "⚡ Wireless repeaters cut your speed by 50% per hop\n"
            "⚡ Hardwired Cat6 backbones deliver 100% full broadband speed to every corner\n"
            "⚡ Discrete routing along exterior mortar lines with weatherproof drip loops\n\n"
            "Fitted by Gary Pearce, ADI Communications (07860 244 274).\n\n"
            "#WiFiMesh #DataCabling #Cat6 #HomeNetworking #BroadbandUK #YorkshireHomes #SmartHomeUK"
        ),
        "threads_post": (
            "Home networking reality check:\n\n"
            "Why spend £300 on wireless mesh pods when solid stone walls and foil plasterboard kill the signal before it reaches the back bedroom?\n\n"
            "A single discrete hardwired Cat6 cable with a ceiling access point gives 100% full speed with zero dropouts.\n\n"
            "What's your biggest Wi-Fi blackspot at home?"
        ),
        "tiktok_tags": "#WiFi #HomeNetworking #Cat6 #Broadband #Tradesman #Yorkshire #SmartHome"
    },
    {
        "hour": 11,
        "id": "tv-wall-mount-hollow-stud",
        "category": "tv",
        "topic": "Can You Mount An 85-Inch TV On Plasterboard?",
        "badge": "📺 TV MOUNTING TRUTH",
        "hook_line1": "CAN YOU MOUNT 85\"",
        "hook_line2": "ON PLASTERBOARD?",
        "subtitle": "GripIt anchors & timber studs vs disaster",
        "script": (
            "Can you safely mount a heavy eighty-five inch OLED TV on a hollow plasterboard stud wall? "
            "The short answer is yes, but only if you use certified heavy-duty hollow-wall anchors and locate the internal timber studs. "
            "Cheap plastic rawl plugs will pull straight out of drywall under dynamic cantilever weight, destroying your five-thousand-pound TV. "
            "We use laser levels, magnetic stud finders, heavy-gauge steel brackets, and conceal all power and HDMI cables inside the wall cavity. "
            "I'm Gary Pearce at ADI Communications. Call 07860 244 274."
        ),
        "ig_caption": (
            "📺 CAN YOU MOUNT AN 85\" TV ON HOLLOW DRYWALL?\n\n"
            "Yes, but never with standard plastic plugs! Here's how we secure large TVs safely:\n"
            "✔ Precision timber stud anchoring\n"
            "✔ Heavy-duty steel cantilever tilt brackets\n"
            "✔ Internal cavity cable routing (zero unsightly wires)\n"
            "✔ Laser-level alignment\n\n"
            "Installed by Gary Pearce, ADI Communications (07860 244 274).\n\n"
            "#TVWallMounting #OLED #HomeCinema #InteriorDesignUK #YorkshireTrades #GaryPearce"
        ),
        "threads_post": (
            "Trade question for TV lovers:\n\n"
            "Would you trust standard drywall anchors to hold a £2,500 77-inch OLED TV on a hollow stud wall?\n\n"
            "We see DIY horror stories every month where brackets pulled out of plasterboard. Always hit the internal timber studs or use rated steel toggles.\n\n"
            "Are your TV wires hidden or dangling?"
        ),
        "tiktok_tags": "#TVMounting #OLED #HomeCinema #DIYFail #Tradesman #Yorkshire"
    },
    {
        "hour": 12,
        "id": "ajax-vs-legacy-bellbox",
        "category": "ajax",
        "topic": "Why Dummy Bellboxes Don't Stop Burglars",
        "badge": "🛡️ ALARM REALITY",
        "hook_line1": "DUMMY BELLBOXES",
        "hook_line2": "DON'T STOP THIEVES!",
        "subtitle": "Why modern burglars test your siren",
        "script": (
            "Do dummy alarm boxes actually deter burglars in 2026? "
            "Experienced intruders know dummy boxes have faded plastic, dead flashing LEDs, and zero tamper switches. "
            "They will kick a rear door knowing no police or phone alert will trigger. "
            "An Ajax Grade 2 Jeweller system features an illuminated 113-decibel external StreetSiren, accelerometer tamper defence, and sends instant photo verification to your mobile phone in under nine seconds. "
            "Protect what matters. Call Gary Pearce on 07860 244 274."
        ),
        "ig_caption": (
            "🛡️ WHY DUMMY ALARMS DON'T FOOL BURGLARS!\n\n"
            "Modern thieves can spot fake sirens from the pavement.\n"
            "🚨 Ajax StreetSiren: 113dB sounder + strobe\n"
            "🚨 Accelerometer tamper: triggers if knocked or levered off brickwork\n"
            "🚨 Encrypted Jeweller 868MHz wireless communication\n"
            "🚨 Photo verification sent to your phone in 9 seconds\n\n"
            "Installed by Gary Pearce, ADI Communications (07860 244 274).\n\n"
            "#AjaxAlarms #HomeSecurityTips #BurglaryPrevention #SmartAlarm #YorkshireHomes"
        ),
        "threads_post": (
            "Security debate:\n\n"
            "Do you think yellow dummy bellboxes on houses still deter burglars in 2026?\n\n"
            "Burglars know dummy boxes have no battery backup and no phone alerts. Grade 2 Ajax smart alarms send photo evidence in 9 seconds.\n\n"
            "Does your alarm notify your smartphone?"
        ),
        "tiktok_tags": "#AjaxAlarms #SmartAlarms #HomeSecurity #CrimePrevention #YorkshireTrades"
    },
    {
        "hour": 13,
        "id": "starlink-garden-office-link",
        "category": "starlink",
        "topic": "Fast Broadband For Your Garden Office",
        "badge": "🛰️ RURAL BROADBAND",
        "hook_line1": "GARDEN OFFICE",
        "hook_line2": "WI-FI IS TOO SLOW!",
        "subtitle": "Gigabit wireless bridge vs bad Wi-Fi",
        "script": (
            "Working from a garden office or converted garage and sick of lagging Zoom calls? "
            "Standard Wi-Fi cannot penetrate double glazing, exterior brick, and timber cladding over long distances. "
            "We install dedicated 5-gigahertz gigabit wireless bridges or armoured direct-burial Cat6 cabling. "
            "Whether you're running Starlink Gen 3 or full fibre, you get flawless 300-megabit speeds right at your garden desk. "
            "I'm Gary Pearce, Lead Engineer at ADI Communications. Call 07860 244 274."
        ),
        "ig_caption": (
            "🛰️ FIX YOUR GARDEN OFFICE WI-FI LAG!\n\n"
            "Double glazing and exterior cladding kill indoor Wi-Fi. Here's how we fix it:\n"
            "✔ 5GHz Point-to-Point Gigabit Wireless Bridge (up to 500m line of sight)\n"
            "✔ Direct-burial armoured external Cat6 cable\n"
            "✔ Dedicated Wi-Fi 6 access point inside the office\n\n"
            "Fitted by Gary Pearce, ADI Communications (07860 244 274).\n\n"
            "#GardenOffice #WorkFromHome #StarlinkUK #HomeNetworking #YorkshireBusiness"
        ),
        "threads_post": (
            "Remote workers:\n\n"
            "Why do so many garden offices suffer from unusable Wi-Fi and frozen video calls?\n\n"
            "Modern foil-backed insulation creates a Faraday cage that blocks indoor Wi-Fi. A 5GHz wireless bridge delivers 300+ Mbps instantly.\n\n"
            "Do you work from an outbuilding or garden room?"
        ),
        "tiktok_tags": "#GardenOffice #WFH #Starlink #Networking #Yorkshire #Tradesman"
    },
    {
        "hour": 14,
        "id": "cctv-local-storage-vs-cloud",
        "category": "cctv",
        "topic": "Stop Paying Monthly Camera Subscriptions",
        "badge": "💰 SAVE MONEY TRUTH",
        "hook_line1": "STOP PAYING £15/MO",
        "hook_line2": "CLOUD CCTV FEES!",
        "subtitle": "Local 4TB Hard Drive vs Cloud Traps",
        "script": (
            "How much are you spending every year on cloud subscriptions for doorbell and security cameras? "
            "At fifteen pounds a month, that's nearly two hundred pounds every year, just to view footage of your own driveway. "
            "And if your internet goes down, cloud cameras record absolutely nothing. "
            "A professional commercial Network Video Recorder with a surveillance-grade four-terabyte hard drive stores thirty days of continuous footage locally. "
            "Zero subscriptions, zero monthly fees, forever. "
            "Call Gary Pearce on 07860 244 274."
        ),
        "ig_caption": (
            "💰 STOP PAYING £15/MONTH CLOUD CCTV FEES!\n\n"
            "Subscription traps cost UK homeowners £180+ every single year.\n"
            "⚡ Commercial PoE NVR: 24/7 continuous local recording\n"
            "⚡ 30-day retention on 4TB Western Digital Purple hard drives\n"
            "⚡ 100% operational even during complete broadband outages\n"
            "⚡ £0 monthly subscription fees forever\n\n"
            "Installed by Gary Pearce, ADI Communications (07860 244 274).\n\n"
            "#CCTVUK #SaveMoney #SmartHome #Hikvision #YorkshireTrades #GaryPearce"
        ),
        "threads_post": (
            "Home budget question:\n\n"
            "Why pay £15 every month to a cloud camera brand when a 4TB local surveillance hard drive stores 30 days of footage for £0 ongoing cost?\n\n"
            "Cloud cameras also stop recording completely if your home broadband goes down. Local NVRs never stop.\n\n"
            "How much do you pay in subscriptions each month?"
        ),
        "tiktok_tags": "#CCTV #SaveMoney #SmartHome #TechTips #YorkshireTrades"
    },
    {
        "hour": 15,
        "id": "ajax-pet-immune-pir",
        "category": "ajax",
        "topic": "Can Dogs and Cats Trigger Wireless Alarms?",
        "badge": "🐕 PET FRIENDLY ALARM",
        "hook_line1": "DO PETS TRIGGER",
        "hook_line2": "SMART ALARMS?",
        "subtitle": "SmartDetect digital algorithm calibration",
        "script": (
            "Will your dog or cat set off your burglar alarm while you're at work? "
            "Cheap DIY alarms use primitive passive infrared sensors that trigger whenever a pet jumps on the sofa. "
            "Ajax MotionProtect uses the proprietary SmartDetect software algorithm. "
            "It analyses thermal radiation mass, velocity, and optical beam patterns, ignoring animals up to twenty kilograms and fifty centimetres tall. "
            "You get zero false alarms and complete peace of mind. "
            "I'm Gary Pearce at ADI Communications. Call me on 07860 244 274."
        ),
        "ig_caption": (
            "🐕 NO MORE FALSE ALARMS FROM DOGS & CATS!\n\n"
            "How Ajax MotionProtect protects your home without false triggers:\n"
            "🐾 SmartDetect algorithm filters out pets up to 20kg / 50cm\n"
            "🐾 Precision optical lens splits infrared radiation\n"
            "🐾 Temperature compensation in hot summers and cold winters\n\n"
            "Certified Ajax installation by Gary Pearce, ADI Communications (07860 244 274).\n\n"
            "#AjaxAlarms #DogLoversUK #CatLoversUK #SmartHome #HomeSecurity #Yorkshire"
        ),
        "threads_post": (
            "Pet owners debate:\n\n"
            "Have you ever had your burglar alarm go off in the middle of the day because your dog jumped on the sofa?\n\n"
            "Modern SmartDetect PIRs calculate heat mass and velocity, ignoring pets up to 20kg while catching human intruders instantly.\n\n"
            "Do you leave your alarm armed with pets indoors?"
        ),
        "tiktok_tags": "#DogLovers #Pets #SmartAlarms #HomeSecurity #Ajax"
    },
    {
        "hour": 16,
        "id": "starlink-storm-brackets-pennines",
        "category": "starlink",
        "topic": "Starlink In 90mph 90mph High Winds",
        "badge": "🛰️ 90MPH STORM PROOF",
        "hook_line1": "STARLINK IN 90MPH",
        "hook_line2": "90MPH HIGH WINDS!",
        "subtitle": "Pennine brackets vs cheap Amazon poles",
        "script": (
            "Will your Starlink dish survive a 90-mile-an-hour winter gale in the Pennines? "
            "Standard thin aluminium poles from online marketplaces flex and twist in high winds, causing instant satellite disconnections and packet loss. "
            "We engineer installations using heavy-gauge galvanised steel Pennine brackets, double-masted support struts, and precision stainless chimney lashings. "
            "Rock-solid stability in extreme weather so you never lose connection. "
            "Call Gary Pearce on 07860 244 274."
        ),
        "ig_caption": (
            "🛰️ 90MPH STORM-TESTED STARLINK INSTALLATIONS!\n\n"
            "Micro-wobble in high winds breaks low-Earth satellite lock. How we build for Pennine gales:\n"
            "✔ Heavy-duty galvanised heavy-duty Starlink chimney brackets\n"
            "✔ Non-drill stainless steel chimney lashing cradles\n"
            "✔ Solid copper exterior Cat6 with drip loop cable seals\n\n"
            "Fitted by Gary Pearce, ADI Communications (07860 244 274).\n\n"
            "#StarlinkUK #StormProof #RuralBroadband #BroadbandInstaller #YorkshireTrades"
        ),
        "threads_post": (
            "Rural broadband reality:\n\n"
            "Why do so many Starlink dishes disconnect during heavy winter gales across the UK?\n\n"
            "A cheap thin mounting pole flexes in 50mph winds, breaking the millimeter-wave satellite beam. Heavy Pennine steel brackets keep it laser-still.\n\n"
            "How does your broadband hold up during storms?"
        ),
        "tiktok_tags": "#Starlink #Storm #Broadband #RuralUK #Engineering"
    },
    {
        "hour": 17,
        "id": "cctv-poe-switch-surge-protection",
        "category": "cctv",
        "topic": "Why Outdoor CCTV Cameras Need Drip Loops",
        "badge": "⚡ TRADE SECRETS",
        "hook_line1": "WHY WATER TRACKS",
        "hook_line2": "INTO YOUR WALLS!",
        "subtitle": "Drip loops & IP67 junction boxes",
        "script": (
            "Here is the number one installation mistake amateur installers make with outdoor cameras: failing to form a proper cable drip loop. "
            "When rain pours down an exterior brick wall, water runs along the black cable directly into the drilled entry hole and straight into your cavity insulation. "
            "Within twelve months, you have damp patches on your living room wallpaper. "
            "Every professional cable entry must curve down below the hole before entering, forcing water to drip harmlessly to the ground. "
            "Do it once, do it right. Call Gary Pearce on 07860 244 274."
        ),
        "ig_caption": (
            "⚡ THE #1 CCTV WATER DAMAGE MISTAKE!\n\n"
            "Water tracks straight down cables into brickwork without a proper drip loop.\n"
            "✔ Precision downward loop forces water to drip to the ground\n"
            "✔ Silicone-sealed external entry grommets\n"
            "✔ IP67 weatherproof junction boxes\n\n"
            "25+ years hands-on trade experience with Gary Pearce (07860 244 274).\n\n"
            "#TradesmanSecrets #CCTVFail #DIYTips #HomeMaintenance #YorkshireTrades"
        ),
        "threads_post": (
            "Building craftsmanship note:\n\n"
            "Did you know that drilling straight through brickwork without a cable drip loop can rot your cavity wall insulation within 12 months?\n\n"
            "Rain runs down the wire right into the mortar hole. A simple downward curve stops it completely.\n\n"
            "What's the worst trade shortcut you've spotted on your house?"
        ),
        "tiktok_tags": "#Tradesman #DIY #CCTV #BuildingTips #Yorkshire"
    },
    {
        "hour": 18,
        "id": "tv-aerial-pixelation-filter",
        "category": "aerial",
        "topic": "Why Your TV Screen Keeps Freezing and Pixelating",
        "badge": "📺 5G SIGNAL INTERFERENCE",
        "hook_line1": "WHY FREEVIEW TV",
        "hook_line2": "KEEPS PIXELATING!",
        "subtitle": "4G & 5G mast interference filters",
        "script": (
            "Why does your Freeview TV screen suddenly freeze, squeak, and break into pixel blocks when a car drives past or in bad weather? "
            "Most homeowners think they need an expensive new aerial. "
            "In 80% of cases, nearby mobile phone masts transmitting high-power 4G and 5G signals are overloading your unshielded TV amplifier. "
            "Fitting a CAI-benchmarked 700-megahertz LTE filter and double-screened WF100 coaxial cable eliminates the noise instantly. "
            "I'm Gary Pearce at ADI Communications. Call me on 07860 244 274."
        ),
        "ig_caption": (
            "📺 WHY YOUR FREEVIEW TV KEEPS PIXELATING!\n\n"
            "It might not be a broken aerial. 4G/5G mobile masts cause high-frequency signal overload.\n"
            "✔ CAI-benchmarked double-screened WF100 cable\n"
            "✔ 700MHz LTE interference rejection filters\n"
            "✔ Precision spectrum analyzer alignment\n\n"
            "Gary Pearce, ADI Communications (07860 244 274).\n\n"
            "#FreeviewTV #TVAerial #TechHelp #YorkshireHomes #GaryPearce"
        ),
        "threads_post": (
            "TV viewer puzzle:\n\n"
            "Does your Freeview TV picture freeze or break into blocks during prime time?\n\n"
            "Most people assume the aerial is broken, but in 80% of cases nearby 4G/5G mobile masts are overloading the booster. A £15 LTE filter solves it.\n\n"
            "Do you still watch standard broadcast Freeview?"
        ),
        "tiktok_tags": "#TV #Freeview #TechTips #HomeHelp #Yorkshire"
    },
    {
        "hour": 19,
        "id": "ajax-doorprotect-plus-vibration",
        "category": "ajax",
        "topic": "Stop Burglars Before They Even Break In",
        "badge": "🚪 PERIMETER DEFENCE",
        "hook_line1": "STOP BURGLARS",
        "hook_line2": "BEFORE BREAK-IN!",
        "subtitle": "DoorProtect Plus shock & tilt sensors",
        "script": (
            "Why wait for a burglar to smash your patio door and step inside your hallway before your alarm triggers? "
            "Standard magnetic reed switches only trigger when a door opens. "
            "The Ajax DoorProtect Plus includes built-in vibration and tilt sensors. "
            "The moment an intruder uses a crowbar or strikes the door frame, the system detects the shock wave and fires the siren immediately, scaring them off before they even enter. "
            "Protect your perimeter. Call Gary Pearce on 07860 244 274."
        ),
        "ig_caption": (
            "🚪 STOP INTRUDERS BEFORE THEY STEP INSIDE!\n\n"
            "Why wait for broken glass? Ajax DoorProtect Plus detects forced entry attempts:\n"
            "🛡️ Built-in accelerometer detects crowbar strikes & lock attacks\n"
            "🛡️ Tilt sensor detects roof window tampering\n"
            "🛡️ 113dB StreetSiren triggers while the door is still locked\n\n"
            "Installed by Gary Pearce, ADI Communications (07860 244 274).\n\n"
            "#AjaxAlarms #HomeSecurity #BurglaryPrevention #SmartHomeUK #Yorkshire"
        ),
        "threads_post": (
            "Home security question:\n\n"
            "Why do standard burglar alarms only sound AFTER an intruder has already broken the lock and entered your hallway?\n\n"
            "Shock and vibration sensors on patio doors trigger the siren on the very first crowbar strike, scaring intruders off outside.\n\n"
            "What security sensors do you have on patio doors?"
        ),
        "tiktok_tags": "#HomeSecurity #Ajax #BurglaryPrevention #SmartHome #Yorkshire"
    },
    {
        "hour": 20,
        "id": "ethernet-beats-wifi-gaming",
        "category": "cat6",
        "topic": "Why Hardwired Ethernet Beats Wi-Fi For Gaming",
        "badge": "🎮 ZERO LATENCY GAMING",
        "hook_line1": "WHY ETHERNET",
        "hook_line2": "DESTROYS WI-FI!",
        "subtitle": "0ms jitter & packet loss elimination",
        "script": (
            "Why do gamers and streamers experience lag spikes even with a one-gigabit broadband package? "
            "Wi-Fi is a half-duplex radio medium. Only one device can transmit at a time, causing packet queueing and jitter spikes whenever a family member streams video. "
            "Solid copper Cat6 Ethernet is full-duplex, delivering simultaneous gigabit throughput with near-zero millisecond jitter. "
            "Hardwire your gaming PC, PS5, and Xbox for unshakeable competitive performance. "
            "Call Gary Pearce on 07860 244 274."
        ),
        "ig_caption": (
            "🎮 WHY WI-FI KILLS YOUR GAMING PING!\n\n"
            "Broadband speed is meaningless if you have radio jitter and packet loss.\n"
            "⚡ Full-duplex solid copper Cat6 hardwired points\n"
            "⚡ Near-zero jitter and zero packet loss\n"
            "⚡ Dedicated RJ45 faceplates in bedrooms and games rooms\n\n"
            "Installed by Gary Pearce, ADI Communications (07860 244 274).\n\n"
            "#GamingSetup #PS5UK #XboxUK #Cat6 #HomeNetworking #YorkshireTrades"
        ),
        "threads_post": (
            "Gamers and tech heads:\n\n"
            "Why do people spend £1,500 on a gaming PC or console, then play on choppy Wi-Fi that drops packets every time someone watches Netflix?\n\n"
            "Hardwired Cat6 copper gives rock-solid 0ms jitter and eliminates lag spikes forever.\n\n"
            "Is your gaming console hardwired with Ethernet or on Wi-Fi?"
        ),
        "tiktok_tags": "#Gaming #PS5 #Xbox #Networking #Cat6 #Yorkshire"
    },
    {
        "hour": 21,
        "id": "cctv-number-plate-recognition",
        "category": "cctv",
        "topic": "Can CCTV Actually Read Number Plates At Night?",
        "badge": "🚗 NUMBER PLATE TRUTH",
        "hook_line1": "CAN CCTV READ",
        "hook_line2": "PLATES AT NIGHT?",
        "subtitle": "DORI standards & shutter speed reality",
        "script": (
            "Can standard domestic CCTV cameras read vehicle number plates in pitch darkness? "
            "Almost never. A moving vehicle at night requires a minimum shutter speed of one-two-thousandth of a second and high-power anti-reflective lighting to avoid retro-reflective white flare. "
            "To capture readable plates for the police, you need a dedicated optical Automatic Number Plate Recognition camera with specialized lens focal length. "
            "Don't get fooled by false marketing claims. "
            "I'm Gary Pearce at ADI Communications. Call me on 07860 244 274 for certified trade guidance."
        ),
        "ig_caption": (
            "🚗 CAN YOUR CCTV READ NUMBER PLATES AT NIGHT?\n\n"
            "Standard cameras cannot read moving plates due to retro-reflective plate flare and slow auto-exposure.\n"
            "✔ Specialized ANPR traffic cameras with fast 1/2000s shutter speeds\n"
            "✔ DORI BS EN 62676-4 identification compliance (250 pixels per metre)\n"
            "✔ Hardwired PoE surveillance\n\n"
            "Gary Pearce, ADI Communications (07860 244 274).\n\n"
            "#ANPR #CCTV #CrimePreventionUK #HomeSecurity #YorkshireTrades"
        ),
        "threads_post": (
            "Honest trade advice:\n\n"
            "Has anyone ever tried to read a vehicle registration plate from standard doorbell or battery camera footage at night?\n\n"
            "It turns into a glowing white rectangle. True ANPR needs fast shutter speeds (1/2000s) and optical zoom to meet police court standards.\n\n"
            "Has your camera ever caught anything useful?"
        ),
        "tiktok_tags": "#CCTV #ANPR #CrimePrevention #HomeSecurity #Yorkshire"
    },
    {
        "hour": 22,
        "id": "ajax-power-cut-failover",
        "category": "ajax",
        "topic": "What Happens To Your Security When Power Cuts?",
        "badge": "🔋 POWER CUT DEFENCE",
        "hook_line1": "WHAT HAPPENS IN A",
        "hook_line2": "WINTER POWER CUT?",
        "subtitle": "16-hour Li-ion battery & 4G dual SIM",
        "script": (
            "What happens to your home security system during a winter power cut or if a burglar cuts your external electricity meter? "
            "Wi-Fi cameras and standard alarms immediately die, leaving your property unprotected. "
            "The Ajax Hub 2 Plus switches seamlessly to its internal lithium-ion backup battery, providing up to sixteen hours of autonomous operation. "
            "And with dual 4G micro-SIM slots, it continues alerting your mobile phone even when municipal broadband is down. "
            "Sleep soundly every night. Call Gary Pearce on 07860 244 274."
        ),
        "ig_caption": (
            "🔋 WHAT HAPPENS TO YOUR ALARM DURING A POWER CUT?\n\n"
            "Burglars often cut external power meters. How Ajax protects you:\n"
            "🛡️ 16-hour internal lithium-ion backup battery\n"
            "🛡️ Dual 4G micro-SIM cellular failover\n"
            "🛡️ Sub-second notification sent to your phone: 'External Power Lost'\n\n"
            "Installed by Gary Pearce, ADI Communications (07860 244 274).\n\n"
            "#AjaxAlarms #PowerCut #HomeSecurityTips #SmartAlarm #YorkshireHomes"
        ),
        "threads_post": (
            "Winter power cut debate:\n\n"
            "If your street loses power tonight or someone cuts your external meter box, is your home security still working?\n\n"
            "Wi-Fi cameras go dark immediately. Ajax hubs run for 16 hours on internal batteries with dual 4G SIM backup.\n\n"
            "Does your alarm have cellular battery backup?"
        ),
        "tiktok_tags": "#PowerCut #HomeSecurity #Ajax #SmartAlarms #Yorkshire"
    }
]

def render_hud_overlay(campaign: dict, output_path: Path):
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

    # 2. Viral Hook Headline Card (Y = 360 to 560)
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

    # 3. Lower-Third Trade Authority Glassmorphism Card (Y = 1310 to 1530)
    draw.rounded_rectangle([60, 1310, 1020, 1530], radius=20, fill=(5, 5, 8, 240), outline=(255, 255, 255, 50), width=2)
    draw.text((90, 1335), "GARY PEARCE • ADI COMMUNICATIONS", font=f_card_title, fill=(255, 255, 255, 255))
    draw.text((90, 1380), "📞 DIRECT MOBILE: 07860 244 274 • 25+ YRS CRAFTSMANSHIP", font=f_card_sub, fill=(255, 160, 122, 255))
    draw.text((90, 1425), "£10M PUBLIC LIABILITY • SOLID COPPER & CAI BENCHMARKED", font=f_card_stars, fill=(200, 200, 200, 255))
    draw.text((90, 1470), "★★★★★ 9.98 / 10 RATING (84+ VERIFIED CLIENT REVIEWS)", font=f_card_stars, fill=(255, 229, 0, 255))

    overlay.save(str(output_path))


async def generate_voiceover(text: str, output_path: Path):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice="en-GB-RyanNeural", rate="-2%", pitch="+0Hz")
    await communicate.save(str(output_path))


def get_audio_duration(audio_path: Path) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(res.stdout.strip())
    except Exception:
        return 45.0


def render_916_reel(img_path: Path, hud_path: Path, audio_path: Path, duration: float, output_path: Path):
    d_frames = int(duration * 30)
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
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", f"{duration:.3f}",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def publish_threads_post(post_text: str) -> bool:
    """Publish directly to Meta Threads via Chrome CDP on port 9223."""
    try:
        data = urllib.request.urlopen('http://127.0.0.1:9223/json').read().decode()
        tabs = json.loads(data)
        th_tab = next((t for t in tabs if 'threads' in t.get('url', '').lower()), None)
        if not th_tab:
            print("  [*] Opening new Threads tab via Chrome CDP...")
            req = urllib.request.Request("http://127.0.0.1:9223/json/new?https%3A%2F%2Fwww.threads.net%2F%40cctv.service.uk", method="PUT")
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                th_tab = json.loads(resp.read().decode())
                await asyncio.sleep(4)

        async with websockets.connect(th_tab["webSocketDebuggerUrl"], max_size=20*1024*1024) as ws:
            # Navigate to profile to ensure clean UI
            await ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": "https://www.threads.net/@cctv.service.uk"}}))
            await asyncio.sleep(4)

            # Click What's new?
            click_expr = """
            (() => {
                const divs = Array.from(document.querySelectorAll('div[role="button"]'));
                const target = divs.find(d => d.innerText && d.innerText.trim() === "What's new?");
                if (target) { target.click(); return true; }
                return false;
            })()
            """
            await ws.send(json.dumps({"id": 2, "method": "Runtime.evaluate", "params": {"expression": click_expr, "returnByValue": True}}))
            await asyncio.sleep(2)

            # Type text into textbox
            type_expr = f"""
            (() => {{
                const box = document.querySelector('div[role="textbox"]');
                if (!box) return false;
                box.focus();
                document.execCommand('insertText', false, {json.dumps(post_text)});
                box.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return true;
            }})()
            """
            await ws.send(json.dumps({"id": 3, "method": "Runtime.evaluate", "params": {"expression": type_expr, "returnByValue": True}}))
            await asyncio.sleep(2)

            # Click Post button
            post_expr = """
            (() => {
                const dialog = document.querySelector('div[role="dialog"]') || document;
                const btns = Array.from(dialog.querySelectorAll('div[role="button"], button'));
                const postBtn = btns.find(b => b.innerText && b.innerText.trim() === 'Post');
                if (postBtn) { postBtn.click(); return true; }
                return false;
            })()
            """
            await ws.send(json.dumps({"id": 4, "method": "Runtime.evaluate", "params": {"expression": post_expr, "returnByValue": True}}))
            await asyncio.sleep(5)
            print("  [+] Threads post submitted successfully")
            return True
    except Exception as e:
        print(f"  [!] Threads publish error: {e}")
        return False


def publish_instagram_reel(video_path: Path, caption: str, campaign_id: str) -> bool:
    """Publish Reel to Instagram via CDP."""
    try:
        ig_agent = Path(r"C:\Users\Gary\.gemini\antigravity\scratch\instagram_agent\instagram_agent.py")
        cmd = [
            sys.executable, str(ig_agent),
            "--video", str(video_path),
            "--campaign", campaign_id,
            "--caption", caption
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
        stdout_text = res.stdout or ""
        success = (res.returncode == 0 and "Reel published live" in stdout_text)
        print(f"  [+] Instagram Reel published: {success}")
        return success
    except Exception as e:
        print(f"  [!] Instagram publish error: {e}")
        return False


async def execute_hourly_cycle(hour: int = None):
    now = datetime.now()
    if hour is None:
        hour = now.hour
    
    # Match campaign by hour or pick modulo
    camp = next((c for c in HOURLY_CAMPAIGNS if c["hour"] == hour), HOURLY_CAMPAIGNS[hour % len(HOURLY_CAMPAIGNS)])
    
    print(f"\n{'='*70}\n[HOURLY AGENT CYCLE: {now.strftime('%Y-%m-%d %H:%M:%S')}] Campaign: {camp['topic']}\n{'='*70}")

    # 1. Pick 100% UNUSED IMAGE
    img_name = media_registry.get_next_unused_image(camp["category"])
    img_path = REPO_ROOT / "assets" / "images" / img_name
    print(f"[+] Unique Image Selected (ZERO prior usage): {img_name}")

    # 2. Render Audio
    audio_path = CACHE_DIR / f"{camp['id']}.mp3"
    print(f"[*] Generating voiceover via edge-tts (Rule 28 £0 cost)...")
    await generate_voiceover(camp["script"], audio_path)
    dur = get_audio_duration(audio_path)
    print(f"  -> Voiceover generated: {dur:.1f}s")

    # 3. Render HUD & 9:16 Video
    hud_path = CACHE_DIR / f"{camp['id']}_hud.png"
    render_hud_overlay(camp, hud_path)
    
    reel_path = REELS_DIR / f"{camp['id']}.mp4"
    print(f"[*] Rendering 1080x1920 9:16 vertical reel via FFmpeg...")
    render_916_reel(img_path, hud_path, audio_path, dur, reel_path)
    print(f"  -> 9:16 Reel generated: {reel_path.name} ({reel_path.stat().st_size / 1024 / 1024:.2f} MB)")

    # 4. Mark image as used
    media_registry.mark_image_used(img_name, camp["id"], "Instagram+Threads")

    # 5. Publish to Meta Threads (@cctv.service.uk)
    print(f"[*] Publishing to Meta Threads (@cctv.service.uk)...")
    threads_success = await publish_threads_post(camp["threads_post"])

    # 6. Publish to Instagram (@cctv.service.uk)
    print(f"[*] Publishing Reel to Instagram (@cctv.service.uk)...")
    ig_success = publish_instagram_reel(reel_path, camp["ig_caption"], camp["id"])

    # 7. Record in Audit Log
    entry = {
        "hour": hour,
        "timestamp": datetime.now().isoformat(),
        "campaign_id": camp["id"],
        "topic": camp["topic"],
        "image_used": img_name,
        "reel_path": str(reel_path),
        "duration_seconds": dur,
        "threads_published": threads_success,
        "instagram_published": ig_success,
        "tiktok_tags": camp["tiktok_tags"],
        "tiktok_status": "READY_FOR_UPLOAD"
    }
    
    log_data = []
    if AUDIT_LOG.exists():
        with open(AUDIT_LOG, "r", encoding="utf-8") as f:
            try: log_data = json.load(f)
            except: pass
    log_data.append(entry)
    with open(AUDIT_LOG, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

    print(f"\n[CYCLE COMPLETE] Logged to hourly_trend_audit.json\n{'='*70}")
    return entry

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycle-now", action="store_true", help="Execute current hour cycle immediately")
    parser.add_argument("--hour", type=int, default=None, help="Target specific hour (9-22)")
    args = parser.parse_args()

    asyncio.run(execute_hourly_cycle(args.hour))
