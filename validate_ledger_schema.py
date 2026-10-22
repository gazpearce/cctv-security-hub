"""
validate_ledger_schema.py
Validates public_backlink_master_ledger.json against JSON Schema Draft 2020-12
and checks 100% mathematical parity across doc3, CSV, JSON, and HTML.
"""

import csv
import json
import os
import re
import sys
from jsonschema import Draft202012Validator

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

def validate():
    json_path = os.path.join(REPO_ROOT, "public_backlink_master_ledger.json")
    csv_path = os.path.join(REPO_ROOT, "public_backlink_master_ledger.csv")
    doc3_path = os.path.join(REPO_ROOT, "doc3_published_asset_links.csv")
    html_path = os.path.join(REPO_ROOT, "public_backlink_ledger.html")
    schema_path = os.path.join(REPO_ROOT, "public_backlink_ledger.schema.json")

    print("[AUDIT] Validating Milestone 3 Backlink Ledger Pipeline...")

    # 1. Load JSON and Schema
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(data))
    if errors:
        print(f"[FAIL] Schema Draft 2020-12 Validation Failed with {len(errors)} error(s):")
        for err in errors[:5]:
            print(f"  - {err.message} at path: {'/'.join(str(p) for p in err.path)}")
        sys.exit(1)
    print("  [PASS] JSON Schema Draft 2020-12 compliance verified.")

    # 2. Mathematical Parity Check
    with open(doc3_path, "r", encoding="utf-8") as f:
        doc3_rows = list(csv.DictReader(f))
    with open(csv_path, "r", encoding="utf-8") as f:
        csv_rows = list(csv.DictReader(f))
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    html_rows = len(re.findall(r'<tr class="hover:bg-white', html_content))

    assert len(doc3_rows) == len(csv_rows), f"Parity mismatch: doc3 ({len(doc3_rows)}) != CSV ({len(csv_rows)})"
    assert len(csv_rows) == len(data["entries"]), f"Parity mismatch: CSV ({len(csv_rows)}) != JSON ({len(data['entries'])})"
    assert data["total_backlinks"] == len(csv_rows), f"Parity mismatch: total_backlinks ({data['total_backlinks']}) != CSV ({len(csv_rows)})"
    assert html_rows == len(csv_rows), f"Parity mismatch: HTML ({html_rows}) != CSV ({len(csv_rows)})"

    print(f"  [PASS] 100% Mathematical Parity verified across {len(doc3_rows)} assets.")

    # 3. Rule 45 Check on Ledger Targets
    for idx, e in enumerate(data["entries"], 1):
        for key in ("tenant_url", "apex_target", "shield_target_url"):
            val = e.get(key, "")
            if "adicommunications.co.uk" in val:
                assert any(sub in val for sub in ("/news/", "/assets/", "/feed/")), \
                    f"Rule 45 violation in entry {idx} key {key}: {val}"

    print("  [PASS] Rule 45 Google Shield Air-Gap compliance verified.")
    print("[SUCCESS] All Milestone 3 Backlink Ledger checks passed 100%!\n")

if __name__ == "__main__":
    validate()
