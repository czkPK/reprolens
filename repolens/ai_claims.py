from __future__ import annotations

import json
import os
import re
import urllib.request
from typing import Any

from .claims import build_claim_matrix, claim_status
from .models import AuditResult


def _config() -> tuple[str, str, str] | None:
    base_url = os.getenv("REPROLENS_LLM_BASE_URL", "").strip()
    api_key = os.getenv("REPROLENS_LLM_API_KEY", "").strip()
    model = os.getenv("REPROLENS_LLM_MODEL", "").strip()
    if base_url and api_key and model:
        return base_url.rstrip("/"), api_key, model
    return None


def _extract_json(text: str) -> Any:
    cleaned = text.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)```", cleaned, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        cleaned = fenced.group(1).strip()
    start = min((index for index in (cleaned.find("["), cleaned.find("{")) if index >= 0), default=-1)
    if start >= 0:
        cleaned = cleaned[start:]
    return json.loads(cleaned)


def _call_llm(base_url: str, api_key: str, model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You map repository claims to audit criteria. Return JSON only. Never invent evidence IDs.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
    }
    request = urllib.request.Request(
        base_url + "/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
    return str(data["choices"][0]["message"]["content"])


def validate_ai_rows(raw: Any, result: AuditResult, rules: list[dict]) -> list[dict]:
    if not isinstance(raw, list):
        raise ValueError("AI response must be a JSON array")
    by_claim = {row["claim_id"]: row for row in rules}
    by_criterion = {item.id: item for item in result.criteria}
    enhanced: dict[str, dict] = {}
    for item in raw:
        if not isinstance(item, dict):
            continue
        claim_id = str(item.get("claim_id", ""))
        if claim_id not in by_claim or claim_id in enhanced:
            continue
        criterion_ids: list[str] = []
        for value in item.get("criterion_ids", []):
            criterion_id = str(value)
            if criterion_id in by_criterion and criterion_id not in criterion_ids:
                criterion_ids.append(criterion_id)
        if not criterion_ids:
            continue
        criteria = [by_criterion[criterion_id] for criterion_id in criterion_ids]
        evidence_ids: list[str] = []
        for criterion in criteria:
            for evidence_id in criterion.evidence_ids:
                if evidence_id not in evidence_ids:
                    evidence_ids.append(evidence_id)
        confidence = str(item.get("confidence", "medium")).lower()
        if confidence not in {"high", "medium", "low"}:
            confidence = "medium"
        enhanced[claim_id] = {
            **by_claim[claim_id],
            "criteria": criterion_ids,
            "status": claim_status(criteria),
            "gaps": [criterion.id for criterion in criteria if criterion.applicable and criterion.status in {"missing", "partial"}],
            "evidence_ids": evidence_ids,
            "reason": str(item.get("reason", ""))[:500],
            "confidence": confidence,
            "ai_assisted": True,
        }
    return [enhanced.get(row["claim_id"], row) for row in rules]


def enhance_claim_matrix(result: AuditResult, enabled: bool = True) -> tuple[list[dict], dict]:
    rules = result.claim_matrix or build_claim_matrix(result)
    if not enabled:
        return rules, {"mode": "rules", "enabled": False, "reason": "AI review not requested"}
    config = _config()
    if config is None:
        return rules, {
            "mode": "rules-fallback",
            "enabled": False,
            "reason": "LLM environment variables are not configured",
        }
    if not rules:
        return rules, {"mode": "llm", "enabled": True, "claims_enhanced": 0}

    base_url, api_key, model = config
    criterion_catalog = [
        {
            "id": item.id,
            "title": item.title,
            "status": item.status,
            "applicable": item.applicable,
            "evidence_ids": item.evidence_ids,
        }
        for item in result.criteria
    ]
    prompt = json.dumps(
        {
            "task": "Map each repository claim to the smallest set of audit criteria that could verify it.",
            "rules": [
                "Use only criterion IDs from the catalog.",
                "Do not invent evidence IDs or facts.",
                "A product description alone is not evidence for a technical claim.",
                "Return a JSON array with claim_id, criterion_ids, confidence, reason.",
            ],
            "criteria": criterion_catalog,
            "claims": rules,
        },
        ensure_ascii=False,
    )
    try:
        content = _call_llm(base_url, api_key, model, prompt)
        enhanced = validate_ai_rows(_extract_json(content), result, rules)
        count = sum(1 for row in enhanced if row.get("ai_assisted"))
        return enhanced, {
            "mode": "llm-assisted",
            "enabled": True,
            "model": model,
            "claims_enhanced": count,
            "validation": "criterion and evidence IDs are checked against repository evidence",
        }
    except Exception as exc:
        return rules, {
            "mode": "rules-fallback",
            "enabled": True,
            "reason": type(exc).__name__,
            "error": str(exc)[:300],
        }
