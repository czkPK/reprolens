from __future__ import annotations

from .models import AuditResult, CriterionResult, Evidence


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
    for claim in claims:
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
                "claim_id": claim.id,
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


def evidence_explanation(item: CriterionResult, evidence: list[Evidence]) -> str:
    by_id = {entry.id: entry for entry in evidence}
    if not item.applicable:
        if item.evidence_ids:
            return "该项不适用于当前项目类型；列出的证据只用于说明识别线索，不参与评分。"
        return "该项不适用于当前项目类型，不需要提供证据。"
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
    suffix = "。" if item.status == "pass" else "；现有证据不足以完全满足该项。"
    return prefix + "；".join(snippets) + suffix
