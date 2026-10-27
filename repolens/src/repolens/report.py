from __future__ import annotations

import json
from pathlib import Path

from .badge import badge_payload, render_badge_svg
from .claims import build_claim_matrix, claim_verification_note, criterion_confidence, evidence_coverage, evidence_explanation, evidence_reference_entries, format_criterion_references
from .html_report import render_claims_html, render_html
from .models import AuditResult


STATUS_LABELS = {
    "pass": "PASS",
    "partial": "PARTIAL",
    "missing": "MISSING",
    "not_applicable": "N/A",
}

CLAIM_STATUS_LABELS = {
    "verified": "已验证",
    "partially_verified": "部分验证",
    "unverified": "未验证",
    "not_applicable": "不适用",
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
    if result.source_url:
        source_lines = [f"- Source: [{result.source_url}]({result.source_url})"]
        if result.source_commit:
            source_lines.append(f"- Source commit: `{result.source_commit}`")
        lines[4:4] = source_lines
    if result.ai_metadata:
        lines.insert(4, f"- Semantic claim mapping: **{result.ai_metadata.get('mode', 'rules')}**")
    for dim in result.dimensions:
        lines.append(f"| {dim.name} | {dim.points:.1f} | {dim.max_points:.1f} | {dim.percent:.1f}% |")

    lines.extend(["", "## Top 3 Priority Actions", ""])
    top_actions = sorted(result.remediations, key=lambda item: item.estimated_score_gain, reverse=True)[:3]
    if not top_actions:
        lines.append("No remediation actions generated.")
    for index, item in enumerate(top_actions, 1):
        lines.append(f"{index}. **{item.action}** — expected gain **+{item.estimated_score_gain:.1f}**; {item.rationale}")

    lines.extend(
        [
            "",
            "## Criteria",
            "",
            "| 检查项编号 | 所属维度 | 检查要求 | 状态 | 证据强度 | 得分 | 证据编号 | 证据说明 |",
            "|---|---|---|---|---|---:|---|---|",
        ]
    )
    lines.extend(
        [
            "",
            "**读表说明：** PASS = 满足要求；PARTIAL = 只有部分证据；MISSING = 应有但没有找到；N/A = 当前项目类型不适用。Confidence 表示证据支持强度，不代表项目整体质量。",
            "",
        ]
    )
    for item in result.criteria:
        evidence = ", ".join(item.evidence_ids) if item.evidence_ids else "-"
        explanation = evidence_explanation(item, result.evidence, result.project_type, result.model_agnostic)
        lines.append(
            f"| {item.id} | {item.dimension} | {item.title} | {STATUS_LABELS.get(item.status, item.status)} | {criterion_confidence(item).upper()} | {item.points:.1f}/{item.max_points:.1f} | {evidence} | {_md(explanation)} |"
        )

    lines.extend(
        [
            "",
            "## Claim-Evidence Matrix",
            "",
            "**读表方法：** 每一行先看 README 说了什么，再看验证状态、检查依据、缺口和支持证据。括号内是内部编号对应的中文含义。",
            "",
            "| 声明编号 | README 声明 | 验证状态 | 检查依据（需要检查的项） | 还缺什么（缺口） | 支持证据 | 验证说明 |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    if not claim_rows:
        lines.append("| - | 未抽取到 README 声明 | 不适用 | - | - | - | 未发现可验证声明。 |")
    for row in claim_rows:
        criteria = format_criterion_references(row.get("criteria", []), result.criteria)
        gaps = format_criterion_references(row.get("gaps", []), result.criteria)
        evidence_entries = evidence_reference_entries(row.get("evidence_ids", []), result.evidence)
        evidence = "<br>".join(
            f"`{entry['id']}` {entry['location']}：{entry['excerpt']}" if entry["excerpt"] else f"`{entry['id']}` {entry['location']}"
            for entry in evidence_entries
        ) or "-"
        status = CLAIM_STATUS_LABELS.get(row.get("status", ""), str(row.get("status", "")))
        lines.append(
            f"| {_md(row.get('claim_id', '-'))} | {_md(row.get('claim', ''))} | {status} | {_md(criteria)} | {_md(gaps)} | {_md(evidence)} | {_md(claim_verification_note(row, result.criteria))} |"
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
        "# ReproLens 声明—证据—缺口矩阵",
        "",
        f"- Repository: `{result.repo_path}`",
        f"- Generated at: `{result.generated_at}`",
        f"- Evidence coverage: **{coverage['covered']}/{coverage['total']} ({coverage['percent']:.1f}%)**",
        f"- Claims extracted: **{len(rows)}**",
        "",
        "## Matrix",
        "",
        "| 声明编号 | README 声明 | 验证状态 | 检查依据（需要检查的项） | 还缺什么（缺口） | 支持证据 | 验证说明 |",
        "|---|---|---|---|---|---|---|",
    ]
    if not rows:
        lines.append("| - | 未抽取到 README 声明 | 不适用 | - | - | - | 未发现可验证声明。 |")
    for row in rows:
        status = CLAIM_STATUS_LABELS.get(row.get("status", ""), str(row.get("status", "")))
        lines.append(
            "| {claim_id} | {claim} | {status} | {criteria} | {gaps} | {evidence} | {note} |".format(
                claim_id=_md(row.get("claim_id", "-")),
                claim=_md(row.get("claim", "")),
                status=status,
                criteria=_md(format_criterion_references(row.get("criteria", []), result.criteria)),
                gaps=_md(format_criterion_references(row.get("gaps", []), result.criteria)),
                evidence="<br>".join(
                    f"`{entry['id']}` {entry['location']}：{_md(entry['excerpt'])}" if entry["excerpt"] else f"`{entry['id']}` {entry['location']}"
                    for entry in evidence_reference_entries(row.get("evidence_ids", []), result.evidence)
                ) or "-",
                note=_md(claim_verification_note(row, result.criteria)),
            )
        )
    lines.extend(
        [
            "",
            "## Status Definitions",
            "",
            "- **已验证**：相关检查项全部通过，并且有证据支持。",
            "- **部分验证**：找到部分证据，但仍有缺口。",
            "- **未验证**：关键证据缺失，当前声明不能视为已验证。",
            "- **不适用**：相关检查项不适用于当前项目类型。",
            "",
            "读表方法：Claim 是 README 原句；Required criteria 是验证这句话需要检查的项；Gaps 是仍未满足的检查项；Evidence 是支持证据编号。该矩阵不执行第三方代码，也不保证语义完全正确。",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(result: AuditResult, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    claim_rows = _claim_rows(result)
    (out_dir / "report.md").write_text(render_markdown(result), encoding="utf-8")
    (out_dir / "report.html").write_text(render_html(result), encoding="utf-8")
    (out_dir / "claims.html").write_text(render_claims_html(result), encoding="utf-8")
    (out_dir / "claims.md").write_text(render_claims_markdown(result), encoding="utf-8")
    (out_dir / "claims.json").write_text(
        json.dumps(claim_rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "ai-review.json").write_text(
        json.dumps(result.ai_metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "badge.svg").write_text(render_badge_svg(result), encoding="utf-8")
    (out_dir / "badge.json").write_text(
        json.dumps(badge_payload(result), ensure_ascii=False, indent=2), encoding="utf-8"
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

