"""
tests/test_challenger_m1vid_adversarial.py
Adversarial Fuzzing, Schema Injection & Edge-Case Stress Test Suite
Constructed by M1-VID Challenger 1 (critic, specialist).

Adversarially challenges:
1. 5-Layer Integrity Firewall Fuzzing (Synthetic domains, dashboard console subdomains,
   disguised root links, path traversals, encoded slashes, auth redirect loops).
2. Sovereign Video Hierarchy & Strict Tier 3 YouTube Isolation in ProfileBrandManager.
3. GoogleOAuthDriver & EmailOtpDriver resilience against network exceptions, malformed
   JSON payloads, WebSocket dropouts, timeouts, and unhandled exceptions.
4. FailureTaxonomyHandler edge cases, unrecognized error patterns, and canonical fallback guarantees.
5. Strict JSON Schema Draft 2020-12 adherence for master_multicategory_platform_catalog.json,
   including additionalProperties: false enforcement and adversarial property injection rejection.
6. Atomic Parity Sync & count recalculation integrity.
"""

import asyncio
import copy
import csv
import http.server
import json
import os
import posixpath
import re
import socket
import sys
import threading
import time
import unittest
import unittest.mock as mock
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import jsonschema
from jsonschema import Draft202012Validator
import websockets

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import automated_video_platform_onboarder as onboarder
from automated_video_platform_onboarder import (
    AutomatedVideoPlatformOnboarder,
    CatalogParitySync,
    EmailOtpDriver,
    FailureReason,
    FailureTaxonomyHandler,
    GoogleOAuthDriver,
    IntegrityFirewall,
    ProfileBrandManager,
    VideoPlatformCDPClient,
)


# =====================================================================
# Mock HTTP Server for Layer 4 Network & Auth Wall Testing
# =====================================================================
class MockAuthServer(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress console logging

    def do_GET(self):
        if self.path == "/status/200":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        elif self.path == "/status/404":
            self.send_response(404)
            self.end_headers()
        elif self.path == "/status/500":
            self.send_response(500)
            self.end_headers()
        elif self.path == "/redirect/google-auth":
            # Redirect to local mock simulating accounts.google.com
            self.send_response(302)
            self.send_header("Location", f"http://127.0.0.1:{self.server.server_port}/accounts.google.com/signin")
            self.end_headers()
        elif self.path == "/accounts.google.com/signin":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html>Google Signin</html>")
        elif self.path == "/redirect/github-auth":
            self.send_response(302)
            self.send_header("Location", f"http://127.0.0.1:{self.server.server_port}/github.com/login/oauth")
            self.end_headers()
        elif self.path == "/github.com/login/oauth":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html>GitHub OAuth</html>")
        elif self.path == "/redirect/auth0":
            self.send_response(302)
            self.send_header("Location", f"http://127.0.0.1:{self.server.server_port}/auth0.com/authorize")
            self.end_headers()
        elif self.path == "/auth0.com/authorize":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html>Auth0 Portal</html>")
        elif self.path == "/hang":
            time.sleep(2.5)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Delayed")
        else:
            self.send_response(400)
            self.end_headers()


# =====================================================================
# Test Class 1: 5-Layer Integrity Firewall Malicious URL Fuzzing
# =====================================================================
class TestIntegrityFirewallMaliciousUrlFuzzing(unittest.TestCase):
    """Adversarial stress-testing of all 5 layers of the Integrity Firewall."""

    @classmethod
    def setUpClass(cls):
        cls.server = http.server.HTTPServer(("127.0.0.1", 0), MockAuthServer)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_layer1_syntax_fuzzing(self):
        """Fuzz Layer 1 with whitespace, illegal schemes, non-strings, and dummy strings."""
        illegal_cases = [
            ("https://youtube.com /test", "embedded whitespace"),
            ("https://youtube.com\n/test", "newline injection"),
            ("https://youtube.com\r/test", "carriage return injection"),
            ("https://youtube.com/(test)", "parenthesis injection"),
            ("ftp://youtube.com/path", "unsupported ftp scheme"),
            ("file:///etc/passwd", "file URI scheme"),
            ("javascript:alert(1)", "javascript scheme"),
            ("data:text/html;base64,PHNjcmlwdD4=", "data URI scheme"),
            ("https://", "empty netloc"),
            ("https://example.com/channel", "dummy example.com domain"),
            ("https://vimeo.com/test.com", "dummy test.com substring"),
            ("https://vimeo.com/d1abcdefg", "dummy d1abcdefg hash"),
            ("https://vimeo.com/placeholder", "dummy placeholder substring"),
            ("https://vimeo.com/your-name", "dummy your-name substring"),
            ("https://vimeo.com/username", "dummy username substring"),
            ("", "empty string"),
            (None, "NoneType input"),
            (12345, "integer input"),
            (["https://youtube.com"], "list input"),
            ({"url": "https://youtube.com"}, "dict input"),
        ]

        for url, desc in illegal_cases:
            with self.subTest(case=desc, url=url):
                ok, msg = IntegrityFirewall.validate_layer1_syntax(url)
                self.assertFalse(ok, f"Layer 1 syntax should REJECT {desc}: {url}. Result: {msg}")

        # Legitimate URLs MUST pass
        valid_cases = [
            "https://www.youtube.com/@CCTV.services",
            "https://vimeo.com/adicommunications",
            "https://dailymotion.com/cctv-security",
            "https://archive.org/details/@gary_pearce",
            "https://rumble.com/c/cctvservices",
        ]
        for url in valid_cases:
            with self.subTest(case="Valid URL", url=url):
                ok, msg = IntegrityFirewall.validate_layer1_syntax(url)
                self.assertTrue(ok, f"Layer 1 syntax should PASS valid URL {url}. Result: {msg}")

    def test_defect_layer1_tab_character_bypass(self):
        """HARDENED: Verify that Layer 1 strictly rejects embedded tab characters."""
        tab_url = "https://youtube.com\t/test"
        ok, msg = IntegrityFirewall.validate_layer1_syntax(tab_url)
        self.assertFalse(ok, f"Layer 1 syntax must reject embedded tab character: '{tab_url}'")

    def test_layer2_synthetic_domains_fuzzing(self):
        """Fuzz Layer 2 against synthetic domains, ports, dots, subdomains, and userinfo."""
        synthetic_cases = [
            ("https://adi-telecoms.org", "exact synthetic domain"),
            ("https://adi-telecoms.org/", "exact synthetic domain with slash"),
            ("https://dailymotion.adi-telecoms.org", "synthetic subdomain"),
            ("https://sub.dailymotion.adi-telecoms.org", "deep synthetic subdomain"),
            ("https://adi-telecoms.org:8443/profile", "synthetic domain with port"),
            ("https://dailymotion.adi-telecoms.org:443/feed", "synthetic subdomain with port"),
            ("https://adi-telecoms.org.", "synthetic domain with trailing FQDN dot"),
            ("https://adi-telecoms.org./path", "synthetic domain with trailing dot and path"),
            ("https://dailymotion.adi-telecoms.org./", "synthetic subdomain with trailing dot"),
            ("https://user:pass@adi-telecoms.org/profile", "synthetic domain with userinfo"),
            ("https://admin@sub.adi-telecoms.org/account", "synthetic subdomain with userinfo"),
        ]

        for url, desc in synthetic_cases:
            with self.subTest(case=desc, url=url):
                ok, msg = IntegrityFirewall.validate_layer2_domain(url)
                self.assertFalse(ok, f"Layer 2 domain should REJECT synthetic domain: {desc} ({url}). Result: {msg}")

        # Authentic domains MUST pass
        legit_cases = [
            "https://youtube.com/@CCTV.services",
            "https://vimeo.com/user123",
            "https://dailymotion.com/channel",
            "https://rumble.com/c/channel",
            "https://peertube.tv/accounts/user",
        ]
        for url in legit_cases:
            with self.subTest(case="Legit domain", url=url):
                ok, msg = IntegrityFirewall.validate_layer2_domain(url)
                self.assertTrue(ok, f"Layer 2 domain should PASS legitimate domain: {url}. Result: {msg}")

    def test_layer3_anti_dashboard_console_fuzzing(self):
        """Fuzz Layer 3 with management subdomains, private session paths, and path traversal tricks."""
        dashboard_cases = [
            # Subdomains
            ("https://app.vimeo.com/manage", "app. subdomain"),
            ("https://dashboard.dailymotion.com/videos", "dashboard. subdomain"),
            ("https://console.rumble.com/analytics", "console. subdomain"),
            ("https://admin.bitchute.com/control", "admin. subdomain"),
            ("https://portal.odysee.com/overview", "portal. subdomain"),
            ("https://account.youtube.com/settings", "account. subdomain"),
            ("https://accounts.google.com/ServiceLogin", "accounts. subdomain"),
            ("https://workspace.google.com/dashboard", "workspace. subdomain"),
            ("https://prod.app.vimeo.com/studio", "sub-subdomain app."),
            ("https://eu.console.aws.amazon.com/home", "sub-subdomain console."),
            # Private paths
            ("https://vimeo.com/app", "exact /app path"),
            ("https://vimeo.com/app/", "exact /app/ path"),
            ("https://vimeo.com/dashboard", "exact /dashboard path"),
            ("https://vimeo.com/dashboard/videos", "nested /dashboard/ path"),
            ("https://vimeo.com/console", "/console path"),
            ("https://vimeo.com/admin", "/admin path"),
            ("https://vimeo.com/admin/settings", "/admin/settings path"),
            ("https://vimeo.com/settings", "/settings path"),
            ("https://vimeo.com/account", "/account path"),
            ("https://vimeo.com/signin", "/signin path"),
            ("https://vimeo.com/sign-in", "/sign-in path"),
            ("https://vimeo.com/login", "/login path"),
            ("https://vimeo.com/portal", "/portal path"),
            ("https://vimeo.com/workspace", "/workspace path"),
            ("https://vimeo.com/onboarding", "/onboarding path"),
            ("https://vimeo.com/welcome", "/welcome path"),
            ("https://vimeo.com/~", "private home path /~"),
            ("https://vimeo.com/~/", "private home path /~/"),
            ("https://vimeo.com/user/~", "trailing /~"),
            # Known fragments
            ("https://app.netlify.com/teams/user", "known netlify app fragment"),
            ("https://dashboard.render.com/web/srv-123", "known render dashboard fragment"),
            ("https://fly.io/app/my-app", "known fly.io app fragment"),
            # Traversal attempts
            ("https://vimeo.com/public/../dashboard", "traversal into /dashboard"),
            ("https://vimeo.com/public/../admin", "traversal into /admin"),
            ("https://vimeo.com/public?redirect=/dashboard", "redirect parameter with /dashboard"),
        ]

        for url, desc in dashboard_cases:
            with self.subTest(case=desc, url=url):
                ok, msg = IntegrityFirewall.validate_layer3_anti_dashboard(url)
                self.assertFalse(ok, f"Layer 3 should REJECT private dashboard: {desc} ({url}). Result: {msg}")

        # Public tenant profiles MUST pass
        public_cases = [
            "https://www.youtube.com/@CCTV.services",
            "https://vimeo.com/cctvservices",
            "https://dailymotion.com/cctvservices",
            "https://rumble.com/c/cctvservices",
            "https://odysee.com/@cctvservices",
            "https://bitchute.com/channel/cctvservices/",
            "https://peertube.tv/c/cctvservices",
        ]
        for url in public_cases:
            with self.subTest(case="Public tenant URL", url=url):
                ok, msg = IntegrityFirewall.validate_layer3_anti_dashboard(url)
                self.assertTrue(ok, f"Layer 3 should PASS public tenant profile: {url}. Result: {msg}")

    def test_layer4_live_http_probing_and_auth_walls(self):
        """Stress-test Layer 4 with mock HTTP server: 200, 404, 500, auth wall redirects, and timeouts."""
        # 200 OK -> Pass
        ok, status, msg = IntegrityFirewall.validate_layer4_live_http_200(f"{self.base_url}/status/200", timeout=3.0)
        self.assertTrue(ok, f"HTTP 200 should pass: status={status}, msg={msg}")
        self.assertEqual(status, 200)

        # 404 Not Found -> Fail
        ok, status, msg = IntegrityFirewall.validate_layer4_live_http_200(f"{self.base_url}/status/404", timeout=3.0)
        self.assertFalse(ok, f"HTTP 404 should fail: status={status}, msg={msg}")
        self.assertEqual(status, 404)

        # 500 Internal Error -> Fail
        ok, status, msg = IntegrityFirewall.validate_layer4_live_http_200(f"{self.base_url}/status/500", timeout=3.0)
        self.assertFalse(ok, f"HTTP 500 should fail: status={status}, msg={msg}")
        self.assertEqual(status, 500)

        # Google login auth wall redirect -> Fail
        ok, status, msg = IntegrityFirewall.validate_layer4_live_http_200(f"{self.base_url}/redirect/google-auth", timeout=3.0)
        self.assertFalse(ok, f"Google auth redirect should fail: status={status}, msg={msg}")
        self.assertIn("accounts.google.com", msg.lower())

        # GitHub login auth wall redirect -> Fail
        ok, status, msg = IntegrityFirewall.validate_layer4_live_http_200(f"{self.base_url}/redirect/github-auth", timeout=3.0)
        self.assertFalse(ok, f"GitHub auth redirect should fail: status={status}, msg={msg}")
        self.assertIn("github.com/login", msg.lower())

        # Auth0 login auth wall redirect -> Fail
        ok, status, msg = IntegrityFirewall.validate_layer4_live_http_200(f"{self.base_url}/redirect/auth0", timeout=3.0)
        self.assertFalse(ok, f"Auth0 auth redirect should fail: status={status}, msg={msg}")
        self.assertIn("auth0.com", msg.lower())

        # Socket timeout / hang -> Fail
        ok, status, msg = IntegrityFirewall.validate_layer4_live_http_200(f"{self.base_url}/hang", timeout=0.5)
        self.assertFalse(ok, f"Timeout should fail: status={status}, msg={msg}")

    def test_layer5_rule_45_adversarial_battery(self):
        """Stress-test Layer 5 Rule 45 against naked roots, ports, dots, index evasion, and path traversals."""
        naked_root_violations = [
            ("https://adicommunications.co.uk", "naked root no slash"),
            ("https://adicommunications.co.uk/", "naked root with slash"),
            ("http://adicommunications.co.uk", "http naked root no slash"),
            ("http://adicommunications.co.uk/", "http naked root with slash"),
            ("https://www.adicommunications.co.uk", "www naked root no slash"),
            ("https://www.adicommunications.co.uk/", "www naked root with slash"),
            ("https://ADICOMMUNICATIONS.CO.UK/", "uppercase naked root"),
            ("https://Www.AdiCommunications.Co.Uk/", "mixed-case www naked root"),
            # Port variations
            ("https://adicommunications.co.uk:443", "port 443 no slash"),
            ("https://adicommunications.co.uk:443/", "port 443 with slash"),
            ("http://adicommunications.co.uk:80", "http port 80 no slash"),
            ("http://adicommunications.co.uk:80/", "http port 80 with slash"),
            ("https://adicommunications.co.uk:8080/", "custom port 8080"),
            ("https://adicommunications.co.uk:8443/", "custom port 8443"),
            # Trailing dots
            ("https://adicommunications.co.uk.", "trailing FQDN dot no slash"),
            ("https://adicommunications.co.uk./", "trailing FQDN dot with slash"),
            ("https://adicommunications.co.uk.:443/", "trailing dot + port 443"),
            ("https://www.adicommunications.co.uk.", "www trailing dot no slash"),
            ("https://www.adicommunications.co.uk./", "www trailing dot with slash"),
            # Default index files
            ("https://adicommunications.co.uk/index.html", "index.html"),
            ("https://adicommunications.co.uk/index.htm", "index.htm"),
            ("https://adicommunications.co.uk/index.php", "index.php"),
            ("https://adicommunications.co.uk:443/index.html", "port 443 + index.html"),
            ("https://adicommunications.co.uk./index.html", "dot + index.html"),
            # Query params & fragments on root
            ("https://adicommunications.co.uk/?utm_source=test", "root with query parameter"),
            ("https://adicommunications.co.uk?ref=twitter", "root no slash with query parameter"),
            ("https://adicommunications.co.uk/#overview", "root with fragment anchor"),
            ("https://adicommunications.co.uk#services", "root no slash with fragment anchor"),
            ("https://adicommunications.co.uk/?", "root with empty query marker"),
            ("https://adicommunications.co.uk/#", "root with empty fragment marker"),
            # Path traversals with slash
            ("https://adicommunications.co.uk/services/../", "traversal /services/../ resolving to root"),
            ("https://adicommunications.co.uk/./", "relative dot /./ resolving to root"),
            ("https://adicommunications.co.uk/news/../index.html", "traversal to index.html"),
            ("https://adicommunications.co.uk/foo/bar/../../", "nested traversal resolving to root"),
            ("https://adicommunications.co.uk//", "double slash root"),
            ("https://adicommunications.co.uk///", "triple slash root"),
            # Embedded text
            ('<a href="https://adicommunications.co.uk/">ADI Home</a>', "HTML double-quoted anchor"),
            ("<a href='https://adicommunications.co.uk'>ADI</a>", "HTML single-quoted anchor"),
            ('[Gary Pearce](https://adicommunications.co.uk/)', "Markdown link format"),
            ('{"website": "https://adicommunications.co.uk/"}', "JSON string value"),
            ('Check out https://adicommunications.co.uk.', "Sentence ending with FQDN period"),
        ]

        for url_or_text, desc in naked_root_violations:
            with self.subTest(case=desc, snippet=url_or_text):
                ok, msg = IntegrityFirewall.validate_layer5_rule_45(url_or_text)
                self.assertFalse(ok, f"Layer 5 Rule 45 should REJECT {desc}: {url_or_text}. Result: {msg}")

        # Legitimate Rule 45 buffer pages MUST pass
        allowed_buffers = [
            ("https://adicommunications.co.uk/news/cctv-field-guide", "editorial news buffer"),
            ("https://adicommunications.co.uk/news/starlink-installation-guide", "editorial news buffer 2"),
            ("https://adicommunications.co.uk/assets/images/sample.webp", "assets image buffer"),
            ("https://adicommunications.co.uk/feed.xml", "RSS feed buffer"),
            ("https://tvandhomesecurity.blogspot.com/", "Blogger Citadel Apex"),
            ("https://www.youtube.com/@CCTV.services", "YouTube Apex"),
            ("https://gary-pearce-forensic-hub.web.app/", "Firebase Citadel Ledger"),
        ]
        for url, desc in allowed_buffers:
            with self.subTest(case=desc, url=url):
                ok, msg = IntegrityFirewall.validate_layer5_rule_45(url)
                self.assertTrue(ok, f"Layer 5 Rule 45 should PASS legitimate buffer {desc}: {url}. Result: {msg}")

    def test_defect_layer5_path_traversal_evasion(self):
        """HARDENED: Verify that /news/.. path traversal is strictly rejected under Rule 45."""
        traversal_urls = [
            "https://adicommunications.co.uk/news/..",
            "https://adicommunications.co.uk/news/..?",
            "https://adicommunications.co.uk/news/..;",
            "https://adicommunications.co.uk/news/..,",
            "https://adicommunications.co.uk/news/..!",
        ]
        for url in traversal_urls:
            with self.subTest(url=url):
                ok, msg = IntegrityFirewall.validate_layer5_rule_45(url)
                self.assertFalse(ok, f"Layer 5 Rule 45 must reject path traversal '{url}'. Result: {msg}")


# =====================================================================
# Test Class 2: Sovereign Air-Gap & ProfileBrandManager Adversarial Tests
# =====================================================================
class TestSovereignAirGapAndBrandManager(unittest.TestCase):
    """Adversarial testing of ProfileBrandManager, Sovereign Tier hierarchy, and Rule 45 air-gap."""

    def setUp(self):
        self.bm = ProfileBrandManager()

    def test_strict_tier3_isolation_rejects_any_adicommunications_reference(self):
        """Tier 3 platforms must strictly REJECT any adicommunications.co.uk link (including buffer pages)."""
        tier3_leak_cases = [
            ("https://adicommunications.co.uk/news/cctv-guide", "buffer news guide"),
            ("https://adicommunications.co.uk/services/cctv", "services subpage"),
            ("https://adicommunications.co.uk/", "naked root"),
            ("https://www.adicommunications.co.uk/assets/test.webp", "assets buffer"),
        ]
        for url, desc in tier3_leak_cases:
            with self.subTest(case=desc, url=url):
                ok, msg = self.bm.audit_profile_url(url, "Rumble", "Tier 3", probe_live=False)
                self.assertFalse(ok, f"Tier 3 must REJECT direct adicommunications.co.uk link ({desc}): {url}")
                # Message must either be Tier 3 violation or Layer 5 failure
                self.assertTrue(
                    "Tier 3 Rule 45 Violation" in msg or "Integrity Firewall Layer 5 failed" in msg,
                    f"Unexpected rejection message: {msg}"
                )

    def test_tier3_permits_youtube_apex_target(self):
        """Tier 3 platforms must pass when pointing to the sovereign YouTube Apex."""
        ok, msg = self.bm.audit_profile_url("https://www.youtube.com/@CCTV.services", "Rumble", "Tier 3", probe_live=False)
        self.assertTrue(ok, f"Tier 3 pointing to YouTube Apex must PASS: {msg}")

    def test_tier_upward_target_url_mapping(self):
        """Assert sovereign hierarchy upward target mapping for Tier 1, 2, and 3."""
        # Tier 1 Apex points to Blogger Citadel Hub
        self.assertEqual(self.bm.get_profile_upward_url("Tier 1 Apex"), "https://tvandhomesecurity.blogspot.com/")
        # Tier 2 points to YouTube Apex
        self.assertEqual(self.bm.get_profile_upward_url("Tier 2 High-DA"), "https://www.youtube.com/@CCTV.services")
        # Tier 3 points EXCLUSIVELY to YouTube Apex
        self.assertEqual(self.bm.get_profile_upward_url("Tier 3 Decentralized"), "https://www.youtube.com/@CCTV.services")

    def test_format_bio_trade_eeat_standards_and_length_firewall(self):
        """Test Gary Pearce bio formatting, length capping, and mandatory credentials."""
        bio = self.bm.format_bio(max_length=250)
        self.assertLessEqual(len(bio), 250)
        self.assertIn("Gary Pearce", bio)
        self.assertIn("ADI Communications", bio)
        self.assertIn("07860 244 274", bio)
        self.assertIn("25+ yrs", bio)
        self.assertIn("£10M Public Liability", bio)
        self.assertNotIn("0800", bio)
        self.assertNotIn("checkatrade", bio.lower())

        # Test truncation with small max_length
        short_bio = self.bm.format_bio(max_length=50)
        self.assertLessEqual(len(short_bio), 50)
        self.assertTrue(short_bio.endswith("..."))


# =====================================================================
# Test Class 3: Auth Drivers (OAuth & OTP) Edge Cases & Resilience
# =====================================================================
class TestAuthDriversResilienceAndEdgeCases(unittest.TestCase):
    """Stress-test VideoPlatformCDPClient, GoogleOAuthDriver, and EmailOtpDriver."""

    def setUp(self):
        self.cdp = VideoPlatformCDPClient("http://127.0.0.1:9223")
        self.oauth = GoogleOAuthDriver(self.cdp)
        self.email_driver = EmailOtpDriver(self.cdp)

    def test_cdp_send_cdp_handles_connection_closed(self):
        """Test send_cdp when WebSocket is closed or raises ConnectionResetError."""
        mock_ws = mock.AsyncMock()
        mock_ws.send.side_effect = ConnectionResetError("Connection lost")

        res = asyncio.run(self.cdp.send_cdp(mock_ws, "Runtime.evaluate", {"expression": "1+1"}))
        self.assertEqual(res, {}, "send_cdp should return empty dict when send fails")

    def test_cdp_send_cdp_handles_malformed_json_frames(self):
        """Test send_cdp when WebSocket receives invalid JSON followed by timeout."""
        mock_ws = mock.AsyncMock()
        mock_ws.send.return_value = None
        # First recv returns corrupted JSON, second raises TimeoutError
        mock_ws.recv.side_effect = ["CORRUPTED_JSON_NOT_A_DICT{", asyncio.TimeoutError()]

        res = asyncio.run(self.cdp.send_cdp(mock_ws, "Runtime.evaluate", {"expression": "true"}, timeout=0.1))
        self.assertEqual(res, {}, "send_cdp should handle malformed JSON frame gracefully")

    def test_cdp_send_cdp_handles_non_dict_json_payloads(self):
        """Test send_cdp when WebSocket receives JSON array or scalar instead of dict."""
        mock_ws = mock.AsyncMock()
        mock_ws.send.return_value = None
        mock_ws.recv.side_effect = ["[1, 2, 3]", "true", "42", asyncio.TimeoutError()]

        res = asyncio.run(self.cdp.send_cdp(mock_ws, "Runtime.evaluate", {"expression": "true"}, timeout=0.1))
        self.assertEqual(res, {}, "send_cdp should handle non-dict JSON payloads without crashing")

    def test_cdp_list_tabs_suppresses_network_errors(self):
        """Test list_tabs suppresses URLError / connection refused gracefully."""
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Connection refused")):
            tabs = self.cdp.list_tabs()
            self.assertEqual(tabs, [])

    def test_cdp_list_tabs_suppresses_malformed_json(self):
        """Test list_tabs handles non-JSON / HTML error pages from CDP."""
        mock_resp = mock.MagicMock()
        mock_resp.read.return_value = b"<html>502 Bad Gateway</html>"
        with mock.patch("urllib.request.urlopen", return_value=mock_resp):
            tabs = self.cdp.list_tabs()
            self.assertEqual(tabs, [])

    def test_defect_google_oauth_crashes_on_malformed_tab_entries(self):
        """HARDENED: execute_google_oauth safely ignores non-dict tabs without crashing."""
        mock_ws = mock.AsyncMock()
        with mock.patch.object(self.cdp, "eval_js", return_value=True):
            # cdp.list_tabs returns a list with None or non-dict entry
            with mock.patch.object(self.cdp, "list_tabs", return_value=[None, "invalid_tab_string"]):
                try:
                    asyncio.run(self.oauth.execute_google_oauth(mock_ws, "vimeo.com", timeout=0.1))
                    crashed = False
                except AttributeError as e:
                    crashed = True
                self.assertFalse(crashed, "Verifies that GoogleOAuthDriver safely ignores non-dict tab elements without crashing")

    def test_google_oauth_button_actuation_failure(self):
        """Test execute_google_oauth when Google SSO button cannot be found or clicked."""
        mock_ws = mock.AsyncMock()
        with mock.patch.object(self.cdp, "eval_js", return_value=False):
            ok, detail = asyncio.run(self.oauth.execute_google_oauth(mock_ws, "vimeo.com", timeout=0.5))
            self.assertFalse(ok)
            self.assertIn("could not be actuated", detail)

    def test_google_oauth_flow_timeout_when_not_redirected(self):
        """Test execute_google_oauth times out cleanly when login does not complete."""
        mock_ws = mock.AsyncMock()

        async def mock_eval(ws, js, **kwargs):
            if "googleBtn" in js:
                return True
            if "hasDashboard" in js:
                return {"isTarget": False, "hasAvatar": False, "hasDashboard": False}
            return None

        with mock.patch.object(self.cdp, "eval_js", side_effect=mock_eval):
            with mock.patch.object(self.cdp, "list_tabs", return_value=[]):
                ok, detail = asyncio.run(self.oauth.execute_google_oauth(mock_ws, "vimeo.com", timeout=0.1))
                self.assertFalse(ok)
                self.assertIn("timed out", detail)

    def test_defect_email_driver_javascript_injection_single_quote(self):
        """HARDENED: autofill_signup_form escapes quotes using json.dumps to preserve JavaScript syntax."""
        mock_ws = mock.AsyncMock()
        captured_js = []

        async def mock_eval(ws, js, **kwargs):
            captured_js.append(js)
            return 1

        with mock.patch.object(self.cdp, "eval_js", side_effect=mock_eval):
            asyncio.run(self.email_driver.autofill_signup_form(mock_ws, username="O'Connor", password="Pass'word123"))

        self.assertGreater(len(captured_js), 0)
        js = captured_js[0]
        has_unescaped_quote = "userInput.value = 'O'Connor';" in js
        self.assertFalse(has_unescaped_quote, "Verifies that EmailOtpDriver does not generate unescaped single quotes")
        self.assertIn('userInput.value = "O\'Connor";', js, "Verifies json.dumps() escaped string literal in autofill JS")

    def test_email_driver_handle_verification_otp_timeout(self):
        """Test handle_verification when OTP input exists but OTP code never arrives."""
        mock_ws = mock.AsyncMock()

        async def mock_eval(ws, js, **kwargs):
            if "otpInputs" in js:
                return True
            return None

        mock_auto_email = mock.MagicMock()
        mock_auto_email.find_otp_code = mock.AsyncMock(return_value=None)

        with mock.patch.dict("sys.modules", {"auto_email_verifier": mock_auto_email}):
            with mock.patch.object(self.cdp, "eval_js", side_effect=mock_eval):
                ok, msg = asyncio.run(self.email_driver.handle_verification(mock_ws, "Vimeo", "vimeo.com", timeout=0.1))
                self.assertFalse(ok)
                self.assertIn("failed to arrive in inbox", msg)

    def test_email_driver_handle_verification_magic_link_timeout(self):
        """Test handle_verification when no OTP prompt and magic link fails to arrive."""
        mock_ws = mock.AsyncMock()

        async def mock_eval(ws, js, **kwargs):
            if "otpInputs" in js:
                return False
            return None

        mock_auto_email = mock.MagicMock()
        mock_auto_email.find_verification_link = mock.AsyncMock(return_value=None)

        with mock.patch.dict("sys.modules", {"auto_email_verifier": mock_auto_email}):
            with mock.patch.object(self.cdp, "eval_js", side_effect=mock_eval):
                ok, msg = asyncio.run(self.email_driver.handle_verification(mock_ws, "Vimeo", "vimeo.com", timeout=0.1))
                self.assertFalse(ok)
                self.assertIn("No OTP code or verification link detected", msg)


# =====================================================================
# Test Class 4: FailureTaxonomyHandler Edge Cases
# =====================================================================
class TestFailureTaxonomyHandlerEdgeCases(unittest.TestCase):
    """Stress-test FailureTaxonomyHandler across all 11 canonical codes and unrecognized patterns."""

    def test_canonical_codes_mapping(self):
        """Verify accurate mapping for all standard signals."""
        cases = [
            # PLATFORM_DEAD
            ("Endpoint error", 404, "Not Found", FailureReason.PLATFORM_DEAD),
            ("Server crashed", 500, "Internal Server Error", FailureReason.PLATFORM_DEAD),
            ("Bad gateway", 502, "Bad Gateway", FailureReason.PLATFORM_DEAD),
            ("Service unavailable", 503, "Service Unavailable", FailureReason.PLATFORM_DEAD),
            ("DNS resolution failed", 200, "nxdomain error", FailureReason.PLATFORM_DEAD),
            ("Host down", 200, "site not found", FailureReason.PLATFORM_DEAD),
            # RATE_LIMITED
            ("Too many requests", 429, "", FailureReason.RATE_LIMITED),
            ("IP throttled", 200, "rate limit exceeded", FailureReason.RATE_LIMITED),
            # CAPTCHA_REQUIRED
            ("<html>cf-turnstile challenge</html>", 200, "", FailureReason.CAPTCHA_REQUIRED),
            ("<html>hcaptcha embedded here</html>", 200, "", FailureReason.CAPTCHA_REQUIRED),
            ("<html>g-recaptcha container</html>", 200, "", FailureReason.CAPTCHA_REQUIRED),
            ("Please verify you are human", 200, "", FailureReason.CAPTCHA_REQUIRED),
            # PHONE_SMS_REQUIRED
            ("Enter your phone number to receive an SMS", 200, "", FailureReason.PHONE_SMS_REQUIRED),
            ("SMS verification required", 200, "", FailureReason.PHONE_SMS_REQUIRED),
            ("Enter your mobile", 200, "", FailureReason.PHONE_SMS_REQUIRED),
            # MANUAL_BILLING_REQUIRED
            ("Enter credit card details to start trial", 200, "", FailureReason.MANUAL_BILLING_REQUIRED),
            ("Stripe billing address mandatory", 200, "", FailureReason.MANUAL_BILLING_REQUIRED),
            # GEO_RESTRICTED
            ("Service not available in your country", 200, "", FailureReason.GEO_RESTRICTED),
            ("Geographic restriction applies", 200, "", FailureReason.GEO_RESTRICTED),
            # WAITLIST_PENDING
            ("You have been added to our waiting list", 200, "", FailureReason.WAITLIST_PENDING),
            ("We will review your account", 200, "", FailureReason.WAITLIST_PENDING),
            # CLI_AUTH_REQUIRED
            ("CLI required: please install CLI tool", 200, "", FailureReason.CLI_AUTH_REQUIRED),
            ("Command line setup only", 200, "", FailureReason.CLI_AUTH_REQUIRED),
        ]

        for ps, sc, em, expected_reason in cases:
            with self.subTest(sc=sc, em=em, expected=expected_reason):
                reason, detail = FailureTaxonomyHandler.evaluate_failure(ps, sc, em)
                self.assertEqual(reason, expected_reason)
                self.assertTrue(FailureReason.is_valid(reason))
                self.assertTrue(bool(detail))

    def test_unrecognized_error_patterns_fallback_guarantee(self):
        """Verify unrecognized error patterns safely fallback to WAITLIST_PENDING and never crash."""
        unrecognized_cases = [
            ("", 200, ""),
            (None, 200, None),
            ("Arbitrary unhandled text string", 200, "Unrecognized error code 998"),
            ("Custom proprietary vendor message", 418, "I am a teapot"),
            ("Internal permission issue", 403, "Forbidden"),
            ("Session invalid", 401, "Unauthorized"),
        ]

        for ps, sc, em in unrecognized_cases:
            with self.subTest(ps=ps, sc=sc, em=em):
                reason, detail = FailureTaxonomyHandler.evaluate_failure(ps, sc, em)
                self.assertTrue(FailureReason.is_valid(reason), f"Reason must be canonical: {reason}")
                self.assertEqual(reason, FailureReason.WAITLIST_PENDING)
                self.assertIsInstance(detail, str)


# =====================================================================
# Test Class 5: Master Catalog Strict JSON Schema Draft 2020-12
# =====================================================================
class TestMasterCatalogDraft202012StrictSchema(unittest.TestCase):
    """Rigorous schema validation and adversarial property injection on master_multicategory_platform_catalog.json."""

    @classmethod
    def setUpClass(cls):
        cls.catalog_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        with open(cls.catalog_path, "r", encoding="utf-8") as f:
            cls.catalog = json.load(f)

        # Build formal Draft 2020-12 schema with additionalProperties: false
        cls.strict_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": [
                "$schema", "version", "title", "description", "lead_engineer",
                "insurance", "rule_45_shield", "total_platforms", "total_joined",
                "total_pending", "category_stacks", "platforms"
            ],
            "properties": {
                "$schema": {"type": "string", "const": "https://json-schema.org/draft/2020-12/schema"},
                "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
                "title": {"type": "string", "minLength": 10},
                "description": {"type": "string", "minLength": 20},
                "lead_engineer": {"type": "string", "pattern": r"07860 244 274"},
                "insurance": {"type": "string", "pattern": r"£10,000,000"},
                "rule_45_shield": {"type": "string", "const": "STRICT_AIR_GAP"},
                "total_platforms": {"type": "integer", "minimum": 550},
                "total_joined": {"type": "integer", "minimum": 0},
                "total_pending": {"type": "integer", "minimum": 0},
                "category_stacks": {"type": "object"},
                "platforms": {
                    "type": "array",
                    "minItems": 550,
                    "items": {
                        "type": "object",
                        "required": [
                            "platform_id", "global_rank", "stack_rank", "name", "domain",
                            "da", "stack_key", "category", "tier", "signup_url", "sso_method",
                            "status", "active_tenant_url", "failure_reason", "failure_detail",
                            "upward_target_url", "rule_45_compliant", "eeat_metadata"
                        ],
                        "properties": {
                            "platform_id": {"type": "string", "pattern": r"^PLAT-[A-Z]+-\d{3}$"},
                            "global_rank": {"type": "integer", "minimum": 1},
                            "stack_rank": {"type": "integer", "minimum": 1, "maximum": 50},
                            "name": {"type": "string", "minLength": 1},
                            "domain": {"type": "string", "minLength": 3},
                            "da": {"type": "integer", "minimum": 1, "maximum": 100},
                            "stack_key": {"type": "string"},
                            "category": {"type": "string"},
                            "tier": {"type": "string"},
                            "signup_url": {"type": "string", "format": "uri"},
                            "sso_method": {"type": "string"},
                            "status": {"type": "string", "enum": ["JOINED", "PENDING"]},
                            "active_tenant_url": {"type": "string"},
                            "failure_reason": {
                                "type": ["string", "null"],
                                "enum": list(FailureReason.ALL_REASONS.keys()) + [None]
                            },
                            "failure_detail": {"type": ["string", "null"]},
                            "upward_target_url": {"type": "string", "format": "uri"},
                            "rule_45_compliant": {"type": "boolean"},
                            "eeat_metadata": {
                                "type": "object",
                                "required": [
                                    "engineer", "business", "telephone", "experience",
                                    "insurance", "qualifications", "rating", "cai_notice",
                                    "avatar_url", "cover_banner_url"
                                ],
                                "properties": {
                                    "engineer": {"type": "string", "const": "Gary Pearce"},
                                    "business": {"type": "string", "const": "ADI Communications"},
                                    "telephone": {"type": "string", "const": "07860 244 274"},
                                    "experience": {"type": "string"},
                                    "insurance": {"type": "string", "pattern": r"£10,000,000"},
                                    "qualifications": {"type": "string"},
                                    "rating": {"type": "string", "pattern": r"9\.98"},
                                    "cai_notice": {"type": "string", "pattern": r"NOT CAI members"},
                                    "avatar_url": {"type": "string"},
                                    "cover_banner_url": {"type": "string"}
                                },
                                "additionalProperties": False
                            }
                        },
                        "additionalProperties": False
                    }
                }
            },
            "additionalProperties": False
        }

        cls.validator = Draft202012Validator(cls.strict_schema)

    def test_meta_schema_conformance(self):
        """Assert master catalog is compliant with Draft202012Validator meta-schema."""
        Draft202012Validator.check_schema(self.catalog)

    def test_catalog_passes_formal_draft_2020_12_schema(self):
        """Assert master catalog cleanly validates against formal Draft 2020-12 schema with 0 errors."""
        errors = list(self.validator.iter_errors(self.catalog))
        self.assertEqual(len(errors), 0, f"Catalog failed Draft 2020-12 schema: {[e.message for e in errors[:5]]}")

    def test_rejection_of_injected_unexpected_root_property(self):
        """Adversarially inject unexpected property at root level and verify rejection."""
        mutated = copy.deepcopy(self.catalog)
        mutated["unexpected_backdoor_field"] = "malicious_payload"

        errors = list(self.validator.iter_errors(mutated))
        self.assertGreater(len(errors), 0, "Validator must reject injected root property")
        self.assertTrue(any("unexpected_backdoor_field" in e.message for e in errors))

    def test_rejection_of_injected_platform_property(self):
        """Adversarially inject unexpected property inside a platform record and verify rejection."""
        mutated = copy.deepcopy(self.catalog)
        mutated["platforms"][0]["injected_unauthorized_key"] = True

        errors = list(self.validator.iter_errors(mutated))
        self.assertGreater(len(errors), 0, "Validator must reject injected platform property")
        self.assertTrue(any("injected_unauthorized_key" in e.message for e in errors))

    def test_rejection_of_invalid_status_enum(self):
        """Adversarially mutate platform status to invalid enum value and verify rejection."""
        mutated = copy.deepcopy(self.catalog)
        mutated["platforms"][0]["status"] = "INVALID_STATUS_CODE"

        errors = list(self.validator.iter_errors(mutated))
        self.assertGreater(len(errors), 0, "Validator must reject invalid status enum")
        self.assertTrue(any("INVALID_STATUS_CODE" in e.message for e in errors))

    def test_rejection_of_invalid_failure_reason_taxonomy(self):
        """Adversarially mutate failure_reason to non-canonical string and verify rejection."""
        mutated = copy.deepcopy(self.catalog)
        mutated["platforms"][0]["failure_reason"] = "UNKNOWN_VENDOR_REASON"

        errors = list(self.validator.iter_errors(mutated))
        self.assertGreater(len(errors), 0, "Validator must reject non-canonical failure reason")
        self.assertTrue(any("UNKNOWN_VENDOR_REASON" in e.message for e in errors))

    def test_rejection_of_missing_required_platform_field(self):
        """Adversarially delete platform_id and verify rejection."""
        mutated = copy.deepcopy(self.catalog)
        del mutated["platforms"][0]["platform_id"]

        errors = list(self.validator.iter_errors(mutated))
        self.assertGreater(len(errors), 0, "Validator must reject missing platform_id")
        self.assertTrue(any("platform_id" in e.message for e in errors))

    def test_rejection_of_corrupted_phone_number(self):
        """Adversarially corrupt phone number to 0800 number and verify rejection."""
        mutated = copy.deepcopy(self.catalog)
        mutated["platforms"][0]["eeat_metadata"]["telephone"] = "0800 123 456"

        errors = list(self.validator.iter_errors(mutated))
        self.assertGreater(len(errors), 0, "Validator must reject 0800 phone number in eeat_metadata")


# =====================================================================
# Test Class 6: CatalogParitySync Defect Isolation & Sync Tests
# =====================================================================
class TestCatalogParitySyncAndAtomicParity(unittest.TestCase):
    """Stress-test CatalogParitySync atomic updating, defect demonstration, and parity."""

    def setUp(self):
        self.temp_json = REPO_ROOT / "temp_test_catalog.json"
        self.temp_csv = REPO_ROOT / "temp_test_doc2.csv"

        # Copy original catalog to temp
        with open(REPO_ROOT / "master_multicategory_platform_catalog.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        with open(self.temp_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        self.sync = CatalogParitySync(json_path=self.temp_json, csv_path=self.temp_csv)

    def tearDown(self):
        if self.temp_json.exists():
            self.temp_json.unlink()
        if self.temp_csv.exists():
            self.temp_csv.unlink()

    def test_sync_platform_update_maintains_global_platforms_and_csv_parity(self):
        """Assert sync_platform_update atomically updates category_stacks, catalog['platforms'], counts, and CSV."""
        catalog = self.sync.load_catalog()
        initial_joined = catalog.get("total_joined", 0)
        initial_pending = catalog.get("total_pending", 0)

        target_p = None
        for p in catalog["category_stacks"]["video"]["platforms"]:
            if p["status"] == "PENDING":
                target_p = p
                break
        self.assertIsNotNone(target_p)
        target_id = target_p["platform_id"]

        # Execute sync update
        ok, msg = self.sync.sync_platform_update(
            platform_id=target_id,
            new_status="JOINED",
            tenant_url="https://vimeo.com/cctvservices"
        )
        self.assertTrue(ok)

        # Reload updated catalog
        updated_catalog = self.sync.load_catalog()
        stack_plat = [p for p in updated_catalog["category_stacks"]["video"]["platforms"] if p["platform_id"] == target_id][0]
        global_plat = [p for p in updated_catalog["platforms"] if p["platform_id"] == target_id][0]

        # In memory/storage: stack was updated to JOINED
        self.assertEqual(stack_plat["status"], "JOINED")
        self.assertEqual(stack_plat["active_tenant_url"], "https://vimeo.com/cctvservices")
        self.assertIsNone(stack_plat["failure_reason"])

        # Global platform list MUST be updated to JOINED
        self.assertEqual(global_plat["status"], "JOINED", "catalog['platforms'] must be updated to JOINED")
        self.assertEqual(global_plat["active_tenant_url"], "https://vimeo.com/cctvservices")
        self.assertIsNone(global_plat["failure_reason"])

        # Global counts must be atomically updated
        self.assertEqual(updated_catalog["total_joined"], initial_joined + 1)
        self.assertEqual(updated_catalog["total_pending"], initial_pending - 1)

        # And CSV generated from catalog['platforms'] MUST reflect JOINED and active URL
        with open(self.temp_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            matching_row = [r for r in reader if r["Platform ID"] == target_id][0]
            self.assertEqual(matching_row["Status"], "JOINED", "doc2 CSV row must be updated to JOINED")
            self.assertEqual(matching_row["Active Tenant URL"], "https://vimeo.com/cctvservices")
            self.assertEqual(matching_row["Failure Reason"], "")

    def test_non_existent_platform_id_returns_clean_error(self):
        """Assert sync_platform_update handles unknown platform ID without crashing or modifying files."""
        ok, msg = self.sync.sync_platform_update("PLAT-FAKE-999", "JOINED")
        self.assertFalse(ok)
        self.assertIn("not found", msg)


if __name__ == "__main__":
    unittest.main()
