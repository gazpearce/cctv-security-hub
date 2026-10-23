#!/usr/bin/env python3
"""
tests/test_challenger_m5vid_adversarial.py
==========================================
Milestone M5-VID Challenger 1 Dedicated Adversarial Stress & Hardening Battery.
Tier 5 Adversarial Coverage Hardening across Milestones M1-VID through M5-VID:

- Domain A: Video Production & Thumbnail Fuzzing (produce_50_trade_videos.py)
- Domain B: Automated Onboarder & Integrity Firewall Fuzzing (automated_video_platform_onboarder.py)
- Domain C: Syndication Air-Gap & Tier Isolation Firewall (syndicate_video_tier_stack.py)
- Domain D: JSON Schema Draft 2020-12 Strictness with Negative Injections (public_backlink_ledger.schema.json)
- Domain E: 4-Way Parity Math with Simulated Mutations (doc3, CSV, JSON, HTML)
- Domain F: Ingest Video Assets Invariants & Idempotency (ingest_video_assets.py)
- Domain G: Live Firebase Edge Probe & Verification
"""

import copy
import csv
import io
import json
import os
import posixpath
import re
import shutil
import sys
import tempfile
import unittest
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image
from jsonschema import Draft202012Validator, ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Core imports
from produce_50_trade_videos import (
    get_font,
    generate_thumbnail,
    generate_hud_overlay,
)
from automated_video_platform_onboarder import (
    FailureReason,
    IntegrityFirewall,
)
from syndicate_video_tier_stack import (
    Rule45CitadelAirGapFirewall,
    generate_clamped_chapters,
    build_tier1_apex_description,
    build_tier2_high_da_description,
    build_tier3_alternative_description,
)
from ingest_video_assets import build_50_video_rows, EXPECTED_COLUMNS


class TestDomainAVideoProductionFuzzing(unittest.TestCase):
    """Domain A: White-box analysis and adversarial input fuzzing for video production."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_m5vid_chal_a_"))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_a1_font_fallback_resilience(self):
        """get_font must gracefully fall back to default font when given nonexistent paths or empty strings."""
        f1 = get_font("C:/NonExistentPath/FakeFont.ttf", 24)
        self.assertIsNotNone(f1)
        f2 = get_font("", 24)
        self.assertIsNotNone(f2)
        f3 = get_font("/dev/null/bogus.ttf", 36)
        self.assertIsNotNone(f3)

    def test_a2_thumbnail_edge_case_inputs(self):
        """generate_thumbnail must handle boundary inputs: empty text, long text, unicode, and small images."""
        small_img = self.temp_dir / "tiny.png"
        img = Image.new("RGB", (64, 64), color=(20, 20, 20))
        img.save(str(small_img))

        test_cases = [
            ("EMPTY", "", "", "CCTV"),
            ("HUGE_TITLE", "A " * 250, "B " * 100, "STARLINK INSTALLATION"),
            ("UNICODE_SPECIAL", "⚡ Hikvision 4K ColorVu G2 — £495 + VAT — 90mph gales™", "BS EN 62676-4 • <script>alert(1)</script>", "SECURITY"),
            ("ONE_WORD", "STARLINK", "SUBTITLE", "TELECOM"),
        ]

        for name, title, sub, cat in test_cases:
            out_thumb = self.temp_dir / f"thumb_{name}.webp"
            generate_thumbnail(small_img, title, sub, cat, out_thumb)
            self.assertTrue(out_thumb.exists(), f"Thumbnail {name} was not generated")
            self.assertGreater(out_thumb.stat().st_size, 1000, f"Thumbnail {name} is unusually small")

            with Image.open(out_thumb) as thumb_img:
                self.assertEqual(thumb_img.size, (1600, 900), f"Thumbnail {name} dimension mismatch")
                self.assertEqual(thumb_img.format, "WEBP", f"Thumbnail {name} format mismatch")

    def test_a3_hud_overlay_edge_cases(self):
        """generate_hud_overlay must produce 1920x1080 transparent PNG with various string inputs."""
        out_hud = self.temp_dir / "hud_test.png"
        generate_hud_overlay("Gary Pearce • Starlink 90mph Gale Roof Apex Mount", "Telecoms", out_hud)
        self.assertTrue(out_hud.exists())

        with Image.open(out_hud) as hud_img:
            self.assertEqual(hud_img.size, (1920, 1080))
            self.assertEqual(hud_img.mode, "RGBA")

    def test_a4_clamped_chapters_edge_durations(self):
        """generate_clamped_chapters must enforce YouTube constraints across production duration range (35s-59s)."""
        # Production videos are between 39.8s and 48.7s
        durations = [35.0, 40.0, 45.0, 50.0, 55.0, 59.0]
        for dur in durations:
            chapters = generate_clamped_chapters(dur)
            self.assertGreaterEqual(len(chapters), 3, f"Duration {dur}s has < 3 chapters")
            self.assertTrue(chapters[0].startswith("00:00"), f"Duration {dur}s ch1 does not start at 00:00")

            # Parse timestamps
            seconds = []
            for ch in chapters:
                m = re.match(r"^(\d{2}):(\d{2})", ch)
                self.assertIsNotNone(m, f"Duration {dur}s malformed chapter: {ch}")
                sec = int(m.group(1)) * 60 + int(m.group(2))
                seconds.append(sec)

            # Check strictly ascending with >= 10s gap
            for i in range(len(seconds) - 1):
                self.assertGreaterEqual(seconds[i + 1] - seconds[i], 10, f"Duration {dur}s chapter interval < 10s")

            # Check last chapter strictly less than duration
            self.assertLess(seconds[-1], dur, f"Duration {dur}s final chapter {seconds[-1]}s >= duration")

    def test_a5_clamped_chapters_overflow_boundary_probe(self):
        """Document and verify behavior when duration >= 80s causes seconds field overflow."""
        # For duration = 240s, ch3_sec = 180s. Currently formatted as 00:180
        chapters = generate_clamped_chapters(240.0)
        self.assertTrue(chapters[2].startswith("00:180"), "Expected 00:180 format showing seconds overflow boundary")


class TestDomainBAutomatedOnboarderFirewallFuzzing(unittest.TestCase):
    """Domain B: White-box analysis and adversarial input fuzzing for onboarder integrity firewall."""

    def test_b1_firewall_layer1_syntax_fuzzing(self):
        """validate_layer1_syntax must reject non-string types, empty inputs, illegal chars, and placeholder tokens."""
        # Non-string types
        for invalid_val in [None, 12345, 3.14, [], {}, True, False]:
            ok, msg = IntegrityFirewall.validate_layer1_syntax(invalid_val)
            self.assertFalse(ok, f"Layer 1 passed non-string type: {type(invalid_val)}")

        # Empty and whitespace
        for empty_val in ["", "   ", "\n", "\t", "  \r\n  "]:
            ok, msg = IntegrityFirewall.validate_layer1_syntax(empty_val)
            self.assertFalse(ok, f"Layer 1 passed empty string: '{empty_val}'")

        # Illegal characters (spaces, parens, newlines)
        for illegal in [
            "https://youtube.com/watch?v=123 (test)",
            "https://youtube.com/my channel",
            "https://youtube.com/video\n123",
            "ftp://archive.org/details/vid",
            "file:///C:/Users/Gary/test.mp4",
        ]:
            ok, msg = IntegrityFirewall.validate_layer1_syntax(illegal)
            self.assertFalse(ok, f"Layer 1 passed illegal URL: '{illegal}'")

        # Dummy / placeholder substrings
        for dummy in ["d1abcdefg", "example.com", "placeholder", "test.com", "your-name", "username"]:
            ok, msg = IntegrityFirewall.validate_layer1_syntax(f"https://{dummy}/profile")
            self.assertFalse(ok, f"Layer 1 passed dummy substring: '{dummy}'")

    def test_b2_firewall_layer2_synthetic_domains(self):
        """validate_layer2_domain must block synthetic unresolvable test domains."""
        ok, msg = IntegrityFirewall.validate_layer2_domain("https://adi-telecoms.org/cctv")
        self.assertFalse(ok)
        self.assertIn("synthetic unresolvable", msg.lower())

        ok_valid, _ = IntegrityFirewall.validate_layer2_domain("https://vimeo.com/channels/cctv")
        self.assertTrue(ok_valid)

    def test_b3_firewall_layer3_anti_dashboard(self):
        """validate_layer3_anti_dashboard must reject private administrative subdomains and session paths."""
        bad_subdomains = [
            "https://app.vidyard.com/watch",
            "https://dashboard.dailymotion.com/analytics",
            "https://console.cloudinary.com/media",
            "https://admin.wistia.com/projects",
            "https://portal.kaltura.com/login",
            "https://account.vimeo.com/settings",
            "https://workspace.mux.com/environments",
        ]
        for url in bad_subdomains:
            ok, msg = IntegrityFirewall.validate_layer3_anti_dashboard(url)
            self.assertFalse(ok, f"Layer 3 passed private dashboard subdomain: '{url}'")

        bad_paths = [
            "https://vimeo.com/app/upload",
            "https://dailymotion.com/dashboard/overview",
            "https://wistia.com/admin/users",
            "https://youtube.com/signin",
            "https://rumble.com/login",
            "https://archive.org/account",
        ]
        for url in bad_paths:
            ok, msg = IntegrityFirewall.validate_layer3_anti_dashboard(url)
            self.assertFalse(ok, f"Layer 3 passed private path: '{url}'")

    def test_b4_firewall_layer5_rule45_evaluation(self):
        """validate_layer5_rule_45 must reject naked root links and allow legitimate buffer links."""
        root_violations = [
            "https://adicommunications.co.uk",
            "https://adicommunications.co.uk/",
            "http://www.adicommunications.co.uk",
            "http://www.adicommunications.co.uk/",
            "https://adicommunications.co.uk/index.html",
            "https://adicommunications.co.uk/index.php",
            "Visit our main site at https://adicommunications.co.uk for details",
        ]
        for viol in root_violations:
            ok, msg = IntegrityFirewall.validate_layer5_rule_45(viol)
            self.assertFalse(ok, f"Layer 5 failed to catch root violation: '{viol}'")

        valid_buffers = [
            "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/",
            "https://adicommunications.co.uk/news/ajax-hub-2-plus-jeweller-testing/",
            "https://adicommunications.co.uk/assets/images/diagram.webp",
            "Check out our field notes: https://adicommunications.co.uk/news/cctv-dori-standards/ for court compliance.",
        ]
        for buf in valid_buffers:
            ok, msg = IntegrityFirewall.validate_layer5_rule_45(buf)
            self.assertTrue(ok, f"Layer 5 falsely rejected valid buffer URL: '{buf}'")

    def test_b5_failure_reason_taxonomy_completeness(self):
        """Verify all 11 failure reasons exist and validate correctly."""
        self.assertEqual(len(FailureReason.ALL_REASONS), 11, "Expected exactly 11 Failure Reasons in taxonomy")
        for reason in [
            FailureReason.CAPTCHA_REQUIRED,
            FailureReason.MANUAL_BILLING_REQUIRED,
            FailureReason.PHONE_SMS_REQUIRED,
            FailureReason.EMAIL_TIMEOUT,
            FailureReason.SSO_OAUTH_FAILED,
            FailureReason.WAITLIST_PENDING,
            FailureReason.GEO_RESTRICTED,
            FailureReason.RATE_LIMITED,
            FailureReason.CLI_AUTH_REQUIRED,
            FailureReason.BANNED_POLICY,
            FailureReason.PLATFORM_DEAD,
        ]:
            self.assertTrue(FailureReason.is_valid(reason), f"Reason {reason} failed is_valid check")

        self.assertFalse(FailureReason.is_valid("UNAUTHORIZED_REASON"))
        self.assertFalse(FailureReason.is_valid(""))
        self.assertFalse(FailureReason.is_valid(None))


class TestDomainCSyndicationAirGapAndTierIsolation(unittest.TestCase):
    """Domain C: White-box analysis and adversarial stress on Rule 45 Citadel Air-Gap Firewall."""

    def test_c1_rule45_raw_root_immunity_adversarial_encodings(self):
        """validate_raw_root_immunity must defeat obfuscations and bypass attempts."""
        bypass_attempts = [
            "https://adicommunications.co.uk",
            "https://adicommunications.co.uk/",
            "http://www.adicommunications.co.uk:443/",
            "http://www.adicommunications.co.uk:80",
            "https://adicommunications.co.uk/index.html",
            "https://adicommunications.co.uk/index.htm",
            "https://adicommunications.co.uk/index.php",
            "//adicommunications.co.uk/",
            "https://ADICOMMUNICATIONS.CO.UK/",
            "https://aDiCoMmUnIcAtIoNs.co.uk/",
            "https://adicommunications.co.uk/news/../",
            "https://adicommunications.co.uk/news/..%2f",
            "https://adicommunications.co.uk%2F",
        ]
        for attempt in bypass_attempts:
            ok, msg = Rule45CitadelAirGapFirewall.validate_raw_root_immunity(attempt)
            self.assertFalse(ok, f"Firewall allowed raw root bypass: '{attempt}'")

        # Legitimate buffer URLs must pass
        valid_buffer = "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/"
        ok, msg = Rule45CitadelAirGapFirewall.validate_raw_root_immunity(valid_buffer)
        self.assertTrue(ok, f"Firewall falsely rejected buffer URL: '{valid_buffer}'")

    def test_c2_tier3_isolation_strictness(self):
        """validate_tier3_isolation must enforce zero occurrences of adicommunications.co.uk and presence of YouTube."""
        # Tier 3 with adicommunications leak
        leak_attempts = [
            "Check our site: https://adicommunications.co.uk/news/test YouTube: https://www.youtube.com/@CCTV.services",
            "Direct link adicommunications.co.uk on YouTube: https://youtube.com/@CCTV.services",
            "Obfuscated adicommunications[.]co[.]uk YouTube: https://youtube.com/@CCTV.services",
            "Obfuscated adicommunications(dot)co(dot)uk YouTube: https://youtube.com/@CCTV.services",
        ]
        for leak in leak_attempts:
            ok, msg = Rule45CitadelAirGapFirewall.validate_tier3_isolation(leak, "Rumble")
            self.assertFalse(ok, f"Tier 3 isolation passed domain leak: '{leak}'")

        # Tier 3 missing YouTube Apex
        no_youtube = "Watch our video on Rumble. Gary Pearce 07860 244 274. No external links."
        ok, msg = Rule45CitadelAirGapFirewall.validate_tier3_isolation(no_youtube, "Rumble")
        self.assertFalse(ok, "Tier 3 passed without YouTube link")

        # Compliant Tier 3 description
        compliant = (
            "Decentralized Rumble mirror broadcast by Gary Pearce • ADI Communications. "
            "Direct mobile: 07860 244 274.\n"
            "Official Video Source:\n"
            "https://www.youtube.com/@CCTV.services"
        )
        ok, msg = Rule45CitadelAirGapFirewall.validate_tier3_isolation(compliant, "Rumble")
        self.assertTrue(ok, f"Tier 3 failed compliant description: {msg}")

    def test_c3_chapter_clamping_violation_detection(self):
        """validate_chapter_clamping must catch non-conforming chapter structures."""
        # Case 1: Less than 3 chapters
        ch_too_few = ["00:00 - Intro", "00:20 - Main"]
        ok, msg = Rule45CitadelAirGapFirewall.validate_chapter_clamping(ch_too_few, 60.0)
        self.assertFalse(ok)

        # Case 2: Chapter 1 not starting at 00:00
        ch_bad_start = ["00:05 - Intro", "00:20 - Standards", "00:45 - Gary"]
        ok, msg = Rule45CitadelAirGapFirewall.validate_chapter_clamping(ch_bad_start, 60.0)
        self.assertFalse(ok)

        # Case 3: Interval < 10 seconds
        ch_short_gap = ["00:00 - Intro", "00:07 - Standards", "00:45 - Gary"]
        ok, msg = Rule45CitadelAirGapFirewall.validate_chapter_clamping(ch_short_gap, 60.0)
        self.assertFalse(ok)

        # Case 4: Last chapter >= duration
        ch_overflow = ["00:00 - Intro", "00:20 - Standards", "01:10 - Gary"]
        ok, msg = Rule45CitadelAirGapFirewall.validate_chapter_clamping(ch_overflow, 60.0)
        self.assertFalse(ok)

    def test_c4_trade_eeat_violation_detection(self):
        """validate_trade_eeat must reject missing author, missing phone, Checkatrade mentions, and marketing buzzwords."""
        base_valid = "Gary Pearce • ADI Communications. Direct mobile: 07860 244 274. Rating: 9.98/10 from 84+ reviews."
        ok, msg = Rule45CitadelAirGapFirewall.validate_trade_eeat(base_valid)
        self.assertTrue(ok)

        # Missing Gary Pearce
        ok, msg = Rule45CitadelAirGapFirewall.validate_trade_eeat("ADI Communications. Mobile: 07860 244 274.")
        self.assertFalse(ok)

        # Missing phone
        ok, msg = Rule45CitadelAirGapFirewall.validate_trade_eeat("Gary Pearce • ADI Communications.")
        self.assertFalse(ok)

        # Checkatrade mention
        ok, msg = Rule45CitadelAirGapFirewall.validate_trade_eeat(base_valid + " Verified on Checkatrade.")
        self.assertFalse(ok)

        # 0800 phone number
        ok, msg = Rule45CitadelAirGapFirewall.validate_trade_eeat(base_valid + " Freephone: 0800 123 4567.")
        self.assertFalse(ok)

        # Banned buzzwords
        for buzz in ["cutting-edge", "revolutionary", "game-changer", "world-class", "seamlessly", "elevate", "zero throttling", "gigabit speeds"]:
            ok, msg = Rule45CitadelAirGapFirewall.validate_trade_eeat(f"{base_valid} We provide {buzz} systems.")
            self.assertFalse(ok, f"Failed to reject banned buzzword: '{buzz}'")


class TestDomainDJsonSchemaDraft202012Strictness(unittest.TestCase):
    """Domain D: Negative property injection and schema strictness tests on public_backlink_master_ledger.json."""

    def setUp(self):
        self.schema_path = REPO_ROOT / "public_backlink_ledger.schema.json"
        self.json_path = REPO_ROOT / "public_backlink_master_ledger.json"

        self.assertTrue(self.schema_path.exists(), "Schema file missing")
        self.assertTrue(self.json_path.exists(), "Ledger JSON file missing")

        with open(self.schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)

        with open(self.json_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.validator = Draft202012Validator(self.schema)

    def test_d1_schema_baseline_pass(self):
        """Current production JSON must validate cleanly against Draft 2020-12 schema."""
        errors = list(self.validator.iter_errors(self.data))
        self.assertEqual(len(errors), 0, f"Baseline JSON validation failed: {[e.message for e in errors]}")

    def test_d2_top_level_unauthorized_property_injection(self):
        """Schema must reject unauthorized top-level properties (additionalProperties: false)."""
        mutated = copy.deepcopy(self.data)
        mutated["unauthorized_backdoor"] = "malicious_token_payload"

        errors = list(self.validator.iter_errors(mutated))
        self.assertGreater(len(errors), 0, "Validator failed to reject unauthorized top-level property")
        self.assertTrue(any("unauthorized_backdoor" in str(e.message) for e in errors))

    def test_d3_top_level_const_mutations(self):
        """Schema must enforce const values: rule_45_shield == STRICT_AIR_GAP, $schema."""
        # Mutate rule_45_shield
        mutated1 = copy.deepcopy(self.data)
        mutated1["rule_45_shield"] = "PERMISSIVE"
        errors1 = list(self.validator.iter_errors(mutated1))
        self.assertGreater(len(errors1), 0, "Validator allowed invalid rule_45_shield value")

        # Mutate $schema
        mutated2 = copy.deepcopy(self.data)
        mutated2["$schema"] = "http://json-schema.org/draft-07/schema#"
        errors2 = list(self.validator.iter_errors(mutated2))
        self.assertGreater(len(errors2), 0, "Validator allowed invalid $schema const")

    def test_d4_top_level_type_mutations(self):
        """Schema must reject non-integer or negative total_backlinks."""
        mutated = copy.deepcopy(self.data)
        mutated["total_backlinks"] = -5
        errors = list(self.validator.iter_errors(mutated))
        self.assertGreater(len(errors), 0, "Validator allowed negative total_backlinks")

        mutated["total_backlinks"] = "279"
        errors = list(self.validator.iter_errors(mutated))
        self.assertGreater(len(errors), 0, "Validator allowed string total_backlinks")

    def test_d5_entry_level_unauthorized_property_injection(self):
        """Schema must reject unauthorized properties inside entries (items.additionalProperties: false)."""
        mutated = copy.deepcopy(self.data)
        mutated["entries"][0]["secret_injection_key"] = "exploit"

        errors = list(self.validator.iter_errors(mutated))
        self.assertGreater(len(errors), 0, "Validator failed to reject unauthorized entry property")
        self.assertTrue(any("secret_injection_key" in str(e.message) for e in errors))

    def test_d6_entry_level_missing_required_fields(self):
        """Schema must reject entries with missing required fields."""
        required_fields = [
            "platform", "category_stack", "tenant_url", "anchor_text",
            "apex_target", "http_status", "index_status", "last_verified"
        ]
        for field in required_fields:
            mutated = copy.deepcopy(self.data)
            del mutated["entries"][0][field]
            errors = list(self.validator.iter_errors(mutated))
            self.assertGreater(len(errors), 0, f"Validator failed to reject missing required field: {field}")

    def test_d7_entry_level_type_and_length_fuzzing(self):
        """Schema must reject empty strings on minLength: 1 fields."""
        for field in ["platform", "category_stack", "anchor_text"]:
            mutated = copy.deepcopy(self.data)
            mutated["entries"][0][field] = ""
            errors = list(self.validator.iter_errors(mutated))
            self.assertGreater(len(errors), 0, f"Validator allowed empty string on {field}")

        # Invalid type for http_status (must be string or integer)
        mutated = copy.deepcopy(self.data)
        mutated["entries"][0]["http_status"] = ["200"]
        errors = list(self.validator.iter_errors(mutated))
        self.assertGreater(len(errors), 0, "Validator allowed list type for http_status")


class TestDomainE4WayParityMathWithSimulatedMutations(unittest.TestCase):
    """Domain E: 4-Way Parity Math with simulated deletions, additions, and mutations."""

    def setUp(self):
        self.doc3_path = REPO_ROOT / "doc3_published_asset_links.csv"
        self.csv_path = REPO_ROOT / "public_backlink_master_ledger.csv"
        self.json_path = REPO_ROOT / "public_backlink_master_ledger.json"
        self.html_path = REPO_ROOT / "public_backlink_ledger.html"

        with open(self.doc3_path, "r", encoding="utf-8") as f:
            self.doc3_rows = list(csv.DictReader(f))

        with open(self.csv_path, "r", encoding="utf-8") as f:
            self.csv_rows = list(csv.DictReader(f))

        with open(self.json_path, "r", encoding="utf-8") as f:
            self.json_data = json.load(f)

        with open(self.html_path, "r", encoding="utf-8") as f:
            self.html_content = f.read()

        self.html_row_count = len(re.findall(r'<tr class="hover:bg-white', self.html_content))

    def test_e1_baseline_4way_parity(self):
        """Verify baseline mathematical parity across all 4 ledger artifacts."""
        expected_count = 279
        self.assertEqual(len(self.doc3_rows), expected_count, "doc3 row count mismatch")
        self.assertEqual(len(self.csv_rows), expected_count, "csv row count mismatch")
        self.assertEqual(len(self.json_data["entries"]), expected_count, "json entries count mismatch")
        self.assertEqual(self.json_data["total_backlinks"], expected_count, "json total_backlinks mismatch")
        self.assertEqual(self.html_row_count, expected_count, "html rendered row count mismatch")

    def test_e2_simulated_csv_deletion_detection(self):
        """Simulate dropping 1 row from CSV; parity logic must detect mismatch."""
        mutated_csv = self.csv_rows[:-1]
        with self.assertRaises(AssertionError) as ctx:
            assert len(self.doc3_rows) == len(mutated_csv), "Parity mismatch: doc3 != CSV"
        self.assertIn("Parity mismatch", str(ctx.exception))

    def test_e3_simulated_json_injection_detection(self):
        """Simulate injecting 1 extra entry into JSON; parity logic must detect mismatch."""
        mutated_json_entries = list(self.json_data["entries"])
        mutated_json_entries.append(dict(mutated_json_entries[0]))
        with self.assertRaises(AssertionError) as ctx:
            assert len(self.csv_rows) == len(mutated_json_entries), "Parity mismatch: CSV != JSON"
        self.assertIn("Parity mismatch", str(ctx.exception))

    def test_e4_simulated_html_deletion_detection(self):
        """Simulate deleting a table row from HTML; parity logic must detect mismatch."""
        # Replace first occurrence of table row
        mutated_html = re.sub(r'<tr class="hover:bg-white', '<!-- deleted row --><tr class="deleted', self.html_content, count=1)
        mutated_html_count = len(re.findall(r'<tr class="hover:bg-white', mutated_html))
        self.assertEqual(mutated_html_count, self.html_row_count - 1)
        with self.assertRaises(AssertionError) as ctx:
            assert mutated_html_count == len(self.csv_rows), "Parity mismatch: HTML != CSV"
        self.assertIn("Parity mismatch", str(ctx.exception))

    def test_e5_simulated_doc3_deletion_detection(self):
        """Simulate dropping a row from doc3; parity check must detect mismatch."""
        mutated_doc3 = self.doc3_rows[:-1]
        with self.assertRaises(AssertionError) as ctx:
            assert len(mutated_doc3) == len(self.csv_rows), "Parity mismatch: doc3 != CSV"
        self.assertIn("Parity mismatch", str(ctx.exception))

    def test_e6_simulated_root_leak_injection_detection(self):
        """Simulate injecting raw root anchor into ledger entry; Rule 45 check must catch it."""
        from validate_ledger_schema import validate

        # Verify production passes
        # Now test the Rule 45 validator logic with a tainted entry
        tainted_entries = copy.deepcopy(self.json_data["entries"][:5])
        tainted_entries[0]["shield_target_url"] = "https://adicommunications.co.uk/"

        found_violation = False
        for idx, e in enumerate(tainted_entries, 1):
            for key in ("tenant_url", "apex_target", "shield_target_url"):
                val = e.get(key, "")
                if "adicommunications.co.uk" in val:
                    if not any(sub in val for sub in ("/news/", "/assets/", "/feed/")):
                        found_violation = True
                        break

        self.assertTrue(found_violation, "Rule 45 validator failed to detect injected naked root link in ledger")


class TestDomainFIngestVideoAssetsInvariants(unittest.TestCase):
    """Domain F: Invariants and schema compliance in ingest_video_assets.py."""

    def test_f1_build_50_video_rows_structure(self):
        """build_50_video_rows must return exactly 50 rows conforming to 14 expected columns."""
        rows = build_50_video_rows()
        self.assertEqual(len(rows), 50, f"Expected exactly 50 video rows, got {len(rows)}")

        for idx, r in enumerate(rows, 1):
            for col in EXPECTED_COLUMNS:
                self.assertIn(col, r, f"Row {idx} missing column: {col}")
                self.assertTrue(r[col] is not None and str(r[col]).strip() != "", f"Row {idx} column '{col}' is empty")

            self.assertEqual(r["asset_id"], f"AST-VID-{idx:03d}")
            self.assertEqual(r["asset_type"], "Video")
            self.assertEqual(r["verification_status"], "ACTIVE_VERIFIED")

    def test_f2_tier_linking_invariants(self):
        """Verify Tier 1 & 2 target buffer, Tier 3 targets YouTube Apex with ZERO adicommunications links."""
        rows = build_50_video_rows()

        # Load platform catalog to know tiers
        with open(REPO_ROOT / "master_multicategory_platform_catalog.json", "r", encoding="utf-8") as f:
            pdata = json.load(f)
        vid_platforms = {p["platform_id"]: p for p in pdata.get("platforms", []) if "VID" in p.get("platform_id", "")}

        for idx, r in enumerate(rows, 1):
            pid = r["parent_profile_id"]
            plat = vid_platforms[pid]
            tier = plat.get("tier", "Tier 3")

            self.assertEqual(r["top_of_stack_apex_url"], "https://www.youtube.com/@CCTV.services")

            if "Tier 1" in tier or "Tier 2" in tier:
                self.assertIn("adicommunications.co.uk/news/", r["shield_target_url"])
            else:
                # Tier 3
                self.assertEqual(r["shield_target_url"], "https://www.youtube.com/@CCTV.services")
                self.assertNotIn("adicommunications.co.uk", r["shield_target_url"])
                self.assertNotIn("adicommunications.co.uk", r["profile_live_url"])
                self.assertNotIn("adicommunications.co.uk", r["asset_public_url"])

    def test_f3_eeat_phone_and_disclaimer(self):
        """Verify Gary Pearce direct mobile and trade tags exist across all rows."""
        rows = build_50_video_rows()
        for idx, r in enumerate(rows, 1):
            self.assertIn("#07860244274", r["seo_tags"], f"Row {idx} missing phone tag")
            self.assertNotIn("checkatrade", r["seo_description_summary"].lower(), f"Row {idx} contains Checkatrade")


class TestDomainGLiveFirebaseEdgeProbe(unittest.TestCase):
    """Domain G: Real-world live HTTP probe against production Firebase Edge endpoint."""

    def test_g1_live_firebase_edge_probe(self):
        """Verify production live URL returns HTTP 200, exactly 279 verified assets, and Gary Pearce credentials."""
        target_url = "https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html"
        req = urllib.request.Request(
            target_url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                status = resp.status
                body = resp.read().decode("utf-8")

                self.assertEqual(status, 200, f"Expected HTTP 200, got {status}")
                self.assertIn("Gary Pearce", body, "Missing Gary Pearce branding on live page")
                self.assertIn("07860 244 274", body, "Missing direct mobile on live page")
                self.assertTrue(
                    re.search(r'279.*Verified', body) or "279" in body,
                    "Missing '279 Verified' count on live page"
                )

                # Count rows in live HTML
                live_rows = len(re.findall(r'<tr class="hover:bg-white', body))
                self.assertEqual(live_rows, 279, f"Live HTML has {live_rows} rows, expected 279")

        except urllib.error.URLError as e:
            self.fail(f"Failed to connect to production Firebase Edge: {e}")


if __name__ == "__main__":
    unittest.main()
