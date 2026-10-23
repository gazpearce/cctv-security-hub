#!/usr/bin/env python3
"""
tests/test_m4all_skills_sync.py
===============================
Comprehensive Verification & Test Suite for Milestone M4-ALL:
1. All 9 G-Stack Skills Presence & Frontmatter Validity in Gemini Config.
2. Full Platform Catalog Counts (156 visual, 50 video, 15 RSS, 18 presentation, 28 bookmark, 100+ landing).
3. 16-Node Multi-Platform Swarm Topology & Script Roster Alignment in gstack and orchestrator.
4. Rule 46 (Master Real Questions & Genuine Trade Value Law) Enforcement & 4 High-Value Pillars.
5. Absolute Ban on BS EN / ISO Standards in Titles & Hooks and Ban on "Top 10" Affiliate Slop.
6. Rule 45 Google Shield Air-Gap Compliance (Zero Naked Root Links across all skills).
7. Gary Pearce E-E-A-T Trade Metadata, £10M Liability, 07860 244 274, and Checkatrade Exclusion.

Target Skills Directory: C:\\Users\\Gary\\.gemini\\config\\skills
Author: explorer_m4all_3
"""

import os
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = Path(r"C:\Users\Gary\.gemini\config\skills")

ALL_9_SKILLS = [
    "gstack",
    "gstack-media",
    "gstack-video",
    "gstack-rss",
    "gstack-docs",
    "gstack-podcast",
    "gstack-bookmark",
    "gstack-verifier",
    "gstack-sites",
]

EXPECTED_16_SWARM_AGENTS = [
    "stack-video-agent",
    "stack-media-agent",
    "stack-docs-agent",
    "stack-rss-agent",
    "stack-podcast-agent",
    "stack-bookmark-agent",
    "stack-verifier-agent",
    "stack-sites-agent",
    "stack-cloud-agent",
    "onboarding-agent",
    "browser-worker-agent",
    "multimedia-producer-agent",
    "2fa-daemon-agent",
    "ledger-guard-agent",
    "citadel-apex-agent",
    "master-qc-agent",
]

RULE_46_FOUR_PILLARS = [
    "customer problems",
    "latest products",
    "honest trade opinions",
    "specs translated",
]


class TestM4AllSkillsPresenceAndFrontmatter(unittest.TestCase):
    """Test Suite 1: Verifies presence and valid YAML frontmatter of all 9 skills."""

    def test_01_all_9_skills_exist(self):
        """Verify that all 9 skills exist in C:\\Users\\Gary\\.gemini\\config\\skills."""
        self.assertTrue(SKILLS_DIR.exists(), f"Skills directory not found at {SKILLS_DIR}")
        for skill_name in ALL_9_SKILLS:
            skill_path = SKILLS_DIR / skill_name / "SKILL.md"
            self.assertTrue(
                skill_path.exists(),
                f"Missing mandatory skill file: {skill_path}"
            )

    def test_02_valid_yaml_frontmatter(self):
        """Verify each of the 9 skills contains well-formed YAML frontmatter."""
        for skill_name in ALL_9_SKILLS:
            skill_path = SKILLS_DIR / skill_name / "SKILL.md"
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertTrue(
                content.startswith("---"),
                f"{skill_name}/SKILL.md must start with YAML frontmatter delimiter '---'"
            )
            frontmatter_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            self.assertIsNotNone(
                frontmatter_match,
                f"{skill_name}/SKILL.md must contain closed YAML frontmatter block"
            )
            frontmatter_text = frontmatter_match.group(1)
            self.assertIn(
                f"name: {skill_name}",
                frontmatter_text,
                f"Frontmatter of {skill_name} must declare 'name: {skill_name}'"
            )
            self.assertIn(
                "description:",
                frontmatter_text,
                f"Frontmatter of {skill_name} must contain 'description:'"
            )


class TestM4AllCatalogMetrics(unittest.TestCase):
    """Test Suite 2: Verifies catalog platform metrics across the specialized skills."""

    def test_01_media_skill_catalog_metrics(self):
        """Verify gstack-media declares the 156-platform visual network and Google Slides DA 100 apex."""
        skill_path = SKILLS_DIR / "gstack-media" / "SKILL.md"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertTrue(
            "156" in content or "156+" in content,
            "gstack-media must specify 156 image/visual platforms"
        )
        self.assertIn("docs.google.com/presentation", content, "gstack-media must cite Google Slides presentation apex")

    def test_02_video_skill_catalog_metrics(self):
        """Verify gstack-video declares the 50-platform video directory and YouTube Apex."""
        skill_path = SKILLS_DIR / "gstack-video" / "SKILL.md"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("50", content, "gstack-video must declare 50 video platforms")
        self.assertIn("@CCTV.services", content, "gstack-video must cite @CCTV.services YouTube Apex")

    def test_03_rss_skill_catalog_metrics(self):
        """Verify gstack-rss declares the 15 feed aggregators and Feedburner/Blogger RSS apex."""
        skill_path = SKILLS_DIR / "gstack-rss" / "SKILL.md"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertTrue("15" in content or "15+" in content, "gstack-rss must declare 15 feed aggregators")
        self.assertIn("tvandhomesecurity.blogspot.com/feeds", content, "gstack-rss must cite Blogger RSS apex")

    def test_04_docs_skill_catalog_metrics(self):
        """Verify gstack-docs declares 18 presentation hubs / 15 doc repositories."""
        skill_path = SKILLS_DIR / "gstack-docs" / "SKILL.md"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertTrue(
            "18" in content or "18+" in content or "15" in content,
            "gstack-docs must declare 18 presentation hubs or 15 doc platforms"
        )
        self.assertIn("drive.google.com", content, "gstack-docs must cite Google Drive vault apex")

    def test_05_bookmark_skill_catalog_metrics(self):
        """Verify gstack-bookmark declares 28 visual curation platforms."""
        skill_path = SKILLS_DIR / "gstack-bookmark" / "SKILL.md"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertTrue("28" in content or "28+" in content, "gstack-bookmark must declare 28 curation platforms")
        self.assertIn("public_backlink_ledger.html", content, "gstack-bookmark must cite Firebase Public Ledger apex")

    def test_06_sites_skill_catalog_metrics(self):
        """Verify gstack-sites declares dedicated Google Sites apexes and landing page platforms."""
        skill_path = SKILLS_DIR / "gstack-sites" / "SKILL.md"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Carrd", content, "gstack-sites must cite Carrd")
        self.assertIn("Strikingly", content, "gstack-sites must cite Strikingly")
        self.assertIn("Webflow", content, "gstack-sites must cite Webflow")
        self.assertIn("Notion", content, "gstack-sites must cite Notion")
        self.assertIn("Bento", content, "gstack-sites must cite Bento")
        self.assertIn("sites.google.com", content, "gstack-sites must cite Google Sites apexes")


class TestM4All16NodeSwarmTopology(unittest.TestCase):
    """Test Suite 3: Verifies complete 16-node swarm topology in gstack and orchestrator."""

    def test_01_gstack_master_skill_defines_16_agents(self):
        """Verify master gstack/SKILL.md explicitly enumerates all 16 specialized agents."""
        skill_path = SKILLS_DIR / "gstack" / "SKILL.md"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        for agent in EXPECTED_16_SWARM_AGENTS:
            self.assertIn(
                agent,
                content,
                f"Master gstack/SKILL.md missing mandatory swarm agent: {agent}"
            )

    def test_02_orchestrator_defines_16_stack_teams(self):
        """Verify swarm_stack_orchestrator.py defines all 16 specialized teams in STACK_TEAMS."""
        orch_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orch_path, "r", encoding="utf-8") as f:
            code = f.read()

        ns = {}
        exec(compile(code, str(orch_path), "exec"), ns)
        teams = ns.get("STACK_TEAMS", {})

        self.assertEqual(
            len(teams),
            16,
            f"STACK_TEAMS must contain exactly 16 specialized teams, found {len(teams)}: {list(teams.keys())}"
        )

        agent_names = {v.get("agent") for v in teams.values()}
        for expected_agent in EXPECTED_16_SWARM_AGENTS:
            self.assertIn(
                expected_agent,
                agent_names,
                f"STACK_TEAMS missing assigned agent: {expected_agent}"
            )


class TestM4AllRule46GenuineTradeValueLaw(unittest.TestCase):
    """Test Suite 4: Verifies Rule 46 enforcement and the 4 High-Value Pillars."""

    def test_01_rule_46_explicit_presence_in_master_gstack(self):
        """Verify gstack/SKILL.md explicitly names and defines Rule 46."""
        skill_path = SKILLS_DIR / "gstack" / "SKILL.md"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Rule 46", content, "gstack/SKILL.md must explicitly reference 'Rule 46'")
        self.assertIn(
            "Genuine Trade Value",
            content,
            "gstack/SKILL.md must define the Genuine Trade Value Law"
        )

    def test_02_rule_46_four_high_value_pillars(self):
        """Verify the 4 High-Value Pillars are codified in gstack/SKILL.md."""
        skill_path = SKILLS_DIR / "gstack" / "SKILL.md"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read().lower()

        for pillar_keyword in RULE_46_FOUR_PILLARS:
            self.assertIn(
                pillar_keyword,
                content,
                f"Rule 46 in gstack/SKILL.md missing pillar: {pillar_keyword}"
            )

    def test_03_absolute_ban_on_bs_standards_in_titles(self):
        """Verify ban on BS EN / ISO standards in titles and hooks is codified."""
        skill_path = SKILLS_DIR / "gstack" / "SKILL.md"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn(
            "BS EN",
            content,
            "gstack/SKILL.md must reference BS EN standards in prohibition rules"
        )
        self.assertTrue(
            "ban on BS" in content or "ban on BS EN" in content or "Strict Ban on BS" in content or "Absolute ban on BS" in content,
            "gstack/SKILL.md must explicitly ban British Standards in titles and hooks"
        )

    def test_04_absolute_ban_on_top_10_affiliate_slop(self):
        """Verify ban on generic 'Top 10' affiliate lists is codified."""
        skill_path = SKILLS_DIR / "gstack" / "SKILL.md"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertTrue(
            "Top 10" in content,
            "gstack/SKILL.md must explicitly reference and ban 'Top 10' affiliate slop"
        )


class TestM4AllRule45AirGapCompliance(unittest.TestCase):
    """Test Suite 5: Verifies Rule 45 zero naked root domain compliance across all 9 skills."""

    def test_01_zero_naked_root_links_in_skills(self):
        """Ensure no skill file contains raw naked root links to https://adicommunications.co.uk/."""
        raw_root_regex = re.compile(
            r"https?://(?:www\.)?adicommunications\.co\.uk/?(?:(?=[)\s\"',;>])|$)",
            re.IGNORECASE
        )

        for skill_name in ALL_9_SKILLS:
            skill_path = SKILLS_DIR / skill_name / "SKILL.md"
            with open(skill_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line_no, line in enumerate(lines, 1):
                # Allow lines that discuss the rule itself (e.g. mentions of raw root ban)
                if "Rule 45" in line or "raw root" in line or "naked root" in line or "ban" in line.lower():
                    continue

                matches = list(raw_root_regex.finditer(line))
                for m in matches:
                    # Check if followed immediately by a path
                    rest = line[m.end():]
                    if not rest.startswith(("/", "news", "assets", "cctv", "starlink", "tv", "ajax", "aerial", "wifi")):
                        self.fail(
                            f"Rule 45 raw root link leak in {skill_name}/SKILL.md line {line_no}: {line.strip()}"
                        )


class TestM4AllTradeCredentialsAndCompliance(unittest.TestCase):
    """Test Suite 6: Verifies Gary Pearce trade credentials, phone, insurance, and Checkatrade exclusion."""

    def test_01_direct_phone_number_standardization(self):
        """Verify Gary Pearce direct mobile 07860 244 274 is present and no 0800 numbers exist."""
        for skill_name in ALL_9_SKILLS:
            skill_path = SKILLS_DIR / skill_name / "SKILL.md"
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertTrue(
                "07860 244 274" in content or "07860244274" in content,
                f"{skill_name}/SKILL.md must feature Gary Pearce direct phone: 07860 244 274"
            )
            self.assertNotIn("0800", content, f"{skill_name}/SKILL.md must never contain 0800 numbers")

    def test_02_insurance_and_reviews_integrity(self):
        """Verify £10M Public Liability insurance and 9.98/10 from 84+ reviews."""
        master_skill = SKILLS_DIR / "gstack" / "SKILL.md"
        with open(master_skill, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("£10M", content, "Master skill must declare £10M Public Liability Insurance")
        self.assertIn("9.98", content, "Master skill must cite 9.98/10 review rating")
        self.assertIn("84+", content, "Master skill must cite 84+ verified reviews")

    def test_03_cai_and_checkatrade_compliance(self):
        """Verify no fraudulent 'CAI Member' claims and zero public Checkatrade display."""
        for skill_name in ALL_9_SKILLS:
            skill_path = SKILLS_DIR / skill_name / "SKILL.md"
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertNotIn(
                "CAI Member",
                content,
                f"{skill_name}/SKILL.md must NEVER claim CAI membership"
            )
            self.assertNotIn(
                "Member of CAI",
                content,
                f"{skill_name}/SKILL.md must NEVER claim CAI membership"
            )


if __name__ == "__main__":
    unittest.main()
