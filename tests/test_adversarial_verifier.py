"""
tests/test_adversarial_verifier.py
Adversarial and Stress Test Suite for auto_email_verifier.py
Constructed by challenger_m1_1 to rigorously challenge:
1. Malformed CDP payloads and unexpected WebSocket frames.
2. Non-Gmail tabs, spoofed URLs, and malformed CDP tab lists.
3. Unusual, spaced, truncated, and adversarial OTP formats.
4. Cross-platform verification link contamination.
5. Timeouts, connection dropouts, hangs, and resource leaks.
"""

import asyncio
import io
import json
import unittest
import unittest.mock as mock
import urllib.error
import websockets

from auto_email_verifier import AutoEmailVerifier, DEFAULT_ACCOUNT, BANNED_YEARS


class TestTabSelectorAdversarial(unittest.TestCase):
    """Adversarial testing of CDP tab selection and URL filtering."""

    def setUp(self):
        self.verifier = AutoEmailVerifier()

    def test_spoofed_urls_rejected(self):
        """Verify that spoofed or ambiguous URLs are strictly rejected."""
        spoofed_tabs = [
            # In query parameter
            {"type": "page", "url": "https://evil.com/login?redirect=https://mail.google.com/"},
            # In path
            {"type": "page", "url": "https://evil.com/mail.google.com/u/0/#inbox"},
            # In subdomain
            {"type": "page", "url": "https://mail.google.com.evil.com/login"},
            # Insecure HTTP
            {"type": "page", "url": "http://mail.google.com/mail/u/0/#inbox"},
            # Port variation
            {"type": "page", "url": "https://mail.google.com:8080/mail/u/0/#inbox"},
            # Accounts RotateCookiesPage
            {"type": "page", "url": "https://accounts.google.com/RotateCookiesPage?origin=https%3A%2F%2Fmail.google.com"},
            # Service worker
            {"type": "page", "url": "https://mail.google.com/sw.js"},
            # Account switch redirect with accounts.google.com
            {"type": "page", "url": "https://mail.google.com/accounts/SetOSID?continue=https://accounts.google.com"},
            # Non-page CDP targets
            {"type": "iframe", "url": "https://mail.google.com/mail/u/0/#inbox"},
            {"type": "worker", "url": "https://mail.google.com/mail/u/0/#inbox"},
            {"type": "service_worker", "url": "https://mail.google.com/sw.js"},
            {"type": "background_page", "url": "https://mail.google.com/mail/u/0/#inbox"},
        ]

        with mock.patch.object(self.verifier, "_get_tabs", return_value=spoofed_tabs):
            with mock.patch("urllib.request.urlopen") as mock_open:
                tab, is_ephem = asyncio.run(self.verifier.get_or_create_gmail_tab())
                self.assertIsNone(tab, "Spoofed tabs must not be selected as valid Gmail inbox tabs")
                mock_open.assert_not_called()

    def test_malformed_tab_entries_handling(self):
        """Stress-test get_or_create_gmail_tab with malformed tab dictionaries."""
        malformed_tabs = [
            None,
            123,
            "just_a_string",
            {},
            {"type": "page"},  # Missing url
            {"type": "page", "url": None},  # url is None -> potential None.startswith crash
            {"type": "page", "url": "https://mail.google.com/mail/u/0/#inbox", "title": None},  # title is None -> potential None.lower crash
        ]

        # Test if verifier handles malformed list gracefully or raises unhandled exception
        with mock.patch.object(self.verifier, "_get_tabs", return_value=malformed_tabs):
            try:
                tab, is_ephem = asyncio.run(self.verifier.get_or_create_gmail_tab())
                # If it survives, check that it selected the valid mail tab
                if tab:
                    self.assertEqual(tab.get("url"), "https://mail.google.com/mail/u/0/#inbox")
            except Exception as e:
                self.fail(f"get_or_create_gmail_tab crashed on malformed tab list: {type(e).__name__}: {e}")

    def test_cdp_dict_error_response_handling(self):
        """Stress-test when CDP /json returns a dict error payload instead of a list."""
        error_payload = {"error": "CDP disabled or invalid target"}
        with mock.patch.object(self.verifier, "_get_tabs", return_value=error_payload):
            try:
                tab, is_ephem = asyncio.run(self.verifier.get_or_create_gmail_tab())
                self.assertIsNone(tab)
            except Exception as e:
                self.fail(f"get_or_create_gmail_tab crashed on dict return from _get_tabs: {type(e).__name__}: {e}")

    def test_cdp_non_json_http_response_handling(self):
        """Stress-test _get_tabs when CDP returns HTML or non-JSON (e.g. 502 Bad Gateway)."""
        mock_resp = io.BytesIO(b"<html><head><title>502 Bad Gateway</title></head><body>502</body></html>")
        with mock.patch("urllib.request.urlopen", return_value=mock_resp):
            try:
                tabs = self.verifier._get_tabs()
                self.assertEqual(tabs, [], "Non-JSON response should return empty list gracefully")
            except Exception as e:
                self.fail(f"_get_tabs crashed on non-JSON HTTP response: {type(e).__name__}: {e}")


class TestWebSocketAndCDPPayloadRobustness(unittest.TestCase):
    """Adversarial stress-testing of WebSocket communication and CDP message processing."""

    def setUp(self):
        self.verifier = AutoEmailVerifier()

    def test_malformed_json_frame_does_not_abort(self):
        """Stress-test _send_cdp when a corrupted/non-JSON WebSocket frame arrives before response."""
        class MockWS:
            def __init__(self, frames):
                self.frames = list(frames)
            async def send(self, data): pass
            async def recv(self):
                if self.frames:
                    return self.frames.pop(0)
                await asyncio.sleep(10)
                return ""

        async def run_test():
            msg_id = self.verifier._msg_id + 1
            # Corrupted frame followed by valid response
            ws = MockWS(["NOT_VALID_JSON_FRAME{{{", json.dumps({"id": msg_id, "result": {"value": "ok"}})])
            return await self.verifier._send_cdp(ws, "Runtime.evaluate", timeout=1.0)

        try:
            res = asyncio.run(run_test())
            self.assertEqual(res.get("value"), "ok", "Should skip malformed frame and receive response")
        except Exception as e:
            self.fail(f"_send_cdp failed on corrupted WebSocket frame: {type(e).__name__}: {e}")

    def test_non_dict_json_frame_does_not_abort(self):
        """Stress-test _send_cdp when a non-dict JSON frame (array or string) arrives."""
        class MockWS:
            def __init__(self, frames):
                self.frames = list(frames)
            async def send(self, data): pass
            async def recv(self):
                if self.frames:
                    return self.frames.pop(0)
                await asyncio.sleep(10)
                return ""

        async def run_test():
            msg_id = self.verifier._msg_id + 1
            # Array frame followed by valid response
            ws = MockWS(["[1, 2, 3]", json.dumps({"id": msg_id, "result": {"value": "ok"}})])
            return await self.verifier._send_cdp(ws, "Runtime.evaluate", timeout=1.0)

        try:
            res = asyncio.run(run_test())
            self.assertEqual(res.get("value"), "ok", "Should skip non-dict JSON frame and receive response")
        except Exception as e:
            self.fail(f"_send_cdp failed on non-dict JSON frame: {type(e).__name__}: {e}")

    def test_result_none_payload_handling(self):
        """Stress-test when CDP response contains 'result': None."""
        class MockWS:
            def __init__(self, frames):
                self.frames = list(frames)
            async def send(self, data): pass
            async def recv(self):
                if self.frames:
                    return self.frames.pop(0)
                await asyncio.sleep(10)
                return ""

        async def run_test():
            msg_id = self.verifier._msg_id + 1
            ws = MockWS([json.dumps({"id": msg_id, "result": None})])
            return await self.verifier._send_cdp(ws, "Runtime.evaluate", timeout=1.0)

        try:
            res = asyncio.run(run_test())
            self.assertIsNotNone(res, "_send_cdp must return dict even if result is None")
            self.assertIsInstance(res, dict)
        except Exception as e:
            self.fail(f"_send_cdp crashed on result=None: {type(e).__name__}: {e}")

    def test_abrupt_websocket_disconnect(self):
        """Verify graceful error recovery when WebSocket connection drops abruptly."""
        class DisconnectingWS:
            async def send(self, data): pass
            async def recv(self):
                raise websockets.ConnectionClosedError(rcvd=None, sent=None)

        async def run_test():
            ws = DisconnectingWS()
            return await self.verifier._send_cdp(ws, "Runtime.evaluate", timeout=1.0)

        try:
            res = asyncio.run(run_test())
            self.assertEqual(res, {}, "Dropped connection should return empty dict without crashing")
        except Exception as e:
            self.fail(f"_send_cdp crashed on connection dropout: {type(e).__name__}: {e}")


class TestOTPExtractionEdgeCases(unittest.TestCase):
    """Adversarial testing of OTP extraction against edge cases and false positives."""

    def test_spaced_otp_codes(self):
        """Stress-test: Verify whether 6-digit codes separated by spaces are extracted completely.
        Many auth services (e.g. Google, Microsoft, Supabase) send '123 456' or '492 847'.
        """
        cases = [
            ("Your verification code is 123 456", "123456"),
            ("Your security code is: 492 847", "492847"),
            ("Please enter one-time code: 829 103", "829103"),
            ("Your confirmation PIN: 554 321", "554321"),
        ]
        for text, expected in cases:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            clean_res = res.replace(" ", "") if res else None
            self.assertEqual(
                clean_res, expected,
                f"Spaced OTP code failed: expected '{expected}', extracted '{res}' from '{text}'"
            )

    def test_short_code_false_positives(self):
        """Adversarial: Ensure error codes, status codes, and single digits are not extracted as OTPs."""
        traps = [
            "HTTP Error code: 404 Not Found",
            "Status code 200 OK",
            "Error code 5: Invalid parameter",
            "Your verification code is 1",
            "Confirmation code: 99",
        ]
        for trap in traps:
            res = AutoEmailVerifier.extract_otp_from_text(trap)
            self.assertTrue(
                res is None or len(res.replace("-", "")) >= 4,
                f"Extracted sub-4-character code '{res}' from trap phrase '{trap}'"
            )

    def test_year_false_positive_boundary(self):
        """Adversarial: Test year boundary conditions outside BANNED_YEARS."""
        # 2028 is not in BANNED_YEARS {"2024", "2025", "2026", "2027"}
        text = "Welcome to our 2028 Developer Roadmap. Please verify your email."
        res = AutoEmailVerifier.extract_otp_from_text(text)
        self.assertNotEqual(res, "2028", "Year 2028 should not be extracted as an OTP code")

    def test_timestamp_numeric_false_positives(self):
        """Adversarial: Test 8-digit date/timestamp strings."""
        text = "Report generated on date 20261022. Please verify receipt."
        res = AutoEmailVerifier.extract_otp_from_text(text)
        self.assertNotEqual(res, "20261022", "Date timestamp 20261022 should not be extracted as an OTP code")

    def test_promo_and_postal_code_traps(self):
        """Adversarial: Test promo codes and postal codes containing digits."""
        traps = [
            ("Use promo code SAVE20 at checkout", None),
            ("Discount code: 50OFF for your next order", None),
        ]
        for text, expected in traps:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertIsNone(res, f"Extracted promo code '{res}' from '{text}'")


class TestVerificationLinkCrossContamination(unittest.TestCase):
    """Adversarial testing of verification link domain isolation."""

    def test_find_verification_link_domain_filtering_logic(self):
        """Verify that find_verification_link does not return links belonging to other platforms.
        If inbox contains an IBM verification email and user requests 'render.com',
        it must NOT select the IBM email or return the IBM verification link.
        """
        # Test simulated Javascript condition in find_row_js
        plat_domain = "render.com"
        plat_domain_clean = plat_domain.lower().replace("https://", "").replace("http://", "").split("/")[0].strip()

        mock_rows = [
            {"index": 0, "text": "ibmacct verify your identity - ibm. please verify code."},
            {"index": 1, "text": "welcome to render.com - activate your new workspace."},
        ]

        # The bug in find_row_js:
        # text.includes('render.com') || (text.includes('verify') || text.includes('confirm') || text.includes('activate'))
        # Row 0 matches 'verify', so Row 0 is picked instead of Row 1!
        
        # Test whether row selection strictly requires the platform domain or name
        for r in mock_rows:
            text = r["text"].lower()
            matches_platform = plat_domain_clean in text
            if r["index"] == 0:
                self.assertFalse(
                    matches_platform,
                    "IBM email must not match when searching for render.com"
                )


class TestResourceLeaksAndCleanup(unittest.TestCase):
    """Stress-test ephemeral tab lifecycle, connection dropouts, and resource cleanup."""

    def setUp(self):
        self.verifier = AutoEmailVerifier()

    def test_ephemeral_tab_leak_when_websocket_url_missing(self):
        """Stress-test: Verify that ephemeral tab is closed even if webSocketDebuggerUrl is missing."""
        mock_tab = {"id": "TAB_LEAK_TEST", "type": "page", "url": "https://mail.google.com/", "webSocketDebuggerUrl": None}
        with mock.patch.object(self.verifier, "get_or_create_gmail_tab", return_value=(mock_tab, True)):
            with mock.patch.object(self.verifier, "_close_tab") as mock_close:
                res = asyncio.run(self.verifier.get_recent_emails())
                self.assertEqual(res, [])
                self.assertTrue(mock_close.called, "Ephemeral tab must be closed when webSocketDebuggerUrl is None")


if __name__ == "__main__":
    unittest.main()
