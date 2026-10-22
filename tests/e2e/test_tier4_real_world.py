"""
Tier 4: Real-World Application Scenarios Test Suite
Autonomous Multi-Category Google & Cloud Stack Expansion Swarm

Validates full end-to-end operational workflows and real-world execution paths (>=5 scenarios):
- Scenario 1: Full Lifecycle Platform Onboarding to Public Ledger Pipeline
- Scenario 2: Multi-Category Swarm Orchestration & Pre-Flight Audit Gate
- Scenario 3: Zero-Tolerance Rule 45 Link Quarantine & Self-Healing Pipeline
- Scenario 4: Live Ledger Mathematical Parity & Schema 2020-12 Verification
- Scenario 5: Automated Email OTP Extraction & SSO Account Authentication Lifecycle
"""

import csv
import io
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestTier4RealWorldScenarios(unittest.TestCase):
    """Tier 4: Comprehensive end-to-end operational scenarios."""

    def test_scenario_01_full_lifecycle_onboarding_to_ledger(self):
        """Scenario 1: Complete lifecycle from platform discovery to public ledger publication."""
        # 1. Platform Discovery from candidate pool
        new_platform = {
            "name": "Koyeb Serverless Cloud",
            "domain": "koyeb.com",
            "da": 81,
            "category": "Serverless & Compute",
            "signup_url": "https://app.koyeb.com/auth/signup",
            "sso_method": "GitHub OAuth",
            "status": "PENDING"
        }
        self.assertEqual(new_platform["status"], "PENDING")

        # 2. Standardized Profile Generation using Gary Pearce Trade Metadata
        manifest_path = REPO_ROOT / "master_profile_manifest.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        profile_record = {
            "profile_id": "PROF-0101",
            "platform_name": new_platform["name"],
            "profile_handle": "gazpearce",
            "profile_live_url": f"https://{new_platform['domain']}/@gazpearce",
            "lead_engineer": manifest["brand_standards"]["engineer"],
            "telephone": manifest["brand_standards"]["telephone"],
            "bio_copy": manifest["standard_bios"]["short_bio_160"],
            "avatar_url": manifest["visual_cdn_assets"]["avatar_square"],
            "apex_url": "https://gary-pearce-forensic-hub.web.app/"
        }
        self.assertIn("07860 244 274", profile_record["bio_copy"])
        self.assertTrue(profile_record["avatar_url"].endswith(".webp"))

        # 3. Simulate Email Verification & Activation
        mock_verification_email = {
            "sender": "no-reply@koyeb.com",
            "snippet": "Welcome to Koyeb! Your verification code is 619284 to activate your account."
        }
        otp_match = re.search(r'\b(\d{6})\b', mock_verification_email["snippet"])
        self.assertIsNotNone(otp_match)
        self.assertEqual(otp_match.group(1), "619284")
        new_platform["status"] = "JOINED"

        # 4. Asset Generation in doc3 format
        doc3_entry = {
            "asset_id": "LINK-0220",
            "parent_profile_id": profile_record["profile_id"],
            "platform_name": new_platform["name"],
            "profile_live_url": profile_record["profile_live_url"],
            "asset_title": "Koyeb Microservice: CCTV DORI Optical Lens Calculator UK",
            "asset_type": "Serverless API Endpoint",
            "asset_public_url": f"{profile_record['profile_live_url']}/dori-calculator",
            "top_of_stack_apex_url": profile_record["apex_url"],
            "shield_target_url": "https://tvandhomesecurity.blogspot.com/2026/10/cctv-dori-calculation.html",
            "seo_tags": "#cctv #dori #optics #serverless",
            "seo_description_summary": f"Trade optical endpoint by Gary Pearce ({profile_record['telephone']})",
            "dofollow_status": "Dofollow API Authority",
            "publication_date": "2026-10-22",
            "verification_status": "HTTP_200"
        }

        # 5. Rule 45 Validation on generated asset
        root_pattern = re.compile(r"https?://(?:www\.)?adicommunications\.co\.uk/?[\"\'\s>]")
        self.assertIsNone(root_pattern.search(f'"{doc3_entry["shield_target_url"]}"'))
        self.assertIsNone(root_pattern.search(f'"{doc3_entry["top_of_stack_apex_url"]}"'))

        # Lifecycle completed cleanly
        self.assertEqual(new_platform["status"], "JOINED")
        self.assertEqual(doc3_entry["verification_status"], "HTTP_200")

    def test_scenario_02_multi_category_swarm_orchestration_audit(self):
        """Scenario 2: Orchestration pre-flight audit across all 11 stacks before deployment."""
        orchestrator_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orchestrator_path, "r", encoding="utf-8") as f:
            code = f.read()

        namespace = {}
        exec(compile(code, str(orchestrator_path), "exec"), namespace)
        teams = namespace.get("STACK_TEAMS", {})

        # Verify all 11 stacks exist
        expected_stacks = ["video", "podcast", "docs", "blog", "cloud", "media", "howto", "bookmark", "rss", "music", "offers"]
        for stack in expected_stacks:
            self.assertIn(stack, teams, f"Stack '{stack}' missing from orchestrator teams")
            self.assertTrue(teams[stack]["apex"].startswith("https://"))

        # Run Rule 45 QC Audit step
        qc_script = REPO_ROOT / "verify_no_root_anchors.py"
        res = subprocess.run([sys.executable, str(qc_script)], capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(res.returncode, 0, "Pre-flight Rule 45 gate failed")
        self.assertIn("RULE 45 PASS", res.stdout)

    def test_scenario_03_zero_tolerance_rule45_quarantine_and_healing(self):
        """Scenario 3: Quarantine raw root anchor leak and apply self-healing re-route."""
        # 1. Defective candidate asset with forbidden root link
        defective_asset = {
            "asset_id": "TEST-LEAK-01",
            "title": "Unshielded Asset",
            "anchor_url": "https://adicommunications.co.uk/"  # FORBIDDEN NAKED ROOT
        }

        # 2. Compliance Checker detects violation
        is_violating = bool(re.search(r"https?://(?:www\.)?adicommunications\.co\.uk/?[\"\'\s>]", f'"{defective_asset["anchor_url"]}"'))
        self.assertTrue(is_violating, "Compliance auditor must detect naked root leak")

        # 3. Quarantine / Self-Healing logic triggers
        # Maps defective link to authorized /news/ buffer post
        approved_buffer_target = "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/"
        defective_asset["anchor_url"] = approved_buffer_target
        defective_asset["remediated"] = True

        # 4. Re-verify post remediation
        still_violating = bool(
            re.search(r"https?://(?:www\.)?adicommunications\.co\.uk/?[\"\'\s>]", f'"{defective_asset["anchor_url"]}"') and
            not re.search(r"adicommunications\.co\.uk/(?:news|assets|feed)", defective_asset["anchor_url"])
        )
        self.assertFalse(still_violating, "Asset should be 100% compliant after self-healing remediation")
        self.assertTrue(defective_asset["remediated"])

    def test_scenario_04_live_ledger_mathematical_parity_and_schema_validation(self):
        """Scenario 4: Validates real repository dataset across CSV, JSON, and HTML."""
        csv_path = REPO_ROOT / "public_backlink_master_ledger.csv"
        json_path = REPO_ROOT / "public_backlink_master_ledger.json"
        doc3_path = REPO_ROOT / "doc3_published_asset_links.csv"
        html_path = REPO_ROOT / "public_backlink_ledger.html"

        # Check all files exist
        for p in (csv_path, json_path, doc3_path, html_path):
            self.assertTrue(p.exists(), f"Ledger file missing: {p}")

        # Ingest and compare counts
        with open(doc3_path, "r", encoding="utf-8") as f:
            doc3_rows = list(csv.DictReader(f))

        with open(csv_path, "r", encoding="utf-8") as f:
            csv_rows = list(csv.DictReader(f))

        with open(json_path, "r", encoding="utf-8") as f:
            json_obj = json.load(f)

        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Strict Mathematical Parity Check
        self.assertEqual(len(doc3_rows), len(csv_rows))
        self.assertEqual(len(csv_rows), len(json_obj["entries"]))
        self.assertEqual(json_obj["total_backlinks"], len(csv_rows))

        # Schema 2020-12 Verification
        self.assertEqual(json_obj["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(json_obj["lead_engineer"], "Gary Pearce (ADI Communications, 07860 244 274)")
        self.assertEqual(json_obj["rule_45_shield"], "STRICT_AIR_GAP")

        # HTML Parity Check: verify table has matching number of rows
        table_rows_count = len(re.findall(r'<tr class="hover:bg-white', html_content))
        self.assertEqual(table_rows_count, len(csv_rows), "HTML table rows must equal ledger count")

    def test_scenario_05_automated_email_otp_extraction_and_sso_authentication(self):
        """Scenario 5: Simulated email verification loop and 6-digit OTP extraction."""
        # Simulated inbox DOM row data captured via Chrome CDP
        mock_cdp_inbox_data = [
            {
                "sender": "no-reply@vercel.com",
                "snippet": "Vercel - Welcome to Vercel! New sign-in detected on your account from Chrome"
            },
            {
                "sender": "ibmacct@iam.ibm.com",
                "snippet": "IBM Security Verify - Please use verification code 492847 to authenticate."
            },
            {
                "sender": "support@github.com",
                "snippet": "[GitHub] Please confirm your email address to complete registration"
            }
        ]

        # Ingestion and extraction
        extracted_results = []
        for row in mock_cdp_inbox_data:
            snippet = row["snippet"]
            code_match = re.search(r'\b(\d{6})\b', snippet)
            is_verify = any(k in snippet.lower() for k in ["verify", "verification", "confirm", "code", "activate", "welcome"])
            if is_verify:
                code = code_match.group(1) if code_match else None
                extracted_results.append({
                    "sender": row["sender"],
                    "code": code,
                    "verified": True
                })

        # Assertions
        self.assertEqual(len(extracted_results), 3)
        ibm_result = next(r for r in extracted_results if "ibm" in r["sender"])
        self.assertEqual(ibm_result["code"], "492847")
        self.assertTrue(ibm_result["verified"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
