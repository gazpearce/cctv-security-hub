# Project: Autonomous Multi-Category Google & Cloud Stack Expansion Swarm

## Architecture
- **Top-of-Stack Google Citadel Apex**: Authoritative Google properties (DA 99-100: Drive CAD Vault, YouTube Channel/Podcasts/Music, Blogger Hub, Firebase Edge, Google Docs/Classroom, Google Maps CID) sit at the top of each of the 11 category stacks.
- **Rule 45 Google Shield Buffer Architecture**: External Tier-2 and Tier-3 platforms channel link equity upward into the category Google Apex or disposable `/news/` editorial buffer guides on `adicommunications.co.uk/news/...`. Zero raw root anchor links to `https://adicommunications.co.uk/` are permitted anywhere.
- **Automated Verification Loop**: Real-time Chrome DevTools Protocol (CDP port 9223) bridge connected to authenticated Google Workspace (`admin@adicommunications.co.uk`), developer Gmail (`aiagent1510@gmail.com`), and GitHub (`gazpearce`) for automated 1-click SSO and OTP/activation link extraction.
- **Public Backlink Discovery Ledger Pipeline**: 3-tier relational database (`doc1` route domains -> `doc2` established profiles -> `doc3` published assets) compiled into `public_backlink_master_ledger.csv`, `public_backlink_master_ledger.json`, and static crawler-indexed `public_backlink_ledger.html`.
- **Master `/gstack` Swarm Skill**: Unified orchestration engine coordinating 11 category stack subagents (`gstack-video`, `gstack-podcast`, `gstack-docs`, `gstack-blog`, `gstack-cloud`, `gstack-media`, `gstack-howto`, `gstack-bookmark`, `gstack-rss`, `gstack-music`, `gstack-offers`) and verification gatekeepers (`gstack-verifier`).

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Top-of-Stack Google Apex Registry | All 11 category stacks mapped to active, verified DA 99-100 Google Citadel endpoints | M2 | ORIGINAL_REQUEST §Architecture, Survey 2 & 3 |
| 2 | Automated Email & OTP Verification Loop Engine | Automated CDP port 9223 Gmail / Workspace inspection, extracting OTPs and activation links via fixed tab selector | M1 | ORIGINAL_REQUEST §R2, Survey 1 & 3 |
| 3 | Multi-Category Stack Expansion & Platform Onboarding Engine | Systematic candidate processing across 11 stacks, onboarding new accounts using Gary's credentials & GitHub SSO | M1 | ORIGINAL_REQUEST §R1, Survey 1 |
| 4 | Profile Standardization & E-E-A-T Trade Metadata | Enforcing Gary Pearce, ADI Communications, 07860 244 274, £10M insurance, CAI disclaimer, 9.98/10 rating, WebP CDN assets | M2 | ORIGINAL_REQUEST §R3, Survey 1 & 3 |
| 5 | Reciprocal Linking & Rule 45 Compliance Engine | Automated validation script verifying 100% compliance: zero raw root links to adicommunications.co.uk/, channeling link equity to Apex | M2 | ORIGINAL_REQUEST §R4, Survey 2 |
| 6 | Backlink Ledger Synchronization & Publishing Pipeline | Syncing doc3, compiling master CSV, JSON schema 2020-12, and HTML discovery ledger with robots index,follow | M3 | ORIGINAL_REQUEST §Acceptance Criteria, Survey 2 |
| 7 | Master /gstack Swarm Orchestration Skill | Consolidated master skill (/gstack) orchestrating, dispatching, and monitoring all 11 category stack subagents | M4 | ORIGINAL_REQUEST §R5, Survey 1 & 3 |
| 8 | Opaque-Box E2E Testing Suite & Hardening | Full 4-tier test suite (Feature, Boundary, Combinatorial, Real-World) + Tier 5 adversarial coverage hardening | E2E_TRACK / M5 | ORIGINAL_REQUEST §Acceptance Criteria, Project Pattern |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Automated Verification & Onboarding Engine | Fix auto_email_verifier.py tab selector, verify CDP 9223 live inbox OTP extraction, build automated platform onboarding script | none | PLANNED |
| M2 | Multi-Category Stack & Profile Standardization | Verify 11 Google Apex entities, enforce Gary Pearce E-E-A-T metadata, enforce Rule 45 zero raw root link firewall | M1 | PLANNED |
| M3 | Backlink Ledger Synchronization & Publishing | Ingest new endpoints into doc3, compile public_backlink_master_ledger.csv/json/html, verify HTTP 200 statuses | M2 | PLANNED |
| M4 | Master /gstack Swarm Orchestration Skill | Validate and configure /gstack master skill, verify subagent dispatching interfaces, ensure command execution parity | M3 | PLANNED |
| M5 | Final Milestone: 100% E2E Test Pass & Hardening | Pass 100% of E2E test suite (Tiers 1-4), perform Tier 5 adversarial hardening with Challenger | M4, E2E_TRACK | PLANNED |
| E2E | E2E Testing Track | Requirement-driven test harness, 4-tier opaque-box test suite covering all features, publish TEST_READY.md | none | DONE |

## Interface Contracts
### Automated Verification Loop ↔ Platform Onboarding Engine
- `auto_email_verifier.py` provides:
  - `get_recent_emails(max_count=10)` -> list of email dicts `{subject, sender, snippet, link}`
  - `find_verification_link(platform_domain)` -> string URL or None
  - `find_otp_code(platform_name)` -> string 4-8 digit code or None
- CDP Connection: `http://127.0.0.1:9223/json`

### Platform Onboarding Engine ↔ Backlink Ledger Pipeline
- Onboarded platform records output format:
  `doc3_published_asset_links.csv`:
  `asset_id, parent_profile_id, platform_name, profile_live_url, asset_title, asset_type, asset_public_url, top_of_stack_apex_url, shield_target_url, seo_tags, seo_description_summary, dofollow_status, publication_date, verification_status`
- Status values: `ACTIVE_VERIFIED`, `PENDING_VERIFICATION`, `FAILED_JOIN`

### Master /gstack Skill ↔ Category Stack Agents
- Master skill invocation: `/gstack <command> [category]`
- Commands: `status`, `expand`, `verify`, `sync`, `audit`
- Subagent dispatch triggers: `gstack-video`, `gstack-podcast`, `gstack-docs`, `gstack-blog`, `gstack-cloud`, `gstack-media`, `gstack-howto`, `gstack-bookmark`, `gstack-rss`, `gstack-music`, `gstack-offers`, `gstack-verifier`

## Code Layout
- `auto_email_verifier.py`: CDP email inspection & OTP extraction
- `verify_no_root_anchors.py`: Rule 45 compliance audit script
- `build_public_backlink_ledger.py`: Backlink ledger compilation script
- `master_cloud_signup_tracker.json`: 154-platform onboarding tracking database
- `doc1_route_domains_directory.csv`: 1,003 route domains registry
- `doc2_established_profiles_list.csv`: Established profiles registry (PROF-001..PROF-100)
- `doc3_published_asset_links.csv`: Published asset links database
- `public_backlink_master_ledger.csv`: Master backlink registry (HTTP 200 verified)
- `public_backlink_master_ledger.json`: Master JSON schema backlink registry
- `public_backlink_ledger.html`: Public crawler-indexed ledger table
- `tests/e2e/`: E2E test runner and test tiers (Tiers 1-4)
- `C:\Users\Gary\.gemini\config\skills\gstack\`: Master `/gstack` swarm orchestration skill
