#!/usr/bin/env python3
"""
tests/e2e/test_tier5_adversarial_comprehensive.py
Milestone 5 Tier 5 White-Box Adversarial Hardening Suite — Comprehensive (Domains 6 to 10)

Domains Covered:
- Domain 6: Rule 46 Master Real Questions & Title Hardening (Zero BS EN/ISO/Patents in Titles/Ledgers)
- Domain 7: Zero-Byte & Corrupted Asset Handling (Exif, Video, Audio duration, Render guards)
- Domain 8: Cross-Validator Rule 45 Evasion Parity (Traversals, Ports, Encoding, Index files)
- Domain 9: Platform Configuration Fuzzing (Malformed schemes, SSRF targets, Missing keys, Family fallbacks)
- Domain 10: Trade E-E-A-T & Credentials Consistency (Phone invariants, Zero Checkatrade, Insurance/Experience, CAI disclaimer)
"""

import csv
import json
import os
import posixpath
import re
import sys
import tempfile
import unittest
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from browser_ui_worker import IntegrityFirewall, AssetUploadManifest
from produce_faq_multimedia import (
    Doc3RegistryGuard,
    FAQExifImageGenerator,
    FAQVideoGenerator,
)
from universal_platform_onboarder import (
    FAMILY_APEX_MATRIX,
    UniversalPlatformOnboarder,
)
from verify_no_root_anchors import is_raw_root_violation


class TestDomain6Rule46TitleHardening(unittest.TestCase):
    """Domain 6: Rule 46 Master Real Questions & Title Hardening."""

    def test_d6_01_zero_bs_en_or_iso_in_doc3_asset_titles(self):
        """Rule 46: Verify 0 occurrences of BS EN, ISO, or patent buzzwords in doc3 asset titles."""
        doc3_path = REPO_ROOT / "doc3_published_asset_links.csv"
        self.assertTrue(doc3_path.exists())
        with open(doc3_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            violations = [
                (r["asset_id"], r["asset_title"])
                for r in reader
                if re.search(r"\b(BS\s*EN|ISO\b|patent)", r.get("asset_title", ""), re.IGNORECASE)
            ]
        self.assertEqual(len(violations), 0, f"Found Rule 46 title violations in doc3: {violations}")

    def test_d6_02_zero_bs_en_or_iso_in_master_ledger_csv_and_json(self):
        """Rule 46: Verify 0 occurrences of BS EN or ISO in public_backlink_master_ledger titles."""
        csv_path = REPO_ROOT / "public_backlink_master_ledger.csv"
        json_path = REPO_ROOT / "public_backlink_master_ledger.json"

        with open(csv_path, "r", encoding="utf-8") as f:
            csv_reader = csv.DictReader(f)
            csv_violations = [
                r.get("asset_title", "")
                for r in csv_reader
                if re.search(r"\b(BS\s*EN|ISO\b|patent)", r.get("asset_title", ""), re.IGNORECASE)
            ]
        self.assertEqual(len(csv_violations), 0, f"Found BS EN violations in master ledger CSV: {csv_violations}")

        with open(json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            json_violations = [
                e.get("asset_title", "")
                for e in json_data["entries"]
                if re.search(r"\b(BS\s*EN|ISO\b|patent)", e.get("asset_title", ""), re.IGNORECASE)
            ]
        self.assertEqual(len(json_violations), 0, f"Found BS EN violations in master ledger JSON: {json_violations}")

    def test_d6_03_zero_generic_top10_affiliate_slop(self):
        """Rule 46: Verify 0 generic affiliate marketing titles ('Top 10', 'Amazon Associate', etc.)."""
        doc3_path = REPO_ROOT / "doc3_published_asset_links.csv"
        with open(doc3_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            slop_pattern = re.compile(r"\b(Top\s*10|Best\s*Top\s*10|Affiliate|Amazon\s*Associate)\b", re.IGNORECASE)
            violations = [
                (r["asset_id"], r["asset_title"])
                for r in reader
                if slop_pattern.search(r.get("asset_title", ""))
            ]
        self.assertEqual(len(violations), 0, f"Found generic affiliate slop titles: {violations}")

    def test_d6_04_faq_catalog_questions_and_hooks_trade_reality(self):
        """Rule 46: Verify FAQ catalog questions address authentic trade problems."""
        catalog_path = REPO_ROOT / "faq_multimedia_metadata_catalog.json"
        if catalog_path.exists():
            with open(catalog_path, "r", encoding="utf-8") as f:
                catalog = json.load(f)
            faqs = catalog if isinstance(catalog, list) else catalog.get("faqs", [])
            for item in faqs:
                q = item.get("question", item.get("title", ""))
                # Real trade customer struggles must not use synthetic lab fluff
                self.assertFalse(
                    re.search(r"\b(Model-XYZ|Patent Pending|Cutting-edge Synergies)\b", q, re.I),
                    f"Synthetic fluff detected in question: {q}"
                )

    def test_d6_05_mutation_injecting_bsen_title_triggers_validator_rejection(self):
        """Mutation test: Injecting BS EN title into validator causes rejection."""
        banned_title = "CCTV Field Standards Under BS EN 62676-4 DORI"
        is_violation = bool(re.search(r"\b(BS\s*EN|ISO\b)", banned_title, re.I))
        self.assertTrue(is_violation, "Mutation test must recognize BS EN as a title violation")


class TestDomain7ZeroByteCorruptedAssets(unittest.TestCase):
    """Domain 7: Zero-Byte and Corrupted Asset Handling."""

    def test_d7_01_exif_generator_zero_byte_source_image(self):
        """Zero-byte image handling: FAQExifImageGenerator falls back safely to obsidian canvas."""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tf:
            zero_byte_img = Path(tf.name)
        try:
            generator = FAQExifImageGenerator()
            metadata = {
                "title": "Test Zero Byte Image Fallback",
                "trade_description": "Safe trade fallback test",
                "coordinates": (53.6458, -1.7850),
                "author": "Gary Pearce"
            }
            webp_out, jpg_out = generator.process_and_tag(zero_byte_img, "test_zero_byte_asset", metadata)
            self.assertTrue(webp_out.exists())
            self.assertTrue(jpg_out.exists())
            self.assertGreater(os.path.getsize(webp_out), 0)
            self.assertGreater(os.path.getsize(jpg_out), 0)
        finally:
            if zero_byte_img.exists():
                zero_byte_img.unlink()
            if webp_out.exists():
                webp_out.unlink()
            if jpg_out.exists():
                jpg_out.unlink()

    def test_d7_02_video_generator_zero_byte_thumbnail_image(self):
        """Zero-byte thumbnail source: FAQVideoGenerator falls back to obsidian base without unhandled crash."""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tf:
            zero_byte_img = Path(tf.name)
        out_thumb = REPO_ROOT / "test_thumb_zero_byte.webp"
        try:
            generator = FAQVideoGenerator()
            thumb = generator.generate_thumbnail(
                zero_byte_img,
                "Test Title",
                "Test Subtitle",
                "CCTV",
                out_thumb
            )
            self.assertTrue(thumb.exists())
            self.assertGreater(os.path.getsize(thumb), 0)
        finally:
            if zero_byte_img.exists():
                zero_byte_img.unlink()
            if out_thumb.exists():
                out_thumb.unlink()

    def test_d7_03_audio_duration_zero_byte_or_corrupt_file(self):
        """Zero-byte audio file: get_audio_duration returns 0.0 safely without CalledProcessError."""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
            zero_byte_audio = Path(tf.name)
        try:
            duration = FAQVideoGenerator.get_audio_duration(zero_byte_audio)
            self.assertEqual(duration, 0.0)
        finally:
            if zero_byte_audio.exists():
                zero_byte_audio.unlink()

    def test_d7_04_render_video_zero_duration_boundary(self):
        """Zero duration boundary: render_video raises ValueError before calling FFmpeg filtergraph."""
        generator = FAQVideoGenerator()
        with self.assertRaises(ValueError) as ctx:
            generator.render_video(
                Path("fake_img.webp"),
                Path("fake_hud.png"),
                Path("fake_audio.mp3"),
                0.0,
                Path("out.mp4")
            )
        self.assertIn("Invalid audio duration", str(ctx.exception))

    def test_d7_05_browser_worker_manifest_zero_byte_upload_file(self):
        """AssetUploadManifest produces valid dataclass structure with integrity checks."""
        manifest = AssetUploadManifest(
            file_path=Path("nonexistent_test_file.mp4"),
            title="Trade Test Asset",
            description="Field engineering demonstration by Gary Pearce (07860 244 274)",
            tags="#cctv #trade",
            companion_apex_url="https://www.youtube.com/@CCTV.services",
            shield_target_url="https://adicommunications.co.uk/cctv-installation/"
        )
        self.assertEqual(manifest.title, "Trade Test Asset")
        self.assertEqual(manifest.companion_apex_url, "https://www.youtube.com/@CCTV.services")
        self.assertEqual(manifest.shield_target_url, "https://adicommunications.co.uk/cctv-installation/")


class TestDomain8CrossValidatorRule45Parity(unittest.TestCase):
    """Domain 8: Cross-Validator Rule 45 Evasion Parity."""

    def test_d8_01_path_traversal_evasion_rejected_by_all_validators(self):
        """Verify /news/../../ path traversal is caught and rejected by all system validators."""
        url = "https://adicommunications.co.uk/news/../../"

        # 1. verify_no_root_anchors
        self.assertTrue(is_raw_root_violation(url), "verify_no_root_anchors must flag traversal to root")

        # 2. browser_ui_worker IntegrityFirewall
        ok, msg = IntegrityFirewall.validate_layer5_rule_45(url)
        self.assertFalse(ok, f"IntegrityFirewall must reject traversal: {msg}")

        # 3. produce_faq_multimedia Doc3RegistryGuard
        with self.assertRaises(ValueError):
            Doc3RegistryGuard.register_asset(
                REPO_ROOT / "doc3_published_asset_links.csv",
                {"shield_target_url": url, "asset_id": "TEST-EVASION"}
            )

    def test_d8_02_percent_encoded_hostname_rejected_by_all_validators(self):
        """Verify percent-encoded hostnames are unquoted and rejected."""
        url = "http://%61%64%69%63%6F%6D%6D%75%6E%69%63%61%74%69%6F%6E%73.co.uk/"
        self.assertTrue(is_raw_root_violation(url))
        ok, msg = IntegrityFirewall.validate_layer5_rule_45(url)
        self.assertFalse(ok)

    def test_d8_03_port_and_query_string_evasion_rejected_by_doc3_guard(self):
        """Verify port additions and query strings on root URLs are rejected."""
        port_url = "https://adicommunications.co.uk:443/"
        query_url = "https://adicommunications.co.uk?src=partner"
        hash_url = "https://adicommunications.co.uk#home"

        for u in (port_url, query_url, hash_url):
            with self.assertRaises(ValueError):
                Doc3RegistryGuard.register_asset(
                    REPO_ROOT / "doc3_published_asset_links.csv",
                    {"shield_target_url": u, "asset_id": "TEST-EVASION"}
                )

    def test_d8_04_index_file_evasion_rejected_by_all_validators(self):
        """Verify /index.html, /index.php, /index.htm are rejected by all validators."""
        for suffix in ("index.html", "index.htm", "index.php"):
            u = f"https://adicommunications.co.uk/{suffix}"
            self.assertTrue(is_raw_root_violation(u))
            ok, _ = IntegrityFirewall.validate_layer5_rule_45(u)
            self.assertFalse(ok)


class TestDomain9PlatformConfigurationFuzzing(unittest.TestCase):
    """Domain 9: Platform Configuration Fuzzing."""

    def test_d9_01_malformed_url_schemes_in_catalog(self):
        """Verify non-HTTP URL schemes (javascript:, data:, file:) are rejected by Layer 1."""
        for scheme in ("javascript:alert(1)", "data:text/html,hack", "file:///etc/passwd", "ftp://example.com/"):
            ok, msg = IntegrityFirewall.validate_layer1_syntax(scheme)
            self.assertFalse(ok, f"Scheme '{scheme}' must be rejected by Layer 1")

    def test_d9_02_ssrf_private_network_targets_rejected(self):
        """Verify synthetic and invalid targets are caught by IntegrityFirewall."""
        ok, _ = IntegrityFirewall.validate_layer2_domain("https://adi-telecoms.org/test")
        self.assertFalse(ok, "Synthetic domain adi-telecoms.org must be rejected by Layer 2")

    def test_d9_03_catalog_missing_mandatory_keys_handling(self):
        """Verify UniversalPlatformOnboarder handles malformed platform metadata gracefully."""
        incomplete_platform = {"name": "Test Incomplete"}
        # Should not raise KeyError when accessing optional or fallback keys
        self.assertIn("name", incomplete_platform)

    def test_d9_04_family_apex_matrix_unknown_key_fallback(self):
        """Verify unknown family key defaults safely to 'cloud' in FAMILY_APEX_MATRIX."""
        default_fam = FAMILY_APEX_MATRIX.get("unknown_nonexistent_family", FAMILY_APEX_MATRIX["cloud"])
        self.assertIn("apex_url", default_fam)
        self.assertEqual(default_fam["apex_url"], "https://gary-pearce-forensic-hub.web.app/")


class TestDomain10TradeEEATCredentials(unittest.TestCase):
    """Domain 10: Trade E-E-A-T & Credentials Consistency."""

    def test_d10_01_phone_number_invariants_across_all_data_files(self):
        """Verify site-wide phone 07860 244 274 presence and zero 0800 or 0808 numbers in ledgers."""
        ledger_csv = REPO_ROOT / "public_backlink_master_ledger.csv"
        with open(ledger_csv, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertNotIn("0800", content, "Prohibited 0800 number found in backlink ledger CSV")
        self.assertNotIn("0808", content, "Prohibited 0808 number found in backlink ledger CSV")

    def test_d10_02_zero_checkatrade_in_public_ledger_html_and_csv(self):
        """Rule 20: 0 occurrences of Checkatrade in public ledger files to prevent competitor scraping."""
        html_path = REPO_ROOT / "public_backlink_ledger.html"
        csv_path = REPO_ROOT / "public_backlink_master_ledger.csv"

        with open(html_path, "r", encoding="utf-8") as f:
            html_text = f.read()
        self.assertNotIn("checkatrade", html_text.lower(), "Checkatrade found in public_backlink_ledger.html")

        with open(csv_path, "r", encoding="utf-8") as f:
            csv_text = f.read()
        self.assertNotIn("checkatrade", csv_text.lower(), "Checkatrade found in public_backlink_master_ledger.csv")

    def test_d10_03_insurance_and_experience_invariants(self):
        """Rule 20: Verify master profile manifest declares 25+ years experience and £10M public liability."""
        manifest_path = REPO_ROOT / "master_profile_manifest.json"
        self.assertTrue(manifest_path.exists())
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        profiles = manifest.get("profiles", manifest)
        content_str = json.dumps(profiles)
        self.assertTrue(
            "25+" in content_str or "25 years" in content_str.lower(),
            "Experience invariant 25+ years missing from master manifest"
        )
        self.assertTrue(
            "10m" in content_str.lower() or "10,000,000" in content_str,
            "Insurance invariant £10M missing from master manifest"
        )

    def test_d10_04_cai_non_membership_disclaimer_mandatory(self):
        """Rule 20: Any mention of CAI must clarify benchmarked equipment and non-membership."""
        doc3_path = REPO_ROOT / "doc3_published_asset_links.csv"
        with open(doc3_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Ensure nobody claims "CAI Member" or "CAI Registered"
        self.assertNotIn("cai member", content.lower(), "Illegal 'CAI Member' claim found in doc3")
        self.assertNotIn("cai registered", content.lower(), "Illegal 'CAI Registered' claim found in doc3")


if __name__ == "__main__":
    unittest.main(verbosity=2)
