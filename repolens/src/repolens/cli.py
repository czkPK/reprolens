from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .ai_claims import enhance_claim_matrix
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
    audit.add_argument("--ai-review", action="store_true", help="Use the configured OpenAI-compatible model for semantic claim-to-criterion mapping.")
    audit.add_argument("--source-url", help=argparse.SUPPRESS)
    audit.add_argument("--source-commit", help=argparse.SUPPRESS)
    return parser


def run_audit(
    root: Path,
    out_dir: Path,
    *,
    execute: bool = False,
    autofix: bool = False,
    explain: bool = False,
    ai_review: bool = False,
    source_url: str | None = None,
    source_commit: str | None = None,
) -> dict:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"repository directory not found: {root}")

    snapshot = scan_repo(root)
    probes = run_probes(root, execute=execute)
    criteria = evaluate_criteria(snapshot)
    findings = build_findings(criteria)
    remediations = plan_remediations(findings, criteria)
    dimensions = score_dimensions(criteria)
    score = total_score(criteria)
    covered, coverage_total, coverage_percent = evidence_coverage(criteria)
    display_path = (
        f"{source_url} @ {source_commit[:12]}"
        if source_url and source_commit
        else source_url or str(root)
    )
    result = AuditResult(
        repo_path=display_path,
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
        source_url=source_url,
        source_commit=source_commit,
        project_type=snapshot.project_type,
        model_agnostic=snapshot.has("model_agnostic"),
    )
    result.claim_matrix = build_claim_matrix(result)
    result.claim_matrix, result.ai_metadata = enhance_claim_matrix(result, enabled=ai_review)

    out_dir = out_dir.expanduser().resolve()
    write_outputs(result, out_dir)
    autofix_result = None
    explanation_path = None
    if explain:
        explanation_path = write_explanation(result, out_dir)
    if autofix:
        autofix_result = generate_autofix(root, result, out_dir / "autofix")

    return {
        "result": result,
        "coverage": {"covered": covered, "total": coverage_total, "percent": coverage_percent},
        "autofix_result": autofix_result,
        "explanation_path": explanation_path,
        "out_dir": out_dir,
    }


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command != "audit":
        parser.error("unknown command")

    root = Path(args.path).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"repository directory not found: {root}")

    run = run_audit(
        root,
        Path(args.out_dir),
        execute=args.execute,
        autofix=args.autofix,
        explain=args.explain,
        ai_review=args.ai_review,
        source_url=args.source_url,
        source_commit=args.source_commit,
    )
    result = run["result"]
    coverage = run["coverage"]
    autofix_result = run["autofix_result"]
    explanation_path = run["explanation_path"]
    out_dir = run["out_dir"]
    score = result.total_score
    findings = result.findings
    remediations = result.remediations
    probes = result.probes

    if args.format == "json":
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"ReproLens audited {result.files_scanned} files.")
        print(f"Score: {score:.1f}/100 ({result.readiness})")
        print(f"Findings: {len(findings)}; remediation actions: {len(remediations)}")
        print(f"Claims: {len(result.claim_matrix)}; evidence coverage: {coverage['covered']}/{coverage['total']} ({coverage['percent']:.1f}%)")
        print(f"Probes: {len(probes)}; execution evidence: {out_dir / 'execution.json'}")
        if explanation_path is not None:
            print(f"Explanation: {explanation_path}")
        if args.ai_review:
            print(f"AI review: {result.ai_metadata.get('mode', 'unknown')}")
        if autofix_result is not None:
            print(f"AutoFix: {autofix_result['before_score']:.1f} -> {autofix_result['after_score']:.1f} (+{autofix_result['delta']:.1f})")
            print(f"Fix proposal: {out_dir / 'autofix' / 'FIX_PROPOSAL.md'}")
        print(f"Report: {out_dir / 'report.md'}")
    return 0

