"""
tests/test_rule45_resilience.py
Empirical stress test harness for Rule 45 naked root anchor detection and delimiter resilience.
"""

import re
import unittest

class TestRule45DelimiterResilience(unittest.TestCase):

    def setUp(self):
        self.pattern = r"https?://(?:www\.)?adicommunications\.co\.uk/?(?:$|[?#\"'\s<>,;)\]}])"
        self.exempt = r"adicommunications\.co\.uk/(?:news|assets|feed)"

    def is_violation(self, text: str) -> bool:
        is_match = bool(re.search(self.pattern, text))
        is_exempt = bool(re.search(self.exempt, text))
        return is_match and not is_exempt

    def test_naked_roots_detected(self):
        cases = [
            "https://adicommunications.co.uk/",
            "https://adicommunications.co.uk",
            "http://adicommunications.co.uk/",
            "http://adicommunications.co.uk",
            "https://www.adicommunications.co.uk/",
            "https://www.adicommunications.co.uk",
            "https://adicommunications.co.uk?foo=bar",
            "https://adicommunications.co.uk/?utm=123",
            "https://adicommunications.co.uk#section",
            'href="https://adicommunications.co.uk"',
            "href='https://adicommunications.co.uk'",
            '<a href="https://adicommunications.co.uk/">',
            '{"url": "https://adicommunications.co.uk"}',
            "(https://adicommunications.co.uk)",
            "[ADI](https://adicommunications.co.uk)",
            "visit https://adicommunications.co.uk today",
            "see https://adicommunications.co.uk, or call",
            "url: https://adicommunications.co.uk; info",
            "link: <https://adicommunications.co.uk>",
            "array = ['https://adicommunications.co.uk']",
            "dict = {'key': 'https://adicommunications.co.uk/'}",
        ]
        for c in cases:
            self.assertTrue(self.is_violation(c), f"Failed to detect naked root violation in: {c}")

    def test_buffer_exemptions_passed(self):
        cases = [
            "https://adicommunications.co.uk/news/cctv-field-guide",
            "https://adicommunications.co.uk/news/",
            "https://adicommunications.co.uk/news",
            "https://adicommunications.co.uk/assets/images/cctv.webp",
            "https://adicommunications.co.uk/feed/rss",
            "https://www.adicommunications.co.uk/news/starlink",
        ]
        for c in cases:
            self.assertFalse(self.is_violation(c), f"False positive for valid buffer in: {c}")

if __name__ == "__main__":
    unittest.main()
