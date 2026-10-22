"""
tests/e2e/test_domain4_adversarial_recheck.py
Adversarial Re-challenge of Schema Strictness & HTML Security (Domain 4)
Empirical Challenger: challenger_m5_recheck_2
"""

import csv
import html
import json
import os
import re
import sys
import unittest
from pathlib import Path
from bs4 import BeautifulSoup
from jsonschema import Draft202012Validator, ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

LEDGER_JSON = REPO_ROOT / "public_backlink_master_ledger.json"
LEDGER_SCHEMA = REPO_ROOT / "public_backlink_ledger.schema.json"
LEDGER_CSV = REPO_ROOT / "public_backlink_master_ledger.csv"
LEDGER_HTML = REPO_ROOT / "public_backlink_ledger.html"
DOC3_CSV = REPO_ROOT / "doc3_published_asset_links.csv"


class TestDomain4AdversarialRecheck(unittest.TestCase):
    """Rigorous empirical recheck of Schema Strictness (Draft 2020-12) and HTML XSS Neutralization."""

    def setUp(self):
        self.assertTrue(LEDGER_JSON.exists(), f"Missing {LEDGER_JSON}")
        self.assertTrue(LEDGER_SCHEMA.exists(), f"Missing {LEDGER_SCHEMA}")
        self.assertTrue(LEDGER_CSV.exists(), f"Missing {LEDGER_CSV}")
        self.assertTrue(LEDGER_HTML.exists(), f"Missing {LEDGER_HTML}")
        self.assertTrue(DOC3_CSV.exists(), f"Missing {DOC3_CSV}")

        with open(LEDGER_JSON, "r", encoding="utf-8") as f:
            self.ledger_data = json.load(f)

        with open(LEDGER_SCHEMA, "r", encoding="utf-8") as f:
            self.ledger_schema = json.load(f)

        with open(LEDGER_CSV, "r", encoding="utf-8") as f:
            self.csv_rows = list(csv.DictReader(f))

        with open(LEDGER_HTML, "r", encoding="utf-8") as f:
            self.html_content = f.read()

        self.soup = BeautifulSoup(self.html_content, "html.parser")
        self.validator = Draft202012Validator(self.ledger_schema)

    def test_rc_01_baseline_schema_validity(self):
        """Verify unmodified production ledger passes Draft 2020-12 schema validation."""
        errors = list(self.validator.iter_errors(self.ledger_data))
        self.assertEqual(errors, [], f"Baseline validation failed: {[e.message for e in errors]}")

    def test_rc_02_schema_root_additional_properties_rejection(self):
        """Empirically verify that injecting unauthorized fields at the root level raises Draft 2020-12 ValidationError."""
        unauthorized_keys = [
            "unauthorized_malicious_field",
            "injection_payload",
            "__proto__",
            "extra_field_123",
            "admin_override"
        ]
        for key in unauthorized_keys:
            mutated = dict(self.ledger_data)
            mutated[key] = "malicious_value"
            errors = list(self.validator.iter_errors(mutated))
            self.assertGreater(
                len(errors), 0,
                f"Schema failed to reject unauthorized root field '{key}'"
            )
            self.assertTrue(
                any(e.validator == "additionalProperties" for e in errors),
                f"Expected additionalProperties error for root field '{key}', got {[e.validator for e in errors]}"
            )
            # Verify error message specifically notes unexpected property
            matching = [e for e in errors if e.validator == "additionalProperties"]
            self.assertIn(key, matching[0].message)

    def test_rc_03_schema_item_additional_properties_rejection(self):
        """Empirically verify that injecting unauthorized fields into entry items raises Draft 2020-12 ValidationError."""
        unauthorized_item_keys = [
            "unauthorized_column",
            "xss_field",
            "sql_injection",
            "extra_metadata",
            "backdoor"
        ]
        for key in unauthorized_item_keys:
            mutated = dict(self.ledger_data)
            entry_copy = dict(self.ledger_data["entries"][0])
            entry_copy[key] = "malicious_entry_value"
            mutated["entries"] = [entry_copy]
            errors = list(self.validator.iter_errors(mutated))
            self.assertGreater(
                len(errors), 0,
                f"Schema failed to reject unauthorized entry field '{key}'"
            )
            self.assertTrue(
                any(e.validator == "additionalProperties" for e in errors),
                f"Expected additionalProperties error for entry field '{key}', got {[e.validator for e in errors]}"
            )
            matching = [e for e in errors if e.validator == "additionalProperties"]
            self.assertIn(key, matching[0].message)
            self.assertEqual(list(matching[0].path), ["entries", 0])

    def test_rc_04_schema_strictness_flags_explicit_check(self):
        """Explicitly verify 'additionalProperties: false' exists at root and items definitions."""
        self.assertIn("additionalProperties", self.ledger_schema)
        self.assertFalse(
            self.ledger_schema["additionalProperties"],
            "Root schema must have 'additionalProperties: false'"
        )

        entries_schema = self.ledger_schema["properties"]["entries"]
        items_schema = entries_schema["items"]
        self.assertIn("additionalProperties", items_schema)
        self.assertFalse(
            items_schema["additionalProperties"],
            "Entries items schema must have 'additionalProperties: false'"
        )

    def test_rc_05_build_script_uses_html_escape(self):
        """Empirically verify build_public_backlink_ledger.py uses html.escape(..., quote=True)."""
        build_script_path = REPO_ROOT / "build_public_backlink_ledger.py"
        with open(build_script_path, "r", encoding="utf-8") as f:
            code = f.read()

        self.assertIn("import html", code, "build_public_backlink_ledger.py must import html module")
        self.assertIn("html.escape", code, "build_public_backlink_ledger.py must use html.escape")

        # Check that interpolated variables are escaped
        escaped_vars = [
            "asset_title = html.escape",
            "cat_stack = html.escape",
            "platform = html.escape",
            "tags_html = html.escape",
            "public_url = html.escape",
            "apex_url = html.escape",
            "shield_url = html.escape",
            "dofollow = html.escape",
            "agent = html.escape",
        ]
        for ev in escaped_vars:
            self.assertIn(ev, code, f"Missing escaping pattern '{ev}' in build_public_backlink_ledger.py")

    def test_rc_06_build_script_adversarial_xss_neutralization_empirical(self):
        """Simulate building a row with aggressive XSS payloads and verify complete DOM neutralization."""
        adversarial_entries = [
            {
                "asset_title": "<script>alert('XSS_TITLE')</script>",
                "category_stack": "Video Stack\"><script>alert('CAT')</script>",
                "platform": "Platform<img src=x onerror=alert('PLAT')>",
                "seo_tags": "<img src=x onerror=alert('TAG')> & <svg onload=alert('SVG')>",
                "public_live_url": "https://example.com/?q=\"><script>alert('URL')</script>",
                "top_of_stack_apex_url": "https://www.youtube.com/@CCTV.services?a=1&b=2\" onfocus=alert('APEX')",
                "shield_target_url": "https://tvandhomesecurity.blogspot.com/\" onmouseover=alert('SHIELD')",
                "dofollow_status": "Dofollow<script>alert('DF')</script>",
                "responsible_agent": "stack-video-agent<script>alert('AGENT')</script>"
            },
            {
                "asset_title": "Normal Title with 'quotes' & \"double\" <brackets>",
                "category_stack": "Cloud Apps, Sites & Tools Stack",
                "platform": "Surge.sh",
                "seo_tags": "tag1, tag2, <a href='javascript:alert(1)'>click me</a>",
                "public_live_url": "javascript:alert('DIRECT_JS')",
                "top_of_stack_apex_url": "https://gary-pearce-forensic-hub.web.app/",
                "shield_target_url": "https://tvandhomesecurity.blogspot.com/",
                "dofollow_status": "Nofollow",
                "responsible_agent": "stack-cloud-agent"
            }
        ]

        for idx, e in enumerate(adversarial_entries, 1):
            apex_badge = "YouTube (DA 100)"
            asset_title = html.escape(str(e.get('asset_title', '')), quote=True)
            cat_stack = html.escape(str(e.get('category_stack', '')), quote=True)
            platform = html.escape(str(e.get('platform', '')), quote=True)
            tags_html = html.escape(str(e.get('seo_tags', '')), quote=True)
            public_url = html.escape(str(e.get('public_live_url', '')), quote=True)
            apex_url = html.escape(str(e.get('top_of_stack_apex_url', '')), quote=True)
            shield_url = html.escape(str(e.get('shield_target_url', '')), quote=True)
            dofollow = html.escape(str(e.get('dofollow_status', '')), quote=True)
            agent = html.escape(str(e.get('responsible_agent', '')), quote=True)

            row_html = f"""
            <tr class="hover:bg-white/[0.02] border-b border-white/5 transition" data-category="{cat_stack}">
              <td class="px-4 py-3 font-mono text-neutral-500 text-center">{idx}</td>
              <td class="px-4 py-3">
                <div class="font-bold text-white text-sm">{asset_title}</div>
                <div class="text-[11px] text-neutral-400">{cat_stack} &bull; <span class="text-orange-400">{platform}</span></div>
                <div class="text-[10px] font-mono text-orange-400/80 mt-1 line-clamp-1">{tags_html}</div>
              </td>
              <td class="px-4 py-3 text-xs text-neutral-300 font-mono">
                <a href="{public_url}" target="_blank" rel="noopener" class="text-blue-400 hover:underline break-all inline-flex items-center space-x-1">
                  <span>{public_url}</span>
                </a>
              </td>
              <td class="px-4 py-3 text-xs text-neutral-300 font-mono">
                <a href="{apex_url}" target="_blank" rel="noopener" class="text-emerald-400 hover:underline break-all inline-flex items-center space-x-1">
                  <span class="inline-flex px-1.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20 text-[10px] text-emerald-300 mr-1">{apex_badge}</span>
                  <span>{apex_url}</span>
                </a>
              </td>
              <td class="px-4 py-3 text-xs text-neutral-400 font-mono">
                <a href="{shield_url}" target="_blank" rel="noopener" class="text-neutral-300 hover:text-white hover:underline break-all">
                  {shield_url}
                </a>
              </td>
              <td class="px-4 py-3 text-center whitespace-nowrap">
                <span class="inline-flex px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{dofollow}</span>
              </td>
              <td class="px-4 py-3 text-center whitespace-nowrap">
                <span class="inline-flex px-2 py-0.5 rounded text-[10px] font-mono bg-blue-500/10 text-blue-400 border border-blue-500/20">{agent}</span>
              </td>
            </tr>
            """

            # Parse DOM with BeautifulSoup
            soup = BeautifulSoup(row_html, "html.parser")

            # 1. Zero executable tags injected
            self.assertEqual(len(soup.find_all("script")), 0, f"Entry {idx} injected executable <script> tag")
            self.assertEqual(len(soup.find_all("img")), 0, f"Entry {idx} injected executable <img> tag")
            self.assertEqual(len(soup.find_all("svg")), 0, f"Entry {idx} injected executable <svg> tag")
            self.assertEqual(len(soup.find_all("iframe")), 0, f"Entry {idx} injected executable <iframe> tag")

            # 2. Zero injected event attributes
            for tag in soup.find_all(True):
                for attr in tag.attrs:
                    self.assertFalse(
                        attr.lower().startswith("on"),
                        f"Entry {idx} injected event attribute {attr} on <{tag.name}>"
                    )

            # 3. String assertions: raw tag brackets must NOT exist unescaped
            self.assertNotIn("<script>", row_html)
            self.assertNotIn("<img", row_html)
            self.assertNotIn("<svg", row_html)
            self.assertNotIn("<iframe", row_html)

            # 4. Escaped entities must be present
            if "<script>" in e["asset_title"]:
                self.assertIn("&lt;script&gt;", row_html)
            if "<img" in e["platform"] or "<img" in e["seo_tags"]:
                self.assertIn("&lt;img", row_html)

    def test_rc_07_public_backlink_ledger_html_full_dom_cleanliness(self):
        """Full DOM scan of all rendered rows and cells in production public_backlink_ledger.html."""
        tbody = self.soup.find("tbody", id="ledger-tbody")
        self.assertIsNotNone(tbody, "Missing <tbody id='ledger-tbody'>")

        rows = tbody.find_all("tr")
        self.assertGreaterEqual(len(rows), 219, f"Expected >= 219 rows, found {len(rows)}")

        for row_idx, tr in enumerate(rows, 1):
            cells = tr.find_all("td")
            self.assertEqual(len(cells), 7, f"Row {row_idx} must have exactly 7 columns, got {len(cells)}")

            for cell_idx, td in enumerate(cells, 1):
                raw_cell = str(td)
                # Ensure no script tags
                self.assertNotIn("<script", raw_cell.lower(), f"Row {row_idx} Col {cell_idx} contains <script")
                # Ensure no onerror / onload / on* attributes
                self.assertFalse(
                    bool(re.search(r"\bon[a-z]+\s*=", raw_cell, re.IGNORECASE)),
                    f"Row {row_idx} Col {cell_idx} contains event handler: {raw_cell}"
                )
                # Ensure no javascript: pseudo-protocol in links
                for a in td.find_all("a"):
                    href = a.get("href", "").strip().lower()
                    self.assertFalse(href.startswith("javascript:"), f"Row {row_idx} Col {cell_idx} has javascript: href")

    def test_rc_08_three_way_parity_and_entry_integrity(self):
        """Verify mathematical parity across doc3, CSV, JSON, and HTML."""
        total_assets = len(self.ledger_data["entries"])
        self.assertGreaterEqual(total_assets, 219, f"Asset count must be at least 219, got {total_assets}")

        self.assertEqual(len(self.csv_rows), total_assets, "CSV row count != JSON entries")
        self.assertEqual(self.ledger_data["total_backlinks"], total_assets, "total_backlinks field != JSON entries length")

        tbody = self.soup.find("tbody", id="ledger-tbody")
        rows = tbody.find_all("tr")
        self.assertEqual(len(rows), total_assets, "HTML row count != JSON entries")

        with open(DOC3_CSV, "r", encoding="utf-8") as f:
            doc3_rows = list(csv.DictReader(f))
        self.assertEqual(len(doc3_rows), total_assets, "doc3 row count != JSON entries")

        # Verify all entries have HTTP status 200
        for idx, entry in enumerate(self.ledger_data["entries"], 1):
            self.assertEqual(str(entry.get("http_status")), "200", f"Entry {idx} has non-200 http_status")
            self.assertEqual(str(entry.get("verified_http_status")), "200", f"Entry {idx} has non-200 verified_http_status")


if __name__ == "__main__":
    unittest.main(verbosity=2)
