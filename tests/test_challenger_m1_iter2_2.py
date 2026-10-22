"""
tests/test_challenger_m1_iter2_2.py
Empirical Challenger Verification Harness for Milestone 1 Iteration 2:
1. Re-challenge Layer 5 Rule 45 evasion attacks (port suffixes, trailing FQDN dots, index variants, traversals, userinfo).
2. Re-challenge Layer 2 & Layer 3 evasion attacks (subdomains, ports, dots, session fragments).
3. Exhaustive audit of all 154 platforms in master_cloud_signup_tracker.json and doc2_cloud_stack_100.csv:
   - Check zero private dashboard URLs (console.*, app.*, dashboard.*, /login, /dashboard, etc.)
   - Check zero synthetic domains (*.adi-telecoms.org)
   - Check mathematical parity across all columns
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

def test_layer5_evasion_battery():
    print("=================================================================")
    print("1. EMPIRICAL LAYER 5 RULE 45 EVASION BATTERY")
    print("=================================================================")
    
    test_cases = [
        # Baseline raw roots (MUST BE REJECTED)
        ("https://adicommunications.co.uk/", False, "naked root https with slash"),
        ("https://adicommunications.co.uk", False, "naked root https no slash"),
        ("http://adicommunications.co.uk/", False, "naked root http with slash"),
        ("http://adicommunications.co.uk", False, "naked root http no slash"),
        ("https://www.adicommunications.co.uk/", False, "www naked root https with slash"),
        ("https://www.adicommunications.co.uk", False, "www naked root https no slash"),
        
        # Port suffixes (MUST BE REJECTED)
        ("https://adicommunications.co.uk:443/", False, "port 443 with slash"),
        ("https://adicommunications.co.uk:443", False, "port 443 no slash"),
        ("http://adicommunications.co.uk:80/", False, "port 80 with slash"),
        ("http://adicommunications.co.uk:80", False, "port 80 no slash"),
        ("https://adicommunications.co.uk:8443/", False, "custom port 8443 with slash"),
        ("https://adicommunications.co.uk:8443", False, "custom port 8443 no slash"),
        ("https://www.adicommunications.co.uk:443/", False, "www port 443 with slash"),
        ("https://www.adicommunications.co.uk:443", False, "www port 443 no slash"),
        
        # Trailing FQDN dots (MUST BE REJECTED)
        ("https://adicommunications.co.uk.", False, "trailing FQDN dot no slash"),
        ("https://adicommunications.co.uk./", False, "trailing FQDN dot with slash"),
        ("https://adicommunications.co.uk.:443/", False, "trailing FQDN dot + port 443 with slash"),
        ("https://adicommunications.co.uk.:443", False, "trailing FQDN dot + port 443 no slash"),
        ("https://www.adicommunications.co.uk.", False, "www trailing FQDN dot no slash"),
        ("https://www.adicommunications.co.uk./", False, "www trailing FQDN dot with slash"),
        ("https://www.adicommunications.co.uk.:443/", False, "www trailing FQDN dot + port 443 with slash"),
        ("https://www.adicommunications.co.uk.:443", False, "www trailing FQDN dot + port 443 no slash"),
        
        # Query parameters and fragments on raw root (MUST BE REJECTED)
        ("https://adicommunications.co.uk/?utm_source=ref", False, "root with query string"),
        ("https://adicommunications.co.uk:443/?utm_source=ref", False, "port 443 + query string"),
        ("https://adicommunications.co.uk./?utm_source=ref", False, "dot + query string"),
        ("https://adicommunications.co.uk/#hero", False, "root with fragment anchor"),
        ("https://adicommunications.co.uk:443/#hero", False, "port 443 + fragment anchor"),
        ("https://adicommunications.co.uk./#hero", False, "dot + fragment anchor"),
        
        # Default index filenames (MUST BE REJECTED)
        ("https://adicommunications.co.uk/index.html", False, "index.html"),
        ("https://adicommunications.co.uk:443/index.html", False, "port 443 + index.html"),
        ("https://adicommunications.co.uk./index.html", False, "dot + index.html"),
        ("https://adicommunications.co.uk/index.htm", False, "index.htm"),
        ("https://adicommunications.co.uk/index.php", False, "index.php"),
        ("https://adicommunications.co.uk:443/index.php", False, "port 443 + index.php"),
        ("https://adicommunications.co.uk./index.php", False, "dot + index.php"),
        
        # Path slash collapse (MUST BE REJECTED)
        ("https://adicommunications.co.uk//", False, "double slash root"),
        ("https://adicommunications.co.uk///", False, "triple slash root"),
        
        # Legitimate Rule 45 buffer subpages (MUST BE ACCEPTED)
        ("https://adicommunications.co.uk/news/cctv-guide", True, "editorial buffer subpage"),
        ("https://adicommunications.co.uk:443/news/cctv-guide", True, "port 443 + buffer subpage"),
        ("https://adicommunications.co.uk./news/cctv-guide", True, "dot + buffer subpage"),
        ("https://adicommunications.co.uk/services/cctv-installation", True, "services subpage"),
        ("https://adicommunications.co.uk/assets/images/diagram.webp", True, "assets subpage"),
        ("https://adicommunications.co.uk/feed.xml", True, "feed subpath"),
        ("https://tvandhomesecurity.blogspot.com/", True, "Google Shield Blogger Hub"),
        ("https://gary-pearce-forensic-hub.web.app/", True, "Google Firebase Citadel Hub"),
    ]
    
    failures = []
    for url, should_pass, label in test_cases:
        passed, msg = IntegrityFirewall.validate_layer5_rule_45(url)
        if passed != should_pass:
            failures.append((label, url, should_pass, passed, msg))
            print(f"[FAIL] {label:42} | Expected {should_pass}, Got {passed} ({msg}) | URL: {url}")
        else:
            print(f"[PASS] {label:42} | Expected {should_pass}, Got {passed} | URL: {url}")
            
    print(f"\nLayer 5 Battery Total: {len(test_cases)} | Passed: {len(test_cases) - len(failures)} | Failed: {len(failures)}")
    return failures


def test_exhaustive_platform_registry_audit():
    print("\n=================================================================")
    print("2. EXHAUSTIVE 154-PLATFORM REGISTRY AUDIT")
    print("=================================================================")
    
    with open(TRACKER_JSON, "r", encoding="utf-8") as f:
        tracker = json.load(f)
        
    platforms = tracker.get("platforms", [])
    
    with open(DOC2_CSV, "r", encoding="utf-8", errors="ignore") as f:
        csv_rows = list(csv.DictReader(f))
        
    print(f"Registry platform counts: JSON={len(platforms)}, CSV={len(csv_rows)}")
    assert len(platforms) == 154, f"Expected 154 platforms in JSON, got {len(platforms)}"
    assert len(csv_rows) == 154, f"Expected 154 rows in CSV, got {len(csv_rows)}"
    
    # 1. Audit status distributions
    joined = [p for p in platforms if p.get("status") == "JOINED"]
    pending = [p for p in platforms if p.get("status") == "PENDING"]
    print(f"Status distribution: JOINED={len(joined)}, PENDING={len(pending)}")
    assert len(joined) == 56, f"Expected exactly 56 JOINED platforms, got {len(joined)}"
    assert len(pending) == 98, f"Expected exactly 98 PENDING platforms, got {len(pending)}"
    
    # 2. Check for private dashboard URLs in active_tenant_url (JOINED)
    # Prohibited patterns:
    # Subdomains: app.*, dashboard.*, console.*, admin.*, portal.*, account.*, accounts.*, workspace.*
    # Paths: /app, /app/, /admin, /signin, /sign-in, /login, /portal, /workspace, /dashboard, /console, /settings, /account, /onboarding, /welcome, /~
    dashboard_violations = []
    synthetic_violations = []
    firewall_violations = []
    rule45_violations = []
    
    for p in joined:
        rank = p.get("rank")
        name = p.get("name")
        url = (p.get("active_tenant_url") or "").strip()
        
        # Test against all firewall layers
        ok, layer, reason = IntegrityFirewall.run_all_layers(url, platform_name=name, probe_live=False)
        if not ok:
            firewall_violations.append((rank, name, layer, reason, url))
            
        # Specific check: Synthetic domain
        parsed = urllib.parse.urlparse(url)
        host = (parsed.hostname or "").lower()
        if "adi-telecoms.org" in host or host.endswith(".adi-telecoms.org"):
            synthetic_violations.append((rank, name, url))
            
        # Specific check: Private dashboard subdomains
        for sub in IntegrityFirewall.DASHBOARD_SUBDOMAINS:
            if host.startswith(sub) or ("." + sub) in host:
                dashboard_violations.append((rank, name, f"Private dashboard subdomain '{sub}'", url))
                
        # Specific check: Private dashboard paths
        if IntegrityFirewall.DASHBOARD_PATH_PATTERN.search(parsed.path):
            dashboard_violations.append((rank, name, f"Private dashboard path '{parsed.path}'", url))
            
        if "/~" in parsed.path or parsed.path.endswith("~"):
            dashboard_violations.append((rank, name, f"Home session fragment '/~'", url))
            
        # Specific check: Rule 45
        r45_ok, r45_msg = IntegrityFirewall.validate_layer5_rule_45(url)
        if not r45_ok:
            rule45_violations.append((rank, name, r45_msg, url))

    # 3. Check for synthetic domains across ALL 154 platforms in signup_url or domain
    for p in platforms:
        rank = p.get("rank")
        name = p.get("name")
        domain = (p.get("domain") or "").lower()
        signup_url = (p.get("signup_url") or "").lower()
        if "adi-telecoms.org" in domain or "adi-telecoms.org" in signup_url:
            synthetic_violations.append((rank, name, f"Synthetic domain in signup: {domain} / {signup_url}"))
            
    print(f"\n--- AUDIT VERIFICATION SUMMARY ---")
    print(f"Firewall Violations in 56 JOINED tenant URLs:   {len(firewall_violations)}")
    print(f"Dashboard Violations in 56 JOINED tenant URLs:  {len(dashboard_violations)}")
    print(f"Synthetic Domain Violations across 154 platforms: {len(synthetic_violations)}")
    print(f"Rule 45 Violations across 56 JOINED tenant URLs: {len(rule45_violations)}")
    
    for v in firewall_violations:
        print(f"  [FIREWALL VIOLATION] Rank {v[0]}: {v[1]} (Layer {v[2]}): {v[3]} -> URL: {v[4]}")
    for v in dashboard_violations:
        print(f"  [DASHBOARD VIOLATION] Rank {v[0]}: {v[1]}: {v[2]} -> URL: {v[3]}")
    for v in synthetic_violations:
        print(f"  [SYNTHETIC VIOLATION] Rank {v[0]}: {v[1]} -> URL: {v[2]}")
    for v in rule45_violations:
        print(f"  [RULE 45 VIOLATION] Rank {v[0]}: {v[1]}: {v[2]} -> URL: {v[3]}")
        
    return {
        "firewall_violations": firewall_violations,
        "dashboard_violations": dashboard_violations,
        "synthetic_violations": synthetic_violations,
        "rule45_violations": rule45_violations,
    }


def test_10_column_mathematical_parity():
    print("\n=================================================================")
    print("3. 10-COLUMN MATHEMATICAL PARITY VERIFICATION")
    print("=================================================================")
    
    with open(TRACKER_JSON, "r", encoding="utf-8") as f:
        tracker = json.load(f)
    with open(DOC2_CSV, "r", encoding="utf-8", errors="ignore") as f:
        csv_rows = list(csv.DictReader(f))
        
    platforms = tracker.get("platforms", [])
    
    col_map = [
        ("rank", "Rank"),
        ("name", "Platform Name"),
        ("domain", "Domain"),
        ("da", "DA"),
        ("category", "Category"),
        ("free_tier", "Free Allowance / Tier"),
        ("sso_method", "1-Click Join Method (SSO)"),
        ("signup_url", "Official Signup / Cloud URL"),
        ("status", "Status"),
        ("active_tenant_url", "Active Tenant URL"),
    ]
    
    discrepancies = []
    
    for idx, (p, r) in enumerate(zip(platforms, csv_rows), 1):
        for json_k, csv_k in col_map:
            val_j = str(p.get(json_k, "")).strip()
            val_c = str(r.get(csv_k, "")).strip()
            if val_j != val_c:
                discrepancies.append({
                    "row_index": idx,
                    "rank": p.get("rank"),
                    "platform": p.get("name"),
                    "column": f"{json_k} <-> {csv_k}",
                    "json_val": val_j,
                    "csv_val": val_c,
                })
                
    print(f"Total Column Discrepancies between JSON and CSV across all 154 rows: {len(discrepancies)}")
    for d in discrepancies[:10]:
        print(f"  [DIFF] Rank {d['rank']} ({d['platform']}) | Col {d['column']}: JSON='{d['json_val']}' != CSV='{d['csv_val']}'")
        
    return discrepancies


if __name__ == "__main__":
    layer5_failures = test_layer5_evasion_battery()
    audit_results = test_exhaustive_platform_registry_audit()
    discrepancies = test_10_column_mathematical_parity()
    
    print("\n=================================================================")
    print("CHALLENGER FINAL VERDICT ASSESSMENT")
    print("=================================================================")
    
    has_layer5_regressions = len(layer5_failures) > 0
    has_registry_violations = (
        len(audit_results["firewall_violations"]) > 0 or
        len(audit_results["dashboard_violations"]) > 0 or
        len(audit_results["synthetic_violations"]) > 0 or
        len(audit_results["rule45_violations"]) > 0 or
        len(discrepancies) > 0
    )
    
    if has_layer5_regressions:
        print(f"[-] Layer 5 Evasion Failures Detected: {len(layer5_failures)}")
    else:
        print("[+] Layer 5 Evasion Battery: 100% RESILIENT (0 failures)")
        
    if has_registry_violations:
        print(f"[-] Registry Violations Detected!")
    else:
        print("[+] Registry Audit: 100% CLEAN (0 dashboard URLs, 0 synthetic domains, 0 parity diffs)")
        
    if not has_layer5_regressions and not has_registry_violations:
        print("\n>>> VERDICT: APPROVE <<<")
        sys.exit(0)
    else:
        print("\n>>> VERDICT: REQUEST_CHANGES <<<")
        sys.exit(1)
