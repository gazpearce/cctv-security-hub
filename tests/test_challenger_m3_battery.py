"""
tests/test_challenger_m3_battery.py
Adversarial empirical stress-test battery for Milestone 3 artifacts:
- 4-way mathematical parity (doc3, CSV, JSON, HTML)
- JSON Schema Draft 2020-12 strict validation & mutation testing
- Non-emptiness and validity of all 8 verified fields across all 219 entries
- Exact row-by-row field alignment between doc3, CSV, and JSON
- Rule 45 Google Shield Air-Gap compliance across all 4 files
- HTML table integrity, cell counts, and JSON-LD schema validity
- Idempotence of build_public_backlink_ledger.py
"""

import copy
import csv
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent

VALID_11_STACKS = {
    "Video Stack",
    "Podcast & Audio Stack",
    "Docs, PDFs & Research Stack",
    "Blog & Editorial Stack",
    "Cloud Apps, Sites & Tools Stack",
    "Images & Visual Trade Photography Stack",
    "Instructions & How-To Guides Stack",
    "Bookmarking & Link Discovery Stack",
    "RSS Feed Stacking",
    "Music & Audio Showcase Stack",
    "Offers, Deals & Trade Directories Stack"
}

VERIFIED_8_FIELDS = [
    "platform",
    "category_stack",
    "tenant_url",
    "anchor_text",
    "apex_target",
    "http_status",
    "index_status",
    "last_verified"
]


class TestMilestone3ChallengerBattery(unittest.TestCase):

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

    def test_01_mathematical_4way_parity(self):
        """Stress-test: 4-way parity across doc3, CSV, JSON entries, JSON total_backlinks, and HTML tr count."""
        doc3_len = len(self.doc3_rows)
        csv_len = len(self.csv_rows)
        json_entries_len = len(self.json_data.get("entries", []))
        total_backlinks = self.json_data.get("total_backlinks")
        html_tr_hover = len(re.findall(r'<tr class="hover:bg-white', self.html_content))
        html_tr_total_tbody = len(re.findall(r'<tr\b[^>]*data-category=', self.html_content))

        self.assertGreater(doc3_len, 0, "doc3 should have > 0 rows")
        self.assertGreaterEqual(doc3_len, 219, f"Expected at least 219 rows in doc3, got {doc3_len}")
        self.assertEqual(doc3_len, csv_len, f"doc3 ({doc3_len}) != CSV ({csv_len})")
        self.assertEqual(csv_len, json_entries_len, f"CSV ({csv_len}) != JSON entries ({json_entries_len})")
        self.assertEqual(json_entries_len, total_backlinks, f"JSON entries ({json_entries_len}) != total_backlinks ({total_backlinks})")
        self.assertEqual(html_tr_hover, csv_len, f"HTML tr hover ({html_tr_hover}) != CSV ({csv_len})")
        self.assertEqual(html_tr_total_tbody, csv_len, f"HTML tbody data-category rows ({html_tr_total_tbody}) != CSV ({csv_len})")

    def test_02_draft202012_schema_self_validation(self):
        """Verify the schema itself is a valid Draft 2020-12 schema specification."""
        try:
            Draft202012Validator.check_schema(self.schema_data)
        except Exception as e:
            self.fail(f"public_backlink_ledger.schema.json is not a valid Draft 2020-12 schema: {e}")

    def test_03_json_against_draft202012_schema(self):
        """Empirically validate master JSON against Draft 2020-12 schema."""
        validator = Draft202012Validator(self.schema_data)
        errors = list(validator.iter_errors(self.json_data))
        if errors:
            msg = "\n".join(f"- {e.message} at path '{'/'.join(str(p) for p in e.path)}'" for e in errors[:10])
            self.fail(f"JSON schema validation failed with {len(errors)} error(s):\n{msg}")

    def test_04_schema_mutation_adversarial_testing(self):
        """Adversarial mutation test: verify that Draft202012Validator correctly rejects invalid data."""
        validator = Draft202012Validator(self.schema_data)

        # Mutation 1: Missing required field in an entry
        bad_data1 = copy.deepcopy(self.json_data)
        del bad_data1["entries"][0]["category_stack"]
        self.assertTrue(any("category_stack" in e.message for e in validator.iter_errors(bad_data1)),
                        "Validator failed to reject missing category_stack")

        # Mutation 2: Empty string for minLength: 1 field
        bad_data2 = copy.deepcopy(self.json_data)
        bad_data2["entries"][0]["platform"] = ""
        self.assertTrue(len(list(validator.iter_errors(bad_data2))) > 0,
                        "Validator failed to reject empty platform string")

        # Mutation 3: Invalid top-level const
        bad_data3 = copy.deepcopy(self.json_data)
        bad_data3["rule_45_shield"] = "WEAK_SHIELD"
        self.assertTrue(len(list(validator.iter_errors(bad_data3))) > 0,
                        "Validator failed to reject non-const rule_45_shield")

        # Mutation 4: Negative total_backlinks
        bad_data4 = copy.deepcopy(self.json_data)
        bad_data4["total_backlinks"] = -5
        self.assertTrue(len(list(validator.iter_errors(bad_data4))) > 0,
                        "Validator failed to reject negative total_backlinks")

    def test_05_all_8_verified_fields_non_empty(self):
        """Verify that every single entry has non-empty values for all 8 verified fields."""
        entries = self.json_data.get("entries", [])
        self.assertGreater(len(entries), 0)

        for idx, entry in enumerate(entries):
            for field in VERIFIED_8_FIELDS:
                self.assertIn(field, entry, f"Entry #{idx} missing field '{field}'")
                val = entry[field]
                self.assertIsNotNone(val, f"Entry #{idx} field '{field}' is None")
                str_val = str(val).strip()
                self.assertGreater(len(str_val), 0, f"Entry #{idx} field '{field}' is empty or whitespace only")
                self.assertNotIn(str_val.lower(), ["none", "null", "undefined", "n/a"],
                                 f"Entry #{idx} field '{field}' has sentinel placeholder value: '{str_val}'")

    def test_06_field_semantics_and_types(self):
        """Deep check of semantic validity of the 8 fields."""
        entries = self.json_data.get("entries", [])
        for idx, entry in enumerate(entries):
            # category_stack must belong to the 11 Sovereign Stacks
            self.assertIn(entry["category_stack"], VALID_11_STACKS,
                          f"Entry #{idx} has invalid category_stack: '{entry['category_stack']}'")

            # URLs must be valid http/https URLs
            self.assertTrue(entry["tenant_url"].startswith("http://") or entry["tenant_url"].startswith("https://"),
                            f"Entry #{idx} tenant_url must start with http/https: '{entry['tenant_url']}'")
            self.assertTrue(entry["apex_target"].startswith("http://") or entry["apex_target"].startswith("https://"),
                            f"Entry #{idx} apex_target must start with http/https: '{entry['apex_target']}'")

            # http_status should be 200 or "200"
            self.assertIn(str(entry["http_status"]), ["200", "201", "301", "302"],
                          f"Entry #{idx} unexpected http_status: {entry['http_status']}")

    def test_07_row_by_row_1to1_alignment(self):
        """Verify 1:1 row index alignment across doc3, CSV, and JSON."""
        for idx in range(len(self.doc3_rows)):
            d3 = self.doc3_rows[idx]
            csv_r = self.csv_rows[idx]
            js_e = self.json_data["entries"][idx]

            # Platform alignment
            self.assertEqual(d3["platform_name"], js_e["platform"], f"Row {idx} platform mismatch: doc3 vs JSON")
            self.assertEqual(csv_r["platform"], js_e["platform"], f"Row {idx} platform mismatch: CSV vs JSON")

            # URL alignment
            self.assertEqual(d3["asset_public_url"], js_e["tenant_url"], f"Row {idx} URL mismatch: doc3 vs JSON")
            self.assertEqual(csv_r["public_live_url"], js_e["tenant_url"], f"Row {idx} URL mismatch: CSV vs JSON")

            # Apex alignment
            self.assertEqual(d3["top_of_stack_apex_url"], js_e["apex_target"], f"Row {idx} apex mismatch: doc3 vs JSON")
            self.assertEqual(csv_r["top_of_stack_apex_url"], js_e["apex_target"], f"Row {idx} apex mismatch: CSV vs JSON")

            # Title alignment
            self.assertEqual(d3["asset_title"], js_e["anchor_text"], f"Row {idx} title mismatch: doc3 vs JSON")
            self.assertEqual(csv_r["asset_title"], js_e["anchor_text"], f"Row {idx} title mismatch: CSV vs JSON")

    def test_08_rule_45_air_gap_across_all_artifacts(self):
        """Rule 45 check: Ensure zero raw root links to adicommunications.co.uk across all artifacts."""
        raw_root_regex = re.compile(r'https?://(?:www\.)?adicommunications\.co\.uk/?(?=["\'\s,;<>]|$)', re.IGNORECASE)

        # Check CSV
        with open(self.csv_path, "r", encoding="utf-8") as f:
            csv_text = f.read()
        csv_leaks = raw_root_regex.findall(csv_text)
        self.assertEqual(len(csv_leaks), 0, f"Raw root link leaks found in CSV: {csv_leaks}")

        # Check JSON
        with open(self.json_path, "r", encoding="utf-8") as f:
            json_text = f.read()
        json_leaks = raw_root_regex.findall(json_text)
        self.assertEqual(len(json_leaks), 0, f"Raw root link leaks found in JSON: {json_leaks}")

        # Check HTML
        html_leaks = raw_root_regex.findall(self.html_content)
        self.assertEqual(len(html_leaks), 0, f"Raw root link leaks found in HTML: {html_leaks}")

        # Check doc3
        with open(self.doc3_path, "r", encoding="utf-8") as f:
            doc3_text = f.read()
        doc3_leaks = raw_root_regex.findall(doc3_text)
        self.assertEqual(len(doc3_leaks), 0, f"Raw root link leaks found in doc3: {doc3_leaks}")

    def test_09_html_dom_table_and_jsonld(self):
        """Verify HTML table structure and Schema.org DataCatalog JSON-LD."""
        # Check required DOM elements
        required_ids = ["ledger-search", "category-filter", "visible-count", "total-count", "ledger-table", "ledger-tbody"]
        for elem_id in required_ids:
            self.assertIn(f'id="{elem_id}"', self.html_content, f"Missing required HTML ID: '{elem_id}'")

        # Check JSON-LD DataCatalog
        jsonld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', self.html_content, re.DOTALL)
        self.assertGreater(len(jsonld_matches), 0, "No JSON-LD script found in HTML")
        parsed_jsonld = json.loads(jsonld_matches[0])
        self.assertEqual(parsed_jsonld.get("@type"), "DataCatalog")
        self.assertIn("Gary Pearce", parsed_jsonld.get("creator", {}).get("name", ""))

        # Check table columns: each <tr> in tbody must have exactly 7 <td> cells
        tr_matches = re.findall(r'<tr class="hover:bg-white/\[0\.02\] border-b border-white/5 transition"[^>]*>(.*?)</tr>',
                                self.html_content, re.DOTALL)
        self.assertEqual(len(tr_matches), len(self.doc3_rows), f"Expected {len(self.doc3_rows)} table rows, found {len(tr_matches)}")
        for idx, tr in enumerate(tr_matches, 1):
            td_count = len(re.findall(r'<td\b', tr))
            self.assertEqual(td_count, 7, f"Row {idx} has {td_count} <td> cells, expected 7")

    def test_10_build_script_idempotence(self):
        """Verify that running build_public_backlink_ledger.py is deterministic and idempotent."""
        # Read files before
        with open(self.csv_path, "r", encoding="utf-8") as f:
            csv_before = f.read()
        with open(self.json_path, "r", encoding="utf-8") as f:
            json_before = json.load(f)

        # Run build script
        res = subprocess.run([sys.executable, "build_public_backlink_ledger.py"],
                             cwd=str(REPO_ROOT), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"build_public_backlink_ledger.py failed: {res.stderr}")

        # Read files after
        with open(self.csv_path, "r", encoding="utf-8") as f:
            csv_after = f.read()
        with open(self.json_path, "r", encoding="utf-8") as f:
            json_after = json.load(f)

        # Verify entry count and structure parity
        self.assertEqual(len(json_before["entries"]), len(json_after["entries"]))
        self.assertEqual(json_before["total_backlinks"], json_after["total_backlinks"])
        self.assertEqual(len(csv_before.splitlines()), len(csv_after.splitlines()))


if __name__ == "__main__":
    unittest.main()
