#!/usr/bin/env python3
"""
tests/e2e/test_tier3_combinations.py
Alias and wrapper for tests/e2e/test_tier3_cross_feature.py
"""

from tests.e2e.test_tier3_cross_feature import TestTier3CrossFeature

__all__ = ["TestTier3CrossFeature"]

if __name__ == "__main__":
    import unittest
    unittest.main(verbosity=2)
