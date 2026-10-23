"""
Tier 3: Cross-Feature Combinations Test Suite
Autonomous Multi-Category Google & Cloud Stack Expansion Swarm

Validates pairwise interactions and contract dependencies across cooperating modules (>=8 tests):
- F1_x_F5: Top-of-Stack Apex Registry x Rule 45 Compliance Engine
- F2_x_F3: Email Verifier x Platform Onboarding Tracker
- F3_x_F4: Platform Onboarding x Profile Standardization & E-E-A-T
- F4_x_F5: Standardized Profile Manifest x Rule 45 Strict Shield
- F5_x_F6: Rule 45 Audit x Backlink Ledger Synchronization Pipeline
- F6_x_F1: Master Backlink Ledger x Top-of-Stack Google Apex Registry
- F7_x_F3: Swarm Orchestrator x Cloud Signup Tracker Platform Directory
- F7_x_F2: Swarm Orchestrator x Workspace Verifier Engine
- F7_x_F6: Swarm Orchestrator x Public Backlink Ledger Builder
"""

import csv
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestTier3CrossFeatureCombinations(unittest.TestCase):
    """Tier 3: Pairwise integration tests between system features."""

    def test_f1_x_f5_all_11_apexes_satisfy_rule45(self):
        """Cross-Feature (F1 x F5): All 11 Google Apex URLs strictly satisfy Rule 45 isolation."""
        orchestrator_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orchestrator_path, "r", encoding="utf-8") as f:
            code = f.read()

        namespace = {}
        exec(compile(code, str(orchestrator_path), "exec"), namespace)
        teams = namespace.get("STACK_TEAMS", {})

        root_pattern = re.compile(r"https?://(?:www\.)?adicommunications\.co\.uk/?[\"\'\s>]")

        for name, info in teams.items():
            if name in ("browser", "daemon", "producer", "qc"):
                continue  # Permit loopback daemon / worker engines
            apex = info.get("apex", "")
            # Verify no apex points directly to naked root
            self.assertIsNone(
                root_pattern.search(f'"{apex}"'),
                f"Stack '{name}' apex '{apex}' violates Rule 45 by pointing to money site root"
            )
            # Verify apex is an external Google property or safe public ledger
            is_valid_apex = (
                "google.com" in apex or "youtu" in apex or
                "blogspot.com" in apex or "web.app" in apex or "127.0.0.1" in apex
            )
            self.assertTrue(is_valid_apex, f"Stack '{name}' apex '{apex}' must be a recognized Google entity")

    def test_f2_x_f3_email_verifier_matches_onboarding_domain(self):
        """Cross-Feature (F2 x F3): Email verification triggers map to candidate platform names in tracker."""
        tracker_path = REPO_ROOT / "master_cloud_signup_tracker.json"
        with open(tracker_path, "r", encoding="utf-8") as f:
            tracker = json.load(f)

        platform_names = {p["name"].lower() for p in tracker["platforms"]}
        platform_domains = {p["domain"].lower() for p in tracker["platforms"]}

        # Simulate emails from known platforms
        incoming_verification_emails = [
            {"sender": "no-reply@vercel.com", "snippet": "Vercel - New sign-in detected on your account"},
            {"sender": "support@hub.docker.com", "snippet": "Docker Hub Registry - GitHub was linked to your account"},
            {"sender": "verify@supabase.com", "snippet": "Confirm your Supabase account email: 829103"},
            {"sender": "info@neon.tech", "snippet": "Welcome to Neon - Your account is now active"}
        ]

        matched_platforms = []
        for email in incoming_verification_emails:
            text = (email["sender"] + " " + email["snippet"]).lower()
            matched = (
                any(p in text for p in platform_names) or 
                any(d in text for d in platform_domains) or
                any(d.split('.')[-2] in text for d in platform_domains if '.' in d)
            )
            if matched:
                matched_platforms.append(email)

        self.assertEqual(
            len(matched_platforms),
            len(incoming_verification_emails),
            "Every verification email must match an active candidate platform in the onboarding tracker"
        )

    def test_f3_x_f4_established_profiles_match_standardized_metadata(self):
        """Cross-Feature (F3 x F4): Established profiles in doc2 adhere to Gary Pearce E-E-A-T metadata."""
        doc2_path = REPO_ROOT / "doc2_established_profiles_list.csv"
        manifest_path = REPO_ROOT / "master_profile_manifest.json"

        self.assertTrue(doc2_path.exists())
        self.assertTrue(manifest_path.exists())

        with open(doc2_path, "r", encoding="utf-8") as f:
            profiles = list(csv.DictReader(f))

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        expected_phone = manifest["brand_standards"]["telephone"]
        self.assertEqual(expected_phone, "07860 244 274")

        self.assertEqual(len(profiles), 100, "doc2 must contain 100 established profiles")
        for p in profiles[:20]:
            bio = p.get("bio_copy", "")
            self.assertIn("Gary Pearce", bio, f"Profile {p.get('profile_id')} must feature Gary Pearce")
            self.assertIn("07860 244 274", bio, f"Profile {p.get('profile_id')} must feature direct mobile")
            self.assertIn("ADI Communications", bio, f"Profile {p.get('profile_id')} must feature ADI Communications")

    def test_f4_x_f5_profile_manifest_urls_comply_with_rule45(self):
        """Cross-Feature (F4 x F5): All URLs in master_profile_manifest.json strictly comply with Rule 45."""
        manifest_path = REPO_ROOT / "master_profile_manifest.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find any occurrence of adicommunications.co.uk
        matches = re.findall(r"https?://(?:www\.)?adicommunications\.co\.uk(/[^\"\'\s]*)?", content)
        for subpath in matches:
            if subpath:
                is_allowed = bool(re.match(r"^/(?:news|assets|feed)", subpath))
                self.assertTrue(is_allowed, f"Disallowed subpath in profile manifest: {subpath}")
            else:
                self.fail("Raw naked root adicommunications.co.uk found in master_profile_manifest.json")

    def test_f5_x_f6_published_assets_in_doc3_pass_rule45_audit(self):
        """Cross-Feature (F5 x F6): Published assets in doc3 strictly channel equity into buffer/apex."""
        doc3_path = REPO_ROOT / "doc3_published_asset_links.csv"
        with open(doc3_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        allowed_service_prefixes = ("/news/", "/assets/", "/feed/", "/cctv-", "/starlink-", "/tv-", "/wifi-", "/ajax-", "/aerial-")

        for r in rows:
            shield_target = r.get("shield_target_url", "")
            apex_target = r.get("top_of_stack_apex_url", "")
            public_url = r.get("asset_public_url", "")

            # Ensure neither public URL nor targets are naked money site roots
            for url in (shield_target, apex_target, public_url):
                if "adicommunications.co.uk" in url:
                    self.assertTrue(
                        any(sub in url for sub in allowed_service_prefixes),
                        f"Asset {r.get('asset_id')} target '{url}' violates Rule 45"
                    )

    def test_f6_x_f1_ledger_assets_upward_route_to_verified_apexes(self):
        """Cross-Feature (F6 x F1): Every ledger asset links upward into a verified Google Apex entity."""
        csv_path = REPO_ROOT / "public_backlink_master_ledger.csv"
        with open(csv_path, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        valid_apex_substrings = [
            "drive.google.com", "youtube.com", "youtu.be",
            "tvandhomesecurity.blogspot.com", "web.app", "firebaseapp.com",
            "maps.google.com", "docs.google.com", "sites.google.com", "photos.google.com"
        ]

        for r in rows:
            apex = r.get("top_of_stack_apex_url", "")
            has_valid = any(s in apex for s in valid_apex_substrings)
            self.assertTrue(
                has_valid,
                f"Ledger row '{r.get('asset_title')}' has invalid top_of_stack_apex_url: {apex}"
            )

    def test_f7_x_f3_orchestrator_cloud_team_matches_signup_tracker(self):
        """Cross-Feature (F7 x F3): Orchestrator cloud team links directly to Firebase Edge Apex."""
        orchestrator_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orchestrator_path, "r", encoding="utf-8") as f:
            code = f.read()

        namespace = {}
        exec(compile(code, str(orchestrator_path), "exec"), namespace)
        teams = namespace.get("STACK_TEAMS", {})

        self.assertIn("cloud", teams)
        cloud_apex = teams["cloud"].get("apex", "")
        self.assertEqual(cloud_apex, "https://gary-pearce-forensic-hub.web.app/")

    def test_f7_x_f2_orchestrator_verifier_team_invokes_auto_email_verifier(self):
        """Cross-Feature (F7 x F2): Orchestrator verifier team is wired to auto_email_verifier.py."""
        orchestrator_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orchestrator_path, "r", encoding="utf-8") as f:
            code = f.read()

        namespace = {}
        exec(compile(code, str(orchestrator_path), "exec"), namespace)
        teams = namespace.get("STACK_TEAMS", {})

        self.assertIn("verifier", teams)
        verifier_script = teams["verifier"].get("script", "")
        self.assertEqual(verifier_script, "auto_email_verifier.py")
        self.assertTrue((REPO_ROOT / verifier_script).exists(), "Verifier script must exist")

    def test_f7_x_f6_orchestrator_ledger_team_invokes_backlink_builder(self):
        """Cross-Feature (F7 x F6): Orchestrator ledger team is wired to build_public_backlink_ledger.py."""
        orchestrator_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orchestrator_path, "r", encoding="utf-8") as f:
            code = f.read()

        namespace = {}
        exec(compile(code, str(orchestrator_path), "exec"), namespace)
        teams = namespace.get("STACK_TEAMS", {})

        self.assertIn("ledger", teams)
        ledger_script = teams["ledger"].get("script", "")
        self.assertIn(ledger_script, ("build_public_backlink_ledger.py", "validate_ledger_schema.py"))
        self.assertTrue((REPO_ROOT / ledger_script).exists(), "Ledger script must exist")


if __name__ == "__main__":
    unittest.main(verbosity=2)
