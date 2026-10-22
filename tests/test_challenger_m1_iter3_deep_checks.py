"""
tests/test_challenger_m1_iter3_deep_checks.py
Comprehensive Empirical Edge-Case Verification Suite for auto_email_verifier.py
Constructed by challenger_m1_iter3_1.

Tests 4 critical dimensions:
1. Disqualified prefix phrases isolation (postal/zip/area/country/error/referral/status codes)
   - Standalone false-positive suppression even with verification keywords
   - Multi-phrase coexistence where real OTP must be extracted while disqualified code is ignored
2. Punctuated phone number collisions (Gary Pearce 07860 244 274 variants and general UK phone numbers)
   - Bracketed '(07860) 244 274'
   - Hyphenated '07860-244-274'
   - Dotted '07860.244.274'
   - Slashed '07860/244/274'
   - International '+44 (0) 7860 244 274'
   - Coexisting phone and valid OTP
3. Valid OTPs across diverse real-world notification formats
   - Reverse patterns ('X is your verification code', 'X is your Google verification code')
   - Labeled alphanumeric and 7-digit codes ('V7042-492847', '0370019')
   - Spaced codes ('123 456', '492 847') with various phrases
   - Boundary punctuation and HTML entity wrapping
4. Real-world email simulation scenarios
"""

import unittest
from auto_email_verifier import AutoEmailVerifier


class TestDisqualifiedPrefixPhrases(unittest.TestCase):
    """Rigorous verification of disqualified prefixes: postal, zip, area, country, error, status, promo, referral."""

    def test_standalone_disqualified_codes_rejected(self):
        traps = [
            ("Postal code: 123456", None),
            ("Postal code is 987654", None),
            ("Zip code: 90210", None),
            ("Zip code is 10001", None),
            ("Area code: 01484", None),
            ("Area code is 0113", None),
            ("Country code: +44", None),
            ("Country code: 44123", None),
            ("Country code is 44123", None),
            ("Status code: 200", None),
            ("Status code 50012", None),
            ("Error code: 500123", None),
            ("Error code 40412", None),
            ("HTTP error: 404", None),
            ("HTTP error 502", None),
            ("Promo code: SAVE20", None),
            ("Promo code is WELCOME50", None),
            ("Discount code: 50OFF", None),
            ("Coupon code: FREE10", None),
            ("Voucher code: 582910", None),
            ("Referral code: 829103", None),
            ("Referral code is 654321", None),
        ]
        for text, expected in traps:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertIsNone(
                res,
                f"Disqualified prefix trapped falsely! Text: '{text}' yielded OTP: '{res}'"
            )

    def test_disqualified_codes_with_generic_verification_intent_rejected(self):
        """Even if 'verify', 'confirm', or 'code' is in the sentence, disqualified codes must be rejected."""
        traps = [
            ("Please verify your address. Postal code is 123456.", None),
            ("Please confirm your location. Zip code: 90210.", None),
            ("Please verify your server settings. Error code is 500123.", None),
            ("Please confirm your country of origin. Country code is 44123.", None),
            ("Please verify your regional phone number. Area code is 01484.", None),
            ("Your verification request encountered an issue. Error code 500123.", None),
            ("Confirm your order using discount code 50OFF now.", None),
            ("Your verification failed. Status code 50012.", None),
            ("Your account verification is complete. Referral code: 829103.", None),
        ]
        for text, expected in traps:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertIsNone(
                res,
                f"Disqualified phrase with intent keyword falsely extracted! Text: '{text}' yielded: '{res}'"
            )

    def test_disqualified_prefix_coexisting_with_valid_otp(self):
        """When a disqualified code is present alongside a genuine OTP, the genuine OTP must be extracted."""
        combos = [
            ("Your postal code is BD19 5AA. Your verification code is 849201.", "849201"),
            ("Status code 200. Your security code is 738192.", "738192"),
            ("Previous request gave error code 500123. Your new verification code is 654321.", "654321"),
            ("Your referral code is 123456. To verify your email, your OTP is 987654.", "987654"),
            ("Zip code: 90210. One-time passcode: 391820.", "391820"),
            ("Area code: 01484. Please enter confirmation PIN: 554321.", "554321"),
            ("Country code is 44123. 839201 is your verification code.", "839201"),
        ]
        for text, expected in combos:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertEqual(
                res, expected,
                f"Failed to extract valid OTP in presence of disqualified prefix! Text: '{text}' -> got '{res}'"
            )


class TestPunctuatedPhoneCollisions(unittest.TestCase):
    """Stress tests verifying all punctuated formats of Gary Pearce's phone number and UK phone numbers."""

    def test_punctuated_phone_alone_returns_none(self):
        formats = [
            "Please confirm your email. Call Gary Pearce on (07860) 244 274.",
            "Please verify your email. Contact Gary Pearce on 07860-244-274.",
            "One-time security notice: Gary Pearce 07860.244.274",
            "Your OTP service is maintained by Gary Pearce (07860) 244-274.",
            "To verify your installation, call Gary Pearce on 07860/244/274.",
            "Contact: +44 (0) 7860 244 274 for verification enquiries.",
            "Contact: +44-7860-244-274 to confirm your appointment.",
            "Direct Mobile: 07860 244274. Verify your booking.",
            "Call (07860) 244274 to verify.",
            "Call 07860-244274 to confirm.",
            "Please verify your account. Call our office on 01484 123 456.",
            "Please confirm your account. Support: 020 7946 0919.",
            "Support line: 0113-244-5678. Confirm your identity.",
        ]
        for text in formats:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertIsNone(
                res,
                f"Phone number falsely extracted as OTP '{res}' from text: '{text}'"
            )

    def test_punctuated_phone_coexisting_with_valid_otp(self):
        combos = [
            ("Call Gary Pearce on (07860) 244 274. Your verification code is 849201.", "849201"),
            ("Call Gary Pearce on 07860-244-274. Your security code is: 492 847.", "492847"),
            ("Call Gary Pearce on 07860.244.274. One-time code: 391820.", "391820"),
            ("Enquiries: 07860/244/274. Your confirmation code is: 518293.", "518293"),
            ("Contact: +44 (0) 7860 244 274. Your code is 637192.", "637192"),
            ("G-748291 is your Google verification code. Contact Gary Pearce: 07860-244-274.", "G-748291"),
            ("Support line: 020 7946 0919. Your login code is 829104.", "829104"),
            ("Questions? (07860) 244 274. 492 847 is your verification code.", "492847"),
        ]
        for text, expected in combos:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertEqual(
                res, expected,
                f"Failed to extract valid OTP when punctuated phone coexists! Text: '{text}' -> got '{res}'"
            )


class TestEmailNotificationFormats(unittest.TestCase):
    """Stress tests verifying reverse patterns, labeled codes, spaced codes, and punctuation boundaries."""

    def test_reverse_patterns(self):
        cases = [
            ("G-839201 is your Google verification code", ["G-839201", "839201"]),
            ("839 201 is your security code", ["839201"]),
            ("839201 is your verification code", ["839201"]),
            ("482910 is your authentication code", ["482910"]),
            ("381920 is your one-time passcode", ["381920"]),
            ("V-123456 is your confirmation code", ["V-123456"]),
            ("001 234 is your verification code", ["001234"]),
            ("1234-5678 is your security code", ["1234-5678", "12345678"]),
            ("987654 is your code", ["987654"]),
            ("748291 is your PIN", ["748291"]),
        ]
        for text, valid_expected in cases:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertIn(
                res, valid_expected,
                f"Reverse pattern failed for '{text}': expected one of {valid_expected}, got '{res}'"
            )

    def test_labeled_alphanumeric_and_7digit_codes(self):
        cases = [
            ("Your verification code: 829103", "829103"),
            ("Security code: 492847", "492847"),
            ("Authentication code is V7042-492847", "V7042-492847"),
            ("IBM Cloud verification code: 0370019", "0370019"),
            ("Your confirmation PIN is 48291", "48291"),
            ("Your access code is 91823", "91823"),
            ("One-time passcode: 3A7B9C", "3A7B9C"),
            ("Security code: 9F2A1B", "9F2A1B"),
        ]
        for text, expected in cases:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            self.assertEqual(res, expected, f"Labeled code failed for '{text}': got '{res}'")

    def test_spaced_codes_with_varied_templates(self):
        cases = [
            ("Your verification code is 123 456", "123456"),
            ("Please use the following verification code: 492 847", "492847"),
            ("Enter one-time passcode: 829 103 to complete login", "829103"),
            ("Security code is: 554 321", "554321"),
            ("Confirmation code: 001 234", "001234"),
            ("Your code is 492 847", "492847"),
            ("Your verification code is 1234 5678", "12345678"),
        ]
        for text, expected in cases:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            clean_res = res.replace(" ", "") if res else None
            self.assertEqual(clean_res, expected, f"Spaced code failed for '{text}': got '{res}'")

    def test_html_entities_and_bracket_boundaries(self):
        cases = [
            ("<div>Your verification code is <strong>839 201</strong></div>", "839201"),
            ("<p>Please verify: <span><b>839201</b></span></p>", "839201"),
            ("Your code is 123&nbsp;456", "123456"),
            ("Your verification code is [839201].", "839201"),
            ("Your verification code is (839201).", "839201"),
            ("Your verification code is <839201>.", "839201"),
            ("Your code is: '839201'", "839201"),
            ('Your code is: "839201"', "839201"),
            ("Your verification code is 839201.", "839201"),
            ("Your verification code is 839201, please enter it now.", "839201"),
            ("Your verification code is 839201!", "839201"),
        ]
        for text, expected in cases:
            res = AutoEmailVerifier.extract_otp_from_text(text)
            clean_res = res.replace(" ", "") if res else None
            self.assertEqual(clean_res, expected, f"HTML / bracket failed for '{text}': got '{res}'")


class TestComplexRealWorldEmailBodies(unittest.TestCase):
    """Stress tests with complete simulated email notification bodies."""

    def test_ibm_cloud_full_body_simulation(self):
        body = """
        IBM Cloud
        Hello Gary,
        Thank you for signing up for an IBM Cloud account.
        Your IBM Cloud verification code is: 0370019
        This code is valid for 10 minutes. If you did not request this, please ignore this email.
        IBM UK Limited, PO Box 41, North Harbour, Portsmouth, Hampshire, PO6 3AU.
        """
        self.assertEqual(AutoEmailVerifier.extract_otp_from_text(body), "0370019")

    def test_ibm_security_verify_alphanumeric_body(self):
        body = """
        IBM Security Verify
        Verify your identity
        Please use the following verification code:
        V7042-492847
        This code will expire in 5 minutes.
        """
        self.assertEqual(AutoEmailVerifier.extract_otp_from_text(body), "V7042-492847")

    def test_google_workspace_body(self):
        body = """
        Google Workspace
        G-492817 is your Google verification code.
        Don't share this code with anyone else.
        Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043
        """
        res = AutoEmailVerifier.extract_otp_from_text(body)
        self.assertIn(res, ["G-492817", "492817"])

    def test_adi_trade_signature_with_otp_email(self):
        body = """
        Subject: Confirm your new developer platform account
        
        Hello Gary,
        Welcome to CloudService! Please confirm your registration.
        Your one-time passcode: 718294
        
        If you experience any issues, please contact:
        Gary Pearce
        Lead Engineer, ADI Communications
        Direct Mobile: 07860 244 274
        Tel: (07860) 244 274
        Web: https://adicommunications.co.uk/news/cctv-guide
        Postal code: BD19 5AA
        Status code: 200 OK
        """
        self.assertEqual(AutoEmailVerifier.extract_otp_from_text(body), "718294")


if __name__ == "__main__":
    unittest.main()
