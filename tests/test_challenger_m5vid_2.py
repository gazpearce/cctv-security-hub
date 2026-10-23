#!/usr/bin/env python3
"""
tests/test_challenger_m5vid_2.py
================================
Adversarial Challenger Test Suite: Milestone M5-VID
Live Edge Deployment & Rule 45 Evasion Final Challenger

Author: challenger_m5vid_2
Role: Empirical Challenger (critic, specialist)
Verification Targets:
  1. Multi-Pass Rule 45 Evasion Probe: Exhaustive scan across all 2,500 syndication descriptions,
     all per-platform syndication manifests, 279 ledger entries, HTML ledgers, and repository markdown files.
     Assert 0 raw root links to adicommunications.co.uk.
  2. Tier 3 Air-Gap Probe: Scan all 31 Tier 3 video platforms across all outputs (1,550 syndication tasks
     and 62 individual manifest directories). Assert 0 occurrences of 'adicommunications.co.uk' and 100% exclusive
     linking to YouTube Apex (https://www.youtube.com/@CCTV.services).
  3. Live Edge HTTP Verification: Automated request to
     https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html.
     Assert HTTP 200, Content-Length > 500KB, valid doctype, exactly 279 matching rows,
     Gary Pearce contact (07860 244 274), Rule 45 Google Shield Air-Gap assertion, and zero Checkatrade mentions.
  4. Video Stack Trade E-E-A-T & Chapter Clamping: Full audit of all 2,500 syndication payloads.
  5. 5-Way Mathematical Parity across doc3, CSV, JSON, local HTML, and live Edge HTML.
"""

import csv
import glob
import json
import os
import re
import posixpath
import urllib.parse
import urllib.request
import unittest
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
SYNDICATION_MANIFEST = REPO_ROOT / "video_stack_50_syndication_manifest.json"
SYNDICATION_DIR = REPO_ROOT / "syndication"
MASTER_TIERS_FILE = REPO_ROOT / "video_stack_master_tiers.json"

LIVE_EDGE_URL = "https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html"
YOUTUBE_APEX = "https://www.youtube.com/@CCTV.services"
GARY_PHONE = "07860 244 274"

ROOT_LINK_REGEX = re.compile(
    r"(?:https?:)?//(?:www\.)?adicommunications\.co\.uk\.?(?::\d+)?(?:/([^\s\"\'<>)]*)|(?=$|[?#\"'\s<>,;)\]}]))",
    re.IGNORECASE
)

BANNED_BUZZWORDS = [
    "cutting-edge",
    "revolutionary",
    "game-changer",
    "world-class",
    "seamlessly",
    "unparalleled",
    "next-level",
    "elevate",
    "atlantic storm-tested",
    "zero throttling",
    "gigabit speeds",
]

PLATFORM_DIR_OVERRIDES = {
    "PLAT-VID-001": "youtube",
    "PLAT-VID-002": "dailymotion",
    "PLAT-VID-003": "vimeo",
    "PLAT-VID-004": "archive_org",
    "PLAT-VID-005": "wistia",
    "PLAT-VID-020": "rumble",
    "PLAT-VID-021": "odysee",
    "PLAT-VID-022": "peertube",
    "PLAT-VID-023": "bitchute",
    "PLAT-VID-024": "dtube",
}


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def check_raw_root_violation(text: str):
    """
    Returns list of matching violations if raw root link to adicommunications.co.uk is detected.
    """
    violations = []
    unquoted = urllib.parse.unquote(text)
    for m in ROOT_LINK_REGEX.finditer(unquoted):
        path = m.group(1) or ""
        clean_path = re.split(r"[?#]", path)[0]
        norm = posixpath.normpath("/" + clean_path.lstrip("/")).rstrip("/")
        if norm == "" or norm in ("/index.html", "/index.htm", "/index.php"):
            violations.append(m.group(0))
    return violations


class TestMultiPassRule45EvasionProbe(unittest.TestCase):
    """
    Test Class 1: Multi-Pass Rule 45 Evasion Probe.
    Scans all 2,500 syndication descriptions, 279 ledger entries, HTML files, and markdown docs.
    """

    @classmethod
    def setUpClass(cls):
        cls.assertTrue(SYNDICATION_MANIFEST.exists(), f"Missing {SYNDICATION_MANIFEST}")
        with open(SYNDICATION_MANIFEST, "r", encoding="utf-8") as f:
            cls.syndication_data = json.load(f)
        cls.syndication_queue = cls.syndication_data.get("syndication_queue", [])

        with open(JSON_FILE, "r", encoding="utf-8") as f:
            cls.ledger_json = json.load(f)

        with open(CSV_FILE, "r", encoding="utf-8") as f:
            cls.ledger_csv = list(csv.DictReader(f))

        with open(DOC3_FILE, "r", encoding="utf-8") as f:
            cls.doc3_rows = list(csv.DictReader(f))

        with open(HTML_FILE, "r", encoding="utf-8") as f:
            cls.html_content = f.read()

    def test_01_syndication_manifest_2500_descriptions_zero_raw_root_links(self):
        """Scan all 2,500 descriptions in video_stack_50_syndication_manifest.json for raw root links."""
        self.assertEqual(len(self.syndication_queue), 2500, "Expected exactly 2,500 syndication queue items")
        violations = []
        for task in self.syndication_queue:
            task_id = task.get("task_id", "")
            desc = task.get("description", "")
            target_url = task.get("target_url", "")
            buffer_url = task.get("buffer_url", "")

            v_desc = check_raw_root_violation(desc)
            if v_desc:
                violations.append((task_id, "description", v_desc))

            for u in (target_url, buffer_url):
                if u:
                    v_u = check_raw_root_violation(u)
                    if v_u:
                        violations.append((task_id, "url", v_u))

        self.assertEqual(len(violations), 0, f"Found {len(violations)} raw root link violations in syndication queue: {violations[:5]}")

    def test_02_per_platform_syndication_files_zero_raw_root_links(self):
        """Scan all individual platform JSON and CSV manifests in syndication/ directory."""
        self.assertTrue(SYNDICATION_DIR.exists(), f"Missing {SYNDICATION_DIR}")
        violations = []
        file_count = 0
        for root, dirs, files in os.walk(SYNDICATION_DIR):
            for fname in files:
                if fname.endswith((".json", ".csv")):
                    file_count += 1
                    fpath = Path(root) / fname
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        v = check_raw_root_violation(content)
                        if v:
                            violations.append((str(fpath), v))

        self.assertGreater(file_count, 50, f"Expected > 50 syndication platform files, found {file_count}")
        self.assertEqual(len(violations), 0, f"Found raw root link violations in syndication directory files: {violations[:5]}")

    def test_03_master_ledger_json_279_entries_zero_raw_root_links(self):
        """Scan all 279 entries in public_backlink_master_ledger.json for raw root links."""
        entries = self.ledger_json.get("entries", [])
        self.assertEqual(len(entries), 279, f"Expected 279 entries, found {len(entries)}")
        violations = []
        for idx, entry in enumerate(entries):
            for key, val in entry.items():
                if isinstance(val, str):
                    v = check_raw_root_violation(val)
                    if v:
                        violations.append((idx, key, v))

        self.assertEqual(len(violations), 0, f"Found raw root link violations in master JSON ledger: {violations[:5]}")

    def test_04_master_ledger_csv_279_entries_zero_raw_root_links(self):
        """Scan all 279 entries in public_backlink_master_ledger.csv for raw root links."""
        self.assertEqual(len(self.ledger_csv), 279, f"Expected 279 rows in CSV, found {len(self.ledger_csv)}")
        violations = []
        for row_idx, row in enumerate(self.ledger_csv):
            for col_name, val in row.items():
                v = check_raw_root_violation(val)
                if v:
                    violations.append((row_idx, col_name, v))

        self.assertEqual(len(violations), 0, f"Found raw root link violations in master CSV ledger: {violations[:5]}")

    def test_05_doc3_published_asset_links_zero_raw_root_links(self):
        """Scan all entries in doc3_published_asset_links.csv for raw root links."""
        self.assertEqual(len(self.doc3_rows), 279, f"Expected 279 rows in doc3, found {len(self.doc3_rows)}")
        violations = []
        for row_idx, row in enumerate(self.doc3_rows):
            for col_name, val in row.items():
                v = check_raw_root_violation(val)
                if v:
                    violations.append((row_idx, col_name, v))

        self.assertEqual(len(violations), 0, f"Found raw root link violations in doc3 CSV: {violations[:5]}")

    def test_06_html_ledger_zero_raw_root_links(self):
        """Scan public_backlink_ledger.html for raw root links."""
        violations = check_raw_root_violation(self.html_content)
        self.assertEqual(len(violations), 0, f"Found raw root link violations in public_backlink_ledger.html: {violations[:5]}")

    def test_07_markdown_docs_zero_raw_root_links(self):
        """Scan root and docs markdown files for raw root links."""
        violations = []
        md_count = 0
        for p in REPO_ROOT.glob("*.md"):
            md_count += 1
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                v = check_raw_root_violation(content)
                if v:
                    violations.append((p.name, v))

        self.assertGreater(md_count, 0, "Expected at least 1 markdown file in root")
        self.assertEqual(len(violations), 0, f"Found raw root link violations in markdown files: {violations[:5]}")


class TestTier3VideoAirGapProbe(unittest.TestCase):
    """
    Test Class 2: Tier 3 Video Air-Gap Probe.
    Validates complete website isolation for all 31 Tier 3 video platforms:
    0 occurrences of adicommunications.co.uk and 100% exclusive linking to YouTube Apex.
    """

    @classmethod
    def setUpClass(cls):
        with open(PLATFORM_CATALOG, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        video_platforms = catalog.get("category_stacks", {}).get("video", {}).get("platforms", [])
        cls.tier3_platforms = [p for p in video_platforms if "Tier 3" in p.get("tier", "")]

        with open(SYNDICATION_MANIFEST, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        cls.queue = manifest.get("syndication_queue", [])

    def test_01_verify_exactly_31_tier3_platforms(self):
        """Assert exactly 31 Tier 3 video platforms exist in platform catalog."""
        self.assertEqual(len(self.tier3_platforms), 31, f"Expected 31 Tier 3 platforms, found {len(self.tier3_platforms)}")

    def test_02_tier3_queue_tasks_complete_domain_isolation(self):
        """Assert all Tier 3 syndication tasks (31 platforms x 50 videos = 1,550 tasks) have 0 domain leaks."""
        tier3_tasks = [t for t in self.queue if "Tier 3" in t.get("tier", "")]
        self.assertEqual(len(tier3_tasks), 1550, f"Expected 1,550 Tier 3 tasks, found {len(tier3_tasks)}")

        leaks = []
        missing_yt = []
        invalid_outbound = []

        for task in tier3_tasks:
            task_id = task.get("task_id", "")
            plat = task.get("platform_name", "")
            desc = task.get("description", "")
            outbound = task.get("outbound_website_link", "")

            if "adicommunications.co.uk" in desc.lower():
                leaks.append((task_id, plat, "found adicommunications.co.uk in description"))

            task_str = json.dumps(task)
            if "adicommunications.co.uk" in task_str.lower():
                leaks.append((task_id, plat, "domain in task JSON"))

            if "youtube.com/@cctv.services" not in desc.lower() and "youtu.be" not in desc.lower():
                missing_yt.append((task_id, plat))

            if outbound not in ("NONE", "NONE (RULE ENFORCED: YOUTUBE ONLY)"):
                invalid_outbound.append((task_id, plat, outbound))

        self.assertEqual(len(leaks), 0, f"Domain leaks found in Tier 3 tasks: {leaks[:5]}")
        self.assertEqual(len(missing_yt), 0, f"Tier 3 tasks missing YouTube Apex link: {missing_yt[:5]}")
        self.assertEqual(len(invalid_outbound), 0, f"Tier 3 tasks with invalid outbound link: {invalid_outbound[:5]}")

    def test_03_tier3_individual_manifest_directories_zero_leaks(self):
        """Scan individual platform manifest files in syndication/ for all 31 Tier 3 platforms."""
        leaks = []
        checked_dirs = set()

        for plat in self.tier3_platforms:
            pid = plat.get("platform_id", "")
            slug = PLATFORM_DIR_OVERRIDES.get(pid, slugify(plat.get("name", "")))
            candidate_dirs = [SYNDICATION_DIR / pid, SYNDICATION_DIR / slug]
            for cdir in candidate_dirs:
                if cdir.exists():
                    checked_dirs.add(str(cdir))
                    for fpath in cdir.glob("*.*"):
                        if fpath.suffix in (".json", ".csv"):
                            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()
                                if "adicommunications.co.uk" in content.lower():
                                    leaks.append((str(fpath), plat.get("name", "")))

        self.assertGreaterEqual(len(checked_dirs), 31, f"Expected to check at least 31 Tier 3 platform dirs, checked {len(checked_dirs)}")
        self.assertEqual(len(leaks), 0, f"Found domain leaks in Tier 3 syndication directories: {leaks[:5]}")


class TestLiveEdgeFirebaseDeployment(unittest.TestCase):
    """
    Test Class 3: Live Edge HTTP Verification.
    Sends live HTTP request to https://gary-pearce-forensic-hub.web.app/public_backlink_ledger.html
    and verifies status 200, payload > 500KB, valid doctype, exactly 279 matching rows,
    Gary Pearce contact 07860 244 274, and zero Checkatrade mentions.
    """

    @classmethod
    def setUpClass(cls):
        req = urllib.request.Request(
            LIVE_EDGE_URL,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                cls.http_status = resp.status
                cls.headers = dict(resp.getheaders())
                cls.raw_bytes = resp.read()
                cls.html_text = cls.raw_bytes.decode("utf-8", errors="replace")
        except Exception as e:
            cls.http_status = -1
            cls.html_text = ""
            cls.raw_bytes = b""
            cls.fetch_error = str(e)

        with open(JSON_FILE, "r", encoding="utf-8") as f:
            cls.local_ledger = json.load(f)

    def test_01_live_http_status_200(self):
        """Assert live HTTP request returns status 200 OK."""
        self.assertEqual(self.http_status, 200, f"Live Edge HTTP status was {self.http_status}")

    def test_02_live_payload_size_greater_than_500kb(self):
        """Assert live payload is greater than 500KB (500,000 bytes)."""
        byte_len = len(self.raw_bytes)
        self.assertGreater(byte_len, 500_000, f"Live payload was {byte_len} bytes (expected > 500,000 bytes)")

    def test_03_valid_html_doctype(self):
        """Assert valid HTML doctype declaration at the beginning of live HTML."""
        stripped = self.html_text.strip()
        self.assertTrue(stripped.lower().startswith("<!doctype html"), "Live page missing valid <!DOCTYPE html>")

    def test_04_live_dom_rendered_table_rows_exactly_279(self):
        """Parse live HTML DOM and assert exactly 279 rows in tbody."""
        soup = BeautifulSoup(self.html_text, "html.parser")
        tbody = soup.find("tbody", id="ledger-tbody")
        self.assertIsNotNone(tbody, "Missing <tbody id='ledger-tbody'> in live HTML")
        rows = tbody.find_all("tr")
        self.assertEqual(len(rows), 279, f"Expected 279 live table rows, found {len(rows)}")

    def test_05_live_rows_match_local_master_ledger(self):
        """Verify live table rows match local public_backlink_master_ledger.json entries."""
        soup = BeautifulSoup(self.html_text, "html.parser")
        tbody = soup.find("tbody", id="ledger-tbody")
        rows = tbody.find_all("tr")
        local_entries = self.local_ledger.get("entries", [])
        self.assertEqual(len(rows), len(local_entries))

        mismatches = []
        for idx, (row, entry) in enumerate(zip(rows, local_entries)):
            row_text = row.get_text()
            expected_plat = entry.get("platform", "")
            expected_url = entry.get("public_live_url", entry.get("tenant_url", ""))
            if expected_plat not in row_text:
                mismatches.append((idx, f"Platform '{expected_plat}' not in row text"))
            links = [a.get("href", "") for a in row.find_all("a")]
            if expected_url and not any(expected_url in link for link in links):
                mismatches.append((idx, f"URL '{expected_url}' not found in row links: {links}"))

        self.assertEqual(len(mismatches), 0, f"Found mismatches between live HTML and local JSON: {mismatches[:5]}")

    def test_06_trade_credentials_and_phone_present(self):
        """Assert Gary Pearce and direct contact 07860 244 274 are present in live HTML."""
        self.assertIn("Gary Pearce", self.html_text, "Gary Pearce missing from live HTML")
        self.assertIn(GARY_PHONE, self.html_text, f"{GARY_PHONE} missing from live HTML")

    def test_07_rule45_shield_and_zero_checkatrade(self):
        """Assert Rule 45 Google Shield Air-Gap is documented and zero Checkatrade mentions."""
        self.assertIn("Rule 45 Google Shield Air-Gap", self.html_text, "Rule 45 Google Shield Air-Gap missing from live HTML")
        self.assertNotIn("checkatrade", self.html_text.lower(), "Rule 20 Violation: 'Checkatrade' found in live HTML")

    def test_08_zero_0800_numbers(self):
        """Assert zero 0800 telephone numbers exist in live HTML."""
        self.assertNotIn("0800", self.html_text, "Rule 20 Violation: '0800' number found in live HTML")


class TestVideoStackTradeEEATAndClamping(unittest.TestCase):
    """
    Test Class 4: Video Stack Trade E-E-A-T & Chapter Clamping.
    Scans all 2,500 syndication queue tasks for chapter timestamp validity,
    trade standards, and absence of banned marketing buzzwords.
    """

    @classmethod
    def setUpClass(cls):
        with open(SYNDICATION_MANIFEST, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        cls.queue = manifest.get("syndication_queue", [])

    def test_01_chapter_markers_valid_and_clamped(self):
        """Verify chapter markers across all 2,500 syndication tasks."""
        chapter_errors = []
        for task in self.queue:
            task_id = task.get("task_id", "")
            desc = task.get("description", "")
            dur = float(task.get("duration_sec", 45.0))

            chapters = [line.strip() for line in desc.splitlines() if re.match(r"^\d{2}:\d{2}\s*-\s*", line.strip())]
            if len(chapters) < 3:
                chapter_errors.append((task_id, f"Fewer than 3 chapters: {len(chapters)}"))
                continue

            if not chapters[0].startswith("00:00"):
                chapter_errors.append((task_id, f"Ch1 does not start with 00:00: {chapters[0]}"))

            parsed_seconds = []
            for ch in chapters:
                m = re.match(r"^(\d{2}):(\d{2})", ch)
                if m:
                    sec = int(m.group(1)) * 60 + int(m.group(2))
                    parsed_seconds.append(sec)

            for i in range(len(parsed_seconds) - 1):
                if parsed_seconds[i + 1] - parsed_seconds[i] < 10:
                    chapter_errors.append((task_id, f"Interval < 10s between ch{i+1} and ch{i+2}"))

            if parsed_seconds and parsed_seconds[-1] >= dur:
                chapter_errors.append((task_id, f"Final timestamp {parsed_seconds[-1]}s >= duration {dur}s"))

        self.assertEqual(len(chapter_errors), 0, f"Chapter clamping errors: {chapter_errors[:5]}")

    def test_02_eeat_and_zero_banned_buzzwords(self):
        """Verify trade E-E-A-T credentials and absence of banned buzzwords across all 2,500 tasks."""
        eeat_errors = []
        buzzword_errors = []

        for task in self.queue:
            task_id = task.get("task_id", "")
            desc = task.get("description", "")
            lower_desc = desc.lower()

            if "Gary Pearce" not in desc:
                eeat_errors.append((task_id, "Missing Gary Pearce"))
            if GARY_PHONE not in desc:
                eeat_errors.append((task_id, f"Missing {GARY_PHONE}"))
            if "checkatrade" in lower_desc:
                eeat_errors.append((task_id, "Found Checkatrade"))
            if "0800" in desc:
                eeat_errors.append((task_id, "Found 0800 number"))
            if "cai member" in lower_desc:
                eeat_errors.append((task_id, "Found 'CAI Member' claim"))

            for b in BANNED_BUZZWORDS:
                if b in lower_desc:
                    buzzword_errors.append((task_id, f"Banned buzzword: {b}"))

        self.assertEqual(len(eeat_errors), 0, f"E-E-A-T violations: {eeat_errors[:5]}")
        self.assertEqual(len(buzzword_errors), 0, f"Banned buzzword violations: {buzzword_errors[:5]}")


class TestLedgerParityAndDraft202012Schema(unittest.TestCase):
    """
    Test Class 5: 5-Way Mathematical Parity & Schema Validation.
    """

    def test_01_schema_compliance_draft_2020_12(self):
        """Validate public_backlink_master_ledger.json against public_backlink_ledger.schema.json."""
        self.assertTrue(SCHEMA_FILE.exists(), f"Missing schema file: {SCHEMA_FILE}")
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            schema = json.load(f)
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(data))
        self.assertEqual(len(errors), 0, f"Schema validation errors: {[e.message for e in errors[:5]]}")

    def test_02_5_way_mathematical_parity_exactly_279_records(self):
        """Assert exact 279-row parity across doc3, CSV, JSON, local HTML, and live Edge HTML."""
        with open(DOC3_FILE, "r", encoding="utf-8") as f:
            doc3_count = len(list(csv.DictReader(f)))
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            csv_count = len(list(csv.DictReader(f)))
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            json_count = len(json.load(f).get("entries", []))
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            html_count = len(soup.find("tbody", id="ledger-tbody").find_all("tr"))

        req = urllib.request.Request(LIVE_EDGE_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            live_soup = BeautifulSoup(resp.read().decode("utf-8"), "html.parser")
            live_count = len(live_soup.find("tbody", id="ledger-tbody").find_all("tr"))

        self.assertEqual(doc3_count, 279, f"doc3 rows: {doc3_count}")
        self.assertEqual(csv_count, 279, f"CSV rows: {csv_count}")
        self.assertEqual(json_count, 279, f"JSON rows: {json_count}")
        self.assertEqual(html_count, 279, f"Local HTML rows: {html_count}")
        self.assertEqual(live_count, 279, f"Live Edge rows: {live_count}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
