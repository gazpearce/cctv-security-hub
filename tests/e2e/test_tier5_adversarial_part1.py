#!/usr/bin/env python3
"""
tests/e2e/test_tier5_adversarial_part1.py
Milestone 5 Tier 5 White-Box Adversarial Hardening Suite — Part 1
Targeting Domains 1, 2, and 5:

Domain 1: Rule 45 Obfuscation & Tier 3 Video Isolation
- Tests Rule 45 evasion attempts against verify_no_root_anchors.py:
  * percent-encoded slashes (%2F, %2f)
  * mixed-case domain ('aDiCoMmunICations.co.uk', 'ADICOMMUNICATIONS.CO.UK')
  * port-appended root ('adicommunications.co.uk:443/', 'adicommunications.co.uk:80/')
  * scheme-relative root ('//adicommunications.co.uk/', '//adicommunications.co.uk')
  * trailing FQDN dot ('adicommunications.co.uk./')
  * path traversal escape ('adicommunications.co.uk/news/../../')
- Tests Tier 3 video platforms (Rumble, BitChute, Odysee, PeerTube, DTube):
  * Link ONLY to YouTube apex (@CCTV.services or watch URLs)
  * ZERO links to adicommunications.co.uk website (including /news/ buffer)
  * Mathematical verification across doc3, doc2, public_backlink_master_ledger, and manifest

Domain 2: Verification Loop & CDP Error Handling (auto_email_verifier.py)
- Tests OTP extraction resilience against multi-numeric strings:
  * phone numbers (07860 244 274, +44 7860 244 274, UK landline/mobile)
  * ISO timestamps & YYYYMMDD dates
  * tracking IDs / order numbers (TRACK-9876543210, Order #9876543210)
  * mixed multi-numeric email body
  * spaced 6/8-digit codes, reverse patterns, alphanumeric tokens
  * negative rejection of banned years (1900-2099), prices (£129), promo codes
- Tests CDP 9223 unreachable / socket error handling:
  * connection refused (port 9999 / closed port)
  * connection timeout / unroutable IP (192.0.2.1)
  * malformed JSON from CDP endpoint
  * broken WebSocket connection handling

Domain 5: Orchestrator Subcommand Robustness & Reachability (swarm_stack_orchestrator.py)
- Tests subcommand argument parsing:
  * malformed subcommand arguments exit with code 2
  * malformed --stack arguments exit with code 2
  * malformed flags exit with code 2
  * valid subcommands recognized
- Tests check_url_reachability():
  * timeout exhaustion on slow servers returns (False, None, timeout_msg, elapsed)
  * SSL handshake failure caught cleanly without unhandled exception
  * connection refused caught cleanly
  * HTTP 404, 429, 500, 503 error status propagation
  * HTTP 301/302 redirect resolution to 200
"""

import asyncio
import csv
import http.server
import json
import os
import re
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from auto_email_verifier import AutoEmailVerifier
from automated_platform_onboarder import IntegrityFirewall
from swarm_stack_orchestrator import check_url_reachability, STACK_TEAMS


class TestDomain1Rule45AdversarialAndTier3Isolation(unittest.TestCase):
    """Domain 1: White-box adversarial testing of Rule 45 obfuscation and Tier 3 video isolation."""

    def _run_scanner_on_line(self, test_line: str) -> bool:
        """
        Executes the exact detection logic from verify_no_root_anchors.py on a test line.
        Returns True if the line was flagged as a violation, False if it evaded detection.
        """
        # Exact implementation from verify_no_root_anchors.py lines 16-18:
        # if re.search(r"https?://(?:www\.)?adicommunications\.co\.uk/?(?:$|[?#\"'\s<>,;)\]}])", line):
        #     if not re.search(r"adicommunications\.co\.uk/(?:news|assets|feed)", line):
        #         violations.append(...)
        is_root = bool(re.search(r"https?://(?:www\.)?adicommunications\.co\.uk/?(?:$|[?#\"'\s<>,;)\]}])", test_line))
        is_exempt = bool(re.search(r"adicommunications\.co\.uk/(?:news|assets|feed)", test_line))
        return is_root and not is_exempt

    def _run_script_on_temp_file(self, content: str) -> int:
        """
        Creates a temporary file inside REPO_ROOT with content, invokes verify_no_root_anchors.py,
        and returns its process return code (0 = PASS, 1 = FAIL/VIOLATION FOUND).
        Cleans up the file before returning.
        """
        temp_file = REPO_ROOT / f"tmp_probe_{os.getpid()}_{time.time_ns()}.csv"
        try:
            temp_file.write_text(content, encoding="utf-8")
            res = subprocess.run(
                [sys.executable, str(REPO_ROOT / "verify_no_root_anchors.py")],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            return res.returncode
        finally:
            if temp_file.exists():
                temp_file.unlink()

    def test_d1_01_verify_no_root_anchors_baseline_pass(self):
        """Verify that verify_no_root_anchors.py currently exits with 0 on clean repository."""
        res = subprocess.run(
            [sys.executable, str(REPO_ROOT / "verify_no_root_anchors.py")],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT)
        )
        self.assertEqual(res.returncode, 0, f"Baseline check failed: {res.stdout} {res.stderr}")
        self.assertIn("RULE 45 PASS", res.stdout)

    def test_d1_02_canonical_naked_root_caught_by_scanner(self):
        """Canonical naked root link must be detected and return exit code 1."""
        content = "platform,url\nTest,https://adicommunications.co.uk/\n"
        exit_code = self._run_script_on_temp_file(content)
        self.assertEqual(exit_code, 1, "verify_no_root_anchors.py failed to catch canonical naked root!")

    def test_d1_03_mixed_case_obfuscation_evasion(self):
        """
        Test Rule 45 detection against mixed-case domain variations:
        'https://aDiCoMmunICations.co.uk/', 'https://ADICOMMUNICATIONS.CO.UK/'.
        Demonstrates vulnerability if verify_no_root_anchors.py lacks case-insensitivity.
        """
        cases = [
            "https://aDiCoMmunICations.co.uk/",
            "http://ADICOMMUNICATIONS.CO.UK/",
            "https://www.ADICOMMUNICATIONS.co.uk/",
            "https://Adicommunications.co.uk/"
        ]
        evaded_cases = []
        for c in cases:
            flagged = self._run_scanner_on_line(f"url: {c}")
            if not flagged:
                evaded_cases.append(c)

        # Assert scanner catches mixed-case obfuscation
        self.assertEqual(
            evaded_cases, [],
            f"VULNERABILITY: verify_no_root_anchors.py failed to catch mixed-case evasion: {evaded_cases}"
        )

    def test_d1_04_port_appended_obfuscation_evasion(self):
        """
        Test Rule 45 detection against port-appended naked root URLs:
        'https://adicommunications.co.uk:443/', 'http://adicommunications.co.uk:80/'.
        Demonstrates vulnerability if verify_no_root_anchors.py assumes no port.
        """
        cases = [
            "https://adicommunications.co.uk:443/",
            "https://adicommunications.co.uk:443",
            "http://adicommunications.co.uk:80/",
            "https://www.adicommunications.co.uk:443/",
            "https://adicommunications.co.uk:8080/"
        ]
        evaded_cases = []
        for c in cases:
            flagged = self._run_scanner_on_line(f"url: {c}")
            if not flagged:
                evaded_cases.append(c)

        self.assertEqual(
            evaded_cases, [],
            f"VULNERABILITY: verify_no_root_anchors.py failed to catch port-appended evasion: {evaded_cases}"
        )

    def test_d1_05_scheme_relative_obfuscation_evasion(self):
        """
        Test Rule 45 detection against protocol/scheme-relative URLs:
        '//adicommunications.co.uk/', '//www.adicommunications.co.uk/'.
        Demonstrates vulnerability if verify_no_root_anchors.py requires 'https?:'.
        """
        cases = [
            "//adicommunications.co.uk/",
            "//adicommunications.co.uk",
            "//www.adicommunications.co.uk/",
            "//www.adicommunications.co.uk"
        ]
        evaded_cases = []
        for c in cases:
            flagged = self._run_scanner_on_line(f'<a href="{c}">Home</a>')
            if not flagged:
                evaded_cases.append(c)

        self.assertEqual(
            evaded_cases, [],
            f"VULNERABILITY: verify_no_root_anchors.py failed to catch scheme-relative evasion: {evaded_cases}"
        )

    def test_d1_06_percent_encoded_slashes_obfuscation_evasion(self):
        """
        Test Rule 45 detection against percent-encoded slashes and characters:
        'https://adicommunications.co.uk%2F', 'https://adicommunications.co.uk%2f'.
        Demonstrates vulnerability if verify_no_root_anchors.py does not unquote URLs.
        """
        cases = [
            "https://adicommunications.co.uk%2F",
            "https://adicommunications.co.uk%2f",
            "https://www.adicommunications.co.uk%2F",
            "https://adicommunications.co.uk%2findex.html"
        ]
        evaded_cases = []
        for c in cases:
            flagged = self._run_scanner_on_line(f"url: {c}")
            if not flagged:
                evaded_cases.append(c)

        self.assertEqual(
            evaded_cases, [],
            f"VULNERABILITY: verify_no_root_anchors.py failed to catch percent-encoded slash evasion: {evaded_cases}"
        )

    def test_d1_07_trailing_fqdn_dot_obfuscation_evasion(self):
        """
        Test Rule 45 detection against trailing FQDN dot:
        'https://adicommunications.co.uk./'.
        """
        cases = [
            "https://adicommunications.co.uk./",
            "https://adicommunications.co.uk.",
            "https://www.adicommunications.co.uk./"
        ]
        evaded_cases = []
        for c in cases:
            flagged = self._run_scanner_on_line(f"url: {c}")
            if not flagged:
                evaded_cases.append(c)

        self.assertEqual(
            evaded_cases, [],
            f"VULNERABILITY: verify_no_root_anchors.py failed to catch trailing FQDN dot evasion: {evaded_cases}"
        )

    def test_d1_08_path_traversal_escaping_obfuscation_evasion(self):
        """
        Test Rule 45 detection against path traversal that escapes /news/ or /assets/ back to root:
        'https://adicommunications.co.uk/news/../../', 'https://adicommunications.co.uk/assets/../'.
        """
        cases = [
            "https://adicommunications.co.uk/news/../../",
            "https://adicommunications.co.uk/news/../",
            "https://adicommunications.co.uk/assets/../"
        ]
        evaded_cases = []
        for c in cases:
            flagged = self._run_scanner_on_line(f"url: {c}")
            if not flagged:
                evaded_cases.append(c)

        self.assertEqual(
            evaded_cases, [],
            f"VULNERABILITY: verify_no_root_anchors.py failed to catch path traversal escape: {evaded_cases}"
        )

    def test_d1_09_integrity_firewall_rule45_adversarial_coverage(self):
        """
        Test IntegrityFirewall.validate_layer5_rule_45 against the full matrix of evasion techniques.
        """
        adversarial_matrix = [
            ("https://aDiCoMmunICations.co.uk/", "mixed-case"),
            ("https://adicommunications.co.uk:443/", "port-appended"),
            ("//adicommunications.co.uk/", "scheme-relative"),
            ("https://adicommunications.co.uk%2F", "percent-encoded slash"),
            ("https://adicommunications.co.uk./", "trailing dot"),
            ("https://adicommunications.co.uk/news/../../", "path traversal escape")
        ]
        failures = []
        for url, desc in adversarial_matrix:
            passed, msg = IntegrityFirewall.validate_layer5_rule_45(url)
            # Must return passed=False (violation detected)
            if passed:
                failures.append((desc, url, msg))

        self.assertEqual(
            failures, [],
            f"VULNERABILITY: IntegrityFirewall.validate_layer5_rule_45 failed to catch evasion vectors: {failures}"
        )

    def test_d1_10_tier3_video_platforms_link_exclusively_to_youtube(self):
        """
        Verify that 100% of Tier 3 video platforms (Rumble, BitChute, Odysee, PeerTube, DTube)
        link EXCLUSIVELY to YouTube apex with ZERO links to adicommunications.co.uk website.
        Audits: doc3_published_asset_links.csv, doc2_established_profiles_list.csv,
        and public_backlink_master_ledger.json.
        """
        tier3_keywords = ["rumble", "bitchute", "odysee", "peertube", "dtube"]

        # 1. Audit doc3
        doc3_file = REPO_ROOT / "doc3_published_asset_links.csv"
        self.assertTrue(doc3_file.exists(), "doc3_published_asset_links.csv must exist")

        checked_t3_count = 0
        with open(doc3_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                plat_lower = row.get("platform_name", "").lower()
                if any(t in plat_lower for t in tier3_keywords):
                    checked_t3_count += 1
                    apex = row.get("top_of_stack_apex_url", "")
                    shield = row.get("shield_target_url", "")
                    desc = row.get("seo_description_summary", "")

                    # Must link to YouTube apex
                    self.assertTrue(
                        "youtube.com" in apex or "youtu.be" in apex,
                        f"Tier 3 platform {row.get('platform_name')} apex must be YouTube, got: '{apex}'"
                    )

                    # Must have ZERO links to adicommunications.co.uk website
                    self.assertNotIn(
                        "adicommunications.co.uk", shield.lower(),
                        f"Tier 3 platform {row.get('platform_name')} violates isolation: shield links to adicommunications: '{shield}'"
                    )
                    self.assertNotIn(
                        "adicommunications.co.uk", desc.lower(),
                        f"Tier 3 platform {row.get('platform_name')} violates isolation: description links to adicommunications: '{desc}'"
                    )

        self.assertGreaterEqual(checked_t3_count, 4, "Must audit at least 4 Tier 3 video platforms in doc3")

        # 2. Audit doc2
        doc2_file = REPO_ROOT / "doc2_established_profiles_list.csv"
        self.assertTrue(doc2_file.exists(), "doc2_established_profiles_list.csv must exist")
        with open(doc2_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                plat_lower = row.get("platform_name", "").lower()
                if any(t in plat_lower for t in tier3_keywords):
                    anchor = row.get("shield_anchor_url", "")
                    self.assertTrue(
                        "youtube.com" in anchor or "youtu.be" in anchor,
                        f"Tier 3 profile {row.get('platform_name')} anchor must be YouTube, got: '{anchor}'"
                    )
                    self.assertNotIn(
                        "adicommunications.co.uk", anchor.lower(),
                        f"Tier 3 profile {row.get('platform_name')} links to adicommunications: '{anchor}'"
                    )

        # 3. Audit ledger JSON
        ledger_file = REPO_ROOT / "public_backlink_master_ledger.json"
        self.assertTrue(ledger_file.exists(), "public_backlink_master_ledger.json must exist")
        with open(ledger_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for entry in data.get("entries", []):
                plat_lower = entry.get("platform", "").lower()
                if any(t in plat_lower for t in tier3_keywords):
                    apex = entry.get("apex_target", "")
                    shield = entry.get("shield_target_url", "")
                    self.assertTrue(
                        "youtube.com" in apex or "youtu.be" in apex,
                        f"Tier 3 ledger entry {entry.get('platform')} apex must be YouTube, got: '{apex}'"
                    )
                    self.assertNotIn(
                        "adicommunications.co.uk", shield.lower(),
                        f"Tier 3 ledger entry {entry.get('platform')} shield links to adicommunications: '{shield}'"
                    )


class TestDomain2VerificationAndCdpErrorHandling(unittest.TestCase):
    """Domain 2: White-box testing of OTP extraction resilience and CDP socket error handling."""

    def test_d2_01_otp_extraction_phone_number_resilience(self):
        """OTP extraction must ignore Gary Pearce and UK phone numbers and accurately extract 4-8 digit OTP."""
        verifier = AutoEmailVerifier()

        test_cases = [
            (
                "Your verification code is 482915. For support, call Gary Pearce on 07860 244 274.",
                "482915"
            ),
            (
                "Use security code 592019 to log in. Queries: +44 7860 244 274.",
                "592019"
            ),
            (
                "Call (07860) 244274. Your one-time passcode: 382910.",
                "382910"
            ),
            (
                "UK office: 01422 123456. One-time pin is 849201.",
                "849201"
            ),
            (
                "Emergency dispatch 07860-244-274. Code: 49281.",
                "49281"
            )
        ]

        for text, expected in test_cases:
            with self.subTest(text=text, expected=expected):
                result = verifier.extract_otp_from_text(text)
                self.assertEqual(result, expected, f"Failed extracting OTP from phone number context: '{text}'")

    def test_d2_02_otp_extraction_timestamp_and_date_resilience(self):
        """OTP extraction must ignore ISO timestamps, YYYYMMDD dates, and banned years (1900-2099)."""
        verifier = AutoEmailVerifier()

        test_cases = [
            (
                "Timestamp: 2026-10-22 14:32:05 UTC. Your login code is 938201.",
                "938201"
            ),
            (
                "Alert generated at 20261022. Use authentication code: 582910.",
                "582910"
            ),
            (
                "Copyright 2026 ADI Communications. Your verification code is 847291.",
                "847291"
            ),
            (
                "Date: 22/10/2026 15:45. Code: 492815.",
                "492815"
            )
        ]

        for text, expected in test_cases:
            with self.subTest(text=text, expected=expected):
                result = verifier.extract_otp_from_text(text)
                self.assertEqual(result, expected, f"Failed extracting OTP from timestamp context: '{text}'")

    def test_d2_03_otp_extraction_tracking_and_order_id_resilience(self):
        """OTP extraction must ignore 10+ digit tracking IDs, order numbers, and invoice numbers."""
        verifier = AutoEmailVerifier()

        test_cases = [
            (
                "Order #9876543210 confirmed. Shipment TRACK-1029384756. Your confirmation PIN is 8372.",
                "8372"
            ),
            (
                "Invoice ID: INV-20261022-99881122. Verification code: 492810.",
                "492810"
            ),
            (
                "Reference #8472910482910. Your OTP is: 58291.",
                "58291"
            )
        ]

        for text, expected in test_cases:
            with self.subTest(text=text, expected=expected):
                result = verifier.extract_otp_from_text(text)
                self.assertEqual(result, expected, f"Failed extracting OTP from tracking/order context: '{text}'")

    def test_d2_04_otp_extraction_multi_numeric_soup(self):
        """OTP extraction must accurately isolate OTP in complex multi-numeric body text."""
        verifier = AutoEmailVerifier()

        body = (
            "Hello Gary Pearce (07860 244 274). Order #9876543210 placed on 2026-10-22 14:30:00. "
            "Tracking ID: GB1029384756. Total: £129.00. "
            "Please enter verification code: 628491 to confirm your account."
        )
        result = verifier.extract_otp_from_text(body)
        self.assertEqual(result, "628491", f"Failed multi-numeric soup extraction: got '{result}'")

    def test_d2_05_otp_extraction_spaced_and_reverse_patterns(self):
        """OTP extraction must handle spaced digits ('492 815') and reverse phrases ('849201 is your code')."""
        verifier = AutoEmailVerifier()

        test_cases = [
            ("Your verification code is: 492 815", "492815"),
            ("Please enter code 123 456 to verify", "123456"),
            ("849201 is your Google verification code", "849201"),
            ("392810 is your security pin", "392810"),
            ("001 234 is your confirmation code", "001234"),
            ("Your GitHub verification code is V7042-492847", "V7042-492847"),
            ("Your confirmation PIN is 0370019", "0370019")
        ]

        for text, expected in test_cases:
            with self.subTest(text=text, expected=expected):
                result = verifier.extract_otp_from_text(text)
                self.assertEqual(result, expected, f"Failed pattern extraction on: '{text}'")

    def test_d2_06_otp_extraction_negative_disqualification(self):
        """OTP extraction must return None when no genuine OTP is present."""
        verifier = AutoEmailVerifier()

        negative_cases = [
            "Please call Gary Pearce on 07860 244 274 for emergency CCTV assistance.",
            "Copyright 2026 ADI Communications Ltd. All rights reserved.",
            "Special promotion: use promo code SAVE20 for a discount.",
            "HTTP error code 500 received from remote server.",
            "Postal code LS1 1AA, West Yorkshire.",
            "Service price is £129 + VAT. Direct mobile 07860 244 274."
        ]

        for text in negative_cases:
            with self.subTest(text=text):
                result = verifier.extract_otp_from_text(text)
                self.assertIsNone(result, f"False positive OTP extracted from non-OTP text: '{text}' -> '{result}'")

    def test_d2_07_cdp_connection_refused_graceful_handling(self):
        """
        CDP methods must gracefully return empty structures without unhandled exceptions
        when target port is unreachable (connection refused).
        """
        # Port 59999 is guaranteed closed on localhost
        dead_endpoint = "http://127.0.0.1:59999"
        verifier = AutoEmailVerifier(cdp_base=dead_endpoint)

        # 1. _get_tabs() must return []
        tabs = verifier._get_tabs()
        self.assertIsInstance(tabs, list)
        self.assertEqual(tabs, [])

        # 2. Async methods must return None / [] cleanly
        async def run_async_probes():
            tab, created = await verifier.get_or_create_gmail_tab()
            self.assertIsNone(tab)
            self.assertFalse(created)

            emails = await verifier.get_recent_emails(max_count=5)
            self.assertEqual(emails, [])

            link = await verifier.find_verification_link("github.com", timeout_secs=1)
            self.assertIsNone(link)

            otp = await verifier.find_otp_code("github", timeout_secs=1)
            self.assertIsNone(otp)

        asyncio.run(run_async_probes())

    def test_d2_08_cdp_unroutable_timeout_socket_handling(self):
        """
        CDP endpoint pointing to non-routable test IP (RFC 5737 192.0.2.1)
        must cleanly time out without raising an uncaught exception.
        """
        blackhole_endpoint = "http://192.0.2.1:9223"
        verifier = AutoEmailVerifier(cdp_base=blackhole_endpoint)

        t0 = time.time()
        tabs = verifier._get_tabs()
        elapsed = time.time() - t0

        self.assertIsInstance(tabs, list)
        self.assertEqual(tabs, [])
        # Urlopen timeout in _get_tabs is 3 seconds
        self.assertLess(elapsed, 5.0, f"CDP timeout took too long: {elapsed:.2f}s")

    def test_d2_09_cdp_malformed_json_response_handling(self):
        """
        CDP endpoint returning non-JSON or corrupted payloads must be handled cleanly.
        """
        class MalformedJsonHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                # Return corrupted JSON syntax
                self.wfile.write(b'{"id": 1, "result": [unclosed array')

            def log_message(self, format, *args):
                pass

        server = http.server.HTTPServer(("127.0.0.1", 0), MalformedJsonHandler)
        port = server.server_port
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            verifier = AutoEmailVerifier(cdp_base=f"http://127.0.0.1:{port}")
            tabs = verifier._get_tabs()
            self.assertEqual(tabs, [], "Malformed JSON must safely result in an empty tabs list")
        finally:
            server.shutdown()
            server.server_close()


class TestDomain5OrchestratorRobustnessAndReachability(unittest.TestCase):
    """Domain 5: White-box testing of swarm_stack_orchestrator.py CLI subcommands and reachability."""

    def test_d5_01_subcommand_invalid_arguments_exit_code_2(self):
        """
        Argparse in swarm_stack_orchestrator.py must reject malformed subcommands,
        unknown flags, and invalid stack choices with exit code 2.
        """
        orchestrator_script = str(REPO_ROOT / "swarm_stack_orchestrator.py")

        malformed_invocations = [
            ([sys.executable, orchestrator_script, "invalid_subcommand"], "invalid positional subcommand"),
            ([sys.executable, orchestrator_script, "--stack", "invalid_stack_choice"], "invalid --stack choice"),
            ([sys.executable, orchestrator_script, "--nonexistent-option"], "unknown CLI option"),
            ([sys.executable, orchestrator_script, "audit", "--unknown-flag"], "unknown flag on valid subcommand")
        ]

        for cmd, desc in malformed_invocations:
            with self.subTest(desc=desc, cmd=cmd):
                res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
                self.assertEqual(
                    res.returncode, 2,
                    f"Expected exit code 2 on {desc}, got {res.returncode}. Stderr: {res.stderr}"
                )
                self.assertIn("error:", res.stderr.lower())

    def test_d5_02_subcommand_valid_help_and_dry_run_routes(self):
        """
        Valid subcommands must be accepted by the parser and display help cleanly.
        """
        orchestrator_script = str(REPO_ROOT / "swarm_stack_orchestrator.py")
        res = subprocess.run(
            [sys.executable, orchestrator_script, "--help"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT)
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("{status,sync,audit,deploy,verify,run}", res.stdout)

        # Test status dry run
        res_status = subprocess.run(
            [sys.executable, orchestrator_script, "status"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT)
        )
        self.assertEqual(res_status.returncode, 0)
        self.assertIn("STATUS PASS", res_status.stdout)

    def test_d5_03_check_url_reachability_timeout_exhaustion(self):
        """
        check_url_reachability() must handle slow/hanging endpoints past timeout
        and return (False, None, timeout_msg, elapsed) without unhandled exception.
        """
        class SlowHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                # Sleep longer than the 0.3s timeout
                time.sleep(1.0)
                self.send_response(200)
                self.end_headers()

            def log_message(self, format, *args):
                pass

        server = http.server.HTTPServer(("127.0.0.1", 0), SlowHandler)
        port = server.server_port
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            url = f"http://127.0.0.1:{port}/slow"
            is_ok, status, msg, elapsed = check_url_reachability(url, timeout=0.3)

            self.assertFalse(is_ok)
            self.assertIsNone(status)
            self.assertIn("Timed Out", msg)
            self.assertGreaterEqual(elapsed, 0.25)
            self.assertLess(elapsed, 2.0)
        finally:
            server.shutdown()
            server.server_close()

    def test_d5_04_check_url_reachability_ssl_failure(self):
        """
        check_url_reachability() must cleanly catch ssl.SSLError and return
        (False, None, ssl_msg, elapsed) without raising an uncaught exception.
        """
        # Spin up a plain HTTP server on localhost, then probe it with https:// scheme
        class PlainHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()

            def log_message(self, format, *args):
                pass

        server = http.server.HTTPServer(("127.0.0.1", 0), PlainHandler)
        port = server.server_port
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            # Probing plain HTTP port with HTTPS triggers an SSL handshake error
            https_url = f"https://127.0.0.1:{port}/"
            is_ok, status, msg, elapsed = check_url_reachability(https_url, timeout=2.0)

            self.assertFalse(is_ok)
            self.assertIsNone(status)
            self.assertTrue(
                "SSL" in msg or "URLError" in msg,
                f"Expected SSL/URLError in message, got: '{msg}'"
            )
        finally:
            server.shutdown()
            server.server_close()

    def test_d5_05_check_url_reachability_connection_refused(self):
        """
        check_url_reachability() must return (False, None, msg, elapsed) on closed ports.
        """
        url = "http://127.0.0.1:59998"
        is_ok, status, msg, elapsed = check_url_reachability(url, timeout=1.0)
        self.assertFalse(is_ok)
        self.assertIsNone(status)
        self.assertTrue("URLError" in msg or "Connection" in msg)

    def test_d5_06_check_url_reachability_http_error_statuses(self):
        """
        check_url_reachability() must return (False, status_code, ...) on 4xx/5xx responses.
        """
        class StatusHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/404":
                    self.send_response(404, "Not Found")
                elif self.path == "/429":
                    self.send_response(429, "Too Many Requests")
                elif self.path == "/500":
                    self.send_response(500, "Internal Server Error")
                elif self.path == "/503":
                    self.send_response(503, "Service Unavailable")
                else:
                    self.send_response(200)
                self.end_headers()

            def log_message(self, format, *args):
                pass

        server = http.server.HTTPServer(("127.0.0.1", 0), StatusHandler)
        port = server.server_port
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            for code in [404, 429, 500, 503]:
                url = f"http://127.0.0.1:{port}/{code}"
                is_ok, status, msg, elapsed = check_url_reachability(url, timeout=2.0)
                self.assertFalse(is_ok, f"Expected False for HTTP {code}")
                self.assertEqual(status, code, f"Expected status {code}, got {status}")
                self.assertIn(str(code), msg)
        finally:
            server.shutdown()
            server.server_close()

    def test_d5_07_check_url_reachability_redirect_success(self):
        """
        check_url_reachability() must follow 301/302 redirects and return True on 200 destination.
        """
        class RedirectHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/redirect":
                    self.send_response(302)
                    self.send_header("Location", f"http://127.0.0.1:{self.server.server_port}/destination")
                    self.end_headers()
                else:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"OK Reachable")

            def log_message(self, format, *args):
                pass

        server = http.server.HTTPServer(("127.0.0.1", 0), RedirectHandler)
        port = server.server_port
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            url = f"http://127.0.0.1:{port}/redirect"
            is_ok, status, msg, elapsed = check_url_reachability(url, timeout=2.0)
            self.assertTrue(is_ok)
            self.assertEqual(status, 200)
            self.assertIn("Reachable", msg)
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
