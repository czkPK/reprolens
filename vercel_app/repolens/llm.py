from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

from .claims import build_claim_matrix, evidence_coverage
from .models import AuditResult


def build_evidence_context(result: AuditResult) -> str:
    lines = [
        f"Repository: {result.repo_path}",
        f"Score: {result.total_score}/100 ({result.readiness})",
        "Criteria:",
    ]
    for item in result.criteria:
        lines.append(
            f"- {item.id} | {item.dimension} | {item.title} | {item.status} | evidence={','.join(item.evidence_ids) or 'none'} | {item.note}"
        )
    claims = result.claim_matrix or build_claim_matrix(result)
    lines.append("Claims:")
    for row in claims:
        lines.append(
            f"- {row['claim_id']} | {row['status']} | criteria={','.join(row['criteria']) or 'none'} | gaps={','.join(row['gaps']) or 'none'} | evidence={','.join(row['evidence_ids']) or 'none'} | {row['claim']}"
        )
    lines.append("Evidence:")
    for evidence in result.evidence:
        location = f"{evidence.path}:{evidence.line}" if evidence.line else evidence.path
        lines.append(f"- {evidence.id} | {location} | {evidence.excerpt}")
    lines.append("Findings:")
    for finding in result.findings:
        lines.append(f"- {finding.id} | {finding.severity} | {finding.criterion_id} | {finding.message}")
    return "\n".join(lines)


def offline_explanation(result: AuditResult) -> str:
    gaps = [item for item in result.criteria if item.status in {"missing", "partial"} and item.applicable]
    gaps.sort(key=lambda item: (item.status != "missing", -item.max_points))
    claims = result.claim_matrix or build_claim_matrix(result)
    covered, total, percent = evidence_coverage(result.criteria)
    claim_labels = {
        "verified": "已验证",
        "partially_verified": "部分验证",
        "unverified": "未验证",
        "not_applicable": "不适用",
    }
    lines = [
        "# ReproLens Explanation",
        "",
        f"当前复现就绪度为 **{result.total_score:.1f}/100（{result.readiness}）**。",
        f"证据覆盖率为 **{covered}/{total}（{percent:.1f}%）**，共抽取 **{len(claims)}** 条 README 声明。",
        "",
        "以下结论只基于仓库中已抽取到的证据，没有证据的内容不会被当作已验证事实。",
        "",
        "## 声明验证",
        "",
    ]
    if not claims:
        lines.append("- 未从根 README 抽取到可验证声明。")
    for row in claims[:8]:
        status = claim_labels.get(row["status"], row["status"])
        gaps_text = "、".join(row["gaps"]) if row["gaps"] else "无"
        lines.append(f"- `{row['claim_id']}` [{status}] {row['claim']}（缺口：{gaps_text}）")
    lines.extend([
        "",
        "## 主要缺口",
        "",
    ])
    if not gaps:
        lines.append("- 当前检查范围内没有发现明显缺口。")
    for item in gaps[:8]:
        evidence = ", ".join(item.evidence_ids) if item.evidence_ids else "无"
        lines.append(f"- `{item.id}` {item.title}：{item.note}（证据：{evidence}）")
    lines.extend(["", "## 优先整改", ""])
    for item in result.remediations[:8]:
        lines.append(f"- {item.action}：预计提升 +{item.estimated_score_gain:.1f}，理由：{item.rationale}")
    lines.extend(
        [
            "",
            "## 证据边界",
            "",
            "本说明没有补全缺失事实；如果证据不足，ReproLens 会保留 `Evidence Missing`，而不是猜测。",
        ]
    )
    return "\n".join(lines) + "\n"


def generate_explanation(result: AuditResult) -> str:
    base_url = os.getenv("REPROLENS_LLM_BASE_URL", "").strip()
    api_key = os.getenv("REPROLENS_LLM_API_KEY", "").strip()
    model = os.getenv("REPROLENS_LLM_MODEL", "").strip()
    if not base_url or not api_key or not model:
        return offline_explanation(result)

    context = build_evidence_context(result)
    prompt = (
        "你是源码复现审计助手。只能依据下面的证据写解释，不得补充未出现的事实。"
        "每条结论必须引用 E-xxx 证据 ID；没有证据时明确写 Evidence Missing。\n\n"
        + context
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You explain only evidence-backed reproduction findings."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
    }
    request = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        return "# ReproLens Explanation\n\n" + content.strip() + "\n"
    except Exception as exc:
        return offline_explanation(result) + f"\n> LLM 调用失败，已回退到离线模板：{type(exc).__name__}\n"


def write_explanation(result: AuditResult, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "explanation.md"
    path.write_text(generate_explanation(result), encoding="utf-8")
    return path
