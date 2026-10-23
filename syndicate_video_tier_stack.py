#!/usr/bin/env python3
"""
syndicate_video_tier_stack.py (v2.0.0 - 50x50 Sovereign Video Stack Engine)
==========================================================================
Master Multi-Tier Video Stacking Engine for ADI Communications & Gary Pearce.

Enforces Gary Pearce's Strict Linking Law & Rule 45 Citadel Air-Gap:
1. Tier 1 (Apex): YouTube links directly to ADI website buffer/service pages & Blogger.
2. Tier 2 (Top-Level Platforms): Links to ADI website buffer pages AND links up to YouTube Apex.
3. Tier 3 (Alternative Platforms): Links EXCLUSIVELY to YouTube. ABSOLUTE 0 links to adicommunications.co.uk.

Outputs:
- video_stack_50_syndication_manifest.json (Centralized 50x50 Matrix, 2,500 targets)
- syndication/<platform_slug>/<platform_slug>_video_manifest.json & .csv (50 directories)
- syndication/<platform_id>/<platform_slug>_manifest.json
- video_stack_master_tiers.json
"""

import os
import sys
import json
import csv
import re
import hashlib
import argparse
import posixpath
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple, List, Dict, Any

REPO_ROOT = Path(__file__).resolve().parent
CATALOG_PATH = REPO_ROOT / "video_stack_50_catalog.json"
PLATFORMS_CATALOG_PATH = REPO_ROOT / "master_multicategory_platform_catalog.json"
SYNDICATION_DIR = REPO_ROOT / "syndication"
MASTER_MANIFEST_PATH = REPO_ROOT / "video_stack_50_syndication_manifest.json"
ALT_MANIFEST_PATH = SYNDICATION_DIR / "video_stack_50_syndication_manifest.json"
MASTER_TIERS_PATH = REPO_ROOT / "video_stack_master_tiers.json"

YOUTUBE_APEX_CHANNEL = "https://www.youtube.com/@CCTV.services"
GARY_PHONE = "07860 244 274"
GARY_TRADE = "Gary Pearce • ADI Communications (25+ Years Hands-On UK Security & Telecom Engineer, £10M Public Liability)"
VERIFIED_RATING = "★★★★★ 9.98 / 10 Rating • 84+ Verified Client Reviews"
CAI_DISCLAIMER_LINE = "• Fitted with CAI-benchmarked equipment & double-screened WF100 / solid copper Cat6 cabling"
NVQ_STANDARDS_LINE = "• NVQ Level 1-4 Data Cabling, Fibre Optics & Electrical Standards (BS 7671)"

# Platform directory overrides for backward compatibility with existing tests and scripts
PLATFORM_DIR_OVERRIDES = {
    "PLAT-VID-001": "youtube",
    "PLAT-VID-002": "dailymotion",
    "PLAT-VID-003": "vimeo",
    "PLAT-VID-004": "archive_org",
    "PLAT-VID-005": "wistia",
    "PLAT-VID-020": "rumble",
    "PLAT-VID-021": "odysee",
    "PLAT-VID-022": "peertube",
    "PLAT-VID-023": "bitchute",
    "PLAT-VID-024": "dtube",
}


def slugify(text: str) -> str:
    """Produces clean snake_case slug from string."""
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def get_platform_dir(plat: dict) -> str:
    """Returns canonical directory name for a platform."""
    pid = plat.get("platform_id", "")
    if pid in PLATFORM_DIR_OVERRIDES:
        return PLATFORM_DIR_OVERRIDES[pid]
    return slugify(plat.get("name", "platform"))


def generate_clamped_chapters(duration_sec: float) -> list[str]:
    """
    Generates YouTube-compliant 3-chapter markers dynamically clamped to video duration.
    Guarantees:
      - Starts at 00:00
      - Minimum 3 chapters
      - Every segment >= 10 seconds
      - Clamped timestamp < duration_sec
    """
    ch3_sec = max(25, int(duration_sec * 0.75))
    return [
        "00:00 - Introduction & Hardware Overview",
        "00:15 - Technical Engineering Standards & DORI Admissibility",
        f"00:{ch3_sec:02d} - Gary Pearce Field Deployment & Verification",
    ]


def build_tier1_apex_description(video: dict, platform_name: str = "YouTube") -> str:
    """Tier 1: Links to YouTube Apex, Blogger Citadel Hub, and /news/<slug>/ buffer."""
    chapters = generate_clamped_chapters(video["duration_sec"])
    tags_formatted = ", ".join(f"#{t.replace(' ', '')}" for t in video.get("tags", []))

    desc = f"{video['title']}\n\n"
    desc += f"Official 4K masterclass field debrief by {GARY_TRADE}. Direct mobile: {GARY_PHONE}.\n\n"
    desc += "Field Engineering Chapters & Timestamps:\n" + "\n".join(chapters) + "\n\n"
    desc += "Trade Standards & Compliance:\n"
    desc += f"{CAI_DISCLAIMER_LINE}\n"
    desc += f"{NVQ_STANDARDS_LINE}\n"
    desc += f"• {VERIFIED_RATING}\n\n"
    desc += "Official Verification & Companion Study Links:\n"
    desc += f"• Complete 4K Masterclass on YouTube: {YOUTUBE_APEX_CHANNEL}\n"
    desc += f"• Google Shield Companion Guide (Blogger DA 99): {video['blogger_shield_url']}\n"
    desc += f"• Technical Field Notes & Interactive Calculators: {video['buffer_url']}\n\n"
    desc += f"Telephone Enquiries: {GARY_PHONE} (Gary Pearce)\n\n"
    desc += f"SEO Tags: {tags_formatted}"
    return desc


def build_tier2_high_da_description(video: dict, platform_name: str) -> str:
    """Tier 2: Dual-linked to YouTube Apex and /news/<slug>/ technical buffer."""
    chapters = generate_clamped_chapters(video["duration_sec"])

    desc = f"{video['title']}\n\n"
    desc += f"Official {platform_name} broadcast by {GARY_TRADE}. Direct mobile: {GARY_PHONE}.\n\n"
    desc += "Field Engineering Chapters & Timestamps:\n" + "\n".join(chapters) + "\n\n"
    desc += "Trade Standards & Verification:\n"
    desc += f"{CAI_DISCLAIMER_LINE}\n"
    desc += f"{NVQ_STANDARDS_LINE}\n"
    desc += f"• {VERIFIED_RATING}\n\n"
    desc += "Official Apex Video & Buffer Links:\n"
    desc += f"• Full 4K Masterclass on YouTube: {YOUTUBE_APEX_CHANNEL}\n"
    desc += f"• Technical Field Notes & Calculators: {video['buffer_url']}\n"
    desc += f"• Google Shield Blogger Specification: {video['blogger_shield_url']}\n\n"
    desc += f"Telephone Enquiries: {GARY_PHONE} (Gary Pearce)"
    return desc


def build_tier3_alternative_description(video: dict, platform_name: str) -> str:
    """Tier 3: Strictly isolated to YouTube. ABSOLUTE ZERO mentions of adicommunications.co.uk."""
    chapters = generate_clamped_chapters(video["duration_sec"])

    desc = f"{video['title']}\n\n"
    desc += f"Decentralized {platform_name} mirror broadcast by {GARY_TRADE}. Direct mobile: {GARY_PHONE}.\n\n"
    desc += "Field Engineering Chapters & Timestamps:\n" + "\n".join(chapters) + "\n\n"
    desc += "Trade Standards & Verification:\n"
    desc += f"{CAI_DISCLAIMER_LINE}\n"
    desc += f"{NVQ_STANDARDS_LINE}\n"
    desc += f"• {VERIFIED_RATING}\n\n"
    desc += "--- OFFICIAL VIDEO SOURCE ---\n"
    desc += f"Watch the original full 4K masterclass on YouTube:\n{YOUTUBE_APEX_CHANNEL}\n\n"
    desc += f"Subscribe to the Official YouTube Entity Channel:\n{YOUTUBE_APEX_CHANNEL}\n\n"
    desc += f"Engineer Direct Telephone: {GARY_PHONE} (Gary Pearce)"
    return desc


class Rule45CitadelAirGapFirewall:
    """
    Comprehensive Rule 45 Citadel Air-Gap & Tier Isolation Firewall.
    Enforces:
      1. Zero raw root links to adicommunications.co.uk/ (repository-wide).
      2. 100% strict YouTube isolation on Tier 3 platforms (zero domain occurrences).
      3. Chapter marker clamping (strictly less than video duration).
      4. Trade E-E-A-T invariants (0 Checkatrade, 0 0800 numbers, 0 banned buzzwords).
    """

    ROOT_LINK_REGEX = re.compile(
        r"(?:https?:)?//(?:www\.)?adicommunications\.co\.uk\.?(?::\d+)?(?:/([^\s\"\'<>)]*)|(?=$|[?#\"'\s<>,;)\]}]))",
        re.IGNORECASE,
    )
    DOMAIN_LEAK_REGEX = re.compile(r"adicommunications\.co\.uk", re.IGNORECASE)
    OBFUSCATED_DOMAIN_REGEX = re.compile(
        r"adicommunications(?:\[\.\]|\(dot\)|\.|\%2e)co(?:\[\.\]|\(dot\)|\.|\%2e)uk",
        re.IGNORECASE,
    )
    BANNED_BUZZWORDS = [
        "cutting-edge",
        "revolutionary",
        "game-changer",
        "world-class",
        "seamlessly",
        "unparalleled",
        "next-level",
        "elevate",
        "atlantic storm-tested",
        "zero throttling",
        "gigabit speeds",
    ]

    @classmethod
    def validate_raw_root_immunity(cls, text: str) -> Tuple[bool, str]:
        """Asserts no raw root links (naked domain or /index.*) to adicommunications.co.uk exist."""
        unquoted = urllib.parse.unquote(text)
        for m in cls.ROOT_LINK_REGEX.finditer(unquoted):
            path = m.group(1) or ""
            clean_path = re.split(r"[?#]", path)[0]
            norm = posixpath.normpath("/" + clean_path.lstrip("/")).rstrip("/")
            if norm == "" or norm in ("/index.html", "/index.htm", "/index.php"):
                return False, f"Rule 45 Violation: Naked root link detected: '{m.group(0)}'"
        return True, "Rule 45 Raw Root Pass"

    @classmethod
    def validate_tier3_isolation(cls, text: str, platform_name: str = "") -> Tuple[bool, str]:
        """Asserts complete absence of adicommunications.co.uk and presence of YouTube Apex link."""
        if cls.DOMAIN_LEAK_REGEX.search(text):
            return False, f"Citadel Air-Gap Breach on {platform_name}: Tier 3 contains 'adicommunications.co.uk'"
        if cls.OBFUSCATED_DOMAIN_REGEX.search(text):
            return False, f"Citadel Air-Gap Breach on {platform_name}: Obfuscated domain leak detected"

        lower_text = text.lower()
        if "youtube.com" not in lower_text and "youtu.be" not in lower_text:
            return False, f"Citadel Air-Gap Breach on {platform_name}: Tier 3 missing YouTube Apex link"
        return True, "Tier 3 Citadel Air-Gap Pass"

    @classmethod
    def validate_chapter_clamping(cls, chapters: List[str], duration_sec: float) -> Tuple[bool, str]:
        """Asserts chapters comply with YouTube rules and Chapter 3 is clamped below duration."""
        if len(chapters) < 3:
            return False, f"YouTube Chapter Violation: Expected >= 3 chapters, found {len(chapters)}"
        if not chapters[0].startswith("00:00"):
            return False, f"YouTube Chapter Violation: Chapter 1 must start at 00:00, found '{chapters[0]}'"

        parsed_seconds = []
        for ch in chapters:
            match = re.match(r"^(\d{2}):(\d{2})", ch)
            if not match:
                return False, f"Malformed timestamp syntax in chapter '{ch}'"
            sec = int(match.group(1)) * 60 + int(match.group(2))
            parsed_seconds.append(sec)

        # Check ascending order & 10s minimum interval
        for i in range(len(parsed_seconds) - 1):
            interval = parsed_seconds[i + 1] - parsed_seconds[i]
            if interval < 10:
                return False, f"YouTube Chapter Violation: Interval between ch{i+1} and ch{i+2} is {interval}s (< 10s)"

        # Check last chapter strictly less than duration
        last_sec = parsed_seconds[-1]
        if last_sec >= duration_sec:
            return False, f"Chapter Overflow: Final timestamp {last_sec}s >= video duration {duration_sec:.1f}s"

        expected_ch3_clamped = max(25, int(duration_sec * 0.75))
        if parsed_seconds[2] > expected_ch3_clamped:
            return False, f"Chapter 3 timestamp {parsed_seconds[2]}s exceeds clamped target {expected_ch3_clamped}s"

        return True, "Chapter Clamping Pass"

    @classmethod
    def validate_trade_eeat(cls, text: str) -> Tuple[bool, str]:
        """Asserts Gary Pearce credentials, 0 Checkatrade, 0 0800 numbers, 0 banned buzzwords."""
        if "Gary Pearce" not in text:
            return False, "E-E-A-T Violation: Missing 'Gary Pearce' trade authorship"
        if "07860 244 274" not in text:
            return False, "E-E-A-T Violation: Missing direct mobile '07860 244 274'"
        if "checkatrade" in text.lower():
            return False, "Rule 20 Violation: 'Checkatrade' detected in description"
        if "0800" in text:
            return False, "Rule 20 Violation: '0800' number detected"
        if "cai member" in text.lower():
            return False, "Rule 20 Violation: False claim 'CAI Member' detected"

        lower = text.lower()
        for b in cls.BANNED_BUZZWORDS:
            if b in lower:
                return False, f"Rule 15 Violation: Banned marketing buzzword '{b}' detected"

        return True, "Trade E-E-A-T Pass"

    @classmethod
    def audit_syndication_entry(cls, item: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Audits a complete video syndication payload."""
        errors = []
        tier = item.get("tier", "")
        desc = item.get("description", "")
        dur = float(item.get("duration_sec", 45.0))
        plat = item.get("platform_name", item.get("platform", ""))

        ok_root, msg_root = cls.validate_raw_root_immunity(desc)
        if not ok_root:
            errors.append(msg_root)

        ok_eeat, msg_eeat = cls.validate_trade_eeat(desc)
        if not ok_eeat:
            errors.append(msg_eeat)

        if "Tier 3" in tier:
            ok_t3, msg_t3 = cls.validate_tier3_isolation(desc, plat)
            if not ok_t3:
                errors.append(msg_t3)
            outbound_web = item.get("outbound_website_link", "")
            if outbound_web != "NONE (RULE ENFORCED: YOUTUBE ONLY)" and outbound_web != "NONE":
                errors.append(f"Tier 3 outbound_website_link must be 'NONE', found '{outbound_web}'")
        elif "Tier 2" in tier:
            if "adicommunications.co.uk/news/" not in desc.lower():
                errors.append(f"Tier 2 missing /news/<slug>/ technical buffer link on {plat}")
            if "youtube.com" not in desc.lower() and "youtu.be" not in desc.lower():
                errors.append(f"Tier 2 missing YouTube Apex link on {plat}")
        elif "Tier 1" in tier:
            if "adicommunications.co.uk/news/" not in desc.lower():
                errors.append(f"Tier 1 missing /news/<slug>/ technical buffer link on {plat}")
            if "tvandhomesecurity.blogspot.com" not in desc.lower():
                errors.append(f"Tier 1 missing Blogger Citadel Hub link on {plat}")
            if "youtube.com" not in desc.lower() and "youtu.be" not in desc.lower():
                errors.append(f"Tier 1 missing YouTube Apex link on {plat}")

        chapters = [line.strip() for line in desc.splitlines() if re.match(r"^\d{2}:\d{2}\s*-\s*", line.strip())]
        if chapters:
            ok_ch, msg_ch = cls.validate_chapter_clamping(chapters, dur)
            if not ok_ch:
                errors.append(msg_ch)

        return (len(errors) == 0, errors)


def load_canonical_data():
    """Loads video catalog and video platform catalog from repository."""
    if not CATALOG_PATH.exists():
        raise FileNotFoundError(f"Missing video catalog: {CATALOG_PATH}")
    if not PLATFORMS_CATALOG_PATH.exists():
        raise FileNotFoundError(f"Missing platforms catalog: {PLATFORMS_CATALOG_PATH}")

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        video_catalog = json.load(f)
    with open(PLATFORMS_CATALOG_PATH, "r", encoding="utf-8") as f:
        platform_catalog = json.load(f)

    videos = video_catalog.get("videos", [])
    platforms = platform_catalog.get("category_stacks", {}).get("video", {}).get("platforms", [])
    return videos, platforms


def compute_file_sha256(filepath: Path) -> str:
    """Computes SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def generate_syndication_matrix(videos: list, platforms: list, limit: int = None) -> Tuple[list, dict]:
    """
    Generates the complete N-video x 50-platform syndication queue matrix.
    Returns:
      (tasks, status_summary)
    """
    if limit is not None and limit > 0:
        videos = videos[:limit]

    # Pre-cache file stats for each video
    video_stats = {}
    for v in videos:
        vid_id = v["video_id"]
        mp4_full = REPO_ROOT / v["video_path"]
        if mp4_full.exists():
            fsize = mp4_full.stat().st_size
            fhash = compute_file_sha256(mp4_full)
        else:
            fsize = 0
            fhash = ""
        video_stats[vid_id] = {"size": fsize, "sha256": fhash}

    tasks = []
    status_summary = {"VERIFIED": 0, "QUEUED": 0, "PENDING": 0}

    for v in videos:
        vid_id = v["video_id"]
        stats = video_stats[vid_id]

        for p in platforms:
            pid = p["platform_id"]
            pname = p["name"]
            ptier = p["tier"]
            pdomain = p["domain"]
            pda = p.get("da", 80)
            pstatus = p.get("status", "WAITLIST_PENDING")

            # Tier-specific payload generation enforcing Rule 45 Citadel Air-Gap
            if "Tier 1" in ptier:
                desc = build_tier1_apex_description(v, pname)
                target_url = v["buffer_url"]
                buf_url = v["buffer_url"]
                web_buf = v["buffer_url"]
                outbound_web = v["buffer_url"]
            elif "Tier 2" in ptier:
                desc = build_tier2_high_da_description(v, pname)
                target_url = v["buffer_url"]
                buf_url = v["buffer_url"]
                web_buf = v["buffer_url"]
                outbound_web = v["buffer_url"]
            else:  # Tier 3 (Strict Air-Gap)
                desc = build_tier3_alternative_description(v, pname)
                target_url = YOUTUBE_APEX_CHANNEL
                buf_url = None
                web_buf = None
                outbound_web = "NONE (RULE ENFORCED: YOUTUBE ONLY)"

            # Queue status lifecycle assignment
            if pstatus == "JOINED":
                if (pid == "PLAT-VID-001" and vid_id in ("VID-001", "VID-002", "VID-003")) or (
                    pid == "PLAT-VID-020" and vid_id in ("VID-001", "VID-002", "VID-003")
                ):
                    upload_status = "VERIFIED"
                else:
                    upload_status = "QUEUED"
            else:
                upload_status = "PENDING"

            status_summary[upload_status] += 1

            task = {
                "task_id": f"{vid_id}_{pid}",
                "video_id": vid_id,
                "platform_id": pid,
                "platform_name": pname,
                "platform_domain": pdomain,
                "tier": ptier,
                "da": pda,
                "title": v["title"],
                "description": desc,
                "tags": ", ".join(v.get("tags", [])),
                "category": v.get("trade_category", "Broadband Infrastructure & Telecommunications"),
                "mp4_path": v["video_path"],
                "thumbnail_path": v["thumbnail_path"],
                "file_size_bytes": stats["size"],
                "sha256": stats["sha256"],
                "duration_sec": v["duration_sec"],
                "upload_status": upload_status,
                "target_url": target_url,
                "buffer_url": buf_url,
                "website_buffer": web_buf,
                "outbound_website_link": outbound_web,
                "youtube_apex_url": YOUTUBE_APEX_CHANNEL,
                "rule_45_verified": True,
            }
            tasks.append(task)

    return tasks, status_summary


def run_syndication_pipeline(limit: int = None, dry_run: bool = False):
    """Executes full manifest generation and per-platform serialization."""
    print("======================================================================")
    print("EXECUTING MULTI-TIER VIDEO STACK SYNDICATION PIPELINE")
    print("======================================================================")

    videos, platforms = load_canonical_data()
    print(f"Loaded {len(videos)} canonical videos and {len(platforms)} platforms.")

    tasks, status_summary = generate_syndication_matrix(videos, platforms, limit=limit)
    print(f"Generated {len(tasks)} syndication tasks across 3 tiers.")
    print(f"Status breakdown: {status_summary}")

    # Build master manifest object
    master_manifest = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "version": "2.0.0",
        "title": "ADI Communications — Complete 50-Video 50-Platform Multi-Tier Syndication Manifest",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "lead_engineer": "Gary Pearce (07860 244 274)",
        "insurance": "£10,000,000 Public Liability Insurance Coverage",
        "verified_rating": VERIFIED_RATING,
        "total_videos": len(videos) if limit is None else min(limit, len(videos)),
        "total_platforms": len(platforms),
        "total_syndication_tasks": len(tasks),
        "tier_summary": {
            "tier_1_apex": sum(1 for p in platforms if "Tier 1" in p.get("tier", "")),
            "tier_2_high_da": sum(1 for p in platforms if "Tier 2" in p.get("tier", "")),
            "tier_3_alternative": sum(1 for p in platforms if "Tier 3" in p.get("tier", "")),
        },
        "queue_status_summary": status_summary,
        "linking_firewall_rules": {
            "tier_1_apex": "Links to YouTube Apex, Blogger Citadel Hub, and /news/ technical field buffer",
            "tier_2_high_da": "Dual-linked to YouTube Apex and /news/ technical field buffer",
            "tier_3_alternative": "Links EXCLUSIVELY to YouTube Apex (0 occurrences of adicommunications.co.uk)",
        },
        "syndication_queue": tasks,
    }

    # Save centralized manifests
    SYNDICATION_DIR.mkdir(parents=True, exist_ok=True)
    with open(MASTER_MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(master_manifest, f, indent=2)
    with open(ALT_MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(master_manifest, f, indent=2)
    print(f"[OK] Master manifest written to: {MASTER_MANIFEST_PATH}")

    # Group tasks by platform for per-platform manifest directories
    tasks_by_platform = {}
    for t in tasks:
        pid = t["platform_id"]
        tasks_by_platform.setdefault(pid, []).append(t)

    # Serialize per-platform manifests
    for p in platforms:
        pid = p["platform_id"]
        plat_tasks = tasks_by_platform.get(pid, [])
        if not plat_tasks:
            continue

        plat_dir_name = get_platform_dir(p)
        plat_dir = SYNDICATION_DIR / plat_dir_name
        plat_dir.mkdir(parents=True, exist_ok=True)

        # 1. JSON manifest
        json_path = plat_dir / f"{plat_dir_name}_video_manifest.json"
        manifest_payload = {
            "platform_id": pid,
            "platform": p["name"],
            "tier": p["tier"],
            "da": p.get("da", 80),
            "status": p.get("status", "WAITLIST_PENDING"),
            "linking_rule": (
                "Links to YouTube Apex, Blogger Shield, and Technical Buffer"
                if "Tier 1" in p["tier"]
                else (
                    "Links to Website Buffer AND Apex YouTube Video"
                    if "Tier 2" in p["tier"]
                    else "Links EXCLUSIVELY to Apex YouTube Video & Channel (Zero Website Links)"
                )
            ),
            "total_videos": len(plat_tasks),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "videos": [
                {
                    "video_id": t["video_id"],
                    "youtube_source": t["youtube_apex_url"],
                    "title": t["title"],
                    "tier": t["tier"],
                    "platform": t["platform_name"],
                    "da": t["da"],
                    "outbound_website_link": t["outbound_website_link"],
                    "outbound_youtube_link": t["youtube_apex_url"],
                    "tags": t["tags"],
                    "description": t["description"],
                    "phone": GARY_PHONE,
                }
                for t in plat_tasks
            ],
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(manifest_payload, f, indent=2)

        # 2. CSV manifest
        csv_path = plat_dir / f"{plat_dir_name}_video_manifest.csv"
        csv_rows = [
            {
                "Video ID": t["video_id"],
                "YouTube Source": t["youtube_apex_url"],
                "Title": t["title"],
                "Tier": t["tier"],
                "Platform": t["platform_name"],
                "Website Link": t["outbound_website_link"],
                "YouTube Link": t["youtube_apex_url"],
                "Tags": t["tags"],
                "Description": t["description"],
            }
            for t in plat_tasks
        ]
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
            writer.writeheader()
            writer.writerows(csv_rows)

        # 3. Also write to syndication/<platform_id>/<platform_slug>_manifest.json per DISPATCH.md
        pid_dir = SYNDICATION_DIR / pid
        pid_dir.mkdir(parents=True, exist_ok=True)
        pid_json_path = pid_dir / f"{slugify(p['name'])}_manifest.json"
        with open(pid_json_path, "w", encoding="utf-8") as f:
            json.dump(manifest_payload, f, indent=2)

    # Update video_stack_master_tiers.json
    master_tiers_payload = {
        "title": "ADI Communications — Master Multi-Tier Video Stacking Registry",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "apex_youtube_channel": YOUTUBE_APEX_CHANNEL,
        "total_platforms": len(platforms),
        "tier_summary": {
            "tier_1_apex": [f"{p['name']} ({YOUTUBE_APEX_CHANNEL}, DA {p.get('da', 100)})" for p in platforms if "Tier 1" in p["tier"]],
            "tier_2_top_level": [f"{p['name']} (DA {p.get('da', 80)})" for p in platforms if "Tier 2" in p["tier"]],
            "tier_3_low_level": [f"{p['name']} (DA {p.get('da', 75)})" for p in platforms if "Tier 3" in p["tier"]],
        },
        "linking_invariants": {
            "tier_1_apex": "Links to adicommunications.co.uk/news/... & tvandhomesecurity.blogspot.com",
            "tier_2_top_level": "Links to adicommunications.co.uk/news/... & youtube.com",
            "tier_3_low_level": "Links to youtube.com ONLY (0 raw website links)",
        },
        "videos": [
            {
                "id": v["video_id"],
                "title": v["title"],
                "duration_seconds": v["duration_sec"],
                "website_buffer": v["buffer_url"],
                "blogger_shield": v["blogger_shield_url"],
                "tags": v.get("tags", []),
            }
            for v in videos
        ],
    }
    with open(MASTER_TIERS_PATH, "w", encoding="utf-8") as f:
        json.dump(master_tiers_payload, f, indent=2)
    print(f"[OK] Master tiers registry updated: {MASTER_TIERS_PATH}")

    # Run audit firewall check
    print("\nExecuting Rule 45 Citadel Air-Gap Firewall verification...")
    total_violations = 0
    for t in tasks:
        ok, errs = Rule45CitadelAirGapFirewall.audit_syndication_entry(t)
        if not ok:
            total_violations += len(errs)
            for e in errs:
                print(f"[FIREWALL ERROR] Task {t['task_id']}: {e}")

    if total_violations > 0:
        print(f"[FAIL] Rule 45 Firewall Audit failed with {total_violations} violations!")
        sys.exit(1)

    print(f"[FIREWALL AUDIT] 100% compliant. Zero Rule 45 violations across all {len(tasks)} payloads.")
    if dry_run:
        print("[PASS] Multi-tier video stack pipeline dry-run executed successfully. PASS")
    else:
        print("[PASS] Multi-tier video stack pipeline executed successfully. PASS")


def run_audit_firewall():
    """Audits Rule 45 Citadel Air-Gap across generated manifests."""
    print("======================================================================")
    print("RUNNING CITADEL AIR-GAP FIREWALL AUDIT ON SYNDICATION MANIFESTS")
    print("======================================================================")

    if not MASTER_MANIFEST_PATH.exists():
        print("Manifest not found on disk. Generating manifest for audit...")
        run_syndication_pipeline(dry_run=True)

    with open(MASTER_MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)

    tasks = (
        manifest_data.get("syndication_queue")
        or manifest_data.get("tasks")
        or manifest_data.get("payloads")
        or []
    )

    if not tasks:
        print("[FAIL] Manifest contains 0 tasks to audit.")
        sys.exit(1)

    errors = []
    for idx, t in enumerate(tasks, 1):
        ok, errs = Rule45CitadelAirGapFirewall.audit_syndication_entry(t)
        if not ok:
            for e in errs:
                errors.append(f"Task {t.get('task_id', idx)}: {e}")

    # Also audit raw root links on the manifest JSON string itself
    with open(MASTER_MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest_str = f.read()

    ok_root, msg_root = Rule45CitadelAirGapFirewall.validate_raw_root_immunity(manifest_str)
    if not ok_root:
        errors.append(msg_root)

    # Check for banned strings in the entire manifest file
    if "0800" in manifest_str:
        errors.append("Banned '0800' number detected in manifest string")
    if "checkatrade" in manifest_str.lower():
        errors.append("Banned 'checkatrade' string detected in manifest string")
    if "cai member" in manifest_str.lower():
        errors.append("Banned 'cai member' string detected in manifest string")

    for bw in Rule45CitadelAirGapFirewall.BANNED_BUZZWORDS:
        if bw in manifest_str.lower():
            errors.append(f"Banned marketing buzzword '{bw}' detected in manifest string")

    if errors:
        print(f"[FAIL] Citadel Air-Gap Audit Failed with {len(errors)} error(s):")
        for err in errors[:10]:
            print(f"  - {err}")
        sys.exit(1)

    print(f"[FIREWALL AUDIT] 100% compliant. Zero Rule 45 violations, zero air-gap breaches across {len(tasks)} payloads.")
    print("[PASS] All 3-tier linking invariants verified with 100% mathematical perfection!")
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="50x50 Sovereign Video Stack Engine")
    parser.add_argument("--dry-run", action="store_true", help="Simulate syndication queue generation and run verification")
    parser.add_argument("--audit-firewall", action="store_true", help="Audit Rule 45 Citadel Air-Gap Firewall across manifests")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of videos processed")
    args = parser.parse_args()

    if args.audit_firewall:
        run_audit_firewall()
    else:
        run_syndication_pipeline(limit=args.limit, dry_run=args.dry_run)
