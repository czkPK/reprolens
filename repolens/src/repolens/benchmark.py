from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .rules import evaluate_criteria
from .scanner import scan_repo
from .scoring import total_score


DEFAULT_CASES = [
    {
        "name": "demo-llm-app",
        "path": "examples/demo-llm-app",
        "expected": {
            "ENV-01": "pass",
            "DATA-02": "missing",
            "LLM-01": "pass",
            "LLM-02": "partial",
            "LLM-03": "pass",
            "LLM-04": "missing",
            "LLM-05": "pass",
            "LLM-06": "missing",
            "LLM-07": "missing",
            "LLM-08": "missing",
        },
    },
    {
        "name": "demo-ai-repo",
        "path": "examples/demo-ai-repo",
        "expected": {
            "ENV-01": "pass",
            "EXP-03": "missing",
            "MODEL-02": "missing",
            "LLM-01": "not_applicable",
        },
    },
]


@dataclass
class BenchmarkResult:
    name: str
    split: str
    score: float
    exact_matches: int
    total_expectations: int
    positive_tp: int
    positive_fp: int
    positive_fn: int
    details: list[dict]


def _is_positive(status: str) -> bool:
    return status in {"missing", "partial"}


def load_cases(base: Path) -> list[dict]:
    path = base / "benchmark" / "cases.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return DEFAULT_CASES


def run_case(case: dict, base: Path) -> BenchmarkResult:
    root = base / case["path"]
    criteria = {item.id: item for item in evaluate_criteria(scan_repo(root))}
    expected_map = case.get("expected", {}) or {}
    details: list[dict] = []
    exact = 0
    tp = fp = fn = 0
    for criterion_id, expected in expected_map.items():
        actual = criteria[criterion_id].status if criterion_id in criteria else "absent"
        ok = actual == expected
        exact += int(ok)
        expected_positive = _is_positive(expected)
        actual_positive = _is_positive(actual)
        if expected_positive and actual_positive:
            tp += 1
        elif actual_positive and not expected_positive:
            fp += 1
        elif expected_positive and not actual_positive:
            fn += 1
        details.append({"criterion_id": criterion_id, "expected": expected, "actual": actual, "match": ok})
    return BenchmarkResult(
        name=case["name"],
        split=case.get("split", "development"),
        score=total_score(list(criteria.values())),
        exact_matches=exact,
        total_expectations=len(expected_map),
        positive_tp=tp,
        positive_fp=fp,
        positive_fn=fn,
        details=details,
    )


def run_benchmark(base: Path) -> list[BenchmarkResult]:
    results: list[BenchmarkResult] = []
    for case in load_cases(base):
        if (base / case["path"]).is_dir():
            results.append(run_case(case, base))
    return results


def _precision(tp: int, fp: int) -> float:
    return round(tp / (tp + fp), 3) if tp + fp else 0.0


def _recall(tp: int, fn: int) -> float:
    return round(tp / (tp + fn), 3) if tp + fn else 0.0


def _f1(precision: float, recall: float) -> float:
    return round(2 * precision * recall / (precision + recall), 3) if precision + recall else 0.0


def render_markdown(results: list[BenchmarkResult], title: str = "ReproLens Benchmark") -> str:
    labeled = [item for item in results if item.total_expectations > 0]
    unlabeled = [item for item in results if item.total_expectations == 0]
    total_exact = sum(item.exact_matches for item in labeled)
    total_expectations = sum(item.total_expectations for item in labeled)
    tp = sum(item.positive_tp for item in labeled)
    fp = sum(item.positive_fp for item in labeled)
    fn = sum(item.positive_fn for item in labeled)
    precision = _precision(tp, fp)
    recall = _recall(tp, fn)
    accuracy = f"{total_exact}/{total_expectations} ({total_exact / total_expectations * 100:.1f}%)" if total_expectations else "N/A"
    lines = [
        f"# {title}",
        "",
        f"- Labeled exact status accuracy: **{accuracy}**",
        f"- Detection precision: **{precision:.3f}**",
        f"- Detection recall: **{recall:.3f}**",
        f"- Detection F1: **{_f1(precision, recall):.3f}**",
        "",
        "## Labeled Cases",
        "",
        "| Case | Score | Exact | TP | FP | FN |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for item in labeled:
        lines.append(
            f"| {item.name} | {item.score:.1f} | {item.exact_matches}/{item.total_expectations} | {item.positive_tp} | {item.positive_fp} | {item.positive_fn} |"
        )
    if unlabeled:
        lines.extend(["", "## Unlabeled Scanned Repositories", "", "| Case | Score | Note |", "|---|---:|---|"])
        for item in unlabeled:
            lines.append(f"| {item.name} | {item.score:.1f} | Missing manual labels |")
    lines.extend(["", "## Case Details", ""])
    for item in labeled:
        lines.extend([f"### {item.name}", "", "| Criterion | Expected | Actual | Match |", "|---|---|---|---|"])
        for detail in item.details:
            lines.append(
                f"| {detail['criterion_id']} | {detail['expected']} | {detail['actual']} | {'YES' if detail['match'] else 'NO'} |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    base = Path(__file__).resolve().parents[2]
    results = run_benchmark(base)
    out_dir = base / "benchmark"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(
        json.dumps([item.__dict__ for item in results], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    markdown = render_markdown(results)
    (out_dir / "results.md").write_text(markdown, encoding="utf-8")
    development = [item for item in results if item.split == "development"]
    holdout = [item for item in results if item.split == "holdout"]
    (out_dir / "development_results.md").write_text(render_markdown(development, "ReproLens Development Set"), encoding="utf-8")
    (out_dir / "holdout_results.md").write_text(render_markdown(holdout, "ReproLens Holdout Set"), encoding="utf-8")
    (out_dir / "holdout_results.json").write_text(json.dumps([item.__dict__ for item in holdout], ensure_ascii=False, indent=2), encoding="utf-8")
    print(markdown)
    print("\n## Holdout Summary\n")
    print(render_markdown(holdout, "ReproLens Holdout Set"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
