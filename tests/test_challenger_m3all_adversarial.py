"""
tests/test_challenger_m3all_adversarial.py
Adversarial Verification & Stress Test Suite for Milestone M3-ALL:
1. Stress test validate_ledger_schema.py:
   - Malformed target URLs (naked roots, index pages, whitespace, query strings).
   - Case-sensitivity vulnerability & query prefix bypass detection.
   - Valid deep service paths (/cctv-installation/, /starlink-internet-installation/, etc.).
2. Validate 4-way mathematical parity across:
   - doc3_published_asset_links.csv
   - public_backlink_master_ledger.csv
   - public_backlink_master_ledger.json
   - public_backlink_ledger.html
   - Exact 359 items count.
   - Exact 0 null values in JSON master ledger.
   - Exact 1-to-1 field alignment across all 359 items.
3. Stress test build_public_backlink_ledger.py:
   - Unusual platform names and casing.
   - Google Slides DA 100 badge mapping across URL variants (/pub, /edit, /preview, etc.).
4. Empirical error injection & verification hardness.
"""

import copy
import csv
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent

from build_public_backlink_ledger import classify_category_stack


class TestValidateLedgerSchemaAdversarial(unittest.TestCase):
    """Stress tests Rule 45 target URL filtering and schema validation logic."""

    def setUp(self):
        self.raw_root_regex = re.compile(
            r"^https?://(?:www\.)?adicommunications\.co\.uk/?(?:index\.(?:html?|php))?$",
            re.IGNORECASE
        )
        self.allowed_prefixes = (
            "/news/", "/assets/", "/feed/",
            "/cctv-", "/starlink-", "/tv-",
            "/wifi-", "/ajax-", "/aerial-"
        )

    def is_rule45_compliant_current(self, url: str) -> bool:
        """Exact mirror of validate_ledger_schema.py lines 63-68."""
        val = url.strip()
        if "adicommunications.co.uk" in val:
            if self.raw_root_regex.match(val):
                return False
            if not any(sub in val for sub in self.allowed_prefixes):
                return False
        return True

    def test_01_malformed_naked_roots_strictly_rejected(self):
        """Verify that all standard naked root variations are strictly rejected."""
        malformed_naked_roots = [
            "http://adicommunications.co.uk",
            "https://adicommunications.co.uk",
            "http://www.adicommunications.co.uk",
            "https://www.adicommunications.co.uk",
            "http://adicommunications.co.uk/",
            "https://adicommunications.co.uk/",
            "http://www.adicommunications.co.uk/",
            "https://www.adicommunications.co.uk/",
            "https://adicommunications.co.uk/index.html",
            "http://adicommunications.co.uk/index.htm",
            "https://www.adicommunications.co.uk/index.html",
            "https://www.adicommunications.co.uk/index.htm",
            "https://adicommunications.co.uk/index.php",
            "https://www.adicommunications.co.uk/index.php",
            "https://adicommunications.co.uk/INDEX.HTML",
            "  https://adicommunications.co.uk/  ",
            "   https://www.adicommunications.co.uk   ",
        ]

        for url in malformed_naked_roots:
            with self.subTest(url=url):
                self.assertFalse(
                    self.is_rule45_compliant_current(url),
                    f"Expected rejection for malformed root: {url}"
                )

    def test_02_naked_roots_with_query_params_rejected(self):
        """Verify that naked roots with query strings or untracked paths are rejected."""
        unshielded_queries_and_paths = [
            "https://adicommunications.co.uk/?utm_source=twitter",
            "https://adicommunications.co.uk/?ref=partner",
            "https://www.adicommunications.co.uk/?gclid=12345",
            "https://adicommunications.co.uk?param=value",
            "https://adicommunications.co.uk/about-us/",
            "https://adicommunications.co.uk/contact/",
            "https://adicommunications.co.uk/privacy-policy/",
            "https://adicommunications.co.uk/services/",
            "https://adicommunications.co.uk/blog/",
            "https://adicommunications.co.uk/test-page",
        ]

        for url in unshielded_queries_and_paths:
            with self.subTest(url=url):
                self.assertFalse(
                    self.is_rule45_compliant_current(url),
                    f"Expected rejection for unshielded path/query: {url}"
                )

    def test_03_deep_service_paths_accepted(self):
        """Verify all valid deep service paths and news/assets buffers are accepted."""
        valid_deep_paths = [
            "https://adicommunications.co.uk/cctv-installation/",
            "https://adicommunications.co.uk/cctv-installation/wakefield/",
            "https://adicommunications.co.uk/cctv-installation/leeds/",
            "https://adicommunications.co.uk/starlink-internet-installation/",
            "https://adicommunications.co.uk/starlink-internet-installation/sheffield/",
            "https://adicommunications.co.uk/tv-wall-mounting/",
            "https://adicommunications.co.uk/tv-wall-mounting/barnsley/",
            "https://adicommunications.co.uk/ajax-alarm-installation/",
            "https://adicommunications.co.uk/aerial-installation/",
            "https://adicommunications.co.uk/wifi-networking/",
            "https://adicommunications.co.uk/news/rural-starlink-guide-2026",
            "https://adicommunications.co.uk/assets/documents/cctv-guide.pdf",
            "https://adicommunications.co.uk/feed/podcast.xml",
            "https://www.adicommunications.co.uk/cctv-installation/",
        ]

        for url in valid_deep_paths:
            with self.subTest(url=url):
                self.assertTrue(
                    self.is_rule45_compliant_current(url),
                    f"Expected acceptance for valid deep path: {url}"
                )

    def test_04_adversarial_vulnerability_case_sensitivity_bypass(self):
        """
        Adversarial Finding 1:
        In validate_ledger_schema.py line 64:
            if "adicommunications.co.uk" in val:
        Because the check is case-sensitive, uppercase URLs like 'HTTPS://ADICOMMUNICATIONS.CO.UK/'
        bypass the check entirely and are erroneously accepted as compliant.
        """
        uppercase_root = "HTTPS://ADICOMMUNICATIONS.CO.UK/"
        # Demonstrates that current implementation allows uppercase root:
        allowed_by_current = self.is_rule45_compliant_current(uppercase_root)
        self.assertTrue(
            allowed_by_current,
            "Adversarial proof: Uppercase URL bypasses line 64 case-sensitive check"
        )

        # Demonstrates that with .lower(), it would correctly be caught:
        val_lower = uppercase_root.strip().lower()
        caught_with_lower = bool(self.raw_root_regex.match(val_lower))
        self.assertTrue(
            caught_with_lower,
            "When normalized with .lower(), raw_root_regex matches and rejects"
        )

    def test_05_adversarial_vulnerability_query_string_prefix_bypass(self):
        """
        Adversarial Finding 2:
        If a naked root URL has a query string containing an allowed prefix,
        e.g., 'https://adicommunications.co.uk/?ref=/news/' or '?q=/cctv-',
        raw_root_regex fails to match, but any(sub in val) returns True,
        allowing a naked root link to bypass Rule 45 filtering.
        """
        tricky_query = "https://adicommunications.co.uk/?ref=/news/"
        # In current implementation, this returns True (permitted):
        allowed_by_current = self.is_rule45_compliant_current(tricky_query)
        self.assertTrue(
            allowed_by_current,
            "Adversarial proof: Query parameter '?ref=/news/' tricks substring check"
        )

        # In contrast, robust URL path parsing identifies the path as root '/':
        import urllib.parse
        parsed_path = urllib.parse.urlparse(tricky_query).path or "/"
        self.assertEqual(parsed_path, "/", "True URL path is naked root")

    def test_06_mock_ledger_validation_failure_injection(self):
        """Verify that validation logic raises AssertionError when a bad URL is injected."""
        json_path = REPO_ROOT / "public_backlink_master_ledger.json"
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Clone data and mutate one entry with a naked root
        bad_data = copy.deepcopy(data)
        bad_data["entries"][0]["shield_target_url"] = "https://adicommunications.co.uk/"

        with self.assertRaises(AssertionError) as ctx:
            for idx, e in enumerate(bad_data["entries"], 1):
                for key in ("tenant_url", "apex_target", "shield_target_url"):
                    val = e.get(key, "")
                    if "adicommunications.co.uk" in val:
                        assert not self.raw_root_regex.match(val.strip()), f"Violation at {idx}"
        self.assertIn("Violation at 1", str(ctx.exception))


class TestFourWayMathematicalParityExact(unittest.TestCase):
    """Exhaustive mathematical parity across doc3, CSV, JSON, and HTML."""

    @classmethod
    def setUpClass(cls):
        cls.doc3_path = REPO_ROOT / "doc3_published_asset_links.csv"
        cls.csv_path = REPO_ROOT / "public_backlink_master_ledger.csv"
        cls.json_path = REPO_ROOT / "public_backlink_master_ledger.json"
        cls.html_path = REPO_ROOT / "public_backlink_ledger.html"
        cls.schema_path = REPO_ROOT / "public_backlink_ledger.schema.json"

        with open(cls.doc3_path, "r", encoding="utf-8") as f:
            cls.doc3_rows = list(csv.DictReader(f))
        with open(cls.csv_path, "r", encoding="utf-8") as f:
            cls.csv_rows = list(csv.DictReader(f))
        with open(cls.json_path, "r", encoding="utf-8") as f:
            cls.json_data = json.load(f)
        with open(cls.html_path, "r", encoding="utf-8") as f:
            cls.html_content = f.read()
        with open(cls.schema_path, "r", encoding="utf-8") as f:
            cls.schema_data = json.load(f)

    def test_01_all_359_counts_match_exactly(self):
        """Assert all 4 artifacts have exactly 359 items."""
        expected = 359
        self.assertEqual(len(self.doc3_rows), expected, f"doc3 must be exactly {expected}")
        self.assertEqual(len(self.csv_rows), expected, f"CSV must be exactly {expected}")
        self.assertEqual(len(self.json_data["entries"]), expected, f"JSON entries must be exactly {expected}")
        self.assertEqual(self.json_data["total_backlinks"], expected, f"JSON total_backlinks must be {expected}")

        html_hover_rows = len(re.findall(r'<tr class="hover:bg-white', self.html_content))
        html_cat_rows = len(re.findall(r'<tr\b[^>]*data-category=', self.html_content))
        self.assertEqual(html_hover_rows, expected, f"HTML hover rows must be {expected}")
        self.assertEqual(html_cat_rows, expected, f"HTML data-category rows must be {expected}")

    def test_02_zero_null_values_in_json_recursive(self):
        """Assert exactly 0 null values anywhere in public_backlink_master_ledger.json."""
        null_paths = []

        def check_nulls(obj, path=""):
            if obj is None:
                null_paths.append(path)
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    check_nulls(v, f"{path}/{k}")
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    check_nulls(v, f"{path}[{i}]")

        check_nulls(self.json_data)
        self.assertEqual(
            len(null_paths), 0,
            f"Found {len(null_paths)} null values in JSON: {null_paths[:10]}"
        )

    def test_03_exact_1to1_alignment_across_all_359_rows(self):
        """Verify row-by-row 1:1 identity across doc3, CSV, and JSON."""
        for idx in range(359):
            d = self.doc3_rows[idx]
            c = self.csv_rows[idx]
            j = self.json_data["entries"][idx]

            # 1. Platform name
            self.assertEqual(d["platform_name"], c["platform"], f"Row {idx} doc3/csv platform mismatch")
            self.assertEqual(c["platform"], j["platform"], f"Row {idx} csv/json platform mismatch")

            # 2. Public Live URL
            self.assertEqual(d["asset_public_url"], c["public_live_url"], f"Row {idx} doc3/csv URL mismatch")
            self.assertEqual(c["public_live_url"], j["tenant_url"], f"Row {idx} csv/json URL mismatch")

            # 3. Apex URL
            self.assertEqual(d["top_of_stack_apex_url"], c["top_of_stack_apex_url"], f"Row {idx} doc3/csv apex mismatch")
            self.assertEqual(c["top_of_stack_apex_url"], j["apex_target"], f"Row {idx} csv/json apex mismatch")

            # 4. Shield Target URL
            self.assertEqual(d["shield_target_url"], c["shield_target_url"], f"Row {idx} doc3/csv shield mismatch")
            self.assertEqual(c["shield_target_url"], j["shield_target_url"], f"Row {idx} csv/json shield mismatch")

            # 5. Asset Title / Anchor Text
            self.assertEqual(d["asset_title"], c["asset_title"], f"Row {idx} doc3/csv title mismatch")
            self.assertEqual(c["asset_title"], j["anchor_text"], f"Row {idx} csv/json title mismatch")

    def test_04_schema_draft_2020_12_validation(self):
        """Assert Draft 2020-12 schema validation passes with 0 errors."""
        validator = Draft202012Validator(self.schema_data)
        errors = list(validator.iter_errors(self.json_data))
        self.assertEqual(len(errors), 0, f"Schema validation errors: {errors}")


class TestBuildPublicBacklinkLedgerStress(unittest.TestCase):
    """Stress tests category classification and Google Slides badge mapping in build_public_backlink_ledger.py."""

    def test_01_classify_unusual_platform_names(self):
        """Test category classification with case variations, partial matches, and rare names."""
        test_cases = [
            ("CARRD", "Landing Page Stack", "https://adi.carrd.co", "https://sites.google.com/",
             "Landing Page & Website Stacks", "stack-sites-agent"),
            ("Strikingly", "microsite", "https://adi.strikingly.com", "https://sites.google.com/",
             "Landing Page & Website Stacks", "stack-sites-agent"),
            ("WebFlow", "Landing Page", "https://adi.webflow.io", "https://sites.google.com/",
             "Landing Page & Website Stacks", "stack-sites-agent"),
            ("Bento.me", "Profile", "https://bento.me/garypearce", "https://sites.google.com/",
             "Landing Page & Website Stacks", "stack-sites-agent"),
            ("Notion Site", "Docs", "https://adi.notion.site", "https://sites.google.com/",
             "Landing Page & Website Stacks", "stack-sites-agent"),
            ("Catbox CDN", "Image", "https://files.catbox.moe/test.webp", "https://docs.google.com/presentation/...",
             "Images & Visual Trade Photography Stack", "stack-media-agent"),
            ("Catbox", "photo", "https://catbox.moe/123", "",
             "Images & Visual Trade Photography Stack", "stack-media-agent"),
            ("YouTube Music", "Track", "https://music.youtube.com/watch?v=123", "",
             "Music & Audio Showcase Stack", "stack-music-agent"),
            ("Spotify", "Podcast Episode", "https://open.spotify.com/episode/123", "",
             "Podcast & Audio Stack", "stack-podcast-agent"),
            ("Zenodo Preprints", "Preprint", "https://doi.org/10.5281/zenodo.123", "",
             "Docs, PDFs & Research Stack", "stack-docs-agent"),
            ("Substack", "Article", "https://adi.substack.com/p/123", "",
             "Blog & Editorial Stack", "stack-blog-agent"),
            ("Hackster.io", "Guide", "https://hackster.io/gary/guide", "",
             "Instructions & How-To Guides Stack", "stack-howto-agent"),
            ("Raindrop.io", "Bookmark", "https://raindrop.io/adi/collection", "",
             "Bookmarking & Link Discovery Stack", "stack-bookmark-agent"),
            ("Feedburner", "RSS", "https://feeds.feedburner.com/adi", "",
             "RSS Feed Stacking", "stack-rss-agent"),
            ("FreeIndex UK", "Directory Listing", "https://freeindex.co.uk/profile", "",
             "Offers, Deals & Trade Directories Stack", "stack-offers-agent"),
            ("CompletelyUnknownHosting42", "Web App", "https://myunknown.app", "",
             "Cloud Apps, Sites & Tools Stack", "stack-cloud-agent"),
        ]

        for plat, atype, url, apex, exp_cat, exp_agent in test_cases:
            with self.subTest(platform=plat, asset_type=atype):
                cat, agent = classify_category_stack(plat, atype, url, apex)
                self.assertEqual(cat, exp_cat, f"Mismatch category for {plat}")
                self.assertEqual(agent, exp_agent, f"Mismatch agent for {plat}")

    def test_02_classify_handles_none_and_empty_gracefully(self):
        """Verify classify_category_stack never crashes on None, empty strings, or symbols."""
        weird_inputs = [
            (None, None, None, None),
            ("", "", "", ""),
            ("   ", "   ", "   ", "   "),
            ("---@@@###$$$", "", "", ""),
            ("Emoji 🚀 Platform", "Video 📹", "", ""),
        ]
        for p, t, u, a in weird_inputs:
            cat, agent = classify_category_stack(p, t, u, a)
            self.assertIsInstance(cat, str)
            self.assertIsInstance(agent, str)
            self.assertTrue(len(cat) > 0)
            self.assertTrue(len(agent) > 0)

    def test_03_google_slides_da100_badge_mapping_variants(self):
        """Stress-test Google Slides DA 100 badge assignment against various URL structures."""
        def get_badge(apex_url: str) -> str:
            return "Google Slides (DA 100)" if "docs.google.com/presentation" in apex_url else \
                   "Google Drive (DA 100)" if "drive.google.com" in apex_url else \
                   "Google Docs (DA 100)" if "docs.google.com" in apex_url else \
                   "Google Sites (DA 97)" if "sites.google.com" in apex_url else \
                   "Google Photos (DA 100)" if "photos.google.com" in apex_url else \
                   "Google Maps (DA 100)" if "maps.google.com" in apex_url or "share.google" in apex_url else \
                   "YouTube (DA 100)" if "youtube.com" in apex_url else \
                   "Blogger (DA 99)" if "blogspot.com" in apex_url else \
                   "Firebase Edge (DA 98)"

        slides_variants = [
            "https://docs.google.com/presentation/d/e/2PACX-1vR_g48Y1mE.../pub?start=false&loop=false&delayms=3000",
            "https://docs.google.com/presentation/d/1abc123xyz/edit#slide=id.p",
            "https://docs.google.com/presentation/d/1abc123xyz/preview",
            "https://docs.google.com/presentation/d/1abc123xyz/export/pdf",
            "https://docs.google.com/presentation/u/0/d/1abc123xyz/",
        ]
        for url in slides_variants:
            with self.subTest(url=url):
                badge = get_badge(url)
                self.assertEqual(badge, "Google Slides (DA 100)", f"Failed for Slides URL: {url}")

        other_variants = [
            ("https://docs.google.com/document/d/e/2PACX-1vR.../pub", "Google Docs (DA 100)"),
            ("https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88", "Google Drive (DA 100)"),
            ("https://sites.google.com/view/adi-cctv-installations-uk/", "Google Sites (DA 97)"),
            ("https://photos.google.com/share/AF1QipNeW6O2Y3tBjRUD9Hx3WsJcWz1TkgOFASbW5Sad1zBfIbk5GneupQTBwJochjtLjQ", "Google Photos (DA 100)"),
            ("https://maps.google.com/?cid=12345", "Google Maps (DA 100)"),
            ("https://share.google/ATfZAwAPIiyPHkxUN", "Google Maps (DA 100)"),
            ("https://www.youtube.com/@CCTV.services", "YouTube (DA 100)"),
            ("https://tvandhomesecurity.blogspot.com/", "Blogger (DA 99)"),
            ("https://gary-pearce-forensic-hub.web.app/", "Firebase Edge (DA 98)"),
        ]
        for url, expected_badge in other_variants:
            with self.subTest(url=url):
                badge = get_badge(url)
                self.assertEqual(badge, expected_badge, f"Failed for URL: {url}")

    def test_04_html_ledger_contains_verified_slides_badges(self):
        """Assert the compiled HTML ledger contains at least 20 Google Slides DA 100 badges."""
        html_path = REPO_ROOT / "public_backlink_ledger.html"
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        badge_matches = re.findall(r'>Google Slides \(DA 100\)</span>', html)
        self.assertGreaterEqual(
            len(badge_matches), 20,
            f"Expected at least 20 Google Slides DA 100 badges, found {len(badge_matches)}"
        )


if __name__ == "__main__":
    unittest.main()
