import unittest

from repolens.claims import _claim_criteria, build_claim_matrix, claim_status, claim_verification_note, criterion_confidence, evidence_coverage, evidence_explanation, evidence_reference_entries, format_criterion_references
from repolens.models import AuditResult, CriterionResult, Evidence
from repolens.scanner import _clean_claim_line


def criterion(status: str, evidence_ids: list[str] | None = None, applicable: bool = True) -> CriterionResult:
    return CriterionResult(
        id="TEST-01",
        dimension="test",
        title="test",
        status=status,
        points=0.0,
        max_points=1.0,
        applicable=applicable,
        note="",
        evidence_ids=evidence_ids or [],
    )


class ClaimTests(unittest.TestCase):
    def test_claim_status_summarizes_mapped_criteria(self):
        self.assertEqual(claim_status([criterion("pass")]), "verified")
        self.assertEqual(claim_status([criterion("pass"), criterion("partial")]), "partially_verified")
        self.assertEqual(claim_status([criterion("pass"), criterion("missing")]), "unverified")
        self.assertEqual(claim_status([criterion("not_applicable", applicable=False)]), "not_applicable")

    def test_criterion_confidence_uses_status_and_evidence_count(self):
        self.assertEqual(criterion_confidence(criterion("pass", ["E-1", "E-2"])), "high")
        self.assertEqual(criterion_confidence(criterion("pass", ["E-1"])), "medium")
        self.assertEqual(criterion_confidence(criterion("missing")), "low")
        self.assertEqual(criterion_confidence(criterion("not_applicable", applicable=False)), "N/A")

    def test_evidence_coverage_ignores_not_applicable_criteria(self):
        covered, total, percent = evidence_coverage(
            [
                criterion("pass", ["E-1"]),
                criterion("partial", ["E-2"]),
                criterion("missing"),
                criterion("not_applicable", ["E-3"], applicable=False),
            ]
        )
        self.assertEqual((covered, total, percent), (2, 3, 66.7))

    def test_agent_claim_requires_trace_specific_evidence(self):
        self.assertNotIn("LLM-06", _claim_criteria("A memory layer for AI agents."))
        self.assertIn("LLM-06", _claim_criteria("The agent records tool call traces."))

    def test_claim_cleaner_removes_markdown_and_html_noise(self):
        claim = _clean_claim_line('<a href="https://example.com"><strong>See the [benchmark guide](https://example.com)</strong></a>')
        self.assertEqual(claim, "See the benchmark guide")

    def test_evidence_explanation_contains_location_and_excerpt(self):
        item = criterion("pass", ["E-1"])
        evidence = [Evidence("E-1", "dependency-manifest", "requirements.txt", 1, "openai>=1.0")]
        explanation = evidence_explanation(item, evidence)
        self.assertIn("requirements.txt:1", explanation)
        self.assertIn("openai>=1.0", explanation)
        self.assertTrue(explanation.startswith("支持证据"))

    def test_not_applicable_explanation_does_not_claim_evidence_support(self):
        item = criterion("not_applicable", ["E-1"], applicable=False)
        evidence = [Evidence("E-1", "readme", "README.md", 1, "demo")]
        self.assertIn("不参与评分", evidence_explanation(item, evidence))

    def test_claim_verification_note_explains_gaps(self):
        note = claim_verification_note({"status": "partially_verified", "gaps": ["LLM-03"]})
        self.assertIn("部分证据", note)
        self.assertIn("LLM-03", note)

    def test_criterion_references_include_chinese_titles(self):
        item = criterion("pass")
        item.id = "LLM-01"
        item.title = "是否记录模型/API 版本"
        self.assertEqual(
            format_criterion_references(["LLM-01"], [item]),
            "LLM-01（是否记录模型/API 版本）",
        )

    def test_build_claim_matrix_separates_claim_and_evidence_ids(self):
        result = AuditResult(
            repo_path="example",
            generated_at="test",
            total_score=0.0,
            readiness="Not Ready",
            dimensions=[],
            criteria=[criterion("pass")],
            findings=[],
            remediations=[],
            evidence=[Evidence("E-013", "claim", "README.md", 1, "The project records retrieval evidence.")],
            files_scanned=1,
        )
        rows = build_claim_matrix(result)
        self.assertEqual(rows[0]["claim_id"], "C-001")
        self.assertEqual(rows[0]["source_evidence_id"], "E-013")

    def test_evidence_reference_entries_include_location_and_excerpt(self):
        entries = evidence_reference_entries(
            ["E-1"],
            [Evidence("E-1", "config", "configs/app.yaml", 8, "vector_store: faiss")],
        )
        self.assertEqual(entries[0]["location"], "configs/app.yaml:8")
        self.assertEqual(entries[0]["excerpt"], "vector_store: faiss")


if __name__ == "__main__":
    unittest.main()
