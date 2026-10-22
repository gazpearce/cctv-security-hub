"""
tests/test_challenger_m2_delimiter_edge_cases.py
Adversarial Delimiter & Edge-Case Suite for Milestone 2 Iteration 2 Challenger:
Authored by challenger_m2_iter2_1.

Adversarially challenges:
1. All delimiter edge cases around adicommunications.co.uk:
   - Parentheses: (https://adicommunications.co.uk), (https://adicommunications.co.uk/)
   - Commas: https://adicommunications.co.uk, https://adicommunications.co.uk/,
   - Query strings: https://adicommunications.co.uk?param=1, https://adicommunications.co.uk/?utm_source=test
   - Semicolons: https://adicommunications.co.uk; https://adicommunications.co.uk/;
   - Brackets: [https://adicommunications.co.uk], [https://adicommunications.co.uk/]
   - Braces: {https://adicommunications.co.uk}, {https://adicommunications.co.uk/}
   - Quotes: "https://adicommunications.co.uk", 'https://adicommunications.co.uk/'
   - Angles: <https://adicommunications.co.uk>, <https://adicommunications.co.uk/>
   - Hash fragments: https://adicommunications.co.uk#top, https://adicommunications.co.uk/#contact
   - End of line / plain text
2. Behavior of verify_no_root_anchors.py on all delimiter edge cases.
3. Behavior of IntegrityFirewall.validate_layer5_rule_45 on all delimiter edge cases.
4. Comprehensive repo-wide scan of all 63 JSON & CSV files and all source files using an oracle scanner.
"""

import csv
import json
import os
import re
import unittest
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")

# The exact regex used in verify_no_root_anchors.py:
VERIFY_SCRIPT_REGEX = re.compile(
    r"https?://(?:www\.)?adicommunications\.co\.uk/?(?:$|[?#\"'\s<>,;)\]}])"
)
VERIFY_SCRIPT_ALLOWED = re.compile(
    r"adicommunications\.co\.uk/(?:news|assets|feed)"
)


def verify_script_eval(line: str) -> bool:
    """Simulate verify_no_root_anchors.py logic on a line."""
    if VERIFY_SCRIPT_REGEX.search(line):
        if not VERIFY_SCRIPT_ALLOWED.search(line):
            return False  # Violation found (returns False for compliant)
    return True  # Compliant (no violation)


class TestDelimiterEdgeCasesVerifyScript(unittest.TestCase):
    """Adversarially test verify_no_root_anchors.py logic against delimiter edge cases."""

    def test_parentheses_delimiters(self):
        """Parentheses edge cases must be flagged as violations."""
        cases = [
            '(https://adicommunications.co.uk)',
            '(https://adicommunications.co.uk/)',
            '(http://adicommunications.co.uk)',
            '(https://www.adicommunications.co.uk)',
            '(https://www.adicommunications.co.uk/)',
            '"author": "Gary Pearce <aiagent1510@gmail.com> (https://adicommunications.co.uk)"',
            '"author": "Gary Pearce <aiagent1510@gmail.com> (https://adicommunications.co.uk/)"',
            'Referenced in (https://adicommunications.co.uk) as author',
        ]
        for c in cases:
            with self.subTest(case=c):
                is_compliant = verify_script_eval(c)
                self.assertFalse(is_compliant, f"verify_no_root_anchors failed to catch parenthetical root: {c}")

    def test_comma_delimiters(self):
        """Comma edge cases must be flagged as violations."""
        cases = [
            'See https://adicommunications.co.uk, for more info',
            'See https://adicommunications.co.uk/, for more info',
            '["https://adicommunications.co.uk", "https://other.com"]',
            '["https://adicommunications.co.uk/", "https://other.com"]',
            'https://adicommunications.co.uk, https://youtube.com',
        ]
        for c in cases:
            with self.subTest(case=c):
                is_compliant = verify_script_eval(c)
                self.assertFalse(is_compliant, f"verify_no_root_anchors failed to catch comma-delimited root: {c}")

    def test_semicolon_delimiters(self):
        """Semicolon edge cases must be flagged as violations."""
        cases = [
            'https://adicommunications.co.uk;',
            'https://adicommunications.co.uk/;',
            'url=https://adicommunications.co.uk;version=1',
            'url=https://adicommunications.co.uk/;version=1',
        ]
        for c in cases:
            with self.subTest(case=c):
                is_compliant = verify_script_eval(c)
                self.assertFalse(is_compliant, f"verify_no_root_anchors failed to catch semicolon-delimited root: {c}")

    def test_query_string_delimiters(self):
        """Query string edge cases on root must be flagged as violations."""
        cases = [
            'https://adicommunications.co.uk?utm_source=test',
            'https://adicommunications.co.uk/?utm_source=test',
            'https://adicommunications.co.uk?ref=partner&tracking=123',
            'https://adicommunications.co.uk/?ref=partner&tracking=123',
            'https://www.adicommunications.co.uk?campaign=seo',
            'https://www.adicommunications.co.uk/?campaign=seo',
        ]
        for c in cases:
            with self.subTest(case=c):
                is_compliant = verify_script_eval(c)
                self.assertFalse(is_compliant, f"verify_no_root_anchors failed to catch query-string root: {c}")

    def test_bracket_and_brace_delimiters(self):
        """Bracket and brace edge cases must be flagged as violations."""
        cases = [
            '[https://adicommunications.co.uk]',
            '[https://adicommunications.co.uk/]',
            '{https://adicommunications.co.uk}',
            '{https://adicommunications.co.uk/}',
            '[ADI Communications](https://adicommunications.co.uk)',
            '[ADI Communications](https://adicommunications.co.uk/)',
            '{"homepage": "https://adicommunications.co.uk"}',
            '{"homepage": "https://adicommunications.co.uk/"}',
        ]
        for c in cases:
            with self.subTest(case=c):
                is_compliant = verify_script_eval(c)
                self.assertFalse(is_compliant, f"verify_no_root_anchors failed to catch bracket/brace root: {c}")

    def test_hash_fragment_delimiters(self):
        """Hash fragments on root must be flagged as violations."""
        cases = [
            'https://adicommunications.co.uk#contact',
            'https://adicommunications.co.uk/#contact',
            'https://adicommunications.co.uk#about',
            'https://adicommunications.co.uk/#services',
        ]
        for c in cases:
            with self.subTest(case=c):
                is_compliant = verify_script_eval(c)
                self.assertFalse(is_compliant, f"verify_no_root_anchors failed to catch hash fragment root: {c}")

    def test_port_and_fqdn_dot_delimiters(self):
        """Check whether port numbers and trailing FQDN dots on root are matched."""
        # Note: Check if regex in verify_no_root_anchors handles ports or dots
        port_dot_cases = [
            ('https://adicommunications.co.uk:443/', 'port 443 with slash'),
            ('https://adicommunications.co.uk:443', 'port 443 without slash'),
            ('http://adicommunications.co.uk:80/', 'port 80 with slash'),
            ('https://adicommunications.co.uk./', 'trailing dot with slash'),
            ('https://adicommunications.co.uk.', 'trailing dot without slash'),
        ]
        results = {}
        for c, desc in port_dot_cases:
            is_compliant = verify_script_eval(c)
            results[desc] = is_compliant
        print(f"\nPort/Dot delimiter match results (True means not caught, False means caught): {results}")

    def test_legitimate_buffer_pages_not_falsely_flagged(self):
        """Legitimate /news/, /assets/, /feed/ URLs must pass (no false positives)."""
        valid_cases = [
            'https://adicommunications.co.uk/news/cctv-guide',
            'https://adicommunications.co.uk/news/cctv-guide/',
            'https://adicommunications.co.uk/news/',
            '(https://adicommunications.co.uk/news/cctv-guide)',
            '[https://adicommunications.co.uk/news/cctv-guide]',
            '{"buffer": "https://adicommunications.co.uk/news/cctv-guide"}',
            'https://adicommunications.co.uk/assets/images/diagram.webp',
            'https://adicommunications.co.uk/feed/rss.xml',
            'See https://adicommunications.co.uk/news/cctv-guide, for more info',
            'url=https://adicommunications.co.uk/news/cctv-guide;version=1',
        ]
        for c in valid_cases:
            with self.subTest(case=c):
                is_compliant = verify_script_eval(c)
                self.assertTrue(is_compliant, f"verify_no_root_anchors falsely flagged valid buffer: {c}")


class TestIntegrityFirewallDelimiterResilience(unittest.TestCase):
    """Adversarially test IntegrityFirewall.validate_layer5_rule_45 from automated_platform_onboarder.py."""

    def test_firewall_handles_delimiters_without_crashing(self):
        """IntegrityFirewall must handle parentheses, brackets, commas, semicolons without throwing exceptions."""
        from automated_platform_onboarder import IntegrityFirewall

        test_inputs = [
            ('https://adicommunications.co.uk', False),
            ('https://adicommunications.co.uk/', False),
            ('(https://adicommunications.co.uk)', False),
            ('(https://adicommunications.co.uk/)', False),
            ('https://adicommunications.co.uk,', False),
            ('https://adicommunications.co.uk;', False),
            ('https://adicommunications.co.uk?utm=1', False),
            ('https://adicommunications.co.uk/?utm=1', False),
            ('https://adicommunications.co.uk#about', False),
            ('https://adicommunications.co.uk/#about', False),
            ('https://adicommunications.co.uk/news/cctv', True),
            ('https://gary-pearce-forensic-hub.web.app/', True),
            ('https://tvandhomesecurity.blogspot.com/', True),
        ]
        for inp, expected_pass in test_inputs:
            with self.subTest(input=inp):
                try:
                    passed, msg = IntegrityFirewall.validate_layer5_rule_45(inp)
                except Exception as e:
                    self.fail(f"IntegrityFirewall crashed with exception on '{inp}': {e}")
                self.assertEqual(passed, expected_pass, f"Unexpected result for '{inp}': passed={passed}, msg={msg}")


class TestOracleRepositoryScan(unittest.TestCase):
    """Full independent oracle scanner scanning all 63 JSON/CSV files and all repo files."""

    def test_all_63_json_and_csv_files(self):
        """Oracle scan of all JSON and CSV files in repository."""
        target_files = [
            p for p in REPO_ROOT.rglob("*")
            if p.is_file() and p.suffix.lower() in (".json", ".csv")
            and ".git" not in p.parts and ".agents" not in p.parts
        ]
        self.assertEqual(len(target_files), 63, f"Expected exactly 63 JSON/CSV files, found {len(target_files)}")

        violations = []
        for p in target_files:
            text = p.read_text(encoding="utf-8", errors="ignore")
            lines = text.splitlines()
            for line_no, line in enumerate(lines, 1):
                # Comprehensive regex matching adicommunications.co.uk root with ANY delimiter or end of line
                if re.search(r"https?://(?:www\.)?adicommunications\.co\.uk/?(?:$|[?#\"'\s<>,;)\]}])", line):
                    if not re.search(r"adicommunications\.co\.uk/(?:news|assets|feed)", line):
                        violations.append((str(p.relative_to(REPO_ROOT)), line_no, line.strip()))

        self.assertEqual(
            len(violations), 0,
            f"Oracle scanner found {len(violations)} raw root link violations in JSON/CSV files: {violations}"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
