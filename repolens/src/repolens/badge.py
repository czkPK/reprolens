from __future__ import annotations

from html import escape

from .models import AuditResult


def badge_color(score: float) -> str:
    if score >= 85:
        return "#0f8a5f"
    if score >= 65:
        return "#2457d6"
    if score >= 40:
        return "#b66a06"
    return "#b42336"


def badge_payload(result: AuditResult) -> dict:
    return {
        "schemaVersion": 1,
        "label": "ReproLens",
        "message": f"{result.total_score:.1f}/100 {result.readiness}",
        "color": badge_color(result.total_score),
        "score": result.total_score,
        "readiness": result.readiness,
        "evidence_coverage": result.evidence_coverage,
        "source_url": result.source_url,
        "source_commit": result.source_commit,
        "generated_at": result.generated_at,
    }


def render_badge_svg(result: AuditResult) -> str:
    payload = badge_payload(result)
    label_width = 105
    message_width = 205
    width = label_width + message_width
    label = escape(payload["label"])
    message = escape(payload["message"])
    color = payload["color"]
    aria = escape(f"ReproLens: {payload['message']}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" role="img" aria-label="{aria}">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#ffffff" stop-opacity=".18"/>
    <stop offset="1" stop-color="#000000" stop-opacity=".08"/>
  </linearGradient>
  <rect width="{width}" height="28" rx="6" fill="#1f2937"/>
  <rect x="{label_width}" width="{message_width}" height="28" rx="6" fill="{color}"/>
  <rect width="{width}" height="28" rx="6" fill="url(#s)"/>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,DejaVu Sans,sans-serif" font-size="11">
    <text x="{label_width / 2:.1f}" y="18" font-weight="700">{label}</text>
    <text x="{label_width + message_width / 2:.1f}" y="18" font-weight="700">{message}</text>
  </g>
</svg>
'''

def render_badge_page(result: AuditResult) -> str:
    payload = badge_payload(result)
    coverage = payload.get("evidence_coverage") or {}
    source = payload.get("source_url") or result.repo_path
    commit = str(payload.get("source_commit") or "-")[:12]
    score = float(payload.get("score") or 0)
    percent = float(coverage.get("percent") or 0)
    covered = coverage.get("covered", 0)
    total = coverage.get("total", 0)
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ReproLens 复现徽章</title>
<style>
body {{ margin:0; background:#f4f7fc; color:#172033; font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif; }}
main {{ max-width:980px; margin:0 auto; padding:40px 22px 70px; }}
h1 {{ margin:0 0 8px; font-size:32px; }}
h2 {{ margin-top:30px; border-bottom:1px solid #dbe4f0; padding-bottom:9px; }}
.meta {{ color:#64748b; line-height:1.7; word-break:break-all; }}
.hero {{ background:#fff; border-radius:18px; padding:28px; margin:22px 0; box-shadow:0 8px 26px rgba(23,32,51,.08); }}
.badge-preview {{ display:inline-block; padding:14px 18px; border-radius:12px; background:#f8faff; border:1px solid #e2e9f4; }}
.badge-preview img {{ display:block; width:310px; max-width:100%; height:28px; }}
.badge-preview:hover {{ border-color:#b9caeb; }}
.cards {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:20px; }}
.card {{ background:#fff; border-radius:14px; padding:16px; box-shadow:0 5px 18px rgba(23,32,51,.07); }}
.label {{ color:#64748b; font-size:13px; }} .value {{ color:#2457d6; font-size:25px; font-weight:800; margin:6px 0; }}
.guide {{ background:#eef3fb; border:1px solid #dbe4f0; border-radius:14px; padding:16px 20px; line-height:1.8; }}
.codebox {{ position:relative; margin-top:14px; }}
pre {{ margin:0; padding:18px 120px 18px 18px; border-radius:12px; background:#172033; color:#eaf0fa; overflow:auto; line-height:1.6; }}
button {{ position:absolute; right:12px; top:12px; border:0; border-radius:8px; padding:8px 12px; background:#2457d6; color:#fff; font-weight:800; cursor:pointer; }}
.links a {{ display:inline-block; margin:8px 10px 0 0; padding:10px 13px; border-radius:10px; background:#eef3fb; color:#2457d6; text-decoration:none; font-weight:800; }}
a {{ color:#2457d6; }}
.small {{ color:#64748b; font-size:13px; line-height:1.7; }}
@media(max-width:760px) {{ .cards {{ grid-template-columns:1fr 1fr; }} }} @media(max-width:480px) {{ .cards {{ grid-template-columns:1fr; }} }}
</style>
</head>
<body><main>
<h1>ReproLens 复现徽章</h1>
<div class="meta">这是绑定到具体 commit 的复现体检快照，不代表项目已经通过运行验证。<br>对象：{escape(source)}<br>Commit：<code>{escape(commit)}</code></div>
<div class="hero">
  <a class="badge-preview" href="report.html" title="点击打开完整复现报告"><img src="badge.svg" alt="ReproLens {score:.1f}/100 {escape(payload['readiness'])}"></a>
  <p class="small">点击徽章可以直接打开完整报告。</p>
  <div class="cards">
    <div class="card"><div class="label">综合评分</div><div class="value">{score:.1f}</div><div class="label">满分 100</div></div>
    <div class="card"><div class="label">复现就绪度</div><div class="value">{escape(payload['readiness'])}</div><div class="label">当前结论</div></div>
    <div class="card"><div class="label">证据覆盖率</div><div class="value">{percent:.1f}%</div><div class="label">{covered}/{total} 个适用检查项</div></div>
    <div class="card"><div class="label">生成日期</div><div class="value" style="font-size:17px">{escape(str(payload.get('generated_at', '-'))[:10])}</div><div class="label">可追溯到生成时间</div></div>
  </div>
</div>
<h2>徽章有什么作用</h2><div class="guide">
它把项目的复现评分、就绪度和证据覆盖率压缩成一张 README 徽章。读者可以点击徽章回到完整报告，查看每一项证据、缺口和整改建议。徽章是“可追溯的审计快照”，不是“项目一定能够复现”的保证。
</div>
<h2>放到 GitHub README</h2><div class="guide">把下面代码加入 README。公网部署或静态文件上传后，徽章图片和报告链接会一起生效。<div class="codebox"><pre id="markdown-code">[![ReproLens](badge.svg)](report.html)</pre><button id="copy-code">复制代码</button></div></div>
<h2>验证与下载</h2><div class="links">
<a href="report.html">打开完整报告</a>
<a href="claims.html">打开声明矩阵</a>
<a href="score.json">打开评分 JSON</a>
<a href="badge.svg" download>下载 SVG 徽章</a>
<a href="badge.json" download>下载徽章 JSON</a>
</div>
<p class="small">嵌入代码会根据当前页面地址自动生成公网版本。重新审计后，应使用新提交对应报告中的徽章，避免把旧分数用于新版本。</p>
<script>
const base = location.href.replace(/badge\\.html(?:[?#].*)?$/, '');
document.getElementById('markdown-code').textContent = '[![ReproLens](' + base + 'badge.svg)](' + base + 'report.html)';
document.getElementById('copy-code').addEventListener('click', async () => {{
  const button = document.getElementById('copy-code');
  try {{
    await navigator.clipboard.writeText(document.getElementById('markdown-code').textContent);
    button.textContent = '已复制';
    setTimeout(() => button.textContent = '复制代码', 1400);
  }} catch (error) {{
    button.textContent = '请手动复制';
  }}
}});
</script>
</main></body></html>'''
