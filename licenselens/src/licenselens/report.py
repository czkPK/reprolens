from __future__ import annotations

import json
from pathlib import Path

from .catalog import get_license
from .graph import build_graph
from .models import AnalysisResult


def _severity_label(value: str) -> str:
    return {"high": "HIGH", "medium": "MEDIUM", "info": "INFO"}.get(value, value.upper())


def render_markdown(result: AnalysisResult) -> str:
    lines = [
        "# LicenseLens Analysis Report",
        "",
        f"- Project: `{result.project_root}`",
        f"- Usage mode: `{result.usage_mode}`",
        f"- Project license: `{result.project_license or 'UNKNOWN'}`",
        f"- Generated at: `{result.generated_at}`",
        "",
        "## Summary",
        "",
        f"- Dependencies: **{len(result.dependencies)}**",
        f"- Findings: **{len(result.findings)}**",
        f"- Remediation actions: **{len(result.remediations)}**",
        "",
        "## Dependencies",
        "",
        "| Package | Version | License | Confidence | Evidence |",
        "|---|---|---|---:|---|",
    ]
    for dep in result.dependencies:
        evidence = ", ".join(f"`{item}`" for item in dep.evidence)
        lines.append(
            f"| {dep.name} | {dep.version or '-'} | {dep.license_spdx} | {dep.confidence:.2f} | {evidence} |"
        )

    lines.extend(["", "## Findings", ""])
    if not result.findings:
        lines.append("No findings. This does not constitute legal advice; verify upstream LICENSE files before release.")
    for finding in result.findings:
        lines.extend(
            [
                f"### {finding.id} [{_severity_label(finding.severity)}] {finding.rule}",
                "",
                f"- Package: `{finding.package}`",
                f"- License: `{finding.license_spdx}`",
                f"- Message: {finding.message}",
                f"- Evidence: {', '.join(f'`{item}`' for item in finding.evidence)}",
                "",
            ]
        )

    lines.extend(["## Remediation Plan", ""])
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
                f"- Evidence: {', '.join(f'`{e}`' for e in item.evidence)}",
                "",
            ]
        )

    lines.extend(
        [
            "## Scope and Limitations",
            "",
            "- This is an engineering compliance check, not legal advice.",
            "- Unknown or custom licenses require manual review of the original LICENSE and upstream terms.",
            "- The current MVP focuses on Python/npm manifests and a defined set of usage modes.",
            "- AI-generated explanations must be reviewed by the team before submission or release.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_notice(result: AnalysisResult) -> str:
    lines = ["# Third-Party Notices", "", "The following dependencies may require attribution or notice retention:", ""]
    required = [dep for dep in result.dependencies if get_license(dep.license_spdx).notice_required]
    if not required:
        lines.append("- No notice-required dependencies detected in the current scope.")
    for dep in required:
        lines.append(f"- {dep.name} {dep.version or ''} — {dep.license_spdx}")
    return "\n".join(lines) + "\n"


def write_outputs(result: AnalysisResult, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.md").write_text(render_markdown(result), encoding="utf-8")
    (out_dir / "analysis.json").write_text(
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "graph.json").write_text(
        json.dumps(build_graph(result), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "remediation.json").write_text(
        json.dumps([item.__dict__ for item in result.remediations], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "notice.md").write_text(render_notice(result), encoding="utf-8")
