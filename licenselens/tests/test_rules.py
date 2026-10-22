import unittest

from licenselens.models import Dependency, UsageMode
from licenselens.rules import analyze_dependencies


class RuleTests(unittest.TestCase):
    def test_agpl_saas_is_high_severity(self):
        deps = [Dependency("agpl-lib", "1.0", "AGPL-3.0-only", "requirements.txt")]
        findings = analyze_dependencies(deps, UsageMode.SAAS, "MIT")
        self.assertTrue(any(f.rule == "network-copyleft" and f.severity == "high" for f in findings))

    def test_mit_internal_has_no_high_findings(self):
        deps = [Dependency("requests", "2.32.3", "Apache-2.0", "requirements.txt")]
        findings = analyze_dependencies(deps, UsageMode.INTERNAL, "MIT")
        self.assertFalse(any(f.severity == "high" for f in findings))

    def test_unknown_license_requires_manual_review(self):
        deps = [Dependency("mystery", "0.1", "UNKNOWN", "requirements.txt")]
        findings = analyze_dependencies(deps, UsageMode.INTERNAL, "MIT")
        self.assertTrue(any(f.rule == "unknown-or-proprietary-license" for f in findings))


if __name__ == "__main__":
    unittest.main()
