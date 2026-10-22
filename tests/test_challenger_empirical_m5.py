"""
tests/test_challenger_empirical_m5.py
Empirical Challenger Adversarial Stress Test Suite for Milestone 5.
"""

import csv
import http.server
import json
import os
import re
import socket
import sys
import threading
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import swarm_stack_orchestrator as sso


class MockAdversarialServer(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress stderr output

    def do_GET(self):
        if self.path == "/status/200":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        elif self.path == "/loop":
            self.send_response(302)
            self.send_header("Location", "/loop")
            self.end_headers()
        elif self.path == "/loop1":
            self.send_response(301)
            self.send_header("Location", "/loop2")
            self.end_headers()
        elif self.path == "/loop2":
            self.send_response(301)
            self.send_header("Location", "/loop1")
            self.end_headers()
        elif self.path == "/hang":
            time.sleep(2.0)
            try:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Delayed")
            except Exception:
                pass
        else:
            self.send_response(404)
            self.end_headers()


class ChallengerReachabilityStressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.HTTPServer(("127.0.0.1", 0), MockAdversarialServer)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_redirect_loop_self(self):
        """Test HTTP 302 redirecting to itself (/loop). Must return False."""
        url = f"{self.base_url}/loop"
        ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=3.0)
        self.assertFalse(ok, f"Redirect loop should return ok=False, got ok={ok}")
        self.assertEqual(status, 302)
        self.assertTrue("Redirect" in msg or "Loop" in msg or "302" in msg)

    def test_redirect_loop_two_hop(self):
        """Test HTTP 301 two-hop redirect loop (/loop1 -> /loop2 -> /loop1). Must return False."""
        url = f"{self.base_url}/loop1"
        ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=3.0)
        self.assertFalse(ok, f"Two-hop redirect loop should return ok=False, got ok={ok}")
        self.assertIn(status, [301, 302])
        self.assertTrue("Redirect" in msg or "Loop" in msg)

    def test_malformed_urls_do_not_crash(self):
        """Test malformed and schemeless URLs. Must catch ValueError and return ok=False without crashing."""
        malformed_urls = [
            "invalid-url",
            "htp://bad",
            "http://",
            "https://",
            "",
            "ftp://unsupported.com",
            "not_even_close",
            "://missing-scheme",
            "http:///bad-path",
            "gopher://ancient.protocol.net"
        ]
        for url in malformed_urls:
            with self.subTest(url=url):
                try:
                    ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=1.0)
                    self.assertFalse(ok, f"Malformed URL '{url}' should return ok=False")
                    self.assertIsNone(status, f"Malformed URL '{url}' should have status=None")
                    self.assertTrue(len(msg) > 0)
                except Exception as e:
                    self.fail(f"check_url_reachability crashed on '{url}' with {type(e).__name__}: {e}")

    def test_timeout_returns_cleanly(self):
        """Test hanging server response with short timeout."""
        url = f"{self.base_url}/hang"
        ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=0.3)
        self.assertFalse(ok)
        self.assertIsNone(status)
        self.assertIn("Timed Out", msg)


class ChallengerCatalogStressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.json_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        cls.csv_path = REPO_ROOT / "doc2_multicategory_stack_550.csv"

        with open(cls.json_path, "r", encoding="utf-8") as f:
            cls.catalog_json = json.load(f)

        with open(cls.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cls.catalog_csv = list(reader)

        cls.all_json_platforms = []
        for stack_key, stack_data in cls.catalog_json.get("category_stacks", {}).items():
            cls.all_json_platforms.extend(stack_data.get("platforms", []))

    def test_catalog_total_count(self):
        """Must have exactly 550 platforms in both JSON and CSV."""
        self.assertEqual(len(self.all_json_platforms), 550, f"Expected 550 platforms in JSON, got {len(self.all_json_platforms)}")
        self.assertEqual(len(self.catalog_csv), 550, f"Expected 550 rows in CSV, got {len(self.catalog_csv)}")
        self.assertEqual(self.catalog_json.get("total_platforms"), 550)

    def test_category_stacks_count(self):
        """Must have exactly 11 category stacks with 50 platforms each."""
        stacks = self.catalog_json.get("category_stacks", {})
        self.assertEqual(len(stacks), 11, f"Expected 11 stacks in JSON, got {len(stacks)}")
        for sk, sdata in stacks.items():
            count = len(sdata.get("platforms", []))
            self.assertEqual(count, 50, f"Stack {sk} has {count} platforms, expected 50")

    def test_unique_platform_ids(self):
        """All platform_ids must be strictly unique."""
        json_ids = [p["platform_id"] for p in self.all_json_platforms]
        csv_ids = [row["Platform ID"] for row in self.catalog_csv]
        self.assertEqual(len(json_ids), len(set(json_ids)), "Duplicate platform_id found in JSON catalog")
        self.assertEqual(len(csv_ids), len(set(csv_ids)), "Duplicate Platform ID found in CSV catalog")
        self.assertEqual(set(json_ids), set(csv_ids), "Mismatch between JSON platform IDs and CSV platform IDs")

    def test_json_csv_exact_parity(self):
        """Every single row in CSV must match the corresponding JSON platform record."""
        json_by_id = {p["platform_id"]: p for p in self.all_json_platforms}

        for row in self.catalog_csv:
            pid = row["Platform ID"]
            self.assertIn(pid, json_by_id, f"CSV Platform ID {pid} missing from JSON")
            jp = json_by_id[pid]

            self.assertEqual(row["Platform Name"], jp["name"])
            self.assertEqual(row["Domain"], jp["domain"])
            self.assertEqual(int(row["DA"]), int(jp["da"]))
            self.assertEqual(row["Stack Key"], jp["stack_key"])
            self.assertEqual(row["Category"], jp["category"])
            self.assertEqual(row["Tier"], jp["tier"])
            self.assertEqual(row["1-Click Join Method (SSO)"], jp["sso_method"])
            self.assertEqual(row["Official Signup URL"], jp["signup_url"])
            self.assertEqual(row["Status"], jp["status"])
            self.assertEqual(row["Active Tenant URL"], jp["active_tenant_url"] or "")
            self.assertEqual(row["Upward Target URL"], jp["upward_target_url"])
            expected_r45 = "TRUE" if jp["rule_45_compliant"] else "FALSE"
            self.assertEqual(row["Rule 45 Compliant"], expected_r45)

    def test_valid_status_codes(self):
        """Statuses must only be JOINED or PENDING (or FAILED_JOIN)."""
        valid_statuses = {"JOINED", "PENDING", "FAILED_JOIN"}
        for p in self.all_json_platforms:
            st = p.get("status")
            self.assertIn(st, valid_statuses, f"Invalid status '{st}' on {p.get('platform_id')}")

    def test_joined_platforms_have_live_profile_urls(self):
        """Every platform marked JOINED must have an active active_tenant_url."""
        joined_count = 0
        for p in self.all_json_platforms:
            if p.get("status") == "JOINED":
                joined_count += 1
                url = (p.get("active_tenant_url") or "").strip()
                self.assertTrue(len(url) > 0, f"JOINED platform {p.get('platform_id')} missing active_tenant_url")
                self.assertTrue(url.startswith("http://") or url.startswith("https://"))
        self.assertEqual(joined_count, self.catalog_json.get("total_joined"))

    def test_eeat_metadata_integrity(self):
        """Every platform must contain valid Gary Pearce E-E-A-T metadata."""
        for p in self.all_json_platforms:
            eeat = p.get("eeat_metadata", {})
            self.assertEqual(eeat.get("engineer"), "Gary Pearce")
            self.assertEqual(eeat.get("business"), "ADI Communications")
            self.assertIn("07860 244 274", eeat.get("telephone", ""))
            self.assertIn("10,000,000", eeat.get("insurance", ""))
            self.assertIn("NOT CAI members", eeat.get("cai_notice", ""))

    def test_rule_45_zero_raw_root_links(self):
        """Adversarial check: zero raw root links to adicommunications.co.uk/ anywhere in catalog."""
        raw_root_pattern = re.compile(
            r'https?://(?:www\.)?adicommunications\.co\.uk/?(?:[#?][^\s\'"]*)?$',
            re.IGNORECASE
        )
        for p in self.all_json_platforms:
            for field in ["signup_url", "active_tenant_url", "upward_target_url"]:
                val = (p.get(field) or "").strip()
                if val:
                    self.assertIsNone(
                        raw_root_pattern.match(val),
                        f"Rule 45 violation: Raw root link in {p['platform_id']} ({field}): {val}"
                    )

        # Whole-file raw string inspection for naked root anchors
        with open(self.json_path, "r", encoding="utf-8") as f:
            json_text = f.read()
        all_adi_in_json = re.findall(r'https?://[^\s",\']*(?:adicommunications\.co\.uk)[^\s",\']*', json_text)
        for url in all_adi_in_json:
            self.assertIsNone(
                raw_root_pattern.match(url),
                f"Rule 45 violation found in raw JSON text: {url}"
            )

        with open(self.csv_path, "r", encoding="utf-8") as f:
            csv_text = f.read()
        all_adi_in_csv = re.findall(r'https?://[^\s",\']*(?:adicommunications\.co\.uk)[^\s",\']*', csv_text)
        for url in all_adi_in_csv:
            self.assertIsNone(
                raw_root_pattern.match(url),
                f"Rule 45 violation found in raw CSV text: {url}"
            )

    def test_tier3_video_platforms_youtube_only(self):
        """
        Adversarial check: Tier 3 video platforms must link strictly and exclusively to YouTube.
        Zero links to adicommunications.co.uk allowed.
        """
        tier3_video = [
            p for p in self.all_json_platforms
            if p.get("stack_key") == "video" and "Tier 3" in p.get("tier", "")
        ]
        self.assertGreaterEqual(len(tier3_video), 5, "Expected at least 5 Tier 3 video platforms")
        for p in tier3_video:
            target = (p.get("upward_target_url") or "").lower()
            self.assertIn(
                "youtube.com",
                target,
                f"Tier 3 video platform {p['platform_id']} must link to YouTube! Found: {target}"
            )
            self.assertNotIn(
                "adicommunications.co.uk",
                target,
                f"Tier 3 video platform {p['platform_id']} illegally links to website: {target}"
            )


if __name__ == "__main__":
    unittest.main()
