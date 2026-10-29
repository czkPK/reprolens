from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from repolens.local_semantic import predict_claims
from repolens.models import AuditResult, CriterionResult
from repolens.rules import SPECS


def main() -> int:
    claims = json.loads((ROOT / "benchmark" / "semantic_claims.json").read_text(encoding="utf-8"))
    rules = [{"claim_id": row["claim_id"], "claim": row["claim"]} for row in claims]
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
    result = AuditResult(
        repo_path="semantic-evaluation",
        generated_at="evaluation",
        total_score=0,
        readiness="Not Ready",
        dimensions=[],
        criteria=criteria,
        findings=[],
        remediations=[],
        evidence=[],
        files_scanned=1,
        claim_matrix=rules,
    )
    predictions, metadata = predict_claims(result, rules)
    by_claim = {row["claim_id"]: row for row in predictions}
    hit1 = hit2 = covered = 0
    misses = []
    for expected in claims:
        prediction = by_claim.get(expected["claim_id"], {})
        ids = prediction.get("criterion_ids", [])
        covered += int(bool(ids))
        hit = expected["expected_criterion"] in ids
        hit1 += int(bool(ids) and ids[0] == expected["expected_criterion"])
        hit2 += int(hit)
        if not hit:
            misses.append({**expected, "predicted": ids})
    total = len(claims)
    report = {
        "model": metadata["model"],
        "mode": metadata["mode"],
        "samples": total,
        "coverage": covered,
        "coverage_rate": round(covered / total, 3),
        "top1_accuracy": round(hit1 / total, 3),
        "top2_hit_rate": round(hit2 / total, 3),
        "misses": misses,
    }
    output = ROOT / "benchmark" / "semantic_evaluation.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
