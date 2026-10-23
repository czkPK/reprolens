from __future__ import annotations

import html
import json
from pathlib import Path


STATUS_LABELS = {
    "pass": "通过",
    "partial": "部分通过",
    "missing": "缺失",
    "not_applicable": "不适用",
}
REPO_URLS = {
    "openai-python": "https://github.com/openai/openai-python",
    "smolagents": "https://github.com/huggingface/smolagents",
    "mem0": "https://github.com/mem0ai/mem0",
}

STATUS_CLASS = {
    "pass": "pass",
    "partial": "partial",
    "missing": "missing",
    "not_applicable": "na",
}


def main() -> int:
    base = Path(__file__).resolve().parents[1]
    labels_dir = base / "benchmark" / "labels"
    out_path = base.parent / "docs" / "人工标注抽查表.html"
    labels = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(labels_dir.glob("*.json"))]

    sections: list[str] = []
    for label in labels:
        counts = {key: 0 for key in STATUS_LABELS}
        for item in label["criteria"]:
            counts[item["expected_status"]] = counts.get(item["expected_status"], 0) + 1
        summary = "，".join(f"{STATUS_LABELS.get(k, k)} {v}" for k, v in counts.items() if v)
        rows = []
        for item in label["criteria"]:
            path = item.get("evidence_path") or "-"
            line = item.get("evidence_line")
            location = f"{path}:{line}" if line else path
            repo_url = REPO_URLS.get(label["repo"])
            if repo_url and path != "-":
                suffix = f"#L{line}" if line else ""
                evidence_html = f"<a target='_blank' href='{html.escape(repo_url + '/blob/main/' + path + suffix)}'>{html.escape(location)}</a>"
            else:
                evidence_html = f"<code>{html.escape(location)}</code>"
            rows.append(
                "<tr>"
                f"<td><code>{html.escape(item['criterion_id'])}</code></td>"
                f"<td><span class='status {STATUS_CLASS.get(item['expected_status'], '')}'>{html.escape(STATUS_LABELS.get(item['expected_status'], item['expected_status']))}</span></td>"
                f"<td>{evidence_html}</td>"
                f"<td>{html.escape(item.get('rationale', ''))}</td>"
                f"<td>{html.escape(item.get('confidence', ''))}</td>"
                "<td><label><input type='checkbox'> 同意</label><br><label><input type='checkbox'> 不同意</label></td>"
                "</tr>"
            )
        sections.append(
            f"<section><h2>{html.escape(label['repo'])} <small>{html.escape(label.get('project_type', ''))}</small></h2>"
            f"<p class='summary'>{html.escape(summary)}</p>"
            "<table><thead><tr><th>检查项</th><th>我的标注</th><th>证据位置</th><th>为什么这样标</th><th>置信度</th><th>你的复核</th></tr></thead><tbody>"
            + "".join(rows)
            + "</tbody></table></section>"
        )

    page = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ReproLens 人工标注抽查表</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f5f7fb;color:#172033;margin:0;padding:28px}}
main{{max-width:1300px;margin:0 auto}}h1{{margin:0 0 8px}}h2{{margin-top:30px}}small{{color:#697386;font-weight:400}}
.notice{{background:#fff;border-left:4px solid #2457d6;padding:14px 18px;border-radius:8px;line-height:1.7}}
.summary{{color:#4b5b73}}table{{width:100%;border-collapse:collapse;background:#fff;box-shadow:0 4px 14px rgba(23,32,51,.06);border-radius:10px;overflow:hidden}}
th,td{{padding:10px;border-bottom:1px solid #edf1f7;text-align:left;vertical-align:top;font-size:13px}}th{{background:#eef3fb}}
.status{{padding:3px 8px;border-radius:999px;font-size:12px;font-weight:700;white-space:nowrap}}.status.pass{{background:#e4f7ec;color:#167a3a}}
.status.partial{{background:#fff4db;color:#9a6500}}.status.missing{{background:#ffe5e8;color:#b42336}}.status.na{{background:#edf0f4;color:#697386}}
code{{background:#f1f4f9;padding:2px 5px;border-radius:4px;word-break:break-all}}label{{white-space:nowrap;font-size:12px}}
</style></head><body><main>
<h1>ReproLens 人工标注抽查表</h1>
<div class="notice"><strong>你不需要全部看。</strong>只需从下面三个仓库里挑 10—15 条，重点看“为什么这样标”和“证据位置”。如果证据支持这个状态，就勾“同意”；如果判断不合理，就勾“不同意”并在旁边写下原因。</div>
<p><strong>状态说明：</strong>通过 = 有明确可核验证据；部分通过 = 有部分证据但不完整；缺失 = 适用检查项没有证据；不适用 = 项目类型不需要该产物。</p>
{''.join(sections)}
</main></body></html>"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page, encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
