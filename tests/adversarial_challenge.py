"""
tests/adversarial_challenge.py
Comprehensive Empirical Adversarial Stress Test Suite for Milestone 1:
- 5-layer integrity firewall stress tests
- Mathematical parity between master_cloud_signup_tracker.json and doc2_cloud_stack_100.csv
- 11-type failure taxonomy validation on edge-cases
- Tracker status and violation forensics
"""

import sys
import json
import csv
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from automated_platform_onboarder import (
    IntegrityFirewall,
    FailureReason,
    AutomatedPlatformOnboarder,
    TRACKER_JSON,
    DOC2_CSV,
)


def test_firewall_stress_cases():
    print("\n=======================================================")
    print("1. STRESS TESTING 5-LAYER INTEGRITY FIREWALL")
    print("=======================================================")

    results = []

    # 1.1 Facade & Synthetic Domains (*.adi-telecoms.org)
    synthetic_test_cases = [
        ("https://adi-telecoms.org/", False, "root synthetic domain"),
        ("https://sub.adi-telecoms.org/page", False, "subdomain synthetic"),
        ("https://evil-adi-telecoms.org/", False, "hyphenated suffix match"),
        ("https://sub.adi-telecoms.org:443/test", False, "port-suffixed synthetic"),
        ("https://sub.adi-telecoms.org./test", False, "FQDN trailing dot synthetic"),
        ("https://adi-telecoms.org:8080/path", False, "custom port synthetic"),
        ("http://adi-telecoms.org", False, "http synthetic"),
    ]

    print("\n--- 1.1 Synthetic Domain Testing ---")
    for url, should_pass, label in synthetic_test_cases:
        passed, msg = IntegrityFirewall.validate_layer2_domain(url)
        all_passed, layer, reason = IntegrityFirewall.run_all_layers(url, probe_live=False)
        matched = (passed == should_pass)
        print(f"[{'PASS' if matched else 'FAIL'}] {label}: '{url}' -> Layer2={passed} ({msg}) | AllLayers={all_passed} (Layer {layer}: {reason})")
        results.append({
            "test": f"Synthetic domain: {label}",
            "url": url,
            "layer": 2,
            "expected_pass": should_pass,
            "actual_pass": passed,
            "all_layers_pass": all_passed,
            "passed": matched
        })

    # 1.2 Private Dashboard URLs
    dashboard_test_cases = [
        ("https://app.netlify.com/start", False, "app.netlify.com/start"),
        ("https://fly.io/app/sign-in", False, "fly.io/app/sign-in"),
        ("https://dashboard.render.com/", False, "dashboard.render.com"),
        ("https://console.cloud.google.com/run", False, "console.cloud.google.com"),
        ("https://replit.com/~", False, "replit home ~"),
        ("https://replit.com/~/cli", False, "replit /~/cli"),
        ("https://supabase.com/dashboard/organizations", False, "supabase dashboard"),
        ("https://myplatform.com/app", False, "/app path without trailing slash"),
        ("https://myplatform.com/app/", False, "/app/ path"),
        ("https://myplatform.com/settings/billing", False, "/settings/ path"),
        ("https://myplatform.com/account", False, "/account path"),
        ("https://myplatform.com/admin", False, "/admin path"),
        ("https://myplatform.com/signin", False, "/signin (no hyphen)"),
        ("https://myplatform.com/portal", False, "/portal path"),
        ("https://adi-cctv-security-hub.netlify.app/", True, "clean public netlify site"),
        ("https://adi-communications.onrender.com/", True, "clean public render site"),
    ]

    print("\n--- 1.2 Private Dashboard URL Testing ---")
    for url, should_pass, label in dashboard_test_cases:
        passed, msg = IntegrityFirewall.validate_layer3_anti_dashboard(url)
        all_passed, layer, reason = IntegrityFirewall.run_all_layers(url, probe_live=False)
        matched = (passed == should_pass)
        print(f"[{'PASS' if matched else 'FAIL'}] {label}: '{url}' -> Layer3={passed} ({msg}) | AllLayers={all_passed} (Layer {layer}: {reason})")
        results.append({
            "test": f"Dashboard URL: {label}",
            "url": url,
            "layer": 3,
            "expected_pass": should_pass,
            "actual_pass": passed,
            "all_layers_pass": all_passed,
            "passed": matched
        })

    # 1.3 Raw Root Links & Rule 45 Compliance
    rule45_test_cases = [
        ("https://adicommunications.co.uk/", False, "raw root https with slash"),
        ("https://adicommunications.co.uk", False, "raw root https without slash"),
        ("http://adicommunications.co.uk/", False, "raw root http with slash"),
        ("http://adicommunications.co.uk", False, "raw root http without slash"),
        ("https://www.adicommunications.co.uk/", False, "raw root www https with slash"),
        ("https://www.adicommunications.co.uk", False, "raw root www https without slash"),
        ("https://adicommunications.co.uk/?utm_source=test", False, "raw root with query params"),
        ("https://adicommunications.co.uk/#overview", False, "raw root with hash anchor"),
        ("https://adicommunications.co.uk/news/cctv-guide", True, "editorial buffer subpage"),
        ("https://adicommunications.co.uk/services/cctv", True, "service buffer subpage"),
        ("https://tvandhomesecurity.blogspot.com/", True, "Google Blogger Shield Hub"),
        ("https://gary-pearce-forensic-hub.web.app/", True, "Google Firebase Citadel Hub"),
        ("Visit us at https://adicommunications.co.uk/ for details", False, "text containing raw root"),
        ("Check <a href=\"https://adicommunications.co.uk/\">ADI</a>", False, "HTML anchor containing raw root"),
    ]

    print("\n--- 1.3 Rule 45 Raw Root Testing ---")
    for url, should_pass, label in rule45_test_cases:
        passed, msg = IntegrityFirewall.validate_layer5_rule_45(url)
        all_passed, layer, reason = IntegrityFirewall.run_all_layers(url, probe_live=False)
        matched = (passed == should_pass)
        print(f"[{'PASS' if matched else 'FAIL'}] {label}: '{url}' -> Layer5={passed} ({msg}) | AllLayers={all_passed} (Layer {layer}: {reason})")
        results.append({
            "test": f"Rule 45: {label}",
            "url": url,
            "layer": 5,
            "expected_pass": should_pass,
            "actual_pass": passed,
            "all_layers_pass": all_passed,
            "passed": matched
        })

    # 1.4 Syntax & Well-Formedness (Layer 1)
    syntax_test_cases = [
        ("https://example.com/", False, "dummy example.com"),
        ("https://d1abcdefg.cloudfront.net/", False, "dummy hash d1abcdefg"),
        ("https://valid-platform.com/user/gary", True, "well formed public URL"),
        ("https://onedrive.live.com/ (Local Vault: C:/data)", False, "parenthetical local path"),
        ("https://test.com/path", False, "dummy test.com"),
        ("ftp://invalid-scheme.com/file", False, "ftp scheme"),
        ("https://", False, "missing netloc"),
        ("not a url at all", False, "raw non-url string"),
        ("", False, "empty string"),
        (None, False, "NoneType"),
        ("https://has space.com/path", False, "space in URL"),
    ]

    print("\n--- 1.4 Syntax & Well-Formedness (Layer 1) ---")
    for url, should_pass, label in syntax_test_cases:
        passed, msg = IntegrityFirewall.validate_layer1_syntax(url)
        matched = (passed == should_pass)
        print(f"[{'PASS' if matched else 'FAIL'}] {label}: '{url}' -> Layer1={passed} ({msg})")
        results.append({
            "test": f"Syntax Layer 1: {label}",
            "url": str(url),
            "layer": 1,
            "expected_pass": should_pass,
            "actual_pass": passed,
            "all_layers_pass": passed,
            "passed": matched
        })

    return results


def test_tracker_and_csv_parity():
    print("\n=======================================================")
    print("2. MATHEMATICAL PARITY & INTEGRITY TESTS")
    print("=======================================================")

    with open(TRACKER_JSON, "r", encoding="utf-8") as f:
        tracker_data = json.load(f)

    with open(DOC2_CSV, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        csv_rows = list(reader)

    platforms = tracker_data.get("platforms", [])
    total_json = len(platforms)
    total_csv = len(csv_rows)

    print(f"JSON Total Platforms: {total_json}")
    print(f"CSV Total Rows:      {total_csv}")

    joined_json = [p for p in platforms if p.get("status") == "JOINED"]
    pending_json = [p for p in platforms if p.get("status") == "PENDING"]

    joined_csv = [r for r in csv_rows if r.get("Status") == "JOINED"]
    pending_csv = [r for r in csv_rows if r.get("Status") == "PENDING"]

    print(f"JSON Status: JOINED={len(joined_json)}, PENDING={len(pending_json)}")
    print(f"CSV Status:  JOINED={len(joined_csv)}, PENDING={len(pending_csv)}")

    # Check tracker metadata fields
    declared_joined = tracker_data.get("joined_count")
    declared_total = tracker_data.get("total_platforms")
    print(f"Tracker metadata: joined_count={declared_joined}, total_platforms={declared_total}")

    parity_errors = []

    # Check 1: Count match
    if total_json != total_csv:
        parity_errors.append(f"Row count mismatch: JSON {total_json} vs CSV {total_csv}")

    if declared_joined != len(joined_json):
        parity_errors.append(f"JSON metadata joined_count ({declared_joined}) != actual JOINED count ({len(joined_json)})")

    if declared_total != total_json:
        parity_errors.append(f"JSON metadata total_platforms ({declared_total}) != actual platform count ({total_json})")

    # Check 2: 1-to-1 match by rank
    csv_by_rank = {r.get("Rank", "").strip(): r for r in csv_rows}
    json_by_rank = {str(p.get("rank", "")).strip(): p for p in platforms}

    for rank, p in json_by_rank.items():
        if rank not in csv_by_rank:
            parity_errors.append(f"Rank {rank} in JSON but not in CSV")
            continue
        c = csv_by_rank[rank]

        # Compare Platform Name
        if p.get("name", "").strip().lower() != c.get("Platform Name", "").strip().lower():
            parity_errors.append(f"Rank {rank} Name mismatch: JSON '{p.get('name')}' vs CSV '{c.get('Platform Name')}'")

        # Compare Status
        if p.get("status", "").strip() != c.get("Status", "").strip():
            parity_errors.append(f"Rank {rank} Status mismatch: JSON '{p.get('status')}' vs CSV '{c.get('Status')}'")

        # Compare Active Tenant URL
        p_tenant = (p.get("active_tenant_url") or "").strip()
        c_tenant = (c.get("Active Tenant URL") or "").strip()
        if p_tenant != c_tenant:
            parity_errors.append(f"Rank {rank} Tenant URL mismatch: JSON '{p_tenant}' vs CSV '{c_tenant}'")

    print(f"\nParity Discrepancies Count: {len(parity_errors)}")
    for err in parity_errors[:10]:
        print(f"   ! PARITY ERROR: {err}")

    # Check duplicates in JSON
    names_json = [p.get("name") for p in platforms]
    dupe_names = {n for n in names_json if names_json.count(n) > 1}
    print(f"Duplicate Platform Names in JSON: {dupe_names if dupe_names else 'None'}")

    ranks_json = [p.get("rank") for p in platforms]
    dupe_ranks = {r for r in ranks_json if ranks_json.count(r) > 1}
    print(f"Duplicate Ranks in JSON: {dupe_ranks if dupe_ranks else 'None'}")

    # Inspect current Firewall Violations in Tracker
    print("\n--- Inspecting Firewall Violations in Tracker's 56 JOINED Platforms ---")
    violations = []
    for p in joined_json:
        url = p.get("active_tenant_url", "")
        passed, layer, reason = IntegrityFirewall.run_all_layers(url, platform_name=p.get("name", ""), probe_live=False)
        if not passed:
            violations.append({
                "rank": p.get("rank"),
                "name": p.get("name"),
                "url": url,
                "layer": layer,
                "reason": reason
            })

    print(f"Total Violations in JOINED Platforms: {len(violations)} of {len(joined_json)}")
    for v in violations:
        print(f"   * Rank {v['rank']}: {v['name']} | Layer {v['layer']} violation: {v['reason']} | URL: {v['url']}")

    return {
        "total_json": total_json,
        "total_csv": total_csv,
        "joined_count": len(joined_json),
        "pending_count": len(pending_json),
        "parity_errors": parity_errors,
        "violations": violations
    }


def test_failure_taxonomy_edge_cases():
    print("\n=======================================================")
    print("3. FAILURE TAXONOMY EDGE-CASE EVALUATION")
    print("=======================================================")

    onboarder = AutomatedPlatformOnboarder()

    test_scenarios = [
        # Policy ban
        {"name": "Facebook Pages", "signup_url": "https://facebook.com/pages/create", "sso_method": "Email", "expected_reason": FailureReason.BANNED_POLICY},
        {"name": "LinkedIn Company", "signup_url": "https://www.linkedin.com/company/setup", "sso_method": "OAuth", "expected_reason": FailureReason.BANNED_POLICY},
        # Manual billing
        {"name": "AWS Cloud", "signup_url": "https://aws.amazon.com/free/", "sso_method": "Email", "expected_reason": FailureReason.MANUAL_BILLING_REQUIRED},
        {"name": "Microsoft Azure", "signup_url": "https://azure.microsoft.com/free/", "sso_method": "Microsoft SSO", "expected_reason": FailureReason.MANUAL_BILLING_REQUIRED},
        {"name": "DigitalOcean Droplets", "signup_url": "https://cloud.digitalocean.com/registrations/new", "sso_method": "GitHub SSO", "expected_reason": FailureReason.MANUAL_BILLING_REQUIRED},
        {"name": "Oracle Cloud Infrastructure", "signup_url": "https://www.oracle.com/cloud/free/", "sso_method": "Email", "expected_reason": FailureReason.MANUAL_BILLING_REQUIRED},
        # CLI only
        {"name": "Flyctl Bare", "signup_url": "https://fly.io/", "sso_method": "CLI Token Exchange", "expected_reason": FailureReason.CLI_AUTH_REQUIRED},
        {"name": "Wrangler Terminal", "signup_url": "https://workers.cloudflare.com/", "sso_method": "CLI", "expected_reason": FailureReason.CLI_AUTH_REQUIRED},
        # Dry run queued
        {"name": "Standard Cloud Web", "signup_url": "https://example-cloud.io/signup", "sso_method": "GitHub OAuth", "expected_reason": FailureReason.WAITLIST_PENDING},
    ]

    taxonomy_results = []
    for sc in test_scenarios:
        res = onboarder.process_candidate(sc, dry_run=True)
        reason = res.get("failure_reason")
        matched = (reason == sc["expected_reason"])
        print(f"[{'PASS' if matched else 'FAIL'}] Platform: {sc['name']:30} -> Classified: {reason:25} (Expected: {sc['expected_reason']})")
        taxonomy_results.append({
            "platform": sc["name"],
            "expected": sc["expected_reason"],
            "actual": reason,
            "passed": matched
        })

    # Test all 11 failure reasons exist and are documented
    print("\n--- Verifying All 11 Canonical Failure Reasons in Taxonomy ---")
    all_codes = sorted(list(FailureReason.ALL_REASONS.keys()))
    print(f"Total Canonical Failure Codes: {len(all_codes)}")
    assert len(all_codes) == 11, f"Expected 11 codes, got {len(all_codes)}"
    for code in all_codes:
        print(f"  - {code:25}: {FailureReason.ALL_REASONS[code]}")

    return taxonomy_results


if __name__ == "__main__":
    fw_results = test_firewall_stress_cases()
    parity_results = test_tracker_and_csv_parity()
    tax_results = test_failure_taxonomy_edge_cases()

    fw_fails = [r for r in fw_results if not r["passed"]]
    for idx, f in enumerate(fw_fails, 1):
        print(f"[{idx}] {f['test']}")
        print(f"    URL:      {f['url']}")
        print(f"    Expected: {f['expected_pass']}")
        print(f"    Actual:   {f['actual_pass']}")
        print(f"    AllLayers:{f['all_layers_pass']}")

