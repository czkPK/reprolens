from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .models import AnalysisResult, UsageMode
from .remediation import plan_remediations
from .report import write_outputs
from .resolver import project_license_override, resolve_dependencies
from .rules import analyze_dependencies


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="licenselens",
        description="Evidence-constrained open-source license conflict diagnosis.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze = subparsers.add_parser("analyze", help="Analyze a local project directory.")
    analyze.add_argument("path", help="Project directory or repository path.")
    analyze.add_argument(
        "--usage",
        choices=[mode.value for mode in UsageMode],
        default=UsageMode.INTERNAL.value,
        help="How the project will be used or distributed.",
    )
    analyze.add_argument("--project-license", default=None, help="Declared project license, e.g. MIT or Apache-2.0.")
    analyze.add_argument("--out-dir", default="licenselens-output", help="Directory for report files.")
    analyze.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Print a compact result.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command != "analyze":
        parser.error("unknown command")

    root = Path(args.path).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"project directory not found: {root}")

    dependencies = resolve_dependencies(root)
    project_license = args.project_license or project_license_override(root)
    usage = UsageMode(args.usage)
    findings = analyze_dependencies(dependencies, usage, project_license)
    remediations = plan_remediations(findings)
    result = AnalysisResult(
        project_root=str(root),
        usage_mode=usage.value,
        project_license=project_license,
        dependencies=dependencies,
        findings=findings,
        remediations=remediations,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
    out_dir = Path(args.out_dir).expanduser().resolve()
    write_outputs(result, out_dir)

    if args.format == "json":
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"LicenseLens analyzed {len(dependencies)} dependencies.")
        print(f"Findings: {len(findings)}; remediation actions: {len(remediations)}")
        print(f"Report: {out_dir / 'report.md'}")
    return 0
