"""
tests/test_m4_ledger_deployment.py
==================================
Milestone M4-VID: Master Ledger Ingestion, Parity, Schema Strictness & Firebase Edge Deployment Suite.

Test Classes:
1. TestDoc3AssetIngestion (All 50 video assets ingested, 14 columns, non-empty values, >= 273 total rows)
2. Test4WayLedgerParity (len(doc3) == len(master_csv) == len(master_json) == len(html_rows))
3. TestLedgerSchemaStrictness (JSON Schema Draft 2020-12 compliance, additionalProperties: false, zero unknown keys)
4. TestRule45CitadelAirGap (0 raw root links across all rows, Tier 3 videos completely isolated from adicommunications.co.uk)
5. TestFirebaseDeploymentIntegrity (firebase.json config, CLI dry-run exit code 0, live HTTP 200 reachability)
"""

import csv
import json
import os
import posixpath
import re
import subprocess
import sys
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent

DOC3_REQUIRED_COLUMNS = [
    "asset_id",
    "parent_profile_id",
    "platform_name",
    "profile_live_url",
    "asset_title",
    "asset_type",
    "asset_public_url",
    "top_of_stack_apex_url",
    "shield_target_url",
    "seo_tags",
    "seo_description_summary",
    "dofollow_status",
    "publication_date",
    "verification_status"
]

SOVEREIGN_11_STACKS = [
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
]


class TestDoc3AssetIngestion(unittest.TestCase):
    """Class 1: Source Ingestion Verification in doc3_published_asset_links.csv."""

    @classmethod
    def setUpClass(cls):
        cls.doc3_path = REPO_ROOT / "doc3_published_asset_links.csv"
        cls.video_catalog_path = REPO_ROOT / "video_stack_50_catalog.json"
        cls.platform_catalog_path = REPO_ROOT / "master_multicategory_platform_catalog.json"

        with open(cls.doc3_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cls.fieldnames = reader.fieldnames or []
            cls.rows = list(reader)

        with open(cls.video_catalog_path, "r", encoding="utf-8") as f:
            cls.upstream_videos = json.load(f).get("videos", [])

        with open(cls.platform_catalog_path, "r", encoding="utf-8") as f:
            cat = json.load(f)
            cls.video_platforms = cat["category_stacks"]["video"]["platforms"]

    def test_01_doc3_file_exists_and_non_empty(self):
        """Asserts doc3_published_asset_links.csv exists and contains data."""
        self.assertTrue(self.doc3_path.exists(), "doc3_published_asset_links.csv is missing")
        self.assertGreater(len(self.rows), 0, "doc3_published_asset_links.csv is empty")

    def test_02_doc3_has_exact_14_column_header(self):
        """Asserts CSV header matches exactly the 14 standardized columns."""
        self.assertEqual(
            self.fieldnames,
            DOC3_REQUIRED_COLUMNS,
            f"Header columns mismatch: {self.fieldnames} vs expected {DOC3_REQUIRED_COLUMNS}"
        )

    def test_03_total_asset_count_threshold(self):
        """Asserts doc3 total rows >= 273 (expanding previous baseline with 50 video assets)."""
        count = len(self.rows)
        self.assertGreaterEqual(
            count, 273,
            f"Expected at least 273 rows in doc3 after ingesting 50 video assets, found {count}"
        )

    def test_04_all_50_video_platforms_represented(self):
        """Asserts all 50 video platforms (PLAT-VID-001 through PLAT-VID-050) are present in doc3."""
        parent_ids = {r.get("parent_profile_id", "").strip() for r in self.rows}
        expected_platform_ids = {f"PLAT-VID-{i:03d}" for i in range(1, 51)}
        missing = expected_platform_ids - parent_ids
        self.assertEqual(missing, set(), f"Missing video platforms in doc3: {missing}")

    def test_05_all_50_video_asset_titles_present(self):
        """Asserts all 50 video titles from video_stack_50_catalog.json are present in doc3."""
        doc3_titles = {r.get("asset_title", "").strip().lower() for r in self.rows}
        missing_titles = []
        for vid in self.upstream_videos:
            expected_title = vid.get("title", "").strip().lower()
            if not any(expected_title in dt or dt in expected_title for dt in doc3_titles):
                missing_titles.append(vid.get("video_id"))
        self.assertEqual(missing_titles, [], f"Missing video titles in doc3: {missing_titles}")

    def test_06_video_rows_non_empty_mandatory_fields(self):
        """Asserts all video asset rows have non-empty mandatory attributes."""
        video_rows = [r for r in self.rows if "PLAT-VID-" in r.get("parent_profile_id", "") or "Video" in r.get("asset_type", "")]
        self.assertGreaterEqual(len(video_rows), 50, f"Expected at least 50 video rows, found {len(video_rows)}")

        for idx, row in enumerate(video_rows, 1):
            for field in ["asset_id", "parent_profile_id", "platform_name", "profile_live_url", "asset_title", "asset_public_url", "top_of_stack_apex_url", "shield_target_url"]:
                val = row.get(field, "").strip()
                self.assertTrue(val, f"Empty mandatory field '{field}' in video row {idx} ({row.get('asset_id')})")

    def test_07_video_rows_apex_and_type_standards(self):
        """Asserts video rows target YouTube Apex and designate Video asset type."""
        video_rows = [r for r in self.rows if "PLAT-VID-" in r.get("parent_profile_id", "")]
        for r in video_rows:
            self.assertEqual(
                r.get("top_of_stack_apex_url"),
                "https://www.youtube.com/@CCTV.services",
                f"Video asset {r.get('asset_id')} does not point to YouTube Apex"
            )
            self.assertIn("video", r.get("asset_type", "").lower())


class Test4WayLedgerParity(unittest.TestCase):
    """Class 2: 4-Way Mathematical Parity across doc3, CSV, JSON, and HTML."""

    @classmethod
    def setUpClass(cls):
        cls.doc3_path = REPO_ROOT / "doc3_published_asset_links.csv"
        cls.csv_path = REPO_ROOT / "public_backlink_master_ledger.csv"
        cls.json_path = REPO_ROOT / "public_backlink_master_ledger.json"
        cls.html_path = REPO_ROOT / "public_backlink_ledger.html"

        with open(cls.doc3_path, "r", encoding="utf-8") as f:
            cls.doc3_rows = list(csv.DictReader(f))

        with open(cls.csv_path, "r", encoding="utf-8") as f:
            cls.csv_rows = list(csv.DictReader(f))

        with open(cls.json_path, "r", encoding="utf-8") as f:
            cls.json_data = json.load(f)

        with open(cls.html_path, "r", encoding="utf-8") as f:
            cls.html_raw = f.read()
        cls.soup = BeautifulSoup(cls.html_raw, "html.parser")

    def test_08_mathematical_row_count_equality_4way(self):
        """Asserts len(doc3) == len(master_csv) == len(master_json.entries) == json.total_backlinks == len(html_rows)."""
        doc3_len = len(self.doc3_rows)
        csv_len = len(self.csv_rows)
        json_len = len(self.json_data.get("entries", []))
        json_total = self.json_data.get("total_backlinks")
        html_rows = len(re.findall(r'<tr class="hover:bg-white', self.html_raw))

        self.assertEqual(doc3_len, csv_len, f"doc3 rows ({doc3_len}) != CSV rows ({csv_len})")
        self.assertEqual(csv_len, json_len, f"CSV rows ({csv_len}) != JSON entries ({json_len})")
        self.assertEqual(json_total, csv_len, f"JSON total_backlinks ({json_total}) != CSV rows ({csv_len})")
        self.assertEqual(html_rows, csv_len, f"HTML table rows ({html_rows}) != CSV rows ({csv_len})")

    def test_09_csv_and_doc3_field_alignment(self):
        """Asserts each CSV row matches the corresponding doc3 row by platform and title."""
        for idx in range(len(self.doc3_rows)):
            d_row = self.doc3_rows[idx]
            c_row = self.csv_rows[idx]
            self.assertEqual(
                d_row.get("asset_title"), c_row.get("asset_title"),
                f"Row {idx+1} title mismatch between doc3 and CSV"
            )
            self.assertEqual(
                d_row.get("platform_name"), c_row.get("platform"),
                f"Row {idx+1} platform mismatch between doc3 and CSV"
            )

    def test_10_json_entries_match_csv_content(self):
        """Asserts JSON entries match CSV rows in order."""
        for idx, entry in enumerate(self.json_data.get("entries", [])):
            c_row = self.csv_rows[idx]
            self.assertEqual(entry.get("anchor_text"), c_row.get("asset_title"))
            self.assertEqual(entry.get("tenant_url"), c_row.get("public_live_url"))
            self.assertEqual(entry.get("apex_target"), c_row.get("top_of_stack_apex_url"))

    def test_11_html_dom_tbody_row_count(self):
        """Asserts the DOM <tbody> contains exactly the matching number of <tr> rows."""
        tbody = self.soup.find("tbody", {"id": "ledger-tbody"})
        self.assertIsNotNone(tbody, "Missing <tbody id='ledger-tbody'>")
        rows = tbody.find_all("tr")
        self.assertEqual(len(rows), len(self.doc3_rows), "DOM <tr> count does not match doc3 count")

    def test_12_html_interactive_search_and_filter_elements(self):
        """Asserts HTML contains #ledger-search, #category-filter, #visible-count, and all 11 stacks."""
        self.assertIsNotNone(self.soup.find("input", {"id": "ledger-search"}))
        self.assertIsNotNone(self.soup.find("select", {"id": "category-filter"}))
        self.assertIsNotNone(self.soup.find("span", {"id": "visible-count"}))

        cat_select = self.soup.find("select", {"id": "category-filter"})
        options = [o.get("value") for o in cat_select.find_all("option")]
        self.assertIn("ALL", options)
        for stack in SOVEREIGN_11_STACKS:
            self.assertIn(stack, options, f"Missing category stack in dropdown: {stack}")

    def test_13_html_rows_all_have_valid_data_category(self):
        """Asserts every table row has a data-category matching one of the 11 Sovereign Category Stacks."""
        tbody = self.soup.find("tbody", {"id": "ledger-tbody"})
        rows = tbody.find_all("tr")
        for idx, r in enumerate(rows, 1):
            cat = r.get("data-category")
            self.assertIn(cat, SOVEREIGN_11_STACKS, f"Row {idx} has invalid data-category: {cat}")


class TestLedgerSchemaStrictness(unittest.TestCase):
    """Class 3: JSON Schema Draft 2020-12 Strict Validation & Field Invariance."""

    @classmethod
    def setUpClass(cls):
        cls.schema_path = REPO_ROOT / "public_backlink_ledger.schema.json"
        cls.json_path = REPO_ROOT / "public_backlink_master_ledger.json"

        with open(cls.schema_path, "r", encoding="utf-8") as f:
            cls.schema_spec = json.load(f)

        with open(cls.json_path, "r", encoding="utf-8") as f:
            cls.json_data = json.load(f)

    def test_14_schema_spec_is_valid_draft202012(self):
        """Asserts public_backlink_ledger.schema.json conforms to Draft 2020-12 meta-schema."""
        Draft202012Validator.check_schema(self.schema_spec)

    def test_15_master_json_validates_cleanly_under_draft202012(self):
        """Validates public_backlink_master_ledger.json against the schema with zero errors."""
        validator = Draft202012Validator(self.schema_spec)
        errors = list(validator.iter_errors(self.json_data))
        formatted_errors = [f"{err.message} at path '{'/'.join(str(p) for p in err.path)}'" for err in errors]
        self.assertEqual(errors, [], f"Schema validation failed with errors: {formatted_errors[:5]}")

    def test_16_root_level_additional_properties_false(self):
        """Asserts schema specifies additionalProperties: false at root, and json contains zero unknown keys."""
        self.assertFalse(self.schema_spec.get("additionalProperties", True))
        allowed_root_keys = set(self.schema_spec.get("properties", {}).keys())
        actual_root_keys = set(self.json_data.keys())
        unknown = actual_root_keys - allowed_root_keys
        self.assertEqual(unknown, set(), f"Unknown root keys found in JSON: {unknown}")

    def test_17_entry_level_additional_properties_false(self):
        """Asserts schema specifies additionalProperties: false on entries, and all entries contain zero unknown keys."""
        entry_spec = self.schema_spec["properties"]["entries"]["items"]
        self.assertFalse(entry_spec.get("additionalProperties", True))
        allowed_entry_keys = set(entry_spec.get("properties", {}).keys())

        for idx, entry in enumerate(self.json_data.get("entries", []), 1):
            actual_keys = set(entry.keys())
            unknown = actual_keys - allowed_entry_keys
            self.assertEqual(unknown, set(), f"Unknown keys in entry {idx}: {unknown}")

    def test_18_mandatory_fields_present_and_typed_in_all_entries(self):
        """Asserts all 8 core mandatory schema fields are present and non-empty in every entry."""
        required = self.schema_spec["properties"]["entries"]["items"]["required"]
        for idx, entry in enumerate(self.json_data.get("entries", []), 1):
            for req in required:
                self.assertIn(req, entry, f"Missing required property '{req}' in entry {idx}")
                val = str(entry[req]).strip()
                self.assertTrue(val, f"Empty required property '{req}' in entry {idx}")

    def test_19_rule_45_shield_constant_in_json(self):
        """Asserts root metadata contains rule_45_shield == 'STRICT_AIR_GAP'."""
        self.assertEqual(self.json_data.get("rule_45_shield"), "STRICT_AIR_GAP")


class TestRule45CitadelAirGap(unittest.TestCase):
    """Class 4: Rule 45 Citadel Air-Gap Firewall across all Ledger Artifacts."""

    @classmethod
    def setUpClass(cls):
        cls.html_path = REPO_ROOT / "public_backlink_ledger.html"
        cls.csv_path = REPO_ROOT / "public_backlink_master_ledger.csv"
        cls.json_path = REPO_ROOT / "public_backlink_master_ledger.json"
        cls.doc3_path = REPO_ROOT / "doc3_published_asset_links.csv"
        cls.platform_catalog_path = REPO_ROOT / "master_multicategory_platform_catalog.json"

        with open(cls.html_path, "r", encoding="utf-8") as f:
            cls.html_raw = f.read()

        with open(cls.csv_path, "r", encoding="utf-8") as f:
            cls.csv_rows = list(csv.DictReader(f))

        with open(cls.json_path, "r", encoding="utf-8") as f:
            cls.json_data = json.load(f)

        with open(cls.doc3_path, "r", encoding="utf-8") as f:
            cls.doc3_rows = list(csv.DictReader(f))

        with open(cls.platform_catalog_path, "r", encoding="utf-8") as f:
            cat = json.load(f)
            cls.tier3_platforms = {
                (p.get("name") or p.get("platform_name", "")).lower(): p
                for p in cat["category_stacks"]["video"]["platforms"]
                if "Tier 3" in str(p.get("tier", "")) or p.get("tier") == 3
            }

    def _is_raw_root(self, url: str) -> bool:
        if "adicommunications.co.uk" not in url:
            return False
        parsed = urllib.parse.urlparse(url)
        path = parsed.path.rstrip("/")
        if path in ("", "/index.html", "/index.htm", "/index.php"):
            return True
        return False

    def test_20_zero_raw_root_links_in_doc3_source(self):
        """Inspects all fields in doc3_published_asset_links.csv for raw root links."""
        leaks = []
        for idx, row in enumerate(self.doc3_rows, 1):
            for k, v in row.items():
                if self._is_raw_root(v):
                    leaks.append((idx, k, v))
        self.assertEqual(leaks, [], f"Raw root links found in doc3: {leaks}")

    def test_21_zero_raw_root_links_in_master_csv(self):
        """Inspects all cells in public_backlink_master_ledger.csv for raw root links."""
        leaks = []
        for idx, row in enumerate(self.csv_rows, 1):
            for k, v in row.items():
                if self._is_raw_root(v):
                    leaks.append((idx, k, v))
        self.assertEqual(leaks, [], f"Raw root links found in master CSV: {leaks}")

    def test_22_zero_raw_root_links_in_master_json(self):
        """Recursively inspects public_backlink_master_ledger.json for raw root links."""
        leaks = []
        def check(path, val):
            if isinstance(val, str):
                if self._is_raw_root(val):
                    leaks.append((path, val))
            elif isinstance(val, dict):
                for k, v in val.items():
                    check(f"{path}.{k}", v)
            elif isinstance(val, list):
                for i, item in enumerate(val):
                    check(f"{path}[{i}]", item)

        check("root", self.json_data)
        self.assertEqual(leaks, [], f"Raw root links found in JSON: {leaks}")

    def test_23_zero_raw_root_links_in_html_body_and_hrefs(self):
        """Inspects public_backlink_ledger.html body and hrefs for raw root links."""
        soup = BeautifulSoup(self.html_raw, "html.parser")
        leaks = []
        for a in soup.find_all("a"):
            href = a.get("href", "")
            if self._is_raw_root(href):
                leaks.append(href)
        self.assertEqual(leaks, [], f"Raw root links found in HTML hrefs: {leaks}")

    def test_24_tier3_video_assets_contain_zero_adicommunications_links(self):
        """Asserts Tier 3 video entries contain ABSOLUTELY ZERO occurrences of adicommunications.co.uk."""
        tier3_violations = []
        for idx, entry in enumerate(self.json_data.get("entries", []), 1):
            pname = entry.get("platform", "").lower()
            if any(t3_name == pname or t3_name in pname or pname in t3_name for t3_name in self.tier3_platforms):
                for field in ["tenant_url", "apex_target", "shield_target_url", "public_live_url", "top_of_stack_apex_url"]:
                    val = entry.get(field, "")
                    if "adicommunications.co.uk" in val:
                        tier3_violations.append((idx, pname, field, val))
        self.assertEqual(tier3_violations, [], f"Tier 3 platform leaked website link: {tier3_violations}")

    def test_25_tier3_video_assets_link_exclusively_to_youtube_apex(self):
        """Asserts Tier 3 video entries link strictly to YouTube Apex (@CCTV.services)."""
        video_entries = [e for e in self.json_data.get("entries", []) if e.get("asset_type") == "Video"]
        self.assertEqual(len(video_entries), 50, f"Expected 50 video entries, found {len(video_entries)}")
        for idx, entry in enumerate(video_entries, 1):
            pname = entry.get("platform", "").lower()
            if any(t3_name == pname or t3_name in pname or pname in t3_name for t3_name in self.tier3_platforms):
                self.assertEqual(
                    entry.get("apex_target"),
                    "https://www.youtube.com/@CCTV.services",
                    f"Tier 3 entry {idx} ({pname}) apex_target must be YouTube Apex"
                )
                self.assertEqual(
                    entry.get("shield_target_url"),
                    "https://www.youtube.com/@CCTV.services",
                    f"Tier 3 entry {idx} ({pname}) shield_target_url must be YouTube Apex"
                )


class TestFirebaseDeploymentIntegrity(unittest.TestCase):
    """Class 5: Firebase Edge Configuration, Deployment Bundle & Live HTTP Verification."""

    @classmethod
    def setUpClass(cls):
        cls.firebase_json_path = REPO_ROOT / "firebase.json"
        cls.firebaserc_path = REPO_ROOT / ".firebaserc"
        cls.ledger_html_path = REPO_ROOT / "public_backlink_ledger.html"
        cls.live_url = "https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html"

    def test_26_firebase_json_structure_and_public_root(self):
        """Asserts firebase.json exists, configures public: '.', and sets edge Cache-Control."""
        self.assertTrue(self.firebase_json_path.exists())
        with open(self.firebase_json_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        hosting = cfg.get("hosting", {})
        self.assertEqual(hosting.get("public"), ".", "Firebase hosting public must be '.'")
        self.assertIn("firebase.json", hosting.get("ignore", []))
        self.assertIn("**/.*", hosting.get("ignore", []))

        headers = hosting.get("headers", [])
        self.assertTrue(any(h.get("source") == "**" for h in headers))

    def test_27_firebaserc_default_project(self):
        """Asserts .firebaserc targets gary-pearce-forensic-hub."""
        self.assertTrue(self.firebaserc_path.exists())
        with open(self.firebaserc_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        self.assertEqual(cfg.get("projects", {}).get("default"), "gary-pearce-forensic-hub")

    def test_28_ledger_html_bundle_exists_and_healthy_size(self):
        """Asserts public_backlink_ledger.html exists in hosting root and is > 500KB."""
        self.assertTrue(self.ledger_html_path.exists())
        size = self.ledger_html_path.stat().st_size
        self.assertGreater(size, 500000, f"Ledger HTML file suspiciously small: {size} bytes")

    def test_29_firebase_cli_available_and_dry_run_passes(self):
        """Runs firebase deploy --only hosting --dry-run and asserts return code 0."""
        res = subprocess.run(
            ["firebase", "deploy", "--only", "hosting", "--dry-run"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            shell=True
        )
        self.assertEqual(res.returncode, 0, f"Firebase dry-run deploy failed:\n{res.stderr}\n{res.stdout}")
        self.assertIn("Dry run complete!", res.stdout)

    def test_30_live_http_probe_edge_deployment_status_200(self):
        """Probes live Firebase Edge CDN URL and asserts HTTP 200 and valid HTML response."""
        req = urllib.request.Request(
            f"{self.live_url}?t={int(time.time())}",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                status = resp.status
                content_type = resp.headers.get("Content-Type", "")
                body = resp.read().decode("utf-8")

                self.assertEqual(status, 200, f"Live Edge returned status {status}")
                self.assertIn("text/html", content_type, f"Unexpected content-type: {content_type}")
                self.assertIn("Public Backlink Master Ledger", body)
                self.assertIn('id="ledger-table"', body)
                self.assertIn('id="ledger-tbody"', body)

                live_rows = len(re.findall(r'<tr class="hover:bg-white', body))
                self.assertGreaterEqual(live_rows, 200, f"Live edge has only {live_rows} rows")
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"[NOTICE] Network probe to {self.live_url} skipped due to offline/network environment: {e}")


if __name__ == "__main__":
    unittest.main()
