from __future__ import annotations

from html import escape

from .claims import build_claim_matrix, claim_verification_note, criterion_confidence, evidence_coverage, evidence_explanation
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


def render_html(result: AuditResult) -> str:
    def e(value: object) -> str:
        return escape(str(value))

    def evidence_links(ids: list[str]) -> str:
        if not ids:
            return "-"
        return " ".join(
            f'<a class="evidence-link" href="#evidence-{e(evidence_id)}"><code>{e(evidence_id)}</code></a>'
            for evidence_id in ids
        )

    if result.evidence_coverage:
        coverage = result.evidence_coverage
    else:
        covered, total, percent = evidence_coverage(result.criteria)
        coverage = {"covered": covered, "total": total, "percent": percent}
    claims = result.claim_matrix or build_claim_matrix(result)
    claim_counts = {key: 0 for key in CLAIM_STATUS_LABELS}
    for row in claims:
        status = str(row.get("status", ""))
        claim_counts[status] = claim_counts.get(status, 0) + 1
    attention_count = claim_counts.get("partially_verified", 0) + claim_counts.get("unverified", 0)

    summary_cards = (
        f'<div class="card"><div class="label">Evidence coverage</div><div class="value">{coverage["percent"]:.1f}%</div><div class="sub">{coverage["covered"]}/{coverage["total"]} applicable criteria</div></div>'
        f'<div class="card"><div class="label">README claims</div><div class="value">{len(claims)}</div><div class="sub">extracted and mapped</div></div>'
        f'<div class="card"><div class="label">Verified claims</div><div class="value">{claim_counts.get("verified", 0)}</div><div class="sub">all mapped checks pass</div></div>'
        f'<div class="card"><div class="label">Needs evidence</div><div class="value">{attention_count}</div><div class="sub">partial or unverified</div></div>'
    )
    dim_cards = "".join(
        f'<div class="card"><div class="label">{e(dim.name)}</div><div class="value">{dim.percent:.1f}%</div><div class="sub">{dim.points:.1f}/{dim.max_points:.1f}</div></div>'
        for dim in result.dimensions
    )
    criteria_rows = "".join(
        f'<tr><td>{e(item.id)}</td><td>{e(item.dimension)}</td><td>{e(item.title)}</td><td><span class="status {e(item.status)}">{e(STATUS_LABELS.get(item.status, item.status))}</span></td><td><span class="confidence {e("not_applicable" if criterion_confidence(item) == "N/A" else criterion_confidence(item).lower())}">{e(criterion_confidence(item).upper())}</span></td><td>{item.points:.1f}/{item.max_points:.1f}</td><td>{evidence_links(item.evidence_ids)}</td><td class="evidence-explanation">{e(evidence_explanation(item, result.evidence))}</td></tr>'
        for item in result.criteria
    )
    claim_rows = "".join(
        f'<tr><td><a class="evidence-link" href="#evidence-{e(row.get("claim_id", ""))}"><code>{e(row.get("claim_id", "-"))}</code></a></td><td>{e(row.get("claim", ""))}</td><td><span class="status {e(row.get("status", ""))}">{e(CLAIM_STATUS_LABELS.get(row.get("status", ""), row.get("status", "")))}</span></td><td>{e(", ".join(row.get("criteria", [])) or "-")}</td><td>{e(", ".join(row.get("gaps", [])) or "-")}</td><td>{evidence_links(row.get("evidence_ids", []))}</td><td class="evidence-explanation">{e(claim_verification_note(row))}</td></tr>'
        for row in claims
    ) or '<tr><td colspan="7">未抽取到 README 声明。</td></tr>'
    finding_items = "".join(
        f'<li><strong>{e(item.id)} [{e(item.severity.upper())}] {e(item.title)}</strong><br>{e(item.message)}<br><small>Evidence: {evidence_links(item.evidence_ids)}</small></li>'
        for item in result.findings
    ) or "<li>No findings.</li>"
    remediation_items = "".join(
        f'<li><strong>{e(item.finding_id)} - {e(item.action)}</strong><br>{e(item.rationale)}<br><small>Cost: {e(item.cost)} | Impact: {e(item.impact)} | Estimated gain: +{item.estimated_score_gain:.1f}</small></li>'
        for item in result.remediations
    ) or "<li>No remediation actions.</li>"
    top_actions = sorted(result.remediations, key=lambda item: item.estimated_score_gain, reverse=True)[:3]
    priority_items = "".join(
        f'<li><strong>+{item.estimated_score_gain:.1f}</strong> {e(item.action)}<br><small>{e(item.rationale)}</small></li>'
        for item in top_actions
    ) or "<li>No priority actions.</li>"
    probe_rows = "".join(
        f'<tr><td>{e(probe.name)}</td><td><span class="status {e(probe.status)}">{e(probe.status.upper())}</span></td><td>{e(probe.returncode if probe.returncode is not None else "-")}</td><td>{probe.duration_seconds:.3f}s</td><td><code>{e(probe.command.replace(chr(10), " ")[:180])}</code></td></tr>'
        for probe in result.probes
    ) or '<tr><td colspan="5">No probes run.</td></tr>'
    evidence_rows = "".join(
        f'<tr id="evidence-{e(item.id)}"><td><code>{e(item.id)}</code></td><td>{e(item.kind)}</td><td><code>{e(item.path)}</code>{f":{item.line}" if item.line else ""}</td><td>{e(item.excerpt)}</td></tr>'
        for item in result.evidence
    ) or '<tr><td colspan="4">No evidence extracted.</td></tr>'
    source_meta = ""
    if result.source_url:
        source_meta = f'<br>Source: <a href="{e(result.source_url)}" target="_blank" rel="noopener noreferrer">{e(result.source_url)}</a>'
        if result.source_commit:
            source_meta += f' @ <code>{e(result.source_commit[:12])}</code>'
    ai_meta = ""
    if result.ai_metadata:
        ai_meta = f'<br>Semantic claim mapping: <strong>{e(result.ai_metadata.get("mode", "rules"))}</strong>'

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
.cards.summary {{ margin-top: 18px; }}
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
.status.verified {{ background: #e4f7ec; color: #167a3a; }}
.status.partially_verified {{ background: #fff4db; color: #9a6500; }}
.status.unverified {{ background: #ffe5e8; color: #b42336; }}
.status.not_applicable {{ background: #edf0f4; color: #697386; }}
.status.fail, .status.timeout, .status.error {{ background: #ffe5e8; color: #b42336; }}
.status.skip {{ background: #edf0f4; color: #697386; }}
.confidence {{ display: inline-block; padding: 3px 8px; border-radius: 999px; font-size: 11px; font-weight: 700; background: #edf0f4; color: #526175; }}
.confidence.high {{ background: #e4f7ec; color: #167a3a; }}
.confidence.medium {{ background: #fff4db; color: #9a6500; }}
.confidence.low {{ background: #ffe5e8; color: #b42336; }}
.evidence-link {{ color: #2457d6; text-decoration: none; }}
.evidence-link:hover {{ text-decoration: underline; }}
tr:target {{ background: #fff8dc; }}
.table-scroll {{ overflow-x: auto; }}
.evidence-explanation {{ min-width: 300px; color: #526175; line-height: 1.55; }}
.table-help {{ color: #5f6b7a; font-size: 13px; line-height: 1.65; margin: 8px 0 12px; }}
ul {{ background: white; border-radius: 12px; padding: 18px 24px 18px 42px; box-shadow: 0 4px 14px rgba(23,32,51,.06); }}
.priority {{ background: linear-gradient(135deg,#eef3fb,#f8faff); border: 1px solid #dbe4f0; border-radius: 12px; padding: 18px 22px; }}
.priority li {{ margin: 10px 0; }}
li {{ margin: 12px 0; line-height: 1.55; }}
code {{ background: #f1f4f9; padding: 2px 5px; border-radius: 4px; word-break: break-all; }}
small {{ color: #697386; }}
</style>
</head>
<body><main>
<h1>ReproLens Audit Report</h1>
<div class="meta">Repository: {e(result.repo_path)}<br>Generated: {e(result.generated_at)} | Files scanned: {result.files_scanned}{source_meta}{ai_meta}</div>
<div class="score"><div><div class="big">{result.total_score:.1f}</div><div class="meta">out of 100</div></div><div><span class="badge">{e(result.readiness)}</span><p class="meta">开源 LLM/RAG/Agent 项目复现就绪度</p><img src="badge.svg" alt="ReproLens badge" style="max-width:310px;height:28px"></div></div>
<h2>Evidence Overview</h2><div class="cards summary">{summary_cards}</div>
<h2>Top 3 Priority Actions</h2><ul class="priority">{priority_items}</ul>
<h2>Dimension Scores</h2><div class="cards">{dim_cards}</div>
<h2>Criteria（检查项）</h2><p class="table-help"><strong>读表说明：</strong>PASS = 满足要求；PARTIAL = 只有部分证据；MISSING = 应有但没有找到；N/A = 当前项目类型不适用。Confidence 表示证据支持强度，不代表项目整体质量。</p><div class="table-scroll"><table><thead><tr><th>检查项编号</th><th>所属维度</th><th>检查要求</th><th>状态</th><th>证据强度</th><th>得分</th><th>证据编号</th><th>证据说明</th></tr></thead><tbody>{criteria_rows}</tbody></table></div>
<h2>Claim-Evidence Matrix（声明验证矩阵）</h2><p class="table-help"><strong>读表方法：</strong>每一行先看 README 原句，再看验证状态、需要检查的项、缺口和支持证据。<br><strong>已验证</strong> = 相关检查项全部通过；<strong>部分验证</strong> = 找到部分证据但仍有缺口；<strong>未验证</strong> = 关键证据缺失；<strong>不适用</strong> = 该声明对应的检查项不适用于此项目。</p><div class="table-scroll"><table><thead><tr><th>声明编号</th><th>README 声明</th><th>验证状态</th><th>需要检查的项</th><th>缺口</th><th>支持证据</th><th>验证说明</th></tr></thead><tbody>{claim_rows}</tbody></table></div>
<h2>Evidence Appendix（证据附录）</h2><p class="meta">证据编号链接到对应文件、行号和原文摘录。</p><table><thead><tr><th>证据编号</th><th>证据类型</th><th>文件位置</th><th>原文摘录</th></tr></thead><tbody>{evidence_rows}</tbody></table>
<h2>Findings</h2><ul>{finding_items}</ul>
<h2>Execution Evidence</h2><table><thead><tr><th>Probe</th><th>Status</th><th>Return code</th><th>Duration</th><th>Command</th></tr></thead><tbody>{probe_rows}</tbody></table>
<h2>Minimal Remediation Plan</h2><ul>{remediation_items}</ul>
<h2>Scope and Limitations</h2><ul><li>This is static reproduction readiness analysis, not proof that the project reproduces successfully.</li><li>No untrusted repository code is executed by default.</li><li>Execution probes run repository scripts only with <code>--execute</code>.</li><li>AI-generated explanations must be reviewed by the team before release.</li></ul>
</main></body></html>"""
