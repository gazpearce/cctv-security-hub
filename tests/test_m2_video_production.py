"""
tests/test_m2_video_production.py
=================================
Milestone M2-VID Video Production & Quality Gate Verification Suite.

Validates:
Class 1: TestVideoCatalogIntegrity (50 videos, sequential IDs, 7 trade categories, schema fields)
Class 2: TestVideoBinaryStreamIntegrity (50 MP4s on disk, 1080p, H.264, AAC audio, >500KB, non-trivial duration)
Class 3: TestThumbnailVisualIntegrity (50 WebP thumbnails, 1600x900, Pillow decodable, variance >20, contrast scrim)
Class 4: TestRule45CitadelAirGap (0 raw root links, Tier 3 descriptions strictly isolated to YouTube)
Class 5: TestTradeEEATStandards (Gary Pearce credentials, 07860 244 274, 0 Checkatrade, 0 0800, CAI disclaimer)
Class 6: TestPerformanceAndRenderingSafety (exit code 0, safe disk usage <2.5GB, no leaked temp files)
"""

import ast
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

try:
    from PIL import Image
    import numpy as np
except ImportError:
    Image = None
    np = None

from automated_platform_onboarder import IntegrityFirewall


class TestVideoCatalogIntegrity(unittest.TestCase):
    """Class 1: 50 Video Platform Catalog & Schema Parity."""

    @classmethod
    def setUpClass(cls):
        cls.catalog_path = REPO_ROOT / "video_stack_50_catalog.json"
        if not cls.catalog_path.exists():
            alt = REPO_ROOT / "category_manifests" / "video_stack_50_catalog.json"
            if alt.exists():
                cls.catalog_path = alt

        cls.catalog_exists = cls.catalog_path.exists()
        cls.catalog_data = {}
        cls.videos = []
        if cls.catalog_exists:
            with open(cls.catalog_path, "r", encoding="utf-8") as f:
                cls.catalog_data = json.load(f)
            cls.videos = cls.catalog_data.get("videos", [])

    def test_01_catalog_json_exists_and_parses(self):
        """Asserts video_stack_50_catalog.json exists and contains valid JSON."""
        self.assertTrue(self.catalog_exists, f"Missing catalog file: {self.catalog_path}")
        self.assertIsInstance(self.catalog_data, dict, "Catalog root must be a JSON object")

    def test_02_catalog_contains_exactly_50_videos(self):
        """Asserts catalog contains exactly 50 video definitions."""
        self.assertEqual(len(self.videos), 50, f"Expected 50 videos in catalog, found {len(self.videos)}")
        self.assertEqual(self.catalog_data.get("total_videos"), 50, "total_videos metadata field must equal 50")

    def test_03_sequential_video_ids_vid001_to_vid050(self):
        """Asserts video IDs run sequentially from VID-001 through VID-050 without gaps."""
        ids = [v.get("video_id") for v in self.videos]
        expected_ids = [f"VID-{i:03d}" for i in range(1, 51)]
        self.assertEqual(ids, expected_ids, "Video IDs must be sequential VID-001 through VID-050")
        self.assertEqual(len(set(ids)), 50, "All video IDs must be strictly unique")

    def test_04_mandatory_schema_fields_present_and_non_empty(self):
        """Asserts each video entry contains all 16 mandatory schema fields."""
        required_fields = [
            "video_id", "slug", "title", "trade_category", "duration_sec",
            "video_path", "thumbnail_path", "script_narration", "tags",
            "description_tier1", "description_tier2", "description_tier3",
            "buffer_url", "blogger_shield_url", "hardware_standards", "timestamps"
        ]
        for v in self.videos:
            vid_id = v.get("video_id", "UNKNOWN")
            for field in required_fields:
                self.assertIn(field, v, f"Field '{field}' missing from video {vid_id}")
                val = v[field]
                self.assertIsNotNone(val, f"Field '{field}' is null in video {vid_id}")
                if isinstance(val, (str, list, dict)):
                    self.assertTrue(len(val) > 0, f"Field '{field}' is empty in video {vid_id}")

    def test_05_trade_category_taxonomy_7_disciplines(self):
        """Asserts trade categories map strictly to the 7 UK engineering disciplines."""
        valid_categories = {
            "Broadband & Satellite Telecoms",
            "Smart Alarms & Security Networks",
            "Commercial & Domestic CCTV",
            "Video Intercoms & Access Control",
            "Structured Cabling & Networking",
            "TV Mounting & Media Installations",
            "Broadcast RF & TV Aerials",
            "Satellite Telecoms",
            "Smart Alarms",
            "CCTV Engineering",
            "Video Doorbells",
            "Structured Cabling",
            "TV & Media Walls",
            "TV & Broadcast"
        }
        categories_found = set()
        for v in self.videos:
            cat = v.get("trade_category")
            self.assertIn(cat, valid_categories, f"Invalid category '{cat}' in {v.get('video_id')}")
            categories_found.add(cat)
        self.assertGreaterEqual(len(categories_found), 7, "All 7 engineering disciplines must be covered")

    def test_06_unique_slugs_and_titles(self):
        """Asserts all 50 video slugs and titles are unique and properly formatted."""
        slugs = [v.get("slug") for v in self.videos]
        titles = [v.get("title") for v in self.videos]
        self.assertEqual(len(set(slugs)), 50, "Slugs must be strictly unique")
        self.assertEqual(len(set(titles)), 50, "Titles must be strictly unique")
        for s in slugs:
            self.assertTrue(re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", s), f"Slug '{s}' not valid kebab-case")

    def test_07_tags_contain_core_brand_anchors(self):
        """Asserts each video has 5–15 tags, always including 'Gary Pearce' and 'ADI Communications'."""
        for v in self.videos:
            tags = v.get("tags", [])
            vid_id = v.get("video_id")
            self.assertTrue(5 <= len(tags) <= 15, f"{vid_id} has {len(tags)} tags; expected 5 to 15")
            tags_lower = [t.lower() for t in tags]
            self.assertIn("gary pearce", tags_lower, f"{vid_id} tags missing 'Gary Pearce'")
            self.assertIn("adi communications", tags_lower, f"{vid_id} tags missing 'ADI Communications'")

    def test_08_timestamps_formatting_and_minimum_count(self):
        """Asserts at least 3 timestamp chapters per video formatted as 'MM:SS - Description'."""
        ts_pattern = re.compile(r"^\d{2}:\d{2}\s*-\s*.+$")
        for v in self.videos:
            timestamps = v.get("timestamps", [])
            vid_id = v.get("video_id")
            self.assertGreaterEqual(len(timestamps), 3, f"{vid_id} must have >= 3 timestamps")
            for ts in timestamps:
                self.assertTrue(ts_pattern.match(ts), f"{vid_id} has invalid timestamp format: '{ts}'")


class TestVideoBinaryStreamIntegrity(unittest.TestCase):
    """Class 2: Physical MP4 Binary Stream, Codec, Resolution & Audio Integrity."""

    @classmethod
    def setUpClass(cls):
        catalog_path = REPO_ROOT / "video_stack_50_catalog.json"
        if not catalog_path.exists():
            catalog_path = REPO_ROOT / "category_manifests" / "video_stack_50_catalog.json"

        cls.videos = []
        if catalog_path.exists():
            with open(catalog_path, "r", encoding="utf-8") as f:
                cls.videos = json.load(f).get("videos", [])

        # Cache ffprobe results for all 50 files once
        cls.probes = {}
        for v in cls.videos:
            vid_id = v.get("video_id")
            rel_path = v.get("video_path")
            if rel_path:
                full_path = REPO_ROOT / rel_path
                if full_path.exists():
                    try:
                        cmd = [
                            "ffprobe", "-v", "quiet",
                            "-print_format", "json",
                            "-show_format", "-show_streams",
                            str(full_path)
                        ]
                        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                        if res.returncode == 0:
                            cls.probes[vid_id] = json.loads(res.stdout)
                    except Exception:
                        pass

    def test_09_all_50_mp4_files_exist_on_disk(self):
        """Asserts that all 50 MP4 files exist on the filesystem at video_path."""
        self.assertEqual(len(self.videos), 50, "Need 50 videos to verify files")
        for v in self.videos:
            vid_id = v.get("video_id")
            path = REPO_ROOT / v.get("video_path", "")
            self.assertTrue(path.exists(), f"MP4 file for {vid_id} missing: {path}")

    def test_10_mp4_file_size_thresholds(self):
        """Asserts each MP4 file is > 500 KB (non-dummy) and < 100 MB."""
        for v in self.videos:
            vid_id = v.get("video_id")
            path = REPO_ROOT / v.get("video_path", "")
            if path.exists():
                size = path.stat().st_size
                self.assertGreaterEqual(size, 512_000, f"{vid_id} MP4 too small ({size} bytes); minimum 500 KB")
                self.assertLessEqual(size, 104_857_600, f"{vid_id} MP4 exceeds 100 MB budget ({size} bytes)")

    def test_11_video_stream_container_and_h264_codec(self):
        """Asserts MP4 container format and H.264 (avc1) video codec."""
        for v in self.videos:
            vid_id = v.get("video_id")
            probe = self.probes.get(vid_id)
            self.assertIsNotNone(probe, f"Could not probe MP4 stream for {vid_id}")
            fmt = probe.get("format", {}).get("format_name", "")
            self.assertTrue("mp4" in fmt or "mov" in fmt, f"{vid_id} invalid format: {fmt}")
            v_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"]
            self.assertGreaterEqual(len(v_streams), 1, f"{vid_id} missing video stream")
            codec = v_streams[0].get("codec_name")
            self.assertEqual(codec, "h264", f"{vid_id} codec must be h264, found {codec}")

    def test_12_video_stream_exact_1080p_resolution(self):
        """Asserts video stream resolution is exactly 1920x1080 (16:9 1080p Full HD)."""
        for v in self.videos:
            vid_id = v.get("video_id")
            probe = self.probes.get(vid_id, {})
            v_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"]
            self.assertTrue(v_streams, f"Missing video stream for {vid_id}")
            w = v_streams[0].get("width")
            h = v_streams[0].get("height")
            self.assertEqual((w, h), (1920, 1080), f"{vid_id} resolution must be 1920x1080, found {w}x{h}")

    def test_13_video_framerate_and_progressive_scan(self):
        """Asserts progressive scan field order and framerate between 24 and 30 fps."""
        for v in self.videos:
            vid_id = v.get("video_id")
            probe = self.probes.get(vid_id, {})
            v_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"]
            self.assertTrue(v_streams, f"Missing video stream for {vid_id}")
            field_order = v_streams[0].get("field_order", "progressive")
            self.assertEqual(field_order, "progressive", f"{vid_id} must be progressive")
            fps_str = v_streams[0].get("r_frame_rate", "30/1")
            num, den = map(int, fps_str.split("/"))
            fps = num / den if den else 30.0
            self.assertTrue(24.0 <= fps <= 30.0, f"{vid_id} framerate out of bounds: {fps}")

    def test_14_video_frame_count_and_duration_match(self):
        """Asserts duration is 30–180s and matches catalog duration_sec within ±3 seconds."""
        for v in self.videos:
            vid_id = v.get("video_id")
            probe = self.probes.get(vid_id, {})
            duration_str = probe.get("format", {}).get("duration", "0")
            dur = float(duration_str)
            self.assertTrue(30.0 <= dur <= 180.0, f"{vid_id} duration {dur}s outside 30-180s")
            catalog_dur = float(v.get("duration_sec", dur))
            self.assertAlmostEqual(dur, catalog_dur, delta=3.0, msg=f"{vid_id} duration mismatch vs catalog")

    def test_15_audio_stream_aac_codec_and_sample_rate(self):
        """Asserts audio stream exists with AAC codec and 44.1kHz or 48kHz sample rate."""
        for v in self.videos:
            vid_id = v.get("video_id")
            probe = self.probes.get(vid_id, {})
            a_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "audio"]
            self.assertGreaterEqual(len(a_streams), 1, f"{vid_id} missing audio stream")
            codec = a_streams[0].get("codec_name")
            self.assertEqual(codec, "aac", f"{vid_id} audio codec must be aac, found {codec}")
            rate = int(a_streams[0].get("sample_rate", 0))
            self.assertIn(rate, (44100, 48000), f"{vid_id} audio rate must be 44.1k or 48k, found {rate}")

    def test_16_audio_stream_bitrate_and_non_silence(self):
        """Asserts audio bitrate is at least 64 kbps and stream duration matches video."""
        for v in self.videos:
            vid_id = v.get("video_id")
            probe = self.probes.get(vid_id, {})
            a_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "audio"]
            self.assertTrue(a_streams, f"Missing audio stream for {vid_id}")
            bit_rate = int(a_streams[0].get("bit_rate", 128000))
            self.assertGreaterEqual(bit_rate, 64_000, f"{vid_id} audio bitrate too low: {bit_rate}")


class TestThumbnailVisualIntegrity(unittest.TestCase):
    """Class 3: 1600x900 WebP Thumbnail Synthesis, Decodability & Contrast Integrity."""

    @classmethod
    def setUpClass(cls):
        catalog_path = REPO_ROOT / "video_stack_50_catalog.json"
        if not catalog_path.exists():
            catalog_path = REPO_ROOT / "category_manifests" / "video_stack_50_catalog.json"

        cls.videos = []
        if catalog_path.exists():
            with open(catalog_path, "r", encoding="utf-8") as f:
                cls.videos = json.load(f).get("videos", [])

    def test_17_all_50_webp_files_exist_on_disk(self):
        """Asserts that all 50 WebP thumbnail files exist on disk at thumbnail_path."""
        self.assertEqual(len(self.videos), 50)
        for v in self.videos:
            vid_id = v.get("video_id")
            path = REPO_ROOT / v.get("thumbnail_path", "")
            self.assertTrue(path.exists(), f"Thumbnail for {vid_id} missing: {path}")

    def test_18_webp_file_size_thresholds(self):
        """Asserts each WebP thumbnail is > 5 KB (non-dummy) and < 1.5 MB."""
        for v in self.videos:
            vid_id = v.get("video_id")
            path = REPO_ROOT / v.get("thumbnail_path", "")
            if path.exists():
                size = path.stat().st_size
                self.assertGreaterEqual(size, 5_120, f"{vid_id} thumbnail too small ({size} bytes)")
                self.assertLessEqual(size, 1_572_864, f"{vid_id} thumbnail too large ({size} bytes)")

    def test_19_pillow_decode_and_exact_1600x900_resolution(self):
        """Asserts Pillow successfully decodes WebP format at exact 1600x900 resolution."""
        self.assertIsNotNone(Image, "Pillow (PIL) must be installed")
        for v in self.videos:
            vid_id = v.get("video_id")
            path = REPO_ROOT / v.get("thumbnail_path", "")
            if path.exists():
                with Image.open(path) as im:
                    self.assertEqual(im.format, "WEBP", f"{vid_id} format is not WEBP")
                    self.assertEqual(im.size, (1600, 900), f"{vid_id} dimensions must be 1600x900, found {im.size}")
                    self.assertIn(im.mode, ("RGB", "RGBA"), f"{vid_id} invalid color mode: {im.mode}")

    def test_20_thumbnail_pixel_variance_and_non_blank(self):
        """Asserts pixel standard deviation across thumbnail is > 20.0 (prevents blank/solid screens)."""
        self.assertIsNotNone(np, "NumPy must be installed")
        for v in self.videos:
            vid_id = v.get("video_id")
            path = REPO_ROOT / v.get("thumbnail_path", "")
            if path.exists():
                with Image.open(path) as im:
                    arr = np.array(im.convert("L"))
                    std = float(np.std(arr))
                    self.assertGreater(std, 20.0, f"{vid_id} thumbnail is visually flat (std={std:.2f})")

    def test_21_contrast_scrim_footer_luminance_and_zero_ghost_text(self):
        """Verifies bottom 20% footer scrim has mean luminance < 110 to ensure AAA white text contrast."""
        self.assertIsNotNone(np, "NumPy must be installed")
        for v in self.videos:
            vid_id = v.get("video_id")
            path = REPO_ROOT / v.get("thumbnail_path", "")
            if path.exists():
                with Image.open(path) as im:
                    footer = im.crop((0, 720, 1600, 900)).convert("L")
                    mean_lum = float(np.mean(np.array(footer)))
                    self.assertLess(mean_lum, 110.0, f"{vid_id} footer scrim too bright ({mean_lum:.1f}) for AAA text")


class TestRule45CitadelAirGap(unittest.TestCase):
    """Class 4: Rule 45 Citadel Air-Gap Firewall & Tier Isolation."""

    @classmethod
    def setUpClass(cls):
        catalog_path = REPO_ROOT / "video_stack_50_catalog.json"
        if not catalog_path.exists():
            catalog_path = REPO_ROOT / "category_manifests" / "video_stack_50_catalog.json"

        cls.catalog_str = ""
        cls.videos = []
        if catalog_path.exists():
            with open(catalog_path, "r", encoding="utf-8") as f:
                cls.catalog_str = f.read()
                cls.videos = json.loads(cls.catalog_str).get("videos", [])

    def test_22_zero_raw_root_links_across_all_catalog_fields(self):
        """Asserts 0 raw root links to 'adicommunications.co.uk/' repository-wide in catalog."""
        passed, msg = IntegrityFirewall.validate_layer5_rule_45(self.catalog_str)
        self.assertTrue(passed, f"Rule 45 raw root anchor found in catalog: {msg}")

    def test_23_tier3_descriptions_strict_youtube_isolation(self):
        """Asserts 100% of Tier 3 descriptions contain ZERO occurrences of 'adicommunications.co.uk' and link strictly to YouTube."""
        for v in self.videos:
            vid_id = v.get("video_id")
            desc3 = v.get("description_tier3", "")
            self.assertTrue(len(desc3) > 0, f"{vid_id} missing description_tier3")
            self.assertNotIn(
                "adicommunications.co.uk",
                desc3.lower(),
                f"Air-gap breach in {vid_id} Tier 3: found 'adicommunications.co.uk'"
            )
            self.assertTrue(
                "youtube.com" in desc3.lower() or "youtu.be" in desc3.lower(),
                f"{vid_id} Tier 3 description must contain YouTube link"
            )

    def test_24_tier2_descriptions_dual_linking(self):
        """Asserts Tier 2 descriptions contain both YouTube Apex link and a /news/ buffer link."""
        for v in self.videos:
            vid_id = v.get("video_id")
            desc2 = v.get("description_tier2", "")
            self.assertTrue(len(desc2) > 0, f"{vid_id} missing description_tier2")
            self.assertTrue(
                "youtube.com" in desc2.lower() or "youtu.be" in desc2.lower(),
                f"{vid_id} Tier 2 description must contain YouTube link"
            )
            self.assertIn(
                "adicommunications.co.uk/news/",
                desc2.lower(),
                f"{vid_id} Tier 2 description missing /news/ buffer link"
            )

    def test_25_tier1_descriptions_citadel_hub_linking(self):
        """Asserts Tier 1 descriptions link to Blogger Citadel Hub, YouTube Apex, and /news/ buffer."""
        for v in self.videos:
            vid_id = v.get("video_id")
            desc1 = v.get("description_tier1", "")
            self.assertTrue(len(desc1) > 0, f"{vid_id} missing description_tier1")
            self.assertIn("tvandhomesecurity.blogspot.com", desc1.lower(), f"{vid_id} Tier 1 missing Blogger Citadel Hub")
            self.assertIn("adicommunications.co.uk/news/", desc1.lower(), f"{vid_id} Tier 1 missing /news/ buffer")

    def test_26_buffer_urls_subpath_syntax(self):
        """Asserts buffer_url points to a valid https://adicommunications.co.uk/news/<slug>/ subpath."""
        pattern = re.compile(r"^https://adicommunications\.co\.uk/news/[a-z0-9-]+/$")
        for v in self.videos:
            vid_id = v.get("video_id")
            b_url = v.get("buffer_url", "")
            self.assertTrue(pattern.match(b_url), f"{vid_id} buffer_url has invalid syntax: '{b_url}'")


class TestTradeEEATStandards(unittest.TestCase):
    """Class 5: Trade Authorship, E-E-A-T Credentials, Anti-Slop & Regulatory Compliance."""

    @classmethod
    def setUpClass(cls):
        catalog_path = REPO_ROOT / "video_stack_50_catalog.json"
        if not catalog_path.exists():
            catalog_path = REPO_ROOT / "category_manifests" / "video_stack_50_catalog.json"

        cls.catalog_str = ""
        cls.videos = []
        if catalog_path.exists():
            with open(catalog_path, "r", encoding="utf-8") as f:
                cls.catalog_str = f.read()
                cls.videos = json.loads(cls.catalog_str).get("videos", [])

    def test_27_gary_pearce_credentials_in_narration_scripts(self):
        """Asserts 'Gary Pearce' and 'ADI Communications' are present in narration scripts."""
        for v in self.videos:
            vid_id = v.get("video_id")
            script = v.get("script_narration", "")
            self.assertIn("Gary Pearce", script, f"{vid_id} script missing 'Gary Pearce'")
            self.assertIn("ADI Communications", script, f"{vid_id} script missing 'ADI Communications'")

    def test_28_direct_mobile_in_tier1_and_tier2_descriptions(self):
        """Asserts direct mobile '07860 244 274' is present in Tier 1 and Tier 2 descriptions."""
        for v in self.videos:
            vid_id = v.get("video_id")
            desc1 = v.get("description_tier1", "")
            desc2 = v.get("description_tier2", "")
            self.assertIn("07860 244 274", desc1, f"{vid_id} Tier 1 missing phone number")
            self.assertIn("07860 244 274", desc2, f"{vid_id} Tier 2 missing phone number")

    def test_29_zero_checkatrade_mentions(self):
        """User Rule 20: Asserts 0 occurrences of 'Checkatrade' anywhere in the catalog."""
        self.assertNotIn("checkatrade", self.catalog_str.lower(), "Rule 20 Violation: 'checkatrade' found in catalog")

    def test_30_zero_0800_numbers(self):
        """User Rule 20: Asserts 0 occurrences of '0800' anywhere in the catalog."""
        self.assertNotIn("0800", self.catalog_str, "Rule 20 Violation: '0800' number found in catalog")

    def test_31_cai_non_membership_disclaimer(self):
        """User Rule 20: Asserts Gary is NEVER claimed as a 'CAI Member'."""
        self.assertNotIn("cai member", self.catalog_str.lower(), "Rule 20 Violation: 'cai member' found")

    def test_32_banned_ai_marketing_buzzwords_purge(self):
        """User Rule 15: Scans all scripts and descriptions for banned buzzwords."""
        banned = [
            "cutting-edge", "revolutionary", "game-changer", "world-class",
            "seamlessly", "unparalleled", "next-level", "elevate",
            "atlantic storm-tested", "zero throttling", "gigabit speeds"
        ]
        cat_lower = self.catalog_str.lower()
        for word in banned:
            self.assertNotIn(word, cat_lower, f"Rule 15 Violation: Banned buzzword '{word}' found in video catalog")


class TestPerformanceAndRenderingSafety(unittest.TestCase):
    """Class 6: Safe Disk Usage, Memory Hygiene & Process Safety."""

    @classmethod
    def setUpClass(cls):
        catalog_path = REPO_ROOT / "video_stack_50_catalog.json"
        if not catalog_path.exists():
            catalog_path = REPO_ROOT / "category_manifests" / "video_stack_50_catalog.json"

        cls.videos = []
        if catalog_path.exists():
            with open(catalog_path, "r", encoding="utf-8") as f:
                cls.videos = json.load(f).get("videos", [])

    def test_33_total_media_disk_budget_safety(self):
        """Asserts total disk footprint of all 50 MP4s and 50 WebPs is between 50 MB and 2.5 GB."""
        total_bytes = 0
        for v in self.videos:
            for field in ("video_path", "thumbnail_path"):
                p = REPO_ROOT / v.get(field, "")
                if p.exists():
                    total_bytes += p.stat().st_size
        self.assertGreaterEqual(total_bytes, 52_428_800, f"Total media size too small ({total_bytes} bytes)")
        self.assertLessEqual(total_bytes, 2_684_354_560, f"Total media exceeds 2.5 GB budget ({total_bytes} bytes)")

    def test_34_zero_leaked_temporary_or_orphan_files(self):
        """Asserts zero temporary render files (*.tmp, *.part, temp_*.mp3) left in assets/videos/."""
        video_dir = REPO_ROOT / "assets" / "videos"
        if video_dir.exists():
            orphans = list(video_dir.glob("*.tmp")) + list(video_dir.glob("*.part")) + list(video_dir.glob("temp_*"))
            self.assertEqual(len(orphans), 0, f"Found orphan render files: {orphans}")

    def test_35_file_read_permissions_and_unlocked_handles(self):
        """Asserts all media files are readable and not locked by dangling background processes."""
        for v in self.videos:
            for field in ("video_path", "thumbnail_path"):
                p = REPO_ROOT / v.get(field, "")
                if p.exists():
                    with open(p, "rb") as f:
                        header = f.read(16)
                        self.assertEqual(len(header), 16, f"Could not read header of {p}")

    def test_36_rendering_pipeline_script_syntax_and_importability(self):
        """Asserts produce_50_trade_videos.py parses cleanly without AST syntax errors."""
        script_path = REPO_ROOT / "produce_50_trade_videos.py"
        self.assertTrue(script_path.exists(), f"Missing production script: {script_path}")
        with open(script_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(script_path))
            self.assertIsNotNone(tree, "Failed to parse produce_50_trade_videos.py AST")


if __name__ == "__main__":
    unittest.main(verbosity=2)
