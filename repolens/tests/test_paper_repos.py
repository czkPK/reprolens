import json
import unittest
from pathlib import Path


class PaperRepoManifestTests(unittest.TestCase):
    def test_manifest_covers_diverse_paper_domains(self):
        path = Path(__file__).resolve().parents[1] / "benchmark" / "paper_repos.json"
        items = json.loads(path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(items), 7)
        self.assertGreaterEqual(len({item["domain"] for item in items}), 7)
        for item in items:
            self.assertTrue(item["paper_url"].startswith("https://arxiv.org/abs/"))
            self.assertTrue(item["repo"].startswith("https://github.com/"))


if __name__ == "__main__":
    unittest.main()
