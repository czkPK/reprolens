from __future__ import annotations

from html import escape

from .models import AuditResult


STATUS_LABELS = {
    "pass": "PASS",
    "partial": "PARTIAL",
    "missing": "MISSING",
    "not_applicable": "N/A",
}


def render_html(result: AuditResult) -> str:
    def e(value: object) -> str:
        return escape(str(value))

    dim_cards = "".join(
        f'<div class="card"><div class="label">{e(dim.name)}</div><div class="value">{dim.percent:.1f}%</div><div class="sub">{dim.points:.1f}/{dim.max_points:.1f}</div></div>'
        for dim in result.dimensions
    )
    criteria_rows = "".join(
        f'<tr><td>{e(item.id)}</td><td>{e(item.dimension)}</td><td>{e(item.title)}</td><td><span class="status {e(item.status)}">{e(STATUS_LABELS.get(item.status, item.status))}</span></td><td>{item.points:.1f}/{item.max_points:.1f}</td><td>{e(", ".join(item.evidence_ids) or "-")}</td></tr>'
        for item in result.criteria
    )
    finding_items = "".join(
        f'<li><strong>{e(item.id)} [{e(item.severity.upper())}] {e(item.title)}</strong><br>{e(item.message)}<br><small>Evidence: {e(", ".join(item.evidence_ids) or "none")}</small></li>'
        for item in result.findings
    ) or "<li>No findings.</li>"
    remediation_items = "".join(
        f'<li><strong>{e(item.finding_id)} - {e(item.action)}</strong><br>{e(item.rationale)}<br><small>Cost: {e(item.cost)} | Impact: {e(item.impact)} | Estimated gain: +{item.estimated_score_gain:.1f}</small></li>'
        for item in result.remediations
    ) or "<li>No remediation actions.</li>"
    probe_rows = "".join(
        f'<tr><td>{e(probe.name)}</td><td><span class="status {e(probe.status)}">{e(probe.status.upper())}</span></td><td>{e(probe.returncode if probe.returncode is not None else "-")}</td><td>{probe.duration_seconds:.3f}s</td><td><code>{e(probe.command.replace(chr(10), " ")[:180])}</code></td></tr>'
        for probe in result.probes
    ) or '<tr><td colspan="5">No probes run.</td></tr>'

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ReproLens Audit Report</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; background: #f5f7fb; color: #172033; }}
main {{ max-width: 1180px; margin: 0 auto; padding: 32px 20px 60px; }}
h1 {{ margin: 0 0 8px; font-size: 30px; }}
h2 {{ margin-top: 32px; border-bottom: 1px solid #dbe2ee; padding-bottom: 8px; }}
.meta {{ color: #5f6b7a; font-size: 14px; }}
.score {{ display: flex; gap: 24px; align-items: center; background: white; border-radius: 16px; padding: 24px; margin: 22px 0; box-shadow: 0 8px 24px rgba(23,32,51,.08); }}
.score .big {{ font-size: 44px; font-weight: 800; color: #2457d6; }}
.badge {{ display: inline-block; padding: 6px 12px; border-radius: 999px; background: #e8eefc; color: #2457d6; font-weight: 700; }}
.cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }}
.card {{ background: white; border-radius: 12px; padding: 16px; box-shadow: 0 4px 14px rgba(23,32,51,.06); }}
.card .label {{ color: #5f6b7a; font-size: 13px; }}
.card .value {{ font-size: 26px; font-weight: 800; color: #2457d6; margin: 6px 0; }}
.card .sub {{ color: #8490a1; font-size: 12px; }}
table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 14px rgba(23,32,51,.06); }}
th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid #edf1f7; font-size: 13px; vertical-align: top; }}
th {{ background: #eef3fb; color: #40506a; }}
.status {{ display: inline-block; padding: 3px 8px; border-radius: 999px; font-size: 12px; font-weight: 700; }}
.status.pass {{ background: #e4f7ec; color: #167a3a; }}
.status.partial {{ background: #fff4db; color: #9a6500; }}
.status.missing {{ background: #ffe5e8; color: #b42336; }}
.status.not_applicable {{ background: #edf0f4; color: #697386; }}
.status.fail, .status.timeout, .status.error {{ background: #ffe5e8; color: #b42336; }}
.status.skip {{ background: #edf0f4; color: #697386; }}
ul {{ background: white; border-radius: 12px; padding: 18px 24px 18px 42px; box-shadow: 0 4px 14px rgba(23,32,51,.06); }}
li {{ margin: 12px 0; line-height: 1.55; }}
code {{ background: #f1f4f9; padding: 2px 5px; border-radius: 4px; word-break: break-all; }}
small {{ color: #697386; }}
</style>
</head>
<body><main>
<h1>ReproLens Audit Report</h1>
<div class="meta">Repository: {e(result.repo_path)}<br>Generated: {e(result.generated_at)} | Files scanned: {result.files_scanned}</div>
<div class="score"><div><div class="big">{result.total_score:.1f}</div><div class="meta">out of 100</div></div><div><span class="badge">{e(result.readiness)}</span><p class="meta">开源 LLM/RAG/Agent 项目复现就绪度</p></div></div>
<h2>Dimension Scores</h2><div class="cards">{dim_cards}</div>
<h2>Criteria</h2><table><thead><tr><th>ID</th><th>Dimension</th><th>Criterion</th><th>Status</th><th>Points</th><th>Evidence</th></tr></thead><tbody>{criteria_rows}</tbody></table>
<h2>Findings</h2><ul>{finding_items}</ul>
<h2>Execution Evidence</h2><table><thead><tr><th>Probe</th><th>Status</th><th>Return code</th><th>Duration</th><th>Command</th></tr></thead><tbody>{probe_rows}</tbody></table>
<h2>Minimal Remediation Plan</h2><ul>{remediation_items}</ul>
<h2>Scope and Limitations</h2><ul><li>This is static reproduction readiness analysis, not proof that the project reproduces successfully.</li><li>No untrusted repository code is executed by default.</li><li>Execution probes run repository scripts only with <code>--execute</code>.</li><li>AI-generated explanations must be reviewed by the team before release.</li></ul>
</main></body></html>"""
