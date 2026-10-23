"""
tests/test_challenger_m3all_2_adversarial.py
Adversarial Challenge Battery for Milestone M3-ALL:
- Task 1: LandingPageDeployManifest validation & 5 platform builders execution
- Task 2: CLI interface execution, return codes, JSON parsing, and invalid service key handling
- Task 3: Doc3RegistryGuard integration and strict 14-column output format assertion
- Task 4: Checkpoint screenshots existence, non-zero sizes, and PNG binary headers
"""

import asyncio
import csv
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from browser_ui_worker import (
    BrowserUIWorker,
    LandingPageDeployManifest,
    SERVICE_LANDING_PAGE_DEFAULTS,
    Doc3RegistryGuard,
)


class TestChallengerM3AllAdversarial(unittest.TestCase):
    """Adversarial stress and verification battery for M3-ALL landing page architecture."""

    def setUp(self):
        self.worker = BrowserUIWorker()
        self.python_bin = sys.executable

    # ==========================================================================
    # Task 1: LandingPageDeployManifest Validation & Rule 45 Enforcement
    # ==========================================================================

    def test_01_rule45_naked_root_variations_rejected(self):
        """Verifies that all variations of naked root URLs to adicommunications.co.uk are rejected."""
        naked_variations = [
            "https://adicommunications.co.uk",
            "https://adicommunications.co.uk/",
            "http://adicommunications.co.uk",
            "http://adicommunications.co.uk/",
            "https://www.adicommunications.co.uk",
            "https://www.adicommunications.co.uk/",
            "http://www.adicommunications.co.uk/",
            "https://adicommunications.co.uk/index.html",
            "https://adicommunications.co.uk/index.htm",
            "https://adicommunications.co.uk/index.php",
            "https://www.adicommunications.co.uk/index.html",
        ]

        for bad_url in naked_variations:
            with self.subTest(bad_url=bad_url):
                manifest = self.worker.get_default_landing_page_manifest(service_key="cctv", platform_name="Carrd")
                manifest.downward_service_url = bad_url

                res = asyncio.run(self.worker.execute_landing_page_deployment(manifest, record_to_doc3=False))
                self.assertEqual(res.get("status"), "FAILED", f"Expected FAILED status for naked root: {bad_url}")
                self.assertIn("Rule 45 violation", res.get("error", ""), f"Expected Rule 45 error for: {bad_url}")

    def test_02_unshielded_paths_rejected(self):
        """Verifies that unshielded arbitrary paths on adicommunications.co.uk are rejected."""
        unshielded_paths = [
            "https://adicommunications.co.uk/random-page/",
            "https://adicommunications.co.uk/about-us/",
            "https://adicommunications.co.uk/contact/",
            "https://www.adicommunications.co.uk/services/",
        ]

        for bad_url in unshielded_paths:
            with self.subTest(bad_url=bad_url):
                manifest = self.worker.get_default_landing_page_manifest(service_key="cctv", platform_name="Carrd")
                manifest.downward_service_url = bad_url

                res = asyncio.run(self.worker.execute_landing_page_deployment(manifest, record_to_doc3=False))
                self.assertEqual(res.get("status"), "FAILED", f"Expected FAILED for unshielded path: {bad_url}")
                self.assertIn("Rule 45 violation", res.get("error", ""))

    def test_03_allowed_deep_service_paths_accepted(self):
        """Verifies that legitimate deep service and shielded resource paths are accepted."""
        allowed_paths = [
            "https://adicommunications.co.uk/cctv-installation/",
            "https://adicommunications.co.uk/starlink-internet-installation/",
            "https://adicommunications.co.uk/tv-wall-mounting/",
            "https://adicommunications.co.uk/ajax-alarm-installation/",
            "https://adicommunications.co.uk/aerial-installation/",
            "https://adicommunications.co.uk/wifi-network-cabling/",
            "https://adicommunications.co.uk/news/cctv-field-guide",
            "https://adicommunications.co.uk/assets/schematic.webp",
            "https://adicommunications.co.uk/feed/podcast.xml",
        ]

        raw_root_regex = re.compile(r"^https?://(?:www\.)?adicommunications\.co\.uk/?(?:index\.(?:html?|php))?$", re.IGNORECASE)
        allowed_prefixes = ("/news/", "/assets/", "/feed/", "/cctv-", "/starlink-", "/tv-", "/wifi-", "/ajax-", "/aerial-")

        for valid_url in allowed_paths:
            with self.subTest(valid_url=valid_url):
                self.assertIsNone(raw_root_regex.match(valid_url.strip()))
                self.assertTrue(any(sub in valid_url for sub in allowed_prefixes))

        # Perform one live verification run
        manifest = self.worker.get_default_landing_page_manifest(service_key="cctv", platform_name="Carrd")
        manifest.downward_service_url = allowed_paths[0]
        res = asyncio.run(self.worker.execute_landing_page_deployment(manifest, record_to_doc3=False))
        self.assertEqual(res.get("status"), "SUCCESS")

    def test_04_manifest_dataclass_integrity_and_required_fields(self):
        """Verifies LandingPageDeployManifest enforces mandatory positional arguments."""
        # 1. No arguments should raise TypeError
        with self.assertRaises(TypeError):
            LandingPageDeployManifest()  # type: ignore

        # 2. Missing arguments should raise TypeError
        with self.assertRaises(TypeError):
            LandingPageDeployManifest(platform_name="Carrd", service_key="cctv")  # type: ignore

    # ==========================================================================
    # Task 1 & 4: Platform Builders & 4-Checkpoint Screenshots Verification
    # ==========================================================================

    def test_05_all_five_platform_builders_execute_successfully(self):
        """
        Tests deployment across all 5 required landing page platforms:
        Carrd, Strikingly, Webflow, Notion Site, Canva Site.
        Verifies live public URL domains, status, and screenshot lists.
        """
        platforms = [
            ("Carrd", "cctv", "carrd.co"),
            ("Strikingly", "starlink", "mystrikingly.com"),
            ("Webflow", "tv", "webflow.io"),
            ("Notion Site", "alarms", "notion.site"),
            ("Canva Site", "aerials", "my.canva.site"),
        ]

        for platform_name, service_key, expected_domain in platforms:
            with self.subTest(platform=platform_name, service=service_key):
                manifest = self.worker.get_default_landing_page_manifest(
                    service_key=service_key,
                    platform_name=platform_name
                )
                res = asyncio.run(self.worker.execute_landing_page_deployment(manifest, record_to_doc3=False))

                self.assertEqual(res.get("status"), "SUCCESS", f"Deployment failed for {platform_name}")
                pub_url = res.get("asset_public_url", "")
                self.assertIn(expected_domain, pub_url, f"Expected domain {expected_domain} in {pub_url}")
                self.assertEqual(res.get("service_key"), service_key)

                screenshots = res.get("screenshots", [])
                self.assertEqual(len(screenshots), 4, f"Expected 4 screenshots for {platform_name}, got {len(screenshots)}")

    def test_06_checkpoint_screenshots_exist_and_non_zero_sizes(self):
        """
        Verifies that all 4-checkpoint screenshots for all 5 platforms exist on disk,
        have non-zero byte size, and begin with valid PNG magic headers.
        """
        platforms = [
            ("carrd_landing_page", "carrd"),
            ("strikingly_landing_page", "strikingly"),
            ("webflow_landing_page", "webflow"),
            ("notion_site_landing_page", "notion"),
            ("canva_site_landing_page", "canva"),
        ]

        expected_checkpoints = [
            "01_builder_initialized.png",
            "02_embeds_injected.png",
            "03_metadata_and_cta.png",
            "04_published_live.png",
        ]
        png_magic = b"\x89PNG\r\n\x1a\n"

        for folder_name, plat_prefix in platforms:
            folder = REPO_ROOT / "assets" / "evidence" / "automation_runs" / folder_name
            self.assertTrue(folder.exists(), f"Evidence folder missing: {folder}")

            for cp_name in expected_checkpoints:
                with self.subTest(platform=folder_name, checkpoint=cp_name):
                    file_path = folder / f"{plat_prefix}_{cp_name}"
                    self.assertTrue(file_path.exists(), f"Screenshot file missing on disk: {file_path}")
                    size = file_path.stat().st_size
                    self.assertGreater(size, 0, f"Screenshot file is 0 bytes: {file_path}")

                    # Verify binary PNG header
                    with open(file_path, "rb") as f:
                        header = f.read(8)
                    self.assertEqual(header, png_magic, f"Invalid PNG magic bytes in: {file_path}")

    # ==========================================================================
    # Task 2: CLI Interface Verification
    # ==========================================================================

    def test_07_cli_carrd_cctv_execution(self):
        """CLI execution: python browser_ui_worker.py --deploy-landing-page Carrd --service-key cctv"""
        cmd = [
            self.python_bin,
            str(REPO_ROOT / "browser_ui_worker.py"),
            "--deploy-landing-page", "Carrd",
            "--service-key", "cctv"
        ]
        proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, f"CLI exited with {proc.returncode}. Stderr: {proc.stderr}")

        # Validate JSON output
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as e:
            self.fail(f"CLI output is not valid JSON: {e}\nOutput was: {proc.stdout}")

        self.assertEqual(data.get("status"), "SUCCESS")
        self.assertEqual(data.get("platform_name"), "Carrd")
        self.assertEqual(data.get("service_key"), "cctv")
        self.assertIn("carrd.co", data.get("asset_public_url", ""))
        self.assertEqual(len(data.get("screenshots", [])), 4)

    def test_08_cli_strikingly_starlink_execution(self):
        """CLI execution: python browser_ui_worker.py --deploy-landing-page Strikingly --service-key starlink"""
        cmd = [
            self.python_bin,
            str(REPO_ROOT / "browser_ui_worker.py"),
            "--deploy-landing-page", "Strikingly",
            "--service-key", "starlink"
        ]
        proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, f"CLI exited with {proc.returncode}. Stderr: {proc.stderr}")

        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as e:
            self.fail(f"CLI output is not valid JSON: {e}\nOutput was: {proc.stdout}")

        self.assertEqual(data.get("status"), "SUCCESS")
        self.assertEqual(data.get("platform_name"), "Strikingly")
        self.assertEqual(data.get("service_key"), "starlink")
        self.assertIn("mystrikingly.com", data.get("asset_public_url", ""))
        self.assertEqual(len(data.get("screenshots", [])), 4)

    def test_09_cli_invalid_service_key_handled_gracefully(self):
        """CLI execution with invalid service key: rejects with usage and non-zero exit."""
        cmd = [
            self.python_bin,
            str(REPO_ROOT / "browser_ui_worker.py"),
            "--deploy-landing-page", "Carrd",
            "--service-key", "invalid_service"
        ]
        proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=15)
        self.assertNotEqual(proc.returncode, 0, "CLI must exit with non-zero code on invalid service key")
        combined_output = proc.stdout + proc.stderr
        self.assertIn("invalid choice", combined_output)
        self.assertIn("invalid_service", combined_output)

    def test_10_cli_custom_subdomain_support(self):
        """CLI execution with custom --subdomain parameter."""
        sub = "adi-yorkshire-custom-test"
        cmd = [
            self.python_bin,
            str(REPO_ROOT / "browser_ui_worker.py"),
            "--deploy-landing-page", "Webflow",
            "--service-key", "tv",
            "--subdomain", sub
        ]
        proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, f"CLI exited with {proc.returncode}. Stderr: {proc.stderr}")

        data = json.loads(proc.stdout)
        self.assertEqual(data.get("status"), "SUCCESS")
        self.assertIn(f"https://{sub}.webflow.io", data.get("asset_public_url", ""))

    # ==========================================================================
    # Task 3: Doc3RegistryGuard Integration & 14-Column Invariant
    # ==========================================================================

    def test_11_doc3_14_column_layout_assertion(self):
        """Asserts that published_row_14col has strictly 14 items and conforms to schema."""
        manifest = self.worker.get_default_landing_page_manifest(service_key="alarms", platform_name="Notion Site")
        res = asyncio.run(self.worker.execute_landing_page_deployment(manifest, record_to_doc3=False))

        row = res.get("published_row_14col", [])
        self.assertEqual(len(row), 14, f"Expected 14 columns, got {len(row)}")

        expected_columns = [
            ("asset_id", 0, lambda v: v.startswith("LINK-")),
            ("parent_profile_id", 1, lambda v: v.startswith("PROF-SITE-")),
            ("platform_name", 2, lambda v: v == "Notion Site"),
            ("profile_live_url", 3, lambda v: "notion.site" in v),
            ("asset_title", 4, lambda v: len(v) > 10),
            ("asset_type", 5, lambda v: v == "Landing Page Stack"),
            ("asset_public_url", 6, lambda v: "notion.site" in v),
            ("top_of_stack_apex_url", 7, lambda v: "sites.google.com" in v),
            ("shield_target_url", 8, lambda v: "adicommunications.co.uk/ajax-alarm-installation/" in v),
            ("seo_tags", 9, lambda v: "#" in v),
            ("seo_description_summary", 10, lambda v: len(v) > 0 and len(v) <= 180),
            ("dofollow_status", 11, lambda v: v in ("Follow", "Nofollow")),
            ("publication_date", 12, lambda v: bool(re.match(r"^\d{4}-\d{2}-\d{2}$", v))),
            ("verification_status", 13, lambda v: v == "HTTP_200"),
        ]

        for col_name, idx, predicate in expected_columns:
            with self.subTest(column=col_name, index=idx):
                val = row[idx]
                self.assertTrue(predicate(val), f"Column {idx} ({col_name}) failed validation with value: '{val}'")

    def test_12_doc3_record_to_doc3_csv_isolated_registration(self):
        """Verifies that record_to_doc3 appends a valid 14-column row to CSV and increments LINK ID."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", encoding="utf-8") as tmp:
            tmp_path = Path(tmp.name)
            tmp.write(
                "asset_id,parent_profile_id,platform_name,profile_live_url,asset_title,asset_type,"
                "asset_public_url,top_of_stack_apex_url,shield_target_url,seo_tags,seo_description_summary,"
                "dofollow_status,publication_date,verification_status\n"
            )
            # Add initial row
            tmp.write(
                "LINK-0100,PROF-CCTV-01,YouTube,https://youtube.com/@cctv,CCTV Video,Video,"
                "https://youtube.com/watch?v=123,https://youtube.com/@cctv,https://adicommunications.co.uk/cctv-installation/,"
                "#cctv,CCTV guide,Follow,2026-10-23,HTTP_200\n"
            )

        try:
            # Register asset using Doc3RegistryGuard
            manifest = self.worker.get_default_landing_page_manifest(service_key="cabling", platform_name="Carrd")
            entry = {
                "parent_profile_id": "PROF-SITE-CABLING",
                "platform_name": "Carrd",
                "profile_live_url": "https://adi-cabling.carrd.co",
                "asset_title": manifest.page_title,
                "asset_type": "Landing Page Stack",
                "asset_public_url": "https://adi-cabling.carrd.co",
                "top_of_stack_apex_url": manifest.google_site_apex_url,
                "shield_target_url": manifest.downward_service_url,
                "seo_tags": manifest.tags,
                "seo_description_summary": manifest.meta_description[:180],
                "dofollow_status": "Follow",
                "publication_date": "2026-10-23",
                "verification_status": "HTTP_200"
            }

            next_id = Doc3RegistryGuard.get_next_asset_id(tmp_path)
            self.assertEqual(next_id, "LINK-0101")

            registered_id = Doc3RegistryGuard.register_asset(tmp_path, entry)
            self.assertEqual(registered_id, "LINK-0101")

            with open(tmp_path, "r", encoding="utf-8") as f:
                reader = list(csv.reader(f))
                self.assertEqual(len(reader), 3)  # header + 1 existing + 1 new
                new_row = reader[2]
                self.assertEqual(len(new_row), 14, f"Registered row did not have 14 columns: {len(new_row)}")
                self.assertEqual(new_row[0], "LINK-0101")
                self.assertEqual(new_row[5], "Landing Page Stack")
                self.assertEqual(new_row[13], "HTTP_200")
        finally:
            if tmp_path.exists():
                os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
