import tempfile
import unittest
from pathlib import Path

from repolens.models import CriterionResult
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

    def test_dimension_without_applicable_criteria_is_na(self):
        criteria = [
            CriterionResult(
                id="MODEL-01",
                dimension="模型可复现",
                title="是否记录模型版本",
                status="not_applicable",
                points=0,
                max_points=8,
                applicable=False,
                note="当前项目不包含模型权重。",
            )
        ]
        dimensions = score_dimensions(criteria)
        model = next(item for item in dimensions if item.name == "模型可复现")
        self.assertFalse(model.applicable)
        self.assertEqual(model.max_points, 0)
        self.assertEqual(model.percent, 0.0)

    def test_dataset_link_satisfies_source_but_not_script(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Example project\n\n"
                "Download the training dataset from "
                "[Hugging Face](https://huggingface.co/datasets/example/project-data).\n",
                encoding="utf-8",
            )
            criteria = evaluate_criteria(scan_repo(root))
        by_id = {item.id: item for item in criteria}
        self.assertEqual(by_id["DATA-01"].status, "pass")
        self.assertEqual(by_id["DATA-02"].status, "missing")
        self.assertIn("没有数据下载或预处理脚本", by_id["DATA-02"].note)
        self.assertEqual(by_id["DATA-02"].evidence_ids, [])

    def test_pinned_dependency_versions_satisfy_environment_lock_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "requirements.txt").write_text("numpy==1.26.4\ntorch==2.4.0\n", encoding="utf-8")
            criteria = evaluate_criteria(scan_repo(root))
        by_id = {item.id: item for item in criteria}
        self.assertEqual(by_id["ENV-02"].status, "pass")
        self.assertIn("固定", by_id["ENV-02"].note)

    def test_unpinned_dependency_manifest_is_only_partial_environment_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "requirements.txt").write_text("numpy\ntorch\n", encoding="utf-8")
            criteria = evaluate_criteria(scan_repo(root))
        by_id = {item.id: item for item in criteria}
        self.assertEqual(by_id["ENV-02"].status, "partial")

    def test_dataset_download_and_license_satisfy_data_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Example dataset\n\n"
                "[Dataset](https://huggingface.co/datasets/example/project-data)\n"
                "```python\nload_dataset(\"example/project-data\")\n```\n"
                "The dataset is released under CC BY-NC 4.0.\n",
                encoding="utf-8",
            )
            criteria = evaluate_criteria(scan_repo(root))
        by_id = {item.id: item for item in criteria}
        self.assertEqual(by_id["DATA-01"].status, "pass")
        self.assertEqual(by_id["DATA-02"].status, "pass")
        self.assertEqual(by_id["DATA-03"].status, "pass")

    def test_prompt_check_not_applicable_for_non_llm_repo(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "demo-ai-repo"
        snapshot = scan_repo(root)
        criteria = evaluate_criteria(snapshot)
        prompt = next(item for item in criteria if item.id == "LLM-02")
        self.assertFalse(prompt.applicable)


if __name__ == "__main__":
    unittest.main()

