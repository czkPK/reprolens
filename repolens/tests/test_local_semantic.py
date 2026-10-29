import json
import unittest
from pathlib import Path

from repolens.local_semantic import load_model, predict_claims
from repolens.models import AuditResult, CriterionResult
from repolens.rules import SPECS


def _result(claims: list[dict]) -> AuditResult:
    criteria = [
        CriterionResult(
            id=spec.id,
            dimension=spec.dimension,
            title=spec.title,
            status="missing",
            points=0,
            max_points=spec.max_points,
            applicable=True,
            note="",
            evidence_ids=[],
        )
        for spec in SPECS
    ]
    return AuditResult(
        repo_path="example",
        generated_at="test",
        total_score=0,
        readiness="Not Ready",
        dimensions=[],
        criteria=criteria,
        findings=[],
        remediations=[],
        evidence=[],
        files_scanned=1,
        claim_matrix=claims,
    )


class LocalSemanticTests(unittest.TestCase):
    def test_model_artifact_is_present_and_auditable(self):
        model = load_model()
        self.assertEqual(model["model_id"], "ReproLens-SmallSemantic-v1")
        self.assertEqual(model["license"], "MIT")
        self.assertEqual(len(model["criteria"]), 25)
        self.assertFalse(model["algorithm"].endswith("api"))

    def test_unseen_claims_map_to_expected_criteria(self):
        claims = [
            {"claim_id": "C-1", "claim": "All runs are repeatable because every random source is fixed."},
            {"claim_id": "C-2", "claim": "Download the pre-trained checkpoint from the project page."},
            {"claim_id": "C-3", "claim": "The system logs every tool invocation with a session identifier."},
            {"claim_id": "C-4", "claim": "Prompt templates are versioned in the prompts directory."},
        ]
        predictions, metadata = predict_claims(_result(claims), claims)
        by_claim = {row["claim_id"]: row for row in predictions}
        self.assertEqual(metadata["mode"], "local-semantic")
        self.assertIn("EXP-03", by_claim["C-1"]["criterion_ids"])
        self.assertIn("MODEL-01", by_claim["C-2"]["criterion_ids"])
        self.assertIn("LLM-06", by_claim["C-3"]["criterion_ids"])
        self.assertIn("LLM-02", by_claim["C-4"]["criterion_ids"])


    def test_curated_semantic_benchmark_meets_accuracy_floor(self):
        path = Path(__file__).resolve().parents[1] / "benchmark" / "semantic_evaluation.json"
        report = json.loads(path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(report["top1_accuracy"], 0.90)
        self.assertGreaterEqual(report["top2_hit_rate"], 0.90)
        self.assertGreaterEqual(report["coverage_rate"], 0.95)


if __name__ == "__main__":
    unittest.main()
