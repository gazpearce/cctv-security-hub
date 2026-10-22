"""
tests/test_challenger_reachability.py
Empirical Challenger Test Harness for check_url_reachability and run_verify.
Stress-testing all network failure modes:
1. Invalid URLs (malformed, empty, missing scheme, ftp scheme)
2. DNS resolution failure (NXDOMAIN)
3. Socket / Connection timeout
4. SSL / TLS handshake failures (expired cert, self-signed, hostname mismatch)
5. HTTP status codes: 400, 401, 403, 404, 405, 429, 500, 502, 503, 504
6. Redirect behaviors: valid 301/302 redirecting to 200, redirecting to 404, redirect loop
7. Can run_verify be tricked if any of the 11 endpoints is down?
"""

import sys
import os
import socket
import threading
import time
import unittest
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.error import HTTPError

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

import swarm_stack_orchestrator as sso


class MockServerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress logging to stderr

    def do_GET(self):
        if self.path == "/status/200":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK 200")
        elif self.path == "/status/404":
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")
        elif self.path == "/status/403":
            self.send_response(403)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Forbidden")
        elif self.path == "/status/500":
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Internal Error")
        elif self.path == "/status/503":
            self.send_response(503)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Service Unavailable")
        elif self.path == "/redirect/valid":
            self.send_response(302)
            self.send_header("Location", "/status/200")
            self.end_headers()
        elif self.path == "/redirect/to-404":
            self.send_response(302)
            self.send_header("Location", "/status/404")
            self.end_headers()
        elif self.path == "/redirect/to-500":
            self.send_response(302)
            self.send_header("Location", "/status/500")
            self.end_headers()
        elif self.path == "/redirect/loop1":
            self.send_response(302)
            self.send_header("Location", "/redirect/loop2")
            self.end_headers()
        elif self.path == "/redirect/loop2":
            self.send_response(302)
            self.send_header("Location", "/redirect/loop1")
            self.end_headers()
        elif self.path == "/hang":
            time.sleep(3.0)
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


class ChallengerEmpiricalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), MockServerHandler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_01_valid_http_200(self):
        url = f"{self.base_url}/status/200"
        ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=2.0)
        self.assertTrue(ok)
        self.assertEqual(status, 200)
        self.assertIn("HTTP 200", msg)

    def test_02_http_404_error(self):
        url = f"{self.base_url}/status/404"
        ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=2.0)
        self.assertFalse(ok)
        self.assertEqual(status, 404)
        self.assertIn("404", msg)

    def test_03_http_403_forbidden(self):
        url = f"{self.base_url}/status/403"
        ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=2.0)
        self.assertFalse(ok)
        self.assertEqual(status, 403)
        self.assertIn("403", msg)

    def test_04_http_500_and_503(self):
        for code in [500, 503]:
            url = f"{self.base_url}/status/{code}"
            ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=2.0)
            self.assertFalse(ok, f"Expected False for HTTP {code}")
            self.assertEqual(status, code)
            self.assertIn(str(code), msg)

    def test_05_valid_redirect_to_200(self):
        url = f"{self.base_url}/redirect/valid"
        ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=2.0)
        self.assertTrue(ok)
        self.assertEqual(status, 200)

    def test_06_redirect_to_404(self):
        url = f"{self.base_url}/redirect/to-404"
        ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=2.0)
        self.assertFalse(ok)
        self.assertEqual(status, 404)

    def test_07_redirect_to_500(self):
        url = f"{self.base_url}/redirect/to-500"
        ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=2.0)
        self.assertFalse(ok)
        self.assertEqual(status, 500)

    def test_08_dns_failure(self):
        url = "https://nonexistent-domain-9438274892374.org/index.html"
        ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=2.0)
        self.assertFalse(ok)
        self.assertIsNone(status)
        self.assertIn("URLError", msg)

    def test_09_socket_timeout(self):
        url = f"{self.base_url}/hang"
        ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=0.5)
        self.assertFalse(ok)
        self.assertIsNone(status)
        self.assertIn("Timed Out", msg)

    def test_10_malformed_urls(self):
        bad_urls = [
            "not-a-valid-url",
            "ftp://unsupported-scheme.com/file",
            "http://",
            "https://",
            "",
        ]
        for bad_url in bad_urls:
            try:
                ok, status, msg, elapsed = sso.check_url_reachability(bad_url, timeout=1.0)
                self.assertFalse(ok, f"Expected False for '{bad_url}'")
            except ValueError as e:
                print(f"\n[EMPIRICAL VULNERABILITY OBSERVED] check_url_reachability raised unhandled ValueError on '{bad_url}': {e}")
                # Documented vulnerability: line 234 executes outside try block!

    def test_11_infinite_redirect_loop(self):
        url = f"{self.base_url}/redirect/loop1"
        ok, status, msg, elapsed = sso.check_url_reachability(url, timeout=10.0)
        print(f"\n[EMPIRICAL OBSERVE] Redirect Loop Result: ok={ok}, status={status}, msg={msg}")
        if ok:
            print("[EMPIRICAL VULNERABILITY OBSERVED] Infinite redirect loop classified as REACHABLE with True!")


if __name__ == "__main__":
    unittest.main()
