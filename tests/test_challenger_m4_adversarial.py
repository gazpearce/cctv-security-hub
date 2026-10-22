"""
tests/test_challenger_m4_adversarial.py
Milestone 4 Adversarial Empirical Test Battery for swarm_stack_orchestrator.py:
1. Direct empirical verification of check_url_reachability() on HTTP 404, Connection Refused, Timeout, and Server Errors.
2. Direct empirical verification of run_verify() failure behavior, sys.exit(1), telemetry reporting, and guarantee that [VERIFY PASS] is never emitted on failure.
3. Subprocess verification of exit codes for CLI subcommands, legacy options, and invalid arguments.
"""

import io
import os
import socket
import ssl
import subprocess
import sys
import threading
import time
import unittest
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import swarm_stack_orchestrator as sso


class MockServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status/200":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        elif self.path == "/status/404":
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")
        elif self.path == "/status/500":
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Internal Server Error")
        elif self.path == "/slow":
            time.sleep(1.0)
            self.send_response(200)
            self.end_headers()
        elif self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/status/200")
            self.end_headers()
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress logging during tests
        return


class TestAdversarialReachabilityEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start a local HTTP server on an ephemeral port
        cls.server = HTTPServer(("127.0.0.1", 0), MockServerHandler)
        cls.port = cls.server.server_address[1]
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_01_reachability_http_200(self):
        """Verify reachability returns True on HTTP 200."""
        ok, code, msg, elapsed = sso.check_url_reachability(f"{self.base_url}/status/200", timeout=2.0)
        self.assertTrue(ok)
        self.assertEqual(code, 200)
        self.assertIn("HTTP 200 (Verified Reachable", msg)
        self.assertGreaterEqual(elapsed, 0.0)

    def test_02_reachability_http_404(self):
        """Adversarially verify check_url_reachability() on HTTP 404."""
        ok, code, msg, elapsed = sso.check_url_reachability(f"{self.base_url}/status/404", timeout=2.0)
        self.assertFalse(ok)
        self.assertEqual(code, 404)
        self.assertIn("HTTP 404", msg)
        self.assertNotIn("Verified Reachable", msg)

    def test_03_reachability_http_500(self):
        """Adversarially verify check_url_reachability() on HTTP 500."""
        ok, code, msg, elapsed = sso.check_url_reachability(f"{self.base_url}/status/500", timeout=2.0)
        self.assertFalse(ok)
        self.assertEqual(code, 500)
        self.assertIn("HTTP 500", msg)

    def test_04_reachability_connection_refused(self):
        """Adversarially verify check_url_reachability() on Connection Refused (closed port)."""
        # 1. Real closed port on OS
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            closed_port = s.getsockname()[1]
        
        ok, code, msg, elapsed = sso.check_url_reachability(f"http://127.0.0.1:{closed_port}/", timeout=1.0)
        self.assertFalse(ok)
        self.assertIsNone(code)
        self.assertGreater(elapsed, 0.0)
        self.assertTrue(
            "URLError" in msg or "refused" in msg.lower() or "timed out" in msg.lower(),
            f"Expected refusal or timeout message, got: {msg}"
        )

        # 2. Explicit ConnectionRefusedError via URLError
        refused_err = urllib.error.URLError(ConnectionRefusedError(10061, "Connection refused"))
        with patch("urllib.request.urlopen", side_effect=refused_err):
            ok_m, code_m, msg_m, elapsed_m = sso.check_url_reachability("http://127.0.0.1:9999/", timeout=1.0)
            self.assertFalse(ok_m)
            self.assertIsNone(code_m)
            self.assertIn("URLError", msg_m)
            self.assertIn("refused", msg_m.lower())

    def test_05_reachability_timeout(self):
        """Adversarially verify check_url_reachability() on Timeout."""
        ok, code, msg, elapsed = sso.check_url_reachability(f"{self.base_url}/slow", timeout=0.05)
        self.assertFalse(ok)
        self.assertIsNone(code)
        self.assertIn("Timed Out", msg)

    def test_06_reachability_redirect_resolution(self):
        """Verify redirect resolution (302 -> 200)."""
        ok, code, msg, elapsed = sso.check_url_reachability(f"{self.base_url}/redirect", timeout=2.0)
        self.assertTrue(ok)
        self.assertEqual(code, 200)

    def test_07_run_verify_catches_404_failure_and_exits_code_1(self):
        """Adversarially test run_verify() when one stack returns HTTP 404."""
        # Monkeypatch STACK_TEAMS so 'howto' returns 404
        orig_teams = dict(sso.STACK_TEAMS)
        bad_teams = dict(orig_teams)
        bad_teams["howto"] = {
            "agent": "stack-howto-agent",
            "apex": f"{self.base_url}/status/404",
            "description": "Test 404",
            "script": "generate_trade_whitepapers.py"
        }

        captured_stdout = io.StringIO()
        with patch.dict(sso.STACK_TEAMS, bad_teams), patch("sys.stdout", captured_stdout):
            with self.assertRaises(SystemExit) as cm:
                sso.run_verify()
            self.assertEqual(cm.exception.code, 1)

        output = captured_stdout.getvalue()
        self.assertIn("[HOWTO   ] Apex:", output)
        self.assertIn("UNREACHABLE: HTTP 404", output)
        self.assertIn("[VERIFY FAIL] 1/11 apex endpoints failed verification!", output)
        self.assertIn("Apex Verification Telemetry: 10/11 Endpoints Reachable", output)
        self.assertNotIn("[VERIFY PASS] All 11/11 Top-of-Stack Google Citadel", output)

    def test_08_run_verify_catches_connection_refused_and_exits_code_1(self):
        """Adversarially test run_verify() when one stack has Connection Refused."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            closed_port = s.getsockname()[1]

        orig_teams = dict(sso.STACK_TEAMS)
        bad_teams = dict(orig_teams)
        bad_teams["music"] = {
            "agent": "stack-music-agent",
            "apex": f"http://127.0.0.1:{closed_port}/",
            "description": "Test Refused",
            "script": "generate_studio_music_tracks.py"
        }

        captured_stdout = io.StringIO()
        with patch.dict(sso.STACK_TEAMS, bad_teams), patch("sys.stdout", captured_stdout):
            with self.assertRaises(SystemExit) as cm:
                sso.run_verify()
            self.assertEqual(cm.exception.code, 1)

        output = captured_stdout.getvalue()
        self.assertIn("[MUSIC   ] Apex:", output)
        self.assertIn("UNREACHABLE:", output)
        self.assertIn("[VERIFY FAIL] 1/11 apex endpoints failed verification!", output)
        self.assertIn("Apex Verification Telemetry: 10/11 Endpoints Reachable", output)
        self.assertNotIn("[VERIFY PASS] All 11/11 Top-of-Stack Google Citadel", output)

    def test_09_run_verify_catches_timeout_and_exits_code_1(self):
        """Adversarially test run_verify() when one stack times out."""
        orig_teams = dict(sso.STACK_TEAMS)
        bad_teams = dict(orig_teams)
        bad_teams["podcast"] = {
            "agent": "stack-podcast-agent",
            "apex": f"{self.base_url}/slow",
            "description": "Test Slow",
            "script": "syndicate_archive_media.py"
        }

        captured_stdout = io.StringIO()
        # Mock check_url_reachability timeout param or mock function to simulate timeout
        with patch.dict(sso.STACK_TEAMS, bad_teams), \
             patch("swarm_stack_orchestrator.check_url_reachability", side_effect=lambda url, timeout=5.0, user_agent="": (
                 (False, None, "Connection Timed Out (>5.0s)", 5.01) if "slow" in url
                 else (True, 200, "HTTP 200 (Verified Reachable in 0.10s)", 0.10)
             )), \
             patch("sys.stdout", captured_stdout):
            with self.assertRaises(SystemExit) as cm:
                sso.run_verify()
            self.assertEqual(cm.exception.code, 1)

        output = captured_stdout.getvalue()
        self.assertIn("[PODCAST ] Apex:", output)
        self.assertIn("UNREACHABLE: Connection Timed Out", output)
        self.assertIn("[VERIFY FAIL] 1/11 apex endpoints failed verification!", output)
        self.assertIn("Apex Verification Telemetry: 10/11 Endpoints Reachable", output)
        self.assertNotIn("[VERIFY PASS] All 11/11 Top-of-Stack Google Citadel", output)

    def test_10_run_verify_catches_missing_stack_key(self):
        """Adversarially test run_verify() when a required stack key is missing from STACK_TEAMS."""
        bad_teams = dict(sso.STACK_TEAMS)
        del bad_teams["offers"]

        captured_stdout = io.StringIO()
        with patch.dict(sso.STACK_TEAMS, bad_teams, clear=True), patch("sys.stdout", captured_stdout):
            with self.assertRaises(SystemExit) as cm:
                sso.run_verify()
            self.assertEqual(cm.exception.code, 1)

        output = captured_stdout.getvalue()
        self.assertIn("[OFFERS  ] Apex: [NOT DEFINED IN STACK_TEAMS] -> FAILED", output)
        self.assertIn("[VERIFY FAIL] 1/11 apex endpoints failed verification!", output)
        self.assertNotIn("[VERIFY PASS] All 11/11 Top-of-Stack Google Citadel", output)


class TestCliSubcommandsAndFlags(unittest.TestCase):
    def run_cli(self, args):
        cmd = [sys.executable, str(REPO_ROOT / "swarm_stack_orchestrator.py")] + args
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        return res

    def test_cli_status(self):
        res = self.run_cli(["status"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("[STATUS PASS]", res.stdout)
        self.assertIn("Total Published Backlinks", res.stdout)

    def test_cli_sync(self):
        res = self.run_cli(["sync"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("[SYNC PASS]", res.stdout)

    def test_cli_audit(self):
        res = self.run_cli(["audit"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("[AUDIT PASS]", res.stdout)

    def test_cli_deploy_skip_deploy(self):
        res = self.run_cli(["deploy", "--skip-deploy"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("[DEPLOY] --skip-deploy requested.", res.stdout)

    def test_cli_legacy_flags_ledger(self):
        res = self.run_cli(["--skip-deploy", "--stack", "ledger"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("EXECUTING TARGET STACK: LEDGER", res.stdout)
        self.assertIn("[SYNC PASS]", res.stdout)

    def test_cli_legacy_flags_all(self):
        res = self.run_cli(["--skip-deploy", "--stack", "all"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("EXECUTING TARGET STACK: ALL", res.stdout)
        self.assertIn("[SYNC PASS]", res.stdout)

    def test_cli_invalid_choice_fails_exit_code_2(self):
        res = self.run_cli(["invalid_choice"])
        self.assertEqual(res.returncode, 2, f"Expected exit code 2, got {res.returncode}: {res.stderr}")
        self.assertIn("invalid choice: 'invalid_choice'", res.stderr)

    def test_cli_invalid_stack_fails_exit_code_2(self):
        res = self.run_cli(["--stack", "nonexistent_stack"])
        self.assertEqual(res.returncode, 2)
        self.assertIn("invalid choice: 'nonexistent_stack'", res.stderr)


if __name__ == "__main__":
    unittest.main()
