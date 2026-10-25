from __future__ import annotations

import json
from pathlib import Path

from .claims import build_claim_matrix, criterion_confidence, evidence_coverage
from .html_report import render_html
from .models import AuditResult


STATUS_LABELS = {
    "pass": "PASS",
    "partial": "PARTIAL",
    "missing": "MISSING",
    "not_applicable": "N/A",
}

CLAIM_STATUS_LABELS = {
    "verified": "VERIFIED",
    "partially_verified": "PARTIALLY VERIFIED",
    "unverified": "UNVERIFIED",
    "not_applicable": "N/A",
}


def _md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def _claim_rows(result: AuditResult) -> list[dict]:
    return result.claim_matrix or build_claim_matrix(result)


def _coverage(result: AuditResult) -> dict:
    if result.evidence_coverage:
        return result.evidence_coverage
    covered, total, percent = evidence_coverage(result.criteria)
    return {"covered": covered, "total": total, "percent": percent}


def render_markdown(result: AuditResult) -> str:
    coverage = _coverage(result)
    claim_rows = _claim_rows(result)
    lines = [
        "# ReproLens Audit Report",
        "",
        f"- Repository: `{result.repo_path}`",
        f"- Generated at: `{result.generated_at}`",
        f"- Files scanned: **{result.files_scanned}**",
        f"- Overall score: **{result.total_score:.1f} / 100**",
        f"- Readiness: **{result.readiness}**",
        f"- Evidence coverage: **{coverage['covered']}/{coverage['total']} ({coverage['percent']:.1f}%)**",
        f"- README claims audited: **{len(claim_rows)}**",
        "",
        "## Dimension Scores",
        "",
        "| Dimension | Points | Max | Percent |",
        "|---|---:|---:|---:|",
    ]
    for dim in result.dimensions:
        lines.append(f"| {dim.name} | {dim.points:.1f} | {dim.max_points:.1f} | {dim.percent:.1f}% |")

    lines.extend(
        [
            "",
            "## Criteria",
            "",
            "| ID | Dimension | Criterion | Status | Confidence | Points | Evidence |",
            "|---|---|---|---|---|---:|---|",
        ]
    )
    for item in result.criteria:
        evidence = ", ".join(item.evidence_ids) if item.evidence_ids else "-"
        lines.append(
            f"| {item.id} | {item.dimension} | {item.title} | {STATUS_LABELS.get(item.status, item.status)} | {criterion_confidence(item).upper()} | {item.points:.1f}/{item.max_points:.1f} | {evidence} |"
        )

    lines.extend(
        [
            "",
            "## Claim-Evidence Matrix",
            "",
            "README claims are mapped to the criteria that must be supported before the claim can be treated as reproducible.",
            "",
            "| Claim | Status | Required criteria | Gaps | Evidence |",
            "|---|---|---|---|---|",
        ]
    )
    if not claim_rows:
        lines.append("| - | N/A | - | - | No README claims extracted. |")
    for row in claim_rows:
        criteria = ", ".join(row.get("criteria", [])) or "-"
        gaps = ", ".join(row.get("gaps", [])) or "-"
        evidence = ", ".join(row.get("evidence_ids", [])) or "-"
        status = CLAIM_STATUS_LABELS.get(row.get("status", ""), str(row.get("status", "")))
        lines.append(
            f"| {_md(row.get('claim', ''))} | {status} | {_md(criteria)} | {_md(gaps)} | {_md(evidence)} |"
        )

    lines.extend(["", "## Findings", ""])
    if not result.findings:
        lines.append("No findings. Verify the evidence appendix manually before release.")
    for finding in result.findings:
        lines.extend(
            [
                f"### {finding.id} [{finding.severity.upper()}] {finding.title}",
                "",
                f"- Criterion: `{finding.criterion_id}`",
                f"- Message: {finding.message}",
                f"- Evidence: {', '.join(f'`{e}`' for e in finding.evidence_ids) if finding.evidence_ids else 'none'}",
                "",
            ]
        )

    lines.extend(["## Execution Evidence", ""])
    if not result.probes:
        lines.append("No execution probes were run.")
    else:
        lines.extend(["| Probe | Status | Return code | Duration | Command |", "|---|---|---:|---:|---|"])
        for probe in result.probes:
            display_command = probe.command.replace("\n", " ")[:180]
            lines.append(
                f"| {probe.name} | {probe.status.upper()} | {probe.returncode if probe.returncode is not None else '-'} | {probe.duration_seconds:.3f}s | `{display_command}` |"
            )
    for probe in result.probes:
        if probe.status not in {"pass", "skip"}:
            lines.extend(["", f"### {probe.name} output", "", "```text", (probe.stderr or probe.stdout or "(no output)")[:2000], "```"])

    lines.extend(["", "## Minimal Remediation Plan", ""])
    if not result.remediations:
        lines.append("No remediation actions generated.")
    for item in result.remediations:
        lines.extend(
            [
                f"### {item.finding_id} - {item.action}",
                "",
                f"- Rationale: {item.rationale}",
                f"- Cost: **{item.cost}**",
                f"- Impact: **{item.impact}**",
                f"- Estimated score gain: **+{item.estimated_score_gain:.1f}**",
                f"- Evidence: {', '.join(f'`{e}`' for e in item.evidence_ids) if item.evidence_ids else 'none'}",
                "",
            ]
        )

    lines.extend(["## Evidence Appendix", ""])
    if not result.evidence:
        lines.append("No evidence extracted.")
    for item in result.evidence:
        location = f"{item.path}:{item.line}" if item.line else item.path
        lines.append(f"- `{item.id}` [{item.kind}] `{location}` — {item.excerpt}")

    lines.extend(
        [
            "",
            "## Scope and Limitations",
            "",
            "- This is static reproduction readiness analysis, not proof that the project reproduces successfully.",
            "- No untrusted repository code is executed by default.",
            "- Execution probes are optional and require explicit --execute; GitHub Action integration is available in the repository.",
            "- AI-generated explanations must be reviewed by the team before submission or release.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_claims_markdown(result: AuditResult) -> str:
    coverage = _coverage(result)
    rows = _claim_rows(result)
    lines = [
        "# ReproLens Claim-Evidence Matrix",
        "",
        f"- Repository: `{result.repo_path}`",
        f"- Generated at: `{result.generated_at}`",
        f"- Evidence coverage: **{coverage['covered']}/{coverage['total']} ({coverage['percent']:.1f}%)**",
        f"- Claims extracted: **{len(rows)}**",
        "",
        "## Matrix",
        "",
        "| Claim ID | Claim | Status | Required criteria | Gaps | Evidence |",
        "|---|---|---|---|---|---|",
    ]
    if not rows:
        lines.append("| - | No README claims extracted. | N/A | - | - | - |")
    for row in rows:
        status = CLAIM_STATUS_LABELS.get(row.get("status", ""), str(row.get("status", "")))
        lines.append(
            "| {claim_id} | {claim} | {status} | {criteria} | {gaps} | {evidence} |".format(
                claim_id=_md(row.get("claim_id", "-")),
                claim=_md(row.get("claim", "")),
                status=status,
                criteria=_md(", ".join(row.get("criteria", [])) or "-"),
                gaps=_md(", ".join(row.get("gaps", [])) or "-"),
                evidence=_md(", ".join(row.get("evidence_ids", [])) or "-"),
            )
        )
    lines.extend(
        [
            "",
            "## Status Definitions",
            "",
            "- **VERIFIED**: every applicable mapped criterion passes with linked evidence.",
            "- **PARTIALLY VERIFIED**: at least one mapped criterion passes but another is partial.",
            "- **UNVERIFIED**: at least one mapped criterion is missing, so the claim is not yet supported.",
            "- **N/A**: none of the mapped criteria apply to this project type.",
            "",
            "The matrix verifies documentation claims against repository evidence. It does not execute untrusted code or guarantee semantic correctness.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(result: AuditResult, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    claim_rows = _claim_rows(result)
    (out_dir / "report.md").write_text(render_markdown(result), encoding="utf-8")
    (out_dir / "report.html").write_text(render_html(result), encoding="utf-8")
    (out_dir / "claims.md").write_text(render_claims_markdown(result), encoding="utf-8")
    (out_dir / "claims.json").write_text(
        json.dumps(claim_rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "score.json").write_text(
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "evidence.json").write_text(
        json.dumps([item.__dict__ for item in result.evidence], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "remediation.json").write_text(
        json.dumps([item.__dict__ for item in result.remediations], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "execution.json").write_text(
        json.dumps([item.__dict__ for item in result.probes], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

