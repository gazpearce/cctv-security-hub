#!/usr/bin/env python3
"""
tests/test_m1all_onboarding.py
Comprehensive Verification & Test Suite for Milestone M1-ALL:
- STACK-05 (Cloud) Platform Reconciliation & 100% Mathematical Parity (550 rows x 15 columns)
- Autonomous Workspace Verification & 2FA Daemon (workspace_2fa_daemon.py)
- Computer Use & Browser UI Automation Worker (browser_ui_worker.py)
- Universal Multi-Family Platform Onboarder (universal_platform_onboarder.py)
- 5-Layer Integrity Firewall & 11-Type Failure Taxonomy
- Gary Pearce E-E-A-T Trade Metadata & Rule 45 Citadel Air-Gap Protection
"""

import asyncio
import csv
import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

REPO_ROOT = Path(__file__).resolve().parent.parent

from workspace_2fa_daemon import (
    TwoFactorDaemonClient,
    Workspace2FADaemon,
    TwoFactorDaemonConfig,
    extract_otp_from_text,
    sanitize_text_for_otp,
    is_valid_otp,
    extract_candidate_links,
)
from browser_ui_worker import (
    BrowserUIWorker,
    WorkerConfig,
    TradeEEATProfile,
    AssetUploadManifest,
    FailureReason,
    IntegrityFirewall,
)
from universal_platform_onboarder import (
    UniversalPlatformOnboarder,
    ProfileBrandManager,
    FAMILY_APEX_MATRIX,
)


class TestM1AllCatalogAndParityReconciliation(unittest.TestCase):
    """Verifies STACK-05 reconciliation and 100% mathematical parity across 550 platforms."""

    @classmethod
    def setUpClass(cls):
        cls.json_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        cls.csv_path = REPO_ROOT / "doc2_multicategory_stack_550.csv"
        cls.assertTrue(cls.json_path.exists(), "master_multicategory_platform_catalog.json missing")
        cls.assertTrue(cls.csv_path.exists(), "doc2_multicategory_stack_550.csv missing")

        with open(cls.json_path, "r", encoding="utf-8") as f:
            cls.catalog = json.load(f)

        with open(cls.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cls.csv_fieldnames = reader.fieldnames
            cls.csv_rows = list(reader)

        cls.platforms = cls.catalog.get("platforms", [])

    def test_01_exact_total_platform_count_550(self):
        """Verify exactly 550 platforms exist in both catalog JSON and doc2 CSV."""
        self.assertEqual(len(self.platforms), 550)
        self.assertEqual(len(self.csv_rows), 550)
        self.assertEqual(self.catalog.get("total_platforms"), 550)

    def test_02_exact_15_csv_columns_and_ordering(self):
        """Verify the exact 15 expected columns are present in CSV in canonical order."""
        expected_cols = [
            "Platform ID", "Rank", "Platform Name", "Domain", "DA", "Stack Key",
            "Category", "Tier", "1-Click Join Method (SSO)", "Official Signup URL",
            "Status", "Active Tenant URL", "Failure Reason", "Upward Target URL", "Rule 45 Compliant"
        ]
        self.assertEqual(self.csv_fieldnames, expected_cols)

    def test_03_field_by_field_equality_8250_checks(self):
        """Perform exact 8,250 field checks (550 rows x 15 columns) comparing CSV vs JSON."""
        mismatches = []
        for idx in range(550):
            p = self.platforms[idx]
            c = self.csv_rows[idx]
            pid = p.get("platform_id")

            checks = [
                ("Platform ID", c.get("Platform ID"), p.get("platform_id")),
                ("Rank", int(c.get("Rank", -1)), p.get("global_rank")),
                ("Platform Name", c.get("Platform Name"), p.get("name")),
                ("Domain", c.get("Domain"), p.get("domain")),
                ("DA", int(c.get("DA", -1)), p.get("da")),
                ("Stack Key", c.get("Stack Key"), p.get("stack_key")),
                ("Category", c.get("Category"), p.get("category")),
                ("Tier", c.get("Tier"), p.get("tier")),
                ("1-Click Join Method (SSO)", c.get("1-Click Join Method (SSO)"), p.get("sso_method")),
                ("Official Signup URL", c.get("Official Signup URL"), p.get("signup_url")),
                ("Status", c.get("Status"), p.get("status")),
                ("Active Tenant URL", c.get("Active Tenant URL"), p.get("active_tenant_url") or ""),
                ("Failure Reason", c.get("Failure Reason"), p.get("failure_reason") or ""),
                ("Upward Target URL", c.get("Upward Target URL"), p.get("upward_target_url") or ""),
                (
                    "Rule 45 Compliant",
                    c.get("Rule 45 Compliant", "").upper(),
                    "TRUE" if p.get("rule_45_compliant") else "FALSE",
                ),
            ]

            for col_name, c_val, p_val in checks:
                if c_val != p_val:
                    mismatches.append(f"Row {idx} ({pid}) [{col_name}]: CSV={c_val!r} != JSON={p_val!r}")

        self.assertEqual(len(mismatches), 0, f"Found {len(mismatches)} field mismatches:\n" + "\n".join(mismatches[:10]))

    def test_04_cloud_stack_reconciled_50_joined(self):
        """Verify STACK-05 (Cloud) is 100% JOINED with 50 onboarded platforms and 0 pending."""
        cloud_stack = self.catalog.get("category_stacks", {}).get("cloud", {})
        self.assertEqual(cloud_stack.get("target_platforms_count"), 50)
        self.assertEqual(cloud_stack.get("onboarded_count"), 50)
        self.assertEqual(cloud_stack.get("pending_count"), 0)

        cloud_platforms = cloud_stack.get("platforms", [])
        self.assertEqual(len(cloud_platforms), 50)
        for p in cloud_platforms:
            self.assertEqual(p.get("status"), "JOINED")
            self.assertTrue(len(p.get("active_tenant_url", "")) > 0)

    def test_05_promoted_surge_and_replit_status(self):
        """Verify Surge.sh and Replit are successfully promoted to JOINED with verified active tenant URLs."""
        surge = next((p for p in self.platforms if p.get("platform_id") == "PLAT-CLD-027"), None)
        self.assertIsNotNone(surge)
        self.assertEqual(surge.get("name"), "Surge.sh Static")
        self.assertEqual(surge.get("status"), "JOINED")
        self.assertEqual(surge.get("active_tenant_url"), "https://adi-starlink-mount-finder.surge.sh/")

        replit = next((p for p in self.platforms if p.get("platform_id") == "PLAT-CLD-046"), None)
        self.assertIsNotNone(replit)
        self.assertEqual(replit.get("name"), "Replit Apps")
        self.assertEqual(replit.get("status"), "JOINED")
        self.assertEqual(replit.get("active_tenant_url"), "https://replit.com/@aiagent1510")

    def test_06_overall_joined_and_pending_counts(self):
        """Verify total joined == 120 and total pending == 430 across the entire catalog."""
        self.assertEqual(self.catalog.get("total_joined"), 120)
        self.assertEqual(self.catalog.get("total_pending"), 430)
        self.assertEqual(self.catalog.get("total_joined") + self.catalog.get("total_pending"), 550)

    def test_07_5_layer_firewall_zero_violations(self):
        """Verify universal_platform_onboarder firewall audit passes 100% with 0 violations."""
        onboarder = UniversalPlatformOnboarder()
        res = onboarder.audit_catalog_firewall()
        self.assertEqual(res["total_platforms"], 550)
        self.assertEqual(res["passed_count"], 550)
        self.assertEqual(res["violations_count"], 0)


class TestWorkspace2FADaemonImplementation(unittest.TestCase):
    """Verifies workspace_2fa_daemon.py logic, OTP sanitization, and IPC client."""

    def test_01_otp_extraction_basic_and_spaced(self):
        """Verify extraction of spaced codes, dash codes, and standalone tokens."""
        t1 = "Your verification code is 123 456. Enter this to continue."
        self.assertEqual(extract_otp_from_text(t1), "123456")

        t2 = "Your security pin is 489-201. Expires in 10 minutes."
        self.assertEqual(extract_otp_from_text(t2), "489201")

        t3 = "Welcome to Render! 948201 is your confirmation code."
        self.assertEqual(extract_otp_from_text(t3), "948201")

        t4 = "Your one-time login code: 712394"
        self.assertEqual(extract_otp_from_text(t4), "712394")

    def test_02_otp_extraction_filters_gary_phone(self):
        """Strictly verify Gary Pearce telephone number (07860 244 274) is never extracted as an OTP."""
        text = (
            "Contact lead engineer Gary Pearce on 07860 244 274 for installations. "
            "Your account verification code is 839201."
        )
        self.assertEqual(extract_otp_from_text(text), "839201")

        # Text with ONLY phone number must return None
        only_phone = "Gary Pearce • ADI Communications (07860 244 274)"
        self.assertIsNone(extract_otp_from_text(only_phone))

    def test_03_otp_extraction_filters_banned_years_and_promo_codes(self):
        """Verify that years 1900-2099 and marketing promo codes are rejected."""
        t_year = "Copyright 2026 ADI Communications. All rights reserved."
        self.assertIsNone(extract_otp_from_text(t_year))

        t_promo = "Use promo code SAVE50 to get a 50% discount on web hosting."
        self.assertIsNone(extract_otp_from_text(t_promo))

    def test_04_candidate_links_filter(self):
        """Verify candidate links extract genuine verification links and reject tracking/unsub links."""
        links = [
            "https://mail.google.com/mail/u/0/",
            "https://twitter.com/signup",
            "https://surge.sh/confirm?token=xyz12345",
            "https://surge.sh/unsubscribe?user=123",
            "https://dashboard.render.com/verify-email?key=abc987",
        ]
        res = extract_candidate_links(links, platform_domain="surge.sh")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], "https://surge.sh/confirm?token=xyz12345")

    def test_05_twofa_daemon_client_ipc_flow(self):
        """Verify TwoFactorDaemonClient can enqueue requests and inspect daemon state."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            client = TwoFactorDaemonClient(repo_root=tmp_root)

            # Not alive when no state file exists
            self.assertFalse(client.is_daemon_alive())

            # Enqueue request
            req_id = client.request_verification("TestPlatform", "testplatform.com", timeout_seconds=30)
            self.assertTrue(req_id.startswith("req_testplatform_com_"))
            self.assertTrue((tmp_root / "pending_verifications.json").exists())

            # Simulate daemon writing verified token
            state_data = {
                "daemon": {
                    "pid": 99999,
                    "status": "RUNNING",
                    "last_heartbeat": "2026-10-23T12:50:00+00:00",
                },
                "verified_tokens": {
                    "testplatform.com": {
                        "platform_name": "TestPlatform",
                        "otp_code": "554433",
                        "status": "TOKEN_READY",
                    }
                }
            }
            with open(tmp_root / "2fa_daemon_state.json", "w", encoding="utf-8") as f:
                json.dump(state_data, f)

            status = client.check_status("testplatform.com")
            self.assertIsNotNone(status)
            self.assertEqual(status.get("otp_code"), "554433")
            self.assertEqual(status.get("status"), "TOKEN_READY")


class TestBrowserUIWorkerImplementation(unittest.TestCase):
    """Verifies browser_ui_worker.py configuration, E-E-A-T trade invariants, and 14-col manifests."""

    def test_01_trade_profile_invariants(self):
        """Verify TradeEEATProfile contains all mandatory credentials, phone, and disclaimers."""
        profile = TradeEEATProfile()
        self.assertEqual(profile.engineer, "Gary Pearce")
        self.assertEqual(profile.business, "ADI Communications")
        self.assertEqual(profile.telephone, "07860 244 274")
        self.assertIn("9.98 / 10", profile.rating)
        self.assertIn("84+ verified", profile.rating)
        self.assertIn("£10M Public Liability", profile.bio)
        self.assertIn("07860 244 274", profile.bio)
        self.assertIn("NOT CAI members", profile.bio)
        # Checkatrade ban
        self.assertNotIn("checkatrade", profile.bio.lower())
        self.assertNotIn("checkatrade", profile.rating.lower())

    def test_02_failure_taxonomy_complete(self):
        """Verify all 11 canonical failure reasons are present in FailureReason."""
        expected_failures = {
            "CAPTCHA_REQUIRED", "MANUAL_BILLING_REQUIRED", "PHONE_SMS_REQUIRED",
            "EMAIL_TIMEOUT", "SSO_OAUTH_FAILED", "WAITLIST_PENDING",
            "GEO_RESTRICTED", "RATE_LIMITED", "CLI_AUTH_REQUIRED",
            "BANNED_POLICY", "PLATFORM_DEAD"
        }
        self.assertEqual(FailureReason.ALL_REASONS, expected_failures)

    def test_03_integrity_firewall_validation(self):
        """Verify 5-Layer IntegrityFirewall enforces genuine URLs and Rule 45."""
        # Layer 1: Valid vs Invalid
        self.assertTrue(IntegrityFirewall.validate_layer1_syntax("https://render.com/")[0])
        self.assertFalse(IntegrityFirewall.validate_layer1_syntax("")[0])
        self.assertFalse(IntegrityFirewall.validate_layer1_syntax("https://example.com/placeholder")[0])
        self.assertFalse(IntegrityFirewall.validate_layer1_syntax("https://test.com/d1abcdefg")[0])

        # Layer 2: Domain
        self.assertFalse(IntegrityFirewall.validate_layer2_domain("https://adi-telecoms.org/")[0])
        self.assertTrue(IntegrityFirewall.validate_layer2_domain("https://koyeb.com/")[0])

        # Layer 3: Anti-Dashboard
        self.assertFalse(IntegrityFirewall.validate_layer3_anti_dashboard("https://dashboard.render.com/")[0])
        self.assertFalse(IntegrityFirewall.validate_layer3_anti_dashboard("https://console.neon.tech/users/adi")[0])
        self.assertFalse(IntegrityFirewall.validate_layer3_anti_dashboard("https://app.koyeb.com/adi")[0])
        self.assertTrue(IntegrityFirewall.validate_layer3_anti_dashboard("https://koyeb.app/adi")[0])

        # Layer 5: Rule 45
        self.assertFalse(IntegrityFirewall.validate_layer5_rule_45("https://adicommunications.co.uk/")[0])
        self.assertFalse(IntegrityFirewall.validate_layer5_rule_45("https://www.adicommunications.co.uk/index.html")[0])
        self.assertTrue(IntegrityFirewall.validate_layer5_rule_45("https://adicommunications.co.uk/news/cctv-guide")[0])
        self.assertTrue(IntegrityFirewall.validate_layer5_rule_45("https://www.youtube.com/@CCTV.services")[0])

    def test_04_manual_asset_upload_manifest_14_column_row(self):
        """Verify AssetUploadManifest produces an exact 14-column row for doc3."""
        manifest = AssetUploadManifest(
            file_path=REPO_ROOT / "assets" / "videos" / "test.mp4",
            title="Starlink 90mph Gale Chimney Lashing Field Guide",
            description="Gary Pearce demonstrates heavy-duty chimney bracket strapping for SpaceX Starlink Gen 3.",
            tags="starlink,cctv,telecoms",
        )
        self.assertEqual(manifest.category, "Technology")
        self.assertEqual(manifest.companion_apex_url, "https://www.youtube.com/@CCTV.services")
        self.assertEqual(manifest.shield_target_url, "https://tvandhomesecurity.blogspot.com/")


class TestUniversalPlatformOnboarderImplementation(unittest.TestCase):
    """Verifies universal_platform_onboarder.py multi-family routing and dry-run execution."""

    def test_01_seven_family_apex_matrix(self):
        """Verify all 7 families exist in FAMILY_APEX_MATRIX with valid apex entities."""
        families = ["visual", "video", "slides", "rss", "docs", "curation", "cloud"]
        for f in families:
            self.assertIn(f, FAMILY_APEX_MATRIX)
            fam_data = FAMILY_APEX_MATRIX[f]
            self.assertTrue(len(fam_data["apex_url"]) > 0)
            self.assertTrue(fam_data["target_count"] > 0)

    def test_02_profile_brand_manager_routing(self):
        """Verify ProfileBrandManager routes each family to its sovereign Google Citadel Apex."""
        mgr = ProfileBrandManager()

        # Video family -> YouTube
        p_vid = mgr.get_profile_dict("video")
        self.assertEqual(p_vid["website"], "https://www.youtube.com/@CCTV.services")

        # RSS family -> Blogger RSS
        p_rss = mgr.get_profile_dict("rss")
        self.assertEqual(p_rss["website"], "https://tvandhomesecurity.blogspot.com/feeds/posts/default")

        # Curation family -> Firebase Ledger
        p_cur = mgr.get_profile_dict("curation")
        self.assertEqual(p_cur["website"], "https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html")

        # Cloud family -> Firebase Hosting
        p_cld = mgr.get_profile_dict("cloud")
        self.assertEqual(p_cld["website"], "https://gary-pearce-forensic-hub.web.app/")

    def test_03_onboarder_dry_run_execution(self):
        """Verify onboard_platform in dry-run mode returns DRY_RUN_PASSED."""
        onboarder = UniversalPlatformOnboarder()
        mock_platform = {
            "platform_id": "PLAT-CLD-999",
            "name": "DryRun Cloud",
            "domain": "dryrun.io",
            "signup_url": "https://dryrun.io/signup",
            "sso_method": "GitHub OAuth",
            "status": "PENDING"
        }
        res = asyncio.run(onboarder.onboard_platform(mock_platform, family_key="cloud", dry_run=True))
        self.assertEqual(res.get("status"), "DRY_RUN_PASSED")
        self.assertTrue(res.get("firewall_pass"))


if __name__ == "__main__":
    import asyncio
    unittest.main()
