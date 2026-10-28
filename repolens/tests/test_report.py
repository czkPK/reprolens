import tempfile
import unittest
from dataclasses import replace
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
        self.assertIn('id="visual-overview"', html)
        self.assertIn("radar-svg", html)
        self.assertIn("donut", html)
        self.assertIn("证据覆盖率", html)
        self.assertIn("Evidence Appendix（证据附录）", html)
        self.assertIn("Evidence Overview（证据总览）", html)
        self.assertIn("Top 3 Priority Actions（三项优先整改行动）", html)
        self.assertIn("Dimension Scores（维度评分）", html)
        self.assertIn("Findings（问题发现）", html)
        self.assertIn("Execution Evidence（执行证据）", html)
        self.assertIn("Minimal Remediation Plan（最小整改计划）", html)
        self.assertIn("Scope and Limitations（适用范围与限制）", html)
        self.assertIn("中文翻译：", html)
        self.assertIn("简单解释：", html)
        self.assertIn('id="evidence"', html)
        self.assertIn('href="#evidence-E-', html)
        self.assertIn("requirements.txt:1", html)
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
        self.assertIn("本次报告中的证据序号", html)
        self.assertIn("证据含义", html)
        self.assertIn('class="evidence-kind"', html)
        self.assertIn("依赖清单", html)
        self.assertIn("是否存在依赖清单", html)
        self.assertIn("LLM-01（是否记录模型/API 版本）", html)
        self.assertIn("MODEL-02（是否提供模型卡或版本说明）", html)
        self.assertIn("已验证", render_claims_markdown(result))
        claims_html = render_claims_html(result)
        self.assertIn("声明验证矩阵", claims_html)
        self.assertIn("README 声明", claims_html)
        self.assertIn("验证说明", claims_html)
        self.assertIn("类型：", claims_html)
        self.assertIn("configs/app.yaml:8", claims_html)
        self.assertIn("sticky-scroll", claims_html)
        self.assertIn('class="claim-table"', claims_html)
        self.assertIn("overflow:visible", claims_html)
        self.assertIn("box-sizing:border-box", claims_html)

    def test_na_dimension_is_rendered_as_na_not_100_percent(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "demo-llm-app"
        snapshot = scan_repo(root)
        criteria = evaluate_criteria(snapshot)
        score = total_score(criteria)
        result = AuditResult(
            repo_path=str(root),
            generated_at="test",
            total_score=score,
            readiness=readiness_label(score),
            dimensions=score_dimensions(criteria),
            criteria=criteria,
            findings=build_findings(criteria),
            remediations=[],
            evidence=snapshot.evidence,
            files_scanned=len(snapshot.files),
        )
        na_dimension = replace(
            next(item for item in result.dimensions if item.name == "数据可复现"),
            points=0,
            max_points=0,
            percent=0,
            applicable=False,
        )
        result = replace(
            result,
            dimensions=[
                na_dimension if item.name == "数据可复现" else item
                for item in result.dimensions
            ],
        )
        html = render_html(result)
        self.assertIn('<div class="value na">N/A</div>', html)
        self.assertIn('class="radar-na">N/A</tspan>', html)
        self.assertIn("不能用 0% 或 100% 代表好坏", html)

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

