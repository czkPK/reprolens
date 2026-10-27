from __future__ import annotations

from html import escape

from .claims import build_claim_matrix, claim_verification_note, criterion_confidence, evidence_coverage, evidence_explanation, evidence_reference_entries, format_criterion_references
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

    def evidence_links(ids: list[str], *, stacked: bool = False) -> str:
        if not ids:
            return "-"
        links = [
            f'<a class="evidence-link" href="#evidence-{e(entry["id"])}" title="{e(entry["location"] + ("：" + entry["excerpt"] if entry["excerpt"] else ""))}"><code>{e(entry["id"])}</code></a>'
            for entry in evidence_reference_entries(ids, result.evidence)
        ]
        if stacked:
            return f'<div class="evidence-id-list">{"".join(links)}</div>'
        return " ".join(links)

    def claim_source_id(row: dict) -> str:
        return str(row.get("source_evidence_id") or row.get("claim_id", ""))

    def evidence_details(ids: list[str]) -> str:
        items = []
        for entry in evidence_reference_entries(ids, result.evidence):
            excerpt = f'<div class="evidence-excerpt">“{e(entry["excerpt"])}”</div>' if entry["excerpt"] else ""
            items.append(
                f'<div class="evidence-item"><a class="evidence-link" href="#evidence-{e(entry["id"])}"><code>{e(entry["id"])}</code></a> '
                f'<span class="evidence-location">{e(entry["location"])}</span>{excerpt}</div>'
            )
        return "".join(items) or "-"

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
        f'<tr><td>{e(item.id)}</td><td>{e(item.dimension)}</td><td>{e(item.title)}</td><td><span class="status {e(item.status)}">{e(STATUS_LABELS.get(item.status, item.status))}</span></td><td><span class="confidence {e("not_applicable" if criterion_confidence(item) == "N/A" else criterion_confidence(item).lower())}">{e(criterion_confidence(item).upper())}</span></td><td>{item.points:.1f}/{item.max_points:.1f}</td><td>{evidence_links(item.evidence_ids, stacked=True)}</td><td class="evidence-explanation">{e(evidence_explanation(item, result.evidence, result.project_type, result.model_agnostic))}</td></tr>'
        for item in result.criteria
    )
    claim_rows = "".join(
        f'<tr><td><a class="evidence-link" href="#evidence-{e(claim_source_id(row))}"><code>{e(row.get("claim_id", "-"))}</code></a></td><td>{e(row.get("claim", ""))}</td><td><span class="status {e(row.get("status", ""))}">{e(CLAIM_STATUS_LABELS.get(row.get("status", ""), row.get("status", "")))}</span></td><td>{e(format_criterion_references(row.get("criteria", []), result.criteria))}</td><td>{e(format_criterion_references(row.get("gaps", []), result.criteria))}</td><td>{evidence_details(row.get("evidence_ids", []))}</td><td class="evidence-explanation">{e(claim_verification_note(row, result.criteria))}</td></tr>'
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
        f'<tr id="evidence-{e(item.id)}"><td><code>{e(item.id)}</code></td><td>{e(item.kind)}</td><td><code class="evidence-path">{e(item.path)}</code>{f":{item.line}" if item.line else ""}</td><td class="evidence-raw">{e(item.excerpt)}</td></tr>'
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
table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: visible; box-shadow: 0 4px 14px rgba(23,32,51,.06); }}
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
.sticky-scroll {{ max-height: 72vh; overflow: auto; border-radius: 12px; scrollbar-gutter: stable; }}
.sticky-scroll table {{ border-collapse: separate; border-spacing: 0; overflow: visible; }}
.sticky-scroll th, .sticky-scroll td {{ box-sizing: border-box; background-clip: padding-box; }}
.sticky-scroll thead th {{ position: sticky; top: 0; z-index: 10; background: #eaf0fa; }}
.sticky-scroll tbody td:nth-child(1), .sticky-scroll thead th:nth-child(1) {{ position: sticky; left: 0; }}
.sticky-scroll tbody td:nth-child(1) {{ z-index: 5; background: #fff; }}
.sticky-scroll thead th:nth-child(1) {{ z-index: 12; background: #eaf0fa; }}
.sticky-scroll tbody td:nth-child(2) {{ position: sticky; z-index: 5; background: #fff; box-shadow: 2px 0 6px rgba(23,32,51,.08); }}
.sticky-scroll thead th:nth-child(2) {{ position: sticky; z-index: 12; background: #eaf0fa; box-shadow: 2px 0 6px rgba(23,32,51,.08); }}
.criteria-table th:nth-child(2), .criteria-table td:nth-child(2) {{ left: 88px; }}
.claim-table th:nth-child(2), .claim-table td:nth-child(2) {{ left: 92px; }}
.evidence-explanation {{ min-width: 300px; color: #526175; line-height: 1.55; }}
.table-help {{ color: #5f6b7a; font-size: 13px; line-height: 1.65; margin: 8px 0 12px; }}
.criteria-table {{ table-layout: fixed; width: 1260px; min-width: 1260px; }}
.criteria-table th:nth-child(1), .criteria-table td:nth-child(1) {{ width: 88px; white-space: nowrap; }}
.criteria-table th:nth-child(2), .criteria-table td:nth-child(2) {{ width: 105px; }}
.criteria-table th:nth-child(3), .criteria-table td:nth-child(3) {{ width: 235px; }}
.criteria-table th:nth-child(4), .criteria-table td:nth-child(4) {{ width: 88px; }}
.criteria-table th:nth-child(5), .criteria-table td:nth-child(5) {{ width: 95px; }}
.criteria-table th:nth-child(6), .criteria-table td:nth-child(6) {{ width: 82px; }}
.criteria-table th:nth-child(7) {{ width: 160px; white-space: nowrap; }}
.criteria-table td:nth-child(7) {{ width: 160px; white-space: normal; overflow-wrap: anywhere; }}
.criteria-table th:nth-child(8), .criteria-table td:nth-child(8) {{ width: 407px; }}
.evidence-id-list {{ display: flex; flex-wrap: wrap; align-items: flex-start; align-content: flex-start; gap: 6px; min-width: 0; }}
.evidence-id-list .evidence-link {{ display: inline-flex; max-width: 100%; }}
.evidence-id-list code {{ display: inline-block; padding: 3px 7px; border: 1px solid #d8e4f8; border-radius: 6px; background: #f4f8ff; color: #2457d6; font-size: 12px; line-height: 1.2; white-space: nowrap; }}
.evidence-scroll {{ max-height: 72vh; overflow: auto; border-radius: 12px; scrollbar-gutter: stable; }}
.evidence-table {{ width: 1280px; min-width: 1280px; table-layout: fixed; border-collapse: separate; border-spacing: 0; overflow: visible; }}
.evidence-table th, .evidence-table td {{ box-sizing: border-box; background-clip: padding-box; vertical-align: top; }}
.evidence-table thead th {{ position: sticky; top: 0; z-index: 10; background: #eaf0fa; white-space: nowrap; }}
.evidence-table tbody td:first-child, .evidence-table thead th:first-child {{ position: sticky; left: 0; }}
.evidence-table tbody td:first-child {{ z-index: 5; background: #fff; box-shadow: 2px 0 6px rgba(23,32,51,.08); }}
.evidence-table thead th:first-child {{ z-index: 12; background: #eaf0fa; box-shadow: 2px 0 6px rgba(23,32,51,.08); }}
.evidence-table th:nth-child(1), .evidence-table td:nth-child(1) {{ width: 96px; white-space: nowrap; }}
.evidence-table th:nth-child(2), .evidence-table td:nth-child(2) {{ width: 144px; }}
.evidence-table th:nth-child(3), .evidence-table td:nth-child(3) {{ width: 390px; }}
.evidence-table th:nth-child(4), .evidence-table td:nth-child(4) {{ width: 650px; }}
.evidence-table td:nth-child(3), .evidence-table td:nth-child(4) {{ overflow-wrap: anywhere; word-break: break-word; line-height: 1.6; }}
.evidence-table code {{ white-space: normal; word-break: break-word; }}
.evidence-table tr:target td, .evidence-table tr:target td:first-child {{ background: #fff8dc; }}
.claim-table {{ table-layout: fixed; width: 1500px; min-width: 1500px; }}
.claim-table th:nth-child(1), .claim-table td:nth-child(1) {{ width: 92px; white-space: nowrap; }}
.claim-table th:nth-child(2), .claim-table td:nth-child(2) {{ width: 380px; }}
.claim-table th:nth-child(3), .claim-table td:nth-child(3) {{ width: 98px; }}
.claim-table th:nth-child(4), .claim-table td:nth-child(4) {{ width: 165px; }}
.claim-table th:nth-child(5), .claim-table td:nth-child(5) {{ width: 105px; }}
.claim-table th:nth-child(6), .claim-table td:nth-child(6) {{ width: 340px; }}
.claim-table th:nth-child(7), .claim-table td:nth-child(7) {{ width: 320px; }}
.evidence-item {{ margin: 0 0 8px; }}
.evidence-location {{ color: #2457d6; font-size: 12px; }}
.evidence-excerpt {{ color: #697386; font-size: 12px; line-height: 1.45; margin-top: 2px; }}
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
<h2 id="criteria">Criteria（检查项）</h2><p class="table-help"><strong>读表说明：</strong>PASS = 满足要求；PARTIAL = 只有部分证据；MISSING = 应有但没有找到；N/A = 当前项目类型不适用。Confidence 表示证据支持强度，不代表项目整体质量。<br><strong>证据编号（E-xxx）</strong> = 仓库中的原始证据编号。点击可跳到证据附录；鼠标悬停可查看文件、行号和原文；右侧“证据说明”会直接解释该编号对应什么内容。<br><strong>表格已固定首行和前两列，可在表格内滚动。</strong></p><div class="table-scroll sticky-scroll"><table class="criteria-table"><thead><tr><th>检查项编号</th><th>所属维度</th><th>检查要求</th><th>状态</th><th>证据强度</th><th>得分</th><th>证据编号<br>（E-xxx）</th><th>证据说明<br>（文件、行号、原文）</th></tr></thead><tbody>{criteria_rows}</tbody></table></div>
<h2 id="claims">Claim-Evidence Matrix（声明验证矩阵）</h2><p class="table-help"><strong>读表方法：</strong>每一行先看 README 原句，再看验证状态、检查依据、缺口和支持证据。检查项编号后面的括号是中文含义。<br><strong>检查依据（需要检查的项）</strong> = 要验证这句话，必须检查哪些规则。<br><strong>还缺什么（缺口）</strong> = 这些规则中哪些还没有满足；显示“-”表示没有缺口。<br><strong>已验证</strong> = 相关检查项全部通过；<strong>部分验证</strong> = 找到部分证据但仍有缺口；<strong>未验证</strong> = 关键证据缺失；<strong>不适用</strong> = 该声明对应的检查项不适用于此项目。<br><strong>表格已固定首行和前两列，可在表格内滚动。</strong></p><div class="table-scroll sticky-scroll"><table class="claim-table"><thead><tr><th>声明编号</th><th>README 声明</th><th>验证状态</th><th>检查依据<br>（需要检查的项）</th><th>还缺什么<br>（缺口）</th><th>支持证据</th><th>验证说明</th></tr></thead><tbody>{claim_rows}</tbody></table></div>
<h2 id="evidence">Evidence Appendix（证据附录）</h2><p class="table-help"><strong>用途：</strong>这里保存每条证据的编号、类型、文件位置和原文。表格固定首行和“证据编号”列，可横向、纵向滚动；长文件路径和原文会自动换行。</p><div class="evidence-scroll"><table class="evidence-table"><thead><tr><th>证据编号</th><th>证据类型</th><th>文件位置</th><th>原文摘录</th></tr></thead><tbody>{evidence_rows}</tbody></table></div>
<h2>Findings</h2><ul>{finding_items}</ul>
<h2>Execution Evidence</h2><table><thead><tr><th>Probe</th><th>Status</th><th>Return code</th><th>Duration</th><th>Command</th></tr></thead><tbody>{probe_rows}</tbody></table>
<h2>Minimal Remediation Plan</h2><ul>{remediation_items}</ul>
<h2>Scope and Limitations</h2><ul><li>This is static reproduction readiness analysis, not proof that the project reproduces successfully.</li><li>No untrusted repository code is executed by default.</li><li>Execution probes run repository scripts only with <code>--execute</code>.</li><li>AI-generated explanations must be reviewed by the team before release.</li></ul>
</main></body></html>"""


def render_claims_html(result: AuditResult) -> str:
    def e(value: object) -> str:
        return escape(str(value))

    claims = result.claim_matrix or build_claim_matrix(result)
    counts = {key: 0 for key in CLAIM_STATUS_LABELS}
    for row in claims:
        status = str(row.get("status", ""))
        counts[status] = counts.get(status, 0) + 1
    coverage = result.evidence_coverage or {}
    if not coverage:
        covered, total, percent = evidence_coverage(result.criteria)
        coverage = {"covered": covered, "total": total, "percent": percent}

    def evidence_links(ids: list[str]) -> str:
        items = []
        for entry in evidence_reference_entries(ids, result.evidence):
            excerpt = f'<div class="evidence-excerpt">“{e(entry["excerpt"])}”</div>' if entry["excerpt"] else ""
            items.append(
                f'<div class="evidence-item"><a href="report.html#evidence-{e(entry["id"])}"><code>{e(entry["id"])}</code></a> '
                f'<span class="evidence-location">{e(entry["location"])}</span>{excerpt}</div>'
            )
        return "".join(items) or "-"

    def claim_source_id(row: dict) -> str:
        return str(row.get("source_evidence_id") or row.get("claim_id", ""))

    cards = (
        f'<div class="card"><div class="label">README 声明</div><div class="value">{len(claims)}</div><div class="sub">从根 README 抽取</div></div>'
        f'<div class="card"><div class="label">已验证</div><div class="value">{counts.get("verified", 0)}</div><div class="sub">相关检查项全部通过</div></div>'
        f'<div class="card"><div class="label">部分验证</div><div class="value">{counts.get("partially_verified", 0)}</div><div class="sub">有证据但仍有缺口</div></div>'
        f'<div class="card"><div class="label">证据覆盖</div><div class="value">{coverage.get("percent", 0):.1f}%</div><div class="sub">{coverage.get("covered", 0)}/{coverage.get("total", 0)} 个适用检查项</div></div>'
    )
    rows = "".join(
        '<tr>'
        f'<td><a href="report.html#evidence-{e(claim_source_id(row))}"><code>{e(row.get("claim_id", "-"))}</code></a></td>'
        f'<td>{e(row.get("claim", ""))}</td>'
        f'<td><span class="status {e(row.get("status", ""))}">{e(CLAIM_STATUS_LABELS.get(row.get("status", ""), row.get("status", "")))}</span></td>'
        f'<td>{e(format_criterion_references(row.get("criteria", []), result.criteria))}</td>'
        f'<td>{e(format_criterion_references(row.get("gaps", []), result.criteria))}</td>'
        f'<td>{evidence_links(row.get("evidence_ids", []))}</td>'
        f'<td class="note">{e(claim_verification_note(row, result.criteria))}</td>'
        '</tr>'
        for row in claims
    ) or '<tr><td colspan="7">未抽取到 README 声明。</td></tr>'

    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ReproLens 声明验证矩阵</title>
<style>
body {{ margin:0; background:#f4f7fc; color:#172033; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif; }}
main {{ max-width:1380px; margin:0 auto; padding:38px 22px 70px; }}
h1 {{ margin:0 0 8px; font-size:32px; }}
h2 {{ margin-top:30px; border-bottom:1px solid #dbe4f0; padding-bottom:9px; }}
.meta {{ color:#64748b; line-height:1.7; }}
.cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:12px; margin:22px 0; }}
.card {{ background:white; border-radius:14px; padding:16px; box-shadow:0 5px 18px rgba(23,32,51,.07); }}
.label,.sub {{ color:#64748b; font-size:13px; }}
.value {{ color:#2457d6; font-size:28px; font-weight:800; margin:5px 0; }}
.guide {{ background:#eef3fb; border:1px solid #dbe4f0; border-radius:14px; padding:16px 20px; line-height:1.75; }}
.table-scroll {{ max-height:72vh; overflow:auto; border-radius:14px; scrollbar-gutter:stable; }}
table {{ width:100%; border-collapse:separate; border-spacing:0; background:white; border-radius:14px; overflow:visible; box-shadow:0 5px 18px rgba(23,32,51,.07); table-layout:fixed; min-width:1350px; }}
th,td {{ box-sizing:border-box; padding:12px; border-bottom:1px solid #edf1f7; text-align:left; vertical-align:top; font-size:13px; line-height:1.6; background-clip:padding-box; }}
th {{ background:#eaf0fa; color:#40506a; }}
thead th {{ position:sticky; top:0; z-index:10; background:#eaf0fa; }}
td:nth-child(1), th:nth-child(1) {{ position:sticky; left:0; }}
td:nth-child(1) {{ z-index:5; background:#fff; }}
th:nth-child(1) {{ z-index:12; }}
td:nth-child(2), th:nth-child(2) {{ position:sticky; left:92px; }}
td:nth-child(2) {{ z-index:5; background:#fff; box-shadow:2px 0 6px rgba(23,32,51,.08); }}
th:nth-child(2) {{ z-index:12; box-shadow:2px 0 6px rgba(23,32,51,.08); }}
.status {{ display:inline-block; border-radius:999px; padding:4px 9px; font-weight:700; white-space:nowrap; }}
.status.verified {{ background:#e4f7ec; color:#167a3a; }}
.status.partially_verified {{ background:#fff4db; color:#9a6500; }}
.status.unverified {{ background:#ffe5e8; color:#b42336; }}
.status.not_applicable {{ background:#edf0f4; color:#697386; }}
.note {{ min-width:260px; color:#526175; }}
td:first-child {{ white-space:nowrap; }}
th:nth-child(1), td:nth-child(1) {{ width:92px; }}
th:nth-child(2), td:nth-child(2) {{ width:31%; }}
th:nth-child(3), td:nth-child(3) {{ width:98px; }}
th:nth-child(4), td:nth-child(4) {{ width:165px; }}
th:nth-child(5), td:nth-child(5) {{ width:105px; }}
th:nth-child(6), td:nth-child(6) {{ width:300px; }}
th:nth-child(7), td:nth-child(7) {{ width:250px; }}
.claim-table {{ table-layout:fixed; width:1500px; min-width:1500px; }}
.claim-table th:nth-child(2), .claim-table td:nth-child(2) {{ width:380px; }}
.claim-table th:nth-child(6), .claim-table td:nth-child(6) {{ width:340px; }}
.claim-table th:nth-child(7), .claim-table td:nth-child(7) {{ width:320px; }}
.evidence-item {{ margin:0 0 8px; }}
.evidence-location {{ color:#2457d6; font-size:12px; }}
.evidence-excerpt {{ color:#697386; font-size:12px; line-height:1.45; margin-top:2px; }}
code {{ background:#f1f4f9; border-radius:4px; padding:2px 5px; word-break:break-all; }}
a {{ color:#2457d6; text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
.back {{ display:inline-block; margin-top:24px; font-weight:700; }}
</style>
</head>
<body><main>
<h1>ReproLens 声明验证矩阵</h1>
<div class="meta">仓库：{e(result.repo_path)}<br>生成时间：{e(result.generated_at)}</div>
<div class="cards">{cards}</div>
<div class="guide"><strong>怎么看这张表：</strong><br>
先看“README 声明”项目声称了什么；再看“验证状态”是否可信；<br>
“检查依据”是验证这句话必须检查的规则，编号后的括号是中文含义；“还缺什么”是这些规则中还没满足的部分，显示“-”表示没有缺口；<br>
“支持证据”中的 E-xxx 可以点击，跳转到完整报告中的文件、行号和原文。</div>
<h2>声明列表</h2>
<p class="guide"><strong>表格已固定首行和前两列</strong>，可在表格内横向和纵向滚动。点击 E-xxx 可查看完整报告中的证据原文。</p><div class="table-scroll sticky-scroll"><table class="claim-table"><thead><tr><th>声明编号</th><th>README 声明</th><th>验证状态</th><th>检查依据<br>（需要检查的项）</th><th>还缺什么<br>（缺口）</th><th>支持证据</th><th>验证说明</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>状态说明</h2>
<div class="guide"><strong>已验证</strong>：相关检查项全部通过，并且有证据支持。<br>
<strong>部分验证</strong>：找到部分证据，但仍有缺口。<br>
<strong>未验证</strong>：关键证据缺失，当前声明不能视为已验证。<br>
<strong>不适用</strong>：相关检查项不适用于当前项目类型，证据只作为识别线索。</div>
<a class="back" href="report.html">返回完整报告</a>
</main></body></html>'''
