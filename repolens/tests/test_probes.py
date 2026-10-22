import tempfile
import unittest
from pathlib import Path

from repolens.probes import run_probes


class ProbeTests(unittest.TestCase):
    def test_syntax_probe_pass(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "demo-llm-app"
        probes = run_probes(root, execute=False)
        self.assertEqual(len(probes), 1)
        self.assertEqual(probes[0].name, "python-syntax")
        self.assertEqual(probes[0].status, "pass")

    def test_syntax_probe_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bad.py").write_text("def broken(:\n    pass\n", encoding="utf-8")
            probes = run_probes(root, execute=False)
            self.assertEqual(probes[0].status, "fail")
            self.assertIn("bad.py", probes[0].stdout)


if __name__ == "__main__":
    unittest.main()
