import unittest
from pathlib import Path

from repolens.html_report import render_html
from repolens.models import AuditResult
from repolens.probes import run_probes
from repolens.remediation import plan_remediations
from repolens.rules import build_findings, evaluate_criteria
from repolens.scanner import scan_repo
from repolens.scoring import readiness_label, score_dimensions, total_score


class ReportTests(unittest.TestCase):
    def test_html_contains_score_and_sections(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "demo-llm-app"
        snapshot = scan_repo(root)
        criteria = evaluate_criteria(snapshot)
        findings = build_findings(criteria)
        score = total_score(criteria)
        result = AuditResult(
            repo_path=str(root),
            generated_at="test",
            total_score=score,
            readiness=readiness_label(score),
            dimensions=score_dimensions(criteria),
            criteria=criteria,
            findings=findings,
            remediations=plan_remediations(findings, criteria),
            evidence=snapshot.evidence,
            files_scanned=len(snapshot.files),
            probes=run_probes(root, execute=False),
        )
        html = render_html(result)
        self.assertIn("ReproLens Audit Report", html)
        self.assertIn("LLM 特有风险", html)
        self.assertIn("Execution Evidence", html)


if __name__ == "__main__":
    unittest.main()
