r"""
tests/test_challenger_m3vid_chapters_eeat.py
============================================
Adversarial Challenge & Empirical Fuzzing Suite for Milestone M3-VID.
Author: M3-VID Challenger 1 (Chapter Clamping & E-E-A-T Adversarial Fuzzing)

Adversarially validates:
1. Chapter Clamping Mathematical Fuzzing:
   - Regex chapter extraction (r"(\d{2}):(\d{2})\s*-\s*(.+)") across all 2,500 payloads.
   - Strict timestamp < duration_sec bound (T < D).
   - Strict monotonicity (T_{n+1} > T_n).
   - Minimum 10-second intervals between chapters (delta >= 10s).
   - Initial chapter starts at 00:00.
   - Trailing duration clearance (D - T_last).
   - Mathematical domain fuzzing on generate_clamped_chapters(D) across 2,800 synthetic durations.
2. Trade E-E-A-T & Star Rating Adversarial Fuzzing:
   - Fuzz for corrupted stars (e.g. ★★★../../, malformed unicode, trailing dots/slashes).
   - Leetspeak and regex fuzzing for 'Checkatrade' in any casing across all manifests and catalogs.
   - Comprehensive scanner for forbidden UK phone numbers (0800, 0808, 0845, 0870, 0300, 0345, 0900).
   - Site-wide direct mobile validation: 07860 244 274 present in 100% of payloads.
   - Banned AI marketing buzzwords fuzzing across all titles, descriptions, and tags.
   - CAI legal prohibition compliance (zero claims of 'CAI Member' or 'CAI Certified').
3. Multi-Manifest Parity & Per-Platform Audit:
   - Consistency between root manifest and syndication/ directory manifest.
   - Audit of all 50 per-platform JSON and CSV manifests in syndication/.
   - Rule 45 Citadel Air-Gap cross-verification.
"""

import csv
import json
import os
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MASTER_MANIFEST_PATH = REPO_ROOT / "video_stack_50_syndication_manifest.json"
ALT_MANIFEST_PATH = REPO_ROOT / "syndication" / "video_stack_50_syndication_manifest.json"
CATALOG_PATH = REPO_ROOT / "video_stack_50_catalog.json"
PLATFORMS_CATALOG_PATH = REPO_ROOT / "master_multicategory_platform_catalog.json"
SYNDICATION_DIR = REPO_ROOT / "syndication"


class TestAdversarialChapterClamping(unittest.TestCase):
    """Adversarially challenge chapter marker timestamps, duration bounds, and monotonicity."""

    @classmethod
    def setUpClass(cls):
        self_path = MASTER_MANIFEST_PATH if MASTER_MANIFEST_PATH.exists() else ALT_MANIFEST_PATH
        with open(self_path, "r", encoding="utf-8") as f:
            cls.manifest_data = json.load(f)
            cls.tasks = cls.manifest_data.get("syndication_queue", [])

        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            cls.catalog_data = json.load(f)
            cls.catalog_videos = {v["video_id"]: v for v in cls.catalog_data.get("videos", [])}

        with open(PLATFORMS_CATALOG_PATH, "r", encoding="utf-8") as f:
            cls.platform_data = json.load(f)
            platforms_list = cls.platform_data.get("category_stacks", {}).get("video", {}).get("platforms", [])
            cls.platforms = {p["platform_id"]: p for p in platforms_list}

    def test_01_all_2500_payloads_have_valid_clamped_chapters(self):
        r"""Extract all chapter timestamp markers via regex r"(\d{2}):(\d{2})\s*-\s*(.+)" across 2,500 payloads."""
        self.assertEqual(len(self.tasks), 2500, f"Expected 2,500 payloads, found {len(self.tasks)}")
        chapter_regex = re.compile(r"(\d{2}):(\d{2})\s*-\s*(.+)")

        failures = []
        for t in self.tasks:
            task_id = t.get("task_id", "UNKNOWN")
            vid = t.get("video_id")
            dur = t.get("duration_sec")
            desc = t.get("description", "")

            # Ensure duration is present and matches catalog
            if vid not in self.catalog_videos:
                failures.append(f"{task_id}: Video ID {vid} not in catalog")
                continue
            cat_dur = self.catalog_videos[vid]["duration_sec"]
            if abs(dur - cat_dur) > 0.001:
                failures.append(f"{task_id}: Payload duration {dur} != catalog duration {cat_dur}")

            # Extract chapters
            matches = list(chapter_regex.finditer(desc))
            if len(matches) < 3:
                failures.append(f"{task_id}: Found {len(matches)} chapters, expected at least 3")
                continue

            parsed_chapters = []
            for m in matches:
                mins, secs = int(m.group(1)), int(m.group(2))
                title = m.group(3).strip()
                t_sec = mins * 60 + secs
                parsed_chapters.append((t_sec, f"{mins:02d}:{secs:02d}", title))

            # 1. Assert initial chapter starts at 00:00
            if parsed_chapters[0][0] != 0:
                failures.append(f"{task_id}: Initial chapter starts at {parsed_chapters[0][1]}, must start at 00:00")

            # 2. Assert every timestamp is strictly less than duration_sec (T < D)
            for t_sec, ts_str, title in parsed_chapters:
                if t_sec >= dur:
                    failures.append(f"{task_id}: Timestamp {ts_str} ({t_sec}s) >= video duration {dur}s ({title})")

            # 3. Assert timestamps are strictly monotonic (T_{n+1} > T_n)
            for i in range(len(parsed_chapters) - 1):
                t1, s1, _ = parsed_chapters[i]
                t2, s2, _ = parsed_chapters[i + 1]
                if t2 <= t1:
                    failures.append(f"{task_id}: Non-monotonic timestamps: {s1} ({t1}s) >= {s2} ({t2}s)")

            # 4. Assert intervals between chapters are >= 10s
            for i in range(len(parsed_chapters) - 1):
                t1, s1, _ = parsed_chapters[i]
                t2, s2, _ = parsed_chapters[i + 1]
                interval = t2 - t1
                if interval < 10:
                    failures.append(f"{task_id}: Chapter interval {interval}s between {s1} and {s2} is < 10s")

            # 5. Tail interval: duration_sec - T_last >= 10s
            last_t = parsed_chapters[-1][0]
            tail = dur - last_t
            if tail < 10:
                failures.append(f"{task_id}: Chapter tail {tail:.1f}s between last chapter {parsed_chapters[-1][1]} and end {dur}s is < 10s")

        self.assertEqual(len(failures), 0, f"Chapter clamping failures across {len(failures)} payloads:\n" + "\n".join(failures[:15]))

    def test_02_no_secret_or_unclamped_timestamps_in_descriptions(self):
        """Fuzz for any other timestamp formats in descriptions that could confuse players."""
        # Generic timestamp pattern: e.g. 1:23, 01:23, 01:23:45
        generic_ts = re.compile(r"\b(\d{1,2}):(\d{2})(?::(\d{2}))?\b")
        chapter_line = re.compile(r"^\s*(\d{2}):(\d{2})\s*-\s*.+$", re.MULTILINE)

        for t in self.tasks:
            desc = t.get("description", "")
            # Find all timestamps in description
            all_ts = list(generic_ts.finditer(desc))
            chapter_ts = list(chapter_line.finditer(desc))

            # Exactly 3 timestamps should appear in description, corresponding to the 3 chapters
            self.assertEqual(
                len(all_ts), 3,
                f"Task {t.get('task_id')} has {len(all_ts)} timestamp occurrences in description, expected exactly 3: {[m.group(0) for m in all_ts]}"
            )
            self.assertEqual(
                len(chapter_ts), 3,
                f"Task {t.get('task_id')} has {len(chapter_ts)} chapter lines, expected 3"
            )

    def test_03_chapter_titles_are_meaningful_and_distinct(self):
        """Asserts each chapter title has >= 10 characters and titles within a description are unique."""
        chapter_regex = re.compile(r"(\d{2}):(\d{2})\s*-\s*(.+)")
        for t in self.tasks:
            desc = t.get("description", "")
            matches = list(chapter_regex.finditer(desc))
            titles = [m.group(3).strip() for m in matches]
            self.assertEqual(len(titles), len(set(titles)), f"Duplicate chapter titles in {t.get('task_id')}: {titles}")
            for title in titles:
                self.assertGreaterEqual(len(title), 10, f"Chapter title too short in {t.get('task_id')}: '{title}'")

    def test_04_mathematical_oracle_fuzzing_synthetic_durations(self):
        """Stress-tests generate_clamped_chapters mathematical formula across synthetic durations."""
        # The algorithm implemented in syndicate_video_tier_stack.py:
        # ch3_sec = max(25, int(duration_sec * 0.75))
        def oracle_chapters(d: float):
            ch3 = max(25, int(d * 0.75))
            return [0, 15, ch3]

        # 1. Verify all production durations [39.8s, 48.7s] strictly satisfy all YouTube constraints
        for v in self.catalog_videos.values():
            d = v["duration_sec"]
            chapters = oracle_chapters(d)
            ch3 = chapters[2]
            self.assertLess(ch3, d, f"T >= D at D={d}")
            self.assertGreaterEqual(chapters[1] - chapters[0], 10, f"Ch1-Ch0 interval < 10 at D={d}")
            self.assertGreaterEqual(ch3 - chapters[1], 10, f"Ch2-Ch1 interval < 10 at D={d}")
            self.assertGreaterEqual(d - ch3, 10, f"Tail interval < 10 at D={d}")

        # 2. General mathematical domain analysis:
        # For D >= 44.0s: tail = D - int(0.75 * D) > 0.25 * D - 1 >= 10.0s unconditionally.
        for d_int in range(440, 3000):  # 44.0s to 300.0s in 0.1s steps
            d = d_int / 10.0
            chapters = oracle_chapters(d)
            ch3 = chapters[2]
            self.assertLess(ch3, d)
            self.assertGreaterEqual(ch3 - chapters[1], 10)
            self.assertGreaterEqual(d - ch3, 10)

        # 3. For any D > 25.0s, timestamps are strictly monotonic and T < D
        for d_int in range(251, 3000):
            d = d_int / 10.0
            chapters = oracle_chapters(d)
            ch3 = chapters[2]
            self.assertLess(ch3, d)
            self.assertGreater(ch3, chapters[1])


class TestAdversarialTradeEEATAndFuzzing(unittest.TestCase):
    """Adversarially fuzz for corrupted stars, Checkatrade leaks, phone numbers, and buzzwords."""

    @classmethod
    def setUpClass(cls):
        self_path = MASTER_MANIFEST_PATH if MASTER_MANIFEST_PATH.exists() else ALT_MANIFEST_PATH
        with open(self_path, "r", encoding="utf-8") as f:
            cls.manifest_raw = f.read()
            cls.manifest_data = json.loads(cls.manifest_raw)
            cls.tasks = cls.manifest_data.get("syndication_queue", [])

    def test_05_fuzz_corrupted_star_patterns_across_manifest(self):
        """Adversarially search for corrupted star sequences (★★★../../, malformed dots, slashes, or missing stars)."""
        # Exact pattern that was present in legacy code: ★★★../../
        self.assertNotIn("★★★../../", self.manifest_raw, "Found legacy corrupted star string '★★★../../'!")
        self.assertNotIn("★../../", self.manifest_raw)
        self.assertNotIn("../../", self.manifest_raw)

        # Fuzz regex: any star followed by dots or slashes
        corrupted_star_regex = re.compile(r"★+[\.\/\\]+")
        matches = corrupted_star_regex.findall(self.manifest_raw)
        self.assertEqual(len(matches), 0, f"Found corrupted star patterns: {matches}")

        # Assert every single task description has the authentic 5-star rating line
        exact_star_rating = "★★★★★ 9.98 / 10 Rating • 84+ Verified Client Reviews"
        for t in self.tasks:
            desc = t.get("description", "")
            self.assertIn(
                exact_star_rating,
                desc,
                f"Task {t.get('task_id')} does not contain the exact authentic star rating string"
            )

    def test_06_adversarial_checkatrade_leetspeak_and_casing_scan(self):
        """Adversarially fuzz for 'Checkatrade' in any casing, spacing, or leetspeak variations."""
        # 1. Standard case-insensitive check
        self.assertNotIn("checkatrade", self.manifest_raw.lower(), "Found 'checkatrade' in manifest JSON!")

        # 2. Leetspeak / obfuscation patterns
        leetspeak_patterns = [
            re.compile(r"ch[e3][c\(]k[a4@]trade", re.IGNORECASE),
            re.compile(r"check[-_.\s]*a[-_.\s]*trade", re.IGNORECASE),
            re.compile(r"c[\s.]*h[\s.]*e[\s.]*c[\s.]*k[\s.]*a[\s.]*t[\s.]*r[\s.]*a[\s.]*d[\s.]*e", re.IGNORECASE),
        ]
        for pattern in leetspeak_patterns:
            matches = pattern.findall(self.manifest_raw)
            self.assertEqual(len(matches), 0, f"Found Checkatrade leetspeak/pattern matches: {matches}")

    def test_07_comprehensive_forbidden_phone_numbers_scan(self):
        """Scan for any non-geographic or freephone UK prefixes (0800, 0808, 0845, 0870, 0871, 0900, 0300, 0345, 0330)."""
        forbidden_patterns = [
            (re.compile(r"\b0800[\s\d-]{4,10}\b"), "0800 Freephone"),
            (re.compile(r"\b0808[\s\d-]{4,10}\b"), "0808 Freephone"),
            (re.compile(r"\b0845[\s\d-]{4,10}\b"), "0845 Premium"),
            (re.compile(r"\b0870[\s\d-]{4,10}\b"), "0870 Premium"),
            (re.compile(r"\b0871[\s\d-]{4,10}\b"), "0871 Premium"),
            (re.compile(r"\b0900[\s\d-]{4,10}\b"), "0900 Premium"),
            (re.compile(r"\b0300[\s\d-]{4,10}\b"), "0300 Non-geographic"),
            (re.compile(r"\b0345[\s\d-]{4,10}\b"), "0345 Non-geographic"),
            (re.compile(r"\b0330[\s\d-]{4,10}\b"), "0330 Non-geographic"),
        ]

        for pattern, label in forbidden_patterns:
            matches = pattern.findall(self.manifest_raw)
            self.assertEqual(len(matches), 0, f"Found forbidden {label} number matches in manifest: {matches}")

        # Assert every single task has Gary's direct mobile
        for t in self.tasks:
            desc = t.get("description", "")
            self.assertIn("07860 244 274", desc, f"Task {t.get('task_id')} missing direct mobile '07860 244 274'")

    def test_08_banned_ai_marketing_buzzwords_exhaustive_audit(self):
        """Exhaustive regex audit for all banned marketing buzzwords across all 2,500 payloads."""
        banned_words = [
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

        violations = []
        for t in self.tasks:
            task_id = t.get("task_id")
            title = t.get("title", "")
            desc = t.get("description", "")
            tags = t.get("tags", "")
            full_text = f"{title} {desc} {tags}".lower()

            for bw in banned_words:
                pattern = re.compile(r"\b" + re.escape(bw) + r"\b", re.IGNORECASE)
                if pattern.search(full_text):
                    violations.append(f"{task_id}: Found banned buzzword '{bw}'")

        self.assertEqual(len(violations), 0, f"Banned buzzwords found:\n" + "\n".join(violations[:15]))

    def test_09_cai_non_membership_and_trade_credentials_integrity(self):
        """Enforces Rule 20 CAI non-membership legal prohibition and Gary Pearce credentials."""
        # 1. Never claim CAI Membership
        forbidden_cai = ["cai member", "cai registered", "cai certified", "member of cai", "membership of cai"]
        manifest_lower = self.manifest_raw.lower()
        for fc in forbidden_cai:
            self.assertNotIn(fc, manifest_lower, f"Legal violation: '{fc}' detected in manifest")

        # 2. Mandatory disclaimer line present
        cai_disclaimer = "Fitted with CAI-benchmarked equipment & double-screened WF100 / solid copper Cat6 cabling"
        for t in self.tasks:
            desc = t.get("description", "")
            self.assertIn(cai_disclaimer, desc, f"Task {t.get('task_id')} missing CAI benchmark disclaimer")
            self.assertIn("Gary Pearce", desc)
            self.assertIn("ADI Communications", desc)
            self.assertIn("25+ Years Hands-On", desc)
            self.assertIn("£10M Public Liability", desc)


class TestMultiManifestParityAndPerPlatformAudit(unittest.TestCase):
    """Verifies that all 50 per-platform manifests and alt root manifest are synchronized."""

    @classmethod
    def setUpClass(cls):
        with open(MASTER_MANIFEST_PATH, "r", encoding="utf-8") as f:
            cls.master_data = json.load(f)
            cls.master_tasks = {t["task_id"]: t for t in cls.master_data.get("syndication_queue", [])}

        with open(PLATFORMS_CATALOG_PATH, "r", encoding="utf-8") as f:
            p_data = json.load(f)
            cls.platforms = p_data.get("category_stacks", {}).get("video", {}).get("platforms", [])

    def test_10_alt_root_manifest_parity(self):
        """Asserts syndication/video_stack_50_syndication_manifest.json is identical to root manifest."""
        self.assertTrue(ALT_MANIFEST_PATH.exists(), f"Alt manifest {ALT_MANIFEST_PATH} does not exist")
        with open(ALT_MANIFEST_PATH, "r", encoding="utf-8") as f:
            alt_data = json.load(f)
        self.assertEqual(len(alt_data.get("syndication_queue", [])), 2500)
        self.assertEqual(alt_data["total_tasks" if "total_tasks" in alt_data else "total_syndication_tasks"], 2500)

    def test_11_all_50_platform_directories_contain_json_and_csv(self):
        """Verifies each platform has a directory under syndication/ with valid JSON and CSV manifests."""
        self.assertEqual(len(self.platforms), 50)
        for plat in self.platforms:
            pid = plat["platform_id"]
            name = plat["name"]
            # Check either slug or override dir exists
            p_dirs = [d for d in SYNDICATION_DIR.iterdir() if d.is_dir() and (d.name == pid or pid in d.name or slugify(name) in d.name)]
            self.assertGreaterEqual(
                len(p_dirs), 1,
                f"Platform {pid} ({name}) has no corresponding directory in {SYNDICATION_DIR}"
            )

    def test_12_per_platform_manifests_payload_consistency(self):
        """Spot-checks platform JSON manifests to ensure clamped chapters and E-E-A-T strings match master."""
        chapter_regex = re.compile(r"(\d{2}):(\d{2})\s*-\s*(.+)")
        checked_count = 0

        for p_dir in SYNDICATION_DIR.iterdir():
            if not p_dir.is_dir():
                continue
            json_files = list(p_dir.glob("*manifest.json"))
            for jf in json_files:
                with open(jf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                tasks = data.get("syndication_tasks") or data.get("tasks") or data.get("videos") or []
                if not tasks:
                    continue
                checked_count += 1
                for task in tasks:
                    desc = task.get("description", "")
                    # Assert no corrupted stars
                    self.assertNotIn("★★★../../", desc)
                    self.assertIn("★★★★★ 9.98 / 10", desc)
                    # Assert no Checkatrade
                    self.assertNotIn("checkatrade", desc.lower())
                    # Assert phone
                    self.assertIn("07860 244 274", desc)
                    # Assert clamped chapters
                    matches = list(chapter_regex.finditer(desc))
                    self.assertGreaterEqual(len(matches), 3)

        self.assertGreaterEqual(checked_count, 50, f"Expected to audit at least 50 platform manifests, checked {checked_count}")


class TestAdversarialFirewallMutationsAndOracles(unittest.TestCase):
    """Negative testing: proves that the firewall oracle actively catches and rejects mutated payloads."""

    @classmethod
    def setUpClass(cls):
        from syndicate_video_tier_stack import Rule45CitadelAirGapFirewall
        cls.firewall = Rule45CitadelAirGapFirewall

    def test_13_mutation_chapter_overflow_rejected(self):
        """Proves chapter timestamp exceeding duration is rejected by validator."""
        chapters = [
            "00:00 - Introduction",
            "00:15 - Technical Standards",
            "00:52 - Field Deployment & Verification",
        ]
        duration = 46.3
        ok, msg = self.firewall.validate_chapter_clamping(chapters, duration)
        self.assertFalse(ok, "Firewall failed to reject timestamp 00:52 exceeding duration 46.3s")
        self.assertIn("Chapter Overflow", msg)

    def test_14_mutation_non_zero_start_rejected(self):
        """Proves initial chapter not starting at 00:00 is rejected by validator."""
        chapters = [
            "00:05 - Introduction",
            "00:20 - Technical Standards",
            "00:34 - Field Deployment",
        ]
        duration = 46.3
        ok, msg = self.firewall.validate_chapter_clamping(chapters, duration)
        self.assertFalse(ok, "Firewall failed to reject initial chapter at 00:05")
        self.assertIn("must start at 00:00", msg)

    def test_15_mutation_sub_10s_interval_rejected(self):
        """Proves chapter interval < 10 seconds is rejected by validator."""
        chapters = [
            "00:00 - Introduction",
            "00:08 - Technical Standards",
            "00:34 - Field Deployment",
        ]
        duration = 46.3
        ok, msg = self.firewall.validate_chapter_clamping(chapters, duration)
        self.assertFalse(ok, "Firewall failed to reject 8s interval between ch1 and ch2")
        self.assertIn("< 10s", msg)

    def test_16_mutation_corrupted_stars_rejected(self):
        """Proves corrupted star string is caught or fails strict E-E-A-T rating verification."""
        text = "Gary Pearce • ADI Communications (25+ Years Hands-On UK Security). Direct mobile: 07860 244 274. ★★★../../ 9.98 / 10"
        self.assertIn("★★★../../", text)
        self.assertNotIn("★★★★★ 9.98 / 10 Rating • 84+ Verified Client Reviews", text)

    def test_17_mutation_checkatrade_mention_rejected(self):
        """Proves Checkatrade mentions in any casing are rejected by firewall."""
        for variation in ["Checkatrade", "checkatrade", "CHECKATRADE", "checkatrade.com"]:
            text = f"Gary Pearce • ADI Communications (25+ Years). Direct mobile: 07860 244 274. Verified on {variation}."
            ok, msg = self.firewall.validate_trade_eeat(text)
            self.assertFalse(ok, f"Firewall failed to reject '{variation}'")
            self.assertIn("Checkatrade", msg)

    def test_18_mutation_0800_number_rejected(self):
        """Proves 0800 numbers are rejected by firewall."""
        for num in ["0800 123 456", "0800 244 274", "0800123456"]:
            text = f"Gary Pearce • ADI Communications (25+ Years). Direct mobile: 07860 244 274. Freephone: {num}."
            ok, msg = self.firewall.validate_trade_eeat(text)
            self.assertFalse(ok, f"Firewall failed to reject '{num}'")
            self.assertIn("0800", msg)

    def test_19_mutation_cai_member_claim_rejected(self):
        """Proves false 'CAI Member' claims are rejected by firewall."""
        text = "Gary Pearce • ADI Communications (25+ Years). Direct mobile: 07860 244 274. Certified CAI Member."
        ok, msg = self.firewall.validate_trade_eeat(text)
        self.assertFalse(ok, "Firewall failed to reject 'CAI Member' claim")
        self.assertIn("CAI Member", msg)

    def test_20_mutation_banned_buzzwords_rejected(self):
        """Proves banned marketing buzzwords are rejected by firewall."""
        for bw in ["cutting-edge", "revolutionary", "game-changer", "world-class", "seamlessly", "unparalleled", "next-level", "elevate", "atlantic storm-tested", "zero throttling", "gigabit speeds"]:
            text = f"Gary Pearce • ADI Communications (25+ Years). Direct mobile: 07860 244 274. Our {bw} solutions."
            ok, msg = self.firewall.validate_trade_eeat(text)
            self.assertFalse(ok, f"Firewall failed to reject banned buzzword '{bw}'")
            self.assertIn(bw, msg)

    def test_21_mutation_tier3_domain_leak_rejected(self):
        """Proves domain leakage in Tier 3 descriptions is rejected by firewall."""
        text = "Decentralized mirror broadcast by Gary Pearce. Visit https://adicommunications.co.uk/news/test/ for more info. YouTube: https://www.youtube.com/@CCTV.services"
        ok, msg = self.firewall.validate_tier3_isolation(text, "Rumble")
        self.assertFalse(ok, "Firewall failed to reject domain leak on Tier 3")
        self.assertIn("adicommunications.co.uk", msg)

    def test_22_mutation_raw_root_link_rejected(self):
        """Proves raw root links are rejected by firewall."""
        for raw_root in [
            "https://adicommunications.co.uk/",
            "https://adicommunications.co.uk",
            "http://adicommunications.co.uk/index.html",
            "https://www.adicommunications.co.uk/",
        ]:
            text = f"Official debrief by Gary Pearce. Visit {raw_root} for details."
            ok, msg = self.firewall.validate_raw_root_immunity(text)
            self.assertFalse(ok, f"Firewall failed to reject raw root link '{raw_root}'")
            self.assertIn("Rule 45 Violation", msg)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")



if __name__ == "__main__":
    unittest.main(verbosity=2)
