import unittest
from datetime import datetime, timezone
from pathlib import Path

from repolens.llm import offline_explanation
from repolens.models import AuditResult
from repolens.probes import run_probes
from repolens.remediation import plan_remediations
from repolens.rules import build_findings, evaluate_criteria
from repolens.scanner import scan_repo
from repolens.scoring import readiness_label, score_dimensions, total_score


class LLMTests(unittest.TestCase):
    def test_offline_explanation_is_evidence_bounded(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "demo-llm-app"
        snapshot = scan_repo(root)
        criteria = evaluate_criteria(snapshot)
        findings = build_findings(criteria)
        score = total_score(criteria)
        result = AuditResult(
            repo_path=str(root),
            generated_at=datetime.now(timezone.utc).isoformat(),
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
        text = offline_explanation(result)
        self.assertIn("ReproLens Explanation", text)
        self.assertIn("证据", text)
        self.assertIn("Evidence Missing", text)


if __name__ == "__main__":
    unittest.main()
