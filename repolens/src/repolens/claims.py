from __future__ import annotations

from .models import AuditResult, CriterionResult, Evidence


EVIDENCE_TYPE_LABELS = {
    "readme": "README 项目说明",
    "dependency-manifest": "依赖清单",
    "lockfile": "依赖版本锁定文件",
    "container": "容器配置文件",
    "model-card": "模型卡",
    "dataset-card": "数据集卡",
    "license": "项目许可证",
    "ci": "持续集成配置",
    "tests": "测试文件",
    "config": "配置文件",
    "script": "运行或处理脚本",
    "instruction": "安装或运行说明",
    "data": "数据文字说明",
    "data-source": "数据集获取链接",
    "data-command": "数据下载或加载命令",
    "data-license": "数据许可说明",
    "model": "模型名称或版本线索",
    "model-source": "模型权重或下载来源",
    "weights": "模型权重文件",
    "llm-provider": "LLM 服务提供方",
    "llm": "LLM 使用线索",
    "prompt": "提示词或模板",
    "llm-config": "LLM 配置参数",
    "rag": "RAG 检索配置",
    "evaluation": "评测与数据划分说明",
    "agent": "Agent 调用或轨迹线索",
    "claim": "README 能力声明",
    "metric": "性能指标",
    "determinism": "随机种子或确定性设置",
    "hardware": "硬件环境",
    "cost": "成本或性能信息",
}


def evidence_type_label(kind: str) -> str:
    return EVIDENCE_TYPE_LABELS.get(kind, "其他证据线索")


def _claim_criteria(text: str) -> list[str]:
    lower = text.lower()
    criteria: set[str] = set()
    if any(word in lower for word in ("accuracy", "f1", "bleu", "rouge", "psnr", "benchmark", "reproduce", "result")):
        criteria.update({"DATA-02", "MODEL-02", "EXP-02", "EXP-03", "EXP-05", "LLM-07"})
    if any(word in lower for word in ("model", "llm", "provider", "huggingface", "openai")):
        criteria.update({"MODEL-02", "LLM-01", "LLM-03"})
    if any(word in lower for word in ("rag", "retrieval", "embedding", "vector store", "index version", "knowledge base")):
        criteria.add("LLM-05")
    if any(word in lower for word in ("tool call", "tool calling", "function calling", "mcp", "trace", "trajectory")):
        criteria.add("LLM-06")
    if any(word in lower for word in ("install", "quickstart", "run", "usage", "pip install", "docker")):
        criteria.update({"ENV-01", "ENV-03", "DOC-02"})
    if any(word in lower for word in ("reproducible", "reproduction", "deterministic", "seed")):
        criteria.update({"ENV-02", "EXP-03", "DOC-03"})
    if not criteria:
        criteria.update({"DOC-02", "EXP-02", "DOC-03"})
    return sorted(criteria)


def claim_status(criteria: list[CriterionResult]) -> str:
    applicable = [item for item in criteria if item.applicable]
    if not applicable:
        return "not_applicable"
    states = {item.status for item in applicable}
    if states == {"pass"}:
        return "verified"
    if "missing" in states:
        return "unverified"
    if "partial" in states or "pass" in states:
        return "partially_verified"
    return "unverified"


def build_claim_matrix(result: AuditResult) -> list[dict]:
    by_id = {item.id: item for item in result.criteria}
    rows: list[dict] = []
    claims: list[Evidence] = [item for item in result.evidence if item.kind == "claim"][:8]
    for index, claim in enumerate(claims, 1):
        ids = _claim_criteria(claim.excerpt)
        criteria = [by_id[cid] for cid in ids if cid in by_id]
        gaps = [item.id for item in criteria if item.applicable and item.status in {"missing", "partial"}]
        evidence_ids: list[str] = []
        for item in criteria:
            for eid in item.evidence_ids:
                if eid not in evidence_ids:
                    evidence_ids.append(eid)
        rows.append(
            {
                "claim_id": f"C-{index:03d}",
                "source_evidence_id": claim.id,
                "claim": claim.excerpt,
                "criteria": [item.id for item in criteria],
                "status": claim_status(criteria),
                "gaps": gaps,
                "evidence_ids": evidence_ids,
            }
        )
    return rows


def criterion_confidence(item: CriterionResult) -> str:
    if item.status == "not_applicable":
        return "N/A"
    count = len(item.evidence_ids)
    if item.status == "pass" and count >= 2:
        return "high"
    if item.status in {"pass", "partial"} and count >= 1:
        return "medium"
    return "low"


def evidence_coverage(criteria: list[CriterionResult]) -> tuple[int, int, float]:
    applicable = [item for item in criteria if item.applicable]
    covered = sum(1 for item in applicable if item.evidence_ids)
    total = len(applicable)
    return covered, total, round(covered / total * 100, 1) if total else 0.0


def _project_label(project_type: str | None, model_agnostic: bool) -> str:
    labels = {
        "agent_framework": "模型无关的 Agent 框架",
        "sdk": "模型无关的 SDK",
        "memory_framework": "模型无关的记忆框架",
        "ml_project": "机器学习项目",
        "application": "AI 应用",
    }
    label = labels.get(project_type or "", "当前项目")
    if project_type == "application" and model_agnostic:
        return "模型无关的 AI 应用"
    return label


def _not_applicable_reason(item: CriterionResult, project_type: str | None, model_agnostic: bool) -> str:
    label = _project_label(project_type, model_agnostic)
    if project_type in {"agent_framework", "sdk", "memory_framework"} and item.id.startswith("MODEL-"):
        return f"这是一个{label}，自身不提供模型权重或模型卡，模型由外部提供方管理，因此不需要提供自有模型卡。"
    if project_type in {"agent_framework", "sdk", "memory_framework"} and item.id.startswith("DATA-"):
        return f"这是一个{label}，自身不拥有训练数据集，因此不需要提供项目自己的数据下载地址、预处理脚本或数据集卡。"
    if project_type in {"agent_framework", "sdk", "memory_framework"} and item.id == "EXP-03":
        return f"这是一个{label}，不训练固定模型，因此不需要设置训练随机种子。"
    if item.id == "LLM-05" and project_type in {"sdk", "agent_framework"}:
        return f"这是一个{label}，自身不维护固定的 RAG 索引或知识库，因此不需要提供索引版本。"
    if item.id == "LLM-06" and project_type in {"sdk", "memory_framework"}:
        return f"这是一个{label}，不是完整的 Agent 执行应用，因此不需要提供项目级 Agent 调用轨迹。"
    return f"这是一个{label}，不具备该检查项对应的项目产物，因此这项检查不适用。"


def evidence_explanation(item: CriterionResult, evidence: list[Evidence], project_type: str | None = None, model_agnostic: bool = False) -> str:
    by_id = {entry.id: entry for entry in evidence}
    if not item.applicable:
        if item.evidence_ids:
            ids = "、".join(item.evidence_ids)
            return _not_applicable_reason(item, project_type, model_agnostic) + f" 列出的 {ids} 只是判断项目类型时看到的识别线索。"
        return _not_applicable_reason(item, project_type, model_agnostic)
    if not item.evidence_ids:
        return "未找到可引用证据，因此该项不能判定为通过。"
    snippets: list[str] = []
    for evidence_id in item.evidence_ids:
        entry = by_id.get(evidence_id)
        if entry is None:
            continue
        location = f"{entry.path}:{entry.line}" if entry.line else entry.path
        excerpt = entry.excerpt.replace("\n", " ").strip()
        if len(excerpt) > 90:
            excerpt = excerpt[:87] + "..."
        snippets.append(f"{evidence_id}（{location}）：“{excerpt}”")
    if not snippets:
        return "证据编号存在，但未找到对应原文，需要人工复核。"
    prefix = "支持证据：" if item.status == "pass" else "部分证据："
    if item.status == "pass":
        suffix = "。"
    else:
        gap = item.note.strip().rstrip("。")
        suffix = f"；仍缺：{gap}。" if gap else "；仍缺：缺少足以满足该检查项的直接证据。"
    return prefix + "；".join(snippets) + suffix


def format_criterion_references(ids: list[str], criteria: list[CriterionResult]) -> str:
    by_id = {item.id: item.title for item in criteria}
    labels = [f"{criterion_id}（{by_id[criterion_id]}）" if criterion_id in by_id else criterion_id for criterion_id in ids]
    return "；".join(labels) if labels else "-"


def evidence_reference_entries(ids: list[str], evidence: list[Evidence], excerpt_limit: int = 90) -> list[dict[str, str]]:
    by_id = {entry.id: entry for entry in evidence}
    result: list[dict[str, str]] = []
    for evidence_id in ids:
        entry = by_id.get(evidence_id)
        if entry is None:
            result.append({
                "id": evidence_id,
                "kind": "unknown",
                "kind_label": "未知证据",
                "location": "未找到对应证据",
                "excerpt": "",
            })
            continue
        location = f"{entry.path}:{entry.line}" if entry.line else entry.path
        excerpt = entry.excerpt.replace("\n", " ").strip()
        if len(excerpt) > excerpt_limit:
            excerpt = excerpt[: excerpt_limit - 3] + "..."
        result.append({
            "id": evidence_id,
            "kind": entry.kind,
            "kind_label": evidence_type_label(entry.kind),
            "location": location,
            "excerpt": excerpt,
        })
    return result


def claim_verification_note(row: dict, criteria: list[CriterionResult] | None = None) -> str:
    status = str(row.get("status", ""))
    gaps = row.get("gaps", [])
    gap_text = format_criterion_references(gaps, criteria) if criteria else "、".join(gaps)
    if status == "verified":
        return "相关检查项均通过，这条 README 声明有证据支持。"
    if status == "partially_verified":
        return f"找到部分证据，但仍有缺口：{gap_text}。"
    if status == "unverified":
        return f"缺少关键证据，当前声明不能视为已验证；缺口：{gap_text}。"
    return "相关检查项不适用于当前项目类型，证据只作为识别线索。"
