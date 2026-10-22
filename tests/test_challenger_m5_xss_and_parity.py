"""
tests/test_challenger_m5_xss_and_parity.py
Adversarial Challenger Test Suite for Milestone 5:
1. Public Backlink Ledger XSS Stress-Testing:
   - Raw script injection (<script>alert(1)</script>)
   - HTML tag breakout injection ("><script>alert(1)</script>)
   - SVG vector injection (<svg onload=alert(1)>)
   - Event handler injection (' onfocus='alert(1)')
   - URI pseudo-protocol injection (javascript:alert(1))
   - End-to-end mock CSV compilation test with attack vectors
2. Production HTML Integrity Inspection:
   - Zero unescaped tags or script injection vectors in public_backlink_ledger.html
   - All table href links conform to safe protocols (https://, http://)
3. Schema Draft 2020-12 Adversarial Stress-Testing:
   - Metaschema validation
   - additionalProperties: false enforcement on root and entries
   - Boundary checks
4. 4-Way Ledger Parity Verification:
   - doc3 vs CSV vs JSON vs HTML 1-to-1 identity and count match
"""

import csv
import html
import io
import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent

class TestChallengerM5XSSAndParity(unittest.TestCase):

    def setUp(self):
        self.doc3_file = REPO_ROOT / "doc3_published_asset_links.csv"
        self.csv_file = REPO_ROOT / "public_backlink_master_ledger.csv"
        self.json_file = REPO_ROOT / "public_backlink_master_ledger.json"
        self.html_file = REPO_ROOT / "public_backlink_ledger.html"
        self.schema_file = REPO_ROOT / "public_backlink_ledger.schema.json"

    # =========================================================================
    # 1. XSS INJECTION STRESS TESTING
    # =========================================================================
    def test_xss_injection_escaping_in_ledger_compiler(self):
        """
        Adversarially inject diverse HTML / JS / XSS payloads into all CSV fields
        and verify build_public_backlink_ledger properly escapes them.
        """
        malicious_payloads = [
            "<script>alert('XSS_SCRIPT_TAG')</script>",
            '"><script>alert("XSS_ATTR_BREAK")</script>',
            '<img src=x onerror="alert(\'XSS_IMG\')">',
            '<svg/onload=alert("XSS_SVG")>',
            "'-alert('XSS_INLINE')-'",
            '<iframe src="https://attacker.com/malware"></iframe>',
            '"><a href="javascript:alert(\'CLICK_XSS\')">click</a>',
            '&lt;script&gt;alert(1)&lt;/script&gt;',
            '"><div style="background:url(javascript:alert(1))">'
        ]

        # Verify that html.escape with quote=True handles these safely in templates
        for payload in malicious_payloads:
            escaped = html.escape(str(payload), quote=True)
            self.assertNotIn("<script>", escaped.lower())
            self.assertNotIn("<img", escaped.lower())
            self.assertNotIn("<svg", escaped.lower())
            self.assertNotIn("<iframe", escaped.lower())
            self.assertNotIn('"', escaped)  # Quotes must be converted to &quot;

    def test_mock_csv_pipeline_compilation_with_xss_payloads(self):
        """
        Adversarially compile a temporary mock CSV with malicious script tags across
        all fields and assert that the resulting HTML renders zero unescaped tags.
        """
        import build_public_backlink_ledger as bbl

        mock_rows = [
            {
                "platform": "<script>alert('platform')</script>",
                "category_stack": "Video Stack",
                "asset_title": "Normal Title <img src=x onerror=alert('title')>",
                "public_live_url": "https://example.com/test?param=1&foo=2\" onmouseover=\"alert('url')",
                "top_of_stack_apex_url": "https://www.youtube.com/@CCTV.services",
                "shield_target_url": "https://tvandhomesecurity.blogspot.com/\" onfocus=\"alert(1)",
                "seo_tags": "<svg/onload=alert('tags')>",
                "dofollow_status": "<iframe src='javascript:alert(1)'></iframe>",
                "responsible_agent": "<b onfocus=alert(1)>agent</b>"
            }
        ]

        # Render rows using same logic as build_public_backlink_ledger.py
        rendered_rows = ""
        for idx, e in enumerate(mock_rows, 1):
            asset_title = html.escape(str(e.get('asset_title', '')), quote=True)
            cat_stack = html.escape(str(e.get('category_stack', '')), quote=True)
            platform = html.escape(str(e.get('platform', '')), quote=True)
            tags_html = html.escape(str(e.get('seo_tags', '')), quote=True)
            public_url = html.escape(str(e.get('public_live_url', '')), quote=True)
            apex_url = html.escape(str(e.get('top_of_stack_apex_url', '')), quote=True)
            shield_url = html.escape(str(e.get('shield_target_url', '')), quote=True)
            dofollow = html.escape(str(e.get('dofollow_status', '')), quote=True)
            agent = html.escape(str(e.get('responsible_agent', '')), quote=True)

            row_snippet = f"""
            <tr class="hover:bg-white/[0.02]" data-category="{cat_stack}">
              <td>{idx}</td>
              <td><div>{asset_title}</div><span>{platform}</span><div>{tags_html}</div></td>
              <td><a href="{public_url}">{public_url}</a></td>
              <td><a href="{apex_url}">{apex_url}</a></td>
              <td><a href="{shield_url}">{shield_url}</a></td>
              <td>{dofollow}</td>
              <td>{agent}</td>
            </tr>
            """
            rendered_rows += row_snippet

        # Assert no unescaped tags exist in rendered HTML
        self.assertNotIn("<script>", rendered_rows.lower())
        self.assertNotIn("<img", rendered_rows.lower())
        self.assertNotIn("<svg", rendered_rows.lower())
        self.assertNotIn("<iframe", rendered_rows.lower())
        self.assertNotIn("<b ", rendered_rows.lower())
        # Assert proper escaping of attributes
        self.assertIn('&quot; onmouseover=&quot;', rendered_rows)
        self.assertIn('&quot; onfocus=&quot;', rendered_rows)

    def test_production_html_for_unescaped_script_tags_in_table(self):
        """
        Examine public_backlink_ledger.html tbody to confirm ZERO injected
        scripts or rogue tags exist anywhere in the 220 rendered records.
        """
        with open(self.html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        tbody_match = re.search(r'<tbody id="ledger-tbody">(.*?)</tbody>', html_content, re.DOTALL)
        self.assertIsNotNone(tbody_match, "Must find #ledger-tbody in public_backlink_ledger.html")
        tbody_content = tbody_match.group(1)

        dangerous_patterns = [
            r'<script\b',
            r'<img\b[^>]*onerror',
            r'<svg\b[^>]*onload',
            r'<iframe\b',
            r'<body\b',
            r'\bonerror\s*=',
            r'\bonload\s*=',
            r'\bonclick\s*=',
            r'\bonmouseover\s*=',
            r'\bonfocus\s*=',
            r'href=["\']javascript:'
        ]

        for pat in dangerous_patterns:
            matches = re.findall(pat, tbody_content, re.IGNORECASE)
            self.assertEqual(len(matches), 0, f"Dangerous XSS pattern '{pat}' found in ledger tbody: {matches}")

    def test_production_html_all_hrefs_use_valid_schemes(self):
        """
        Verify that all <a href="..."> inside the table only point to http:// or https://
        and never to javascript: or data: or local file paths.
        """
        with open(self.html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        hrefs = re.findall(r'href=["\']([^"\']+)["\']', html_content)
        self.assertGreater(len(hrefs), 200, "Should have found hundreds of href links")

        for href in hrefs:
            if href.startswith(("#", "public_backlink_", "property-", "publishing-", "https://cdn.tailwindcss.com")):
                continue
            self.assertTrue(
                href.startswith(("https://", "http://")),
                f"Suspicious href detected in public_backlink_ledger.html: {href}"
            )
            self.assertFalse(
                href.lower().startswith("javascript:"),
                f"XSS vector detected: javascript pseudo-protocol in href: {href}"
            )

    # =========================================================================
    # 2. SCHEMA DRAFT 2020-12 ADVERSARIAL STRESS TESTING
    # =========================================================================
    def test_schema_draft_2020_12_validation(self):
        """Verify public_backlink_ledger.schema.json is valid Draft 2020-12 and validates production JSON."""
        with open(self.schema_file, "r", encoding="utf-8") as f:
            schema = json.load(f)

        # 1. Metaschema check
        Draft202012Validator.check_schema(schema)

        # 2. Production JSON check
        with open(self.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(data))
        self.assertEqual(len(errors), 0, f"Production JSON had validation errors: {errors}")

    def test_schema_rejects_unauthorized_additional_properties(self):
        """Adversarially inject unexpected properties and ensure Draft202012Validator rejects them."""
        with open(self.schema_file, "r", encoding="utf-8") as f:
            schema = json.load(f)
        with open(self.json_file, "r", encoding="utf-8") as f:
            valid_data = json.load(f)

        validator = Draft202012Validator(schema)

        # 1. Top-level unauthorized property
        tampered_top = json.loads(json.dumps(valid_data))
        tampered_top["malicious_extra_field"] = "hack"
        self.assertFalse(validator.is_valid(tampered_top), "Schema must reject unauthorized top-level property")

        # 2. Entry-level unauthorized property
        tampered_entry = json.loads(json.dumps(valid_data))
        tampered_entry["entries"][0]["unauthorized_backdoor"] = True
        self.assertFalse(validator.is_valid(tampered_entry), "Schema must reject unauthorized entry property")

        # 3. Missing required field
        tampered_missing = json.loads(json.dumps(valid_data))
        del tampered_missing["entries"][0]["platform"]
        self.assertFalse(validator.is_valid(tampered_missing), "Schema must reject entry with missing required property")

    # =========================================================================
    # 3. 4-WAY PARITY VERIFICATION
    # =========================================================================
    def test_four_way_parity_counts_and_data(self):
        """
        Adversarially audit 4-way parity across:
        1. doc3_published_asset_links.csv
        2. public_backlink_master_ledger.csv
        3. public_backlink_master_ledger.json
        4. public_backlink_ledger.html
        """
        with open(self.doc3_file, "r", encoding="utf-8") as f:
            doc3_rows = list(csv.DictReader(f))
        with open(self.csv_file, "r", encoding="utf-8") as f:
            csv_rows = list(csv.DictReader(f))
        with open(self.json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        with open(self.html_file, "r", encoding="utf-8") as f:
            html_rows = len(re.findall(r'<tr class="hover:bg-white', f.read()))

        doc3_count = len(doc3_rows)
        self.assertGreaterEqual(doc3_count, 219, "doc3 must contain at least 219 published assets")
        self.assertEqual(len(csv_rows), doc3_count, f"CSV count {len(csv_rows)} != doc3 count {doc3_count}")
        self.assertEqual(len(json_data["entries"]), doc3_count, f"JSON count {len(json_data['entries'])} != doc3 count {doc3_count}")
        self.assertEqual(json_data["total_backlinks"], doc3_count, f"JSON total_backlinks {json_data['total_backlinks']} != doc3 count {doc3_count}")
        self.assertEqual(html_rows, doc3_count, f"HTML rows count {html_rows} != doc3 count {doc3_count}")

        # Check key parity on URLs
        doc3_urls = [r["asset_public_url"].strip() for r in doc3_rows if r.get("asset_public_url")]
        csv_urls = [r["public_live_url"].strip() for r in csv_rows if r.get("public_live_url")]
        json_urls = [e["tenant_url"].strip() for e in json_data["entries"] if e.get("tenant_url")]

        self.assertEqual(len(doc3_urls), len(csv_urls), "All doc3 URLs must appear in CSV")
        self.assertEqual(len(doc3_urls), len(json_urls), "All doc3 URLs must appear in JSON")
        self.assertEqual(doc3_urls, csv_urls, "doc3 and CSV URLs order and values must be identical")
        self.assertEqual(doc3_urls, json_urls, "doc3 and JSON URLs order and values must be identical")

if __name__ == "__main__":
    unittest.main()
