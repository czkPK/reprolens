from __future__ import annotations

import math
from html import escape

from .claims import build_claim_matrix, claim_verification_note, criterion_confidence, evidence_coverage, evidence_explanation, evidence_reference_entries, evidence_type_label, format_criterion_references, format_gap_references
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
        links = []
        for entry in evidence_reference_entries(ids, result.evidence):
            kind_label = entry.get("kind_label") or evidence_type_label(entry.get("kind", ""))
            tooltip = f"{kind_label}；{entry['location']}"
            if entry["excerpt"]:
                tooltip += f"；原文：{entry['excerpt']}"
            links.append(
                f'<a class="evidence-link" href="#evidence-{e(entry["id"])}" title="{e(tooltip)}">'
                f'<code>{e(entry["id"])}</code><span class="evidence-kind">{e(kind_label)}</span></a>'
            )
        if stacked:
            return f'<div class="evidence-id-list">{"".join(links)}</div>'
        return " ".join(links)

    def claim_source_id(row: dict) -> str:
        return str(row.get("source_evidence_id") or row.get("claim_id", ""))

    def evidence_details(ids: list[str]) -> str:
        items = []
        for entry in evidence_reference_entries(ids, result.evidence):
            excerpt = f'<div class="evidence-excerpt">“{e(entry["excerpt"])}”</div>' if entry["excerpt"] else ""
            kind_label = entry.get("kind_label") or evidence_type_label(entry.get("kind", ""))
            items.append(
                f'<div class="evidence-item"><a class="evidence-link" href="#evidence-{e(entry["id"])}"><code>{e(entry["id"])}</code></a> '
                f'<span class="evidence-kind">类型：{e(kind_label)}</span> '
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

    def radar_svg() -> str:
        dims = result.dimensions
        if len(dims) < 3:
            return '<div class="visual-empty">暂无足够维度数据</div>'
        width, height = 430, 340
        cx, cy, radius = 215, 165, 112
        angles = [-math.pi / 2 + 2 * math.pi * index / len(dims) for index in range(len(dims))]

        def point(index: int, scale: float) -> tuple[float, float]:
            angle = angles[index]
            return cx + math.cos(angle) * radius * scale, cy + math.sin(angle) * radius * scale

        def polygon(scale: float) -> str:
            return " ".join(f"{x:.1f},{y:.1f}" for x, y in (point(index, scale) for index in range(len(dims))))

        grids = "".join(
            f'<polygon points="{polygon(level)}" class="radar-grid" />'
            for level in (0.25, 0.5, 0.75, 1.0)
        )
        axes = "".join(
            f'<line x1="{cx}" y1="{cy}" x2="{point(index, 1.0)[0]:.1f}" y2="{point(index, 1.0)[1]:.1f}" class="radar-axis" />'
            for index in range(len(dims))
        )
        values = [max(0.0, min(1.0, dim.percent / 100 if dim.applicable else 0.0)) for dim in dims]
        data_points = " ".join(f"{x:.1f},{y:.1f}" for x, y in (point(index, values[index]) for index in range(len(dims))))
        dots = "".join(
            f'<circle cx="{point(index, values[index])[0]:.1f}" cy="{point(index, values[index])[1]:.1f}" r="4" class="radar-dot" />'
            for index in range(len(dims))
        )
        labels = []
        for index, dim in enumerate(dims):
            x, y = point(index, 1.2)
            cosine = math.cos(angles[index])
            anchor = "middle" if abs(cosine) < 0.25 else ("start" if cosine > 0 else "end")
            if dim.applicable:
                label = f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" class="radar-label">{e(dim.name)}</text>'
            else:
                label = (
                    f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" class="radar-label">'
                    f'<tspan x="{x:.1f}" dy="-0.35em">{e(dim.name)}</tspan>'
                    f'<tspan x="{x:.1f}" dy="1.25em" class="radar-na">N/A</tspan></text>'
                )
            labels.append(label)
        return (
            f'<svg class="radar-svg" viewBox="0 0 {width} {height}" role="img" aria-label="六维复现能力雷达图">'
            f'{grids}{axes}<polygon points="{data_points}" class="radar-area" />{dots}{"".join(labels)}</svg>'
        )

    claim_total = len(claims)
    claim_colors = {
        "verified": "#16a34a",
        "partially_verified": "#f59e0b",
        "unverified": "#dc2626",
        "not_applicable": "#94a3b8",
    }
    segments = []
    start_angle = 0.0
    for key in ("verified", "partially_verified", "unverified", "not_applicable"):
        count = claim_counts.get(key, 0)
        if count <= 0 or claim_total <= 0:
            continue
        end_angle = start_angle + count / claim_total * 360
        segments.append(f"{claim_colors[key]} {start_angle:.2f}deg {end_angle:.2f}deg")
        start_angle = end_angle
    donut_background = f"conic-gradient({', '.join(segments)})" if segments else "conic-gradient(#e9eef8 0deg 360deg)"
    coverage_percent = max(0.0, min(100.0, float(coverage.get("percent", 0))))
    score_value = max(0.0, min(100.0, float(result.total_score)))
    legend = "".join(
        f'<div class="legend-item"><span class="legend-dot" style="background:{claim_colors[key]}"></span>'
        f'<span>{CLAIM_STATUS_LABELS[key]}</span><strong>{claim_counts.get(key, 0)}</strong></div>'
        for key in ("verified", "partially_verified", "unverified", "not_applicable")
    )
    visual_overview = f"""
<section id="visual-overview" class="visual-section">
  <div class="visual-heading"><div><h2>复现诊断总览</h2><p>先看整体强弱，再进入下方逐项证据。</p></div><span class="visual-hint">图表由本次 audit 数据直接生成</span></div>
  <div class="visual-grid">
    <article class="visual-card score-visual">
      <div class="visual-title">综合评分</div>
      <div class="gauge" style="--score-angle:{score_value * 3.6:.1f}deg"><div class="gauge-inner"><strong>{score_value:.1f}</strong><span>/ 100</span></div></div>
      <div class="gauge-caption">{e(result.readiness)}</div>
    </article>
    <article class="visual-card radar-card">
      <div class="visual-title">六维能力雷达</div>
      {radar_svg()}
      <div class="visual-foot">各维度按可用满分归一化。N/A（不适用）表示该维度没有适用检查项，雷达图中按中心点处理，并且不参与总分计算。</div>
    </article>
    <article class="visual-card claims-visual">
      <div class="visual-title">README 声明状态</div>
      <div class="donut-row"><div class="donut" style="background:{donut_background}"><div class="donut-hole"><strong>{claim_total}</strong><span>条声明</span></div></div><div class="legend">{legend}</div></div>
      <div class="coverage-line"><span>证据覆盖率</span><strong>{coverage_percent:.1f}%</strong></div>
      <div class="coverage-track"><div style="width:{coverage_percent:.1f}%"></div></div>
      <div class="visual-foot">{coverage.get("covered", 0)}/{coverage.get("total", 0)} 个适用检查项存在关联证据</div>
    </article>
  </div>
</section>
"""

    summary_cards = (
        f'<div class="card"><div class="label">Evidence coverage（证据覆盖率）</div><div class="value">{coverage["percent"]:.1f}%</div><div class="sub">{coverage["covered"]}/{coverage["total"]} 个适用检查项</div></div>'
        f'<div class="card"><div class="label">README claims（README 声明数）</div><div class="value">{len(claims)}</div><div class="sub">从 README 中抽取并映射</div></div>'
        f'<div class="card"><div class="label">Verified claims（已验证声明）</div><div class="value">{claim_counts.get("verified", 0)}</div><div class="sub">相关检查项全部通过</div></div>'
        f'<div class="card"><div class="label">Needs evidence（仍需证据）</div><div class="value">{attention_count}</div><div class="sub">部分验证或未验证</div></div>'
    )
    dim_cards = "".join(
        (
            f'<div class="card"><div class="label">{e(dim.name)}</div><div class="value">{dim.percent:.1f}%</div><div class="sub">{dim.points:.1f}/{dim.max_points:.1f} 分</div></div>'
            if dim.applicable
            else f'<div class="card"><div class="label">{e(dim.name)}</div><div class="value na">N/A</div><div class="sub">无适用检查项，不计入总分</div></div>'
        )
        for dim in result.dimensions
    )
    criteria_rows = "".join(
        f'<tr><td>{e(item.id)}</td><td>{e(item.dimension)}</td><td>{e(item.title)}</td><td><span class="status {e(item.status)}">{e(STATUS_LABELS.get(item.status, item.status))}</span></td><td><span class="confidence {e("not_applicable" if criterion_confidence(item) == "N/A" else criterion_confidence(item).lower())}">{e(criterion_confidence(item).upper())}</span></td><td>{item.points:.1f}/{item.max_points:.1f}</td><td>{evidence_links(item.evidence_ids, stacked=True)}</td><td class="evidence-explanation">{e(evidence_explanation(item, result.evidence, result.project_type, result.model_agnostic))}</td></tr>'
        for item in result.criteria
    )
    claim_rows = "".join(
        f'<tr><td><a class="evidence-link" href="#evidence-{e(claim_source_id(row))}"><code>{e(row.get("claim_id", "-"))}</code></a></td><td>{e(row.get("claim", ""))}</td><td><span class="status {e(row.get("status", ""))}">{e(CLAIM_STATUS_LABELS.get(row.get("status", ""), row.get("status", "")))}</span></td><td>{e(format_criterion_references(row.get("criteria", []), result.criteria))}</td><td>{e(format_gap_references(row.get("gaps", []), result.criteria))}</td><td>{evidence_details(row.get("evidence_ids", []))}</td><td class="evidence-explanation">{e(claim_verification_note(row, result.criteria))}</td></tr>'
        for row in claims
    ) or '<tr><td colspan="7">未抽取到 README 声明。</td></tr>'
    finding_items = "".join(
        f'<li><strong>{e(item.id)} [{e(item.severity.upper())}] {e(item.title)}</strong><br>{e(item.message)}<br><small>证据（Evidence）：{evidence_links(item.evidence_ids)}</small></li>'
        for item in result.findings
    ) or "<li>没有发现问题。</li>"
    remediation_items = "".join(
        f'<li><strong>{e(item.finding_id)} - {e(item.action)}</strong><br>{e(item.rationale)}<br><small>修复成本（Cost）：{e(item.cost)} | 影响（Impact）：{e(item.impact)} | 预计提分（Estimated gain）：+{item.estimated_score_gain:.1f}</small></li>'
        for item in result.remediations
    ) or "<li>没有生成整改建议。</li>"
    top_actions = sorted(result.remediations, key=lambda item: item.estimated_score_gain, reverse=True)[:3]
    priority_items = "".join(
        f'<li><strong>+{item.estimated_score_gain:.1f}</strong> {e(item.action)}<br><small>{e(item.rationale)}</small></li>'
        for item in top_actions
    ) or "<li>No priority actions.</li>"
    probe_rows = "".join(
        f'<tr><td>{e(probe.name)}</td><td><span class="status {e(probe.status)}">{e(probe.status.upper())}</span></td><td>{e(probe.returncode if probe.returncode is not None else "-")}</td><td>{probe.duration_seconds:.3f}s</td><td><code>{e(probe.command.replace(chr(10), " ")[:180])}</code></td></tr>'
        for probe in result.probes
    ) or '<tr><td colspan="5">本次没有运行执行探测。</td></tr>'
    evidence_rows = "".join(
        f'<tr id="evidence-{e(item.id)}"><td><code>{e(item.id)}</code></td><td><strong class="evidence-kind-main">{e(evidence_type_label(item.kind))}</strong><br><code>{e(item.kind)}</code></td><td><code class="evidence-path">{e(item.path)}</code>{f":{item.line}" if item.line else ""}</td><td class="evidence-raw">{e(item.excerpt)}</td></tr>'
        for item in result.evidence
    ) or '<tr><td colspan="4">未提取到证据。</td></tr>'
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
.card .value.na {{ color: #8490a1; }}
.section-note {{ color: #5f6b7a; font-size: 13px; line-height: 1.65; margin: 8px 0 12px; }}
.section-note strong {{ color: #40506a; }}
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
.evidence-kind {{ color:#5f6b7a; font-size:10px; margin-left:4px; white-space:normal; }}
.evidence-kind-main {{ color:#40506a; font-size:12px; }}
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
.evidence-id-list .evidence-link {{ display: flex; flex-direction: column; align-items: flex-start; gap: 2px; max-width: 100%; padding: 4px 7px; border: 1px solid #d8e4f8; border-radius: 7px; background: #f4f8ff; }}
.evidence-id-list .evidence-kind {{ margin-left: 0; font-size: 10px; line-height: 1.25; }}
.evidence-id-list code {{ display: inline-block; padding: 0; border: 0; background: transparent; color: #2457d6; font-size: 12px; line-height: 1.2; white-space: nowrap; }}
.evidence-scroll {{ max-height: 72vh; overflow: auto; border-radius: 12px; scrollbar-gutter: stable; }}
.evidence-table {{ width: 1280px; min-width: 1280px; table-layout: fixed; border-collapse: separate; border-spacing: 0; overflow: visible; }}
.evidence-table th, .evidence-table td {{ box-sizing: border-box; background-clip: padding-box; vertical-align: top; }}
.evidence-table thead th {{ position: sticky; top: 0; z-index: 10; background: #eaf0fa; white-space: nowrap; }}
.evidence-table tbody td:first-child, .evidence-table thead th:first-child {{ position: sticky; left: 0; }}
.evidence-table tbody td:first-child {{ z-index: 5; background: #fff; box-shadow: 2px 0 6px rgba(23,32,51,.08); }}
.evidence-table thead th:first-child {{ z-index: 12; background: #eaf0fa; box-shadow: 2px 0 6px rgba(23,32,51,.08); }}
.evidence-table th:nth-child(1), .evidence-table td:nth-child(1) {{ width: 96px; white-space: nowrap; }}
.evidence-table th:nth-child(2), .evidence-table td:nth-child(2) {{ width: 185px; }}
.evidence-table th:nth-child(3), .evidence-table td:nth-child(3) {{ width: 365px; }}
.evidence-table th:nth-child(4), .evidence-table td:nth-child(4) {{ width: 634px; }}
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
.visual-section {{ margin: 26px 0 8px; padding: 24px; background: linear-gradient(135deg,#f8faff,#eef4ff); border: 1px solid #dce6f5; border-radius: 18px; }}
.visual-heading {{ display:flex; justify-content:space-between; align-items:flex-end; gap:14px; margin-bottom:18px; }}
.visual-heading h2 {{ margin:0; border:0; padding:0; font-size:24px; }}
.visual-heading p {{ margin:6px 0 0; color:#64748b; font-size:13px; }}
.visual-hint {{ color:#64748b; font-size:12px; }}
.visual-grid {{ display:grid; grid-template-columns:0.82fr 1.25fr 1fr; gap:14px; align-items:stretch; }}
.visual-card {{ background:rgba(255,255,255,.92); border:1px solid #e4ebf6; border-radius:14px; padding:16px; box-shadow:0 5px 18px rgba(23,32,51,.05); min-width:0; }}
.visual-title {{ color:#40506a; font-weight:800; font-size:14px; margin-bottom:12px; }}
.score-visual {{ display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.gauge {{ width:170px; height:170px; border-radius:50%; background:conic-gradient(#2457d6 var(--score-angle), #e5ecf8 0); display:grid; place-items:center; margin:6px auto 10px; }}
.gauge-inner {{ width:126px; height:126px; border-radius:50%; background:#fff; display:flex; flex-direction:column; align-items:center; justify-content:center; box-shadow:inset 0 0 0 1px #eef2f8; }}
.gauge-inner strong {{ font-size:38px; color:#2457d6; line-height:1; }}
.gauge-inner span {{ color:#8490a1; font-size:12px; margin-top:4px; }}
.gauge-caption {{ padding:6px 10px; border-radius:999px; background:#eef3fb; color:#31507a; font-size:12px; font-weight:800; }}
.radar-svg {{ width:100%; height:auto; display:block; overflow:visible; }}
.radar-grid {{ fill:none; stroke:#dce5f2; stroke-width:1; }}
.radar-axis {{ stroke:#e4ebf5; stroke-width:1; }}
.radar-area {{ fill:rgba(36,87,214,.18); stroke:#2457d6; stroke-width:2.2; }}
.radar-dot {{ fill:#2457d6; stroke:#fff; stroke-width:1.5; }}
.radar-label {{ fill:#526175; font-size:11px; font-family:"Microsoft YaHei",sans-serif; }}
.radar-na {{ fill:#8a98aa; font-size:10px; font-weight:700; }}
.visual-foot {{ color:#8490a1; font-size:11px; line-height:1.5; margin-top:8px; }}
.donut-row {{ display:flex; align-items:center; gap:18px; }}
.donut {{ width:138px; height:138px; border-radius:50%; display:grid; place-items:center; flex:0 0 138px; }}
.donut-hole {{ width:96px; height:96px; border-radius:50%; background:#fff; display:flex; flex-direction:column; align-items:center; justify-content:center; box-shadow:inset 0 0 0 1px #eef2f8; }}
.donut-hole strong {{ font-size:28px; color:#2457d6; line-height:1; }}
.donut-hole span {{ color:#8490a1; font-size:11px; margin-top:4px; }}
.legend {{ display:flex; flex-direction:column; gap:8px; min-width:0; }}
.legend-item {{ display:grid; grid-template-columns:10px 1fr auto; align-items:center; gap:7px; color:#526175; font-size:12px; }}
.legend-dot {{ width:9px; height:9px; border-radius:50%; }}
.legend-item strong {{ color:#172033; }}
.coverage-line {{ display:flex; justify-content:space-between; gap:10px; margin-top:18px; color:#526175; font-size:12px; }}
.coverage-line strong {{ color:#2457d6; }}
.coverage-track {{ height:8px; background:#e9eef7; border-radius:999px; overflow:hidden; margin-top:7px; }}
.coverage-track div {{ height:100%; border-radius:999px; background:linear-gradient(90deg,#2457d6,#0ea5e9); }}
.visual-empty {{ color:#8490a1; font-size:13px; }}
@media(max-width:980px) {{ .visual-grid {{ grid-template-columns:1fr 1fr; }} .claims-visual {{ grid-column:1/-1; }} }}
@media(max-width:620px) {{ .visual-section {{ padding:16px; }} .visual-grid {{ grid-template-columns:1fr; }} .claims-visual {{ grid-column:auto; }} .donut-row {{ align-items:flex-start; }} .visual-heading {{ display:block; }} .visual-hint {{ display:block; margin-top:8px; }} }}
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
<div class="score"><div><div class="big">{result.total_score:.1f}</div><div class="meta">out of 100</div></div><div><span class="badge">{e(result.readiness)}</span><p class="meta">开源 LLM/RAG/Agent 项目复现就绪度</p></div></div>
{visual_overview}
<h2>Evidence Overview（证据总览）</h2><p class="section-note"><strong>中文翻译：</strong>证据总览。<strong>简单解释：</strong>汇总证据覆盖率、README 声明数量和仍需补充证据的数量，先判断证据基础是否完整。</p><div class="cards summary">{summary_cards}</div>
<h2>Top 3 Priority Actions（三项优先整改行动）</h2><p class="section-note"><strong>中文翻译：</strong>三项优先整改行动。<strong>简单解释：</strong>按照预计提分从高到低，列出最值得先处理的三项修改。</p><ul class="priority">{priority_items}</ul>
<h2>Dimension Scores（维度评分）</h2><p class="section-note"><strong>中文翻译：</strong>维度评分。<strong>简单解释：</strong>展示六个复现维度的得分。显示 N/A 表示该维度没有适用检查项，不能用 0% 或 100% 代表好坏。</p><div class="cards">{dim_cards}</div>
<h2 id="criteria">Criteria（检查项）</h2><p class="section-note"><strong>中文翻译：</strong>检查项。<strong>简单解释：</strong>逐条列出检查要求、当前状态、得分、对应证据以及证据说明。</p><p class="table-help"><strong>读表说明：</strong>PASS = 满足要求；PARTIAL = 只有部分证据；MISSING = 应有但没有找到；N/A = 当前项目类型不适用。Confidence 表示证据支持强度，不代表项目整体质量。<br><strong>证据编号（E-xxx）</strong> = 本次报告中的证据序号，不是固定分类。例如 E-005 只表示本次报告的第 5 条证据，具体含义由编号后的中文类型、文件位置和原文共同决定；同一仓库重新分析后序号可能变化。点击可跳到证据附录。<br><strong>表格已固定首行和前两列，可在表格内滚动。</strong></p><div class="table-scroll sticky-scroll"><table class="criteria-table"><thead><tr><th>检查项编号</th><th>所属维度</th><th>检查要求</th><th>状态</th><th>证据强度</th><th>得分</th><th>证据编号<br>（E-xxx）</th><th>证据说明<br>（文件、行号、原文）</th></tr></thead><tbody>{criteria_rows}</tbody></table></div>
<h2 id="claims">Claim-Evidence Matrix（声明验证矩阵）</h2><p class="section-note"><strong>中文翻译：</strong>声明与证据矩阵。<strong>简单解释：</strong>检查 README 中声称具备的能力，是否能被仓库里的文件证据支持。</p><p class="table-help"><strong>读表方法：</strong>每一行先看 README 原句，再看验证状态、检查依据、缺口和支持证据。检查项编号后面的括号是中文含义。<br><strong>检查依据（需要检查的项）</strong> = 要验证这句话，必须检查哪些规则。<br><strong>还缺什么（缺口）</strong> = 直接说明缺少的文件、脚本、说明或记录；显示“-”表示没有缺口。<br><strong>已验证</strong> = 相关检查项全部通过；<strong>部分验证</strong> = 找到部分证据但仍有缺口；<strong>未验证</strong> = 关键证据缺失；<strong>不适用</strong> = 该声明对应的检查项不适用于此项目。<br><strong>表格已固定首行和前两列，可在表格内滚动。</strong></p><div class="table-scroll sticky-scroll"><table class="claim-table"><thead><tr><th>声明编号</th><th>README 声明</th><th>验证状态</th><th>检查依据<br>（需要检查的项）</th><th>还缺什么<br>（缺口）</th><th>支持证据</th><th>验证说明</th></tr></thead><tbody>{claim_rows}</tbody></table></div>
<h2 id="evidence">Evidence Appendix（证据附录）</h2><p class="section-note"><strong>中文翻译：</strong>证据附录。<strong>简单解释：</strong>集中保存证据编号、类型、文件位置和原文，方便评委或维护者人工复核。</p><p class="table-help"><strong>编号说明：</strong>E-xxx 只是本次报告内的顺序编号，每次扫描可能变化。真正的“意思”由“中文证据含义 + 文件位置 + 原文”共同确定。<br><strong>用途：</strong>这里保存每条证据的编号、中文含义、原始类型、文件位置和原文。表格固定首行和“证据编号”列，可横向、纵向滚动。</p><div class="evidence-scroll"><table class="evidence-table"><thead><tr><th>证据编号<br>（本次报告序号）</th><th>证据含义<br>（自动识别类型）</th><th>文件位置</th><th>原文摘录</th></tr></thead><tbody>{evidence_rows}</tbody></table></div>
<h2>Findings（问题发现）</h2><p class="section-note"><strong>中文翻译：</strong>问题发现。<strong>简单解释：</strong>列出当前检查中发现的主要缺口、风险等级和对应证据。</p><ul>{finding_items}</ul>
<h2>Execution Evidence（执行证据）</h2><p class="section-note"><strong>中文翻译：</strong>执行证据。<strong>简单解释：</strong>记录实际运行过的探测命令、结果和耗时；它只证明这些探测执行过，不代表整个项目已经复现成功。</p><table><thead><tr><th>Probe（探测项）</th><th>Status（状态）</th><th>Return code（返回码）</th><th>Duration（耗时）</th><th>Command（命令）</th></tr></thead><tbody>{probe_rows}</tbody></table>
<h2>Minimal Remediation Plan（最小整改计划）</h2><p class="section-note"><strong>中文翻译：</strong>最小整改计划。<strong>简单解释：</strong>给出成本较低、能够提高复现就绪度的修改建议，并估算预计提分。</p><ul>{remediation_items}</ul>
<h2>Scope and Limitations（适用范围与限制）</h2><p class="section-note"><strong>中文翻译：</strong>适用范围与限制。<strong>简单解释：</strong>说明本报告能证明什么、不能证明什么，避免把静态体检结果误解为完整复现成功。</p><ul><li>本报告执行的是静态复现就绪度分析，不等同于证明项目能够成功复现。</li><li>系统默认不会执行来自不可信仓库的代码。</li><li>只有使用 <code>--execute</code> 时，才会运行仓库中的探测脚本。</li><li>AI 生成的解释在正式发布前仍需要团队人工复核。</li></ul>
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
            kind_label = entry.get("kind_label") or evidence_type_label(entry.get("kind", ""))
            items.append(
                f'<div class="evidence-item"><a href="report.html#evidence-{e(entry["id"])}"><code>{e(entry["id"])}</code></a> '
                f'<span class="evidence-kind">类型：{e(kind_label)}</span> '
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
        f'<td>{e(format_gap_references(row.get("gaps", []), result.criteria))}</td>'
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
.evidence-kind {{ color:#5f6b7a; font-size:11px; margin-right:4px; }}
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
“支持证据”中的 E-xxx 是本次报告内的顺序编号，具体含义看后面的中文类型、文件名和原文。编号可以点击，跳转到完整报告中的证据位置。</div>
<h2>声明列表</h2>
<p class="guide"><strong>表格已固定首行和前两列</strong>，可在表格内横向和纵向滚动。点击 E-xxx 可查看完整报告中的证据原文。</p><div class="table-scroll sticky-scroll"><table class="claim-table"><thead><tr><th>声明编号</th><th>README 声明</th><th>验证状态</th><th>检查依据<br>（需要检查的项）</th><th>还缺什么<br>（缺口）</th><th>支持证据</th><th>验证说明</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>状态说明</h2>
<div class="guide"><strong>已验证</strong>：相关检查项全部通过，并且有证据支持。<br>
<strong>部分验证</strong>：找到部分证据，但仍有缺口。<br>
<strong>未验证</strong>：关键证据缺失，当前声明不能视为已验证。<br>
<strong>不适用</strong>：相关检查项不适用于当前项目类型，证据只作为识别线索。</div>
<a class="back" href="report.html">返回完整报告</a>
</main></body></html>'''

