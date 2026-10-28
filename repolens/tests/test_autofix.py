import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from repolens.autofix import generate_autofix
from repolens.models import AuditResult
from repolens.probes import run_probes
from repolens.remediation import plan_remediations
from repolens.rules import build_findings, evaluate_criteria
from repolens.scanner import scan_repo
from repolens.scoring import readiness_label, score_dimensions, total_score


class AutoFixTests(unittest.TestCase):
    def test_autofix_generates_proposal_and_improves_score(self):
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
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "autofix"
            report = generate_autofix(root, result, out)
            self.assertGreater(report["after_score"], report["before_score"])
            self.assertTrue(report["original_unchanged"])
            self.assertEqual(len(report["original_fingerprint"]), 64)
            self.assertTrue((out / "autofix.json").exists())
            self.assertTrue((out.parent / "autofix.html").exists())
            self.assertTrue((out / "FIX_PROPOSAL.md").exists())
            self.assertTrue((out / "proposal" / "Dockerfile").exists())
            self.assertTrue((out / "proposal" / "prompts" / "prompt_metadata.json").exists())
            self.assertTrue((out / "proposal" / "tests" / "test_smoke.py").exists())
            autofix_html = (out.parent / "autofix.html").read_text(encoding="utf-8")
            self.assertIn("原仓库未被修改", autofix_html)
            self.assertIn("autofix/proposal/Dockerfile", autofix_html)
            self.assertIn("AutoFix 前后评分对比", autofix_html)
            self.assertIn("compare-bar before", autofix_html)
            self.assertIn("compare-bar after", autofix_html)


if __name__ == "__main__":
    unittest.main()
