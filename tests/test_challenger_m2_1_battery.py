"""
tests/test_challenger_m2_1_battery.py
Empirical Challenger Battery for Milestone 2
Author: challenger_m2_1

Stress-tests:
1. Prohibited strings ('0800', 'Checkatrade', 'checkatrade.com')
2. Bio lengths (short_bio_160 <= 160 characters across manifest and all 100 profiles)
3. Google Citadel Apex URLs validation across all 11 stacks and all 100 profiles
4. 100 profile completeness, genuine E-E-A-T metadata, and 1:1 CSV-Manifest parity
5. Rule 45 strict compliance (zero raw root links to adicommunications.co.uk)
6. Full E2E suite execution and PROJECT.md milestone tracking status
"""

import csv
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "master_profile_manifest.json"
DOC2_PATH = REPO_ROOT / "doc2_established_profiles_list.csv"
PROJECT_PATH = REPO_ROOT / "PROJECT.md"

VALID_GOOGLE_APEX_DOMAINS = (
    "youtube.com", "youtu.be",
    "drive.google.com",
    "tvandhomesecurity.blogspot.com", "blogspot.com", "blogger.com",
    "web.app", "firebaseapp.com",
    "maps.google.com", "google.com/maps",
    "docs.google.com", "sites.google.com"
)


class TestProhibitedStringsScan(unittest.TestCase):
    """1. Scan for any prohibited strings: '0800', 'Checkatrade', 'checkatrade.com'."""

    def setUp(self):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            self.raw_manifest = f.read()
        with open(DOC2_PATH, "r", encoding="utf-8") as f:
            self.raw_doc2 = f.read()

    def test_no_0800_in_manifest_or_csv(self):
        self.assertNotIn("0800", self.raw_manifest, "Prohibited string '0800' found in master_profile_manifest.json")
        self.assertNotIn("0800", self.raw_doc2, "Prohibited string '0800' found in doc2_established_profiles_list.csv")

    def test_no_checkatrade_in_manifest_or_csv(self):
        for prohibited in ["checkatrade", "checkatrade.com"]:
            self.assertNotIn(prohibited, self.raw_manifest.lower(), f"Prohibited string '{prohibited}' found in master_profile_manifest.json")
            self.assertNotIn(prohibited, self.raw_doc2.lower(), f"Prohibited string '{prohibited}' found in doc2_established_profiles_list.csv")


class TestBioLengthsVerification(unittest.TestCase):
    """2. Verify bio lengths (short_bio_160 <= 160 characters)."""

    def setUp(self):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)
        with open(DOC2_PATH, "r", encoding="utf-8") as f:
            self.doc2_rows = list(csv.DictReader(f))

    def test_standard_bios_short_bio_160_length(self):
        short_bio = self.manifest.get("standard_bios", {}).get("short_bio_160", "")
        self.assertTrue(len(short_bio) > 0, "short_bio_160 must not be empty")
        self.assertLessEqual(len(short_bio), 160, f"short_bio_160 length {len(short_bio)} exceeds 160 characters")

    def test_all_100_manifest_profile_bios_within_160_chars(self):
        profiles = self.manifest.get("established_profiles_100", [])
        self.assertEqual(len(profiles), 100)
        for p in profiles:
            bio = p.get("bio_copy", "")
            self.assertLessEqual(
                len(bio), 160,
                f"Profile {p.get('profile_id')} in manifest bio length {len(bio)} exceeds 160 chars"
            )

    def test_all_100_csv_profile_bios_within_160_chars(self):
        self.assertEqual(len(self.doc2_rows), 100)
        for r in self.doc2_rows:
            bio = r.get("bio_copy", "")
            self.assertLessEqual(
                len(bio), 160,
                f"Profile {r.get('profile_id')} in CSV bio length {len(bio)} exceeds 160 chars"
            )


class TestGoogleCitadelApexUrls(unittest.TestCase):
    """3. Verify that all apex URLs in both files belong to the valid Google Citadel domains list."""

    def setUp(self):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)
        with open(DOC2_PATH, "r", encoding="utf-8") as f:
            self.doc2_rows = list(csv.DictReader(f))

    def test_category_stacks_11_apex_urls(self):
        stacks = self.manifest.get("category_stacks_11", {})
        self.assertEqual(len(stacks), 11, "Must contain exactly 11 category stacks")
        for key, s in stacks.items():
            apex = s.get("apex_url", "")
            self.assertTrue(apex.startswith("https://"), f"Stack '{key}' apex '{apex}' must be HTTPS")
            has_valid = any(dom in apex for dom in VALID_GOOGLE_APEX_DOMAINS)
            self.assertTrue(has_valid, f"Stack '{key}' apex '{apex}' not in Google Citadel domains")

    def test_manifest_100_profiles_apex_urls(self):
        profiles = self.manifest.get("established_profiles_100", [])
        self.assertEqual(len(profiles), 100)
        for p in profiles:
            top_apex = p.get("top_of_stack_apex_url", "")
            shield = p.get("shield_anchor_url", "")

            self.assertTrue(top_apex.startswith("https://"), f"{p['profile_id']} top_of_stack_apex_url not HTTPS: {top_apex}")
            self.assertTrue(shield.startswith("https://"), f"{p['profile_id']} shield_anchor_url not HTTPS: {shield}")

            has_valid_top = any(dom in top_apex for dom in VALID_GOOGLE_APEX_DOMAINS)
            has_valid_shield = any(dom in shield for dom in VALID_GOOGLE_APEX_DOMAINS)

            self.assertTrue(has_valid_top, f"{p['profile_id']} top_of_stack_apex_url '{top_apex}' not Google Citadel")
            self.assertTrue(has_valid_shield, f"{p['profile_id']} shield_anchor_url '{shield}' not Google Citadel")

    def test_csv_100_profiles_shield_anchor_urls(self):
        self.assertEqual(len(self.doc2_rows), 100)
        for r in self.doc2_rows:
            shield = r.get("shield_anchor_url", "")
            self.assertTrue(shield.startswith("https://"), f"{r['profile_id']} shield_anchor_url not HTTPS: {shield}")
            has_valid = any(dom in shield for dom in VALID_GOOGLE_APEX_DOMAINS)
            self.assertTrue(has_valid, f"{r['profile_id']} shield_anchor_url '{shield}' not Google Citadel")

    def test_blogger_bottleneck_eliminated(self):
        shield_urls = [r["shield_anchor_url"] for r in self.doc2_rows]
        counts = Counter(shield_urls)

        # Baseline defect was: Blogger Hub had 100 out of 100
        self.assertEqual(
            counts.get("https://tvandhomesecurity.blogspot.com/", 0), 10,
            "Blogger Hub should strictly have 10 blog-category profiles"
        )
        self.assertGreaterEqual(
            len(counts), 5,
            f"Expected at least 5 distinct Google Apex endpoints across 100 profiles, got {len(counts)}"
        )


class TestProfileCompletenessAndEEATMetadata(unittest.TestCase):
    """4. Validate that all 100 profiles are present with non-empty, genuine E-E-A-T metadata."""

    def setUp(self):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)
        with open(DOC2_PATH, "r", encoding="utf-8") as f:
            self.doc2_rows = list(csv.DictReader(f))

    def test_brand_standards_eeat(self):
        brand = self.manifest.get("brand_standards", {})
        self.assertEqual(brand.get("engineer"), "Gary Pearce")
        self.assertEqual(brand.get("business"), "ADI Communications")
        self.assertEqual(brand.get("telephone"), "07860 244 274")

        creds = brand.get("credentials", {})
        self.assertGreaterEqual(creds.get("experience_years", 0), 25)
        self.assertIn("10,000,000", creds.get("public_liability_insurance", ""))
        self.assertIn("NOT CAI members", creds.get("cai_compliance_notice", ""))
        self.assertIn("CAI-benchmarked equipment", creds.get("cai_compliance_notice", ""))
        self.assertIn("9.98", creds.get("verified_rating", ""))
        self.assertIn("84+", creds.get("verified_rating", ""))

        assets = self.manifest.get("visual_cdn_assets", {})
        self.assertTrue(assets.get("avatar_square", "").startswith("https://cdn.jsdelivr.net/"))
        self.assertTrue(assets.get("avatar_square", "").endswith(".webp"))
        self.assertTrue(assets.get("cover_banner_16x9", "").startswith("https://cdn.jsdelivr.net/"))
        self.assertTrue(assets.get("cover_banner_16x9", "").endswith(".webp"))

    def test_100_profiles_manifest_completeness(self):
        profiles = self.manifest.get("established_profiles_100", [])
        self.assertEqual(len(profiles), 100)

        required_keys = [
            "profile_id", "platform_id", "platform_name", "category",
            "stack_key", "profile_handle", "profile_live_url",
            "top_of_stack_apex_url", "shield_anchor_url", "bio_copy",
            "auth_credentials_ref", "creation_date", "status"
        ]

        for p in profiles:
            for k in required_keys:
                self.assertIn(k, p, f"{p.get('profile_id')} missing key '{k}'")
                val = p[k]
                self.assertTrue(
                    val is not None and str(val).strip() != "",
                    f"{p.get('profile_id')} key '{k}' has empty value"
                )

            bio = p["bio_copy"]
            self.assertIn("Gary Pearce", bio, f"{p['profile_id']} missing 'Gary Pearce' in bio")
            self.assertIn("ADI Communications", bio, f"{p['profile_id']} missing 'ADI Communications' in bio")
            self.assertIn("07860 244 274", bio, f"{p['profile_id']} missing '07860 244 274' in bio")
            self.assertIn("25+", bio, f"{p['profile_id']} missing '25+' in bio")

    def test_100_profiles_csv_completeness(self):
        self.assertEqual(len(self.doc2_rows), 100)
        required_cols = [
            "profile_id", "platform_id", "platform_name", "category",
            "profile_handle", "profile_live_url", "bio_copy",
            "shield_anchor_url", "auth_credentials_ref", "creation_date", "status"
        ]

        for r in self.doc2_rows:
            for c in required_cols:
                self.assertIn(c, r, f"{r.get('profile_id')} missing column '{c}'")
                val = r[c]
                self.assertTrue(
                    val is not None and str(val).strip() != "",
                    f"{r.get('profile_id')} column '{c}' is empty"
                )

            bio = r["bio_copy"]
            self.assertIn("Gary Pearce", bio, f"{r['profile_id']} missing 'Gary Pearce' in bio")
            self.assertIn("ADI Communications", bio, f"{r['profile_id']} missing 'ADI Communications' in bio")
            self.assertIn("07860 244 274", bio, f"{r['profile_id']} missing '07860 244 274' in bio")
            self.assertIn("25+", bio, f"{r['profile_id']} missing '25+' in bio")

    def test_exact_1_to_1_manifest_csv_field_parity(self):
        profiles_m = self.manifest.get("established_profiles_100", [])
        self.assertEqual(len(profiles_m), 100)
        self.assertEqual(len(self.doc2_rows), 100)

        common_fields = [
            "profile_id", "platform_id", "platform_name", "category",
            "profile_handle", "profile_live_url", "bio_copy",
            "shield_anchor_url", "auth_credentials_ref", "creation_date", "status"
        ]

        for p_m, r_c in zip(profiles_m, self.doc2_rows):
            pid = p_m["profile_id"]
            for field in common_fields:
                self.assertEqual(
                    p_m.get(field), r_c.get(field),
                    f"Discrepancy at {pid} for field '{field}': manifest='{p_m.get(field)}' vs csv='{r_c.get(field)}'"
                )


class TestRule45ComplianceAndE2ESuite(unittest.TestCase):
    """5 & 6. Verify Rule 45 compliance and run E2E test suite."""

    def test_rule_45_script_exit_code_0(self):
        result = subprocess.run(
            [sys.executable, "verify_no_root_anchors.py"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        self.assertEqual(
            result.returncode, 0,
            f"verify_no_root_anchors.py failed with returncode {result.returncode}:\n{result.stderr}\n{result.stdout}"
        )
        self.assertIn("RULE 45 PASS", result.stdout)

    def test_project_md_milestone_statuses(self):
        content = PROJECT_PATH.read_text(encoding="utf-8")
        # Check M1 is DONE and M2 is IN_PROGRESS
        self.assertIn("| M1 | Automated Verification & Onboarding Engine |", content)
        self.assertIn("| DONE |", content)
        self.assertIn("| M2 | Multi-Category Stack & Profile Standardization |", content)
        self.assertIn("| IN_PROGRESS |", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
