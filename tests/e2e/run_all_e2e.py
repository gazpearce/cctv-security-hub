#!/usr/bin/env python3
"""
Unified E2E Test Suite Runner
Autonomous Multi-Category Google & Cloud Stack Expansion Swarm

Runs all 4 verification tiers:
  Tier 1: Feature Coverage (>=40 tests)
  Tier 2: Boundary & Corner Cases (>=40 tests)
  Tier 3: Cross-Feature Combinations (>=8 tests)
  Tier 4: Real-World Application Scenarios (>=5 tests)

Supports running via:
  python tests/e2e/run_all_e2e.py
  python tests/e2e/run_all_e2e.py --tier 1
  pytest tests/e2e/
  python -m unittest discover -s tests/e2e
"""

import argparse
import io
import json
import os
import sys
import time
import unittest
from pathlib import Path

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Color codes
USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
GREEN = "\033[92m" if USE_COLOR else ""
RED = "\033[91m" if USE_COLOR else ""
YELLOW = "\033[93m" if USE_COLOR else ""
CYAN = "\033[96m" if USE_COLOR else ""
BOLD = "\033[1m" if USE_COLOR else ""
RESET = "\033[0m" if USE_COLOR else ""

TIER_MODULES = {
    1: {
        "name": "Tier 1: Feature Coverage (F1 to F8)",
        "module": "tests.e2e.test_tier1_features",
        "file": "test_tier1_features.py"
    },
    2: {
        "name": "Tier 2: Boundary & Corner Cases",
        "module": "tests.e2e.test_tier2_boundaries",
        "file": "test_tier2_boundaries.py"
    },
    3: {
        "name": "Tier 3: Cross-Feature Combinations",
        "module": "tests.e2e.test_tier3_cross_feature",
        "file": "test_tier3_cross_feature.py"
    },
    4: {
        "name": "Tier 4: Real-World Application Scenarios",
        "module": "tests.e2e.test_tier4_real_world",
        "file": "test_tier4_real_world.py"
    }
}


def run_tier(tier_num: int, verbose: bool = False):
    """Executes a single test tier and returns summary statistics."""
    tier_info = TIER_MODULES.get(tier_num)
    if not tier_info:
        raise ValueError(f"Invalid tier: {tier_num}")

    module_name = tier_info["module"]
    tests_dir = Path(__file__).resolve().parent
    file_path = tests_dir / tier_info["file"]

    if not file_path.exists():
        return {
            "tier": tier_num,
            "name": tier_info["name"],
            "tests_run": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "duration": 0.0,
            "success": False,
            "error_msg": f"Test file not found: {file_path}"
        }

    loader = unittest.defaultTestLoader
    try:
        suite = loader.loadTestsFromName(module_name)
    except Exception as e:
        return {
            "tier": tier_num,
            "name": tier_info["name"],
            "tests_run": 0,
            "passed": 0,
            "failed": 0,
            "errors": 1,
            "skipped": 0,
            "duration": 0.0,
            "success": False,
            "error_msg": f"Failed to load suite {module_name}: {e}"
        }

    verbosity_level = 2 if verbose else 1
    stream = io.StringIO() if not verbose else sys.stderr
    runner = unittest.TextTestRunner(stream=stream, verbosity=verbosity_level)

    start_time = time.time()
    result = runner.run(suite)
    duration = time.time() - start_time

    tests_run = result.testsRun
    failed = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    passed = tests_run - (failed + errors + skipped)
    success = result.wasSuccessful()

    return {
        "tier": tier_num,
        "name": tier_info["name"],
        "tests_run": tests_run,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "skipped": skipped,
        "duration": round(duration, 3),
        "success": success,
        "failures_detail": [f"{t}: {err}" for t, err in result.failures],
        "errors_detail": [f"{t}: {err}" for t, err in result.errors]
    }


def main():
    parser = argparse.ArgumentParser(description="Unified E2E Test Suite Runner")
    parser.add_argument("--tier", choices=["1", "2", "3", "4", "all"], default="all",
                        help="Specify tier to run (default: all)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose test execution output")
    parser.add_argument("--json", dest="json_output", action="store_true", help="Print summary as JSON")
    args = parser.parse_args()

    tiers_to_run = [1, 2, 3, 4] if args.tier == "all" else [int(args.tier)]

    if not args.json_output:
        print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
        print(f"{BOLD}{CYAN}  Autonomous Multi-Category Google & Cloud Stack Expansion Swarm{RESET}")
        print(f"{BOLD}  Unified Opaque-Box E2E Test Runner — Tiers 1 to 4{RESET}")
        print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    overall_start = time.time()
    results = []

    for tier_num in tiers_to_run:
        tier_name = TIER_MODULES[tier_num]["name"]
        if not args.json_output:
            print(f"{BOLD}>> Running {tier_name}...{RESET}")
        tier_res = run_tier(tier_num, verbose=args.verbose)
        results.append(tier_res)

        if not args.json_output:
            status_badge = f"{GREEN}[PASS]{RESET}" if tier_res["success"] else f"{RED}[FAIL]{RESET}"
            print(f"   {status_badge} Tests: {tier_res['tests_run']} | Passed: {tier_res['passed']} | "
                  f"Failed: {tier_res['failed']} | Errors: {tier_res['errors']} | Time: {tier_res['duration']}s\n")

    overall_duration = round(time.time() - overall_start, 3)
    total_run = sum(r["tests_run"] for r in results)
    total_passed = sum(r["passed"] for r in results)
    total_failed = sum(r["failed"] for r in results)
    total_errors = sum(r["errors"] for r in results)
    total_skipped = sum(r["skipped"] for r in results)
    all_success = all(r["success"] for r in results)

    if args.json_output:
        summary = {
            "success": all_success,
            "total_run": total_run,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_errors": total_errors,
            "total_skipped": total_skipped,
            "duration": overall_duration,
            "tiers": results
        }
        print(json.dumps(summary, indent=2))
        sys.exit(0 if all_success else 1)

    print(f"{BOLD}{CYAN}----------------------------------------------------------------------{RESET}")
    print(f"{BOLD}E2E TEST EXECUTION SUMMARY{RESET}")
    print(f"{BOLD}{CYAN}----------------------------------------------------------------------{RESET}")
    print(f"Total Tiers Executed:   {len(results)}")
    print(f"Total Tests Run:        {total_run}")
    print(f"Total Passed:           {GREEN}{total_passed}{RESET}")
    print(f"Total Failed:           {RED if total_failed > 0 else ''}{total_failed}{RESET}")
    print(f"Total Errors:           {RED if total_errors > 0 else ''}{total_errors}{RESET}")
    print(f"Total Duration:         {overall_duration}s")

    if all_success:
        print(f"\n{GREEN}{BOLD}>>> ALL EXECUTED E2E TESTS PASSED (100% SUCCESS) <<<{RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{RED}{BOLD}>>> E2E TEST FAILURES DETECTED <<< {RESET}\n")
        for r in results:
            if not r["success"]:
                print(f"{RED}Failure in {r['name']}:{RESET}")
                for f in r.get("failures_detail", []):
                    print(f"  - {f}")
                for e in r.get("errors_detail", []):
                    print(f"  - ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
