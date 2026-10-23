"""
tests/test_4way_ledger_manifest_parity.py
Adversarial mathematical parity and referential integrity test between
CSV, JSON, HTML ledgers and master_profile_manifest.json.
"""

import csv
import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

class Test4WayLedgerManifestParity(unittest.TestCase):

    def setUp(self):
        self.doc3_file = REPO_ROOT / "doc3_published_asset_links.csv"
        self.csv_file = REPO_ROOT / "public_backlink_master_ledger.csv"
        self.json_file = REPO_ROOT / "public_backlink_master_ledger.json"
        self.html_file = REPO_ROOT / "public_backlink_ledger.html"
        self.manifest_file = REPO_ROOT / "master_profile_manifest.json"

    def test_row_count_mathematical_parity(self):
        with open(self.doc3_file, "r", encoding="utf-8") as f:
            doc3_rows = list(csv.DictReader(f))
        with open(self.csv_file, "r", encoding="utf-8") as f:
            csv_rows = list(csv.DictReader(f))
        with open(self.json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        with open(self.html_file, "r", encoding="utf-8") as f:
            html_rows = len(re.findall(r'<tr class="hover:bg-white', f.read()))

        count = len(doc3_rows)
        self.assertGreaterEqual(count, 219, f"doc3 row count must be at least 219, found {count}")
        self.assertEqual(len(csv_rows), count, "CSV row count must match doc3")
        self.assertEqual(len(json_data["entries"]), count, "JSON entries must match doc3")
        self.assertEqual(json_data["total_backlinks"], count, "JSON total_backlinks must match count")
        self.assertEqual(html_rows, count, "HTML table rows must match count")

    def test_manifest_referential_integrity(self):
        with open(self.manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        manifest_stacks = manifest["category_stacks_11"]
        self.assertEqual(len(manifest_stacks), 11, "Manifest must have 11 category stacks")

        established_profiles = {p["profile_id"]: p for p in manifest["established_profiles_100"]}
        self.assertEqual(len(established_profiles), 100, "Manifest must have 100 established profiles")

        with open(self.json_file, "r", encoding="utf-8") as f:
            ledger_data = json.load(f)

        valid_apex_prefixes = [v["apex_url"] for v in manifest_stacks.values()]
        # Blogger apex also includes individual blog post permalinks
        valid_domains = [
            "youtube.com", "drive.google.com", "blogspot.com",
            "web.app", "sites.google.com", "maps.google.com",
            "photos.google.com", "docs.google.com"
        ]

        for idx, entry in enumerate(ledger_data["entries"], 1):
            actual_apex = entry.get("apex_target") or entry.get("top_of_stack_apex_url")
            self.assertTrue(
                any(domain in actual_apex for domain in valid_domains),
                f"Entry {idx} ({entry.get('platform')}) has invalid non-Google apex: {actual_apex}"
            )

    def test_rule45_across_all_ledger_records(self):
        with open(self.json_file, "r", encoding="utf-8") as f:
            ledger_data = json.load(f)

        raw_root_regex = re.compile(r"^https?://(?:www\.)?adicommunications\.co\.uk/?(?:index\.(?:html?|php))?$", re.IGNORECASE)
        allowed_prefixes = ("/news/", "/assets/", "/feed/", "/cctv-", "/starlink-", "/tv-", "/wifi-", "/ajax-", "/aerial-")

        for idx, entry in enumerate(ledger_data["entries"], 1):
            for field in ["tenant_url", "apex_target", "shield_target_url"]:
                val = entry.get(field, "")
                if "adicommunications.co.uk" in val:
                    self.assertFalse(
                        bool(raw_root_regex.match(val.strip())),
                        f"Rule 45 raw root leak in entry {idx} field '{field}': {val}"
                    )
                    self.assertTrue(
                        any(sub in val for sub in allowed_prefixes),
                        f"Rule 45 leak in entry {idx} field '{field}': {val}"
                    )

if __name__ == "__main__":
    unittest.main()
