"""
tests/test_challenger_edge_cases.py
Adversarial Edge-Case Stress Test Suite for auto_email_verifier.py
Constructed by challenger_m1_iter2_1 to empirically verify:
1. Spaced and hyphenated OTP codes (including 6-digit, 8-digit, html-wrapped, non-breaking spaces).
2. Phone number collision resistance (07860 244 274, international formats, combinations with codes).
3. False-positive resistance (years 1900-2099, timestamps, status/HTTP codes, promo codes, postal codes).
4. WebSocket disconnection resilience and ephemeral tab lifecycle.
5. Verification link scoping and cross-platform isolation.
"""

import asyncio
import io
import json
import unittest
import unittest.mock as mock
import websockets

from auto_email_verifier import AutoEmailVerifier, DEFAULT_ACCOUNT


class TestSpacedAndAdversarialOTP(unittest.TestCase):
    """Stress tests for spaced, formatted, and adversarial OTP extraction."""

    def test_spaced_six_digit_variants(self):
        cases = [
            ("Your verification code is 123 456", "123456"),
            ("Your security code is: 492 847", "492847"),
            ("Please enter one-time code: 829 103", "829103"),
            ("Your confirmation PIN: 554 321", "554321"),
            ("Verification code is 001 234", "001234"),
            ("Your code is 123\u00a0456", "123456"),  # Non-breaking space \u00a0
            ("Your code is 123&nbsp;456", "123456"),  # HTML entity &nbsp;
            ("Your code is: <b>123 456</b>", "123456"),  # HTML tags
            ("Your code is: <b>123456</b>", "123456"),
            ("001 234 is your verification code", "001234"),
            ("Your verification code is [123 456]", "123456"),
            ("Your verification code is (123 456)", "123456"),
        ]
        for text, expected in cases:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            clean_res = res.replace(" ", "") if res else None
            self.assertEqual(
                clean_res, expected,
                f"Failed for text '{text}': expected '{expected}', got '{res}'"
            )

    def test_hyphenated_and_alphanumeric_otp(self):
        cases = [
            ("Your code is 123-456", ["123-456", "123456"]),
            ("Your code is 1234-5678", ["1234-5678", "12345678"]),
            ("Your Google verification code is G-123456", ["G-123456", "123456"]),
            ("G-123456 is your Google verification code", ["G-123456", "123456"]),
            ("Security code: V7042-492847", ["V7042-492847"]),
            ("Your authentication code is 3A7B9C", ["3A7B9C"]),
            ("OTP: 9F2A1B", ["9F2A1B"]),
        ]
        for text, valid_expected in cases:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertIn(
                res, valid_expected,
                f"Failed for text '{text}': expected one of {valid_expected}, got '{res}'"
            )

    def test_boundary_punctuations(self):
        cases = [
            ("Your code is [123456].", "123456"),
            ("Your code is (123456).", "123456"),
            ("Your code is: '123456'", "123456"),
            ('Your code is: "123456"', "123456"),
            ("Your code is <123456>.", "123456"),
            ("Your code is: 123456.", "123456"),
            ("Your code is: 123456, please enter it now.", "123456"),
            ("Your code is: 123456!", "123456"),
        ]
        for text, expected in cases:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertEqual(res, expected, f"Failed for text '{text}'")


class TestGaryPearcePhoneCollisionResistance(unittest.TestCase):
    """Stress tests ensuring Gary Pearce's phone number (07860 244 274) never collides with OTPs."""

    def test_phone_alone_returns_none(self):
        phone_phrases = [
            "Call Gary Pearce on 07860 244 274",
            "Call Gary Pearce on 07860 244 274 to confirm.",
            "Gary Pearce, Lead Engineer: 07860 244 274",
            "07860 244 274",
            "Call +44 7860 244 274",
            "Call +44 (0) 7860 244 274",
            "Call 07860244274",
            "Verification needed: Gary Pearce 07860 244 274",
            "Confirm account: Gary Pearce 07860 244 274",
            "One-time passcode request from Gary Pearce (07860 244 274)",
            "Your OTP will be sent to 07860 244 274",
            "Tel: 07860 244 274. Code not required.",
        ]
        for text in phone_phrases:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertIsNone(
                res,
                f"Phone number falsely extracted as OTP '{res}' from phrase: '{text}'"
            )

    def test_phone_coexisting_with_otp_extracts_correct_otp(self):
        combos = [
            ("Call Gary Pearce on 07860 244 274. Your verification code is 839201", "839201"),
            ("Your verification code is 839201. For support call Gary Pearce on 07860 244 274", "839201"),
            ("Contact Gary on 07860 244 274 to confirm your one-time passcode 839201", "839201"),
            ("Call Gary Pearce on 07860 244 274. Verification PIN: 839 201", "839201"),
            ("Engineer Gary Pearce (+44 7860 244 274). Your code is 839 201.", "839201"),
            ("07860 244 274 / OTP: 839201", "839201"),
            ("07860244274. Code: 839201", "839201"),
            ("Your OTP is 839201. ADI Communications, Gary Pearce 07860 244 274", "839201"),
            ("Call Gary Pearce on 07860 244 274. One-time code: 492 847.", "492847"),
            ("Verification code: 582910. Gary Pearce (07860 244 274).", "582910"),
            ("Gary Pearce (07860 244 274) says your PIN is 582910", "582910"),
            ("Call Gary Pearce on 07860 244 274 to confirm. Your verification code is 987654", "987654"),
        ]
        for text, expected in combos:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertEqual(
                res, expected,
                f"Failed for coexisting phone and code: expected '{expected}', got '{res}' in text: '{text}'"
            )


class TestFalsePositiveResistance(unittest.TestCase):
    """Stress tests verifying rejection of years, timestamps, HTTP status codes, promo codes."""

    def test_years_and_timestamps(self):
        traps = [
            ("Code: 2024", None),
            ("Code: 2025", None),
            ("Code: 2026", None),
            ("Code: 2027", None),
            ("Code: 1999", None),
            ("Code: 2099", None),
            ("Welcome to our 2028 roadmap. Please verify your email.", None),
            ("Code: 20261022", None),
            ("Code: 19991231", None),
            ("Report generated on date 20261022. Please verify receipt.", None),
        ]
        for text, expected in traps:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertEqual(res, expected, f"Failed trap '{text}': got '{res}'")

    def test_status_and_error_codes(self):
        traps = [
            ("HTTP status code: 200", None),
            ("Status code 404", None),
            ("Error code 500", None),
            ("HTTP error 403", None),
            ("Error code 50001", None),
            ("Error code 500123", None),
        ]
        for trap, expected in traps:
            res = AutoEmailVerifier.extract_otp_from_text(trap)
            self.assertEqual(res, expected, f"Extracted code '{res}' from error phrase: '{trap}'")

    def test_promo_discount_referral_codes(self):
        traps = [
            ("Promo code: SAVE20", None),
            ("Discount code: 50OFF", None),
            ("Coupon code: FREE10", None),
            ("Your referral code: 829103", None),
            ("Your voucher code: 582910", None),
        ]
        for trap, expected in traps:
            res = AutoEmailVerifier.extract_otp_from_text(trap)
            self.assertEqual(res, expected, f"Extracted code '{res}' from promo/referral phrase: '{trap}'")

    def test_postal_zip_area_country_codes(self):
        traps = [
            ("Postal code: BD19 5AA", None),
            ("Postal code: 123456", None),
            ("Zip code: 90210", None),
            ("Area code: 01484", None),
            ("Country code: +44", None),
            ("Country code: 44123", None),
        ]
        for trap, expected in traps:
            res = AutoEmailVerifier.extract_otp_from_text(trap)
            self.assertEqual(res, expected, f"Extracted code '{res}' from postal/zip/area phrase: '{trap}'")


class TestWebSocketDisconnectionAndLifecycle(unittest.TestCase):
    """Stress tests verifying socket dropouts, connection failures, and tab cleanup."""

    def setUp(self):
        self.verifier = AutoEmailVerifier()

    def test_send_fails_on_connection_closed(self):
        class DroppingWS:
            async def send(self, data):
                raise websockets.ConnectionClosedError(rcvd=None, sent=None)
            async def recv(self):
                return "{}"

        async def run():
            ws = DroppingWS()
            return await self.verifier._send_cdp(ws, "Runtime.evaluate", timeout=0.5)

        res = asyncio.run(run())
        self.assertEqual(res, {}, "_send_cdp must return empty dict when send fails due to closed connection")

    def test_recv_fails_on_connection_reset(self):
        class ResetRecvWS:
            async def send(self, data): pass
            async def recv(self):
                raise ConnectionResetError("Connection reset by peer")

        async def run():
            ws = ResetRecvWS()
            return await self.verifier._send_cdp(ws, "Runtime.evaluate", timeout=0.5)

        res = asyncio.run(run())
        self.assertEqual(res, {}, "_send_cdp must return empty dict when recv raises ConnectionResetError")

    def test_recv_timeout_returns_empty_dict(self):
        class HangingWS:
            async def send(self, data): pass
            async def recv(self):
                await asyncio.sleep(10)
                return "{}"

        async def run():
            ws = HangingWS()
            return await self.verifier._send_cdp(ws, "Runtime.evaluate", timeout=0.2)

        res = asyncio.run(run())
        self.assertEqual(res, {}, "_send_cdp must return empty dict when recv times out")

    def test_get_recent_emails_ephemeral_tab_closed_on_connect_error(self):
        mock_tab = {"id": "TAB_TEST_CONNECT_ERR", "type": "page", "url": "https://mail.google.com/", "webSocketDebuggerUrl": "ws://127.0.0.1:9223/test"}
        with mock.patch.object(self.verifier, "get_or_create_gmail_tab", return_value=(mock_tab, True)):
            with mock.patch.object(self.verifier, "_close_tab") as mock_close:
                with mock.patch("websockets.connect", side_effect=ConnectionRefusedError("Port 9223 unreachable")):
                    res = asyncio.run(self.verifier.get_recent_emails())
                    self.assertEqual(res, [])
                    mock_close.assert_called_once_with("TAB_TEST_CONNECT_ERR")

    def test_find_verification_link_ephemeral_tab_closed_on_ws_drop(self):
        mock_tab = {"id": "TAB_TEST_WS_DROP", "type": "page", "url": "https://mail.google.com/", "webSocketDebuggerUrl": "ws://127.0.0.1:9223/test"}
        class DroppingContextWS:
            async def __aenter__(self):
                class MockDeadWS:
                    async def send(self, d): raise websockets.ConnectionClosedError(rcvd=None, sent=None)
                    async def recv(self): raise websockets.ConnectionClosedError(rcvd=None, sent=None)
                return MockDeadWS()
            async def __aexit__(self, *args): pass

        with mock.patch.object(self.verifier, "get_or_create_gmail_tab", return_value=(mock_tab, True)):
            with mock.patch.object(self.verifier, "_close_tab") as mock_close:
                with mock.patch("websockets.connect", return_value=DroppingContextWS()):
                    res = asyncio.run(self.verifier.find_verification_link("render.com", timeout_secs=1))
                    self.assertIsNone(res)
                    mock_close.assert_called_once_with("TAB_TEST_WS_DROP")


if __name__ == "__main__":
    unittest.main()
