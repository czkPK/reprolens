from __future__ import annotations

import hashlib
import os
from html import escape
from pathlib import Path
from urllib.parse import quote


def tree_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    ignored = {
        ".git", ".venv", "venv", "node_modules", "__pycache__",
        ".pytest_cache", ".mypy_cache", "dist", "build", "reports",
    }
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name not in ignored)
        for name in sorted(files):
            path = Path(current) / name
            rel = path.relative_to(root).as_posix()
            digest.update(rel.encode("utf-8"))
            digest.update(b"\0")
            try:
                digest.update(path.read_bytes())
            except OSError:
                digest.update(b"<unreadable>")
            digest.update(b"\0")
    return digest.hexdigest()


def write_autofix_html(report: dict, out_dir: Path) -> None:
    accepted_rows = "".join(
        f'<tr><td><a href="autofix/proposal/{quote(item["path"], safe="/")}"><code>{escape(item["path"])}</code></a></td><td>{escape(item["reason"])}</td></tr>'
        for item in report["generated_files"]
    ) or '<tr><td colspan="2">没有候选修改能够提高评分。</td></tr>'
    rejected_rows = "".join(
        f'<tr><td><code>{escape(item["path"])}</code></td><td>{escape(item["reason"])}</td></tr>'
        for item in report["rejected_files"]
    ) or '<tr><td colspan="2">没有被丢弃的候选修改。</td></tr>'
    fixed = "".join(f"<li><code>{escape(item)}</code></li>" for item in report["fixed_criteria"]) or "<li>无</li>"
    changed = "".join(f"<li><code>{escape(item)}</code></li>" for item in report["changed_criteria"]) or "<li>无</li>"
    remaining = "".join(f"<li><code>{escape(item)}</code></li>" for item in report["remaining_gaps"]) or "<li>无</li>"
    unchanged = bool(report.get("original_unchanged"))
    status_text = "原仓库未被修改" if unchanged else "检测到原仓库内容发生变化"
    status_class = "pass" if unchanged else "fail"
    fingerprint = escape(str(report.get("original_fingerprint", "-")))
    html = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ReproLens AutoFix 验证</title>
<style>
body {{ margin:0; background:#f4f7fc; color:#172033; font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif; }}
main {{ max-width:1120px; margin:0 auto; padding:38px 22px 70px; }}
h1 {{ margin:0 0 8px; font-size:32px; }}
h2 {{ margin-top:30px; border-bottom:1px solid #dbe4f0; padding-bottom:9px; }}
.meta {{ color:#64748b; line-height:1.7; }}
.cards {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:22px 0; }}
.card {{ background:#fff; border-radius:14px; padding:16px; box-shadow:0 5px 18px rgba(23,32,51,.07); }}
.label {{ color:#64748b; font-size:13px; }}
.value {{ color:#2457d6; font-size:30px; font-weight:800; margin:6px 0; }}
.verification {{ display:flex; align-items:center; gap:12px; padding:16px 18px; border-radius:12px; background:#eef8f2; border:1px solid #cfeada; }}
.verification.fail {{ background:#fff0f2; border-color:#f5c9d0; color:#9e1f31; }}
.check {{ display:inline-grid; place-items:center; width:28px; height:28px; border-radius:50%; background:#167a3a; color:#fff; font-weight:900; }}
.fail .check {{ background:#b42336; }}
.guide {{ background:#eef3fb; border:1px solid #dbe4f0; border-radius:14px; padding:16px 20px; line-height:1.8; }}
table {{ width:100%; border-collapse:separate; border-spacing:0; background:#fff; border-radius:14px; overflow:hidden; box-shadow:0 5px 18px rgba(23,32,51,.07); }}
th,td {{ padding:12px 14px; border-bottom:1px solid #edf1f7; text-align:left; vertical-align:top; font-size:13px; line-height:1.6; }}
th {{ background:#eaf0fa; color:#40506a; }}
code {{ background:#f1f4f9; border-radius:4px; padding:2px 5px; word-break:break-all; }}
.links a {{ display:inline-block; margin:6px 10px 0 0; padding:10px 13px; border-radius:10px; background:#eef3fb; color:#2457d6; text-decoration:none; font-weight:800; }}
.columns {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }}
.panel {{ background:#fff; border-radius:14px; padding:16px; box-shadow:0 5px 18px rgba(23,32,51,.07); }}
ul {{ margin:8px 0 0; padding-left:26px; line-height:1.8; }}
a {{ color:#2457d6; }}
@media(max-width:820px) {{ .cards,.columns {{ grid-template-columns:1fr 1fr; }} }}
@media(max-width:560px) {{ .cards,.columns {{ grid-template-columns:1fr; }} }}
</style>
</head>
<body><main>
<h1>AutoFix 验证报告</h1>
<div class="meta">生成时间：{escape(report["generated_at"])}</div>
<div class="cards">
  <div class="card"><div class="label">修改前</div><div class="value">{report["before_score"]:.1f}</div><div class="label">原始仓库评分</div></div>
  <div class="card"><div class="label">修改后</div><div class="value">{report["after_score"]:.1f}</div><div class="label">隔离副本复测评分</div></div>
  <div class="card"><div class="label">评分提升</div><div class="value">+{report["delta"]:.1f}</div><div class="label">只保留有效修改</div></div>
  <div class="card"><div class="label">保留文件</div><div class="value">{len(report["generated_files"])}</div><div class="label">丢弃 {len(report["rejected_files"])} 个无效候选</div></div>
</div>
<div class="verification {status_class}"><span class="check">{"✓" if unchanged else "!"}</span><div><strong>{status_text}</strong><br><span>原仓库内容指纹：<code>{fingerprint}</code></span></div></div>
<h2>AutoFix 做了什么</h2><div class="guide">
1. 只读取原始仓库，并在隔离副本中生成候选文件；<br>
2. 每加入一个候选文件，就重新扫描并计算评分；<br>
3. 只有在评分提高时才保留该文件，否则自动删除并记为“已丢弃”；<br>
4. 最后对全部保留文件共同作用后的副本重新评分，得到修改后分数。
</div>
<h2>实际保留的修改</h2><table><thead><tr><th>生成文件</th><th>解决的问题</th></tr></thead><tbody>{accepted_rows}</tbody></table>
<h2>被自动丢弃的候选修改</h2><table><thead><tr><th>候选文件</th><th>丢弃原因</th></tr></thead><tbody>{rejected_rows}</tbody></table>
<h2>检查项变化</h2><div class="columns"><div class="panel"><strong>变为通过</strong><ul>{fixed}</ul></div><div class="panel"><strong>状态发生变化</strong><ul>{changed}</ul></div><div class="panel"><strong>仍然存在的缺口</strong><ul>{remaining}</ul></div></div>
<h2>原始证据文件</h2><div class="links">
<a href="autofix/FIX_PROPOSAL.md">打开整改提案</a>
<a href="autofix/autofix.json">打开 AutoFix JSON</a>
<a href="autofix/remediation.patch">打开整改补丁</a>
<a href="report.html">返回完整审计报告</a>
</div>
<h2>验证结论</h2><div class="guide"><strong>可核验结果：</strong>修改前 {report["before_score"]:.1f} 分，隔离副本复测 {report["after_score"]:.1f} 分，提升 {report["delta"]:.1f} 分。原仓库内容指纹在 AutoFix 前后保持一致。生成文件中的 TODO 仍需要项目维护者补充，模板不会因此被判定为完全可复现。</div>
</main></body></html>'''
    (out_dir.parent / "autofix.html").write_text(html, encoding="utf-8")
