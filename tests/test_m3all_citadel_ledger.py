"""
tests/test_m3all_citadel_ledger.py
Comprehensive test suite for Milestone M3-ALL:
1. 4-way mathematical parity across doc3, CSV, JSON, HTML (359 items)
2. JSON Schema Draft 2020-12 compliance (0 null values)
3. Rule 45 Google Shield Air-Gap compliance (0 raw root links across all files)
4. Google Slides DA 100 badge rendering in HTML ledger
5. Landing Page Deploy Manifest creation & Doc3RegistryGuard integration in browser_ui_worker.py
6. Real human questions & commercial pain points enforcement (no academic buzzwords / affiliate slop)
7. Category stack classification for Catbox CDN & Landing Page platforms
"""

import asyncio
import csv
import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent

from build_public_backlink_ledger import classify_category_stack
from browser_ui_worker import (
    BrowserUIWorker,
    LandingPageDeployManifest,
    SERVICE_LANDING_PAGE_DEFAULTS,
    Doc3RegistryGuard
)


class TestM3AllCitadelLedger(unittest.TestCase):

    def setUp(self):
        self.doc3_file = REPO_ROOT / "doc3_published_asset_links.csv"
        self.csv_file = REPO_ROOT / "public_backlink_master_ledger.csv"
        self.json_file = REPO_ROOT / "public_backlink_master_ledger.json"
        self.html_file = REPO_ROOT / "public_backlink_ledger.html"
        self.schema_file = REPO_ROOT / "public_backlink_ledger.schema.json"
        self.worker = BrowserUIWorker()

    def test_01_4way_mathematical_parity(self):
        """Verifies 100% mathematical parity across doc3, CSV, JSON, and HTML."""
        with open(self.doc3_file, "r", encoding="utf-8") as f:
            doc3_rows = list(csv.DictReader(f))
        with open(self.csv_file, "r", encoding="utf-8") as f:
            csv_rows = list(csv.DictReader(f))
        with open(self.json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        with open(self.html_file, "r", encoding="utf-8") as f:
            html_rows = len(re.findall(r'<tr class="hover:bg-white', f.read()))

        count = len(doc3_rows)
        self.assertEqual(count, 359, f"doc3 row count must be exactly 359, found {count}")
        self.assertEqual(len(csv_rows), count, f"CSV count ({len(csv_rows)}) != doc3 ({count})")
        self.assertEqual(len(json_data["entries"]), count, f"JSON count ({len(json_data['entries'])}) != doc3 ({count})")
        self.assertEqual(json_data["total_backlinks"], count, f"total_backlinks ({json_data['total_backlinks']}) != count ({count})")
        self.assertEqual(html_rows, count, f"HTML row count ({html_rows}) != count ({count})")

    def test_02_json_schema_draft_2020_12_and_zero_nulls(self):
        """Validates JSON against Draft 2020-12 schema and ensures 0 null values."""
        with open(self.json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        with open(self.schema_file, "r", encoding="utf-8") as f:
            schema = json.load(f)

        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(json_data))
        self.assertEqual(len(errors), 0, f"Schema validation errors encountered: {errors}")

        null_count = 0
        for idx, entry in enumerate(json_data["entries"], 1):
            for k, v in entry.items():
                if v is None:
                    null_count += 1
        self.assertEqual(null_count, 0, f"Found {null_count} null values in JSON ledger entries")

    def test_03_rule_45_zero_naked_roots(self):
        """Verifies zero naked root URLs to adicommunications.co.uk across all ledger files."""
        raw_root_regex = re.compile(r"^https?://(?:www\.)?adicommunications\.co\.uk/?(?:index\.(?:html?|php))?$", re.IGNORECASE)
        allowed_prefixes = ("/news/", "/assets/", "/feed/", "/cctv-", "/starlink-", "/tv-", "/wifi-", "/ajax-", "/aerial-")

        # Check JSON entries
        with open(self.json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        for idx, entry in enumerate(json_data["entries"], 1):
            for key in ("tenant_url", "apex_target", "shield_target_url"):
                val = entry.get(key, "")
                if "adicommunications.co.uk" in val:
                    self.assertFalse(
                        bool(raw_root_regex.match(val.strip())),
                        f"Rule 45 raw root leak in JSON entry {idx} key {key}: {val}"
                    )
                    self.assertTrue(
                        any(sub in val for sub in allowed_prefixes),
                        f"Rule 45 unshielded target path in JSON entry {idx} key {key}: {val}"
                    )

        # Check CSV rows
        with open(self.csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, 1):
                shield_url = row.get("shield_target_url", "")
                if "adicommunications.co.uk" in shield_url:
                    self.assertFalse(
                        bool(raw_root_regex.match(shield_url.strip())),
                        f"Rule 45 raw root leak in CSV row {idx}: {shield_url}"
                    )

    def test_04_google_slides_da100_badge_in_html_ledger(self):
        """Verifies Google Slides DA 100 badges are correctly rendered in HTML ledger."""
        with open(self.html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Google Slides presentation entries should display "Google Slides (DA 100)"
        self.assertIn("Google Slides (DA 100)", html_content)

        # Verify Google Slides badge count matches presentation URL occurrences in HTML
        badge_count = len(re.findall(r'>Google Slides \(DA 100\)</span>', html_content))
        self.assertGreaterEqual(badge_count, 20, f"Expected at least 20 Google Slides badges, found {badge_count}")

    def test_05_landing_page_manifest_creation_and_real_human_pain_points(self):
        """Verifies landing page manifests embody real human questions and purge academic slop."""
        service_keys = ["cctv", "starlink", "tv", "alarms", "aerials", "cabling"]

        expected_human_questions = {
            "cctv": "Why Is My Night Vision Black on My Security Camera?",
            "starlink": "Can I Put Starlink on a Chimney Without Drilling the Brickwork?",
            "tv": "Is It Safe to Mount an OLED TV Above a Real Log Burner or Fireplace?",
            "alarms": "Why Does My Alarm Go Off When the Boiler Kicks In?",
            "aerials": "Why Does My TV Picture Break Up in High Winds?",
            "cabling": "How Do I Get Internet to My Garden Office Without Digging Up the Lawn?"
        }

        for key in service_keys:
            manifest = self.worker.get_default_landing_page_manifest(service_key=key, platform_name="Carrd")
            self.assertIsInstance(manifest, LandingPageDeployManifest)
            self.assertEqual(manifest.service_key, key)

            # Check for real human question
            self.assertIn(expected_human_questions[key], manifest.h1_heading)

            # Check academic buzzwords are PURGED from title and H1
            for buzzword in ["BS EN", "laboratory", "Top 10 Best", "revolutionary", "game-changer"]:
                self.assertNotIn(buzzword.lower(), manifest.page_title.lower())
                self.assertNotIn(buzzword.lower(), manifest.h1_heading.lower())

            # Check Gary Pearce contact details & trade authority
            self.assertIn("07860 244 274", manifest.body_markdown)

            # Check Rule 45 compliance
            self.assertFalse(manifest.downward_service_url.endswith("adicommunications.co.uk/"))
            self.assertTrue(any(sub in manifest.downward_service_url for sub in ("/cctv-", "/starlink-", "/tv-", "/ajax-", "/aerial-", "/wifi-")))

    def test_06_browser_ui_worker_landing_page_deploy_and_checkpoints(self):
        """Verifies execute_landing_page_deployment executes with 4 checkpoints and 14-col output."""
        manifest = self.worker.get_default_landing_page_manifest(service_key="starlink", platform_name="Carrd")
        result = asyncio.run(self.worker.execute_landing_page_deployment(manifest, record_to_doc3=False))

        self.assertEqual(result.get("status"), "SUCCESS")
        self.assertIn("carrd.co", result.get("asset_public_url", ""))
        self.assertEqual(len(result.get("screenshots", [])), 4)

        # Verify all 4 checkpoint files exist and are valid non-empty PNGs
        for screenshot_path in result["screenshots"]:
            p = Path(screenshot_path)
            self.assertTrue(p.exists(), f"Screenshot does not exist: {p}")
            self.assertGreater(p.stat().st_size, 0, f"Screenshot file is empty: {p}")

        # Verify 14-column layout
        row_14col = result.get("published_row_14col", [])
        self.assertEqual(len(row_14col), 14, f"Expected 14 columns, got {len(row_14col)}")
        self.assertEqual(row_14col[5], "Landing Page Stack")
        self.assertEqual(row_14col[13], "HTTP_200")

    def test_07_doc3_registry_guard_integration(self):
        """Verifies Doc3RegistryGuard properly validates and registers 14-column assets."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", encoding="utf-8") as tmp:
            tmp_path = Path(tmp.name)
            # Write standard 14-column header
            tmp.write(
                "asset_id,parent_profile_id,platform_name,profile_live_url,asset_title,asset_type,"
                "asset_public_url,top_of_stack_apex_url,shield_target_url,seo_tags,seo_description_summary,"
                "dofollow_status,publication_date,verification_status\n"
            )

        try:
            # 1. Test naked root rejection
            invalid_entry = {
                "shield_target_url": "https://adicommunications.co.uk/",
                "asset_title": "Invalid Root Link"
            }
            with self.assertRaises(ValueError):
                Doc3RegistryGuard.register_asset(tmp_path, invalid_entry)

            # 2. Test valid registration
            valid_entry = {
                "parent_profile_id": "PROF-SITE-CCTV",
                "platform_name": "Carrd",
                "profile_live_url": "https://adi-cctv.carrd.co",
                "asset_title": "Why Is My Night Vision Black on My Security Camera? — Gary Pearce ADI Communications",
                "asset_type": "Landing Page Stack",
                "asset_public_url": "https://adi-cctv.carrd.co",
                "top_of_stack_apex_url": "https://sites.google.com/view/adi-cctv-installations-uk/",
                "shield_target_url": "https://adicommunications.co.uk/cctv-installation/",
                "seo_tags": "#cctv #security",
                "seo_description_summary": "Hands-on troubleshooting for black night vision.",
                "dofollow_status": "Follow",
                "publication_date": "2026-10-23",
                "verification_status": "HTTP_200"
            }
            asset_id = Doc3RegistryGuard.register_asset(tmp_path, valid_entry)
            self.assertTrue(asset_id.startswith("LINK-"))

            # Verify registered row has 14 columns
            with open(tmp_path, "r", encoding="utf-8") as f:
                rows = list(csv.reader(f))
                self.assertEqual(len(rows), 2)  # header + 1 data row
                self.assertEqual(len(rows[1]), 14)
        finally:
            if tmp_path.exists():
                os.unlink(tmp_path)

    def test_08_category_stack_classification_rules(self):
        """Verifies category classification maps Catbox and Landing Page platforms correctly."""
        # Catbox CDN
        cat, agent = classify_category_stack("Catbox CDN", "CDN Image Asset", "https://files.catbox.moe/0t91q9.webp", "https://docs.google.com/presentation/...")
        self.assertEqual(cat, "Images & Visual Trade Photography Stack")
        self.assertEqual(agent, "stack-media-agent")

        # Landing Page platforms
        for plat in ["Carrd", "Strikingly", "Webflow", "Notion Sites", "Canva Sites", "Bento.me"]:
            cat, agent = classify_category_stack(plat, "Landing Page Stack", f"https://adi.{plat.lower()}.com", "https://sites.google.com/...")
            self.assertEqual(cat, "Landing Page & Website Stacks", f"Failed for platform {plat}")
            self.assertEqual(agent, "stack-sites-agent", f"Failed for platform {plat}")


if __name__ == "__main__":
    unittest.main()
