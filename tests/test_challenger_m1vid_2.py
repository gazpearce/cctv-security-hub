#!/usr/bin/env python3
"""
tests/test_challenger_m1vid_2.py
Empirical Challenger Test Suite: Milestone 1 (M1-VID)
Empirical Registry Parity & Rule 45 Isolation Challenge

Author: Challenger M1-VID 2
Role: Empirical Challenger (critic, specialist)
Verification Target:
  1. 100% Mathematical Parity across all 550 platforms x 15 columns
     between master_multicategory_platform_catalog.json and doc2_multicategory_stack_550.csv
  2. 50 Video Platform Catalog authenticity, tiering, uniqueness, and taxonomy
  3. Strict Rule 45 Citadel Air-Gap & Tier 3 YouTube-only isolation
  4. Exhaustive elimination of synthetic domains (adi-telecoms.org) in video registries
  5. Exhaustive check for raw root links and the forbidden term 'checkatrade'
  6. E2E Tool Verification and Integrity Firewall Audits
"""

import csv
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CANONICAL_FAILURE_TAXONOMY = {
    "CREDENTIALS_EXHAUSTED",
    "CAPTCHA_UNSOLVED",
    "PHONE_SMS_REQUIRED",
    "WAITLIST_PENDING",
    "MANUAL_DOCUMENT_VERIFICATION",
    "OAUTH_CLIENT_RESTRICTION",
    "ENTERPRISE_CUSTOM_DOMAIN",
    "PAYWALL_PAYMENT_METHOD",
    "SERVICE_DEPRECATED_OFFLINE",
    "GEO_RESTRICTION_UK",
    "RATE_LIMITED_BLOCK",
}

EXPECTED_CSV_COLUMNS = [
    "Platform ID",
    "Rank",
    "Platform Name",
    "Domain",
    "DA",
    "Stack Key",
    "Category",
    "Tier",
    "1-Click Join Method (SSO)",
    "Official Signup URL",
    "Status",
    "Active Tenant URL",
    "Failure Reason",
    "Upward Target URL",
    "Rule 45 Compliant",
]

PRODUCTION_DATA_FILES = [
    "master_multicategory_platform_catalog.json",
    "doc2_multicategory_stack_550.csv",
    "category_manifests/01_video_stack.csv",
    "master_profile_manifest.json",
    "public_backlink_master_ledger.csv",
    "public_backlink_master_ledger.json",
    "public_backlink_ledger.html",
    "doc1_route_domains_directory.csv",
    "doc2_established_profiles_list.csv",
    "doc3_published_asset_links.csv",
]


class TestMathematicalParityAcross550Platforms(unittest.TestCase):
    """Class 1: 100% Mathematical Parity across 550 rows x 15 columns."""

    @classmethod
    def setUpClass(cls):
        cls.json_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        cls.csv_path = REPO_ROOT / "doc2_multicategory_stack_550.csv"
        
        cls.assertTrue(cls.json_path.exists(), f"Missing {cls.json_path}")
        cls.assertTrue(cls.csv_path.exists(), f"Missing {cls.csv_path}")

        with open(cls.json_path, "r", encoding="utf-8") as f:
            cls.catalog = json.load(f)

        with open(cls.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cls.csv_fieldnames = reader.fieldnames
            cls.csv_rows = list(reader)

        cls.platforms = cls.catalog.get("platforms", [])

    def test_01_exact_total_platform_count_550(self):
        """Verify exactly 550 platforms exist in both JSON and CSV."""
        self.assertEqual(len(self.platforms), 550, f"Expected 550 in JSON, got {len(self.platforms)}")
        self.assertEqual(len(self.csv_rows), 550, f"Expected 550 in CSV, got {len(self.csv_rows)}")
        self.assertEqual(self.catalog.get("total_platforms"), 550)

    def test_02_exact_15_csv_columns_and_ordering(self):
        """Verify exactly the 15 expected columns are present in CSV in proper order."""
        self.assertEqual(self.csv_fieldnames, EXPECTED_CSV_COLUMNS)

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

    def test_04_symmetrical_11_stacks_of_50(self):
        """Verify exactly 11 stacks exist, each having exactly 50 platforms (100% symmetrical)."""
        stacks = self.catalog.get("category_stacks", {})
        self.assertEqual(len(stacks), 11, f"Expected 11 category stacks, got {len(stacks)}")

        for s_key, s_data in stacks.items():
            self.assertEqual(s_data.get("target_platforms_count"), 50)
            plat_count = len(s_data.get("platforms", []))
            self.assertEqual(plat_count, 50, f"Stack {s_key} has {plat_count} platforms, expected 50")
            joined = s_data.get("onboarded_count", 0)
            pending = s_data.get("pending_count", 0)
            self.assertEqual(joined + pending, 50, f"Stack {s_key} joined+pending != 50")

    def test_05_global_and_stack_rank_sequencing(self):
        """Verify global ranks 1..550 and stack ranks 1..50 are strictly sequential."""
        global_ranks = [p["global_rank"] for p in self.platforms]
        self.assertEqual(global_ranks, list(range(1, 551)))

        for s_key, s_data in self.catalog.get("category_stacks", {}).items():
            s_ranks = [p["stack_rank"] for p in s_data.get("platforms", [])]
            self.assertEqual(s_ranks, list(range(1, 51)), f"Stack {s_key} ranks not 1..50")

    def test_06_overall_joined_and_pending_counts(self):
        """Verify total joined == 96 and total pending == 454 (sum 550)."""
        joined_count = sum(1 for p in self.platforms if p["status"] == "JOINED")
        pending_count = sum(1 for p in self.platforms if p["status"] == "PENDING")
        self.assertEqual(joined_count, 96)
        self.assertEqual(pending_count, 454)
        self.assertEqual(joined_count + pending_count, 550)
        self.assertEqual(self.catalog.get("total_joined"), 96)
        self.assertEqual(self.catalog.get("total_pending"), 454)


class TestVideoStackPlatformAuthenticityAndUniqueness(unittest.TestCase):
    """Class 2: Authenticity, uniqueness, and taxonomy of the 50 Video Platforms."""

    @classmethod
    def setUpClass(cls):
        cls.json_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        with open(cls.json_path, "r", encoding="utf-8") as f:
            cat = json.load(f)
        cls.video_platforms = [p for p in cat["platforms"] if p.get("stack_key") == "video"]

    def test_07_video_platform_count_and_id_sequencing(self):
        """Verify video platforms are PLAT-VID-001 through PLAT-VID-050."""
        self.assertEqual(len(self.video_platforms), 50)
        expected_ids = [f"PLAT-VID-{i:03d}" for i in range(1, 51)]
        actual_ids = [p["platform_id"] for p in self.video_platforms]
        self.assertEqual(actual_ids, expected_ids)

    def test_08_video_domain_uniqueness(self):
        """Verify all 50 video platforms have 100% unique domains."""
        domains = [p["domain"].lower() for p in self.video_platforms]
        unique_domains = set(domains)
        self.assertEqual(len(domains), len(unique_domains), f"Duplicate domains in video stack: {domains}")
        self.assertEqual(len(unique_domains), 50)

    def test_09_video_platform_name_uniqueness(self):
        """Verify all 50 video platforms have 100% unique names."""
        names = [p["name"].lower() for p in self.video_platforms]
        unique_names = set(names)
        self.assertEqual(len(names), len(unique_names), f"Duplicate names in video stack: {names}")
        self.assertEqual(len(unique_names), 50)

    def test_10_video_tier_distribution(self):
        """Verify exactly 1 Tier 1, 18 Tier 2, and 31 Tier 3 video platforms."""
        t1 = [p for p in self.video_platforms if p["tier"] == "Tier 1 Apex"]
        t2 = [p for p in self.video_platforms if p["tier"] == "Tier 2"]
        t3 = [p for p in self.video_platforms if p["tier"] == "Tier 3"]

        self.assertEqual(len(t1), 1, f"Expected 1 Tier 1 Apex, got {len(t1)}")
        self.assertEqual(len(t2), 18, f"Expected 18 Tier 2, got {len(t2)}")
        self.assertEqual(len(t3), 31, f"Expected 31 Tier 3, got {len(t3)}")
        self.assertEqual(len(t1) + len(t2) + len(t3), 50)

        # Check Tier 1 is YouTube
        self.assertEqual(t1[0]["platform_id"], "PLAT-VID-001")
        self.assertEqual(t1[0]["domain"], "youtube.com")

    def test_11_video_joined_and_pending_status_integrity(self):
        """Verify 8 JOINED and 42 PENDING video platforms with valid state invariants."""
        joined = [p for p in self.video_platforms if p["status"] == "JOINED"]
        pending = [p for p in self.video_platforms if p["status"] == "PENDING"]

        self.assertEqual(len(joined), 8)
        self.assertEqual(len(pending), 42)

        for p in joined:
            self.assertTrue(
                p.get("active_tenant_url"),
                f"JOINED platform {p['platform_id']} missing active_tenant_url",
            )
            self.assertIsNone(
                p.get("failure_reason"),
                f"JOINED platform {p['platform_id']} has failure_reason: {p.get('failure_reason')}",
            )

        for p in pending:
            self.assertEqual(
                p.get("active_tenant_url", ""),
                "",
                f"PENDING platform {p['platform_id']} has active_tenant_url: {p.get('active_tenant_url')}",
            )
            self.assertIn(
                p.get("failure_reason"),
                CANONICAL_FAILURE_TAXONOMY,
                f"PENDING platform {p['platform_id']} has non-canonical failure reason: {p.get('failure_reason')}",
            )

    def test_12_absence_of_truncated_domain_artifacts(self):
        """Verify known truncated domain artifacts do not exist in video platforms."""
        banned_domain_artifacts = [
            "sproutvideot.com",
            "brightcovetr.com",
            "dtubeipfs.com",
            "kickstreamin.com",
            "dlivestream.com",
            "thetatv.com",
        ]
        domains = [p["domain"].lower() for p in self.video_platforms]
        for bad in banned_domain_artifacts:
            self.assertNotIn(bad, domains, f"Found truncated domain artifact {bad}")


class TestRule45CitadelAirGapAndIsolation(unittest.TestCase):
    """Class 3: Rule 45 Citadel Air-Gap & Tier 3 YouTube-Only Isolation."""

    @classmethod
    def setUpClass(cls):
        cls.json_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        with open(cls.json_path, "r", encoding="utf-8") as f:
            cls.catalog = json.load(f)
        cls.video_platforms = [p for p in cls.catalog["platforms"] if p.get("stack_key") == "video"]

    def test_13_tier3_video_absolute_adicommunications_isolation(self):
        """Verify 0 occurrences of 'adicommunications.co.uk' in all 31 Tier 3 video platforms."""
        t3 = [p for p in self.video_platforms if p["tier"] == "Tier 3"]
        self.assertEqual(len(t3), 31)

        for p in t3:
            for field in ("signup_url", "active_tenant_url", "upward_target_url"):
                val = p.get(field, "") or ""
                self.assertNotIn(
                    "adicommunications.co.uk",
                    val.lower(),
                    f"Rule 45 Violation: {p['platform_id']} [{field}] leaks 'adicommunications.co.uk': {val}",
                )

    def test_14_tier3_video_upward_target_is_youtube_apex_only(self):
        """Verify 100% of Tier 3 video platforms link exclusively to the YouTube Apex channel."""
        t3 = [p for p in self.video_platforms if p["tier"] == "Tier 3"]
        expected_apex = "https://www.youtube.com/@CCTV.services"

        for p in t3:
            self.assertEqual(
                p.get("upward_target_url"),
                expected_apex,
                f"Platform {p['platform_id']} Tier 3 target is not YouTube Apex: {p.get('upward_target_url')}",
            )

    def test_15_tier2_video_upward_target(self):
        """Verify Tier 2 video platforms point upward to YouTube Apex."""
        t2 = [p for p in self.video_platforms if p["tier"] == "Tier 2"]
        expected_apex = "https://www.youtube.com/@CCTV.services"
        for p in t2:
            self.assertEqual(
                p.get("upward_target_url"),
                expected_apex,
                f"Platform {p['platform_id']} Tier 2 target is not YouTube Apex: {p.get('upward_target_url')}",
            )

    def test_16_tier1_video_upward_target_is_blogger_citadel(self):
        """Verify Tier 1 YouTube points upward to Blogger Citadel Hub."""
        t1 = [p for p in self.video_platforms if p["tier"] == "Tier 1 Apex"][0]
        self.assertEqual(t1["upward_target_url"], "https://tvandhomesecurity.blogspot.com/")

    def test_17_zero_raw_root_links_across_entire_550_catalog(self):
        """Verify zero raw root links ('adicommunications.co.uk/' or unbuffered) across all 550 platforms."""
        root_regex = re.compile(
            r"(?:https?:)?//(?:www\.)?adicommunications\.co\.uk/?(?=$|[?#\s\"'])",
            re.IGNORECASE,
        )
        for p in self.catalog["platforms"]:
            for field in ("signup_url", "active_tenant_url", "upward_target_url"):
                val = p.get(field) or ""
                self.assertFalse(
                    root_regex.search(val),
                    f"Platform {p['platform_id']} has raw root link in {field}: {val}",
                )


class TestSyntheticDomainsAndCheckatradePurge(unittest.TestCase):
    """Class 4: Exhaustive check for synthetic domains and Checkatrade mentions."""

    def test_18_zero_synthetic_domains_in_catalog_json_and_csv(self):
        """Verify adi-telecoms.org does not appear in master catalog JSON or CSV."""
        json_path = REPO_ROOT / "master_multicategory_platform_catalog.json"
        csv_path = REPO_ROOT / "doc2_multicategory_stack_550.csv"

        json_text = json_path.read_text(encoding="utf-8")
        csv_text = csv_path.read_text(encoding="utf-8")

        self.assertNotIn("adi-telecoms.org", json_text.lower())
        self.assertNotIn("adi-telecoms.org", csv_text.lower())

    def test_19_zero_synthetic_domains_in_video_manifest_csv(self):
        """Verify 01_video_stack.csv contains zero references to adi-telecoms.org."""
        manifest_path = REPO_ROOT / "category_manifests" / "01_video_stack.csv"
        if manifest_path.exists():
            text = manifest_path.read_text(encoding="utf-8")
            self.assertNotIn("adi-telecoms.org", text.lower())

    def test_20_zero_synthetic_domains_in_video_profiles_doc2_established(self):
        """Verify doc2_established_profiles_list.csv video entries (PLAT-0203..0212) have no synthetic domains."""
        csv_path = REPO_ROOT / "doc2_established_profiles_list.csv"
        self.assertTrue(csv_path.exists())

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Video profiles are rows 22-31 (1-indexed), i.e. index 21-30
        video_rows = [r for r in rows if len(r) > 3 and "Video and streaming stacks" in r[3]]
        self.assertGreaterEqual(len(video_rows), 10)

        for r in video_rows:
            row_str = " ".join(r)
            self.assertNotIn(
                "adi-telecoms.org",
                row_str.lower(),
                f"Video profile row leaks synthetic domain: {row_str}",
            )

    def test_21_zero_synthetic_domains_in_video_routes_doc1(self):
        """Verify doc1_route_domains_directory.csv video entries have no synthetic domains."""
        csv_path = REPO_ROOT / "doc1_route_domains_directory.csv"
        self.assertTrue(csv_path.exists())

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        video_rows = [r for r in rows if len(r) > 2 and "Video and streaming stacks" in r[2]]
        self.assertGreaterEqual(len(video_rows), 10)

        for r in video_rows:
            row_str = " ".join(r)
            self.assertNotIn(
                "adi-telecoms.org",
                row_str.lower(),
                f"doc1 video row leaks synthetic domain: {row_str}",
            )

    def test_22_zero_checkatrade_in_production_data_files(self):
        """Verify 'checkatrade' does not appear in any production data file or catalog."""
        violations = []
        for fn in PRODUCTION_DATA_FILES:
            p = REPO_ROOT / fn
            if not p.exists():
                continue
            content = p.read_text(encoding="utf-8", errors="ignore").lower()
            if "checkatrade" in content:
                count = content.count("checkatrade")
                violations.append(f"{fn} contains {count} occurrences of 'checkatrade'")

        self.assertEqual(len(violations), 0, "Checkatrade found in production data:\n" + "\n".join(violations))


class TestE2EAutomationAndSchemaAudit(unittest.TestCase):
    """Class 5: Verification of scripts, schemas, and live test suites."""

    def test_23_run_verify_no_root_anchors(self):
        """Run verify_no_root_anchors.py and assert exit code 0."""
        res = subprocess.run(
            [sys.executable, "verify_no_root_anchors.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"verify_no_root_anchors failed: {res.stderr or res.stdout}")
        self.assertIn("RULE 45 PASS", res.stdout)

    def test_24_run_onboarder_firewall_audit(self):
        """Run automated_video_platform_onboarder.py --audit-firewall and assert 50 PASSED, 0 FAILED."""
        res = subprocess.run(
            [sys.executable, "automated_video_platform_onboarder.py", "--audit-firewall"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"onboarder firewall audit failed: {res.stderr or res.stdout}")
        self.assertIn("50 PASSED, 0 FAILED", res.stdout)

    def test_25_run_validate_ledger_schema(self):
        """Run validate_ledger_schema.py and assert exit code 0."""
        res = subprocess.run(
            [sys.executable, "validate_ledger_schema.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"validate_ledger_schema failed: {res.stderr or res.stdout}")
        self.assertIn("SUCCESS", res.stdout)

    def test_26_run_m1_video_platforms_unit_tests(self):
        """Run tests/test_m1_video_platforms.py and assert 23/23 tests pass."""
        res = subprocess.run(
            [sys.executable, "-m", "unittest", "tests/test_m1_video_platforms.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"test_m1_video_platforms failed: {res.stderr}")
        self.assertIn("OK", res.stderr)


if __name__ == "__main__":
    unittest.main()
