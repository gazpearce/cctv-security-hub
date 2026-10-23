"""
tests/test_challenger_m3_2_battery.py
Adversarial Empirical Stress-Test Battery for Milestone 3:
1. Rule 45 link leaks deep scan (HTML, CSV, JSON, doc3)
2. Static DOM row integrity and 4-way mathematical parity
3. Category filter dropdown & data-category attribute parity across all 11 Sovereign Category Stacks
4. Simulated client-side filter & search matrix
5. Schema.org DataCatalog JSON-LD extraction and validation
6. JSON Schema Draft 2020-12 strict validation and field invariance
7. Generator idempotency and regeneration verification
"""

import csv
import json
import os
import re
import unittest
from bs4 import BeautifulSoup
from jsonschema import Draft202012Validator
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

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

class TestMilestone3EmpiricalChallenger(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html_path = REPO_ROOT / "public_backlink_ledger.html"
        cls.csv_path = REPO_ROOT / "public_backlink_master_ledger.csv"
        cls.json_path = REPO_ROOT / "public_backlink_master_ledger.json"
        cls.doc3_path = REPO_ROOT / "doc3_published_asset_links.csv"
        cls.schema_path = REPO_ROOT / "public_backlink_ledger.schema.json"

        with open(cls.html_path, "r", encoding="utf-8") as f:
            cls.html_raw = f.read()
        cls.soup = BeautifulSoup(cls.html_raw, "html.parser")

        with open(cls.csv_path, "r", encoding="utf-8") as f:
            cls.csv_rows = list(csv.DictReader(f))

        with open(cls.doc3_path, "r", encoding="utf-8") as f:
            cls.doc3_rows = list(csv.DictReader(f))

        with open(cls.json_path, "r", encoding="utf-8") as f:
            cls.json_data = json.load(f)

        with open(cls.schema_path, "r", encoding="utf-8") as f:
            cls.schema_spec = json.load(f)

    # -------------------------------------------------------------------------
    # 1. RULE 45 AIR-GAP DEEP EMPIRICAL STRESS TEST
    # -------------------------------------------------------------------------
    def test_r45_01_no_naked_root_links_in_html_hrefs(self):
        """Inspect all <a> href attributes in public_backlink_ledger.html for Rule 45 leaks."""
        links = self.soup.find_all("a")
        self.assertGreater(len(links), 100, "Expected at least 100 anchor links in the ledger HTML")
        leaks = []
        for a in links:
            href = a.get("href", "")
            if "adicommunications.co.uk" in href:
                if not any(sub in href for sub in ("/news/", "/assets/", "/feed/")):
                    leaks.append(href)
        self.assertEqual(leaks, [], f"Rule 45 leak detected in HTML hrefs: {leaks}")

    def test_r45_02_no_naked_root_links_in_html_raw_body(self):
        """Regex scan the entire raw HTML for any naked root adicommunications.co.uk mentions."""
        pattern = re.compile(r"https?://(?:www\.)?adicommunications\.co\.uk/?(?:$|[?#\"'\s<>,;)\]}])")
        leaks = []
        for line_no, line in enumerate(self.html_raw.splitlines(), 1):
            if pattern.search(line):
                if not re.search(r"adicommunications\.co\.uk/(?:news|assets|feed)", line):
                    leaks.append((line_no, line.strip()))
        self.assertEqual(leaks, [], f"Raw root link found in HTML body: {leaks}")

    def test_r45_03_no_naked_root_links_in_csv_cells(self):
        """Inspect every column cell in public_backlink_master_ledger.csv."""
        leaks = []
        for r_idx, row in enumerate(self.csv_rows, 1):
            for col, val in row.items():
                if "adicommunications.co.uk" in val:
                    if not any(sub in val for sub in ("/news/", "/assets/", "/feed/")):
                        leaks.append((r_idx, col, val))
        self.assertEqual(leaks, [], f"Rule 45 leak in CSV: {leaks}")

    def test_r45_04_no_naked_root_links_in_json_recursive(self):
        """Recursively scan all keys and values in public_backlink_master_ledger.json."""
        leaks = []
        def check_val(path, val):
            if isinstance(val, str):
                if "adicommunications.co.uk" in val:
                    if not any(sub in val for sub in ("/news/", "/assets/", "/feed/")):
                        leaks.append((path, val))
            elif isinstance(val, dict):
                for k, v in val.items():
                    check_val(f"{path}.{k}", v)
            elif isinstance(val, list):
                for i, item in enumerate(val):
                    check_val(f"{path}[{i}]", item)

        check_val("root", self.json_data)
        self.assertEqual(leaks, [], f"Rule 45 leak in JSON: {leaks}")

    def test_r45_05_no_naked_root_links_in_doc3_source(self):
        """Inspect source doc3_published_asset_links.csv to verify source hygiene."""
        leaks = []
        for r_idx, row in enumerate(self.doc3_rows, 1):
            for col, val in row.items():
                if "adicommunications.co.uk" in val:
                    if not any(sub in val for sub in ("/news/", "/assets/", "/feed/")):
                        leaks.append((r_idx, col, val))
        self.assertEqual(leaks, [], f"Rule 45 leak in doc3 source: {leaks}")

    def test_r45_06_inventory_of_all_adicommunications_urls_in_ledger_files(self):
        """Inventory all adicommunications.co.uk URLs in ledger files and ensure each is an allowed buffer."""
        for path in (self.html_path, self.csv_path, self.json_path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            urls = set(re.findall(r"https?://[^\s\"\'<>]*adicommunications\.co\.uk[^\s\"\'<>]*", content))
            for u in urls:
                # Every single URL must contain /news/, /assets/, or /feed/
                is_allowed = any(sub in u for sub in ("/news/", "/assets/", "/feed/"))
                self.assertTrue(is_allowed, f"Disallowed adicommunications URL '{u}' found in {path.name}")

    # -------------------------------------------------------------------------
    # 2. CATEGORY FILTER & 11 SOVEREIGN STACKS EMPIRICAL VERIFICATION
    # -------------------------------------------------------------------------
    def test_cat_01_all_11_stacks_present_in_select_dropdown(self):
        """Verify the #category-filter select dropdown contains 'ALL' and all 11 exact stacks."""
        cat_select = self.soup.find("select", {"id": "category-filter"})
        self.assertIsNotNone(cat_select, "Missing <select id='category-filter'> element")
        
        options = cat_select.find_all("option")
        opt_values = [o.get("value") for o in options]
        
        self.assertIn("ALL", opt_values, "Missing 'ALL' option in category filter")
        for stack in SOVEREIGN_11_STACKS:
            self.assertIn(stack, opt_values, f"Missing stack option in dropdown: {stack}")
        
        self.assertEqual(len(opt_values), 12, f"Expected 12 options (ALL + 11 stacks), got {len(opt_values)}: {opt_values}")

    def test_cat_02_all_table_rows_have_valid_data_category(self):
        """Verify every table row in tbody has a data-category matching one of the 11 stacks."""
        tbody = self.soup.find("tbody", {"id": "ledger-tbody"})
        self.assertIsNotNone(tbody, "Missing <tbody id='ledger-tbody'>")
        
        rows = tbody.find_all("tr")
        n_assets = len(self.doc3_rows)
        self.assertEqual(len(rows), n_assets, f"Expected {n_assets} rows in tbody, got {len(rows)}")
        
        invalid_rows = []
        category_counts = {}
        for idx, r in enumerate(rows, 1):
            cat = r.get("data-category")
            if not cat or cat not in SOVEREIGN_11_STACKS:
                invalid_rows.append((idx, cat))
            else:
                category_counts[cat] = category_counts.get(cat, 0) + 1

        self.assertEqual(invalid_rows, [], f"Rows with invalid data-category: {invalid_rows}")
        
        # Verify sum matches total
        total_counted = sum(category_counts.values())
        self.assertEqual(total_counted, n_assets)

    def test_cat_03_simulated_javascript_category_filtering(self):
        """Simulate client-side JavaScript category filtering logic for all 11 stacks."""
        tbody = self.soup.find("tbody", {"id": "ledger-tbody"})
        rows = tbody.find_all("tr")
        n_assets = len(self.doc3_rows)

        # 1. Filter: 'ALL'
        visible_all = [r for r in rows if r.get("data-category")]
        self.assertEqual(len(visible_all), n_assets)

        # 2. Filter: Dynamically computed category distribution from CSV ledger
        expected_distribution = {stack: 0 for stack in SOVEREIGN_11_STACKS}
        for r in self.csv_rows:
            cat = r["category"]
            self.assertIn(cat, expected_distribution, f"Unknown category in CSV: {cat}")
            expected_distribution[cat] += 1

        for stack, expected_count in expected_distribution.items():
            matching_rows = [r for r in rows if r.get("data-category") == stack]
            self.assertEqual(len(matching_rows), expected_count, 
                             f"Category '{stack}' DOM rows ({len(matching_rows)}) must match CSV count ({expected_count})")

    def test_cat_04_simulated_search_and_category_matrix(self):
        """Simulate combined search query + category filtering matching applyFilter() logic."""
        tbody = self.soup.find("tbody", {"id": "ledger-tbody"})
        rows = tbody.find_all("tr")

        def simulate_filter(query, cat):
            q = (query or "").lower().strip()
            count = 0
            for r in rows:
                row_cat = r.get("data-category", "")
                row_text = r.get_text().lower()
                matches_cat = (cat == "ALL" or row_cat == cat)
                matches_q = (not q or q in row_text)
                if matches_cat and matches_q:
                    count += 1
            return count

        # Query tests
        self.assertEqual(simulate_filter("", "ALL"), len(self.doc3_rows))
        self.assertEqual(simulate_filter("pinterest", "ALL"), 26)
        self.assertEqual(simulate_filter("pinterest", "Images & Visual Trade Photography Stack"), 26)
        self.assertEqual(simulate_filter("pinterest", "Video Stack"), 0)
        expected_cctv = sum(1 for r in rows if "cctv" in r.get_text().lower())
        self.assertGreater(expected_cctv, 0, "Expected at least one CCTV asset")
        self.assertEqual(simulate_filter("cctv", "ALL"), expected_cctv)
        self.assertEqual(simulate_filter("nonexistent_term_404_xyz", "ALL"), 0)

    # -------------------------------------------------------------------------
    # 3. 4-WAY MATHEMATICAL PARITY & DOM INTEGRITY
    # -------------------------------------------------------------------------
    def test_parity_01_4way_count_parity(self):
        """Verify 100% count parity across doc3, CSV, JSON, and HTML."""
        doc3_count = len(self.doc3_rows)
        csv_count = len(self.csv_rows)
        json_count = len(self.json_data["entries"])
        json_meta_count = self.json_data["total_backlinks"]
        
        tbody = self.soup.find("tbody", {"id": "ledger-tbody"})
        html_row_count = len(tbody.find_all("tr"))
        html_regex_count = len(re.findall(r'<tr class="hover:bg-white', self.html_raw))

        self.assertGreaterEqual(doc3_count, 219, f"doc3 must contain at least 219 rows, found {doc3_count}")
        self.assertEqual(csv_count, doc3_count, f"CSV count ({csv_count}) != doc3 ({doc3_count})")
        self.assertEqual(json_count, doc3_count, f"JSON entries count ({json_count}) != doc3 ({doc3_count})")
        self.assertEqual(json_meta_count, doc3_count, f"JSON metadata total_backlinks ({json_meta_count}) != doc3 ({doc3_count})")
        self.assertEqual(html_row_count, doc3_count, f"HTML DOM tbody rows ({html_row_count}) != doc3 ({doc3_count})")
        self.assertEqual(html_regex_count, doc3_count, f"HTML regex rows ({html_regex_count}) != doc3 ({doc3_count})")

    def test_parity_02_field_level_alignment(self):
        """Check field alignment across CSV, JSON, and HTML for all items."""
        tbody = self.soup.find("tbody", {"id": "ledger-tbody"})
        html_rows = tbody.find_all("tr")

        for idx in range(len(self.doc3_rows)):
            csv_r = self.csv_rows[idx]
            json_r = self.json_data["entries"][idx]
            html_r = html_rows[idx]

            # Compare platform
            self.assertEqual(csv_r["platform"], json_r["platform"])
            self.assertEqual(csv_r["category"], json_r["category_stack"])
            self.assertEqual(csv_r["public_live_url"], json_r["tenant_url"])
            self.assertEqual(csv_r["top_of_stack_apex_url"], json_r["apex_target"])

            # Verify HTML data-category matches CSV category
            self.assertEqual(html_r.get("data-category"), csv_r["category"])
            # Verify live URL appears in HTML row
            self.assertIn(csv_r["public_live_url"], str(html_r))

    # -------------------------------------------------------------------------
    # 4. JSON SCHEMA DRAFT 2020-12 VALIDATION & JSON-LD
    # -------------------------------------------------------------------------
    def test_schema_01_draft202012_strict_validation(self):
        """Validate public_backlink_master_ledger.json with jsonschema.Draft202012Validator."""
        validator = Draft202012Validator(self.schema_spec)
        errors = list(validator.iter_errors(self.json_data))
        self.assertEqual(errors, [], f"JSON Schema Draft 2020-12 validation errors: {errors}")

    def test_schema_02_top_level_metadata(self):
        """Verify all required top-level metadata fields in JSON."""
        expected_meta = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "version": "3.1.0",
            "title": "Public Backlink Master Ledger & Apex Google Pyramid Stack",
            "rule_45_shield": "STRICT_AIR_GAP",
            "total_backlinks": len(self.doc3_rows)
        }
        for k, v in expected_meta.items():
            self.assertEqual(self.json_data.get(k), v, f"Metadata mismatch for {k}")

        self.assertIn("Gary Pearce", self.json_data.get("lead_engineer", ""))
        self.assertIn("07860 244 274", self.json_data.get("lead_engineer", ""))

    def test_schema_03_jsonld_structured_data_in_html(self):
        """Validate Schema.org DataCatalog JSON-LD inside public_backlink_ledger.html."""
        script_tag = self.soup.find("script", {"type": "application/ld+json"})
        self.assertIsNotNone(script_tag, "Missing application/ld+json script tag in HTML")
        
        ld_data = json.loads(script_tag.string)
        self.assertEqual(ld_data.get("@context"), "https://schema.org")
        self.assertEqual(ld_data.get("@type"), "DataCatalog")
        self.assertIn("Gary Pearce", ld_data.get("creator", {}).get("name", ""))
        self.assertEqual(ld_data.get("creator", {}).get("telephone"), "+44 7860 244 274")
        self.assertEqual(ld_data.get("publisher", {}).get("name"), "ADI Communications")
        self.assertEqual(ld_data.get("publisher", {}).get("url"), "https://tvandhomesecurity.blogspot.com/")

    def test_cat_05_category_counts_cross_format_parity(self):
        """Verify that category counts across CSV, JSON, and HTML are 100% identical for each of the 11 stacks."""
        csv_counts = {}
        for r in self.csv_rows:
            c = r["category"]
            csv_counts[c] = csv_counts.get(c, 0) + 1

        json_counts = {}
        for e in self.json_data["entries"]:
            c = e["category_stack"]
            json_counts[c] = json_counts.get(c, 0) + 1

        tbody = self.soup.find("tbody", {"id": "ledger-tbody"})
        html_counts = {}
        for r in tbody.find_all("tr"):
            c = r.get("data-category")
            html_counts[c] = html_counts.get(c, 0) + 1

        for stack in SOVEREIGN_11_STACKS:
            c_csv = csv_counts.get(stack, 0)
            c_json = json_counts.get(stack, 0)
            c_html = html_counts.get(stack, 0)
            self.assertEqual(c_csv, c_json, f"Mismatch CSV vs JSON for {stack}")
            self.assertEqual(c_json, c_html, f"Mismatch JSON vs HTML for {stack}")

    def test_html_01_interactive_elements_and_dom_ids(self):
        """Verify presence and attributes of all interactive controls in public_backlink_ledger.html."""
        self.assertIsNotNone(self.soup.find("input", {"id": "ledger-search"}))
        self.assertIsNotNone(self.soup.find("select", {"id": "category-filter"}))
        
        vis_count = self.soup.find("span", {"id": "visible-count"})
        self.assertIsNotNone(vis_count)
        expected_str = str(len(self.doc3_rows))
        self.assertEqual(vis_count.text.strip(), expected_str)
        
        tot_count = self.soup.find("span", {"id": "total-count"})
        self.assertIsNotNone(tot_count)
        self.assertEqual(tot_count.text.strip(), expected_str)

        table = self.soup.find("table", {"id": "ledger-table"})
        self.assertIsNotNone(table)

    def test_html_02_all_external_urls_have_rel_noopener_and_target_blank(self):
        """Ensure all external links in the table body have target='_blank' and rel='noopener'."""
        tbody = self.soup.find("tbody", {"id": "ledger-tbody"})
        for a in tbody.find_all("a"):
            href = a.get("href", "")
            if href.startswith("http"):
                self.assertEqual(a.get("target"), "_blank", f"Link {href} missing target='_blank'")
                self.assertIn("noopener", a.get("rel", []), f"Link {href} missing rel='noopener'")

    def test_generator_01_idempotent_rebuild(self):
        """Run build_public_backlink_ledger.py and verify mathematical parity is preserved."""
        import subprocess
        res = subprocess.run(["python", "build_public_backlink_ledger.py"], cwd=str(REPO_ROOT), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Generator script failed: {res.stderr}")
        self.assertIn("Generated", res.stdout)
        
        # Re-verify file counts after build
        with open(self.csv_path, "r", encoding="utf-8") as f:
            c_len = len(list(csv.DictReader(f)))
        with open(self.json_path, "r", encoding="utf-8") as f:
            j_data = json.load(f)
        with open(self.html_path, "r", encoding="utf-8") as f:
            h_rows = len(re.findall(r'<tr class="hover:bg-white', f.read()))

        expected_len = len(self.doc3_rows)
        self.assertEqual(c_len, expected_len)
        self.assertEqual(len(j_data["entries"]), expected_len)
        self.assertEqual(j_data["total_backlinks"], expected_len)
        self.assertEqual(h_rows, expected_len)


if __name__ == "__main__":
    unittest.main()

