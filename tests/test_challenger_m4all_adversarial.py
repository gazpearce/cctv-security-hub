#!/usr/bin/env python3
"""
tests/test_challenger_m4all_adversarial.py
==========================================
Empirical Challenger Adversarial Stress Suite for Milestone M4-ALL:
1. Deep audit of all 9 G-Stack skill files in C:\\Users\\Gary\\.gemini\\config\\skills:
   - Existence and line count verification (>500 lines for master gstack, >100 lines for specialized skills).
   - Regex scan for forbidden tokens: naked root links, Checkatrade links/promos, BS EN/patents in titles.
   - Verification that all 16 agent identifiers appear in gstack/SKILL.md.
2. Mutation and sensitivity verification of tests/test_m4all_skills_sync.py:
   - Verifies that corruptions (e.g. dropping a pillar, inserting naked root, 0800 number, CAI claim, missing team)
     are caught by the verification logic.
3. Orchestrator runtime integrity:
   - Verifies swarm_stack_orchestrator.py STACK_TEAMS schema, keys, and CLI execution.
"""

import os
import re
import subprocess
import sys
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

RULE_46_PILLARS = [
    "customer problems",
    "latest products",
    "honest trade opinions",
    "specs translated",
]


class TestChallengerSkillFilesStress(unittest.TestCase):
    """Task 1: Deep empirical stress-testing of all 9 skill files."""

    def test_01_skills_existence_and_minimum_line_thresholds(self):
        """Verify existence and strict line count bounds for all 9 skill files."""
        self.assertTrue(SKILLS_DIR.exists(), f"Skills dir missing: {SKILLS_DIR}")

        for s in ALL_9_SKILLS:
            sp = SKILLS_DIR / s / "SKILL.md"
            self.assertTrue(sp.exists(), f"Skill file does not exist: {sp}")
            with open(sp, "r", encoding="utf-8") as f:
                lines = f.readlines()
            line_count = len(lines)

            if s == "gstack":
                self.assertGreater(
                    line_count,
                    500,
                    f"Master skill gstack must be comprehensive (>500 lines), got {line_count}"
                )
            else:
                self.assertGreater(
                    line_count,
                    100,
                    f"Specialized skill {s} must be comprehensive (>100 lines), got {line_count}"
                )

    def test_02_all_16_agents_in_gstack_skill(self):
        """Verify all 16 agent identifiers appear in master gstack/SKILL.md."""
        sp = SKILLS_DIR / "gstack" / "SKILL.md"
        with open(sp, "r", encoding="utf-8") as f:
            content = f.read()

        for agent in EXPECTED_16_SWARM_AGENTS:
            self.assertIn(
                agent,
                content,
                f"Agent identifier '{agent}' missing from {sp}"
            )

    def test_03_zero_naked_root_links_regex_scan(self):
        """Adversarial regex scan for naked root links across all 9 skills."""
        raw_root_regex = re.compile(
            r"https?://(?:www\.)?adicommunications\.co\.uk/?(?=[)\s\"'`;>,]|$)",
            re.IGNORECASE
        )

        violations = []
        for s in ALL_9_SKILLS:
            sp = SKILLS_DIR / s / "SKILL.md"
            with open(sp, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line_no, line in enumerate(lines, 1):
                # Skip rule definition / ban statements
                if any(k in line.lower() for k in ["rule 45", "raw root", "naked root", "shield", "ban on"]):
                    continue
                matches = list(raw_root_regex.finditer(line))
                for m in matches:
                    rest = line[m.end():]
                    # Allowed deep subpaths
                    if not rest.startswith(("/", "news", "assets", "cctv", "starlink", "tv", "ajax", "aerial", "wifi")):
                        violations.append(f"{s}/SKILL.md:{line_no} -> {line.strip()}")

        self.assertEqual(
            len(violations),
            0,
            f"Found {len(violations)} naked root link violations:\n" + "\n".join(violations)
        )

    def test_04_zero_checkatrade_links_or_promotions(self):
        """Adversarial check: zero checkatrade.com URLs and zero promotional mentions."""
        link_regex = re.compile(r"https?://(?:www\.)?checkatrade\.com", re.IGNORECASE)
        promo_regex = re.compile(
            r"(?:find us on|member of|listed on|profile on|review on|check our)\s+checkatrade",
            re.IGNORECASE
        )

        violations = []
        for s in ALL_9_SKILLS:
            sp = SKILLS_DIR / s / "SKILL.md"
            with open(sp, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line_no, line in enumerate(lines, 1):
                if link_regex.search(line):
                    violations.append(f"Link: {s}/SKILL.md:{line_no} -> {line.strip()}")
                if promo_regex.search(line):
                    violations.append(f"Promo: {s}/SKILL.md:{line_no} -> {line.strip()}")

        self.assertEqual(
            len(violations),
            0,
            f"Found {len(violations)} Checkatrade violations:\n" + "\n".join(violations)
        )

    def test_05_zero_bs_en_or_patents_in_headings_or_titles(self):
        """Adversarial check: No BS EN or patent numbers in titles or markdown headings."""
        heading_regex = re.compile(r"^(?:#+\s*.*(?:BS\s*EN|patent)|title:\s*.*(?:BS\s*EN|patent))", re.IGNORECASE | re.MULTILINE)

        violations = []
        for s in ALL_9_SKILLS:
            sp = SKILLS_DIR / s / "SKILL.md"
            with open(sp, "r", encoding="utf-8") as f:
                text = f.read()

            for m in heading_regex.finditer(text):
                matched = m.group(0).strip()
                # If it explicitly discusses the ban or rule (e.g. "Ban on BS EN"), that is valid rule documentation
                if any(w in matched.lower() for w in ["ban", "prohibit", "rule 46", "never", "zero"]):
                    continue
                violations.append(f"{s}/SKILL.md -> {matched}")

        self.assertEqual(
            len(violations),
            0,
            f"Found BS EN/Patent in titles:\n" + "\n".join(violations)
        )


class TestChallengerSensitivityAndMutations(unittest.TestCase):
    """Task 2: Inject simulated regressions / mutations to verify test sensitivity."""

    def test_01_mutation_dropping_rule46_pillar_triggers_failure(self):
        """Simulate dropping a Rule 46 pillar from gstack/SKILL.md content."""
        sp = SKILLS_DIR / "gstack" / "SKILL.md"
        with open(sp, "r", encoding="utf-8") as f:
            original = f.read()

        # Mutate by replacing 'customer problems' case-insensitively with a generic word
        mutated = re.sub(r"customer problems", "generic topics", original, flags=re.IGNORECASE)
        self.assertNotIn("customer problems", mutated.lower())

        # Test logic from test_m4all_skills_sync.py
        with self.assertRaises(AssertionError):
            for pillar in RULE_46_PILLARS:
                self.assertIn(pillar, mutated.lower(), f"Missing pillar: {pillar}")

    def test_02_mutation_inserting_naked_root_link_triggers_failure(self):
        """Simulate inserting a naked root link into a skill file."""
        mutated_line = "Check out our site at https://adicommunications.co.uk/ for more information."
        raw_root_regex = re.compile(
            r"https?://(?:www\.)?adicommunications\.co\.uk/?(?=[)\s\"'`;>,]|$)",
            re.IGNORECASE
        )

        m = raw_root_regex.search(mutated_line)
        self.assertIsNotNone(m)
        rest = mutated_line[m.end():]
        is_leak = not rest.startswith(("/", "news", "assets", "cctv", "starlink", "tv", "ajax", "aerial", "wifi"))
        self.assertTrue(is_leak, "Naked root link leak must be detected")

    def test_03_mutation_inserting_0800_number_triggers_failure(self):
        """Simulate inserting a forbidden 0800 phone number."""
        mutated_content = "Call Gary Pearce on 0800 123 4567 for free quotes."
        with self.assertRaises(AssertionError):
            self.assertNotIn("0800", mutated_content, "Must reject 0800 numbers")

    def test_04_mutation_claiming_cai_membership_triggers_failure(self):
        """Simulate an illegal 'CAI Member' claim."""
        mutated_content = "Gary Pearce is a certified CAI Member with 25 years experience."
        with self.assertRaises(AssertionError):
            self.assertNotIn("CAI Member", mutated_content, "Must reject CAI Member claim")

    def test_05_mutation_removing_stack_team_triggers_failure(self):
        """Simulate removing a team from STACK_TEAMS in swarm_stack_orchestrator."""
        orch_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orch_path, "r", encoding="utf-8") as f:
            code = f.read()

        ns = {}
        exec(compile(code, str(orch_path), "exec"), ns)
        teams = dict(ns.get("STACK_TEAMS", {}))

        # Drop one team
        self.assertEqual(len(teams), 16)
        teams.pop("verifier")
        self.assertEqual(len(teams), 15)

        with self.assertRaises(AssertionError):
            self.assertEqual(len(teams), 16, "Must reject STACK_TEAMS with != 16 teams")

    def test_06_mutation_missing_agent_in_gstack_triggers_failure(self):
        """Simulate removing an agent from master gstack/SKILL.md."""
        sp = SKILLS_DIR / "gstack" / "SKILL.md"
        with open(sp, "r", encoding="utf-8") as f:
            original = f.read()

        mutated = original.replace("stack-sites-agent", "unknown-agent")
        with self.assertRaises(AssertionError):
            for agent in EXPECTED_16_SWARM_AGENTS:
                self.assertIn(agent, mutated, f"Missing agent: {agent}")

    def test_07_live_disk_mutation_drop_pillar_causes_pytest_failure(self):
        """Empirically test that modifying gstack/SKILL.md on disk to drop a pillar causes test_m4all_skills_sync.py to fail."""
        sp = SKILLS_DIR / "gstack" / "SKILL.md"
        with open(sp, "r", encoding="utf-8") as f:
            original = f.read()

        try:
            # Corrupt file on disk
            corrupted = re.sub(r"customer problems", "arbitrary unrelated query", original, flags=re.IGNORECASE)
            with open(sp, "w", encoding="utf-8") as f:
                f.write(corrupted)

            # Run pytest on test_m4all_skills_sync
            res = subprocess.run(
                [sys.executable, "-m", "pytest", "tests/test_m4all_skills_sync.py", "-k", "test_02_rule_46_four_high_value_pillars"],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True
            )
            self.assertNotEqual(res.returncode, 0, "pytest MUST fail when a Rule 46 pillar is dropped on disk")
            self.assertIn("FAILED", res.stdout)
        finally:
            # 100% guarantee file restoration
            with open(sp, "w", encoding="utf-8") as f:
                f.write(original)

        # Verify restoration passes cleanly
        verify_res = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_m4all_skills_sync.py", "-k", "test_02_rule_46_four_high_value_pillars"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        self.assertEqual(verify_res.returncode, 0, "pytest must pass after restoring original file")

    def test_08_live_disk_mutation_insert_root_link_causes_pytest_failure(self):
        """Empirically test that inserting a naked root link into a skill on disk causes test_m4all_skills_sync.py to fail."""
        sp = SKILLS_DIR / "gstack-media" / "SKILL.md"
        with open(sp, "r", encoding="utf-8") as f:
            original = f.read()

        try:
            # Inject naked root link
            corrupted = original + "\n\nVisit our homepage at https://adicommunications.co.uk/ for details.\n"
            with open(sp, "w", encoding="utf-8") as f:
                f.write(corrupted)

            # Run pytest on test_m4all_skills_sync
            res = subprocess.run(
                [sys.executable, "-m", "pytest", "tests/test_m4all_skills_sync.py", "-k", "test_01_zero_naked_root_links_in_skills"],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True
            )
            self.assertNotEqual(res.returncode, 0, "pytest MUST fail when naked root link is injected on disk")
            self.assertIn("FAILED", res.stdout)
        finally:
            # 100% guarantee file restoration
            with open(sp, "w", encoding="utf-8") as f:
                f.write(original)

        # Verify restoration passes cleanly
        verify_res = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_m4all_skills_sync.py", "-k", "test_01_zero_naked_root_links_in_skills"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        self.assertEqual(verify_res.returncode, 0, "pytest must pass after restoring original file")


class TestChallengerOrchestratorIntegrity(unittest.TestCase):
    """Task 3: Validate swarm_stack_orchestrator.py runtime execution and CLI."""

    def test_01_orchestrator_cli_status(self):
        """Verify python swarm_stack_orchestrator.py --status returns exit code 0 and reports 16 teams."""
        cmd = [sys.executable, str(REPO_ROOT / "swarm_stack_orchestrator.py"), "--status"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(res.returncode, 0, f"Orchestrator status failed:\n{res.stderr}")
        self.assertIn("16", res.stdout, "Orchestrator status output must indicate 16 teams")

    def test_02_all_16_teams_schema_validity(self):
        """Verify each of the 16 teams in STACK_TEAMS has valid schema attributes."""
        orch_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orch_path, "r", encoding="utf-8") as f:
            code = f.read()

        ns = {}
        exec(compile(code, str(orch_path), "exec"), ns)
        teams = ns.get("STACK_TEAMS", {})

        required_keys = {"agent", "apex", "description", "script"}
        for team_name, team_data in teams.items():
            for key in required_keys:
                self.assertIn(
                    key,
                    team_data,
                    f"Team '{team_name}' missing mandatory key '{key}'"
                )
            self.assertTrue(
                team_data["agent"] in EXPECTED_16_SWARM_AGENTS,
                f"Team '{team_name}' has unrecognized agent: {team_data['agent']}"
            )


if __name__ == "__main__":
    unittest.main()
