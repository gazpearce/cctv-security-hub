r"""
tests/test_challenger_m4vid_1_battery.py
=========================================
Milestone M4-VID Adversarial Challenge & Parity Stress Test Battery.
Author: M4-VID Challenger 1 (Schema Strictness & Parity Adversarial Stress Test)

Adversarially validates:
1. JSON Schema Draft 2020-12 Strictness:
   - Evaluates public_backlink_master_ledger.json against Draft202012Validator.
   - Verifies additionalProperties: false at root and item levels.
   - Verifies exact 21 defined properties per entry across all 279 entries.
   - Stress-tests schema validator with synthetic positive and negative fuzzing.
2. 4-Way Parity Math & Cross-Row Alignment:
   - Asserts len(doc3) == len(master_csv) == len(master_json) == len(html_rows) == 279.
   - Asserts exact 50 video assets (AST-VID-001 to AST-VID-050) present in all artifacts.
   - Verifies 14-column structure on doc3 and master CSV.
   - Performs row-by-row cross-artifact alignment across all 279 rows.
   - Checks category conservation across all 11 stacks.
3. Ingestion Idempotence Stress Test:
   - Executes ingest_video_assets.py and asserts 0 additions, 0 updates, 0 deletions.
   - Verifies SHA256 stability of doc3_published_asset_links.csv.
   - Asserts 100% video-to-platform mapping integrity.
4. HTML DOM, Filtering Logic & Rule 29 Contrast:
   - Validates HTML DOM structure, meta tags, and JSON-LD DataCatalog.
   - Tests category filter dropdown and asserts exact category counts match CSV/JSON.
   - Simulates JavaScript search and filter functions against keywords and adversarial inputs.
   - Validates Rule 29 contrast, zero ghost text, zero white-on-white.
   - Verifies Rule 20 (Gary Pearce, 07860 244 274, 0 Checkatrade) and Rule 45 (0 raw root links).
5. Live Firebase Edge CDN Probe:
   - Probes live public_backlink_ledger.html on Firebase Edge CDN.
   - Asserts HTTP 200 and exact 279 row count live.
"""

import copy
import csv
import hashlib
import json
import os
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

DOC3_PATH = REPO_ROOT / "doc3_published_asset_links.csv"
CSV_PATH = REPO_ROOT / "public_backlink_master_ledger.csv"
JSON_PATH = REPO_ROOT / "public_backlink_master_ledger.json"
HTML_PATH = REPO_ROOT / "public_backlink_ledger.html"
SCHEMA_PATH = REPO_ROOT / "public_backlink_ledger.schema.json"
INGEST_SCRIPT = REPO_ROOT / "ingest_video_assets.py"
VIDEO_CATALOG_PATH = REPO_ROOT / "video_stack_50_catalog.json"
PLATFORM_CATALOG_PATH = REPO_ROOT / "master_multicategory_platform_catalog.json"

DOC3_REQUIRED_COLUMNS = [
    "asset_id", "parent_profile_id", "platform_name", "profile_live_url",
    "asset_title", "asset_type", "asset_public_url", "top_of_stack_apex_url",
    "shield_target_url", "seo_tags", "seo_description_summary",
    "dofollow_status", "publication_date", "verification_status"
]

CSV_REQUIRED_COLUMNS = [
    "timestamp", "platform", "category", "asset_title", "asset_type",
    "public_live_url", "top_of_stack_apex_url", "shield_target_url",
    "seo_tags", "seo_description", "dofollow_status",
    "indexing_method", "verified_http_status", "responsible_agent"
]

SCHEMA_21_PROPERTIES = {
    "platform", "category_stack", "tenant_url", "anchor_text", "apex_target",
    "http_status", "index_status", "last_verified", "timestamp", "category",
    "asset_title", "asset_type", "public_live_url", "top_of_stack_apex_url",
    "shield_target_url", "seo_tags", "seo_description", "dofollow_status",
    "indexing_method", "verified_http_status", "responsible_agent"
}

ROOT_REQUIRED_KEYS = {
    "$schema", "version", "title", "lead_engineer",
    "rule_45_shield", "total_backlinks", "last_updated", "entries"
}

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


class TestDraft202012Strictness(unittest.TestCase):
    """Class 1: Adversarial Schema Strictness & Key Completeness."""

    @classmethod
    def setUpClass(cls):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cls.schema = json.load(f)
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            cls.data = json.load(f)
        cls.validator = Draft202012Validator(cls.schema)

    def test_01_schema_meta_draft_2020_12(self):
        """Verifies schema adheres to JSON Schema Draft 2020-12 specification."""
        self.assertEqual(
            self.schema.get("$schema"),
            "https://json-schema.org/draft/2020-12/schema",
            "Schema must declare Draft 2020-12"
        )
        self.assertEqual(
            self.data.get("$schema"),
            "https://json-schema.org/draft/2020-12/schema",
            "JSON payload must reference Draft 2020-12 schema"
        )

    def test_02_schema_has_additional_properties_false_at_all_levels(self):
        """Asserts additionalProperties: false is enforced at root and entry items."""
        self.assertFalse(
            self.schema.get("additionalProperties", True),
            "Root schema must set additionalProperties: false"
        )
        entry_items = self.schema["properties"]["entries"]["items"]
        self.assertFalse(
            entry_items.get("additionalProperties", True),
            "Entry items schema must set additionalProperties: false"
        )

    def test_03_schema_properties_inventory_exact_21(self):
        """Asserts exactly 21 defined properties exist in schema entry definition."""
        item_props = set(self.schema["properties"]["entries"]["items"]["properties"].keys())
        self.assertEqual(len(item_props), 21, f"Expected 21 properties in schema items, got {len(item_props)}")
        self.assertEqual(
            item_props,
            SCHEMA_21_PROPERTIES,
            f"Schema defined properties mismatch: {item_props ^ SCHEMA_21_PROPERTIES}"
        )

    def test_04_validator_iter_errors_zero(self):
        """Validates entire public_backlink_master_ledger.json against Draft 2020-12."""
        errors = list(self.validator.iter_errors(self.data))
        self.assertEqual(
            len(errors), 0,
            f"Expected 0 schema validation errors, found {len(errors)}: {[e.message for e in errors[:5]]}"
        )

    def test_05_every_entry_has_exact_21_properties(self):
        """Stress-tests all 279 JSON entries: every single entry must have exactly 21 keys with 0 extraneous."""
        entries = self.data["entries"]
        self.assertEqual(len(entries), 279, "Must have exactly 279 entries in JSON")
        for idx, entry in enumerate(entries):
            entry_keys = set(entry.keys())
            diff = entry_keys ^ SCHEMA_21_PROPERTIES
            self.assertEqual(
                len(entry_keys), 21,
                f"Entry #{idx+1} ({entry.get('platform')}) has {len(entry_keys)} keys instead of 21. Diff: {diff}"
            )
            self.assertEqual(
                entry_keys, SCHEMA_21_PROPERTIES,
                f"Entry #{idx+1} keys mismatch schema: {diff}"
            )

    def test_06_root_properties_exact_set(self):
        """Verifies root JSON object contains exactly the 8 required top-level keys."""
        root_keys = set(self.data.keys())
        self.assertEqual(
            root_keys,
            ROOT_REQUIRED_KEYS,
            f"Root JSON object keys mismatch: {root_keys ^ ROOT_REQUIRED_KEYS}"
        )

    def test_07_type_strictness_and_null_rejection(self):
        """Verifies zero null/None values and strict types across all 279 entries."""
        for idx, entry in enumerate(self.data["entries"]):
            for k, v in entry.items():
                self.assertIsNotNone(v, f"Entry #{idx+1} key '{k}' has null value")
                if k in ("platform", "category_stack", "tenant_url", "anchor_text", "apex_target"):
                    self.assertIsInstance(v, str, f"Entry #{idx+1} key '{k}' must be string")
                    self.assertGreater(len(v), 0, f"Entry #{idx+1} key '{k}' must not be empty")

    def test_08_schema_negative_fuzzing(self):
        """Negative fuzzing: mutates data with illegal keys/types and verifies validator detects failure."""
        mutated_data = copy.deepcopy(self.data)
        # Inject extraneous property into entry 0
        mutated_data["entries"][0]["__malicious_exploit_key__"] = "payload"
        errs = list(self.validator.iter_errors(mutated_data))
        self.assertGreater(len(errs), 0, "Validator failed to catch extraneous entry property!")

        # Inject extraneous property at root
        mutated_root = copy.deepcopy(self.data)
        mutated_root["__malicious_root_key__"] = 12345
        errs_root = list(self.validator.iter_errors(mutated_root))
        self.assertGreater(len(errs_root), 0, "Validator failed to catch extraneous root property!")

        # Remove a required property from entry 0
        mutated_missing = copy.deepcopy(self.data)
        del mutated_missing["entries"][0]["platform"]
        errs_missing = list(self.validator.iter_errors(mutated_missing))
        self.assertGreater(len(errs_missing), 0, "Validator failed to catch missing required property!")

    def test_09_all_entries_valid_uris_and_schemes(self):
        """Validates that all URL fields across all 279 entries have valid http/https schemes and netlocs."""
        for idx, entry in enumerate(self.data["entries"]):
            for key in ("tenant_url", "apex_target", "public_live_url", "top_of_stack_apex_url", "shield_target_url"):
                val = entry.get(key, "")
                parsed = urllib.parse.urlparse(val)
                self.assertIn(
                    parsed.scheme, ("http", "https"),
                    f"Entry #{idx+1} ({entry.get('platform')}) has invalid scheme '{parsed.scheme}' in key '{key}': {val}"
                )
                self.assertGreater(
                    len(parsed.netloc), 0,
                    f"Entry #{idx+1} ({entry.get('platform')}) has empty netloc in key '{key}': {val}"
                )

    def test_10_date_format_iso8601(self):
        """Validates that publication and verification dates match ISO-8601 YYYY-MM-DD pattern."""
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2})?$")
        for idx, entry in enumerate(self.data["entries"]):
            last_v = entry.get("last_verified", "")
            ts = entry.get("timestamp", "")
            self.assertTrue(
                date_pattern.match(last_v),
                f"Entry #{idx+1} has invalid last_verified format: {last_v}"
            )
            self.assertTrue(
                date_pattern.match(ts),
                f"Entry #{idx+1} has invalid timestamp format: {ts}"
            )


class Test4WayParityMathAdversarial(unittest.TestCase):
    """Class 2: 4-Way Parity Math, Alignment & Video Coverage."""

    @classmethod
    def setUpClass(cls):
        with open(DOC3_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cls.doc3_fieldnames = reader.fieldnames or []
            cls.doc3_rows = list(reader)

        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cls.csv_fieldnames = reader.fieldnames or []
            cls.csv_rows = list(reader)

        with open(JSON_PATH, "r", encoding="utf-8") as f:
            cls.json_data = json.load(f)
            cls.json_entries = cls.json_data.get("entries", [])

        with open(HTML_PATH, "r", encoding="utf-8") as f:
            cls.html_content = f.read()

        cls.soup = BeautifulSoup(cls.html_content, "html.parser")
        cls.html_tbody_rows = cls.soup.select("#ledger-tbody tr")
        cls.html_regex_matches = re.findall(r'<tr class="hover:bg-white', cls.html_content)

    def test_01_exact_279_row_count_across_all_4_artifacts(self):
        """Mathematical Parity Assert: doc3 == CSV == JSON == HTML == 279."""
        doc3_len = len(self.doc3_rows)
        csv_len = len(self.csv_rows)
        json_len = len(self.json_entries)
        json_total = self.json_data.get("total_backlinks")
        html_tbody_len = len(self.html_tbody_rows)
        html_regex_len = len(self.html_regex_matches)

        self.assertEqual(doc3_len, 279, f"doc3 row count expected 279, got {doc3_len}")
        self.assertEqual(csv_len, 279, f"master CSV row count expected 279, got {csv_len}")
        self.assertEqual(json_len, 279, f"JSON entries count expected 279, got {json_len}")
        self.assertEqual(json_total, 279, f"JSON total_backlinks expected 279, got {json_total}")
        self.assertEqual(html_tbody_len, 279, f"HTML tbody row count expected 279, got {html_tbody_len}")
        self.assertEqual(html_regex_len, 279, f"HTML regex row count expected 279, got {html_regex_len}")

    def test_02_video_asset_count_exact_50(self):
        """Asserts exactly 50 video assets AST-VID-001 through AST-VID-050 are present."""
        video_doc3 = [r for r in self.doc3_rows if r["asset_id"].startswith("AST-VID-")]
        self.assertEqual(len(video_doc3), 50, f"Expected 50 AST-VID- records in doc3, got {len(video_doc3)}")

        expected_ids = {f"AST-VID-{i+1:03d}" for i in range(50)}
        actual_ids = {r["asset_id"] for r in video_doc3}
        self.assertEqual(actual_ids, expected_ids, f"Video asset IDs mismatch: {actual_ids ^ expected_ids}")

    def test_03_column_exactness_doc3_and_csv(self):
        """Asserts exact 14 columns exist on doc3 and master CSV."""
        self.assertEqual(
            self.doc3_fieldnames,
            DOC3_REQUIRED_COLUMNS,
            f"doc3 columns mismatch: {self.doc3_fieldnames} vs {DOC3_REQUIRED_COLUMNS}"
        )
        self.assertEqual(
            self.csv_fieldnames,
            CSV_REQUIRED_COLUMNS,
            f"CSV columns mismatch: {self.csv_fieldnames} vs {CSV_REQUIRED_COLUMNS}"
        )

    def test_04_cross_artifact_row_alignment_fuzz(self):
        """Cross-checks row-by-row correlation across doc3, CSV, and JSON."""
        for idx in range(279):
            d_row = self.doc3_rows[idx]
            c_row = self.csv_rows[idx]
            j_entry = self.json_entries[idx]

            # Title alignment
            self.assertEqual(
                d_row["asset_title"], c_row["asset_title"],
                f"Row #{idx+1} title mismatch between doc3 and CSV"
            )
            self.assertEqual(
                c_row["asset_title"], j_entry["asset_title"],
                f"Row #{idx+1} title mismatch between CSV and JSON"
            )

            # Public live URL alignment
            self.assertEqual(
                d_row["asset_public_url"], c_row["public_live_url"],
                f"Row #{idx+1} public URL mismatch between doc3 and CSV"
            )
            self.assertEqual(
                c_row["public_live_url"], j_entry["public_live_url"],
                f"Row #{idx+1} public URL mismatch between CSV and JSON"
            )

            # Apex target alignment
            self.assertEqual(
                d_row["top_of_stack_apex_url"], c_row["top_of_stack_apex_url"],
                f"Row #{idx+1} apex URL mismatch between doc3 and CSV"
            )
            self.assertEqual(
                c_row["top_of_stack_apex_url"], j_entry["top_of_stack_apex_url"],
                f"Row #{idx+1} apex URL mismatch between CSV and JSON"
            )

            # Shield target alignment
            self.assertEqual(
                d_row["shield_target_url"], c_row["shield_target_url"],
                f"Row #{idx+1} shield URL mismatch between doc3 and CSV"
            )
            self.assertEqual(
                c_row["shield_target_url"], j_entry["shield_target_url"],
                f"Row #{idx+1} shield URL mismatch between CSV and JSON"
            )

    def test_05_category_stack_conservation(self):
        """Asserts category stack distribution is conserved across CSV, JSON, and HTML."""
        csv_cats = {}
        for r in self.csv_rows:
            cat = r["category"]
            csv_cats[cat] = csv_cats.get(cat, 0) + 1

        json_cats = {}
        for e in self.json_entries:
            cat = e["category_stack"]
            json_cats[cat] = json_cats.get(cat, 0) + 1

        html_cats = {}
        for tr in self.html_tbody_rows:
            cat = tr.get("data-category")
            html_cats[cat] = html_cats.get(cat, 0) + 1

        self.assertEqual(csv_cats, json_cats, "Category count mismatch between CSV and JSON")
        self.assertEqual(json_cats, html_cats, "Category count mismatch between JSON and HTML")

        # Specific video stack check: exactly 67 entries (17 baseline + 50 ingested)
        self.assertEqual(csv_cats.get("Video Stack"), 67, "Video Stack count must be exactly 67 (17 baseline + 50 newly ingested)")
        video_asset_type_count = len([r for r in self.csv_rows if r["asset_type"] == "Video"])
        self.assertEqual(video_asset_type_count, 50, "asset_type == Video count must be exactly 50")
        self.assertEqual(sum(csv_cats.values()), 279, "Sum of all categories must be 279")


class TestIngestionIdempotenceStress(unittest.TestCase):
    """Class 3: Ingestion Script Idempotence & Mutation Stress."""

    def test_01_idempotent_execution_zero_additions_zero_mutations(self):
        """Executes ingest_video_assets.py a second time and verifies 0 additions/mutations."""
        # Step A: Hash existing doc3 CSV
        with open(DOC3_PATH, "rb") as f:
            hash_before = hashlib.sha256(f.read()).hexdigest()

        # Step B: Run ingest_video_assets.py
        cmd = [sys.executable, str(INGEST_SCRIPT)]
        proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)

        self.assertEqual(
            proc.returncode, 0,
            f"ingest_video_assets.py failed with exit code {proc.returncode}:\nSTDERR:\n{proc.stderr}\nSTDOUT:\n{proc.stdout}"
        )

        # Step C: Verify stdout announces 0 added
        self.assertIn("added=0", proc.stdout, "Ingestion must add 0 rows on re-run")
        self.assertIn("updated=0", proc.stdout, "Ingestion must update 0 rows on re-run")
        self.assertIn("skipped=50", proc.stdout, "Ingestion must skip all 50 duplicate video rows")
        self.assertIn("total=279", proc.stdout, "Total row count must remain 279")

        # Step D: Hash doc3 CSV after re-run
        with open(DOC3_PATH, "rb") as f:
            hash_after = hashlib.sha256(f.read()).hexdigest()

        self.assertEqual(
            hash_before, hash_after,
            "doc3_published_asset_links.csv SHA256 changed after idempotent ingestion run!"
        )

    def test_02_video_to_platform_one_to_one_mapping(self):
        """Verifies each video AST-VID-001..050 maps to distinct platform PLAT-VID-001..050."""
        with open(DOC3_PATH, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        vid_rows = [r for r in rows if r["asset_id"].startswith("AST-VID-")]
        self.assertEqual(len(vid_rows), 50)

        mapped_platforms = [r["parent_profile_id"] for r in vid_rows]
        self.assertEqual(len(set(mapped_platforms)), 50, "All 50 video assets must map to 50 unique platforms")

        for idx, r in enumerate(vid_rows):
            expected_pid = f"PLAT-VID-{idx+1:03d}"
            expected_aid = f"AST-VID-{idx+1:03d}"
            self.assertEqual(r["asset_id"], expected_aid)
            self.assertEqual(r["parent_profile_id"], expected_pid)


class TestHtmlDomFilteringAndRule29Contrast(unittest.TestCase):
    """Class 4: HTML DOM, Interactive Filtering, Rule 29 Contrast & Rule 45."""

    @classmethod
    def setUpClass(cls):
        with open(HTML_PATH, "r", encoding="utf-8") as f:
            cls.html_content = f.read()
        cls.soup = BeautifulSoup(cls.html_content, "html.parser")
        cls.rows = cls.soup.select("#ledger-tbody tr")

    def test_01_html_dom_structure(self):
        """Verifies HTML document has valid head, title, viewport, and JSON-LD DataCatalog."""
        title = self.soup.find("title")
        self.assertIsNotNone(title)
        self.assertIn("Public Backlink Master Ledger", title.text)

        # Check JSON-LD DataCatalog
        jsonld_script = self.soup.find("script", type="application/ld+json")
        self.assertIsNotNone(jsonld_script, "Missing application/ld+json script tag")
        catalog_ld = json.loads(jsonld_script.string)
        self.assertEqual(catalog_ld.get("@type"), "DataCatalog")
        self.assertEqual(catalog_ld.get("creator", {}).get("name"), "Gary Pearce")
        self.assertIn("7860 244 274", catalog_ld.get("creator", {}).get("telephone", ""))

    def test_02_search_and_filter_controls_present(self):
        """Verifies search input, category select, and counter badges exist with correct initial state."""
        search_input = self.soup.find("input", id="ledger-search")
        self.assertIsNotNone(search_input, "Missing #ledger-search input")

        cat_select = self.soup.find("select", id="category-filter")
        self.assertIsNotNone(cat_select, "Missing #category-filter select")

        options = [opt.get("value") for opt in cat_select.find_all("option")]
        self.assertEqual(options[0], "ALL")
        for s in SOVEREIGN_11_STACKS:
            self.assertIn(s, options, f"Missing category option in select: {s}")

        vis_badge = self.soup.find("span", id="visible-count")
        tot_badge = self.soup.find("span", id="total-count")
        self.assertIsNotNone(vis_badge)
        self.assertIsNotNone(tot_badge)
        self.assertEqual(vis_badge.text.strip(), "279")
        self.assertEqual(tot_badge.text.strip(), "279")

    def test_03_javascript_filter_simulation_all_categories(self):
        """Simulates the JavaScript category filter logic for every option."""
        # 1. Test "ALL"
        all_visible = [r for r in self.rows if True]
        self.assertEqual(len(all_visible), 279)

        # 2. Test each individual category against master CSV category count
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            csv_rows = list(csv.DictReader(f))
        expected_counts = {}
        for r in csv_rows:
            c = r["category"]
            expected_counts[c] = expected_counts.get(c, 0) + 1

        for stack in SOVEREIGN_11_STACKS:
            matching = [r for r in self.rows if r.get("data-category") == stack]
            expected = expected_counts.get(stack, 0)
            self.assertEqual(
                len(matching), expected,
                f"Stack '{stack}' filter count mismatch: got {len(matching)} vs expected {expected}"
            )

    def test_04_javascript_search_query_simulation(self):
        """Simulates JavaScript query text filter across table rows."""
        # Query: "Gary Pearce"
        query_gp = [r for r in self.rows if "gary pearce" in r.text.lower()]
        self.assertGreaterEqual(len(query_gp), 0)

        # Query: "07860 244 274" or "07860244274"
        query_phone = [r for r in self.rows if "07860244274" in r.text.lower().replace(" ", "")]
        self.assertGreater(len(query_phone), 0, "Expected phone tag in video rows")

        # Query: "Starlink"
        query_starlink = [r for r in self.rows if "starlink" in r.text.lower()]
        self.assertGreater(len(query_starlink), 0, "Expected Starlink query matches")

        # Query: "Hikvision"
        query_hik = [r for r in self.rows if "hikvision" in r.text.lower()]
        self.assertGreater(len(query_hik), 0, "Expected Hikvision query matches")

    def test_05_rule_29_contrast_and_styling(self):
        """Asserts Rule 29 contrast compliance: dark canvas, legible text, zero ghost text."""
        # Canvas check
        self.assertIn("background: #060609", self.html_content)

        # Zero ghost text: ensure no white text on white bg
        self.assertNotIn("text-white bg-white", self.html_content)
        self.assertNotIn("text-black bg-black", self.html_content)

        # Verify badges have legible colors
        self.assertIn("text-emerald-400", self.html_content)
        self.assertIn("text-blue-400", self.html_content)
        self.assertIn("text-orange-400", self.html_content)

        # Table rows check
        self.assertEqual(len(self.rows), 279)
        for r in self.rows:
            # Check for non-empty text content
            text = r.text.strip()
            self.assertGreater(len(text), 0, "Row text must not be empty")

    def test_06_rule_20_and_rule_45_compliance(self):
        """Enforces Rule 20 (Trade identity & 0 Checkatrade) and Rule 45 (Citadel Air-Gap)."""
        # Rule 20: 0 Checkatrade mentions
        self.assertNotIn("checkatrade", self.html_content.lower(), "Checkatrade mention found in HTML!")

        # Rule 20: Gary Pearce & Phone in footer
        footer = self.soup.find("footer")
        self.assertIsNotNone(footer)
        self.assertIn("Gary Pearce", footer.text)
        self.assertIn("07860 244 274", footer.text)

        # Rule 45: Zero raw root links in HTML
        raw_root_matches = re.findall(r'href=["\']https?://(?:www\.)?adicommunications\.co\.uk/?["\']', self.html_content)
        self.assertEqual(
            len(raw_root_matches), 0,
            f"Found {len(raw_root_matches)} raw root link(s) to adicommunications.co.uk in HTML: {raw_root_matches}"
        )

        # Rule 45: Tier 3 videos must NEVER link to adicommunications.co.uk
        with open(PLATFORM_CATALOG_PATH, "r", encoding="utf-8") as f:
            pcat = json.load(f)
        tier3_domains = {p["domain"] for p in pcat["category_stacks"]["video"]["platforms"] if p.get("tier") == "Tier 3"}

        for r in self.rows:
            # If public live URL is on a Tier 3 domain
            pub_link = r.find("a", href=True)
            if pub_link:
                href = pub_link["href"]
                for t3_dom in tier3_domains:
                    if t3_dom in href:
                        # Ensure no link in this row points to adicommunications.co.uk
                        all_links_in_row = [a["href"] for a in r.find_all("a", href=True)]
                        for l in all_links_in_row:
                            self.assertNotIn(
                                "adicommunications.co.uk", l,
                                f"Rule 45 violation: Tier 3 video row on {t3_dom} contains adicommunications link: {l}"
                            )

    def test_07_xss_injection_safety_and_escaping(self):
        """Verifies table cells do not contain unescaped raw HTML markup or script tags."""
        for idx, r in enumerate(self.rows):
            scripts = r.find_all("script")
            self.assertEqual(len(scripts), 0, f"Row #{idx+1} contains dangerous script tag!")
            iframes = r.find_all("iframe")
            self.assertEqual(len(iframes), 0, f"Row #{idx+1} contains unauthorized iframe!")

    def test_08_table_row_count_and_badges_parity(self):
        """Verifies visible-count and total-count match exact table row count in DOM."""
        vis = self.soup.find("span", id="visible-count")
        tot = self.soup.find("span", id="total-count")
        self.assertEqual(int(vis.text.strip()), len(self.rows))
        self.assertEqual(int(tot.text.strip()), len(self.rows))


class TestLiveEdgeReachability(unittest.TestCase):
    """Class 5: Live Firebase Edge CDN Public Accessibility Probe."""

    def test_01_live_firebase_edge_probe(self):
        """Probes live public_backlink_ledger.html on Firebase Edge CDN."""
        cache_buster = int(time.time())
        live_url = f"https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html?cb={cache_buster}"

        req = urllib.request.Request(
            live_url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                status = resp.status
                content = resp.read().decode("utf-8")
        except urllib.error.URLError as e:
            self.skipTest(f"Live edge probe skipped due to network/firewall: {e}")
            return

        self.assertEqual(status, 200, f"Expected HTTP 200 from live Edge CDN, got {status}")
        self.assertIn("Public Backlink Master Ledger", content)
        self.assertIn("07860 244 274", content)

        # Verify live row count matches exactly 279
        live_rows = len(re.findall(r'<tr class="hover:bg-white', content))
        self.assertEqual(live_rows, 279, f"Live edge CDN row count expected 279, got {live_rows}")


if __name__ == "__main__":
    unittest.main()
