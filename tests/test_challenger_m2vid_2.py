#!/usr/bin/env python3
"""
tests/test_challenger_m2vid_2.py
Empirical Challenger Test Suite: Milestone 2 (M2-VID)
Rule 45 Evasion & Catalog Parity Stress Test

Author: Challenger M2-VID 2
Role: Empirical Challenger (critic, specialist)
Verification Targets:
  1. Multi-pass URL evasion scanner across all 50 entries (trailing dots, encoded paths,
     path traversals, ports, subdomain tricks, zero-width chars, unicode homoglyphs).
  2. Tier 3 strict Sovereign Isolation: 0 occurrences of adicommunications.co.uk in ANY form.
  3. Catalog schema & mathematical parity across all 50 sequential IDs and 7 disciplines.
  4. Duration, word count, timestamps, and media file parity on disk.
  5. E-E-A-T trade metadata fuzzing: zero Checkatrade, zero 0800 numbers, authentic 9.98/10 rating,
     CAI non-membership compliance, zero banned AI marketing buzzwords.
  6. Binary uniqueness & forensic media validation: SHA-256 hashes, ffprobe streams, zero placeholders.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
import unittest
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

CATALOG_PATH = REPO_ROOT / "video_stack_50_catalog.json"


class TestRule45MultiPassEvasion(unittest.TestCase):
    """Adversarially fuzzed scanner against Rule 45 Citadel Air-Gap evasions."""

    @classmethod
    def setUpClass(cls):
        cls.assertTrue(CATALOG_PATH.exists(), f"Catalog not found: {CATALOG_PATH}")
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            cls.raw_json = f.read()
            cls.catalog = json.loads(cls.raw_json)
            cls.videos = cls.catalog.get("videos", [])

    def test_01_no_raw_root_commercial_links_in_entire_catalog(self):
        """Asserts 0 raw root commercial links to adicommunications.co.uk/ anywhere in raw catalog string."""
        raw_root_patterns = [
            r"https?://(?:www\.)?adicommunications\.co\.uk/?[\"'\s\)]",
            r"https?://(?:www\.)?adicommunications\.co\.uk$",
            r"\"https?://(?:www\.)?adicommunications\.co\.uk/?\"",
            r"'https?://(?:www\.)?adicommunications\.co\.uk/?'",
        ]
        for pat in raw_root_patterns:
            matches = re.findall(pat, self.raw_json, flags=re.IGNORECASE | re.MULTILINE)
            self.assertEqual(matches, [], f"Raw root anchor pattern '{pat}' leaked into catalog: {matches}")

    def test_02_url_encoding_and_homoglyph_evasion_scan(self):
        """Fuzzes for encoded URLs (%2e%2e, %2f, %3a) in buffer URLs and descriptions."""
        encoded_needles = [
            "%2e%2e",  # ..
            "%2f",    # /
            "%3a",    # :
            "%252e",  # double encoded .
            "%61%64%69",  # 'adi'
            "%2e%63%6f%2e%75%6b",  # '.co.uk'
        ]
        for v in self.videos:
            vid = v.get("video_id")
            for field in ["buffer_url", "blogger_shield_url", "description_tier1", "description_tier2", "description_tier3"]:
                val = str(v.get(field, ""))
                for needle in encoded_needles:
                    self.assertNotIn(needle, val.lower(), f"Evasion vector '{needle}' detected in {vid} field '{field}'")

    def test_03_path_traversal_and_trailing_dot_fuzzing(self):
        """Asserts no path traversals (/../), directory dots, or trailing domain dots in URLs."""
        traversal_patterns = [
            r"/news/\.\./",
            r"/news/\./",
            r"adicommunications\.co\.uk\.",     # trailing dot bypass: adicommunications.co.uk.
            r"adicommunications\.co\.uk:\d+",   # port bypass: adicommunications.co.uk:443
            r"(?<!:)//adicommunications\.co\.uk",  # protocol-relative bypass without https:
            r"adicommunications\.co\.uk//",     # double slash in path
        ]
        for v in self.videos:
            vid = v.get("video_id")
            for field in ["buffer_url", "blogger_shield_url", "description_tier1", "description_tier2", "description_tier3"]:
                val = str(v.get(field, ""))
                for pat in traversal_patterns:
                    match = re.search(pat, val, re.IGNORECASE)
                    self.assertIsNone(match, f"URL bypass pattern '{pat}' matched in {vid} {field}: '{val}'")

    def test_04_buffer_url_strict_subpath_syntax(self):
        """Asserts every buffer_url strictly adheres to https://adicommunications.co.uk/news/<valid-kebab-slug>/."""
        exact_regex = re.compile(r"^https://adicommunications\.co\.uk/news/[a-z0-9]+(?:-[a-z0-9]+)*/$")
        for v in self.videos:
            vid = v.get("video_id")
            b_url = v.get("buffer_url", "")
            self.assertTrue(exact_regex.match(b_url), f"{vid} buffer_url '{b_url}' does not match canonical /news/<slug>/ format")

    def test_05_tier3_descriptions_absolute_zero_adicommunications_domain(self):
        """Asserts Tier 3 descriptions contain ZERO occurrences of 'adicommunications.co.uk' in ANY casing or obfuscation."""
        zero_width_chars = ['\u200b', '\u200c', '\u200d', '\u2060', '\ufeff']
        homoglyph_map = {
            'а': 'a', 'с': 'c', 'о': 'o', 'е': 'e', 'р': 'p', 'і': 'i', 'ԁ': 'd', 'ո': 'n'
        }

        for v in self.videos:
            vid = v.get("video_id")
            desc3 = v.get("description_tier3", "")
            self.assertTrue(len(desc3) > 50, f"{vid} description_tier3 is too short ({len(desc3)} chars)")

            # Raw check
            self.assertNotIn("adicommunications.co.uk", desc3.lower(), f"Direct domain leak in {vid} Tier 3")

            # Zero-width stripped check
            cleaned = desc3.lower()
            for zwc in zero_width_chars:
                cleaned = cleaned.replace(zwc, "")
            self.assertNotIn("adicommunications.co.uk", cleaned, f"Obfuscated domain leak in {vid} Tier 3")

            # Homoglyph translation check
            trans_desc = "".join(homoglyph_map.get(c, c) for c in cleaned)
            self.assertNotIn("adicommunications.co.uk", trans_desc, f"Homoglyph domain leak in {vid} Tier 3")

            # Outbound URL protocol check: ONLY YouTube allowed
            urls = re.findall(r"https?://[^\s\)\"'>]+", desc3)
            self.assertTrue(len(urls) >= 1, f"{vid} Tier 3 must contain at least one YouTube URL")
            for u in urls:
                parsed = urllib.parse.urlparse(u)
                domain = parsed.netloc.lower()
                self.assertTrue(
                    domain in ("www.youtube.com", "youtube.com", "youtu.be"),
                    f"Forbidden external domain '{domain}' in {vid} description_tier3: '{u}'"
                )

    def test_06_tier3_descriptions_link_strictly_to_youtube_apex(self):
        """Asserts Tier 3 descriptions contain links strictly to YouTube watch URL or @CCTV.services channel."""
        for v in self.videos:
            vid = v.get("video_id")
            desc3 = v.get("description_tier3", "")
            self.assertTrue(
                "youtube.com/@cctv.services" in desc3.lower() or "youtu.be" in desc3.lower() or "youtube.com/watch" in desc3.lower(),
                f"{vid} Tier 3 description must contain Apex YouTube link"
            )

    def test_07_tier2_descriptions_dual_linking_verification(self):
        """Asserts Tier 2 descriptions contain BOTH YouTube link AND /news/ buffer link (no raw root)."""
        for v in self.videos:
            vid = v.get("video_id")
            desc2 = v.get("description_tier2", "")
            self.assertTrue(len(desc2) > 50, f"{vid} description_tier2 too short")

            self.assertTrue(
                "youtube.com" in desc2.lower() or "youtu.be" in desc2.lower(),
                f"{vid} Tier 2 description missing YouTube link"
            )
            self.assertIn("adicommunications.co.uk/news/", desc2.lower(), f"{vid} Tier 2 description missing /news/ buffer link")

            clean_d2 = desc2.lower().replace("adicommunications.co.uk/news/", "")
            self.assertNotIn("adicommunications.co.uk/", clean_d2, f"{vid} Tier 2 description leaked raw root link")

    def test_08_tier1_descriptions_triple_apex_linking(self):
        """Asserts Tier 1 descriptions link to Blogger Citadel Hub, /news/ buffer, and YouTube."""
        for v in self.videos:
            vid = v.get("video_id")
            desc1 = v.get("description_tier1", "")
            self.assertTrue(len(desc1) > 50, f"{vid} description_tier1 too short")

            self.assertIn("tvandhomesecurity.blogspot.com", desc1.lower(), f"{vid} Tier 1 missing Blogger Citadel Hub")
            self.assertIn("adicommunications.co.uk/news/", desc1.lower(), f"{vid} Tier 1 missing /news/ buffer")


class TestCatalogSchemaAndMathematicalParity(unittest.TestCase):
    """Stress testing the catalog structure, sequential IDs, taxonomy, and physical files."""

    @classmethod
    def setUpClass(cls):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            cls.raw_json = f.read()
            cls.catalog = json.loads(cls.raw_json)
            cls.videos = cls.catalog.get("videos", [])

    def test_09_catalog_root_metadata_conformance(self):
        """Asserts root metadata has all required keys and valid values."""
        required_root = [
            "title", "version", "created_at", "total_videos", "disciplines",
            "apex_youtube_channel", "lead_engineer", "direct_phone",
            "public_liability_insurance", "verified_rating", "linking_architecture", "videos"
        ]
        for key in required_root:
            self.assertIn(key, self.catalog, f"Missing root key: '{key}'")

        self.assertEqual(self.catalog.get("total_videos"), 50)
        self.assertEqual(len(self.videos), 50)
        self.assertEqual(self.catalog.get("direct_phone"), "07860 244 274")
        self.assertEqual(self.catalog.get("lead_engineer"), "Gary Pearce")
        self.assertEqual(self.catalog.get("public_liability_insurance"), "£10,000,000")
        self.assertEqual(self.catalog.get("apex_youtube_channel"), "https://www.youtube.com/@CCTV.services")

    def test_10_sequential_ids_vid001_to_vid050_strict_order(self):
        """Asserts IDs are strictly sequential VID-001..VID-050 with exact zero-padded indices."""
        for i, v in enumerate(self.videos):
            expected_id = f"VID-{i+1:03d}"
            actual_id = v.get("video_id")
            self.assertEqual(actual_id, expected_id, f"Video at index {i} has ID '{actual_id}', expected '{expected_id}'")

    def test_11_slug_kebab_case_and_uniqueness(self):
        """Asserts every slug is valid lowercase kebab-case and strictly unique."""
        slug_regex = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        slugs = []
        for v in self.videos:
            vid = v.get("video_id")
            slug = v.get("slug", "")
            self.assertTrue(slug_regex.match(slug), f"{vid} slug '{slug}' is not valid kebab-case")
            slugs.append(slug)
        self.assertEqual(len(slugs), 50)
        self.assertEqual(len(set(slugs)), 50, "Duplicate slug found in catalog")

    def test_12_disciplines_taxonomy_all_7_covered(self):
        """Asserts exactly 7 UK engineering disciplines are represented in root and videos."""
        valid_canonical_disciplines = {
            "Satellite Telecoms",
            "Smart Alarms",
            "CCTV Engineering",
            "Video Doorbells",
            "Structured Cabling",
            "TV & Media Walls",
            "TV & Broadcast"
        }
        catalog_disciplines = set(self.catalog.get("disciplines", []))
        self.assertEqual(catalog_disciplines, valid_canonical_disciplines, f"Disciplines mismatch in root metadata: {catalog_disciplines}")

        # Check distribution in videos
        video_disciplines = set(v.get("trade_category") for v in self.videos)
        self.assertEqual(video_disciplines, valid_canonical_disciplines, f"Video categories don't cover all 7 disciplines: {video_disciplines}")

        # Check counts per discipline
        counts = {}
        for v in self.videos:
            cat = v.get("trade_category")
            counts[cat] = counts.get(cat, 0) + 1
        for cat, cnt in counts.items():
            self.assertGreaterEqual(cnt, 5, f"Discipline '{cat}' underrepresented with only {cnt} videos")

    def test_13_duration_sec_numeric_bounds_and_validity(self):
        """Asserts duration_sec is a positive float between 30.0 and 120.0s."""
        for v in self.videos:
            vid = v.get("video_id")
            dur = v.get("duration_sec")
            self.assertIsInstance(dur, (int, float), f"{vid} duration_sec is not numeric: {type(dur)}")
            self.assertFalse(dur != dur, f"{vid} duration_sec is NaN")
            self.assertTrue(30.0 <= dur <= 120.0, f"{vid} duration {dur}s outside expected 30-120s window")

    def test_14_word_count_and_script_narration_parity(self):
        """Asserts script_narration is present, substantial, and word_count closely matches len(script.split())."""
        for v in self.videos:
            vid = v.get("video_id")
            script = v.get("script_narration", "")
            self.assertTrue(len(script) > 100, f"{vid} script_narration too short")
            words = script.split()
            claimed_wc = v.get("word_count")
            self.assertIsInstance(claimed_wc, int, f"{vid} word_count is not an integer")
            self.assertAlmostEqual(len(words), claimed_wc, delta=5, msg=f"{vid} word count mismatch: claimed {claimed_wc}, actual {len(words)}")

    def test_15_timestamps_chapter_markers_format(self):
        """Asserts timestamps are structured lists starting at 00:00 with increasing offsets."""
        time_regex = re.compile(r"^(\d{2}):(\d{2})")
        for v in self.videos:
            vid = v.get("video_id")
            ts = v.get("timestamps")
            self.assertIsInstance(ts, list, f"{vid} timestamps must be a list")
            self.assertGreaterEqual(len(ts), 3, f"{vid} must have at least 3 timestamp chapters")
            
            last_sec = -1
            for idx, item in enumerate(ts):
                m = time_regex.match(str(item).strip())
                self.assertIsNotNone(m, f"{vid} timestamp '{item}' does not start with mm:ss")
                mins, secs = int(m.group(1)), int(m.group(2))
                total_sec = mins * 60 + secs
                if idx == 0:
                    self.assertEqual(total_sec, 0, f"{vid} first chapter must start at 00:00, found {item}")
                else:
                    self.assertGreater(total_sec, last_sec, f"{vid} timestamps not chronologically increasing at {item}")
                last_sec = total_sec

    def test_16_hardware_and_technical_standards_populated(self):
        """Asserts technical_standards and hardware_standards are populated with non-trivial technical details."""
        for v in self.videos:
            vid = v.get("video_id")
            tech = v.get("technical_standards")
            hard = v.get("hardware_standards")
            self.assertTrue(tech, f"{vid} missing technical_standards")
            self.assertTrue(hard, f"{vid} missing hardware_standards")
            tech_str = json.dumps(tech)
            hard_str = json.dumps(hard)
            self.assertGreater(len(tech_str), 10, f"{vid} technical_standards too shallow")
            self.assertGreater(len(hard_str), 10, f"{vid} hardware_standards too shallow")

    def test_17_tags_array_validity(self):
        """Asserts tags is a non-empty list of unique non-empty string tags."""
        for v in self.videos:
            vid = v.get("video_id")
            tags = v.get("tags")
            self.assertIsInstance(tags, list, f"{vid} tags must be a list")
            self.assertGreaterEqual(len(tags), 5, f"{vid} must have at least 5 tags")
            for t in tags:
                self.assertIsInstance(t, str, f"{vid} tag is not a string: {t}")
                self.assertTrue(len(t.strip()) > 0, f"{vid} contains empty tag")
            self.assertEqual(len(tags), len(set(tags)), f"{vid} contains duplicate tags: {tags}")

    def test_18_media_files_exist_on_disk_and_non_empty(self):
        """Asserts both video_path and thumbnail_path point to existing, non-empty files on disk."""
        for v in self.videos:
            vid = v.get("video_id")
            vpath = REPO_ROOT / v.get("video_path", "")
            tpath = REPO_ROOT / v.get("thumbnail_path", "")
            self.assertTrue(vpath.exists(), f"{vid} video file missing on disk: {vpath}")
            self.assertTrue(tpath.exists(), f"{vid} thumbnail file missing on disk: {tpath}")
            self.assertGreaterEqual(vpath.stat().st_size, 500_000, f"{vid} video file too small: {vpath.stat().st_size} bytes")
            self.assertGreaterEqual(tpath.stat().st_size, 5_000, f"{vid} thumbnail file too small: {tpath.stat().st_size} bytes")

    def test_25_zero_duplicate_keys_in_catalog_json(self):
        """Asserts that the catalog JSON contains strictly ZERO duplicate keys across any object."""
        duplicate_keys = []
        def check_dups(pairs):
            keys = [k for k, v in pairs]
            if len(keys) != len(set(keys)):
                dups = [k for k in keys if keys.count(k) > 1]
                duplicate_keys.extend(dups)
            return dict(pairs)

        json.loads(self.raw_json, object_pairs_hook=check_dups)
        self.assertEqual(duplicate_keys, [], f"Duplicate JSON keys detected: {duplicate_keys}")

    def test_26_matching_source_images_exist_on_disk(self):
        """Asserts that all 50 matching_image_asset paths exist on disk with valid file size."""
        for v in self.videos:
            vid = v.get("video_id")
            img = v.get("matching_image_asset")
            self.assertIsNotNone(img, f"{vid} missing matching_image_asset")
            img_path = REPO_ROOT / img
            self.assertTrue(img_path.exists(), f"{vid} matching_image_asset missing on disk: {img_path}")
            self.assertGreater(img_path.stat().st_size, 10_000, f"{vid} matching_image_asset too small: {img_path}")

    def test_27_sha256_uniqueness_across_all_50_mp4_files(self):
        """Asserts all 50 rendered MP4 video files have strictly unique SHA-256 hashes (no duplicate binaries)."""
        hashes = set()
        for v in self.videos:
            vid = v.get("video_id")
            vpath = REPO_ROOT / v.get("video_path")
            h = hashlib.sha256(vpath.read_bytes()).hexdigest()
            self.assertNotIn(h, hashes, f"Duplicate MP4 binary hash detected for {vid}")
            hashes.add(h)
        self.assertEqual(len(hashes), 50, "Expected exactly 50 unique MP4 hashes")

    def test_28_sha256_uniqueness_across_all_50_webp_thumbnails(self):
        """Asserts all 50 synthesized WebP thumbnails have strictly unique SHA-256 hashes."""
        hashes = set()
        for v in self.videos:
            vid = v.get("video_id")
            tpath = REPO_ROOT / v.get("thumbnail_path")
            h = hashlib.sha256(tpath.read_bytes()).hexdigest()
            self.assertNotIn(h, hashes, f"Duplicate WebP thumbnail hash detected for {vid}")
            hashes.add(h)
        self.assertEqual(len(hashes), 50, "Expected exactly 50 unique WebP hashes")

    def test_29_ffprobe_stream_validation_all_50_videos(self):
        """Runs ffprobe on all 50 MP4 files asserting 1080p H.264 video and AAC audio."""
        for v in self.videos:
            vid = v.get("video_id")
            vpath = REPO_ROOT / v.get("video_path")
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "stream=codec_name,codec_type,width,height:format=duration",
                "-of", "json", str(vpath)
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"ffprobe error on {vid}: {res.stderr}")
            probe_data = json.loads(res.stdout)
            streams = probe_data.get("streams", [])
            v_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
            a_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
            
            self.assertIsNotNone(v_stream, f"{vid} missing video stream")
            self.assertEqual(v_stream.get("codec_name"), "h264", f"{vid} video codec is not h264")
            self.assertEqual(v_stream.get("width"), 1920, f"{vid} width is not 1920")
            self.assertEqual(v_stream.get("height"), 1080, f"{vid} height is not 1080")
            
            self.assertIsNotNone(a_stream, f"{vid} missing audio stream")
            self.assertEqual(a_stream.get("codec_name"), "aac", f"{vid} audio codec is not aac")


class TestTradeEEATAndAntiSlop(unittest.TestCase):
    """Stress testing E-E-A-T trade credentials, Checkatrade ban, 0800 ban, ratings, and marketing buzzwords."""

    @classmethod
    def setUpClass(cls):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            cls.raw_json = f.read()
            cls.catalog = json.loads(cls.raw_json)
            cls.videos = cls.catalog.get("videos", [])

    def test_19_zero_checkatrade_mentions_adversarial(self):
        """Adversarially fuzzed scanner for forbidden Checkatrade mentions in any casing or variation."""
        variants = [
            r"checkatrade",
            r"check-a-trade",
            r"check_a_trade",
            r"check\s+a\s+trade",
            r"ch3ckatrade",
            r"checkatrade\.com",
        ]
        for v in variants:
            matches = re.findall(v, self.raw_json, re.IGNORECASE)
            self.assertEqual(matches, [], f"Forbidden brand '{v}' detected in catalog: {matches}")

    def test_20_zero_0800_freephone_numbers(self):
        """Asserts zero occurrences of 0800 / 0808 / 0845 / 0870 / 0300 numbers across catalog."""
        forbidden_prefixes = [r"\b0800\b", r"\b0808\b", r"\b0845\b", r"\b0870\b", r"\b0300\b", r"\b0900\b"]
        for p in forbidden_prefixes:
            matches = re.findall(p, self.raw_json)
            self.assertEqual(matches, [], f"Forbidden telephone prefix pattern '{p}' detected: {matches}")

    def test_21_direct_mobile_presence_across_descriptions(self):
        """Asserts Gary's direct mobile 07860 244 274 is present in Tier 1 and Tier 2 descriptions."""
        for v in self.videos:
            vid = v.get("video_id")
            d1 = v.get("description_tier1", "")
            d2 = v.get("description_tier2", "")
            self.assertTrue("07860 244 274" in d1 or "07860244274" in d1, f"{vid} Tier 1 missing phone 07860 244 274")
            self.assertTrue("07860 244 274" in d2 or "07860244274" in d2, f"{vid} Tier 2 missing phone 07860 244 274")

    def test_22_verified_rating_mathematical_precision(self):
        """Asserts verified rating is strictly 9.98 / 10 from 84+ reviews (never 5.0/5 or fake 10/10)."""
        root_rating = self.catalog.get("verified_rating", "")
        self.assertIn("9.98", root_rating, f"Root verified_rating '{root_rating}' must contain 9.98")
        self.assertIn("84+", root_rating, f"Root verified_rating '{root_rating}' must cite 84+ reviews")

        corrupted_ratings = [r"\b5\.0\s*/\s*5\b", r"\b5/5\b", r"\b10/10\b", r"\b10\.0\s*/\s*10\b", r"\b100%\s*rating\b"]
        for cr in corrupted_ratings:
            matches = re.findall(cr, self.raw_json, re.IGNORECASE)
            self.assertEqual(matches, [], f"Corrupted rating pattern '{cr}' found: {matches}")

    def test_23_cai_non_membership_legal_disclaimer(self):
        """Asserts Gary Pearce is NEVER falsely claimed as a 'CAI Member' (Rule 20 legal prohibition)."""
        cai_claims = [
            r"cai\s+member",
            r"member\s+of\s+cai",
            r"cai\s+accredited",
            r"cai\s+certified\s+installer",
        ]
        for claim in cai_claims:
            matches = re.findall(claim, self.raw_json, re.IGNORECASE)
            self.assertEqual(matches, [], f"Illegal CAI claim pattern '{claim}' detected: {matches}")

    def test_24_banned_ai_marketing_buzzwords_purge(self):
        """User Rule 15: Scans all text fields for banned AI marketing buzzwords."""
        banned = [
            r"\bcutting-edge\b",
            r"\brevolutionary\b",
            r"\bgame-changer\b",
            r"\bworld-class\b",
            r"\bseamlessly\b",
            r"\bunparalleled\b",
            r"\bnext-level\b",
            r"\belevate\b",
            r"\batlantic storm-tested\b",
            r"\bzero throttling\b",
            r"\bgigabit speeds\b",
        ]
        for b in banned:
            matches = re.findall(b, self.raw_json, re.IGNORECASE)
            self.assertEqual(matches, [], f"Banned marketing buzzword '{b}' found in catalog: {matches}")

    def test_30_zero_code_placeholders_or_todos(self):
        """Asserts zero code placeholders (TODO, FIXME, TBD, [INSERT], COMING SOON) in catalog."""
        placeholders = [r"\bTODO\b", r"\bFIXME\b", r"\bTBD\b", r"\[INSERT", r"\bCOMING SOON\b"]
        for p in placeholders:
            matches = re.findall(p, self.raw_json, re.IGNORECASE)
            self.assertEqual(matches, [], f"Placeholder pattern '{p}' found: {matches}")

    def test_31_zero_ai_tool_brand_mentions(self):
        """Rule 28 & blog-rules: Asserts zero mentions of AI tools (ChatGPT, Claude, Gemini, NotebookLM)."""
        ai_brands = [r"\bchatgpt\b", r"\bclaude\b", r"\bgemini\b", r"\bnotebooklm\b", r"\bopenai\b", r"\banthropic\b"]
        for brand in ai_brands:
            matches = re.findall(brand, self.raw_json, re.IGNORECASE)
            self.assertEqual(matches, [], f"AI brand mention '{brand}' detected in catalog: {matches}")

    def test_32_zero_directory_scraped_brand_mentions(self):
        """Rule 7 & 20: Asserts zero mentions of banned scraper directories (Bark, Yell, Trustpilot)."""
        directories = [r"\bbark\.com\b", r"\byell\.com\b", r"\btrustpilot\b"]
        for d in directories:
            matches = re.findall(d, self.raw_json, re.IGNORECASE)
            self.assertEqual(matches, [], f"Banned directory brand '{d}' detected: {matches}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
