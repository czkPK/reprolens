import tempfile
import unittest
from pathlib import Path

from repolens.html_report import render_claims_html, render_html
from repolens.models import AuditResult
from repolens.probes import run_probes
from repolens.remediation import plan_remediations
from repolens.report import render_claims_markdown, write_outputs
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
        self.assertIn("Claim-Evidence Matrix", html)
        self.assertIn("Evidence coverage", html)
        self.assertIn("Evidence Appendix", html)
        self.assertIn('href="#evidence-E-', html)
        self.assertIn('title="requirements.txt:1', html)
        self.assertIn('class="criteria-table"', html)
        self.assertIn('class="evidence-id-list"', html)
        self.assertIn('class="evidence-table"', html)
        self.assertIn('class="evidence-scroll"', html)
        self.assertIn("width: 1280px", html)
        self.assertIn('class="evidence-path"', html)
        self.assertIn("flex-wrap: wrap", html)
        self.assertIn("overflow-wrap: anywhere", html)
        self.assertIn("sticky-scroll", html)
        self.assertIn("表格已固定首行和前两列", html)
        self.assertIn("Top 3 Priority Actions", html)
        self.assertIn("证据说明", html)
        self.assertIn("是否存在依赖清单", html)
        self.assertIn("LLM-01（是否记录模型/API 版本）", html)
        self.assertIn("MODEL-02（是否提供模型卡或版本说明）", html)
        self.assertIn("已验证", render_claims_markdown(result))
        claims_html = render_claims_html(result)
        self.assertIn("声明验证矩阵", claims_html)
        self.assertIn("README 声明", claims_html)
        self.assertIn("验证说明", claims_html)
        self.assertIn("configs/app.yaml:8", claims_html)
        self.assertIn("sticky-scroll", claims_html)
        self.assertIn('class="claim-table"', claims_html)
        self.assertIn("overflow:visible", claims_html)
        self.assertIn("box-sizing:border-box", claims_html)

    def test_write_outputs_creates_claim_files(self):
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
        with tempfile.TemporaryDirectory() as tmp:
            write_outputs(result, Path(tmp))
            self.assertTrue((Path(tmp) / "claims.json").exists())
            self.assertTrue((Path(tmp) / "claims.md").exists())
            self.assertTrue((Path(tmp) / "claims.html").exists())
            self.assertTrue((Path(tmp) / "badge.svg").exists())
            self.assertTrue((Path(tmp) / "badge.json").exists())
            self.assertIn("ReproLens", (Path(tmp) / "badge.svg").read_text(encoding="utf-8"))
            self.assertIn("Claim-Evidence Matrix", (Path(tmp) / "report.md").read_text(encoding="utf-8"))
            self.assertIn("声明验证矩阵", (Path(tmp) / "claims.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
