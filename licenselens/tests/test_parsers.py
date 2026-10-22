import tempfile
import unittest
from pathlib import Path

from licenselens.parsers import parse_package_json, parse_pyproject, parse_requirements


class ParserTests(unittest.TestCase):
    def test_requirements(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "requirements.txt"
            path.write_text("requests==2.32.3\n# comment\nnumpy>=2.1\n", encoding="utf-8")
            self.assertEqual(parse_requirements(path), [("requests", "2.32.3"), ("numpy", "2.1")])

    def test_pyproject(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "pyproject.toml"
            path.write_text('[project]\ndependencies = ["requests==2.32.3", "numpy>=2.1"]\n', encoding="utf-8")
            parsed = parse_pyproject(path)
            self.assertIn(("requests", "2.32.3"), parsed)
            self.assertIn(("numpy", "2.1"), parsed)

    def test_package_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "package.json"
            path.write_text('{"dependencies": {"react": "^18.0.0"}}', encoding="utf-8")
            self.assertEqual(parse_package_json(path), [("react", "^18.0.0")])


if __name__ == "__main__":
    unittest.main()
