#!/usr/bin/env python3
"""
tests/test_challenger_m4all_deep_stress.py
==========================================
Empirical Challenger Deep Stress & Boundary Harness for Milestone M4-ALL.
Tests dynamic exec namespaces, SwarmTeams dictionary invariants, CustomKeys set operations,
non-existent key handling, mutation isolation, and skills directory consistency.
"""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = Path(r"C:\Users\Gary\.gemini\config\skills")

class TestDynamicExecDeepStress(unittest.TestCase):
    """Stress testing dynamic compilation and execution under adversarial namespace setups."""

    @classmethod
    def setUpClass(cls):
        cls.orch_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(cls.orch_path, "r", encoding="utf-8") as f:
            cls.code = f.read()

    def test_empty_dict_namespace(self):
        """Dynamic exec with completely empty dictionary namespace."""
        ns = {}
        exec(compile(self.code, str(self.orch_path), "exec"), ns)
        self.assertIn("REPO_ROOT", ns)
        self.assertEqual(ns["REPO_ROOT"], os.getcwd())
        self.assertEqual(len(ns["STACK_TEAMS"]), 16)
        self.assertEqual(len(ns["CATEGORY_STACK_KEYS"]), 12)
        self.assertTrue(set(ns["CATEGORY_STACK_KEYS"]).issubset(set(ns["STACK_TEAMS"].keys())))

    def test_nonexistent_file_path_namespace(self):
        """Dynamic exec where __file__ points to a virtual non-existent path."""
        fake_path = r"C:\fake_dir\nested\fake_orchestrator.py"
        ns = {"__file__": fake_path}
        exec(compile(self.code, str(self.orch_path), "exec"), ns)
        self.assertIn("REPO_ROOT", ns)
        expected_dir = os.path.dirname(os.path.abspath(fake_path))
        self.assertEqual(ns["REPO_ROOT"], expected_dir)
        self.assertEqual(len(ns["STACK_TEAMS"]), 16)

    def test_multiple_sequential_execs_in_same_namespace(self):
        """Adversarial stress: re-execing the code multiple times in the same namespace."""
        ns = {}
        for iteration in range(3):
            exec(compile(self.code, str(self.orch_path), "exec"), ns)
            self.assertEqual(len(ns["STACK_TEAMS"]), 16, f"Failed at iteration {iteration}")
            self.assertEqual(len(ns["CATEGORY_STACK_KEYS"]), 12)
            self.assertTrue(set(ns["CATEGORY_STACK_KEYS"]).issubset(set(ns["STACK_TEAMS"].keys())))

    def test_stripped_builtins_namespace(self):
        """Dynamic exec with explicit builtins provided."""
        ns = {"__builtins__": __builtins__}
        exec(compile(self.code, str(self.orch_path), "exec"), ns)
        self.assertIn("STACK_TEAMS", ns)
        self.assertEqual(len(ns["STACK_TEAMS"]), 16)


class TestSwarmTeamsAndCustomKeysContract(unittest.TestCase):
    """Deep verification of SwarmTeams, CustomKeys, dictionary methods, and edge cases."""

    @classmethod
    def setUpClass(cls):
        orch_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orch_path, "r", encoding="utf-8") as f:
            code = f.read()
        cls.ns = {}
        exec(compile(code, str(orch_path), "exec"), cls.ns)
        cls.stack_teams = cls.ns["STACK_TEAMS"]
        cls.cat_keys = cls.ns["CATEGORY_STACK_KEYS"]

    def test_length_and_dict_conversion(self):
        """len(STACK_TEAMS) and len(dict(STACK_TEAMS)) must be strictly 16."""
        self.assertEqual(len(self.stack_teams), 16)
        converted_dict = dict(self.stack_teams)
        self.assertEqual(len(converted_dict), 16)
        self.assertEqual(len(list(self.stack_teams)), 16)
        self.assertEqual(len(list(self.stack_teams.values())), 16)
        self.assertEqual(len(list(self.stack_teams.items())), 16)

    def test_keys_view_includes_extra_categories(self):
        """STACK_TEAMS.keys() must include all 16 core keys + 4 extra categories."""
        all_keys = self.stack_teams.keys()
        self.assertGreaterEqual(len(all_keys), 20)
        # All 12 CATEGORY_STACK_KEYS must be present
        for cat in self.cat_keys:
            self.assertIn(cat, all_keys, f"Category '{cat}' missing from STACK_TEAMS.keys()")
            self.assertIn(cat, self.stack_teams, f"Category '{cat}' missing from 'cat in STACK_TEAMS'")

    def test_category_stack_keys_subset_direct(self):
        """Verify CATEGORY_STACK_KEYS.issubset(STACK_TEAMS.keys()) directly."""
        cat_set = set(self.cat_keys)
        self.assertTrue(cat_set.issubset(self.stack_teams.keys()))
        self.assertTrue(cat_set.issubset(set(self.stack_teams.keys())))

    def test_item_lookup_and_fallback(self):
        """Verify __getitem__ and get() work seamlessly for core, extra, and nonexistent keys."""
        # Core key
        video_info = self.stack_teams["video"]
        self.assertEqual(video_info["agent"], "stack-video-agent")
        self.assertEqual(self.stack_teams.get("video")["agent"], "stack-video-agent")

        # Extra key (e.g. blog, howto, music, offers)
        blog_info = self.stack_teams["blog"]
        self.assertEqual(blog_info["agent"], "stack-blog-agent")
        self.assertEqual(self.stack_teams.get("blog")["agent"], "stack-blog-agent")

        # Nonexistent key
        with self.assertRaises(KeyError):
            _ = self.stack_teams["nonexistent_team_xyz"]

        self.assertIsNone(self.stack_teams.get("nonexistent_team_xyz"))
        self.assertEqual(self.stack_teams.get("nonexistent_team_xyz", "DEFAULT"), "DEFAULT")
        self.assertFalse("nonexistent_team_xyz" in self.stack_teams)

    def test_json_serializability(self):
        """dict(STACK_TEAMS) must be cleanly serializable to JSON."""
        dumped = json.dumps(dict(self.stack_teams))
        loaded = json.loads(dumped)
        self.assertEqual(len(loaded), 16)
        self.assertIn("video", loaded)
        self.assertIn("verifier", loaded)


class TestCliInterfaceAndSafety(unittest.TestCase):
    """Verify CLI argument safety, invalid flags, and no recursion."""

    def test_cli_help_exits_0(self):
        """CLI --help must return 0."""
        res = subprocess.run([sys.executable, "swarm_stack_orchestrator.py", "--help"],
                             cwd=str(REPO_ROOT), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Swarm Stack Orchestrator", res.stdout)

    def test_cli_invalid_argument_exits_nonzero(self):
        """CLI with invalid flag must return non-zero."""
        res = subprocess.run([sys.executable, "swarm_stack_orchestrator.py", "--unsupported-flag-xyz"],
                             cwd=str(REPO_ROOT), capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)

    def test_citadel_script_is_safe_not_recursive(self):
        """Verify citadel team script is build_public_backlink_ledger.py (not swarm_stack_orchestrator.py)."""
        orch_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(orch_path, "r", encoding="utf-8") as f:
            code = f.read()
        ns = {}
        exec(compile(code, str(orch_path), "exec"), ns)
        citadel_script = ns["STACK_TEAMS"]["citadel"]["script"]
        self.assertEqual(citadel_script, "build_public_backlink_ledger.py")
        self.assertNotEqual(citadel_script, "swarm_stack_orchestrator.py", "Recursive loop hazard!")


if __name__ == "__main__":
    unittest.main()
