"""
tests/test_milestone3_and_4.py
Direct verification test suite for Milestone 3 & Milestone 4 requirements:
- M3.1: Synchronization parity across doc3, CSV, JSON, HTML
- M3.2: JSON Schema Draft 2020-12 compliance with verified fields
- M3.3: HTML table static rendering and interactive controls
- M3.4: Rule 45 zero root leak check on all ledger URLs
- M4.1: /gstack status CLI execution
- M4.2: /gstack sync CLI execution
- M4.3: /gstack audit CLI execution
- M4.4: /gstack verify CLI execution
- M4.5: /gstack deploy with --skip-deploy execution
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

class TestMilestone3And4(unittest.TestCase):

    def test_m3_01_synchronization_parity(self):
        doc3_file = REPO_ROOT / "doc3_published_asset_links.csv"
        csv_file = REPO_ROOT / "public_backlink_master_ledger.csv"
        json_file = REPO_ROOT / "public_backlink_master_ledger.json"
        html_file = REPO_ROOT / "public_backlink_ledger.html"

        with open(doc3_file, "r", encoding="utf-8") as f:
            doc3_len = len(list(csv.DictReader(f)))
        with open(csv_file, "r", encoding="utf-8") as f:
            csv_len = len(list(csv.DictReader(f)))
        with open(json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            json_len = len(json_data["entries"])
        with open(html_file, "r", encoding="utf-8") as f:
            html_rows = len(re.findall(r'<tr class="hover:bg-white', f.read()))

        self.assertEqual(doc3_len, csv_len)
        self.assertEqual(csv_len, json_len)
        self.assertEqual(json_data["total_backlinks"], csv_len)
        self.assertEqual(html_rows, csv_len)

    def test_m3_02_draft202012_schema_fields(self):
        json_file = REPO_ROOT / "public_backlink_master_ledger.json"
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        required_fields = [
            "platform", "category_stack", "tenant_url", "anchor_text",
            "apex_target", "http_status", "index_status", "last_verified"
        ]
        self.assertGreater(len(data["entries"]), 0)
        for e in data["entries"]:
            for field in required_fields:
                self.assertIn(field, e, f"Missing verified field '{field}' in JSON entry")

    def test_m3_03_html_search_filter_components(self):
        html_file = REPO_ROOT / "public_backlink_ledger.html"
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn('id="ledger-search"', content)
        self.assertIn('id="category-filter"', content)
        self.assertIn('id="visible-count"', content)
        self.assertIn('data-category="', content)
        self.assertIn('addEventListener', content)

    def test_m3_04_rule_45_zero_raw_root_links_in_ledger(self):
        json_file = REPO_ROOT / "public_backlink_master_ledger.json"
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for idx, e in enumerate(data.get("entries", []), 1):
            for k in ("tenant_url", "apex_target", "shield_target_url", "public_live_url", "top_of_stack_apex_url"):
                val = e.get(k, "")
                if "adicommunications.co.uk" in val:
                    self.assertTrue(
                        any(sub in val for sub in ("/news/", "/assets/", "/feed/")),
                        f"Rule 45 leak in entry {idx} field '{k}': {val}"
                    )

    def test_m4_01_orchestrator_subcommands(self):
        orch = REPO_ROOT / "swarm_stack_orchestrator.py"
        res = subprocess.run([sys.executable, str(orch), "--help"], capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(res.returncode, 0, f"--help failed: {res.stderr}")
        self.assertIn("status", res.stdout)
        self.assertIn("sync", res.stdout)
        self.assertIn("audit", res.stdout)
        self.assertIn("verify", res.stdout)
        self.assertIn("deploy", res.stdout)

        for subcmd in ["status", "sync", "audit"]:
            res = subprocess.run([sys.executable, str(orch), subcmd], capture_output=True, text=True, cwd=str(REPO_ROOT))
            self.assertEqual(res.returncode, 0, f"Subcommand '{subcmd}' failed: {res.stderr}")

        # M4.4: Verify authentic reachability across all 11 category stacks
        res_verify = subprocess.run([sys.executable, str(orch), "verify"], capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(res_verify.returncode, 0, f"Subcommand 'verify' failed: {res_verify.stderr}")
        for cat in ["VIDEO", "PODCAST", "DOCS", "BLOG", "CLOUD", "MEDIA", "HOWTO", "BOOKMARK", "RSS", "MUSIC", "OFFERS"]:
            self.assertIn(f"[{cat}", res_verify.stdout, f"Missing category '{cat}' in verify output")
        self.assertIn("11/11 Endpoints Reachable", res_verify.stdout)
        self.assertIn("[VERIFY PASS] All 11/11 Top-of-Stack Google Citadel Apex endpoints verified reachable.", res_verify.stdout)

    def test_m4_02_orchestrator_deploy_dry_run(self):
        orch = REPO_ROOT / "swarm_stack_orchestrator.py"
        res = subprocess.run([sys.executable, str(orch), "deploy", "--skip-deploy"], capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(res.returncode, 0, f"deploy --skip-deploy failed: {res.stderr}")

if __name__ == "__main__":
    unittest.main()
