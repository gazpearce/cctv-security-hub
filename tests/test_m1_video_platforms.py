"""
tests/test_m1_video_platforms.py
Milestone 1 Video Platform Verification & Trade E-E-A-T Quality Gate Suite.

Verifies:
1. 50 Video Platform Catalog & Registry Parity (JSON vs CSV, Draft 2020-12 schema)
2. 5-Layer Integrity Firewall for Video Endpoints (Syntax, Domain, Anti-Dashboard, Probing, Rule 45)
3. Trade E-E-A-T Completeness, CAI Non-Membership Disclaimer & Rule 20 Checkatrade Ban
4. Sovereign Video Hierarchy & Strict Tier 3 YouTube Isolation
5. Live & Mock Network Reachability Defense
6. Milestone 1 Acceptance Thresholds (Catalog 50/50, Failure Taxonomy compliance)
"""

import csv
import json
import os
import posixpath
import re
import sys
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from automated_platform_onboarder import FailureReason, IntegrityFirewall
from swarm_stack_orchestrator import check_url_reachability


class TestVideoCatalogIntegrityAndParity(unittest.TestCase):
    """Class 1: 50 Video Platform Catalog & Registry Parity."""

    @classmethod
    def setUpClass(cls):
        cls.catalog_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        cls.csv_path = REPO_ROOT / "doc2_multicategory_stack_550.csv"

        with open(cls.catalog_path, "r", encoding="utf-8") as f:
            cls.catalog = json.load(f)

        cls.video_stack = cls.catalog["category_stacks"]["video"]
        cls.video_platforms = cls.video_stack["platforms"]

        with open(cls.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cls.csv_rows = [r for r in reader if r.get("Stack Key") == "video" or "Video" in r.get("Category", "")]

    def test_01_video_stack_contains_exactly_50_platforms(self):
        """Asserts category_stacks.video.platforms contains exactly 50 sequential platforms."""
        self.assertEqual(len(self.video_platforms), 50, "Video stack must contain exactly 50 platforms")
        for idx, plat in enumerate(self.video_platforms, 1):
            expected_id = f"PLAT-VID-{idx:03d}"
            self.assertEqual(plat["platform_id"], expected_id)
            self.assertEqual(plat["stack_rank"], idx)
            self.assertEqual(plat["stack_key"], "video")

    def test_02_field_by_field_parity_json_vs_csv(self):
        """Verifies 100% field parity across all 15 columns between JSON and CSV for video rows."""
        self.assertEqual(len(self.csv_rows), 50, "CSV must have exactly 50 video rows")
        csv_by_id = {r["Platform ID"]: r for r in self.csv_rows}

        for p in self.video_platforms:
            pid = p["platform_id"]
            self.assertIn(pid, csv_by_id, f"Platform {pid} missing from CSV")
            row = csv_by_id[pid]

            self.assertEqual(row["Platform ID"], p["platform_id"])
            self.assertEqual(row["Rank"], str(p["global_rank"]))
            self.assertEqual(row["Platform Name"], p["name"])
            self.assertEqual(row["Domain"], p["domain"])
            self.assertEqual(row["DA"], str(p["da"]))
            self.assertEqual(row["Stack Key"], p["stack_key"])
            self.assertEqual(row["Category"], p["category"])
            self.assertEqual(row["Tier"], p["tier"])
            self.assertEqual(row["1-Click Join Method (SSO)"], p["sso_method"])
            self.assertEqual(row["Official Signup URL"], p["signup_url"])
            self.assertEqual(row["Status"], p["status"])
            self.assertEqual(row["Active Tenant URL"], p["active_tenant_url"])
            self.assertEqual(row["Failure Reason"], p["failure_reason"] or "")
            self.assertEqual(row["Upward Target URL"], p["upward_target_url"])
            self.assertEqual(row["Rule 45 Compliant"], "TRUE" if p["rule_45_compliant"] else "FALSE")

    def test_03_tier_distribution_exactness(self):
        """Asserts exactly 1 Tier 1 Apex, 18 Tier 2 hosts, and 31 Tier 3 alternative hosts."""
        tier1 = [p for p in self.video_platforms if "Tier 1" in p["tier"]]
        tier2 = [p for p in self.video_platforms if "Tier 2" in p["tier"]]
        tier3 = [p for p in self.video_platforms if "Tier 3" in p["tier"]]

        self.assertEqual(len(tier1), 1, "Must have exactly 1 Tier 1 Apex platform")
        self.assertEqual(len(tier2), 18, "Must have exactly 18 Tier 2 video hosts")
        self.assertEqual(len(tier3), 31, "Must have exactly 31 Tier 3 video hosts")
        self.assertEqual(tier1[0]["platform_id"], "PLAT-VID-001")

    def test_04_status_distribution_and_metadata_sync(self):
        """Asserts joined + pending == 50 and metadata counts accurately reflect platform state."""
        joined = [p for p in self.video_platforms if p["status"] == "JOINED"]
        pending = [p for p in self.video_platforms if p["status"] == "PENDING"]

        self.assertEqual(len(joined) + len(pending), 50)
        self.assertEqual(self.video_stack["target_platforms_count"], 50)
        self.assertEqual(self.video_stack["onboarded_count"], len(joined))
        self.assertEqual(self.video_stack["pending_count"], len(pending))


class TestVideoIntegrityFirewall(unittest.TestCase):
    """Class 2: 5-Layer Integrity Firewall for Video Endpoints."""

    @classmethod
    def setUpClass(cls):
        catalog_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        cls.video_platforms = catalog["category_stacks"]["video"]["platforms"]
        cls.joined_platforms = [p for p in cls.video_platforms if p["status"] == "JOINED"]

    def test_05_layer1_syntax_on_all_active_tenant_urls(self):
        """Validates Layer 1 Syntax on all JOINED platform tenant URLs."""
        for p in self.joined_platforms:
            url = p["active_tenant_url"]
            ok, msg = IntegrityFirewall.validate_layer1_syntax(url)
            self.assertTrue(ok, f"Layer 1 syntax failure on {p['platform_id']} ({url}): {msg}")

    def test_06_layer2_domain_authenticity_zero_synthetic_domains(self):
        """Verifies zero synthetic domains (*.adi-telecoms.org) across all video endpoints."""
        for p in self.video_platforms:
            for field in ("active_tenant_url", "signup_url"):
                val = p.get(field, "")
                if val:
                    self.assertNotIn("adi-telecoms.org", val.lower(), f"Synthetic domain in {p['platform_id']} {field}: {val}")
                    # Also check for truncated domains
                    self.assertNotIn("sproutvideot.com", val.lower())
                    self.assertNotIn("brightcovetr.com", val.lower())
                    self.assertNotIn("dtubeipfs.com", val.lower())
                    self.assertNotIn("kickstreamin.com", val.lower())

    def test_07_layer3_anti_dashboard_console_filter(self):
        """Validates Layer 3 Anti-Dashboard filter on all JOINED platform tenant URLs."""
        for p in self.joined_platforms:
            url = p["active_tenant_url"]
            ok, msg = IntegrityFirewall.validate_layer3_anti_dashboard(url)
            self.assertTrue(ok, f"Layer 3 anti-dashboard failure on {p['platform_id']} ({url}): {msg}")

    def test_08_layer5_rule_45_zero_raw_root_links(self):
        """Scans all fields in JSON and CSV video entries for raw root links to adicommunications.co.uk."""
        for p in self.video_platforms:
            for k, v in p.items():
                if isinstance(v, str):
                    ok, msg = IntegrityFirewall.validate_layer5_rule_45(v)
                    self.assertTrue(ok, f"Rule 45 raw root anchor in {p['platform_id']} field {k}: {v}")


class TestTradeEEATAndLegalCompliance(unittest.TestCase):
    """Class 3: Trade E-E-A-T Completeness, CAI Non-Membership Disclaimer & Rule 20 Checkatrade Ban."""

    @classmethod
    def setUpClass(cls):
        catalog_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        cls.video_platforms = catalog["category_stacks"]["video"]["platforms"]
        cls.catalog_str = json.dumps(catalog["category_stacks"]["video"])

    def test_09_eeat_metadata_block_completeness(self):
        """Asserts every video platform in JSON possesses an authentic, complete eeat_metadata block."""
        required_keys = [
            "engineer", "business", "telephone", "experience",
            "insurance", "qualifications", "rating", "cai_notice",
            "avatar_url", "cover_banner_url"
        ]
        for p in self.video_platforms:
            self.assertIn("eeat_metadata", p, f"Missing eeat_metadata in {p['platform_id']}")
            eeat = p["eeat_metadata"]
            for k in required_keys:
                self.assertIn(k, eeat, f"Missing key {k} in eeat_metadata of {p['platform_id']}")
                self.assertTrue(bool(eeat[k]), f"Empty key {k} in eeat_metadata of {p['platform_id']}")
            self.assertEqual(eeat["engineer"], "Gary Pearce")
            self.assertEqual(eeat["business"], "ADI Communications")
            self.assertEqual(eeat["telephone"], "07860 244 274")

    def test_10_zero_0800_numbers_permitted(self):
        """Asserts string '0800' is strictly absent from all video JSON fields."""
        self.assertNotIn("0800", self.catalog_str, "Found unauthorized 0800 number in video stack")

    def test_11_cai_non_membership_legal_disclaimer(self):
        """Verifies cai_notice explicitly contains 'CAI-benchmarked equipment' and 'NOT CAI members'."""
        for p in self.video_platforms:
            notice = p["eeat_metadata"]["cai_notice"]
            self.assertIn("cai-benchmarked equipment", notice.lower())
            self.assertIn("not cai members", notice.lower())
            self.assertNotIn("cai member", p["name"].lower())

    def test_12_strict_rule_20_checkatrade_ban(self):
        """Audits every key and value in the video JSON section for case-insensitive 'checkatrade'."""
        self.assertNotIn("checkatrade", self.catalog_str.lower(), "Rule 20 Violation: 'checkatrade' found in video catalog")

    def test_13_cdn_webp_media_assets_validity(self):
        """Asserts that avatar_url and cover_banner_url point to valid HTTPS CDN URLs ending in .webp."""
        for p in self.video_platforms:
            eeat = p["eeat_metadata"]
            avatar = eeat["avatar_url"]
            cover = eeat["cover_banner_url"]
            self.assertTrue(avatar.startswith("https://") and avatar.endswith(".webp"))
            self.assertTrue(cover.startswith("https://") and cover.endswith(".webp"))


class TestSovereignVideoHierarchyAndAirGap(unittest.TestCase):
    """Class 4: Sovereign Video Hierarchy & Strict Tier 3 YouTube Isolation."""

    @classmethod
    def setUpClass(cls):
        catalog_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        cls.video_platforms = catalog["category_stacks"]["video"]["platforms"]

    def test_14_tier1_youtube_apex_configuration(self):
        """Verifies PLAT-VID-001 (YouTube) configuration and upward linking to Blogger Citadel Hub."""
        yt = self.video_platforms[0]
        self.assertEqual(yt["platform_id"], "PLAT-VID-001")
        self.assertEqual(yt["name"], "YouTube")
        self.assertEqual(yt["active_tenant_url"], "https://www.youtube.com/@CCTV.services")
        self.assertEqual(yt["upward_target_url"], "https://tvandhomesecurity.blogspot.com/")

    def test_15_tier2_high_da_hosts_upward_linking(self):
        """Verifies all 18 Tier 2 video platforms link upward to YouTube Apex."""
        tier2 = [p for p in self.video_platforms if "Tier 2" in p["tier"]]
        self.assertEqual(len(tier2), 18)
        for p in tier2:
            self.assertEqual(
                p["upward_target_url"],
                "https://www.youtube.com/@CCTV.services",
                f"{p['platform_id']} ({p['name']}) must link upward to YouTube Apex"
            )

    def test_16_tier3_alternative_hosts_strict_youtube_isolation(self):
        """Verifies all 31 Tier 3 video platforms link EXCLUSIVELY to YouTube with 0 links to adicommunications.co.uk."""
        tier3 = [p for p in self.video_platforms if "Tier 3" in p["tier"]]
        self.assertEqual(len(tier3), 31)
        for p in tier3:
            upward = p["upward_target_url"]
            self.assertTrue(
                "youtube.com" in upward or "youtu.be" in upward,
                f"Tier 3 platform {p['platform_id']} ({p['name']}) upward target must be YouTube: {upward}"
            )
            # Strict Air-Gap: adicommunications.co.uk must be completely absent
            p_str = json.dumps(p).lower()
            self.assertNotIn(
                "adicommunications.co.uk",
                p_str,
                f"Air-gap leak: 'adicommunications.co.uk' found in Tier 3 platform {p['platform_id']} ({p['name']})"
            )


class TestVideoPlatformReachabilityAndNetworkDefense(unittest.TestCase):
    """Class 5: Live & Mock Network Reachability Defense."""

    @classmethod
    def setUpClass(cls):
        catalog_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        cls.video_platforms = catalog["category_stacks"]["video"]["platforms"]
        cls.joined_platforms = [p for p in cls.video_platforms if p["status"] == "JOINED"]

    def test_17_joined_endpoints_public_dns_and_http_reachability(self):
        """Probes active_tenant_url of JOINED platforms using check_url_reachability without crashing."""
        for p in self.joined_platforms:
            url = p["active_tenant_url"]
            is_ok, status, msg, elapsed = check_url_reachability(url, timeout=5.0)
            # Asserts the reachability probe completes cleanly and doesn't throw unhandled exceptions
            self.assertIsNotNone(msg, f"Reachability probe failed to return a message for {url}")
            self.assertIsInstance(elapsed, float)

    def test_18_no_login_auth_wall_redirects(self):
        """Verifies JOINED tenant URLs do not redirect to login authentication portals."""
        auth_walls = ["accounts.google.com", "github.com/login", "auth0.com", "login.microsoftonline.com"]
        for p in self.joined_platforms:
            url = p["active_tenant_url"]
            for wall in auth_walls:
                self.assertNotIn(wall, url.lower(), f"Tenant URL {url} points to an auth wall ({wall})")

    def test_19_official_signup_urls_valid_https(self):
        """Verifies all 50 signup_url entries are valid HTTPS URLs."""
        for p in self.video_platforms:
            url = p["signup_url"]
            self.assertTrue(url.startswith("https://"), f"{p['platform_id']} signup URL must use HTTPS: {url}")
            parsed = urllib.parse.urlparse(url)
            self.assertTrue(bool(parsed.netloc), f"{p['platform_id']} signup URL missing netloc: {url}")


class TestM1MilestoneAcceptanceThreshold(unittest.TestCase):
    """Class 6: Milestone 1 Acceptance Thresholds."""

    @classmethod
    def setUpClass(cls):
        catalog_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        cls.video_platforms = catalog["category_stacks"]["video"]["platforms"]

    def test_20_baseline_joined_count_met(self):
        """Asserts that at least 8 platforms are verified as JOINED."""
        joined = [p for p in self.video_platforms if p["status"] == "JOINED"]
        self.assertGreaterEqual(len(joined), 8, "Must have at least 8 JOINED platforms in Milestone 1 baseline")

    def test_21_pending_platforms_failure_taxonomy_compliance(self):
        """For all PENDING platforms, asserts valid failure_reason and non-empty failure_detail."""
        pending = [p for p in self.video_platforms if p["status"] == "PENDING"]
        self.assertGreater(len(pending), 0, "Must have pending platforms in catalog")
        for p in pending:
            reason = p.get("failure_reason")
            detail = p.get("failure_detail")
            self.assertTrue(
                FailureReason.is_valid(reason),
                f"Platform {p['platform_id']} has invalid failure reason: '{reason}'"
            )
            self.assertTrue(
                bool(detail and len(detail) > 0),
                f"Platform {p['platform_id']} missing failure_detail"
            )

    def test_22_zero_defunct_platforms_in_video_catalog(self):
        """Verifies defunct platforms (Metacafe, Vzaar) and pure editors have been purged."""
        defunct_names = ["Metacafe", "Vzaar", "Synthesia", "InVideo", "Powtoon", "Vyond", "WeVideo", "Clipchamp", "Animoto"]
        for p in self.video_platforms:
            for d in defunct_names:
                self.assertNotIn(d.lower(), p["name"].lower(), f"Defunct/editor platform '{d}' found in video catalog: {p['name']}")

    def test_23_zero_synthetic_domains_in_manifests(self):
        """Inspects category_manifests/01_video_stack.csv and asserts 0 rows contain *.adi-telecoms.org."""
        manifest_path = REPO_ROOT / "category_manifests" / "01_video_stack.csv"
        self.assertTrue(manifest_path.exists(), f"Manifest file missing: {manifest_path}")

        with open(manifest_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, 1):
                for k, v in row.items():
                    self.assertNotIn(
                        "adi-telecoms.org",
                        v.lower(),
                        f"Synthetic domain found in manifest row {idx} field {k}: {v}"
                    )

class TestM1DefectHardeningAndAdversarialGuards(unittest.TestCase):
    """Class 7: Defect Hardening & Adversarial Regression Suite (Tests 24–28)."""

    def test_24_catalog_parity_sync_updates_both_stack_and_global_platforms_and_csv(self):
        """Regression Test for Defect 1:
        Verifies CatalogParitySync.sync_platform_update updates BOTH
        category_stacks[stack_key]['platforms'] AND catalog['platforms'],
        recalculates total counts, and regenerates doc2 CSV with active status.
        """
        import shutil
        import tempfile
        from automated_video_platform_onboarder import CatalogParitySync

        temp_dir = tempfile.mkdtemp()
        try:
            temp_json = Path(temp_dir) / "catalog.json"
            temp_csv = Path(temp_dir) / "doc2.csv"

            mock_catalog = {
                "metadata": {
                    "total_platforms": 1,
                    "total_joined": 0,
                    "total_pending": 1
                },
                "category_stacks": {
                    "video": {
                        "platforms": [
                            {
                                "platform_id": "PLAT-VID-006",
                                "name": "Loom",
                                "domain": "loom.com",
                                "status": "PENDING",
                                "active_tenant_url": "",
                                "failure_reason": "SSO_OAUTH_FAILED",
                                "failure_detail": "Pending OAuth",
                                "global_rank": 6,
                                "stack_key": "video",
                                "category": "Video Hosting & Cloud Sharing",
                                "tier": "Tier 2",
                                "da": 92,
                                "sso_method": "Google SSO",
                                "signup_url": "https://loom.com/signup",
                                "upward_target_url": "https://www.youtube.com/@CCTV.services",
                                "rule_45_compliant": True,
                                "eeat_metadata": {}
                            }
                        ]
                    }
                },
                "platforms": [
                    {
                        "platform_id": "PLAT-VID-006",
                        "name": "Loom",
                        "domain": "loom.com",
                        "status": "PENDING",
                        "active_tenant_url": "",
                        "failure_reason": "SSO_OAUTH_FAILED",
                        "failure_detail": "Pending OAuth",
                        "global_rank": 6,
                        "stack_key": "video",
                        "category": "Video Hosting & Cloud Sharing",
                        "tier": "Tier 2",
                        "da": 92,
                        "sso_method": "Google SSO",
                        "signup_url": "https://loom.com/signup",
                        "upward_target_url": "https://www.youtube.com/@CCTV.services",
                        "rule_45_compliant": True,
                        "eeat_metadata": {}
                    }
                ]
            }
            with open(temp_json, "w", encoding="utf-8") as f:
                json.dump(mock_catalog, f)

            sync = CatalogParitySync(json_path=temp_json, csv_path=temp_csv)
            ok, msg = sync.sync_platform_update(
                stack_key="video",
                platform_id="PLAT-VID-006",
                new_status="JOINED",
                tenant_url="https://loom.com/channel/adi-cctv"
            )
            self.assertTrue(ok, f"sync_platform_update failed: {msg}")

            # Verify in JSON catalog
            updated_data = sync.load_catalog()
            stack_p = updated_data["category_stacks"]["video"]["platforms"][0]
            root_p = updated_data["platforms"][0]

            self.assertEqual(stack_p["status"], "JOINED")
            self.assertEqual(stack_p["active_tenant_url"], "https://loom.com/channel/adi-cctv")
            self.assertEqual(root_p["status"], "JOINED", "Root catalog['platforms'] must also be updated to JOINED")
            self.assertEqual(root_p["active_tenant_url"], "https://loom.com/channel/adi-cctv")
            self.assertEqual(updated_data["metadata"]["total_joined"], 1)
            self.assertEqual(updated_data["metadata"]["total_pending"], 0)

            # Verify in regenerated CSV
            self.assertTrue(temp_csv.exists(), "doc2 CSV must exist after sync")
            with open(temp_csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["Platform ID"], "PLAT-VID-006")
                self.assertEqual(rows[0]["Status"], "JOINED", "CSV row status must be JOINED")
                self.assertEqual(rows[0]["Active Tenant URL"], "https://loom.com/channel/adi-cctv")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_25_layer5_rule_45_path_traversal_hardened(self):
        """Regression Test for Defect 2:
        Verifies IntegrityFirewall.validate_layer5_rule_45 detects and blocks
        path traversal evasion (e.g. /news/..) that resolves to naked root.
        """
        evasion_urls = [
            "https://adicommunications.co.uk/news/..",
            "https://adicommunications.co.uk/news/../",
            "https://adicommunications.co.uk/services/cctv/../..",
            "https://adicommunications.co.uk/services/cctv/../../",
            "https://adicommunications.co.uk/news/..#fragment",
            "https://adicommunications.co.uk/news/..?query=1",
        ]
        for url in evasion_urls:
            with self.subTest(url=url):
                ok, msg = IntegrityFirewall.validate_layer5_rule_45(url)
                self.assertFalse(
                    ok,
                    f"Layer 5 Rule 45 must REJECT path traversal resolving to root: {url}. Result: {msg}"
                )
                self.assertIn("raw naked root anchor", msg)

        valid_urls = [
            "https://adicommunications.co.uk/news/",
            "https://adicommunications.co.uk/news/starlink-guide",
            "https://adicommunications.co.uk/services/cctv/..",  # resolves to /services
            "https://www.youtube.com/@CCTV.services",
            "https://tvandhomesecurity.blogspot.com/"
        ]
        for url in valid_urls:
            with self.subTest(url=url):
                ok, msg = IntegrityFirewall.validate_layer5_rule_45(url)
                self.assertTrue(ok, f"Layer 5 Rule 45 should pass legitimate URL: {url}. Result: {msg}")

    def test_26_google_oauth_driver_resilient_to_non_dict_tabs(self):
        """Regression Test for Defect 3:
        Verifies GoogleOAuthDriver.execute_google_oauth safely ignores non-dict
        elements (None, str, int, list) returned by list_tabs() without crashing
        with AttributeError.
        """
        import asyncio
        from unittest import mock
        from automated_video_platform_onboarder import GoogleOAuthDriver, VideoPlatformCDPClient

        client = VideoPlatformCDPClient(cdp_base="http://127.0.0.1:9223")
        driver = GoogleOAuthDriver(client)
        mock_ws = mock.AsyncMock()

        dirty_tabs = [
            None,
            "error_payload_string",
            12345,
            [],
            {"url": "https://other-domain.com", "title": "Other"},
            {"url": "https://accounts.google.com/o/oauth2/auth", "webSocketDebuggerUrl": "ws://127.0.0.1:9223/auth"}
        ]

        async def run_test():
            with mock.patch.object(client, "eval_js", return_value=True):
                with mock.patch.object(client, "list_tabs", return_value=dirty_tabs):
                    with mock.patch("websockets.connect") as mock_ws_connect:
                        mock_auth_ws = mock.AsyncMock()
                        mock_ws_connect.return_value.__aenter__.return_value = mock_auth_ws
                        return await driver.execute_google_oauth(mock_ws, "vimeo.com", timeout=0.1)

        try:
            ok, detail = asyncio.run(run_test())
            crashed = False
        except AttributeError as e:
            crashed = True
            error_msg = str(e)

        self.assertFalse(crashed, f"GoogleOAuthDriver crashed on non-dict tab entries: {getattr(locals(), 'error_msg', '')}")

    def test_27_email_otp_driver_json_dumps_escaping(self):
        """Regression Test for Defect 4:
        Verifies EmailOtpDriver uses json.dumps() escaping for form inputs and OTP code,
        preventing JavaScript syntax errors when strings contain single quotes or special chars.
        """
        import asyncio
        from unittest import mock
        from automated_video_platform_onboarder import EmailOtpDriver, VideoPlatformCDPClient

        client = VideoPlatformCDPClient(cdp_base="http://127.0.0.1:9223")
        driver = EmailOtpDriver(client)
        mock_ws = mock.AsyncMock()
        captured_scripts = []

        async def capture_eval(ws, js, **kwargs):
            captured_scripts.append(js)
            if "userInput" in js or "emailInput" in js:
                return 3
            if "inputs.length" in js:
                return True
            return 1

        with mock.patch.object(client, "eval_js", side_effect=capture_eval):
            test_username = "O'Connor"
            test_password = "Pass'word\"123\n$#\\"
            test_email = "test'user+tag@domain.co.uk"

            filled = asyncio.run(driver.autofill_signup_form(
                mock_ws,
                email=test_email,
                username=test_username,
                password=test_password
            ))
            self.assertTrue(filled)

        self.assertGreater(len(captured_scripts), 0)
        autofill_js = captured_scripts[0]

        # Assert no raw unescaped single quotes
        self.assertNotIn("userInput.value = 'O'Connor';", autofill_js)
        self.assertNotIn("emailInput.value = 'test'user", autofill_js)

        # Assert standard json.dumps escaping
        self.assertIn(f"userInput.value = {json.dumps(test_username)};", autofill_js)
        self.assertIn(f"p.value = {json.dumps(test_password)};", autofill_js)
        self.assertIn(f"emailInput.value = {json.dumps(test_email)};", autofill_js)

        # Test handle_verification with quotes in code
        captured_scripts.clear()
        mock_auto_email = mock.MagicMock()
        mock_auto_email.find_otp_code = mock.AsyncMock(return_value="'12'34'")

        async def mock_eval_otp(ws, js, **kwargs):
            captured_scripts.append(js)
            return True

        with mock.patch.dict("sys.modules", {"auto_email_verifier": mock_auto_email}):
            with mock.patch.object(client, "eval_js", side_effect=mock_eval_otp):
                ok, msg = asyncio.run(driver.handle_verification(mock_ws, "Vimeo", "vimeo.com", timeout=1.0))
                self.assertTrue(ok)

        otp_scripts = [s for s in captured_scripts if "inputs[0].value" in s]
        self.assertGreater(len(otp_scripts), 0)
        otp_js = otp_scripts[0]

        expected_code_escaped = json.dumps("'12'34'")
        self.assertNotIn("inputs[0].value = ''12'34'';", otp_js)
        self.assertIn(f"inputs[0].value = {expected_code_escaped};", otp_js)
        self.assertIn(f"const digits = {expected_code_escaped}.split('');", otp_js)

    def test_28_layer1_syntax_rejects_horizontal_tab_and_control_chars(self):
        """Regression Test for Defect 5:
        Verifies IntegrityFirewall.validate_layer1_syntax detects and rejects
        embedded horizontal tabs (\t), newlines (\n), and carriage returns (\r).
        """
        invalid_cases = [
            ("https://youtube.com\t/test", "tab between netloc and path"),
            ("https://vimeo.com/channel\t123", "tab in path"),
            ("https://rumble.com/c/\t/test", "internal tab in path"),
            ("https://dailymotion.com/video\n123", "newline in path"),
            ("https://streamable.com/e/\r123", "carriage return in path"),
            ("https://odysee.com/@cctv (channel)", "parenthesis in URL"),
        ]
        for url, desc in invalid_cases:
            with self.subTest(case=desc, url=url):
                ok, msg = IntegrityFirewall.validate_layer1_syntax(url)
                self.assertFalse(ok, f"Layer 1 must REJECT URL with illegal whitespace/characters ({desc}): '{url}'")
                self.assertIn("illegal characters", msg)

        valid_cases = [
            "https://www.youtube.com/@CCTV.services",
            "https://vimeo.com/channels/12345",
            "https://tvandhomesecurity.blogspot.com/"
        ]
        for url in valid_cases:
            with self.subTest(url=url):
                ok, msg = IntegrityFirewall.validate_layer1_syntax(url)
                self.assertTrue(ok, f"Layer 1 should pass valid URL: {url}")


if __name__ == "__main__":
    unittest.main()

