from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .autofix import generate_autofix
from .claims import build_claim_matrix, evidence_coverage
from .llm import write_explanation
from .models import AuditResult
from .probes import run_probes
from .remediation import plan_remediations
from .report import write_outputs
from .rules import build_findings, evaluate_criteria
from .scanner import scan_repo
from .scoring import readiness_label, score_dimensions, total_score


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repolens",
        description="Evidence-constrained reproduction readiness auditor for open-source LLM/RAG/Agent repositories.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit = subparsers.add_parser("audit", help="Audit a local repository.")
    audit.add_argument("path", help="Repository directory.")
    audit.add_argument("--out-dir", default="repolens-output", help="Directory for report files.")
    audit.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Print a compact result.")
    audit.add_argument("--execute", action="store_true", help="Run repository scripts with --help and pytest collection probes. Only use on trusted repositories.")
    audit.add_argument("--autofix", action="store_true", help="Generate a conservative fix proposal and re-audit a staging copy.")
    audit.add_argument("--explain", action="store_true", help="Generate an evidence-grounded explanation with offline fallback.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command != "audit":
        parser.error("unknown command")

    root = Path(args.path).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"repository directory not found: {root}")

    snapshot = scan_repo(root)
    probes = run_probes(root, execute=args.execute)
    criteria = evaluate_criteria(snapshot)
    findings = build_findings(criteria)
    remediations = plan_remediations(findings, criteria)
    dimensions = score_dimensions(criteria)
    score = total_score(criteria)
    covered, coverage_total, coverage_percent = evidence_coverage(criteria)
    result = AuditResult(
        repo_path=str(root),
        generated_at=datetime.now(timezone.utc).isoformat(),
        total_score=score,
        readiness=readiness_label(score),
        dimensions=dimensions,
        criteria=criteria,
        findings=findings,
        remediations=remediations,
        evidence=snapshot.evidence,
        files_scanned=len(snapshot.files),
        probes=probes,
        evidence_coverage={
            "covered": covered,
            "total": coverage_total,
            "percent": coverage_percent,
        },
    )
    result.claim_matrix = build_claim_matrix(result)

    out_dir = Path(args.out_dir).expanduser().resolve()
    write_outputs(result, out_dir)
    autofix_result = None
    explanation_path = None
    if args.explain:
        explanation_path = write_explanation(result, out_dir)
    if args.autofix:
        autofix_result = generate_autofix(root, result, out_dir / "autofix")

    if args.format == "json":
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"ReproLens audited {len(snapshot.files)} files.")
        print(f"Score: {score:.1f}/100 ({result.readiness})")
        print(f"Findings: {len(findings)}; remediation actions: {len(remediations)}")
        print(f"Claims: {len(result.claim_matrix)}; evidence coverage: {covered}/{coverage_total} ({coverage_percent:.1f}%)")
        print(f"Probes: {len(probes)}; execution evidence: {out_dir / 'execution.json'}")
        if explanation_path is not None:
            print(f"Explanation: {explanation_path}")
        if autofix_result is not None:
            print(f"AutoFix: {autofix_result['before_score']:.1f} -> {autofix_result['after_score']:.1f} (+{autofix_result['delta']:.1f})")
            print(f"Fix proposal: {out_dir / 'autofix' / 'FIX_PROPOSAL.md'}")
        print(f"Report: {out_dir / 'report.md'}")
    return 0

