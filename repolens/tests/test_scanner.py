import tempfile
import unittest
from pathlib import Path

from repolens.scanner import scan_repo


class ScannerTests(unittest.TestCase):
    def test_demo_repo_flags(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "demo-ai-repo"
        snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("readme"))
        self.assertTrue(snapshot.has("deps"))
        self.assertTrue(snapshot.has("train_script"))
        self.assertTrue(snapshot.has("eval_script"))
        self.assertTrue(snapshot.has("install_instructions"))
        self.assertTrue(snapshot.has("run_instructions"))
        self.assertTrue(snapshot.has("data_mention"))
        self.assertTrue(snapshot.has("expected_results"))
        self.assertFalse(snapshot.has("seed"))
        self.assertTrue(snapshot.has("ml_project"))
        self.assertFalse(snapshot.has("llm_project"))

    def test_demo_llm_repo_flags(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "demo-llm-app"
        snapshot = scan_repo(root)
        self.assertTrue(snapshot.has("llm_project"))
        self.assertTrue(snapshot.has("rag_project"))
        self.assertTrue(snapshot.has("agent_project"))
        self.assertTrue(snapshot.has("model_provider"))
        self.assertTrue(snapshot.has("model_version"))
        self.assertTrue(snapshot.has("prompt_files"))
        self.assertTrue(snapshot.has("sampling_params"))
        self.assertTrue(snapshot.has("rag_index"))
        self.assertFalse(snapshot.has("prompt_version"))
        self.assertFalse(snapshot.has("agent_trace"))
        self.assertFalse(snapshot.has("eval_dataset"))

    def test_claim_extraction_skips_copyright_and_docs_boilerplate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "Copyright 2024 Example Team. All rights reserved.\n"
                "Full documentation can be found here: https://example.com/model\n"
                "```bash\n"
                "pip install example-package\n"
                "```\n"
                "The project supports benchmark reproduction with a fixed seed and evaluation dataset.\n",
                encoding="utf-8",
            )
            claims = [item.excerpt for item in scan_repo(root).evidence if item.kind == "claim"]
        self.assertEqual(len(claims), 1)
        self.assertIn("benchmark reproduction", claims[0])


if __name__ == "__main__":
    unittest.main()
