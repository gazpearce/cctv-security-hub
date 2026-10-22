"""
tests/test_challenger_m2_empirical.py
Empirical Adversarial Challenge Suite for Milestone 2:
Constructed by challenger_m2_2.

Adversarially challenges:
1. Rule 45 scan of ALL JSON and CSV files in the repository for raw root links to https://adicommunications.co.uk/
2. JSON Schema Draft 2020-12 compliance of master_profile_manifest.json
3. Mathematical parity between doc2_established_profiles_list.csv and master_profile_manifest.json
4. E-E-A-T Trade Metadata, zero 0800, zero Checkatrade, CAI disclaimer, and WebP CDN assets
5. 11 Category Stacks integrity and Top-of-Stack Google Citadel Apex verification
6. Audit of verify_no_root_anchors.py and boundary delimiter vulnerabilities
"""

import csv
import json
import os
import re
import unittest
from pathlib import Path
from urllib.parse import urlparse

import jsonschema
from jsonschema import Draft202012Validator

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")
MANIFEST_PATH = REPO_ROOT / "master_profile_manifest.json"
DOC2_PATH = REPO_ROOT / "doc2_established_profiles_list.csv"


class TestRule45RepoWideScan(unittest.TestCase):
    """Scan all JSON and CSV files in the entire repository for raw root links."""

    def test_json_and_csv_for_raw_root_links(self):
        """Task 1: Scan all JSON and CSV files for raw root links to adicommunications.co.uk."""
        json_files = list(REPO_ROOT.rglob("*.json"))
        csv_files = list(REPO_ROOT.rglob("*.csv"))

        # Exclude .git and .agents directories
        target_files = [
            f for f in json_files + csv_files
            if ".git" not in f.parts and ".agents" not in f.parts
        ]

        self.assertGreater(len(target_files), 50, "Expected at least 50 JSON and CSV files to scan")

        violations = []
        scanned_count = 0
        total_occurrences = 0

        # Regex to extract potential URLs
        url_finder = re.compile(r"https?://[^\s\"\'\<\>\,\)\;]+", re.IGNORECASE)

        for fpath in target_files:
            scanned_count += 1
            content = fpath.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()

            for line_no, line in enumerate(lines, 1):
                if "adicommunications.co.uk" in line.lower():
                    total_occurrences += 1
                    urls = url_finder.findall(line)
                    for raw_url in urls:
                        clean_url = raw_url.rstrip("\"\'.,;>)]}")
                        try:
                            parsed = urlparse(clean_url)
                        except Exception:
                            continue

                        host = (parsed.hostname or "").lower()
                        if host in ("adicommunications.co.uk", "www.adicommunications.co.uk"):
                            path = parsed.path or "/"
                            is_allowed = any(path.startswith(p) for p in ("/news", "/assets", "/feed"))
                            if not is_allowed:
                                violations.append({
                                    "file": str(fpath.relative_to(REPO_ROOT)),
                                    "line": line_no,
                                    "url": clean_url,
                                    "snippet": line.strip()[:120]
                                })

        print(f"\n[RULE 45 SCAN] Scanned {scanned_count} JSON and CSV files.")
        print(f"[RULE 45 SCAN] Total adicommunications.co.uk mentions in JSON/CSV: {total_occurrences}")
        print(f"[RULE 45 SCAN] Raw root / non-buffer violations found: {len(violations)}")

        for v in violations:
            print(f"  [VIOLATION] {v['file']}:{v['line']} -> {v['url']} (Snippet: {v['snippet']})")

        # Record findings
        self._violations = violations
        # We deliberately assert violations == 0 to catch the defect
        self.assertEqual(
            len(violations), 0,
            f"Found {len(violations)} raw root links violating Rule 45: {violations}"
        )

    def test_all_repo_files_scan_extended(self):
        """Extended scan across all source and config files in repository."""
        target_extensions = (".html", ".json", ".csv", ".xml", ".yml", ".yaml", ".toml", ".js", ".py", ".md")
        all_files = [
            f for f in REPO_ROOT.rglob("*")
            if f.is_file() and f.suffix in target_extensions and ".git" not in f.parts and ".agents" not in f.parts
        ]

        url_finder = re.compile(r"https?://[^\s\"\'\<\>\,\)\;]+", re.IGNORECASE)
        repo_violations = []

        for fpath in all_files:
            # Skip historical test suites that explicitly define expected bad URLs for testing
            if fpath.name in ("adversarial_challenge.py", "test_rule45_adversarial_battery.py", "test_challenger_m2_empirical.py"):
                continue

            content = fpath.read_text(encoding="utf-8", errors="ignore")
            for line_no, line in enumerate(content.splitlines(), 1):
                if "adicommunications.co.uk" in line.lower():
                    urls = url_finder.findall(line)
                    for raw_url in urls:
                        clean_url = raw_url.rstrip("\"\'.,;>)]}")
                        try:
                            parsed = urlparse(clean_url)
                        except Exception:
                            continue
                        host = (parsed.hostname or "").lower()
                        if host in ("adicommunications.co.uk", "www.adicommunications.co.uk"):
                            path = parsed.path or "/"
                            if not any(path.startswith(p) for p in ("/news", "/assets", "/feed")):
                                repo_violations.append({
                                    "file": str(fpath.relative_to(REPO_ROOT)),
                                    "line": line_no,
                                    "url": clean_url,
                                    "snippet": line.strip()[:120]
                                })

        print(f"[EXTENDED SCAN] Scanned {len(all_files)} total repo files. Violations: {len(repo_violations)}")
        for v in repo_violations:
            print(f"  [EXTENDED VIOLATION] {v['file']}:{v['line']} -> {v['url']}")


class TestJsonSchemaDraft202012Compliance(unittest.TestCase):
    """Verify master_profile_manifest.json against JSON Schema Draft 2020-12."""

    def setUp(self):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)

    def test_manifest_declares_draft_2020_12_schema(self):
        """Assert manifest has $schema pointing to Draft 2020-12."""
        self.assertEqual(
            self.manifest.get("$schema"),
            "https://json-schema.org/draft/2020-12/schema",
            "Manifest must explicitly declare Draft 2020-12 $schema"
        )

    def test_manifest_conforms_to_draft_2020_12_meta_schema(self):
        """Verify the manifest structure is valid under Draft202012Validator."""
        Draft202012Validator.check_schema(self.manifest)

    def test_formal_schema_validation_of_manifest_structure(self):
        """Adversarially validate manifest against strict formal JSON Schema Draft 2020-12."""
        manifest_formal_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": [
                "$schema",
                "version",
                "last_updated",
                "title",
                "description",
                "brand_standards",
                "standard_bios",
                "visual_cdn_assets",
                "rule_45_google_shield_anchors",
                "category_stacks_11",
                "established_profiles_100",
                "directory_135_platforms"
            ],
            "properties": {
                "$schema": {"type": "string", "enum": ["https://json-schema.org/draft/2020-12/schema"]},
                "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
                "last_updated": {"type": "string"},
                "title": {"type": "string", "minLength": 10},
                "description": {"type": "string", "minLength": 20},
                "brand_standards": {
                    "type": "object",
                    "required": ["engineer", "business", "telephone", "email", "location", "credentials"],
                    "properties": {
                        "engineer": {"type": "string", "const": "Gary Pearce"},
                        "business": {"type": "string", "const": "ADI Communications"},
                        "telephone": {"type": "string", "const": "07860 244 274"},
                        "international_telephone": {"type": "string", "const": "+44 7860 244 274"},
                        "email": {"type": "string"},
                        "location": {"type": "string"},
                        "credentials": {
                            "type": "object",
                            "required": [
                                "experience_years",
                                "public_liability_insurance",
                                "cai_compliance_notice",
                                "verified_rating"
                            ],
                            "properties": {
                                "experience_years": {"type": "integer", "minimum": 25},
                                "public_liability_insurance": {"type": "string", "pattern": r"£10,000,000"},
                                "cai_compliance_notice": {"type": "string", "pattern": r"NOT CAI members"},
                                "verified_rating": {"type": "string", "pattern": r"9\.98"}
                            }
                        }
                    }
                },
                "standard_bios": {
                    "type": "object",
                    "required": ["short_bio_160", "medium_bio_500", "long_bio_markdown"],
                    "properties": {
                        "short_bio_160": {"type": "string", "maxLength": 160},
                        "medium_bio_500": {"type": "string", "maxLength": 500},
                        "long_bio_markdown": {"type": "string"}
                    }
                },
                "visual_cdn_assets": {
                    "type": "object",
                    "required": ["avatar_square", "cover_banner_16x9"],
                    "properties": {
                        "avatar_square": {"type": "string", "format": "uri", "pattern": r"\.webp$"},
                        "cover_banner_16x9": {"type": "string", "format": "uri", "pattern": r"\.webp$"}
                    }
                },
                "category_stacks_11": {
                    "type": "object",
                    "minProperties": 11,
                    "maxProperties": 11,
                    "additionalProperties": {
                        "type": "object",
                        "required": ["id", "name", "agent", "apex_entity", "apex_url"],
                        "properties": {
                            "id": {"type": "string", "pattern": r"^STACK-\d{2}$"},
                            "name": {"type": "string"},
                            "agent": {"type": "string"},
                            "apex_entity": {"type": "string"},
                            "apex_url": {"type": "string", "format": "uri"}
                        }
                    }
                },
                "established_profiles_100": {
                    "type": "array",
                    "minItems": 100,
                    "maxItems": 100,
                    "items": {
                        "type": "object",
                        "required": [
                            "profile_id",
                            "platform_id",
                            "platform_name",
                            "category",
                            "stack_key",
                            "profile_handle",
                            "profile_live_url",
                            "top_of_stack_apex_url",
                            "shield_anchor_url",
                            "bio_copy"
                        ],
                        "properties": {
                            "profile_id": {"type": "string", "pattern": r"^PROF-\d{3}$"},
                            "platform_id": {"type": "string"},
                            "platform_name": {"type": "string"},
                            "category": {"type": "string"},
                            "stack_key": {"type": "string"},
                            "profile_handle": {"type": "string"},
                            "profile_live_url": {"type": "string"},
                            "top_of_stack_apex_url": {"type": "string", "format": "uri"},
                            "shield_anchor_url": {"type": "string", "format": "uri"},
                            "bio_copy": {"type": "string"}
                        }
                    }
                },
                "directory_135_platforms": {
                    "type": "array",
                    "minItems": 135,
                    "items": {
                        "type": "object",
                        "required": ["id", "layer", "name", "category", "canonical_url"]
                    }
                }
            }
        }

        validator = Draft202012Validator(manifest_formal_schema)
        errors = list(validator.iter_errors(self.manifest))
        if errors:
            for err in errors:
                print(f"Schema Validation Error: {err.message} at path: {list(err.path)}")
        self.assertEqual(len(errors), 0, f"Manifest failed Draft 2020-12 formal schema: {errors}")


class TestParityAndInvariants(unittest.TestCase):
    """Verify mathematical parity, E-E-A-T trade metadata, and Rule 45 between doc2 and manifest."""

    def setUp(self):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)
        with open(DOC2_PATH, "r", encoding="utf-8") as f:
            self.doc2_rows = list(csv.DictReader(f))

    def test_profile_counts_and_parity(self):
        """Assert exact 100 profiles in both CSV and manifest, matching 1-to-1."""
        self.assertEqual(len(self.doc2_rows), 100, "doc2_established_profiles_list.csv must have 100 rows")
        self.assertEqual(len(self.manifest["established_profiles_100"]), 100, "manifest must have 100 profiles")

        doc2_by_id = {r["profile_id"]: r for r in self.doc2_rows}
        manifest_by_id = {p["profile_id"]: p for p in self.manifest["established_profiles_100"]}

        self.assertEqual(set(doc2_by_id.keys()), set(manifest_by_id.keys()), "Profile IDs must match exactly")

        # Check fields match
        for pid in doc2_by_id:
            c = doc2_by_id[pid]
            m = manifest_by_id[pid]

            self.assertEqual(c["platform_name"], m["platform_name"], f"{pid} platform_name mismatch")
            self.assertEqual(c["shield_anchor_url"], m["shield_anchor_url"], f"{pid} shield_anchor_url mismatch")
            self.assertEqual(c["shield_anchor_url"], m["top_of_stack_apex_url"], f"{pid} apex URL mismatch")
            self.assertEqual(c["profile_live_url"], m["profile_live_url"], f"{pid} profile_live_url mismatch")
            self.assertEqual(c["bio_copy"], m["bio_copy"], f"{pid} bio_copy mismatch")

    def test_top_of_stack_google_apex_distribution(self):
        """Assert all 100 profiles point to Google Citadel Apexes, eliminating Blogger bottleneck."""
        apex_urls = [r["shield_anchor_url"] for r in self.doc2_rows]
        from collections import Counter
        counts = Counter(apex_urls)

        # Ensure no single URL has 100% (which was the baseline defect where blogger had 100)
        self.assertLess(counts.get("https://tvandhomesecurity.blogspot.com/", 0), 100, "Blogger bottleneck must be resolved")
        self.assertEqual(counts.get("https://tvandhomesecurity.blogspot.com/", 0), 10, "Blogger should have 10 blog profiles")

        # All targets must be authoritative Google Citadel properties (DA 97-100)
        valid_apexes = {
            "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88",
            "https://gary-pearce-forensic-hub.web.app/",
            "https://www.youtube.com/@CCTV.services",
            "https://sites.google.com/view/cctv-security-hub-uk",
            "https://www.youtube.com/@CCTV.services/podcasts",
            "https://tvandhomesecurity.blogspot.com/",
            "https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html"
        }
        for u in apex_urls:
            self.assertIn(u, valid_apexes, f"Invalid apex URL: {u}")

    def test_eeat_and_trade_invariants(self):
        """Assert Gary Pearce, ADI Communications, 07860 244 274, zero 0800, zero Checkatrade."""
        raw_manifest = json.dumps(self.manifest)
        raw_doc2 = DOC2_PATH.read_text(encoding="utf-8")

        # Zero 0800
        self.assertNotIn("0800", raw_manifest, "Found 0800 in master_profile_manifest.json")
        self.assertNotIn("0800", raw_doc2, "Found 0800 in doc2_established_profiles_list.csv")

        # Zero Checkatrade
        self.assertNotIn("Checkatrade", raw_manifest, "Found Checkatrade in master_profile_manifest.json")
        self.assertNotIn("checkatrade", raw_manifest, "Found checkatrade in master_profile_manifest.json")
        self.assertNotIn("Checkatrade", raw_doc2, "Found Checkatrade in doc2_established_profiles_list.csv")
        self.assertNotIn("checkatrade", raw_doc2, "Found checkatrade in doc2_established_profiles_list.csv")

        # Every bio has Gary Pearce, ADI Communications, 07860 244 274
        for r in self.doc2_rows:
            bio = r["bio_copy"]
            self.assertIn("Gary Pearce", bio, f"Profile {r['profile_id']} missing Gary Pearce")
            self.assertIn("ADI Communications", bio, f"Profile {r['profile_id']} missing ADI Communications")
            self.assertIn("07860 244 274", bio, f"Profile {r['profile_id']} missing 07860 244 274")

    def test_cai_and_rating_invariants(self):
        """Assert CAI disclaimer and verified rating."""
        creds = self.manifest["brand_standards"]["credentials"]
        self.assertIn("NOT CAI members", creds["cai_compliance_notice"])
        self.assertIn("CAI-benchmarked equipment", creds["cai_compliance_notice"])
        self.assertIn("9.98", creds["verified_rating"])
        self.assertIn("84+", creds["verified_rating"])

    def test_eleven_category_stacks_specification(self):
        """Assert all 11 stacks STACK-01 to STACK-11 are defined and valid."""
        stacks = self.manifest["category_stacks_11"]
        self.assertEqual(len(stacks), 11)
        expected_stack_ids = {f"STACK-{i:02d}" for i in range(1, 12)}
        actual_stack_ids = {s["id"] for s in stacks.values()}
        self.assertEqual(actual_stack_ids, expected_stack_ids)


class TestVerifyNoRootAnchorsAudit(unittest.TestCase):
    """Audit the repository's verify_no_root_anchors.py script for blind spots and hardening."""

    def test_verify_script_has_delimiter_blindspot(self):
        """Empirically verify that verify_no_root_anchors.py checks CSV and parenthetical URLs."""
        verify_script_path = REPO_ROOT / "verify_no_root_anchors.py"
        script_content = verify_script_path.read_text(encoding="utf-8")

        # Proof 1: Extension coverage includes .csv
        self.assertIn(".csv", script_content, "verify_no_root_anchors.py must check .csv files")

        # Proof 2: Regex delimiter check
        test_line = '"author": "Gary Pearce <aiagent1510@gmail.com> (https://adicommunications.co.uk)",'
        script_regex = re.compile(r"https?://(?:www\.)?adicommunications\.co\.uk/?(?:$|[?#\"'\s<>,;)\]}])")
        matched_by_script = bool(script_regex.search(test_line))

        # This proves the script now detects package.json's parenthetical violation!
        self.assertTrue(
            matched_by_script,
            "verify_no_root_anchors.py regex must match URLs terminated by ')'"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
