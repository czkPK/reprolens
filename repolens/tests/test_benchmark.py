import unittest
from pathlib import Path

from repolens.benchmark import run_benchmark


class BenchmarkTests(unittest.TestCase):
    def test_fixture_expectations(self):
        base = Path(__file__).resolve().parents[1]
        results = run_benchmark(base)
        self.assertEqual(sum(item.exact_matches for item in results), sum(item.total_expectations for item in results))


if __name__ == "__main__":
    unittest.main()
