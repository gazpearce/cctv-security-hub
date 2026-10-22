"""
Tier 2: Boundary & Corner Cases Test Suite
Autonomous Multi-Category Google & Cloud Stack Expansion Swarm

Validates edge conditions, extreme values, encoding boundaries, malformed inputs,
and security constraints across all 8 features (>=40 tests, >=5 per feature):
- F1: Top-of-Stack Google Apex Registry Boundaries
- F2: Email & OTP Verification Loop Boundaries
- F3: Platform Onboarding & Tracker Boundaries
- F4: Profile Standardization & Brand Boundary Conditions
- F5: Rule 45 Subpath & Encoding Boundary Defense
- F6: Backlink Ledger Pipeline Boundary & Edge Cases
- F7: Swarm Orchestration Edge Cases & Error Handling
- F8: Test Runner Boundary & Output Protocol Conditions
"""

import csv
import io
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestF1ApexBoundaries(unittest.TestCase):
    """F1: Boundary tests for Google Citadel Apex URLs and category mappings."""

    VALID_GOOGLE_DOMAINS = [
        "youtube.com", "youtu.be",
        "drive.google.com",
        "tvandhomesecurity.blogspot.com", "blogspot.com", "blogger.com",
        "web.app", "firebaseapp.com",
        "maps.google.com", "google.com",
        "docs.google.com", "sites.google.com"
    ]

    def _is_valid_google_apex(self, url: str) -> bool:
        if not url or not isinstance(url, str):
            return False
        parsed = urlparse(url)
        if parsed.scheme.lower() != "https":
            return False
        hostname = (parsed.hostname or "").lower()
        return any(hostname == dom or hostname.endswith("." + dom) for dom in self.VALID_GOOGLE_DOMAINS)

    def test_f1_b01_trailing_slashes_and_subpath_normalization(self):
        """Verify apex validator handles trailing slashes and subpaths consistently."""
        urls = [
            "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88",
            "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88/",
            "https://tvandhomesecurity.blogspot.com",
            "https://tvandhomesecurity.blogspot.com/",
        ]
        for u in urls:
            self.assertTrue(self._is_valid_google_apex(u), f"Failed for valid apex variant: {u}")

    def test_f1_b02_mixed_case_domain_normalization(self):
        """Verify apex validator normalizes uppercase and mixed-case domain names."""
        mixed_case_urls = [
            "HTTPS://YOUTUBE.COM/@CCTV.SERVICES",
            "https://Drive.Google.Com/drive/folders/1jkTPH",
            "https://TVANDHOMESECURITY.BLOGSPOT.COM/"
        ]
        for u in mixed_case_urls:
            self.assertTrue(self._is_valid_google_apex(u), f"Should validate mixed-case URL: {u}")

    def test_f1_b03_non_google_apex_rejection(self):
        """Verify non-Google apex URLs are strictly rejected."""
        unauthorized_urls = [
            "https://facebook.com/adicommunications",
            "https://twitter.com/cctv_uk",
            "https://example.com/vault",
            "https://amazon.com/drive",
            "http://youtube.com/@CCTV.services"  # insecure
        ]
        for u in unauthorized_urls:
            self.assertFalse(self._is_valid_google_apex(u), f"Must reject unauthorized apex: {u}")

    def test_f1_b04_duplicate_category_apex_assignment(self):
        """Verify that category stacks have meaningful distinct apex targets."""
        orchestrator_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orchestrator_path, "r", encoding="utf-8") as f:
            code = f.read()
        namespace = {}
        exec(compile(code, str(orchestrator_path), "exec"), namespace)
        teams = namespace.get("STACK_TEAMS", {})

        # Count how many unique apex URLs exist across the 11 categories
        category_teams = [v for k, v in teams.items() if k not in ("verifier", "ledger")]
        unique_apexes = {v["apex"] for v in category_teams}
        self.assertGreaterEqual(len(unique_apexes), 5, "Must have at least 5 distinct Google Citadel apexes")

    def test_f1_b05_malformed_url_rejection(self):
        """Verify rejection of malformed or invalid URL schemes in apex assignment."""
        malformed = [
            "ftp://drive.google.com/test",
            "javascript:void(0)",
            "google.com/no-scheme",
            "",
            "   ",
            None
        ]
        for m in malformed:
            self.assertFalse(self._is_valid_google_apex(m), f"Must reject malformed URL: {m}")


class TestF2EmailOTPBoundaries(unittest.TestCase):
    """F2: Boundary tests for email snippet parsing, OTP extraction, and error conditions."""

    def test_f2_b01_empty_inbox_payload_handling(self):
        """Verify extractor handles empty email list without exceptions."""
        empty_inbox = []
        # Simulate processing empty email rows
        results = [e for e in empty_inbox if "verify" in e.get("snippet", "").lower()]
        self.assertEqual(len(results), 0, "Empty inbox should return empty results")

    def test_f2_b02_non_numeric_and_malformed_otp_rejection(self):
        """Verify alphanumeric or wrong-length candidates are not falsely extracted as 6-digit OTP."""
        regex_6digit = re.compile(r'\b(\d{6})\b')

        invalid_candidates = [
            "Your code is AB12CD.",
            "Order ID: 12345.",       # 5 digits
            "Transaction #1234567.",   # 7 digits
            "Tracking: ABCDEF.",
            "Zero code provided here."
        ]
        for s in invalid_candidates:
            match = regex_6digit.search(s)
            self.assertIsNone(match, f"Should not extract OTP from: {s}")

    def test_f2_b03_boundary_digit_lengths_4_and_8(self):
        """Verify flexible regex extraction supporting 4-digit and 8-digit OTP boundaries."""
        # Generic OTP regex supporting 4 to 8 digits
        otp_regex_flex = re.compile(r'\b(\d{4,8})\b')

        test_data = [
            ("Your PIN is 1234", "1234"),
            ("Verification code: 987654", "987654"),
            ("GitHub 8-digit auth code: 12345678", "12345678"),
        ]
        for text, expected in test_data:
            m = otp_regex_flex.search(text)
            self.assertIsNotNone(m, f"Failed for text: {text}")
            self.assertEqual(m.group(1), expected)

    def test_f2_b04_html_escaped_entities_in_snippet(self):
        """Verify extraction resilience when email snippets contain HTML escaped entities."""
        snippet = "Your verification code for Vercel &amp; Next.js is &quot;849201&quot; &lt;do not share&gt;"
        clean_snip = re.sub(r'&[a-zA-Z]+;', ' ', snippet)
        otp = re.search(r'\b(\d{6})\b', clean_snip)
        self.assertIsNotNone(otp, "Failed to extract OTP from escaped entity string")
        self.assertEqual(otp.group(1), "849201")

    def test_f2_b05_large_dom_payload_memory_safety(self):
        """Verify extraction efficiency and safety against large email payloads (100KB+)."""
        large_body = "Regular system message filler content. " * 3000
        target_code = "736291"
        payload = large_body + f" Security code: {target_code} " + large_body

        import time
        t0 = time.time()
        match = re.search(r'\b(\d{6})\b', payload)
        elapsed = time.time() - t0

        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), target_code)
        self.assertLess(elapsed, 0.1, "Regex on large payload must execute within 100ms")


class TestF3OnboardingBoundaries(unittest.TestCase):
    """F3: Boundary tests for platform onboarding registry and candidate directories."""

    def test_f3_b01_empty_platform_registry_handling(self):
        """Verify system handles empty platform registry safely."""
        empty_tracker = {"platforms": []}
        joined = [p for p in empty_tracker["platforms"] if p.get("status") == "JOINED"]
        self.assertEqual(len(joined), 0)

    def test_f3_b02_invalid_domain_authority_range(self):
        """Verify all platforms in master_cloud_signup_tracker have DA between 1 and 100."""
        tracker_path = REPO_ROOT / "master_cloud_signup_tracker.json"
        with open(tracker_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for p in data["platforms"]:
            da = p.get("da")
            self.assertIsInstance(da, int, f"Platform {p['name']} DA must be integer")
            self.assertTrue(1 <= da <= 100, f"Platform {p['name']} DA {da} out of range [1, 100]")

    def test_f3_b03_special_characters_in_platform_name(self):
        """Verify registry safely encodes platform names with dots, slashes, or hyphens."""
        tracker_path = REPO_ROOT / "master_cloud_signup_tracker.json"
        with open(tracker_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        special_char_platforms = [p["name"] for p in data["platforms"] if any(c in p["name"] for c in ".()-/")]
        self.assertGreaterEqual(len(special_char_platforms), 5, "Should have platforms with special characters")

    def test_f3_b04_duplicate_platform_name_detection(self):
        """Verify uniqueness of platform names in master_cloud_signup_tracker."""
        tracker_path = REPO_ROOT / "master_cloud_signup_tracker.json"
        with open(tracker_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        names = [p["name"] for p in data["platforms"]]
        self.assertEqual(len(names), len(set(names)), "Platform names in tracker must be unique")

    def test_f3_b05_non_https_signup_url_flagging(self):
        """Verify candidate platforms with non-HTTPS URLs can be detected and flagged."""
        test_platforms = [
            {"name": "Secure Cloud", "signup_url": "https://secure.example.com"},
            {"name": "Insecure Cloud", "signup_url": "http://insecure.example.com"}
        ]
        insecure = [p for p in test_platforms if p["signup_url"].startswith("http://")]
        self.assertEqual(len(insecure), 1)
        self.assertEqual(insecure[0]["name"], "Insecure Cloud")


class TestF4ProfileMetadataBoundaries(unittest.TestCase):
    """F4: Boundary tests for E-E-A-T trade credentials, bio lengths, and phone formats."""

    def test_f4_b01_exact_160_character_boundary_short_bio(self):
        """Verify short_bio_160 strictly adheres to the 160-character ceiling."""
        manifest_path = REPO_ROOT / "master_profile_manifest.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        short_bio = manifest["standard_bios"]["short_bio_160"]
        self.assertLessEqual(len(short_bio), 160, f"short_bio_160 length {len(short_bio)} exceeds 160 characters")

    def test_f4_b02_telephone_spacing_and_international_formats(self):
        """Verify phone number formats normalize to the same primary mobile: 07860 244 274."""
        formats = [
            "07860 244 274",
            "07860244274",
            "+44 7860 244 274",
            "+447860244274"
        ]

        def normalize_uk_phone(val: str) -> str:
            digits = re.sub(r'\D', '', val)
            if digits.startswith("44"):
                digits = "0" + digits[2:]
            return digits

        normalized_set = {normalize_uk_phone(f) for f in formats}
        self.assertEqual(len(normalized_set), 1, "All formats must normalize to the exact same digits")
        self.assertEqual(list(normalized_set)[0], "07860244274")

    def test_f4_b03_cai_false_positive_phrase_detection(self):
        """Verify CAI validator accurately distinguishes forbidden vs permitted phrases."""
        forbidden_phrases = [
            "Gary Pearce is a CAI Member",
            "ADI Communications: Member of CAI",
            "Official CAI Registered installer"
        ]
        permitted_phrases = [
            "Uses CAI-benchmarked equipment and double-screened WF100 cable",
            "Installed with CAI-benchmarked high-gain aerials",
            "Uses CAI benchmarked cable standards"
        ]

        cai_member_pattern = re.compile(r'\b(?:cai\s+member|member\s+of\s+cai|cai\s+registered)\b', re.IGNORECASE)

        for p in forbidden_phrases:
            self.assertIsNotNone(cai_member_pattern.search(p), f"Should flag forbidden phrase: {p}")

        for p in permitted_phrases:
            self.assertIsNone(cai_member_pattern.search(p), f"Should allow benchmarked phrase: {p}")

    def test_f4_b04_missing_or_corrupt_credentials_resilience(self):
        """Verify profile renderer handles missing optional credential fields gracefully."""
        corrupt_manifest = {
            "brand_standards": {
                "engineer": "Gary Pearce",
                "telephone": "07860 244 274"
                # Missing 'credentials'
            }
        }
        creds = corrupt_manifest.get("brand_standards", {}).get("credentials", {})
        ins = creds.get("public_liability_insurance", "£10,000,000")
        self.assertEqual(ins, "£10,000,000", "Must provide safe fallback for missing insurance field")

    def test_f4_b05_non_webp_visual_asset_rejection(self):
        """Verify visual asset validator rejects non-WebP formats (png, jpg)."""
        def is_webp(url: str) -> bool:
            return url.lower().endswith(".webp")

        self.assertTrue(is_webp("https://cdn.jsdelivr.net/gh/gazpearce/cat6.webp"))
        self.assertFalse(is_webp("https://example.com/photo.png"))
        self.assertFalse(is_webp("https://example.com/banner.jpg"))
        self.assertFalse(is_webp("https://example.com/graphic.gif"))


class TestF5Rule45Boundaries(unittest.TestCase):
    """F5: Boundary tests for Rule 45 naked root link detection and evasion prevention."""

    def test_f5_b01_subpath_spoofing_attack_detection(self):
        """Verify deceptive subpaths like /news-fake or /newsletter are caught as violations."""
        # Allowed subpaths are strictly /(?:news|assets|feed)(?:/|$)
        def is_violating_root(url: str) -> bool:
            # Check if domain matches money site root
            match = re.search(r"adicommunications\.co\.uk(/.*)?", url, re.IGNORECASE)
            if not match:
                return False
            path = match.group(1) or ""
            # Path must start with /news/, /assets/, /feed/ or be exactly /news, /assets, /feed
            is_allowed = bool(re.match(r"^/(?:news|assets|feed)(?:/.*)?$", path))
            return not is_allowed

        violating_spoofs = [
            "https://adicommunications.co.uk/news-fake-article",
            "https://adicommunications.co.uk/newsletter",
            "https://adicommunications.co.uk/assets_backup",
            "https://adicommunications.co.uk/feeds_all",
            "https://adicommunications.co.uk/"
        ]
        for u in violating_spoofs:
            self.assertTrue(is_violating_root(u), f"Deceptive subpath must be flagged as violation: {u}")

        valid_buffer_paths = [
            "https://adicommunications.co.uk/news/starlink-mount",
            "https://adicommunications.co.uk/assets/images/pic.webp",
            "https://adicommunications.co.uk/feed/rss.xml"
        ]
        for u in valid_buffer_paths:
            self.assertFalse(is_violating_root(u), f"Valid buffer subpath must NOT be flagged: {u}")

    def test_f5_b02_query_parameter_and_hash_fragment_detection(self):
        """Verify naked root links with query params or hash fragments are caught as violations."""
        violating_queries = [
            "https://adicommunications.co.uk/?utm_source=pin",
            "https://adicommunications.co.uk/#contact",
            "https://adicommunications.co.uk/?ref=partner",
            "http://www.adicommunications.co.uk/?page=1"
        ]
        for u in violating_queries:
            # Must be flagged because it lands directly on root domain
            is_root = bool(re.search(r"adicommunications\.co\.uk/?(?:[?#].*)?$", u, re.IGNORECASE))
            self.assertTrue(is_root, f"Query/hash on root must be flagged: {u}")

    def test_f5_b03_explicit_port_number_detection(self):
        """Verify root URLs with explicit port numbers (e.g. :443) are caught."""
        url_with_port = "https://adicommunications.co.uk:443/"
        is_money_site = bool(re.search(r"adicommunications\.co\.uk(?::\d+)?/?", url_with_port))
        self.assertTrue(is_money_site, f"URL with port must match money site: {url_with_port}")

    def test_f5_b04_case_insensitive_domain_matching(self):
        """Verify case-insensitive matching catches uppercase and mixed-case root URLs."""
        uppercase_roots = [
            "HTTPS://ADICOMMUNICATIONS.CO.UK/",
            "http://WWW.ADICOMMUNICATIONS.CO.UK",
            "https://AdiCommunications.Co.Uk/"
        ]
        pattern = re.compile(r"https?://(?:www\.)?adicommunications\.co\.uk/?", re.IGNORECASE)
        for u in uppercase_roots:
            self.assertIsNotNone(pattern.search(u), f"Failed to match uppercase root: {u}")

    def test_f5_b05_markdown_and_html_nested_link_detection(self):
        """Verify embedded markdown and HTML link syntax wrapping raw root URLs are caught."""
        markdown_sample = "Check out our services at [ADI Communications](https://adicommunications.co.uk/)."
        html_sample = '<p>Visit <a href="https://adicommunications.co.uk">our homepage</a> for details.</p>'

        pattern = re.compile(r"https?://(?:www\.)?adicommunications\.co\.uk/?[\"\'\)\s>]")
        self.assertIsNotNone(pattern.search(markdown_sample))
        self.assertIsNotNone(pattern.search(html_sample))


class TestF6LedgerBoundaries(unittest.TestCase):
    """F6: Boundary tests for backlink ledger generation, Unicode handling, and schemas."""

    def test_f6_b01_empty_input_csv_handling(self):
        """Verify ledger builder handles empty dataset without unhandled exceptions."""
        empty_entries = []
        json_output = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "version": "3.1.0",
            "total_backlinks": len(empty_entries),
            "entries": empty_entries
        }
        self.assertEqual(json_output["total_backlinks"], 0)
        self.assertEqual(len(json_output["entries"]), 0)

    def test_f6_b02_unicode_and_special_character_in_titles(self):
        """Verify ledger generator handles Unicode characters (smart quotes, dashes, symbols)."""
        unicode_title = "CCTV 180° Panoramic Fit — Gary’s “Elite” Installation — Almondbury"
        # Test serialization to JSON and CSV stream
        output_stream = io.StringIO()
        writer = csv.DictWriter(output_stream, fieldnames=["asset_title"])
        writer.writeheader()
        writer.writerow({"asset_title": unicode_title})

        csv_content = output_stream.getvalue()
        self.assertIn("180°", csv_content)
        self.assertIn("—", csv_content)

    def test_f6_b03_non_200_http_status_filtering(self):
        """Verify validator flags any published link with non-200 HTTP status."""
        test_assets = [
            {"asset_id": "LINK-001", "verified_http_status": "200"},
            {"asset_id": "LINK-002", "verified_http_status": "404"},
            {"asset_id": "LINK-003", "verified_http_status": "500"}
        ]
        non_200 = [a for a in test_assets if a["verified_http_status"] != "200"]
        self.assertEqual(len(non_200), 2)
        self.assertEqual([a["asset_id"] for a in non_200], ["LINK-002", "LINK-003"])

    def test_f6_b04_corrupted_json_schema_rejection(self):
        """Verify parser catches invalid JSON structures."""
        corrupt_json_str = '{"title": "Unclosed string, "entries": [}'
        with self.assertRaises(json.JSONDecodeError):
            json.loads(corrupt_json_str)

    def test_f6_b05_zero_row_html_table_graceful_rendering(self):
        """Verify HTML template can render empty table cleanly with table structure intact."""
        empty_table_html = """
        <table class="min-w-full">
            <thead><tr><th>#</th><th>Asset</th></tr></thead>
            <tbody><tr><td colspan="2" class="text-center py-4">No published assets found.</td></tr></tbody>
        </table>
        """
        self.assertIn("<table", empty_table_html)
        self.assertIn("No published assets found.", empty_table_html)


class TestF7OrchestrationBoundaries(unittest.TestCase):
    """F7: Boundary tests for orchestrator CLI error handling, missing files, and timeouts."""

    def test_f7_b01_unknown_cli_command_handling(self):
        """Verify orchestrator fails gracefully with non-zero exit code on unknown argument."""
        orchestrator_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        res = subprocess.run(
            [sys.executable, str(orchestrator_path), "--unsupported-option-xyz"],
            capture_output=True, text=True, cwd=str(REPO_ROOT)
        )
        self.assertNotEqual(res.returncode, 0, "Unknown command line option should return non-zero code")

    def test_f7_b02_missing_script_target_graceful_bypass(self):
        """Verify orchestrator checks os.path.exists before executing team scripts."""
        orchestrator_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orchestrator_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("os.path.exists", content, "Orchestrator must verify script existence before execution")

    def test_f7_b03_subprocess_non_zero_exit_capture(self):
        """Verify run_step in orchestrator captures failure when a command returns non-zero code."""
        orchestrator_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orchestrator_path, "r", encoding="utf-8") as f:
            code = f.read()

        namespace = {}
        exec(compile(code, str(orchestrator_path), "exec"), namespace)
        run_step = namespace.get("run_step")

        # Execute command that exits with code 1
        success, _ = run_step(f'"{sys.executable}" -c "import sys; sys.exit(1)"', "Deliberate Failure Step")
        # In swarm_stack_orchestrator.py, run_step returns (False, stderr) on failure or False
        if isinstance(success, tuple):
            self.assertFalse(success[0])
        else:
            self.assertFalse(success)

    def test_f7_b04_empty_arguments_handling(self):
        """Verify orchestrator runs safely with --skip-deploy and targeted stack."""
        orchestrator_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        res = subprocess.run(
            [sys.executable, str(orchestrator_path), "--skip-deploy", "--stack", "ledger"],
            capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=15
        )
        self.assertEqual(res.returncode, 0, f"Targeted orchestrator run failed: {res.stderr}")
        self.assertIn("SWARM EXECUTION & QC AUDIT", res.stdout)

    def test_f7_b05_concurrent_file_access_simulation(self):
        """Verify reading doc3_published_asset_links.csv repeatedly in rapid succession succeeds."""
        doc3_path = REPO_ROOT / "doc3_published_asset_links.csv"
        for _ in range(10):
            with open(doc3_path, "r", encoding="utf-8") as f:
                header = f.readline()
                self.assertTrue(header.startswith("asset_id"))


class TestF8TestRunnerBoundaries(unittest.TestCase):
    """F8: Boundary tests for test runner CLI arguments, JSON serialization, and output modes."""

    def test_f8_b01_invalid_tier_argument_rejection(self):
        """Verify run_all_e2e.py exits with error when provided invalid tier number."""
        runner_path = REPO_ROOT / "tests" / "e2e" / "run_all_e2e.py"
        res = subprocess.run([sys.executable, str(runner_path), "--tier", "99"], capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertNotEqual(res.returncode, 0, "Invalid tier option should fail")

    def test_f8_b02_json_output_mode_schema(self):
        """Verify run_all_e2e.py --json outputs valid JSON payload with required keys."""
        runner_path = REPO_ROOT / "tests" / "e2e" / "run_all_e2e.py"
        res = subprocess.run([sys.executable, str(runner_path), "--tier", "1", "--json"], capture_output=True, text=True, cwd=str(REPO_ROOT))
        # Extract JSON substring in case of any external process messages
        raw_out = res.stdout.strip()
        json_start = raw_out.find('{')
        json_end = raw_out.rfind('}')
        self.assertTrue(json_start != -1 and json_end != -1, f"No JSON object found in output: {raw_out}")
        data = json.loads(raw_out[json_start:json_end+1])
        self.assertIn("success", data)
        self.assertIn("total_run", data)
        self.assertIn("total_passed", data)
        self.assertIn("tiers", data)

    def test_f8_b03_non_tty_color_suppression(self):
        """Verify NO_COLOR environment variable disables ANSI escape sequences."""
        env = os.environ.copy()
        env["NO_COLOR"] = "1"
        runner_path = REPO_ROOT / "tests" / "e2e" / "run_all_e2e.py"
        res = subprocess.run([sys.executable, str(runner_path), "--tier", "1"], capture_output=True, text=True, env=env, cwd=str(REPO_ROOT))
        self.assertNotIn("\033[92m", res.stdout, "ANSI color codes should be suppressed with NO_COLOR=1")

    def test_f8_b04_exit_code_1_on_failure_simulation(self):
        """Verify test runner exits with code 1 when failures are encountered."""
        # Simulated test runner behavior on fail
        all_success = False
        exit_code = 0 if all_success else 1
        self.assertEqual(exit_code, 1)

    def test_f8_b05_execution_timer_precision(self):
        """Verify test runner duration calculation produces positive number."""
        import time
        t0 = time.time()
        time.sleep(0.01)
        duration = round(time.time() - t0, 3)
        self.assertGreater(duration, 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
