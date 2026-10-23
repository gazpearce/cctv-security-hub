#!/usr/bin/env python3
"""
tests/test_challenger_m4vid_2.py
================================
Adversarial Challenger Test Suite: Milestone M4-VID
Rule 45 Evasion & Live Edge Deployment Challenger

Author: Challenger M4-VID 2
Role: Empirical Challenger (critic, specialist)
Verification Targets:
  1. Multi-pass Rule 45 Evasion Scanner across all 279 records in doc3, CSV, JSON, HTML.
  2. Tier 3 Video Air-Gap: 31 Tier 3 video assets contain ABSOLUTELY ZERO occurrences
     of 'adicommunications.co.uk' and link 100% exclusively to YouTube Apex.
  3. Live Edge Probe: Connect via urllib to https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html,
     assert HTTP 200, payload > 500KB, and exactly 279 matching DOM rows.
  4. 4-Way Mathematical Parity & Strict Schema Integrity (Draft 2020-12).
  5. Checkatrade Ban & Direct Phone Standardization (07860 244 274).
"""

import csv
import html
import json
import os
import re
import sys
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent

DOC3_FILE = REPO_ROOT / "doc3_published_asset_links.csv"
CSV_FILE = REPO_ROOT / "public_backlink_master_ledger.csv"
JSON_FILE = REPO_ROOT / "public_backlink_master_ledger.json"
HTML_FILE = REPO_ROOT / "public_backlink_ledger.html"
SCHEMA_FILE = REPO_ROOT / "public_backlink_ledger.schema.json"
PLATFORM_CATALOG = REPO_ROOT / "master_multicategory_platform_catalog.json"
VIDEO_CATALOG = REPO_ROOT / "video_stack_50_catalog.json"

LIVE_EDGE_URL = "https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html"
YOUTUBE_APEX = "https://www.youtube.com/@CCTV.services"


class TestMultiPassRule45EvasionScanner(unittest.TestCase):
    """
    Class 1: Adversarial Multi-Pass Rule 45 Evasion Scanner.
    Exhaustively scans for raw root commercial links in all 279 records across
    doc3_published_asset_links.csv, public_backlink_master_ledger.csv,
    public_backlink_master_ledger.json, and public_backlink_ledger.html.
    """

    @classmethod
    def setUpClass(cls):
        with open(DOC3_FILE, "r", encoding="utf-8") as f:
            cls.doc3_rows = list(csv.DictReader(f))

        with open(CSV_FILE, "r", encoding="utf-8") as f:
            cls.csv_rows = list(csv.DictReader(f))

        with open(JSON_FILE, "r", encoding="utf-8") as f:
            cls.json_data = json.load(f)

        with open(HTML_FILE, "r", encoding="utf-8") as f:
            cls.html_content = f.read()

        cls.soup = BeautifulSoup(cls.html_content, "html.parser")

    def _detect_raw_root_leak(self, text: str) -> bool:
        """
        Adversarial detector for any raw root URL to adicommunications.co.uk:
        - http / https
        - www or non-www
        - uppercase / mixed case variations
        - URL encoded representations (%2f, %2F, %3A, etc.)
        - trailing dots (adicommunications.co.uk.)
        - default index filenames (/index.html, /index.php, /index.htm)
        - root path variations ('', '/', '/?')
        """
        if not text or not isinstance(text, str):
            return False

        unquoted = urllib.parse.unquote(text).lower()

        if "adicommunications.co.uk" not in unquoted:
            return False

        root_patterns = [
            r"https?://(?:www\.)?adicommunications\.co\.uk\.?(?::\d+)?/?(?:\?.*|#.*)?$",
            r"https?://(?:www\.)?adicommunications\.co\.uk\.?(?::\d+)?/index\.(?:html?|php)(?:\?.*|#.*)?$",
            r"^adicommunications\.co\.uk\.?(?::\d+)?/?(?:\?.*|#.*)?$",
            r"^www\.adicommunications\.co\.uk\.?(?::\d+)?/?(?:\?.*|#.*)?$"
        ]

        for pat in root_patterns:
            if re.search(pat, unquoted.strip()):
                return True

        raw_anchor_patterns = [
            r"href=[\"']https?://(?:www\.)?adicommunications\.co\.uk\.?/?[\"']",
            r"href=[\"']https?://(?:www\.)?adicommunications\.co\.uk\.?/index\.(?:html?|php)[\"']"
        ]
        for pat in raw_anchor_patterns:
            if re.search(pat, text, re.IGNORECASE):
                return True

        return False

    def test_01_doc3_zero_raw_root_leaks_across_all_279_rows(self):
        """Multi-pass scan of all columns in doc3_published_asset_links.csv."""
        violations = []
        for idx, row in enumerate(self.doc3_rows, 1):
            for col, val in row.items():
                if self._detect_raw_root_leak(val):
                    violations.append((idx, row.get("asset_id"), col, val))
        self.assertEqual(violations, [], f"Raw root links found in doc3: {violations}")

    def test_02_master_csv_zero_raw_root_leaks_across_all_279_rows(self):
        """Multi-pass scan of all cells in public_backlink_master_ledger.csv."""
        violations = []
        for idx, row in enumerate(self.csv_rows, 1):
            for col, val in row.items():
                if self._detect_raw_root_leak(val):
                    violations.append((idx, row.get("platform"), col, val))
        self.assertEqual(violations, [], f"Raw root links found in master CSV: {violations}")

    def test_03_master_json_zero_raw_root_leaks(self):
        """Recursive deep scan of public_backlink_master_ledger.json."""
        violations = []

        def walk(val, path=""):
            if isinstance(val, str):
                if self._detect_raw_root_leak(val):
                    violations.append((path, val))
            elif isinstance(val, dict):
                for k, v in val.items():
                    walk(v, f"{path}.{k}")
            elif isinstance(val, list):
                for i, v in enumerate(val):
                    walk(v, f"{path}[{i}]")

        walk(self.json_data, "root")
        self.assertEqual(violations, [], f"Raw root links found in master JSON: {violations}")

    def test_04_html_hrefs_and_text_zero_raw_root_leaks(self):
        """Multi-pass scan of all <a> tags and raw HTML content."""
        violations = []
        for a in self.soup.find_all("a"):
            href = a.get("href", "")
            if self._detect_raw_root_leak(href):
                violations.append(("a_href", str(a)))

        raw_matches = re.findall(
            r"https?://(?:www\.)?adicommunications\.co\.uk/?[\"'\s<>]",
            self.html_content,
            re.IGNORECASE
        )
        self.assertEqual(violations, [], f"Raw root links found in HTML anchor tags: {violations}")
        self.assertEqual(raw_matches, [], f"Raw root links found in HTML text body: {raw_matches}")


class TestTier3VideoCitadelAirGap(unittest.TestCase):
    """
    Class 2: Tier 3 Video Citadel Air-Gap Firewall.
    Scans all 31 Tier 3 video assets.
    Asserts ABSOLUTE ZERO occurrences of 'adicommunications.co.uk' and
    100% exclusive linking to https://www.youtube.com/@CCTV.services.
    """

    @classmethod
    def setUpClass(cls):
        with open(PLATFORM_CATALOG, "r", encoding="utf-8") as f:
            cat = json.load(f)
        all_video_platforms = cat["category_stacks"]["video"]["platforms"]

        cls.tier3_platforms = [
            p for p in all_video_platforms
            if "Tier 3" in str(p.get("tier", "")) or p.get("tier") == 3
        ]
        cls.tier3_pids = {p["platform_id"] for p in cls.tier3_platforms}

        with open(DOC3_FILE, "r", encoding="utf-8") as f:
            cls.doc3_rows = list(csv.DictReader(f))

        cls.tier3_doc3_rows = [
            r for r in cls.doc3_rows
            if r.get("parent_profile_id") in cls.tier3_pids
        ]

        cls.tier3_public_urls = {r["asset_public_url"] for r in cls.tier3_doc3_rows}
        cls.tier3_titles = {r["asset_title"] for r in cls.tier3_doc3_rows}

        with open(CSV_FILE, "r", encoding="utf-8") as f:
            cls.csv_rows = list(csv.DictReader(f))

        cls.tier3_csv_rows = [
            r for r in cls.csv_rows
            if r.get("public_live_url") in cls.tier3_public_urls
            or r.get("asset_title") in cls.tier3_titles
        ]

        with open(JSON_FILE, "r", encoding="utf-8") as f:
            cls.json_data = json.load(f)

        cls.tier3_json_entries = [
            e for e in cls.json_data.get("entries", [])
            if e.get("tenant_url") in cls.tier3_public_urls
            or e.get("asset_title") in cls.tier3_titles
        ]

        with open(HTML_FILE, "r", encoding="utf-8") as f:
            cls.html_content = f.read()

        cls.soup = BeautifulSoup(cls.html_content, "html.parser")

    def test_05_tier3_video_platform_census_count_is_31(self):
        """Asserts exactly 31 Tier 3 video platforms exist in the catalog."""
        self.assertEqual(
            len(self.tier3_platforms),
            31,
            f"Expected 31 Tier 3 video platforms, got {len(self.tier3_platforms)}"
        )

    def test_06_doc3_tier3_video_rows_zero_adicommunications_occurrences(self):
        """Asserts exactly 31 Tier 3 video rows in doc3 contain ABSOLUTELY ZERO occurrences of 'adicommunications.co.uk'."""
        self.assertEqual(
            len(self.tier3_doc3_rows),
            31,
            f"Expected 31 Tier 3 video rows in doc3, found {len(self.tier3_doc3_rows)}"
        )

        leaks = []
        for idx, row in enumerate(self.tier3_doc3_rows, 1):
            for col, val in row.items():
                if "adicommunications.co.uk" in val.lower():
                    leaks.append((idx, row.get("asset_id"), col, val))

        self.assertEqual(leaks, [], f"Tier 3 video row leaked adicommunications.co.uk in doc3: {leaks}")

    def test_07_doc3_tier3_video_rows_link_strictly_to_youtube_apex(self):
        """Asserts all 31 Tier 3 video rows in doc3 link strictly to YouTube Apex in both apex and shield columns."""
        for r in self.tier3_doc3_rows:
            aid = r.get("asset_id")
            pname = r.get("platform_name")
            self.assertEqual(
                r.get("top_of_stack_apex_url"),
                YOUTUBE_APEX,
                f"{aid} ({pname}) top_of_stack_apex_url != YouTube Apex"
            )
            self.assertEqual(
                r.get("shield_target_url"),
                YOUTUBE_APEX,
                f"{aid} ({pname}) shield_target_url != YouTube Apex"
            )

    def test_08_csv_tier3_video_entries_zero_adicommunications_and_youtube_only(self):
        """Asserts all 31 Tier 3 video rows in master CSV have 0 domain leaks and link strictly to YouTube Apex."""
        self.assertEqual(
            len(self.tier3_csv_rows),
            31,
            f"Expected 31 Tier 3 video entries in master CSV, found {len(self.tier3_csv_rows)}"
        )

        for r in self.tier3_csv_rows:
            pname = r.get("platform")
            for k, v in r.items():
                self.assertNotIn(
                    "adicommunications.co.uk",
                    str(v).lower(),
                    f"Domain leaked in Tier 3 CSV row {pname} field {k}: {v}"
                )

            self.assertEqual(r.get("top_of_stack_apex_url"), YOUTUBE_APEX)
            self.assertEqual(r.get("shield_target_url"), YOUTUBE_APEX)

    def test_09_json_tier3_video_entries_zero_adicommunications_and_youtube_only(self):
        """Asserts Tier 3 video entries in JSON ledger have 0 domain leaks and link strictly to YouTube Apex."""
        self.assertEqual(
            len(self.tier3_json_entries),
            31,
            f"Expected 31 Tier 3 video entries in JSON, found {len(self.tier3_json_entries)}"
        )

        for entry in self.tier3_json_entries:
            pname = entry.get("platform")
            for k, v in entry.items():
                self.assertNotIn(
                    "adicommunications.co.uk",
                    str(v).lower(),
                    f"Domain leaked in Tier 3 entry {pname} field {k}: {v}"
                )

            self.assertEqual(entry.get("apex_target"), YOUTUBE_APEX, f"{pname} apex_target != YouTube Apex")
            self.assertEqual(entry.get("shield_target_url"), YOUTUBE_APEX, f"{pname} shield_target_url != YouTube Apex")
            self.assertEqual(entry.get("top_of_stack_apex_url"), YOUTUBE_APEX, f"{pname} top_of_stack_apex_url != YouTube Apex")

    def test_10_html_tier3_table_rows_air_gap_integrity(self):
        """Asserts Tier 3 rows in public_backlink_ledger.html table render zero adicommunications.co.uk links."""
        rows = self.soup.find_all("tr", class_=re.compile("hover:bg-white"))
        tier3_html_rows = []
        for tr in rows:
            for u in self.tier3_public_urls:
                if u in str(tr):
                    tier3_html_rows.append(tr)
                    break

        self.assertEqual(
            len(tier3_html_rows),
            31,
            f"Expected exactly 31 Tier 3 HTML rows, found {len(tier3_html_rows)}"
        )

        for tr in tier3_html_rows:
            tr_str = str(tr).lower()
            self.assertNotIn(
                "adicommunications.co.uk",
                tr_str,
                f"HTML row for Tier 3 platform leaked adicommunications.co.uk: {tr}"
            )


class TestLiveFirebaseEdgeDeploymentProbe(unittest.TestCase):
    """
    Class 3: Live Firebase Edge Deployment Probe.
    Connects via urllib to https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html.
    Asserts HTTP 200, payload > 500KB, and exactly 279 matching DOM rows.
    """

    @classmethod
    def setUpClass(cls):
        cls.live_response_code = None
        cls.live_payload_bytes = None
        cls.live_html = ""
        cls.live_headers = {}
        cls.fetch_error = None

        cache_buster = int(time.time())
        url_with_cb = f"{LIVE_EDGE_URL}?cb={cache_buster}"
        req = urllib.request.Request(
            url_with_cb,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ADI-Edge-Challenger/2.0",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                cls.live_response_code = resp.status
                cls.live_payload_bytes = resp.read()
                cls.live_html = cls.live_payload_bytes.decode("utf-8")
                cls.live_headers = dict(resp.headers)
        except Exception as e:
            cls.fetch_error = str(e)

        with open(DOC3_FILE, "r", encoding="utf-8") as f:
            doc3_rows = list(csv.DictReader(f))

        cls.tier3_urls = {
            r["asset_public_url"] for r in doc3_rows
            if r.get("parent_profile_id", "").startswith("PLAT-VID-")
            and int(r.get("parent_profile_id", "0").split("-")[-1]) >= 20
        }

        with open(VIDEO_CATALOG, "r", encoding="utf-8") as f:
            vcat = json.load(f)
        cls.video_titles = [v["title"] for v in vcat.get("videos", [])]

    def test_11_live_edge_http_200_status(self):
        """Asserts live Firebase Edge returns HTTP 200 OK."""
        self.assertIsNone(self.fetch_error, f"Network request to live edge failed: {self.fetch_error}")
        self.assertEqual(
            self.live_response_code,
            200,
            f"Live Edge did not return HTTP 200: {self.live_response_code}"
        )

    def test_12_live_edge_payload_size_greater_than_500kb(self):
        """Asserts live payload size exceeds 500KB (> 500,000 bytes)."""
        self.assertIsNotNone(self.live_payload_bytes)
        size = len(self.live_payload_bytes)
        self.assertGreater(
            size,
            500000,
            f"Live edge payload size suspiciously small: {size} bytes (< 500,000)"
        )

    def test_13_live_edge_dom_row_count_matches_local_build_279_rows(self):
        """Parses live DOM table and asserts exactly 279 table rows."""
        soup = BeautifulSoup(self.live_html, "html.parser")
        tbody = soup.find("tbody", id="ledger-tbody")
        self.assertIsNotNone(tbody, "Missing <tbody id='ledger-tbody'> in live HTML")

        tr_elements = tbody.find_all("tr")
        self.assertEqual(
            len(tr_elements),
            279,
            f"Live DOM table row count mismatch: expected 279, got {len(tr_elements)}"
        )

    def test_14_live_edge_badges_and_headers_match_279(self):
        """Asserts visible-count and total-count badges in live HTML equal 279."""
        soup = BeautifulSoup(self.live_html, "html.parser")
        vis_count = soup.find("span", id="visible-count")
        tot_count = soup.find("span", id="total-count")

        self.assertIsNotNone(vis_count, "Missing #visible-count badge in live HTML")
        self.assertIsNotNone(tot_count, "Missing #total-count badge in live HTML")
        self.assertEqual(vis_count.text.strip(), "279", f"#visible-count text is {vis_count.text}")
        self.assertEqual(tot_count.text.strip(), "279", f"#total-count text is {tot_count.text}")

    def test_15_live_edge_contains_ingested_video_assets(self):
        """Asserts video assets from video_stack_50_catalog.json are present in live Edge DOM."""
        for title in [self.video_titles[0], self.video_titles[24], self.video_titles[49]]:
            escaped = html.escape(title, quote=True)
            self.assertIn(escaped, self.live_html, f"Missing video title in live DOM: {title}")

    def test_16_live_edge_tier3_rows_zero_domain_leaks_and_exclusive_youtube(self):
        """Asserts all 31 Tier 3 video assets are present in live Edge DOM and leak 0 domain references."""
        soup = BeautifulSoup(self.live_html, "html.parser")
        rows = soup.find_all("tr", class_=re.compile("hover:bg-white"))
        live_t3_rows = []
        for tr in rows:
            for u in self.tier3_urls:
                if u in str(tr):
                    live_t3_rows.append(tr)
                    break

        self.assertEqual(
            len(live_t3_rows),
            31,
            f"Expected 31 Tier 3 rows in live Edge DOM, found {len(live_t3_rows)}"
        )

        for tr in live_t3_rows:
            tr_str = str(tr).lower()
            self.assertNotIn(
                "adicommunications.co.uk",
                tr_str,
                f"Live Edge Tier 3 row leaked domain: {tr}"
            )

    def test_17_live_edge_zero_raw_root_leaks(self):
        """Asserts live Edge served page contains zero raw root anchor leaks."""
        soup = BeautifulSoup(self.live_html, "html.parser")
        leaks = []
        for a in soup.find_all("a"):
            href = a.get("href", "")
            if "adicommunications.co.uk" in href.lower():
                parsed = urllib.parse.urlparse(href)
                path = parsed.path.rstrip("/")
                if path in ("", "/index.html", "/index.htm", "/index.php"):
                    leaks.append(href)
        self.assertEqual(leaks, [], f"Raw root leaks found on live edge: {leaks}")


class TestLedgerParityAndIntegrityAdversarial(unittest.TestCase):
    """
    Class 4: 4-Way Parity, Schema Strictness, Checkatrade Ban & Telephone Telemetry.
    """

    @classmethod
    def setUpClass(cls):
        with open(DOC3_FILE, "r", encoding="utf-8") as f:
            cls.doc3_rows = list(csv.DictReader(f))

        with open(CSV_FILE, "r", encoding="utf-8") as f:
            cls.csv_rows = list(csv.DictReader(f))

        with open(JSON_FILE, "r", encoding="utf-8") as f:
            cls.json_data = json.load(f)

        with open(HTML_FILE, "r", encoding="utf-8") as f:
            cls.html_content = f.read()

        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            cls.schema_spec = json.load(f)

        cls.soup = BeautifulSoup(cls.html_content, "html.parser")

    def test_18_4way_mathematical_parity_across_all_artifacts_is_279(self):
        """Asserts doc3 == master_csv == master_json == html_table == 279."""
        doc3_count = len(self.doc3_rows)
        csv_count = len(self.csv_rows)
        json_count = len(self.json_data.get("entries", []))
        json_meta_count = self.json_data.get("total_backlinks")

        tbody = self.soup.find("tbody", id="ledger-tbody")
        html_count = len(tbody.find_all("tr")) if tbody else 0

        self.assertEqual(doc3_count, 279, f"doc3 count is {doc3_count}, expected 279")
        self.assertEqual(csv_count, 279, f"csv count is {csv_count}, expected 279")
        self.assertEqual(json_count, 279, f"json count is {json_count}, expected 279")
        self.assertEqual(json_meta_count, 279, f"json total_backlinks is {json_meta_count}, expected 279")
        self.assertEqual(html_count, 279, f"html row count is {html_count}, expected 279")

    def test_19_json_schema_draft_2020_12_strict_compliance(self):
        """Asserts public_backlink_master_ledger.json validates against schema with 0 errors."""
        validator = Draft202012Validator(self.schema_spec)
        errors = list(validator.iter_errors(self.json_data))
        self.assertEqual(errors, [], f"Schema validation errors: {[e.message for e in errors]}")

    def test_20_checkatrade_ban_zero_occurrences_repository_wide(self):
        """Asserts zero occurrences of 'checkatrade' across all 4 ledger artifacts."""
        self.assertNotIn("checkatrade", self.html_content.lower(), "Found 'checkatrade' in HTML")
        self.assertNotIn("checkatrade", json.dumps(self.json_data).lower(), "Found 'checkatrade' in JSON")

        with open(CSV_FILE, "r", encoding="utf-8") as f:
            csv_raw = f.read()
        self.assertNotIn("checkatrade", csv_raw.lower(), "Found 'checkatrade' in CSV")

        with open(DOC3_FILE, "r", encoding="utf-8") as f:
            doc3_raw = f.read()
        self.assertNotIn("checkatrade", doc3_raw.lower(), "Found 'checkatrade' in doc3")

    def test_21_direct_telephone_telemetry_standardization(self):
        """Asserts direct telephone 07860 244 274 is present and zero 0800 numbers appear."""
        self.assertIn("07860 244 274", self.html_content)
        self.assertNotIn("0800", self.html_content)


if __name__ == "__main__":
    unittest.main()
