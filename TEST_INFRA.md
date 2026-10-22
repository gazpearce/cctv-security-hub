# Test Infrastructure Specification: Autonomous Multi-Category Google & Cloud Stack Expansion Swarm

**Document Version:** 1.0.0  
**Target Project:** `C:\Users\Gary\github-cctv-seo`  
**Test Suite Directory:** `C:\Users\Gary\github-cctv-seo\tests\e2e\`  
**Test Framework:** Python standard `unittest` and `pytest 9.1+` compatible  
**Lead Engineer & Business Entity:** Gary Pearce, ADI Communications (`07860 244 274`)  
**Compliance Standard:** British English (`en-GB`), Rule 45 Google Shield Air-Gap, JSON Schema Draft 2020-12  

---

## 1. Executive Summary & Test Philosophy

This document defines the comprehensive opaque-box End-to-End (E2E) test infrastructure for the **Autonomous Multi-Category Google & Cloud Stack Expansion Swarm**.

The test harness exercises the system strictly through public interfaces, CLI commands, data feeds, relational datasets, and external integration contracts. It enforces the following core testing invariants:
1. **Opaque-Box Verification**: Tests validate observable behaviors, exit codes, generated files, schema adherence, and network/CDP interface contracts rather than private internal implementation details.
2. **Deterministic Output & Authoritative Sources**: Expected outputs are derived strictly from `ORIGINAL_REQUEST.md`, `PROJECT.md`, `RULE[user_global]`, and official specifications (e.g. JSON Schema Draft 2020-12).
3. **No Facade Tests**: Every test exercises genuine parsing, validation, transformation, or verification logic with explicit assertions.
4. **Adversarial & Boundary Verification**: Exhaustively tests encoding anomalies, missing files, malformed markup, out-of-range metrics, and security boundaries (specifically the Rule 45 zero-raw-root-link firewall).
5. **Test Isolation**: Each test operates independently with isolated fixtures, temporary mock environments where needed, and zero shared mutable state leaks.

---

## 2. Feature Inventory Mapping

Every feature from `PROJECT.md § Feature Inventory` is mapped to dedicated test suites across all 4 tiers:

| Feature ID | Feature Name | Primary Implementation / Interfaces | Test Suite Module | Target Tier 1 Classes | Target Tier 2 Classes |
|:---:|:---|:---|:---|:---|:---|
| **F1** | Top-of-Stack Google Apex Registry | `swarm_stack_orchestrator.py` (`STACK_TEAMS`), `doc1_music_stack_100.csv`, `doc2_cloud_stack_100.csv`, `doc3_published_asset_links.csv` | `test_tier1_features.py`, `test_tier2_boundaries.py` | `TestF1TopTierGoogleApexRegistry` | `TestF1ApexBoundaries` |
| **F2** | Automated Email & OTP Verification Loop Engine | `auto_email_verifier.py`, CDP port 9223 (`http://127.0.0.1:9223/json`), DOM evaluation | `test_tier1_features.py`, `test_tier2_boundaries.py` | `TestF2AutomatedEmailOTPVerification` | `TestF2EmailOTPBoundaries` |
| **F3** | Multi-Category Stack Expansion & Platform Onboarding Engine | `master_cloud_signup_tracker.json`, `doc1_route_domains_directory.csv`, `doc2_cloud_stack_100.csv`, `autonomous_cloud_deployer.py` | `test_tier1_features.py`, `test_tier2_boundaries.py` | `TestF3MultiCategoryStackExpansion` | `TestF3OnboardingBoundaries` |
| **F4** | Profile Standardization & E-E-A-T Trade Metadata | `master_profile_manifest.json`, `doc2_established_profiles_list.csv`, jsDelivr CDN assets | `test_tier1_features.py`, `test_tier2_boundaries.py` | `TestF4ProfileStandardizationEEAT` | `TestF4ProfileMetadataBoundaries` |
| **F5** | Reciprocal Linking & Rule 45 Compliance Engine | `verify_no_root_anchors.py`, `fix_rule45_anchors.py`, repository-wide scan | `test_tier1_features.py`, `test_tier2_boundaries.py` | `TestF5Rule45ComplianceEngine` | `TestF5Rule45Boundaries` |
| **F6** | Backlink Ledger Synchronization & Publishing Pipeline | `build_public_backlink_ledger.py`, `doc3_published_asset_links.csv`, `public_backlink_master_ledger.csv/json/html` | `test_tier1_features.py`, `test_tier2_boundaries.py` | `TestF6BacklinkLedgerPipeline` | `TestF6LedgerBoundaries` |
| **F7** | Master `/gstack` Swarm Orchestration Skill | `swarm_stack_orchestrator.py`, `C:\Users\Gary\.gemini\config\skills\gstack\SKILL.md`, 12 companion skills | `test_tier1_features.py`, `test_tier2_boundaries.py` | `TestF7MasterGStackOrchestrator` | `TestF7OrchestrationBoundaries` |
| **F8** | Opaque-Box E2E Testing Suite & Hardening | `tests/e2e/run_all_e2e.py`, `TEST_INFRA.md`, `TEST_READY.md` | `test_tier1_features.py`, `test_tier2_boundaries.py` | `TestF8TestingSuiteHardening` | `TestF8TestRunnerBoundaries` |

---

## 3. Test Architecture & Tier Coverage Thresholds

The test suite is structured into 4 distinct verification tiers totaling **>=93 test cases**:

```
tests/e2e/
├── __init__.py
├── run_all_e2e.py                  # Unified CLI Test Runner with ANSI/Text reporting
├── test_tier1_features.py          # Tier 1: Feature Coverage (>=40 tests; >=5 per feature)
├── test_tier2_boundaries.py        # Tier 2: Boundary & Corner Cases (>=40 tests; >=5 per feature)
├── test_tier3_cross_feature.py     # Tier 3: Cross-Feature Interactions (>=8 pairwise tests)
└── test_tier4_real_world.py        # Tier 4: Real-World Operational Scenarios (>=5 scenarios)
```

### Coverage Thresholds by Tier

| Tier | Purpose | Required Threshold | Designed Count | Passing Criteria |
|:---:|:---|:---:|:---:|:---|
| **Tier 1** | **Feature Coverage**: Verifies primary functional paths and contracts for all 8 features. | $\ge 5$ tests per feature ($\ge 40$ tests) | **41 tests** | 100% Pass; zero assertions failed. |
| **Tier 2** | **Boundary & Edge Cases**: Extreme values, malformed inputs, edge conditions, security rules. | $\ge 5$ tests per feature ($\ge 40$ tests) | **41 tests** | 100% Pass; proper rejection / error handling. |
| **Tier 3** | **Cross-Feature Combinations**: Pairwise interactions between cooperating system modules. | $\ge 8$ pairwise combinations | **9 tests** | 100% Pass; end-to-end relational consistency. |
| **Tier 4** | **Real-World Application Scenarios**: Multi-step lifecycles and realistic failure/recovery scenarios. | $\ge 5$ comprehensive scenarios | **5 scenarios** | 100% Pass; clean lifecycle completion. |
| **Total** | **Full E2E Testing Suite** | **$\ge 93$ test cases** | **96 test cases** | **100% Pass across all tiers** |

---

## 4. Detailed Specification of Test Tiers

### Tier 1: Feature Coverage (`test_tier1_features.py`)
- **F1 (Apex Registry)**:
  - `test_f1_01_all_11_stacks_defined_with_google_apex`: Validates all 11 stacks in `STACK_TEAMS` map to Google Apex entities.
  - `test_f1_02_apex_urls_valid_https_google_domains`: Validates Apex URLs use HTTPS and authentic Google authority domains (`youtube.com`, `drive.google.com`, `blogger.com` / `blogspot.com`, `firebase.app` / `web.app`, `maps.google.com`, `docs.google.com`).
  - `test_f1_03_published_assets_contain_valid_apex`: Validates every record in `doc3_published_asset_links.csv` routes upward to a valid Google Apex.
  - `test_f1_04_music_and_cloud_registries_have_apex_targets`: Verifies presence and non-emptiness of Apex targets in `doc1_music_stack_100.csv` and `doc2_cloud_stack_100.csv`.
  - `test_f1_05_zero_insecure_http_in_apex_registries`: Verifies zero insecure HTTP protocol URLs in Apex definitions.
- **F2 (Automated Email & OTP Loop)**:
  - `test_f2_01_cdp_endpoint_configuration`: Validates CDP base URL format `http://127.0.0.1:9223`.
  - `test_f2_02_tab_selector_filters_real_gmail_inbox`: Validates tab matching logic selects `https://mail.google.com/` and excludes cookie/auth tabs.
  - `test_f2_03_otp_code_regex_extraction`: Tests accurate extraction of 6-digit numeric OTP codes from email text.
  - `test_f2_04_verification_keyword_matching`: Validates identification of activation triggers (`verify`, `confirm`, `activate`, `welcome`).
  - `test_f2_05_email_verifier_graceful_error_handling`: Verifies graceful failure (returns None/empty) when CDP service is unreachable.
- **F3 (Platform Expansion & Onboarding Engine)**:
  - `test_f3_01_cloud_signup_tracker_structure`: Validates 154 platforms in `master_cloud_signup_tracker.json` with required schema fields.
  - `test_f3_02_cloud_tracker_status_values`: Validates all status values are `JOINED` or `PENDING` (no invalid status strings).
  - `test_f3_03_route_domains_directory_row_count`: Validates `doc1_route_domains_directory.csv` contains >=1,000 route domains.
  - `test_f3_04_official_signup_urls_valid_https`: Validates candidate signup URLs are well-formed HTTPS web addresses.
  - `test_f3_05_sso_join_methods_classified`: Validates supported SSO categories (GitHub, Google, Email, API) across candidate platforms.
- **F4 (Profile Standardization & E-E-A-T)**:
  - `test_f4_01_manifest_json_schema_valid`: Validates `master_profile_manifest.json` against JSON Schema Draft 2020-12.
  - `test_f4_02_engineer_identity_and_direct_mobile`: Validates Gary Pearce name, ADI Communications, and direct mobile `07860 244 274` (zero 0800 numbers).
  - `test_f4_03_cai_non_membership_disclaimer`: Validates strict compliance with CAI disclaimer (uses benchmarked equipment; never claims CAI membership).
  - `test_f4_04_verified_rating_and_checkatrade_ban`: Validates 9.98/10 rating across 84+ reviews and zero occurrences of banned word "Checkatrade".
  - `test_f4_05_visual_cdn_webp_assets_integrity`: Validates jsDelivr CDN URLs for square avatar and 16:9 banner ending in `.webp`.
- **F5 (Rule 45 Compliance Engine)**:
  - `test_f5_01_verify_no_root_anchors_script_execution`: Runs `verify_no_root_anchors.py` and confirms exit code 0.
  - `test_f5_02_regex_detects_forbidden_root_anchors`: Tests Rule 45 regex against direct money site roots.
  - `test_f5_03_regex_permits_allowed_buffer_subpaths`: Verifies permitted `/news/`, `/assets/`, `/feed/` subpaths pass cleanly.
  - `test_f5_04_published_assets_zero_raw_root_links`: Verifies zero naked root links in `doc3_published_asset_links.csv`.
  - `test_f5_05_fix_rule45_anchors_redirection_mapping`: Tests self-healing re-routing logic to approved buffer destinations.
- **F6 (Backlink Ledger Publishing Pipeline)**:
  - `test_f6_01_doc3_published_assets_structure`: Validates 14 columns, valid `LINK-xxxx` IDs, and `ACTIVE_VERIFIED` status in `doc3`.
  - `test_f6_02_mathematical_parity_across_csv_json_html`: Validates row count parity between `public_backlink_master_ledger.csv`, `.json`, and `.html`.
  - `test_f6_03_json_master_ledger_metadata_and_schema`: Validates JSON ledger attributes (`lead_engineer`, `rule_45_shield`, `total_backlinks`).
  - `test_f6_04_html_ledger_googlebot_meta_and_table`: Validates `<meta name="robots" content="index, follow">` and table structure.
  - `test_f6_05_build_ledger_deterministic_regeneration`: Executes `build_public_backlink_ledger.py` and verifies outputs regenerate cleanly.
- **F7 (Master `/gstack` Swarm Orchestration)**:
  - `test_f7_01_master_gstack_skill_markdown_exists`: Validates `gstack/SKILL.md` exists and defines the 16-node Google AI Matrix.
  - `test_f7_02_companion_skills_completeness`: Validates presence of all 12 companion skills (`gstack-video` through `gstack-verifier`).
  - `test_f7_03_orchestrator_stack_teams_mapping`: Validates `swarm_stack_orchestrator.py` maps all 11 stacks + verifier + ledger.
  - `test_f7_04_orchestrator_cli_help_and_commands`: Validates CLI execution with `--help` and standard operational arguments.
  - `test_f7_05_orchestrator_step_runner_capture`: Validates subprocess execution logging and error handling in orchestrator engine.
- **F8 (Testing Suite & Hardening)**:
  - `test_f8_01_run_all_e2e_runner_executable`: Validates `run_all_e2e.py` exists and is directly executable.
  - `test_f8_02_test_infra_specification_exists`: Validates presence and completeness of `TEST_INFRA.md`.
  - `test_f8_03_test_ready_document_exists`: Validates presence of `TEST_READY.md`.
  - `test_f8_04_test_independence_and_no_leftover_artifacts`: Verifies tests execute in isolated directories with zero persistent temporary pollution.
  - `test_f8_05_total_e2e_test_count_meets_threshold`: Verifies discovered test count across all tiers $\ge 93$.

---

### Tier 2: Boundary & Corner Cases (`test_tier2_boundaries.py`)
Exhaustive stress tests for edge conditions:
- **F1 (Apex Boundaries)**: URL trailing slash normalization, mixed-case domain normalization, invalid domain rejections, internationalized domain handling, duplicate stack category protection.
- **F2 (Email OTP Boundaries)**: Empty email inbox list, non-numeric OTP candidate rejection, 4-digit / 8-digit OTP boundaries, corrupted HTML DOM payload handling, 20MB payload size limits.
- **F3 (Onboarding Boundaries)**: Empty platforms registry handling, invalid Domain Authority (<0 or >100) handling, unusual character encoding in platform titles, duplicate platform names, non-HTTPS signup URLs.
- **F4 (Profile Boundaries)**: Exact 160-character boundary test for short bio, phone number spacing variations (`07860244274`, `07860 244 274`, `+44 7860 244 274`), CAI false-positive avoidance, missing credential field resilience, non-WebP image format rejection.
- **F5 (Rule 45 Boundaries)**: Subpath collision attacks (`adicommunications.co.uk/news-fake` vs `/news/`), query-string edge cases (`adicommunications.co.uk?ref=foo`), port specifiers (`adicommunications.co.uk:443/`), mixed-case hostnames (`ADICOMMUNICATIONS.CO.UK/`), embedded markdown link variations.
- **F6 (Ledger Boundaries)**: Empty CSV input file resilience, Unicode / emoji asset title handling, HTTP non-200 code injection, corrupted JSON input rejection, zero-row HTML table generation.
- **F7 (Orchestration Boundaries)**: Unknown CLI action argument, missing target script resilience, non-zero subprocess error code propagation, empty argument dispatch, concurrent file access protection.
- **F8 (Test Runner Boundaries)**: Invalid tier filter argument, summary aggregation with zero failures, ANSI color disablement on non-TTY, exit code 1 on failed tests, runtime measurement accuracy.

---

### Tier 3: Cross-Feature Interactions (`test_tier3_cross_feature.py`)
Validates contract interfaces across functional boundaries:
1. `test_f1_x_f5_all_11_apexes_satisfy_rule45`: Verifies that none of the 11 Google Apex entities route to forbidden raw root money links.
2. `test_f2_x_f3_email_verifier_matches_onboarding_domain`: Verifies email verification extraction against candidate platform domains in `master_cloud_signup_tracker.json`.
3. `test_f3_x_f4_established_profiles_match_standardized_metadata`: Verifies established profile list records in `doc2` match `master_profile_manifest.json` standards.
4. `test_f4_x_f5_profile_manifest_urls_comply_with_rule45`: Verifies all URLs and anchors in `master_profile_manifest.json` strictly comply with Rule 45.
5. `test_f5_x_f6_published_assets_in_doc3_pass_rule45_audit`: Verifies all published assets in `doc3` pass the Rule 45 validator.
6. `test_f6_x_f1_ledger_assets_upward_route_to_verified_apexes`: Verifies every asset in the compiled ledger routes to a recognized Top-of-Stack Google Apex.
7. `test_f7_x_f3_orchestrator_cloud_team_matches_signup_tracker`: Verifies orchestrator cloud deployment configurations align with the 154-platform tracker.
8. `test_f7_x_f2_orchestrator_verifier_team_invokes_auto_email_verifier`: Verifies orchestrator verifier team references and executes `auto_email_verifier.py`.
9. `test_f7_x_f6_orchestrator_ledger_team_invokes_backlink_builder`: Verifies orchestrator ledger team references and executes `build_public_backlink_ledger.py`.

---

### Tier 4: Real-World Application Scenarios (`test_tier4_real_world.py`)
Simulates complete real-world operational workflows:
1. `test_scenario_01_full_lifecycle_onboarding_to_ledger`:
   Complete lifecycle: ingest new candidate platform, generate Gary Pearce profile, extract mock email verification, register asset in `doc3`, compile master CSV/JSON/HTML ledgers, and verify HTTP 200 and Rule 45 compliance.
2. `test_scenario_02_multi_category_swarm_orchestration_audit`:
   Full pre-flight audit across all 11 category stacks, verifying that all subagent teams have valid apex endpoints, scripts, and pass Rule 45 compliance before deployment.
3. `test_scenario_03_zero_tolerance_rule45_quarantine_and_healing`:
   Injects raw root link defect into candidate asset dataset, verifies that compliance auditor catches and blocks publication, applies self-healing re-route to `/news/` buffer, and verifies final clean build.
4. `test_scenario_04_live_ledger_mathematical_parity_and_schema_validation`:
   Executes `build_public_backlink_ledger.py` on real repository files, asserts 100% mathematical parity across CSV, JSON, and HTML, and validates JSON against draft 2020-12 schema.
5. `test_scenario_05_automated_email_otp_extraction_and_sso_authentication`:
   Simulates full authentication loop: platform signup triggers email, CDP inspection extracts 6-digit OTP code, and verifies account onboarding readiness.

---

## 5. Execution Commands & Test Harness Invocation

### Method 1: Unified E2E Test Runner (Recommended)
```bash
# Run all tiers (Tiers 1-4) with full summary reporting:
python tests/e2e/run_all_e2e.py

# Run specific tier:
python tests/e2e/run_all_e2e.py --tier 1
python tests/e2e/run_all_e2e.py --tier 2
python tests/e2e/run_all_e2e.py --tier 3
python tests/e2e/run_all_e2e.py --tier 4

# Run with JSON summary output:
python tests/e2e/run_all_e2e.py --json

# Run in verbose mode:
python tests/e2e/run_all_e2e.py -v
```

### Method 2: Standard `pytest`
```bash
# Run entire E2E test suite:
pytest tests/e2e/ -v

# Run individual test files:
pytest tests/e2e/test_tier1_features.py -v
pytest tests/e2e/test_tier2_boundaries.py -v
pytest tests/e2e/test_tier3_cross_feature.py -v
pytest tests/e2e/test_tier4_real_world.py -v

# Run with concise summary:
pytest tests/e2e/ -q
```

### Method 3: Standard Python `unittest`
```bash
# Discover and run all tests in tests/e2e:
python -m unittest discover -s tests/e2e -p "test_*.py" -v
```

---

## 6. Authoritative Sources of Expected Output

Every test case derives its assertions from an explicit authoritative source:
1. `ORIGINAL_REQUEST.md`: Specification of 11 category stacks, Gary Pearce credentials, Rule 45 requirements, `/gstack` orchestration skill.
2. `PROJECT.md`: Feature Inventory (F1 to F8), Interface Contracts, Milestones.
3. `RULE[user_global]`: Gary Pearce (07860 244 274), CAI non-membership prohibition, 9.98/10 rating across 84+ reviews, WebP format requirements.
4. `MASTER_SEO_STACK_LINKING_BLUEPRINT.md`: Apex entity topology and buffer article URLs.
5. `master_profile_manifest.json`: Single source of truth for brand standards, bios, and CDN visual assets.
6. `verify_no_root_anchors.py`: Canonical regex definition for Rule 45 enforcement.
7. `JSON Schema Draft 2020-12`: Official schema standard for ledger and manifest files.

---

## 7. Pass/Fail & Exit Code Contract

- **Exit Code 0**: All tests passed (100% success rate across all executed tiers).
- **Exit Code 1**: One or more tests failed, assertion errors encountered, or unhandled exceptions thrown.
- **Reporting**: The test runner outputs clear ANSI-colored or clean plain-text metrics detailing total tests run, passed, failed, errors, execution duration, and per-tier breakdown.
