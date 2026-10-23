"""
tests/test_dynamic_exec_orchestrator.py
Adversarial stress test suite for dynamic compilation and exec() of swarm_stack_orchestrator.py
verifying zero NameError, REPO_ROOT resilience, and interface completeness.
"""

import os
import unittest
from pathlib import Path
from swarm_stack_orchestrator import CATEGORY_STACK_KEYS

REPO_ROOT = Path(__file__).resolve().parent.parent

class TestDynamicExecOrchestrator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.orch_path = REPO_ROOT / "swarm_stack_orchestrator.py"
        with open(cls.orch_path, "r", encoding="utf-8") as f:
            cls.code = f.read()

    def test_exec_with_empty_globals(self):
        """Adversarial test: namespace is an empty dict {} without __file__."""
        ns = {}
        compiled = compile(self.code, str(self.orch_path), "exec")
        exec(compiled, ns)

        self.assertIn("REPO_ROOT", ns)
        self.assertEqual(ns["REPO_ROOT"], os.getcwd())
        self.assertIn("STACK_TEAMS", ns)
        self.assertEqual(len(ns["STACK_TEAMS"]), 16)
        self.assertIn("CATEGORY_STACK_KEYS", ns)
        self.assertEqual(len(ns["CATEGORY_STACK_KEYS"]), len(CATEGORY_STACK_KEYS))
        self.assertTrue(set(ns["CATEGORY_STACK_KEYS"]).issubset(set(ns["STACK_TEAMS"].keys())))
        self.assertTrue(callable(ns.get("check_url_reachability")))

    def test_exec_with_none_file(self):
        """Adversarial test: namespace has __file__ explicitly set to None."""
        ns = {"__file__": None}
        compiled = compile(self.code, str(self.orch_path), "exec")
        exec(compiled, ns)

        self.assertIn("REPO_ROOT", ns)
        self.assertEqual(ns["REPO_ROOT"], os.getcwd())
        self.assertEqual(len(ns["STACK_TEAMS"]), 16)

    def test_exec_with_empty_string_file(self):
        """Adversarial test: namespace has __file__ set to empty string."""
        ns = {"__file__": ""}
        compiled = compile(self.code, str(self.orch_path), "exec")
        exec(compiled, ns)

        self.assertIn("REPO_ROOT", ns)
        self.assertEqual(ns["REPO_ROOT"], os.getcwd())

    def test_exec_with_custom_globals(self):
        """Adversarial test: arbitrary globals without __file__."""
        ns = {"__name__": "sandbox_module", "TEST_FLAG": True}
        compiled = compile(self.code, str(self.orch_path), "exec")
        exec(compiled, ns)

        self.assertIn("STACK_TEAMS", ns)
        teams = ns["STACK_TEAMS"]
        self.assertIn("verifier", teams)
        self.assertIn("ledger", teams)

    def test_exec_with_standard_file(self):
        """Standard execution: __file__ is a valid file path."""
        ns = {"__file__": str(self.orch_path)}
        compiled = compile(self.code, str(self.orch_path), "exec")
        exec(compiled, ns)

        self.assertEqual(Path(ns["REPO_ROOT"]).resolve(), REPO_ROOT.resolve())

if __name__ == "__main__":
    unittest.main()
