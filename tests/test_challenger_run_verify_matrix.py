"""
tests/test_challenger_run_verify_matrix.py
Adversarially tests run_verify exit code and output when individual endpoints fail.
Verifies whether run_verify can be tricked into returning exit code 0 under various failure modes.
"""

import copy
import subprocess
import sys
import os
import unittest
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

import swarm_stack_orchestrator as sso


class MockFailureServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/status/200":
            self.send_response(200)
            self.end_headers()
        elif self.path == "/status/404":
            self.send_response(404)
            self.end_headers()
        elif self.path == "/status/500":
            self.send_response(500)
            self.end_headers()
        elif self.path == "/loop":
            self.send_response(302)
            self.send_header("Location", "/loop")
            self.end_headers()


class RunVerifyFailureMatrixTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), MockFailureServer)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def run_verify_subprocess(self, target_stack, mock_url):
        code = f"""
import sys
import swarm_stack_orchestrator as sso
sso.STACK_TEAMS['{target_stack}']['apex'] = '{mock_url}'
sso.run_verify()
"""
        res = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        return res.returncode, res.stdout, res.stderr

    def test_matrix_all_11_stacks_fail_on_404(self):
        """Every stack must cause run_verify to exit 1 when returning HTTP 404."""
        for stack in sso.CATEGORY_STACK_KEYS:
            with self.subTest(stack=stack):
                ret, stdout, stderr = self.run_verify_subprocess(stack, f"{self.base_url}/status/404")
                self.assertEqual(ret, 1, f"Stack {stack} did not trigger exit code 1 on 404!")
                self.assertIn("[VERIFY FAIL]", stdout)
                self.assertIn("10/11 Endpoints Reachable", stdout)

    def test_matrix_all_11_stacks_fail_on_500(self):
        """Every stack must cause run_verify to exit 1 when returning HTTP 500."""
        for stack in sso.CATEGORY_STACK_KEYS:
            with self.subTest(stack=stack):
                ret, stdout, stderr = self.run_verify_subprocess(stack, f"{self.base_url}/status/500")
                self.assertEqual(ret, 1, f"Stack {stack} did not trigger exit code 1 on 500!")
                self.assertIn("[VERIFY FAIL]", stdout)
                self.assertIn("10/11 Endpoints Reachable", stdout)

    def test_matrix_all_11_stacks_fail_on_dns_error(self):
        """Every stack must cause run_verify to exit 1 when DNS fails."""
        bad_dns = "https://this-does-not-exist-9999999.invalid/"
        for stack in sso.CATEGORY_STACK_KEYS:
            with self.subTest(stack=stack):
                ret, stdout, stderr = self.run_verify_subprocess(stack, bad_dns)
                self.assertEqual(ret, 1, f"Stack {stack} did not trigger exit code 1 on DNS failure!")
                self.assertIn("[VERIFY FAIL]", stdout)
                self.assertIn("10/11 Endpoints Reachable", stdout)

    def test_matrix_redirect_loop_vulnerability(self):
        """
        Adversarial test: an infinite redirect loop is probed.
        Does run_verify get TRICKED into returning exit code 0?
        """
        ret, stdout, stderr = self.run_verify_subprocess("howto", f"{self.base_url}/loop")
        print("\n--- Redirect Loop Subprocess Test ---")
        print("Return code:", ret)
        if ret == 0:
            print("ALERT: run_verify WAS TRICKED into returning exit code 0 on an infinite redirect loop!")
        # We record whether it's vulnerable
        self.vulnerable = (ret == 0)

    def test_matrix_malformed_url_vulnerability(self):
        """
        Adversarial test: malformed URL without scheme.
        Does run_verify crash unhandled with ValueError?
        """
        ret, stdout, stderr = self.run_verify_subprocess("video", "not-a-valid-url")
        print("\n--- Malformed URL Subprocess Test ---")
        print("Return code:", ret)
        print("Stderr:", stderr[:200] if stderr else "None")
        # If it crashed with ValueError, returncode is 1, but it failed via unhandled exception
        if "ValueError" in stderr:
            print("ALERT: run_verify crashed with unhandled ValueError rather than clean verification failure!")


if __name__ == "__main__":
    unittest.main()
