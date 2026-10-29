import os
import unittest
from unittest.mock import patch

from repolens.ai_claims import _extract_json, enhance_claim_matrix, validate_ai_rows
from repolens.models import AuditResult, CriterionResult


def _criterion(criterion_id: str, status: str, evidence_ids: list[str]) -> CriterionResult:
    return CriterionResult(
        id=criterion_id,
        dimension="LLM",
        title=criterion_id,
        status=status,
        points=1.0 if status == "pass" else 0.5 if status == "partial" else 0.0,
        max_points=1.0,
        applicable=True,
        note="",
        evidence_ids=evidence_ids,
    )


def _result() -> AuditResult:
    return AuditResult(
        repo_path="example",
        generated_at="test",
        total_score=50.0,
        readiness="At Risk",
        dimensions=[],
        criteria=[
            _criterion("LLM-05", "pass", ["E-001"]),
            _criterion("LLM-06", "partial", ["E-002"]),
        ],
        findings=[],
        remediations=[],
        evidence=[],
        files_scanned=1,
        claim_matrix=[
            {
                "claim_id": "E-010",
                "claim": "The project records agent traces.",
                "criteria": ["LLM-05"],
                "status": "verified",
                "gaps": [],
                "evidence_ids": ["E-001"],
            }
        ],
    )


class AIClaimTests(unittest.TestCase):
    def test_extract_json_from_fenced_response(self):
        self.assertEqual(_extract_json('```json\n[{"claim_id":"E-1"}]\n```')[0]["claim_id"], "E-1")

    def test_ai_rows_are_validated_against_repository_evidence(self):
        rows = validate_ai_rows(
            [{"claim_id": "E-010", "criterion_ids": ["LLM-06", "UNKNOWN"], "confidence": "high", "reason": "trace evidence"}],
            _result(),
            _result().claim_matrix,
        )
        self.assertEqual(rows[0]["criteria"], ["LLM-06"])
        self.assertEqual(rows[0]["status"], "partially_verified")
        self.assertEqual(rows[0]["evidence_ids"], ["E-002"])
        self.assertTrue(rows[0]["ai_assisted"])

    def test_unknown_only_mapping_keeps_rule_result(self):
        result = _result()
        rows = validate_ai_rows(
            [{"claim_id": "E-010", "criterion_ids": ["UNKNOWN"]}],
            result,
            result.claim_matrix,
        )
        self.assertEqual(rows, result.claim_matrix)

    def test_local_semantic_mode_is_default(self):
        with patch.dict(os.environ, {}, clear=True):
            rows, metadata = enhance_claim_matrix(_result(), enabled=True)
        self.assertEqual(metadata["mode"], "local-semantic")
        self.assertEqual(metadata["provider"], "local")
        self.assertFalse(metadata["external_api"])
        self.assertEqual(metadata["claims_enhanced"], 1)
        self.assertIn("LLM-06", rows[0]["criteria"])
        self.assertTrue(rows[0]["ai_assisted"])

    def test_external_mode_without_configuration_falls_back_to_rules(self):
        with patch.dict(os.environ, {"REPROLENS_SEMANTIC_MODE": "llm"}, clear=True):
            rows, metadata = enhance_claim_matrix(_result(), enabled=True)
        self.assertEqual(rows, _result().claim_matrix)
        self.assertEqual(metadata["mode"], "rules-fallback")

    def test_disabled_semantic_mode_returns_rules(self):
        with patch.dict(os.environ, {"REPROLENS_SEMANTIC_MODE": "off"}, clear=True):
            rows, metadata = enhance_claim_matrix(_result(), enabled=True)
        self.assertEqual(rows, _result().claim_matrix)
        self.assertEqual(metadata["mode"], "rules")


if __name__ == "__main__":
    unittest.main()
