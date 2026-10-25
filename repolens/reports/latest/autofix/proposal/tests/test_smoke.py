import unittest
from pathlib import Path


class SmokeTest(unittest.TestCase):
    def test_project_files_exist(self):
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "README.md").exists())


if __name__ == "__main__":
    unittest.main()
