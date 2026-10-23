#!/usr/bin/env python3
"""
tests/test_challenger_m4all_orchestrator.py
============================================
Adversarial Challenger Test Suite for Milestone M4-ALL:
Empirical validation of swarm_stack_orchestrator.py 16-team architecture,
CLI dispatch interfaces, status reporting, error handling, and hostile inputs.
"""

import os
import sys
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

class TestChallengerM4AllOrchestrator(unittest.TestCase):
    """Adversarial stress and verification tests for swarm_stack_orchestrator.py."""

    @classmethod
    def setUpClass(cls):
        cls.orch_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        cls.assertTrue(cls.orch_path.exists(), f"Orchestrator not found at {cls.orch_path}")
        with open(cls.orch_path, "r", encoding="utf-8") as f:
            cls.code = f.read()

        cls.ns = {}
        exec(compile(cls.code, str(cls.orch_path), "exec"), cls.ns)
        cls.stack_teams = cls.ns.get("STACK_TEAMS", {})

    # =========================================================================
    # Task 1: 16-Team Topology and STACK_TEAMS Invariants
    # =========================================================================

    def test_01_stack_teams_exact_count_16(self):
        """Assert STACK_TEAMS contains exactly 16 teams."""
        self.assertEqual(
            len(self.stack_teams), 16,
            f"Expected exactly 16 STACK_TEAMS, found {len(self.stack_teams)}: {list(self.stack_teams.keys())}"
        )

    def test_02_stack_teams_structure_and_schema(self):
        """Verify each of the 16 teams defines agent, apex, description, and script."""
        required_keys = {"agent", "apex", "description", "script"}
        for team_name, info in self.stack_teams.items():
            with self.subTest(team=team_name):
                self.assertIsInstance(info, dict, f"Team '{team_name}' must be a dictionary")
                missing = required_keys - set(info.keys())
                self.assertEqual(len(missing), 0, f"Team '{team_name}' missing keys: {missing}")
                self.assertTrue(info["agent"].strip(), f"Team '{team_name}' has empty agent")
                self.assertTrue(info["apex"].startswith(("https://", "http://")), f"Team '{team_name}' invalid apex: {info['apex']}")
                self.assertTrue(info["description"].strip(), f"Team '{team_name}' has empty description")
                self.assertTrue(info["script"].strip(), f"Team '{team_name}' has empty script")

    def test_03_all_16_agents_unique(self):
        """Verify all 16 teams map to 16 unique subagent identifiers."""
        agents = [info["agent"] for info in self.stack_teams.values()]
        self.assertEqual(len(agents), 16)
        self.assertEqual(len(set(agents)), 16, f"Duplicate agents found: {agents}")

    # =========================================================================
    # Task 2: CLI Invocations and Status Reporting
    # =========================================================================

    def test_04_cli_status_subcommand(self):
        """Execute 'python swarm_stack_orchestrator.py status' and assert exit 0 with all 16 teams."""
        cmd = [sys.executable, str(self.orch_path), "status"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(res.returncode, 0, f"Command failed: {res.stderr}")
        self.assertIn("[STATUS PASS] All 16 Swarm Teams cataloged.", res.stdout)
        for team_name in self.stack_teams.keys():
            self.assertIn(team_name.upper(), res.stdout)

    def test_05_cli_status_flag(self):
        """Execute 'python swarm_stack_orchestrator.py --status' and assert exit 0 with all 16 teams."""
        cmd = [sys.executable, str(self.orch_path), "--status"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(res.returncode, 0, f"Command failed: {res.stderr}")
        self.assertIn("[STATUS PASS] All 16 Swarm Teams cataloged.", res.stdout)
        for team_name in self.stack_teams.keys():
            self.assertIn(team_name.upper(), res.stdout)

    def test_06_cli_status_with_all_16_individual_stack_flags(self):
        """Verify '--status --stack <team>' succeeds with exit 0 for each of the 16 teams."""
        for team_name in self.stack_teams.keys():
            with self.subTest(team=team_name):
                cmd = [sys.executable, str(self.orch_path), "--status", "--stack", team_name]
                res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
                self.assertEqual(res.returncode, 0, f"--status --stack {team_name} failed: {res.stderr}")
                self.assertIn("[STATUS PASS] All 16 Swarm Teams cataloged.", res.stdout)

    # =========================================================================
    # Task 3: Error Handling & Hostile Input Validation
    # =========================================================================

    def test_07_invalid_stack_non_existent_team(self):
        """Pass invalid --stack non_existent_team and assert clean exit code 2 without unhandled traceback."""
        cmd = [sys.executable, str(self.orch_path), "--stack", "non_existent_team"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(res.returncode, 2, f"Expected exit code 2, got {res.returncode}")
        self.assertIn("invalid choice: 'non_existent_team'", res.stderr)
        self.assertNotIn("Traceback (most recent call last):", res.stderr)

    def test_08_invalid_stack_suffixed_names(self):
        """Pass invalid suffixed team names like citations_team and assert clean exit code 2."""
        for invalid_name in ["citations_team", "citadel_team", "verifier_team", "sites_team"]:
            with self.subTest(name=invalid_name):
                cmd = [sys.executable, str(self.orch_path), "--stack", invalid_name]
                res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
                self.assertEqual(res.returncode, 2, f"Expected exit code 2, got {res.returncode}")
                self.assertIn(f"invalid choice: '{invalid_name}'", res.stderr)
                self.assertNotIn("Traceback (most recent call last):", res.stderr)

    def test_09_invalid_subcommand(self):
        """Pass invalid subcommand and assert clean exit code 2 without unhandled traceback."""
        cmd = [sys.executable, str(self.orch_path), "invalid_command_xyz"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(res.returncode, 2, f"Expected exit code 2, got {res.returncode}")
        self.assertIn("invalid choice: 'invalid_command_xyz'", res.stderr)
        self.assertNotIn("Traceback (most recent call last):", res.stderr)

    def test_10_unrecognized_argument(self):
        """Pass unrecognized argument --unknown-flag and assert clean exit code 2."""
        cmd = [sys.executable, str(self.orch_path), "--unknown-flag"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(res.returncode, 2, f"Expected exit code 2, got {res.returncode}")
        self.assertIn("unrecognized arguments", res.stderr)
        self.assertNotIn("Traceback (most recent call last):", res.stderr)

    # =========================================================================
    # Task 4: Operational Subcommands (sync, audit)
    # =========================================================================

    def test_11_subcommand_audit(self):
        """Execute 'python swarm_stack_orchestrator.py audit' and assert exit 0."""
        cmd = [sys.executable, str(self.orch_path), "audit"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(res.returncode, 0, f"Audit failed: {res.stderr}")
        self.assertIn("[AUDIT PASS]", res.stdout)

    def test_12_subcommand_sync(self):
        """Execute 'python swarm_stack_orchestrator.py sync' and assert exit 0."""
        cmd = [sys.executable, str(self.orch_path), "sync"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(res.returncode, 0, f"Sync failed: {res.stderr}")
        self.assertIn("[SYNC PASS]", res.stdout)


if __name__ == "__main__":
    unittest.main()
