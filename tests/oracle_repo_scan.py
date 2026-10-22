"""
tests/oracle_repo_scan.py
Adversarial scan of all files across the repository for Rule 45 compliance.
"""

from pathlib import Path
import re
from urllib.parse import urlparse

REPO_ROOT = Path(r"C:\Users\Gary\github-cctv-seo")
URL_FINDER = re.compile(r"https?://[^\s\"\'\<\>\,\)\;\]\}]+", re.IGNORECASE)

EXCLUDED_DIRS = {".git", ".agents", "__pycache__"}
TEST_FILES_TO_SKIP = {
    "adversarial_challenge.py",
    "test_rule45_adversarial_battery.py",
    "test_challenger_m1_iter2_2.py",
    "test_challenger_m2_empirical.py",
    "test_challenger_m2_delimiter_edge_cases.py",
    "oracle_repo_scan.py",
    "test_tier1_features.py",
    "test_tier2_boundaries.py",
    "test_tier4_real_world.py",
}

BINARY_EXTS = {
    ".png", ".jpg", ".jpeg", ".webp", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot", ".mp3", ".mp4", ".zip", ".tar", ".gz"
}

def scan():
    all_files = [
        f for f in REPO_ROOT.rglob("*")
        if f.is_file()
        and not any(d in f.parts for d in EXCLUDED_DIRS)
        and f.suffix.lower() not in BINARY_EXTS
        and f.name not in TEST_FILES_TO_SKIP
    ]

    print(f"Total non-binary repo files identified: {len(all_files)}")

    json_csv_files = [f for f in all_files if f.suffix.lower() in (".json", ".csv")]
    print(f"Total JSON/CSV files: {len(json_csv_files)}")

    # 1. Scan JSON/CSV files specifically
    json_csv_violations = []
    for f in json_csv_files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"Error reading {f}: {e}")
            continue

        for line_no, line in enumerate(content.splitlines(), 1):
            if "adicommunications.co.uk" in line.lower():
                urls = URL_FINDER.findall(line)
                for raw_url in urls:
                    clean_url = raw_url.rstrip("\"\'.,;>)]}")
                    try:
                        p = urlparse(clean_url)
                    except Exception:
                        continue
                    host = (p.hostname or "").lower()
                    if host in ("adicommunications.co.uk", "www.adicommunications.co.uk"):
                        path = p.path or "/"
                        if not any(path.startswith(prefix) for prefix in ("/news", "/assets", "/feed")):
                            json_csv_violations.append({
                                "file": str(f.relative_to(REPO_ROOT)),
                                "line": line_no,
                                "url": clean_url,
                                "snippet": line.strip()[:100]
                            })

    print(f"\n--- JSON and CSV Results (63 files) ---")
    print(f"Raw root / non-buffer violations in JSON/CSV: {len(json_csv_violations)}")
    for v in json_csv_violations:
        print(f"  VIOLATION: {v['file']}:{v['line']} -> {v['url']}")

    # 2. Scan ALL files (HTML, JS, PY, MD, YAML, etc.)
    all_repo_raw_root_violations = []
    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for line_no, line in enumerate(content.splitlines(), 1):
            if "adicommunications.co.uk" in line.lower():
                urls = URL_FINDER.findall(line)
                for raw_url in urls:
                    clean_url = raw_url.rstrip("\"\'.,;>)]}")
                    try:
                        p = urlparse(clean_url)
                    except Exception:
                        continue
                    host = (p.hostname or "").lower()
                    if host in ("adicommunications.co.uk", "www.adicommunications.co.uk"):
                        path = p.path or "/"
                        # Raw root check:
                        if path in ("/", "") or path.endswith(("/index.html", "/index.htm", "/index.php")):
                            all_repo_raw_root_violations.append({
                                "file": str(f.relative_to(REPO_ROOT)),
                                "line": line_no,
                                "url": clean_url,
                                "snippet": line.strip()[:100]
                            })

    print(f"\n--- All Repository Files Raw Root Scan ---")
    print(f"Total files scanned: {len(all_files)}")
    print(f"Raw root URL violations across entire repo: {len(all_repo_raw_root_violations)}")
    for v in all_repo_raw_root_violations:
        print(f"  ALL-REPO VIOLATION: {v['file']}:{v['line']} -> {v['url']}")

if __name__ == "__main__":
    scan()
