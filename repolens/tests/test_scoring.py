import unittest
from pathlib import Path

from repolens.remediation import plan_remediations
from repolens.rules import build_findings, evaluate_criteria
from repolens.scanner import scan_repo
from repolens.scoring import readiness_label, score_dimensions, total_score


class ScoringTests(unittest.TestCase):
    def test_demo_repo_score_and_findings(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "demo-ai-repo"
        snapshot = scan_repo(root)
        criteria = evaluate_criteria(snapshot)
        findings = build_findings(criteria)
        remediations = plan_remediations(findings, criteria)
        dimensions = score_dimensions(criteria)
        score = total_score(criteria)

        self.assertGreater(len(criteria), 10)
        self.assertGreater(len(findings), 0)
        self.assertGreater(len(remediations), 0)
        self.assertTrue(0 <= score <= 100)
        self.assertIn(readiness_label(score), {"Ready", "Partially Ready", "At Risk", "Not Ready"})
        self.assertTrue(any(d.max_points > 0 for d in dimensions))
        self.assertTrue(any(item.id == "EXP-03" and item.status == "missing" for item in criteria))

    def test_prompt_check_not_applicable_for_non_llm_repo(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "demo-ai-repo"
        snapshot = scan_repo(root)
        criteria = evaluate_criteria(snapshot)
        prompt = next(item for item in criteria if item.id == "LLM-02")
        self.assertFalse(prompt.applicable)


if __name__ == "__main__":
    unittest.main()

