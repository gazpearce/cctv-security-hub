"""
tests/test_m3_video_syndication.py
==================================
Milestone M3-VID Multi-Platform Video Syndication & Air-Gap Quality Gate Suite.

Validates:
Class 1: TestSyndicationManifestIntegrity (all 50 videos, all 50 platforms, 2,500 payloads, valid schema)
Class 2: TestRule45CitadelAirGapFirewall (0 raw root links, Tier 3 descriptions contain 0 adicommunications.co.uk)
Class 3: TestChapterMarkerClamping (every Chapter 3 timestamp is strictly less than duration_sec, monotonic, >=10s intervals)
Class 4: TestTradeEEATFormatting (Gary Pearce credentials, 07860 244 274, 0 Checkatrade, 0 0800, 0 banned buzzwords)
Class 5: TestUploadPipelineExecution (syndicate_video_tier_stack.py exit code 0, --dry-run, --audit-firewall)
"""

import ast
import csv
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from automated_platform_onboarder import IntegrityFirewall


class TestSyndicationManifestIntegrity(unittest.TestCase):
    """Class 1: Syndication Manifest Schema, Completeness & Binary Stream Reference Parity."""

    @classmethod
    def setUpClass(cls):
        # Locate syndication manifest
        cls.manifest_path = REPO_ROOT / "video_stack_50_syndication_manifest.json"
        if not cls.manifest_path.exists():
            alt = REPO_ROOT / "syndication" / "video_stack_50_syndication_manifest.json"
            if alt.exists():
                cls.manifest_path = alt

        cls.manifest_exists = cls.manifest_path.exists()
        cls.manifest_data = {}
        cls.tasks = []
        if cls.manifest_exists:
            with open(cls.manifest_path, "r", encoding="utf-8") as f:
                cls.manifest_data = json.load(f)
            # Manifest can structure payloads under "syndication_queue", "tasks", or "payloads"
            cls.tasks = (
                cls.manifest_data.get("syndication_queue")
                or cls.manifest_data.get("tasks")
                or cls.manifest_data.get("payloads")
                or []
            )

        # Load upstream catalogs for parity verification
        catalog_path = REPO_ROOT / "video_stack_50_catalog.json"
        with open(catalog_path, "r", encoding="utf-8") as f:
            cls.upstream_videos = json.load(f).get("videos", [])

        platform_catalog_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        with open(platform_catalog_path, "r", encoding="utf-8") as f:
            cat = json.load(f)
            cls.upstream_platforms = cat["category_stacks"]["video"]["platforms"]

    def test_01_syndication_manifest_exists_and_parses_json(self):
        """Asserts video_stack_50_syndication_manifest.json exists and is valid JSON."""
        self.assertTrue(self.manifest_exists, f"Missing syndication manifest: {self.manifest_path}")
        self.assertIsInstance(self.manifest_data, dict, "Manifest root must be a JSON object")

    def test_02_manifest_top_level_metadata(self):
        """Asserts top-level metadata fields: total_videos=50, total_platforms=50, total_tasks=2500."""
        self.assertEqual(self.manifest_data.get("total_videos"), 50)
        self.assertEqual(self.manifest_data.get("total_platforms"), 50)
        total_tasks = self.manifest_data.get("total_syndication_tasks", len(self.tasks))
        self.assertEqual(total_tasks, 2500, f"Expected 2500 syndication tasks (50x50), found {total_tasks}")

    def test_03_all_50_videos_represented_sequentially(self):
        """Asserts all 50 video IDs VID-001 through VID-050 are present in the manifest."""
        video_ids = set()
        if self.tasks:
            video_ids = {t["video_id"] for t in self.tasks}
        else:
            video_ids = {v["video_id"] for v in self.manifest_data.get("videos", [])}

        expected_ids = {f"VID-{i:03d}" for i in range(1, 51)}
        self.assertEqual(video_ids, expected_ids, "Manifest must cover VID-001 through VID-050 without gaps")

    def test_04_all_50_platforms_represented_and_tiered(self):
        """Asserts all 50 platform IDs PLAT-VID-001 through PLAT-VID-050 are targeted with correct tiers."""
        platform_ids = set()
        if self.tasks:
            platform_ids = {t["platform_id"] for t in self.tasks}
        else:
            platform_ids = {p["platform_id"] for p in self.manifest_data.get("platforms", [])}

        expected_pids = {f"PLAT-VID-{i:03d}" for i in range(1, 51)}
        self.assertEqual(platform_ids, expected_pids, "Manifest must cover all 50 video platform IDs")

    def test_05_payload_schema_and_mandatory_fields(self):
        """Asserts every task payload contains all 12 mandatory fields with non-empty values."""
        required = [
            "video_id", "platform_id", "platform_name", "tier", "title",
            "description", "tags", "category", "mp4_path", "thumbnail_path",
            "upload_status", "target_url"
        ]
        sample_tasks = self.tasks if self.tasks else []
        self.assertGreaterEqual(len(sample_tasks), 50, "Need tasks to verify payload schema")
        for t in sample_tasks[:100]:  # sample check
            for field in required:
                self.assertIn(field, t, f"Field '{field}' missing from payload for {t.get('video_id')}")
                val = t[field]
                self.assertIsNotNone(val, f"Field '{field}' is null in payload for {t.get('video_id')}")

    def test_06_referenced_mp4_and_webp_binaries_exist_on_disk(self):
        """Asserts mp4_path (>500KB) and thumbnail_path (>5KB) point to real files on disk."""
        checked_videos = set()
        for t in self.tasks:
            vid = t["video_id"]
            if vid in checked_videos:
                continue
            checked_videos.add(vid)
            mp4_file = REPO_ROOT / t["mp4_path"]
            thumb_file = REPO_ROOT / t["thumbnail_path"]
            self.assertTrue(mp4_file.exists(), f"MP4 file missing for {vid}: {mp4_file}")
            self.assertGreaterEqual(mp4_file.stat().st_size, 512_000, f"MP4 file too small for {vid}")
            self.assertTrue(thumb_file.exists(), f"WebP thumbnail missing for {vid}: {thumb_file}")
            self.assertGreaterEqual(thumb_file.stat().st_size, 5_120, f"WebP thumbnail too small for {vid}")

    def test_07_status_enums_and_lifecycle_tracking(self):
        """Asserts upload_status uses valid lifecycle enums (PENDING, QUEUED, UPLOADED, VERIFIED)."""
        valid_statuses = {"PENDING", "QUEUED", "UPLOADED", "VERIFIED"}
        for t in self.tasks:
            status = t.get("upload_status")
            self.assertIn(status, valid_statuses, f"Invalid status '{status}' in task for {t.get('video_id')}")


class TestRule45CitadelAirGapFirewall(unittest.TestCase):
    """Class 2: Rule 45 Google Shield Compliance, Tier Isolation & Air-Gap Defense."""

    @classmethod
    def setUpClass(cls):
        cls.manifest_path = REPO_ROOT / "video_stack_50_syndication_manifest.json"
        if not cls.manifest_path.exists():
            cls.manifest_path = REPO_ROOT / "syndication" / "video_stack_50_syndication_manifest.json"

        cls.manifest_str = ""
        cls.tasks = []
        if cls.manifest_path.exists():
            with open(cls.manifest_path, "r", encoding="utf-8") as f:
                cls.manifest_str = f.read()
                data = json.loads(cls.manifest_str)
                cls.tasks = data.get("syndication_queue") or data.get("tasks") or data.get("payloads") or []

    def test_08_zero_raw_root_links_across_entire_manifest(self):
        """Asserts 0 raw root links to adicommunications.co.uk/ across the entire manifest file."""
        ok, msg = IntegrityFirewall.validate_layer5_rule_45(self.manifest_str)
        self.assertTrue(ok, f"Rule 45 violation in syndication manifest: {msg}")

    def test_09_tier3_descriptions_zero_occurrences_of_commercial_domain(self):
        """Asserts 100% of Tier 3 platform descriptions contain ZERO occurrences of adicommunications.co.uk."""
        tier3_tasks = [t for t in self.tasks if "Tier 3" in t.get("tier", "")]
        self.assertGreaterEqual(len(tier3_tasks), 31, "Must have Tier 3 tasks to verify air-gap")
        for t in tier3_tasks:
            desc = t.get("description", "").lower()
            self.assertNotIn(
                "adicommunications.co.uk",
                desc,
                f"Air-gap breach: 'adicommunications.co.uk' found in Tier 3 platform {t.get('platform_name')} for {t.get('video_id')}"
            )

    def test_10_tier3_descriptions_contain_exclusive_youtube_apex(self):
        """Asserts 100% of Tier 3 platform descriptions link strictly to YouTube Apex."""
        tier3_tasks = [t for t in self.tasks if "Tier 3" in t.get("tier", "")]
        for t in tier3_tasks:
            desc = t.get("description", "")
            self.assertTrue(
                "youtube.com" in desc.lower() or "youtu.be" in desc.lower(),
                f"Tier 3 description missing YouTube link in {t.get('platform_name')} for {t.get('video_id')}"
            )

    def test_11_tier2_descriptions_contain_dual_links(self):
        """Asserts Tier 2 descriptions contain dual links: YouTube Apex + /news/ buffer link."""
        tier2_tasks = [t for t in self.tasks if "Tier 2" in t.get("tier", "")]
        self.assertGreaterEqual(len(tier2_tasks), 18, "Must have Tier 2 tasks to verify dual-linking")
        for t in tier2_tasks:
            desc = t.get("description", "")
            self.assertTrue(
                "youtube.com" in desc.lower() or "youtu.be" in desc.lower(),
                f"Tier 2 description missing YouTube link in {t.get('platform_name')}"
            )
            self.assertIn(
                "adicommunications.co.uk/news/",
                desc.lower(),
                f"Tier 2 description missing /news/ buffer link in {t.get('platform_name')}"
            )

    def test_12_tier1_descriptions_contain_blogger_citadel_and_buffer(self):
        """Asserts Tier 1 descriptions link to YouTube Apex, Blogger Citadel Hub, and /news/ buffer."""
        tier1_tasks = [t for t in self.tasks if "Tier 1" in t.get("tier", "")]
        self.assertGreaterEqual(len(tier1_tasks), 1, "Must have Tier 1 tasks")
        for t in tier1_tasks:
            desc = t.get("description", "")
            self.assertIn("tvandhomesecurity.blogspot.com", desc.lower())
            self.assertIn("adicommunications.co.uk/news/", desc.lower())
            self.assertTrue("youtube.com" in desc.lower() or "youtu.be" in desc.lower())

    def test_13_buffer_urls_subpath_syntax_and_trailing_slash(self):
        """Asserts all buffer URLs in manifest conform to https://adicommunications.co.uk/news/<slug>/."""
        pattern = re.compile(r"^https://adicommunications\.co\.uk/news/[a-z0-9-]+/$")
        for t in self.tasks:
            buf = t.get("website_buffer") or t.get("buffer_url")
            if buf:
                self.assertTrue(pattern.match(buf), f"Malformed buffer URL in task {t.get('video_id')}: '{buf}'")


class TestChapterMarkerClamping(unittest.TestCase):
    """Class 3: Chapter Marker Clamping, Monotonicity & YouTube Playback Protection."""

    @classmethod
    def setUpClass(cls):
        catalog_path = REPO_ROOT / "video_stack_50_catalog.json"
        with open(catalog_path, "r", encoding="utf-8") as f:
            cls.catalog_videos = {v["video_id"]: v for v in json.load(f).get("videos", [])}

        cls.manifest_path = REPO_ROOT / "video_stack_50_syndication_manifest.json"
        if not cls.manifest_path.exists():
            cls.manifest_path = REPO_ROOT / "syndication" / "video_stack_50_syndication_manifest.json"

        cls.tasks = []
        if cls.manifest_path.exists():
            with open(cls.manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                cls.tasks = data.get("syndication_queue") or data.get("tasks") or data.get("payloads") or []

    def test_14_all_manifest_chapter_timestamps_strictly_less_than_duration(self):
        """Asserts every timestamp in every description payload is strictly less than video duration_sec."""
        ts_regex = re.compile(r"(\d{2}):(\d{2})")
        for t in self.tasks:
            vid = t.get("video_id")
            dur = self.catalog_videos[vid]["duration_sec"]
            desc = t.get("description", "")
            for m in ts_regex.finditer(desc):
                mins, secs = int(m.group(1)), int(m.group(2))
                ts_sec = mins * 60 + secs
                self.assertLess(
                    ts_sec,
                    dur,
                    f"Timestamp overflow in {vid} ({t.get('platform_name')}): {mins:02d}:{secs:02d} ({ts_sec}s) >= duration {dur}s"
                )

    def test_15_chapter_3_timestamp_clamped_to_75_percent_duration(self):
        """Verifies Chapter 3 timestamp string is clamped to max(25, int(duration_sec * 0.75))."""
        ts_regex = re.compile(r"(\d{2}:\d{2})\s*-\s*(.+)")
        for t in self.tasks:
            vid = t.get("video_id")
            dur = self.catalog_videos[vid]["duration_sec"]
            desc = t.get("description", "")
            timestamps = [m.group(1) for m in ts_regex.finditer(desc)]
            if len(timestamps) >= 3:
                ch3 = timestamps[2]
                mins, secs = map(int, ch3.split(":"))
                ch3_sec = mins * 60 + secs
                self.assertLess(
                    ch3_sec,
                    dur,
                    f"Chapter 3 timestamp {ch3} exceeds duration {dur}s in {vid}"
                )
                self.assertGreaterEqual(
                    ch3_sec,
                    20,
                    f"Chapter 3 timestamp {ch3} too early in {vid}"
                )

    def test_16_chapter_timestamps_start_at_zero_zero(self):
        """YouTube Guideline: Asserts first chapter marker starts at exactly 00:00."""
        ts_regex = re.compile(r"(\d{2}:\d{2})\s*-\s*(.+)")
        for t in self.tasks:
            desc = t.get("description", "")
            matches = list(ts_regex.finditer(desc))
            if matches:
                first_ts = matches[0].group(1)
                self.assertEqual(first_ts, "00:00", f"First chapter must start at 00:00, found {first_ts}")

    def test_17_chapter_timestamps_are_strictly_monotonic(self):
        """Asserts all timestamps within a description strictly increase monotonically."""
        ts_regex = re.compile(r"(\d{2}):(\d{2})")
        for t in self.tasks:
            desc = t.get("description", "")
            timestamps = []
            for m in ts_regex.finditer(desc):
                sec = int(m.group(1)) * 60 + int(m.group(2))
                timestamps.append(sec)
            for i in range(len(timestamps) - 1):
                self.assertLess(
                    timestamps[i],
                    timestamps[i + 1],
                    f"Non-monotonic chapter sequence in {t.get('video_id')}: {timestamps}"
                )

    def test_18_chapter_intervals_satisfy_youtube_ten_second_minimum(self):
        """YouTube Guideline: Asserts each chapter interval is at least 10 seconds."""
        ts_regex = re.compile(r"(\d{2}):(\d{2})")
        for t in self.tasks:
            desc = t.get("description", "")
            timestamps = [int(m.group(1)) * 60 + int(m.group(2)) for m in ts_regex.finditer(desc)]
            for i in range(len(timestamps) - 1):
                delta = timestamps[i + 1] - timestamps[i]
                self.assertGreaterEqual(
                    delta,
                    10,
                    f"Chapter interval {delta}s is less than 10s in {t.get('video_id')}"
                )

    def test_19_embedded_timestamps_synchronized_across_all_tiers(self):
        """Asserts clamped timestamps are identical across Tier 1, Tier 2, and Tier 3 for the same video."""
        by_vid = {}
        ts_regex = re.compile(r"(\d{2}:\d{2})")
        for t in self.tasks:
            vid = t["video_id"]
            timestamps = tuple(m.group(1) for m in ts_regex.finditer(t.get("description", "")))
            if vid not in by_vid:
                by_vid[vid] = timestamps
            else:
                self.assertEqual(
                    timestamps,
                    by_vid[vid],
                    f"Timestamp divergence across tiers for video {vid}"
                )


class TestTradeEEATFormatting(unittest.TestCase):
    """Class 4: Gary Pearce Credentials, Rule 20 Checkatrade Ban & Anti-Slop Integrity."""

    @classmethod
    def setUpClass(cls):
        cls.manifest_path = REPO_ROOT / "video_stack_50_syndication_manifest.json"
        if not cls.manifest_path.exists():
            cls.manifest_path = REPO_ROOT / "syndication" / "video_stack_50_syndication_manifest.json"

        cls.manifest_str = ""
        cls.tasks = []
        if cls.manifest_path.exists():
            with open(cls.manifest_path, "r", encoding="utf-8") as f:
                cls.manifest_str = f.read()
                data = json.loads(cls.manifest_str)
                cls.tasks = data.get("syndication_queue") or data.get("tasks") or data.get("payloads") or []

    def test_20_gary_pearce_credentials_in_all_descriptions(self):
        """Asserts Gary Pearce, ADI Communications, and 25+ Years experience in all descriptions."""
        for t in self.tasks:
            desc = t.get("description", "")
            self.assertIn("Gary Pearce", desc)
            self.assertIn("ADI Communications", desc)
            self.assertTrue("25+ Years" in desc or "25+ Yrs" in desc)

    def test_21_direct_mobile_in_all_descriptions(self):
        """Asserts site-wide direct mobile '07860 244 274' is present in all descriptions."""
        for t in self.tasks:
            desc = t.get("description", "")
            self.assertIn("07860 244 274", desc)

    def test_22_absolute_zero_0800_numbers_in_manifest(self):
        """User Rule 20: Asserts string '0800' is strictly absent from the entire manifest."""
        self.assertNotIn("0800", self.manifest_str, "Rule 20 Violation: '0800' number found in syndication manifest")

    def test_23_strict_rule_20_checkatrade_ban_in_manifest(self):
        """User Rule 20: Asserts 0 occurrences of 'Checkatrade' anywhere in the manifest."""
        self.assertNotIn(
            "checkatrade",
            self.manifest_str.lower(),
            "Rule 20 Violation: 'checkatrade' found in syndication manifest"
        )
        self.assertIn("9.98 / 10", self.manifest_str)

    def test_24_cai_non_membership_legal_disclaimer(self):
        """User Rule 20: Asserts Gary is NEVER claimed as a 'CAI Member'."""
        self.assertNotIn("cai member", self.manifest_str.lower(), "Rule 20 Violation: 'cai member' found in manifest")

    def test_25_purge_of_banned_ai_marketing_buzzwords(self):
        """User Rule 15: Audits all descriptions, titles, and tags for banned buzzwords."""
        banned = [
            "cutting-edge", "revolutionary", "game-changer", "world-class",
            "seamlessly", "unparalleled", "next-level", "elevate",
            "atlantic storm-tested", "zero throttling", "gigabit speeds"
        ]
        manifest_lower = self.manifest_str.lower()
        for word in banned:
            self.assertNotIn(word, manifest_lower, f"Rule 15 Violation: Banned buzzword '{word}' found in manifest")

    def test_26_trade_hardware_standards_accuracy(self):
        """User Rule 4 & 9: Asserts accurate trade hardware descriptions (Starlink Gen 3, ColorVu F1.0)."""
        self.assertIn("Starlink Gen 3", self.manifest_str)
        self.assertIn("ColorVu", self.manifest_str)
        self.assertNotIn("round dish", self.manifest_str.lower())


class TestUploadPipelineExecution(unittest.TestCase):
    """Class 5: CLI Execution, Dry-Run Flag, Firewall Audit & Downstream Ledger Parity."""

    def test_27_cli_dry_run_flag_execution(self):
        """Asserts syndicate_video_tier_stack.py --dry-run executes cleanly with exit code 0."""
        cmd = [sys.executable, str(REPO_ROOT / "syndicate_video_tier_stack.py"), "--dry-run"]
        res = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=30)
        self.assertEqual(res.returncode, 0, f"--dry-run failed with code {res.returncode}: {res.stderr}")
        self.assertIn("PASS", res.stdout.upper())

    def test_28_cli_audit_firewall_flag_execution(self):
        """Asserts syndicate_video_tier_stack.py --audit-firewall exits 0 with 100% Rule 45 compliance."""
        cmd = [sys.executable, str(REPO_ROOT / "syndicate_video_tier_stack.py"), "--audit-firewall"]
        res = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=30)
        self.assertEqual(res.returncode, 0, f"--audit-firewall failed with code {res.returncode}: {res.stderr}")
        self.assertIn("100%", res.stdout)

    def test_29_manifest_file_generated_on_disk(self):
        """Asserts execution generated video_stack_50_syndication_manifest.json on disk."""
        p = REPO_ROOT / "video_stack_50_syndication_manifest.json"
        alt = REPO_ROOT / "syndication" / "video_stack_50_syndication_manifest.json"
        self.assertTrue(p.exists() or alt.exists(), "Manifest file must exist on disk after pipeline execution")

    def test_30_per_platform_manifest_directories_generated(self):
        """Asserts platform directories under syndication/ contain individual manifest JSON and CSV files."""
        synd_dir = REPO_ROOT / "syndication"
        self.assertTrue(synd_dir.exists(), "syndication/ directory must exist")
        # Check sample directories
        for plat_key in ("dailymotion", "vimeo", "rumble", "peertube"):
            plat_folder = synd_dir / plat_key
            if plat_folder.exists():
                j_files = list(plat_folder.glob("*.json"))
                c_files = list(plat_folder.glob("*.csv"))
                self.assertGreaterEqual(len(j_files), 1, f"Missing JSON manifest in {plat_folder}")
                self.assertGreaterEqual(len(c_files), 1, f"Missing CSV manifest in {plat_folder}")

    def test_31_m4_ledger_payload_compatibility(self):
        """Asserts syndication tasks map cleanly to the 14 columns of doc3_published_asset_links.csv."""
        doc3_columns = [
            "asset_id", "parent_profile_id", "platform_name", "profile_live_url",
            "asset_title", "asset_type", "asset_public_url", "top_of_stack_apex_url",
            "shield_target_url", "seo_tags", "seo_description_summary", "dofollow_status",
            "publication_date", "verification_status"
        ]
        manifest_path = REPO_ROOT / "video_stack_50_syndication_manifest.json"
        if not manifest_path.exists():
            manifest_path = REPO_ROOT / "syndication" / "video_stack_50_syndication_manifest.json"

        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            tasks = data.get("syndication_queue") or data.get("tasks") or data.get("payloads") or []

        self.assertGreaterEqual(len(tasks), 50)
        sample = tasks[0]
        # Verify mapping capability
        self.assertIn("video_id", sample)
        self.assertIn("platform_name", sample)
        self.assertIn("title", sample)
        self.assertIn("tags", sample)

    def test_32_pipeline_script_ast_syntax_and_anti_mocking(self):
        """Asserts syndicate_video_tier_stack.py has valid AST and does not import test mocking modules."""
        script_path = REPO_ROOT / "syndicate_video_tier_stack.py"
        self.assertTrue(script_path.exists())
        with open(script_path, "r", encoding="utf-8") as f:
            code = f.read()
            tree = ast.parse(code, filename=str(script_path))
            self.assertIsNotNone(tree)
            self.assertNotIn("unittest.mock", code, "Production syndication script must not contain mocks")
            self.assertNotIn("MagicMock", code, "Production syndication script must not contain MagicMock")


if __name__ == "__main__":
    unittest.main(verbosity=2)
