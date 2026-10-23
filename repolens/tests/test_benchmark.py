import unittest
from pathlib import Path

from repolens.benchmark import DEFAULT_CASES, run_case


class BenchmarkTests(unittest.TestCase):
    def test_fixture_expectations(self):
        base = Path(__file__).resolve().parents[1]
        results = [run_case(case, base) for case in DEFAULT_CASES]
        self.assertEqual(sum(item.exact_matches for item in results), sum(item.total_expectations for item in results))


if __name__ == "__main__":
    unittest.main()
