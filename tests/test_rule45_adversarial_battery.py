"""
tests/test_rule45_adversarial_battery.py
Adversarial Empirical Stress Test Suite for Rule 45 Google Shield Buffer Architecture:
Tests port variations, trailing FQDN dots, embedded HTML anchors, markdown links,
query strings, fragment identifiers, and index file evasion techniques.
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from automated_platform_onboarder import IntegrityFirewall


class TestRule45AdversarialBattery(unittest.TestCase):
    """Stress tests for Rule 45 naked root link detection and evasion prevention."""

    def test_port_variations_on_naked_root(self):
        """Port variations on naked root must be strictly REJECTED (False)."""
        port_cases = [
            ("https://adicommunications.co.uk:443/", "https port 443 with slash"),
            ("https://adicommunications.co.uk:443", "https port 443 without slash"),
            ("http://adicommunications.co.uk:80/", "http port 80 with slash"),
            ("http://adicommunications.co.uk:80", "http port 80 without slash"),
            ("https://adicommunications.co.uk:8080/", "https custom port 8080 with slash"),
            ("https://adicommunications.co.uk:8080", "https custom port 8080 without slash"),
            ("https://adicommunications.co.uk:8443/", "https custom port 8443 with slash"),
            ("https://adicommunications.co.uk:8443", "https custom port 8443 without slash"),
            ("https://www.adicommunications.co.uk:443/", "www https port 443 with slash"),
            ("https://www.adicommunications.co.uk:443", "www https port 443 without slash"),
            ("http://www.adicommunications.co.uk:80/", "www http port 80 with slash"),
            ("http://www.adicommunications.co.uk:80", "www http port 80 without slash"),
        ]
        for url, desc in port_cases:
            with self.subTest(case=desc, url=url):
                passed, msg = IntegrityFirewall.validate_layer5_rule_45(url)
                self.assertFalse(passed, f"Failed to reject port variation: {desc} ({url}). Result: {msg}")

    def test_trailing_fqdn_dots_on_naked_root(self):
        """Trailing FQDN dots on naked root must be strictly REJECTED (False)."""
        dot_cases = [
            ("https://adicommunications.co.uk.", "trailing FQDN dot without slash"),
            ("https://adicommunications.co.uk./", "trailing FQDN dot with slash"),
            ("https://adicommunications.co.uk.:443/", "trailing FQDN dot + port 443 with slash"),
            ("https://adicommunications.co.uk.:443", "trailing FQDN dot + port 443 without slash"),
            ("https://www.adicommunications.co.uk.", "www trailing FQDN dot without slash"),
            ("https://www.adicommunications.co.uk./", "www trailing FQDN dot with slash"),
            ("https://www.adicommunications.co.uk.:443/", "www trailing FQDN dot + port 443 with slash"),
            ("https://www.adicommunications.co.uk.:443", "www trailing FQDN dot + port 443 without slash"),
            ("http://adicommunications.co.uk.", "http trailing FQDN dot without slash"),
            ("http://adicommunications.co.uk./", "http trailing FQDN dot with slash"),
            ("http://adicommunications.co.uk.:80/", "http trailing FQDN dot + port 80 with slash"),
            ("http://adicommunications.co.uk.:80", "http trailing FQDN dot + port 80 without slash"),
        ]
        for url, desc in dot_cases:
            with self.subTest(case=desc, url=url):
                passed, msg = IntegrityFirewall.validate_layer5_rule_45(url)
                self.assertFalse(passed, f"Failed to reject trailing FQDN dot: {desc} ({url}). Result: {msg}")

    def test_embedded_html_anchors(self):
        """Embedded HTML anchor tags containing naked root links must be strictly REJECTED (False)."""
        anchor_cases = [
            ('<a href="https://adicommunications.co.uk/">ADI</a>', "double quoted href with slash"),
            ('<a href="https://adicommunications.co.uk">ADI</a>', "double quoted href without slash"),
            ("<a href='https://adicommunications.co.uk/'>ADI</a>", "single quoted href with slash"),
            ("<a href='https://adicommunications.co.uk'>ADI</a>", "single quoted href without slash"),
            ('<a href="http://adicommunications.co.uk/">ADI</a>', "http double quoted href with slash"),
            ('<a href="http://adicommunications.co.uk">ADI</a>', "http double quoted href without slash"),
            ('<a href="https://www.adicommunications.co.uk/">ADI</a>', "www double quoted href with slash"),
            ('<a href="https://www.adicommunications.co.uk">ADI</a>', "www double quoted href without slash"),
            ('<a href="https://adicommunications.co.uk:443/">ADI</a>', "port 443 in HTML anchor"),
            ('<a href="https://adicommunications.co.uk:443">ADI</a>', "port 443 without slash in HTML anchor"),
            ('<a href="https://adicommunications.co.uk./">ADI</a>', "trailing dot in HTML anchor"),
            ('<a href="https://adicommunications.co.uk.">ADI</a>', "trailing dot without slash in HTML anchor"),
            ('<a target="_blank" href="https://adicommunications.co.uk/">ADI</a>', "target before href"),
            ('<a href="https://adicommunications.co.uk/" target="_blank" rel="noopener">ADI</a>', "target after href"),
            ("<a class=\"nav-link\" href='https://adicommunications.co.uk/'>Home</a>", "class before href"),
        ]
        for snippet, desc in anchor_cases:
            with self.subTest(case=desc, snippet=snippet):
                passed, msg = IntegrityFirewall.validate_layer5_rule_45(snippet)
                self.assertFalse(passed, f"Failed to reject HTML anchor: {desc} ({snippet}). Result: {msg}")

    def test_query_params_and_fragments_on_naked_root(self):
        """Query parameters and fragments on naked root must be strictly REJECTED (False)."""
        query_cases = [
            ("https://adicommunications.co.uk/?utm_source=twitter", "query string with slash"),
            ("https://adicommunications.co.uk?utm_source=twitter", "query string without slash"),
            ("https://adicommunications.co.uk:443/?utm_source=twitter", "port 443 with query string"),
            ("https://adicommunications.co.uk./?utm_source=twitter", "dot with query string"),
            ("https://adicommunications.co.uk/#contact", "hash fragment with slash"),
            ("https://adicommunications.co.uk#contact", "hash fragment without slash"),
            ("https://adicommunications.co.uk:443/#contact", "port 443 with fragment"),
            ("https://adicommunications.co.uk./#contact", "dot with fragment"),
        ]
        for url, desc in query_cases:
            with self.subTest(case=desc, url=url):
                passed, msg = IntegrityFirewall.validate_layer5_rule_45(url)
                self.assertFalse(passed, f"Failed to reject query/fragment on naked root: {desc} ({url}). Result: {msg}")

    def test_default_index_files_and_slash_collapse(self):
        """Default index files and slash collapses on root must be strictly REJECTED (False)."""
        index_cases = [
            ("https://adicommunications.co.uk/index.html", "index.html"),
            ("https://adicommunications.co.uk/index.htm", "index.htm"),
            ("https://adicommunications.co.uk/index.php", "index.php"),
            ("https://adicommunications.co.uk:443/index.html", "port 443 + index.html"),
            ("https://adicommunications.co.uk./index.html", "dot + index.html"),
            ("https://adicommunications.co.uk//", "double slash root"),
            ("https://adicommunications.co.uk///", "triple slash root"),
        ]
        for url, desc in index_cases:
            with self.subTest(case=desc, url=url):
                passed, msg = IntegrityFirewall.validate_layer5_rule_45(url)
                self.assertFalse(passed, f"Failed to reject index/slash collapse: {desc} ({url}). Result: {msg}")

    def test_markdown_and_plain_text_root_violations(self):
        """Markdown links and natural prose containing naked root anchors must be strictly REJECTED (False)."""
        text_cases = [
            ("[ADI Communications](https://adicommunications.co.uk/)", "markdown link with slash"),
            ("[ADI Communications](https://adicommunications.co.uk)", "markdown link without slash"),
            ("[ADI](http://adicommunications.co.uk/)", "http markdown link"),
            ("[ADI](https://adicommunications.co.uk:443/)", "port 443 markdown link"),
            ("Visit https://adicommunications.co.uk/ today for info", "prose with trailing word"),
            ("Visit https://adicommunications.co.uk today for info", "prose no slash with trailing word"),
            ("Check out https://www.adicommunications.co.uk/", "prose with www"),
        ]
        for text, desc in text_cases:
            with self.subTest(case=desc, text=text):
                passed, msg = IntegrityFirewall.validate_layer5_rule_45(text)
                self.assertFalse(passed, f"Failed to reject text/markdown root link: {desc} ({text}). Result: {msg}")

    def test_legitimate_rule45_buffer_subpages(self):
        """Legitimate editorial and service buffer subpages must be ACCEPTED (True)."""
        valid_cases = [
            ("https://adicommunications.co.uk/news/cctv-field-guide", "news buffer subpage"),
            ("https://adicommunications.co.uk:443/news/cctv-field-guide", "port 443 + news buffer"),
            ("https://adicommunications.co.uk./news/cctv-field-guide", "dot + news buffer"),
            ("https://adicommunications.co.uk/services/cctv-installation", "services subpage"),
            ("https://adicommunications.co.uk/assets/images/diagram.webp", "assets subpage"),
            ("https://adicommunications.co.uk/feed.xml", "feed XML subpath"),
            ('<a href="https://adicommunications.co.uk/news/cctv-guide">ADI Guide</a>', "HTML anchor to buffer page"),
            ("<a href='https://adicommunications.co.uk/services/starlink'>Starlink</a>", "HTML anchor single quoted to services"),
            ("[Read field notes](https://adicommunications.co.uk/news/fluke-cable-testing)", "markdown link to buffer page"),
            ("https://tvandhomesecurity.blogspot.com/", "Google Shield Blogger Hub"),
            ("https://gary-pearce-forensic-hub.web.app/", "Google Firebase Citadel Hub"),
        ]
        for item, desc in valid_cases:
            with self.subTest(case=desc, item=item):
                passed, msg = IntegrityFirewall.validate_layer5_rule_45(item)
                self.assertTrue(passed, f"Legitimate buffer page was incorrectly rejected: {desc} ({item}). Msg: {msg}")


if __name__ == "__main__":
    unittest.main()
